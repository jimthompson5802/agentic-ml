"""US-18 M1 classification through the approved public fitting boundary."""

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
import pytest
import yaml
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from test_planning import planning_project as planning_project

from agentic_ml.planning import ResolveRequest, resolve_plan
from agentic_ml.planning.models import JSONValue
from agentic_ml.splitting import create_partitions
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    validate_configuration,
)

pytestmark = pytest.mark.milestone_1


@pytest.fixture
def training_project(planning_project: Path) -> Path:
    """Prepare real strict classification inputs in an independent project."""
    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace("logistic_regression", "dummy_classifier")
    )
    (planning_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_classifier": {
                        "fixed": {"strategy": "most_frequent"},
                        "search": {},
                    }
                },
            }
        )
    )
    return planning_project


def candidate_for(
    root: Path, algorithm: str = "dummy_classifier", registry: Path | None = None
) -> CandidateRequest:
    """Resolve and validate genuine strict inputs using public APIs."""
    plan = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert plan.plan_id is not None, plan.diagnostics
    validated = validate_configuration(
        ConfigurationRequest(root, plan.plan_id, registry)
    )
    assert validated.validation_id is not None, validated.diagnostics
    return CandidateRequest(root, validated.validation_id, algorithm, {})


def source_frame() -> pd.DataFrame:
    """Use independently specified labels and held-out extremes."""
    return pd.DataFrame(
        {
            "id": range(8),
            "x": [-3.0, -1.0, 1.0, 3.0, -2.0, 2.0, -100.0, 100.0],
            "label": [0, 0, 1, 1, 0, 1, 1, 0],
        }
    )


def test_baseline_constructs_fits_and_preserves_inputs(training_project: Path) -> None:
    """AC-01/02/03/04: baseline predicts literal labels without held-out fit."""
    from agentic_ml.training import fit_classifier

    candidate = candidate_for(training_project)
    frame = source_frame()
    before = frame.copy(deep=True)
    _, partition = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
    )
    saved = json.dumps(partition, sort_keys=True)
    preprocessing = Pipeline([("scale", StandardScaler())])
    cwd = Path.cwd()
    fitted, record = fit_classifier(
        frame,
        project_root=training_project,
        candidate=candidate,
        estimator_bindings={"dummy_classifier": DummyClassifier},
        preprocessing=preprocessing,
        partition_record=partition,
        selected_columns=["x"],
        output_schema=[{"name": "x", "dtype": "float64"}],
    )
    assert fitted.predict(frame.iloc[4:6][["x"]]).tolist() == [0, 0]
    np.testing.assert_allclose(
        fitted["preprocessing"].transform(pd.DataFrame({"x": [0.0, 100.0]})),
        [[0.0], [100.0 / np.sqrt(5.0)]],
        rtol=1e-12,
        atol=1e-12,
    )
    assert fitted.classes_.tolist() == [0, 1]
    assert record["parameters"] == {
        "strategy": "most_frequent",
        "constant": None,
        "random_state": None,
    }
    assert record["parameter_origins"] == {
        "strategy": "fixed",
        "constant": "default",
        "random_state": "default",
    }
    assert record["estimator_class"] == {
        "module": "sklearn.dummy",
        "qualname": "DummyClassifier",
    }
    assert record["fit_partition"] == "train"
    assert record["classes"] == [0, 1]
    assert record["validation_id"] == candidate.validation_id
    assert json.loads(json.dumps(record, allow_nan=False)) == record
    pd.testing.assert_frame_equal(frame, before)
    assert json.dumps(partition, sort_keys=True) == saved
    assert not hasattr(preprocessing["scale"], "mean_")
    assert Path.cwd() == cwd


TREE_PARAMETERS: dict[str, JSONValue] = {
    "ccp_alpha": 0.0,
    "class_weight": None,
    "criterion": "gini",
    "max_depth": 1,
    "max_features": None,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "min_weight_fraction_leaf": 0.0,
    "monotonic_cst": None,
    "random_state": 17,
    "splitter": "best",
}


def declared_candidate(
    root: Path, algorithm: str, parameters: dict[str, JSONValue]
) -> CandidateRequest:
    """Use independently declared complete scalar profiles, not estimator introspection."""
    brief = root / "brief.md"
    brief.write_text(brief.read_text().replace("dummy_classifier", algorithm))
    (root / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {algorithm: {"fixed": parameters, "search": {}}},
            }
        )
    )
    kinds = {
        type(None): "null",
        bool: "boolean",
        int: "integer",
        float: "float",
        str: "string",
    }
    (root / "registry.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": [
                    {
                        "id": algorithm,
                        "interface_version": "1.0",
                        "tasks": ["classification"],
                        "adapter": {"id": "project_classifier", "version": "1.0"},
                        "library": {
                            "distribution": "scikit-learn",
                            "reference_version": "1.9.1",
                        },
                        "parameters": {
                            name: {"types": [kinds[type(value)]], "default": value}
                            for name, value in parameters.items()
                        },
                        "requires_non_null": [],
                    }
                ],
            }
        )
    )
    return candidate_for(root, algorithm, Path("registry.yaml"))


def fit_case(
    root: Path,
    candidate: CandidateRequest,
    bindings: Mapping[str, type[BaseEstimator]],
    *,
    frame: pd.DataFrame | None = None,
    partition_record: Mapping[str, object] | None = None,
    selected_columns: Sequence[str] = ("x",),
    fit_partition: str = "train",
    preprocessing: Pipeline | None = None,
    output_schema: Sequence[Mapping[str, str]] | None = None,
) -> tuple[Pipeline, dict[str, object]]:
    """Invoke the public helper with a valid controlled source by default."""
    from agentic_ml.training import fit_classifier

    if frame is None:
        frame = source_frame()
    if partition_record is None:
        _, partition_record = create_partitions(
            frame,
            row_id="id",
            target="label",
            layout="train_validation_test",
            memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
        )
    if preprocessing is None:
        preprocessing = Pipeline([("scale", StandardScaler())])
    if output_schema is None:
        output_schema = [{"name": "x", "dtype": "float64"}]
    return fit_classifier(
        frame,
        project_root=root,
        candidate=candidate,
        estimator_bindings=bindings,
        preprocessing=preprocessing,
        partition_record=partition_record,
        selected_columns=selected_columns,
        output_schema=output_schema,
        fit_partition=fit_partition,
    )


def test_rejects_metadata_that_omits_native_defaults(training_project: Path) -> None:
    """AC-04: native constructor defaults cannot silently bypass complete metadata."""
    from sklearn.tree import DecisionTreeClassifier

    parameters = dict(TREE_PARAMETERS)
    del parameters["class_weight"]
    candidate = declared_candidate(training_project, "tree", parameters)
    with pytest.raises(ValueError, match="parameters"):
        fit_case(training_project, candidate, {"tree": DecisionTreeClassifier})


def test_rejects_mismatched_project_root(
    training_project: Path, tmp_path: Path
) -> None:
    """AC-01/04: evidence from one project cannot train through another root."""
    candidate = candidate_for(training_project)
    with pytest.raises(ValueError, match="project_root"):
        fit_case(tmp_path, candidate, {"dummy_classifier": DummyClassifier})


def test_rejects_absent_estimator_binding(training_project: Path) -> None:
    """AC-01/03: a missing class binding has an actionable public error."""
    candidate = candidate_for(training_project)
    with pytest.raises(ValueError, match="binding.*dummy_classifier"):
        fit_case(training_project, candidate, {})


def test_rejects_regressor_binding_before_preprocessing(training_project: Path) -> None:
    """AC-01/03: a valid native regressor is not a classifier extension."""
    from sklearn.dummy import DummyRegressor

    candidate = declared_candidate(
        training_project,
        "regressor",
        {"strategy": "mean", "constant": None, "quantile": None},
    )
    with pytest.raises(ValueError, match="classifier"):
        fit_case(training_project, candidate, {"regressor": DummyRegressor})


@pytest.mark.parametrize("field", ["task", "library"])
def test_rejects_incompatible_configuration_identity(
    training_project: Path, field: str
) -> None:
    """AC-01/04: native bindings cannot change the validated task/framework."""
    declared_candidate(
        training_project,
        "metadata",
        {"strategy": "most_frequent", "constant": None, "random_state": None},
    )
    registry = yaml.safe_load((training_project / "registry.yaml").read_text())
    if field == "task":
        brief = training_project / "brief.md"
        brief.write_text(
            brief.read_text().replace(
                "task_type: classification", "task_type: regression"
            )
        )
        registry["algorithms"][0]["tasks"] = ["regression"]
    else:
        registry["algorithms"][0]["library"] = {
            "distribution": "pandas",
            "reference_version": "3.1.0",
        }
    (training_project / "registry.yaml").write_text(yaml.safe_dump(registry))
    candidate = candidate_for(training_project, "metadata", Path("registry.yaml"))
    with pytest.raises(ValueError, match=field):
        fit_case(training_project, candidate, {"metadata": DummyClassifier})


FOREST_PARAMETERS: dict[str, JSONValue] = {
    "bootstrap": False,
    "ccp_alpha": 0.0,
    "class_weight": None,
    "criterion": "gini",
    "max_depth": 1,
    "max_features": None,
    "max_leaf_nodes": None,
    "max_samples": None,
    "min_impurity_decrease": 0.0,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "min_weight_fraction_leaf": 0.0,
    "monotonic_cst": None,
    "n_estimators": 3,
    "n_jobs": 1,
    "oob_score": False,
    "random_state": 17,
    "verbose": 0,
    "warm_start": False,
}


@pytest.mark.parametrize("algorithm", ["tree", "forest"])
def test_project_classes_construct_fresh_predictive_pipelines(
    training_project: Path, algorithm: str
) -> None:
    """AC-01/03/04: project bindings alone extend fitting to native classifiers."""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier

    parameters = TREE_PARAMETERS if algorithm == "tree" else FOREST_PARAMETERS
    cls = DecisionTreeClassifier if algorithm == "tree" else RandomForestClassifier
    candidate = declared_candidate(training_project, algorithm, parameters)
    first, record = fit_case(training_project, candidate, {algorithm: cls})
    second, repeated = fit_case(training_project, candidate, {algorithm: cls})
    assert first.predict(pd.DataFrame({"x": [-2.0, 2.0]})).tolist() == [0, 1]
    assert second.predict(pd.DataFrame({"x": [-4.0, 4.0]})).tolist() == [0, 1]
    assert first["estimator"] is not second["estimator"]
    assert first["preprocessing"] is not second["preprocessing"]
    assert record == repeated
    assert record["parameters"] == parameters
    assert set(record) == {
        "schema_version",
        "algorithm",
        "estimator_class",
        "validation_id",
        "parameters",
        "parameter_origins",
        "fit_partition",
        "classes",
        "preprocessing",
        "versions",
    }
    assert json.loads(json.dumps(record, allow_nan=False)) == record


def test_rejects_missing_training_target(training_project: Path) -> None:
    """AC-03: a missing training label has an explicit target diagnostic."""
    candidate = candidate_for(training_project)
    frame = source_frame()
    frame["label"] = frame["label"].astype(float)
    frame.loc[0, "label"] = float("nan")
    _, partition = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
    )
    with pytest.raises(ValueError, match="target"):
        fit_case(
            training_project,
            candidate,
            {"dummy_classifier": DummyClassifier},
            frame=frame,
            partition_record=partition,
        )


@pytest.mark.parametrize("fault", ["shape", "labels"])
def test_rejects_incompatible_native_predictions(
    training_project: Path, monkeypatch: pytest.MonkeyPatch, fault: str
) -> None:
    """AC-03: reject malformed results from the external sklearn predict boundary."""
    from collections.abc import Sized
    from typing import cast

    from numpy.typing import NDArray

    def malformed(self: object, x: object) -> NDArray[np.int64]:
        count = len(cast(Sized, x))
        return (
            np.zeros((count, 1), dtype=np.int64)
            if fault == "shape"
            else np.full(count, 999, dtype=np.int64)
        )

    candidate = candidate_for(training_project)
    monkeypatch.setattr(DummyClassifier, "predict", malformed)
    with pytest.raises(ValueError, match="prediction"):
        fit_case(training_project, candidate, {"dummy_classifier": DummyClassifier})


@pytest.mark.parametrize("stage", ["construction", "estimator fit"])
def test_native_failures_preserve_algorithm_and_stage(
    training_project: Path, stage: str
) -> None:
    """AC-01/03: retain native failures with useful public execution context."""
    from sklearn.tree import DecisionTreeClassifier

    parameters = dict(TREE_PARAMETERS)
    if stage == "construction":
        parameters["unknown_parameter"] = 1
    else:
        parameters["max_depth"] = 0
    candidate = declared_candidate(training_project, "broken_tree", parameters)
    with pytest.raises((TypeError, ValueError)) as captured:
        fit_case(training_project, candidate, {"broken_tree": DecisionTreeClassifier})
    assert any(
        stage in note and "broken_tree" in note
        for note in getattr(captured.value, "__notes__", [])
    )


def test_rejects_nonscalar_candidate_parameters(training_project: Path) -> None:
    """AC-01/04: nested objects cannot enter the scalar training contract."""
    original = candidate_for(training_project)
    candidate = CandidateRequest(
        training_project,
        original.validation_id,
        "dummy_classifier",
        {"strategy": ["most_frequent"]},
    )
    with pytest.raises(TypeError, match="parameters.strategy"):
        fit_case(training_project, candidate, {"dummy_classifier": DummyClassifier})


@pytest.mark.parametrize(
    "damage",
    [
        "source",
        "overlap",
        "missing",
        "fit_scope",
        "target_feature",
        "id_feature",
        "width",
    ],
)
def test_training_reuses_partition_and_preprocessing_guards(
    training_project: Path, damage: str
) -> None:
    """AC-03/04: existing source/split/feature boundaries apply to model fitting."""
    candidate = candidate_for(training_project)
    frame = source_frame()
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
    )
    if damage == "source":
        frame.loc[0, "x"] = 12.0
    elif damage in ("overlap", "missing"):
        memberships = cast(dict[str, list[int]], record["memberships"])
        memberships["validation"] = [0, 5] if damage == "overlap" else [4]
    with pytest.raises(ValueError):
        fit_case(
            training_project,
            candidate,
            {"dummy_classifier": DummyClassifier},
            frame=frame,
            partition_record=record,
            fit_partition="validation" if damage == "fit_scope" else "train",
            selected_columns=["label"]
            if damage == "target_feature"
            else ["id"]
            if damage == "id_feature"
            else ["x"],
            output_schema=[
                {"name": "x", "dtype": "float64"},
                {"name": "extra", "dtype": "float64"},
            ]
            if damage == "width"
            else None,
        )


def test_two_way_fitting_does_not_consume_final_test_labels(
    training_project: Path,
) -> None:
    """AC-03: two-way fitting needs no validation and ignores final-test labels."""
    candidate = candidate_for(training_project)
    frame = source_frame()
    frame.loc[4:, "label"] = 99
    _, record = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": [0, 1, 2, 3], "test": [4, 5, 6, 7]},
    )
    fitted, metadata = fit_case(
        training_project,
        candidate,
        {"dummy_classifier": DummyClassifier},
        frame=frame,
        partition_record=record,
    )
    assert fitted.classes_.tolist() == [0, 1]
    assert metadata["classes"] == [0, 1]
    assert fitted.predict(pd.DataFrame({"x": [0.0]})).tolist() == [0]


def test_multiclass_and_imputation_use_only_training_values(
    training_project: Path,
) -> None:
    """AC-01/03: multiclass fitting preserves independently checked learned state."""
    from sklearn.impute import SimpleImputer

    candidate = candidate_for(training_project)
    frame = source_frame()
    frame.loc[:3, "x"] = [1.0, float("nan"), 3.0, 2.0]
    frame.loc[:3, "label"] = [0, 1, 2, 0]
    preprocessing = Pipeline(
        [("impute", SimpleImputer()), ("scale", StandardScaler(with_std=False))]
    )
    fitted, metadata = fit_case(
        training_project,
        candidate,
        {"dummy_classifier": DummyClassifier},
        frame=frame,
        preprocessing=preprocessing,
    )
    assert fitted.classes_.tolist() == [0, 1, 2]
    assert metadata["classes"] == [0, 1, 2]
    np.testing.assert_allclose(
        fitted["preprocessing"].transform(pd.DataFrame({"x": [100.0, float("nan")]})),
        [[98.0], [0.0]],
        rtol=1e-12,
        atol=1e-12,
    )
    assert fitted.predict(pd.DataFrame({"x": [100.0]})).tolist() == [0]


@pytest.mark.parametrize(
    "damage", ["stale", "fixed", "default", "search", "typed_search"]
)
def test_live_candidate_rejection_precedes_construction(
    training_project: Path, damage: str
) -> None:
    """AC-01/04: invalid/stale parameters cannot reach even a failing constructor."""
    if damage in ("search", "typed_search"):
        path = training_project / "search.yaml"
        document = yaml.safe_load(path.read_text())
        document["algorithms"]["dummy_classifier"]["search"] = {
            "random_state": {"type": "integer", "min": 1, "max": 2, "scale": "linear"}
        }
        path.write_text(yaml.safe_dump(document))
    initial = candidate_for(training_project)
    parameters: dict[str, JSONValue] = {}
    if damage == "stale":
        brief = training_project / "brief.md"
        brief.write_text(
            brief.read_text().replace("Predict churn.", "Predict another outcome.")
        )
    elif damage == "fixed":
        parameters = {"strategy": "prior"}
    elif damage == "default":
        parameters = {"random_state": 17}
    else:
        parameters = {"random_state": 3 if damage == "search" else 1.0}
    candidate = CandidateRequest(
        training_project, initial.validation_id, "dummy_classifier", parameters
    )
    # StandardScaler cannot construct from DummyClassifier parameters. A native
    # constructor TypeError would reveal that invalid evidence reached construction.
    with pytest.raises(ValueError, match="Diagnostic"):
        fit_case(training_project, candidate, {"dummy_classifier": StandardScaler})


@pytest.mark.parametrize("binding", [None, DummyClassifier(), object, StandardScaler])
def test_invalid_class_bindings_fail_clearly(
    training_project: Path, binding: object
) -> None:
    """AC-01/03: bindings must be native estimator classes, not instances/factories."""
    candidate = candidate_for(training_project)
    with pytest.raises((TypeError, ValueError)):
        fit_case(
            training_project,
            candidate,
            cast(Mapping[str, type[BaseEstimator]], {"dummy_classifier": binding}),
        )


def test_invalid_fit_scope_precedes_construction(training_project: Path) -> None:
    """AC-03: forbidden fitting scope is rejected before a native constructor."""
    candidate = candidate_for(training_project)
    with pytest.raises(ValueError, match="fit_partition"):
        fit_case(
            training_project,
            candidate,
            {"dummy_classifier": StandardScaler},
            fit_partition="test",
        )


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_candidate_parameters_fail_clearly(
    training_project: Path, value: float
) -> None:
    """AC-04: scalar metadata must not silently serialize nonfinite values."""
    original = candidate_for(training_project)
    candidate = CandidateRequest(
        training_project,
        original.validation_id,
        "dummy_classifier",
        {"random_state": value},
    )
    with pytest.raises(ValueError, match="finite"):
        fit_case(training_project, candidate, {"dummy_classifier": DummyClassifier})


def test_continuous_training_target_is_not_classification(
    training_project: Path,
) -> None:
    """AC-01/03: regression targets cannot enter the classification fit path."""
    candidate = candidate_for(training_project)
    frame = source_frame()
    frame["label"] = frame["label"].astype(float)
    frame.loc[:3, "label"] = [0.1, 0.2, 0.3, 0.4]
    with pytest.raises(ValueError, match="target"):
        fit_case(
            training_project,
            candidate,
            {"dummy_classifier": DummyClassifier},
            frame=frame,
        )


@pytest.mark.parametrize(
    "damage",
    ["relative", "missing", "type", "candidate_type", "bindings_type", "nonnative"],
)
def test_explicit_public_input_checks(training_project: Path, damage: str) -> None:
    """AC-01/04: explicit root/candidate/class boundaries retain clear errors."""
    candidate = candidate_for(training_project)
    bindings: Mapping[str, type[BaseEstimator]] = {"dummy_classifier": DummyClassifier}
    root = training_project
    expected: type[Exception] = ValueError
    if damage == "relative":
        root = Path("relative")
    elif damage == "missing":
        root = training_project / "absent"
        expected = FileNotFoundError
    elif damage == "type":
        root = cast(Path, str(training_project))
        expected = TypeError
    elif damage == "candidate_type":
        candidate = cast(CandidateRequest, None)
        expected = TypeError
    elif damage == "bindings_type":
        bindings = cast(Mapping[str, type[BaseEstimator]], [])
        expected = TypeError
    else:

        class ProjectEstimator(BaseEstimator):
            """Unsupported custom class; no M2 custom-component claim."""

        bindings = {"dummy_classifier": ProjectEstimator}
    with pytest.raises(expected):
        fit_case(root, candidate, bindings)


def test_candidate_root_type_has_public_diagnostic(training_project: Path) -> None:
    """AC-04: malformed request roots produce TypeError rather than attribute errors."""
    original = candidate_for(training_project)
    candidate = CandidateRequest(
        cast(Path, str(training_project)),
        original.validation_id,
        original.algorithm,
        {},
    )
    with pytest.raises(TypeError, match="candidate.project_root"):
        fit_case(training_project, candidate, {"dummy_classifier": DummyClassifier})
