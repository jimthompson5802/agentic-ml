"""Resolve semantic configuration from independently verified planning evidence."""

import hashlib
from copy import deepcopy
from dataclasses import replace
from importlib.metadata import PackageNotFoundError, distribution, version
from pathlib import Path
from typing import cast

from agentic_ml.planning import PlanningError, inspect_plan, verify_plan
from agentic_ml.planning.models import Diagnostic, JSONValue
from agentic_ml.planning.parsing import InputError, mapping, sequence, strict_yaml
from agentic_ml.planning.paths import ProjectAccess, relative_path
from agentic_ml.validation.checks import digest, reject
from agentic_ml.validation.domains import check_space
from agentic_ml.validation.models import (
    ConfigurationRequest,
    ConfigurationResult,
    ValidationError,
    ValidationInspection,
)
from agentic_ml.validation.registry import validate_registry


def harness_identity() -> dict[str, JSONValue]:
    """Observe installed harness identity without importing training libraries."""
    package = distribution("agentic-ml")
    text = package.read_text("direct_url.json")
    import json

    origin: JSONValue = (
        cast(JSONValue, json.loads(text))
        if text
        else {"kind": "wheel", "distribution": "agentic-ml"}
    )
    return {"version": package.version, "origin": origin}


def library_version(name: str) -> str | None:
    """Record missing libraries explicitly without importing their code."""
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def derive(
    access: ProjectAccess, plan_id: str, registry_path: str | None
) -> tuple[dict[str, JSONValue], dict[str, JSONValue], bytes | None]:
    """Verify current inputs and derive one immutable semantic configuration."""
    verified = verify_plan(
        project_root=access.root, plan_id=plan_id, check_current=True
    )
    if not verified.integrity or verified.status != "input_ready":
        raise InputError(verified.diagnostics[0])
    inspected = inspect_plan(project_root=access.root, plan_id=plan_id)
    if inspected.status != "input_ready" or inspected.plan is None:
        raise InputError(inspected.diagnostics[0])
    plan = inspected.plan
    for raw in sequence(plan["inputs"]):
        entry = mapping(raw)
        content = access.read(str(entry["path"]))
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            reject(
                "stale_validation",
                str(entry["path"]),
                "Revalidate current project inputs.",
            )
    source = None
    declarations = None
    if registry_path is not None:
        source = access.read(registry_path)
        raw, _ = strict_yaml(source, registry_path)
        if not isinstance(raw, dict):
            reject("invalid_registry", "", "Supply a registry mapping.", registry_path)
        declarations = raw
    result = validate_registry(declarations)
    if result.registry is None:
        raise InputError(result.diagnostics[0])
    registry = result.registry
    task = mapping(mapping(plan["effective"])["data"])["task_type"]
    specs = {
        str(mapping(item)["id"]): mapping(item)
        for item in sequence(registry["algorithms"])
    }
    for boundary in ("declared_search", "effective_search"):
        for name, raw in sorted(mapping(mapping(plan[boundary])["algorithms"]).items()):
            spec = specs.get(name)
            if spec is None:
                reject(
                    "unknown_algorithm",
                    "algorithms." + name,
                    "Select a registered algorithm or supply explicit metadata.",
                )
            try:
                check_space(mapping(raw), spec, task, "algorithms." + name)
            except InputError as error:
                source_path = next(
                    str(mapping(item)["path"])
                    for item in sequence(plan["inputs"])
                    if mapping(item)["name"] == "search-space.yaml"
                )
                _, marks = strict_yaml(access.read(source_path), source_path)
                field = error.diagnostic.field
                mark = marks.get(field)
                if mark is None:
                    alternate = field.replace(".fixed.", ".search.")
                    mark = marks.get(alternate)
                if mark is None:
                    field_parent = field
                    while mark is None and "." in field_parent:
                        field_parent = field_parent.rsplit(".", 1)[0]
                        mark = marks.get(field_parent)
                diagnostic = replace(
                    error.diagnostic,
                    source_path=source_path,
                    line=None if mark is None else mark[0],
                    column=None if mark is None else mark[1],
                )
                raise InputError(diagnostic) from error
    effective: dict[str, JSONValue] = {}
    for name, raw in sorted(
        mapping(mapping(plan["effective_search"])["algorithms"]).items()
    ):
        space = mapping(raw)
        spec = specs.get(name)
        if spec is None:
            reject(
                "unknown_algorithm",
                "algorithms." + name,
                "Select a registered algorithm or supply explicit metadata.",
            )
        fixed, search = mapping(space["fixed"]), mapping(space["search"])
        defaults = {
            key: deepcopy(mapping(value)["default"])
            for key, value in mapping(spec["parameters"]).items()
            if key not in fixed and key not in search
        }
        effective[name] = {
            "task": task,
            "adapter": deepcopy(spec["adapter"]),
            "library_distribution": mapping(spec["library"])["distribution"],
            "fixed": deepcopy(fixed),
            "defaults": defaults,
            "search": deepcopy(search),
        }
    libraries: list[JSONValue] = []
    library_specs = {
        digest(mapping(specs[name]["library"])): mapping(specs[name]["library"])
        for name in effective
    }
    for lib in sorted(
        library_specs.values(),
        key=lambda x: (str(x["distribution"]), str(x["reference_version"])),
    ):
        libraries.append(
            {**lib, "installed_version": library_version(str(lib["distribution"]))}
        )
    current_harness = harness_identity()
    if current_harness != plan["harness"]:
        reject(
            "stale_validation",
            "harness",
            "Resolve a new plan for the current harness identity.",
        )
    config: dict[str, JSONValue] = {
        "schema_version": "1.0",
        "project_root": str(access.root),
        "experiment_id": plan["experiment_id"],
        "plan_id": plan_id,
        "registry_id": result.registry_id,
        "registry_source": None
        if source is None
        else {"path": registry_path, "sha256": hashlib.sha256(source).hexdigest()},
        "harness": current_harness,
        "libraries": libraries,
        "algorithms": effective,
        "capabilities": ["configuration_validation", "candidate_validation"],
        "execution_authorized": False,
    }
    access.recheck()
    return config, registry, source


def validate_configuration(request: ConfigurationRequest) -> ConfigurationResult:
    """Validate and preserve current semantic inputs without authorizing execution."""
    from agentic_ml.validation.storage import publish

    access: ProjectAccess | None = None
    try:
        access = ProjectAccess(request.project_root)
        selected = (
            None if request.registry is None else relative_path(str(request.registry))
        )
        config, registry, source = derive(access, request.plan_id, selected)
        validation_id = publish(access, config, registry, source)
        access.recheck()
        final, _, _ = derive(access, request.plan_id, selected)
        if digest(final) != digest(config):
            reject(
                "stale_validation", "inputs", "Revalidate changed inputs explicitly."
            )
        return ConfigurationResult("valid", validation_id, config)
    except InputError as error:
        return ConfigurationResult("blocked", None, None, (error.diagnostic,))
    except PlanningError as error:
        raise ValidationError(error.code, str(error)) from error
    except OSError as error:
        raise ValidationError(
            "validation_io", "Unable to access validation inputs or storage."
        ) from error
    finally:
        if access is not None:
            access.close()


def inspect_validation(
    *, project_root: Path, validation_id: str
) -> ValidationInspection:
    """Independently rederive evidence integrity and current semantic inputs."""
    from agentic_ml.validation.storage import read_bundle

    access: ProjectAccess | None = None
    config: dict[str, JSONValue] | None = None
    intact = False
    try:
        access = ProjectAccess(project_root)
        config, registry, source = read_bundle(access, validation_id)
        intact = True
        selected = config["registry_source"]
        path = None if selected is None else str(mapping(selected)["path"])
        current, current_registry, current_source = derive(
            access, str(config["plan_id"]), path
        )
        if (
            digest(current) != digest(config)
            or digest(registry) != digest(current_registry)
            or source != current_source
        ):
            reject(
                "stale_validation",
                "inputs",
                "Revalidate current inputs and library observations explicitly.",
            )
        access.recheck()
        return ValidationInspection("valid", validation_id, config, (), True, True)
    except InputError as error:
        return ValidationInspection(
            "blocked", validation_id, config, (error.diagnostic,), intact, False
        )
    except (FileNotFoundError, NotADirectoryError, ValueError, TypeError, KeyError):
        diagnostic = Diagnostic(
            "invalid_validation",
            "validation_id",
            "",
            None,
            None,
            "Restore intact evidence for this validation identity.",
        )
        return ValidationInspection(
            "blocked", validation_id, config, (diagnostic,), False, False
        )
    except PlanningError as error:
        raise ValidationError(error.code, str(error)) from error
    except OSError as error:
        raise ValidationError(
            "validation_io", "Unable to access preserved validation evidence."
        ) from error
    finally:
        if access is not None:
            access.close()
