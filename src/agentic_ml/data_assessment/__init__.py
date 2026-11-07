"""Native pandas descriptive reports for experiment projects."""

import math
from numbers import Integral, Real

import pandas as pd


def assess_data(frame: pd.DataFrame, *, target: str) -> dict[str, object]:
    """Describe a frame without assigning a quality judgment.

    Args:
        frame: Native frame with unique, nonempty string column names.
        target: Existing classification target; numeric targets also get counts.

    Returns:
        Versioned plain report with ordered column summaries and target balance.
        Missing/nonfinite statistics are null; float frequency infinities are
        explicit strings. Proportions exclude missing values; missingness rates
        include all rows and are null for an empty frame. No input is modified.

    Raises:
        TypeError: Input is not a DataFrame or a column has unsupported data.
        ValueError: Column names or the target are invalid.
    """
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a pandas DataFrame")
    if not frame.columns.is_unique or any(
        not isinstance(name, str) or not name for name in frame.columns
    ):
        raise ValueError("column names must be unique nonempty strings")
    if not isinstance(target, str) or not target or target not in frame.columns:
        raise ValueError("target must name an existing column")
    columns: list[dict[str, object]] = []
    for name in frame.columns:
        series = frame[name]
        _validate_series(series, name)
        entry: dict[str, object] = {
            "name": name,
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_rate": float(series.isna().mean()) if len(frame) else None,
        }
        if pd.api.types.is_numeric_dtype(
            series.dtype
        ) and not pd.api.types.is_bool_dtype(series.dtype):
            entry["summary"] = {
                key: _scalar(value)
                for key, value in series.describe(percentiles=[0.25, 0.5, 0.75]).items()
            }
        else:
            entry["frequencies"] = _frequencies(series)
        columns.append(entry)
    return {
        "schema_version": "1.0",
        "row_count": len(frame),
        "target": target,
        "columns": columns,
        "target_balance": _frequencies(frame[target]),
    }


def _frequencies(series: pd.Series) -> list[dict[str, object]]:
    counts = series.value_counts(sort=False, dropna=True)
    proportions = series.value_counts(sort=False, dropna=True, normalize=True)
    return [
        {
            "value": ("Infinity" if value > 0 else "-Infinity")
            if pd.api.types.is_float_dtype(series.dtype)
            and isinstance(value, Real)
            and math.isinf(value)
            else _scalar(value),
            "count": int(count),
            "proportion": _scalar(proportion),
        }
        for (value, count), proportion in zip(counts.items(), proportions, strict=True)
    ]


def _scalar(value: object) -> object:
    if value is None or value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if pd.api.types.is_bool(value):
        return bool(value)
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        return float(value) if math.isfinite(value) else None
    return value


def _validate_series(series: pd.Series, name: str) -> None:
    dtype = series.dtype
    if isinstance(dtype, pd.CategoricalDtype):
        for value in dtype.categories:
            if not isinstance(value, (str, bool, Integral, Real, pd.Timestamp)) or (
                isinstance(value, Real) and not math.isfinite(value)
            ):
                raise TypeError(f"Unsupported categorical scalar in column {name}")
        return
    if pd.api.types.is_object_dtype(dtype):
        if any(not isinstance(value, str) for value in series.dropna()):
            raise TypeError(f"Unsupported object in column {name}")
        return
    if isinstance(dtype, pd.StringDtype) or isinstance(dtype, pd.DatetimeTZDtype):
        return
    if getattr(dtype, "kind", None) in {"i", "u", "f", "b", "M"} and not isinstance(
        dtype, (pd.SparseDtype, pd.ArrowDtype)
    ):
        return
    raise TypeError(f"Unsupported dtype in column {name}: {dtype}")
