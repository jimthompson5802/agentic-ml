"""Materialize one candidate against live, independently checked configuration evidence."""

from copy import deepcopy

from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.parsing import InputError, mapping, sequence
from agentic_ml.planning.paths import ProjectAccess
from agentic_ml.validation.checks import bounded, digest, equal, reject, schema
from agentic_ml.validation.configuration import inspect_validation
from agentic_ml.validation.domains import check_combinations, contains
from agentic_ml.validation.models import (
    CandidateRequest,
    CandidateResult,
    ValidationError,
)
from agentic_ml.validation.registry import permits
from agentic_ml.validation.storage import read_bundle


def validate_candidate(request: CandidateRequest) -> CandidateResult:
    """Check every proposed value, inherit defaults and reverify current evidence."""
    access: ProjectAccess | None = None
    try:
        bounded(request.parameters)
        envelope: dict[str, JSONValue] = {
            "schema_version": "1.0",
            "algorithm": request.algorithm,
            "parameters": request.parameters,
        }
        schema(envelope, "candidate", "invalid_candidate")
        inspected = inspect_validation(
            project_root=request.project_root, validation_id=request.validation_id
        )
        if inspected.status != "valid" or inspected.configuration is None:
            return CandidateResult(
                "blocked",
                request.validation_id,
                request.algorithm,
                None,
                None,
                inspected.diagnostics,
            )
        algorithms = mapping(inspected.configuration["algorithms"])
        if request.algorithm not in algorithms:
            reject(
                "unknown_algorithm",
                "algorithm",
                "Select an algorithm in the effective allowed set.",
            )
        selected = mapping(algorithms[request.algorithm])
        fixed, defaults, search = (
            mapping(selected["fixed"]),
            mapping(selected["defaults"]),
            mapping(selected["search"]),
        )
        for name, value in sorted(request.parameters.items()):
            field = "parameters." + name
            if name in fixed:
                if not equal(value, fixed[name]):
                    reject(
                        "fixed_parameter",
                        field,
                        "Retain the recorded fixed value or revise experiment inputs.",
                    )
            elif name in defaults:
                if not equal(value, defaults[name]):
                    reject(
                        "default_parameter",
                        field,
                        "Retain the recorded default; omitted parameters are not tunable.",
                    )
            elif name not in search:
                reject(
                    "unknown_parameter",
                    field,
                    "Use a registered parameter in the effective configuration.",
                )
            elif not contains(mapping(search[name]), value):
                reject(
                    "outside_boundary",
                    field,
                    "Choose an allowed typed categorical value or inclusive range value.",
                )
        for name in sorted(search):
            if name not in request.parameters:
                reject(
                    "missing_parameter",
                    "parameters." + name,
                    "Supply a value for this tunable parameter.",
                )
        parameters: dict[str, JSONValue] = deepcopy(
            {**fixed, **defaults, **request.parameters}
        )
        access = ProjectAccess(request.project_root)
        _, registry, _ = read_bundle(access, request.validation_id)
        spec = next(
            mapping(item)
            for item in sequence(registry["algorithms"])
            if mapping(item)["id"] == request.algorithm
        )
        for name, value in parameters.items():
            if not permits(mapping(mapping(spec["parameters"])[name]), value):
                reject(
                    "invalid_parameter_type",
                    "parameters." + name,
                    "Use the registered scalar type and domain without coercion.",
                )
        check_combinations(
            spec,
            {
                name: {"type": "categorical", "choices": [value]}
                for name, value in parameters.items()
            },
            "parameters",
        )
        access.recheck()
        current = inspect_validation(
            project_root=request.project_root, validation_id=request.validation_id
        )
        if current.status != "valid":
            return CandidateResult(
                "blocked",
                request.validation_id,
                request.algorithm,
                None,
                None,
                current.diagnostics,
            )
        if current.configuration is None or digest(current.configuration) != digest(
            inspected.configuration
        ):
            reject(
                "stale_validation",
                "inputs",
                "Revalidate changed candidate evidence explicitly.",
            )
        origins = {
            name: "fixed"
            if name in fixed
            else "default"
            if name in defaults
            else "candidate"
            for name in parameters
        }
        return CandidateResult(
            "valid", request.validation_id, request.algorithm, parameters, origins
        )
    except InputError as error:
        return CandidateResult(
            "blocked",
            request.validation_id,
            request.algorithm,
            None,
            None,
            (error.diagnostic,),
        )
    except OSError as error:
        raise ValidationError(
            "validation_io", "Unable to access candidate validation evidence."
        ) from error
    finally:
        if access is not None:
            access.close()
