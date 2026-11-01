"""Structural search-boundary validation shared by public planning interfaces."""

import json
import math
from copy import deepcopy
from dataclasses import dataclass, field
from importlib.resources import files

from jsonschema import Draft202012Validator

from agentic_ml.planning.models import Diagnostic, JSONValue
from agentic_ml.planning.parsing import InputError, fail, mapping, validate

type SearchSpace = dict[str, JSONValue]


@dataclass(frozen=True)
class SearchSelection:
    """Supply resolved brief constraints and optional execution narrowing.

    Missing mode/allowed values represent unresolved delegated choices. The
    resolver remains responsible for marking these decisions blocked.
    """

    mode: JSONValue = None
    allowed: JSONValue = None
    execution: dict[str, JSONValue] = field(default_factory=dict)
    budgets: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(frozen=True)
class BoundaryResult:
    """Return an independent effective space or blocking structural diagnostics."""

    effective_search: SearchSpace | None
    effective_budgets: dict[str, JSONValue] | None
    diagnostics: tuple[Diagnostic, ...]


def validate_boundaries(
    declared: SearchSpace, requested: SearchSelection
) -> BoundaryResult:
    """Validate structural boundaries without registry access or execution.

    Diagnostic source paths are logical names: search-space.yaml, experiment.md
    and experiment.yaml. The resolver maps them to selected paths and locations.
    Inputs are never mutated. An accepted result grants no execution authority.
    """
    try:
        validate(declared, "search-space", "search-space.yaml", {})
        check_declared(declared)
        check_execution(requested.execution)
        effective = deepcopy(declared)
        pool = mapping(effective["algorithms"])
        allowed = requested.allowed
        mode = requested.mode
        if mode is not None and mode not in ("use", "select", "compare"):
            fail("invalid_boundary", "algorithms.mode", "experiment.md")
        if allowed is not None:
            if (
                not isinstance(allowed, list)
                or not allowed
                or any(
                    not isinstance(name, str) or name not in pool for name in allowed
                )
                or len({str(name) for name in allowed}) != len(allowed)
            ):
                fail("invalid_boundary", "algorithms.allowed", "experiment.md")
            if mode == "use" and len(allowed) != 1:
                fail("invalid_boundary", "algorithms.allowed", "experiment.md")
            pool = {name: raw for name, raw in pool.items() if name in allowed}
        subset = requested.execution.get("algorithm_subset")
        if subset is not None:
            if (
                not isinstance(subset, list)
                or not subset
                or any(not isinstance(name, str) or name not in pool for name in subset)
                or len({str(name) for name in subset}) != len(subset)
                or mode in ("use", "compare")
                and set(map(str, subset)) != set(pool)
                or allowed is None
                or mode is None
            ):
                fail(
                    "invalid_boundary", "execution.algorithm_subset", "experiment.yaml"
                )
            pool = {name: raw for name, raw in pool.items() if name in subset}
        effective["algorithms"] = pool
        apply_parameters(pool, requested.execution)
        budgets = deepcopy(requested.budgets)
        for key, value in mapping(
            requested.execution.get("budget_overrides", {})
        ).items():
            ceiling = budgets.get(key)
            if (
                type(value) not in (int, float)
                or not scalar(value)
                or not isinstance(value, (int, float))
                or value <= 0
                or type(ceiling) not in (int, float)
                or not isinstance(ceiling, (int, float))
                or value > ceiling
            ):
                fail(
                    "invalid_boundary",
                    "execution.budget_overrides." + key,
                    "experiment.yaml",
                )
            budgets[key] = value
        return BoundaryResult(effective, budgets, ())
    except InputError as error:
        return BoundaryResult(None, None, (error.diagnostic,))


def check_execution(execution: dict[str, JSONValue]) -> None:
    """Apply the installed execution schema equally to direct checker callers."""
    definition = json.loads(
        files("agentic_ml")
        .joinpath("schemas/planning/1.0/experiment.json")
        .read_bytes()
    )["properties"]["execution"]
    errors = list(
        Draft202012Validator(definition).iter_errors(
            {"status": "configured", **execution}
        )
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        fail("invalid_boundary", ("execution." + path).rstrip("."), "experiment.yaml")


def scalar(value: JSONValue) -> bool:
    """Recognize finite JSON scalar values within the versioned numeric limit."""
    return (
        value is None
        or isinstance(value, (str, bool))
        or type(value) is int
        and abs(value) <= 9007199254740991
        or type(value) is float
        and math.isfinite(value)
    )


def same(left: JSONValue, right: JSONValue) -> bool:
    """Compare categorical/fixed values without collapsing scalar types."""
    return type(left) is type(right) and left == right


def valid_space(value: JSONValue) -> bool:
    """Recognize a complete categorical or inclusive numeric search definition."""
    if not isinstance(value, dict):
        return False
    kind = value.get("type")
    if kind == "categorical":
        choices = value.get("choices")
        return (
            set(value) == {"type", "choices"}
            and isinstance(choices, list)
            and bool(choices)
            and all(scalar(item) for item in choices)
            and all(
                not same(item, prior)
                for i, item in enumerate(choices)
                for prior in choices[:i]
            )
        )
    if kind not in ("integer", "float") or set(value) != {
        "type",
        "min",
        "max",
        "scale",
    }:
        return False
    low, high = value["min"], value["max"]
    if not (
        type(low) in (int, float)
        and type(high) in (int, float)
        and scalar(low)
        and scalar(high)
        and isinstance(low, (int, float))
        and isinstance(high, (int, float))
    ):
        return False
    return (
        (kind != "integer" or type(low) is int and type(high) is int)
        and low <= high
        and value["scale"] in ("linear", "logarithmic")
        and (value["scale"] != "logarithmic" or low > 0 and high > 0)
    )


def check_declared(declared: dict[str, JSONValue]) -> None:
    """Reject malformed domains and parameters that are both fixed and tunable."""
    for name, raw in mapping(declared["algorithms"]).items():
        algorithm = mapping(raw)
        for parameter, value in mapping(algorithm["fixed"]).items():
            if not scalar(value):
                fail(
                    "invalid_boundary",
                    f"algorithms.{name}.fixed.{parameter}",
                    "search-space.yaml",
                )
        for parameter in mapping(algorithm["search"]):
            if parameter in mapping(algorithm["fixed"]) or not valid_space(
                mapping(algorithm["search"])[parameter]
            ):
                fail(
                    "invalid_boundary",
                    f"algorithms.{name}.search.{parameter}",
                    "search-space.yaml",
                )


def apply_parameters(
    pool: dict[str, JSONValue], execution: dict[str, JSONValue]
) -> None:
    """Apply scalar selections and search replacements to an independent copy."""
    for name, raw in mapping(execution.get("parameters", {})).items():
        if name not in pool:
            fail("invalid_boundary", f"execution.parameters.{name}", "experiment.yaml")
        algorithm = mapping(pool[name])
        fixed, search = mapping(algorithm["fixed"]), mapping(algorithm["search"])
        for parameter, value in mapping(raw).items():
            if not scalar(value) or not (
                parameter in fixed
                and same(value, fixed[parameter])
                or parameter in search
                and contains(mapping(search[parameter]), value)
            ):
                fail(
                    "invalid_boundary",
                    f"execution.parameters.{name}.{parameter}",
                    "experiment.yaml",
                )
            fixed[parameter] = value
            search.pop(parameter, None)
    for name, raw in mapping(execution.get("search_overrides", {})).items():
        if name not in pool:
            fail(
                "invalid_boundary",
                f"execution.search_overrides.{name}",
                "experiment.yaml",
            )
        search = mapping(mapping(pool[name])["search"])
        for parameter, replacement in mapping(raw).items():
            if (
                parameter not in search
                or not valid_space(replacement)
                or not subset_space(mapping(search[parameter]), mapping(replacement))
            ):
                fail(
                    "invalid_boundary",
                    f"execution.search_overrides.{name}.{parameter}",
                    "experiment.yaml",
                )
        search.update(deepcopy(mapping(raw)))


def contains(space: dict[str, JSONValue], value: JSONValue) -> bool:
    """Check scalar membership with type-aware categories and inclusive bounds."""
    if space["type"] == "categorical":
        choices = space["choices"]
        return isinstance(choices, list) and any(same(value, item) for item in choices)
    if (
        type(value) not in (int, float)
        or not isinstance(value, (int, float))
        or space["type"] == "integer"
        and type(value) is not int
    ):
        return False
    low, high = space["min"], space["max"]
    return (
        isinstance(low, (int, float))
        and isinstance(high, (int, float))
        and low <= value <= high
    )


def subset_space(
    declared: dict[str, JSONValue], requested: dict[str, JSONValue]
) -> bool:
    """Check that a replacement preserves domain kind/scale and only narrows."""
    if requested["type"] != declared["type"]:
        return False
    if declared["type"] == "categorical":
        choices = requested["choices"]
        return isinstance(choices, list) and all(
            contains(declared, item) for item in choices
        )
    return (
        requested["scale"] == declared["scale"]
        and contains(declared, requested["min"])
        and contains(declared, requested["max"])
    )
