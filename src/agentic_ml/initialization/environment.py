"""Synchronize the selected experiment environment while preserving its pin."""

import hashlib
import json
import os
import subprocess
import tomllib
from dataclasses import replace
from typing import Any

import tomlkit

from .journal import read_journal, write_private
from .models import InitializationError, InitResult
from .preflight import check_path

REQUIREMENTS = (
    "numpy>=2,<3",
    "pandas>=2,<4",
    "scikit-learn>=1.6,<2",
    "nbclient>=0.10,<1",
    "ipykernel>=6,<8",
    "nbformat>=5,<6",
    "dvc>=3,<4",
    "mlflow>=3,<4",
)


def synchronize(result: InitResult) -> InitResult:
    """Declare requirements, lock and sync with restartable private evidence."""
    root = result.project_root
    lock = root / ".agentic-ml/init.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)
    try:
        return _synchronize(result)
    finally:
        lock.unlink(missing_ok=True)


def _synchronize(result: InitResult) -> InitResult:
    root = result.project_root
    journal = read_journal(root)
    assert journal is not None
    journal_path = root / ".agentic-ml/init.json"
    names = ("pyproject.toml", "uv.lock")
    for name in names:
        check_path(root / name)
    previous = journal.get("environment")
    if previous is not None and not previous.get("verified", False):
        for name in names:
            if (
                hashlib.sha256((root / name).read_bytes()).hexdigest()
                != previous["checksums"][name]
            ):
                raise InitializationError(
                    "Interrupted environment metadata changed; review before retry",
                    stage="lock",
                )
    document = tomlkit.parse((root / "pyproject.toml").read_text())
    source = tomllib.loads(tomlkit.dumps(document))["tool"]["uv"]["sources"][
        "agentic-ml"
    ]
    dependencies = document["project"]["dependencies"]
    for requirement in REQUIREMENTS:
        if requirement not in dependencies:
            dependencies.append(requirement)
    original_metadata = (root / "pyproject.toml").read_bytes()
    original_lock = (root / "uv.lock").read_bytes()
    planned = tomlkit.dumps(document).encode()
    if planned != (root / "pyproject.toml").read_bytes():
        write_private(root / "pyproject.toml", planned)
    environment: dict[str, Any] = {
        "checksums": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in names
        }
    }
    journal["environment"] = environment
    write_private(journal_path, json.dumps(journal).encode())
    env = dict(os.environ)
    for key in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    env["UV_PROJECT_ENVIRONMENT"] = str(root / ".venv")
    for stage, arguments in (
        ("lock", ["lock"]),
        ("sync", ["sync", "--locked", "--inexact"]),
        ("environment-check", ["lock", "--check"]),
    ):
        try:
            completed = subprocess.run(
                ["uv", *arguments, "--project", str(root)],
                cwd=root,
                env=env,
                capture_output=True,
                check=False,
            )
            code = completed.returncode
        except OSError as error:
            raise InitializationError(
                "Unable to start uv; setup evidence preserved",
                stage=stage,
                completed_steps=tuple(journal["completed_steps"]),
            ) from error
        environment["checksums"] = {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in names
        }
        environment["last_stage"] = stage
        environment["exit_code"] = code
        write_private(journal_path, json.dumps(journal).encode())
        if code:
            raise InitializationError(
                f"uv {stage} failed (exit {code}); setup evidence preserved",
                stage=stage,
                completed_steps=tuple(journal["completed_steps"]),
                recovery="Resolve the uv failure; rerun init with the same options and unchanged metadata. Review .agentic-ml/init.json and backups.",
            )
        metadata = tomllib.loads((root / "pyproject.toml").read_text())
        locked = tomllib.loads((root / "uv.lock").read_text())
        expected = source["git"] + "?rev=" + source["rev"] + "#" + source["rev"]
        pins = [p for p in locked["package"] if p["name"] == "agentic-ml"]
        if metadata["tool"]["uv"]["sources"]["agentic-ml"] != source or (
            len(pins) != 1 or pins[0]["source"].get("git") != expected
        ):
            raise InitializationError(
                "Harness pin changed; review before retry", stage=stage
            )
        if stage != "environment-check" and stage not in journal["completed_steps"]:
            journal["completed_steps"].append(stage)
        if stage in journal["pending_steps"]:
            journal["pending_steps"].remove(stage)
        write_private(journal_path, json.dumps(journal).encode())
    probe = subprocess.run(
        [
            str(root / ".venv/bin/python"),
            "-I",
            "-c",
            "import importlib, sys; "
            "[importlib.import_module(name) for name in sys.argv[1:]]",
            "numpy",
            "pandas",
            "sklearn",
            "nbclient",
            "ipykernel",
            "nbformat",
            "dvc",
            "mlflow",
            journal["package"],
        ],
        cwd=root,
        env=env,
        capture_output=True,
        check=False,
    )
    if probe.returncode:
        raise InitializationError(
            "Installed environment import verification failed",
            stage="environment-check",
            completed_steps=tuple(journal["completed_steps"]),
        )
    if "environment-check" not in journal["completed_steps"]:
        journal["completed_steps"].append("environment-check")
    environment["verified"] = True
    write_private(journal_path, json.dumps(journal).encode())
    changed = set(result.updated)
    unchanged = set(result.unchanged)
    if planned != original_metadata:
        changed.add("pyproject.toml")
        unchanged.discard("pyproject.toml")
    if original_lock != (root / "uv.lock").read_bytes():
        changed.add("uv.lock")
    return replace(
        result,
        updated=tuple(sorted(changed)),
        unchanged=tuple(sorted(unchanged)),
        setup_pending=("storage",),
    )
