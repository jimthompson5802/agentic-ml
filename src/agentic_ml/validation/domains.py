"""Analytic parameter-domain and universal implication validation."""

from typing import cast

from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.parsing import mapping, sequence
from agentic_ml.validation.checks import equal, reject
from agentic_ml.validation.registry import permits


def contains(domain: dict[str, JSONValue], value: JSONValue) -> bool:
    """Test exact scalar membership without enumerating numeric intervals."""
    if "choices" in domain:
        return any(equal(value, item) for item in sequence(domain["choices"]))
    kind = domain["type"]
    if type(value) is not (int if kind == "integer" else float):
        return False
    number = value
    return cast(float, domain["min"]) <= number <= cast(float, domain["max"])


def validate_domain(
    domain: dict[str, JSONValue], spec: dict[str, JSONValue], field: str
) -> None:
    """Require all values in a declared search domain to satisfy its registry spec."""
    if domain.get("type") == "categorical":
        choices = sequence(domain["choices"])
        if not choices or any(not permits(spec, x) for x in choices):
            reject(
                "invalid_domain",
                field,
                "Use nonempty choices satisfying the registered parameter domain.",
            )
        if any(
            any(equal(value, old) for old in choices[:index])
            for index, value in enumerate(choices)
        ):
            reject("invalid_domain", field, "Use type-distinct categorical choices.")
        return
    kind = str(domain["type"])
    if kind not in sequence(spec["types"]):
        reject("invalid_domain", field, "Use a range type accepted by the parameter.")
    low, high = domain["min"], domain["max"]
    # Structural planning already checks finite, ordered bounds and positive logs.
    if kind == "float":
        low, high = float(cast(float, low)), float(cast(float, high))
    if not permits(spec, low) or not permits(spec, high):
        reject(
            "invalid_domain",
            field,
            "Keep inclusive bounds inside the registered parameter domain.",
        )
    if "choices" in spec:
        if not equal(low, high) or not permits(spec, low):
            reject(
                "invalid_domain",
                field,
                "Use categorical choices for a discrete registered domain.",
            )


def check_combinations(
    spec: dict[str, JSONValue], domains: dict[str, JSONValue], field: str
) -> None:
    """Reject any space admitting a null value forbidden by an implication."""
    rules = sorted(sequence(spec["requires_non_null"]), key=lambda x: str(x))
    for item in rules:
        rule = mapping(item)
        first, second = str(rule["if_parameter"]), str(rule["then_parameter"])
        if contains(mapping(domains[first]), rule["equals"]) and contains(
            mapping(domains[second]), None
        ):
            reject(
                "incompatible_combination",
                field,
                f"Parameter {first} requires non-null {second} for the declared strategy.",
            )


def check_space(
    space: dict[str, JSONValue], spec: dict[str, JSONValue], task: JSONValue, field: str
) -> None:
    """Validate task, parameters and every combination in one algorithm space."""
    if task not in sequence(spec["tasks"]):
        reject(
            "task_mismatch",
            field,
            "Choose a registered algorithm supporting the effective task.",
        )
    params = mapping(spec["parameters"])
    fixed, search = mapping(space["fixed"]), mapping(space["search"])
    domains: dict[str, JSONValue] = {}
    for name in sorted(set(fixed) | set(search)):
        if name not in params:
            reject(
                "unknown_parameter",
                field + "." + name,
                "Use a registered parameter name.",
            )
    for name, raw in sorted(params.items()):
        param = mapping(raw)
        location = field + (".search." if name in search else ".fixed.") + name
        if name in search:
            domain = mapping(search[name])
            validate_domain(domain, param, location)
            domains[name] = domain
        else:
            value = fixed.get(name, param["default"])
            if not permits(param, value):
                reject(
                    "invalid_parameter_type",
                    location,
                    "Supply a value of the registered scalar type and domain without coercion.",
                )
            domains[name] = {"type": "categorical", "choices": [value]}
    check_combinations(spec, domains, field)
