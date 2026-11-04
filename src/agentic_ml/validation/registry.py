"""Validate declarative algorithm metadata without importing algorithm code."""

import json
from copy import deepcopy
from importlib.resources import files
from typing import cast

from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.parsing import InputError, mapping, sequence
from agentic_ml.validation.checks import (
    bounded,
    digest,
    equal,
    reject,
    scalar_type,
    schema,
)
from agentic_ml.validation.models import RegistryDocument, RegistryResult


def permits(spec: dict[str, JSONValue], value: JSONValue) -> bool:
    """Check an exact scalar against a registered parameter domain."""
    if scalar_type(value) not in sequence(spec["types"]):
        return False
    if "choices" in spec and not any(
        equal(value, x) for x in sequence(spec["choices"])
    ):
        return False
    if value is not None and type(value) in (int, float):
        number = cast(int | float, value)
        if "minimum" in spec and number < cast(int | float, spec["minimum"]):
            return False
        if "maximum" in spec and number > cast(int | float, spec["maximum"]):
            return False
    return True


def check_parameters(spec: dict[str, JSONValue], prefix: str) -> None:
    """Reject inconsistent defaults, scalar domains and implication metadata."""
    parameters = mapping(spec["parameters"])
    for name, value in sorted(parameters.items()):
        param = mapping(value)
        field = prefix + ".parameters." + name
        limits = {"minimum", "maximum"} & param.keys()
        types = sequence(param["types"])
        if limits and (
            "choices" in param
            or not set(map(str, types)) <= {"integer", "float", "null"}
            or not set(map(str, types)) & {"integer", "float"}
        ):
            reject(
                "invalid_registry",
                field,
                "Use either numeric bounds or scalar choices.",
            )
        if (
            "minimum" in param
            and "maximum" in param
            and cast(float, param["minimum"]) > cast(float, param["maximum"])
        ):
            reject("invalid_registry", field, "Order inclusive numeric bounds.")
        if "float" not in types and any(type(param[key]) is not int for key in limits):
            reject(
                "invalid_registry",
                field,
                "Use integer bounds for an integer-only domain.",
            )
        if "choices" in param:
            choices = sequence(param["choices"])
            for index, choice in enumerate(choices):
                if not permits(param, choice) or any(
                    equal(choice, old) for old in choices[:index]
                ):
                    reject(
                        "invalid_registry", field, "Use legal, type-distinct choices."
                    )
        if not permits(param, param["default"]):
            reject(
                "invalid_registry",
                field + ".default",
                "Default must satisfy the parameter domain.",
            )
    for rule_value in sequence(spec["requires_non_null"]):
        rule = mapping(rule_value)
        first, second = str(rule["if_parameter"]), str(rule["then_parameter"])
        if (
            first not in parameters
            or second not in parameters
            or not permits(mapping(parameters[first]), rule["equals"])
        ):
            reject(
                "invalid_registry",
                prefix + ".requires_non_null",
                "Reference existing parameters and a legal antecedent value.",
            )


def validate_registry(declarations: RegistryDocument | None = None) -> RegistryResult:
    """Return validated additive metadata, without loading a training adapter."""
    registry = cast(
        RegistryDocument,
        json.loads(
            files("agentic_ml")
            .joinpath("registry/validation/1.0/builtins.json")
            .read_bytes()
        ),
    )
    try:
        bounded(declarations)
        supplied: RegistryDocument = (
            deepcopy(declarations)
            if declarations is not None
            else {"schema_version": "1.0", "algorithms": []}
        )
        if not isinstance(supplied, dict):
            reject("invalid_registry", "", "Supply a registry mapping.")
        if supplied.get("schema_version") != "1.0":
            reject(
                "unsupported_version",
                "schema_version",
                "Use validation schema version 1.0.",
            )
        existing = sequence(registry["algorithms"])
        seen = {str(mapping(item)["id"]) for item in existing}
        additions = supplied.get("algorithms")
        if isinstance(additions, list):
            for index, item in enumerate(additions):
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    name = str(item["id"])
                    if name in seen:
                        reject(
                            "duplicate_algorithm",
                            f"algorithms.{index}.id",
                            "Choose an ID distinct from built-ins and other declarations.",
                        )
                    seen.add(name)
                    if (
                        "interface_version" in item
                        and item["interface_version"] != "1.0"
                    ):
                        reject(
                            "unsupported_version",
                            f"algorithms.{index}.interface_version",
                            "Use validation interface version 1.0.",
                        )
        schema(supplied, "registry", "invalid_registry")
        combined = existing + sequence(supplied["algorithms"])
        registry["algorithms"] = combined
        schema(registry, "registry", "invalid_registry")
        for item in combined:
            spec = mapping(item)
            check_parameters(spec, "algorithms." + str(spec["id"]))
        registry["algorithms"] = sorted(
            combined, key=lambda item: str(mapping(item)["id"])
        )
        return RegistryResult("valid", registry, digest(registry))
    except InputError as error:
        return RegistryResult("blocked", None, None, (error.diagnostic,))
