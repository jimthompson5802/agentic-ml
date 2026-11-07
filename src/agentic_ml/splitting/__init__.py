"""Native scikit-learn partitions and project-owned membership records."""

import hashlib
import math
from collections.abc import Mapping, Sequence
from importlib.metadata import version
from numbers import Integral, Real
from typing import Literal

import pandas as pd
from sklearn.model_selection import train_test_split


def create_partitions(
    frame: pd.DataFrame,
    *,
    row_id: str,
    target: str,
    layout: Literal["train_test", "train_validation_test"],
    seed: int | None = None,
    test_size: float | None = None,
    validation_size: float | None = None,
    shuffle: bool = True,
    stratify: bool = False,
    memberships: Mapping[str, Sequence[str | int]] | None = None,
    protocol: Mapping[str, object] | None = None,
) -> tuple[dict[str, pd.DataFrame], dict[str, object]]:
    """Create seeded or supplied partitions and identify the consumed frame.

    Args:
        frame: Native DataFrame with unique nonmissing string or integer row IDs.
        row_id: Existing ID column; the DataFrame index is preserved, not used as ID.
        target: Existing target column, used for explicit stratification.
        layout: Train/test or train/validation/test; no validation placeholder.
        seed: Required native random state in generated mode, excluding booleans.
        test_size: Generated test fraction relative to the original frame.
        validation_size: Generated validation fraction relative to the original frame.
        shuffle: Native shuffle flag; must stay True for supplied membership.
        stratify: Explicit native target stratification; False for supplied membership.
        memberships: Exact ordered IDs for every partition, covering every source row.
        protocol: Supplied/time/group JSON declaration; prohibited in generated mode.

    Returns:
        Independent partition frames and a JSON-compatible version 1.0 record.
        Source identity hashes index-free, attrs-free native Parquet bytes and is
        bound to recorded library versions. Project code owns JSON persistence and
        saved/current source comparisons. Supplied protocols are declarations,
        without chronological or group-separation certification.

    Raises:
        TypeError: An argument or row ID has an unsupported type.
        ValueError: Settings, layout, names or membership are invalid. Native split
            errors retain their type and receive a partition-stage note.
        Exception: Native Parquet serialization errors propagate without fallback.
    """
    _validate_frame(frame, row_id, target)
    if not isinstance(layout, str):
        raise TypeError("layout must be a string")
    if layout not in ("train_test", "train_validation_test"):
        raise ValueError("layout must be train_test or train_validation_test")
    if not isinstance(shuffle, bool) or not isinstance(stratify, bool):
        raise TypeError("shuffle and stratify must be booleans")
    if memberships is not None:
        if (
            seed is not None
            or test_size is not None
            or validation_size is not None
            or not shuffle
            or stratify
        ):
            raise ValueError(
                "supplied mode forbids seed/fractions and nondefault flags"
            )
        declared_protocol = _protocol(frame, protocol)
        names = (
            ["train", "test"]
            if layout == "train_test"
            else ["train", "validation", "test"]
        )
        parts = _supplied_parts(frame, row_id, names, memberships)
        return parts, {
            "schema_version": "1.0",
            "row_id": row_id,
            "target": target,
            "source": _source(frame),
            "layout": layout,
            "method": "supplied",
            "settings": {},
            "protocol": declared_protocol,
            "memberships": {name: _ids(part[row_id]) for name, part in parts.items()},
        }
    if protocol is not None:
        raise ValueError("protocol is prohibited in seeded mode")
    if seed is None:
        raise ValueError("seed is required")
    if isinstance(seed, bool) or not isinstance(seed, Integral):
        raise TypeError("seed must be an integer")
    if not 0 <= seed < 2**32:
        raise ValueError("seed must be in [0, 2**32)")
    seed = int(seed)
    test_size = _fraction(test_size, "test_size")
    if layout == "train_test" and validation_size is not None:
        raise ValueError("validation_size is prohibited for train_test")
    if layout == "train_validation_test":
        validation_size = _fraction(validation_size, "validation_size")
        if test_size + validation_size >= 1:
            raise ValueError("test_size and validation_size sum must be below 1")
    calls: list[dict[str, object]] = []
    train, test = _split(
        frame, target, test_size, seed, shuffle, stratify, "test", calls
    )
    parts = {"train": train.copy(deep=True), "test": test.copy(deep=True)}
    if layout == "train_validation_test":
        assert validation_size is not None and test_size is not None
        train, validation = _split(
            train,
            target,
            validation_size / (1 - test_size),
            seed,
            shuffle,
            stratify,
            "validation",
            calls,
        )
        parts = {
            "train": train.copy(deep=True),
            "validation": validation.copy(deep=True),
            "test": test.copy(deep=True),
        }
    return parts, {
        "schema_version": "1.0",
        "row_id": row_id,
        "target": target,
        "source": _source(frame),
        "layout": layout,
        "method": "seeded",
        "protocol": None,
        "settings": {
            "seed": seed,
            "test_size": test_size,
            "validation_size": validation_size,
            "shuffle": shuffle,
            "stratify": stratify,
            "calls": calls,
        },
        "memberships": {name: _ids(part[row_id]) for name, part in parts.items()},
    }


def _supplied_parts(
    frame: pd.DataFrame,
    row_id: str,
    names: list[str],
    memberships: Mapping[str, Sequence[str | int]],
) -> dict[str, pd.DataFrame]:
    if not isinstance(memberships, Mapping):
        raise TypeError("memberships must be a mapping")
    if set(memberships) != set(names):
        raise ValueError("membership keys must match layout")
    lookup = pd.Index(frame[row_id])
    if not len(lookup):
        raise ValueError("nonempty supplied partitions require source rows")
    seen = lookup[:0]
    for name in names:
        values = memberships[name]
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise TypeError(f"{name} membership must be a sequence")
        if not values:
            raise ValueError(f"{name} membership must be nonempty")
        integral = isinstance(lookup[0], Integral)
        for value in values:
            if isinstance(value, bool) or (
                not isinstance(value, Integral)
                if integral
                else not isinstance(value, str)
            ):
                raise TypeError(f"{name} membership ID must match source ID type")
        index = pd.Index(values)
        if not index.is_unique:
            raise ValueError(f"{name} membership has duplicate IDs")
        if not index.isin(lookup).all():
            raise ValueError(f"{name} membership contains unknown IDs")
        if len(index.intersection(seen)):
            raise ValueError(f"{name} membership overlaps another partition")
        seen = seen.append(index)
    if len(seen) != len(lookup):
        raise ValueError("membership coverage must include every source row")
    parts = {
        name: frame.iloc[lookup.get_indexer(memberships[name])].copy(deep=True)
        for name in names
    }
    return parts


def _split(
    frame: pd.DataFrame,
    target: str,
    fraction: float,
    seed: int,
    shuffle: bool,
    stratify: bool,
    stage: str,
    calls: list[dict[str, object]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    calls.append(
        {
            "test_size": fraction,
            "random_state": seed,
            "shuffle": shuffle,
            "stratify": target if stratify else None,
        }
    )
    try:
        train, held_out = train_test_split(
            frame,
            test_size=fraction,
            random_state=seed,
            shuffle=shuffle,
            stratify=frame[target] if stratify else None,
        )
    except ValueError as error:
        error.add_note(f"Failure while reserving {stage} partition")
        raise
    return train, held_out


def _fraction(value: object, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is required")
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a fraction")
    fraction = float(value)
    if not math.isfinite(fraction) or not 0 < fraction < 1:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return fraction


def _validate_frame(frame: pd.DataFrame, row_id: str, target: str) -> None:
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame must be a pandas DataFrame")
    if not frame.columns.is_unique or any(
        not isinstance(name, str) or not name for name in frame.columns
    ):
        raise ValueError("column names must be unique nonempty strings")
    for name, value in (("row_id", row_id), ("target", target)):
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        if not value or value not in frame.columns:
            raise ValueError(f"{name} must name an existing column")
    ids = frame[row_id]
    if ids.isna().any():
        raise ValueError("source IDs must be nonmissing")
    values = ids.tolist()
    if any(isinstance(value, bool) for value in values) or not (
        all(isinstance(value, str) for value in values)
        or all(isinstance(value, Integral) for value in values)
    ):
        raise TypeError(
            "source IDs must be homogeneous string or integer IDs, excluding bool"
        )
    if not ids.is_unique:
        raise ValueError("source IDs must be unique")


def _protocol(
    frame: pd.DataFrame, protocol: Mapping[str, object] | None
) -> dict[str, object]:
    if protocol is None:
        return {"kind": "supplied"}
    if not isinstance(protocol, Mapping):
        raise TypeError("protocol must be a mapping")
    kind = protocol.get("kind")
    if kind not in ("supplied", "time", "group"):
        raise ValueError("protocol kind must be supplied, time or group")
    allowed = (
        {"kind", "description"}
        if kind == "supplied"
        else {"kind", "column", "description"}
    )
    if set(protocol) - allowed:
        raise ValueError("protocol has unknown keys")
    if kind != "supplied":
        column = protocol.get("column")
        if not isinstance(column, str) or column not in frame.columns:
            raise ValueError("protocol column must name an existing column")
    if "description" in protocol and not isinstance(protocol["description"], str):
        raise TypeError("protocol description must be a string")
    return dict(protocol)


def _source(frame: pd.DataFrame) -> dict[str, object]:
    snapshot = frame.copy(deep=True)
    snapshot.attrs.clear()
    payload = snapshot.to_parquet(engine="pyarrow", index=False, compression=None)
    return {
        "row_count": len(frame),
        "schema": [
            {"name": name, "dtype": str(frame[name].dtype)} for name in frame.columns
        ],
        "sha256": hashlib.sha256(payload).hexdigest(),
        "identity_format": "pandas-parquet-v1",
        "versions": {
            name: version(name)
            for name in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
        },
    }


def _ids(series: pd.Series) -> list[str | int]:
    return [
        int(value) if isinstance(value, Integral) else str(value) for value in series
    ]
