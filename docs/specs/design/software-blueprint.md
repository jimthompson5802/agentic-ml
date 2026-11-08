# MVP software blueprint

Active design 0.15. Scope and document approved at Gates 1–3.
This document assigns responsibilities and distinguishes existing contracts from
future work. It does not finalize future schemas or deliver executable behavior.
[Authority](../agentic-ml-harness-design.md) and [criteria](../user-stories.md) govern.

## Existing public contracts

The installed package currently implements the following exports. Preserve names,
request/result fields, schema versions and strict behavior. The original
initialization/planning/approval/validation contract reference remains in the
[0.14 blueprint](software-blueprint-v0.14-reference.md#existing-public-contracts)
and its accepted contract reports; that material describes these existing APIs
without activating its separate future platform catalogue.

| Module | Public exports |
|---|---|
| `agentic_ml.initialization` | `InitOptions`, `InitResult`, `InitializationError`, `initialize_project` |
| `agentic_ml.planning` | `BoundaryResult`, `SearchSelection`, `SearchSpace`, `validate_boundaries`, `Diagnostic`, `PlanningError`, `PlanResult`, `PlanStatus`, `PlanInspection`, `VerificationResult`, `ResolveRequest`, `resolve_plan`, `inspect_plan`, `verify_plan` |
| `agentic_ml.approvals` | `ApprovalError`, `ApprovalRecord`, `ApprovalRequest`, `approve_plan`, `RevocationRequest`, `RevocationRecord`, `revoke_approval` |
| `agentic_ml.validation` | `CandidateRequest`, `CandidateResult`, `ConfigurationRequest`, `ConfigurationResult`, `RegistryDocument`, `RegistryResult`, `ValidationError`, `ValidationInspection`, `validate_candidate`, `validate_configuration`, `validate_registry`, `inspect_validation` |
| `agentic_ml.extraction` | `extract_data` |
| `agentic_ml.data_quality` | `validate_data`, `run_validated_step`, `DataQualityError` |
| `agentic_ml.data_assessment` | `assess_data` |
| `agentic_ml.splitting` | `create_partitions` |

### Initialization and paths

`initialize_project(InitOptions) -> InitResult` initializes draft project files,
locked environment and configured local stores. Explicit root and optional
experiment/package/storage choices are accepted. Results identify created,
updated, unchanged and pending setup items; InitializationError preserves stage,
conflict and recovery diagnostics. Preserve project files, dependency pin and
setup-journal safety. Draft 0.1 inputs are not a runnable experiment definition.
See [accepted initialization contract](../../verification/us-02-ip1.md).

### Strict planning and approvals

`resolve_plan(ResolveRequest) -> PlanResult`, `inspect_plan`, `verify_plan`
and the boundary helper preserve 1.0 plan bundles, root/cwd handling, source
checksums, input readiness and narrowing rules. PlanningError and field/source
diagnostics remain actionable. Inspect/verify use keyword project root/plan ID;
verify can check currentness.

`approve_plan(ApprovalRequest) -> ApprovalRecord` and
`revoke_approval(RevocationRequest) -> RevocationRecord` retain exact-scope
matching, revocation/staleness and ApprovalError behavior. These unauthenticated
delegated-decision records do not establish trusted authorship or general
execution permissions. See [accepted planning contract](../../verification/us-03-ip1.md).

### Semantic validation

`validate_registry`, `validate_configuration`, `validate_candidate` and
`inspect_validation` retain their current signatures, typed requests/results,
diagnostics, defaults and integrity/currentness behavior. Current configuration
requests bind a project root and real plan ID; candidate requests bind a validation
identity, algorithm and parameters. Metadata validation does not load user code,
train, reserve budget or grant authorization.

Built-in metadata currently covers dummy classifier/regressor profiles plus
supplied additive metadata. This does not establish useful real-estimator training
support. See [accepted validation contract](../../verification/us-05-ip1.md).

### Local extraction

`extract_data` accepts a project callback over named pandas DataFrames, explicit
project root/source/code/output paths and plain settings/reader options. It returns
the native output frame and a JSON-compatible provenance dictionary, publishing
`dataset.csv` or `dataset.parquet` together with `extraction.json` to a fresh
destination. Source/code/output identities and timing are recorded; project
pandas code owns selection/filter/join semantics. Extraction completion is not a
quality-passed result. US-11 AC-01–05 were accepted on 2026-11-07 UTC; see the
[implemented contract](../../extraction.md) and
[owning plan](../../plans/milestone-1-us-11.md#story-completion-review).
Actual DVC identity integration remains US-13 work.

### Dataset quality

`agentic_ml.data_quality` exports `validate_data`, `run_validated_step` and
`DataQualityError`. The [quality guide](../../data-quality.md) specifies seven
rule families and JSON reports. `validate_data` reports failures;
`run_validated_step` checks a copied input immediately before a project operation
and raises `DataQualityError` on required-check failure. Advisory failures permit
the operation; empty rules report `not_checked` and also permit it. Reports do not
validate later operations or the callback's output. Gates 1–3 and issue #15
AC-01/05 were accepted on 2026-11-07 UTC. Future runners must integrate this boundary.

### Assessment and partitions

`assess_data(frame, *, target)` returns native pandas summaries, missingness and
classification target balance as a versioned plain dictionary without a quality
judgment. `create_partitions` returns partition DataFrames and a versioned record
for explicit `train_test` or `train_validation_test` layouts, seeded generation
or supplied membership. It records exact row IDs, settings and source identity
using index/attrs-free native Parquet bytes bound to library versions.

Project code owns JSON save/load, saved-document validation and old/current source
comparison. Supplied time/group protocols are declarations; row membership,
coverage and disjointness are checked without certifying chronology or group
separation. Neither helper fits preprocessing or models. Gates 1–4 are approved;
issue #19 AC-02/03 were accepted on 2026-11-08 UTC. See the
[implemented contracts](../../data-assessment-and-splits.md) and
[installed evidence](../../verification/us-12-19-ip4.md).

### CLI and resources

The actual CLI implements `--version`, `init`,
`plan resolve/inspect/verify/approve/revoke-approval`, `config validate/inspect`
and `candidate validate`. No experiment `run`, `train` or `reproduce` command
is implemented. Preserve packaged schemas/registry/template/runtime-resource paths
under `src/agentic_ml/`; no relocation is authorized here.

## Planned MVP responsibilities

These are software responsibilities, not promises of named modules/classes or
complete new interfaces. Owning story plans specify concrete public contracts
and test boundaries before code. Use native library interfaces where possible.

| Capability | Implementation seam | Story owner / observable result |
|---|---|---|
| Runnable basic experiment | Setup/defaults and validated explicit settings compatible with existing APIs | US-39-AC-01/02: separate project runs without manual schema conversion or mandatory formal planning |
| Data integration | Consume accepted extraction, quality, assessment and partition helpers in experiment stages; add real DVC identities | US-13/39: versioned inputs and integrated checks; delivered US-11/12 contracts remain intact |
| Feature/model pipeline | Pandas DataFrames/project feature functions plus native scikit-learn compatible fit/transform/predict and persistence | US-14/15/16/18: train-only fit, validation comparisons and usable fitted artifacts |
| Local experiment/search | Supported project script/API path using native estimator/search behavior | US-10/20: logs/status, validated candidates and maximum trial count |
| Evaluation/reporting | Metric/output checks over recorded pipeline results | US-21/24/26: baseline/validation/final metrics and distinct failure/quality outcomes |
| Tracking | MLflow run/artifact records with project/config/environment/DVC references | US-26: inspectable evidence, no second general run-state store |
| Stages/reproduction | Native DVC pipeline files and operations in project environment | US-13/27/40: cached/reexecuted distinctions, invalidation and checked replay |
| Notebook/assistant usability | Fresh-kernel notebook and externally owned assistant session invoking public paths | US-09/39/40: ASW-01–08 evidence without a managed adapter |

## Decisions required before dependent code

| Decision | Owner and blocking work |
|---|---|
| Basic-path public entrypoint/configuration and validation bridge | US-39-AC-01/02 owning contract review; preserve strict 0.1/1.0 APIs and avoid fabricated plan IDs. Blocks simple-path execution implementation. |
| Supported real scikit-learn estimator/parameter inventory and compatible custom-object persistence | US-05/16/18/20 owning plans; blocks training/tuning coverage claims. |
| Concrete example output checks/tolerances and reproducible fitted-state format | US-15/21/27/39/40 owning plans; blocks executable acceptance/reproduction claims. |

These are bounded story implementation decisions. The scope revision neither
needs a fully specified future type catalogue nor accepts every pending ADR.
Development approval/test-boundary gates remain in force.

## Historical platform contracts

The [complete reviewed 0.14 catalogue](software-blueprint-v0.14-reference.md)
preserves prior typed records, protocol replacements, diagrams and blockers.
Its future classes/schemas are not current MVP prerequisites. ExperimentRunner
narrows to local execution responsibilities; DataSourceAdapter to local files;
ModelAdapter/FeatureEngineeringAdapter to native compatible objects; Evaluator
to supported output/metric checks. Managed AgentAdapter, ApprovalService,
DataAcquisitionPlanner/Executor and later WorkflowStore remain deferred.
Existing approval functions remain implemented; deferring a general ApprovalService
does not remove their accepted contract.

The previous 160-criterion coverage index is historical design evidence. Current
[traceability](acceptance-traceability.md) covers all 228 local criteria, including
the six planned M50 US-41 distribution-initialization criteria ([issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64)), and
explicitly labels accepted, planned and roadmap outcomes.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](software-blueprint-v0.14-reference.md).

<a id="ownership-and-criterion-map-1"></a>

<a id="ownership-and-criterion-map-2"></a>

<a id="software-implementation-blueprint"></a>

<a id="authority-and-notation"></a>

<a id="milestone-1-ownership-and-criterion-map"></a>

<a id="bootstrap-and-initialization"></a>

<a id="planning-and-decision-approvals"></a>

<a id="proposed-execution-and-evidence-contracts"></a>

<a id="experimentspec-proposed-immutable-execution-description"></a>

<a id="enforcement-decision-required-before-execution"></a>

<a id="proposed-data-contracts"></a>

<a id="m1-record-catalogue"></a>

<a id="implemented-initialization-records"></a>

<a id="implemented-planning-and-approval-records"></a>

<a id="implemented-semantic-validation-records"></a>

<a id="proposed-common-record-rules"></a>

<a id="proposed-authorization-and-accounting-records"></a>

<a id="proposed-capture-and-run-records"></a>

<a id="proposed-source-dataset-and-approval-records"></a>

<a id="proposed-restoration-records"></a>

<a id="error-classes-and-future-name-reconciliation"></a>

<a id="m1-verification-summary"></a>

<a id="milestone-2-assessment-features-and-pipeline-reuse"></a>

<a id="criterion-ownership-and-public-boundaries"></a>

<a id="assessment-and-split-records"></a>

<a id="component-registration-and-preprocessing-protocols"></a>

<a id="ordered-feature-plans-execution-and-reference-comparison"></a>

<a id="pipeline-stage-and-reuse-records"></a>

<a id="lifecycle-failures-and-enforcement"></a>

<a id="fit-transform-restore-and-comparison-flow"></a>

<a id="m2-verification-scenarios-and-completion-boundary"></a>

<a id="milestone-3-training-tuning-and-independent-evaluation"></a>

<a id="ownership-and-criterion-map"></a>

<a id="model-registration-and-algorithm-selection"></a>

<a id="training-models-predictions-and-checkpoints"></a>

<a id="baselines-and-bounded-tuning"></a>

<a id="independent-evaluation-and-final-decisions"></a>

<a id="reporting-and-public-verification"></a>

<a id="milestone-4-bounded-agent-integration"></a>

<a id="runtime-guidance-selection-and-preservation"></a>

<a id="adapter-capabilities-tasks-and-results"></a>

<a id="delegated-proposals-and-controlled-file-changes"></a>

<a id="interactive-kernels-and-bounded-development-iteration"></a>

<a id="errors-unresolved-integration-mechanisms-and-verification"></a>

<a id="milestone-5-supervised-workflow-and-durable-recovery"></a>

<a id="ownership-and-criterion-coverage"></a>

<a id="workflow-planning-and-state-records"></a>

<a id="scoped-workflow-decisions"></a>

<a id="durable-store-ownership-and-reconciliation"></a>

<a id="two-adapters-under-one-contract"></a>

<a id="audit-and-retry-safe-tracking-publication"></a>

<a id="recovery-and-gate-verification-flow"></a>

<a id="milestone-6-authorized-acquisition-and-measured-improvement"></a>

<a id="evidence-and-proposal-records"></a>

<a id="acquisition-authorization-execution-and-lineage"></a>

<a id="consistent-evaluation-stopping-and-recovery"></a>

<a id="final-m16-reconciliation"></a>

<a id="original-nine-protocol-dispositions"></a>

<a id="open-decision-and-assurance-register"></a>
