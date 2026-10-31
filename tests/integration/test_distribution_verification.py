"""Exercise distribution verification through its public command."""

import base64
import csv
import hashlib
import io
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest

pytestmark = pytest.mark.xdist_group("distribution")

ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "tests/packaging/verify_distributions.py"


@pytest.fixture(scope="module")
def artifacts(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build real distribution fixtures independently of the driver."""
    destination = tmp_path_factory.mktemp("artifacts")
    subprocess.run(["uv", "build", "--out-dir", str(destination)], cwd=ROOT, check=True)
    return destination


def test_both_installed_wheel_paths_pass(artifacts: Path, tmp_path: Path) -> None:
    """Real wheels pass from separate experiment projects outside the checkout."""
    result = subprocess.run(
        [sys.executable, str(DRIVER), "--artifacts-dir", str(artifacts)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS direct-wheel" in result.stdout
    assert "PASS rebuilt-wheel" in result.stdout


def test_complete_initialization_from_both_artifact_paths(
    artifacts: Path, tmp_path: Path
) -> None:
    """AC-01–05: both artifact identities supply complete external-project setup."""
    workspace = tmp_path / "initialization"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_initialization.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(workspace),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS initialization {label}" in result.stdout
        for kind in ("fresh", "existing"):
            project = workspace / label / kind
            assert (project / ".dvc/config").is_file()
            assert (project / ".agentic-ml/mlflow.db").is_file()
            assert (project / ".agentic-ml/state/project.json").is_file()
            assert (
                project / "experiments/initial/notebooks/04_results.ipynb"
            ).is_file()
        assert (
            workspace / label / "existing/src/custom/__init__.py"
        ).read_text() == '"""Existing project."""\nVALUE = 42\n'


def damaged_wheel_result(
    artifacts: Path, tmp_path: Path, member: str, replacement: bytes | None
) -> subprocess.CompletedProcess[str]:
    """Construct an independently damaged wheel with a consistent RECORD."""
    damaged = tmp_path / "damaged"
    damaged.mkdir()
    wheel = next(artifacts.glob("*.whl"))
    with ZipFile(wheel) as archive:
        entries = {n: archive.read(n) for n in archive.namelist()}
    if replacement is None:
        del entries[member]
    else:
        entries[member] = replacement
    record = next(n for n in entries if n.endswith(".dist-info/RECORD"))
    rows = io.StringIO()
    writer = csv.writer(rows)
    for name, data in entries.items():
        if name != record:
            digest = (
                base64.urlsafe_b64encode(hashlib.sha256(data).digest())
                .rstrip(b"=")
                .decode()
            )
            writer.writerow([name, "sha256=" + digest, len(data)])
    writer.writerow([record, "", ""])
    entries[record] = rows.getvalue().encode()
    with ZipFile(damaged / wheel.name, "w") as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    shutil.copy(next(artifacts.glob("*.tar.gz")), damaged)
    result = subprocess.run(
        [sys.executable, str(DRIVER), "--artifacts-dir", str(damaged)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return result


def test_missing_template_reports_installed_failure(
    artifacts: Path, tmp_path: Path
) -> None:
    """A missing template fails at its installed check."""
    result = damaged_wheel_result(
        artifacts, tmp_path, "agentic_ml/templates/provisional.txt", None
    )
    assert result.returncode != 0
    assert "direct-wheel installed checks" in result.stderr
    assert "template resource missing" in result.stderr
    assert "PASS direct-wheel" not in result.stdout
    assert "PASS rebuilt-wheel" not in result.stdout


def test_altered_guidance_reports_installed_failure(
    artifacts: Path, tmp_path: Path
) -> None:
    """Guidance must equal the independently specified provisional text."""
    result = damaged_wheel_result(
        artifacts,
        tmp_path,
        "agentic_ml/runtime_guidance/provisional.md",
        b"Unexpected guidance.\n",
    )
    assert result.returncode != 0
    assert "direct-wheel installed checks" in result.stderr
    assert "runtime guidance contents differ" in result.stderr
    assert "PASS direct-wheel" not in result.stdout


def test_wrong_cli_version_reports_installed_failure(
    artifacts: Path, tmp_path: Path
) -> None:
    """An installed CLI cannot report a different version than wheel metadata."""
    result = damaged_wheel_result(
        artifacts,
        tmp_path,
        "agentic_ml/cli/__init__.py",
        b'def main():\n    print("9.9.9")\n',
    )
    assert result.returncode != 0
    assert "direct-wheel installed checks" in result.stderr
    assert "CLI version mismatch: '9.9.9" in result.stderr
    assert "PASS direct-wheel" not in result.stdout


def test_missing_artifacts_fail_with_selection_diagnostic(tmp_path: Path) -> None:
    """An empty artifact directory fails before any installation."""
    result = subprocess.run(
        [sys.executable, str(DRIVER), "--artifacts-dir", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert (
        "artifact selection: expected exactly one wheel and one sdist" in result.stderr
    )
    assert "PASS" not in result.stdout


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
def test_ambiguous_artifacts_fail_before_install(
    artifacts: Path, tmp_path: Path, kind: str
) -> None:
    """Multiple candidate artifacts must never silently select one."""
    for artifact in artifacts.iterdir():
        shutil.copy(artifact, tmp_path)
    original = next(artifacts.glob("*.whl" if kind == "wheel" else "*.tar.gz"))
    shutil.copy(original, tmp_path / ("duplicate-" + original.name))
    result = subprocess.run(
        [sys.executable, str(DRIVER), "--artifacts-dir", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert (
        "artifact selection: expected exactly one wheel and one sdist" in result.stderr
    )
    assert " install" not in result.stdout


def test_corrupted_sdist_cannot_reuse_direct_success(
    artifacts: Path, tmp_path: Path
) -> None:
    """A good direct wheel cannot conceal an unreadable source distribution."""
    shutil.copy(next(artifacts.glob("*.whl")), tmp_path)
    (tmp_path / "corrupt.tar.gz").write_bytes(b"This is not an archive.")
    result = subprocess.run(
        [sys.executable, str(DRIVER), "--artifacts-dir", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode != 0
    assert "PASS direct-wheel" in result.stdout
    assert "PASS rebuilt-wheel" not in result.stdout
    assert "sdist extraction" in result.stderr


def test_missing_initialization_schema_reports_installed_failure(
    artifacts: Path, tmp_path: Path
) -> None:
    """The installed artifact must contain usable initialization schemas."""
    result = damaged_wheel_result(
        artifacts,
        tmp_path,
        "agentic_ml/templates/initialization/schemas/project.json",
        None,
    )
    assert result.returncode != 0
    assert "initialization resource missing" in result.stderr
    assert "PASS direct-wheel" not in result.stdout
