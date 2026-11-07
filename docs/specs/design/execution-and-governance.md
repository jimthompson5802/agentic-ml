# Execution, Tracking, Evaluation and Reproduction

Active design 0.15; [authority](../agentic-ml-harness-design.md).
Current executable package does not yet deliver this experiment workflow.
See [existing versus proposed APIs](software-blueprint.md).

## Local execution and limits

Execute project-owned Python in the selected project's locked environment with
explicit root/cwd and validated settings. Expose available logs, final completion/
failure status and artifact locations. Retain completed-trial results and
diagnostics when finalization is possible. M2 saved notebooks execute from a fresh
kernel in cell order with explicit inputs, saved outputs/errors and artifact
references rather than hidden notebook-to-notebook state.

Validate candidates before fitting through supported script/API/notebook paths.
Enforce the configured maximum trial count and declared search bounds; fixed and
default parameters do not become tunable. Record trial count and elapsed time.
Do not infer hard wall-clock/memory/GPU/cost limits or resource enforcement.
A local process is not a durable submission/status/recovery service. Forced-kill
artifact preservation, idempotent recovery, async cancellation and budget
reconciliation are deferred. Preserve available diagnostics without promising
evidence that was never written.

## Tracking and storage ownership

| Store | MVP contents and responsibility |
|---|---|
| MLflow | Status, effective parameters, metrics, fitted model/pipeline, available outputs/logs and configuration/code/data/environment references |
| DVC | Versioned source/derived data and split records, native stages, dependency/parameter/output hashes and cache |
| Git | Committed source/notebooks/configuration, dependency lock, DVC metadata/stage definitions and nonsecret references |
| Toolkit | Setup/validation, common experiment/evaluation helpers, result links and actionable diagnostics |

Local MLflow SQLite/artifact and DVC storage defaults already initialize under
US-02. This does not imply run logging or pipeline execution exists. Existing
setup journals/state files remain setup evidence; do not require a new workflow
database or second general run-ID/manifest lifecycle for MVP delivery.

Link results to their MLflow run, DVC data state, committed experiment revision,
effective settings, toolkit repository/full SHA/version and lock/environment
identity. Record build identity where available. Save the selected fitted pipeline.
Comprehensive immutable source/guidance/approval bundles and automatic dirty/
untracked helper capture are deferred. Unsaved/uncommitted work is not promised
as reproducible committed-project evidence.

## Evaluation and final testing

Supported checks assess process status, required output artifacts, split
disjointness, training-only fitting, compatible prediction outputs, consistent
metrics/direction and baseline comparisons. Compute these from records/outputs,
not assistant narrative. Distinguish execution failure, configured validation
failure and insufficient quality. Comprehensive scientific-validity certification,
stress/slice robustness requirements and protected evaluator infrastructure are deferred.

Fit baseline/candidates on training data; select with validation results. The
scientist may direct a feature/parameter revision before final testing. Once a
model is selected, evaluate the separate test partition and save its metrics/model.
The supported workflow does not automatically retune from final-test feedback.
User/assistant file access is trusted; OS-enforced holdout denial is not claimed.
There is no mandatory final-model approval gate. Toolkit development gates and
explicit acceptance remain separate and unchanged.

## Native DVC pipeline and reproduction

Declare extraction/preparation/training/evaluation stages with dependencies,
parameters, output paths and explicit working directories in native DVC files.
Keep `dvc.yaml`/`dvc.lock` metadata in Git and dataset content in configured DVC
storage. Let DVC execute/cache stages; the toolkit does not reimplement a
general dependency scheduler or cache admission service.

M1 supplies real stage execution for classification. M2 starts with a fresh
committed experiment checkout, its full-SHA toolkit dependency and lockfile,
restores available DVC content and runs declared stages. Verify required input
identities; fail on missing code/dependencies/data or corrupt content without
silent substitution. Current data access/credentials must be supplied by the user,
not embedded in evidence.

Demonstrate unchanged-stage reuse and invalidation after changing a declared
data/code/parameter dependency. Distinguish cached outputs from newly executed
training; retain traceable original result/data/code references. Actual reruns
record their MLflow results and comparison references. Cache reuse alone does
not prove evaluation success or authorize a claim that training reran.

Declare output checks/metric tolerances in the owning plan and compare reproduced
outputs, restored fitted transforms and predictions against them. Byte equality
is not required when declared numerical tolerances apply. No complete automatic
second-machine migration or dirty-source replay guarantee is made.

## Assistant evidence and development gates

US-39/40 require a scientist-owned external assistant session to prepare, invoke,
inspect and revise the experiment and reproduce it through DVC. Record one
concrete product/interface/version, prompts, consequential edits/actions,
commands/outcomes and verified MLflow/DVC references. No full transcript,
managed adapter, assistant usage accounting or multiple-product certification is required.
The [walkthrough](../example-walkthrough.md) maps each scenario to criteria.

User experiment phase approvals are optional explicit-path capability; existing
strict planning/approval APIs retain readiness/staleness/revocation checks and
unauthenticated-record limitations. They do not authenticate workspace writers.
Development phase approvals, test-boundary review, TDD, story/milestone acceptance
and publication permission continue to follow repository policy.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/execution-and-governance.md).

<a id="execution-and-governance"></a>

<a id="9-execution-evaluation-and-governance"></a>

<a id="execution"></a>

<a id="execution-backend-evolution"></a>

<a id="experiment-tracking-data-versioning-and-pipelines"></a>

<a id="run-evidence-capture-and-restoration"></a>

<a id="notebook-development-and-execution-contract"></a>

<a id="independent-evaluation"></a>

<a id="workflow-states"></a>

<a id="recovery-and-reconciliation"></a>

<a id="agent-cancellation-usage-and-resumption"></a>

<a id="governance"></a>

<a id="notebook-editor-setup"></a>
