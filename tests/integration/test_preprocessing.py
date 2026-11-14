"""Public train-only preprocessing behavior for US-15-AC-01/02."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from agentic_ml.splitting import create_partitions

pytestmark = pytest.mark.milestone_1


def test_scaler_fits_training_rows_and_preserves_inputs() -> None:
    """Held-out extremes cannot influence training mean or scale."""
    from agentic_ml.preprocessing import fit_preprocessing

    frame = pd.DataFrame(
        {
            "id": range(6),
            "x": [1.0, 3.0, 100.0, 200.0, 1000.0, 2000.0],
            "label": list("ABABAB"),
        }
    )
    before = frame.copy(deep=True)
    _, partition = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        memberships={"train": [0, 1], "validation": [2, 3], "test": [4, 5]},
    )
    saved = json.dumps(partition, allow_nan=False)
    original = Pipeline([("scale", StandardScaler())])
    cwd = Path.cwd()
    fitted, metadata = fit_preprocessing(
        frame,
        partition_record=partition,
        pipeline=original,
        selected_columns=["x"],
        output_schema=[{"name": "x", "dtype": "float64"}],
    )
    np.testing.assert_allclose(
        fitted.transform(frame[["x"]]).ravel(),
        [-1, 1, 98, 198, 998, 1998],
        rtol=1e-12,
        atol=1e-12,
    )
    np.testing.assert_allclose(fitted.transform(pd.DataFrame({"x": [5.0]})), [[3.0]])
    assert not hasattr(original["scale"], "mean_")
    pd.testing.assert_frame_equal(frame, before)
    assert json.dumps(partition, allow_nan=False) == saved
    assert Path.cwd() == cwd
    assert metadata["fit_partition"] == "train"
    assert metadata["partition_record"] == partition
    assert metadata["selected_columns"] == ["x"]
    assert set(metadata) == {
        "schema_version",
        "fit_partition",
        "partition_record",
        "selected_columns",
        "input_schema",
        "output_schema",
        "pipeline",
        "versions",
    }
    assert json.loads(json.dumps(metadata, allow_nan=False)) == metadata


def test_rejects_validation_fit_scope() -> None:
    """Supported fitting cannot claim a held-out fit scope."""
    from agentic_ml.preprocessing import fit_preprocessing

    frame = pd.DataFrame(
        {"id": [0, 1, 2], "x": [1.0, 3.0, 100.0], "label": list("ABA")}
    )
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2]},
    )
    with pytest.raises(ValueError, match="fit_partition"):
        fit_preprocessing(
            frame,
            partition_record=record,
            pipeline=Pipeline([("scale", StandardScaler())]),
            selected_columns=["x"],
            output_schema=[{"name": "x", "dtype": "float64"}],
            fit_partition="validation",
        )


def _source() -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = pd.DataFrame(
        {"id": [0, 1, 2, 3], "x": [1.0, 3.0, 100.0, 200.0], "label": list("ABAB")}
    )
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2, 3]},
    )
    return frame, record


def _fit(
    frame: pd.DataFrame, record: dict[str, Any], **kwargs: Any
) -> tuple[Any, dict[str, object]]:
    from agentic_ml.preprocessing import fit_preprocessing

    options: dict[str, Any] = {
        "pipeline": Pipeline([("scale", StandardScaler())]),
        "selected_columns": ["x"],
        "output_schema": [{"name": "x", "dtype": "float64"}],
    }
    options.update(kwargs)
    return fit_preprocessing(frame, partition_record=record, **options)


def test_rejects_changed_source_values() -> None:
    """Valid IDs cannot conceal a different current source snapshot."""
    frame, record = _source()
    frame.loc[0, "x"] = 99.0
    with pytest.raises(ValueError, match="source"):
        _fit(frame, record)


def test_rejects_duplicate_features() -> None:
    """Repeated selection cannot silently duplicate the learned feature."""
    frame, record = _source()
    with pytest.raises(ValueError, match="selected_columns"):
        _fit(frame, record, selected_columns=["x", "x"])


@pytest.mark.parametrize(
    ("members", "message"),
    [
        ({"train": [0, 1], "test": [1, 2, 3]}, "overlap"),
        ({"train": [0, 0, 1], "test": [2, 3]}, "duplicate"),
        ({"train": [0, 1], "test": [2, 4]}, "unknown"),
        ({"train": [0, 1], "test": [2]}, "coverage"),
        ({"train": [], "test": [0, 1, 2, 3]}, "nonempty"),
        ({"train": [0, 1], "validation": [2], "test": [3]}, "keys"),
    ],
)
def test_reuses_partition_membership_rejections(
    members: dict[str, list[int]], message: str
) -> None:
    """The fitting entrypoint retains existing partition rejection rules."""
    frame, record = _source()
    before = frame.copy(deep=True)
    record["memberships"] = members
    with pytest.raises(ValueError, match=message):
        _fit(frame, record)
    pd.testing.assert_frame_equal(frame, before)


@pytest.mark.parametrize("columns", [[], ["missing"], ["id"], ["label"]])
def test_rejects_invalid_feature_selection(columns: list[str]) -> None:
    """Only explicitly selected feature columns may enter learned fitting."""
    frame, record = _source()
    with pytest.raises(ValueError, match="selected_columns"):
        _fit(frame, record, selected_columns=columns)


def test_two_way_string_ids_and_reordered_index() -> None:
    """Recorded IDs and order select training rows independently of index."""
    frame = pd.DataFrame(
        {"id": ["held", "b", "a"], "x": [100.0, 3.0, 1.0], "label": list("ABA")},
        index=[88, 22, 11],
    )
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": ["a", "b"], "test": ["held"]},
    )
    fitted, metadata = _fit(frame, record)
    np.testing.assert_allclose(fitted.transform(frame[["x"]]).ravel(), [98, 1, -1])
    assert metadata["partition_record"] == record
    assert record["memberships"] == {"train": ["a", "b"], "test": ["held"]}


def test_rejects_declared_output_width_mismatch() -> None:
    """A successful native fit cannot publish a false output schema."""
    frame, record = _source()
    with pytest.raises(ValueError, match="output_schema"):
        _fit(
            frame,
            record,
            output_schema=[
                {"name": "one", "dtype": "float64"},
                {"name": "two", "dtype": "float64"},
            ],
        )


def test_rejects_non_pipeline() -> None:
    """The public result contract requires a native Pipeline input."""
    frame, record = _source()
    with pytest.raises(TypeError, match="pipeline"):
        _fit(frame, record, pipeline=StandardScaler())


def test_imputation_uses_training_statistic_and_records_missing_value() -> None:
    """Imputation learns two despite the held-out value of one hundred."""
    frame = pd.DataFrame(
        {"id": [0, 1, 2, 3], "x": [1.0, np.nan, 3.0, 100.0], "label": list("ABAB")}
    )
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1, 2], "test": [3]},
    )
    fitted, metadata = _fit(
        frame, record, pipeline=Pipeline([("impute", SimpleImputer())])
    )
    np.testing.assert_allclose(fitted.transform(frame[["x"]]).ravel(), [1, 2, 3, 100])
    assert '"missing_value"' in json.dumps(metadata, allow_nan=False)


def test_native_composition_preserves_unseen_category_and_step_order() -> None:
    """Imputation/scaling and encoding reuse training state on unseen values."""
    frame, record = _source()
    frame["cat"] = ["a", "b", "c", "a"]
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2, 3]},
    )
    pipeline = Pipeline(
        [
            (
                "features",
                ColumnTransformer(
                    [
                        (
                            "numeric",
                            Pipeline(
                                [
                                    ("impute", SimpleImputer()),
                                    ("scale", StandardScaler()),
                                ]
                            ),
                            ["x"],
                        ),
                        (
                            "category",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                            ["cat"],
                        ),
                    ]
                ),
            )
        ]
    )
    fitted, metadata = _fit(
        frame,
        record,
        pipeline=pipeline,
        selected_columns=["x", "cat"],
        output_schema=[
            {"name": name, "dtype": "float64"} for name in ["x", "cat_a", "cat_b"]
        ],
    )
    np.testing.assert_allclose(
        fitted.transform(frame[["x", "cat"]]),
        [[-1, 1, 0], [1, 0, 1], [98, 0, 0], [198, 1, 0]],
        rtol=1e-12,
        atol=1e-12,
    )
    assert '"numpy_dtype"' in json.dumps(metadata, allow_nan=False)


def test_rejects_unrecordable_pipeline_settings_before_fit() -> None:
    """An opaque memory setting is a metadata failure before native fitting."""
    frame, record = _source()
    with pytest.raises(TypeError, match="pipeline.*memory"):
        _fit(
            frame,
            record,
            pipeline=Pipeline([("scale", StandardScaler())], memory=object()),
        )


def test_rejects_incompatible_partition_record_version() -> None:
    """Only the consumed versioned record can identify training rows."""
    frame, record = _source()
    record["schema_version"] = "0.9"
    with pytest.raises(ValueError, match="partition_record"):
        _fit(frame, record)


@pytest.mark.parametrize(
    "schema",
    [
        [],
        [{"name": "x"}],
        [{"name": "x", "dtype": "int64"}],
        [{"name": "x", "dtype": "float64"}, {"name": "x", "dtype": "float64"}],
    ],
)
def test_declared_schema_rejections(schema: list[dict[str, str]]) -> None:
    """Missing, duplicate or inaccurate declarations cannot report success."""
    frame, record = _source()
    with pytest.raises(ValueError, match="output_schema"):
        _fit(frame, record, output_schema=schema)


def test_native_fit_error_retains_type_and_stage_context() -> None:
    """Native numeric conversion failure is visible without input mutation."""
    frame = pd.DataFrame(
        {"id": [0, 1, 2], "x": ["bad", "worse", "held"], "label": list("ABA")}
    )
    before = frame.copy(deep=True)
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2]},
    )
    with pytest.raises(ValueError, match="convert") as failure:
        _fit(frame, record)
    assert any("preprocessing training" in note for note in failure.value.__notes__)
    pd.testing.assert_frame_equal(frame, before)


def test_preserves_original_seeded_record_and_independent_metadata() -> None:
    """Supplied reconstruction cannot replace the seed settings or alias input."""
    frame = pd.DataFrame(
        {"id": range(5), "x": [1.0, 2.0, 3.0, 4.0, 5.0], "label": list("ABABA")}
    )
    _, record = create_partitions(
        frame, row_id="id", target="label", layout="train_test", seed=42, test_size=0.4
    )
    before = json.dumps(record, allow_nan=False)
    _, metadata = _fit(frame, record)
    assert metadata["partition_record"] == record
    assert record["method"] == "seeded"
    returned = metadata["partition_record"]
    assert isinstance(returned, dict)
    returned["settings"] = {"changed": True}
    assert json.dumps(record, allow_nan=False) == before


def test_numpy_categories_and_scalar_settings_are_plain_json() -> None:
    """Native explicit categories and scalar limits retain finite JSON values."""
    frame, record = _source()
    fitted, metadata = _fit(
        frame,
        record,
        pipeline=Pipeline(
            [
                (
                    "encode",
                    OneHotEncoder(
                        categories=[np.array([1.0, 3.0, 100.0, 200.0])],
                        max_categories=np.int64(10),
                        sparse_output=False,
                        handle_unknown="ignore",
                    ),
                )
            ]
        ),
        output_schema=[{"name": n, "dtype": "float64"} for n in ["a", "b", "c", "d"]],
    )
    encoded: Any = metadata["pipeline"]
    parameters = encoded["parameters"]["steps"][0][1]["parameters"]
    assert parameters["categories"] == [[1.0, 3.0, 100.0, 200.0]]
    assert parameters["max_categories"] == 10
    assert json.loads(json.dumps(metadata, allow_nan=False)) == metadata
    np.testing.assert_array_equal(fitted.transform(frame[["x"]]), np.eye(4))


def test_rejects_unknown_record_method() -> None:
    """A valid membership cannot conceal unsupported record semantics."""
    frame, record = _source()
    record["method"] = "invented"
    with pytest.raises(ValueError, match="partition_record.*method"):
        _fit(frame, record)


def test_rejects_nonempty_supplied_settings() -> None:
    """Supplied records cannot add unvalidated settings to the handoff."""
    frame, record = _source()
    record["settings"] = {"seed": 4}
    with pytest.raises(ValueError, match="partition_record.*settings"):
        _fit(frame, record)


def test_rejects_malformed_seeded_settings() -> None:
    """Recorded native seeded calls must agree with their effective settings."""
    frame, _ = _source()
    _, record = create_partitions(
        frame, row_id="id", target="label", layout="train_test", seed=42, test_size=0.5
    )
    settings: Any = record["settings"]
    settings["calls"][0]["random_state"] = 43
    with pytest.raises(ValueError, match="partition_record.*settings"):
        _fit(frame, record)


def test_rejects_non_json_record_memberships() -> None:
    """Input records must be plain finite JSON before any successful fit."""
    frame, record = _source()
    record["memberships"]["train"] = [np.int64(0), np.int64(1)]
    with pytest.raises(TypeError, match="partition_record"):
        _fit(frame, record)


@pytest.mark.parametrize(
    "name",
    [
        "bool",
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "float16",
        "float32",
        "float64",
    ],
)
@pytest.mark.parametrize("descriptor", [False, True])
def test_dtype_descriptors_and_sparse_outputs(name: str, descriptor: bool) -> None:
    """Every allowed native dtype retains its canonical tag and sparse shape."""
    frame, record = _source()
    dtype = np.dtype(name)
    if name == "float16":
        with pytest.raises(
            ValueError, match="scipy.sparse does not support dtype float16"
        ) as error:
            _fit(
                frame,
                record,
                pipeline=Pipeline(
                    [
                        (
                            "encode",
                            OneHotEncoder(dtype=dtype if descriptor else dtype.type),
                        )
                    ]
                ),
            )
        assert any("training fit/transform" in note for note in error.value.__notes__)
        return
    fitted, metadata = _fit(
        frame,
        record,
        pipeline=Pipeline(
            [
                (
                    "encode",
                    OneHotEncoder(
                        dtype=dtype if descriptor else dtype.type,
                        handle_unknown="ignore",
                    ),
                )
            ]
        ),
        output_schema=[{"name": n, "dtype": name} for n in ["one", "three"]],
    )
    transformed = fitted.transform(frame[["x"]])
    assert transformed.format == "csr"
    assert transformed.shape == (4, 2)
    np.testing.assert_array_equal(
        transformed.toarray(), [[1, 0], [0, 1], [0, 0], [0, 0]]
    )
    encoded: Any = metadata["pipeline"]
    assert encoded["parameters"]["steps"][0][1]["parameters"]["dtype"] == {
        "kind": "numpy_dtype",
        "name": name,
    }
    assert json.loads(json.dumps(metadata, allow_nan=False)) == metadata


@pytest.mark.parametrize(
    "setting",
    [
        float("nan"),
        float("inf"),
        -float("inf"),
        np.float32("nan"),
        np.float64("inf"),
        {"kind": "numpy_dtype", "name": "float64"},
        {"kind": "missing_value", "value": "nan"},
        {1: "invalid"},
    ],
)
def test_rejects_nonfinite_and_reserved_literal_settings(setting: object) -> None:
    """Only the native imputer sentinel may describe a missing NaN parameter."""
    frame, record = _source()
    with pytest.raises(ValueError, match="pipeline.*memory"):
        _fit(
            frame,
            record,
            pipeline=Pipeline([("scale", StandardScaler())], memory=setting),
        )


@pytest.mark.parametrize(
    "setting", [lambda value: value, np.dtype("complex128"), object()]
)
def test_rejects_callable_and_unsupported_native_settings(setting: object) -> None:
    """No callable, unsupported dtype or opaque object becomes repr metadata."""
    frame, record = _source()
    with pytest.raises(TypeError, match="pipeline.*memory"):
        _fit(
            frame,
            record,
            pipeline=Pipeline([("scale", StandardScaler())], memory=setting),
        )


def test_rejects_cyclic_settings_with_field_context() -> None:
    """Cyclic native settings fail before sklearn cloning recurses."""
    frame, record = _source()
    setting: list[object] = []
    setting.append(setting)
    with pytest.raises(ValueError, match="pipeline.*memory.*cyclic"):
        _fit(
            frame,
            record,
            pipeline=Pipeline([("scale", StandardScaler())], memory=setting),
        )


def test_all_null_native_imputation_rejects_dropped_output_column() -> None:
    """The helper preserves native all-null dropping instead of changing defaults."""
    frame, _ = _source()
    frame["x"] = float("nan")
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2, 3]},
    )
    with pytest.warns(UserWarning, match="Skipping features"):
        with pytest.raises(ValueError, match="output_schema width"):
            _fit(frame, record, pipeline=Pipeline([("impute", SimpleImputer())]))


def test_metadata_retains_effective_defaults_and_ordered_schemas() -> None:
    """Record defaults and declarations independently of fitted internals."""
    frame, record = _source()
    _, metadata = _fit(frame, record)
    assert metadata["input_schema"] == [{"name": "x", "dtype": "float64"}]
    assert metadata["output_schema"] == [{"name": "x", "dtype": "float64"}]
    assert metadata["pipeline"] == {
        "class_name": "sklearn.pipeline.Pipeline",
        "parameters": {
            "memory": None,
            "transform_input": None,
            "verbose": False,
            "steps": [
                [
                    "scale",
                    {
                        "class_name": "sklearn.preprocessing._data.StandardScaler",
                        "parameters": {
                            "copy": True,
                            "with_mean": True,
                            "with_std": True,
                        },
                    },
                ]
            ],
        },
    }
    versions: Any = metadata["versions"]
    assert set(versions) == {"agentic-ml", "pandas", "pyarrow", "scikit-learn"}
    assert all(isinstance(v, str) and v for v in versions.values())


def test_rejects_source_identity_wrong_count_type() -> None:
    """Float/int equality cannot disguise an invalid versioned source field."""
    frame, record = _source()
    record["source"]["row_count"] = 4.0
    with pytest.raises(ValueError, match="source"):
        _fit(frame, record)


def test_native_dataframe_output_checks_each_dtype() -> None:
    """Native pandas output retains ordered per-column dtype validation."""
    frame, record = _source()
    fitted, metadata = _fit(
        frame,
        record,
        pipeline=Pipeline([("scale", StandardScaler())]).set_output(transform="pandas"),
    )
    result = fitted.transform(frame[["x"]])
    assert isinstance(result, pd.DataFrame)
    np.testing.assert_allclose(result["x"], [-1, 1, 98, 198])
    assert metadata["output_schema"] == [{"name": "x", "dtype": "float64"}]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("protocol", None),
        ("settings", []),
        ("method", []),
        ("unknown", "extra"),
        ("schema_version", "2.0"),
    ],
)
def test_rejects_malformed_supplied_record_fields(field: str, value: object) -> None:
    """Unknown or mistyped record fields cannot become successful metadata."""
    frame, record = _source()
    record[field] = value
    with pytest.raises((TypeError, ValueError), match="partition_record"):
        _fit(frame, record)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seed", True),
        ("test_size", float("nan")),
        ("shuffle", 1),
        ("calls", []),
        ("extra", 1),
    ],
)
def test_rejects_seeded_record_field_boundaries(field: str, value: object) -> None:
    """Seeded history retains native types and exact versioned settings keys."""
    frame, _ = _source()
    _, record = create_partitions(
        frame, row_id="id", target="label", layout="train_test", seed=42, test_size=0.5
    )
    settings: Any = record["settings"]
    settings[field] = value
    with pytest.raises((TypeError, ValueError), match="partition_record"):
        _fit(frame, record)


def test_rejects_tuple_membership_in_plain_record() -> None:
    """A versioned record uses JSON arrays even though split inputs allow sequences."""
    frame, record = _source()
    record["memberships"]["train"] = (0, 1)
    with pytest.raises(TypeError, match="partition_record"):
        _fit(frame, record)


def test_dataframe_output_validates_mixed_column_dtypes() -> None:
    """Native heterogeneous output is checked column by column in declared order."""
    frame, _ = _source()
    frame["category"] = ["a", "b", "held", "a"]
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1], "test": [2, 3]},
    )
    pipeline = Pipeline(
        [
            (
                "features",
                ColumnTransformer(
                    [("scale", StandardScaler(), ["x"])], remainder="passthrough"
                ),
            )
        ]
    ).set_output(transform="pandas")
    fitted, metadata = _fit(
        frame,
        record,
        pipeline=pipeline,
        selected_columns=["x", "category"],
        output_schema=[
            {"name": "numeric", "dtype": "float64"},
            {"name": "category", "dtype": "str"},
        ],
    )
    result = fitted.transform(frame[["x", "category"]])
    assert [str(dtype) for dtype in result.dtypes] == ["float64", "str"]
    np.testing.assert_allclose(result.iloc[:, 0], [-1, 1, 98, 198])
    assert result.iloc[:, 1].tolist() == ["a", "b", "held", "a"]
    assert metadata["selected_columns"] == ["x", "category"]
