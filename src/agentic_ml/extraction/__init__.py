"""Record project-owned pandas extraction through installed public interfaces."""

import sys
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Literal

import pandas as pd

from agentic_ml.extraction.provenance import digest, publish, validate_json
from agentic_ml.extraction.sources import (
    fingerprint,
    local_path,
    read_source,
    resolve_local,
    schema,
    stable_bytes,
)

__all__ = ["extract_data"]


def extract_data(
    extract: Callable[[dict[str, pd.DataFrame], dict[str, object]], pd.DataFrame],
    *,
    project_root: Path,
    sources: Mapping[str, Path],
    destination: Path,
    code_paths: Sequence[Path],
    settings: Mapping[str, object] | None = None,
    read_options: Mapping[str, Mapping[str, object]] | None = None,
    output_format: Literal["csv", "parquet"] = "parquet",
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Extract project data and publish its output and provenance together.

    Args:
        extract: Project function accepting named DataFrames and copied settings.
        project_root: Absolute project directory used to resolve relative paths.
        sources: Named local CSV/Parquet paths, including absolute external files.
        destination: Fresh project-local output directory with an existing parent.
        code_paths: Declared project source files to identify in the report.
        settings: JSON-compatible project configuration, deeply copied at entry.
        read_options: JSON-compatible native pandas reader kwargs for each source.
        output_format: CSV or Parquet, without serializing the DataFrame index.

    Returns:
        The native output DataFrame and its JSON-compatible provenance dictionary.

    Raises:
        ValueError: A declaration, settings value, column schema or identity fails.
        TypeError: The extractor/reader does not supply the required native type.
        FileNotFoundError: A declared file or output parent does not exist.
        FileExistsError: The destination already exists or appears during work.
        OSError: Reading, writing or publication fails. Native pandas and project
            exceptions also propagate unchanged with source/stage context notes.
    """
    stage = "configuration"
    started = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    clock = monotonic()
    try:
        if not project_root.is_absolute() or not project_root.is_dir():
            raise ValueError("project_root must be an existing absolute directory")
        if not callable(extract):
            raise TypeError("extract must be callable")
        if not sources or any(
            not isinstance(name, str) or not name for name in sources
        ):
            raise ValueError("At least one named source is required")
        if not code_paths:
            raise ValueError("At least one declared project code path is required")
        if output_format not in {"csv", "parquet"}:
            raise ValueError("output_format must be csv or parquet")
        effective_settings = deepcopy(dict(settings or {}))
        options = deepcopy(
            {name: dict(value) for name, value in (read_options or {}).items()}
        )
        validate_json(effective_settings)
        validate_json(options)
        if set(options) - set(sources):
            raise ValueError("Reader options reference an unknown source")
        target = resolve_local(project_root, destination, inside=True)
        if target.exists():
            raise FileExistsError(target)
        if not target.parent.is_dir():
            raise FileNotFoundError(target.parent)
        snapshots: dict[Path, tuple[int, int, int, int, int]] = {}
        declared_code: list[dict[str, object]] = []
        for code in code_paths:
            path = local_path(project_root, code, inside=True)
            data, snapshot = stable_bytes(path)
            snapshots[path] = snapshot
            declared_code.append({"path": str(path), "sha256": digest(data)})
        frames: dict[str, pd.DataFrame] = {}
        inspected: list[dict[str, object]] = []
        for name, path in sources.items():
            stage = f"source {name}"
            resolved = local_path(project_root, path)
            frame, description, snapshot = read_source(
                resolved, name, options.get(name, {})
            )
            frames[name] = frame
            snapshots[resolved] = snapshot
            description.update(supplied_path=str(path), resolved_path=str(resolved))
            inspected.append(description)
        stage = "callback"
        output = extract(
            {name: frame.copy(deep=True) for name, frame in frames.items()},
            deepcopy(effective_settings),
        )
        if not isinstance(output, pd.DataFrame):
            raise TypeError("Project extraction must return a pandas DataFrame")
        schema(output)
        report: dict[str, object] = {
            "schema_version": "1.0",
            "status": "complete",
            "sources": inspected,
            "project_root": str(project_root),
            "working_directory": str(Path.cwd()),
            "extraction": {
                "settings": effective_settings,
                "module": getattr(extract, "__module__", None),
                "name": getattr(extract, "__qualname__", None),
                "code": declared_code,
            },
            "started_at": started,
        }
        stage = "output"

        def verify_inputs() -> None:
            for path, snapshot in snapshots.items():
                if fingerprint(local_path(project_root, path)) != snapshot:
                    raise ValueError(
                        f"Declared input changed before publication: {path}"
                    )
            resolve_local(project_root, destination, inside=True)

        verify_inputs()
        publish(output, target, output_format, report, clock, verify_inputs)
        return output, report
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(f"extraction {stage}; root={project_root}; cwd={Path.cwd()}")
