"""Preserve native artifact ownership when publishing project results."""

import json
import tempfile
from collections.abc import Mapping
from pathlib import Path

from mlflow import MlflowClient


def require_available(client: MlflowClient, run_id: str, path: str) -> None:
    """Reject an occupied artifact path or a conflicting non-directory ancestor."""
    parts = path.split("/")
    for index in range(len(parts)):
        parent = "/".join(parts[:index])
        name = "/".join(parts[: index + 1])
        for entry in client.list_artifacts(run_id, parent or None):
            if entry.path == name and (index == len(parts) - 1 or not entry.is_dir):
                raise FileExistsError(f"Artifact path already exists: {name}")


def shared_provenance(
    client: MlflowClient, run_id: str, provenance: Mapping[str, object]
) -> None:
    """Reuse identical shared references without overwriting existing bytes."""
    existing = {item.path: item for item in client.list_artifacts(run_id)}
    if "provenance.json" in existing:
        if existing["provenance.json"].is_dir:
            raise FileExistsError("provenance.json is already a directory")
        previous = Path(client.download_artifacts(run_id, "provenance.json"))
        try:
            saved_provenance = json.loads(previous.read_text(encoding="utf-8"))
            saved_json = json.dumps(saved_provenance, sort_keys=True, allow_nan=False)
        except (ValueError, UnicodeDecodeError) as decode_error:
            raise FileExistsError(
                "Existing provenance.json is corrupt"
            ) from decode_error
        if saved_json != json.dumps(dict(provenance), sort_keys=True, allow_nan=False):
            raise FileExistsError("Conflicting shared provenance.json")
    else:
        with tempfile.TemporaryDirectory(prefix="agentic-ml-tracking-") as local:
            path = Path(local) / "provenance.json"
            path.write_text(
                json.dumps(dict(provenance), allow_nan=False), encoding="utf-8"
            )
            client.log_artifact(run_id, str(path))
