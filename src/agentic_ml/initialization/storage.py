"""Initialize project-associated local storage without experiment authority."""

import hashlib
import json
import os
import subprocess
from dataclasses import replace
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from .journal import read_journal, write_private
from .models import InitializationError, InitResult
from .preflight import check_path, probe_writable
from .validation import validate_document


def preflight_storage(
    root: Path, stores: dict[str, str], saved: dict[str, Any] | None
) -> None:
    """Reject unowned nonempty destinations before durable setup changes."""
    if (
        saved is not None
        and saved.get("storage_stage")
        and saved["status"] != "complete"
    ):
        for name in ("pyproject.toml", "uv.lock"):
            if (
                hashlib.sha256((root / name).read_bytes()).hexdigest()
                != saved["environment"]["checksums"][name]
            ):
                raise InitializationError(
                    "Interrupted storage metadata changed; review before retry"
                )
    cache = root / ".dvc/cache"
    check_path(cache)
    probe_writable(cache / ".setup-probe")
    ignore = root / ".gitignore"
    negations = (
        [
            line[1:].lstrip("/").rstrip("/")
            for line in ignore.read_text().splitlines()
            if line.startswith("!") and line != "!/.env.example"
        ]
        if ignore.exists()
        else []
    )
    for name, value in stores.items():
        path = root / value
        check_path(path)
        if name == "state":
            check_path(path / "project.json")
            state = path / "project.json"
            if saved is not None and state.exists():
                if validate_document(state.read_bytes(), "state") != {
                    "schema_version": "0.1",
                    "experiment": saved["experiment"],
                    "status": "unconfigured",
                    "approvals": [],
                    "runs": [],
                }:
                    raise InitializationError("Existing state identity conflict")
        if path.exists():
            if name == "mlflow_backend":
                occupied = True
                if not path.is_file():
                    raise InitializationError("Storage file destination conflict")
            else:
                if not path.is_dir():
                    raise InitializationError("Storage directory destination conflict")
                occupied = any(path.iterdir())
            stages = {"DVC": 0, "MLflow": 1, "state": 2}
            required_stage = {
                "dvc_store": 0,
                "mlflow_backend": 1,
                "artifacts": 1,
                "state": 2,
            }[name]
            owned = (
                saved is not None
                and stages.get(saved.get("storage_stage", ""), -1) >= required_stage
            )
            if occupied and not owned:
                raise InitializationError("Existing storage content conflict")
        probe_writable(path if name == "mlflow_backend" else path / ".setup-probe")
        if path.is_relative_to(root):
            relative = path.relative_to(root).as_posix()
            if any(
                fnmatchcase(relative, pattern)
                or fnmatchcase(relative + "/project.json", pattern)
                or pattern.startswith(relative + "/")
                for pattern in negations
            ):
                raise InitializationError(
                    "Ignore negation exposes selected storage conflict"
                )
    _dvc_configuration(root, root / stores["dvc_store"])
    if saved is not None and "MLflow" in saved["completed_steps"]:
        database = root / stores["mlflow_backend"]
        if not database.is_file():
            raise InitializationError("Missing MLflow storage conflict")
        env = dict(os.environ, MLFLOW_DISABLE_TELEMETRY="true")
        checked = subprocess.run(
            [
                str(root / ".venv/bin/python"),
                "-I",
                "-c",
                _MLFLOW_CHECK,
                str(database),
                str(root / stores["artifacts"]),
                saved["experiment"],
            ],
            cwd=root,
            env=env,
            capture_output=True,
            check=False,
        )
        if checked.returncode:
            raise InitializationError("Existing MLflow storage identity conflict")


def _dvc_configuration(root: Path, destination: Path) -> tuple[bool, bool]:
    """Read DVC's public effective configuration without changing its defaults."""
    for name in (".dvc/config", ".dvc/config.local", ".dvc/.gitignore", ".dvcignore"):
        check_path(root / name)
    if not (root / ".dvc").exists():
        return False, False
    env = dict(os.environ, DVC_NO_ANALYTICS="1")
    result = subprocess.run(
        [str(root / ".venv/bin/dvc"), "config", "--list"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise InitializationError("DVC configuration conflict")
    config = dict(
        line.split("=", 1) for line in result.stdout.splitlines() if "=" in line
    )
    default = config.get("core.remote")
    configured_cache = config.get("cache.dir")
    if (
        configured_cache is not None
        and Path(configured_cache).resolve() != root / ".dvc/cache"
    ):
        raise InitializationError("Existing DVC cache location conflict")
    named = config.get("remote.agentic-ml-store.url")
    for value in (named, config.get(f"remote.{default}.url") if default else None):
        if value is not None and (
            "://" in value or Path(value).resolve() != destination.resolve()
        ):
            raise InitializationError("DVC default or named remote conflict")
    if default is not None and f"remote.{default}.url" not in config:
        raise InitializationError("DVC default remote conflict")
    return default is not None, named is not None


def initialize_storage(result: InitResult) -> InitResult:
    """Initialize stores with an exclusive setup lock and safe failure evidence."""
    root = result.project_root
    lock = root / ".agentic-ml/init.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)
    journal = read_journal(root)
    assert journal is not None
    try:
        return _initialize_storage(result, journal)
    except (OSError, InitializationError) as error:
        stage = journal.get("storage_stage", "DVC")
        journal["status"] = "incomplete"
        code = journal.get("storage_exit_code")
        journal["storage_failure"] = {"stage": stage, "exit_code": code}
        write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
        raise InitializationError(
            f"{stage} setup failed"
            + (f" (exit {code})" if code is not None else "")
            + "; available evidence preserved",
            stage=stage,
            completed_steps=tuple(journal["completed_steps"]),
            recovery="Resolve the storage failure; preserve .agentic-ml/init.json and backups, then rerun init with the same options.",
        ) from error
    finally:
        lock.unlink(missing_ok=True)


def _initialize_storage(result: InitResult, journal: dict[str, Any]) -> InitResult:
    root = result.project_root
    journal["storage_stage"] = "DVC"
    journal["storage_exit_code"] = None
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    destination = root / journal["storage"]["dvc_store"]
    env = dict(os.environ)
    for key in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    env["DVC_NO_ANALYTICS"] = "1"
    has_default, has_named = _dvc_configuration(root, destination)
    commands = []
    if not (root / ".dvc").exists():
        commands.append(["init"])
    if not has_default:
        if has_named:
            commands.append(["remote", "default", "agentic-ml-store"])
        else:
            commands.append(
                ["remote", "add", "--default", "agentic-ml-store", str(destination)]
            )
    for arguments in commands:
        completed = subprocess.run(
            [str(root / ".venv/bin/dvc"), *arguments],
            cwd=root,
            env=env,
            capture_output=True,
            check=False,
        )
        journal["storage_exit_code"] = completed.returncode
        if completed.returncode:
            raise InitializationError(
                f"DVC setup failed (exit {completed.returncode}); evidence preserved",
                stage="DVC",
                completed_steps=tuple(journal["completed_steps"]),
            )
    destination.mkdir(parents=True, exist_ok=True)
    (root / ".dvc/cache").mkdir(parents=True, exist_ok=True)
    if "DVC" not in journal["completed_steps"]:
        journal["completed_steps"].append("DVC")
        journal["pending_steps"].remove("DVC")
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    database = root / journal["storage"]["mlflow_backend"]
    artifacts = root / journal["storage"]["artifacts"]
    journal["storage_stage"] = "MLflow"
    journal["storage_exit_code"] = None
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    database.parent.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            str(root / ".venv/bin/python"),
            "-I",
            "-c",
            _MLFLOW_SETUP,
            str(database),
            str(artifacts),
            journal["experiment"],
        ],
        cwd=root,
        env=env,
        capture_output=True,
        check=False,
    )
    journal["storage_exit_code"] = completed.returncode
    if completed.returncode:
        raise InitializationError(
            f"MLflow setup failed (exit {completed.returncode}); evidence preserved",
            stage="MLflow",
            completed_steps=tuple(journal["completed_steps"]),
        )
    if "MLflow" not in journal["completed_steps"]:
        journal["completed_steps"].append("MLflow")
        journal["pending_steps"].remove("MLflow")
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    state = root / journal["storage"]["state"] / "project.json"
    journal["storage_stage"] = "state"
    journal["storage_exit_code"] = None
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    content = json.dumps(
        {
            "schema_version": "0.1",
            "experiment": journal["experiment"],
            "status": "unconfigured",
            "approvals": [],
            "runs": [],
        }
    ).encode()
    state.parent.mkdir(parents=True, exist_ok=True)
    if not state.exists():
        write_private(state, content)
    validate_document(state.read_bytes(), "state")
    for stage in ("state", "finalize"):
        if stage not in journal["completed_steps"]:
            journal["completed_steps"].append(stage)
    journal["pending_steps"] = []
    journal["status"] = "complete"
    journal.pop("storage_failure", None)
    write_private(root / ".agentic-ml/init.json", json.dumps(journal).encode())
    return replace(result, setup_pending=())


_MLFLOW_SETUP = """
import sys
from pathlib import Path
from mlflow import MlflowClient
database, artifacts, name = sys.argv[1:]
client = MlflowClient(tracking_uri="sqlite:///" + database)
name = "agentic-ml:" + name
location = Path(artifacts).as_uri()
experiment = client.get_experiment_by_name(name)
if experiment is None:
    client.create_experiment(name, artifact_location=location)
experiment = client.get_experiment_by_name(name)
assert experiment is not None and experiment.artifact_location == location
"""

_MLFLOW_CHECK = """
import sys
from pathlib import Path
from mlflow import MlflowClient
database, artifacts, name = sys.argv[1:]
uri = "sqlite:///" + Path(database).as_uri() + "?mode=ro&uri=true"
client = MlflowClient(tracking_uri=uri)
experiment = client.get_experiment_by_name("agentic-ml:" + name)
assert experiment is not None and experiment.artifact_location == Path(artifacts).as_uri()
"""
