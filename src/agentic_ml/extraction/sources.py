"""Read declared local bytes using native pandas readers."""

import hashlib
from collections.abc import Callable, Mapping
from io import BytesIO
from pathlib import Path

import pandas as pd


def resolve_local(root: Path, path: Path, *, inside: bool = False) -> Path:
    """Resolve a local declaration without symlinks or relative traversal."""
    if ".." in path.parts:
        raise ValueError(f"Relative traversal is unsupported: {path}")
    absolute = root / path
    for candidate in (absolute, *absolute.parents):
        if candidate.is_symlink():
            raise ValueError(f"Symlink path is unsupported: {candidate}")
    if inside and not absolute.is_relative_to(root):
        raise ValueError(f"Project-owned path is outside project: {path}")
    return absolute


def local_path(root: Path, path: Path, *, inside: bool = False) -> Path:
    """Require a declared regular input file."""
    absolute = resolve_local(root, path, inside=inside)
    if not absolute.is_file():
        if not absolute.exists():
            raise FileNotFoundError(absolute)
        raise ValueError(f"Input must be a regular file: {path}")
    return absolute


def schema(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Describe the actual pandas columns without introducing schema classes."""
    if not frame.columns.is_unique or any(
        not isinstance(name, str) for name in frame.columns
    ):
        raise ValueError("DataFrame columns must be unique strings")
    return [
        {"name": name, "dtype": str(dtype)}
        for name, dtype in zip(frame.columns, frame.dtypes, strict=True)
    ]


def fingerprint(path: Path) -> tuple[int, int, int, int, int]:
    """Detect ordinary replacement and mutation of a declared input."""
    stat = path.stat()
    return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def stable_bytes(path: Path) -> tuple[bytes, tuple[int, int, int, int, int]]:
    """Read owned bytes while checking the declared file did not change."""
    before = fingerprint(path)
    data = path.read_bytes()
    if fingerprint(path) != before:
        raise ValueError(f"Declared input changed during reading: {path}")
    return data, before


def native_frame(
    reader: Callable[..., object], data: bytes, options: Mapping[str, object]
) -> pd.DataFrame:
    """Forward dynamic native reader kwargs, then verify the concrete result.

    Reader options are intentionally supplied by the experiment project. Pandas
    performs option validation; this one boundary checks the result without
    pretending the caller's arbitrary options have a statically fixed signature.
    """
    result = reader(BytesIO(data), **options)
    if not isinstance(result, pd.DataFrame):
        raise TypeError("Native source reader must return a pandas DataFrame")
    return result


def read_source(
    path: Path, name: str, options: Mapping[str, object]
) -> tuple[pd.DataFrame, dict[str, object], tuple[int, int, int, int, int]]:
    """Parse the same owned bytes used for the recorded content identity."""
    data, snapshot = stable_bytes(path)
    kind = path.suffix.lower().removeprefix(".")
    # Native readers validate arbitrary keyword options. Keep their return as
    # object until the public DataFrame boundary is checked, without Any.
    reader: Callable[..., object]
    if kind == "csv":
        reader = pd.read_csv
        effective: dict[str, object] = {
            "encoding": "utf-8",
            "sep": ",",
            "header": "infer",
            "index_col": None,
            "on_bad_lines": "error",
            "dtype_backend": "numpy_nullable",
        }
        if "delimiter" in options:
            effective.pop("sep")
    elif kind == "parquet":
        reader = pd.read_parquet
        effective = {"engine": "pyarrow", "dtype_backend": "numpy_nullable"}
    else:
        raise ValueError(f"Unsupported local source format: {path}")
    effective.update(options)
    if kind == "parquet" and effective["engine"] != "pyarrow":
        raise ValueError("Parquet extraction requires engine='pyarrow'")
    frame = native_frame(reader, data, effective)
    return (
        frame,
        {
            "name": name,
            "format": kind,
            "reader_options": effective,
            "schema": schema(frame),
            "row_count": len(frame),
            "byte_count": len(data),
            "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
        },
        snapshot,
    )
