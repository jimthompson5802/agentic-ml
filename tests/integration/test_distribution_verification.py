"""Exercise distribution verification through its public command."""

import base64
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from zipfile import ZipFile

import pytest
from pytest_workspace_support import owned_workspace

pytestmark = [pytest.mark.xdist_group("distribution")]

ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "tests/packaging/verify_distributions.py"


@pytest.fixture(scope="module")
def artifacts(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Build real distribution fixtures independently of the driver."""
    destination = owned_workspace(request, tmp_path_factory, "artifacts")
    subprocess.run(["uv", "build", "--out-dir", str(destination)], cwd=ROOT, check=True)
    return destination


@pytest.mark.milestone_0
@pytest.mark.milestone_50
def test_both_installed_wheel_paths_pass(artifacts: Path, tmp_path: Path) -> None:
    """Real wheels pass from separate experiment projects outside the checkout."""
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "verification"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS direct-wheel" in result.stdout
    assert "PASS rebuilt-wheel" in result.stdout
    workspace = Path(
        next(
            line.removeprefix("WORKSPACE ")
            for line in result.stdout.splitlines()
            if line.startswith("WORKSPACE ")
        )
    )
    assert workspace.is_relative_to(tmp_path)
    assert not (workspace / "direct-wheel").exists()
    assert not (workspace / "rebuilt-wheel").exists()
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    assert json.loads((records / "summary.json").read_text())["cleanup"] == "complete"
    for label in ("direct-wheel", "rebuilt-wheel"):
        identity = json.loads((records / "identities" / (label + ".json")).read_text())
        assert identity
    assert (workspace / "source").is_dir()


@pytest.mark.milestone_1
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
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(damaged),
            "--workspace",
            str(tmp_path / "verification"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return result


@pytest.mark.milestone_0
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


@pytest.mark.milestone_0
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


@pytest.mark.milestone_0
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


@pytest.mark.milestone_0
def test_missing_artifacts_fail_with_selection_diagnostic(tmp_path: Path) -> None:
    """An empty artifact directory fails before any installation."""
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(tmp_path),
            "--workspace",
            str(tmp_path / "verification"),
        ],
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


@pytest.mark.milestone_0
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
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(tmp_path),
            "--workspace",
            str(tmp_path / "verification"),
        ],
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


@pytest.mark.milestone_0
def test_corrupted_sdist_cannot_reuse_direct_success(
    artifacts: Path, tmp_path: Path
) -> None:
    """A good direct wheel cannot conceal an unreadable source distribution."""
    shutil.copy(next(artifacts.glob("*.whl")), tmp_path)
    (tmp_path / "corrupt.tar.gz").write_bytes(b"This is not an archive.")
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(tmp_path),
            "--workspace",
            str(tmp_path / "verification"),
        ],
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


@pytest.mark.milestone_1
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


@pytest.mark.milestone_1
@pytest.mark.skip(
    reason="Temporarily skipped at developer request pending diagnosis of 120s timeouts."
)
def test_missing_planning_schema_fails_installed_inventory(
    artifacts: Path, tmp_path: Path
) -> None:
    """US-03 AC-03: neither wheel may omit the versioned planning contract."""
    result = damaged_wheel_result(
        artifacts, tmp_path, "agentic_ml/schemas/planning/1.0/plan.json", None
    )
    assert result.returncode != 0
    assert "planning resource missing" in result.stderr


@pytest.mark.milestone_1
def test_missing_validation_schema_fails_installed_inventory(
    artifacts: Path, tmp_path: Path
) -> None:
    """US-05 AC-01/04: installed validation requires its versioned schemas."""
    result = damaged_wheel_result(
        artifacts, tmp_path, "agentic_ml/schemas/validation/1.0/candidate.json", None
    )
    assert result.returncode != 0
    assert "validation resource missing" in result.stderr


@pytest.mark.milestone_1
def test_planning_from_both_artifact_paths(artifacts: Path, tmp_path: Path) -> None:
    """US-03 AC-01/03/04/05: installed interfaces work without checkout imports."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_planning.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "planning"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS planning direct-wheel" in result.stdout
    assert "PASS planning rebuilt-wheel" in result.stdout
    workspace = tmp_path / "planning"
    assert not list(workspace.rglob("pyvenv.cfg"))
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == "complete"
    assert len(summary["child_records"]) == 1
    child = Path(summary["child_records"][0])
    assert json.loads((child / "summary.json").read_text())["parent_records"] == str(
        records
    )
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert not (workspace / "distributions" / label).exists()


@pytest.mark.milestone_1
def test_missing_approval_schema_fails_installed_inventory(
    artifacts: Path, tmp_path: Path
) -> None:
    """US-03 AC-04: installed approval schemas are required on both wheel paths."""
    result = damaged_wheel_result(
        artifacts, tmp_path, "agentic_ml/schemas/approvals/1.0/approval.json", None
    )
    assert result.returncode != 0
    assert "approval resource missing" in result.stderr
    assert "PASS direct-wheel" not in result.stdout


@pytest.mark.milestone_50
def test_explicit_distribution_retention_keeps_both_interpreters(
    artifacts: Path, tmp_path: Path
) -> None:
    """A parent can consume both wheel paths and their persistent identities."""
    workspace = tmp_path / "retained"
    parent_records = tmp_path / "parent-records"
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(workspace),
            "--keep-workspace",
            "--parent-records",
            str(parent_records),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["parent_records"] == str(parent_records)
    assert summary["cleanup"] == "retained"
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert (workspace / label / "bin/python").is_file()
        identity = json.loads((records / "identities" / (label + ".json")).read_text())
        assert identity["prefix"] == str(workspace / label)
    assert len(json.loads((records / "identities/artifacts.json").read_text())) == 3


@pytest.mark.milestone_50
@pytest.mark.skip(
    reason="Temporarily skipped at developer request pending diagnosis of 120s timeouts."
)
def test_rebuilt_probe_failure_retains_both_environments(
    artifacts: Path, tmp_path: Path
) -> None:
    """A late failure retains the successful direct environment and failed rebuilt one."""
    damaged = tmp_path / "late-failure"
    damaged.mkdir()
    shutil.copy(next(artifacts.glob("*.whl")), damaged)
    with tarfile.open(next(artifacts.glob("*.tar.gz")), "r:gz") as original:
        with tarfile.open(damaged / "damaged.tar.gz", "w:gz") as target:
            for member in original.getmembers():
                data = original.extractfile(member) if member.isfile() else None
                if member.name.endswith("runtime_guidance/provisional.md"):
                    replacement = b"Damaged rebuilt guidance.\n"
                    member.size = len(replacement)
                    data = io.BytesIO(replacement)
                target.addfile(member, data)
    result = subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--artifacts-dir",
            str(damaged),
            "--workspace",
            str(tmp_path / "verification"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode != 0
    assert "PASS direct-wheel" in result.stdout
    assert "PASS rebuilt-wheel" not in result.stdout
    assert "runtime guidance contents differ" in result.stderr
    workspace = Path(
        next(
            line.removeprefix("WORKSPACE ")
            for line in result.stdout.splitlines()
            if line.startswith("WORKSPACE ")
        )
    )
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    assert (workspace / "direct-wheel/bin/python").is_file()
    assert (workspace / "rebuilt-wheel/bin/python").is_file()
    summary = json.loads((records / "summary.json").read_text())
    assert summary["verification_exit_code"] == 1
    assert summary["cleanup"] == "retained"
    identity = json.loads((records / "identities/rebuilt-wheel.json").read_text())
    assert identity["status"] == "unavailable"
    assert (records / "commands.json").is_file()


@pytest.mark.milestone_1
def test_extraction_from_both_artifact_paths(artifacts: Path, tmp_path: Path) -> None:
    """US-11 AC-01–05: installed project pandas extraction verifies both wheels."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_extraction.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "extraction"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS extraction {label}" in result.stdout, result.stdout
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == "complete"
    assert len(summary["child_records"]) == 1
    assert not list((tmp_path / "extraction").rglob("pyvenv.cfg"))


@pytest.mark.milestone_1
def test_data_quality_from_both_artifact_paths(artifacts: Path, tmp_path: Path) -> None:
    """US-12 AC-01/05: installed quality and blocking verify both wheels."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_data_quality.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "data_quality"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS data_quality {label}" in result.stdout, result.stdout
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == "complete"
    assert len(summary["child_records"]) == 1
    assert not list((tmp_path / "data_quality").rglob("pyvenv.cfg"))


@pytest.mark.milestone_1
def test_assessment_splits_from_both_artifact_paths(
    artifacts: Path, tmp_path: Path
) -> None:
    """US-12 AC-02/03: installed assessment and splits verify both wheels."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_assessment_splits.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "assessment_splits"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS assessment_splits {label}" in result.stdout, result.stdout
        assert f"PASS dataset_versioning {label}" in result.stdout, result.stdout
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == "complete"
    assert len(summary["child_records"]) == 1
    assert not list((tmp_path / "assessment_splits").rglob("pyvenv.cfg"))
