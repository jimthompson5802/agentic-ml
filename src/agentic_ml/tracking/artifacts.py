"""Preserve native artifact ownership when publishing project results."""

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
