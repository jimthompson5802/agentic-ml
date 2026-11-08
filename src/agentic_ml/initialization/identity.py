"""Check toolkit source, lock and installed distribution identities."""

import hashlib
import json
import re
import stat
import sys
import tomllib
import zipfile
from email.parser import BytesParser
from importlib.metadata import Distribution, distribution, distributions
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qs, urlsplit

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version

from .journal import read_journal
from .models import InitializationError
from .paths import check_path


def toolkit_identity(
    root: Path, metadata: dict[str, Any], lock: dict[str, Any]
) -> dict[str, str]:
    """Validate the selected toolkit before initialization writes."""
    try:
        sources = metadata["tool"]["uv"]["sources"]
        dependencies = metadata["project"]["dependencies"]
    except (KeyError, TypeError) as error:
        raise _wheel_error(
            "Missing or malformed toolkit declaration metadata"
        ) from error
    if not isinstance(sources, dict):
        raise _wheel_error("Malformed toolkit source metadata")
    selected = [
        value
        for name, value in sources.items()
        if canonicalize_name(name) == "agentic-ml"
    ]
    if len(selected) != 1 or not isinstance(selected[0], dict):
        raise _wheel_error("Toolkit declaration must select exactly one source")
    source = selected[0]
    if isinstance(source, dict) and "path" in source:
        try:
            return _wheel_identity(root, source, dependencies, lock)
        except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
            raise _wheel_error(
                "Invalid wheel declaration, lock, archive or installed metadata"
            ) from error
    if "git" not in source:
        raise _wheel_error("Unsupported toolkit declaration; select a local wheel path")
    revision = source["rev"]
    url = source["git"]
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
    return {
        "kind": "git",
        "name": "agentic-ml",
        "version": str(Version(installed.version)),
        "url": url,
        "revision": revision,
    }


def _wheel_identity(
    root: Path, source: dict[str, Any], dependencies: list[str], lock: dict[str, Any]
) -> dict[str, str]:
    if set(source) != {"path"} or not isinstance(source["path"], str):
        raise _wheel_error("Unsupported wheel declaration")
    if not isinstance(dependencies, list) or any(
        not isinstance(d, str) for d in dependencies
    ):
        raise _wheel_error("Malformed wheel dependency declaration")
    requirements = [Requirement(d) for d in dependencies]
    declared = [r for r in requirements if canonicalize_name(r.name) == "agentic-ml"]
    if (
        len(declared) != 1
        or declared[0].extras
        or declared[0].marker
        or declared[0].url
    ):
        raise _wheel_error(
            "Wheel declaration requires one unconditional dependency without extras"
        )
    if Path(source["path"]).suffix != ".whl":
        raise _wheel_error(
            "Unsupported wheel declaration; directories and source archives are excluded"
        )
    try:
        check_path(root / source["path"])
    except InitializationError as error:
        raise _wheel_error("Wheel locator symlink or path conflict") from error
    path = (root / source["path"]).resolve()
    if not path.is_file() or path.suffix != ".whl":
        raise _wheel_error("Retained wheel is missing; restore the locked wheel")
    entries = lock.get("package", [])
    if not isinstance(entries, list) or any(not isinstance(p, dict) for p in entries):
        raise _wheel_error("Malformed wheel lock package metadata")
    packages = [
        p
        for p in entries
        if isinstance(p.get("name"), str)
        and canonicalize_name(p["name"]) == "agentic-ml"
    ]
    if len(packages) != 1:
        raise _wheel_error("Wheel lock must contain exactly one toolkit package")
    package = packages[0]
    if Version(package["version"]) not in declared[0].specifier:
        raise _wheel_error("Wheel declaration version differs from lock")
    try:
        check_path(root / package["source"]["path"])
    except InitializationError as error:
        raise _wheel_error("Locked wheel locator symlink or path conflict") from error
    if (
        set(package["source"]) != {"path"}
        or (root / package["source"]["path"]).resolve() != path
    ):
        raise _wheel_error("Locked wheel source differs from declaration")
    (wheel,) = package["wheels"]
    filename_name, filename_version, _, _ = parse_wheel_filename(path.name)
    if filename_name != "agentic-ml" or filename_version != Version(package["version"]):
        raise _wheel_error("Wheel filename identity differs from lock")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if wheel["filename"] != path.name or wheel["hash"] != "sha256:" + digest:
        raise _wheel_error("Retained wheel differs from locked SHA-256")
    installed, direct = _installed_wheel(root)
    if direct.get("url") != path.as_uri() or Version(installed.version) != Version(
        package["version"]
    ):
        raise _wheel_error("Installed wheel identity differs from selected project")
    if not isinstance(direct.get("archive_info"), dict):
        raise _wheel_error("Installed wheel archive metadata is missing or malformed")
    archive_info = direct["archive_info"]
    if "hashes" in archive_info:
        hashes = archive_info["hashes"]
        if not isinstance(hashes, dict) or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in hashes.items()
        ):
            raise _wheel_error("Installed wheel archive hashes are malformed")
        if "sha256" in hashes and hashes["sha256"] != digest:
            raise _wheel_error("Installed wheel archive SHA-256 differs from lock")
    if "hash" in archive_info and archive_info["hash"] != "sha256=" + digest:
        raise _wheel_error(
            "Installed wheel archive hash is malformed or differs from lock"
        )
    _verify_payload(path, installed, package["version"])
    return {
        "kind": "wheel",
        "name": "agentic-ml",
        "version": str(Version(installed.version)),
        "locator": path.as_uri(),
        "sha256": digest,
        "verification": "locked-archive-and-installed-payload",
    }


def current_identity(root: Path) -> dict[str, str]:
    """Recheck identity after native environment synchronization."""
    return toolkit_identity(
        root,
        tomllib.loads((root / "pyproject.toml").read_text()),
        tomllib.loads((root / "uv.lock").read_text()),
    )


def _wheel_error(message: str) -> InitializationError:
    return InitializationError(
        message,
        recovery="Restore the reviewed locked wheel and project metadata, then run uv sync --locked; deliberately select a new wheel only for an explicit upgrade.",
    )


def _verify_payload(path: Path, installed: Distribution, version: str) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise _wheel_error("Unsupported wheel layout: duplicate members")
        for member in archive.infolist():
            name = member.filename
            parts = PurePosixPath(name).parts
            if (
                not parts
                or name.startswith("/")
                or "\\" in name
                or ".." in parts
                or any(part.endswith(".data") for part in parts)
                or stat.S_ISLNK(member.external_attr >> 16)
                or str(PurePosixPath(name)) != name.rstrip("/")
            ):
                raise _wheel_error(
                    "Unsupported wheel layout: unsafe or relocated members"
                )
        (metadata_name,) = [
            name for name in names if name.endswith(".dist-info/METADATA")
        ]
        metadata = BytesParser().parsebytes(archive.read(metadata_name))
        if (
            len(metadata.get_all("Name", [])) != 1
            or len(metadata.get_all("Version", [])) != 1
        ):
            raise _wheel_error("Wheel metadata requires one Name and Version")
        if canonicalize_name(metadata["Name"]) != "agentic-ml" or Version(
            metadata["Version"]
        ) != Version(version):
            raise _wheel_error("Wheel metadata identity differs from lock")
        wheel_name = metadata_name.removesuffix("METADATA") + "WHEEL"
        if (
            wheel_name not in names
            or BytesParser().parsebytes(archive.read(wheel_name))["Root-Is-Purelib"]
            != "true"
        ):
            raise _wheel_error("Unsupported wheel layout: purelib wheel required")
        record = metadata_name.removesuffix("METADATA") + "RECORD"
        for member in archive.infolist():
            if member.is_dir() or member.filename == record:
                continue
            destination = Path(str(installed.locate_file(member.filename)))
            if not destination.is_file() or destination.read_bytes() != archive.read(
                member
            ):
                raise _wheel_error("Installed wheel payload differs from locked wheel")


def _installed_wheel(root: Path) -> tuple[Distribution, dict[str, Any]]:
    candidates = [
        d
        for d in distributions()
        if canonicalize_name(d.metadata.get("Name", "")) == "agentic-ml"
    ]
    if len(candidates) != 1:
        raise _wheel_error("Installed toolkit metadata is missing or ambiguous")
    installed = candidates[0]
    if Path(sys.prefix).resolve() != (root / ".venv").resolve() or not Path(
        str(installed.locate_file(""))
    ).resolve().is_relative_to((root / ".venv").resolve()):
        raise _wheel_error("Use the selected project's installed wheel environment")
    try:
        direct = json.loads(installed.read_text("direct_url.json") or "{}")
    except (ValueError, OSError) as error:
        raise _wheel_error("Installed wheel origin metadata is malformed") from error
    if (
        not isinstance(direct, dict)
        or "url" not in direct
        or "vcs_info" in direct
        or "dir_info" in direct
    ):
        raise _wheel_error("Installed wheel origin metadata is missing or unsupported")
    return installed, direct


def validate_saved_identity(root: Path, identity: dict[str, str]) -> None:
    """Reject conflicting saved toolkit identity before any rerun writes."""
    saved = read_journal(root)
    if saved is None:
        return
    environment = saved.get("environment", {})
    if not isinstance(environment, dict):
        raise _wheel_error("Malformed setup journal environment identity")
    previous = environment.get("toolkit_identity")
    if previous is None and identity["kind"] == "git":
        return
    if not isinstance(previous, dict) or previous.get("kind") not in ("git", "wheel"):
        raise _wheel_error("Missing or malformed setup journal toolkit identity")
    if previous != identity:
        raise _wheel_error(
            "Setup journal toolkit identity changed; review before retry"
        )
