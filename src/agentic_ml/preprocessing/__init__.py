"""Training-only fitting of native preprocessing pipelines."""

import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from importlib.metadata import version
from typing import Literal, cast

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from agentic_ml.splitting import create_partitions


def fit_preprocessing(
    frame: pd.DataFrame,
    *,
    partition_record: Mapping[str, object],
    pipeline: Pipeline,
    selected_columns: Sequence[str],
    output_schema: Sequence[Mapping[str, str]],
    fit_partition: str = "train",
) -> tuple[Pipeline, dict[str, object]]:
    """Fit a cloned native pipeline on recorded training rows.

    Args:
        frame: Native source DataFrame identified by the partition record.
        partition_record: Existing create_partitions record for this frame.
        pipeline: Native sklearn preprocessing Pipeline to clone.
        selected_columns: Ordered feature column names, excluding ID and target.
        output_schema: Declared ordered output names and dtype strings.
        fit_partition: Required training scope, exactly train.

    Returns:
        Fitted native pipeline and a plain preprocessing metadata dictionary.

    Raises:
        TypeError: Arguments have unsupported types.
        ValueError: Membership, features, source identity or fit scope is invalid.
    """
    if not isinstance(pipeline, Pipeline):
        raise TypeError("pipeline must be a native sklearn Pipeline")
    if fit_partition != "train":
        raise ValueError("fit_partition must be train")
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a pandas DataFrame")
    if not isinstance(partition_record, Mapping):
        raise TypeError("partition_record must be a mapping")
    try:
        encoded_record = json.dumps(dict(partition_record), allow_nan=False)
        if json.loads(encoded_record) != dict(partition_record):
            raise TypeError("record must use string-keyed dictionaries and JSON lists")
    except (TypeError, ValueError) as error:
        raise type(error)(
            f"partition_record must be finite plain JSON: {error}"
        ) from error
    record = partition_record
    if (
        set(record)
        != {
            "schema_version",
            "row_id",
            "target",
            "source",
            "layout",
            "method",
            "settings",
            "protocol",
            "memberships",
        }
        or record.get("schema_version") != "1.0"
    ):
        raise ValueError("partition_record must have existing version 1.0 keys")
    if record["method"] not in ("seeded", "supplied"):
        raise ValueError("partition_record.method must be seeded or supplied")
    if record["method"] == "supplied" and record["settings"] != {}:
        raise ValueError("partition_record.settings must be empty in supplied mode")
    row_id, target, layout = record["row_id"], record["target"], record["layout"]
    if (
        not isinstance(row_id, str)
        or not isinstance(target, str)
        or not isinstance(layout, str)
    ):
        raise TypeError("partition_record row_id, target and layout must be strings")
    if isinstance(selected_columns, (str, bytes)) or not isinstance(
        selected_columns, Sequence
    ):
        raise TypeError("selected_columns must be a sequence of feature names")
    columns = list(selected_columns)
    if (
        not columns
        or any(
            not isinstance(name, str) or name not in frame.columns for name in columns
        )
        or len(set(columns)) != len(columns)
        or record["row_id"] in columns
        or record["target"] in columns
    ):
        raise ValueError(
            "selected_columns must be unique existing features excluding row_id and target"
        )
    parts, current = create_partitions(
        frame,
        row_id=row_id,
        target=target,
        layout=cast(Literal["train_test", "train_validation_test"], layout),
        memberships=cast(Mapping[str, Sequence[str | int]], record["memberships"]),
        protocol=cast(Mapping[str, object] | None, record["protocol"]),
    )
    if json.dumps(current["source"], sort_keys=True) != json.dumps(
        record["source"], sort_keys=True
    ):
        raise ValueError("partition_record source does not match current frame")
    _record_settings(frame, record)
    settings = _settings(pipeline)
    fitted = clone(pipeline)
    if isinstance(output_schema, (str, bytes)) or not isinstance(
        output_schema, Sequence
    ):
        raise TypeError("output_schema must be a sequence")
    schema = list(output_schema)
    if not schema or any(
        not isinstance(col, Mapping)
        or set(col) != {"name", "dtype"}
        or any(
            not isinstance(col[key], str) or not col[key] for key in ("name", "dtype")
        )
        for col in schema
    ):
        raise ValueError("output_schema requires nonempty name/dtype records")
    if len({col["name"] for col in schema}) != len(schema):
        raise ValueError("output_schema names must be unique")
    try:
        fitted.fit(parts["train"][columns])
        transformed = fitted.transform(parts["train"][columns])
    except (ValueError, TypeError) as error:
        error.add_note("Failure during preprocessing training fit/transform")
        raise
    if len(transformed.shape) != 2 or transformed.shape[1] != len(schema):
        raise ValueError("output_schema width does not match training transform")
    dtypes = (
        [str(dtype) for dtype in transformed.dtypes]
        if isinstance(transformed, pd.DataFrame)
        else [str(transformed.dtype)] * transformed.shape[1]
    )
    if dtypes != [column["dtype"] for column in schema]:
        raise ValueError("output_schema dtypes do not match training transform")
    return fitted, {
        "schema_version": "1.0",
        "fit_partition": fit_partition,
        "partition_record": deepcopy(dict(partition_record)),
        "selected_columns": list(selected_columns),
        "input_schema": [
            {"name": name, "dtype": str(frame[name].dtype)} for name in selected_columns
        ],
        "output_schema": [dict(column) for column in output_schema],
        "pipeline": settings,
        "versions": {
            name: version(name)
            for name in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
        },
    }


def _settings(
    value: object,
    owner: object = None,
    field: str = "",
    path: str = "pipeline",
    active: frozenset[int] = frozenset(),
) -> object:
    if id(value) in active:
        raise ValueError(f"{path} has cyclic settings")
    active = active | {id(value)}
    if (
        isinstance(value, float)
        and math.isnan(value)
        and type(owner) is SimpleImputer
        and field == "missing_values"
    ):
        return {"kind": "missing_value", "value": "nan"}
    dtype_names = {
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
    if isinstance(value, np.ndarray):
        return _settings(value.tolist(), path=path, active=active)
    if isinstance(value, np.generic):
        return _settings(value.item(), owner, field, path, active)
    if isinstance(value, (type, np.dtype)):
        for name in dtype_names:
            native = np.dtype(name)
            if value is native.type or (
                isinstance(value, np.dtype) and value == native
            ):
                return {"kind": "numpy_dtype", "name": name}
    if isinstance(value, BaseEstimator):
        return {
            "class_name": f"{type(value).__module__}.{type(value).__qualname__}",
            "parameters": {
                key: _settings(item, value, key, f"{path}.parameters.{key}", active)
                for key, item in value.get_params(deep=False).items()
            },
        }
    if isinstance(value, (tuple, list)):
        return [
            _settings(item, path=f"{path}[{index}]", active=active)
            for index, item in enumerate(value)
        ]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path} requires finite numeric values")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value) or value.get("kind") in (
            "numpy_dtype",
            "missing_value",
        ):
            raise ValueError(
                f"{path} requires string keys and no reserved literal tags"
            )
        return {
            key: _settings(item, path=f"{path}.{key}", active=active)
            for key, item in value.items()
        }
    raise TypeError(f"{path} contains unsupported settings type {type(value).__name__}")


def _record_settings(frame: pd.DataFrame, record: Mapping[str, object]) -> None:
    """Validate retained seeded settings through the native public split API."""
    if record["method"] == "supplied":
        if not isinstance(record["protocol"], Mapping):
            raise ValueError("partition_record.protocol must be a supplied declaration")
        return
    settings = record["settings"]
    keys = {"seed", "test_size", "validation_size", "shuffle", "stratify", "calls"}
    if not isinstance(settings, dict) or set(settings) != keys:
        raise ValueError("partition_record.settings must have existing seeded keys")
    if record["protocol"] is not None:
        raise ValueError("partition_record.protocol must be null in seeded mode")
    try:
        _, regenerated = create_partitions(
            frame,
            row_id=cast(str, record["row_id"]),
            target=cast(str, record["target"]),
            layout=cast(
                Literal["train_test", "train_validation_test"], record["layout"]
            ),
            seed=cast(int, settings["seed"]),
            test_size=cast(float, settings["test_size"]),
            validation_size=cast(float | None, settings["validation_size"]),
            shuffle=cast(bool, settings["shuffle"]),
            stratify=cast(bool, settings["stratify"]),
        )
        # Strict JSON also rejects NaN, opaque values and bool/int substitutions.
        if json.dumps(settings, allow_nan=False, sort_keys=True) != json.dumps(
            regenerated["settings"], allow_nan=False, sort_keys=True
        ):
            raise ValueError("recorded calls disagree with native settings")
    except (TypeError, ValueError) as error:
        raise type(error)(f"partition_record.settings: {error}") from error
