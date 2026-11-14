"""Validate committed project references before native result publication."""

import hashlib
import re
import subprocess
from collections.abc import Mapping
from pathlib import Path, PurePosixPath


def object_map(value: object, field: str) -> Mapping[str, object]:
    """Require an ordinary string-keyed record and identify invalid input fields."""
    if not isinstance(value, Mapping) or any(not isinstance(k, str) for k in value):
        raise TypeError(f"{field} must be a string-keyed mapping")
    return value


def local_path(root: Path, name: object) -> Path:
    """Resolve normalized existing project paths without symlink traversal."""
    if not isinstance(name, str):
        raise TypeError("reference path must be a string")
    if (
        not name
        or "\\" in name
        or PurePosixPath(name).is_absolute()
        or any(part in ("", ".", "..") for part in name.split("/"))
    ):
        raise ValueError(f"Invalid project-relative path: {name}")
    path = root / name
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f"Symlink reference: {name}")
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def local_file(root: Path, name: object) -> Path:
    """Require an existing regular project file for a content reference."""
    path = local_path(root, name)
    if not path.is_file():
        raise ValueError(f"Reference must identify a file: {name}")
    return path


def file_reference(root: Path, value: object, commit: str | None) -> Path:
    """Compare consumed reference bytes and optional committed Git blob bytes."""
    reference = object_map(value, "FileRef")
    if set(reference) != {"path", "sha256"}:
        raise ValueError("FileRef requires exactly path and sha256")
    path = local_file(root, reference["path"])
    digest = reference["sha256"]
    if (
        not isinstance(digest, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is None
    ):
        raise ValueError(f"Invalid sha256: {path.relative_to(root)}")
    data = path.read_bytes()
    if "sha256:" + hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(
            f"Consumed reference checksum mismatch: {path.relative_to(root)}"
        )
    if commit is not None:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "show",
                f"{commit}:{path.relative_to(root).as_posix()}",
            ],
            capture_output=True,
            check=False,
            timeout=30,
        )
        if result.returncode or result.stdout != data:
            raise ValueError(f"Committed reference mismatch: {path.relative_to(root)}")
    return path


def committed_references(root: Path, provenance: Mapping[str, object]) -> None:
    """Check declared code, configuration, lock and DVC metadata against Git."""
    experiment = object_map(provenance["experiment"], "experiment")
    commit = experiment["commit_sha"]
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError("experiment.commit_sha must be a full 40-hex commit")
    file_reference(root, experiment["entrypoint"], commit)
    code = experiment["code"]
    if not isinstance(code, list) or not code or experiment["entrypoint"] not in code:
        raise ValueError("experiment.code must include entrypoint")
    for value in code:
        file_reference(root, value, commit)
    config = object_map(provenance["configuration"], "configuration")
    files = config["files"]
    if not isinstance(files, list) or not files:
        raise ValueError("configuration.files must be nonempty")
    for value in files:
        file_reference(root, value, commit)
    environment = object_map(provenance["environment"], "environment")
    file_reference(root, environment["lockfile"], commit)
    data = provenance["data"]
    if not isinstance(data, list) or not data:
        raise ValueError("data must contain native DVC references")
    for value in data:
        reference = object_map(value, "DvcRef")
        file_reference(root, reference["metadata"], commit)


def validate_json(value: object, field: str, active: set[int] | None = None) -> None:
    """Require finite plain JSON values and reject cyclic settings with context."""
    import math

    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{field} must contain finite JSON numbers")
        return
    active = set() if active is None else active
    if id(value) in active:
        raise ValueError(f"{field} contains a cycle")
    active.add(id(value))
    try:
        if isinstance(value, dict) and all(isinstance(key, str) for key in value):
            for key, item in value.items():
                validate_json(item, f"{field}.{key}", active)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                validate_json(item, f"{field}[{index}]", active)
        else:
            raise TypeError(f"{field} must contain plain JSON values")
    finally:
        active.remove(id(value))


def exact_record(value: object, field: str, keys: set[str]) -> Mapping[str, object]:
    """Check required versioned keys without ignoring unknown or missing fields."""
    record = object_map(value, field)
    if set(record) != keys:
        raise ValueError(f"{field} requires exactly {', '.join(sorted(keys))}")
    return record


def provenance_schema(provenance: Mapping[str, object]) -> None:
    """Validate the versioned provenance structure independently of publication."""
    exact_record(
        provenance,
        "provenance",
        {
            "schema_version",
            "experiment",
            "configuration",
            "data",
            "split_record",
            "environment",
            "toolkit",
        },
    )
    validate_json(dict(provenance), "provenance")
    if provenance["schema_version"] != "1.0":
        raise ValueError("provenance.schema_version must be 1.0")
    exact_record(
        provenance["experiment"],
        "provenance.experiment",
        {"commit_sha", "entrypoint", "code"},
    )
    configuration = exact_record(
        provenance["configuration"], "provenance.configuration", {"files", "effective"}
    )
    object_map(configuration["effective"], "provenance.configuration.effective")
    exact_record(
        provenance["environment"],
        "provenance.environment",
        {"lockfile", "python_version", "libraries"},
    )
    exact_record(
        provenance["toolkit"],
        "provenance.toolkit",
        {"installation", "repository_url", "commit_sha", "build_identity"},
    )
    file_ref = object_map(provenance["split_record"], "provenance.split_record")
    exact_record(file_ref, "provenance.split_record", {"path", "sha256"})
    data = provenance["data"]
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("provenance.data must include dataset and saved split")
    for reference in data:
        exact_record(
            reference,
            "provenance.data[]",
            {"metadata", "output_path", "hash_name", "hash_value", "member_path"},
        )


def dvc_references(root: Path, provenance: Mapping[str, object]) -> None:
    """Check native pointer identity and current DVC output/member integrity."""
    import json
    import os
    import sys

    import yaml

    split = file_reference(root, provenance["split_record"], None)
    saved = json.loads(split.read_text(encoding="utf-8"))
    if not isinstance(saved, dict) or saved.get("schema_version") != "1.0":
        raise ValueError("split_record must contain an existing partition record 1.0")
    consumed: set[Path] = set()
    checked: set[Path] = set()
    references = provenance["data"]
    if not isinstance(references, list):
        raise TypeError("provenance.data must be a list")
    for item in references:
        reference = object_map(item, "DvcRef")
        metadata = file_reference(root, reference["metadata"], None)
        if metadata.suffix != ".dvc":
            raise ValueError("provenance.data requires native .dvc pointers")
        pointer = object_map(
            yaml.safe_load(metadata.read_text(encoding="utf-8")), "DVC pointer"
        )
        outputs = pointer.get("outs")
        if not isinstance(outputs, list):
            raise ValueError("DVC pointer is missing native outputs")
        matched = []
        for value in outputs:
            output = object_map(value, "DVC output")
            native_path = output.get("path")
            if not isinstance(native_path, str):
                raise ValueError("DVC output.path must be a string")
            path = metadata.parent / native_path
            if (
                path.resolve().is_relative_to(root.resolve())
                and path.relative_to(root).as_posix() == reference["output_path"]
            ):
                matched.append(output)
        if len(matched) != 1:
            raise ValueError(
                "provenance.data.output_path does not select one native output"
            )
        output = matched[0]
        hash_name, hash_value = reference["hash_name"], reference["hash_value"]
        if (
            not isinstance(hash_name, str)
            or not isinstance(hash_value, str)
            or output.get("hash") != hash_name
            or output.get(hash_name) != hash_value
        ):
            raise ValueError("provenance.data hash does not match native DVC metadata")
        name = reference["output_path"]
        if (
            not isinstance(name, str)
            or any(part in ("", ".", "..") for part in name.split("/"))
            or PurePosixPath(name).is_absolute()
        ):
            raise ValueError("provenance.data.output_path must be project-relative")
        member = reference["member_path"]
        if member is not None:
            if not isinstance(member, str) or not hash_value.endswith(".dir"):
                raise ValueError(
                    "provenance.data.member_path requires native directory output"
                )
            path = local_file(root, name + "/" + member)
        else:
            path = local_path(root, name)
            if path.is_dir() != hash_value.endswith(".dir"):
                raise ValueError(
                    "provenance.data output kind differs from native DVC hash"
                )
        consumed.add(path)
        if metadata not in checked:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dvc",
                    "status",
                    "--json",
                    "--no-updates",
                    str(metadata.relative_to(root)),
                ],
                cwd=root,
                env={**os.environ, "DVC_NO_ANALYTICS": "1"},
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            if result.returncode or json.loads(result.stdout):
                raise ValueError(
                    f"provenance.data integrity failed: {metadata.name}; {result.stdout} {result.stderr}"
                )
            checked.add(metadata)
    if split not in consumed or len(consumed) < 2:
        raise ValueError(
            "provenance.data must identify both consumed dataset and saved split"
        )


def environment_identity(root: Path, provenance: Mapping[str, object]) -> None:
    """Check native installed versions and the accepted Git/retained-wheel identity."""
    import platform
    import tomllib
    from importlib.metadata import PackageNotFoundError, distribution, version

    from packaging.utils import canonicalize_name
    from packaging.version import Version

    from agentic_ml.initialization.identity import current_identity
    from agentic_ml.initialization.models import InitializationError

    environment = object_map(provenance["environment"], "provenance.environment")
    lock = object_map(environment["lockfile"], "provenance.environment.lockfile")
    if lock["path"] != "uv.lock":
        raise ValueError("provenance.environment.lockfile must identify uv.lock")
    if environment["python_version"] != platform.python_version():
        raise ValueError(
            "provenance.environment.python_version differs from installed Python"
        )
    libraries = object_map(environment["libraries"], "provenance.environment.libraries")
    locked = tomllib.loads((root / "uv.lock").read_text(encoding="utf-8"))
    packages = locked.get("package", [])
    locked_versions: dict[str, set[Version]] = {}
    for package in packages:
        if (
            isinstance(package, dict)
            and isinstance(package.get("name"), str)
            and isinstance(package.get("version"), str)
        ):
            locked_versions.setdefault(canonicalize_name(package["name"]), set()).add(
                Version(package["version"])
            )
    if not {"agentic-ml", "mlflow", "dvc", "pandas", "pyarrow", "scikit-learn"} <= set(
        libraries
    ):
        raise ValueError(
            "provenance.environment.libraries must include required runtime versions"
        )
    for name, supplied in libraries.items():
        try:
            actual = version(name)
        except PackageNotFoundError as error:
            raise ValueError(
                f"provenance.environment library unavailable: {name}"
            ) from error
        if not isinstance(supplied, str) or supplied != actual:
            raise ValueError(f"provenance.environment library version mismatch: {name}")
        if Version(actual) not in locked_versions.get(canonicalize_name(name), set()):
            raise ValueError(
                f"provenance.environment library is outside committed lock: {name}"
            )
    toolkit = object_map(provenance["toolkit"], "provenance.toolkit")
    try:
        actual_identity = current_identity(root)
    except InitializationError as error:
        raise ValueError(
            "provenance.toolkit installation identity is invalid"
        ) from error
    if toolkit["installation"] != actual_identity:
        raise ValueError(
            "provenance.toolkit installation differs from installed/locked identity"
        )
    installed = distribution("agentic-ml")
    if actual_identity["kind"] == "git":
        if (
            toolkit["repository_url"] != actual_identity["url"]
            or toolkit["commit_sha"] != actual_identity["revision"]
        ):
            raise ValueError("provenance.toolkit Git URL/full SHA mismatch")
    else:
        if toolkit["commit_sha"] is not None and toolkit[
            "commit_sha"
        ] != installed.metadata.get("Source-Commit"):
            raise ValueError(
                "provenance.toolkit source commit is unavailable or mismatched"
            )
        if toolkit["repository_url"] is not None:
            urls = installed.metadata.get_all("Project-URL") or []
            repositories = [
                item.split(",", 1)[1].strip()
                for item in urls
                if item.lower().startswith("repository,")
            ]
            if toolkit["repository_url"] not in repositories:
                raise ValueError(
                    "provenance.toolkit repository URL is unavailable or mismatched"
                )
    if toolkit["build_identity"] is not None and toolkit[
        "build_identity"
    ] != installed.metadata.get("Build-Identity"):
        raise ValueError(
            "provenance.toolkit build identity is unavailable or mismatched"
        )
