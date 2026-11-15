# Experiment tracking contract

Status: log_run_results and log_preprocessing are implemented. Gates 1–3
are approved; Phase 4 installed integration is technically complete, with Gate 4
approved; #17 AC-01–05 recording scope was explicitly accepted on 2026-11-15. [Plan](plans/milestone-1-us-26-recording.md),
[native findings](verification/us-26-recording-ip1.md) and the
[shared field/type specification](plans/milestone-1-us-15-us-26-execution-order.md#proposed-handoff-types)
define the review boundary. Issue #17 owns AC-01–05. Native probes do not verify
those criteria through toolkit interfaces.

US-26 explicitly concurs with revision **US-15-US-26-SC-01**;
[renewed consumer evidence](verification/us26-sc01-concurrence.md) confirms
full effective-setting parity and native persistence. Both Gate 1 decisions
were approved by the developer; later phase gates remain separate.

## Public calls and ownership

```python
from agentic_ml.tracking import log_preprocessing, log_run_results

artifacts = log_preprocessing(
    run_id=run_id,
    pipeline=fitted_pipeline,
    record=preprocessing_record,
    provenance=experiment_provenance,
    project_root=project_root,
    tracking_uri=tracking_uri,
    artifact_path="preprocessing",
)
result = log_run_results(
    run_id=run_id,
    project_root=project_root,
    tracking_uri=tracking_uri,
    provenance=experiment_provenance,
    parameters={"C": 1},
    metrics={"validation_accuracy": 0.75},
    outputs={"predictions": predictions_path, "stdout": stdout_path},
    expected_outputs=["predictions"],
    process_exit_code=0,
    validation_passed=True,
    executed_notebook=None,
)
```

Both calls are implemented. The experiment project supplies the existing native
run and complete provenance.
Project execution creates the native MLflow run with an explicitly configured
MlflowClient, fits preprocessing, computes metrics, writes outputs and prepares
provenance once. Both calls use the same existing run ID and identical provenance.
No ambient active run, cwd inference, new run store or implicit run creation.
The [index's exact signatures and return fields](plans/milestone-1-us-15-us-26-execution-order.md#proposed-public-boundaries)
define the implemented boundaries; returns are ordinary dictionaries.

Resolve file inputs from an absolute existing project_root. Use project-relative
FileRef paths and independently verified SHA-256 for source/configuration/lock;
compare those files to the declared Git commit. Native .dvc pointers, output hash
algorithm/value and optional directory member are separate DvcRef fields. Inspect
native DVC metadata and consumed bytes; do not turn a Parquet/content SHA into a
DVC identifier. Logging neither restores nor downloads missing project inputs.
The consumed split JSON must equal record.partition_record.

The preprocessing record has exactly schema_version, fit_partition,
partition_record, selected_columns, input_schema, output_schema, pipeline and
versions. Retain the producer's effective settings, schema, original memberships,
seed/protocol and source identity. Strict finite JSON and field-specific errors apply. Under accepted SC-01,
validate and preserve exactly {"kind":"missing_value","value":"nan"} only
at built-in SimpleImputer.missing_values, and exactly
{"kind":"numpy_dtype","name":"float64"} for supported dtype descriptors.
The shared index lists allowed canonical dtype names and reserved-map rules.
Reject malformed/extra tag keys or unsupported contexts; do not execute/import
class names to validate metadata. Rejecting literal reserved maps is a producer
encoding rule; consumer validation accepts canonical generated tags in supported
contexts. NaN metrics/provenance and infinities remain
invalid. See the producer's
[complete metadata/native-save evidence](verification/us15-us26-contract-revision.md). Producer ownership and native reuse are described in
[US-15's proposed contract](preprocessing.md).
Metadata is evidence of a declaration; independent train-only numeric tests
remain required to verify fitting scope.

Provenance has exactly schema_version, experiment, configuration, data,
split_record, environment and toolkit, with the nested representations in the
shared specification. Reuse installed Git/full SHA or retained-wheel archive,
lock, origin/version and payload validation. Wheel source/build fields remain
null when unavailable. Do not fabricate them or use this editable checkout as
an installed-project success fixture. Existing initialization identity internals
may be reused without changing initialization's public contract.

## Artifacts and finalization

```text
preprocessing/pipeline/     # native MLflow sklearn model directory
preprocessing/metadata.json
provenance.json
outputs/<name>/<filename>
notebooks/executed.ipynb
```

Save the native pipeline locally through mlflow.sklearn.save_model, then publish
with the explicitly selected client's log_artifacts. This preserves the existing
run artifact layout without adopting MLflow 3's separate logged-model namespace.
Use mlflow.sklearn.load_model for transformation-only pipelines; a predict-based
pyfunc flavor is not required. Native environment/model files supplement the
required project lock provenance; they do not replace it.

MLflow 3.17.2 locally defaults to skops. The composed imputer/scaler/encoder
fixture needs an explicit numpy.dtype trusted type under the locked versions.
Developer accepted the bounded serialization choice through SC-01; Gate 1
approved the complete feasibility evidence and public boundaries;
no automatic fallback to pickle/cloudpickle or broad trust discovery is proposed.

Validate supported metadata, provenance, fitted state and artifact destinations
before publication. Reject conflicts instead of overwriting completed artifacts.
Identical provenance may be reused; different provenance raises FileExistsError.
This does not promise atomic publication or recovery after interruption.

log_preprocessing leaves successful lifecycle finalization to project execution
or log_run_results. The latter requires process exit zero, all expected outputs
and successful recording for native FINISHED. Record validation_status separately
as passed, failed or not_checked; validation failure may accompany a successfully
completed process. Supplied metrics are recorded, not computed or certified.
A nonzero exit, missing output even with zero exit, or recording failure sets
FAILED where possible and raises a contextual exception. Preserve available
stdout/stderr, partial output and notebook bytes before reporting failure.
The native MLflow logger alone does not finalize a failed run; these helpers
explicitly request FAILED when recording fails.

Use TypeError/ValueError for invalid types/values, FileNotFoundError for missing
required references and FileExistsError for artifact conflicts. Preserve native
serialization/storage exception types and chained causes, adding run/stage and
available artifact context. If artifact storage itself fails, retain local
available diagnostics and report their location; do not claim remote retention.
Public tests verify incompatible/finalized runs and output/path conflicts.

An executed notebook is supplied by project code. Validate its nbformat structure,
retain exact bytes including outputs/error cells and link committed source in
experiment.code. Tests create it with native nbclient in a fresh kernel;
this helper does not implement a notebook runner.

## Verification boundary

Gate 1 confirmed the plan's public case matrix before product tests. Invoke
public helpers and independently inspect MlflowClient records/downloaded bytes,
Git blobs, native DVC hashes/members, lock and installed origins. Check explicit
store/cwd behavior, missing/dirty/mismatched references, invalid metadata,
serialization/storage failures, expected outputs and notebook success/errors.
A supported built-in fitted pipeline with an extra unserializable fitted-state
attribute is the proposed serialization failure fixture; its effective parameters
remain supported so the failure reaches native serialization.

IP2/IP3 use an independently fitted fixture. [IP4 evidence](verification/us-26-recording-ip4.md)
now verifies actual installed US-15-to-US-26 handoff on direct and sdist-rebuilt wheel paths. M2 restored
transformation/replay, reports/comparisons, reverse lookup and assistant workflow
acceptance retain their separate owners. No whole-story acceptance is claimed here.

## Implemented results path and verification

[Phase 2 evidence](verification/us-26-recording-ip2.md) covers the public
log_run_results path through separate normally installed wheel and full-SHA Git
projects. The helper validates consumed committed FileRefs, native .dvc output
and member integrity, installed toolkit identity, Python/library versions and
recorded versions in uv.lock. It does not run a process, fit a model, compute a
metric or restore missing data.

Expected output names must be nonempty and unique. Output names contain only
letters, digits, underscores, dots and hyphens, beginning with a letter/digit;
provenance and notebook are reserved artifact-map keys. Sources must be regular
files without symlink components. Relative output paths resolve from project_root;
explicit absolute output paths are accepted. Return artifacts includes provenance,
the named outputs and notebook when supplied. Lists/dictionaries in parameters
use canonical JSON with sorted keys; scalar parameters keep native MLflow
string conversion. Nonfinite parameter/metric values are rejected.

Only active RUNNING runs accept recording. Existing terminal runs remain unchanged;
unknown/incompatible run/store selections retain native exceptions with context.
Unavailable storage cannot be claimed as remote diagnostic retention: inspect
the contextual notes for original local files and failed retention/finalization.
The caller owns output files and supplies an already-executed notebook; the
toolkit records its exact bytes and validates its structure/source reference.
No notebook execution service or atomic artifact publication is provided.

The Phase 2 component tests use one direct wheel and a full-SHA Git fixture.
Actual US-15 preprocessing output and direct/sdist-rebuilt wheel integration
now pass [Phase 4 verification](verification/us-26-recording-ip4.md). Gates 2 and 3 are approved; whole-story and
milestone acceptance remain pending.


## Independent scaler script

Save the following as `record_demo.py` in a normally installed experiment project.
It uses native sklearn directly and needs no US-15 import. Prepare the project's
committed source/configuration/uv.lock and native DVC references first, following
the [dataset recipe](dataset-versioning.md). This small example uses
`data/input.csv` with numeric feature `x`, and its existing `data/split.json`.
Include this script in the committed entrypoint/code references. Then write
`run-provenance.json` using the exact [shared schema](plans/milestone-1-us-15-us-26-execution-order.md#shared-experiment-provenance-10),
with FileRef checksums and native DVC dataset/split references from that project.
Provenance is supplied project evidence, rather than invented automatically.

Create a native MLflow run using an explicit MlflowClient and retain its run ID.
From any cwd, invoke the project interpreter with the absolute script/root paths:
`/project/.venv/bin/python -I /project/record_demo.py /project TRACKING_URI RUN_ID`.
The example fits only the saved training membership, records preprocessing,
writes transformed features and finalizes the same existing run. Empty metrics
and unchecked configured validation make no model-quality claim. This is a
recording example, not the full classification workflow or restored-project replay.

<!-- us26-independent-script -->
```python
"""Record an independent scaler in a prepared, committed experiment project."""

import json
import sys
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from agentic_ml.tracking import log_preprocessing, log_run_results

root = Path(sys.argv[1])
tracking_uri, run_id = sys.argv[2:4]
provenance = json.loads((root / "run-provenance.json").read_text())
partition = json.loads((root / "data/split.json").read_text())
frame = pd.read_csv(root / "data/input.csv")
selected = ["x"]
train = frame.set_index(partition["row_id"]).loc[
    partition["memberships"]["train"], selected
]
pipeline = Pipeline([("scale", StandardScaler())]).fit(train)
transformed = pd.DataFrame(pipeline.transform(frame[selected]), columns=selected)
settings = pipeline.get_params(deep=False)
settings["steps"] = [
    [
        name,
        {
            "class_name": f"{type(step).__module__}.{type(step).__qualname__}",
            "parameters": step.get_params(deep=False),
        },
    ]
    for name, step in pipeline.steps
]
record = {
    "schema_version": "1.0",
    "fit_partition": "train",
    "partition_record": partition,
    "selected_columns": selected,
    "input_schema": [{"name": n, "dtype": str(frame[n].dtype)} for n in selected],
    "output_schema": [
        {"name": n, "dtype": str(transformed[n].dtype)} for n in selected
    ],
    "pipeline": {"class_name": "sklearn.pipeline.Pipeline", "parameters": settings},
    "versions": {
        n: version(n) for n in ("agentic-ml", "pandas", "pyarrow", "scikit-learn")
    },
}
log_preprocessing(
    run_id=run_id,
    pipeline=pipeline,
    record=record,
    provenance=provenance,
    project_root=root,
    tracking_uri=tracking_uri,
)
transformed.to_csv(root / "features.csv", index=False)
result = log_run_results(
    run_id=run_id,
    project_root=root,
    tracking_uri=tracking_uri,
    provenance=provenance,
    parameters={"preprocessing": "StandardScaler"},
    metrics={},
    outputs={"features": Path("features.csv")},
    expected_outputs=["features"],
    process_exit_code=0,
    validation_passed=None,
)
print(json.dumps(result, allow_nan=False))
```

Native missing-value/dtype encoding is unnecessary for this scaler's scalar
settings. For imputer/encoder compositions, use the exact SC-01 tags; arbitrary
objects/callables, nonfinite values and literal reserved native maps are rejected.
The consumer compares every effective native setting, validates fitted state,
saved split equality/disjoint membership, schemas, versions and committed/native
references. Output names remain project declarations. Output dtypes and training
scope still need the producer's independent transform tests; metadata alone does
not prove them. Successful preprocessing leaves RUNNING; log_run_results finishes
only after required outputs are recorded. On recording failure, inspect exception
notes for stage/run/root and an available local diagnostics directory. Successful
local staging directories are removed; failed ones remain for inspection. A
storage failure cannot guarantee remote retention. No broader skops trust or
pickle fallback is used.

[Phase 3 evidence](verification/us-26-recording-ip3.md) records 241 passing
tracking/splitting tests and shared checks. Gate 3 is approved. Actual
US-15 producer preservation and both installed wheel paths now pass Phase 4 verification;
Gate 4 is approved; #17 AC-01–05 recording scope was explicitly accepted on 2026-11-15.


## Actual producer script

Save this as `track.py` in a normally installed experiment project. Prepare and
commit `data/input.csv`, its existing `data/split.json`, configuration, source
notebook and `uv.lock`; version the consumed data directory with native DVC.
The five-row example is the same imputer/scaler/encoder fixture in the
[preprocessing guide](preprocessing.md). Supply `run-provenance.json` using the
shared schema and an existing native run, then invoke:
`/project/.venv/bin/python -I /project/track.py /project TRACKING_URI RUN_ID`.
The literal checks belong to this fixed example. Replace them with independently
defined checks for a different project. The supplied metric is illustrative;
the script does not train or evaluate a classifier.

<!-- us26-producer-script -->
```python
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
```

The installed verification runs this exact script on both direct and genuinely
sdist-rebuilt wheels. It also supplies fresh-kernel notebooks, checks recorded
error cells, missing outputs despite process exit zero, and invalid committed
references. The preprocessing declaration and supplied validation result remain
separate from process completion. Native artifact loading checks fitted-state
readability; M2 restored-project transformation/replay remains separately owned.
