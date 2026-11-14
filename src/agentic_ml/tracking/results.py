"""Validate supplied result declarations without inferring model quality."""

import json
import math
import re
from collections.abc import Mapping, Sequence
from pathlib import Path

from .provenance import validate_json


def validate_results(
    parameters: Mapping[str, object],
    metrics: Mapping[str, float],
    outputs: Mapping[str, Path],
    expected_outputs: Sequence[str],
    process_exit_code: int,
    validation_passed: bool | None,
) -> None:
    """Reject invalid values, required-output names and ambiguous status types."""
    if not isinstance(process_exit_code, int) or isinstance(process_exit_code, bool):
        raise TypeError("process_exit_code must be an integer excluding bool")
    if validation_passed is not None and not isinstance(validation_passed, bool):
        raise TypeError("validation_passed must be bool or None")
    validate_json(dict(parameters), "parameters")
    for name, value in metrics.items():
        if not isinstance(name, str) or not name:
            raise ValueError("metrics must have nonempty string names")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"metrics.{name} must be numeric")
        if not math.isfinite(value):
            raise ValueError(f"metrics.{name} must be finite")
    if isinstance(expected_outputs, (str, bytes)) or not isinstance(
        expected_outputs, Sequence
    ):
        raise TypeError("expected_outputs must be a sequence of names")
    if not expected_outputs or len(set(expected_outputs)) != len(expected_outputs):
        raise ValueError("expected_outputs must be nonempty and unique")
    for name in (*outputs, *expected_outputs):
        if (
            not isinstance(name, str)
            or name in {"provenance", "notebook"}
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name) is None
        ):
            raise ValueError(f"Unsafe output name: {name}")
    for name, path in outputs.items():
        if not isinstance(path, Path):
            raise TypeError(f"outputs.{name} must be a Path")
    missing = set(expected_outputs) - set(outputs)
    if missing:
        raise FileNotFoundError(
            f"Missing expected_outputs: {', '.join(sorted(missing))}"
        )


def output_file(root: Path, path: Path) -> Path:
    """Resolve a supplied regular output file while rejecting symlink components."""
    if not isinstance(root, Path) or not isinstance(path, Path):
        raise TypeError("Output root and source must be Paths")
    source = root / path
    if any(part.is_symlink() for part in (source, *source.parents)):
        raise ValueError(f"Symlink output: {path}")
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise ValueError(f"Output must be a regular file: {path}")
    return source


def validate_notebook(source: Path, provenance: Mapping[str, object]) -> None:
    """Check supplied notebook structure and its declared committed-source link."""
    import nbformat
    from jsonschema.exceptions import ValidationError

    from .provenance import object_map

    try:
        book = json.loads(source.read_text(encoding="utf-8"))
        nbformat.validate(book)
    except (ValidationError, ValueError, TypeError) as error:
        raise ValueError("executed_notebook has invalid nbformat structure") from error
    code = object_map(provenance["experiment"], "experiment")["code"]
    if not isinstance(code, list) or not any(
        isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and item["path"].endswith(".ipynb")
        for item in code
    ):
        raise ValueError(
            "executed_notebook requires a committed source notebook in experiment.code"
        )
