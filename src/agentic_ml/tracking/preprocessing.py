"""Check native preprocessing descriptions without reconstructing estimators."""

import json
import math
import re
import shutil
import sys
import tempfile
from collections.abc import Mapping
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path, PurePosixPath

import mlflow.sklearn
import numpy as np
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted

from .artifacts import require_available, shared_provenance
from .provenance import (
    committed_references,
    dvc_references,
    environment_identity,
    exact_record,
    local_path,
    object_map,
    provenance_schema,
    validate_json,
)


def partition_record(value: object) -> None:
    """Validate existing partition-record structure and disjoint full membership."""
    field = "record.partition_record"
    record = exact_record(
        value,
        field,
        {
            "schema_version",
            "layout",
            "row_id",
            "target",
            "source",
            "method",
            "settings",
            "protocol",
            "memberships",
        },
    )
    if record["schema_version"] != "1.0" or record["layout"] not in (
        "train_test",
        "train_validation_test",
    ):
        raise ValueError(f"{field} requires a supported 1.0 layout")
    if (
        any(
            not isinstance(record[key], str) or not record[key]
            for key in ("row_id", "target")
        )
        or record["row_id"] == record["target"]
    ):
        raise ValueError(f"{field} requires distinct row_id/target names")
    source = exact_record(
        record["source"],
        field + ".source",
        {"row_count", "schema", "sha256", "identity_format", "versions"},
    )
    count = source["row_count"]
    if type(count) is not int or count <= 0:
        raise ValueError(f"{field}.source.row_count must be positive")
    if (
        source["identity_format"] != "pandas-parquet-v1"
        or not isinstance(source["sha256"], str)
        or re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is None
    ):
        raise ValueError(
            f"{field}.source requires its existing native content identity"
        )
    names = column_schema(source["schema"], field + ".source.schema")
    if record["row_id"] not in names or record["target"] not in names:
        raise ValueError(f"{field}.source.schema must include ID/target")
    object_map(source["versions"], field + ".source.versions")
    object_map(record["settings"], field + ".settings")
    if record["method"] not in ("supplied", "seeded"):
        raise ValueError(f"{field}.method is unsupported")
    if record["protocol"] is not None:
        object_map(record["protocol"], field + ".protocol")
    partitions = (
        {"train", "test"}
        if record["layout"] == "train_test"
        else {"train", "validation", "test"}
    )
    memberships = exact_record(
        record["memberships"], field + ".memberships", partitions
    )
    seen: set[str | int] = set()
    id_types: set[type] = set()
    for ids in memberships.values():
        if not isinstance(ids, list) or not ids:
            raise ValueError(f"{field}.memberships must contain nonempty lists")
        for row_id in ids:
            if type(row_id) not in (str, int):
                raise ValueError(f"{field}.memberships requires string/integer IDs")
            if row_id in seen:
                raise ValueError(f"{field}.memberships must be unique and disjoint")
            seen.add(row_id)
            id_types.add(type(row_id))
    if len(id_types) != 1 or len(seen) != count:
        raise ValueError(f"{field}.memberships must homogeneously cover source rows")


def column_schema(value: object, field: str) -> list[str]:
    """Require ordered, unique names with explicit dtype declarations."""
    if not isinstance(value, list):
        raise TypeError(f"{field} must be a list")
    if not value:
        raise ValueError(f"{field} must be nonempty")
    names: list[str] = []
    for item in value:
        entry = exact_record(item, field, {"name", "dtype"})
        if any(not isinstance(v, str) or not v for v in entry.values()):
            raise ValueError(f"{field} requires nonempty name/dtype strings")
        name = str(entry["name"])
        if name in names:
            raise ValueError(f"{field} names must be unique")
        names.append(name)
    return names


def native_parameters(
    native: object,
    encoded: object,
    field: str,
    owner: object = None,
    parameter: str | None = None,
) -> None:
    """Compare complete declared native settings recursively, without imports."""
    dtypes = {
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
    }
    if isinstance(native, (float, np.floating)) and math.isnan(float(native)):
        if (
            type(owner) is not SimpleImputer
            or parameter != "missing_values"
            or (encoded != {"kind": "missing_value", "value": "nan"})
        ):
            raise ValueError(f"{field} requires the canonical SimpleImputer NaN tag")
    elif isinstance(native, np.dtype) or (
        isinstance(native, type) and issubclass(native, np.generic)
    ):
        name = np.dtype(native).name
        if name not in dtypes or encoded != {"kind": "numpy_dtype", "name": name}:
            raise ValueError(f"{field} requires a supported canonical numpy dtype tag")
    elif isinstance(native, (np.generic, np.ndarray)):
        native_parameters(native.tolist(), encoded, field, owner, parameter)
    elif isinstance(native, BaseEstimator):
        if type(native) not in {
            Pipeline,
            ColumnTransformer,
            SimpleImputer,
            StandardScaler,
            OneHotEncoder,
        }:
            raise TypeError(
                f"{field} contains a component outside the supported M1 inventory"
            )
        description = exact_record(encoded, field, {"class_name", "parameters"})
        if description["class_name"] != (
            f"{type(native).__module__}.{type(native).__qualname__}"
        ):
            raise ValueError(f"{field}.class_name differs from native estimator")
        settings = object_map(description["parameters"], field + ".parameters")
        params = native.get_params(deep=False)
        if set(settings) != set(params):
            raise ValueError(f"{field}.parameters must include every effective setting")
        for key, value in params.items():
            native_parameters(
                value, settings[key], f"{field}.parameters.{key}", native, key
            )
    elif isinstance(native, (tuple, list)):
        if not isinstance(encoded, list) or len(encoded) != len(native):
            raise ValueError(f"{field} differs from native sequence")
        for index, (value, description) in enumerate(zip(native, encoded, strict=True)):
            native_parameters(value, description, f"{field}[{index}]")
    elif isinstance(native, Mapping):
        if native.get("kind") in ("missing_value", "numpy_dtype"):
            raise ValueError(
                f"{field} contains a reserved literal native parameter map"
            )
        settings = object_map(encoded, field)
        if set(settings) != set(native):
            raise ValueError(f"{field} differs from native map")
        for key, value in native.items():
            native_parameters(value, settings[key], f"{field}.{key}")
    else:
        validate_json(native, field)
        if type(native) is not type(encoded) or native != encoded:
            raise ValueError(f"{field} differs from native value")


def log_preprocessing(
    *,
    run_id: str,
    pipeline: Pipeline,
    record: Mapping[str, object],
    provenance: Mapping[str, object],
    project_root: Path,
    tracking_uri: str,
    artifact_path: str = "preprocessing",
) -> dict[str, object]:
    """Save native fitted preprocessing and its supplied experiment references.

    The existing selected run remains RUNNING after successful recording.
    Metadata declarations do not certify training-only fitting.

    Args:
        run_id: Existing native MLflow run.
        pipeline: Independently fitted native sklearn Pipeline.
        record: Versioned preprocessing metadata.
        provenance: Shared experiment references.
        project_root: Explicit absolute experiment root.
        tracking_uri: Explicit selected tracking store.
        artifact_path: Run-relative preprocessing artifact directory.

    Returns:
        Existing run ID and pipeline, metadata and provenance artifact URIs.

    Raises:
        ValueError: Invalid declarations or references.
        Exception: Native serialization and storage errors remain visible.
    """
    client: MlflowClient | None = None
    eligible = False
    stage = "run selection"
    directory: Path | None = None
    try:
        if not isinstance(tracking_uri, str) or not tracking_uri.strip():
            raise ValueError("tracking_uri must explicitly select a store")
        client = MlflowClient(tracking_uri=tracking_uri)
        run = client.get_run(run_id)
        if run.info.status != "RUNNING" or run.info.lifecycle_stage != "active":
            raise ValueError(f"Run {run_id} must be active and RUNNING")
        eligible = True
        stage = "metadata and references"
        if not isinstance(project_root, Path):
            raise TypeError("project_root must be a Path")
        if not project_root.is_absolute() or not project_root.is_dir():
            raise ValueError("project_root must be an existing absolute directory")
        if not isinstance(artifact_path, str):
            raise TypeError("artifact_path must be a run-relative string")
        if (
            not artifact_path
            or "\\" in artifact_path
            or PurePosixPath(artifact_path).is_absolute()
            or any(part in {"", ".", ".."} for part in artifact_path.split("/"))
            or artifact_path.split("/")[0] == "provenance.json"
        ):
            raise ValueError(
                "artifact_path must be a normalized run-relative directory"
            )
        if not isinstance(pipeline, Pipeline):
            raise TypeError("pipeline must be a native sklearn Pipeline")
        check_is_fitted(pipeline)
        exact_record(
            record,
            "record",
            {
                "schema_version",
                "fit_partition",
                "partition_record",
                "selected_columns",
                "input_schema",
                "output_schema",
                "pipeline",
                "versions",
            },
        )
        validate_json(dict(record), "record")
        partition_record(record["partition_record"])
        if record["schema_version"] != "1.0":
            raise ValueError("record.schema_version must be 1.0")
        if record["fit_partition"] != "train":
            raise ValueError("record.fit_partition must be train")
        versions = object_map(record["versions"], "record.versions")
        if not {"agentic-ml", "pandas", "pyarrow", "scikit-learn"} <= set(versions):
            raise ValueError("record.versions requires preprocessing library versions")
        for name, supplied in versions.items():
            try:
                actual = version(name)
            except PackageNotFoundError as error:
                raise ValueError(
                    f"record.versions library unavailable: {name}"
                ) from error
            if supplied != actual:
                raise ValueError(f"record.versions differs from installed {name}")
        native_parameters(pipeline, record["pipeline"], "record.pipeline")
        output_names = column_schema(record["output_schema"], "record.output_schema")
        provenance_schema(provenance)
        committed_references(project_root, provenance)
        dvc_references(project_root, provenance)
        environment_identity(project_root, provenance)
        split_ref = object_map(provenance["split_record"], "provenance.split_record")
        saved_split = json.loads(
            local_path(project_root, split_ref["path"]).read_text()
        )
        if record["partition_record"] != saved_split:
            raise ValueError(
                "record.partition_record differs from consumed saved split"
            )
        selected = record["selected_columns"]
        if (
            not isinstance(selected, list)
            or not selected
            or any(not isinstance(name, str) or not name for name in selected)
        ):
            raise ValueError("record.selected_columns must be nonempty feature names")
        if len(set(selected)) != len(selected) or any(
            name in {saved_split["row_id"], saved_split["target"]} for name in selected
        ):
            raise ValueError(
                "record.selected_columns must be unique and exclude ID/target"
            )
        source_schema = {item["name"]: item for item in saved_split["source"]["schema"]}
        if any(name not in source_schema for name in selected):
            raise ValueError("record.selected_columns absent from partition source")
        if column_schema(record["input_schema"], "record.input_schema") != selected or (
            record["input_schema"] != [source_schema[name] for name in selected]
        ):
            raise ValueError("record.input_schema differs from selected source schema")
        if len(output_names) != len(pipeline.get_feature_names_out(selected)):
            raise ValueError("record.output_schema width differs from fitted pipeline")
        require_available(client, run_id, artifact_path)
        directory = Path(tempfile.mkdtemp(prefix="agentic-ml-preprocessing-"))
        metadata = directory / "metadata.json"
        metadata.write_text(json.dumps(dict(record), allow_nan=False), encoding="utf-8")
        references = directory / "provenance.json"
        references.write_text(
            json.dumps(dict(provenance), allow_nan=False), encoding="utf-8"
        )
        stage = "shared provenance"
        shared_provenance(client, run_id, provenance)
        stage = "metadata artifact"
        client.log_artifact(run_id, str(metadata), artifact_path)
        stage = "native serialization"
        model = directory / "pipeline"
        mlflow.sklearn.save_model(
            pipeline,
            str(model),
            serialization_format="skops",
            skops_trusted_types=["numpy.dtype"],
        )
        stage = "pipeline artifact"
        client.log_artifacts(run_id, str(model), artifact_path + "/pipeline")
        return {
            "run_id": run_id,
            "artifacts": {
                "pipeline": run.info.artifact_uri + "/" + artifact_path + "/pipeline",
                "metadata": run.info.artifact_uri
                + "/"
                + artifact_path
                + "/metadata.json",
                "provenance": run.info.artifact_uri + "/provenance.json",
            },
        }
    finally:
        failure = sys.exception()
        if isinstance(failure, Exception):
            failure.add_note(
                f"tracking run_id={run_id}; stage={stage}; project_root={project_root}"
            )
            if directory is not None:
                failure.add_note(f"Available local recording diagnostics: {directory}")
            if eligible and client is not None:
                try:
                    client.set_terminated(run_id, status="FAILED")
                except (OSError, ValueError, MlflowException) as status_error:
                    failure.add_note(
                        f"Failed to record native FAILED status: {status_error}"
                    )
        elif directory is not None:
            shutil.rmtree(directory)
