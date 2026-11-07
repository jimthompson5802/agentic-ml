"""Verify US-11 pandas extraction through its confirmed public function."""

import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, cast

import pandas as pd
import pytest

from agentic_ml.extraction import extract_data

pytestmark = pytest.mark.milestone_1


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Create explicit local input and project code in a separate project."""
    (tmp_path / "people.csv").write_text(
        "id,age,group\n1,20,A\n2,35,B\n3,40,A\n4,,C\n", encoding="utf-8"
    )
    (tmp_path / "extract.py").write_text("# Project extraction fixture.\n")
    return tmp_path


def identity(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Return the native frame without a toolkit-specific wrapper."""
    return frames["people"]


def test_pandas_source_schema_and_identity(project: Path) -> None:
    """AC-01/02/04: report the actual bytes and parsed source schema."""
    frame, report = extract_data(
        identity,
        project_root=project,
        sources={"people": Path("people.csv")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
    )
    assert isinstance(frame, pd.DataFrame)
    assert frame["id"].tolist() == [1, 2, 3, 4]
    source = cast(list[dict[str, object]], report["sources"])[0]
    assert source["row_count"] == 4
    assert source["schema"] == [
        {"name": "id", "dtype": "Int64"},
        {"name": "age", "dtype": "Int64"},
        {"name": "group", "dtype": "string"},
    ]
    data = (project / "people.csv").read_bytes()
    assert source["byte_count"] == len(data)
    assert source["sha256"] == "sha256:" + hashlib.sha256(data).hexdigest()


def test_parquet_native_reader_options(project: Path) -> None:
    """AC-01/02/03: native Parquet projection and options are recorded."""
    pd.DataFrame({"id": [5, 6], "text": ["a", "b"]}).to_parquet(
        project / "people.parquet", index=False
    )
    frame, report = extract_data(
        identity,
        project_root=project,
        sources={"people": Path("people.parquet")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        read_options={"people": {"columns": ["id"]}},
    )
    assert frame.to_dict("list") == {"id": [5, 6]}
    source = cast(list[dict[str, object]], report["sources"])[0]
    assert source["format"] == "parquet"
    assert source["reader_options"] == {
        "engine": "pyarrow",
        "dtype_backend": "numpy_nullable",
        "columns": ["id"],
    }


def test_native_reader_options_and_paths(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-02/03/05: root-based paths and native options retain provenance."""
    source_path = project / "people.csv"
    source_path.write_bytes("id;city\n01;Montréal\n".encode("latin1"))
    elsewhere = project / "other"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    frame, report = extract_data(
        identity,
        project_root=project,
        sources={"people": Path("people.csv")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        read_options={
            "people": {
                "delimiter": ";",
                "encoding": "latin1",
                "dtype": {"id": "string"},
            }
        },
    )
    assert frame.to_dict("list") == {"id": ["01"], "city": ["Montréal"]}
    assert report["project_root"] == str(project)
    assert report["working_directory"] == str(elsewhere)
    source = cast(list[dict[str, object]], report["sources"])[0]
    assert source["resolved_path"] == str(source_path)
    assert source["supplied_path"] == "people.csv"


@pytest.mark.parametrize(
    "failure",
    [
        "missing",
        "corrupt",
        "symlink",
        "traversal",
        "relative_root",
        "directory",
        "format",
        "missing_code",
    ],
)
def test_missing_and_invalid_paths(project: Path, failure: str) -> None:
    """AC-05: invalid sources/root/code fail with source context and no output."""
    path = Path("people.csv")
    root = project
    code = Path("extract.py")
    if failure == "missing":
        path = Path("missing.csv")
    elif failure == "corrupt":
        path = Path("bad.parquet")
        (project / path).write_bytes(b"not parquet")
    elif failure == "symlink":
        path = Path("link.csv")
        (project / path).symlink_to(project / "people.csv")
    elif failure == "traversal":
        path = Path("other/../people.csv")
        (project / "other").mkdir()
    elif failure == "relative_root":
        root = Path(".")
    elif failure == "directory":
        path = Path("folder.csv")
        (project / path).mkdir()
    elif failure == "format":
        path = Path("unsupported.txt")
        (project / path).write_text("id\n1\n")
    else:
        code = Path("missing.py")
    with pytest.raises((ValueError, OSError)) as caught:
        extract_data(
            identity,
            project_root=root,
            sources={"people": path},
            destination=Path("result"),
            code_paths=[code],
        )
    assert any(
        "source" in note or "configuration" in note for note in caught.value.__notes__
    )
    assert not (project / "result").exists()


@pytest.mark.parametrize(
    "threshold,expected", [(30, [(2, "beta"), (3, "alpha")]), (40, [(3, "alpha")])]
)
def test_pandas_selection_filter_merge(
    project: Path, threshold: int, expected: list[tuple[int, str]]
) -> None:
    """AC-01/03: project pandas code consumes settings and supplies native output."""
    pd.DataFrame({"group": ["A", "B"], "label": ["alpha", "beta"]}).to_parquet(
        project / "groups.parquet", index=False
    )

    def extract(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        minimum = settings["minimum"]
        assert isinstance(minimum, int)
        people = frames["people"]
        return (
            people.loc[people.age.ge(minimum)]
            .merge(frames["groups"], on="group", how="left", validate="many_to_one")[
                ["id", "label"]
            ]
            .sort_values("id")
        )

    frame, report = extract_data(
        extract,
        project_root=project,
        sources={"people": Path("people.csv"), "groups": Path("groups.parquet")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        settings={"minimum": threshold},
    )
    assert list(frame.itertuples(index=False, name=None)) == expected
    assert cast(dict[str, object], report["extraction"])["settings"] == {
        "minimum": threshold
    }


@pytest.mark.parametrize("kind", ["csv", "parquet"])
def test_pandas_output_provenance(project: Path, kind: str) -> None:
    """AC-02/03/04: a complete readable bundle records identities and time."""
    start = datetime.now(UTC)
    frame, report = extract_data(
        identity,
        project_root=project,
        sources={"people": Path("people.csv")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        output_format=cast("Literal['csv', 'parquet']", kind),
    )
    end = datetime.now(UTC)
    path = project / "result" / f"dataset.{kind}"
    assert path.is_file()
    persisted = pd.read_csv(path) if kind == "csv" else pd.read_parquet(path)
    assert persisted.columns.tolist() == ["id", "age", "group"]
    assert persisted["id"].tolist() == [1, 2, 3, 4]
    assert frame.index.tolist() == [0, 1, 2, 3]
    assert json.loads((project / "result/extraction.json").read_text()) == report
    assert report["schema_version"] == "1.0" and report["status"] == "complete"
    output = cast(dict[str, object], report["output"])
    assert output["sha256"] == "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    assert output["row_count"] == 4 and output["byte_count"] == path.stat().st_size
    extraction = cast(dict[str, object], report["extraction"])
    code = cast(list[dict[str, object]], extraction["code"])[0]
    assert (
        code["sha256"]
        == "sha256:" + hashlib.sha256((project / "extract.py").read_bytes()).hexdigest()
    )
    assert (
        start
        <= datetime.fromisoformat(str(report["started_at"]))
        <= datetime.fromisoformat(str(report["completed_at"]))
        <= end
    )
    assert datetime.fromtimestamp(path.stat().st_mtime, UTC) <= datetime.fromisoformat(
        str(report["completed_at"])
    )
    assert cast(float, report["elapsed_seconds"]) >= 0
    assert set(cast(dict[str, object], report["versions"])) == {
        "agentic-ml",
        "pandas",
        "pyarrow",
    }


@pytest.mark.parametrize(
    "failure",
    [
        "exists",
        "empty_exists",
        "missing_parent",
        "traversal",
        "overlap",
        "symlink_parent",
        "empty_sources",
        "empty_code",
        "unknown_options",
        "bad_settings",
        "bad_format",
    ],
)
def test_preflight_before_project_code(project: Path, failure: str) -> None:
    """AC-05: invalid destinations/configuration never invoke project code."""
    destination = Path("result")
    sources = {"people": Path("people.csv")}
    codes = [Path("extract.py")]
    settings: dict[str, object] = {}
    read_options: dict[str, dict[str, object]] = {}
    kind = "parquet"
    if failure in {"exists", "empty_exists"}:
        (project / destination).mkdir()
        if failure == "exists":
            (project / destination / "keep").write_text("unchanged")
    elif failure == "missing_parent":
        destination = Path("missing/result")
    elif failure == "traversal":
        destination = Path("../outside")
    elif failure == "overlap":
        destination = Path(".")
    elif failure == "symlink_parent":
        (project / "link").symlink_to(project, target_is_directory=True)
        destination = Path("link/result")
    elif failure == "empty_sources":
        sources = {}
    elif failure == "empty_code":
        codes = []
    elif failure == "unknown_options":
        read_options = {"unknown": {}}
    elif failure == "bad_settings":
        settings = {"invalid": float("nan")}
    else:
        kind = "unsupported"

    def sentinel(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        (project / "invoked").write_text("called")
        return frames["people"]

    with pytest.raises((ValueError, TypeError, OSError)):
        extract_data(
            sentinel,
            project_root=project,
            sources=sources,
            destination=destination,
            code_paths=codes,
            settings=settings,
            read_options=read_options,
            output_format=cast("Literal['csv', 'parquet']", kind),
        )
    assert not (project / "invoked").exists()
    if failure == "exists":
        assert (project / "result/keep").read_text() == "unchanged"


@pytest.mark.parametrize(
    "invalid", ["scalar", "duplicate_columns", "nonstring_columns"]
)
def test_invalid_callback_output(project: Path, invalid: str) -> None:
    """AC-05: invalid native results fail through standard exceptions."""

    def extract(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        if invalid == "scalar":
            return cast(pd.DataFrame, 42)
        if invalid == "duplicate_columns":
            return pd.DataFrame([[1, 2]], columns=["a", "a"])
        return pd.DataFrame({0: [1]})

    expected = TypeError if invalid == "scalar" else ValueError
    with pytest.raises(expected) as caught:
        extract_data(
            extract,
            project_root=project,
            sources={"people": Path("people.csv")},
            destination=Path("result"),
            code_paths=[Path("extract.py")],
        )
    assert any("callback" in note for note in caught.value.__notes__)
    assert not (project / "result").exists()
    assert not list(project.glob(".extraction-*"))


@pytest.mark.parametrize("changed", ["source", "code", "destination"])
def test_changed_inputs_and_publication_conflict(project: Path, changed: str) -> None:
    """AC-04/05: project-side mutations cannot publish misleading provenance."""

    def mutate(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        if changed == "source":
            (project / "people.csv").write_text("id\n99\n")
        elif changed == "code":
            (project / "extract.py").write_text("# replaced\n")
        else:
            (project / "result").mkdir()
            (project / "result/keep").write_text("owned by project")
        return frames["people"]

    with pytest.raises((ValueError, FileExistsError)):
        extract_data(
            mutate,
            project_root=project,
            sources={"people": Path("people.csv")},
            destination=Path("result"),
            code_paths=[Path("extract.py")],
        )
    assert not (project / "result/extraction.json").exists()
    assert not list(project.glob(".extraction-*"))
    if changed == "destination":
        assert (project / "result/keep").read_text() == "owned by project"


@pytest.mark.parametrize(
    "method,expected",
    [
        ("eq", [2]),
        ("ne", [1, 3]),
        ("lt", [1]),
        ("le", [1, 2]),
        ("gt", [3]),
        ("ge", [2, 3]),
        ("isin", [1, 3]),
        ("empty", []),
        ("isna", [4]),
        ("notna", [1, 2, 3]),
    ],
)
def test_native_filter_boundary_cases(
    project: Path, method: str, expected: list[int]
) -> None:
    """AC-01/03: existing callback delegation retains native pandas semantics."""

    def native(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        people = frames["people"]
        age = people["age"]
        masks = {
            "eq": age.eq(35),
            "ne": age.ne(35),
            "lt": age.lt(35),
            "le": age.le(35),
            "gt": age.gt(35),
            "ge": age.ge(35),
            "isin": age.isin([20, 40]),
            "empty": age.isin([]),
            "isna": age.isna(),
            "notna": age.notna(),
        }
        return people.loc[masks[method], ["id"]]

    frame, _ = extract_data(
        native,
        project_root=project,
        sources={"people": Path("people.csv")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        settings={"native_method": method},
    )
    assert frame.id.tolist() == expected


@pytest.mark.parametrize(
    "how,expected",
    [
        ("inner", ["a", "b"]),
        ("left", ["a", "b", "x"]),
        ("right", ["a", "b", "y"]),
        ("outer", ["a", "b", "x", "y"]),
    ],
)
def test_pandas_configured_merge(project: Path, how: str, expected: list[str]) -> None:
    """AC-01/03: project native joins remain available without toolkit wrappers."""
    pd.DataFrame({"key": ["b", "a", "x"], "left": [2, 1, 3]}).to_csv(
        project / "people.csv", index=False
    )
    pd.DataFrame({"key": ["a", "b", "y"], "right": [10, 20, 40]}).to_parquet(
        project / "right.parquet", index=False
    )

    def native(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        mode = settings["how"]
        assert mode in {"inner", "left", "right", "outer"}
        return (
            frames["people"]
            .merge(
                frames["right"],
                on="key",
                how=cast("Literal['inner', 'left', 'right', 'outer']", mode),
            )
            .sort_values("key")
        )

    frame, report = extract_data(
        native,
        project_root=project,
        sources={"people": Path("people.csv"), "right": Path("right.parquet")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        settings={"how": how},
    )
    assert frame.key.tolist() == expected
    assert cast(dict[str, object], report["extraction"])["settings"] == {"how": how}


def test_exception_identity_and_copied_settings(project: Path) -> None:
    """AC-03/05: preserve project exceptions and protect caller settings."""
    original = RuntimeError("project failure")
    settings: dict[str, object] = {"columns": ["id"]}

    def failure(
        frames: dict[str, pd.DataFrame], values: dict[str, object]
    ) -> pd.DataFrame:
        cast(list[str], values["columns"]).append("mutated")
        raise original

    with pytest.raises(RuntimeError) as caught:
        extract_data(
            failure,
            project_root=project,
            sources={"people": Path("people.csv")},
            destination=Path("result"),
            code_paths=[Path("extract.py")],
            settings=settings,
        )
    assert caught.value is original
    assert any("callback" in note for note in caught.value.__notes__)
    assert settings == {"columns": ["id"]}
    assert not (project / "result").exists()


@pytest.mark.parametrize("kind", ["csv", "parquet"])
def test_empty_dataframe_preserves_native_handoff(project: Path, kind: str) -> None:
    """AC-01/02: empty output remains readable and reports serialization types."""

    def empty(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        return frames["people"].iloc[:0]

    frame, report = extract_data(
        empty,
        project_root=project,
        sources={"people": Path("people.csv")},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
        output_format=cast("Literal['csv', 'parquet']", kind),
    )
    assert isinstance(frame, pd.DataFrame) and frame.empty
    assert frame.columns.tolist() == ["id", "age", "group"]
    assert cast(dict[str, object], report["output"])["row_count"] == 0


def test_actual_write_failure(project: Path) -> None:
    """AC-05: public OS write failure retains context and no completed bundle."""
    script = """
import resource
import signal
from pathlib import Path
from agentic_ml.extraction import extract_data
root = Path.cwd()
resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
try:
    extract_data(lambda frames, settings: frames["people"], project_root=root,
                 sources={"people": Path("people.csv")}, destination=Path("result"),
                 code_paths=[Path("extract.py")])
except OSError as error:
    assert any(".extraction-" in note for note in error.__notes__)
    assert not (root / "result").exists()
    assert not list(root.glob(".extraction-*"))
else:
    raise AssertionError("The original filesystem write failure was hidden")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "validation", ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]
)
def test_native_duplicate_keys_and_cardinality(project: Path, validation: str) -> None:
    """AC-01/03/05: native pandas cardinality remains observable through helper."""
    pd.DataFrame({"key": ["a", "a"], "left": ["l1", "l2"]}).to_csv(
        project / "people.csv", index=False
    )
    pd.DataFrame({"key": ["a", "a"], "right": ["r1", "r2"]}).to_parquet(
        project / "right.parquet", index=False
    )

    def merge(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        return (
            frames["people"]
            .merge(
                frames["right"],
                on="key",
                validate=cast(
                    "Literal['one_to_one', 'one_to_many', 'many_to_one', 'many_to_many']",
                    validation,
                ),
            )
            .sort_values(["left", "right"])
        )

    def run() -> tuple[pd.DataFrame, dict[str, object]]:
        return extract_data(
            merge,
            project_root=project,
            sources={"people": Path("people.csv"), "right": Path("right.parquet")},
            destination=Path("result"),
            code_paths=[Path("extract.py")],
            settings={"validate": validation},
        )

    if validation == "many_to_many":
        frame, _ = run()
        assert list(frame[["left", "right"]].itertuples(index=False, name=None)) == [
            ("l1", "r1"),
            ("l1", "r2"),
            ("l2", "r1"),
            ("l2", "r2"),
        ]
    else:
        with pytest.raises(pd.errors.MergeError) as caught:
            run()
        assert any("callback" in note for note in caught.value.__notes__)
        assert not (project / "result").exists()


def test_native_null_keys_and_external_source(project: Path) -> None:
    """AC-01/03: native null keys match with an explicit external local input."""
    nested = project / "experiment"
    nested.mkdir()
    (nested / "extract.py").write_text("# declared project code\n")
    pd.DataFrame({"key": [None], "left": [1]}).to_parquet(
        project / "left.parquet", index=False
    )
    pd.DataFrame({"key": [None], "right": [2]}).to_parquet(
        project / "right.parquet", index=False
    )

    def merge(
        frames: dict[str, pd.DataFrame], settings: dict[str, object]
    ) -> pd.DataFrame:
        return frames["left"].merge(frames["right"], on="key")

    frame, _ = extract_data(
        merge,
        project_root=nested,
        sources={"left": project / "left.parquet", "right": project / "right.parquet"},
        destination=Path("result"),
        code_paths=[Path("extract.py")],
    )
    assert frame[["left", "right"]].to_dict("list") == {"left": [1], "right": [2]}


@pytest.mark.parametrize(
    "failure", ["zero_csv", "bad_kwargs", "iterator", "engine", "unreadable"]
)
def test_native_reader_failures(project: Path, failure: str) -> None:
    """AC-05: propagate native parser/option/access failures with source notes."""
    source = project / "people.csv"
    options: dict[str, object] = {}
    if failure == "zero_csv":
        source.write_bytes(b"")
    elif failure == "bad_kwargs":
        options = {"not_a_pandas_option": True}
    elif failure == "iterator":
        options = {"iterator": True}
    elif failure == "engine":
        source = project / "people.parquet"
        pd.DataFrame({"id": [1]}).to_parquet(source, index=False)
        options = {"engine": "fastparquet"}
    else:
        source.chmod(0)
    try:
        with pytest.raises((ValueError, TypeError, OSError)) as caught:
            extract_data(
                identity,
                project_root=project,
                sources={"people": source},
                destination=Path("result"),
                code_paths=[Path("extract.py")],
                read_options={"people": options},
            )
        assert any("source people" in note for note in caught.value.__notes__)
        assert not (project / "result").exists()
    finally:
        source.chmod(0o600)
