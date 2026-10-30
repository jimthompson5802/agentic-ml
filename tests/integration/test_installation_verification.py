"""Exercise pinned installation verification through subprocess interfaces."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "tests/installation/verify_installation.py"
PROBE = ROOT / "tests/installation/check_project.py"


@pytest.fixture(scope="module")
def source_repository(tmp_path_factory: pytest.TempPathFactory) -> tuple[str, str]:
    """Create an independent local Git source for repeatable driver tests."""
    source = tmp_path_factory.mktemp("installation-source")
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
        subprocess.run(command, cwd=source, check=True, capture_output=True)
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True
    ).strip()
    return source.as_uri(), revision


def test_pinned_project_runs_without_checkout_or_cache(
    source_repository: tuple[str, str], tmp_path: Path
) -> None:
    """A normal Git dependency exposes installed interfaces after cache removal."""
    repository, revision = source_repository
    workspace = tmp_path / "verification"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--repository",
            repository,
            "--revision",
            revision,
            "--workspace",
            str(workspace),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS pinned installation" in result.stdout
    assert not (workspace / "cache").exists()
    identity = json.loads((workspace / "identity.json").read_text())
    assert identity["resolved_revision"] == revision
    assert identity["repository"] == repository
    assert len(identity["lock_sha256"]) == 64
    assert identity["distributions"] == [["agentic-ml", "0.1.0"]]
    assert str(ROOT) not in identity["package_path"]


@pytest.fixture(scope="module")
def installed_project(
    source_repository: tuple[str, str], tmp_path_factory: pytest.TempPathFactory
) -> tuple[Path, str, str]:
    """Install once for independent public-probe rejection scenarios."""
    repository, revision = source_repository
    workspace = tmp_path_factory.mktemp("probe-parent") / "verification"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--repository",
            repository,
            "--revision",
            revision,
            "--workspace",
            str(workspace),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return workspace / "experiment", repository, revision


def probe_project(
    project: Path, repository: str, revision: str
) -> subprocess.CompletedProcess[str]:
    """Invoke the installed interpreter with independently supplied expectations."""
    return subprocess.run(
        [
            str(project / ".venv/bin/python"),
            "-I",
            str(PROBE),
            "--project",
            str(project),
            "--repository",
            repository,
            "--revision",
            revision,
            "--checkout",
            str(ROOT),
        ],
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
    )


def test_wrong_revision_is_rejected(installed_project: tuple[Path, str, str]) -> None:
    """A successful install cannot count as the independently expected revision."""
    project, repository, _ = installed_project
    result = probe_project(project, repository, "f" * 40)
    assert result.returncode != 0
    assert "revision mismatch" in result.stderr


def test_missing_template_is_rejected(installed_project: tuple[Path, str, str]) -> None:
    """Installed imports alone do not establish that packaged templates exist."""
    project, repository, revision = installed_project
    site = project / ".venv/lib/python3.12/site-packages"
    template = site / "agentic_ml/templates/provisional.txt"
    content = template.read_bytes()
    template.unlink()
    try:
        result = probe_project(project, repository, revision)
        assert result.returncode != 0
        assert "template resource missing" in result.stderr
    finally:
        template.write_bytes(content)


def test_altered_guidance_is_rejected(installed_project: tuple[Path, str, str]) -> None:
    """Installed runtime guidance must match independently specified contents."""
    project, repository, revision = installed_project
    guidance = (
        project
        / ".venv/lib/python3.12/site-packages/agentic_ml"
        / "runtime_guidance/provisional.md"
    )
    content = guidance.read_bytes()
    guidance.write_text("Unexpected guidance.\n")
    try:
        result = probe_project(project, repository, revision)
        assert result.returncode != 0
        assert "runtime guidance contents differ" in result.stderr
    finally:
        guidance.write_bytes(content)


def test_missing_metadata_is_rejected(installed_project: tuple[Path, str, str]) -> None:
    """A package directory cannot substitute for installed distribution metadata."""
    project, repository, revision = installed_project
    site = project / ".venv/lib/python3.12/site-packages"
    metadata = next(site.glob("agentic_ml-*.dist-info"))
    hidden = metadata.with_suffix(".hidden")
    metadata.rename(hidden)
    try:
        result = probe_project(project, repository, revision)
        assert result.returncode != 0
        assert "PackageNotFoundError" in result.stderr
    finally:
        hidden.rename(metadata)


def test_locked_revision_mismatch_is_rejected(
    installed_project: tuple[Path, str, str],
) -> None:
    """A lockfile with a different resolved commit cannot pass installed checks."""
    project, repository, revision = installed_project
    lock = project / "uv.lock"
    original = lock.read_bytes()
    lock.write_text(original.decode().replace("#" + revision, "#" + "f" * 40))
    try:
        result = probe_project(project, repository, revision)
        assert result.returncode != 0
        assert "locked revision mismatch" in result.stderr
    finally:
        lock.write_bytes(original)


def test_unknown_commit_fails_at_install(
    source_repository: tuple[str, str], tmp_path: Path
) -> None:
    """An unavailable full commit yields a retained installation diagnostic."""
    repository, _ = source_repository
    workspace = tmp_path / "invalid"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--repository",
            repository,
            "--revision",
            "0" * 40,
            "--workspace",
            str(workspace),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode != 0
    assert "FAIL install" in result.stderr
    assert "not our ref" in result.stderr or "couldn't find remote ref" in result.stderr
    assert (workspace / "install.log").is_file()
    assert "PASS pinned installation" not in result.stdout


def test_stale_lock_is_rejected_without_rewrite(
    installed_project: tuple[Path, str, str],
) -> None:
    """Locked synchronization refuses changed project metadata and preserves lock."""
    project, _, _ = installed_project
    declaration = project / "pyproject.toml"
    original = declaration.read_bytes()
    lock = (project / "uv.lock").read_bytes()
    declaration.write_text(
        original.decode().replace('version = "0.1.0"', 'version = "0.2.0"', 1)
    )
    try:
        result = subprocess.run(
            ["uv", "sync", "--locked", "--project", str(project)],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        assert result.returncode != 0
        assert "lockfile" in result.stderr and "needs to be updated" in result.stderr
        assert (project / "uv.lock").read_bytes() == lock
    finally:
        declaration.write_bytes(original)


def test_source_mapping_without_dependency_is_rejected(
    installed_project: tuple[Path, str, str],
) -> None:
    """A source mapping alone does not declare the harness as a dependency."""
    project, repository, revision = installed_project
    declaration = project / "pyproject.toml"
    original = declaration.read_bytes()
    declaration.write_text(original.decode().replace('    "agentic-ml",\n', ""))
    try:
        result = probe_project(project, repository, revision)
        assert result.returncode != 0
        assert "declared dependency mismatch" in result.stderr
    finally:
        declaration.write_bytes(original)


def test_locked_sync_preserves_environment_identity(
    source_repository: tuple[str, str], tmp_path: Path
) -> None:
    """Unchanged locked synchronization preserves declaration, lock and identity."""
    repository, revision = source_repository
    workspace = tmp_path / "stable"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--repository",
            repository,
            "--revision",
            revision,
            "--workspace",
            str(workspace),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    before = json.loads((workspace / "identity-before-sync.json").read_text())
    after = json.loads((workspace / "identity.json").read_text())
    assert before == after
    assert (workspace / "uv-before-sync.lock").read_bytes() == (
        workspace / "experiment/uv.lock"
    ).read_bytes()
    assert (workspace / "pyproject-before-sync.toml").read_bytes() == (
        workspace / "experiment/pyproject.toml"
    ).read_bytes()
    assert "PASS stable synchronization" in result.stdout


def test_explicit_upgrade_changes_pin_lock_and_identity(
    source_repository: tuple[str, str], tmp_path: Path
) -> None:
    """Two commits with the same package version have different identities."""
    from urllib.parse import unquote, urlsplit

    repository, revision_a = source_repository
    source = Path(unquote(urlsplit(repository).path))
    (source / "upgrade-note.txt").write_text("Independent second commit.\n")
    subprocess.run(["git", "add", "upgrade-note.txt"], cwd=source, check=True)
    subprocess.run(
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
            "second fixture",
        ],
        cwd=source,
        check=True,
        capture_output=True,
    )
    revision_b = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True
    ).strip()
    assert revision_a != revision_b
    workspace = tmp_path / "upgrade"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--repository",
            repository,
            "--revision",
            revision_a,
            "--upgrade-revision",
            revision_b,
            "--workspace",
            str(workspace),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    before = json.loads((workspace / "identity.json").read_text())
    after = json.loads((workspace / "identity-after-upgrade.json").read_text())
    assert before["resolved_revision"] == revision_a
    assert after["resolved_revision"] == revision_b
    assert after["requested_revision"] == revision_b
    assert after["locked_revision"] == revision_b
    assert before["lock_sha256"] != after["lock_sha256"]
    assert before["package_version"] == after["package_version"] == "0.1.0"
    assert (workspace / "uv-before-sync.lock").read_bytes() != (
        workspace / "experiment/uv.lock"
    ).read_bytes()
    assert revision_b in (workspace / "experiment/pyproject.toml").read_text()
    assert revision_a in (workspace / "pyproject-before-sync.toml").read_text()
    assert not (workspace / "cache").exists()
    assert "PASS explicit upgrade" in result.stdout


def test_retained_old_install_cannot_pass_as_upgrade(
    installed_project: tuple[Path, str, str],
) -> None:
    """Updating declarations and lock cannot hide an old installed Git revision."""
    project, repository, revision_a = installed_project
    revision_b = "f" * 40
    declaration = project / "pyproject.toml"
    lock = project / "uv.lock"
    original_declaration = declaration.read_bytes()
    original_lock = lock.read_bytes()
    declaration.write_text(
        original_declaration.decode().replace(revision_a, revision_b)
    )
    lock.write_text(original_lock.decode().replace(revision_a, revision_b))
    try:
        result = probe_project(project, repository, revision_b)
        assert result.returncode != 0
        assert "installed revision mismatch" in result.stderr
    finally:
        declaration.write_bytes(original_declaration)
        lock.write_bytes(original_lock)
