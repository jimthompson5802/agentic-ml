"""Run a committed experiment's native preprocessing and tracking handoff."""

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from agentic_ml.preprocessing import fit_preprocessing
from agentic_ml.tracking import log_preprocessing, log_run_results


def run(
    root: Path,
    tracking_uri: str,
    run_id: str,
    *,
    process_exit_code: int = 0,
    expected_output: str = "features",
    executed_notebook: Path | None = None,
) -> dict[str, Any]:
    """Fit training rows, check the fixed example, then record the existing run."""
    frame = pd.read_csv(root / "data/input.csv")
    partition = json.loads((root / "data/split.json").read_text())
    provenance = json.loads((root / "run-provenance.json").read_text())
    pipeline = Pipeline(
        [
            (
                "features",
                ColumnTransformer(
                    [
                        (
                            "numeric",
                            Pipeline(
                                [
                                    ("impute", SimpleImputer()),
                                    ("scale", StandardScaler(with_std=False)),
                                ]
                            ),
                            ["x"],
                        ),
                        (
                            "category",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                            ["category"],
                        ),
                    ]
                ),
            ),
        ]
    )
    names = ["centered_x", "category_a", "category_b"]
    fitted, record = fit_preprocessing(
        frame,
        partition_record=partition,
        pipeline=pipeline,
        selected_columns=["x", "category"],
        output_schema=[{"name": name, "dtype": "float64"} for name in names],
    )
    transformed = fitted.transform(frame[["x", "category"]])
    # Independent literal oracle BEFORE any logging; held-out rows cannot fit.
    np.testing.assert_allclose(
        transformed, [[-1, 1, 0], [0, 0, 1], [1, 1, 0], [98, 0, 0], [198, 1, 0]]
    )
    np.testing.assert_allclose(
        fitted.transform(pd.DataFrame({"x": [5.0], "category": ["b"]})), [[3, 0, 1]]
    )
    assert not hasattr(pipeline["features"], "transformers_")
    json.dumps(record, allow_nan=False)
    preprocessing = log_preprocessing(
        run_id=run_id,
        pipeline=fitted,
        record=record,
        provenance=provenance,
        project_root=root,
        tracking_uri=tracking_uri,
    )
    pd.DataFrame(transformed, columns=names).to_csv(root / "features.csv", index=False)
    result = log_run_results(
        run_id=run_id,
        project_root=root,
        tracking_uri=tracking_uri,
        provenance=provenance,
        parameters={"preprocessing": record["pipeline"]},
        metrics={"validation_accuracy": 0.75},
        outputs={"features": Path("features.csv")},
        expected_outputs=[expected_output],
        process_exit_code=process_exit_code,
        validation_passed=False,
        executed_notebook=executed_notebook,
    )
    return {"record": record, "preprocessing": preprocessing, "result": result}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), sys.argv[2], sys.argv[3]), allow_nan=False))
