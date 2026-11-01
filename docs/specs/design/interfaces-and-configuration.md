# Interfaces and Configuration

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Interfaces and Contracts.

**Related contracts:** Read [execution and governance](execution-and-governance.md); [data and features](data-and-features.md); [repository layout](repository-layout.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 8. Interfaces and Contracts

### Contributor development and package verification (Milestone 0)

US-31–33 establish the harness repository before experiment-user features. macOS is the initial verified local development platform. Linux (Ubuntu 24.04) is the initial CI platform, per US-32 SC-01. Windows and other platforms remain eligible for future verification; document platform-specific requirements and known limitations without claiming those platforms are verified. Python 3.12 or newer is required. CI verifies Python 3.12 as the minimum supported version; document any additional versions tested.

Provide contributor prerequisites, clone/setup instructions, runtime and development dependency synchronization through `uv` and the committed lockfile, configuration/credential guidance with practical local defaults, and shared commands for tests, linting, formatting checks, type checks, and smoke verification. Commit tool configurations and control tool versions through development dependencies and the lockfile. Document Python naming, typing, docstring, import, and error-handling conventions; enforce conventions through automated checks where supported. Document when and how contributors may add rule suppressions and check exclusions, requiring a recorded justification for each exception.

The initial CLI implements `agentic-ml --version`, reporting the installed distribution version and exiting successfully. The source-checkout smoke check invokes it. Verify setup on macOS from a fresh checkout and a new development environment using only documented prerequisites and steps. Run all documented development checks and retain the operating system, Python/tool versions, commands, and results as review evidence. CI starts from a clean checkout on pull requests and default-branch updates, installs required tools, synchronizes runtime and development dependencies without changing the lockfile, and runs the same documented checks. Failed checks produce a failing CI result; check results and diagnostic logs are accessible from the pull request.

Build wheel and source distributions. Install each directly built wheel and each wheel rebuilt from the source distribution with declared runtime dependencies into a clean environment. Run checks outside the checkout without editable installation or development dependencies: verify version output against distribution metadata, `agentic_ml` imports, and access to packaged templates and runtime guidance. Document local reproduction and run these checks in CI. Milestone 0 ships at least one minimal template and one minimal runtime guidance file with explicitly provisional contents. Installed-package checks read both resources and compare their contents with expected values for each wheel build path. Complete, usable experiment initialization resources belong to Milestone 1.

All contracts should have versioned JSON Schemas and typed Python models. `AgentAdapter` applies to managed delegation; interactive assistants use the public CLI/API for plan validation, submission, status, artifact retrieval, evaluation feedback, and cancellation without implementing this interface. These conceptual interfaces require further design for asynchronous operations, error handling, and authorization. Submission idempotency and recovery must satisfy the behavioral contract below; exact schemas and persistence mechanisms remain implementation decisions.

```python
from typing import Protocol, Any


class AgentAdapter(Protocol):
    def capabilities(self) -> set[str]: ...
    def execute(self, task: "AgentTask") -> "AgentResult": ...
    def cancel(self, task_id: str) -> None: ...


class DataSourceAdapter(Protocol):
    def discover(self) -> "DataSourceMetadata": ...
    def extract(self, spec: "ExtractionSpec") -> "DatasetRef": ...
    def validate(self, dataset: "DatasetRef") -> "ValidationReport": ...


class DataAcquisitionPlanner(Protocol):
    def diagnose(
        self, dataset: "DatasetRef", evaluation: "EvaluationReport"
    ) -> "DataGapReport": ...
    def propose(self, gaps: "DataGapReport") -> "DataAcquisitionProposal": ...


class DataAcquisitionExecutor(Protocol):
    def execute(
        self, proposal: "DataAcquisitionProposal", authorization: "ApprovalRecord"
    ) -> "DatasetRef": ...


class FeatureEngineeringAdapter(Protocol):
    def propose(
        self, dataset: "DatasetRef", context: "FeatureContext"
    ) -> "FeaturePlan": ...
    def transform(
        self, dataset: "DatasetRef", plan: "FeaturePlan"
    ) -> "FeatureSetRef": ...
    def evaluate(self, feature_set: "FeatureSetRef") -> "FeatureEvaluationReport": ...


class ExperimentRunner(Protocol):
    def submit(self, spec: "ExperimentSpec", submission_key: str) -> str: ...
    def lookup_submission(self, submission_key: str) -> "SubmissionStatus": ...
    def status(self, run_id: str) -> "RunStatus": ...
    def cancel(self, run_id: str) -> None: ...
    def artifacts(self, run_id: str) -> list[str]: ...


class ModelAdapter(Protocol):
    def train(self, context: "TrainingContext") -> Any: ...
    def predict(self, model: Any, data: Any) -> Any: ...
    def save(self, model: Any, path: str) -> None: ...
    def load(self, path: str) -> Any: ...


class Evaluator(Protocol):
    def evaluate(
        self, run_id: str, criteria: "AcceptanceCriteria"
    ) -> "EvaluationReport": ...


class ApprovalService(Protocol):
    def request(self, phase_id: str) -> str: ...
    def decide(self, approval_id: str, decision: str) -> None: ...
```

Managed adapter capability discovery must identify supported task types, invocation interface/version, guidance delivery, result retrieval, cancellation behavior, and available usage accounting before delegation. Unsupported required capabilities block managed delegation. The common contract describes verified behavior rather than assuming every assistant exposes equivalent session control.

### PyTorch checkpoint restoration

PyTorch integrations must provide a documented checkpoint restore path through the supplied or built-in model implementation, separately from final-model `save`/`load` persistence. The model implementation defines the checkpoint format, declares the state it contains, and restores that declared state. Preserve emitted checkpoints as run artifacts together with model, executed-code, configuration, and dependency identities needed to load them in the recorded environment. The experiment runner captures and preserves these artifacts; it does not interpret framework-specific checkpoint payloads.

Restoration recovers the state declared by the checkpoint. Exact training continuation is not guaranteed by checkpoint capture or restoration alone; it requires explicit support for the necessary optimizer, scheduler, random-number, and data-loader state. Concrete restore API signatures and checkpoint payloads remain framework-specific implementation decisions subject to this contract.

### Primary contracts

| Contract | Key fields |
|---|---|
| `MLTaskSpec` | Objective, target, task type, data, feature guidance, delegated decisions, algorithm mode, metrics, budgets, policies, source brief reference |
| `ExperimentProjectConfig` | Schema version, project root and environment reference, tracking/storage/state locations, access policy references, interactive/managed mode, optional managed adapter and verified product/interface/version, explicit project guidance mapping, project-local component declarations |
| `ComponentSpec` | Identifier, kind, Python entrypoint, interface version, supported tasks/prediction outputs where applicable, parameter types/defaults/constraints, code or dependency identity, agent modification permission |
| `ExperimentConfig` | Schema version, experiment identifier, brief/search-space references, notebook entrypoints, data references, feature pipeline component references and parameters, working directory, execution settings; resolved into the approved `ExperimentSpec` |
| `RuntimeInstructionBundle` | Harness-supplied shared/task-specific guidance snapshots, audience, task mapping, ordered source paths, versions/checksums; separately identified additional assistant context where observable, with capture limitations |
| `SearchSpaceSpec` | Schema version, registered algorithm identifiers, fixed parameters, typed choices/ranges, scales, configuration checksum |
| `WorkflowPlan` | Workflow phases, dependencies, gates, iteration limits |
| `AgentTask` / `AgentResult` | Durable task/attempt identifiers, scope, approved plan and guidance references, allowed tools, proposed changes, output/artifact references, status, available usage evidence, cancellation outcome |
| `ExtractionSpec` / `DatasetRef` | Source, query, snapshot, checksum, schema, lineage |
| `DataGapReport` / `DataAcquisitionProposal` | Evidence, acquisition hypothesis, scope, cost, approval |
| `FeaturePlan` / `FeatureSetRef` | Ordered component references, effective parameters, input/output schemas, fitting scope, modification permissions, fitted state, versions, provenance |
| `ExperimentSpec` / `ExperimentResult` | Project/experiment identity, model, data, notebook/code snapshots, experiment Git revision, harness repository URL/full commit SHA/package version, build identity where available, environment/lockfile identity, effective parameters, source configuration references, runtime instruction bundle reference, resolved decisions, resources, metrics, artifacts |
| `EvaluationReport` | Metrics, validity checks, baseline comparison, evidence |
| `ApprovalRecord` | Authenticated developer identity, scope and plan/configuration identity, decision, timestamp, verification evidence, audit trail; submission by an agent does not establish developer approval |
| `WorkflowRecoveryRecord` | Project/workflow/phase identity and progress, task/attempt associations, submission key, approved configuration and input-manifest checksum, guidance and approval references, harness/runner/MLflow run identities, evidence/artifact references, budget reservations and accounted usage, terminal or reviewable outcomes, recovery ownership/version |
| `SubmissionStatus` | Submission key and bound input identity, acceptance state (accepted, definitively not accepted, or unknown), runner run identity and execution status where known, evidence supporting the observation; lookup failure is unknown, not proof of non-acceptance |

### Submission identity and recovery contracts

Before runner submission, persist a project-associated recovery record with a stable submission key for that task attempt, the approved configuration and immutable input-manifest checksum, applicable approval/guidance references, and a reservation against applicable execution budgets. If this record cannot be persisted, do not submit. Preserve workflow phase progress and dataset lineage, including across acquisition and subsequent downstream work.

Repeated submission with the same key and identical bound inputs returns the existing run identity without starting another execution. Reusing a key with different inputs fails. The runner must durably associate the key and input identity with the execution before starting work and support lookup by that key after restart. Concurrent submissions with the same key must obey the same rule. Retain this association for as long as the workflow can be resumed; lost or unavailable associations produce an unknown status rather than making the key eligible for fresh execution.

`lookup_submission` must distinguish accepted work, definitive evidence that submission was never accepted, and uncertainty. A timeout, missing MLflow record, or unavailable runner alone is insufficient evidence of non-acceptance. Backend-specific implementations must meet these semantics; inability to establish status leads to review under [§9](execution-and-governance.md#9-execution-evaluation-and-governance), not blind resubmission. A permitted retry after a failed or cancelled execution is a new attempt with a new submission key linked to its predecessor; a transport retry of the original submission keeps its original key.

Recovery reconciles runner status, durable workflow records, and MLflow evidence as specified in [§9](execution-and-governance.md#9-execution-evaluation-and-governance). Publishing tracking records and terminal manifests must also tolerate retries: durably associate the tracking identity with the harness run, reconcile uncertain publication, and reuse existing records and identical immutable manifests rather than create duplicate logical results or overwrite conflicting evidence. Conflicting or uncertain identities require review. Explicit reproduction under the restoration lifecycle remains a new linked run, distinct from recovery of an existing attempt.

### User-supplied ML components

Users may supply existing model implementations, training routines, and feature-preparation code in their experiment repository or as pinned Python dependencies. Using these components must not require modifying the harness.

Project configuration declares each component's identifier, Python entrypoint, interface version, supported tasks where applicable, and parameter specification. The harness combines these declarations with its built-in registry for that project. Duplicate identifiers and incompatible interfaces are rejected before execution.

User-supplied components receive the same execution controls, parameter validation, independent evaluation, provenance tracking, and resource limits as built-in components.

Users may designate supplied components as immutable or authorize agents to modify them. Supplied code is immutable by default; agents may configure and invoke it within approved boundaries. Changes to immutable components require explicit developer approval and a new versioned experiment configuration. Permission to modify code does not expand the approved component, data-access, parameter, or evaluation boundaries.

The following capabilities become versioned public interfaces, refining the conceptual adapters above:

| Component | Required capabilities |
|---|---|
| Custom model | Train using approved training/validation inputs; predict through an interface usable by the independent evaluator; save and restore the fitted model |
| Stateful preprocessor | Fit on training inputs; transform using fitted state; save and restore that state |
| Stateless transformation | Transform inputs without fitting; declare output schema |

Framework-native implementations may be integrated through project-local wrappers. Training routines may return framework-specific models, provided the wrapper exposes the required prediction and persistence operations. The existing `FeatureEngineeringAdapter` plans and evaluates feature work; supplied preprocessors and transformations provide the execution capabilities listed above. Exact preprocessor method signatures remain subject to interface design.

Component declarations include supported prediction outputs, such as labels, probabilities, or regression values. Before training, the harness rejects components that cannot provide the outputs required by the approved evaluation metrics. Protected test data remains accessible only through independent evaluation.

The following configuration illustrates the intended workflow; the precise schemas remain subject to interface design:

```yaml
# project.yaml
components:
  models:
    custom_churn_model:
      interface_version: "0.1"
      entrypoint: churn_experiments.models:ChurnModelAdapter
      task_types: [classification]
      prediction_outputs: [labels, probabilities]
      agent_may_modify: false
      parameters:
        regularization:
          type: float
          default: 0.1
          minimum: 0.0

  preprocessors:
    domain_features:
      interface_version: "0.1"
      entrypoint: churn_experiments.features:DomainFeatureAdapter
      kind: stateful
      agent_may_modify: false
      parameters: {}
```

```yaml
# search-space.yaml
schema_version: "0.1"
algorithms:
  custom_churn_model:
    search:
      regularization:
        type: float
        min: 0.001
        max: 1.0
        scale: logarithmic
```

```yaml
# experiment.yaml — additional fields
features:
  pipeline:
    - component: domain_features
      parameters: {}
```

Component parameter specifications define valid types, defaults, and constraints. Experiment search spaces define the narrower values agents may explore. Declaring a component does not automatically authorize its use or parameter tuning. Feature pipeline parameters are fixed by the approved feature plan; changes require the applicable feature-engineering workflow phase authorization and a recorded plan revision.

Run lineage preserves component declarations, exact project-code snapshots or pinned dependency identities, effective parameters, and fitted artifacts. Component code changes authorized within a workflow phase are captured in each run's source snapshot.

### Project initialization and installation

Provide a documented bootstrap path starting with a vanilla Python interpreter and local raw data. Users first install `uv` and Git, then install the harness as a Python package directly from its GitHub repository into the user project's environment. Pin the Git dependency to a full commit SHA and use a normal package installation, rather than an editable installation. Package-registry distribution is future work.

Users do not need to manually clone or maintain a harness working checkout. The installer may fetch the pinned source into its managed cache to build and install the package. Downloads require network access and, for a private repository, configured Git credentials; keep credentials outside committed configuration.

The intended installation and initialization sequence is:

```bash
# After installing uv and Git:
mkdir customer-churn
cd customer-churn

git init
uv init
uv add "git+https://github.com/OWNER/HARNESS-REPO.git" --rev FULL_COMMIT_SHA

uv run agentic-ml init
# Open this project in VS Code and select its .venv notebook kernel.
```

The repository URL and commit SHA are placeholders. These commands specify the intended product interface; the harness and CLI still require implementation. There is no separate initializer-tool installation: `agentic-ml init` runs from the harness already installed in the project's `.venv`.

`agentic-ml init` must:

1. Add project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and any project-package scaffolding to the existing user repository.
2. Preserve existing files and report conflicts rather than silently overwriting them. Preserve the declared harness Git dependency and pinned commit.
3. Add required ML, notebook-execution, and interactive notebook kernel dependencies to the project's `pyproject.toml` and synchronize its `uv` environment and lockfile. Users commit their project files and `uv.lock` to Git.
4. Initialize project-local DVC metadata and configure local DVC storage, MLflow tracking/artifact storage, and durable workflow-state storage. Remote backend choices remain configurable.
5. Generate explicit settings or prompts for raw-data paths/permissions, agent adapter/authentication, and the mechanism for presenting and recording approvals. Authentication and experiment-specific choices remain explicit setup steps; initialization does not authorize data access or execution. Keep credentials outside committed configuration.

After initialization, users register existing raw data, including approved sources outside the repository, and resolve experiment-specific inputs before dependent work begins. Existing inputs are snapshotted and versioned without requiring external acquisition.

The harness repository's root `pyproject.toml` must define its build system, package metadata, supported Python versions, dependencies, and `agentic-ml` CLI entrypoint. Package the `src/agentic_ml/` implementation, initialization templates, and default runtime guidance. Load resources from the installed package without relying on a source checkout. The Python import name remains `agentic_ml`; the distribution name and actual GitHub URL require implementation decisions.

The project lockfile records the resolved harness Git revision and library versions. Harness upgrades explicitly change the declared full commit SHA and project lockfile, creating a new environment identity; package version alone does not identify Git revisions. Resumed runs use the preserved compatible configuration and instruction bundle. The harness repository's own lockfile is for product development and does not replace the experiment project's environment record.

### Developer experiment inputs

Developers provide two complementary inputs: a Markdown experiment brief describing intent and constraints, and a YAML configuration defining the allowed algorithms and hyperparameter search spaces. These inputs are distinct from the resolved `ExperimentSpec` submitted for execution.

Store these as `experiments/<name>/experiment.md` and `search-space.yaml` in the user repository. An adjacent `experiment.yaml` identifies notebook entrypoints, data references, feature pipeline components and parameters, and execution settings; it does not replace the brief or expand the search space. A project-root `project.yaml` holds project-wide environment, tracking, storage, agent, guidance settings, and user-supplied component declarations. Relative paths in these declarative inputs resolve against the experiment repository root; notebook working directories are explicitly recorded. The schemas and CLI/API commands beyond the selected `agentic-ml init` interface require further design.

The Markdown brief uses recognizable sections with natural-language guidance for:

- Dataset location and target variable.
- Task type, initially classification or regression for tabular experiments.
- Features to include or exclude, or explicit delegation of feature selection to the agent; include information-availability and leakage constraints.
- Evaluation metric and optimization direction, or delegation to the agent to propose them.
- Evaluation split strategy and constraints, including time or group boundaries where applicable.
- Algorithm mode: **use** a specified algorithm, **select** an algorithm from a declared allowed set, or **compare** every algorithm in that set.
- Trial counts, runtime limits, and other experiment budgets.

Example developer brief:

```markdown
# Experiment: Predict customer churn

## Data
Dataset: ./data/customers.parquet
Target: churned
Task: classification

## Features
Choose suitable features.
Exclude customer_id and information unavailable at prediction time.

## Evaluation
Propose a metric appropriate for an imbalanced target and its direction.
Use a time-based split on signup_date.

## Algorithms
Compare all classification algorithms declared in ./experiments/churn/search-space.yaml.

## Budget
Run at most 50 hyperparameter trials per algorithm.
```

Before integrated agent support, developers supply experiment decisions through the brief and configuration files, optionally prepared with an external coding assistant. The harness validates these inputs and records the effective, versioned plan, including supplied decisions, defaults, source references, input checksums, and approval evidence, before dependent execution. Unresolved delegated choices and ambiguous or conflicting requirements block affected execution; delegated decisions require approval before use. The resolved plan identifies the allowed algorithm set, selected features, metric and direction, split protocol, and budgets as those capabilities are introduced.

For this toolkit version, experiment approvals use explicit scoped
unauthenticated records under
[US-03-SC-01](../../plans/milestone-1-us-03.md#us-03-sc-01--unauthenticated-experiment-approvals-2026-10-31).
Reviewer labels are self-declared; workspace writers can fabricate records or
rewrite approval history. Authentication is deferred. Existing harness development
and testing approval gates remain unchanged. Plan/decision matching and missing,
stale or revoked record checks still apply; a record grants no implicit execution
or data access.

Milestone 4 adds harness-managed agent proposals and iteration. The agent proposes delegated decisions and records its reasoning; those proposals use the same harness validation, plan recording, and applicable problem-definition and evaluation approval gates before use.

### Development and runtime agent instructions

Use `AGENTS.md` for coding agents and ML experiment agents, with separate repository ownership and an explicit audience in each file. Ship default runtime guidance as resources in the installable harness distribution; the paths below identify their locations in the harness source repository.

| Instruction location | Audience and scope |
|---|---|
| Harness repository `AGENTS.md` | Harness development conventions |
| Harness `src/agentic_ml/AGENTS.md` and targeted component files | Coding agents implementing and maintaining the harness; component responsibilities, invariants, relevant contracts, and verification guidance |
| Harness `runtime_guidance/AGENTS.md` | Packaged shared scientific and operational practices for experiment agents |
| Harness `runtime_guidance/{data,features,modeling}/AGENTS.md` | Packaged task-specific practices for data assessment, feature engineering, and training/tuning |
| Experiment repository `AGENTS.md` | Project development conventions; excluded from the harness runtime loader, but an external assistant may load it independently |
| Experiment repository `runtime_guidance/` (optional) | Project-authored runtime practices, selected only through an explicit configured mapping |

Add deeper development files only where a component needs distinct instructions. Keep shared rules in their common parent and load task-specific runtime guidance only when relevant.

The runtime instruction loader must:

1. Select packaged shared/task-specific guidance and any configured project guidance through an explicit task-to-guidance mapping. Record source ownership, package version or project path, and load order; the filename alone does not activate instructions. Neither repository's development files are automatically included by the harness runtime loader. This restriction does not assert control over instructions independently loaded by an external assistant.
2. Assemble shared guidance before task-specific guidance. Task-specific instructions may specialize shared practices within the experiment's constraints; incompatible requirements require clarification before affected work begins rather than silent override.
3. Keep input authority explicit: runtime guidance describes how to work, the resolved experiment brief defines objectives and experiment-specific constraints, and YAML defines allowed algorithms and hyperparameter boundaries. Guidance cannot broaden data access, bypass approval gates, change evaluation criteria, or expand the search boundary. Harness-enforced policies apply to every task.
4. Snapshot the exact contents, paths, versions/checksums, and loading order of all harness-supplied runtime guidance when the experiment plan is resolved. Preserve the instruction bundle with run lineage and use it for subsequent tasks and resumed execution in that experiment.
5. Treat adoption of changed runtime guidance as a new versioned experiment configuration subject to the existing gates. Record conflicting instructions as a validation error or clarification request before dependent execution.

The preserved bundle identifies what the harness supplied, not the assistant's complete instruction context. Record additional instructions, session configuration, and assistant identity/version where observable, and explicitly record capture limitations. Interactive use presents the preserved bundle for the developer/assistant to consume; managed adapters must demonstrate delivery of the referenced bundle. Neither mode claims complete prompt capture or deterministic reproduction of assistant reasoning. Conflicts visible to the harness block affected execution; unavailable context cannot be certified conflict-free.

Runtime instruction files contain reusable practices. Dataset locations, targets, chosen metrics, budgets, and algorithm search spaces remain in the experiment brief, resolved plan, and YAML configuration. Executable validation and access controls enforce these constraints independently of agent compliance with Markdown instructions.

### Algorithm and hyperparameter configuration

The YAML configuration references supported algorithm identifiers from the project's combined built-in and user-supplied component registry. It separates fixed parameters from tunable parameters and supports categorical choices, integer ranges, and floating-point ranges. Numeric ranges declare minimum and maximum bounds and a linear (raw-value) or logarithmic sampling scale.

```yaml
schema_version: "0.1"
algorithms:
  random_forest_classifier:
    fixed:
      random_state: 42
    search:
      n_estimators:
        type: integer
        min: 100
        max: 1000
        scale: linear
      max_depth:
        type: categorical
        choices: [null, 5, 10, 20, 40]
      min_samples_leaf:
        type: integer
        min: 1
        max: 20
        scale: linear

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

Configuration rules:

- The YAML is a **hard allowed boundary for the current experiment**, not an initial space the agent may expand. The brief may narrow that boundary but cannot expand it.
- Fixed parameters retain their declared values. Search parameters may take only declared choices or values within their inclusive bounds. Integer ranges produce integers; logarithmic ranges require strictly positive bounds.
- The harness validates algorithm/task compatibility, parameter names and types, nonempty choices, ordered bounds, and parameter combinations before execution. Initial configurations should use mutually compatible combinations; a conditional-parameter schema is deferred.
- Parameters omitted from the YAML use registry-defined defaults, recorded with the adapter/library version in the resolved run configuration. Omission does not authorize the agent to tune them.
- Every candidate, including candidates submitted through custom code or notebooks, is subject to the same boundary validation. Invalid candidates are rejected before training.
- Search-space definitions specify where to search; the resolved trial and runtime budgets specify how much work may occur. Comparing all algorithms does not require exhaustively enumerating every parameter combination.
- The agent may recommend new algorithms, choices, ranges, or fixed values based on evidence. It records these recommendations for a subsequent experiment without modifying the current inputs or expanding the current run. A developer-adopted revision creates a new versioned experiment configuration subject to the existing gates.
- Preserve the original Markdown, YAML, their versions/checksums, the resolved plan, and effective parameters with run lineage so that delegated decisions and boundary compliance are auditable.

### Resolved experiment example

```yaml
schema_version: "0.1"
experiment:
  id: experiment-001
  task_type: classification
  hypothesis: "A neural network improves macro F1 over baseline"
dataset:
  uri: data/training.parquet
  version: sha256:...
  target: label
  split_manifest: splits/v1.json
model:
  framework: pytorch
  entrypoint: experiments/image-classification/notebooks/03_model_development.ipynb
  parameters:
    hidden_layers: [128, 64]
    learning_rate: 0.001
    batch_size: 128
    epochs: 50
evaluation:
  primary_metric: f1_macro
  direction: maximize
  baseline_run_id: baseline-001
  min_relative_improvement: 0.03
  protected_test_set: true
resources:
  accelerator: gpu
  gpu_count: 1
  max_runtime_minutes: 30
  max_memory_gb: 16
reproducibility:
  seed: 42
  repetitions: 3
  experiment_git_revision: "<experiment-repository-commit>"
  source_snapshot: "sha256:<notebook-and-code-snapshot>"
  harness_version: "<installed-version>"
  harness_repository_url: "https://github.com/OWNER/HARNESS-REPO.git"
  harness_git_commit: "<full-harness-commit-sha>"
  harness_build_identity: "sha256:<distribution-hash-if-available>"
  project_lockfile: uv.lock
  project_lockfile_checksum: "sha256:<lockfile-hash>"
governance:
  phase: model_development
  approval_required_to_advance: true
```

