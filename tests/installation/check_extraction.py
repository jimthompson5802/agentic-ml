"""Verify US-11 through installed APIs and actual independent project code."""

import argparse
import hashlib
import importlib
import importlib.util
import json
import shutil
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from typing import cast

import pandas as pd

import agentic_ml
from agentic_ml.extraction import extract_data


def checksum(path: Path) -> str:
    """Independently hash the actual bytes that the project can inspect."""
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Exercise installed extraction without contributor tools or checkout imports."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--project-code", type=Path, required=True)
    args = parser.parse_args()
    workspace = args.workspace
    root = workspace / "experiment with spaces"
    root.mkdir(parents=True)
    code = root / "project_extraction.py"
    shutil.copy(args.project_code, code)
    spec = importlib.util.spec_from_file_location("project_extraction", code)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert Path(module.__file__ or "").resolve() == code.resolve()
    package = Path(agentic_ml.__file__ or "").resolve()
    assert package.is_relative_to(Path(sys.prefix).resolve())
    assert "site-packages" in package.parts
    assert not package.is_relative_to(workspace)
    assert sys.prefix != sys.base_prefix
    assert importlib.util.find_spec("pytest") is None
    assert importlib.util.find_spec("mypy") is None
    cwd = Path.cwd()
    assert cwd != root
    (root / "people.csv").write_text(
        "id;age;group\n1;20;A\n2;35;B\n3;40;A\n", encoding="utf-8"
    )
    pd.DataFrame({"group": ["A", "B"], "label": ["alpha", "beta"]}).to_parquet(
        root / "groups.parquet", index=False
    )
    settings: dict[str, object] = {
        "minimum_age": 30,
        "columns": ["id", "label"],
        "join_key": "group",
        "join_how": "left",
        "join_validate": "many_to_one",
    }
    callable_type = Callable[[dict[str, pd.DataFrame], dict[str, object]], pd.DataFrame]
    extract = cast(callable_type, module.extract_people)
    start = datetime.now(UTC)
    frame, report = extract_data(
        extract,
        project_root=root,
        sources={"people": Path("people.csv"), "groups": Path("groups.parquet")},
        destination=Path("result"),
        code_paths=[Path("project_extraction.py")],
        settings=settings,
        read_options={"people": {"sep": ";"}},
    )
    end = datetime.now(UTC)
    assert list(frame.itertuples(index=False, name=None)) == [(2, "beta"), (3, "alpha")]
    assert frame.columns.tolist() == ["id", "label"]
    assert settings["columns"] == ["id", "label"]
    assert report["project_root"] == str(root)
    assert report["working_directory"] == str(cwd) and Path.cwd() == cwd
    assert report["status"] == "complete" and report["schema_version"] == "1.0"
    assert start <= datetime.fromisoformat(str(report["started_at"])) <= end
    assert start <= datetime.fromisoformat(str(report["completed_at"])) <= end
    assert cast(float, report["elapsed_seconds"]) >= 0
    extraction = cast(dict[str, object], report["extraction"])
    assert extraction["settings"] == settings
    assert extraction["module"] == "project_extraction"
    assert extraction["name"] == "extract_people"
    assert extraction["code"] == [{"path": str(code), "sha256": checksum(code)}]
    sources = cast(list[dict[str, object]], report["sources"])
    for description, name, rows in zip(
        sources, ("people.csv", "groups.parquet"), (3, 2), strict=True
    ):
        source = root / name
        assert description["resolved_path"] == str(source)
        assert description["supplied_path"] == name
        assert description["sha256"] == checksum(source)
        assert description["byte_count"] == source.stat().st_size
        assert description["row_count"] == rows
    assert sources[0]["schema"] == [
        {"name": "id", "dtype": "Int64"},
        {"name": "age", "dtype": "Int64"},
        {"name": "group", "dtype": "string"},
    ]
    assert sources[1]["schema"] == [
        {"name": "group", "dtype": "string"},
        {"name": "label", "dtype": "string"},
    ]
    assert cast(dict[str, object], sources[0]["reader_options"])["sep"] == ";"
    output = cast(dict[str, object], report["output"])
    dataset = root / "result/dataset.parquet"
    assert output["sha256"] == checksum(dataset)
    assert output["byte_count"] == dataset.stat().st_size
    assert output["row_count"] == 2
    assert output["schema"] == [
        {"name": "id", "dtype": "Int64"},
        {"name": "label", "dtype": "string"},
    ]
    assert list(pd.read_parquet(dataset).itertuples(index=False, name=None)) == [
        (2, "beta"),
        (3, "alpha"),
    ]
    assert json.loads((root / "result/extraction.json").read_text()) == report
    assert report["versions"] == {
        name: version(name) for name in ("agentic-ml", "pandas", "pyarrow")
    }
    # Pyarrow has no typing metadata; inspect its native exception dynamically.
    arrow_invalid = cast(
        type[Exception], importlib.import_module("pyarrow").ArrowInvalid
    )
    cases: list[tuple[str, Callable[..., pd.DataFrame], type[Exception], str]] = [
        ("invalid", module.invalid_return, TypeError, "callback"),
        ("project", module.project_failure, RuntimeError, "callback"),
        ("native", module.native_failure, KeyError, "callback"),
        ("missing", extract, FileNotFoundError, "source people"),
        ("corrupt", extract, arrow_invalid, "source people"),
    ]
    for name, callback, expected, stage in cases:
        source_path = Path("people.csv")
        if name == "missing":
            source_path = Path("missing.csv")
        elif name == "corrupt":
            source_path = Path("corrupt.parquet")
            (root / source_path).write_bytes(b"not a parquet file")
        try:
            extract_data(
                callback,
                project_root=root,
                sources={"people": source_path},
                destination=Path(name),
                code_paths=[Path("project_extraction.py")],
            )
        except expected as error:
            assert any(stage in note and str(root) in note for note in error.__notes__)
            if name == "project":
                assert error is module.PROJECT_ERROR
        else:
            raise AssertionError(f"{name} did not report its required failure")
        assert not (root / name).exists()
        assert not list(root.glob(".extraction-*"))
    identity = {
        "package": str(package),
        "project_code": str(code),
        "python": sys.version,
        "prefix": sys.prefix,
        "working_directory": str(cwd),
        "versions": report["versions"],
        "verified_failures": [case[0] for case in cases],
        "report": report,
    }
    (workspace / "identity.json").write_text(json.dumps(identity, indent=2))


if __name__ == "__main__":
    main()
