"""Atomic, descriptor-based publication of immutable semantic validation evidence."""

import hashlib
import os
import stat
import uuid

from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.paths import ProjectAccess
from agentic_ml.planning.storage import canonical, check_store, write_file
from agentic_ml.validation.checks import digest, reject, schema
from agentic_ml.validation.models import ValidationError

STORE = ".agentic-ml/validations"


def publish(
    access: ProjectAccess,
    config: dict[str, JSONValue],
    registry: dict[str, JSONValue],
    source: bytes | None,
) -> str:
    """Publish a complete immutable bundle under a cooperating-writer lock."""
    check_store(access, access.read("project.yaml"), store=STORE)
    schema(config, "configuration", "invalid_validation")
    schema(registry, "registry", "invalid_validation")
    validation_id = digest(config)
    parent = access.directory(STORE, create=True)
    locked = False
    try:
        try:
            lock = os.open(
                "validate.lock",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
        except FileExistsError as error:
            raise ValidationError(
                "validation_busy",
                "Validation lock exists; operator review is required.",
            ) from error
        locked = True
        lock_info = os.fstat(lock)
        os.close(lock)
        try:
            info = os.stat(validation_id[7:], dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            info = None
        if info is not None:
            if not stat.S_ISDIR(info.st_mode):
                reject(
                    "invalid_validation",
                    "members",
                    "Use a regular validation bundle directory.",
                )
            stored, captured, selected_source = read_bundle(access, validation_id)
            if stored != config or captured != registry or selected_source != source:
                reject(
                    "invalid_validation",
                    "members",
                    "Preserve original evidence; conflicting bundles cannot be overwritten.",
                )
            access.recheck()
            return validation_id
        members = {
            "configuration.json": canonical(config),
            "registry.json": canonical(registry),
        }
        if source is not None:
            members["registry-source.yaml"] = source
        manifest: dict[str, JSONValue] = {
            "schema_version": "1.0",
            "validation_id": validation_id,
            "files": {
                name: hashlib.sha256(data).hexdigest() for name, data in members.items()
            },
        }
        members["manifest.json"] = canonical(manifest)
        stage_name = ".pending-" + uuid.uuid4().hex
        os.mkdir(stage_name, mode=0o700, dir_fd=parent)
        stage = os.open(
            stage_name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent
        )
        try:
            for name, content in members.items():
                write_file(stage, name, content)
            os.fsync(stage)
            access.recheck()
            current_parent = access.directory(STORE)
            try:
                if (
                    os.fstat(current_parent).st_dev,
                    os.fstat(current_parent).st_ino,
                ) != (os.fstat(parent).st_dev, os.fstat(parent).st_ino):
                    reject(
                        "unsafe_path",
                        "store",
                        "Preserve the selected validation store directory.",
                    )
            finally:
                os.close(current_parent)
            os.rename(
                stage_name, validation_id[7:], src_dir_fd=parent, dst_dir_fd=parent
            )
            os.fsync(parent)
        finally:
            os.close(stage)
        read_bundle(access, validation_id)
        return validation_id
    finally:
        if locked:
            current = os.stat("validate.lock", dir_fd=parent, follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (lock_info.st_dev, lock_info.st_ino):
                os.unlink("validate.lock", dir_fd=parent)
                os.fsync(parent)
        os.close(parent)


def read_bundle(
    access: ProjectAccess, validation_id: str
) -> tuple[dict[str, JSONValue], dict[str, JSONValue], bytes | None]:
    """Check exact bundle inventory, schemas and content-derived identities."""
    import re

    from agentic_ml.planning.parsing import mapping
    from agentic_ml.planning.storage import checked_json
    from agentic_ml.validation.checks import reject, schema

    if not isinstance(validation_id, str) or not re.fullmatch(
        r"sha256:[0-9a-f]{64}", validation_id
    ):
        reject(
            "invalid_validation",
            "validation_id",
            "Use an existing SHA-256 validation identity.",
        )
    directory = STORE + "/" + validation_id[7:]
    manifest = mapping(checked_json(access.read(directory + "/manifest.json")))
    schema(manifest, "manifest", "invalid_validation")
    members = mapping(manifest["files"])
    expected = {"configuration.json", "registry.json"}
    if "registry-source.yaml" in members:
        expected.add("registry-source.yaml")
    if set(members) != expected or manifest["validation_id"] != validation_id:
        reject("invalid_validation", "members", "Use an intact validation bundle.")
    fd = access.directory(directory)
    try:
        if set(os.listdir(fd)) != expected | {"manifest.json"}:
            reject(
                "invalid_validation",
                "members",
                "Use the exact preserved member inventory.",
            )
    finally:
        os.close(fd)
    captured: dict[str, bytes] = {}
    for name, checksum in sorted(members.items()):
        content = access.read(directory + "/" + name)
        if hashlib.sha256(content).hexdigest() != checksum:
            reject(
                "invalid_validation",
                name,
                "Restore evidence with matching content checksums.",
            )
        captured[name] = content
    config = mapping(checked_json(captured["configuration.json"]))
    registry = mapping(checked_json(captured["registry.json"]))
    schema(config, "configuration", "invalid_validation")
    schema(registry, "registry", "invalid_validation")
    if (
        digest(config) != validation_id
        or digest(registry) != config["registry_id"]
        or config["project_root"] != str(access.root)
    ):
        reject(
            "invalid_validation",
            "validation_id",
            "Use evidence bound to this project and registry.",
        )
    return config, registry, captured.get("registry-source.yaml")
