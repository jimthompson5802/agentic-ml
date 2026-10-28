| Slice | User-visible outcome | Stories |
|---|---|---|
| **1. Run and record a reproducible experiment** | Initialize a separate project, extract and validate data, execute a notebook, inspect its recorded results, and reproduce the run. | US-01, US-02, US-03, US-05, US-09, US-10, US-11, US-12, US-13; initial US-26 and US-27 |
| **2. Build and compare reproducible features** | Produce and compare feature pipelines whose fitted state and outputs can be restored. | US-14, US-15; preprocessing portion of US-16; pipeline portion of US-27 |
| **3. Train, tune, and independently evaluate models** | Compare baselines and candidate models within declared boundaries and obtain an independent assessment. | US-06, US-18, US-19, US-20, US-21, US-24; model portion of US-16; reporting portion of US-26 |
| **4. Let an agent improve an experiment** | Generate reviewable notebooks and improve a model using development feedback within an approved phase. | US-04, US-07, US-08, US-17, US-22; first-adapter portion of US-30 |
| **5. Supervise and resume the complete workflow** | Run the multi-phase workflow with durable approvals, interruption recovery, and interchangeable agents. | US-23, US-25; second-adapter portion of US-30; audit portion of US-26 |
| **6. Improve the dataset through authorized acquisition** | Diagnose a data limitation, authorize acquisition, version the resulting data, and measure the effect of retraining. | US-28, US-29 |

This document is the authoritative source of product requirements and acceptance criteria. The stories originated from version 0.10 of the [Agentic ML Development Harness design document](agentic-ml-harness-design.md); the design document now describes the supporting design and references the criteria defined here. These requirements describe proposed behavior, not implemented capabilities or finalized interfaces.

Acceptance criteria use stable IDs of the form `US-<story>-AC-<criterion>`, such as `US-01-AC-01`. Criterion numbers are unique within a story and continue across slices. Preserve IDs when wording changes or criteria move; assign the next unused number to a new criterion and never reuse a retired ID. Architecture references identify supporting design sections rather than defining another set of requirements.

Slices are cumulative. Repeated story identifiers describe incremental delivery of the same user outcome. Access controls, applicable approvals, budget enforcement, independent validation, and provenance accompany each capability when introduced; Slice 5 completes their durable multi-phase orchestration. The acceptance criteria below define verifiable outcomes without settling its pending API, configuration-schema, or isolation-design decisions.

## Slice 1: Run and record a reproducible experiment

Starting with Python and local raw data, the developer creates a separate experiment repository and completes an extraction-to-recorded-notebook run without an agent or a manually maintained harness checkout.

### US-01: Install a pinned harness version

As a developer, I want to install a pinned harness version into my own experiment repository so that my project has a reproducible environment.

Acceptance criteria:

- <a id="us-01-ac-01"></a> **US-01-AC-01:** Documented bootstrap instructions cover installing `uv` and Git, creating the user Git/Python project, and installing the harness from GitHub at a full commit SHA.
- <a id="us-01-ac-02"></a> **US-01-AC-02:** The harness is a normal installed dependency; runtime use requires no manually maintained harness checkout or installer cache.
- <a id="us-01-ac-03"></a> **US-01-AC-03:** The project lockfile records the resolved harness revision and dependencies; the installed package exposes `agent-ml`, `agentic_ml`, templates, and runtime guidance.
- <a id="us-01-ac-04"></a> **US-01-AC-04:** An explicit harness upgrade changes the commit pin and lockfile, producing a new environment identity.

Architecture references: §8 Project initialization and installation; §9 Execution.

### US-02: Initialize an experiment project

As a developer, I want to initialize configuration, notebooks, dependencies, and local storage while preserving existing files so that I can start experimenting safely.

Acceptance criteria:

- <a id="us-02-ac-01"></a> **US-02-AC-01:** `uv run agent-ml init` adds project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and required project-package scaffolding.
- <a id="us-02-ac-02"></a> **US-02-AC-02:** Initialization preserves existing files and the pinned harness dependency, reporting conflicts instead of silently overwriting files.
- <a id="us-02-ac-03"></a> **US-02-AC-03:** Required ML, notebook execution, and JupyterLab dependencies are declared and synchronized with the project environment and lockfile.
- <a id="us-02-ac-04"></a> **US-02-AC-04:** Project-associated DVC, MLflow, and durable-state storage are initialized with local defaults and configurable locations.
- <a id="us-02-ac-05"></a> **US-02-AC-05:** Data access, agent authentication, and approval presentation remain explicit setup choices; initialization grants no execution or data-access authorization, and credentials remain outside committed configuration.

Architecture references: §8 Project initialization and installation.

### US-03: Define experiment objectives and boundaries

As a data scientist, I want to describe objectives and constraints in Markdown and declare search boundaries in YAML so that agents work toward my intended outcome.

Acceptance criteria:

- <a id="us-03-ac-01"></a> **US-03-AC-01:** The experiment brief captures data, target, task type, feature guidance, metric and direction, split constraints, algorithm mode, and budgets, including explicitly delegated decisions.
- <a id="us-03-ac-02"></a> **US-03-AC-02:** Search-space YAML declares allowed algorithms, fixed parameters, and tunable choices or ranges; execution configuration cannot expand these boundaries.
- <a id="us-03-ac-03"></a> **US-03-AC-03:** Resolved inputs produce a versioned plan containing the effective decisions, source references, and checksums before dependent execution.
- <a id="us-03-ac-04"></a> **US-03-AC-04:** Ambiguous or conflicting requirements block affected runs until resolved; delegated decisions require approval before use.
- <a id="us-03-ac-05"></a> **US-03-AC-05:** Relative input paths resolve against the experiment repository root, with the notebook working directory recorded explicitly.

Architecture references: §8 Developer experiment inputs; §8 Algorithm and hyperparameter configuration.

### US-05: Reject invalid configurations before execution

As a data scientist, I want invalid algorithms, parameters, and search configurations rejected before training so that compute is spent on valid candidates.

Acceptance criteria:

- <a id="us-05-ac-01"></a> **US-05-AC-01:** Validation checks registered algorithm identifiers, task compatibility, parameter names, types, defaults, and compatible combinations.
- <a id="us-05-ac-02"></a> **US-05-AC-02:** Categorical choices are nonempty; numeric bounds are ordered and inclusive; integer ranges yield integers; logarithmic bounds are strictly positive.
- <a id="us-05-ac-03"></a> **US-05-AC-03:** Fixed values remain fixed, and omitted parameters use recorded registry defaults without becoming tunable.
- <a id="us-05-ac-04"></a> **US-05-AC-04:** Invalid inputs produce actionable validation errors before training starts.
- <a id="us-05-ac-05"></a> **US-05-AC-05:** As training entrypoints are introduced, every candidate submitted through Python, custom code, or notebooks receives the same boundary checks.

Architecture references: §8 Algorithm and hyperparameter configuration; §8 User-supplied ML components.

### US-09: Execute saved notebooks reproducibly

As a data scientist, I want saved notebooks executed automatically from a fresh kernel with explicit inputs so that recorded results do not depend on hidden state.

Acceptance criteria:

- <a id="us-09-ac-01"></a> **US-09-AC-01:** Managed execution uses the selected project's locked environment, a fresh kernel, cell order, explicit parameters, and a recorded working directory.
- <a id="us-09-ac-02"></a> **US-09-AC-02:** The run preserves the source notebook, parameters, environment identity, executed notebook with cell outputs, errors, and generated artifacts.
- <a id="us-09-ac-03"></a> **US-09-AC-03:** Notebook-to-notebook dependencies use recorded artifact references rather than another kernel's variables.
- <a id="us-09-ac-04"></a> **US-09-AC-04:** Cell errors, timeouts, and cancellation produce the corresponding run status; successful execution remains subject to independent validation.
- <a id="us-09-ac-05"></a> **US-09-AC-05:** Access restrictions, approvals, and budgets apply equally to notebook and Python entrypoints; unauthorized filesystem or credential access is blocked.

Architecture references: §9 Execution; §9 Notebook development and execution contract.

### US-10: Control and inspect runs

As a data scientist, I want to submit, monitor, cancel, and inspect runs so that I can control execution and understand failures.

Acceptance criteria:

- <a id="us-10-ac-01"></a> **US-10-AC-01:** The local runner supports submission, status inspection, cancellation, logs, and artifact retrieval through the harness interfaces.
- <a id="us-10-ac-02"></a> **US-10-AC-02:** Runs record completion, failure, timeout, or cancellation outcomes with available diagnostic evidence.
- <a id="us-10-ac-03"></a> **US-10-AC-03:** Runtime and experiment-count limits prevent further unauthorized work; supported resource limits are enforced.
- <a id="us-10-ac-04"></a> **US-10-AC-04:** Unsuccessful model performance is distinguishable from execution failure when modeling is added.
- <a id="us-10-ac-05"></a> **US-10-AC-05:** Cancelled or budget-exhausted work preserves available evidence for review.

Architecture references: §8 ExperimentRunner interface; §9 Execution; §9 Workflow states.

### US-11: Extract approved source data

As a data scientist, I want approved data extracted from supported local, SQL, or object-storage sources so that I can work with existing datasets.

Acceptance criteria:

- <a id="us-11-ac-01"></a> **US-11-AC-01:** Initial connectors support local CSV/Parquet, SQL, and object storage; acceptance demonstrations extract data from at least two source types.
- <a id="us-11-ac-02"></a> **US-11-AC-02:** Source discovery exposes permitted schema and metadata without unrestricted data exposure.
- <a id="us-11-ac-03"></a> **US-11-AC-03:** Extraction executes only approved queries or sampling plans within source allowlists, permissions, network restrictions, and cost/record limits.
- <a id="us-11-ac-04"></a> **US-11-AC-04:** Each snapshot records source identity, query, parameters, extraction time, checksums, and permissions metadata.
- <a id="us-11-ac-05"></a> **US-11-AC-05:** Extraction failures are reported without presenting incomplete output as a validated dataset.

Architecture references: §6 Data extraction requirements.

### US-12: Assess data quality and define splits

As a data scientist, I want data-quality assessments and an explicit split protocol so that I can identify unsuitable data before modeling.

Acceptance criteria:

- <a id="us-12-ac-01"></a> **US-12-AC-01:** Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.
- <a id="us-12-ac-02"></a> **US-12-AC-02:** Assessment includes distributions, class balance where relevant, anomalies, and leakage diagnostics.
- <a id="us-12-ac-03"></a> **US-12-AC-03:** A versioned split manifest records training, validation, and protected-test partitions, respecting approved time or group constraints.
- <a id="us-12-ac-04"></a> **US-12-AC-04:** Dataset assessment and split protocol are presented for approval before dependent feature or modeling work.

Architecture references: §4 Data extraction and EDA; §5 Development phases and gates; §6 Data extraction requirements; §9 Independent evaluation.

### US-13: Version and restore datasets

As a data scientist, I want to version and restore datasets with verified content hashes so that experiments use identifiable, recoverable inputs.

Acceptance criteria:

- <a id="us-13-ac-01"></a> **US-13-AC-01:** DVC versions source snapshots, split manifests, and derived datasets as those artifacts are introduced.
- <a id="us-13-ac-02"></a> **US-13-AC-02:** Git tracks DVC metadata and relevant manifests while dataset content resides in the configured cache/storage and is excluded from Git.
- <a id="us-13-ac-03"></a> **US-13-AC-03:** A dataset can be restored from configured storage using its recorded metadata, and restored content hashes are verified.
- <a id="us-13-ac-04"></a> **US-13-AC-04:** Missing or mismatched content prevents the dataset from being treated as successfully restored.

Architecture references: §9 Experiment tracking, data versioning, and pipelines.

### US-26: Record run artifacts and provenance

As a data scientist, I want recorded runs linked to their exact inputs, code, and environment so that I can inspect and audit results.

Acceptance criteria:

- <a id="us-26-ac-01"></a> **US-26-AC-01:** MLflow records run status, effective parameters, available metrics, outputs, and artifact references, linked to the harness run identifier.
- <a id="us-26-ac-02"></a> **US-26-AC-02:** Each run links to the exact DVC dataset state, experiment Git revision, source snapshots including uncommitted changes, and configuration checksums.
- <a id="us-26-ac-03"></a> **US-26-AC-03:** Provenance includes the harness repository URL, full commit SHA, package version, build identity where available, and project lockfile/environment identity.
- <a id="us-26-ac-04"></a> **US-26-AC-04:** Source snapshots include notebooks, imported helpers, project code, configuration, and applicable runtime guidance; later slices extend these records to components, pipelines, and approvals.
- <a id="us-26-ac-05"></a> **US-26-AC-05:** Basic execution correctness is independently checked against expected artifacts; notebook completion alone does not establish experiment acceptance.

Architecture references: §3 Component responsibilities; §9 Experiment tracking, data versioning, and pipelines; §9 Independent evaluation.

### US-27: Reproduce a basic run in a clean environment

As a collaborating data scientist, I want to reproduce an experiment on another machine so that I can independently check its results.

Acceptance criteria:

- <a id="us-27-ac-01"></a> **US-27-AC-01:** An experiment checkout, recorded source snapshots, lockfile, and dataset metadata restore the pinned harness commit and required inputs without a maintained harness checkout.
- <a id="us-27-ac-02"></a> **US-27-AC-02:** Reproduction executes the recorded source, including preserved uncommitted changes, rather than assuming the Git revision alone identifies it.
- <a id="us-27-ac-03"></a> **US-27-AC-03:** Declared output checks or tolerances determine whether the basic run reproduces successfully; metric tolerances apply when modeling is introduced.
- <a id="us-27-ac-04"></a> **US-27-AC-04:** Missing source, dependencies, or dataset content is reported explicitly instead of silently substituted.

Architecture references: §8 Project initialization and installation; §9 Experiment tracking, data versioning, and pipelines; §9 Independent evaluation.

## Slice 2: Build and compare reproducible features

Starting with versioned data and an approved split protocol, the developer prepares features, compares alternatives, and restores fitted preprocessing and pipeline outputs.

### US-14: Generate and compare feature pipelines

As a data scientist, I want agents to generate and compare feature pipelines on consistent splits so that feature improvements have credible evidence.

Acceptance criteria:

- <a id="us-14-ac-01"></a> **US-14-AC-01:** Feature plans identify ordered components, effective parameters, input/output schemas, fitting scope, and modification permissions.
- <a id="us-14-ac-02"></a> **US-14-AC-02:** The harness executes candidate transformations and records their definitions, dependencies, outputs, and lineage.
- <a id="us-14-ac-03"></a> **US-14-AC-03:** Candidate feature sets are compared against a fixed baseline using the same approved validation protocol.
- <a id="us-14-ac-04"></a> **US-14-AC-04:** Feature artifacts trace back to their source datasets and are independently validated before phase advancement.
- <a id="us-14-ac-05"></a> **US-14-AC-05:** This slice supports supplied or explicitly authored candidates; agent generation is exercised when agent integration arrives in Slice 4.

Architecture references: §7 Feature Engineering; §5 Development phases and gates.

### US-15: Preserve training-only preprocessing

As a data scientist, I want preprocessing fitted only on training data and preserved for reuse so that validation and inference transformations remain consistent.

Acceptance criteria:

- <a id="us-15-ac-01"></a> **US-15-AC-01:** Stateful preprocessing fits only on the approved training partition and applies unchanged fitted state to validation, test, and inference inputs.
- <a id="us-15-ac-02"></a> **US-15-AC-02:** Transformations that violate split boundaries or leakage rules are rejected.
- <a id="us-15-ac-03"></a> **US-15-AC-03:** Preparation code, fitted state, dependencies, parameters, and output schemas are preserved as artifacts.
- <a id="us-15-ac-04"></a> **US-15-AC-04:** Restored preprocessing reproduces validation and inference transformations under declared reproducibility checks.

Architecture references: §7 Feature Engineering; §8 User-supplied ML components.

### US-16: Register supplied preprocessing components

As a data scientist, I want to register my existing preprocessors without changing the harness so that I can reuse domain-specific implementations.

Acceptance criteria:

- <a id="us-16-ac-01"></a> **US-16-AC-01:** Project configuration registers stateful preprocessors and stateless transformations from project code or pinned dependencies through versioned public interfaces.
- <a id="us-16-ac-02"></a> **US-16-AC-02:** Declarations include identifiers, entrypoints, interface versions, parameter specifications, and modification permissions; duplicate identifiers and incompatible interfaces are rejected.
- <a id="us-16-ac-03"></a> **US-16-AC-03:** Stateful components support fitting, transformation, and fitted-state persistence/restoration; stateless components declare their output schema.
- <a id="us-16-ac-04"></a> **US-16-AC-04:** Registered components follow the same validation, resource, access, and lineage rules as built-in components.
- <a id="us-16-ac-05"></a> **US-16-AC-05:** Lineage records declarations, exact code snapshots or pinned dependency identities, effective parameters, and fitted artifacts.

Architecture references: §7 Feature Engineering; §8 User-supplied ML components; §9 Independent evaluation.

### US-27: Reproduce and reuse pipeline stages

As a data scientist, I want reproducible pipeline stages and valid output reuse so that I can avoid redundant work while preserving trustworthy results.

Acceptance criteria:

- <a id="us-27-ac-05"></a> **US-27-AC-05:** DVC pipeline definitions record stage dependencies, parameters, and outputs, with resolved hashes preserved in `dvc.lock`.
- <a id="us-27-ac-06"></a> **US-27-AC-06:** Stage working directories and paths are explicit and consistent with harness execution.
- <a id="us-27-ac-07"></a> **US-27-AC-07:** Reproducing declared stages restores or generates the expected outputs under the recorded configuration.
- <a id="us-27-ac-08"></a> **US-27-AC-08:** Reused outputs retain producer provenance and remain subject to current authorization and evaluation checks.
- <a id="us-27-ac-09"></a> **US-27-AC-09:** Cache reuse alone does not establish experiment acceptance or bypass a gate.

Architecture references: §8 Project initialization and installation; §9 Experiment tracking, data versioning, and pipelines; §9 Independent evaluation.

## Slice 3: Train, tune, and independently evaluate models

Starting with approved features, the developer establishes baselines, compares and tunes candidates within declared limits, and obtains an independent assessment and final report.

### US-06: Choose an algorithm execution mode

As a data scientist, I want to use one algorithm, select among allowed algorithms, or compare the allowed set so that experimentation matches my question and budget.

Acceptance criteria:

- <a id="us-06-ac-01"></a> **US-06-AC-01:** Use mode runs the specified allowed algorithm; select mode records a selection from the allowed set; compare mode evaluates every algorithm in that set within the approved plan and budgets.
- <a id="us-06-ac-02"></a> **US-06-AC-02:** All modes respect task compatibility, parameter boundaries, and trial/runtime budgets.
- <a id="us-06-ac-03"></a> **US-06-AC-03:** Comparing algorithms does not require exhaustive enumeration of parameter combinations.
- <a id="us-06-ac-04"></a> **US-06-AC-04:** Suggested algorithms or expanded ranges are recorded only as recommendations for a subsequent experiment; adopting them requires a new versioned configuration and applicable approvals.

Architecture references: §8 Developer experiment inputs; §8 Algorithm and hyperparameter configuration.

### US-16: Register supplied models

As a data scientist, I want to register my existing model implementations without changing the harness so that I can reuse domain-specific training code.

Acceptance criteria:

- <a id="us-16-ac-06"></a> **US-16-AC-06:** Project-local or pinned-dependency models register through the public component interface without harness modifications.
- <a id="us-16-ac-07"></a> **US-16-AC-07:** Models support training on approved inputs, evaluator-compatible prediction, and fitted-model persistence/restoration.
- <a id="us-16-ac-08"></a> **US-16-AC-08:** Before training, validation rejects unsupported tasks, invalid parameters, incompatible interfaces, and prediction outputs incompatible with the approved metrics.
- <a id="us-16-ac-09"></a> **US-16-AC-09:** Supplied models can be tuned within approved boundaries and independently evaluated after restoration.
- <a id="us-16-ac-10"></a> **US-16-AC-10:** Component declarations, code/dependency identities, effective parameters, and fitted artifacts appear in run lineage.

Architecture references: §7 Feature Engineering; §8 User-supplied ML components; §9 Independent evaluation.

### US-18: Train across supported frameworks

As a data scientist, I want to train and evaluate scikit-learn, LightGBM, and PyTorch models so that I can compare approaches across supported frameworks.

Acceptance criteria:

- <a id="us-18-ac-01"></a> **US-18-AC-01:** End-to-end runs cover tabular classification, tabular regression, and a basic PyTorch deep-learning example.
- <a id="us-18-ac-02"></a> **US-18-AC-02:** A simple reproducible baseline is recorded and approved before candidate improvement comparisons.
- <a id="us-18-ac-03"></a> **US-18-AC-03:** Framework adapters expose training, prediction, and persistence operations usable by independent evaluation.
- <a id="us-18-ac-04"></a> **US-18-AC-04:** Each run records effective parameters, framework/library identities, metrics, model artifacts, and feature/data lineage.

Architecture references: §4 Baseline modeling and Model development; §8 ModelAdapter interface; §9 Experiment tracking, data versioning, and pipelines.

### US-19: Manage PyTorch execution

As a data scientist, I want PyTorch runs to support CPU/GPU execution, checkpoints, and cancellation so that deep-learning experiments are manageable.

Acceptance criteria:

- <a id="us-19-ac-01"></a> **US-19-AC-01:** Basic PyTorch training runs on CPU and supports GPU execution when the required hardware/backend is available.
- <a id="us-19-ac-02"></a> **US-19-AC-02:** Checkpoints are captured as run artifacts and can be restored by the model implementation.
- <a id="us-19-ac-03"></a> **US-19-AC-03:** Cancellation stops managed training and preserves available logs, checkpoints, and status.
- <a id="us-19-ac-04"></a> **US-19-AC-04:** Resource requests, hardware metadata, runtime limits, and supported quotas are recorded and enforced where supported.

Architecture references: §9 Execution; §8 ModelAdapter interface.

### US-20: Tune within declared limits

As a data scientist, I want bounded tuning with enforced trial and runtime limits so that agents cannot exceed the authorized search or budget.

Acceptance criteria:

- <a id="us-20-ac-01"></a> **US-20-AC-01:** Candidates use only declared algorithms, fixed values, categorical choices, and numeric ranges; omitted defaults cannot be tuned.
- <a id="us-20-ac-02"></a> **US-20-AC-02:** Candidate validation rejects boundary violations before training, including submissions from custom code and notebooks.
- <a id="us-20-ac-03"></a> **US-20-AC-03:** Experiment-count and runtime budgets stop new work and leave a reviewable summary of completed trials.
- <a id="us-20-ac-04"></a> **US-20-AC-04:** The optimization summary identifies the search performed, resources consumed, candidate evidence, and model proposed for final evaluation.

Architecture references: §8 Algorithm and hyperparameter configuration; §5 Optimization; §9 Execution.

### US-21: Independently assess experiment results

As a data scientist, I want independent evaluation of execution, leakage, model quality, robustness, and reproducibility so that acceptance rests on evidence.

Acceptance criteria:

- <a id="us-21-ac-01"></a> **US-21-AC-01:** The evaluator checks successful execution and required artifacts independently of agent assertions.
- <a id="us-21-ac-02"></a> **US-21-AC-02:** Scientific-validity checks reject split violations, improper preprocessing fitting, and leakage.
- <a id="us-21-ac-03"></a> **US-21-AC-03:** Approved metrics and baseline comparisons are computed consistently, respecting optimization direction.
- <a id="us-21-ac-04"></a> **US-21-AC-04:** Defined folds, slices, or stress tests assess robustness; repeated runs are checked against explicit reproducibility tolerances.
- <a id="us-21-ac-05"></a> **US-21-AC-05:** Structured evaluation results distinguish execution failure, scientific invalidity, and insufficient model quality.

Architecture references: §9 Independent evaluation.

### US-24: Protect final holdout evaluation

As a data scientist, I want protected holdout evaluation reserved for the authorized final phase so that final-test results do not influence development.

Acceptance criteria:

- <a id="us-24-ac-01"></a> **US-24-AC-01:** Experiment agents, training code, and exploratory kernels cannot access protected test data; protection is enforced independently of agent instructions.
- <a id="us-24-ac-02"></a> **US-24-AC-02:** Only the independent evaluator accesses the holdout for the authorized final evaluation.
- <a id="us-24-ac-03"></a> **US-24-AC-03:** Protected-test results cannot drive feature, model, or acquisition improvement loops.
- <a id="us-24-ac-04"></a> **US-24-AC-04:** Unsuccessful final evaluation ends in rejection or review; further development requires a separately approved protocol preserving holdout protection.
- <a id="us-24-ac-05"></a> **US-24-AC-05:** Completion requires developer approval of successful final evaluation.

Architecture references: §4 Final evaluation; §9 Notebook development and execution contract; §9 Governance; ADR-006.

### US-26: Compare runs and review the final report

As a data scientist, I want run comparisons and a final report linked to their evidence so that I can judge the model against the original objective.

Acceptance criteria:

- <a id="us-26-ac-06"></a> **US-26-AC-06:** MLflow comparisons expose effective parameters, metrics, execution status, and model artifacts for baseline and candidate runs.
- <a id="us-26-ac-07"></a> **US-26-AC-07:** The final report identifies the model, approved metrics, baseline comparison, validity/robustness/reproducibility findings, and acceptance outcome.
- <a id="us-26-ac-08"></a> **US-26-AC-08:** Model lineage traces through component identities, fitted feature pipelines, source datasets, exact code/configuration snapshots, and environment identity.
- <a id="us-26-ac-09"></a> **US-26-AC-09:** Reports preserve references to independent evaluation evidence rather than treating generated narrative as proof of acceptance.

Architecture references: §3 Component responsibilities; §9 Experiment tracking, data versioning, and pipelines; §9 Independent evaluation.

## Slice 4: Let an agent improve an experiment

An agent resolves delegated choices, generates notebooks, and improves a model using development feedback while the developer retains control of phase scope and component permissions.

### US-04: Approve delegated experiment decisions

As a data scientist, I want agents to propose delegated feature, metric, and algorithm decisions for approval so that I retain control over the experiment design.

Acceptance criteria:

- <a id="us-04-ac-01"></a> **US-04-AC-01:** Agents resolve only explicitly delegated choices and record the proposed decisions and reasoning in the structured plan.
- <a id="us-04-ac-02"></a> **US-04-AC-02:** The plan identifies features, metric and direction, split protocol, allowed algorithms, and budgets.
- <a id="us-04-ac-03"></a> **US-04-AC-03:** Ambiguities and conflicts are surfaced before affected execution, and dependent work waits for approval through applicable gates.
- <a id="us-04-ac-04"></a> **US-04-AC-04:** Original inputs, resolved decisions, and their versions/checksums remain available in run lineage.

Architecture references: §8 Developer experiment inputs; §4 Problem definition.

### US-07: Generate reviewable experiment notebooks

As a data scientist, I want agents to generate readable notebooks and project code so that I can inspect, edit, and understand their work.

Acceptance criteria:

- <a id="us-07-ac-01"></a> **US-07-AC-01:** Generated notebooks include explanatory Markdown covering objectives, assumptions, code, results, and proposed next steps, with explicit parameter cells.
- <a id="us-07-ac-02"></a> **US-07-AC-02:** Notebooks import generic capabilities from the installed harness and shared project logic from the experiment package without paths into a harness checkout.
- <a id="us-07-ac-03"></a> **US-07-AC-03:** Saved notebooks support interactive use and fresh-kernel managed execution without hidden state.
- <a id="us-07-ac-04"></a> **US-07-AC-04:** Generated notebooks, helpers, and project code stay within the experiment repository and authorized storage; the harness installation/source remain unchanged.

Architecture references: §9 Notebook development and execution contract; §3 Harness and experiment project boundary.

### US-08: Explore interactively under the same controls

As a data scientist, I want to explore interactively in JupyterLab under the experiment's access rules so that exploration preserves evaluation integrity.

Acceptance criteria:

- <a id="us-08-ac-01"></a> **US-08-AC-01:** JupyterLab launches from the project environment with the required notebook dependencies.
- <a id="us-08-ac-02"></a> **US-08-AC-02:** Interactive kernels cannot access protected test data, including through arbitrary Python outside harness API calls.
- <a id="us-08-ac-03"></a> **US-08-AC-03:** Training cells submit through managed APIs that enforce candidate boundaries, applicable approvals, budgets, and tracking.
- <a id="us-08-ac-04"></a> **US-08-AC-04:** Interactive execution cannot establish acceptance; recorded results require managed execution of saved snapshots and independent evaluation.

Architecture references: §9 Notebook development and execution contract; §8 Project initialization and installation; ADR-006.

### US-17: Respect immutable supplied components

As a data scientist, I want supplied code to remain immutable unless I approve changes so that agents respect ownership and component permissions.

Acceptance criteria:

- <a id="us-17-ac-01"></a> **US-17-AC-01:** Supplied components are immutable by default; agents may configure and invoke them only within authorized boundaries.
- <a id="us-17-ac-02"></a> **US-17-AC-02:** Attempts to modify immutable components are blocked unless recorded developer approval authorizes the change.
- <a id="us-17-ac-03"></a> **US-17-AC-03:** Approved changes to immutable code create a new versioned experiment configuration.
- <a id="us-17-ac-04"></a> **US-17-AC-04:** Modification permission does not expand algorithm, parameter, data-access, or evaluation boundaries; authorized code changes appear in run snapshots.

Architecture references: §8 User-supplied ML components; §4 Scope changes.

### US-22: Improve models using development feedback

As a data scientist, I want agents to revise experiments using structured development feedback so that model improvement can proceed within approved scope.

Acceptance criteria:

- <a id="us-22-ac-01"></a> **US-22-AC-01:** The agent receives structured evaluation feedback and produces revised notebooks or code with an evidence-based explanation.
- <a id="us-22-ac-02"></a> **US-22-AC-02:** Revisions remain within the current approved phase, component permissions, parameter boundaries, access scope, and budgets.
- <a id="us-22-ac-03"></a> **US-22-AC-03:** Each revision undergoes managed execution and independent evaluation, preserving its source snapshots and results.
- <a id="us-22-ac-04"></a> **US-22-AC-04:** Iteration stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or developer cancellation.
- <a id="us-22-ac-05"></a> **US-22-AC-05:** Phase returns and scope expansions await authorization; protected-test feedback never enters the revision loop.

Architecture references: §4 Hierarchical Closed-Loop Workflow; §9 Independent evaluation.

### US-30: Connect the first agent with preserved runtime guidance

As a data scientist, I want an agent adapter with explicit, preserved runtime guidance so that agent behavior follows the approved experiment context.

Acceptance criteria:

- <a id="us-30-ac-01"></a> **US-30-AC-01:** The first coding-assistant adapter supports capability discovery, structured task/result exchange, and cancellation through the common contract.
- <a id="us-30-ac-02"></a> **US-30-AC-02:** Runtime loading explicitly selects packaged shared guidance, relevant task-specific guidance, and configured project guidance, recording ownership and order.
- <a id="us-30-ac-03"></a> **US-30-AC-03:** Development `AGENTS.md` files from either repository are excluded from automatic runtime loading.
- <a id="us-30-ac-04"></a> **US-30-AC-04:** The plan snapshots guidance contents, paths, versions/checksums, and load order; subsequent tasks use the preserved bundle.
- <a id="us-30-ac-05"></a> **US-30-AC-05:** Conflicting guidance or attempts to expand experiment constraints block affected execution; adopting changed guidance requires a new versioned configuration and applicable approvals.

Architecture references: §8 AgentAdapter interface; §8 Development and runtime agent instructions.

## Slice 5: Supervise and resume the complete workflow

The developer supervises all development phases through durable, scoped approval decisions, recovers interrupted work, and can use another agent adapter without changing experiment contracts.

### US-23: Approve phase progression and scope changes

As a data scientist, I want to approve, revise, or reject phase progression using validated evidence so that I supervise consequential decisions.

Acceptance criteria:

- <a id="us-23-ac-01"></a> **US-23-AC-01:** Initial plan approval completes problem definition; later phase advancement is blocked until sufficient independent evidence and developer approval are recorded.
- <a id="us-23-ac-02"></a> **US-23-AC-02:** Each decision records reviewer, scope, decision, timestamp, and associated evidence in durable project-associated state.
- <a id="us-23-ac-03"></a> **US-23-AC-03:** Revision authorizes work only within its recorded scope; phase returns, expanded permissions, and changed evaluation criteria require authorization before execution.
- <a id="us-23-ac-04"></a> **US-23-AC-04:** Phases can be skipped only when the approved plan identifies valid existing artifacts supporting the skip.
- <a id="us-23-ac-05"></a> **US-23-AC-05:** Rejection or cancellation preserves results; successful final evaluation requires explicit model approval before completion.

Architecture references: §4 Hierarchical Closed-Loop Workflow; §5 Development phases and gates; §9 Governance.

### US-25: Resume interrupted workflows

As a data scientist, I want interrupted workflows to resume from durable state without repeating completed runs so that work and approvals are preserved.

Acceptance criteria:

- <a id="us-25-ac-01"></a> **US-25-AC-01:** Project-associated durable state preserves phase progress, run identifiers, evidence, approvals, budgets, and terminal or reviewable outcomes.
- <a id="us-25-ac-02"></a> **US-25-AC-02:** Recovery reconciles recorded work and resumes without duplicating completed runs or bypassing pending gates.
- <a id="us-25-ac-03"></a> **US-25-AC-03:** Resumed tasks use the preserved compatible configuration and runtime instruction bundle, even if source guidance has changed.
- <a id="us-25-ac-04"></a> **US-25-AC-04:** Cancelled, failed, budget-exhausted, and review-required outcomes retain evidence and do not silently authorize further work.

Architecture references: §3 Component responsibilities; §9 Workflow states; §8 Development and runtime agent instructions.

### US-30: Use interchangeable agent adapters

As a data scientist, I want interchangeable agent adapters so that I can change assistants without redefining the experiment workflow.

Acceptance criteria:

- <a id="us-30-ac-06"></a> **US-30-AC-06:** Two adapters successfully execute tasks using the same versioned task/result contract.
- <a id="us-30-ac-07"></a> **US-30-AC-07:** Capability discovery identifies which tasks each adapter supports before delegation.
- <a id="us-30-ac-08"></a> **US-30-AC-08:** Both adapters obey the same cancellation, guidance-loading, approval, access, and budget requirements.
- <a id="us-30-ac-09"></a> **US-30-AC-09:** Agent selection does not alter independent evaluation or the experiment's allowed boundaries.

Architecture references: §8 AgentAdapter interface; §8 Development and runtime agent instructions.

### US-26: Audit workflow decisions and evidence

As a reviewer, I want run lineage connected to workflow decisions so that I can reconstruct what was authorized, executed, and accepted.

Acceptance criteria:

- <a id="us-26-ac-10"></a> **US-26-AC-10:** Harness manifests connect runs, MLflow records, DVC state, configuration versions, runtime bundles, and approval records.
- <a id="us-26-ac-11"></a> **US-26-AC-11:** The audit trail identifies the scope authorizing each phase, approved scope changes, and the evidence used for each decision.
- <a id="us-26-ac-12"></a> **US-26-AC-12:** Bidirectional run references allow lookup from a harness result to its MLflow run and from the tracking record to harness provenance.
- <a id="us-26-ac-13"></a> **US-26-AC-13:** Resumption and reuse preserve original producer provenance and the decisions authorizing subsequent use.

Architecture references: §3 Component responsibilities; §9 Experiment tracking, data versioning, and pipelines; §9 Independent evaluation.

## Slice 6: Improve the dataset through authorized acquisition

The developer reviews evidence of data limitations, authorizes a bounded acquisition, and evaluates the effect of the resulting dataset through approved downstream work.

### US-28: Diagnose data gaps and propose acquisition

As a data scientist, I want evidence-backed data-gap diagnoses and acquisition proposals so that I can decide whether additional data is worth obtaining.

Acceptance criteria:

- <a id="us-28-ac-01"></a> **US-28-AC-01:** Diagnosis records evidence of data deficiencies, such as underrepresented classes or slices, using approved data and development evaluation results.
- <a id="us-28-ac-02"></a> **US-28-AC-02:** A structured proposal records its reason, evidence, acquisition hypothesis, source, strategy, expected benefit, costs, limits, and required authorization.
- <a id="us-28-ac-03"></a> **US-28-AC-03:** Expected benefit is presented as a hypothesis rather than a guaranteed improvement.
- <a id="us-28-ac-04"></a> **US-28-AC-04:** Proposals do not use protected final-test feedback or expand access, evaluation protocols, or budgets without approval.

Architecture references: §6 Acquisition strategies and Acquisition proposal contract; §4 Outer loop.

### US-29: Acquire data and measure its effect within approved limits

As a data scientist, I want authorized acquisition to enforce limits, version new data, compare outcomes, and stop at defined conditions so that data improvement remains controlled.

Acceptance criteria:

- <a id="us-29-ac-01"></a> **US-29-AC-01:** Acquisition is blocked without recorded authorization covering source, strategy, scope, and limits; approved in-scope activity need not request permission for every operation.
- <a id="us-29-ac-02"></a> **US-29-AC-02:** Execution enforces source permissions and cost, record, runtime, and compute budgets, preserving evidence when a limit is reached.
- <a id="us-29-ac-03"></a> **US-29-AC-03:** Acquired data is validated and versioned with source lineage; synthetic or augmented data is explicitly identified as distinct from observed data.
- <a id="us-29-ac-04"></a> **US-29-AC-04:** Returning to validation/EDA and downstream development requires the applicable phase authorization, with complete audit records.
- <a id="us-29-ac-05"></a> **US-29-AC-05:** Before-and-after model comparisons use consistent approved evaluation protocols and link results to the corresponding dataset versions.
- <a id="us-29-ac-06"></a> **US-29-AC-06:** The acquisition loop stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or cancellation, preserving a reviewable outcome.
- <a id="us-29-ac-07"></a> **US-29-AC-07:** Resumption after acquisition retains approvals, budget usage, dataset lineage, and completed-run identities; advanced acquisition strategies remain deferred according to the design document's implementation plan.

Architecture references: §6 Data Extraction and Iterative Acquisition; §4 Scope changes and stopping conditions; §9 Governance.
