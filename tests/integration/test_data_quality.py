"""Public data-quality behavior for experiment projects."""

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import cast

import pandas as pd
import pytest

from agentic_ml.data_quality import DataQualityError, run_validated_step, validate_data

pytestmark = pytest.mark.milestone_1


def test_explicit_no_checks_does_not_claim_validation() -> None:
    """Test explicit no checks does not claim validation."""
    frame = pd.DataFrame({"id": pd.Series([1], dtype="int64")})
    assert validate_data(frame, rules=[]) == {
        "schema_version": "1.0",
        "status": "not_checked",
        "blocked": False,
        "row_count": 1,
        "columns": [{"name": "id", "dtype": "int64"}],
        "checks": [],
    }


def test_passing_row_count_reports_measurement() -> None:
    """Test passing row count reports measurement."""
    frame = pd.DataFrame({"id": pd.Series([1, 2], dtype="int64")})
    report = validate_data(frame, rules=[{"id": "rows", "kind": "row_count", "min": 2}])
    assert report["status"] == "passed"
    assert report["blocked"] is False
    assert report["row_count"] == 2
    assert report["columns"] == [{"name": "id", "dtype": "int64"}]
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["expected"] == {"min": 2, "max": None}
    assert checks[0]["actual"] == {"count": 2}
    assert checks[0]["passed"] is True


def test_schema_reports_missing_and_unexpected_columns() -> None:
    """Test schema reports missing and unexpected columns."""
    frame = pd.DataFrame({"id": [1], "extra": [2]})
    report = validate_data(
        frame,
        rules=[
            {
                "id": "schema",
                "kind": "columns",
                "columns": ["id", "age"],
                "exact": True,
            }
        ],
    )
    assert report["status"] == "failed"
    assert report["blocked"] is True
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"missing": ["age"], "unexpected": ["extra"]}
    assert checks[0]["passed"] is False


def test_dtype_mismatch_reports_actual_dtype() -> None:
    """Test dtype mismatch reports actual dtype."""
    report = validate_data(
        pd.DataFrame({"age": pd.Series([1], dtype="Int64")}),
        rules=[
            {"id": "types", "kind": "dtypes", "columns": {"age": "int64"}},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"dtypes": {"age": "Int64"}}
    assert checks[0]["passed"] is False
    assert report["blocked"] is True


def test_unknown_rule_is_rejected() -> None:
    """Test unknown rule is rejected."""
    with pytest.raises(ValueError, match="kind"):
        validate_data(
            pd.DataFrame({"id": [1]}), rules=[{"id": "bad", "kind": "unknown"}]
        )


@pytest.mark.parametrize("minimum", [-1, True, 1.5])
def test_invalid_row_count_minimum_is_rejected(minimum: object) -> None:
    """Test invalid row count minimum is rejected."""
    with pytest.raises((ValueError, TypeError)):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "rows", "kind": "row_count", "min": minimum},
            ],
        )


def test_null_rule_counts_missing_values() -> None:
    """Test null rule counts missing values."""
    report = validate_data(
        pd.DataFrame({"age": pd.Series([1, None], dtype="Int64")}),
        rules=[
            {"id": "present", "kind": "nulls", "column": "age"},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["expected"] == {"column": "age", "max_count": 0}
    assert checks[0]["actual"] == {"count": 1}
    assert report["blocked"] is True


def test_duplicate_rule_counts_excess_rows() -> None:
    """Test duplicate rule counts excess rows."""
    report = validate_data(
        pd.DataFrame({"id": [1, 1, 1, 2]}),
        rules=[
            {"id": "unique", "kind": "duplicates", "columns": ["id"], "max_count": 1},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"count": 2}
    assert report["blocked"] is True


def test_range_counts_invalid_and_missing_values() -> None:
    """Test range counts invalid and missing values."""
    report = validate_data(
        pd.DataFrame({"age": [0.0, 121.0, float("inf"), float("nan")]}),
        rules=[
            {"id": "age", "kind": "range", "column": "age", "min": 0, "max": 120},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"invalid_count": 2, "missing_count": 1}
    assert report["blocked"] is True


def test_allowed_values_excludes_missing_values() -> None:
    """Test allowed values excludes missing values."""
    report = validate_data(
        pd.DataFrame({"group": ["A", "Z", None]}),
        rules=[
            {
                "id": "group",
                "kind": "allowed_values",
                "column": "group",
                "values": ["A", "B"],
            },
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"invalid_count": 1, "missing_count": 1}
    assert report["blocked"] is True


def test_required_failure_blocks_project_step(tmp_path: object) -> None:
    """Test required failure blocks project step."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    sentinel = tmp_path / "ran"

    def step(frame: pd.DataFrame, settings: dict[str, object]) -> None:
        sentinel.write_text("ran")

    with pytest.raises(DataQualityError) as error:
        run_validated_step(
            pd.DataFrame({"id": [1]}),
            step,
            rules=[
                {"id": "rows", "kind": "row_count", "min": 2},
            ],
        )
    assert not sentinel.exists()
    assert error.value.report["blocked"] is True
    assert "rows" in str(error.value)


def test_missing_referenced_column_is_an_advisory_failure() -> None:
    """Test missing referenced column is an advisory failure."""
    report = validate_data(
        pd.DataFrame({"id": [1]}),
        rules=[
            {"id": "age", "kind": "nulls", "column": "age", "required": False},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"missing_columns": ["age"]}
    assert report["status"] == "failed"
    assert report["blocked"] is False


def test_non_scalar_object_cells_are_rejected_even_without_rules() -> None:
    """Test non scalar object cells are rejected even without rules."""
    with pytest.raises(TypeError):
        validate_data(pd.DataFrame({"values": [[1, 2]]}), rules=[])


def test_duplicate_rule_ids_are_rejected_before_measurement() -> None:
    """Test duplicate rule ids are rejected before measurement."""
    with pytest.raises(ValueError, match="id"):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "same", "kind": "row_count", "min": 1},
                {"id": "same", "kind": "row_count", "min": 1},
            ],
        )


def test_step_mutations_do_not_change_caller_inputs() -> None:
    """Test step mutations do not change caller inputs."""
    frame = pd.DataFrame({"id": [1]})
    settings: dict[str, object] = {"values": [1]}

    def step(data: pd.DataFrame, options: dict[str, object]) -> int:
        data.loc[0, "id"] = 2
        values = options["values"]
        assert isinstance(values, list)
        values.append(2)
        return 7

    result, report = run_validated_step(frame, step, rules=[], settings=settings)
    assert result == 7 and report["status"] == "not_checked"
    assert frame.loc[0, "id"] == 1
    assert settings == {"values": [1]}


def test_invalid_settings_rejected_before_step() -> None:
    """Test invalid settings rejected before step."""
    invoked: list[bool] = []

    def step(data: pd.DataFrame, options: dict[str, object]) -> None:
        invoked.append(True)

    with pytest.raises((TypeError, ValueError)):
        run_validated_step(
            pd.DataFrame({"id": [1]}), step, rules=[], settings={"bad": float("nan")}
        )
    assert not invoked


def test_project_exception_keeps_identity_and_stage_note() -> None:
    """Test project exception keeps identity and stage note."""
    failure = RuntimeError("project failed")

    def step(data: pd.DataFrame, options: dict[str, object]) -> None:
        raise failure

    with pytest.raises(RuntimeError) as error:
        run_validated_step(pd.DataFrame({"id": [1]}), step, rules=[])
    assert error.value is failure
    assert any("validated" in note for note in error.value.__notes__)


def test_unknown_rule_key_is_rejected() -> None:
    """Test unknown rule key is rejected."""
    with pytest.raises(ValueError, match="key"):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "rows", "kind": "row_count", "min": 1, "typo": 4},
            ],
        )


@pytest.mark.parametrize("columns", [["", "x"], ["x", "x"], [1, "x"]])
def test_invalid_frame_column_names_are_rejected(columns: list[object]) -> None:
    """Test invalid frame column names are rejected."""
    frame = pd.DataFrame([[1, 2]], columns=columns)
    with pytest.raises(ValueError):
        validate_data(frame, rules=[])


def test_inverted_row_count_bounds_are_rejected() -> None:
    """Test inverted row count bounds are rejected."""
    with pytest.raises(ValueError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "rows", "kind": "row_count", "min": 3, "max": 2},
            ],
        )


def test_range_on_string_dtype_is_a_reported_failure() -> None:
    """Test range on string dtype is a reported failure."""
    report = validate_data(
        pd.DataFrame({"age": pd.Series(["young"], dtype="str")}),
        rules=[
            {"id": "age", "kind": "range", "column": "age", "min": 0},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"dtype": "str", "reason": "non_real_numeric"}
    assert report["blocked"] is True


def test_duplicate_rule_on_zero_columns_is_a_reported_failure() -> None:
    """Test duplicate rule on zero columns is a reported failure."""
    report = validate_data(
        pd.DataFrame(index=[0, 1]),
        rules=[
            {"id": "unique", "kind": "duplicates"},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"reason": "no_columns"}
    assert report["blocked"] is True


@pytest.mark.parametrize(
    "rule",
    [
        {"id": "r", "kind": "row_count"},
        {"id": "r", "kind": "columns", "columns": []},
        {"id": "r", "kind": "nulls"},
        {"id": "r", "kind": "allowed_values", "column": "id", "values": []},
    ],
)
def test_missing_rule_parameters_are_rejected(rule: dict[str, object]) -> None:
    """Test missing rule parameters are rejected."""
    with pytest.raises(ValueError):
        validate_data(pd.DataFrame({"id": [1]}), rules=[rule])


@pytest.mark.parametrize(
    "rule",
    [
        {"id": "r", "kind": "nulls", "column": "id", "required": "yes"},
        {"id": "r", "kind": "duplicates", "columns": ["id"], "max_count": True},
        {"id": "r", "kind": "columns", "columns": "id"},
    ],
)
def test_wrong_rule_parameter_types_are_rejected(rule: dict[str, object]) -> None:
    """Test wrong rule parameter types are rejected."""
    with pytest.raises(TypeError):
        validate_data(pd.DataFrame({"id": [1]}), rules=[rule])


@pytest.mark.parametrize(
    "bounds", [{"min": float("nan")}, {"min": True}, {"min": 2, "max": 1}]
)
def test_invalid_range_bounds_are_rejected(bounds: dict[str, object]) -> None:
    """Test invalid range bounds are rejected."""
    with pytest.raises((ValueError, TypeError)):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "r", "kind": "range", "column": "id", **bounds},
            ],
        )


@pytest.mark.parametrize("columns", [["id", "id"], [""], []])
def test_invalid_duplicate_column_lists_are_rejected(columns: list[str]) -> None:
    """Test invalid duplicate column lists are rejected."""
    with pytest.raises(ValueError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "r", "kind": "duplicates", "columns": columns},
            ],
        )


@pytest.mark.parametrize(
    "rule",
    [
        {"kind": "row_count", "min": 1},
        {"id": "", "kind": "row_count", "min": 1},
    ],
)
def test_missing_or_empty_rule_id_is_rejected(rule: dict[str, object]) -> None:
    """Test missing or empty rule id is rejected."""
    with pytest.raises(ValueError):
        validate_data(pd.DataFrame({"id": [1]}), rules=[rule])


def test_each_operation_rechecks_current_data(tmp_path: object) -> None:
    """Test each operation rechecks current data."""
    from pathlib import Path

    assert isinstance(tmp_path, Path)
    sentinel = tmp_path / "runs"
    frame = pd.DataFrame({"age": [20]})
    rules = [{"id": "age", "kind": "range", "column": "age", "max": 120}]

    def step(data: pd.DataFrame, options: dict[str, object]) -> None:
        sentinel.write_text(str(data.loc[0, "age"]))

    run_validated_step(frame, step, rules=rules)
    assert sentinel.read_text() == "20"
    frame.loc[0, "age"] = 121
    with pytest.raises(DataQualityError):
        run_validated_step(frame, step, rules=rules)
    assert sentinel.read_text() == "20"


def test_nested_settings_require_string_keys() -> None:
    """Test nested settings require string keys."""

    def step(data: pd.DataFrame, options: dict[str, object]) -> None:
        raise AssertionError("must not run")

    with pytest.raises(TypeError):
        run_validated_step(
            pd.DataFrame({"id": [1]}), step, rules=[], settings={"nested": {1: "x"}}
        )


@pytest.mark.parametrize("rules", [None, "", {}, ["bad"]])
def test_invalid_rule_container_is_rejected(rules: object) -> None:
    """Test invalid rule container is rejected."""
    with pytest.raises(TypeError):
        validate_data(
            pd.DataFrame({"id": [1]}), rules=cast(Sequence[Mapping[str, object]], rules)
        )


def test_report_does_not_alias_rule_declarations() -> None:
    """Test report does not alias rule declarations."""
    rules: list[dict[str, object]] = [
        {"id": "groups", "kind": "allowed_values", "column": "group", "values": ["A"]}
    ]
    report = validate_data(pd.DataFrame({"group": ["A"]}), rules=rules)
    checks = report["checks"]
    assert isinstance(checks, list)
    checks[0]["expected"]["values"].append("B")
    assert rules[0]["values"] == ["A"]


@pytest.mark.parametrize("values", [[None], [float("inf")], [{"x": 1}]])
def test_invalid_allowed_values_are_rejected(values: list[object]) -> None:
    """Test invalid allowed values are rejected."""
    with pytest.raises((TypeError, ValueError)):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "r", "kind": "allowed_values", "column": "id", "values": values},
            ],
        )


def test_dtype_rule_accepts_mapping_and_normalizes_dtype() -> None:
    """Test dtype rule accepts mapping and normalizes dtype."""
    from types import MappingProxyType

    report = validate_data(
        pd.DataFrame({"id": [1]}),
        rules=[
            {"id": "r", "kind": "dtypes", "columns": MappingProxyType({"id": "int64"})},
        ],
    )
    assert report["status"] == "passed"


@pytest.mark.parametrize("column", [None, 3, ""])
def test_invalid_column_argument_is_rejected(column: object) -> None:
    """Test invalid column argument is rejected."""
    with pytest.raises((TypeError, ValueError)):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "r", "kind": "nulls", "column": column},
            ],
        )


def test_noncallable_step_is_rejected_before_quality_check() -> None:
    """Test noncallable step is rejected before quality check."""
    with pytest.raises(TypeError):
        run_validated_step(
            pd.DataFrame({"id": [1]}),
            cast(Callable[[pd.DataFrame, dict[str, object]], None], None),
            rules=[
                {"id": "r", "kind": "row_count", "min": 2},
            ],
        )


def test_non_boolean_exact_is_rejected() -> None:
    """Reject a non-boolean exact setting."""
    with pytest.raises(TypeError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[{"id": "r", "kind": "columns", "columns": ["id"], "exact": 1}],
        )


def test_wrong_dtype_declaration_type_is_rejected() -> None:
    """Reject a non-string pandas dtype declaration."""
    with pytest.raises(TypeError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[{"id": "r", "kind": "dtypes", "columns": {"id": int}}],
        )


def test_advisory_failure_runs_step_and_report_is_json_serializable(
    tmp_path: Path,
) -> None:
    """An advisory failure remains visible without blocking the step."""
    import json

    called: list[int] = []
    sentinel = tmp_path / "ran"

    def step(data: pd.DataFrame, options: dict[str, object]) -> int:
        called.append(len(data))
        sentinel.write_text(str(data.loc[0, "id"]))
        return 9

    result, report = run_validated_step(
        pd.DataFrame({"id": [1]}),
        step,
        rules=[{"id": "rows", "kind": "row_count", "min": 2, "required": False}],
    )
    assert result == 9 and called == [1]
    assert sentinel.read_text() == "1"
    assert report["status"] == "failed" and report["blocked"] is False
    assert json.loads(json.dumps(report, allow_nan=False)) == report


def test_non_string_rule_id_is_type_error() -> None:
    """Distinguish an invalid ID type from a missing ID."""
    with pytest.raises(TypeError):
        validate_data(
            pd.DataFrame({"id": [1]}), rules=[{"id": 0, "kind": "row_count", "min": 1}]
        )


def test_invalid_pandas_dtype_is_a_value_error() -> None:
    """Invalid dtype text is malformed configuration."""
    with pytest.raises(ValueError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=[
                {"id": "r", "kind": "dtypes", "columns": {"id": "not-a-dtype"}},
            ],
        )


def test_seven_rule_baseline_reports_independent_measurements() -> None:
    """All configured rule families can evaluate together in declaration order."""
    frame = pd.DataFrame(
        {
            "id": pd.Series([1, 2, 3, 4], dtype="int64"),
            "age": pd.Series([20, 35, 40, 50], dtype="int64"),
            "group": pd.Series(["A", "B", "A", "C"], dtype="str"),
        }
    )
    rules: list[dict[str, object]] = [
        {
            "id": "schema",
            "kind": "columns",
            "columns": ["id", "age", "group"],
            "exact": True,
        },
        {"id": "types", "kind": "dtypes", "columns": {"id": "int64", "age": "int64"}},
        {"id": "rows", "kind": "row_count", "min": 4, "max": 4},
        {"id": "present", "kind": "nulls", "column": "age"},
        {"id": "unique", "kind": "duplicates", "columns": ["id"]},
        {"id": "range", "kind": "range", "column": "age", "min": 0, "max": 120},
        {
            "id": "group",
            "kind": "allowed_values",
            "column": "group",
            "values": ["A", "B", "C"],
        },
    ]
    report = validate_data(frame, rules=rules)
    checks = report["checks"]
    assert isinstance(checks, list)
    assert report["status"] == "passed" and not report["blocked"]
    assert [check["actual"] for check in checks] == [
        {"missing": [], "unexpected": []},
        {"dtypes": {"id": "int64", "age": "int64"}},
        {"count": 4},
        {"count": 0},
        {"count": 0},
        {"invalid_count": 0, "missing_count": 0},
        {"invalid_count": 0, "missing_count": 0},
    ]


def test_non_dataframe_is_rejected_by_step_boundary() -> None:
    """A bad frame fails before any operation is called."""
    with pytest.raises(TypeError):
        run_validated_step(
            cast(pd.DataFrame, None), lambda data, settings: None, rules=[]
        )


@pytest.mark.parametrize("kind", [None, 0, []])
def test_non_string_rule_kind_is_type_error(kind: object) -> None:
    """A present but invalid kind type is a configuration type error."""
    with pytest.raises(TypeError):
        validate_data(
            pd.DataFrame({"id": [1]}),
            rules=cast(Sequence[Mapping[str, object]], [{"id": "r", "kind": kind}]),
        )


def test_all_null_nullable_range_and_null_checks() -> None:
    """Range excludes missing values while the null rule counts them."""
    frame = pd.DataFrame({"age": pd.Series([None, None, None, None], dtype="Int64")})
    report = validate_data(
        frame,
        rules=[
            {"id": "present", "kind": "nulls", "column": "age"},
            {"id": "bounds", "kind": "range", "column": "age", "min": 0, "max": 120},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"count": 4}
    assert checks[1]["actual"] == {"invalid_count": 0, "missing_count": 4}
    assert checks[1]["passed"] is True and report["blocked"] is True


def test_no_checks_runs_sentinel_step(tmp_path: Path) -> None:
    """Explicitly unchecked input can reach a project operation."""
    sentinel = tmp_path / "ran"

    def step(data: pd.DataFrame, options: dict[str, object]) -> str:
        sentinel.write_text(str(data.loc[0, "age"]))
        return "done"

    result, report = run_validated_step(pd.DataFrame({"age": [999]}), step, rules=[])
    assert result == "done" and sentinel.read_text() == "999"
    assert report["status"] == "not_checked" and report["checks"] == []


def test_settings_support_nested_read_only_mappings() -> None:
    """String-keyed mappings need not be mutable dictionaries."""
    from types import MappingProxyType

    result, _ = run_validated_step(
        pd.DataFrame({"id": [1]}),
        lambda data, settings: settings,
        rules=[],
        settings={"nested": MappingProxyType({"x": [1]})},
    )
    assert result == {"nested": {"x": [1]}}


def test_complex_object_cell_is_rejected() -> None:
    """Unsupported scalar categories cannot escape the snapshot boundary."""
    with pytest.raises(TypeError):
        validate_data(pd.DataFrame({"id": pd.Series([1 + 2j], dtype=object)}), rules=[])


def test_mixed_required_and_advisory_failures_report_both(tmp_path: Path) -> None:
    """Only required failures block, and every configured result remains visible."""
    sentinel = tmp_path / "ran"

    def step(data: pd.DataFrame, options: dict[str, object]) -> None:
        sentinel.write_text("ran")

    rules: list[dict[str, object]] = [
        {"id": "advisory", "kind": "row_count", "min": 2, "required": False},
        {"id": "required", "kind": "nulls", "column": "missing"},
    ]
    with pytest.raises(DataQualityError) as error:
        run_validated_step(pd.DataFrame({"id": [1]}), step, rules=rules)
    checks = error.value.report["checks"]
    assert isinstance(checks, list)
    assert [check["passed"] for check in checks] == [False, False]
    assert "required" in str(error.value) and "advisory" not in str(error.value)
    assert not sentinel.exists()


@pytest.mark.parametrize(
    "kind,key",
    [("columns", "columns"), ("dtypes", "columns"), ("allowed_values", "values")],
)
def test_none_rule_parameter_is_type_error(kind: str, key: str) -> None:
    """Present parameters of the wrong type are not missing parameters."""
    rule: dict[str, object] = {"id": "r", "kind": kind, key: None}
    if kind == "allowed_values":
        rule["column"] = "id"
    with pytest.raises(TypeError):
        validate_data(pd.DataFrame({"id": [1]}), rules=[rule])


def test_duplicate_defaults_use_all_columns_and_ignore_index() -> None:
    """Duplicate checks compare row values rather than index labels."""
    frame = pd.DataFrame({"id": [1, 1, 2], "group": ["A", "A", "A"]}, index=[7, 7, 7])
    report = validate_data(frame, rules=[{"id": "dup", "kind": "duplicates"}])
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["expected"] == {"columns": ["id", "group"], "max_count": 0}
    assert checks[0]["actual"] == {"count": 1}


def test_empty_frame_preserves_schema_and_fails_row_minimum() -> None:
    """An empty frame is evaluated without losing its declared schema."""
    frame = pd.DataFrame({"age": pd.Series([], dtype="Int64")})
    report = validate_data(
        frame,
        rules=[
            {"id": "types", "kind": "dtypes", "columns": {"age": "Int64"}},
            {"id": "rows", "kind": "row_count", "min": 1},
            {"id": "present", "kind": "nulls", "column": "age"},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert [check["passed"] for check in checks] == [True, False, True]
    assert checks[1]["actual"] == {"count": 0}


def test_unsupported_period_object_is_rejected() -> None:
    """Unsupported object scalar families are not part of the snapshot contract."""
    frame = pd.DataFrame(
        {"value": pd.Series([pd.Period("2020-01", freq="M")], dtype=object)}
    )
    with pytest.raises(TypeError):
        validate_data(frame, rules=[])


def test_decimal_object_values_are_supported() -> None:
    """Scalar numeric object values are allowed without recursive copying."""
    from decimal import Decimal

    frame = pd.DataFrame({"value": pd.Series([Decimal("1.2")], dtype=object)})
    assert validate_data(frame, rules=[])["status"] == "not_checked"


def test_custom_object_with_datetime_dtype_is_rejected() -> None:
    """A custom object cannot impersonate a scalar via a dtype attribute."""

    class PretendScalar:
        dtype = "datetime64[ns]"

    frame = pd.DataFrame({"value": pd.Series([PretendScalar()], dtype=object)})
    with pytest.raises(TypeError):
        validate_data(frame, rules=[])


def test_row_count_failure_message_identifies_limit() -> None:
    """A failed row count report states the measured and required limits."""
    report = validate_data(
        pd.DataFrame({"id": [1, 2, 3]}),
        rules=[
            {"id": "rows", "kind": "row_count", "max": 2},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"count": 3}
    assert "3" in checks[0]["message"] and "2" in checks[0]["message"]
    assert report["blocked"] is True


def test_inclusive_range_and_native_missing_duplicate_keys() -> None:
    """Bounds include endpoints and duplicate keys use pandas missing equality."""
    frame = pd.DataFrame({"age": [0, 120, 40, 50], "key": [None, None, "a", "b"]})
    report = validate_data(
        frame,
        rules=[
            {"id": "range", "kind": "range", "column": "age", "min": 0, "max": 120},
            {"id": "dup", "kind": "duplicates", "columns": ["key"], "max_count": 1},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"invalid_count": 0, "missing_count": 0}
    assert checks[1]["actual"] == {"count": 1}
    assert report["status"] == "passed"


def test_missing_columns_fail_each_affected_rule_without_stopping_others() -> None:
    """Report missing columns for every affected check in supplied order."""
    report = validate_data(
        pd.DataFrame({"id": [1]}),
        rules=[
            {"id": "schema", "kind": "columns", "columns": ["id", "age"]},
            {"id": "types", "kind": "dtypes", "columns": {"age": "int64"}},
            {"id": "nulls", "kind": "nulls", "column": "age"},
            {"id": "range", "kind": "range", "column": "age", "min": 0},
            {"id": "rows", "kind": "row_count", "min": 1},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["actual"] == {"missing": ["age"], "unexpected": []}
    assert [check["actual"] for check in checks[1:4]] == [
        {"missing_columns": ["age"]}
    ] * 3
    assert [check["passed"] for check in checks] == [False, False, False, False, True]


def test_validate_data_does_not_mutate_inputs() -> None:
    """Checks preserve both the caller's frame and rule declarations."""
    from copy import deepcopy

    frame = pd.DataFrame({"id": [1, 1], "age": [0.0, float("nan")]})
    original = frame.copy(deep=True)
    rules: list[dict[str, object]] = [
        {"id": "dup", "kind": "duplicates", "columns": ["id"]},
        {"id": "range", "kind": "range", "column": "age", "min": 0},
    ]
    original_rules = deepcopy(rules)
    validate_data(frame, rules=rules)
    pd.testing.assert_frame_equal(frame, original)
    assert rules == original_rules


def test_numpy_boolean_scalar_in_object_column_is_supported() -> None:
    """Object columns may contain native scalar booleans."""
    import numpy as np

    frame = pd.DataFrame({"flag": pd.Series([np.bool_(True)], dtype=object)})
    assert validate_data(frame, rules=[])["status"] == "not_checked"


def test_custom_categorical_values_are_rejected() -> None:
    """Categorical values must also satisfy the scalar snapshot contract."""

    class MutableValue:
        pass

    frame = pd.DataFrame({"value": pd.Categorical([MutableValue()])})
    with pytest.raises(TypeError):
        validate_data(frame, rules=[])


def test_unused_custom_category_is_rejected() -> None:
    """Unused categorical metadata must not alias mutable custom values."""

    class MutableValue:
        pass

    frame = pd.DataFrame(
        {"value": pd.Categorical(["a"], categories=["a", MutableValue()])}
    )
    with pytest.raises(TypeError):
        validate_data(frame, rules=[])


@pytest.mark.parametrize(
    "case,expected_failed",
    [
        ("missing_age", ["schema", "types", "present", "bounds"]),
        ("extra", ["schema"]),
        ("float_age", ["types"]),
        ("short", ["rows"]),
        ("long", ["rows"]),
        ("duplicate", ["unique"]),
        ("out_of_range", ["bounds"]),
        ("unknown_group", ["groups"]),
    ],
)
def test_baseline_mutations_have_expected_failures(
    case: str, expected_failed: list[str]
) -> None:
    """Independent mutations each fail the contract's specified checks."""
    frame = pd.DataFrame(
        {
            "id": pd.Series([1, 2, 3, 4], dtype="int64"),
            "age": pd.Series([20, 35, 40, 50], dtype="int64"),
            "group": pd.Series(["A", "B", "A", "C"], dtype="str"),
        }
    )
    if case == "missing_age":
        frame = frame.drop(columns="age")
    elif case == "extra":
        frame["extra"] = 1
    elif case == "float_age":
        frame["age"] = frame["age"].astype("float64")
    elif case == "short":
        frame = frame.iloc[:-1].copy()
    elif case == "long":
        extra = frame.iloc[[0]].copy()
        extra.loc[0, "id"] = 5
        extra.loc[0, "age"] = 60
        frame = pd.concat([frame, extra], ignore_index=True)
    elif case == "duplicate":
        frame.loc[1, "id"] = 1
    elif case == "out_of_range":
        frame.loc[0, "age"] = 121
    else:
        frame.loc[0, "group"] = "Z"
    rules: list[dict[str, object]] = [
        {
            "id": "schema",
            "kind": "columns",
            "columns": ["id", "age", "group"],
            "exact": True,
        },
        {"id": "types", "kind": "dtypes", "columns": {"id": "int64", "age": "int64"}},
        {"id": "rows", "kind": "row_count", "min": 4, "max": 4},
        {"id": "present", "kind": "nulls", "column": "age"},
        {"id": "unique", "kind": "duplicates", "columns": ["id"]},
        {"id": "bounds", "kind": "range", "column": "age", "min": 0, "max": 120},
        {
            "id": "groups",
            "kind": "allowed_values",
            "column": "group",
            "values": ["A", "B", "C"],
        },
    ]
    report = validate_data(frame, rules=rules)
    checks = report["checks"]
    assert isinstance(checks, list)
    assert [check["id"] for check in checks if not check["passed"]] == expected_failed
    assert report["blocked"] is True


def test_nonexact_schema_allows_extra_columns() -> None:
    """The default schema check requires names without forbidding extras."""
    report = validate_data(
        pd.DataFrame({"id": [1], "extra": [2]}),
        rules=[
            {"id": "schema", "kind": "columns", "columns": ["id"]},
        ],
    )
    checks = report["checks"]
    assert isinstance(checks, list)
    assert checks[0]["expected"] == {"columns": ["id"], "exact": False}
    assert checks[0]["actual"] == {"missing": [], "unexpected": []}
    assert report["status"] == "passed"
