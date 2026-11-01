"""Verify initialization through installed CLI/API in separate pinned projects."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a public command without inheriting harness environment overrides."""
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


@pytest.fixture(scope="module")
def source_repository(tmp_path_factory: pytest.TempPathFactory) -> tuple[str, str]:
    """Commit the reviewed source to an isolated Git dependency fixture."""
    source = tmp_path_factory.mktemp("init-source")
    shutil.copytree(ROOT / "src", source / "src")
    for name in ("pyproject.toml", "README.md"):
        shutil.copy(ROOT / name, source)
    for command in (
        ["git", "init"],
        ["git", "add", "."],
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
    ):
        result = run(command, source)
        assert result.returncode == 0, result.stderr
    revision = run(["git", "rev-parse", "HEAD"], source).stdout.strip()
    return source.as_uri(), revision


@pytest.fixture
def project(source_repository: tuple[str, str], tmp_path: Path) -> Path:
    """Install a full-SHA dependency into a fresh external experiment project."""
    target = tmp_path / "experiment"
    target.mkdir()
    url, revision = source_repository
    for command in (
        ["git", "init"],
        ["uv", "init", "--no-package", "--python", "3.12"],
        ["uv", "add", "git+" + url, "--rev", revision],
    ):
        result = run(command, target)
        assert result.returncode == 0, result.stdout + result.stderr
    return target


def initialize(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Invoke the installed entrypoint in its own project environment."""
    return run([str(project / ".venv/bin/agentic-ml"), "init", *args], project)


def test_initializes_usable_dvc_default_store(project: Path) -> None:
    """AC-04: initialized DVC exposes a writable local default remote."""
    result = initialize(project)
    assert result.returncode == 0, result.stderr
    dvc = str(project / ".venv/bin/dvc")
    remote = run([dvc, "remote", "list"], project)
    assert remote.returncode == 0, remote.stderr
    assert "agentic-ml-store" in remote.stdout
    assert (project / ".agentic-ml/dvc-store").is_dir()
    default = run([dvc, "config", "core.remote"], project)
    assert default.stdout.strip() == "agentic-ml-store"
    relative_root = run([dvc, "root"], project)
    assert relative_root.returncode == 0, relative_root.stderr
    assert (project / relative_root.stdout.strip()).resolve() == project.resolve()
    cache = project / ".dvc/cache"
    assert cache.is_dir()
    probe = cache / "setup-verification"
    probe.write_bytes(b"local cache probe")
    assert probe.read_bytes() == b"local cache probe"
    probe.unlink()


def test_initializes_mlflow_without_creating_runs(project: Path) -> None:
    """AC-04/05: a project-associated experiment reopens without implicit runs."""
    result = initialize(project)
    assert result.returncode == 0, result.stderr
    assert (project / ".agentic-ml/mlflow.db").is_file()
    probe = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            """
from pathlib import Path
from mlflow import MlflowClient
root = Path.cwd()
client = MlflowClient(tracking_uri="sqlite:///" + str(root / ".agentic-ml/mlflow.db"))
experiment = client.get_experiment_by_name("agentic-ml:initial")
assert experiment is not None
assert experiment.artifact_location == (root / ".agentic-ml/artifacts").as_uri()
assert client.search_runs([experiment.experiment_id]) == []
""",
        ],
        project,
    )
    assert probe.returncode == 0, probe.stderr


def test_initializes_durable_state_without_authority(project: Path) -> None:
    """AC-04/05: setup state reopens with no approvals or experiment runs."""
    result = initialize(project)
    assert result.returncode == 0, result.stderr
    state = project / ".agentic-ml/state/project.json"
    assert state.is_file()
    assert json.loads(state.read_text()) == {
        "schema_version": "0.1",
        "experiment": "initial",
        "status": "unconfigured",
        "approvals": [],
        "runs": [],
    }
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "complete" and journal["pending_steps"] == []
    assert "Setup pending:" not in result.stdout


@pytest.mark.parametrize("store", ["state", "database", "artifacts", "dvc"])
def test_existing_unowned_stores_are_preserved_before_setup(
    project: Path, store: str
) -> None:
    """AC-02/04: unrelated storage content prevents any durable setup writes."""
    paths = {
        "state": ".agentic-ml/state/project.json",
        "database": ".agentic-ml/mlflow.db",
        "artifacts": ".agentic-ml/artifacts/mine.txt",
        "dvc": ".agentic-ml/dvc-store/mine.txt",
    }
    target = project / paths[store]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"existing user content")
    metadata = (project / "pyproject.toml").read_bytes()
    result = initialize(project)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "conflict" in result.stderr.lower()
    assert target.read_bytes() == b"existing user content"
    assert (project / "pyproject.toml").read_bytes() == metadata
    assert not (project / "project.yaml").exists()
    assert not (project / ".agentic-ml/init.json").exists()


def test_changed_completed_state_is_preserved_on_rerun(project: Path) -> None:
    """AC-02: completed setup cannot reset an altered durable state file."""
    first = initialize(project)
    assert first.returncode == 0, first.stderr
    state = project / ".agentic-ml/state/project.json"
    changed = b'{"schema_version":"0.1","experiment":"initial","status":"review-required","approvals":[],"runs":[]}'
    state.write_bytes(changed)
    before = (project / ".agentic-ml/init.json").read_bytes()
    second = initialize(project)
    assert second.returncode == 1, second.stdout + second.stderr
    assert "conflict" in second.stderr.lower()
    assert state.read_bytes() == changed
    assert (project / ".agentic-ml/init.json").read_bytes() == before


def test_external_storage_reopens_with_same_explicit_options(
    project: Path, tmp_path: Path
) -> None:
    """AC-04: explicit external stores are usable and preserved on retry."""
    external = tmp_path / "external"
    arguments = (
        "--dvc-store",
        str(external / "dvc"),
        "--mlflow-backend",
        str(external / "mlflow.db"),
        "--artifact-store",
        str(external / "artifacts"),
        "--state-store",
        str(external / "state"),
    )
    first = initialize(project, *arguments)
    assert first.returncode == 0, first.stderr
    state = external / "state/project.json"
    assert json.loads(state.read_text())["approvals"] == []
    marker = external / "artifacts/mine.txt"
    marker.write_bytes(b"preserve existing artifact")
    second = initialize(project, *arguments)
    assert second.returncode == 0, second.stderr
    assert marker.read_bytes() == b"preserve existing artifact"
    assert (external / "mlflow.db").is_file()
    assert (external / "dvc").is_dir()


@pytest.mark.parametrize("compatible", [False, True])
def test_preserves_existing_dvc_default(project: Path, compatible: bool) -> None:
    """AC-02/04: reuse matching DVC configuration; reject other defaults early."""
    dvc = str(project / ".venv/bin/dvc")
    assert run([dvc, "init"], project).returncode == 0
    destination = ".agentic-ml/dvc-store" if compatible else "my-existing-store"
    added = run([dvc, "remote", "add", "--default", "existing", destination], project)
    assert added.returncode == 0, added.stderr
    original = (project / ".dvc/config").read_bytes()
    metadata = (project / "pyproject.toml").read_bytes()
    result = initialize(project)
    assert result.returncode == (0 if compatible else 1), result.stdout + result.stderr
    assert (project / ".dvc/config").read_bytes() == original
    if not compatible:
        assert "conflict" in result.stderr.lower()
        assert (project / "pyproject.toml").read_bytes() == metadata
        assert not (project / "project.yaml").exists()


@pytest.mark.parametrize(
    "stage,change_metadata",
    [("DVC", False), ("MLflow", False), ("state", False), ("DVC", True)],
)
def test_storage_failure_retains_stage_and_retries_safely(
    project: Path, stage: str, change_metadata: bool
) -> None:
    """AC-02/04: tool/filesystem failures retain safe evidence and reusable stores."""
    script = r"""
import os, subprocess, sys
from pathlib import Path
from unittest.mock import patch
from agentic_ml.initialization import InitOptions, InitializationError, initialize_project
stage = sys.argv[1]
original_run, original_replace = subprocess.run, os.replace
def run(command, *args, **kwargs):
    tool = str(command[0])
    if (stage == "DVC" and tool.endswith("/dvc") and command[1] == "remote") or (stage == "MLflow" and tool.endswith("/python") and "MlflowClient" in str(command)):
        return subprocess.CompletedProcess(command, 73, b"", b"token=sentinel-secret")
    return original_run(command, *args, **kwargs)
def replace(source, target, *args, **kwargs):
    if stage == "state" and str(target).endswith("/state/project.json"):
        raise PermissionError("sentinel-secret")
    return original_replace(source, target, *args, **kwargs)
with patch("subprocess.run", run), patch("os.replace", replace):
    try:
        initialize_project(InitOptions(project_root=Path.cwd()))
    except InitializationError as error:
        assert error.stage == stage, (error.stage, str(error))
        assert "sync" in error.completed_steps
        print(error)
    else:
        raise AssertionError("setup must fail")
"""
    failed = run(
        [str(project / ".venv/bin/python"), "-I", "-c", script, stage], project
    )
    assert failed.returncode == 0, failed.stdout + failed.stderr
    assert "sentinel-secret" not in failed.stdout + failed.stderr
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "incomplete"
    assert journal["storage_failure"]["stage"] == stage
    assert journal["storage_failure"]["exit_code"] == (None if stage == "state" else 73)
    assert stage not in journal["completed_steps"]
    assert not (project / ".agentic-ml/init.lock").exists()
    if change_metadata:
        metadata = project / "pyproject.toml"
        metadata.write_text(
            metadata.read_text() + "\n# edit after interrupted storage\n"
        )
        before = (project / ".agentic-ml/init.json").read_bytes()
    retried = initialize(project)
    if change_metadata:
        assert retried.returncode == 1, retried.stdout + retried.stderr
        assert "changed" in retried.stderr.lower()
        assert (project / ".agentic-ml/init.json").read_bytes() == before
    else:
        assert retried.returncode == 0, retried.stderr
        assert "Initialization complete" in retried.stdout


def test_replaced_mlflow_database_is_not_reinitialized(project: Path) -> None:
    """AC-02: rerun rejects a replaced store before changing setup evidence."""
    first = initialize(project)
    assert first.returncode == 0, first.stderr
    database = project / ".agentic-ml/mlflow.db"
    database.write_bytes(b"")
    before = (project / ".agentic-ml/init.json").read_bytes()
    second = initialize(project)
    assert second.returncode == 1, second.stdout + second.stderr
    assert "conflict" in second.stderr.lower()
    assert database.read_bytes() == b""
    assert (project / ".agentic-ml/init.json").read_bytes() == before


def test_environment_journal_does_not_adopt_unowned_database(
    project: Path, tmp_path: Path
) -> None:
    """AC-02/04: a journal from an earlier stage grants no ownership of new stores."""
    uv = shutil.which("uv")
    assert uv is not None
    tools = tmp_path / "tools"
    tools.mkdir()
    executable = tools / "uv"
    executable.write_text(
        '#!/bin/sh\nif [ "$1" = sync ]; then exit 73; fi\nexec "' + uv + '" "$@"\n'
    )
    executable.chmod(0o700)
    env = dict(os.environ)
    env["PATH"] = str(tools) + os.pathsep + env["PATH"]
    first = subprocess.run(
        [str(project / ".venv/bin/agentic-ml"), "init"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert first.returncode == 1 and "sync" in first.stderr
    database = project / ".agentic-ml/mlflow.db"
    database.write_bytes(b"")
    journal = project / ".agentic-ml/init.json"
    before = journal.read_bytes()
    second = initialize(project)
    assert second.returncode == 1, second.stdout + second.stderr
    assert "conflict" in second.stderr.lower()
    assert database.read_bytes() == b"" and journal.read_bytes() == before


@pytest.mark.parametrize(
    "boundary", ["cache-symlink", "cache-config", "permission", "ignore"]
)
def test_storage_boundary_fails_before_setup(
    project: Path, tmp_path: Path, boundary: str
) -> None:
    """AC-02/04/05: unsafe cache, inaccessible stores and exposed stores fail early."""
    outside = tmp_path / "outside"
    outside.mkdir()
    arguments: tuple[str, ...] = ()
    restricted: Path | None = None
    if boundary.startswith("cache"):
        dvc = str(project / ".venv/bin/dvc")
        assert run([dvc, "init"], project).returncode == 0
        if boundary == "cache-symlink":
            (project / ".dvc/cache").symlink_to(outside, target_is_directory=True)
        else:
            assert (
                run([dvc, "config", "cache.dir", str(outside)], project).returncode == 0
            )
    elif boundary == "permission":
        restricted = project / "store-artifacts"
        restricted.mkdir()
        restricted.chmod(0o500)
        arguments = ("--artifact-store", "store-artifacts")
    else:
        (project / ".gitignore").write_text("!/stores/**\n")
        arguments = ("--artifact-store", "stores/artifacts")
    before = (project / "pyproject.toml").read_bytes()
    try:
        result = initialize(project, *arguments)
        assert result.returncode == 1, result.stdout + result.stderr
        assert not (project / "project.yaml").exists()
        assert not (project / ".agentic-ml/init.json").exists()
        assert (project / "pyproject.toml").read_bytes() == before
        assert list(outside.iterdir()) == []
    finally:
        if restricted is not None:
            restricted.chmod(0o700)


def test_installed_cli_creates_inert_project_scaffolding(project: Path) -> None:
    """Initialization supplies draft inputs and valid output-free notebook files."""
    result = initialize(project)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Initialization complete" in result.stdout
    base = project / "experiments/initial"
    for name in ("project.yaml", "src/experiment/__init__.py"):
        assert (project / name).is_file()
    for name in ("experiment.md", "search-space.yaml", "experiment.yaml"):
        assert (base / name).is_file()
    for section in ("Data", "Features", "Evaluation", "Algorithms", "Budget"):
        assert "## " + section in (base / "experiment.md").read_text()
    expected = {
        "01_data_assessment.ipynb",
        "02_features_and_baseline.ipynb",
        "03_model_development.ipynb",
        "04_results.ipynb",
    }
    assert {p.name for p in (base / "notebooks").iterdir()} == expected
    for path in (base / "notebooks").iterdir():
        notebook = json.loads(path.read_text())
        assert notebook["nbformat"] == 4 and notebook["nbformat_minor"] == 5
        assert notebook["metadata"]["kernelspec"]["name"] == "python3"
        assert notebook["cells"][0]["cell_type"] == "markdown"
        parameters = notebook["cells"][1]
        assert parameters["metadata"]["tags"] == ["parameters"]
        assert "run_id = None" in "".join(parameters["source"])
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert cell["outputs"] == [] and cell["execution_count"] is None
    assert (project / ".dvc/config").is_file()
    assert (project / ".agentic-ml/mlflow.db").is_file()


def test_conflicting_file_blocks_all_scaffold_writes(project: Path) -> None:
    """A user-owned config is preserved and no partial scaffold is written."""
    (project / "project.yaml").write_text("user-owned: true\n")
    before = (project / "pyproject.toml").read_bytes()
    result = initialize(project)
    assert result.returncode == 1
    assert "conflict" in result.stderr.lower()
    assert (project / "project.yaml").read_text() == "user-owned: true\n"
    assert (project / "pyproject.toml").read_bytes() == before
    assert not (project / "experiments").exists()


def test_shared_metadata_is_additive_and_rerun_preserves_edits(project: Path) -> None:
    """Build scaffolding and ignores are additive; repeated init retains user work."""
    import tomllib

    pyproject = project / "pyproject.toml"
    original = tomllib.loads(pyproject.read_text())
    pyproject.write_text(
        pyproject.read_text() + "\n# custom setting\n[tool.example]\nkeep = true\n"
    )
    (project / ".gitignore").write_text("# user rules\ncustom/\n")
    lock = (project / "uv.lock").read_bytes()
    first = initialize(project)
    assert first.returncode == 0, first.stderr
    result = tomllib.loads(pyproject.read_text())
    assert result["build-system"]["build-backend"] == "hatchling.build"
    assert result["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] == [
        "src/experiment"
    ]
    assert set(original["project"]["dependencies"]) <= set(
        result["project"]["dependencies"]
    )
    assert result["tool"]["uv"]["sources"] == original["tool"]["uv"]["sources"]
    assert result["tool"]["example"]["keep"] is True
    assert "# custom setting" in pyproject.read_text()
    ignores = (project / ".gitignore").read_text()
    assert ignores.startswith("# user rules\ncustom/\n")
    for pattern in (
        "/.agentic-ml/",
        "/.venv/",
        "/data/",
        "/.env",
        "/.env.*",
        "!/.env.example",
    ):
        assert pattern in ignores.splitlines()
    lock = (project / "uv.lock").read_bytes()
    brief = project / "experiments/initial/experiment.md"
    brief.write_text("# My reviewed draft\n")
    before = {
        p.relative_to(project): p.read_bytes()
        for p in (pyproject, brief, project / ".gitignore")
    }
    second = initialize(project)
    assert second.returncode == 0, second.stderr
    for name, contents in before.items():
        assert (project / name).read_bytes() == contents
    assert (project / "uv.lock").read_bytes() == lock
    assert "Unchanged" in second.stdout


@pytest.mark.parametrize(
    "change", ["pin", "lock", "missing", "workspace", "nested", "package", "build"]
)
def test_invalid_project_is_rejected_before_writes(project: Path, change: str) -> None:
    """Reject incompatible project identity and metadata without scaffolding."""
    config = project / "pyproject.toml"
    text = config.read_text()
    if change == "pin":
        import tomllib

        revision = tomllib.loads(text)["tool"]["uv"]["sources"]["agentic-ml"]["rev"]
        config.write_text(text.replace(revision, "main"))
    elif change == "lock":
        (project / "uv.lock").write_text("version = 1\npackage = []\n")
    elif change == "missing":
        config.unlink()
    elif change == "workspace":
        config.write_text(text + "\n[tool.uv.workspace]\nmembers = []\n")
    elif change == "nested":
        (project / "nested").mkdir()
        shutil.copy(config, project / "nested/pyproject.toml")
    elif change == "package":
        config.write_text(text.replace('name = "experiment"', 'name = "123-invalid"'))
    else:
        config.write_text(
            text
            + '\n[build-system]\nrequires = []\nbuild-backend = "unsupported.build"\n'
        )
    before = {
        p.relative_to(project): p.read_bytes()
        for p in project.rglob("*")
        if p.is_file() and ".venv" not in p.parts and ".git" not in p.parts
    }
    result = initialize(project)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert not (project / "experiments").exists()
    assert not (project / ".agentic-ml").exists()
    for name, value in before.items():
        assert (project / name).read_bytes() == value


@pytest.mark.parametrize(
    "boundary",
    [
        "symlink",
        "store-overlap",
        "store-secret",
        "store-existing",
        "ignore-negation",
        "file-parent",
        "concurrent",
    ],
)
def test_unsafe_destinations_are_rejected(
    project: Path, tmp_path: Path, boundary: str
) -> None:
    """Setup writes cannot escape declared destinations or overwrite local state."""
    arguments: list[str] = []
    outside = tmp_path / "outside"
    outside.mkdir()
    if boundary == "symlink":
        (project / "experiments").symlink_to(outside, target_is_directory=True)
    elif boundary == "store-overlap":
        arguments = ["--state-store", "src/state"]
    elif boundary == "store-secret":
        arguments = [
            "--dvc-store",
            "https://user:sentinel-secret@example.invalid/store",
        ]
    elif boundary == "store-existing":
        (outside / "mine.txt").write_text("preserve")
        arguments = ["--artifact-store", str(outside)]
    elif boundary == "ignore-negation":
        (project / ".gitignore").write_text("!/.agentic-ml/state/\n")
    elif boundary == "file-parent":
        (project / "experiments").write_text("preserve")
    else:
        (project / ".agentic-ml").mkdir()
        (project / ".agentic-ml/init.lock").write_text("busy")
    result = initialize(project, *arguments)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert "sentinel-secret" not in result.stdout + result.stderr
    assert not (project / "project.yaml").exists()
    assert not (outside / "initial").exists()


def test_public_api_from_other_cwd_records_explicit_unconfigured_setup(
    project: Path, tmp_path: Path
) -> None:
    """CLI/API resolve relative stores at the selected root and grant no authority."""
    script = """
import json, sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, initialize_project
result = initialize_project(InitOptions(project_root=Path(sys.argv[1]), experiment="baseline", dvc_store=Path("stores/dvc")))
print(json.dumps({"root": str(result.project_root), "pending": result.setup_pending, "created": result.created}))
"""
    result = run(
        [str(project / ".venv/bin/python"), "-I", "-c", script, str(project)], tmp_path
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["root"] == str(project.resolve())
    assert payload["pending"] == []
    config = (project / "project.yaml").read_text()
    assert "stores/dvc" in config
    assert "data_access: unconfigured" in config
    assert "agent: unconfigured" in config
    assert "approval_presentation: unconfigured" in config
    assert "guidance: {}" in config
    assert (project / "stores/dvc").is_dir()
    assert not (project / "AGENTS.md").exists()
    assert not (project / "runtime_guidance").exists()
    # Same explicit options through the installed CLI, from another cwd.
    cli = run(
        [
            str(project / ".venv/bin/agentic-ml"),
            "init",
            "--project-root",
            str(project),
            "--experiment",
            "baseline",
            "--dvc-store",
            "stores/dvc",
        ],
        tmp_path,
    )
    assert cli.returncode == 0, cli.stderr
    assert "Unchanged" in cli.stdout


@pytest.mark.parametrize(
    "mutation", ["schema", "identity", "storage", "missing-file", "journal"]
)
def test_rerun_rejects_incompatible_saved_setup(project: Path, mutation: str) -> None:
    """Saved setup state never masks incompatible config or missing evidence."""
    first = initialize(project)
    assert first.returncode == 0, first.stderr
    config = project / "project.yaml"
    if mutation == "schema":
        config.write_text(
            config.read_text().replace("'0.1'", "'99.0'").replace('"0.1"', '"99.0"')
        )
    elif mutation == "identity":
        config.write_text(
            config.read_text().replace("package: experiment", "package: changed")
        )
    elif mutation == "storage":
        config.write_text(
            config.read_text().replace(".agentic-ml/state", "different/state")
        )
    elif mutation == "missing-file":
        (project / "experiments/initial/experiment.yaml").unlink()
    else:
        (project / ".agentic-ml/init.json").write_text('{"schema_version":"99"}')
    before = config.read_bytes()
    result = initialize(project)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert config.read_bytes() == before


def test_explicit_existing_package_preserves_source_and_build(project: Path) -> None:
    """A developer-selected src package keeps its source and build backend."""
    source = project / "src/my_package/__init__.py"
    source.parent.mkdir(parents=True)
    source.write_text('"""My package."""\nVALUE = 42\n')
    config = project / "pyproject.toml"
    config.write_text(
        config.read_text()
        + '\n[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n'
    )
    original = config.read_bytes()
    result = initialize(project, "--package-name", "my_package")
    assert result.returncode == 0, result.stderr
    import tomllib

    before = tomllib.loads(original.decode())
    after = tomllib.loads(config.read_text())
    assert set(before["project"]["dependencies"]) <= set(
        after["project"]["dependencies"]
    )
    assert "numpy>=2,<3" in after["project"]["dependencies"]
    after["project"]["dependencies"] = before["project"]["dependencies"]
    assert after == before
    assert source.read_text() == '"""My package."""\nVALUE = 42\n'
    assert not (project / "src/experiment").exists()


def test_setup_inventory_and_backups_are_private_and_preserve_originals(
    project: Path,
) -> None:
    """Scaffold completion retains a recoverable setup record without permissions."""
    import hashlib
    import stat

    (project / ".gitignore").write_text("# existing user ignores\n")
    original = {
        name: (project / name).read_bytes()
        for name in ("pyproject.toml", "uv.lock", ".gitignore")
    }
    result = initialize(project)
    assert result.returncode == 0, result.stderr
    state = project / ".agentic-ml"
    journal = json.loads((state / "init.json").read_text())
    assert journal["status"] == "complete"
    assert journal["completed_steps"] == [
        "preflight",
        "scaffold",
        "lock",
        "sync",
        "environment-check",
        "DVC",
        "MLflow",
        "state",
        "finalize",
    ]
    assert journal["pending_steps"] == []
    assert not (state / "init.lock").exists()
    for name, content in original.items():
        backup = state / journal["backups"][name]
        assert backup.read_bytes() == content
        assert stat.S_IMODE(backup.stat().st_mode) == 0o600
    assert stat.S_IMODE((state / "init.json").stat().st_mode) == 0o600
    for name, digest in (
        journal["checksums"] | journal["environment"]["checksums"]
    ).items():
        assert hashlib.sha256((project / name).read_bytes()).hexdigest() == digest
    assert (project / "uv.lock").read_bytes() != original["uv.lock"]


def test_interrupted_scaffold_preserves_evidence_and_retries_safely(
    project: Path,
) -> None:
    """An external filesystem failure retains originals and permits a safe rerun."""
    script = """
import os, sys
from pathlib import Path
from agentic_ml.initialization import InitOptions, InitializationError, initialize_project
original = os.replace
def fail(source, target, *args, **kwargs):
    if str(target).endswith("/project.yaml"):
        raise PermissionError("fixture failure")
    return original(source, target, *args, **kwargs)
os.replace = fail
try:
    initialize_project(InitOptions(Path(sys.argv[1])))
except InitializationError as error:
    print(error.stage)
    print(error.completed_steps)
    sys.exit(1)
sys.exit(0)
"""
    original = (project / "pyproject.toml").read_bytes()
    first = run(
        [str(project / ".venv/bin/python"), "-I", "-c", script, str(project)], project
    )
    assert first.returncode == 1 and "scaffold" in first.stdout, first.stderr
    state = project / ".agentic-ml"
    assert (state / "init.json").is_file()
    assert not (state / "init.lock").exists()
    journal = json.loads((state / "init.json").read_text())
    assert (state / journal["backups"]["pyproject.toml"]).read_bytes() == original
    second = initialize(project)
    assert second.returncode == 0, second.stderr
    assert (project / "project.yaml").is_file()
    assert (state / journal["backups"]["pyproject.toml"]).read_bytes() == original


def test_unrelated_ignore_exceptions_are_preserved(project: Path) -> None:
    """A user exception unrelated to generated stores does not block setup."""
    (project / ".gitignore").write_text("docs/*\n!docs/README.md\n")
    result = initialize(project)
    assert result.returncode == 0, result.stderr
    assert (project / ".gitignore").read_text().startswith("docs/*\n!docs/README.md\n")


def test_new_package_scaffold_is_importable_after_normal_project_install(
    project: Path,
) -> None:
    """Generated build metadata installs the project package without source tricks."""
    first = initialize(project)
    assert first.returncode == 0, first.stderr
    # Also verify that a normal no-dependency reinstall preserves public imports.
    install = run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(project / ".venv/bin/python"),
            "--no-deps",
            ".",
        ],
        project,
    )
    assert install.returncode == 0, install.stderr
    probe = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            "import experiment; print(experiment.__doc__)",
        ],
        project.parent,
    )
    assert probe.returncode == 0, probe.stderr
    assert probe.stdout.strip() == "Project-owned experiment code."


def test_custom_internal_storage_roots_are_ignored(project: Path) -> None:
    """Explicit internal stores stay outside Git without hiding source files."""
    result = initialize(
        project, "--dvc-store", "stores/data", "--artifact-store", "outputs/models"
    )
    assert result.returncode == 0, result.stderr
    for name in ("stores/data/probe", "outputs/models/probe"):
        ignored = run(["git", "check-ignore", "--no-index", name], project)
        assert ignored.returncode == 0, ignored.stdout + ignored.stderr
    visible = run(["git", "check-ignore", "--no-index", "project.yaml"], project)
    assert visible.returncode == 1
    assert (project / "stores/data").is_dir()


def test_credentials_in_project_metadata_are_not_copied_to_setup_evidence(
    project: Path,
) -> None:
    """Refuse credential-bearing configuration before writing backups or logs."""
    config = project / "pyproject.toml"
    config.write_text(
        config.read_text()
        + '\n[[tool.uv.index]]\nurl = "https://user:sentinel-secret@example.invalid/simple"\n'
    )
    result = initialize(project)
    assert result.returncode == 1
    assert "sentinel-secret" not in result.stdout + result.stderr
    assert not (project / ".agentic-ml").exists()
    assert not (project / "project.yaml").exists()


def test_unwritable_destination_fails_before_durable_setup(project: Path) -> None:
    """A denied destination is found before any scaffold or setup journal write."""
    directory = project / "experiments"
    directory.mkdir()
    directory.chmod(0o500)
    try:
        result = initialize(project)
        assert result.returncode == 1
        assert "Traceback" not in result.stderr
        assert not (project / "project.yaml").exists()
        assert not (project / ".agentic-ml").exists()
    finally:
        directory.chmod(0o700)


def test_existing_project_code_is_not_copied_into_setup_journal(project: Path) -> None:
    """Preserving selected user code does not snapshot it into setup evidence."""
    source = project / "src/custom/__init__.py"
    source.parent.mkdir(parents=True)
    source.write_text('"""My package."""\nPRIVATE_VALUE = "source-sentinel"\n')
    config = project / "pyproject.toml"
    config.write_text(
        config.read_text()
        + '\n[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n'
    )
    result = initialize(project, "--package-name", "custom")
    assert result.returncode == 0, result.stderr
    for path in (project / ".agentic-ml").rglob("*"):
        if path.is_file():
            assert b"source-sentinel" not in path.read_bytes()
    assert "source-sentinel" in source.read_text()


def test_init_synchronizes_required_environment(project: Path) -> None:
    """Installed init supplies ML/notebook tools and an importable project package."""
    import tomllib

    original = tomllib.loads((project / "pyproject.toml").read_text())
    result = initialize(project)
    assert result.returncode == 0, result.stdout + result.stderr
    metadata = tomllib.loads((project / "pyproject.toml").read_text())
    required = {
        "numpy>=2,<3",
        "pandas>=2,<4",
        "scikit-learn>=1.6,<2",
        "nbclient>=0.10,<1",
        "ipykernel>=6,<8",
        "nbformat>=5,<6",
        "dvc>=3,<4",
        "mlflow>=3,<4",
    }
    assert required <= set(metadata["project"]["dependencies"])
    assert metadata["tool"]["uv"]["sources"] == original["tool"]["uv"]["sources"]
    probe = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            "import numpy, pandas, sklearn, nbclient, ipykernel, nbformat, dvc, mlflow, experiment",
        ],
        project,
    )
    assert probe.returncode == 0, probe.stderr
    lock = (project / "uv.lock").read_bytes()
    for command in (["uv", "sync", "--locked"], ["uv", "lock", "--check"]):
        checked = run(command, project)
        assert checked.returncode == 0, checked.stderr
    assert (project / "uv.lock").read_bytes() == lock


def test_dependency_conflict_preserves_settings_and_allows_reviewed_retry(
    project: Path,
) -> None:
    """Resolver failures retain conflicting bounds and the original harness source."""
    import tomllib

    metadata = project / "pyproject.toml"
    metadata.write_text(
        metadata.read_text().replace('"agentic-ml",', '"agentic-ml",\n    "numpy<2",')
    )
    original = tomllib.loads(metadata.read_text())
    lock = (project / "uv.lock").read_bytes()
    result = initialize(project)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "lock" in result.stderr and "exit" in result.stderr
    assert "numpy<2" in metadata.read_text()
    assert (
        tomllib.loads(metadata.read_text())["tool"]["uv"]["sources"]
        == original["tool"]["uv"]["sources"]
    )
    assert (project / "uv.lock").read_bytes() == lock
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "incomplete"
    assert journal["environment"]["exit_code"] != 0
    assert "sync" not in journal["completed_steps"]
    assert not (project / ".agentic-ml/init.lock").exists()
    second = initialize(project)
    assert second.returncode == 1
    assert "lock" in second.stderr


def test_sync_success_requires_importable_project(
    project: Path, tmp_path: Path
) -> None:
    """A tool reporting success without installing the project cannot complete setup."""
    tools = tmp_path / "tools"
    tools.mkdir()
    executable = tools / "uv"
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o700)
    env = dict(os.environ)
    env["PATH"] = str(tools) + os.pathsep + env["PATH"]
    result = subprocess.run(
        [str(project / ".venv/bin/agentic-ml"), "init"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "environment-check" in result.stderr
    saved = json.loads((project / ".agentic-ml/init.json").read_text())
    assert "environment-check" not in saved["completed_steps"]
    assert not (project / ".agentic-ml/init.lock").exists()


@pytest.mark.parametrize("change_metadata", [False, True])
def test_sync_failure_retry_preserves_metadata(
    project: Path, tmp_path: Path, change_metadata: bool
) -> None:
    """A failed sync retains evidence and retries only unchanged intermediate files."""
    uv = shutil.which("uv")
    assert uv is not None
    tools = tmp_path / "tools"
    tools.mkdir()
    executable = tools / "uv"
    executable.write_text(
        '#!/bin/sh\nif [ "$1" = sync ]; then echo "token=sentinel-secret" >&2; exit 73; fi\n'
        'exec "' + uv + '" "$@"\n'
    )
    executable.chmod(0o700)
    env = dict(os.environ)
    env["PATH"] = str(tools) + os.pathsep + env["PATH"]
    failed = subprocess.run(
        [str(project / ".venv/bin/agentic-ml"), "init"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert failed.returncode == 1
    assert "sync" in failed.stderr and "73" in failed.stderr
    assert "sentinel-secret" not in failed.stdout + failed.stderr
    journal = project / ".agentic-ml/init.json"
    assert "sentinel-secret" not in journal.read_text()
    saved = json.loads(journal.read_text())
    assert "lock" in saved["completed_steps"] and "sync" not in saved["completed_steps"]
    metadata = project / "pyproject.toml"
    if change_metadata:
        metadata.write_text(metadata.read_text() + "\n# user edit after failure\n")
    before = metadata.read_bytes()
    retried = initialize(project)
    assert metadata.read_bytes() == before
    if change_metadata:
        assert retried.returncode == 1
        assert "changed" in retried.stderr
    else:
        assert retried.returncode == 0, retried.stderr
        assert "Initialization complete" in retried.stdout


def test_sync_preserves_existing_bounds_packages_and_environment_choice(
    project: Path, tmp_path: Path
) -> None:
    """Setup intersects existing bounds, retains unrelated packages and uses .venv."""
    import tomllib

    added = run(["uv", "add", "numpy>=2.0,<2.5", "humanize>=4,<5"], project)
    assert added.returncode == 0, added.stderr
    extra = run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(project / ".venv/bin/python"),
            "more-itertools",
        ],
        project,
    )
    assert extra.returncode == 0, extra.stderr
    original = tomllib.loads((project / "pyproject.toml").read_text())
    other = tmp_path / "other-environment"
    env = dict(os.environ)
    env["UV_PROJECT_ENVIRONMENT"] = str(other)
    env["VIRTUAL_ENV"] = str(other)
    result = subprocess.run(
        [str(project / ".venv/bin/agentic-ml"), "init"],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not other.exists()
    metadata = tomllib.loads((project / "pyproject.toml").read_text())
    assert set(original["project"]["dependencies"]) <= set(
        metadata["project"]["dependencies"]
    )
    assert metadata["tool"]["uv"]["sources"] == original["tool"]["uv"]["sources"]
    probe = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            "import humanize, more_itertools; from importlib.metadata import version; print(version('numpy'))",
        ],
        project,
    )
    assert probe.returncode == 0, probe.stderr
    assert probe.stdout.startswith(("2.0.", "2.1.", "2.2.", "2.3.", "2.4."))


def test_symlink_environment_is_rejected_before_setup(
    project: Path, tmp_path: Path
) -> None:
    """Setup cannot synchronize an environment outside its selected project root."""
    outside = tmp_path / "outside-environment"
    environment = project / ".venv"
    environment.rename(outside)
    environment.symlink_to(outside, target_is_directory=True)
    result = initialize(project)
    assert result.returncode == 1
    assert "Symlink" in result.stderr
    assert not (project / "project.yaml").exists()
    assert not (project / ".agentic-ml").exists()


@pytest.mark.parametrize(
    "destination",
    [
        "directory-symlink",
        "directory-file",
        "file-symlink",
        "file-directory",
        "conflict",
    ],
)
def test_unsafe_backup_destinations_preserve_project_and_external_files(
    project: Path, tmp_path: Path, destination: str
) -> None:
    """AC-02/05: invalid backup destinations fail before durable setup writes."""
    (project / ".gitignore").write_bytes(b"# existing ignore rules\n")
    state = project / ".agentic-ml"
    state.mkdir()
    backups = state / "backups"
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "pyproject.toml.original"
    sentinel.write_bytes(b"external original")
    if destination == "directory-symlink":
        backups.symlink_to(outside, target_is_directory=True)
    elif destination == "directory-file":
        backups.write_bytes(b"existing backup path")
    else:
        backups.mkdir()
        target = backups / "pyproject.toml.original"
        if destination == "file-symlink":
            target.symlink_to(sentinel)
        elif destination == "file-directory":
            target.mkdir()
        else:
            target.write_bytes(b"unrelated backup")
    originals = {
        name: (project / name).read_bytes()
        for name in ("pyproject.toml", "uv.lock", ".gitignore")
    }
    result = initialize(project)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert not (project / "project.yaml").exists()
    assert not (state / "init.json").exists()
    assert not (state / "init.lock").exists()
    assert sentinel.read_bytes() == b"external original"
    for name, content in originals.items():
        assert (project / name).read_bytes() == content
    if destination == "directory-symlink":
        assert backups.is_symlink()
        assert list(outside.iterdir()) == [sentinel]
    elif destination == "directory-file":
        assert backups.read_bytes() == b"existing backup path"
    elif destination == "file-symlink":
        assert (backups / "pyproject.toml.original").is_symlink()
    elif destination == "file-directory":
        assert (backups / "pyproject.toml.original").is_dir()
    else:
        assert (backups / "pyproject.toml.original").read_bytes() == b"unrelated backup"


@pytest.mark.parametrize(
    "flag", ["--mlflow-backend", "--dvc-store", "--artifact-store", "--state-store"]
)
@pytest.mark.parametrize(
    "destination",
    [
        ".agentic-ml/init.json",
        ".agentic-ml/init.tmp",
        ".agentic-ml/init.lock",
        ".agentic-ml/backups",
        ".agentic-ml",
        ".agentic-ml/init.json/child",
        ".agentic-ml/init.tmp/child",
        ".agentic-ml/init.lock/child",
        ".agentic-ml/backups/nested",
    ],
)
def test_storage_cannot_overlap_initialization_metadata(
    project: Path, flag: str, destination: str
) -> None:
    """AC-02/04: reject metadata overlaps before creating a stranded journal."""
    originals = {
        name: (project / name).read_bytes() for name in ("pyproject.toml", "uv.lock")
    }
    result = initialize(project, flag, destination)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Storage overlaps protected project paths" in result.stderr
    assert not (project / "project.yaml").exists()
    assert not (project / ".agentic-ml").exists()
    for name, content in originals.items():
        assert (project / name).read_bytes() == content


@pytest.mark.parametrize("destination", ["init.json", "init.tmp"])
def test_rejected_storage_override_can_retry_with_matching_backups(
    project: Path,
    destination: str,
) -> None:
    """AC-02/04: API rejection leaves a fresh identity and valid backups reusable."""
    (project / ".gitignore").write_bytes(b"# preserve existing rules\n")
    originals = {
        name: (project / name).read_bytes()
        for name in ("pyproject.toml", "uv.lock", ".gitignore")
    }
    rejected = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            "-c",
            f"""
from pathlib import Path
from agentic_ml.initialization import InitOptions, InitializationError, initialize_project
try:
    initialize_project(InitOptions(Path.cwd(), mlflow_backend=Path('.agentic-ml/{destination}')))
except InitializationError as error:
    assert 'Storage overlaps protected project paths' in str(error)
else:
    raise AssertionError('metadata overlap was accepted')
""",
        ],
        project,
    )
    assert rejected.returncode == 0, rejected.stdout + rejected.stderr
    assert not (project / ".agentic-ml").exists()
    for name, content in originals.items():
        assert (project / name).read_bytes() == content
    backups = project / ".agentic-ml/backups"
    backups.mkdir(parents=True)
    for name, content in originals.items():
        (backups / (name.lstrip(".") + ".original")).write_bytes(content)
    corrected = initialize(project)
    assert corrected.returncode == 0, corrected.stdout + corrected.stderr
    journal = json.loads((project / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "complete"
    assert journal["storage"]["mlflow_backend"] == ".agentic-ml/mlflow.db"
    for name, content in originals.items():
        assert (backups / (name.lstrip(".") + ".original")).read_bytes() == content


def test_versioned_planning_inputs_coexist_with_initialization(
    project: Path, tmp_path: Path
) -> None:
    """US-03 AC-03/05: planning retains installed pins, drafts and init reruns."""
    initial = initialize(project)
    assert initial.returncode == 0, initial.stdout + initial.stderr
    probe = ROOT / "tests/installation/check_planning.py"
    result = run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            str(probe),
            "--workspace",
            str(tmp_path / "planning-probe"),
            "--project",
            str(project),
        ],
        tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    rerun = initialize(project)
    assert rerun.returncode == 0, rerun.stdout + rerun.stderr
    replaced = project / "experiments/initial/experiment.yaml"
    reviewed_bytes = (project / "experiment.yaml").read_bytes()
    replaced.write_bytes(reviewed_bytes)
    conflict = initialize(project)
    assert conflict.returncode != 0
    assert "conflict" in conflict.stderr.lower()
    assert replaced.read_bytes() == reviewed_bytes
