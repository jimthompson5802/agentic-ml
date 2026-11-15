"""US-18 classification verified through both normal installed artifact paths."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from test_preprocessing_tracking import artifacts as artifacts

ROOT = Path(__file__).resolve().parents[2]
pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("distribution")]


def test_training_from_both_artifact_paths(artifacts: Path, tmp_path: Path) -> None:
    """AC-01–04: installed guide runs, native predictions, lineage and failures."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_training.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "training"),
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
        identity = json.loads(
            (records / "identities" / (label + "-training.json")).read_text()
        )
        assert identity["predictions"] == [[0, 0], [0, 1], [0, 1]]
        assert identity["scores"] == [0.5, 1.0, 1.0]
        assert identity["outcomes"] == {
            "missing_input": "FAILED",
            "invalid_provenance": "FAILED",
        }
        assert identity["fresh_instances"]
        assert identity["parameter_coverage_rejected"]
        assert identity["constructor_error_preserved"]
        assert identity["toolkit_identity"]["kind"] == "wheel"
        assert identity["training_module"].endswith("agentic_ml/training/__init__.py")
    assert not list((tmp_path / "training").rglob("pyvenv.cfg"))
