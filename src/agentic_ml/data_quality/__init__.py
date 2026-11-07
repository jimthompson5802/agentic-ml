"""Validation of experiment data quality."""

import json
import math
import numbers
import sys
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from datetime import date, time, timedelta
from typing import cast

import pandas as pd


def _check_settings(value: object) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("settings numbers must be finite")
        return
    if isinstance(value, list):
        for item in value:
            _check_settings(item)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("settings keys must be strings")
            _check_settings(item)
        return
    raise TypeError("settings must contain JSON-compatible values")


def _copy_settings(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _copy_settings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_copy_settings(item) for item in value]
    return value


class DataQualityError(ValueError):
    """A required data-quality check failed."""

    def __init__(self, report: dict[str, object]) -> None:
        """Retain the report describing required failures."""
        self.report = report
        checks = report["checks"]
        assert isinstance(checks, list)
        ids = [
            str(check["id"])
            for check in checks
            if check["required"] and not check["passed"]
        ]
        super().__init__(f"Required data-quality checks failed: {', '.join(ids)}")


def run_validated_step[T](
    frame: pd.DataFrame,
    step: Callable[[pd.DataFrame, dict[str, object]], T],
    *,
    rules: Sequence[Mapping[str, object]],
    settings: Mapping[str, object] | None = None,
) -> tuple[T, dict[str, object]]:
    """Check a snapshot before executing a project operation.

    Args:
        frame: Scalar-valued input frame to snapshot and check.
        step: Project operation receiving the checked frame and copied settings.
        rules: Explicit quality rules; an empty sequence selects no checks.
        settings: Optional JSON-compatible project settings.

    Returns:
        The operation result and the report describing its input.

    Raises:
        DataQualityError: A required check failed; its report contains results.
        TypeError: An input or declaration has an unsupported type.
        ValueError: A declaration has an invalid value.
    """
    if not callable(step):
        raise TypeError("step must be callable")
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a DataFrame")
    if settings is not None and not isinstance(settings, Mapping):
        raise TypeError("settings must be a mapping")
    _check_settings(settings)
    copied_settings = cast(dict[str, object], _copy_settings(settings or {}))
    json.dumps(copied_settings, allow_nan=False)
    snapshot = frame.copy(deep=True)
    report = validate_data(snapshot, rules=rules)
    if report["blocked"]:
        raise DataQualityError(report)
    try:
        result = step(snapshot, copied_settings)
    except Exception as error:
        error.add_note("Failure in validated-operation stage")
        raise
    return result, report


def validate_data(
    frame: pd.DataFrame, *, rules: Sequence[Mapping[str, object]]
) -> dict[str, object]:
    """Check a data frame against explicit quality rules.

    Args:
        frame: Scalar-valued pandas frame to inspect without changing it.
        rules: Ordered rule mappings; an empty sequence selects no checks.

    Returns:
        A JSON-compatible report, including failed required or advisory checks.

    Raises:
        TypeError: An input or declaration has an unsupported type.
        ValueError: A declaration or frame column name has an invalid value.
    """
    if not isinstance(rules, Sequence) or isinstance(rules, (str, bytes)):
        raise TypeError("rules must be a sequence of mappings")
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a DataFrame")
    if not frame.columns.is_unique or any(
        not isinstance(name, str) or not name for name in frame.columns
    ):
        raise ValueError("frame column names must be unique nonempty strings")
    for name in frame.columns:
        series = frame[name]
        if series.dtype == object or isinstance(series.dtype, pd.CategoricalDtype):
            object_values = (
                series.cat.categories
                if isinstance(series.dtype, pd.CategoricalDtype)
                else series
            )
            for value in object_values:
                if value is None or value is pd.NA or value is pd.NaT:
                    continue
                dtype = getattr(value, "dtype", None)
                real_number = isinstance(value, numbers.Number) and not (
                    isinstance(value, numbers.Complex)
                    and not isinstance(value, numbers.Real)
                )
                if not pd.api.types.is_scalar(value) or not (
                    isinstance(value, (str, bool, date, time, timedelta))
                    or real_number
                    or (
                        dtype is not None
                        and (
                            pd.api.types.is_datetime64_any_dtype(dtype)
                            or pd.api.types.is_timedelta64_dtype(dtype)
                            or pd.api.types.is_bool_dtype(dtype)
                        )
                    )
                ):
                    raise TypeError(f"Unsupported value in {name}")
    checks: list[dict[str, object]] = []
    ids: set[object] = set()
    for rule in rules:
        if not isinstance(rule, Mapping):
            raise TypeError("each rule must be a mapping")
        if "id" not in rule:
            raise ValueError("rule id is required")
        if not isinstance(rule["id"], str):
            raise TypeError("rule id must be a string")
        if not rule["id"]:
            raise ValueError("rule id is required")
        if rule["id"] in ids:
            raise ValueError(f"Duplicate rule id: {rule['id']}")
        ids.add(rule["id"])
        if "kind" not in rule:
            raise ValueError("rule kind is required")
        if not isinstance(rule["kind"], str):
            raise TypeError("rule kind must be a string")
        if rule.get("kind") not in {
            "columns",
            "dtypes",
            "row_count",
            "nulls",
            "duplicates",
            "range",
            "allowed_values",
        }:
            raise ValueError(f"Unsupported rule kind: {rule.get('kind')}")
        kind_keys = {
            "columns": {"columns", "exact"},
            "dtypes": {"columns"},
            "row_count": {"min", "max"},
            "nulls": {"column", "max_count"},
            "duplicates": {"columns", "max_count"},
            "range": {"column", "min", "max"},
            "allowed_values": {"column", "values"},
        }
        if set(rule) - {"id", "kind", "required"} - kind_keys[rule["kind"]]:
            raise ValueError("Unknown rule key")
        rule_kind = rule["kind"]
        if "required" in rule and not isinstance(rule["required"], bool):
            raise TypeError("required must be boolean")
        if "exact" in rule and not isinstance(rule["exact"], bool):
            raise TypeError("exact must be boolean")
        if (
            rule_kind in {"columns", "duplicates"}
            and "columns" in rule
            and not isinstance(rule["columns"], list)
        ):
            raise TypeError("columns must be a list")
        if rule_kind in {"columns", "duplicates"} and "columns" in rule:
            declared_columns = cast(list[object], rule["columns"])
            if any(not isinstance(name, str) for name in declared_columns):
                raise TypeError("column names must be strings")
            if (
                not declared_columns
                or any(not name for name in declared_columns)
                or len(set(declared_columns)) != len(declared_columns)
            ):
                raise ValueError("column names must be nonempty and unique")
        if "max_count" in rule:
            max_count = rule["max_count"]
            if type(max_count) is not int:
                raise TypeError("max_count must be an integer")
            if max_count < 0:
                raise ValueError("max_count must be nonnegative")
        if rule_kind in {"row_count", "range"} and not ({"min", "max"} & set(rule)):
            raise ValueError("At least one bound is required")
        if rule_kind == "range":
            for key in ("min", "max"):
                if key in rule:
                    bound = rule[key]
                    if type(bound) not in {int, float}:
                        raise TypeError(f"{key} must be a number")
                    if isinstance(bound, float) and not math.isfinite(bound):
                        raise ValueError(f"{key} must be finite")
            if (
                "min" in rule
                and "max" in rule
                and cast(float, rule["min"]) > cast(float, rule["max"])
            ):
                raise ValueError("min must not exceed max")
        if rule_kind in {"nulls", "range", "allowed_values"} and "column" not in rule:
            raise ValueError("column is required")
        if rule_kind in {"nulls", "range", "allowed_values"}:
            if not isinstance(rule["column"], str):
                raise TypeError("column must be a string")
            if not rule["column"]:
                raise ValueError("column must not be empty")
        if rule_kind in {"columns", "dtypes"} and "columns" not in rule:
            raise ValueError("columns are required")
        if rule_kind == "dtypes":
            dtype_columns = rule["columns"]
            if not isinstance(dtype_columns, Mapping):
                raise TypeError("dtype columns must be a mapping")
            if not dtype_columns:
                raise ValueError("dtype columns must not be empty")
            for name, dtype_name in dtype_columns.items():
                if not isinstance(name, str) or not isinstance(dtype_name, str):
                    raise TypeError("dtype names and columns must be strings")
                if not name:
                    raise ValueError("dtype column must not be empty")
                try:
                    pd.api.types.pandas_dtype(dtype_name)
                except (TypeError, ValueError) as error:
                    raise ValueError(
                        f"Invalid dtype for {name}: {dtype_name}"
                    ) from error
        if rule_kind == "allowed_values" and "values" not in rule:
            raise ValueError("values are required")
        if rule_kind == "allowed_values":
            allowed = rule["values"]
            if not isinstance(allowed, list):
                raise TypeError("values must be a list")
            if not allowed:
                raise ValueError("values must not be empty")
            for item in allowed:
                if type(item) not in {str, int, float, bool}:
                    raise TypeError("allowed values must be JSON scalars")
                if isinstance(item, float) and not math.isfinite(item):
                    raise ValueError("allowed numbers must be finite")
        if rule.get("kind") == "row_count":
            for key in ("min", "max"):
                if key in rule:
                    value = rule[key]
                    if type(value) is not int:
                        raise TypeError(f"{key} must be an integer")
                    if value < 0:
                        raise ValueError(f"{key} must be nonnegative")
            if (
                "min" in rule
                and "max" in rule
                and cast(int, rule["min"]) > cast(int, rule["max"])
            ):
                raise ValueError("min must not exceed max")
    for rule in rules:
        kind = rule["kind"]
        if kind in {"nulls", "range", "allowed_values", "duplicates"}:
            names = (
                rule.get("columns", list(frame.columns))
                if kind == "duplicates"
                else [rule["column"]]
            )
            assert isinstance(names, list)
            missing_names = [name for name in names if name not in frame.columns]
            if missing_names:
                expected = {
                    key: value
                    for key, value in rule.items()
                    if key not in {"id", "kind", "required"}
                }
                if kind in {"nulls", "duplicates"}:
                    expected.setdefault("max_count", 0)
                if kind == "range":
                    expected.setdefault("min", None)
                    expected.setdefault("max", None)
                checks.append(
                    {
                        "id": rule["id"],
                        "kind": kind,
                        "required": rule.get("required", True),
                        "expected": expected,
                        "actual": {"missing_columns": missing_names},
                        "passed": False,
                        "message": f"{rule['id']}: missing columns {missing_names}",
                    }
                )
                continue
        if rule["kind"] == "allowed_values":
            column, values = rule["column"], rule["values"]
            series = frame[column]
            missing_mask = series.isna()
            count = int(
                (~missing_mask & ~series.isin(cast(list[object], values))).sum()
            )
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "allowed_values",
                    "required": rule.get("required", True),
                    "expected": {"column": column, "values": values},
                    "actual": {
                        "invalid_count": count,
                        "missing_count": int(missing_mask.sum()),
                    },
                    "passed": count == 0,
                    "message": f"{rule['id']}: {count} values not allowed",
                }
            )
            continue
        if rule["kind"] == "range":
            column = rule["column"]
            minimum, maximum = rule.get("min"), rule.get("max")
            series = frame[column]
            dtype = series.dtype
            if (
                not pd.api.types.is_numeric_dtype(dtype)
                or pd.api.types.is_bool_dtype(dtype)
                or pd.api.types.is_complex_dtype(dtype)
            ):
                checks.append(
                    {
                        "id": rule["id"],
                        "kind": "range",
                        "required": rule.get("required", True),
                        "expected": {"column": column, "min": minimum, "max": maximum},
                        "actual": {"dtype": str(dtype), "reason": "non_real_numeric"},
                        "passed": False,
                        "message": f"{rule['id']}: non-real-numeric dtype {dtype}",
                    }
                )
                continue
            comparison_series = series
            if any(
                isinstance(bound, int) and abs(bound) > sys.float_info.max
                for bound in (minimum, maximum)
            ):
                # Preserve Python scalar comparisons when a bound cannot fit a float.
                comparison_series = series.astype(object)
            invalid = pd.Series(False, index=series.index)
            if minimum is not None:
                invalid |= comparison_series < minimum
            if maximum is not None:
                invalid |= comparison_series > maximum
            count = int(invalid.fillna(False).sum())
            missing_count = int(series.isna().sum())
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "range",
                    "required": rule.get("required", True),
                    "expected": {"column": column, "min": minimum, "max": maximum},
                    "actual": {"invalid_count": count, "missing_count": missing_count},
                    "passed": count == 0,
                    "message": f"{rule['id']}: {count} values outside {minimum} to {maximum}",
                }
            )
            continue
        if rule["kind"] == "duplicates":
            columns = rule.get("columns", list(frame.columns))
            assert isinstance(columns, list)
            limit = cast(int, rule.get("max_count", 0))
            if not columns:
                checks.append(
                    {
                        "id": rule["id"],
                        "kind": "duplicates",
                        "required": rule.get("required", True),
                        "expected": {"columns": [], "max_count": limit},
                        "actual": {"reason": "no_columns"},
                        "passed": False,
                        "message": f"{rule['id']}: no columns to check",
                    }
                )
                continue
            count = int(frame.duplicated(subset=columns, keep="first").sum())
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "duplicates",
                    "required": rule.get("required", True),
                    "expected": {"columns": columns.copy(), "max_count": limit},
                    "actual": {"count": count},
                    "passed": count <= limit,
                    "message": f"{rule['id']}: {count} duplicates; maximum {limit}",
                }
            )
            continue
        if rule["kind"] == "nulls":
            column = rule["column"]
            limit = cast(int, rule.get("max_count", 0))
            count = int(frame[column].isna().sum())
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "nulls",
                    "required": rule.get("required", True),
                    "expected": {"column": column, "max_count": limit},
                    "actual": {"count": count},
                    "passed": count <= limit,
                    "message": f"{rule['id']}: {column} has {count} missing values; maximum {limit}",
                }
            )
            continue
        if rule["kind"] == "dtypes":
            declared = rule["columns"]
            if not isinstance(declared, Mapping):
                raise TypeError("dtype columns must be a mapping")
            expected = {
                name: str(pd.api.types.pandas_dtype(dtype))
                for name, dtype in declared.items()
            }
            missing = [name for name in expected if name not in frame.columns]
            actual = {
                name: str(frame[name].dtype) for name in expected if name not in missing
            }
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "dtypes",
                    "required": rule.get("required", True),
                    "expected": {"columns": expected},
                    "actual": {"missing_columns": missing}
                    if missing
                    else {"dtypes": actual},
                    "passed": not missing and actual == expected,
                    "message": f"{rule['id']}: missing {missing}; expected {expected}, actual {actual}",
                }
            )
            continue
        if rule["kind"] == "columns":
            names = rule["columns"]
            assert isinstance(names, list)
            exact = rule.get("exact", False)
            missing = [name for name in names if name not in frame.columns]
            unexpected = (
                [name for name in frame.columns if name not in names] if exact else []
            )
            checks.append(
                {
                    "id": rule["id"],
                    "kind": "columns",
                    "required": rule.get("required", True),
                    "expected": {"columns": names.copy(), "exact": exact},
                    "actual": {"missing": missing, "unexpected": unexpected},
                    "passed": not missing and not unexpected,
                    "message": f"{rule['id']}: missing {missing}, unexpected {unexpected}",
                }
            )
            continue
        minimum = cast(int | None, rule.get("min"))
        maximum = cast(int | None, rule.get("max"))
        count = len(frame)
        passed = (minimum is None or count >= minimum) and (
            maximum is None or count <= maximum
        )
        checks.append(
            {
                "id": rule["id"],
                "kind": rule["kind"],
                "required": rule.get("required", True),
                "expected": {"min": minimum, "max": maximum},
                "actual": {"count": count},
                "passed": passed,
                "message": f"{rule['id']}: row count {count}, bounds {minimum} to {maximum}",
            }
        )
    return deepcopy(
        {
            "schema_version": "1.0",
            "status": (
                "not_checked"
                if not checks
                else "passed"
                if all(check["passed"] for check in checks)
                else "failed"
            ),
            "blocked": any(
                not check["passed"] and check["required"] for check in checks
            ),
            "row_count": len(frame),
            "columns": [
                {"name": name, "dtype": str(dtype)}
                for name, dtype in frame.dtypes.items()
            ],
            "checks": checks,
        }
    )
