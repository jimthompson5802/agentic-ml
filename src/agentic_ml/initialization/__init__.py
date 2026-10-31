"""Initialize experiment-owned draft files through installed public interfaces."""

import hashlib
import json
import os
import socket
from importlib.resources import files
from pathlib import Path
from typing import Any

import tomlkit
import yaml

from .journal import read_journal, write_private
from .models import InitializationError, InitOptions, InitResult
from .preflight import (
    check_path,
    probe_writable,
    project_identity,
    storage_paths,
    validate_destinations,
)
from .scaffold import render
from .validation import validate_document

__all__ = ["InitOptions", "InitResult", "InitializationError", "initialize_project"]


def _initialize_project(options: InitOptions) -> InitResult:
    """Create draft scaffolding; environment and storage setup remain pending."""
    root, metadata, package = project_identity(options)
    stores = storage_paths(options, root)
    contents = render(options, package)
    validate_destinations(root, contents)
    project_config = yaml.safe_load(contents["project.yaml"])
    project_config["storage"] = stores
    contents["project.yaml"] = yaml.safe_dump(project_config, sort_keys=False).encode()
    validate_document(contents["project.yaml"], "project")
    validate_document(
        contents[f"experiments/{options.experiment}/experiment.yaml"], "experiment"
    )
    validate_document(
        contents[f"experiments/{options.experiment}/search-space.yaml"], "search-space"
    )
    saved = read_journal(root)
    if saved is not None:
        if saved.get("schema_version") != "0.1":
            raise InitializationError("Setup journal schema conflict")
        if (
            saved["experiment"] != options.experiment
            or saved["package"] != package
            or saved["storage"] != stores
        ):
            raise InitializationError("Project identity conflict")
        if set(saved["inventory"]) != set(contents) | {"pyproject.toml", ".gitignore"}:
            raise InitializationError("Saved setup inventory conflict")
        if "scaffold" not in saved["completed_steps"]:
            return _resume_scaffold(root, saved)
        for name in saved["inventory"]:
            if not (root / name).is_file():
                raise InitializationError("Missing saved scaffold file")
        current_config = validate_document(
            (root / "project.yaml").read_bytes(), "project"
        )
        if current_config != project_config:
            raise InitializationError("Saved project identity or storage conflict")
        base = root / f"experiments/{options.experiment}"
        experiment = validate_document(
            (base / "experiment.yaml").read_bytes(), "experiment"
        )
        expected = validate_document(
            contents[f"experiments/{options.experiment}/experiment.yaml"], "experiment"
        )
        if experiment != expected:
            raise InitializationError("Saved experiment identity conflict")
        validate_document((base / "search-space.yaml").read_bytes(), "search-space")
        return InitResult(
            root, (), (), tuple(sorted(saved["inventory"])), ("environment", "storage")
        )
    if "build-system" in metadata:
        name = f"src/{package}/__init__.py"
        contents[name] = (root / name).read_bytes()
    original = (root / "pyproject.toml").read_bytes()
    document = tomlkit.parse(original.decode())
    if "build-system" not in metadata:
        document["build-system"] = {
            "requires": ["hatchling>=1.27,<2"],
            "build-backend": "hatchling.build",
        }
        document.setdefault("tool", {}).setdefault("hatch", {}).setdefault(
            "build", {}
        ).setdefault("targets", {}).setdefault("wheel", {})["packages"] = [
            f"src/{package}"
        ]
    contents["pyproject.toml"] = tomlkit.dumps(document).encode()
    ignore = root / ".gitignore"
    previous_ignore = ignore.read_bytes() if ignore.exists() else b""
    block = (
        files("agentic_ml").joinpath("templates/initialization/ignore.txt").read_bytes()
    )
    extra = [
        "/" + value
        for value in stores.values()
        if not Path(value).is_absolute() and not value.startswith(".agentic-ml/")
    ]
    if extra:
        block = block.replace(
            b"# END agentic-ml initialization",
            ("\n".join(extra) + "\n# END agentic-ml initialization").encode(),
        )
    contents[".gitignore"] = (
        previous_ignore
        + (b"\n" if previous_ignore and not previous_ignore.endswith(b"\n") else b"")
        + block
    )
    conflicts = tuple(
        name
        for name, value in contents.items()
        if name not in ("pyproject.toml", ".gitignore")
        and (root / name).exists()
        and (root / name).read_bytes() != value
    )
    if conflicts:
        raise InitializationError(
            "File conflict: " + ", ".join(conflicts), conflicts=conflicts
        )
    for name in (*contents, ".agentic-ml/init.json"):
        probe_writable(root / name)
    for store_path in stores.values():
        probe_writable(root / store_path)
    created: list[str] = []
    updated: list[str] = []
    unchanged: list[str] = []
    originals = {
        name: (root / name).read_bytes() if (root / name).exists() else None
        for name in contents
    }
    state = root / ".agentic-ml"
    state.mkdir(mode=0o700, exist_ok=True)
    lock = state / "init.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        json.dump({"pid": os.getpid(), "hostname": socket.gethostname()}, stream)
    try:
        backup_dir = state / "backups"
        backup_dir.mkdir(mode=0o700, exist_ok=True)
        backups: dict[str, str] = {}
        for name in ("pyproject.toml", "uv.lock", ".gitignore"):
            target = root / name
            if target.exists():
                backup_name = name.lstrip(".") + ".original"
                write_private(backup_dir / backup_name, target.read_bytes())
                backups[name] = "backups/" + backup_name
        journal = {
            "schema_version": "0.1",
            "experiment": options.experiment,
            "package": package,
            "storage": stores,
            "inventory": sorted(contents),
            "checksums": {
                name: hashlib.sha256(value).hexdigest()
                for name, value in contents.items()
            },
            "planned_contents": {
                name: value.decode()
                for name, value in contents.items()
                if originals[name] != value
            },
            "original_checksums": {
                name: hashlib.sha256(value).hexdigest() if value is not None else None
                for name, value in originals.items()
            },
            "created_paths": [],
            "backups": backups,
            "completed_steps": ["preflight"],
            "pending_steps": [
                "scaffold",
                "lock",
                "sync",
                "DVC",
                "MLflow",
                "state",
                "finalize",
            ],
            "status": "incomplete",
        }
        write_private(state / "init.json", json.dumps(journal).encode())
        for name, value in contents.items():
            target = root / name
            check_path(target)
            current = target.read_bytes() if target.exists() else None
            if current != originals[name]:
                raise InitializationError(
                    "Destination changed during initialization", stage="scaffold"
                )
            if current == value:
                unchanged.append(name)
                continue
            (updated if current is not None else created).append(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            write_private(target, value)
        journal["created_paths"] = created
        journal["completed_steps"] = ["preflight", "scaffold"]
        journal["pending_steps"] = [
            "lock",
            "sync",
            "DVC",
            "MLflow",
            "state",
            "finalize",
        ]
        write_private(state / "init.json", json.dumps(journal).encode())
    except OSError as error:
        raise InitializationError(
            "Scaffolding failed; preserved available setup evidence",
            stage="scaffold",
            completed_steps=("preflight",),
            recovery="Resolve the filesystem error; preserve .agentic-ml/init.json and backups for review before retry.",
        ) from error
    finally:
        lock.unlink(missing_ok=True)
    return InitResult(
        root,
        tuple(sorted(created)),
        tuple(sorted(updated)),
        tuple(sorted(unchanged)),
        ("environment", "storage"),
    )


def _resume_scaffold(root: Path, saved: dict[str, Any]) -> InitResult:
    """Resume only unchanged planned writes after a filesystem interruption."""
    pending: dict[str, bytes] = {}
    for name in saved["inventory"]:
        target = root / name
        check_path(target)
        current = (
            hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
        )
        if current == saved["checksums"][name]:
            continue
        if name not in saved["planned_contents"]:
            raise InitializationError(
                "Preserved project file changed during interrupted setup"
            )
        planned = saved["planned_contents"][name].encode()
        if hashlib.sha256(planned).hexdigest() != saved["checksums"][name]:
            raise InitializationError("Setup journal content conflict")
        if current != saved["original_checksums"][name]:
            raise InitializationError(
                "Interrupted setup files changed; review before retry"
            )
        pending[name] = planned
    lock = root / ".agentic-ml/init.lock"
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)
    try:
        for name, value in pending.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            write_private(target, value)
        saved["completed_steps"] = ["preflight", "scaffold"]
        saved["pending_steps"] = ["lock", "sync", "DVC", "MLflow", "state", "finalize"]
        write_private(root / ".agentic-ml/init.json", json.dumps(saved).encode())
    finally:
        lock.unlink(missing_ok=True)
    return InitResult(root, (), tuple(sorted(pending)), (), ("environment", "storage"))


def initialize_project(options: InitOptions) -> InitResult:
    """Create draft files, preserving safe diagnostics on metadata or I/O failure."""
    try:
        return _initialize_project(options)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise InitializationError(
            "Invalid setup metadata or filesystem destination"
        ) from error
