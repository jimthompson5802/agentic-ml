"""Verify US-41 wheel identity through installed experiment CLI and API."""

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tomllib
import uuid
from pathlib import Path

import pytest
from pytest_workspace_support import owned_workspace

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.milestone_50


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Invoke native tools without inheriting checkout environment overrides."""
    env = dict(os.environ)
    for key in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )


@pytest.fixture(scope="module", params=["direct-wheel", "rebuilt-wheel"])
def wheel(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Build each genuine artifact path independently of the installed project."""
    source = owned_workspace(request, tmp_path_factory, "wheel-source")
    shutil.copytree(ROOT / "src", source / "src")
    for name in ("pyproject.toml", "README.md"):
        shutil.copy(ROOT / name, source)
    records = ROOT / ".dev-records/verification" / ("us-41-ip4-" + uuid.uuid4().hex)
    records.mkdir(parents=True)
    commands = []

    def build(command: list[str], cwd: Path) -> None:
        result = run(command, cwd)
        commands.append(
            {
                "command": command,
                "cwd": str(cwd),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        (records / "commands.json").write_text(json.dumps(commands, indent=2))
        assert result.returncode == 0, result.stdout + result.stderr

    build(["uv", "build", "--out-dir", str(source / "dist")], source)
    archive = next((source / "dist").glob("*.tar.gz"))
    if request.param == "rebuilt-wheel":
        extracted = source / "extracted"
        with tarfile.open(archive) as distribution:
            distribution.extractall(extracted, filter="data")
        source = next(extracted.iterdir())
        build(["uv", "build", "--wheel", "--out-dir", str(source / "dist")], source)
    artifact = next((source / "dist").glob("*.whl"))
    (records / "artifacts.json").write_text(
        json.dumps(
            {
                "path": request.param,
                "wheel": str(artifact),
                "wheel_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                "sdist": str(archive),
                "sdist_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )
    return artifact


@pytest.fixture
def project(wheel: Path, tmp_path: Path) -> Path:
    """Install genuine local wheel metadata into an independent project."""
    target = tmp_path / "experiment"
    target.mkdir()
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    shutil.copy(wheel, artifacts)
    for command in (
        ["git", "init"],
        ["uv", "init", "--no-package", "--python", "3.12"],
        ["uv", "add", "../artifacts/" + wheel.name],
    ):
        result = run(command, target)
        assert result.returncode == 0, result.stdout + result.stderr
    return target


def test_cli_initializes_locked_local_wheel(project: Path, wheel: Path) -> None:
    """AC-02/03: installed CLI accepts native wheel origin and locked integrity."""
    result = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Initialization complete" in result.stdout
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "complete"
    assert journal["environment"]["toolkit_identity"] == {
        "kind": "wheel",
        "name": "agentic-ml",
        "version": "0.1.0",
        "locator": (project.parent / "artifacts" / wheel.name).as_uri(),
        "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
        "verification": "locked-archive-and-installed-payload",
    }
    metadata = tomllib.loads((project / "pyproject.toml").read_text())
    assert metadata["tool"]["uv"]["sources"]["agentic-ml"] == {
        "path": "../artifacts/" + wheel.name,
    }
    assert (project / ".dvc/config").is_file()
    assert (project / ".agentic-ml/mlflow.db").is_file()
    assert (
        json.loads((project / ".agentic-ml/state/project.json").read_text())["runs"]
        == []
    )

    lock_before = (project / "uv.lock").read_bytes()
    rerun = run(
        [str(project / ".venv/bin/agentic-ml"), "init", "--project-root", str(project)],
        project.parent,
    )
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr
    assert (project / "uv.lock").read_bytes() == lock_before
    probe = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            r"import sys, agentic_ml; from pathlib import Path; from importlib.metadata import distribution; from importlib.resources import files; assert Path(agentic_ml.__file__).is_relative_to(Path(sys.prefix)); assert distribution('agentic-ml').version == '0.1.0'; assert files('agentic_ml').joinpath('templates/provisional.txt').read_text() == 'Provisional Milestone 0 template; experiment initialization is unavailable.\n'",
        ],
        project.parent,
    )
    assert probe.returncode == 0, probe.stdout + probe.stderr


def test_api_rerun_preserves_compatible_project_from_unrelated_cwd(
    project: Path, wheel: Path, tmp_path: Path
) -> None:
    """AC-02/03/04: normalized absolute wheel selection survives public API reruns."""
    metadata = project / "pyproject.toml"
    metadata.write_text(
        metadata.read_text()
        .replace(
            'agentic-ml = { path = "../artifacts/' + wheel.name + '" }',
            '"AGENTIC.ML" = { path = "'
            + str(project.parent / "artifacts" / wheel.name)
            + '" }',
        )
        .replace('"agentic-ml",', '"AGENTIC.ML==0.1.0",')
    )
    selected = run(["uv", "lock"], project)
    assert selected.returncode == 0, selected.stdout + selected.stderr
    original = metadata.read_bytes()
    script = """
import json, sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, initialize_project
root = Path(sys.argv[1])
result = initialize_project(InitOptions(root))
assert result.project_root == root and result.setup_pending == ()
"""
    command = [str(project / ".venv/bin/python"), "-I", "-c", script, str(project)]
    first = run(command, tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    notebook = project / "experiments/initial/notebooks/01_data_assessment.ipynb"
    assert notebook.is_file()
    custom = project / "src/experiment/__init__.py"
    custom.write_text('"""Scientist customization."""\nSENTINEL = 17\n')
    marker = project / ".agentic-ml/artifacts/mine.txt"
    marker.write_bytes(b"preserve existing artifact")
    backup = project / ".agentic-ml/backups/pyproject.toml.original"
    assert backup.read_bytes() == original
    second = run(command, tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    assert custom.read_text().endswith("SENTINEL = 17\n")
    assert marker.read_bytes() == b"preserve existing artifact"
    assert backup.read_bytes() == original


def snapshot(project: Path) -> dict[str, str]:
    """Capture project files and directories outside installer-owned environment."""
    return {
        path.relative_to(project).as_posix(): (
            hashlib.sha256(path.read_bytes()).hexdigest()
            if path.is_file()
            else "directory"
        )
        for path in project.rglob("*")
        if ".venv" not in path.relative_to(project).parts
        or (
            any(
                part.startswith(("agentic_ml", "AGENTIC.ML"))
                for part in path.relative_to(project).parts
            )
            and "__pycache__" not in path.parts
        )
    }


def build_upgrade(wheel: Path, destination: Path, version: str) -> Path:
    """Build a reviewed alternative with distinct source bytes and locator."""
    source = destination / "source"
    shutil.copytree(wheel.parents[1] / "src", source / "src")
    for name in ("pyproject.toml", "README.md"):
        shutil.copy(wheel.parents[1] / name, source)
    metadata = source / "pyproject.toml"
    metadata.write_text(
        metadata.read_text().replace('version = "0.1.0"', f'version = "{version}"')
    )
    package = source / "src/agentic_ml/__init__.py"
    package.write_text(package.read_text() + "\n# Reviewed upgrade fixture.\n")
    built = run(
        ["uv", "build", "--wheel", "--out-dir", str(destination / "dist")], source
    )
    assert built.returncode == 0, built.stdout + built.stderr
    return next((destination / "dist").glob("*.whl"))


def test_explicit_new_version_upgrade_preserves_project(
    project: Path, wheel: Path, tmp_path: Path
) -> None:
    """AC-05: native selection upgrades a completed setup without losing work."""
    command = [str(project / ".venv/bin/agentic-ml"), "init"]
    first = run(command, project)
    assert first.returncode == 0, first.stdout + first.stderr
    backup = snapshot(project / ".agentic-ml/backups")
    custom = project / "src/experiment/__init__.py"
    custom.write_text('"""Scientist work."""\nVALUE = 42\n')
    artifact = project / ".agentic-ml/artifacts/result.txt"
    artifact.write_bytes(b"scientist result")
    dvc_content = project / ".agentic-ml/dvc-store/scientist.txt"
    dvc_content.write_bytes(b"preserved DVC content")
    database = project / ".agentic-ml/mlflow.db"
    database_before = database.read_bytes()
    state = project / ".agentic-ml/state/project.json"
    state_before = state.read_bytes()
    dvc_config = (project / ".dvc/config").read_bytes()
    upgraded = build_upgrade(wheel, tmp_path / "reviewed", "0.1.1")
    before = (project / "uv.lock").read_bytes()
    for ordinary in (["uv", "sync", "--locked"], command):
        stable = run(ordinary, project)
        assert stable.returncode == 0, stable.stdout + stable.stderr
        assert (project / "uv.lock").read_bytes() == before
    for native in (["uv", "add", str(upgraded)], ["uv", "sync", "--locked"]):
        selected = run(native, project)
        assert selected.returncode == 0, selected.stdout + selected.stderr
    result = run(command, project)
    assert result.returncode == 0, result.stdout + result.stderr
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    identity = journal["environment"]["toolkit_identity"]
    assert identity["version"] == "0.1.1"
    assert identity["locator"] == upgraded.as_uri()
    assert identity["sha256"] == hashlib.sha256(upgraded.read_bytes()).hexdigest()
    assert journal["status"] == "complete"
    assert custom.read_text().endswith("VALUE = 42\n")
    assert artifact.read_bytes() == b"scientist result"
    assert dvc_content.read_bytes() == b"preserved DVC content"
    assert database.read_bytes() == database_before
    assert state.read_bytes() == state_before
    assert (project / ".dvc/config").read_bytes() == dvc_config
    assert snapshot(project / ".agentic-ml/backups") == backup


def reject_identity(project: Path, expected: str) -> None:
    """Check API and CLI diagnostics and compare damaged inputs before/after."""
    before = snapshot(project)
    script = """
import sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, InitializationError, initialize_project
try:
    initialize_project(InitOptions(Path(sys.argv[1])))
except InitializationError as error:
    assert error.stage == "preflight", error.stage
    assert sys.argv[2] in str(error).lower(), str(error)
    assert "wheel" in error.recovery.lower() and "sync --locked" in error.recovery
else:
    raise AssertionError("inconsistent wheel identity was accepted")
"""
    api = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-B",
            "-c",
            script,
            str(project),
            expected,
        ],
        project.parent,
    )
    assert api.returncode == 0, api.stdout + api.stderr
    cli = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert cli.returncode == 1, cli.stdout + cli.stderr
    assert expected in cli.stderr.lower(), cli.stderr
    assert "sync --locked" in cli.stderr
    assert snapshot(project) == before


def test_same_version_upgrade_uses_artifact_identity(
    project: Path, wheel: Path, tmp_path: Path
) -> None:
    """AC-03/05: API refreshes a completed setup for a distinct same-version wheel."""
    script = """
import sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, initialize_project
assert initialize_project(InitOptions(Path(sys.argv[1]))).setup_pending == ()
"""
    command = [str(project / ".venv/bin/python"), "-I", "-c", script, str(project)]
    initialized = run(command, tmp_path)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    upgraded = build_upgrade(wheel, tmp_path / "same-version", "0.1.0")
    assert (
        hashlib.sha256(upgraded.read_bytes()).digest()
        != hashlib.sha256(wheel.read_bytes()).digest()
    )
    selected = run(["uv", "add", str(upgraded)], project)
    assert selected.returncode == 0, selected.stdout + selected.stderr
    synced = run(["uv", "sync", "--locked"], project)
    assert synced.returncode == 0, synced.stdout + synced.stderr
    result = run(command, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    identity = json.loads((project / ".agentic-ml/init.json").read_text())[
        "environment"
    ]["toolkit_identity"]
    assert identity["version"] == "0.1.0"
    assert identity["locator"] == upgraded.as_uri()
    assert identity["sha256"] == hashlib.sha256(upgraded.read_bytes()).hexdigest()
    before = (project / "uv.lock").read_bytes()
    rerun = run(command, tmp_path)
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr
    assert (project / "uv.lock").read_bytes() == before


def test_verified_but_incomplete_setup_rejects_changed_metadata(project: Path) -> None:
    """AC-04/05: verification alone cannot authorize metadata refresh on retry."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stdout + first.stderr
    path = project / ".agentic-ml/init.json"
    journal = json.loads(path.read_text())
    journal["status"] = "incomplete"
    journal["completed_steps"] = [
        s
        for s in journal["completed_steps"]
        if s not in ("DVC", "MLflow", "state", "finalize")
    ]
    journal["pending_steps"] = ["DVC", "MLflow", "state", "finalize"]
    journal.pop("storage_stage")
    for value in journal["storage"].values():
        store = project / value
        if store.is_dir():
            shutil.rmtree(store)
        else:
            store.unlink()
    path.write_text(json.dumps(journal))
    metadata = project / "pyproject.toml"
    metadata.write_text(metadata.read_text() + "\n# Changed after interrupted setup\n")
    reject_identity(project, "metadata changed")


def test_failed_sync_marks_completed_setup_incomplete(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-04/05: interrupted native synchronization cannot remain complete."""
    command = [str(project / ".venv/bin/agentic-ml"), "init"]
    first = run(command, project)
    assert first.returncode == 0, first.stdout + first.stderr
    tools = tmp_path / "tools"
    tools.mkdir()
    native = shutil.which("uv")
    assert native is not None
    shim = tools / "uv"
    shim.write_text(
        '#!/bin/sh\nif [ "$1" = "sync" ]; then exit 73; fi\nexec "'
        + native
        + '" "$@"\n'
    )
    shim.chmod(0o700)
    with monkeypatch.context() as context:
        context.setenv("PATH", str(tools) + os.pathsep + os.environ["PATH"])
        failed = run(command, project)
    assert failed.returncode == 1, failed.stdout + failed.stderr
    assert "sync" in failed.stderr and "73" in failed.stderr
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "incomplete"
    assert "finalize" in journal["pending_steps"]
    resumed = run(command, project)
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    assert (
        json.loads((project / ".agentic-ml/init.json").read_text())["status"]
        == "complete"
    )


def test_upgrade_rejects_malformed_prior_version(project: Path) -> None:
    """AC-03/04: a different saved locator cannot authorize malformed history."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stdout + first.stderr
    path = project / ".agentic-ml/init.json"
    journal = json.loads(path.read_text())
    identity = journal["environment"]["toolkit_identity"]
    identity["locator"] = (project.parent / "prior.whl").as_uri()
    identity["version"] = "invalid-version"
    path.write_text(json.dumps(journal))
    reject_identity(project, "journal")


@pytest.fixture(scope="module")
def replacement_wheel(
    wheel: Path,
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Share a genuine reviewed same-version replacement for transition cases."""
    destination = owned_workspace(request, tmp_path_factory, "replacement-wheel")
    return build_upgrade(wheel, destination, "0.1.0")


@pytest.mark.parametrize(
    "interruption",
    [
        "scaffold",
        "lock",
        "sync",
        "environment-check",
        "DVC",
        "MLflow",
        "state",
        "pending-finalize",
        "missing-finalize",
        "unverified",
    ],
)
def test_incomplete_setup_cannot_infer_upgrade(
    project: Path, replacement_wheel: Path, interruption: str
) -> None:
    """AC-04/05: no partial or inconsistent completion record authorizes upgrade."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stdout + first.stderr
    path = project / ".agentic-ml/init.json"
    journal = json.loads(path.read_text())
    if interruption == "unverified":
        journal["environment"]["verified"] = False
    elif interruption == "missing-finalize":
        journal["completed_steps"].remove("finalize")
    elif interruption == "pending-finalize":
        journal["pending_steps"] = ["finalize"]
    else:
        journal["status"] = "incomplete"
        index = journal["completed_steps"].index(interruption)
        journal["pending_steps"] = journal["completed_steps"][index:]
        journal["completed_steps"] = journal["completed_steps"][:index]
        if interruption in ("scaffold", "lock"):
            journal["environment"] = {
                "toolkit_identity": journal["environment"]["toolkit_identity"]
            }
    path.write_text(json.dumps(journal))
    selected = run(["uv", "add", str(replacement_wheel)], project)
    assert selected.returncode == 0, selected.stdout + selected.stderr
    reject_identity(project, "changed")


def test_stale_upgrade_declaration_fails_before_writes(
    project: Path, replacement_wheel: Path, wheel: Path
) -> None:
    """AC-04/05: a declaration edit alone cannot refresh the locked selection."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stdout + first.stderr
    metadata = project / "pyproject.toml"
    metadata.write_text(
        metadata.read_text().replace(
            "../artifacts/" + wheel.name, str(replacement_wheel)
        )
    )
    reject_identity(project, "source differs")


def test_recorded_git_identity_cannot_switch_to_wheel(project: Path) -> None:
    """AC-04: a saved Git setup does not authorize switching source kinds."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stdout + first.stderr
    path = project / ".agentic-ml/init.json"
    journal = json.loads(path.read_text())
    journal["environment"]["toolkit_identity"] = {
        "kind": "git",
        "name": "agentic-ml",
        "version": "0.1.0",
        "url": "file:///reviewed/prior",
        "revision": "a" * 40,
    }
    path.write_text(json.dumps(journal))
    reject_identity(project, "source-kind")


def test_payload_tampering_fails_before_project_writes(project: Path) -> None:
    """AC-03/04: independently compare installed resource bytes with locked wheel."""
    resource = next(
        (project / ".venv/lib").glob(
            "python*/site-packages/agentic_ml/templates/provisional.txt"
        )
    )
    resource.write_bytes(b"changed installed payload\n")
    reject_identity(project, "payload")


def installed_metadata(project: Path) -> Path:
    """Locate the genuine installed wheel metadata for controlled fixture damage."""
    return next(
        (project / ".venv/lib").glob("python*/site-packages/agentic_ml-*.dist-info")
    )


def test_missing_archive_metadata_fails_before_project_writes(project: Path) -> None:
    """AC-03/04: archive_info must exist even when installer supplies no hashes."""
    path = installed_metadata(project) / "direct_url.json"
    value = json.loads(path.read_text())
    del value["archive_info"]
    path.write_text(json.dumps(value))
    reject_identity(project, "archive")


@pytest.mark.parametrize(
    "archive",
    [
        {"hashes": {"sha256": "0" * 64}},
        {"hash": "sha256=" + "0" * 64},
        {"hashes": []},
        {"hash": 7},
    ],
)
def test_contradictory_installed_archive_hash_is_rejected(
    project: Path, archive: dict[str, object]
) -> None:
    """AC-03/04: present archive hashes must be valid and match the locked artifact."""
    path = installed_metadata(project) / "direct_url.json"
    value = json.loads(path.read_text())
    value["archive_info"] = archive
    path.write_text(json.dumps(value))
    reject_identity(project, "archive")


@pytest.mark.parametrize(
    "damage",
    [
        "missing-dependency",
        "duplicate-dependency",
        "extra",
        "marker",
        "direct-url",
        "registry",
        "url-source",
        "source-list",
        "duplicate-source",
        "editable",
        "directory",
        "sdist",
    ],
)
def test_unsupported_declaration_is_rejected_before_writes(
    project: Path, damage: str
) -> None:
    """AC-03/04: exactly one unconditional local wheel dependency is supported."""
    import tomlkit

    path = project / "pyproject.toml"
    document = tomlkit.parse(path.read_text())
    dependencies = document["project"]["dependencies"]
    sources = document["tool"]["uv"]["sources"]
    source = sources["agentic-ml"]
    if damage == "missing-dependency":
        dependencies.clear()
    elif damage == "duplicate-dependency":
        dependencies.append("AGENTIC.ML")
    elif damage == "extra":
        dependencies[0] = "agentic-ml[unsupported]"
    elif damage == "marker":
        dependencies[0] = 'agentic-ml; python_version >= "3.12"'
    elif damage == "direct-url":
        dependencies[0] = (
            "agentic-ml @ "
            + (project.parent / "artifacts" / Path(source["path"]).name).as_uri()
        )
    elif damage == "registry":
        del sources["agentic-ml"]
    elif damage == "url-source":
        sources["agentic-ml"] = {"url": "https://example.invalid/toolkit.whl"}
    elif damage == "source-list":
        sources["agentic-ml"] = [{"path": source["path"]}]
    elif damage == "duplicate-source":
        sources["AGENTIC.ML"] = {"path": source["path"]}
    elif damage == "editable":
        source["editable"] = True
    elif damage == "directory":
        source["path"] = "../artifacts"
    else:
        source["path"] = "../artifacts/agentic_ml-0.1.0.tar.gz"
    path.write_text(tomlkit.dumps(document))
    reject_identity(project, "declaration")


@pytest.mark.parametrize(
    "damage",
    [
        "duplicate",
        "missing-direct",
        "malformed-direct",
        "nonobject-direct",
        "origin",
        "version",
        "name",
        "vcs",
        "directory",
        "editable",
    ],
)
def test_invalid_installed_identity_is_rejected(project: Path, damage: str) -> None:
    """AC-03/04: reject ambiguous, unsupported or mismatched installed metadata."""
    directory = installed_metadata(project)
    direct = directory / "direct_url.json"
    value = json.loads(direct.read_text())
    if damage == "duplicate":
        shutil.copytree(directory, directory.with_name("AGENTIC.ML-999.dist-info"))
    elif damage == "missing-direct":
        direct.unlink()
    elif damage == "malformed-direct":
        direct.write_text("{")
    elif damage == "nonobject-direct":
        direct.write_text("[]")
    elif damage == "origin":
        value["url"] = "file:///different/wheel.whl"
        direct.write_text(json.dumps(value))
    elif damage in ("version", "name"):
        path = directory / "METADATA"
        path.write_text(
            path.read_text().replace("Version: 0.1.0", "Version: 9.0.0")
            if damage == "version"
            else path.read_text().replace("Name: agentic-ml", "Name: another-toolkit")
        )
    else:
        value["vcs_info" if damage == "vcs" else "dir_info"] = {
            "editable": damage == "editable"
        }
        direct.write_text(json.dumps(value))
    reject_identity(project, "install")


@pytest.mark.parametrize(
    "damage",
    ["duplicate", "parent", "absolute", "backslash", "symlink", "data", "non-purelib"],
)
def test_unsupported_wheel_layout_is_rejected(project: Path, damage: str) -> None:
    """AC-03/04: bounded payload comparison never accepts unsafe or relocated members."""
    import zipfile

    import tomlkit

    path = next((project.parent / "artifacts").glob("*.whl"))
    with zipfile.ZipFile(path) as archive:
        members = [(entry, archive.read(entry)) for entry in archive.infolist()]
    with zipfile.ZipFile(path, "w") as archive:
        for entry, content in members:
            if damage == "non-purelib" and entry.filename.endswith(".dist-info/WHEEL"):
                content = content.replace(
                    b"Root-Is-Purelib: true", b"Root-Is-Purelib: false"
                )
            archive.writestr(entry, content)
        if damage == "duplicate":
            entry, content = members[0]
            with pytest.warns(UserWarning, match="Duplicate name"):
                archive.writestr(entry, content)
        elif damage != "non-purelib":
            names = {
                "parent": "../outside",
                "absolute": "/outside",
                "backslash": "agentic_ml\\outside",
                "symlink": "agentic_ml/link",
                "data": "agentic_ml-0.1.0.data/purelib/outside",
            }
            entry = zipfile.ZipInfo(names[damage])
            if damage == "symlink":
                entry.create_system = 3
                entry.external_attr = 0o120777 << 16
            archive.writestr(entry, b"unsafe")
    lock_path = project / "uv.lock"
    lock = tomlkit.parse(lock_path.read_text())
    package = next(p for p in lock["package"] if p["name"] == "agentic-ml")
    package["wheels"][0]["hash"] = (
        "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    )
    lock_path.write_text(tomlkit.dumps(lock))
    reject_identity(project, "layout")


@pytest.mark.parametrize(
    "damage",
    [
        "source",
        "missing",
        "duplicate",
        "version",
        "hash",
        "hash-syntax",
        "filename",
        "wheels",
        "absent-wheel",
        "replaced-wheel",
        "corrupt-wheel",
    ],
)
def test_invalid_locked_identity_is_rejected(project: Path, damage: str) -> None:
    """AC-03/04: incomplete or inconsistent lock and retained artifact fail preflight."""
    import tomlkit

    path = project / "uv.lock"
    document = tomlkit.parse(path.read_text())
    packages = document["package"]
    index = next(i for i, p in enumerate(packages) if p["name"] == "agentic-ml")
    package = packages[index]
    wheel = project.parent / "artifacts" / package["wheels"][0]["filename"]
    if damage == "source":
        package["source"] = {"registry": "https://example.invalid"}
    elif damage == "missing":
        del packages[index]
    elif damage == "duplicate":
        packages.append(package)
    elif damage == "version":
        package["version"] = "9.0.0"
    elif damage == "hash":
        package["wheels"][0]["hash"] = "sha256:" + "0" * 64
    elif damage == "hash-syntax":
        package["wheels"][0]["hash"] = "sha256:invalid"
    elif damage == "filename":
        package["wheels"][0]["filename"] = "different.whl"
    elif damage == "wheels":
        package["wheels"] = []
    elif damage == "absent-wheel":
        wheel.unlink()
    elif damage == "replaced-wheel":
        wheel.write_bytes(wheel.read_bytes() + b"changed encoding")
    else:
        wheel.write_bytes(b"corrupt archive")
        package["wheels"][0]["hash"] = (
            "sha256:" + hashlib.sha256(wheel.read_bytes()).hexdigest()
        )
    path.write_text(tomlkit.dumps(document))
    reject_identity(project, "wheel")


def test_wheel_symlink_is_rejected_before_project_writes(project: Path) -> None:
    """AC-04: a retained wheel locator cannot traverse a symlink."""
    wheel = next((project.parent / "artifacts").glob("*.whl"))
    retained = wheel.with_suffix(".retained")
    wheel.rename(retained)
    wheel.symlink_to(retained)
    reject_identity(project, "symlink")


@pytest.mark.parametrize("damage", ["unknown-kind", "malformed", "missing", "changed"])
def test_saved_toolkit_identity_is_checked_before_rerun(
    project: Path, damage: str
) -> None:
    """AC-03/04: saved setup evidence cannot conceal an invalid toolkit identity."""
    first = run([str(project / ".venv/bin/agentic-ml"), "init"], project)
    assert first.returncode == 0, first.stderr
    path = project / ".agentic-ml/init.json"
    journal = json.loads(path.read_text())
    identity = journal["environment"]["toolkit_identity"]
    if damage == "unknown-kind":
        identity["kind"] = "unknown"
    elif damage == "malformed":
        identity["sha256"] = []
    elif damage == "missing":
        del journal["environment"]["toolkit_identity"]
    else:
        identity["sha256"] = "0" * 64
    path.write_text(json.dumps(journal))
    reject_identity(project, "journal")


@pytest.mark.parametrize(
    "damage",
    [
        "missing-pyproject",
        "missing-lock",
        "malformed-pyproject",
        "malformed-lock",
        "missing-sources",
        "malformed-sources",
    ],
)
def test_missing_or_malformed_project_identity_is_actionable(
    project: Path, damage: str
) -> None:
    """AC-04: missing or unreadable identity has native recovery before writes."""
    if damage.startswith("missing-") and damage != "missing-sources":
        (
            project / ("pyproject.toml" if damage.endswith("pyproject") else "uv.lock")
        ).unlink()
    elif damage in ("malformed-pyproject", "malformed-lock"):
        (
            project / ("pyproject.toml" if damage.endswith("pyproject") else "uv.lock")
        ).write_text("[")
    else:
        path = project / "pyproject.toml"
        text = path.read_text()
        path.write_text(
            text[: text.index("[tool.uv.sources]")]
            + ("[tool.uv]\nsources = []\n" if damage == "malformed-sources" else "")
        )
    reject_identity(project, "metadata")


def test_wrong_environment_fails_without_repairing_selected_project(
    project: Path,
) -> None:
    """AC-04: an installed wheel cannot initialize another project's environment."""
    target = project.parent / "other"
    target.mkdir()
    (target / ".venv").mkdir()
    for name in ("pyproject.toml", "uv.lock"):
        shutil.copy(project / name, target)
    assert run(["git", "init"], target).returncode == 0
    before = snapshot(target)
    script = """
import sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, InitializationError, initialize_project
try:
    initialize_project(InitOptions(Path(sys.argv[1])))
except InitializationError as error:
    assert "environment" in str(error) and "sync --locked" in error.recovery
else:
    raise AssertionError("wrong environment accepted")
"""
    result = run(
        [str(project / ".venv/bin/python"), "-I", "-B", "-c", script, str(target)],
        project.parent,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    cli = run(
        [str(project / ".venv/bin/agentic-ml"), "init", "--project-root", str(target)],
        project.parent,
    )
    assert cli.returncode == 1 and "environment" in cli.stderr, cli.stdout + cli.stderr
    assert snapshot(target) == before


def test_wheel_filename_must_identify_the_locked_toolkit(project: Path) -> None:
    """AC-03/04: a renamed foreign wheel cannot pass via matching locator and hash."""
    import tomlkit

    artifact = next((project.parent / "artifacts").glob("*.whl"))
    renamed = artifact.with_name("another_toolkit-0.1.0-py3-none-any.whl")
    artifact.rename(renamed)
    metadata = project / "pyproject.toml"
    metadata.write_text(metadata.read_text().replace(artifact.name, renamed.name))
    path = project / "uv.lock"
    lock = tomlkit.parse(path.read_text())
    package = next(p for p in lock["package"] if p["name"] == "agentic-ml")
    package["source"]["path"] = "../artifacts/" + renamed.name
    package["wheels"][0]["filename"] = renamed.name
    path.write_text(tomlkit.dumps(lock))
    direct = installed_metadata(project) / "direct_url.json"
    value = json.loads(direct.read_text())
    value["url"] = renamed.as_uri()
    direct.write_text(json.dumps(value))
    reject_identity(project, "filename")


@pytest.mark.parametrize(
    "damage",
    [
        "missing-name",
        "missing-version",
        "wrong-name",
        "wrong-version",
        "missing-metadata",
    ],
)
def test_invalid_wheel_metadata_is_rejected(project: Path, damage: str) -> None:
    """AC-03/04: archive metadata must identify the same named, versioned toolkit."""
    import zipfile

    import tomlkit

    wheel = next((project.parent / "artifacts").glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        members = [(entry, archive.read(entry)) for entry in archive.infolist()]
    with zipfile.ZipFile(wheel, "w") as archive:
        for entry, content in members:
            if entry.filename.endswith(".dist-info/METADATA"):
                if damage == "missing-metadata":
                    continue
                changes = {
                    "missing-name": (b"Name: agentic-ml\n", b""),
                    "missing-version": (b"Version: 0.1.0\n", b""),
                    "wrong-name": (b"Name: agentic-ml", b"Name: another-toolkit"),
                    "wrong-version": (b"Version: 0.1.0", b"Version: 9.0.0"),
                }
                before, after = changes[damage]
                content = content.replace(before, after)
            archive.writestr(entry, content)
    path = project / "uv.lock"
    lock = tomlkit.parse(path.read_text())
    package = next(p for p in lock["package"] if p["name"] == "agentic-ml")
    package["wheels"][0]["hash"] = (
        "sha256:" + hashlib.sha256(wheel.read_bytes()).hexdigest()
    )
    path.write_text(tomlkit.dumps(lock))
    reject_identity(project, "metadata")
