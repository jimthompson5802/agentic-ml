"""Persist setup progress without representing experiment authorization."""

import json
import os
from pathlib import Path
from typing import Any


def write_private(path: Path, content: bytes) -> None:
    """Replace a setup-owned file atomically with owner-only permissions."""
    temporary = path.with_suffix(".tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def read_journal(root: Path) -> dict[str, Any] | None:
    """Read a saved setup inventory if present."""
    path = root / ".agentic-ml/init.json"
    if not path.exists():
        return None
    value: dict[str, Any] = json.loads(path.read_text())
    return value
