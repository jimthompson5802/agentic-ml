"""Experiment-owned extraction, preparation and JSON persistence."""

import json
from pathlib import Path

import pandas as pd

from agentic_ml.data_assessment import assess_data
from agentic_ml.splitting import create_partitions


def extract(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    """Select project data with native pandas."""
    return frames["data"].copy()


def prepare(frame: pd.DataFrame, settings: dict[str, object]) -> dict[str, object]:
    """Assess and partition only after the caller's quality policy allows it."""
    Path(str(settings["sentinel"])).write_text("prepared")
    assessment = assess_data(frame, target="label")
    _, record = create_partitions(
        frame, row_id="id", target="label", layout="train_test", seed=42, test_size=0.4
    )
    return {"assessment": assessment, "record": record}


def save_load(path: Path, record: dict[str, object]) -> dict[str, object]:
    """Persist plain JSON using project-owned file operations."""
    path.write_text(json.dumps(record, allow_nan=False), encoding="utf-8")
    result: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    assert result == record
    return result
