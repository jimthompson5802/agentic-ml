"""US-14 feature comparisons verified through both normal installed artifact paths."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
from test_preprocessing_tracking import artifacts as artifacts

ROOT = Path(__file__).resolve().parents[2]
pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("distribution")]


def test_feature_comparison_from_both_artifact_paths(
    artifacts: Path, tmp_path: Path
) -> None:
    """AC-01–05: copied recipe, literal outcomes, lineage and representative failures."""
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_feature_comparison.py"),
            "--artifacts-dir",
            str(artifacts),
            "--workspace",
            str(tmp_path / "feature-comparison"),
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
    child = Path(summary["child_records"][0])
    child_summary = json.loads((child / "summary.json").read_text())
    child_commands = json.loads((child / "commands.json").read_text())
    assert any(
        row["command"][:2] == ["uv", "build"] and "--wheel" in row["command"]
        for row in child_commands
    )
    wheels = {
        "direct-wheel": next(artifacts.glob("*.whl")),
        "rebuilt-wheel": next(
            (Path(child_summary["workspace"]) / "rebuilt").glob("*.whl")
        ),
    }
    assert wheels["direct-wheel"].resolve() != wheels["rebuilt-wheel"].resolve()
    prefixes = []
    for label in ("direct-wheel", "rebuilt-wheel"):
        identity = json.loads(
            (records / "identities" / (label + "-feature-comparison.json")).read_text()
        )
        assert identity["scores"] == {
            "accuracy": [0.5, 1.0, 0.5, 0.0],
            "zero_one_loss": [0.5, 0.0, 0.5, 1.0],
        }
        assert identity["adjusted_deltas"] == [0.0, 0.5, 0.0, -0.5]
        assert identity["outcomes"] == {
            "missing_input": "rejected_before_run",
            "unknown_variant": "rejected_before_run",
            "invalid_provenance": "FAILED",
            "artifact_storage": "FAILED",
        }
        assert identity["mixed_columns"] == [
            "id",
            "n_value",
            "count_value",
            "is_a",
            "is_b",
        ]
        assert identity["toolkit_identity"]["kind"] == "wheel"
        assert (
            identity["toolkit_identity"]["sha256"]
            == hashlib.sha256(wheels[label].read_bytes()).hexdigest()
        )
        prefixes.append(identity["prefix"])
        assert identity["recipe_sha256"] == {
            name: hashlib.sha256(
                (ROOT / "examples/feature-comparison" / name).read_bytes()
            ).hexdigest()
            for name in (
                "prepare_comparison.py",
                "compare_features.py",
                "feature_variants.py",
            )
        }
        assert identity["training_module"].endswith("agentic_ml/training/__init__.py")
        assert set(identity["recipe_sha256"]) == {
            "prepare_comparison.py",
            "compare_features.py",
            "feature_variants.py",
        }
    assert prefixes[0] != prefixes[1]
    assert not list((tmp_path / "feature-comparison").rglob("pyvenv.cfg"))
