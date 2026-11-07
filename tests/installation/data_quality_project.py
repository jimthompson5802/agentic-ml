"""Project-owned extraction, quality declarations and dependent operation."""

from pathlib import Path

import pandas as pd

PROJECT_ERROR = RuntimeError("project operation failed")
RULES: list[dict[str, object]] = [
    {
        "id": "schema",
        "kind": "columns",
        "columns": ["id", "age", "group"],
        "exact": True,
    },
    {"id": "types", "kind": "dtypes", "columns": {"id": "int64", "age": "int64"}},
    {"id": "rows", "kind": "row_count", "min": 4, "max": 4},
    {"id": "age_present", "kind": "nulls", "column": "age"},
    {"id": "unique_id", "kind": "duplicates", "columns": ["id"]},
    {"id": "age_bounds", "kind": "range", "column": "age", "min": 0, "max": 120},
    {
        "id": "known_group",
        "kind": "allowed_values",
        "column": "group",
        "values": ["A", "B", "C"],
    },
]


def extract(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Use native pandas to select the project dataset and explicit dtypes."""
    return frames["people"].astype({"id": "int64", "age": "int64", "group": "str"})


def consume(frame: pd.DataFrame, settings: dict[str, object]) -> list[int]:
    """Persist consumed values at the project-selected sentinel path."""
    values = [int(value) for value in frame["age"]]
    Path(str(settings["sentinel"])).write_text(str(values))
    frame.loc[0, "age"] = 999
    settings["changed"] = True
    return values


def fail(frame: pd.DataFrame, settings: dict[str, object]) -> None:
    """Raise an identifiable original project exception."""
    raise PROJECT_ERROR
