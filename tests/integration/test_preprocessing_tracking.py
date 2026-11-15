"""Verify the actual installed preprocessing-to-tracking handoff."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_workspace_support import owned_workspace

pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("distribution")]
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def artifacts(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Build the same combined source into a real wheel and source archive."""
    destination = owned_workspace(request, tmp_path_factory, "tracking-artifacts")
    subprocess.run(["uv", "build", "--out-dir", str(destination)], cwd=ROOT, check=True)
    return destination


def test_actual_producer_from_both_artifact_paths(
    artifacts: Path, tmp_path: Path
) -> None:
    """US-26 AC-01–05 / US-15 AC-03: normal installed native handoff."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_tracking.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "tracking"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=600,
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
    assert summary["cleanup"] == "complete"
    assert len(summary["child_records"]) == 1
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS tracking {label}" in result.stdout
        identity = json.loads(
            (records / "identities" / (label + "-tracking.json")).read_text()
        )
        assert identity["outcomes"] == {
            "success": "FINISHED",
            "notebook_error": "FAILED",
            "missing_output": "FAILED",
            "invalid_reference": "FAILED",
        }
        assert identity["pipeline_module"].endswith(
            "agentic_ml/preprocessing/__init__.py"
        )
        assert identity["metadata"] == identity["downloaded_metadata"]
    assert not list((tmp_path / "tracking").rglob("pyvenv.cfg"))
