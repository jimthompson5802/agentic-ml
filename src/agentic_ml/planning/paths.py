"""Descriptor-based bounded project access without following symbolic links."""

import os
import stat
from pathlib import Path

from agentic_ml.planning.parsing import fail


def relative_path(value: str) -> str:
    """Validate and normalize a selected project-relative path."""
    path = Path(value)
    if (
        not value
        or "\x00" in value
        or ":" in value
        or path.is_absolute()
        or ".." in path.parts
    ):
        fail("unsafe_path", "path", value)
    return path.as_posix()


def data_reference(root: Path, value: str) -> dict[str, str | bool]:
    """Normalize a data location lexically without accessing the target."""
    if not value or "\x00" in value or ":" in value:
        fail("unsafe_data_reference", "data", "experiment.yaml")
    path = Path(os.path.abspath(root / value))
    return {
        "original": value,
        "absolute": str(path),
        "external": not path.is_relative_to(root),
    }


def identity(info: os.stat_result) -> tuple[int, int, int, int, int]:
    """Describe a captured filesystem object for replacement detection."""
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


class ProjectAccess:
    """Hold a canonical root descriptor and verify all captured path identities."""

    def __init__(self, root: Path) -> None:
        """Open an explicit absolute root with no-follow directory traversal."""
        if not root.is_absolute() or ".." in root.parts:
            fail("unsafe_root", "project_root", str(root))
        self.root = root
        self.snapshots: dict[str, tuple[int, int, int, int, int]] = {}
        self.fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in root.parts[1:]:
                next_fd = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.fd
                )
                os.close(self.fd)
                self.fd = next_fd
            self.root_identity = identity(os.fstat(self.fd))[:2]
        except OSError:
            os.close(self.fd)
            fail("unsafe_root", "project_root", str(root))

    def close(self) -> None:
        """Release the project root descriptor."""
        os.close(self.fd)

    def directory(self, path: str, *, create: bool = False) -> int:
        """Open a directory below root, optionally creating missing components."""
        value = relative_path(path)
        fd = os.dup(self.fd)
        try:
            for part in Path(value).parts:
                if create:
                    try:
                        os.mkdir(part, mode=0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                next_fd = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
                )
                os.close(fd)
                fd = next_fd
            return fd
        except OSError:
            os.close(fd)
            raise

    def info(self, path: str) -> os.stat_result:
        """Stat a selected object through no-follow ancestor descriptors."""
        value = relative_path(path)
        if value == ".":
            return os.fstat(self.fd)
        parent = self.directory(str(Path(value).parent))
        try:
            info = os.stat(Path(value).name, dir_fd=parent, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                fail("unsafe_path", "path", value)
            return info
        finally:
            os.close(parent)

    def read(self, path: str, *, max_bytes: int = 1048576) -> bytes:
        """Read at most one MiB from a stable regular selected input."""
        value = relative_path(path)
        if stat.S_ISLNK(self.info(value).st_mode):
            fail("unsafe_path", "path", value)
        parent = self.directory(str(Path(value).parent))
        try:
            fd = os.open(
                Path(value).name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=parent,
            )
            try:
                before = os.fstat(fd)
                if not stat.S_ISREG(before.st_mode) or before.st_size > max_bytes:
                    fail("invalid_input_file", "", value)
                chunks = bytearray()
                while chunk := os.read(fd, min(65536, max_bytes + 1 - len(chunks))):
                    chunks.extend(chunk)
                    if len(chunks) > max_bytes:
                        fail("input_limit", "", value)
                if identity(before) != identity(os.fstat(fd)):
                    fail("changed_source", "", value)
                self.snapshots[value] = identity(before)
                return bytes(chunks)
            finally:
                os.close(fd)
        finally:
            os.close(parent)

    def remember(self, path: str, *, directory: bool = False) -> None:
        """Validate a notebook or working directory without opening contents."""
        info = self.info(path)
        if not (
            stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
        ):
            fail("unsafe_path", "path", path)
        # Directory contents may change when planning creates its own store.
        if not directory:
            self.snapshots[path] = identity(info)

    def recheck(self) -> None:
        """Fail if any selected input or canonical root was replaced."""
        current = ProjectAccess(self.root)
        try:
            if current.root_identity != self.root_identity:
                fail("changed_source", "project_root", str(self.root))
            for path, expected in self.snapshots.items():
                if identity(current.info(path)) != expected:
                    fail("changed_source", "", path)
        finally:
            current.close()
