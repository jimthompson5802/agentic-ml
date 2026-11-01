"""Descriptor-based append-only publication of experiment approval records."""

import os
import stat
import uuid
from collections.abc import Iterator
from contextlib import contextmanager

from agentic_ml.approvals.models import ApprovalError
from agentic_ml.planning.models import JSONValue, PlanningError
from agentic_ml.planning.paths import ProjectAccess, identity
from agentic_ml.planning.storage import (
    canonical,
    check_store,
    identifier,
    read_bundle,
    write_file,
)

STORE = ".agentic-ml/plan-approvals"


@contextmanager
def locked(access: ProjectAccess, plan_id: str) -> Iterator[tuple[str, int]]:
    """Hold the same exclusive lock for cooperating readers and writers."""
    path = STORE + "/" + identifier(plan_id)
    _, sources = read_bundle(access, plan_id)
    try:
        check_store(access, sources["project.yaml"], store=STORE)
    except PlanningError as error:
        raise ApprovalError(error.code, str(error)) from error
    parent = access.directory(path, create=True)
    lock = None
    try:
        try:
            lock = os.open(
                "approval.lock",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent,
            )
        except FileExistsError as error:
            raise ApprovalError(
                "approval_busy",
                "Approval lock exists; operator review is required.",
                operational=True,
            ) from error
        yield path, parent
    finally:
        if lock is not None:
            original = os.fstat(lock)
            current = os.stat("approval.lock", dir_fd=parent, follow_symlinks=False)
            os.close(lock)
            if (original.st_dev, original.st_ino) == (current.st_dev, current.st_ino):
                os.unlink("approval.lock", dir_fd=parent)
                os.fsync(parent)
        os.close(parent)


def read_records(
    access: ProjectAccess, path: str, kind: str
) -> list[tuple[str, bytes]]:
    """Read regular final records; ignore private incomplete staging files."""
    directory = path + "/" + kind
    try:
        fd = access.directory(directory)
    except FileNotFoundError:
        return []
    try:
        before = identity(os.fstat(fd))
        contents = []
        for name in sorted(os.listdir(fd)):
            if name.startswith(".pending-"):
                continue
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            try:
                valid = str(uuid.UUID(name.removesuffix(".json"))) + ".json" == name
            except ValueError:
                valid = False
            if not valid or not stat.S_ISREG(info.st_mode):
                raise ApprovalError(
                    "invalid_approval", "Invalid approval record member."
                )
            contents.append((name, access.read(directory + "/" + name)))
        if before != identity(os.fstat(fd)):
            raise ApprovalError(
                "changed_approval", "Approval directory changed during verification."
            )
        access.snapshots[directory] = before
        access.recheck()
        return contents
    finally:
        os.close(fd)


def append_record(
    access: ProjectAccess,
    path: str,
    kind: str,
    record_id: str,
    value: dict[str, JSONValue],
) -> None:
    """Publish a synchronized record atomically without replacing another file."""
    fd = access.directory(path + "/" + kind, create=True)
    staging = ".pending-" + str(uuid.uuid4())
    try:
        write_file(fd, staging, canonical(value))
        access.recheck()
        os.link(
            staging,
            record_id + ".json",
            src_dir_fd=fd,
            dst_dir_fd=fd,
            follow_symlinks=False,
        )
        os.unlink(staging, dir_fd=fd)
        os.fsync(fd)
    finally:
        os.close(fd)
