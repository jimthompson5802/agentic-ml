"""Publish pandas output together with plain-dictionary extraction metadata."""

import hashlib
import json
import math
import shutil
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from tempfile import mkdtemp
from time import monotonic

import pandas as pd

from agentic_ml.extraction.sources import schema


def validate_json(value: object) -> None:
    """Reject configuration that cannot be recorded literally as JSON."""
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Extraction settings must contain finite numbers")
        return
    if isinstance(value, list):
        for item in value:
            validate_json(item)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for item in value.values():
            validate_json(item)
        return
    raise TypeError("Extraction settings must contain JSON-compatible values")


def digest(data: bytes) -> str:
    """Identify bytes independently of pandas' logical representations."""
    return "sha256:" + hashlib.sha256(data).hexdigest()


def publish(
    frame: pd.DataFrame,
    destination: Path,
    kind: str,
    report: dict[str, object],
    clock: float,
    verify: Callable[[], None],
) -> None:
    """Prepare a readable output/report pair before exposing the destination."""
    staging = Path(mkdtemp(prefix=".extraction-", dir=destination.parent))
    try:
        path = staging / f"dataset.{kind}"
        if kind == "csv":
            options: dict[str, object] = {
                "encoding": "utf-8",
                "sep": ",",
                "header": True,
                "lineterminator": "\n",
                "index": False,
            }
            frame.to_csv(
                path,
                encoding="utf-8",
                sep=",",
                header=True,
                lineterminator="\n",
                index=False,
            )
            restored = pd.read_csv(path, dtype_backend="numpy_nullable")
        else:
            options = {"engine": "pyarrow", "compression": "snappy", "index": False}
            frame.to_parquet(path, engine="pyarrow", compression="snappy", index=False)
            restored = pd.read_parquet(
                path, engine="pyarrow", dtype_backend="numpy_nullable"
            )
        if restored.columns.tolist() != frame.columns.tolist() or len(restored) != len(
            frame
        ):
            raise ValueError("Serialized output has different rows or columns")
        data = path.read_bytes()
        report["output"] = {
            "filename": path.name,
            "format": kind,
            "byte_count": len(data),
            "sha256": digest(data),
            "row_count": len(frame),
            "frame_schema": schema(frame),
            "schema": schema(restored),
            "writer_options": options,
        }
        report["versions"] = {
            name: version(name) for name in ("agentic-ml", "pandas", "pyarrow")
        }
        verify()
        report["completed_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        report["elapsed_seconds"] = monotonic() - clock
        (staging / "extraction.json").write_text(
            json.dumps(report, allow_nan=False), encoding="utf-8"
        )
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(destination)
        staging.rename(destination)
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(f"extraction output/publication; staging={staging}")
        if staging.exists():
            try:
                shutil.rmtree(staging)
            except OSError as cleanup_error:
                if error is None:
                    raise
                error.add_note(f"Staging cleanup failed at {staging}: {cleanup_error}")
