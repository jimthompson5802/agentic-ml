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


def test_installed_cli_creates_inert_project_scaffolding(project: Path) -> None:
    """Initialization supplies draft inputs and valid output-free notebook files."""
    result = initialize(project)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "environment" in result.stdout and "storage" in result.stdout
    assert "pending" in result.stdout.lower()
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
    assert not (project / ".dvc").exists()
    assert not (project / ".agentic-ml/mlflow.db").exists()


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
    assert result["project"]["dependencies"] == original["project"]["dependencies"]
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
    assert payload["pending"] == ["environment", "storage"]
    config = (project / "project.yaml").read_text()
    assert "stores/dvc" in config
    assert "data_access: unconfigured" in config
    assert "agent: unconfigured" in config
    assert "approval_presentation: unconfigured" in config
    assert "guidance: {}" in config
    assert not (project / "stores").exists()
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
    assert config.read_bytes() == original
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
    assert journal["status"] == "incomplete"
    assert journal["completed_steps"] == ["preflight", "scaffold"]
    assert journal["pending_steps"] == [
        "lock",
        "sync",
        "DVC",
        "MLflow",
        "state",
        "finalize",
    ]
    assert not (state / "init.lock").exists()
    for name, content in original.items():
        backup = state / journal["backups"][name]
        assert backup.read_bytes() == content
        assert stat.S_IMODE(backup.stat().st_mode) == 0o600
    assert stat.S_IMODE((state / "init.json").stat().st_mode) == 0o600
    for name, digest in journal["checksums"].items():
        assert hashlib.sha256((project / name).read_bytes()).hexdigest() == digest
    assert (project / "uv.lock").read_bytes() == original["uv.lock"]


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
    # IP2 leaves environment synchronization to IP3; verify the emitted package
    # independently using a normal no-dependency install of the project itself.
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
    assert not (project / "stores").exists()


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
            assert "source-sentinel" not in path.read_text()
    assert "source-sentinel" in source.read_text()
