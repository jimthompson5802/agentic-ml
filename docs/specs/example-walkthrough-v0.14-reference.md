# Historical design 0.14 reference

**Historical reference only.** Captured from `0404916` before the approved MVP
scope revision. Original contents follow unchanged after the separator. Current
[design](agentic-ml-harness-design.md) and [stories](user-stories.md) govern new work.
Relative links retain their original locations and may resolve to revised documents.
The preserved design content is also identical at `0a7b643`; use that pre-revision
commit for historical story/design context, because `0404916` already revises stories.
Previous documentation approvals remain historical facts, not current MVP obligations.

---

# Example scenario: Build a customer churn model

The intended experience is a notebook-centered ML project in the data scientist's own repository. A coding assistant helps write and improve the experiment. The toolkit controls execution, tracking, independent evaluation, and approvals.

This walkthrough follows the [user stories](user-stories.md) and [toolkit design](agentic-ml-harness-design.md). Initialization, planning, plan approvals, and semantic configuration validation are implemented; the complete experience remains a design spanning Milestones 1–6. The [software blueprint](design/software-blueprint.md) distinguishes implemented APIs from proposed contracts and owns their detailed fields and signatures. Function names below describe those contracts; proposed APIs are not executable usage examples.

## How to read the sample prompts

**Blockquotes beginning with `>` are sample natural-language prompts that the data scientist types into a coding assistant**, such as Codex, Claude Code, or GitHub Copilot, with the experiment repository open. They are not terminal commands or defined `agentic-ml` syntax.

The assistant reads the project's brief and configuration, creates or revises notebooks and supporting code, and invokes the public toolkit CLI/API where available. No agent adapter is required for this interactive use.

A prompt asking the assistant to present work for approval does not itself grant approval. The scientist must record the actual decision through the applicable toolkit approval mechanism. Existing plan approvals cover delegated decisions; proposed workflow gates cover progression and scope changes. Current approval records use unauthenticated reviewer labels and do not establish protection against fabricated workspace approvals. Assistant proposals do not themselves authorize work.

## 1. Create the experiment project

After installing Git and `uv`, the scientist runs:

```bash
mkdir customer-churn
cd customer-churn

git init
uv init
uv add "git+https://github.com/OWNER/HARNESS-REPO.git" --rev FULL_COMMIT_SHA

uv run agentic-ml init
# Open this project in VS Code and select its .venv notebook kernel.
```

The repository URL and SHA are placeholders. The toolkit is installed as a pinned dependency; the scientist does not maintain a separate toolkit checkout.

Initialization creates configuration, notebook templates, project-package scaffolding, and local defaults for DVC, MLflow, and workflow state. An illustrative project includes:

```text
customer-churn/
├── project.yaml
├── pyproject.toml
├── uv.lock
├── src/churn_experiments/
└── experiments/baseline-comparison/
    ├── experiment.md
    ├── search-space.yaml
    ├── experiment.yaml
    └── notebooks/
        ├── 01_data_assessment.ipynb
        ├── 02_features_and_baseline.ipynb
        ├── 03_model_development.ipynb
        └── 04_results.ipynb
```

Experiment and package names are user-selected. Initialization does not authorize data access or execution. Data permissions, credentials, storage settings, and approval presentation require explicit setup; credentials remain outside committed configuration.

**Classes and functions:** `initialize_project(InitOptions) -> InitResult` performs preflight checks and creates the selected project scaffold. `InitOptions` makes the project root, names, and storage choices explicit; `InitResult` identifies created, unchanged, updated, and pending items. `InitializationError` preserves conflicts, completed steps, and recovery information so a rerun can proceed safely.

## 2. Describe the prediction problem and boundaries

The scientist writes—or asks the assistant to draft—these inputs:

| File | What the scientist specifies |
|---|---|
| `experiment.md` | Data, target, prediction task, feature restrictions, metric, split constraints, algorithm mode, and budgets |
| `search-space.yaml` | Allowed algorithms, fixed parameters, and permitted tuning ranges |
| `experiment.yaml` | Notebook/code entrypoints, data references, feature pipeline, and execution settings |
| `project.yaml` | Project-wide storage, tracking, agent settings, and custom component declarations |

Sample coding-assistant prompt:

> Prepare a churn classification experiment using our customer dataset. Predict `churned`, exclude `customer_id` and any information unavailable at prediction time, and respect customer grouping and temporal boundaries. Propose an appropriate metric for the imbalanced target. Compare logistic regression and random forest. Limit optimization to 20 trials per algorithm and 60 minutes total. Draft the brief and configurations, explain unresolved decisions, and present the resolved plan for my approval.

For example, part of the proposed search space could be:

```yaml
schema_version: "0.1"
algorithms:
  logistic_regression:
    fixed:
      max_iter: 2000
    search:
      C:
        type: float
        min: 0.0001
        max: 100
        scale: logarithmic
      class_weight:
        type: categorical
        choices: [null, balanced]
```

This excerpt covers one algorithm; the complete configuration would also declare the approved random forest search space. The YAML is a hard boundary: the assistant cannot introduce another algorithm or extend a parameter range during the experiment. Omitted parameters use recorded registry defaults and do not become tunable.

The toolkit validates and records the effective, versioned plan. The scientist resolves ambiguities and approves delegated choices, access scope, evaluation protocol, and budgets before dependent execution. Plan-decision approval and execution authorization are separate contracts.

**Classes and functions:** `resolve_plan(ResolveRequest)` preserves supplied inputs and produces a `PlanResult`; `inspect_plan()` and `verify_plan()` expose its contents, integrity, and currentness. `approve_plan()` and `revoke_approval()` record decisions about delegated choices. `validate_registry()`, `validate_configuration(ConfigurationRequest)`, and `validate_candidate(CandidateRequest)` check declarations, the resolved configuration, and individual parameter selections; `inspect_validation()` retrieves their evidence. Proposed `authorize()` checks access and operation scope, while `reserve()` allocates resource capacity. Proposed `WorkflowScope`, `request_gate()`, and `decide_gate()` bind later workflow decisions to exact evidence and permitted changes.

## 3. Assess the data and approve the splits

**Notebook:** `01_data_assessment.ipynb`

Sample coding-assistant prompt:

> Prepare the data-assessment notebook. Use the authorized source to create a versioned snapshot. Report missing values, distributions, target balance, anomalies, and possible leakage. Propose reproducible training, validation, and protected-test splits that respect the approved time and customer-group constraints. Present the assessment and split protocol for review.

The scientist opens the notebook in VS Code, reads its explanations, and can execute cells for exploration.

For an accepted, recorded result, the saved notebook must undergo toolkit-managed execution: a fresh kernel, ordered cells, explicit inputs, a locked environment, a recorded working directory, and a frozen source snapshot. Interactive execution alone does not establish acceptance.

The scientist reviews the assessment and approves the split protocol before dependent feature or modeling work. Protected-test data remains inaccessible to exploratory notebooks and the assistant.

**Proposed classes and functions:** `DataSourceAdapter.discover()`, `.extract()`, and `.validate()` support approved source access. `validate_dataset()`, `version_dataset()`, and `approve_dataset()` establish quality evidence, a content-addressed `DatasetRef`, and separate dataset acceptance. `assess_dataset()` returns a `DatasetAssessment`; `create_split()` preserves exact memberships in a `SplitManifest`; `approve_assessment()` records approval of matching assessment and split evidence. Managed notebook execution uses `capture_inputs()`, `prepare_experiment_spec()`, and `LocalExperimentRunner.submit()` to run frozen inputs. `start_kernel()` and `stop_kernel()` manage exploratory sessions separately from accepted execution.

## 4. Develop features and establish a baseline

**Notebook:** `02_features_and_baseline.ipynb`

This notebook supports two separate workflow phases, with an approval boundary between them. Its filename does not authorize executing both workflow phases together.

First, feature engineering:

> Build a reproducible preprocessing pipeline with imputation, categorical encoding, and scaling where appropriate. Fit all learned transformations on training data only. Compare the proposed features against the approved baseline feature set using the fixed reference estimator, settings, and validation metric. Show gains, ties, or regressions and preserve pipeline artifacts and lineage.

The baseline feature set, fixed reference estimator and settings, and validation metric require approval before this comparison. The scientist reviews the comparison evidence and approves the feature pipeline before proceeding to baseline modeling.

Then, baseline modeling:

> Using the approved features and split protocol, train the agreed simple baselines. Record their parameters, validation metrics, and artifacts. Present the baseline results for approval before candidate-model comparisons.

If the scientist already has preprocessing or model code, the assistant can register and invoke the project-local implementation. Supplied components are immutable by default; changing them requires authorization and a new versioned experiment configuration.

**Proposed classes and functions:** `register_components()` validates `ComponentSpec` declarations. An ordered `FeaturePlan` selects transformations; `execute_features()` fits `StatefulPreprocessor` instances on training data only and applies their `transform()` methods alongside `StatelessTransformation` steps. `approve_feature_comparison()` binds candidate plans to a fixed protocol; `compare_features()` uses a `ReferenceEstimator` and returns a `FeatureEvaluationReport`. `register_models()`, `select_algorithms()`, and `train_model()` establish baseline models; `evaluate_model()` supplies independent development evidence before `approve_baseline()`. `approve_component_change()` permits only exact reviewed code changes.

## 5. Compare models, then tune candidates

**Notebook:** `03_model_development.ipynb`

Sample model-development prompt:

> Compare the approved logistic regression and random forest candidates against the accepted baseline. Use only the declared algorithms and parameters. Diagnose errors using development data, record each candidate through the toolkit, and summarize the evidence at the model-development approval gate.

After reviewing the evidence and approving progression to optimization, the scientist could prompt:

> Tune the approved candidates within `search-space.yaml` and the remaining trial and runtime budgets. Preserve fixed parameters. Stop when the budget is exhausted or the approved stopping condition is met. Present the optimization summary and recommended model for final evaluation.

The assistant can revise and rerun work within the currently approved workflow phase without approval for every trial. Moving to another workflow phase, expanding the search space, or changing permissions requires authorization.

Training cells submit through toolkit APIs so candidate validation, budgets, tracking, and approvals apply. The blueprint proposes the API contracts below; this walkthrough does not prescribe executable training/tuning CLI syntax.

Notebook-to-notebook dependencies use recorded, versioned artifact references rather than variables retained in another notebook's kernel.

**Proposed classes and functions:** `ModelAdapter.train()`, `.predict()`, `.save()`, and `.load()` provide a common framework boundary, implemented by `SklearnModelAdapter`, `LightGBMModelAdapter`, and `PyTorchModelAdapter`. `TrainingRequest` binds validated parameters, feature identities, compute, authorization, and reservation; `train_model()` returns a `TrainingResult` with fitted artifacts and available checkpoints. `tune_models(TuningRequest)` evaluates a finite candidate order and returns an `OptimizationSummary`. Managed assistance uses `AgentAdapter`, `record_proposals()`, and `apply_revision()`; `prepare_feedback()` and `improve_experiment()` implement bounded development iteration under `IterationPolicy`. `cancel_iteration()` records task and child-run cancellation separately.

## 6. Authorize independent final evaluation

**Notebook:** `04_results.ipynb` presents results and the final report.

Sample coding-assistant prompt:

> Prepare the selected model and its recorded preprocessing pipeline for independent final evaluation. Summarize the development results, reproducibility evidence, limitations, and required holdout checks. Present the candidate for my authorization.

Once authorized, the independent evaluator accesses the protected holdout. The results notebook presents its recorded findings; ordinary notebook code does not gain holdout access.

The scientist approves or rejects the final model after reviewing the independent assessment. Holdout results cannot feed another tuning, feature-improvement, or data-acquisition loop. Further development after unsuccessful final evaluation requires a separately approved evaluation protocol that preserves holdout protection.

The resulting evidence includes the selected model and preprocessing artifacts, evaluation results, and reproducibility records. Production deployment is outside this walkthrough.

**Proposed classes and functions:** `AcceptanceCriteria` freezes metrics, thresholds, robustness checks, and reproduction tolerances. `authorize_final_evaluation()` selects one frozen model; `evaluate_final()` accesses protected inputs inside the evaluator boundary and produces an `EvaluationReport`. That report distinguishes execution, scientific validity, and model quality. `decide_model()` records the separate `ModelDecision`; passing evaluation alone does not accept the model.

## 7. Inspect, reproduce, or resume work

The scientist inspects readable notebooks alongside MLflow records containing metrics, parameters, model artifacts, logs, and executed notebook snapshots. DVC versions datasets and pipeline outputs. Toolkit manifests connect those records to source, configuration, environment, approvals, and data lineage.

A reproduction request to the coding assistant could be:

> Restore recorded run `<run-id>` in a clean environment, verify its source and data checksums, execute its captured entrypoint, and compare the outputs against the recorded tolerances. Report missing inputs explicitly.

Restoration uses captured source—including required uncommitted changes—and the original locked environment. Storage must be accessible, and current access and execution authorization still apply. The blueprint proposes restoration APIs; exact restoration CLI commands remain undecided.

With managed orchestration, a resume request could be:

> Resume this experiment from its durable state. Reconcile existing runs before submitting work, preserve consumed budgets, and stop at the next developer approval gate.

Completed work with sufficient verified evidence is reused; active work is reattached. Uncertain execution status requires review rather than automatic duplicate submission. Durable toolkit state, rather than assistant conversation memory, determines where work resumes.

**Proposed classes and functions:** `inspect_run()` retrieves connected run evidence; runner `status()`, `logs()`, and `artifacts()` expose execution details. `restore_run()` and `reproduce_run()` restore captured inputs and compare a new run against recorded checks. `restore_dataset()`, `restore_preprocessing()`, `restore_model()`, and `restore_checkpoint()` verify individual persisted assets; `reproduce_stage()` verifies pipeline reuse. `WorkflowOrchestrator.inspect()` and `.recover()` reconcile durable `WorkflowState` through `WorkflowStore` and its proposed `SQLiteWorkflowStore` implementation. `tracking.audit.lookup()` connects workflow, run, and MLflow records; `finalize_publication()` reconciles incomplete tracking writes without blind duplication.

## Interactive and managed operation

| Interaction mode | Scientist's experience |
|---|---|
| Interactive assistant | Prompt an external coding assistant, review its edits, and have it invoke the public toolkit CLI/API. No agent adapter is required. The toolkit does not own the assistant session. |
| Managed agent | Configure a verified adapter, approve bounded work, and let the orchestrator delegate revisions and execution until a gate or stopping condition. |

Both modes use the same experiment evidence, boundaries, budgets, and approval controls. Reviewing every notebook edit is optional unless configured as an additional gate; workflow phase approvals remain mandatory.

The notebooks are the scientist's working interface. The toolkit supplies reproducible execution and independent evidence for assessing the resulting model.

## Delivery expectations

The complete scenario spans cumulative milestones in the user stories:

| Milestone | Capability used in this scenario |
|---|---|
| 1 | Initialize a separate project, validate and record supplied inputs, extract/version data, execute saved notebooks, inspect records, and reproduce runs without an agent dependency |
| 2 | Assess data, approve splits, build reproducible feature pipelines, and compare features using a fixed approved reference estimator |
| 3 | Compare and tune models, persist model artifacts, and obtain authorized independent final evaluation |
| 4 | Use a verified managed agent integration for notebook generation and bounded improvement within an approved workflow phase |
| 5 | Supervise and resume the durable workflow across workflow phases |
| 6 | Authorize additional data acquisition when development evidence identifies a data limitation |

An external coding assistant can help prepare project inputs and invoke available public interfaces before managed agent support arrives. If development evidence suggests acquiring more data, the scientist must authorize its source, strategy, and limits, along with a return to the affected workflow phases. Protected-test feedback cannot drive that acquisition.


## Class and function reference

This reference covers the public software contracts and supporting records in the
[software blueprint](design/software-blueprint.md), rather than every private
helper in the source tree. Initialization, planning, plan approvals, and semantic
validation are implemented. Other capabilities below are proposed contracts;
document approval is not executable acceptance. The blueprint owns exact fields,
defaults, signatures, and verification obligations.

### How the objects work together

Request records make project roots, input identities, scope, and destinations
explicit. Services validate those requests and perform controlled operations.
Result records preserve outcomes, diagnostics, and evidence. Protocols define
interchangeable implementations. Records generally have no behavioral methods;
constructing a record does not authorize or execute work. Proposed persisted
records are schema-versioned and preserve immutable identities and nested values.

### Functions by responsibility

Names are Python interface references, not executable CLI examples.

| Functions | Responsibility |
|---|---|
| `initialize_project()` | Preflight the selected project and create scaffolding, preserving conflicts and partial setup information. |
| `resolve_plan()`, `inspect_plan()`, `verify_plan()` | Preserve experiment inputs, expose the resolved plan, and verify integrity and currentness. |
| `validate_boundaries()` | Check declared search and budget boundaries without widening them; return effective boundaries or diagnostics. |
| `approve_plan()`, `revoke_approval()` | Record or revoke exact delegated-decision approval without deleting history. |
| `validate_registry()`, `validate_configuration()`, `validate_candidate()`, `inspect_validation()` | Check registry metadata, resolved configuration, and effective candidate parameters; inspect preserved evidence. |
| `authorize()`, `reserve()` | Check current operation/access scope and durably reserve capacity once per submission key. |
| `capture_inputs()`, `prepare_experiment_spec()` | Freeze required source, data, parameters, environment, guidance, and checks; build a matching execution specification. |
| `check_execution()`, `inspect_run()` | Independently assess execution/output checks and retrieve connected run evidence. |
| `validate_dataset()`, `version_dataset()`, `restore_dataset()`, `approve_dataset()` | Establish dataset quality, publish verified DVC content, restore exact bytes, and record separate acceptance. |
| `restore_run()`, `reproduce_run()` | Restore original captured inputs and execute a new authorized run against original output checks. |
| `assess_dataset()`, `create_split()`, `approve_assessment()` | Produce development findings, preserve constrained partition membership, and approve matching evidence. |
| `register_components()`, `restore_preprocessing()` | Validate component implementations and restore verified fitted preprocessing without retraining. |
| `execute_features()`, `approve_feature_comparison()`, `compare_features()` | Execute ordered training-fitted transformations and compare approved features under a fixed reference protocol. |
| `reproduce_stage()` | Reuse verified pipeline output or execute captured stage inputs under current authorization. |
| `register_models()`, `select_algorithms()` | Validate framework contracts and record an allowed model choice or comparison set. |
| `train_model()`, `restore_model()`, `frameworks.pytorch.restore_checkpoint()` | Train checked candidates, restore fitted artifacts, and restore declared checkpoint state. |
| `approve_baseline()`, `tune_models()` | Approve independently evaluated baseline evidence and execute finite bounded candidate search. |
| `evaluate_model()`, `authorize_final_evaluation()`, `evaluate_final()`, `decide_model()` | Separate development evaluation, protected final authorization/evaluation, and developer acceptance. |
| `tracking.reporting.compare_runs()`, `tracking.reporting.build_final_report()` | Compare compatible run evidence and assemble a report whose acceptance follows the recorded decision. |
| `select_guidance()`, `inspect_bundle()` | Preserve explicitly selected runtime instructions, ownership, versions, checksums, and load order. |
| `record_proposals()`, `approve_component_change()`, `apply_revision()` | Preserve agent proposals, approve exact code changes, and publish checked notebook/code revisions. |
| `start_kernel()`, `stop_kernel()` | Manage explicit exploratory kernel sessions under the project environment and access boundary. |
| `prepare_feedback()`, `improve_experiment()`, `cancel_iteration()` | Use development-only evidence for bounded revision/execution/evaluation cycles and record cancellation outcomes. |
| `request_gate()`, `decide_gate()` | Bind workflow review and decisions to exact state, evidence, and permitted scope. |
| `select_adapter()` | Select a verified integration with required capabilities without silent fallback. |
| `tracking.audit.lookup()`, `tracking.audit.finalize_publication()` | Retrieve connected audit evidence and reconcile tracking publication without blind duplicate creation. |
| `approve_acquisition()`, `cancel_acquisition()` | Approve exact source/strategy/limits and record cancellation without assuming external termination. |
| `compare_acquisition()` | Compare before/after development evidence using a fixed cohort and scoring protocol. |
| `run_acquisition_loop()`, `resume_acquisition_loop()` | Execute scoped proposals, pause at downstream gates, and reconcile preserved progress before continuation. |

### Behavioral classes and protocol methods

| Class or protocol | Methods and behavior |
|---|---|
| `ExperimentSpec` | Immutable execution selection and evidence bindings; no launch, approval, or mutation methods. Preparation derives it from verified evidence. |
| `ExperimentRunner`, `LocalExperimentRunner` | `submit()` admits captured work; `lookup_submission()` reconciles acceptance; `status()` observes progress; `cancel()` reports cancellation certainty; `artifacts()` and proposed `logs()` expose retained evidence. Explicit project root; no process-global project. |
| `DataSourceAdapter` | `discover()` returns permitted metadata; `extract()` performs scoped extraction; `validate()` delegates to shared dataset validation. Local CSV/Parquet, SQL, and object-storage implementations use the same contract. |
| `StatefulPreprocessor` | `fit()` learns from training only; `transform()` preserves fitted state and row alignment; `output_schema()` describes fitted outputs; `save()` and `load()` preserve/restore verified state. |
| `StatelessTransformation` | `transform()` applies an unlearned transformation; `output_schema()` is available before execution. |
| `ReferenceEstimator` | `fit()`, `predict()`, `save()`, and `load()` support a fixed-estimator feature comparison without general algorithm tuning. |
| `ModelAdapter` | `train()`, `predict()`, `save()`, and `load()` operate on verified training contexts and fitted artifacts inside controlled workers. |
| `SklearnModelAdapter`, `LightGBMModelAdapter`, `PyTorchModelAdapter` | Implement the common model contract and preserve actual framework/hardware identities; PyTorch additionally implements checkpoint restoration. |
| `CheckpointRestorer` | `restore_checkpoint()` verifies and restores declared state; usable state does not by itself promise exact training continuation. |
| `AgentAdapter`, `FirstManagedAgentAdapter`, `SecondManagedAgentAdapter` | `capabilities()` declares verified support; `submit()` binds an attempt; `status()` and `result()` observe it; `cancel()` records task cancellation separately from experiment runs. Concrete products/versions remain selection decisions. |
| `WorkflowOrchestrator` | `start()` creates planned state; `advance()` performs one permitted step; `inspect()` reads state; `cancel()` stops scheduling; `recover()` reconciles external work before continuation. |
| `WorkflowStore`, `SQLiteWorkflowStore` | `read()`, `claim_owner()`, `renew_owner()`, and `commit()` provide durable version-checked state and exclusive ownership. The proposed SQLite mechanism targets a single host and local filesystem. |
| `DataAcquisitionPlanner`, `EvidenceBasedAcquisitionPlanner` | `diagnose()` derives data gaps from development evidence; `propose()` records an authored strategy, benefit hypothesis, and limits. |
| `DataAcquisitionExecutor`, `ApprovedSourceAcquisitionExecutor` | `execute()` uses approved source connectors, validates/version-controls outputs, and retains lineage, partial results, and cumulative usage. |

### Complete record and alias index

The following inventory names every record/alias in the blueprint's type tables,
including supporting initialization models that are not additional package exports.
Each description summarizes its contract; follow the blueprint for complete fields.
Aliases and notation are identified explicitly rather than presented as classes.

**Implemented initialization records**

| Record or alias | Contract |
|---|---|
| `InitOptions` | None selects documented local defaults; explicit store overrides authorize setup writes only. Package name is validated or derived from the project. |
| `InitResult` | Service-produced inventory and remaining setup choices; success is not experiment authorization. |
| `ProjectConfig` | Draft project/storage/setup mappings; packaged initialization schema governs keys. |
| `DraftExperiment` | Root-relative configuration references; inert draft, not ExperimentSpec. |
| `DraftSearchSpace` | Empty initial algorithm set grants no search permission. |
| `InitialState` | Initial storage state, not a recovery state machine. |

**Implemented planning and approval records**

| Record or alias | Contract |
|---|---|
| `ResolveRequest` | Experiment input resolves against explicit root. |
| `Diagnostic` | Safe field/source diagnostic; unavailable coordinates are None, not guessed. |
| `PlanResult` | A captured blocked plan may still have an identity; readiness is recomputed. |
| `VerificationResult(PlanResult)` | Integrity is distinct from readiness and reviewer authentication. |
| `PlanInspection` | Plan is preserved evidence where readable, never a trusted success flag. |
| `SearchSelection` | None means unresolved delegation. Structural checker narrows declared boundaries without registry access. |
| `BoundaryResult` | Failure returns neither effective value; inputs remain unmodified. |
| `ApprovalRequest` | Approves all proposed delegated decisions in the exact plan; nonblank reviewer/reason. |
| `ApprovalRecord` | Service derives scope and decision values from verified evidence, not caller claims. Schema 1.0, authentication none, UUID record identity and UTC timestamp; schema defines purpose/decision constants. |
| `RevocationRequest` | Revokes one existing approval in that exact plan scope. |
| `RevocationRecord` | Append-only scoped revocation; same assurance limits as approval. |

**Implemented semantic validation records**

| Record or alias | Contract |
|---|---|
| `RegistryResult` | Blocked registry has neither registry nor ID. |
| `ConfigurationRequest` | Optional registry path resolves against project root. |
| `ConfigurationResult` | Successful evidence published immutably; failure cannot claim valid configuration. |
| `CandidateRequest` | No trial launch, sampling or budget reservation. |
| `CandidateResult` | Fully effective values and source origins on success. |
| `ValidationInspection(ConfigurationResult)` | Intact stale evidence is integrity true/current false/blocked. |

**Proposed authorization and accounting records**

| Record or alias | Contract |
|---|---|
| `ResourceLimits` | Positive supplied limits; decimal cost string with matching currency or both None. None means not applicable, not unlimited when policy requires a limit. Reject unsupported mandatory limits. |
| `AccessScope` | Paths are explicit resolved project/external locations; endpoint allowlist is explicit, empty denies network. No credential values. |
| `AuthorizationRequest` | Scope may narrow approved policy, never expand it. Validation ID is mandatory for applicable validated execution, not basic extraction/restoration. |
| `AuthorizationRecord` | Service-written immutable decision record. Approval authenticity is not established; enforcement and currentness remain required. |
| `AuthorizationResult` | Only allowed returns a record; no launch or reservation. |
| `ReservationRequest` | Nonblank key and effective limits within authorization. Atomic admission against remaining project experiment budget. |
| `Reservation` | Durable state snapshots under one identity; retained uncertainty cannot release capacity. No mutable input-manifest reference creates a capture/reservation cycle. |
| `ResourceUsage` | Nonnegative observations; unavailable cost is explicit, never reported as zero. Settlement accounts each submission once. |

**Proposed capture and run records**

| Record or alias | Contract |
|---|---|
| `EnvironmentRecord` | Full commit SHA, actual interpreter/platform and exact dependency files. Environment ID hashes the record payload excluding its own ID. |
| `OutputCheck` | Unique nonblank ID; path under output root. exists requires expected true; sha256 requires EvidenceId; numeric requires finite number. Tolerances nonnegative, zero unless numeric. Numeric output is a JSON numeric scalar; pass when absolute error ≤ absolute tolerance + relative tolerance × absolute expected. |
| `CaptureRequest` | Explicit source-root selection; required external files registered; exclude secrets/environments/stores. Capture actual environment, do not accept caller-invented environment identity. |
| `InputManifest` | Manifest ID is computed over stored payload excluding its own ID and carried in the returned wrapper/store index. Exact stored payload bytes determine ExperimentSpec.input_manifest_id. Ordered guidance refs preserve order. |
| `RunStatus` | Execution state only; completed does not imply checks passed or acceptance. |
| `SubmissionStatus` | Accepted requires known run/input IDs. not_accepted requires definitive durable evidence. Lookup failures return unknown. |
| `CancellationResult` | Terminal means observed terminal execution, which may have completed before cancellation. No false claim of termination. |
| `LogSnapshot` | Ordered log chunks; partial logs remain readable after failure. |
| `CheckResult` | Result follows original check; unavailable evidence is incomplete, not pass. |
| `ExecutionCheckRequest` | Evaluator loads original checks from verified input manifest; caller cannot substitute checks. |
| `ExecutionAssessment` | Pass requires completed execution and every declared check passed. Failed execution cannot pass; missing evidence is incomplete. |
| `TerminalManifest` | Immutable terminal observation; no submitted/running status. Missing assessment remains explicit. ID follows input-manifest payload convention. |
| `RunRecord` | Inspection snapshot, not authoritative state transition. Missing terminal evidence cannot imply success. |

**Proposed source, dataset and approval records**

| Record or alias | Contract |
|---|---|
| `DataSourceMetadata` | Only permitted metadata, no raw rows or credentials from discovery. |
| `ExtractionSpec` | Local file, SQL query or object key according to connector; sampling {} means no sampling. Connector validates against approved query/sampling scope; no inferred permission. |
| `DatasetRef` | Nonnegative rows, exact source lineage and content. ID hashes dataset manifest payload. Missing validation/versioning refs mean extracted only, never accepted. |
| `QualityRule` | column empty for whole dataset; expected schema mapping, type string or nonnegative count. M1 supports these declarative rules, no executable rule strings. |
| `DatasetValidationRequest` | Validate verified content, unique rule IDs, reject unsupported rule kinds; do not silently ignore rules. |
| `ValidationReport` | Independent observed values; extraction completion alone does not pass validation. |
| `DatasetVersionRequest` | Passing matching report required before publishing validated version; returns new enriched DatasetRef, never mutates old evidence. |
| `DatasetRestoreRequest` | No overwrite of caller files; content hashes must match before exposing restored output as usable. |
| `DatasetApprovalRequest` | Nonblank labels; passing report for exact verified dataset. Operation means approve, not implicit approval through validation. |
| `DatasetApprovalRecord` | Durable exact-scope record; changed dataset/report does not inherit acceptance. |

**Proposed restoration records**

| Record or alias | Contract |
|---|---|
| `RestoreRequest` | Explicit empty/new destination, current source/store access; never silently replace existing files. |
| `RestoredRun` | Returned only after all required evidence/data/environment checks; locked environment materialized with pinned toolkit. Destination paths are local materialization results, not portable identities. |
| `ReproductionRequest` | References verified restoration; rechecks materialized content before new execution. |
| `ReproductionResult` | New run keeps original declared checks; successful launch alone is not reproduction success. |

**Assessment and split records**

| Record or alias | Contract |
|---|---|
| `AssessmentRequest` | Columns must exist in verified source schema. Classification requires target. Inspect only authorized development data; never inspect protected memberships after sealing. |
| `AssessmentFinding` | Unique finding ID; empty column means whole dataset. Method identifies statistic/anomaly/leakage rule and version; observed values retain counts/units and cannot assert universal absence of leakage. |
| `DatasetAssessment` | Include distributions, class counts/balance where relevant, anomaly and leakage diagnostics; blocking findings prevent dependent work until resolved in new evidence. |
| `SplitRequest` | Unique nonnull row key; finite positive fractions sum to 1 within 1e-12. Time/group columns are explicit constraints, even when combined. Time strategy sorts ascending; group strategy allocates whole groups. Reject constraints that cannot satisfy nonempty disjoint partitions. |
| `PartitionRef` | Membership preserves exact source row keys, not mutable row positions. Positive count. Protected membership/content references are redacted from experiment-facing views and resolved only by authorized services. |
| `SplitManifest` | Exactly one partition per role; memberships disjoint and cover source rows. Check all declared time/group constraints. Version source/membership hashes with DVC. Protected record stored in evaluator-side storage, not exposed as an ordinary experiment artifact. |
| `AssessmentApprovalRequest` | Nonblank reviewer/reason; matching source dataset and reviewable assessment/passing split checks required. |
| `AssessmentApprovalRecord` | Durable exact-scope approval. Changed source, assessment or split requires new approval. No reviewer authenticity claim. |

**Component registration and preprocessing protocols**

| Record or alias | Contract |
|---|---|
| `ParameterSpec` | No type coercion; false has_default requires default None. Nonempty choices restrict values; numeric bounds are inclusive/ordered. Reject default outside constraints and conflicting declarations. |
| `ComponentSpec` | Entrypoint is module:attribute from captured project code or a locked dependency. Unique ID and parameter names; explicit immutable-by-default declaration emitted by configuration authoring. Component identity includes code/lock, not entrypoint alone. |
| `RegistrationRequest` | Validate against combined built-in/project registry; no replacement of duplicates. Does not authorize tuning. |
| `ComponentRegistry` | Returned only when declarations, signatures, version and parameter specifications pass; immutable record snapshot. |
| `DataPartition` | Service-issued view; inference uses source split identity for fitted-state lineage. No training/interactive constructor may mint protected access. Materialization obeys role-specific access, not caller-supplied role text. |
| `TransformResult` | Output schema must match declaration; retain row-key alignment, reject row loss/duplication unless a separately approved contract permits it (not M2). |
| `FittedComponent` | Only approved training membership fits state. Store exact code/dependencies/parameters/schema; state checksum unchanged across transforms. |
| `PreprocessingRestoreRequest` | Verify state/code/dependencies before loading; hostile/unapproved serialized code must not execute during inspection. |

**Ordered feature plans, execution and reference comparison**

| Record or alias | Contract |
|---|---|
| `FeatureStep` | Stateful steps require training scope, stateless require none; fixed effective parameters and modification permission cannot exceed ComponentSpec. |
| `FeaturePlan` | Ordered schema-compatible pipeline; nonempty unique input columns exclude target and approved leakage exclusions. Empty steps permit explicit raw-feature baseline. |
| `FeatureExecutionRequest` | Verify approved assessment/split and authorized plan selection before training-only fit. |
| `FeatureSetRef` | No protected-test content in returned record. Immutable output/state hashes and row-key checks establish lineage. Stateless steps preserve code/parameters through the plan/registry. |
| `ReferenceEstimatorSpec` | Fixed explicit estimator/settings, no algorithm search or tunable domains. Project-authored wrappers permitted for this reference purpose, not general M3 model registration. |
| `MetricSpec` | M2 minimal built-ins; accuracy requires maximize/labels and MSE minimize/finite regression values. Nonnegative tolerances govern reproduction, not whether gain is positive. Additional metrics require explicit contract extension. |
| `FeatureComparisonProtocol` | Frozen baseline, estimator/settings, metric/direction and split binding. Each candidate uses the same protocol; changing any creates new identity and approval. |
| `FeatureApprovalRequest` | Explicit authorized authored candidates, nonblank reviewer/reason; every plan shares approved source/split. |
| `FeatureApprovalRecord` | Authorizes recorded comparison scope, not code modifications or holdout use. |
| `ReferenceFitResult` | Model fitted on training only; predictions correspond to approved validation row keys. Preserve model/code/environment without exposing holdout. |
| `FeatureComparisonRequest` | Check matching approved candidate plan, baseline and split; reserve both baseline/candidate work when needed, cache reuse separately validated. |
| `FeatureEvaluationReport` | Finite independent scores. gain = candidate − baseline for maximize, baseline − candidate for minimize; positive/zero/negative selects outcome. An invalid comparison never supports an improvement claim. |

**Pipeline stage and reuse records**

| Record or alias | Contract |
|---|---|
| `PipelineStage` | Source-root-relative cwd and entrypoint as M1; dependency/output/check paths resolve against stage cwd for DVC and toolkit identically. No absolute/escaping paths or shell command execution. |
| `PipelineDefinition` | Unique stage IDs and acyclic dependency graph derived from inputs/outputs; exact source definitions frozen. |
| `StageRequest` | Explicit reuse request does not bypass permission or verification. |
| `StageResult` | Success requires verified outputs and resolved dvc.lock hashes. Blocked may preserve available evidence but cannot imply accepted output. |
| `StageReuseRecord` | Preserve original producer and separately record present authorization/evaluation. Never create a new producer identity for a cache hit. |

**Model registration and algorithm selection**

| Record or alias | Contract |
|---|---|
| `ModelSpec` | Tasks classification/regression only; outputs labels/probabilities/regression_values. Unique IDs/parameters, explicit immutable-by-default permission; captured project code or pinned dependency, never toolkit edits. |
| `ModelRegistrationRequest` | Reject duplicate IDs across active combined model registry; validate signatures/version/task/output metadata before importing under execution controls. |
| `ModelRegistry` | Returned only on valid registration; code/dependency identities preserved. Scalar metadata must agree with M1 validation registry; disagreement blocks execution. |
| `AlgorithmSelectionRequest` | use/select require one explicit allowed choice; compare requires None and schedules every allowed algorithm. No agent reasoning dependency. |
| `AlgorithmSelection` | Immutable effective allowed set/selection; compare is algorithm coverage, not exhaustive parameter enumeration. Budget-shortened coverage stays incomplete, never silently becomes select mode. |
| `SearchRecommendation` | Proposal for a later configuration only; never expands active selection, registry or parameter bounds. |

**Training, models, predictions and checkpoints**

| Record or alias | Contract |
|---|---|
| `ComputeRequest` | Positive requested quantities; CPU count is 1 device. Reject unavailable device or mandatory unsupported quota before launch, never silently substitute hardware. |
| `ComputeObservation` | Actual device/version and explicit enforcement limitations; no unsupported limit reported as enforced. |
| `TrainingRequest` | Candidate requires exact baseline approval. Always call M1 validate_candidate and compatibility checks before reservation consumption/training, including Python/notebook/custom-code calls. Parameters materialized with origins, not resampled by adapter. |
| `TrainingContext` | Service supplies approved aligned training inputs and, only if authorized, development validation for early stopping. Never protected inputs. Writes limited to authorized run/checkpoint storage. |
| `FittedModel` | Immutable fitted artifacts and exact code/lock/feature lineage; state loading is isolated and verified. |
| `PredictionResult` | Stable row alignment; probabilities finite in [0,1] with declared class order and row sums within 1e-6 of 1; regression finite; labels match declared classes. Empty class_order for regression. |
| `TrainingResult` | Completed training requires model artifacts, but no scientific/quality/acceptance implication. Failure/cancellation preserves previously emitted checkpoints. |
| `ModelRestoreRequest` | Explicit destination; verify code/state/environment before load, no implicit retraining. |
| `CheckpointRecord` | Nonnegative step; declared_state lists actual model/optimizer/scheduler/RNG/loader state supplied by implementation. Immutable artifacts capture available state, never promise absent continuation state. |
| `CheckpointRestoreRequest` | Verify checksum, format, code/environment compatibility and permitted writes. |
| `CheckpointRestoration` | Required declared state must be usable under recorded checks; no exact-continuation claim merely from usable true. |

**Baselines and bounded tuning**

| Record or alias | Contract |
|---|---|
| `BaselineApprovalRequest` | Matching scientifically valid development baseline and nonblank labels before candidate comparisons. |
| `BaselineApprovalRecord` | Immutable reviewed baseline identity and evidence; baseline changes invalidate dependent comparisons. |
| `TuningRequest` | Explicit finite candidate order provides simple local non-exhaustive tuning. Each CandidateRequest uses same project/validation binding and immutable checked boundaries. Evaluation uses the fixed criteria_id, not a trial-selected metric. No Optuna dependency required. |
| `TrialRecord` | Rejected candidate starts no training; trial/run identity and reservation are durably allocated once for each admitted candidate. |
| `OptimizationSummary` | Summarize coverage/search and consumed resources, including unsuccessful work. Proposal uses development evidence only; no final access authorization. |

**Independent evaluation and final decisions**

| Record or alias | Contract |
|---|---|
| `EvaluationCheckSpec` | Nonempty ID and finite nonnegative tolerances. Fold/slice inputs contain explicit development row memberships; stress inputs contain an approved transformed development dataset; repeat inputs reference repeated development run evidence. expected is a finite scalar score. All input identities are frozen before evaluation and cannot include protected data in development. |
| `AcceptanceCriteria` | Freeze metric/output compatibility, thresholds, fold/slice/stress definitions and rerun tolerances before evaluation. quality_threshold is an inclusive lower bound for maximize and upper bound for minimize; baseline gain uses direction-normalized candidate improvement. Output kind must match the metric; checks require explicit expected values. |
| `EvaluationRequest` | Development validation only; baseline None allowed only for baseline evaluation. Evaluator restores model and fitted preprocessing from verified evidence. |
| `EvaluationReport` | Model quality cannot be sufficient if execution/validity prerequisites fail. Missing evidence is explicit. Robustness and reproduction checks remain separate individual results; no narrative acceptance claim. |
| `FinalEvaluationApprovalRequest` | Select exactly one frozen candidate and separately authorize final evaluation scope. All development prerequisites and pending gates checked. |
| `FinalEvaluationApproval` | Bound final scope, no reusable permission for iterative testing. |
| `FinalEvaluationRequest` | Protected evaluator resolves test resources internally. Repeat transport request reattaches to same final attempt, never creates another evaluation. |
| `ModelDecisionRequest` | Approve requires completed, scientifically valid, quality-sufficient final evidence and required checks passed. |
| `ModelDecision` | Only explicit approve permits model acceptance; reject/review preserves evidence and stops dependent improvement. |

**Reporting and public verification**

| Record or alias | Contract |
|---|---|
| `RunComparisonRequest` | Same approved comparison protocol/features/split or explicit incomparable result, not silently mixed metrics. |
| `RunComparison` | Preserve baseline/candidate parameters, statuses, models and evaluation refs; missing links cannot imply comparability. |
| `FinalReportRequest` | No decision means awaiting review, not accepted. Protected report readable only in final-review context. |
| `FinalReport` | Includes original objective, metrics/baseline, validity/robustness/reproduction, component/fitted-feature/data/code/config/environment lineage and independent evidence references. Document text cannot override ModelDecision or evaluation. |

**Runtime guidance selection and preservation**

| Record or alias | Contract |
|---|---|
| `GuidanceSource` | Packaged runtime-resource path or project runtime path, never arbitrary discovery. Nonempty version; explicit task mapping, no filename-based activation. Development AGENTS.md files are not selectable runtime sources. |
| `GuidanceSelectionRequest` | Only configured mappings; source ownership/path resolved explicitly. Shared first, task second, project last; preserve configured order within each layer. |
| `PreservedGuidance` | Preserve exact UTF-8 bytes, original path/version and checksum. Contiguous zero-based load indexes, no source silently overwritten. |
| `GuidanceConflict` | Explicit observable conflict with another source or approved experiment field. Nonblank resolution only for resolved; unresolved blocks dependent work. No promise to infer every contradiction in unrestricted natural language. |
| `RuntimeInstructionBundle` | Immutable selected contents/order/ownership. No toolkit/experiment development files loaded automatically. Bound plan remains preserved; changed selection/content creates new bundle and configuration. |
| `GuidanceSelectionResult` | Only ready bundle may be delivered; absent source, unknown version or unresolved visible conflict blocks. Preserve diagnostic evidence for rejected selections. |
| `ExternalContextRecord` | Capture only permitted observable context; false when anything unknown. No credential/session secret copies. External independently loaded AGENTS.md is outside toolkit loader guarantee. |
| `GuidanceDeliveryReceipt` | Must match bundle's ordered content identities; acknowledged means delivery evidence, not proof of instruction compliance or deterministic reasoning. |

**Adapter capabilities, tasks and results**

| Record or alias | Contract |
|---|---|
| `AgentIntegrationSpec` | Exact verified invocation interface/version, not a marketing product name. No credential values. Unverified version cannot claim supported status. |
| `AgentCapabilities` | Task kinds delegated_decisions/generate_notebook/revise_experiment. Missing required capability blocks delegation. Measurement/enforcement named separately for tokens/cost/runtime; unavailable usage is explicit. |
| `AgentTask` | Bound approved phase/scope. Paths/tools narrow authorization, never broaden it. Feedback is development-only. Fresh attempt ID on permitted retry; identical transport retry keeps same attempt. |
| `AgentBudget` | Positive limits, exact decimal cost and currency paired. Required tokens/cost limit unsupported by adapter blocks task rather than claiming enforcement; optional unavailable measurements remain limitations. Toolkit run budgets remain independently enforced. |
| `AgentUsage` | Nonnegative known quantities; unknown is None, not zero. Durable measurement IDs prevent double accounting. Runtime observation does not imply complete token/cost accounting. |
| `AgentTaskStatus` | Task status is independent of experiment RunStatus and model acceptance. |
| `AgentTaskHandle` | Durable binding before accepting execution; unknown external acceptance goes to needs_review, not automatic resend. |
| `AgentResult` | Untrusted proposal/evidence references, not authority. Completed managed result requires matching delivered bundle. Cross-attempt/late cancelled results cannot advance work. |
| `AgentCancellation` | Cancels assistant task, not automatically every experiment run. Explicit child-work disposition is recorded; late results cannot bypass stop decision. |

**Delegated proposals and controlled file changes**

| Record or alias | Contract |
|---|---|
| `DecisionProposal` | Only explicitly delegated fields; nonblank rationale and schema-valid proposed values. Undelegated scientific decisions cannot be overwritten. |
| `DecisionProposalRequest` | Preserve original input bytes, write revised proposed inputs at explicit new location, never alter original evidence. |
| `DecisionProposalResult` | Reuse resolver schemas and approval semantics; source/resolved versions retained. Proposed delegated decisions remain blocked until existing approve_plan records match. |
| `ProposedFileChange` | Root-relative safe project path. Create requires absent before; replace/delete require exact prior hash. Delete has after None; other operations require captured content. Reject toolkit install/source and unauthorized paths. |
| `NotebookRevisionRequest` | Verify active task/scope and file identities before applying; agent rationale cannot authorize changes. |
| `NotebookRevision` | Saved notebook/helper snapshot with Markdown objectives/assumptions/code/results/next steps and tagged parameter cell. No hidden unsaved state. Results narrative remains unverified until managed run/evaluation. |
| `ComponentChangeRequest` | Exact immutable code identities and narrowly proposed changes; no blanket algorithm/data/metric expansion. Nonblank reviewer/reason. |
| `ComponentChangeApproval` | Permission matches hashed proposed changes. Default absent permission denies immutable writes. Pinned dependency change requires a new locked dependency identity, never editing site-packages in place. |

**Interactive kernels and bounded development iteration**

| Record or alias | Contract |
|---|---|
| `InteractiveKernelRequest` | Locked project environment, declared ipykernel dependency, explicit authorized cwd; no protected-test/evaluator credentials. |
| `InteractiveKernelSession` | Nonsecret reference to protected local connection settings; never publish raw kernel tokens. VS Code connection documented separately; no acceptance effect. |
| `DevelopmentFeedback` | Only verified development-phase EvaluationReport can generate feedback; reject final-phase evidence or derived protected-test recommendations. |
| `IterationPolicy` | Positive counts, finite nonnegative gain in metric's approved direction. Stagnation means patience consecutive independently valid comparisons below minimum_gain; invalidity never counts as improvement. |
| `IterationRequest` | Caller supplies a fresh UUID so cancellation can target active work before the blocking improve call returns. Persist identity before first task; identical retry reconciles existing work, conflicting request fails. One approved workflow phase only; independent toolkit budgets and no implicit phase return/acquisition. |
| `IterationStep` | Nonnegative index; preserve unsuccessful/partial attempts and consumed budgets. No duplicate acceptance/accounting after uncertain adapter responses. |
| `IterationResult` | Success is development criteria met, not final model acceptance. Stop at configured max iterations as budget_exhausted. Unknown work remains needs_review, never silently retried. |

**Workflow planning and state records**

| Record or alias | Contract |
|---|---|
| `WorkflowPhase` | Maps to design's seven ML workflow phases, never implementation phase numbers. |
| `PhasePlan` | Positive iteration ceiling, acyclic dependencies. Skipping needs approved sufficient existing artifacts, not missing execution evidence interpreted as success. |
| `WorkflowPlan` | One occurrence per included phase; initial approval completes problem definition. Preserve input decisions and frozen approved protocols; cannot expand experiment search/access scope. |
| `WorkflowStatus` | Separate from agent task/run status and model quality. Terminal/review states never silently authorize work. |
| `PhaseProgress` | Evidence must match this phase and configuration. Skipped requires recorded approval and verified skip artifacts. |
| `WorkflowState` | Nonnegative monotonically increasing version/epoch. Snapshot only, not mutable live handle. State references remain inspectable after failure/cancellation. |
| `WorkflowStartRequest` | Caller UUID supports inspection/cancel before blocking work finishes; starting creates planned state, not initial approval or task execution. Same UUID/request is idempotent. |
| `WorkflowAdvanceRequest` | Requires current owner/version and matching approved decision/evidence before entering next authorized phase or scheduling work. |
| `WorkflowCancelRequest` | Nonblank reason; durable cancellation takes precedence over subsequent scheduling. Child task/run cancellation tracked separately. |

**Scoped workflow decisions**

| Record or alias | Contract |
|---|---|
| `WorkflowScope` | Explicit proposed change, never implicit broad permission. A changed criterion/access/budget/configuration requires a new reviewed scope. Final-feedback restrictions remain non-bypassable. |
| `WorkflowGateRequest` | Independent evidence must be sufficient/current before request becomes reviewable; insufficient evidence keeps work blocked. |
| `WorkflowGate` | Bind exact reviewed version; changed configuration/evidence makes old pending gate stale. |
| `WorkflowDecisionRequest` | Nonblank self-declared labels. A requested revision uses an explicitly proposed scope; cannot infer changes from free-text reason. |
| `WorkflowDecision` | Durable append-only record with exact binding. Current version does not prove developer identity or reject all forged agent-written approvals. |

**Durable store, ownership and reconciliation**

| Record or alias | Contract |
|---|---|
| `RecoveryOwnership` | Increment epoch on ownership acquisition, never reset/reuse it. Lease expiry alone does not authorize an old owner; every mutation/submission checks stored owner+epoch and lease. |
| `OwnershipRequest` | Positive duration; acquire atomically only without current live owner or after expiry. Renew preserves epoch and rejects replaced owner. Clock anomalies require review rather than concurrent authority. |
| `WorkflowCommit` | Atomic compare-and-swap for state/events/intents/usage; version increments exactly once. Failed checks perform no partial commit. |
| `SubmissionIntent` | Persist before any runner/adapter call. Key bound to exact input/config/guidance; unknown cannot free reservation or permit a new attempt. |
| `UsageMeasurement` | Measurement IDs immutable; duplicate identical observation is a no-op, conflicting duplicate requires review. Snapshots for one attempt replace prior cumulative totals, never sum cumulative reports twice. |
| `WorkflowRecoveryRecord` | Durable reconciliation snapshot connects progress and exact preserved records; transcript/memory is not state. Reuse never changes producer identity. |
| `RecoveryRequest` | Acquire exclusive epoch before reconciliation; current access required even for historically approved evidence. |
| `ReconciliationItem` | Observations require runner/task/tracking evidence. Missing MLflow record or timeout alone is unknown, not never accepted. |
| `RecoveryResult` | No new execution until pending/unknown admissions reconciled and approvals/remaining budgets checked. Terminal states remain stopped unless separately authorized action. |

**Two adapters under one contract**

| Record or alias | Contract |
|---|---|
| `AdapterRegistry` | Unique integration IDs and at least two independently verified concrete integrations for story acceptance; no credentials. |
| `AdapterSelectionRequest` | Explicit integration selection and live capability checks; no silent fallback to another assistant. |
| `AdapterSelection` | Reject missing guidance/access/cancellation/budget capabilities before delegation. Selection cannot alter plan, criteria, dataset access or evaluator. |

**Audit and retry-safe tracking publication**

| Record or alias | Contract |
|---|---|
| `AuditEvent` | Append-only increasing workflow sequence; exact authorizing decisions/inputs retained. Append-only is cooperative storage semantics, not authenticity against workspace writers. |
| `WorkflowManifest` | Connect approved scope, MLflow/DVC, configurations, guidance and runs without relocating protected content into public manifests. |
| `EvidenceReuseRecord` | Original producer identities immutable; subsequent-use permission stored separately. Reuse requires current authorization/evaluation, not historical success alone. |
| `TrackingPublication` | Unique durable logical publication per toolkit run. Reuse identical publication; conflicting manifests/IDs require review, never overwrite. |
| `AuditLookupRequest` | Exactly one selector; authorization redacts protected references. |
| `AuditLookupResult` | Missing/conflicting references explicit; lookup success does not establish completeness or authenticity. |

**Evidence and proposal records**

| Record or alias | Contract |
|---|---|
| `DataGapRequest` | Verified approved development data/evaluations only; reject final reports, protected memberships and derived final feedback. |
| `DataGapFinding` | Explicit development row/slice definition, observed counts/metrics with units and methods; nonblank explanation, no inference from protected-test results. |
| `DataGapReport` | Absence of a supported finding is explicit empty findings, not an invented acquisition need. Preserve exact evidence sources and approved scope. |
| `AcquisitionLimits` | Positive finite resource/compute/record ceilings; nonnegative exact decimal cost with currency. Zero cost is an explicit free-source ceiling, not unknown pricing. |
| `AcquisitionStrategy` | Uses approved local/SQL/object source connector and explicit sampling/query scope. No new external source or strategy implicitly authorized. |
| `DataOrigin` | Synthetic/augmented input requires producer and parent lineage or explicit unavailable-parent explanation. Label imported synthetic inputs even when this release does not generate them. Never silently label generated data observed. |
| `AcquisitionProposalRequest` | Nonblank benefit hypothesis, finite nonnegative decimal estimate in limits currency. Request is not execution approval. |
| `DataAcquisitionProposal` | Preserve reason/evidence/hypothesis/source/strategy/cost/limits and required return/approval scope. Cannot alter active evaluation/access/budget rules by itself. |

**Acquisition authorization, execution and lineage**

| Record or alias | Contract |
|---|---|
| `AcquisitionApprovalRequest` | Nonblank reviewer/reason; matching reviewed source/strategy/scope/limits and authorizing WorkflowDecision. No blanket permission to query other sources. |
| `AcquisitionApproval` | Current exact-scope record; no per-operation approval needed inside approved limits. Unauthenticated assurance follows existing exception, no protection against fabricated workspace approvals claimed. |
| `AcquisitionRequest` | Bind M5 durable intent/epoch and M1 extraction authorization; caller acquisition UUID allows cancellation/recovery. Key and exact inputs preserved across transport retries. |
| `AcquisitionLineage` | Source/query/sampling/time/permission references and synthetic provenance retained; new content never overwrites old dataset identity. |
| `AcquisitionResult` | completed requires verified content/quality/versioning/lineage; other states preserve partial output but never call it accepted data. New dataset acceptance remains a separate M1 dataset approval. |
| `AcquisitionCancellation` | Cancellation is not confirmation of terminal source operation; preserve uncertain external request and budget reservation. |
| `AcquisitionAccounting` | Nonnegative cumulative compute; measurement IDs settle once. Unknown work retains compute reservations as well as M5 cost/runtime/trial capacity. Persist as versioned M6 extension in the same local workflow transaction, not a silent change to ResourceUsage. |

**Consistent evaluation, stopping and recovery**

| Record or alias | Contract |
|---|---|
| `AcquisitionComparisonProtocol` | Fixed development validation cohort and identical approved metric/direction/settings/tolerances. Before/after training/split identities may differ, but cohort membership/content and scoring protocol cannot silently change. |
| `AcquisitionComparisonRequest` | Verified independent development evaluations, matching acquired lineage and separately authorized downstream work; no final-test evidence. |
| `AcquisitionComparison` | Direction-normalized gain as M2; positive/zero/negative only for valid aligned evidence. Missing/mismatched protocol/cohort is incomparable, never an improvement claim. |
| `AcquisitionLoopPolicy` | Positive counts; finite nonnegative required improvement. Stop stagnation after patience consecutive valid comparisons below minimum_gain. Invalid results cannot count as improvement. |
| `AcquisitionLoopRequest` | Explicit finite ordered proposals, each separately approved in scope. No automatic strategy expansion, protected feedback or approval generation. |
| `AcquisitionLoopStep` | Nonnegative index; pending downstream approval records partial progress and stops, rather than running work in unapproved phase. |
| `AcquisitionLoopResult` | Success meets approved development goal, not final model acceptance. completed means finite proposal list exhausted without another terminal condition. Preserve all consumed usage, outcomes and linked producer identities. |
| `AcquisitionResumeRequest` | Reuse M5 exclusive recovery ownership/current authorization. Restore proposal/approval/usage/data/config/bundle identities before additional admission. |


Additional inline-defined records and aliases complete the table inventory:

| Record, alias, or notation | Purpose |
|---|---|
| `PrepareExperimentRequest`, `PreparedExperiment` | Bind verified manifest, authorization, reservation, and submission key; only a ready result contains a spec. |
| `ArtifactRef` | Identifies an artifact by verified checksum, relative path, media type, size, and nonsecret storage location. |
| `JSONValue`, `SearchSpace`, `RegistryDocument` | Existing JSON value and document aliases, not executable classes. |
| `PlanStatus`, `ValidationStatus` | Existing literal aliases for plan readiness and semantic validity. |
| `EvidenceId`, `RecordId` | Proposed content-hash and UUID identity aliases. |
| `ProjectContext` | Shorthand for explicit project root, project ID, and experiment ID fields; not a class. |

### Error classes and conceptual-name replacements

Implemented `InitializationError` preserves stage, conflicts, completed steps, and
recovery instructions. `PlanningError` and `ValidationError` carry safe code/message;
`ApprovalError` additionally distinguishes operational failures.

Proposed error classes carry safe code/message and available evidence identities;
they do not retry, approve, or clean up work themselves:

- Execution and data: `ExecutionError`, `TrackingError`, `AuthorizationError`,
  `RestorationError`, `DatasetError`.
- Assessment and features: `AssessmentError`, `SplitError`, `ComponentError`,
  `FeatureError`, `PipelineError`.
- Modeling and reporting: `ModelError`, `SelectionError`, `CheckpointError`,
  `TuningError`, `EvaluationError`, `ReportError`.
- Agent work: `GuidanceError`, `AgentError`, `DecisionError`,
  `RevisionError`, `ComponentPermissionError`, `InteractiveError`,
  `IterationError`.
- Workflow: `WorkflowError`, `WorkflowStoreError`, `WorkflowDecisionError`,
  `RecoveryError`, `AdapterSelectionError`, `AuditError`.
- Acquisition: `AcquisitionError`, `AcquisitionApprovalError`,
  `AcquisitionComparisonError`, `AcquisitionRecoveryError`.

Older conceptual names do not add competing APIs. `FeatureEngineeringAdapter` is
replaced by authored `FeaturePlan`, `execute_features()`, and `compare_features()`;
`Evaluator` by separate development/final evaluation services; `ApprovalService`
by typed workflow gate services. `ExperimentResult` maps to `RunRecord` and
`TerminalManifest`. Conceptual `ExperimentConfig`, `MLTaskSpec`, `SearchSpaceSpec`,
and `ExperimentProjectConfig` map to preserved planning inputs/schemas and
initialization drafts. No separate M2 `FeatureContext` class is proposed.

### Boundaries and remaining decisions

Completion, scientific validity, model quality, and developer acceptance are
separate outcomes. Reuse retains the original producer identity and requires
current authorization. Unknown external acceptance retains reservations and blocks
blind resubmission. Restoration never silently substitutes current inputs.

Implementation still requires verified OS filesystem/network/credential isolation,
protected partition and evaluator access, assistant/kernel isolation, two concrete
agent integrations, and per-source acquisition limits/reconciliation. Authenticated
reviewer identity remains deferred under the recorded approval exception. See the
[decision register](design/software-blueprint.md#open-decision-and-assurance-register).
Private helper algorithms are outside this public inventory.
