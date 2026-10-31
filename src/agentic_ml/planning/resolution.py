"""Resolve declarative experiment inputs into preserved plans."""

import hashlib
import json
import stat
from importlib.metadata import distribution
from importlib.resources import files
from pathlib import Path
from typing import cast

from jsonschema import Draft202012Validator

from agentic_ml.planning.models import (
    Diagnostic,
    JSONValue,
    PlanInspection,
    PlanningError,
    PlanResult,
    ResolveRequest,
    VerificationResult,
)
from agentic_ml.planning.parsing import (
    InputError,
    derive_decisions,
    fail,
    mapping,
    parse_brief,
    sequence,
    strict_yaml,
    validate,
)
from agentic_ml.planning.paths import ProjectAccess, data_reference, relative_path
from agentic_ml.planning.storage import canonical, publish


def prepare(
    access: ProjectAccess,
    experiment: str,
    sources: dict[str, bytes],
    *,
    preserved: bool = False,
) -> dict[str, JSONValue]:
    """Validate selected source bytes and derive reviewable scientific decisions."""
    marker = None if preserved else access.info(".git")
    if marker is not None and not (
        stat.S_ISREG(marker.st_mode) or stat.S_ISDIR(marker.st_mode)
    ):
        fail("invalid_project", "", "project.yaml")
    project_raw, _ = strict_yaml(sources["project.yaml"], "project.yaml")
    schema = json.loads(
        files("agentic_ml")
        .joinpath("templates/initialization/schemas/project.json")
        .read_bytes()
    )
    if list(Draft202012Validator(schema).iter_errors(project_raw)):
        fail("invalid_project", "", "project.yaml")
    project = mapping(project_raw)
    raw, marks = strict_yaml(sources["experiment.yaml"], experiment)
    validate(raw, "experiment", experiment, marks)
    config = mapping(raw)
    brief_path = relative_path(str(config["brief"]))
    search_path = relative_path(str(config["search_space"]))
    if not preserved:
        sources["experiment.md"] = access.read(brief_path)
        sources["search-space.yaml"] = access.read(search_path)
    brief, positions = parse_brief(sources["experiment.md"], brief_path)
    effective, decisions, pending, diagnostics = derive_decisions(
        brief, brief_path, positions
    )
    execution = mapping(config["execution"])
    if any(
        execution.get(key)
        for key in (
            "algorithm_subset",
            "parameters",
            "search_overrides",
            "budget_overrides",
        )
    ):
        fail(
            "boundary_validation_pending", "execution", experiment, *marks["execution"]
        )
    search_raw, search_marks = strict_yaml(sources["search-space.yaml"], search_path)
    validate(search_raw, "search-space", search_path, search_marks)
    notebooks = [relative_path(str(path)) for path in sequence(config["notebooks"])]
    if len(set(notebooks)) != len(notebooks):
        fail("duplicate_path", "notebooks", experiment)
    if not preserved:
        for path in notebooks:
            access.remember(path)
    cwd = relative_path(str(config["working_directory"]))
    if not preserved:
        access.remember(cwd, directory=True)
    references = [
        data_reference(access.root, str(path)) for path in sequence(config["data"])
    ]
    data = mapping(effective["data"])
    if isinstance(data["sources"], list):
        brief_references = [
            data_reference(access.root, str(path)) for path in data["sources"]
        ]
        if [ref["absolute"] for ref in references] != [
            ref["absolute"] for ref in brief_references
        ]:
            fail("conflicting_data", "data", experiment, *marks["data"])
    effective["data_references"] = cast(JSONValue, references)
    effective["notebooks"] = cast(JSONValue, notebooks)
    effective["working_directory"] = cwd
    if preserved:
        from agentic_ml.planning.storage import checked_json

        harness = mapping(checked_json(sources["harness-origin.json"]))
    else:
        package = distribution("agentic-ml")
        origin_text = package.read_text("direct_url.json")
        origin: JSONValue = (
            cast(JSONValue, json.loads(origin_text))
            if origin_text
            else {"kind": "wheel", "distribution": "agentic-ml"}
        )
        harness = {"version": package.version, "origin": origin}
        sources["harness-origin.json"] = canonical(harness)
    inputs: list[JSONValue] = []
    for logical, path in (
        ("experiment.md", brief_path),
        ("search-space.yaml", search_path),
        ("experiment.yaml", experiment),
        ("project.yaml", "project.yaml"),
        ("pyproject.toml", "pyproject.toml"),
        ("uv.lock", "uv.lock"),
    ):
        inputs.append(
            {
                "name": logical,
                "path": path,
                "sha256": hashlib.sha256(sources[logical]).hexdigest(),
            }
        )
    return {
        "schema_version": "1.0",
        "project": {
            "root": str(access.root),
            "name": mapping(project["project"])["package"],
        },
        "experiment_id": config["id"],
        "inputs": inputs,
        "effective": effective,
        "declared_search": search_raw,
        "effective_search": search_raw,
        "decisions": decisions,
        "defaults": [
            {
                "field": "execution." + key,
                "value": value,
                "source": "structural_inheritance",
            }
            for key, value in (
                ("algorithm_subset", mapping(effective["algorithms"])["allowed"]),
                ("parameters", {}),
                ("search_overrides", {}),
                ("budget_overrides", {}),
            )
        ],
        "pending_decisions": pending,
        "diagnostics": cast(
            JSONValue, [diagnostic.__dict__ for diagnostic in diagnostics]
        ),
        "harness": harness,
        "capabilities": ["input_resolution"],
    }


def resolve_plan(request: ResolveRequest) -> PlanResult:
    """Capture explicit inputs; unresolved decisions remain blocked."""
    access: ProjectAccess | None = None
    try:
        access = ProjectAccess(request.project_root)
        experiment = relative_path(str(request.experiment))
        sources = {
            name: access.read(path)
            for name, path in (
                ("experiment.yaml", experiment),
                ("project.yaml", "project.yaml"),
                ("pyproject.toml", "pyproject.toml"),
                ("uv.lock", "uv.lock"),
            )
        }
        plan = prepare(access, experiment, sources)
        plan_id = publish(access, plan, sources)
        diagnostics = plan_diagnostics(plan)
        return PlanResult(
            plan_id,
            "blocked" if plan["pending_decisions"] else "input_ready",
            diagnostics,
        )
    except InputError as error:
        return PlanResult(None, "blocked", (error.diagnostic,))
    except (FileNotFoundError, NotADirectoryError):
        return PlanResult(
            None,
            "blocked",
            (
                Diagnostic(
                    "missing_or_unsafe_input",
                    "",
                    "",
                    None,
                    None,
                    "Required project input is missing or unsafe.",
                ),
            ),
        )
    except OSError as error:
        raise PlanningError(
            "input_io", "Unable to access selected project inputs."
        ) from error
    finally:
        if access is not None:
            access.close()


def plan_diagnostics(plan: dict[str, JSONValue]) -> tuple[Diagnostic, ...]:
    """Restore typed diagnostics from a freshly derived plan."""
    result = []
    for item in sequence(plan["diagnostics"]):
        value = mapping(item)
        result.append(
            Diagnostic(
                str(value["code"]),
                str(value["field"]),
                str(value["source_path"]),
                cast(int | None, value["line"]),
                cast(int | None, value["column"]),
                str(value["message"]),
            )
        )
    return tuple(result)


def verify_evidence(
    access: ProjectAccess, plan_id: str, check_current: bool
) -> tuple[VerificationResult, dict[str, JSONValue] | None]:
    """Recompute the preserved plan and its current-source requirements."""
    from agentic_ml.planning.storage import read_bundle

    plan, sources = read_bundle(access, plan_id)
    validate(plan, "plan", "plan.json", {})
    config_input = next(
        mapping(item)
        for item in sequence(plan["inputs"])
        if mapping(item)["name"] == "experiment.yaml"
    )
    if mapping(plan["project"])["root"] != str(access.root):
        fail("stale_source", "project.root", "plan.json")
    derived = prepare(access, str(config_input["path"]), dict(sources), preserved=True)
    if canonical(derived) != canonical(plan):
        fail("corrupt_plan", "derived_decisions", "plan.json")
    if check_current:
        for item in sequence(plan["inputs"]):
            entry = mapping(item)
            try:
                current = access.read(str(entry["path"]))
            except (OSError, InputError):
                fail("stale_source", str(entry["name"]), str(entry["path"]))
            if current != sources[str(entry["name"])]:
                fail("stale_source", str(entry["name"]), str(entry["path"]))
    access.recheck()
    diagnostics = plan_diagnostics(plan)
    return VerificationResult(
        plan_id, "blocked" if diagnostics else "input_ready", diagnostics, True
    ), plan


def checked_evidence(
    project_root: Path, plan_id: str, check_current: bool
) -> tuple[VerificationResult, dict[str, JSONValue] | None]:
    """Convert invalid evidence into safe public verification diagnostics."""
    access: ProjectAccess | None = None
    try:
        access = ProjectAccess(project_root)
        return verify_evidence(access, plan_id, check_current)
    except InputError as error:
        return VerificationResult(plan_id, "blocked", (error.diagnostic,), False), None
    except (
        ValueError,
        KeyError,
        StopIteration,
        TypeError,
        FileNotFoundError,
        NotADirectoryError,
    ):
        return VerificationResult(
            plan_id,
            "blocked",
            (
                Diagnostic(
                    "corrupt_plan",
                    "",
                    "plan.json",
                    None,
                    None,
                    "Plan evidence is missing, invalid or corrupt.",
                ),
            ),
            False,
        ), None
    except OSError as error:
        raise PlanningError(
            "plan_io", "Unable to read preserved planning evidence."
        ) from error
    finally:
        if access is not None:
            access.close()


def verify_plan(
    *, project_root: Path, plan_id: str, check_current: bool = False
) -> VerificationResult:
    """Recompute integrity and readiness; optionally compare current source bytes."""
    return checked_evidence(project_root, plan_id, check_current)[0]


def inspect_plan(*, project_root: Path, plan_id: str) -> PlanInspection:
    """Return verified preserved evidence without trusting a stored readiness flag."""
    result, plan = checked_evidence(project_root, plan_id, False)
    return PlanInspection(
        plan_id, result.status, result.integrity, plan, result.diagnostics
    )
