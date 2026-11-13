"""US-13 AC-01/02: execute the guide's project recipe and native storage."""

import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TypedDict, cast

import pandas as pd
import pytest
import yaml

pytestmark = pytest.mark.milestone_1
GUIDE = Path(__file__).resolve().parents[2] / "docs/dataset-versioning.md"
KINDS = ("source", "extracted", "partitions", "derived")


class Settings(TypedDict):
    """Project settings consumed by the guide-derived fixture."""

    sources: dict[str, str]
    memberships: dict[str, dict[str, list[int]]]


def recipe(root: Path, prefix: str, version: str = "A") -> str:
    """Execute a command taken directly from the documented shell fragments."""
    commands = [
        line
        for block in re.findall(r"```sh\n(.*?)```", GUIDE.read_text(), re.S)
        for line in block.splitlines()
    ]
    line = next(
        line
        for line in commands
        if line.startswith(prefix)
        and ("--version" not in line or line.endswith(version))
    )
    line = line.replace("/absolute/path/to/experiment/.venv/bin/python", sys.executable)
    line = line.replace("/absolute/path/to/experiment/.venv/bin/dvc", "dvc")
    line = line.replace("/absolute/path/to/experiment", str(root))
    return run(root, *shlex.split(line))


def run(root: Path, *args: str, success: bool = True) -> str:
    """Run a public command with explicit cwd and preserve native diagnostics."""
    command = list(args)
    if command[0] == "dvc":
        command[0] = str(Path(sys.executable).parent / "dvc")
    result = subprocess.run(
        command,
        cwd=root,
        env={**os.environ, "DVC_NO_ANALYTICS": "1"},
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    output = result.stdout + result.stderr
    assert (result.returncode == 0) == success, (command, output)
    return output


def pointer(root: Path, kind: str) -> str:
    """Read the native directory identity without reimplementing its algorithm."""
    metadata = yaml.safe_load((root / f"data/{kind}.dvc").read_text())
    return str(metadata["outs"][0]["md5"])


def retained(root: Path, storage: Path, kind: str, identity: str) -> None:
    """Independently compare every native manifest member to its original bytes."""
    objects = storage / "files/md5"
    manifest = objects / identity[:2] / identity[2:]
    entries = json.loads(manifest.read_text())
    assert entries
    for entry in entries:
        digest = entry["md5"]
        data = (objects / digest[:2] / digest[2:]).read_bytes()
        assert hashlib.md5(data).hexdigest() == digest
        assert data == (root / "data" / kind / entry["relpath"]).read_bytes()


@pytest.mark.parametrize("source_format", ["csv", "parquet"])
def test_guide_versions_and_retains_project_artifacts(
    tmp_path: Path, source_format: str
) -> None:
    """AC-01/02: literal outputs, commits A/B and cache/remote content agree."""
    root = tmp_path / "experiment"
    root.mkdir()
    guide = GUIDE.read_text()
    config = cast(
        Settings, json.loads(re.findall(r"```json\n(.*?)```", guide, re.S)[0])
    )
    script = re.findall(r"```python\n(.*?)```", guide, re.S)[0]
    config["sources"]["input"] = f"data/source/input.{source_format}"
    (root / "versioning.json").write_text(json.dumps(config))
    (root / "version_data.py").write_text(script)
    run(root, "git", "init")
    run(root, "git", "config", "user.email", "fixture@example.invalid")
    run(root, "git", "config", "user.name", "US-13 fixture")
    run(root, "dvc", "init")
    remote = tmp_path / "storage" if source_format == "csv" else root / "storage"
    if remote.is_relative_to(root):
        (root / ".gitignore").write_text("/storage/\n")
    run(root, "dvc", "remote", "add", "--default", "local", str(remote))
    (root / "data/source").mkdir(parents=True)
    source = root / config["sources"]["input"]
    history: dict[str, dict[str, str]] = {}
    for version, first in (("A", "A"), ("B", "Z")):
        frame = pd.DataFrame(
            {"id": [0, 1, 2, 3, 4], "label": [first, "B", "C", "D", "E"]}
        )
        if source_format == "csv":
            frame.to_csv(source, index=False)
        else:
            frame.to_parquet(source, index=False)
        recipe(root, "/absolute/path/to/experiment/.venv/bin/python", version)
        extracted = root / f"data/extracted/{version}"
        assert pd.read_parquet(extracted / "dataset.parquet").to_dict(
            "list"
        ) == frame.to_dict("list")
        report = json.loads((extracted / "extraction.json").read_text())
        assert (
            report["sources"][0]["sha256"]
            == "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
        )
        for layout, memberships in config["memberships"].items():
            directory = root / f"data/partitions/{version}/{layout}"
            record = json.loads((directory / "split.json").read_text())
            assert json.loads(json.dumps(record, allow_nan=False)) == record
            assert record["memberships"] == memberships
            assert record["layout"] == layout
            for name, ids in memberships.items():
                part = pd.read_parquet(directory / f"{name}.parquet")
                assert part.to_dict("list") == frame.set_index("id", drop=False).loc[
                    ids
                ].to_dict("list")
        assert pd.read_csv(root / f"data/derived/{version}/selected.csv").to_dict(
            "list"
        ) == {"id": [0, 2, 4], "label": [first, "C", "E"]}
        recipe(
            root,
            "/absolute/path/to/experiment/.venv/bin/dvc add data/source data/extracted",
        )
        history[version] = {kind: pointer(root, kind) for kind in KINDS}
        recipe(
            root,
            "/absolute/path/to/experiment/.venv/bin/dvc add data/source data/extracted",
        )
        assert history[version] == {kind: pointer(root, kind) for kind in KINDS}
        recipe(root, "/absolute/path/to/experiment/.venv/bin/dvc push")
        recipe(root, "/absolute/path/to/experiment/.venv/bin/dvc status --cloud")
        for kind in KINDS:
            for storage in (root / ".dvc/cache", remote):
                retained(root, storage, kind, history[version][kind])
        run(root, "git", "add", ".")
        run(root, "git", "commit", "-m", f"data: record version {version}")
        tracked = set(run(root, "git", "ls-files").splitlines())
        expected = {
            "version_data.py",
            "versioning.json",
            ".dvc/config",
            ".dvc/.gitignore",
            ".dvcignore",
            "data/.gitignore",
        } | {f"data/{kind}.dvc" for kind in KINDS}
        if remote.is_relative_to(root):
            expected.add(".gitignore")
        assert tracked == expected
        for kind in KINDS:
            metadata = yaml.safe_load(run(root, "git", "show", f"HEAD:data/{kind}.dvc"))
            assert metadata["outs"][0]["md5"] == history[version][kind]
    assert all(history["A"][kind] != history["B"][kind] for kind in KINDS)
    for kind in KINDS:
        old = yaml.safe_load(run(root, "git", "show", f"HEAD~1:data/{kind}.dvc"))
        assert old["outs"][0]["md5"] == history["A"][kind]
        # A's source was replaced; all original cache/remote bytes must still exist.
        for storage in (root / ".dvc/cache", remote):
            objects = storage / "files/md5"
            identity = history["A"][kind]
            for entry in json.loads(
                (objects / identity[:2] / identity[2:]).read_text()
            ):
                digest = entry["md5"]
                assert (
                    hashlib.md5(
                        (objects / digest[:2] / digest[2:]).read_bytes()
                    ).hexdigest()
                    == digest
                )
    # Independent edits demonstrate sensitivity without relying on new directories.
    for kind, relative, content in (
        ("source", config["sources"]["input"], b"changed source bytes\n"),
        (
            "partitions",
            "data/partitions/B/train_test/split.json",
            b'{"memberships":{"train":[4,2,0],"test":[1,3]}}\n',
        ),
        ("derived", "data/derived/B/selected.csv", b"id,label\n4,E\n2,C\n0,Z\n"),
    ):
        before = {name: pointer(root, name) for name in KINDS}
        (root / relative).write_bytes(content)
        run(root, "dvc", "add", f"data/{kind}")
        assert pointer(root, kind) != before[kind]
        assert all(
            pointer(root, name) == before[name] for name in KINDS if name != kind
        )
    for path in (str(source.relative_to(root)), ".dvc/cache"):
        assert path in run(root, "git", "check-ignore", path)
    configuration = (root / ".dvc/config").read_bytes()
    assert "missing" in run(root, "dvc", "add", "data/missing", success=False).lower()
    tracked_file = root / "tracked.csv"
    tracked_file.write_text("id\n1\n")
    run(root, "git", "add", "tracked.csv")
    tracked_before = run(root, "git", "ls-files")
    assert "git" in run(root, "dvc", "add", "tracked.csv", success=False).lower()
    assert run(root, "git", "ls-files") == tracked_before
    duplicate = root / "data/duplicate.dvc"
    duplicate.write_bytes((root / "data/source.dvc").read_bytes())
    original = source.read_bytes()
    conflict = run(root, "dvc", "add", "data/source", success=False)
    assert "source.dvc" in conflict and "duplicate.dvc" in conflict
    assert source.read_bytes() == original
    duplicate.unlink()  # Only this test-created conflicting pointer is removed.
    blocker = root / "blocked"
    blocker.write_text("regular file")
    run(root, "dvc", "remote", "add", "--local", "bad", str(blocker / "remote"))
    before_push = {kind: pointer(root, kind) for kind in KINDS}
    assert run(root, "dvc", "push", "-r", "bad", success=False).strip()
    assert before_push == {kind: pointer(root, kind) for kind in KINDS}
    assert "up to date" in run(root, "dvc", "status").lower()
    assert (root / ".dvc/config").read_bytes() == configuration
    assert "local" in run(root, "dvc", "remote", "default")
