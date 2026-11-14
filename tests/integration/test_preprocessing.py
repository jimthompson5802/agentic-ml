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
