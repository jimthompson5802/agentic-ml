"""Validate project identity before modifying an experiment project."""

import json
import keyword
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from fnmatch import fnmatchcase
from importlib.metadata import distribution
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from .models import InitializationError, InitOptions


def project_identity(options: InitOptions) -> tuple[Path, dict[str, Any], str]:
    """Require an explicit Git root and the matching installed pinned harness."""
    root = options.project_root.absolute()
    if root.is_symlink() or not root.is_dir():
        raise InitializationError("Project root must be an existing directory")
    root = root.resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode or Path(result.stdout.strip()).resolve() != root:
        raise InitializationError("Select the Git project root explicitly")
    if (root / "src/agentic_ml").exists():
        raise InitializationError("Cannot initialize the harness source project")
    for name in ("pyproject.toml", "uv.lock"):
        check_path(root / name)
    try:
        metadata = tomllib.loads((root / "pyproject.toml").read_text())
        lock = tomllib.loads((root / "uv.lock").read_text())
        project = metadata["project"]
        source = metadata["tool"]["uv"]["sources"]["agentic-ml"]
        dependencies = project["dependencies"]
        revision = source["rev"]
        url = source["git"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise InitializationError("Missing or invalid project metadata/lock") from error
    reject_credentials(metadata)
    if (
        not isinstance(revision, str)
        or re.fullmatch(r"[0-9a-fA-F]{40}", revision) is None
    ):
        raise InitializationError("Harness dependency requires a full commit SHA")
    if (
        not isinstance(url, str)
        or urlsplit(url).scheme not in ("https", "file")
        or set(source) != {"git", "rev"}
        or not isinstance(dependencies, list)
        or not any(
            isinstance(d, str) and re.match(r"^agentic[-_]ml(?:$|[<>=!~ ;\[])", d)
            for d in dependencies
        )
    ):
        raise InitializationError("Invalid pinned harness dependency")
    candidates = [p for p in lock.get("package", []) if p.get("name") == "agentic-ml"]
    if len(candidates) != 1:
        raise InitializationError("Lock must contain exactly one pinned harness")
    locked = urlsplit(candidates[0].get("source", {}).get("git", ""))
    if (
        locked.fragment != revision
        or parse_qs(locked.query).get("rev") != [revision]
        or locked._replace(query="", fragment="").geturl() != url
    ):
        raise InitializationError("Locked harness does not match the declared pin")
    installed = distribution("agentic-ml")
    direct = json.loads(installed.read_text("direct_url.json") or "{}")
    if (
        Path(sys.prefix).resolve() != (root / ".venv").resolve()
        or direct.get("url") != url
        or direct.get("vcs_info", {}).get("commit_id") != revision
        or direct.get("dir_info", {}).get("editable")
    ):
        raise InitializationError("Use the selected project's installed pinned harness")
    uv = metadata.get("tool", {}).get("uv", {})
    if "workspace" in uv:
        raise InitializationError("Workspace projects are not supported by init")
    for path in root.rglob("pyproject.toml"):
        relative = path.relative_to(root)
        if len(relative.parts) > 1 and relative.parts[0] not in (
            ".venv",
            ".git",
            ".agentic-ml",
        ):
            raise InitializationError(
                "Nested project metadata conflicts with initialization"
            )
    if re.fullmatch(r"[a-z][a-z0-9-]*", options.experiment) is None:
        raise InitializationError("Invalid experiment name")
    package = options.package_name or project.get("name", "").replace("-", "_")
    if (
        not package.isidentifier()
        or keyword.iskeyword(package)
        or package == "agentic_ml"
    ):
        raise InitializationError("Specify a valid project package name")
    build = metadata.get("build-system")
    if build is not None:
        if (
            (
                options.package_name is None
                and not (root / ".agentic-ml/init.json").exists()
            )
            or not isinstance(build, dict)
            or not (root / f"src/{package}/__init__.py").is_file()
        ):
            raise InitializationError(
                "Existing build requires an explicitly selected src package"
            )
    elif uv.get("package") is True or "hatch" in metadata.get("tool", {}):
        raise InitializationError("Existing package build settings conflict")
    return root, metadata, package


def check_path(path: Path) -> None:
    """Reject symlink components and non-directory parents without following them."""
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise InitializationError("Symlink destination conflict")
        if parent != path and parent.exists() and not parent.is_dir():
            raise InitializationError("Destination parent is not a directory")


def storage_paths(options: InitOptions, root: Path) -> dict[str, str]:
    """Resolve explicit local setup destinations and reject unsafe overlaps."""
    selected: dict[str, Path] = {}
    for name, supplied, default in (
        ("dvc_store", options.dvc_store, ".agentic-ml/dvc-store"),
        ("mlflow_backend", options.mlflow_backend, ".agentic-ml/mlflow.db"),
        ("artifacts", options.artifact_store, ".agentic-ml/artifacts"),
        ("state", options.state_store, ".agentic-ml/state"),
    ):
        value = str(supplied) if supplied is not None else default
        if ":" in value or "@" in value or "\n" in value or "\r" in value:
            raise InitializationError(
                "Storage must be a local path without credentials or URI schemes"
            )
        path = Path(value)
        path = Path(os.path.abspath(root / path))
        check_path(path)
        protected = (
            ".git",
            ".venv",
            "src",
            "experiments",
            "project.yaml",
            "pyproject.toml",
            "uv.lock",
            ".gitignore",
            ".dvc",
        )
        for name_protected in protected:
            other = root / name_protected
            if path == root or path.is_relative_to(other) or other.is_relative_to(path):
                raise InitializationError("Storage overlaps protected project paths")
        if not path.is_relative_to(root) and path.exists():
            if path.is_file() or any(path.iterdir()):
                raise InitializationError("External storage contains existing content")
        selected[name] = path
    values = list(selected.values())
    if any(
        a.is_relative_to(b) or b.is_relative_to(a)
        for i, a in enumerate(values)
        for b in values[i + 1 :]
    ):
        raise InitializationError("Storage destinations overlap")
    return {
        name: str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        for name, path in selected.items()
    }


def validate_destinations(root: Path, contents: dict[str, bytes]) -> None:
    """Preflight all scaffold destinations and existing ignore exceptions."""
    for name in (
        *contents,
        "uv.lock",
        "pyproject.toml",
        ".gitignore",
        ".agentic-ml/init.json",
        ".agentic-ml/init.lock",
    ):
        check_path(root / name)
        path = root / name
        if path.exists() and not path.is_file():
            raise InitializationError("Expected a file destination")
    lock = root / ".agentic-ml/init.lock"
    if lock.exists():
        raise InitializationError(
            "Initialization is already locked",
            recovery="Confirm no live initializer before manually removing .agentic-ml/init.lock.",
        )
    ignore = root / ".gitignore"
    if ignore.exists():
        for line in ignore.read_text().splitlines():
            if not line.startswith("!") or line == "!/.env.example":
                continue
            pattern = line[1:].lstrip("/").rstrip("/")
            protected = (".agentic-ml", ".venv", "data", ".env", ".env.local")
            if any(
                pattern.startswith(name + "/")
                or fnmatchcase(name, pattern)
                or fnmatchcase(name + "/state/project.json", pattern)
                for name in protected
            ):
                raise InitializationError(
                    "Ignore negation conflicts with setup store exclusions"
                )


def reject_credentials(value: object) -> None:
    """Refuse explicit credentials before copying metadata into private backups."""
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                isinstance(key, str)
                and key.lower()
                in {
                    "password",
                    "token",
                    "secret",
                    "api_key",
                    "access_key",
                    "secret_key",
                }
                and item
            ):
                raise InitializationError(
                    "Keep credentials outside project configuration"
                )
            reject_credentials(item)
    elif isinstance(value, list):
        for item in value:
            reject_credentials(item)
    elif isinstance(value, str) and "://" in value:
        uri = urlsplit(value)
        if uri.username is not None or uri.password is not None:
            raise InitializationError("Keep credentials outside project configuration")


def probe_writable(path: Path) -> None:
    """Check setup write access using only an automatically removed private file."""
    parent = path.parent
    while not parent.exists():
        parent = parent.parent
    try:
        with tempfile.TemporaryFile(dir=parent) as stream:
            stream.write(b"setup permission probe")
            stream.flush()
    except OSError as error:
        raise InitializationError("Setup destination is not writable") from error
