"""Shared strict scalar, resource and diagnostic checks for validation."""

import hashlib
import json
import math
from importlib.resources import files
from typing import NoReturn, cast

from jsonschema import Draft202012Validator

from agentic_ml.planning.models import Diagnostic, JSONValue
from agentic_ml.planning.parsing import InputError
from agentic_ml.planning.storage import canonical


def reject(code: str, field: str, message: str, source: str = "") -> NoReturn:
    """Raise one safe, actionable diagnostic without exposing supplied values."""
    raise InputError(Diagnostic(code, field, source, None, None, message))


def digest(value: JSONValue) -> str:
    """Return the canonical content identity of a finite JSON value."""
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def bounded(value: object, depth: int = 0) -> None:
    """Reject unsupported Python objects and oversized recursive input trees."""
    if depth > 20:
        reject("input_limit", "", "Use nesting of at most 20 levels.")
    if type(value) not in (dict, list, str, int, float, bool, type(None)):
        reject("invalid_parameter_type", "", "Use finite JSON-compatible values.")
    if isinstance(value, str) and len(value) > 4096:
        reject("input_limit", "", "Use strings of at most 4096 characters.")
    if type(value) is int and abs(value) > 9007199254740991:
        reject("invalid_parameter_type", "", "Use a safe integer.")
    if type(value) is float and not math.isfinite(value):
        reject("invalid_parameter_type", "", "Use a finite number.")
    if isinstance(value, dict):
        for key, child in value.items():
            if type(key) is not str:
                reject("invalid_parameter_type", "", "Use string mapping keys.")
            bounded(key, depth + 1)
            bounded(child, depth + 1)
    elif isinstance(value, list):
        if len(value) > 1000:
            reject("input_limit", "", "Use at most 1000 list entries.")
        for child in value:
            bounded(child, depth + 1)
    if depth == 0 and len(canonical(cast(JSONValue, value))) > 1048576:
        reject("input_limit", "", "Use at most one MiB of input.")


def schema(value: JSONValue, name: str, code: str) -> None:
    """Check a packaged validation schema and report its first stable error."""
    raw = (
        files("agentic_ml").joinpath(f"schemas/validation/1.0/{name}.json").read_bytes()
    )
    validator = Draft202012Validator(json.loads(raw))
    errors = sorted(
        validator.iter_errors(value), key=lambda e: str(list(e.absolute_path))
    )
    if errors:
        field = ".".join(map(str, errors[0].absolute_path))
        reject(
            code,
            field,
            "Use the documented validation fields, types and supported values.",
        )


def scalar_type(value: JSONValue) -> str:
    """Name the exact scalar type without bool/integer or numeric coercion."""
    return {
        type(None): "null",
        bool: "boolean",
        int: "integer",
        float: "float",
        str: "string",
    }.get(type(value), "invalid")


def equal(left: JSONValue, right: JSONValue) -> bool:
    """Compare scalar values with explicit type identity."""
    return type(left) is type(right) and left == right
