# Experiment tracking contract

Status: proposed US-26 M1 contract for Gate 1 review; these toolkit helpers are
not implemented. [Plan](plans/milestone-1-us-26-recording.md),
[native findings](verification/us-26-recording-ip1.md) and the
[shared field/type specification](plans/milestone-1-us-15-us-26-execution-order.md#proposed-handoff-types)
define the review boundary. Issue #17 owns AC-01–05. Native probes do not verify
those criteria through toolkit interfaces.

US-26 explicitly concurs with revision **US-15-US-26-SC-01**;
[renewed consumer evidence](verification/us26-sc01-concurrence.md) confirms
full effective-setting parity and native persistence. Both Gate 1 decisions
remain pending.

## Public calls and ownership

```python
from agentic_ml.tracking import log_preprocessing, log_run_results

artifacts = log_preprocessing(
    run_id=run_id, pipeline=fitted_pipeline, record=preprocessing_record,
    provenance=experiment_provenance, project_root=project_root,
    tracking_uri=tracking_uri, artifact_path="preprocessing",
)
result = log_run_results(
    run_id=run_id, project_root=project_root, tracking_uri=tracking_uri,
    provenance=experiment_provenance, parameters={"C": 1},
    metrics={"validation_accuracy": 0.75},
    outputs={"predictions": predictions_path, "stdout": stdout_path},
    expected_outputs=["predictions"], process_exit_code=0,
    validation_passed=True, executed_notebook=None,
)
```

This is a future script outline, not an executable example of existing exports.
Project execution creates the native MLflow run with an explicitly configured
MlflowClient, fits preprocessing, computes metrics, writes outputs and prepares
provenance once. Both calls use the same existing run ID and identical provenance.
No ambient active run, cwd inference, new run store or implicit run creation.
The [index's exact signatures and return fields](plans/milestone-1-us-15-us-26-execution-order.md#proposed-public-boundaries)
are authoritative proposals; returns are ordinary dictionaries.

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
[complete metadata/native-save evidence](../../US-15-preprocessing/docs/verification/us15-us26-contract-revision.md). Producer ownership and native reuse are described in
[US-15's proposed contract](../../US-15-preprocessing/docs/preprocessing.md).
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
still reviews the complete feasibility evidence and public boundaries;
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
Native logging failure alone does not change a run's RUNNING status.

Use TypeError/ValueError for invalid types/values, FileNotFoundError for missing
required references and FileExistsError for artifact conflicts. Preserve native
serialization/storage exception types and chained causes, adding run/stage and
available artifact context. If artifact storage itself fails, retain local
available diagnostics and report their location; do not claim remote retention.
Native MLflow does not enforce all toolkit preconditions: later behavior tests
must verify rejection of incompatible/finalized runs and output/path conflicts.

An executed notebook is supplied by project code. Validate its nbformat structure,
retain exact bytes including outputs/error cells and link committed source in
experiment.code. Future tests create it with native nbclient in a fresh kernel;
this helper does not implement a notebook runner.

## Verification boundary

Before product tests, Gate 1 confirms the plan's public case matrix. Invoke
public helpers and independently inspect MlflowClient records/downloaded bytes,
Git blobs, native DVC hashes/members, lock and installed origins. Check explicit
store/cwd behavior, missing/dirty/mismatched references, invalid metadata,
serialization/storage failures, expected outputs and notebook success/errors.
A supported built-in fitted pipeline with an extra unserializable fitted-state
attribute is the proposed serialization failure fixture; its effective parameters
remain supported so the failure reaches native serialization.

IP2/IP3 use an independently fitted fixture. IP4 alone owns actual installed
US-15-to-US-26 handoff on direct and sdist-rebuilt wheel paths. M2 restored
transformation/replay, reports/comparisons, reverse lookup and assistant workflow
acceptance retain their separate owners. No executable acceptance is claimed here.
