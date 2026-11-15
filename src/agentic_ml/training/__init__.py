"""Construct and fit native classifiers on recorded training rows."""

import math
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from copy import deepcopy
from importlib.metadata import version
from pathlib import Path
from typing import Literal, Protocol, cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.base import BaseEstimator, is_classifier
from sklearn.pipeline import Pipeline
from sklearn.utils.multiclass import type_of_target

from agentic_ml.preprocessing import fit_preprocessing
from agentic_ml.splitting import create_partitions
from agentic_ml.validation import (
    CandidateRequest,
    inspect_validation,
    validate_candidate,
)


class _Classifier(Protocol):
    """Native operations required after classifier compatibility validation."""

    classes_: NDArray[np.generic]

    def fit(self, x: object, y: object) -> object: ...

    def predict(self, x: object) -> NDArray[np.generic]: ...


def _scalars(parameters: Mapping[str, object]) -> None:
    for name, value in parameters.items():
        if not isinstance(name, str) or type(value) not in (
            type(None),
            bool,
            int,
            float,
            str,
        ):
            raise TypeError(f"parameters.{name} must be a plain JSON scalar")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"parameters.{name} must be finite")


@contextmanager
def _stage(algorithm: str, stage: str) -> Iterator[None]:
    try:
        yield
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(f"classification algorithm={algorithm}; stage={stage}")


def fit_classifier(
    frame: pd.DataFrame,
    *,
    project_root: Path,
    candidate: CandidateRequest,
    estimator_bindings: Mapping[str, type[BaseEstimator]],
    preprocessing: Pipeline,
    partition_record: Mapping[str, object],
    selected_columns: Sequence[str],
    output_schema: Sequence[Mapping[str, str]],
    fit_partition: str = "train",
) -> tuple[Pipeline, dict[str, object]]:
    """Construct a validated native classifier and fit recorded training rows.

    Args:
        frame: Current source DataFrame identified by the partition record.
        project_root: Absolute experiment project directory.
        candidate: Live strict candidate request for the same project.
        estimator_bindings: Project-owned algorithm names and native classes.
        preprocessing: Native transformer Pipeline to clone and fit.
        partition_record: Existing versioned source and partition record.
        selected_columns: Ordered feature names excluding ID and target.
        output_schema: Expected transformed feature names and dtypes.
        fit_partition: Required scope, exactly train.

    Returns:
        Fitted native prediction Pipeline and finite plain training metadata.

    Raises:
        TypeError: Input types or parameter encodings are unsupported.
        ValueError: Evidence, parameters, partitions or compatibility are invalid.
        Exception: Native constructor, fitting and prediction errors propagate.
    """
    if fit_partition != "train":
        raise ValueError("fit_partition must be train")
    if not isinstance(project_root, Path):
        raise TypeError("project_root must be a Path")
    if not project_root.is_absolute():
        raise ValueError("project_root must be absolute")
    if not project_root.is_dir():
        raise FileNotFoundError(project_root)
    if not isinstance(candidate, CandidateRequest):
        raise TypeError("candidate must be a CandidateRequest")
    if not isinstance(candidate.project_root, Path):
        raise TypeError("candidate.project_root must be a Path")
    if project_root.resolve() != candidate.project_root.resolve():
        raise ValueError("project_root must match candidate.project_root")
    if not isinstance(candidate.parameters, Mapping):
        raise TypeError("candidate.parameters must be a mapping")
    _scalars(candidate.parameters)
    result = validate_candidate(candidate)
    if result.parameters is None:
        raise ValueError(str(result.diagnostics))
    inspection = inspect_validation(
        project_root=project_root, validation_id=candidate.validation_id
    )
    if inspection.status != "valid" or inspection.configuration is None:
        raise ValueError(str(inspection.diagnostics))
    algorithms = cast(Mapping[str, object], inspection.configuration["algorithms"])
    settings = cast(Mapping[str, object], algorithms[candidate.algorithm])
    if settings["task"] != "classification":
        raise ValueError("task must be classification")
    if settings["library_distribution"] != "scikit-learn":
        raise ValueError("library_distribution must be scikit-learn")
    parameters = deepcopy(result.parameters)
    if not isinstance(estimator_bindings, Mapping):
        raise TypeError("estimator_bindings must be a mapping")
    if candidate.algorithm not in estimator_bindings:
        raise ValueError(f"Missing estimator binding for {candidate.algorithm}")
    estimator_class = estimator_bindings[candidate.algorithm]
    if not isinstance(estimator_class, type) or not issubclass(
        estimator_class, BaseEstimator
    ):
        raise TypeError("estimator binding must be a native estimator class")
    if not estimator_class.__module__.startswith("sklearn."):
        raise ValueError("estimator binding must be a native sklearn classifier")
    with _stage(candidate.algorithm, "construction"):
        estimator = estimator_class(**parameters)
    if not is_classifier(estimator):
        raise ValueError("estimator binding must construct a classifier")
    native = estimator.get_params(deep=False)
    _scalars(native)
    if native.keys() != parameters.keys() or any(
        type(value) is not type(parameters[name]) or value != parameters[name]
        for name, value in native.items()
    ):
        raise ValueError("parameters must cover and match all native defaults")
    fitted_preprocessing, record = fit_preprocessing(
        frame,
        partition_record=partition_record,
        pipeline=preprocessing,
        selected_columns=selected_columns,
        output_schema=output_schema,
        fit_partition=fit_partition,
    )
    parts, _ = create_partitions(
        frame,
        row_id=cast(str, partition_record["row_id"]),
        target=cast(str, partition_record["target"]),
        layout=cast(
            Literal["train_test", "train_validation_test"], partition_record["layout"]
        ),
        memberships=cast(
            Mapping[str, Sequence[str | int]], partition_record["memberships"]
        ),
        protocol=cast(Mapping[str, object] | None, partition_record["protocol"]),
    )
    target = parts["train"][cast(str, partition_record["target"])]
    if target.isna().any() or type_of_target(target) not in ("binary", "multiclass"):
        raise ValueError(
            "target must be nonmissing, one-dimensional classification labels"
        )
    classifier = cast(_Classifier, estimator)
    with _stage(candidate.algorithm, "estimator fit"):
        classifier.fit(
            fitted_preprocessing.transform(parts["train"][list(selected_columns)]),
            target,
        )
    with _stage(candidate.algorithm, "prediction compatibility"):
        prediction = classifier.predict(
            fitted_preprocessing.transform(parts["train"][list(selected_columns)])
        )
    if (
        prediction.ndim != 1
        or len(prediction) != len(target)
        or not np.isin(prediction, classifier.classes_).all()
    ):
        raise ValueError(
            "prediction must contain one fitted class label per training row"
        )
    fitted = Pipeline(
        [("preprocessing", fitted_preprocessing), ("estimator", estimator)]
    )
    return fitted, {
        "schema_version": "1.0",
        "algorithm": candidate.algorithm,
        "estimator_class": {
            "module": estimator_class.__module__,
            "qualname": estimator_class.__qualname__,
        },
        "validation_id": candidate.validation_id,
        "parameters": parameters,
        "parameter_origins": deepcopy(result.origins),
        "fit_partition": fit_partition,
        "classes": classifier.classes_.tolist(),
        "preprocessing": record,
        "versions": {
            name: version(name)
            for name in ("agentic-ml", "scikit-learn", "pandas", "numpy", "pyarrow")
        },
    }
