"""Independent installed-project preprocessing oracles from the runnable guide."""

import argparse
import hashlib
import json
import re
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import agentic_ml.preprocessing
from agentic_ml.preprocessing import fit_preprocessing
from agentic_ml.splitting import create_partitions


def main() -> None:
    """Execute the documented project and verify literal held-out expectations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--guide", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace.resolve()
    root.mkdir()
    cwd = Path.cwd()
    script = re.findall(r"```python\n(.*?)```", args.guide.read_text(), re.S)[0]
    project_code = root / "preprocess.py"
    project_code.write_text(script)
    namespace: dict[str, Any] = {"__name__": "__main__", "__file__": str(project_code)}
    exec(compile(script, str(project_code), "exec"), namespace)
    fitted, record = namespace["fitted_pipeline"], namespace["record"]
    assert isinstance(fitted, Pipeline)
    np.testing.assert_allclose(namespace["validation"], [[98, 0, 0]])
    np.testing.assert_allclose(namespace["test"], [[198, 1, 0]])
    np.testing.assert_allclose(namespace["inference"], [[3, 0, 1]])
    np.testing.assert_allclose(
        fitted.transform(namespace["frame"][["x", "category"]]),
        [[-1, 1, 0], [0, 0, 1], [1, 1, 0], [98, 0, 0], [198, 1, 0]],
    )
    assert not hasattr(namespace["pipeline"]["features"], "transformers_")
    assert record["partition_record"] == namespace["partition_record"]
    assert set(record) == {
        "schema_version",
        "fit_partition",
        "partition_record",
        "selected_columns",
        "input_schema",
        "output_schema",
        "pipeline",
        "versions",
    }
    assert record["schema_version"] == "1.0"
    assert record["fit_partition"] == "train"
    assert record["selected_columns"] == ["x", "category"]
    assert record["input_schema"] == [
        {"name": "x", "dtype": "float64"},
        {"name": "category", "dtype": "str"},
    ]
    assert record["output_schema"] == [
        {"name": name, "dtype": "float64"}
        for name in ["centered_x", "category_a", "category_b"]
    ]
    params = record["pipeline"]["parameters"]
    assert params["memory"] is None and params["transform_input"] is None
    transformers = params["steps"][0][1]["parameters"]["transformers"]
    assert [item[0] for item in transformers] == ["numeric", "category"]
    assert transformers[0][2] == ["x"] and transformers[1][2] == ["category"]
    assert transformers[0][1]["parameters"]["steps"][0][1]["parameters"][
        "missing_values"
    ] == {
        "kind": "missing_value",
        "value": "nan",
    }
    assert transformers[1][1]["parameters"]["dtype"] == {
        "kind": "numpy_dtype",
        "name": "float64",
    }
    assert record["versions"] == {
        name: version(name)
        for name in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
    }
    text = json.dumps(record, allow_nan=False, sort_keys=True)
    assert json.loads(text) == record
    (root / "metadata.json").write_text(text)
    # Independent two-way/string-ID project; the index is deliberately unrelated.
    frame = pd.DataFrame(
        {"id": ["test", "b", "a"], "x": [100.0, 3.0, 1.0], "label": ["A", "B", "A"]},
        index=[88, 22, 11],
    )
    _, partition = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_test",
        memberships={"train": ["a", "b"], "test": ["test"]},
    )
    options: dict[str, Any] = dict(
        pipeline=Pipeline([("scale", StandardScaler())]),
        selected_columns=["x"],
        output_schema=[{"name": "x", "dtype": "float64"}],
    )
    fitted_two, _ = fit_preprocessing(frame, partition_record=partition, **options)
    np.testing.assert_allclose(fitted_two.transform(frame[["x"]]), [[98], [1], [-1]])
    for invalid_scope in ("test", "validation"):
        try:
            fit_preprocessing(
                frame,
                partition_record=partition,
                fit_partition=invalid_scope,
                **options,
            )
        except ValueError as error:
            assert "fit_partition" in str(error)
        else:
            raise AssertionError("Held-out fitting was accepted")
    partition["memberships"] = {"train": ["a", "b"], "test": ["a", "test"]}
    try:
        fit_preprocessing(frame, partition_record=partition, **options)
    except ValueError as error:
        assert "overlap" in str(error)
    else:
        raise AssertionError("Overlapping training rows were accepted")
    module = Path(agentic_ml.preprocessing.__file__).resolve()
    assert module.is_relative_to(Path(sys.prefix).resolve())
    assert Path.cwd() == cwd and not cwd.is_relative_to(root)
    (root / "identity.json").write_text(
        json.dumps(
            {
                "python": sys.version,
                "prefix": sys.prefix,
                "module": str(module),
                "versions": record["versions"],
                "metadata_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "guide_script_sha256": hashlib.sha256(script.encode()).hexdigest(),
                "cwd": str(cwd),
                "project": str(root),
            },
            indent=2,
        )
    )
    print("PASS installed preprocessing", flush=True)


if __name__ == "__main__":
    main()
