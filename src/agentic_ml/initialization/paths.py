"""Check filesystem paths shared by setup and toolkit identity validation."""

from pathlib import Path

from .models import InitializationError


def check_path(path: Path) -> None:
    """Reject symlink components and non-directory parents without following them."""
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise InitializationError("Symlink destination conflict")
        if parent != path and parent.exists() and not parent.is_dir():
            raise InitializationError("Destination parent is not a directory")
