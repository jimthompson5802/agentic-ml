"""Immutable, atomic local plan publication and evidence integrity checks."""

import hashlib
import json
import os
import re
import stat
import uuid
from pathlib import Path
from typing import cast

from agentic_ml.planning.models import JSONValue, PlanningError
from agentic_ml.planning.parsing import fail, mapping, sequence, strict_yaml
from agentic_ml.planning.paths import ProjectAccess

STORE = ".agentic-ml/plans"
SOURCE_NAMES = {
    "experiment.md",
    "search-space.yaml",
    "experiment.yaml",
    "project.yaml",
    "pyproject.toml",
    "uv.lock",
    "harness-origin.json",
}


def canonical(value: JSONValue) -> bytes:
    """Serialize finite JSON deterministically with one terminal newline."""
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def identifier(plan_id: str) -> str:
    """Validate a public immutable plan identifier."""
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", plan_id):
        fail("invalid_plan_id", "plan_id", "")
    return plan_id[7:]


def checked_json(content: bytes) -> JSONValue:
    """Parse finite JSON, rejecting duplicates and noncanonical encodings."""

    def pairs(items: list[tuple[str, JSONValue]]) -> dict[str, JSONValue]:
        result: dict[str, JSONValue] = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result

    value = cast(JSONValue, json.loads(content, object_pairs_hook=pairs))
    if canonical(value) != content:
        raise ValueError("Noncanonical JSON")
    return value


def check_store(access: ProjectAccess, project_bytes: bytes) -> None:
    """Reject planning storage overlapping configured stores or selected sources."""
    raw, _ = strict_yaml(project_bytes, "project.yaml")
    storage = mapping(mapping(raw)["storage"])
    destination = access.root / STORE
    protected = [
        Path(os.path.abspath(access.root / str(value))) for value in storage.values()
    ]
    if any(
        destination == path
        or destination.is_relative_to(path)
        or path.is_relative_to(destination)
        for path in protected
    ):
        raise PlanningError(
            "storage_conflict", "Planning store overlaps a configured project store."
        )
    if any(path == STORE or path.startswith(STORE + "/") for path in access.snapshots):
        raise PlanningError(
            "storage_conflict", "Planning store overlaps selected inputs."
        )


def read_bundle(
    access: ProjectAccess, plan_id: str, *, staging: str | None = None
) -> tuple[dict[str, JSONValue], dict[str, bytes]]:
    """Independently check exact member inventory, lengths, hashes and plan id."""
    directory = STORE + "/" + (identifier(plan_id) if staging is None else staging)
    bundle_fd = access.directory(directory)
    try:
        source_fd = os.open(
            "sources", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=bundle_fd
        )
        try:
            if (
                set(os.listdir(bundle_fd)) != {"plan.json", "manifest.json", "sources"}
                or set(os.listdir(source_fd)) != SOURCE_NAMES
            ):
                fail("corrupt_plan", "members", directory)
        finally:
            os.close(source_fd)
    finally:
        os.close(bundle_fd)
    try:
        manifest = mapping(checked_json(access.read(directory + "/manifest.json")))
        if (
            set(manifest) != {"schema_version", "files"}
            or manifest["schema_version"] != "1.0"
        ):
            raise ValueError("Unsupported manifest")
        expected = {"plan.json"} | {"sources/" + name for name in SOURCE_NAMES}
        captured: dict[str, bytes] = {}
        for item in sequence(manifest["files"]):
            entry = mapping(item)
            if set(entry) != {"path", "length", "sha256"}:
                raise ValueError("Invalid manifest entry")
            name = str(entry["path"])
            if name not in expected:
                raise ValueError("Unexpected or duplicate member")
            expected.remove(name)
            content = access.read(
                directory + "/" + name,
                max_bytes=33554432 if name == "plan.json" else 1048576,
            )
            if (
                type(entry["length"]) is not int
                or len(content) != entry["length"]
                or hashlib.sha256(content).hexdigest() != entry["sha256"]
            ):
                raise ValueError("Checksum mismatch")
            captured[name] = content
        if expected or hashlib.sha256(captured["plan.json"]).hexdigest() != identifier(
            plan_id
        ):
            raise ValueError("Invalid plan identity")
        plan = mapping(checked_json(captured.pop("plan.json")))
        return plan, {
            name.removeprefix("sources/"): content for name, content in captured.items()
        }
    except (ValueError, KeyError, UnicodeError, TypeError) as error:
        fail("corrupt_plan", "manifest", directory)
        raise AssertionError("unreachable") from error


def write_file(directory: int, name: str, content: bytes) -> None:
    """Exclusively create and synchronize a regular file at a held descriptor."""
    fd = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
        dir_fd=directory,
    )
    try:
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(content)
            stream.flush()
            os.fsync(fd)
    finally:
        os.close(fd)


def publish(
    access: ProjectAccess, plan: dict[str, JSONValue], sources: dict[str, bytes]
) -> str:
    """Publish one complete bundle under an exclusive cooperating-writer lock."""
    check_store(access, sources["project.yaml"])
    content = canonical(plan)
    plan_id = "sha256:" + hashlib.sha256(content).hexdigest()
    parent = access.directory(STORE, create=True)
    locked = False
    try:
        try:
            lock = os.open(
                "resolve.lock",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
        except FileExistsError as error:
            raise PlanningError(
                "plan_busy", "Planning lock exists; operator review is required."
            ) from error
        locked = True
        lock_identity = os.fstat(lock)
        os.close(lock)
        name = identifier(plan_id)
        try:
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            info = None
        if info is not None:
            if not stat.S_ISDIR(info.st_mode):
                fail("corrupt_plan", "members", STORE + "/" + name)
            existing, captured = read_bundle(access, plan_id)
            if canonical(existing) != content or captured != sources:
                fail("corrupt_plan", "members", STORE + "/" + name)
            access.recheck()
            return plan_id
        staging = ".pending-" + str(uuid.uuid4())
        os.mkdir(staging, mode=0o700, dir_fd=parent)
        stage = os.open(
            staging, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent
        )
        try:
            os.mkdir("sources", mode=0o700, dir_fd=stage)
            source_fd = os.open(
                "sources", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=stage
            )
            entries: list[JSONValue] = []
            try:
                for source_name in sorted(sources):
                    source = sources[source_name]
                    write_file(source_fd, source_name, source)
                    entries.append(
                        {
                            "path": "sources/" + source_name,
                            "length": len(source),
                            "sha256": hashlib.sha256(source).hexdigest(),
                        }
                    )
                os.fsync(source_fd)
            finally:
                os.close(source_fd)
            write_file(stage, "plan.json", content)
            entries.append(
                {
                    "path": "plan.json",
                    "length": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
            write_file(
                stage,
                "manifest.json",
                canonical({"schema_version": "1.0", "files": entries}),
            )
            os.fsync(stage)
            read_bundle(access, plan_id, staging=staging)
            access.recheck()
            # Staging snapshots describe evidence before its atomic rename.
            for path in tuple(access.snapshots):
                if path.startswith(STORE + "/" + staging + "/"):
                    del access.snapshots[path]
            current_parent = access.directory(STORE)
            try:
                if (
                    os.fstat(current_parent).st_dev,
                    os.fstat(current_parent).st_ino,
                ) != (os.fstat(parent).st_dev, os.fstat(parent).st_ino):
                    fail("changed_store", "", STORE)
            finally:
                os.close(current_parent)
            os.rename(staging, name, src_dir_fd=parent, dst_dir_fd=parent)
            os.fsync(parent)
        finally:
            os.close(stage)
        read_bundle(access, plan_id)
        return plan_id
    finally:
        if locked:
            current_lock = os.stat("resolve.lock", dir_fd=parent, follow_symlinks=False)
            if (current_lock.st_dev, current_lock.st_ino) == (
                lock_identity.st_dev,
                lock_identity.st_ino,
            ):
                os.unlink("resolve.lock", dir_fd=parent)
                os.fsync(parent)
        os.close(parent)
