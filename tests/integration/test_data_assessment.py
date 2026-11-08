"""Public descriptive assessment contract (US-12-AC-02)."""

import json
from pathlib import Path
from typing import cast

import pandas as pd
import pytest

from agentic_ml.data_assessment import assess_data

pytestmark = pytest.mark.milestone_1


def test_numeric_missingness_and_target_balance() -> None:
    """Report literal sample statistics without changing the caller."""
    frame = pd.DataFrame(
        {"value": [1.0, 3.0, 5.0, None], "label": ["A", "A", "B", None]}
    )
    before = frame.copy(deep=True)
    report = assess_data(frame, target="label")
    assert report["schema_version"] == "1.0"
    assert report["row_count"] == 4
    assert report["target"] == "label"
    columns = cast(list[dict[str, object]], report["columns"])
    assert columns[0] == {
        "name": "value",
        "dtype": "float64",
        "missing_count": 1,
        "missing_rate": 0.25,
        "summary": {
            "count": 3.0,
            "mean": 3.0,
            "std": 2.0,
            "min": 1.0,
            "25%": 2.0,
            "50%": 3.0,
            "75%": 4.0,
            "max": 5.0,
        },
    }
    assert report["target_balance"] == [
        {"value": "A", "count": 2, "proportion": 2 / 3},
        {"value": "B", "count": 1, "proportion": 1 / 3},
    ]
    assert columns[1]["missing_count"] == 1
    assert columns[1]["missing_rate"] == 0.25
    assert columns[1]["frequencies"] == report["target_balance"]
    json.dumps(report, allow_nan=False)
    pd.testing.assert_frame_equal(frame, before)


def test_nullable_empty_and_singleton_summaries_are_finite_json() -> None:
    """Missing statistics and empty rates serialize as null."""
    for values in ([], [None], [7]):
        frame = pd.DataFrame({"value": pd.Series(values, dtype="Int64")})
        report = assess_data(frame, target="value")
        column = cast(list[dict[str, object]], report["columns"])[0]
        summary = cast(dict[str, object], column["summary"])
        assert summary["count"] == (1 if values == [7] else 0)
        assert summary["std"] is None
        assert column["missing_rate"] == (
            None if not values else 1.0 if values == [None] else 0.0
        )
        assert report["target_balance"] == (
            [] if values != [7] else [{"value": 7, "count": 1, "proportion": 1.0}]
        )
        json.dumps(report, allow_nan=False)


def test_boolean_category_and_datetime_frequencies() -> None:
    """Preserve category order, unused levels, boolean values and ISO dates."""
    frame = pd.DataFrame(
        {
            "flag": pd.Series([True, False, None], dtype="boolean"),
            "label": pd.Categorical(
                ["B", "B", None], categories=["A", "B", "C"], ordered=True
            ),
            "when": pd.to_datetime(
                pd.Series(["2024-01-01T00:00:00Z", "2024-01-01T00:00:00Z", None])
            ),
        }
    )
    report = assess_data(frame, target="label")
    columns = cast(list[dict[str, object]], report["columns"])
    assert columns[0]["frequencies"] == [
        {"value": True, "count": 1, "proportion": 0.5},
        {"value": False, "count": 1, "proportion": 0.5},
    ]
    assert report["target_balance"] == [
        {"value": "A", "count": 0, "proportion": 0.0},
        {"value": "B", "count": 2, "proportion": 1.0},
        {"value": "C", "count": 0, "proportion": 0.0},
    ]
    assert columns[2]["frequencies"] == [
        {"value": "2024-01-01T00:00:00+00:00", "count": 2, "proportion": 1.0}
    ]
    json.dumps(report, allow_nan=False)


def test_infinite_numeric_target_retains_explicit_frequency_values() -> None:
    """Infinity is observed, while nonfinite summary statistics become null."""
    frame = pd.DataFrame({"label": [float("inf"), float("-inf"), 1.0, None]})
    report = assess_data(frame, target="label")
    column = cast(list[dict[str, object]], report["columns"])[0]
    assert column["missing_count"] == 1
    assert report["target_balance"] == [
        {"value": "Infinity", "count": 1, "proportion": 1 / 3},
        {"value": "-Infinity", "count": 1, "proportion": 1 / 3},
        {"value": 1.0, "count": 1, "proportion": 1 / 3},
    ]
    summary = cast(dict[str, object], column["summary"])
    assert summary["mean"] is None
    assert summary["min"] is None
    assert summary["max"] is None
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize(
    "series",
    [
        pd.Series([[1]], dtype=object),
        pd.Series([{"a": 1}], dtype=object),
        pd.Series([1, "a"], dtype=object),
        pd.Series([object()], dtype=object),
        pd.Series([1j]),
        pd.Series(pd.to_timedelta([1], unit="D")),
        pd.Series(pd.period_range("2024", periods=1, freq="Y")),
        pd.Series(pd.Categorical([1j])),
    ],
)
def test_unsupported_column_types_name_the_column(series: pd.Series) -> None:
    """Reject unsupported data rather than coercing its representation."""
    with pytest.raises(TypeError, match="bad"):
        assess_data(pd.DataFrame({"bad": series}), target="bad")


@pytest.mark.parametrize(
    "frame,target",
    [
        (pd.DataFrame([[1, 2]], columns=["x", "x"]), "x"),
        (pd.DataFrame({"": [1]}), ""),
        (pd.DataFrame({1: [1]}), 1),
        (pd.DataFrame({"x": [1]}), "absent"),
        (pd.DataFrame({"x": [1]}), None),
    ],
)
def test_invalid_column_names_and_target(frame: pd.DataFrame, target: str) -> None:
    """Reject invalid names and target with a value error."""
    with pytest.raises(ValueError, match="column|target"):
        assess_data(frame, target=target)


def test_non_dataframe_is_rejected() -> None:
    """Require native frame input."""
    with pytest.raises(TypeError, match="DataFrame"):
        assess_data(cast(pd.DataFrame, [1]), target="label")


def test_arrow_extension_is_rejected_with_column_context() -> None:
    """The supported nullable dtypes do not imply arbitrary extension support."""
    with pytest.raises(TypeError, match="bad"):
        assess_data(
            pd.DataFrame({"bad": pd.Series([1], dtype="int64[pyarrow]")}), target="bad"
        )


@pytest.mark.parametrize(
    "dtype", ["int8", "uint64", "float32", "Int32", "UInt64", "Float64"]
)
def test_supported_numeric_dtypes_keep_schema_and_literal_summary(dtype: str) -> None:
    """Retain native numeric dtypes and sample-statistic semantics."""
    frame = pd.DataFrame({"label": pd.Series([1, 3, 5], dtype=dtype)})
    report = assess_data(frame, target="label")
    column = cast(list[dict[str, object]], report["columns"])[0]
    assert column["dtype"] == dtype
    assert column["summary"] == pytest.approx(
        {
            "count": 3,
            "mean": 3,
            "std": 2,
            "min": 1,
            "25%": 2,
            "50%": 3,
            "75%": 4,
            "max": 5,
        },
        rel=1e-12,
        abs=1e-12,
    )
    assert report["target_balance"] == [
        {"value": value, "count": 1, "proportion": 1 / 3} for value in [1, 3, 5]
    ]
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize(
    "dtype", ["string", "object", "boolean", "category", "datetime64[ns]"]
)
def test_all_missing_nonnumeric_columns(dtype: str) -> None:
    """Missing targets have no observed balance and use all-row missing rates."""
    frame = pd.DataFrame({"label": pd.Series([None, None], dtype=dtype)})
    report = assess_data(frame, target="label")
    assert report["target_balance"] == []
    column = cast(list[dict[str, object]], report["columns"])[0]
    assert column["missing_count"] == 2
    assert column["missing_rate"] == 1.0
    assert column["frequencies"] == []
    json.dumps(report, allow_nan=False)


def test_caller_index_attrs_and_cwd_are_preserved() -> None:
    """The public helper leaves caller state unchanged."""
    frame = pd.DataFrame({"label": pd.Series(["B", "A", "B"], dtype="string")})
    frame.index = pd.Index([9, 9, 3], name="external")
    frame.attrs = {"project": {"value": [1]}}
    before = frame.copy(deep=True)
    cwd = Path.cwd()
    report = assess_data(frame, target="label")
    assert report["target_balance"] == [
        {"value": "B", "count": 2, "proportion": 2 / 3},
        {"value": "A", "count": 1, "proportion": 1 / 3},
    ]
    pd.testing.assert_frame_equal(frame, before)
    assert frame.attrs == before.attrs
    assert Path.cwd() == cwd


@pytest.mark.parametrize(
    "levels", [[True, False], [1, 2], [1.5, 2.5], [pd.Timestamp("2024-01-01")]]
)
def test_supported_categorical_scalar_levels(levels: list[object]) -> None:
    """Categorical scalar values use the same JSON policy as other columns."""
    frame = pd.DataFrame({"label": pd.Categorical([levels[0]], categories=levels)})
    report = assess_data(frame, target="label")
    expected = (
        levels[0].isoformat() if isinstance(levels[0], pd.Timestamp) else levels[0]
    )
    balance = cast(list[dict[str, object]], report["target_balance"])
    assert balance[0] == {"value": expected, "count": 1, "proportion": 1.0}
    json.dumps(report, allow_nan=False)
