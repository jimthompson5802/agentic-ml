"""Validate initialization schema slices without resolving experiment decisions."""

import json
from importlib.resources import files
from typing import Any

import jsonschema
import yaml

from .models import InitializationError


def validate_document(content: bytes, schema_name: str) -> dict[str, Any]:
    """Validate one YAML/JSON draft against an installed schema resource."""
    try:
        value: dict[str, Any] = yaml.safe_load(content)
        schema = json.loads(
            files("agentic_ml")
            .joinpath(f"templates/initialization/schemas/{schema_name}.json")
            .read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator(schema).validate(value)
    except (yaml.YAMLError, jsonschema.ValidationError, ValueError) as error:
        raise InitializationError(
            "Initialization configuration schema conflict"
        ) from error
    return value
