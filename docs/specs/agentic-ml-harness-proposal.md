# Agentic ML Development Harness — Architecture Proposal

**Version:** 0.10
**Status:** Proposed specification; ADR-001 accepted; ADR-007 installation decisions accepted
**Date:** 2026-10-27

## 1. Executive Summary

Build an agent-independent machine learning development harness for tabular ML and deep learning. Within the installed package, a workflow orchestrator coordinates AI coding assistants and specialized ML agents; distinct execution and evaluation components independently execute, validate, and track experiments. Development is supervised: agents may iterate within approved phases and budgets, while developers approve phase transitions and expanded data-access scope.

The harness is a versioned Python dependency installed into a separate user experiment repository. That repository is the unit users own, review, version, and share: it contains experiment briefs, configuration, agent-generated notebooks and Python code, and data-versioning metadata. Notebooks are the primary user interface for inspecting, running, and refining experiments; the harness provides reusable capabilities and independent execution and evaluation controls.

A central design principle is **hierarchical closed-loop ML development**:

- **Inner loop — model improvement:** feature engineering, training, hyperparameter optimization, and evaluation.
- **Outer loop — data improvement:** data gap diagnosis, iterative acquisition, extraction, validation, dataset versioning, and retraining.

## 2. Scope and Design Decisions

| Dimension | Decision |
|---|---|
| Orchestration | Distinct orchestration and execution/evaluation components within the installed harness package |
| Agent integrations | Standardized adapters for coding assistants and specialized agents |
| ML frameworks | Initial scikit-learn, LightGBM, and PyTorch; extensible |
| Package management | Use `uv` for Python dependency management, lockfiles, and virtual environments |
| Initial distribution | Install the Python package directly from its GitHub repository using `uv`, pinned to a full Git commit SHA; package-registry distribution is future work |
| CLI and Python imports | Use `agent-ml` as the installed CLI name and retain `agentic_ml` as the Python import/package directory name |
| Repository boundary | Separate harness product repository and user experiment repositories; consume the harness as a versioned Python dependency through its public API and CLI |
| Jupyter notebooks | Agent-generated notebooks in the user experiment repository are the primary experiment interface; support interactive use and automatic harness-managed execution |
| Model types | Tabular classification/regression and deep learning |
| Autonomy | Supervised with developer approvals at phase boundaries |
| Data | Extraction, EDA, feature engineering, and iterative acquisition are first-class |
| Execution | Local subprocesses for the proof of concept; Ray planned for later distributed and parallel execution; container/GPU backends incrementally |
| Experiment tracking | MLflow for runs, parameters, metrics, model artifacts, and experiment comparisons |
| Data versioning and pipelines | DVC for dataset and derived-data versioning, dependency tracking, and reproducible pipelines; Git versions DVC metadata and pipeline definitions |
| Agent instructions | Targeted `AGENTS.md` files in separate development and runtime guidance trees; runtime loading is explicit and versioned |
| Experiment guidance | Developer-authored Markdown brief plus versioned YAML algorithm and hyperparameter boundaries |
| Search autonomy | Agent searches only within declared boundaries; expansions are recommendations for subsequent experiments |
| Deployment | Outside initial scope |

### Principles

1. Agent and ML-framework independence through versioned interfaces.
2. Explicit separation of planning/delegation, execution, evaluation, and approval.
3. Independent, evidence-based validation; agent claims alone never establish success.
4. Reproducibility, provenance, and data-to-model lineage by design.
5. Budgeted, interruptible, resumable closed loops.
6. Controlled data access and protected evaluation datasets.
7. Extensible operations: standardized tasks plus sandboxed custom code.

## 3. Architecture

```mermaid
flowchart TB
    U[Developer / Data Scientist]

    subgraph H["Installed agentic-ml Package — Public Python API and CLI"]
        O[Workflow Orchestrator]
        G{Approval Service}
        A[Agent Integration Layer<br/>Coding Assistant and Specialized ML Adapters]

        subgraph R["Execution and Evaluation"]
            X[Managed Execution<br/>Data, Features, Training, and Tuning]
            E[Independent Evaluation]
        end
    end

    subgraph P["User Experiment Project"]
        N[Notebooks and Experiment Code]
        C[Brief, Configuration, and Custom Components<br/>Supplied Models and Preprocessors]
    end

    U --> O
    O -->|Request phase or scope approval| G
    U -->|Approve, revise, or reject| G
    G -->|Recorded decision| O
    O -->|Delegate within approved scope| A
    U -->|Inspect, edit, and run| N
    A -->|Generate and revise authorized code| N
    C -->|Inputs and component references| N
    C -->|Resolve plan and boundaries| O

    O -->|Authorize managed runs| X
    N -->|Invoke within approved scope| X
    X -->|Run artifacts| E
    E -. Development evidence or final review results .-> O
    X <-->|Versioned data and pipeline outputs| D[(DVC Storage)]
    X -->|Runs, snapshots, and model artifacts| M[(MLflow Tracking and Artifacts)]
    E -->|Evaluation results| M
    D -. Dataset and pipeline references .-> M
```

The installed harness package supplies orchestration, agent integration, approval handling, execution, and evaluation. Separation of orchestration from execution/evaluation means distinct component responsibilities within the package, rather than separate installations or repositories. Agent adapters connect to coding assistants or external agent services; those external systems need not run inside the package. Package boundaries show implementation ownership, not process or deployment boundaries.

These capabilities operate in the selected experiment project's environment using its configuration and project-associated state/storage. The orchestrator coordinates approved work; execution independently enforces boundaries, and evaluation assesses results. Project-owned models and preprocessors run through harness interfaces alongside built-in components. Interactive notebook use follows the same access rules and cannot establish acceptance by itself. Protected holdout access is reserved for independent final evaluation; its feedback cannot drive development iterations. Harness manifests link DVC and MLflow records to project snapshots, component identities, approvals, and durable project-associated workflow state.

### Component responsibilities

| Component | Responsibilities |
|---|---|
| Workflow orchestrator | Plans phases, delegates tasks, maintains durable state, controls iterations, enforces approvals and budgets, resumes work |
| Agent integration | Capability discovery, structured task/result exchange, cancellation, CLI/SDK/tool adapters |
| Data extraction engine | Source discovery, approved queries, ingestion, snapshots, schema checks, lineage |
| Data acquisition planner | Diagnose gaps, propose additional samples/labels/sources, estimate costs and expected benefit |
| Data acquisition executor | Enforce recorded acquisition authorization, execute acquisition, validate and version results |
| EDA/validation | Profiling, missingness, class balance, anomalies, leakage diagnostics, split strategy |
| Feature engineering | Propose/fit/transform/select features, version pipelines, evaluate feature sets |
| Experiment runner | Backend-independent submission, status, cancellation, resources, logs, artifacts, and checkpoints; local execution initially, Ray-backed execution later |
| Framework adapters | Standardized and custom training entrypoints for scikit-learn, LightGBM, PyTorch |
| Evaluation engine | Metrics, baseline comparisons, scientific validity, robustness, reproducibility |
| Tracking and artifact store | MLflow records runs, parameters, metrics, and model artifacts; links to DVC dataset/pipeline versions and harness manifests for complete lineage |
| Data versioning and pipelines | DVC tracks source and derived datasets, dependencies, stage outputs, and reproducible pipeline definitions; integrates with harness execution |
| Approval service | Phase and acquisition approvals, authorization scope, audit records |

### Harness and experiment project boundary

The harness repository contains reusable execution, evaluation, tracking, agent integration, orchestration, approval handling, templates, and default runtime guidance. Each user experiment repository contains objectives, notebooks, supplied and generated code, configuration, and versioning metadata. One experiment repository may contain multiple related experiments sharing project code and dependencies.

```mermaid
flowchart LR
    subgraph H["Harness repository"]
        direction TB
        HC["Reusable Python package<br/>src/agentic_ml/<br/>Orchestration, Adapters, Approvals, Execution, and Evaluation"]
        HR["Templates and runtime guidance<br/>templates/ · runtime_guidance/"]
        HD["Package metadata and tests<br/>pyproject.toml · tests/"]
    end

    subgraph U["User experiment repository"]
        direction TB
        UC["Project configuration<br/>pyproject.toml · uv.lock · project.yaml"]
        UP["Custom models and preprocessing<br/>src/churn_experiments/"]
        UE["Experiment definitions and notebooks<br/>experiments/baseline-comparison/<br/>experiment.md · search-space.yaml<br/>experiment.yaml · notebooks/ · helpers/"]
    end

    H -->|Install agentic-ml package| U
```

Directory contents are illustrative subsets; Section 12 provides fuller layouts. The installation arrow represents a pinned GitHub package dependency installed into the user project's Python environment.

Experiment agents operate within the experiment repository and use the installed harness through its public Python API and CLI. Routine experiment work does not modify the harness installation or source repository and must not require a neighboring harness checkout. Changes to shared harness capabilities follow a separate software-development review process.

The orchestrator operates on an explicitly selected experiment project and environment. Durable workflow state and run artifacts are stored in configured locations associated with that project, independently of the harness source tree.

## 4. Hierarchical Closed-Loop Workflow

```mermaid
flowchart TD
    A[Define Objectives, Components, and Boundaries] --> B[Developer Approves Plan]
    B --> C["Execute Authorized Phase (see Phase Descriptions Below)"]
    C --> D[Independently Validate Phase Evidence]
    D --> E[Developer Reviews Phase]
    E -->|Advance| F[Next Phase]
    F --> C
    E -->|Revise| G[Revise Within Approved Scope]
    G --> C
    E -->|Approve Final Model| H[Complete]
    E -->|Reject or Stop| I[Preserve Results and Stop]
```

The diagram summarizes the phase cycle. The individual phases are:

1. **Problem definition:** Define the objective, target, metrics, data sources, allowed algorithms, supplied components, constraints, and budgets. Approve the task contract and plan.
2. **Data extraction and EDA:** Obtain and version data, inspect its quality and distributions, and establish training/validation/test splits. Approve the dataset assessment and split protocol.
3. **Feature engineering:** Use supplied preprocessing or develop transformations and feature sets. Fit stateful preprocessing only on training data. Review the validated pipeline and lineage.
4. **Baseline modeling:** Train simple, reproducible reference models. Approve baseline results for later comparisons.
5. **Model development:** Train and compare candidate models, including user-supplied algorithms, and improve them within approved boundaries. Review candidate evidence.
6. **Optimization:** Tune hyperparameters within the declared search space and budgets. Approve the optimization summary and candidate for final evaluation.
7. **Final evaluation:** Evaluate the selected model on the protected holdout, check robustness and reproducibility, and produce the final report. Approve or reject the model.

**Each phase transition requires approval.** Agents can iterate within an approved phase. Valid existing artifacts can support skipping a phase when that is approved in the plan. Section 5 defines the gate evidence for each phase.

Data acquisition is an activity that can trigger a return to earlier phases, rather than an eighth phase. Supplied components and authorized data acquisition fit within “Execute Authorized Phase”; their detailed requirements appear in Sections 6–8. The following rules apply:

- **Phases:** Initial plan approval completes problem definition. Execution then follows the configured phases in Section 5: data extraction and EDA → feature engineering → baseline modeling → model development → optimization → final evaluation. Each phase approval authorizes entry to the next phase and its recorded scope.
- **Iteration:** Agents may iterate within the current approved phase, component permissions, parameter boundaries, access scope, and budgets without approval for every run. Evidence is independently validated against phase-specific requirements before developer review; only sufficient evidence permits advancement.
- **Scope changes:** Phase returns, expanded permissions, and changes to immutable components require authorization before execution. Authorized changes are recorded durably; changes to immutable code, allowed algorithms, or data-access scope create a new versioned experiment configuration. Acquisition requires recorded authorization covering its source, strategy, and limits, followed by authorized validation/EDA and downstream work.
- **Final evaluation:** Protected-test evaluation occurs only in its authorized final phase. Its results cannot feed feature, model, or acquisition improvement loops, so the revision arrow does not apply to protected-test feedback. Unsuccessful final evaluation ends in rejection or review; any further development requires a separately approved evaluation protocol that preserves holdout protection. Completion requires developer approval of successful final evaluation.

**Inner loop:** feature engineering → training/tuning → evaluation → evidence-based revision.  
**Outer loop:** diagnose data limitations → propose acquisition → approve where required → acquire/validate/version → retrain and compare.

Both loops must terminate on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or developer cancellation. Budget exhaustion preserves evidence and produces a reviewable status.

### Notebook-centered user workflow

1. Install `uv` and Git, create a separate user repository and Python project, install the harness from a pinned GitHub commit, and run `uv run agent-ml init` to add experiment scaffolding and configure its environment.
2. Configure local data access, tracking, storage, and an agent adapter; optionally register supplied algorithms and preprocessors with their parameter specifications and modification permissions. Write the experiment brief, feature pipeline configuration, and search-space configuration.
3. Ask the agent to generate readable notebooks that invoke supplied or built-in components. Generate new experiment-specific implementations or helper code only as needed and authorized.
4. Inspect the notebooks and approve the resolved task contract, phase plan, component selection, evaluation protocol, access scope, and budgets through the applicable gates before dependent execution. Validate component interfaces, parameters, and evaluation compatibility before training.
5. Open the notebooks in JupyterLab, execute approved work, and inspect results. The agent may also execute and revise notebooks automatically within the current approved phase, component permissions, parameter boundaries, and budgets. Phase returns and scope changes require authorization; changes to immutable supplied code require approval and a new versioned experiment configuration.
6. Record experiments through harness-managed execution of saved notebook and code snapshots, followed by independent evaluation. Interactive exploration alone does not establish acceptance.
7. Review evidence at every phase boundary and approve entry to the next phase or request changes. Review final evaluation separately to approve or reject the final model. Preserved state supports interruption and resumption.

Reviewing every notebook edit is optional unless configured as an additional gate; phase approvals and scope controls remain mandatory.

## 5. Standard Development Phases and Gates

| Phase | Activities | Required gate evidence |
|---|---|---|
| 1. Problem definition | Objective, target, metrics, sources, budgets, constraints | Approved ML task contract |
| 2. Data extraction and EDA | Source discovery, snapshots, profiling, quality, split strategy | Approved dataset assessment and split protocol |
| 3. Feature engineering | Transformations, selection, fitted pipelines, baseline feature sets | Validated feature pipeline and lineage |
| 4. Baseline modeling | Train reproducible simple baselines | Approved baseline results |
| 5. Model development | Candidate architectures, training, iterative improvement | Candidate comparison and experiment evidence |
| 6. Optimization | Hyperparameter search within budgets | Approved optimization summary |
| 7. Final evaluation | Protected holdout, robustness, reproducibility, reporting | Final model approval/rejection |

Phases may be configured or skipped when valid preexisting artifacts are supplied. Agents can iterate within approved phase scope; phase transitions require approval. Additional data acquisition may trigger an explicit scope approval and a return to earlier phases.

## 6. Data Extraction and Iterative Acquisition

### Data extraction requirements

- Connect to local CSV/Parquet, SQL, and object storage initially; add APIs later.
- Discover source schemas and metadata without unrestricted data exposure.
- Execute approved extraction queries and sampling plans.
- Version extracted datasets with DVC; capture source identity, query, parameters, extraction time, checksums, and permissions metadata in associated manifests. Commit DVC metadata to Git; store dataset content in the DVC cache and configured remote storage.
- Validate schema, row counts, nulls, types, duplicates, and other configured quality rules.
- Enforce least-privilege access, source allowlists, network restrictions, and cost/record limits.

### Acquisition strategies

- Additional observations from approved sources.
- Targeted sampling for underrepresented classes or data slices.
- Additional feature columns or related datasets.
- Human or external labeling workflows.
- Active learning: select informative unlabeled examples.
- Data augmentation and synthetic data, explicitly labeled and tracked as distinct from observed data.

### Acquisition proposal contract

```yaml
proposal:
  id: acquisition-001
  reason: underrepresented_class
  evidence:
    affected_class: minority_class
    current_samples: 250
    observed_recall: 0.61
  acquisition:
    strategy: targeted_sampling
    source: approved_training_database
    target_additional_samples: 500
  expected_benefit:
    hypothesis: improve_minority_class_recall
    metric: recall
  constraints:
    max_records: 500
    max_runtime_minutes: 15
  approval:
    required: true
```

The predicted benefit is a hypothesis, not a guarantee. Compare before/after training with consistent evaluation protocols. Never use protected final-test feedback to guide acquisition. Changes to evaluation protocols require separate approval.

## 7. Feature Engineering

The feature engineering engine must:

- Propose and execute missing-value handling, encoding, scaling, feature construction, selection, and dimensionality reduction.
- Support domain-specific transformations and custom code.
- Track feature definitions, fitted preprocessors, parameters, versions, and dependencies.
- Fit stateful transformations only on training data; apply unchanged to validation/test data.
- Compare candidate feature sets against a fixed baseline and split protocol.
- Support deep-learning preprocessing, image augmentation, tokenization, and PyTorch datasets where relevant.
- Make transformations reusable for inference without requiring model deployment in the initial release.

Experiment-specific transformations belong in the experiment repository's notebooks or helper modules. Code shared across experiments in that repository belongs in its own Python package. Generic feature-engineering capabilities belong in the harness package; promoting project code into the harness is a separate development change.

Feature preparation supports user-supplied stateless transformations and stateful preprocessors. Stateful preprocessors expose separate fitting and transformation operations: fitting receives only the approved training partition, and the fitted state is reused unchanged for validation, test, and inference.

Users may require a supplied preparation pipeline or explicitly delegate selection and modification to the agent. The resolved feature plan records component order, effective parameters, input/output schemas, fitting scope, and whether agent modifications are permitted.

Preserve the preparation code, fitted state, dependencies, and output feature schema as run artifacts. Supplied pipelines must satisfy the same leakage, reproducibility, and lineage checks as generated pipelines.

## 8. Interfaces and Contracts

All contracts should have versioned JSON Schemas and typed Python models. These conceptual interfaces require further design for asynchronous operations, idempotency, error handling, and authorization.

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
    def diagnose(self, dataset: "DatasetRef", evaluation: "EvaluationReport") -> "DataGapReport": ...
    def propose(self, gaps: "DataGapReport") -> "DataAcquisitionProposal": ...

class DataAcquisitionExecutor(Protocol):
    def execute(self, proposal: "DataAcquisitionProposal", authorization: "ApprovalRecord") -> "DatasetRef": ...

class FeatureEngineeringAdapter(Protocol):
    def propose(self, dataset: "DatasetRef", context: "FeatureContext") -> "FeaturePlan": ...
    def transform(self, dataset: "DatasetRef", plan: "FeaturePlan") -> "FeatureSetRef": ...
    def evaluate(self, feature_set: "FeatureSetRef") -> "FeatureEvaluationReport": ...

class ExperimentRunner(Protocol):
    def submit(self, spec: "ExperimentSpec") -> str: ...
    def status(self, run_id: str) -> "RunStatus": ...
    def cancel(self, run_id: str) -> None: ...
    def artifacts(self, run_id: str) -> list[str]: ...

class ModelAdapter(Protocol):
    def train(self, context: "TrainingContext") -> Any: ...
    def predict(self, model: Any, data: Any) -> Any: ...
    def save(self, model: Any, path: str) -> None: ...
    def load(self, path: str) -> Any: ...

class Evaluator(Protocol):
    def evaluate(self, run_id: str, criteria: "AcceptanceCriteria") -> "EvaluationReport": ...

class ApprovalService(Protocol):
    def request(self, phase_id: str) -> str: ...
    def decide(self, approval_id: str, decision: str) -> None: ...
```

### Primary contracts

| Contract | Key fields |
|---|---|
| `MLTaskSpec` | Objective, target, task type, data, feature guidance, delegated decisions, algorithm mode, metrics, budgets, policies, source brief reference |
| `ExperimentProjectConfig` | Schema version, project root and environment reference, tracking/storage/state locations, access policy references, agent adapter, explicit project guidance mapping, project-local component declarations |
| `ComponentSpec` | Identifier, kind, Python entrypoint, interface version, supported tasks/prediction outputs where applicable, parameter types/defaults/constraints, code or dependency identity, agent modification permission |
| `ExperimentConfig` | Schema version, experiment identifier, brief/search-space references, notebook entrypoints, data references, feature pipeline component references and parameters, working directory, execution settings; resolved into the approved `ExperimentSpec` |
| `RuntimeInstructionBundle` | Shared/task-specific guidance snapshots, audience, task mapping, ordered source paths, versions/checksums |
| `SearchSpaceSpec` | Schema version, registered algorithm identifiers, fixed parameters, typed choices/ranges, scales, configuration checksum |
| `WorkflowPlan` | Phases, dependencies, gates, iteration limits |
| `AgentTask` / `AgentResult` | Task scope, context, tools, proposed changes, outputs |
| `ExtractionSpec` / `DatasetRef` | Source, query, snapshot, checksum, schema, lineage |
| `DataGapReport` / `DataAcquisitionProposal` | Evidence, acquisition hypothesis, scope, cost, approval |
| `FeaturePlan` / `FeatureSetRef` | Ordered component references, effective parameters, input/output schemas, fitting scope, modification permissions, fitted state, versions, provenance |
| `ExperimentSpec` / `ExperimentResult` | Project/experiment identity, model, data, notebook/code snapshots, experiment Git revision, harness repository URL/full commit SHA/package version, build identity where available, environment/lockfile identity, effective parameters, source configuration references, runtime instruction bundle reference, resolved decisions, resources, metrics, artifacts |
| `EvaluationReport` | Metrics, validity checks, baseline comparison, evidence |
| `ApprovalRecord` | Reviewer, scope, decision, timestamp, audit trail |

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

Component parameter specifications define valid types, defaults, and constraints. Experiment search spaces define the narrower values agents may explore. Declaring a component does not automatically authorize its use or parameter tuning. Feature pipeline parameters are fixed by the approved feature plan; changes require the applicable feature-phase authorization and a recorded plan revision.

Run lineage preserves component declarations, exact project-code snapshots or pinned dependency identities, effective parameters, and fitted artifacts. Component code changes authorized within a phase are captured in each run's source snapshot.

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

uv run agent-ml init
uv run jupyter lab
```

The repository URL and commit SHA are placeholders. These commands specify the intended product interface; the harness and CLI still require implementation. There is no separate initializer-tool installation: `agent-ml init` runs from the harness already installed in the project's `.venv`.

`agent-ml init` must:

1. Add project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and any project-package scaffolding to the existing user repository.
2. Preserve existing files and report conflicts rather than silently overwriting them. Preserve the declared harness Git dependency and pinned commit.
3. Add required ML, notebook-execution, and interactive JupyterLab dependencies to the project's `pyproject.toml` and synchronize its `uv` environment and lockfile. Users commit their project files and `uv.lock` to Git.
4. Initialize project-local DVC metadata and configure local DVC storage, MLflow tracking/artifact storage, and durable workflow-state storage. Remote backend choices remain configurable.
5. Generate explicit settings or prompts for raw-data paths/permissions, agent adapter/authentication, and the mechanism for presenting and recording approvals. Authentication and experiment-specific choices remain explicit setup steps; initialization does not authorize data access or execution. Keep credentials outside committed configuration.

After initialization, users register existing raw data, including approved sources outside the repository, and resolve experiment-specific inputs before dependent work begins. Existing inputs are snapshotted and versioned without requiring external acquisition.

The harness repository's root `pyproject.toml` must define its build system, package metadata, supported Python versions, dependencies, and `agent-ml` CLI entrypoint. Package the `src/agentic_ml/` implementation, initialization templates, and default runtime guidance. Load resources from the installed package without relying on a source checkout. The Python import name remains `agentic_ml`; the distribution name and actual GitHub URL require implementation decisions.

The project lockfile records the resolved harness Git revision and library versions. Harness upgrades explicitly change the declared full commit SHA and project lockfile, creating a new environment identity; package version alone does not identify Git revisions. Resumed runs use the preserved compatible configuration and instruction bundle. The harness repository's own lockfile is for product development and does not replace the experiment project's environment record.

### Developer experiment inputs

Developers provide two complementary inputs: a Markdown experiment brief describing intent and constraints, and a YAML configuration defining the allowed algorithms and hyperparameter search spaces. These inputs are distinct from the resolved `ExperimentSpec` submitted for execution.

Store these as `experiments/<name>/experiment.md` and `search-space.yaml` in the user repository. An adjacent `experiment.yaml` identifies notebook entrypoints, data references, feature pipeline components and parameters, and execution settings; it does not replace the brief or expand the search space. A project-root `project.yaml` holds project-wide environment, tracking, storage, agent, guidance settings, and user-supplied component declarations. Relative paths in these declarative inputs resolve against the experiment repository root; notebook working directories are explicitly recorded. The schemas and CLI/API commands beyond the selected `agent-ml init` interface require further design.

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

Before execution, the agent resolves delegated choices into a structured plan, records its reasoning, and submits that plan through the existing problem-definition and evaluation gates. Ambiguous or conflicting requirements must be resolved before affected runs begin. The resolved plan identifies the allowed algorithm set, selected features, metric and direction, split protocol, and budgets.

### Development and runtime agent instructions

Use `AGENTS.md` for coding agents and ML experiment agents, with separate repository ownership and an explicit audience in each file. Ship default runtime guidance as resources in the installable harness distribution; the paths below identify their locations in the harness source repository.

| Instruction location | Audience and scope |
|---|---|
| Harness repository `AGENTS.md` | Harness development conventions |
| Harness `src/agentic_ml/AGENTS.md` and targeted component files | Coding agents implementing and maintaining the harness; component responsibilities, invariants, relevant contracts, and verification guidance |
| Harness `runtime_guidance/AGENTS.md` | Packaged shared scientific and operational practices for experiment agents |
| Harness `runtime_guidance/{data,features,modeling}/AGENTS.md` | Packaged task-specific practices for data assessment, feature engineering, and training/tuning |
| Experiment repository `AGENTS.md` | Project development conventions; not automatically loaded as runtime experiment guidance |
| Experiment repository `runtime_guidance/` (optional) | Project-authored runtime practices, selected only through an explicit configured mapping |

Add deeper development files only where a component needs distinct instructions. Keep shared rules in their common parent and load task-specific runtime guidance only when relevant.

The runtime instruction loader must:

1. Select packaged shared/task-specific guidance and any configured project guidance through an explicit task-to-guidance mapping. Record source ownership, package version or project path, and load order; the filename alone does not activate instructions. Neither repository's development files are automatically included in experiment-agent runtime context.
2. Assemble shared guidance before task-specific guidance. Task-specific instructions may specialize shared practices within the experiment's constraints; incompatible requirements require clarification before affected work begins rather than silent override.
3. Keep input authority explicit: runtime guidance describes how to work, the resolved experiment brief defines objectives and experiment-specific constraints, and YAML defines allowed algorithms and hyperparameter boundaries. Guidance cannot broaden data access, bypass approval gates, change evaluation criteria, or expand the search boundary. Harness-enforced policies apply to every task.
4. Snapshot the exact contents, paths, versions/checksums, and loading order of all applicable runtime guidance when the experiment plan is resolved. Preserve the instruction bundle with run lineage and use it for subsequent tasks and resumed execution in that experiment.
5. Treat adoption of changed runtime guidance as a new versioned experiment configuration subject to the existing gates. Record conflicting instructions as a validation error or clarification request before dependent execution.

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

## 9. Execution, Evaluation, and Governance

### Execution

- Declare dependencies separately in the harness and experiment repositories' `pyproject.toml` files and commit their respective `uv.lock` files. Execute user experiments in the selected experiment project's environment, including its installed harness version and project package.
- Support local Python subprocesses, followed by containerized and GPU execution.
- Support automatic execution of Jupyter notebooks as experiment entrypoints using `nbclient` and an `ipykernel` kernel in the experiment's `uv`-managed environment; provide JupyterLab for interactive development.
- Execute notebooks from a fresh kernel, in cell order, with explicit input parameters and a recorded working directory. Apply experiment timeouts, cancellation, resource budgets, and filesystem/network restrictions to notebook execution.
- Preserve the source notebook, supplied parameters, executed notebook with cell outputs, execution errors, and generated artifacts in the run record. Cell errors fail execution; successful notebooks remain subject to independent evaluation and protected-data rules.
- Keep experiment-specific preprocessing, models, and training logic in the experiment repository's notebooks, helpers, or project package. Both notebook and Python entrypoints import generic capabilities from the installed harness public API; they must not import through paths into the harness source checkout.
- Enforce timeouts, cancellation, experiment counts, memory/GPU quotas where supported.
- Capture logs, exit status, project environment/lockfile identity, experiment Git revision, exact executed notebook/code snapshots including uncommitted changes, harness repository URL/full commit SHA/package version, build identity where available, datasets, checkpoints, and artifacts.
- Treat unsuccessful model performance as a valid experiment result, distinct from execution failure.
- Restrict filesystem, network, and credential access for agent-generated code.
- Resolve paths against the selected experiment project and record the working directory. Explicitly authorize writable project paths, storage locations, and access to external raw data. Routine experiment execution must not modify the harness installation or source repository.

### Execution backend evolution

The proof of concept executes experiments locally through the `ExperimentRunner` interface, covering submission, status monitoring, cancellation, resource limits where supported, and artifact collection. Keep orchestration and independent evaluation separate from backend-specific scheduling and transport. Implement the local runner first; introduce additional backend abstractions when integration requires them.

Ray is the planned backend for later distributed and parallel execution. Initial Ray support will run independent experiments and hyperparameter trials in parallel. Distributing a single model-training job is a separate, subsequent capability requiring framework-specific design as needed.

Ray dependencies, integration, cluster provisioning, distributed scheduling, and distributed training are outside proof-of-concept scope. Future Ray execution must preserve the existing search boundaries, aggregate experiment budgets, approval gates, cancellation semantics, and provenance requirements. The proof of concept does not require Ray installation or a cluster to execute or validate its local workflow.

### Experiment tracking, data versioning, and pipelines

- Use **MLflow** as the experiment tracking system for Python and notebook runs. Record effective parameters, metrics, execution status, model artifacts, and references to dataset, feature, environment, and instruction provenance.
- Use **DVC** to version raw datasets, extracted snapshots, split manifests, and derived feature datasets. Use `dvc.yaml` to declare pipeline stages and their dependencies, parameters, and outputs; preserve resolved dependency/output hashes in `dvc.lock`.
- Track DVC metadata, pipeline definitions, and lockfiles in the experiment repository's Git history. Exclude dataset contents and large generated artifacts from Git. Configure DVC storage for sharing and restoring versioned data; support local storage initially and choose remote backends/access configuration during implementation.
- The workflow orchestrator retains responsibility for agent delegation, approvals, budgets, and recovery. DVC executes reproducible data and training stages under harness control; it does not replace workflow governance or independent evaluation.
- Link each MLflow run to the experiment Git revision, exact executed notebook/helper/project-code snapshots, harness repository URL/full commit SHA/package version and build identity where available, project lockfile/environment identity, DVC data/output hashes, applicable stage definitions and lockfile snapshot, and harness run identifier. Preserve uncommitted source and resolved metadata in immutable run snapshots. Record the MLflow run identifier in the harness result for bidirectional lookup.
- Keep ownership explicit: DVC manages versioned data and pipeline outputs, MLflow manages experiment records and model artifacts, and harness manifests connect both to approvals and runtime instruction bundles.
- Store executed notebook snapshots and model artifacts in configured MLflow artifact storage, versioned datasets in DVC storage, and durable workflow state in configured project-associated state storage. These locations may be local or external; preserve references and nonsecret configuration in the experiment repository and exclude generated stores from Git.
- DVC stage reuse must preserve producer provenance and remain subject to current evaluation and authorization checks. A cached stage does not establish that an experiment meets acceptance criteria.

### Notebook development and execution contract

- Use `experiments/<name>/notebooks/` in the user repository as the primary interface for data assessment, feature/baseline work, model development, and results analysis. Agents generate and revise these notebooks; users inspect, edit, and run them in JupyterLab. Python entrypoints remain available for advanced use.
- Provide numbered notebook templates for these activities; allow fewer or additional notebooks as appropriate. Include explanatory Markdown describing objectives, assumptions, generated code, results, and proposed next steps.
- Declare JupyterLab and `ipykernel` in the experiment project's dependencies or an explicitly installed interactive dependency group managed by `uv`. Include `nbclient` and `ipykernel` in the installed harness notebook-execution dependencies. Users do not need the harness development environment.
- Use an explicit parameter cell for dataset/configuration references and run identifiers. Require saved notebooks to execute from a fresh kernel in cell order with a defined working directory and locked environment; do not depend on hidden interactive state.
- Exchange artifacts across notebooks through recorded versioned references rather than variables in another notebook's kernel. Snapshot imported experiment helpers and project code with each recorded run.
- Import project-specific shared logic from the experiment repository's own Python package and generic capabilities from the installed harness. Promoting project code into the harness requires a separate development review.
- Users may execute cells interactively for exploration. Recorded experiment results require harness-managed execution of saved source snapshots and independent evaluation; successful interactive execution alone does not establish acceptance.
- Training cells submit work through harness APIs so candidate validation, budgets, approvals, and tracking apply. Interactive and automated work follow the same split, protected-test, and acquisition rules.
- Define the interactive-kernel isolation and protected-data boundary under ADR-006. API checks alone cannot constrain arbitrary Python in an unrestricted kernel. Protected test data must remain inaccessible to experiment-agent and exploratory kernels; approved final evaluation occurs through the independent evaluator.
- Record notebook runs in MLflow with the same configuration, source snapshots, dual harness/experiment identities, dataset versions, feature lineage, and environment provenance as Python entrypoints.

### Independent evaluation

1. **Execution correctness:** code completes and expected artifacts exist.
2. **Scientific validity:** split boundaries, preprocessing fitting, and leakage rules are respected.
3. **Model quality:** agreed metrics and baseline comparisons are computed consistently.
4. **Generalization/robustness:** folds, slices, or stress tests satisfy defined criteria.
5. **Reproducibility:** reruns meet explicit metric tolerances, acknowledging GPU nondeterminism where applicable.

### Workflow states

`Planned → Running → Evaluating → AwaitingApproval → Approved → NextPhase/Completed`.

Additional terminal or reviewable states: `Failed`, `Cancelled`, `BudgetExhausted`, and `NeedsReview`. A rejection or revision request returns work to an authorized phase; it does not silently bypass gates.

### Governance

- Approvals are durable, scoped, and auditable.
- New data sources, expanded permissions, changed evaluation criteria, and phase transitions require authorization.
- Protected test sets cannot be used for iterative tuning or data acquisition decisions.
- Resource limits and stopping conditions apply to both inner and outer loops.

## 10. Acceptance Criteria

| ID | Acceptance criterion |
|---|---|
| AC-01 | Two agent adapters successfully use the same task contract |
| AC-02 | End-to-end training/evaluation with scikit-learn, LightGBM, and PyTorch |
| AC-03 | Experiments support submission, monitoring, cancellation, and inspection |
| AC-04 | Each run records parameters, metrics, artifacts, and provenance in MLflow with linked harness and DVC references |
| AC-05 | Independent evaluator determines acceptance without trusting agent assertions |
| AC-06 | Agent revises experiments using structured evaluation feedback |
| AC-07 | Phase advancement is blocked without approval |
| AC-08 | Experiment-count and runtime budgets stop new work |
| AC-09 | Repeated runs satisfy specified reproducibility tolerances |
| AC-10 | Interrupted workflows resume without duplicating completed runs |
| AC-11 | Unauthorized filesystem/credential access is blocked |
| AC-12 | Final report includes model, metrics, baseline, and lineage |
| AC-13 | Leakage and protected-test violations are rejected |
| AC-14 | PyTorch supports checkpoints, cancellation, and CPU/GPU execution |
| AC-15 | Extract data from at least two source types |
| AC-16 | Restore a DVC-versioned dataset from configured storage using its recorded metadata and verify its content hashes |
| AC-17 | Detect schema mismatches and extraction failures |
| AC-18 | Agent generates and executes candidate feature transformations |
| AC-19 | Feature sets are compared on consistent validation splits |
| AC-20 | Fitted feature pipelines and outputs are reproducible |
| AC-21 | Feature transforms violating split boundaries are rejected |
| AC-22 | Model lineage traces back to features and source datasets |
| AC-23 | Agent identifies data deficiencies with recorded evidence |
| AC-24 | Agent creates a structured acquisition proposal |
| AC-25 | Unauthorized acquisition is blocked |
| AC-26 | Approved acquisition creates versioned datasets with lineage |
| AC-27 | Harness compares performance before/after acquisition |
| AC-28 | Acquisition respects cost, record, and compute budgets |
| AC-29 | Acquisition loops terminate at stopping conditions |
| AC-30 | Workflow resumes after approved acquisition with complete audit trail |
| AC-31 | Harness automatically executes a parameterized notebook from a fresh kernel and records its environment, inputs, executed outputs, and artifacts |
| AC-32 | Notebook errors, timeouts, and cancellation produce the corresponding run status; notebook runs enforce the same access, budget, lineage, and evaluation rules as Python entrypoints |
| AC-33 | Markdown guidance and YAML search spaces resolve into a versioned plan that records delegated feature, metric, and algorithm decisions |
| AC-34 | Search supports categorical choices and integer/float ranges with linear/logarithmic scales; invalid configurations and out-of-bound candidates are rejected before training |
| AC-35 | Use, select, and compare modes respect the allowed algorithm set and budgets; search-space expansion is recorded only as a recommendation for a subsequent experiment |
| AC-36 | Run lineage preserves source inputs, resolved decisions, effective defaults, and configuration versions/checksums |
| AC-37 | Runtime explicitly loads shared and relevant task-specific guidance, records the mapping and load order, and excludes development instructions from automatic runtime loading |
| AC-38 | Resumed experiments use the preserved runtime instruction bundle; conflicting guidance or attempted expansion of experiment constraints blocks affected execution |
| AC-39 | DVC reproduces declared pipeline stages with recorded dependencies and outputs; reused stages retain producer provenance and respect harness governance |
| AC-40 | MLflow run records link to the exact DVC dataset/pipeline state, experiment Git revision and source snapshot, harness repository URL/full commit SHA/package version, build identity where available, and project lockfile/environment identity |
| AC-41 | Starting with Python and local raw data, documented bootstrap steps install uv/Git, create the user Git/Python project, install the harness from a full GitHub commit SHA, and run agent-ml init to produce a locked environment, notebook templates, configuration, and local tracking/DVC/state storage without a manually maintained harness checkout |
| AC-42 | Agent-generated notebooks import the installed harness and project package and support interactive use and fresh-kernel automated execution without hidden state or paths into a harness checkout |
| AC-43 | Routine experiment generation and execution modify only the experiment repository and authorized storage; the harness installation/source remain unchanged |
| AC-44 | Each recorded run preserves exact notebook, helper, project-code, configuration, and runtime-guidance snapshots, including uncommitted source changes |
| AC-45 | On a second machine, the experiment checkout and recorded snapshots/environment/data restore the pinned GitHub harness commit and reproduce a run within declared tolerances without a manually maintained harness checkout |
| AC-46 | Interactive kernels cannot access protected test data; interactive success does not bypass phase approval or independent evaluation, and managed training enforces candidate boundaries and budgets |
| AC-47 | Installed harness guidance and explicitly configured project guidance load with recorded ownership/order; neither repository's development instructions load automatically into runtime experiment tasks |
| AC-48 | A clean-environment GitHub installation exposes the agent-ml CLI and packaged templates/runtime guidance without relying on the installer cache or source checkout at runtime |
| AC-49 | agent-ml init preserves existing project files and the pinned Git dependency, reports conflicts, and installs the notebook dependencies needed to launch JupyterLab from the project environment |
| AC-50 | A user-supplied algorithm runs, tunes, persists, restores, and undergoes independent evaluation from a separate experiment repository without harness modifications |
| AC-51 | A supplied stateful preprocessor fits only on training data; restored state reproduces validation and inference transformations |
| AC-52 | Invalid component declarations, parameter values, and incompatible prediction outputs are rejected before training |
| AC-53 | Agents cannot modify immutable supplied components without recorded developer approval |
| AC-54 | Run lineage captures component declarations, exact code snapshots or pinned dependency identities, effective parameters, and fitted artifacts |

### Reference acceptance-test datasets

- Small tabular classification dataset (scikit-learn/LightGBM).
- Tabular regression dataset (metrics and objective direction).
- Small image classification dataset (PyTorch CPU; optional GPU).
- Notebook fixtures covering successful parameterized execution, cell errors, timeouts, and cancellation.
- Negative fixtures for leakage, schema errors, missing artifacts, unauthorized access, and skipped approval gates.
- Runtime-guidance fixtures covering task selection, conflicting instructions, development/runtime separation, and resumption after source guidance changes.
- Experiment-input fixtures covering delegated decisions, all three algorithm modes, numeric/categorical search spaces, and rejected boundary violations.
- User-supplied component fixtures covering project-local and pinned-dependency implementations, model persistence/restoration, stateful and stateless preparation, training-only fitting, duplicate identifiers, incompatible interfaces/prediction outputs, parameter validation, immutable-code approval, and component lineage.
- Separate experiment-project fixtures covering pinned GitHub installation, agent-ml init and file conflicts, installed CLI/resources, generated notebooks, project-package imports, uncommitted source snapshots, interactive access boundaries, and restoration in a clean environment.

## 11. Phased Implementation Plan

| Implementation phase | Deliverables | Exit criteria |
|---|---|---|
| 1. Data and harness foundation | GitHub-installable package pinned by full commit SHA, agent-ml CLI/init, packaged templates/guidance, bootstrap documentation, project configuration and locked environment, Markdown brief resolution, YAML search-space validation, schemas, local Python/notebook execution, extraction, snapshots, validation, MLflow tracking, local DVC/state storage, public API | Clean-environment GitHub install and initialization followed by repeatable extraction/notebook execution in a separate project without agents or a manually maintained harness checkout |
| 2. EDA and feature pipelines | Profiling, split manifests, transformations, project-local registration of user-supplied stateful/stateless preparation, fitted-state persistence/restoration, DVC pipeline stages and lockfiles, lineage, feature comparison | Validated, reproducible feature artifacts, including supplied preprocessing without harness modifications |
| 3. Model experimentation | scikit-learn, LightGBM, basic PyTorch, project-local custom model registration and parameter validation, model persistence/restoration, bounded hyperparameter evaluation, algorithm use/select/compare modes, evaluation, baseline comparisons | Tabular and basic deep-learning runs tracked and assessed; supplied models run and undergo independent evaluation without harness modifications |
| 4. Agent integration | First coding-assistant adapter, project-local notebook/code generation, packaged/project runtime instruction loading and snapshots, structured feedback, inner-loop iteration | Agent improves a model through user-reviewable notebooks within an approved budget without modifying the harness |
| 5. Orchestration and approvals | Durable workflow, gates, recovery, second adapter | Supervised multi-phase workflow with enforced approvals |
| 6. Iterative data acquisition | Gap diagnosis, proposals, approved extraction, retraining comparisons | Outer-loop improvement with lineage and budgets |
| 7. Advanced capabilities (after proof of concept) | Ray-backed runner for parallel experiments and hyperparameter trials, followed by distributed training as needed; Optuna, active learning, labeling, augmentation, specialized agents, containers | Ray execution preserves harness governance and lineage; extensible multi-agent workflow with advanced compute/data strategies |

The phase order is an implementation sequence, not a restriction on the final development workflow. Basic PyTorch is included early; advanced distributed deep learning comes later.

## 12. Proposed Repository Layout

### Harness product repository

This repository contains the installable product, templates, examples, and product tests. Example projects and fixtures demonstrate usage; user experiment repositories are created separately.

```text
agent-ml-harness/
├── AGENTS.md
├── README.md
├── pyproject.toml             # Build metadata, dependencies, agent-ml entrypoint
├── uv.lock
├── docs/
│   └── specs/
├── templates/                # Separate-project and notebook scaffolding
├── runtime_guidance/         # Included as resources in the distribution
│   ├── AGENTS.md
│   ├── data/AGENTS.md
│   ├── features/AGENTS.md
│   └── modeling/AGENTS.md
├── src/agentic_ml/
│   ├── AGENTS.md
│   ├── contracts/
│   ├── orchestrator/
│   │   └── AGENTS.md
│   ├── agents/adapters/
│   ├── approvals/            # Approval service and scoped decision handling
│   ├── data/
│   │   ├── sources/
│   │   ├── acquisition/
│   │   └── validation/
│   ├── features/
│   │   └── AGENTS.md
│   ├── harness/
│   │   ├── execution/
│   │   ├── evaluation/
│   │   └── resources/
│   ├── frameworks/
│   │   ├── sklearn/
│   │   ├── lightgbm/
│   │   └── pytorch/
│   ├── tracking/
│   ├── storage/
│   └── cli/
├── examples/
│   ├── tabular-classification/
│   │   ├── experiment.md
│   │   ├── search-space.yaml
│   │   ├── experiment.yaml
│   │   └── notebooks/
│   ├── tabular-regression/
│   └── image-classification/
└── tests/
    ├── unit/
    ├── integration/
    ├── acceptance/
    └── fixtures/
```

### Separate user experiment repository

The following is an illustrative initialized project, not a directory inside the harness repository. Its project package name and experiment names are user-selected.

```text
customer-churn/
├── README.md
├── AGENTS.md                 # Project development conventions
├── pyproject.toml            # Project package and harness Git dependency/full SHA
├── uv.lock                   # Resolved experiment environment
├── project.yaml              # Storage, tracking, state, agent, guidance, components
├── .gitignore
├── .dvc/
├── data/                     # DVC-managed content; excluded from Git
├── data.dvc                  # Illustrative data-version metadata tracked in Git
├── runtime_guidance/         # Optional explicitly mapped project practices
├── src/churn_experiments/    # Shared project code, custom models/preprocessors
└── experiments/
    └── baseline-comparison/
        ├── experiment.md
        ├── search-space.yaml
        ├── experiment.yaml   # Entrypoints, data, feature pipeline, execution
        ├── dvc.yaml
        ├── dvc.lock
        ├── notebooks/
        │   ├── 01_data_assessment.ipynb
        │   ├── 02_features_and_baseline.ipynb
        │   ├── 03_model_development.ipynb
        │   └── 04_results.ipynb
        └── helpers/          # Optional experiment-specific Python
```

Project configuration and experiment-input paths resolve against the user repository root. DVC stage paths follow DVC's declared stage working-directory semantics; pipeline templates must make those paths explicit and consistent with harness execution. Raw sources may remain outside the repository under approved access rules; `data/` represents versioned project snapshots.

Executed notebook snapshots, model artifacts, DVC content/cache, and durable workflow state live in configured project-associated storage and are excluded from Git when stored beneath the project root. Track source notebooks, generated Python, briefs, configuration, project dependency lockfiles, DVC metadata/pipeline definitions, and artifact references in the experiment repository. Preserve immutable source snapshots for runs even when the working tree has uncommitted changes.

## 13. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Validation/test leakage | Split manifests, training-only fitting, protected holdout policies |
| Overfitting through repeated experimentation | Iteration budgets, fixed validation protocol, independent final evaluation |
| Agent coupling | Versioned task contracts, capability discovery, multiple adapter acceptance tests |
| Unsafe generated code | Sandboxing, least privilege, constrained network/filesystem access |
| Irreproducible results | Dataset snapshots, dependency lockfiles, seeds, hardware metadata, tolerances |
| Data acquisition drift or cost | Scoped approval, source allowlists, acquisition budgets, controlled before/after comparisons |
| Workflow inconsistency | Durable state, idempotent jobs, audit trail, recovery tests |
| Restrictive framework abstraction | Standard operations plus custom training entrypoints |
| Hidden dependency on harness checkout | Installed public API, separate-project acceptance fixtures, project lockfile, explicit harness build identity |
| Notebook state or source drift | Fresh-kernel execution, explicit artifact references, immutable notebook/helper snapshots including uncommitted changes |

## 14. Architecture Decision Records

### ADR-001 — Hierarchical Closed-Loop ML Development

**Status: Accepted**

**Decision:** The harness will implement a model-improvement inner loop and data-improvement outer loop. The orchestrator coordinates both, while the harness executes and independently validates actions. Developers approve phase boundaries and acquisition scope changes.

**Rationale:** Poor model performance can reflect insufficient or unrepresentative data, not just inadequate features, architecture, or hyperparameters. Feedback must support both model and dataset improvement.

**Consequences:** Requires data-gap diagnostics, acquisition contracts, dataset versioning, authorization, consistent before/after evaluation, and termination conditions for both loops.

### ADR-007 — GitHub Package Installation and Project Initialization

**Status: Installation decisions accepted; remaining interface details pending**

**Decision:** Initially install the harness as a normal Python package directly from its GitHub repository using `uv`, pinned to a full commit SHA. Use `agent-ml` as the installed CLI name and retain `agentic_ml` as the Python import name. Users install `uv` and Git, initialize a separate Git/Python project, install the harness into that project's environment, and then run `uv run agent-ml init`. No separate initializer-tool installation is required. Package-registry distribution is future work.

**Rationale:** Direct GitHub installation supports the separate-repository workflow without requiring package-registry publishing. A full commit pin identifies the exact harness source used by an experiment.

**Consequences:** The repository must build an installable package containing the CLI, templates, and runtime guidance. The initializer preserves existing project files and the pinned dependency. Run provenance records the harness repository URL, full commit SHA, package version, and project lockfile identity. Users need GitHub access at installation/restoration time; the installer may fetch source into its cache, but runtime use requires no manually maintained harness checkout.

**Remaining decisions:** Actual GitHub URL and distribution name, supported Python versions, API compatibility/versioning policy, project/experiment configuration schemas, and CLI/API details beyond `agent-ml init`.

### Pending decisions

- **ADR-002:** Expose harness through Python API and CLI initially; consider MCP server later.
- **ADR-003:** Start with a lightweight durable state-machine orchestrator; evaluate agent orchestration frameworks if complexity requires.
- **ADR-004:** Hybrid ML operations: standardized capabilities plus sandboxed custom Python code, with project-local registration of user-supplied algorithms and feature preparation through versioned public interfaces. Components may come from project code or pinned dependencies; using them requires no harness modifications. Supplied code is immutable by default, with explicit developer approval required to change immutable components. This proposed decision remains pending.
- **ADR-005:** Choose configurable project-associated DVC storage, MLflow backend/artifact storage, and durable workflow-state configuration, including single-machine local defaults; DVC data versioning/pipelines and MLflow experiment tracking are selected stack components.
- **ADR-006:** Define the authorization and isolation model for data connectors, generated code, and interactive notebook kernels, including protected-test isolation and project/harness filesystem boundaries.
- **ADR-007 remaining details:** Finalize the repository URL/distribution name, supported Python versions, API compatibility/versioning, configuration schemas, and remaining CLI/API commands; GitHub installation, full commit pinning, and the agent-ml CLI/init sequence are selected above.

## 15. Next Steps

1. Ratify pending architectural decisions and clarify nonfunctional targets.
2. Convert requirements and acceptance criteria into independently testable user stories.
3. Define JSON Schemas and Python models for core contracts.
4. Build the Phase 1 vertical slice in a separate user project: initialize/install → extract → validate → snapshot → run notebook → evaluate → track, recording both experiment and harness identities.
5. Add inner-loop agent iteration, supervised orchestration, and then outer-loop acquisition.

**Guiding principle:** Build an ML experimentation and data-development harness that agents can use, rather than a framework that hardcodes one particular agent's reasoning or workflow.
