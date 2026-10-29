Planning terms follow the [repository terminology](../../README.md#planning-terminology): milestones group user stories into usable product increments, implementation phases group tasks within a story with developer approval gates, and workflow phases describe ML experiment execution.

| Milestone | User-visible outcome | Stories |
|---|---|---|
| **0. Establish the harness development foundation** | Set up this repository, run the harness from source, and verify contributor changes and distributable packages locally and in CI. | US-31, US-32, US-33 |
| **1. Run and record a reproducible experiment** | Initialize a separate project, extract and validate data, execute a notebook, inspect its recorded results, and reproduce the run. | US-01, US-02, US-03, US-05, US-09, US-10, US-11, validation portion of US-12, US-13; initial US-26 and US-27 |
| **2. Assess data and build reproducible feature pipelines** | Profile data, approve versioned splits, restore fitted feature pipelines and outputs, and compare predictive performance using a fixed approved reference estimator. | assessment/split portion of US-12; US-14, US-15; preprocessing portion of US-16; pipeline portion of US-27 |
| **3. Train, tune, and independently evaluate models** | Compare baselines and candidate models within declared boundaries and obtain an independent assessment. | US-06, US-18, US-19, US-20, US-21, US-24; model portion of US-16; reporting portion of US-26 |
| **4. Let an agent improve an experiment** | Generate reviewable notebooks and improve a model using development feedback within an approved workflow phase. | US-04, US-07, US-08, US-17, US-22; first-adapter portion of US-30 |
| **5. Supervise and resume the complete workflow** | Run the workflow spanning multiple ML workflow phases with durable approvals, interruption recovery, and interchangeable agents. | US-23, US-25; second-adapter portion of US-30; audit portion of US-26 |
| **6. Improve the dataset through authorized acquisition** | Diagnose a data limitation, authorize acquisition, version the resulting data, and measure the effect of retraining. | US-28, US-29 |
| **99. Future enhancements** | Capture improvements deferred because they are not critical to current functionality. | US-34 |

This document is the authoritative source of product requirements and acceptance criteria. The stories originated from version 0.10 of the [Agentic ML Development Harness design document](agentic-ml-harness-design.md); the design document now describes the supporting design and references the criteria defined here. These requirements describe proposed behavior, not implemented capabilities or finalized interfaces.

Acceptance criteria use stable IDs of the form `US-<story>-AC-<criterion>`, such as `US-01-AC-01`. Criterion numbers are unique within a story and continue across milestones. Preserve IDs when wording changes or criteria move; assign the next unused number to a new criterion and never reuse a retired ID. Architecture references identify supporting design sections rather than defining another set of requirements.

Milestones are cumulative. Repeated story identifiers describe incremental delivery of the same user outcome. Access controls, applicable approvals, budget enforcement, independent validation, and provenance accompany each capability when introduced; Milestone 5 completes their durable orchestration across workflow phases. The acceptance criteria below define verifiable outcomes without settling its pending API, configuration-schema, or isolation-design decisions.

## Milestone 0: Establish the harness development foundation

Contributors set up this repository for harness development, run the CLI from the local source checkout, and verify changes using documented checks. Automated CI checks verify changes, and clean-environment package checks verify distributable artifacts. This milestone establishes the development foundation for the experiment-user capabilities introduced in Milestone 1.

See the design's [Milestone 0 dependencies and delivery order](design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order) for capability dependencies between these stories and recommended implementation sequencing.

### US-31: Set up the harness development environment

As a contributor, I want documented steps to set up this repository for local development so that I can make changes and verify them consistently.

Acceptance criteria:

- <a id="us-31-ac-01"></a> **US-31-AC-01:** Documented prerequisites specify Python 3.12 or newer and required tools, and identify the Python versions verified by CI. macOS is the initial verified development platform; Linux and Windows remain eligible for future verification, and platform-specific requirements and known limitations are documented.
- <a id="us-31-ac-02"></a> **US-31-AC-02:** Instructions cover cloning the harness repository and installing runtime and development dependencies using `uv` and the committed lockfile.
- <a id="us-31-ac-03"></a> **US-31-AC-03:** Contributors can run the harness CLI from the local source checkout.
- <a id="us-31-ac-04"></a> **US-31-AC-04:** Documented commands run automated tests, linting, formatting checks, and type checks.
- <a id="us-31-ac-05"></a> **US-31-AC-05:** A documented smoke check confirms that the environment is ready for development.
- <a id="us-31-ac-06"></a> **US-31-AC-06:** Setup identifies required configuration and credentials and provides local defaults where practical.
- <a id="us-31-ac-07"></a> **US-31-AC-07:** Setup instructions are verified on macOS from a fresh checkout and a new development environment using only the documented prerequisites and setup steps. Verification runs all documented development checks, including `agent-ml --version`, and records the operating system and Python/tool versions, commands run, and results as review evidence.
- <a id="us-31-ac-08"></a> **US-31-AC-08:** The repository includes configuration for automated tests, linting, formatting, and type checking. Tool versions are controlled through the development dependencies and committed lockfile, and the documented local commands use these configurations.
- <a id="us-31-ac-09"></a> **US-31-AC-09:** Documented Python coding conventions cover naming, typing, docstrings, imports, and error handling. Automated checks enforce the conventions that the selected tools can verify.
- <a id="us-31-ac-10"></a> **US-31-AC-10:** Documented guidance defines when and how contributors may add rule suppressions and check exclusions, requiring a recorded justification for each exception so that it can be reviewed.

### US-32: Verify changes automatically in CI

As a contributor, I want automated checks on every pull request so that I receive consistent feedback before changes are merged.

Acceptance criteria:

- <a id="us-32-ac-01"></a> **US-32-AC-01:** CI runs on pull requests and updates to the default branch from a clean checkout, using macOS as the initial verification platform.
- <a id="us-32-ac-02"></a> **US-32-AC-02:** CI verifies Python 3.12 as the minimum supported version, documents any additional Python versions tested, installs the required tools, and synchronizes runtime and development dependencies using `uv` and the committed lockfile without modifying the lockfile.
- <a id="us-32-ac-03"></a> **US-32-AC-03:** CI runs automated tests, linting, formatting checks, type checks, and the development smoke check using the same documented commands available locally under US-31.
- <a id="us-32-ac-04"></a> **US-32-AC-04:** Failed checks produce a failing CI result, and contributors can inspect check results and diagnostic logs from the pull request.

### US-33: Build and verify the harness package

As a contributor, I want to build and verify distributable packages with a minimal CLI that reports its version so that I can confirm the harness installs and runs outside the source checkout.

Acceptance criteria:

- <a id="us-33-ac-01"></a> **US-33-AC-01:** A documented command builds both wheel and source distributions from the repository.
- <a id="us-33-ac-02"></a> **US-33-AC-02:** Verification installs the built wheel and its declared runtime dependencies in a clean environment and runs outside the source checkout without relying on an editable installation or development dependencies.
- <a id="us-33-ac-03"></a> **US-33-AC-03:** Installed-package checks verify the `agent-ml` CLI, `agentic_ml` imports, and access to at least one minimal packaged template and one minimal runtime guidance file. Both files have explicitly provisional contents for Milestone 0; checks read them through the installed package and compare their contents with expected values. Usable experiment initialization resources are delivered in Milestone 1.
- <a id="us-33-ac-04"></a> **US-33-AC-04:** Verification builds a wheel from the source distribution and confirms that it passes the same installed-package checks.
- <a id="us-33-ac-05"></a> **US-33-AC-05:** CI runs package build and verification checks and reports failures with diagnostic logs; the commands are documented for local reproduction.
- <a id="us-33-ac-06"></a> **US-33-AC-06:** The Milestone 0 CLI provides `agent-ml --version`, which prints the installed package version and exits successfully. The reported version matches the installed distribution metadata. Experiment commands are introduced in later milestones.
- <a id="us-33-ac-07"></a> **US-33-AC-07:** The installed-package checks run `agent-ml --version` for both the directly built wheel and the wheel rebuilt from the source distribution, verifying successful exit and the expected version. The documented source-checkout smoke check also runs `agent-ml --version`.

## Milestone 1: Run and record a reproducible experiment

Starting with Python and local raw data, the developer creates a separate experiment repository and completes an extraction-to-recorded-notebook run without requiring an agent or a manually maintained harness checkout. Developers may use an external coding assistant to prepare inputs and code and invoke the public harness CLI/API without an agent adapter; the harness must validate, record, and execute supplied inputs without an agent dependency. This milestone covers extraction, snapshots, basic validation and review, recorded execution, and restoration. Detailed profiling and train/validation/protected-test splits are introduced in Milestone 2; Milestone 1 versioning and restoration cover the source dataset and recorded run inputs.

### US-01: Install a pinned harness version

As a developer, I want to install a pinned harness version into my own experiment repository so that my project has a reproducible environment.

Acceptance criteria:

- <a id="us-01-ac-01"></a> **US-01-AC-01:** Documented bootstrap instructions cover installing `uv` and Git, creating the user Git/Python project, and installing the harness from GitHub at a full commit SHA.
- <a id="us-01-ac-02"></a> **US-01-AC-02:** The harness is a normal installed dependency; runtime use requires no manually maintained harness checkout or installer cache.
- <a id="us-01-ac-03"></a> **US-01-AC-03:** The project lockfile records the resolved harness revision and dependencies; the installed package exposes `agent-ml`, `agentic_ml`, templates, and runtime guidance.
- <a id="us-01-ac-04"></a> **US-01-AC-04:** An explicit harness upgrade changes the commit pin and lockfile, producing a new environment identity.

Architecture references: [§8 Project initialization and installation](design/interfaces-and-configuration.md#project-initialization-and-installation); [§9 Execution](design/execution-and-governance.md#execution).

### US-02: Initialize an experiment project

As a developer, I want to initialize configuration, notebooks, dependencies, and local storage while preserving existing files so that I can start experimenting safely.

Acceptance criteria:

- <a id="us-02-ac-01"></a> **US-02-AC-01:** `uv run agent-ml init` adds project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and required project-package scaffolding.
- <a id="us-02-ac-02"></a> **US-02-AC-02:** Initialization preserves existing files and the pinned harness dependency, reporting conflicts instead of silently overwriting files.
- <a id="us-02-ac-03"></a> **US-02-AC-03:** Required ML, notebook execution, and JupyterLab dependencies are declared and synchronized with the project environment and lockfile.
- <a id="us-02-ac-04"></a> **US-02-AC-04:** Project-associated DVC, MLflow, and durable-state storage are initialized with local defaults and configurable locations.
- <a id="us-02-ac-05"></a> **US-02-AC-05:** Data access, agent authentication, and approval presentation remain explicit setup choices; initialization grants no execution or data-access authorization, and credentials remain outside committed configuration.

Architecture references: [§8 Project initialization and installation](design/interfaces-and-configuration.md#project-initialization-and-installation).

### US-03: Define experiment objectives and boundaries

As a data scientist, I want to describe objectives and constraints in Markdown and declare search boundaries in YAML so that agents work toward my intended outcome.

Acceptance criteria:

- <a id="us-03-ac-01"></a> **US-03-AC-01:** The experiment brief captures data, target, task type, feature guidance, metric and direction, split constraints, algorithm mode, and budgets, including explicitly delegated decisions.
- <a id="us-03-ac-02"></a> **US-03-AC-02:** Search-space YAML declares allowed algorithms, fixed parameters, and tunable choices or ranges; execution configuration cannot expand these boundaries.
- <a id="us-03-ac-03"></a> **US-03-AC-03:** Resolved inputs produce a versioned plan containing the effective decisions, source references, and checksums before dependent execution.
- <a id="us-03-ac-04"></a> **US-03-AC-04:** Ambiguous or conflicting requirements block affected runs until resolved; delegated decisions require approval before use.
- <a id="us-03-ac-05"></a> **US-03-AC-05:** Relative input paths resolve against the experiment repository root, with the notebook working directory recorded explicitly.

Architecture references: [§8 Developer experiment inputs](design/interfaces-and-configuration.md#developer-experiment-inputs); [§8 Algorithm and hyperparameter configuration](design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration).

### US-05: Reject invalid configurations before execution

As a data scientist, I want invalid algorithms, parameters, and search configurations rejected before training so that compute is spent on valid candidates.

Acceptance criteria:

- <a id="us-05-ac-01"></a> **US-05-AC-01:** Validation checks registered algorithm identifiers, task compatibility, parameter names, types, defaults, and compatible combinations.
- <a id="us-05-ac-02"></a> **US-05-AC-02:** Categorical choices are nonempty; numeric bounds are ordered and inclusive; integer ranges yield integers; logarithmic bounds are strictly positive.
- <a id="us-05-ac-03"></a> **US-05-AC-03:** Fixed values remain fixed, and omitted parameters use recorded registry defaults without becoming tunable.
- <a id="us-05-ac-04"></a> **US-05-AC-04:** Invalid inputs produce actionable validation errors before training starts.
- <a id="us-05-ac-05"></a> **US-05-AC-05:** As training entrypoints are introduced, every candidate submitted through Python, custom code, or notebooks receives the same boundary checks.

Architecture references: [§8 Algorithm and hyperparameter configuration](design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration); [§8 User-supplied ML components](design/interfaces-and-configuration.md#user-supplied-ml-components).

### US-09: Execute saved notebooks reproducibly

As a data scientist, I want saved notebooks executed automatically from a fresh kernel with explicit inputs so that recorded results do not depend on hidden state.

Acceptance criteria:

- <a id="us-09-ac-01"></a> **US-09-AC-01:** Managed execution uses the selected project's locked environment, a fresh kernel, cell order, explicit parameters, and a recorded working directory.
- <a id="us-09-ac-02"></a> **US-09-AC-02:** The run preserves the source notebook, parameters, environment identity, executed notebook with cell outputs, errors, and generated artifacts.
- <a id="us-09-ac-03"></a> **US-09-AC-03:** Notebook-to-notebook dependencies use recorded artifact references rather than another kernel's variables.
- <a id="us-09-ac-04"></a> **US-09-AC-04:** Cell errors, timeouts, and cancellation produce the corresponding run status; successful execution remains subject to independent validation.
- <a id="us-09-ac-05"></a> **US-09-AC-05:** Access restrictions, approvals, and budgets apply equally to notebook and Python entrypoints; unauthorized filesystem or credential access is blocked.

Architecture references: [§9 Execution](design/execution-and-governance.md#execution); [§9 Notebook development and execution contract](design/execution-and-governance.md#notebook-development-and-execution-contract).

### US-10: Control and inspect runs

As a data scientist, I want to submit, monitor, cancel, and inspect runs so that I can control execution and understand failures.

Acceptance criteria:

- <a id="us-10-ac-01"></a> **US-10-AC-01:** The local runner supports submission, status inspection, cancellation, logs, and artifact retrieval through the harness interfaces.
- <a id="us-10-ac-02"></a> **US-10-AC-02:** Runs record completion, failure, timeout, or cancellation outcomes with available diagnostic evidence.
- <a id="us-10-ac-03"></a> **US-10-AC-03:** Runtime and experiment-count limits prevent further unauthorized work; supported resource limits are enforced.
- <a id="us-10-ac-04"></a> **US-10-AC-04:** Unsuccessful model performance is distinguishable from execution failure when modeling is added.
- <a id="us-10-ac-05"></a> **US-10-AC-05:** Cancelled or budget-exhausted work preserves available evidence for review.

Architecture references: [§8 ExperimentRunner interface](design/interfaces-and-configuration.md#8-interfaces-and-contracts); [§9 Execution](design/execution-and-governance.md#execution); [§9 Workflow states](design/execution-and-governance.md#workflow-states).

### US-11: Extract approved source data

As a data scientist, I want approved data extracted from supported local, SQL, or object-storage sources so that I can work with existing datasets.

Acceptance criteria:

- <a id="us-11-ac-01"></a> **US-11-AC-01:** Initial connectors support local CSV/Parquet, SQL, and object storage; acceptance demonstrations extract data from at least two source types.
- <a id="us-11-ac-02"></a> **US-11-AC-02:** Source discovery exposes permitted schema and metadata without unrestricted data exposure.
- <a id="us-11-ac-03"></a> **US-11-AC-03:** Extraction executes only approved queries or sampling plans within source allowlists, permissions, network restrictions, and cost/record limits.
- <a id="us-11-ac-04"></a> **US-11-AC-04:** Each snapshot records source identity, query, parameters, extraction time, checksums, and permissions metadata.
- <a id="us-11-ac-05"></a> **US-11-AC-05:** Extraction failures are reported without presenting incomplete output as a validated dataset.

Architecture references: [§6 Data extraction requirements](design/data-and-features.md#data-extraction-requirements).

### US-12: Validate extracted data

As a data scientist, I want basic data validation and review so that I can identify extraction and quality-rule failures before accepting a reproducible data run.

Acceptance criteria:

- <a id="us-12-ac-01"></a> **US-12-AC-01:** Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.
- <a id="us-12-ac-05"></a> **US-12-AC-05:** Basic validation results are presented for approval before the dataset is accepted for the Milestone 1 run.

Architecture references: [§4 Data extraction and EDA](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§5 Workflow phases and gates](agentic-ml-harness-design.md#5-standard-workflow-phases-and-gates); [§6 Data extraction requirements](design/data-and-features.md#data-extraction-requirements); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-13: Version and restore datasets

As a data scientist, I want to version and restore datasets with verified content hashes so that experiments use identifiable, recoverable inputs.

Acceptance criteria:

- <a id="us-13-ac-01"></a> **US-13-AC-01:** DVC versions source snapshots, split manifests, and derived datasets as those artifacts are introduced.
- <a id="us-13-ac-02"></a> **US-13-AC-02:** Git tracks DVC metadata and relevant manifests while dataset content resides in the configured cache/storage and is excluded from Git.
- <a id="us-13-ac-03"></a> **US-13-AC-03:** A dataset can be restored from configured storage using its recorded metadata, and restored content hashes are verified.
- <a id="us-13-ac-04"></a> **US-13-AC-04:** Missing or mismatched content prevents the dataset from being treated as successfully restored.

Architecture references: [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines).

### US-26: Record run artifacts and provenance

As a data scientist, I want recorded runs linked to their exact inputs, code, and environment so that I can inspect and audit results.

Acceptance criteria:

- <a id="us-26-ac-01"></a> **US-26-AC-01:** MLflow records run status, effective parameters, available metrics, outputs, and artifact references, linked to the harness run identifier.
- <a id="us-26-ac-02"></a> **US-26-AC-02:** Each run links to the exact DVC dataset state, experiment Git revision, source snapshots including uncommitted changes, and configuration checksums.
- <a id="us-26-ac-03"></a> **US-26-AC-03:** Provenance includes the harness repository URL, full commit SHA, package version, build identity where available, and project lockfile/environment identity.
- <a id="us-26-ac-04"></a> **US-26-AC-04:** Source snapshots include notebooks, imported helpers, project code, configuration, and applicable runtime guidance; later milestones extend these records to components, pipelines, and approvals.
- <a id="us-26-ac-05"></a> **US-26-AC-05:** Basic execution correctness is independently checked against expected artifacts; notebook completion alone does not establish experiment acceptance.

Architecture references: [§3 Component responsibilities](agentic-ml-harness-design.md#component-responsibilities); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-27: Reproduce a basic run in a clean environment

As a collaborating data scientist, I want to reproduce an experiment on another machine so that I can independently check its results.

Acceptance criteria:

- <a id="us-27-ac-01"></a> **US-27-AC-01:** An experiment checkout, recorded source snapshots, lockfile, and dataset metadata restore the pinned harness commit and required inputs without a maintained harness checkout.
- <a id="us-27-ac-02"></a> **US-27-AC-02:** Reproduction executes the recorded source, including preserved uncommitted changes, rather than assuming the Git revision alone identifies it.
- <a id="us-27-ac-03"></a> **US-27-AC-03:** Declared output checks or tolerances determine whether the basic run reproduces successfully; metric tolerances apply when modeling is introduced.
- <a id="us-27-ac-04"></a> **US-27-AC-04:** Missing source, dependencies, or dataset content is reported explicitly instead of silently substituted.

Architecture references: [§8 Project initialization and installation](design/interfaces-and-configuration.md#project-initialization-and-installation); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

## Milestone 2: Assess data and build reproducible feature pipelines

Starting with versioned source data, the developer profiles the dataset, creates versioned training/validation/protected-test splits respecting time and group constraints, and obtains approval of the assessment and split protocol before dependent feature or modeling work. The developer then prepares features, compares their predictive performance using a fixed approved reference estimator, metric, and split protocol, and restores fitted preprocessing and pipeline outputs. Milestone 2 includes the minimal training/evaluation capability for these comparisons; broader model experimentation remains in Milestone 3.

### US-12: Assess data quality and define splits

As a data scientist, I want detailed data-quality assessments and an explicit split protocol so that I can identify unsuitable data before feature engineering or modeling.

Acceptance criteria:

- <a id="us-12-ac-02"></a> **US-12-AC-02:** Assessment includes distributions, class balance where relevant, anomalies, and leakage diagnostics.
- <a id="us-12-ac-03"></a> **US-12-AC-03:** A versioned split manifest records training, validation, and protected-test partitions, respecting approved time or group constraints.
- <a id="us-12-ac-04"></a> **US-12-AC-04:** Dataset assessment and split protocol are presented for approval before dependent feature or modeling work.

Architecture references: [§4 Data extraction and EDA](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§5 Workflow phases and gates](agentic-ml-harness-design.md#5-standard-workflow-phases-and-gates); [§6 Data extraction requirements](design/data-and-features.md#data-extraction-requirements); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-14: Generate and compare feature pipelines

As a data scientist, I want agents to generate and compare feature pipelines on consistent splits so that feature improvements have credible evidence.

Acceptance criteria:

- <a id="us-14-ac-01"></a> **US-14-AC-01:** Feature plans identify ordered components, effective parameters, input/output schemas, fitting scope, and modification permissions.
- <a id="us-14-ac-02"></a> **US-14-AC-02:** The harness executes candidate transformations and records their definitions, dependencies, outputs, and lineage.
- <a id="us-14-ac-03"></a> **US-14-AC-03:** Candidate feature sets are compared for predictive performance against a fixed approved baseline feature set using the same fixed approved reference estimator, estimator settings, metric, and split protocol. Improvement follows the declared metric direction; comparisons record gains, ties, or regressions. Milestone 2 includes the minimal training/evaluation capability needed for this comparison; broader model experimentation remains in Milestone 3.
- <a id="us-14-ac-04"></a> **US-14-AC-04:** Feature artifacts trace back to their source datasets and are independently validated before workflow phase advancement.
- <a id="us-14-ac-05"></a> **US-14-AC-05:** This milestone supports supplied or explicitly authored candidates; agent generation is exercised when agent integration arrives in Milestone 4.

Architecture references: [§7 Feature Engineering](design/data-and-features.md#7-feature-engineering); [§5 Workflow phases and gates](agentic-ml-harness-design.md#5-standard-workflow-phases-and-gates).

### US-15: Preserve training-only preprocessing

As a data scientist, I want preprocessing fitted only on training data and preserved for reuse so that validation and inference transformations remain consistent.

Acceptance criteria:

- <a id="us-15-ac-01"></a> **US-15-AC-01:** Stateful preprocessing fits only on the approved training partition and applies unchanged fitted state to validation, test, and inference inputs.
- <a id="us-15-ac-02"></a> **US-15-AC-02:** Transformations that violate split boundaries or leakage rules are rejected.
- <a id="us-15-ac-03"></a> **US-15-AC-03:** Preparation code, fitted state, dependencies, parameters, and output schemas are preserved as artifacts.
- <a id="us-15-ac-04"></a> **US-15-AC-04:** Restored preprocessing reproduces validation and inference transformations under declared reproducibility checks.

Architecture references: [§7 Feature Engineering](design/data-and-features.md#7-feature-engineering); [§8 User-supplied ML components](design/interfaces-and-configuration.md#user-supplied-ml-components).

### US-16: Register supplied preprocessing components

As a data scientist, I want to register my existing preprocessors without changing the harness so that I can reuse domain-specific implementations.

Acceptance criteria:

- <a id="us-16-ac-01"></a> **US-16-AC-01:** Project configuration registers stateful preprocessors and stateless transformations from project code or pinned dependencies through versioned public interfaces.
- <a id="us-16-ac-02"></a> **US-16-AC-02:** Declarations include identifiers, entrypoints, interface versions, parameter specifications, and modification permissions; duplicate identifiers and incompatible interfaces are rejected.
- <a id="us-16-ac-03"></a> **US-16-AC-03:** Stateful components support fitting, transformation, and fitted-state persistence/restoration; stateless components declare their output schema.
- <a id="us-16-ac-04"></a> **US-16-AC-04:** Registered components follow the same validation, resource, access, and lineage rules as built-in components.
- <a id="us-16-ac-05"></a> **US-16-AC-05:** Lineage records declarations, exact code snapshots or pinned dependency identities, effective parameters, and fitted artifacts.

Architecture references: [§7 Feature Engineering](design/data-and-features.md#7-feature-engineering); [§8 User-supplied ML components](design/interfaces-and-configuration.md#user-supplied-ml-components); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-27: Reproduce and reuse pipeline stages

As a data scientist, I want reproducible pipeline stages and valid output reuse so that I can avoid redundant work while preserving trustworthy results.

Acceptance criteria:

- <a id="us-27-ac-05"></a> **US-27-AC-05:** DVC pipeline definitions record stage dependencies, parameters, and outputs, with resolved hashes preserved in `dvc.lock`.
- <a id="us-27-ac-06"></a> **US-27-AC-06:** Stage working directories and paths are explicit and consistent with harness execution.
- <a id="us-27-ac-07"></a> **US-27-AC-07:** Reproducing declared stages restores or generates the expected outputs under the recorded configuration.
- <a id="us-27-ac-08"></a> **US-27-AC-08:** Reused outputs retain producer provenance and remain subject to current authorization and evaluation checks.
- <a id="us-27-ac-09"></a> **US-27-AC-09:** Cache reuse alone does not establish experiment acceptance or bypass a gate.

Architecture references: [§8 Project initialization and installation](design/interfaces-and-configuration.md#project-initialization-and-installation); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

## Milestone 3: Train, tune, and independently evaluate models

Starting with approved features, the developer establishes baselines, compares and tunes candidates within declared limits, and obtains an independent assessment and final report.

### US-06: Choose an algorithm execution mode

As a data scientist, I want to use one algorithm, select among allowed algorithms, or compare the allowed set so that experimentation matches my question and budget.

Acceptance criteria:

- <a id="us-06-ac-01"></a> **US-06-AC-01:** Use mode runs the specified allowed algorithm; select mode records a selection from the allowed set; compare mode evaluates every algorithm in that set within the approved plan and budgets.
- <a id="us-06-ac-02"></a> **US-06-AC-02:** All modes respect task compatibility, parameter boundaries, and trial/runtime budgets.
- <a id="us-06-ac-03"></a> **US-06-AC-03:** Comparing algorithms does not require exhaustive enumeration of parameter combinations.
- <a id="us-06-ac-04"></a> **US-06-AC-04:** Suggested algorithms or expanded ranges are recorded only as recommendations for a subsequent experiment; adopting them requires a new versioned configuration and applicable approvals.

Architecture references: [§8 Developer experiment inputs](design/interfaces-and-configuration.md#developer-experiment-inputs); [§8 Algorithm and hyperparameter configuration](design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration).

### US-16: Register supplied models

As a data scientist, I want to register my existing model implementations without changing the harness so that I can reuse domain-specific training code.

Acceptance criteria:

- <a id="us-16-ac-06"></a> **US-16-AC-06:** Project-local or pinned-dependency models register through the public component interface without harness modifications.
- <a id="us-16-ac-07"></a> **US-16-AC-07:** Models support training on approved inputs, evaluator-compatible prediction, and fitted-model persistence/restoration.
- <a id="us-16-ac-08"></a> **US-16-AC-08:** Before training, validation rejects unsupported tasks, invalid parameters, incompatible interfaces, and prediction outputs incompatible with the approved metrics.
- <a id="us-16-ac-09"></a> **US-16-AC-09:** Supplied models can be tuned within approved boundaries and independently evaluated after restoration.
- <a id="us-16-ac-10"></a> **US-16-AC-10:** Component declarations, code/dependency identities, effective parameters, and fitted artifacts appear in run lineage.

Architecture references: [§7 Feature Engineering](design/data-and-features.md#7-feature-engineering); [§8 User-supplied ML components](design/interfaces-and-configuration.md#user-supplied-ml-components); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-18: Train across supported frameworks

As a data scientist, I want to train and evaluate scikit-learn, LightGBM, and PyTorch models so that I can compare approaches across supported frameworks.

Acceptance criteria:

- <a id="us-18-ac-01"></a> **US-18-AC-01:** End-to-end runs cover tabular classification, tabular regression, and a basic PyTorch deep-learning example.
- <a id="us-18-ac-02"></a> **US-18-AC-02:** A simple reproducible baseline is recorded and approved before candidate improvement comparisons.
- <a id="us-18-ac-03"></a> **US-18-AC-03:** Framework adapters expose training, prediction, and persistence operations usable by independent evaluation.
- <a id="us-18-ac-04"></a> **US-18-AC-04:** Each run records effective parameters, framework/library identities, metrics, model artifacts, and feature/data lineage.

Architecture references: [§4 Baseline modeling and Model development](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§8 ModelAdapter interface](design/interfaces-and-configuration.md#8-interfaces-and-contracts); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines).

### US-19: Manage PyTorch execution

As a data scientist, I want PyTorch runs to support CPU/GPU execution, checkpoints, and cancellation so that deep-learning experiments are manageable.

Acceptance criteria:

- <a id="us-19-ac-01"></a> **US-19-AC-01:** Basic PyTorch training runs on CPU and supports GPU execution when the required hardware/backend is available.
- <a id="us-19-ac-02"></a> **US-19-AC-02:** Checkpoints are captured as run artifacts and can be restored by the model implementation.
- <a id="us-19-ac-03"></a> **US-19-AC-03:** Cancellation stops managed training and preserves available logs, checkpoints, and status.
- <a id="us-19-ac-04"></a> **US-19-AC-04:** Resource requests, hardware metadata, runtime limits, and supported quotas are recorded and enforced where supported.

Architecture references: [§9 Execution](design/execution-and-governance.md#execution); [§8 ModelAdapter interface](design/interfaces-and-configuration.md#8-interfaces-and-contracts).

### US-20: Tune within declared limits

As a data scientist, I want bounded tuning with enforced trial and runtime limits so that agents cannot exceed the authorized search or budget.

Acceptance criteria:

- <a id="us-20-ac-01"></a> **US-20-AC-01:** Candidates use only declared algorithms, fixed values, categorical choices, and numeric ranges; omitted defaults cannot be tuned.
- <a id="us-20-ac-02"></a> **US-20-AC-02:** Candidate validation rejects boundary violations before training, including submissions from custom code and notebooks.
- <a id="us-20-ac-03"></a> **US-20-AC-03:** Experiment-count and runtime budgets stop new work and leave a reviewable summary of completed trials.
- <a id="us-20-ac-04"></a> **US-20-AC-04:** The optimization summary identifies the search performed, resources consumed, candidate evidence, and model proposed for final evaluation.

Architecture references: [§8 Algorithm and hyperparameter configuration](design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration); [§5 Optimization](agentic-ml-harness-design.md#5-standard-workflow-phases-and-gates); [§9 Execution](design/execution-and-governance.md#execution).

### US-21: Independently assess experiment results

As a data scientist, I want independent evaluation of execution, leakage, model quality, robustness, and reproducibility so that acceptance rests on evidence.

Acceptance criteria:

- <a id="us-21-ac-01"></a> **US-21-AC-01:** The evaluator checks successful execution and required artifacts independently of agent assertions.
- <a id="us-21-ac-02"></a> **US-21-AC-02:** Scientific-validity checks reject split violations, improper preprocessing fitting, and leakage.
- <a id="us-21-ac-03"></a> **US-21-AC-03:** Approved metrics and baseline comparisons are computed consistently, respecting optimization direction.
- <a id="us-21-ac-04"></a> **US-21-AC-04:** Defined folds, data slices, or stress tests assess robustness; repeated runs are checked against explicit reproducibility tolerances.
- <a id="us-21-ac-05"></a> **US-21-AC-05:** Structured evaluation results distinguish execution failure, scientific invalidity, and insufficient model quality.

Architecture references: [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-24: Protect final holdout evaluation

As a data scientist, I want protected holdout evaluation reserved for the authorized final workflow phase so that final-test results do not influence development.

Acceptance criteria:

- <a id="us-24-ac-01"></a> **US-24-AC-01:** Experiment agents, training code, and exploratory kernels cannot access protected test data; protection is enforced independently of agent instructions.
- <a id="us-24-ac-02"></a> **US-24-AC-02:** Only the independent evaluator accesses the holdout for the authorized final evaluation.
- <a id="us-24-ac-03"></a> **US-24-AC-03:** Protected-test results cannot drive feature, model, or acquisition improvement loops.
- <a id="us-24-ac-04"></a> **US-24-AC-04:** Unsuccessful final evaluation ends in rejection or review; further development requires a separately approved protocol preserving holdout protection.
- <a id="us-24-ac-05"></a> **US-24-AC-05:** Completion requires developer approval of successful final evaluation.

Architecture references: [§4 Final evaluation](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§9 Notebook development and execution contract](design/execution-and-governance.md#notebook-development-and-execution-contract); [§9 Governance](design/execution-and-governance.md#governance); [ADR-006](design/architecture-decisions.md#pending-decisions).

### US-26: Compare runs and review the final report

As a data scientist, I want run comparisons and a final report linked to their evidence so that I can judge the model against the original objective.

Acceptance criteria:

- <a id="us-26-ac-06"></a> **US-26-AC-06:** MLflow comparisons expose effective parameters, metrics, execution status, and model artifacts for baseline and candidate runs.
- <a id="us-26-ac-07"></a> **US-26-AC-07:** The final report identifies the model, approved metrics, baseline comparison, validity/robustness/reproducibility findings, and acceptance outcome.
- <a id="us-26-ac-08"></a> **US-26-AC-08:** Model lineage traces through component identities, fitted feature pipelines, source datasets, exact code/configuration snapshots, and environment identity.
- <a id="us-26-ac-09"></a> **US-26-AC-09:** Reports preserve references to independent evaluation evidence rather than treating generated narrative as proof of acceptance.

Architecture references: [§3 Component responsibilities](agentic-ml-harness-design.md#component-responsibilities); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

## Milestone 4: Let an agent improve an experiment

An agent resolves delegated choices, generates notebooks, and improves a model using development feedback while the developer retains control of workflow phase scope and component permissions.

### US-04: Approve delegated experiment decisions

As a data scientist, I want agents to propose delegated feature, metric, and algorithm decisions for approval so that I retain control over the experiment design.

Acceptance criteria:

- <a id="us-04-ac-01"></a> **US-04-AC-01:** Agents resolve only explicitly delegated choices and record the proposed decisions and reasoning in the structured plan.
- <a id="us-04-ac-02"></a> **US-04-AC-02:** The plan identifies features, metric and direction, split protocol, allowed algorithms, and budgets.
- <a id="us-04-ac-03"></a> **US-04-AC-03:** Ambiguities and conflicts are surfaced before affected execution, and dependent work waits for approval through applicable gates.
- <a id="us-04-ac-04"></a> **US-04-AC-04:** Original inputs, resolved decisions, and their versions/checksums remain available in run lineage.

Architecture references: [§8 Developer experiment inputs](design/interfaces-and-configuration.md#developer-experiment-inputs); [§4 Problem definition](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow).

### US-07: Generate reviewable experiment notebooks

As a data scientist, I want agents to generate readable notebooks and project code so that I can inspect, edit, and understand their work.

Acceptance criteria:

- <a id="us-07-ac-01"></a> **US-07-AC-01:** Generated notebooks include explanatory Markdown covering objectives, assumptions, code, results, and proposed next steps, with explicit parameter cells.
- <a id="us-07-ac-02"></a> **US-07-AC-02:** Notebooks import generic capabilities from the installed harness and shared project logic from the experiment package without paths into a harness checkout.
- <a id="us-07-ac-03"></a> **US-07-AC-03:** Saved notebooks support interactive use and fresh-kernel managed execution without hidden state.
- <a id="us-07-ac-04"></a> **US-07-AC-04:** Generated notebooks, helpers, and project code stay within the experiment repository and authorized storage; the harness installation/source remain unchanged.

Architecture references: [§9 Notebook development and execution contract](design/execution-and-governance.md#notebook-development-and-execution-contract); [§3 Harness and experiment project boundary](agentic-ml-harness-design.md#harness-and-experiment-project-boundary).

### US-08: Explore interactively under the same controls

As a data scientist, I want to explore interactively in JupyterLab under the experiment's access rules so that exploration preserves evaluation integrity.

Acceptance criteria:

- <a id="us-08-ac-01"></a> **US-08-AC-01:** JupyterLab launches from the project environment with the required notebook dependencies.
- <a id="us-08-ac-02"></a> **US-08-AC-02:** Interactive kernels cannot access protected test data, including through arbitrary Python outside harness API calls.
- <a id="us-08-ac-03"></a> **US-08-AC-03:** Training cells submit through managed APIs that enforce candidate boundaries, applicable approvals, budgets, and tracking.
- <a id="us-08-ac-04"></a> **US-08-AC-04:** Interactive execution cannot establish acceptance; recorded results require managed execution of saved snapshots and independent evaluation.

Architecture references: [§9 Notebook development and execution contract](design/execution-and-governance.md#notebook-development-and-execution-contract); [§8 Project initialization and installation](design/interfaces-and-configuration.md#project-initialization-and-installation); [ADR-006](design/architecture-decisions.md#pending-decisions).

### US-17: Respect immutable supplied components

As a data scientist, I want supplied code to remain immutable unless I approve changes so that agents respect ownership and component permissions.

Acceptance criteria:

- <a id="us-17-ac-01"></a> **US-17-AC-01:** Supplied components are immutable by default; agents may configure and invoke them only within authorized boundaries.
- <a id="us-17-ac-02"></a> **US-17-AC-02:** Attempts to modify immutable components are blocked unless recorded developer approval authorizes the change.
- <a id="us-17-ac-03"></a> **US-17-AC-03:** Approved changes to immutable code create a new versioned experiment configuration.
- <a id="us-17-ac-04"></a> **US-17-AC-04:** Modification permission does not expand algorithm, parameter, data-access, or evaluation boundaries; authorized code changes appear in run snapshots.

Architecture references: [§8 User-supplied ML components](design/interfaces-and-configuration.md#user-supplied-ml-components); [§4 Scope changes](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow).

### US-22: Improve models using development feedback

As a data scientist, I want agents to revise experiments using structured development feedback so that model improvement can proceed within approved scope.

Acceptance criteria:

- <a id="us-22-ac-01"></a> **US-22-AC-01:** The agent receives structured evaluation feedback and produces revised notebooks or code with an evidence-based explanation.
- <a id="us-22-ac-02"></a> **US-22-AC-02:** Revisions remain within the current approved workflow phase, component permissions, parameter boundaries, access scope, and budgets.
- <a id="us-22-ac-03"></a> **US-22-AC-03:** Each revision undergoes managed execution and independent evaluation, preserving its source snapshots and results.
- <a id="us-22-ac-04"></a> **US-22-AC-04:** Iteration stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or developer cancellation.
- <a id="us-22-ac-05"></a> **US-22-AC-05:** Workflow phase returns and scope expansions await authorization; protected-test feedback never enters the revision loop.

Architecture references: [§4 Hierarchical Closed-Loop Workflow](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

### US-30: Connect the first agent with preserved runtime guidance

As a data scientist, I want an agent adapter with explicit, preserved runtime guidance so that agent behavior follows the approved experiment context.

Acceptance criteria:

- <a id="us-30-ac-01"></a> **US-30-AC-01:** The first managed coding-assistant adapter verifies a concrete product/interface/version and supports capability discovery, structured task/result exchange, and documented task cancellation through the common contract. Interactive assistants can use the public harness CLI/API without an adapter. Acceptance demonstrates task receipt, project-code/notebook revision, managed execution, development-feedback consumption, and stopping at a developer approval boundary.
- <a id="us-30-ac-02"></a> **US-30-AC-02:** Runtime loading explicitly selects packaged shared guidance, relevant task-specific guidance, and configured project guidance, recording ownership and order.
- <a id="us-30-ac-03"></a> **US-30-AC-03:** Development `AGENTS.md` files from either repository are excluded from automatic loading by the harness runtime loader. Instructions independently loaded by an external assistant are outside this guarantee; observable additional context and capture limitations are recorded.
- <a id="us-30-ac-04"></a> **US-30-AC-04:** The plan snapshots harness-supplied guidance contents, paths, versions/checksums, and load order; subsequent tasks reference the preserved bundle, with managed adapters demonstrating delivery. This records harness-supplied guidance, not the assistant's complete instruction context.
- <a id="us-30-ac-05"></a> **US-30-AC-05:** Conflicting guidance or attempts to expand experiment constraints block affected execution; adopting changed guidance requires a new versioned configuration and applicable approvals.

Architecture references: [§8 AgentAdapter interface](design/interfaces-and-configuration.md#8-interfaces-and-contracts); [§8 Development and runtime agent instructions](design/interfaces-and-configuration.md#development-and-runtime-agent-instructions).

## Milestone 5: Supervise and resume the complete workflow

The developer supervises all workflow phases through durable, scoped approval decisions, recovers interrupted work, and can use another agent adapter without changing experiment contracts.

### US-23: Approve workflow phase progression and scope changes

As a data scientist, I want to approve, revise, or reject workflow phase progression using validated evidence so that I supervise consequential decisions.

Acceptance criteria:

- <a id="us-23-ac-01"></a> **US-23-AC-01:** Initial plan approval completes problem definition; later workflow phase advancement is blocked until sufficient independent evidence and developer approval are recorded.
- <a id="us-23-ac-02"></a> **US-23-AC-02:** Each decision records an authenticated developer reviewer, reviewed plan/configuration identity and scope, decision, timestamp, and associated evidence in durable project-associated state. Agent actions and assistant tool-execution permissions cannot stand in for developer approval.
- <a id="us-23-ac-03"></a> **US-23-AC-03:** Revision authorizes work only within its recorded scope; workflow phase returns, expanded permissions, and changed evaluation criteria require authorization before execution.
- <a id="us-23-ac-04"></a> **US-23-AC-04:** Workflow phases can be skipped only when the approved plan identifies valid existing artifacts supporting the skip.
- <a id="us-23-ac-05"></a> **US-23-AC-05:** Rejection or cancellation preserves results; successful final evaluation requires explicit model approval before completion.

Architecture references: [§4 Hierarchical Closed-Loop Workflow](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§5 Workflow phases and gates](agentic-ml-harness-design.md#5-standard-workflow-phases-and-gates); [§9 Governance](design/execution-and-governance.md#governance).

### US-25: Resume interrupted workflows

As a data scientist, I want interrupted workflows to resume from durable state without repeating completed runs so that work and approvals are preserved.

Acceptance criteria:

- <a id="us-25-ac-01"></a> **US-25-AC-01:** Project-associated durable state preserves workflow phase progress, run identifiers, evidence, approvals, budgets, and terminal or reviewable outcomes.
- <a id="us-25-ac-02"></a> **US-25-AC-02:** Recovery reconciles recorded work and resumes without duplicating completed runs or bypassing pending gates.
- <a id="us-25-ac-03"></a> **US-25-AC-03:** Resumed tasks use the preserved compatible configuration and runtime instruction bundle, even if source guidance has changed.
- <a id="us-25-ac-04"></a> **US-25-AC-04:** Cancelled, failed, budget-exhausted, and review-required outcomes retain evidence and do not silently authorize further work.

Architecture references: [§3 Component responsibilities](agentic-ml-harness-design.md#component-responsibilities); [§9 Workflow states](design/execution-and-governance.md#workflow-states); [§8 Development and runtime agent instructions](design/interfaces-and-configuration.md#development-and-runtime-agent-instructions).

### US-30: Use interchangeable agent adapters

As a data scientist, I want interchangeable agent adapters so that I can change assistants without redefining the experiment workflow.

Acceptance criteria:

- <a id="us-30-ac-06"></a> **US-30-AC-06:** Two adapters successfully execute tasks using the same versioned task/result contract.
- <a id="us-30-ac-07"></a> **US-30-AC-07:** Capability discovery identifies which tasks each adapter supports before delegation.
- <a id="us-30-ac-08"></a> **US-30-AC-08:** Both managed adapters meet the common cancellation, harness-guidance delivery, developer-approval, access, and harness-run budget requirements, including boundaries for assistant tools/workspaces. Agent-task cancellation is recorded separately from experiment-run cancellation; assistant usage measurement/control capabilities and limitations are explicit. Resumption uses durable task/run evidence and consumed budgets rather than assistant memory.
- <a id="us-30-ac-09"></a> **US-30-AC-09:** Agent selection does not alter independent evaluation or the experiment's allowed boundaries.

Architecture references: [§8 AgentAdapter interface](design/interfaces-and-configuration.md#8-interfaces-and-contracts); [§8 Development and runtime agent instructions](design/interfaces-and-configuration.md#development-and-runtime-agent-instructions).

### US-26: Audit workflow decisions and evidence

As a reviewer, I want run lineage connected to workflow decisions so that I can reconstruct what was authorized, executed, and accepted.

Acceptance criteria:

- <a id="us-26-ac-10"></a> **US-26-AC-10:** Harness manifests connect runs, MLflow records, DVC state, configuration versions, runtime bundles, and approval records.
- <a id="us-26-ac-11"></a> **US-26-AC-11:** The audit trail identifies the scope authorizing each workflow phase, approved scope changes, and the evidence used for each decision.
- <a id="us-26-ac-12"></a> **US-26-AC-12:** Bidirectional run references allow lookup from a harness result to its MLflow run and from the tracking record to harness provenance.
- <a id="us-26-ac-13"></a> **US-26-AC-13:** Resumption and reuse preserve original producer provenance and the decisions authorizing subsequent use.

Architecture references: [§3 Component responsibilities](agentic-ml-harness-design.md#component-responsibilities); [§9 Experiment tracking, data versioning, and pipelines](design/execution-and-governance.md#experiment-tracking-data-versioning-and-pipelines); [§9 Independent evaluation](design/execution-and-governance.md#independent-evaluation).

## Milestone 6: Improve the dataset through authorized acquisition

The developer reviews evidence of data limitations, authorizes a bounded acquisition, and evaluates the effect of the resulting dataset through approved downstream work.

### US-28: Diagnose data gaps and propose acquisition

As a data scientist, I want evidence-backed data-gap diagnoses and acquisition proposals so that I can decide whether additional data is worth obtaining.

Acceptance criteria:

- <a id="us-28-ac-01"></a> **US-28-AC-01:** Diagnosis records evidence of data deficiencies, such as underrepresented classes or data slices, using approved data and development evaluation results.
- <a id="us-28-ac-02"></a> **US-28-AC-02:** A structured proposal records its reason, evidence, acquisition hypothesis, source, strategy, expected benefit, costs, limits, and required authorization.
- <a id="us-28-ac-03"></a> **US-28-AC-03:** Expected benefit is presented as a hypothesis rather than a guaranteed improvement.
- <a id="us-28-ac-04"></a> **US-28-AC-04:** Proposals do not use protected final-test feedback or expand access, evaluation protocols, or budgets without approval.

Architecture references: [§6 Acquisition strategies and Acquisition proposal contract](design/data-and-features.md#6-data-extraction-and-iterative-acquisition); [§4 Outer loop](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow).

### US-29: Acquire data and measure its effect within approved limits

As a data scientist, I want authorized acquisition to enforce limits, version new data, compare outcomes, and stop at defined conditions so that data improvement remains controlled.

Acceptance criteria:

- <a id="us-29-ac-01"></a> **US-29-AC-01:** Acquisition is blocked without recorded authorization covering source, strategy, scope, and limits; approved in-scope activity need not request permission for every operation.
- <a id="us-29-ac-02"></a> **US-29-AC-02:** Execution enforces source permissions and cost, record, runtime, and compute budgets, preserving evidence when a limit is reached.
- <a id="us-29-ac-03"></a> **US-29-AC-03:** Acquired data is validated and versioned with source lineage; synthetic or augmented data is explicitly identified as distinct from observed data.
- <a id="us-29-ac-04"></a> **US-29-AC-04:** Returning to validation/EDA and downstream development requires the applicable workflow phase authorization, with complete audit records.
- <a id="us-29-ac-05"></a> **US-29-AC-05:** Before-and-after model comparisons use consistent approved evaluation protocols and link results to the corresponding dataset versions.
- <a id="us-29-ac-06"></a> **US-29-AC-06:** The acquisition loop stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or cancellation, preserving a reviewable outcome.
- <a id="us-29-ac-07"></a> **US-29-AC-07:** Resumption after acquisition retains approvals, budget usage, dataset lineage, and completed-run identities; advanced acquisition strategies remain deferred according to the design's [milestone delivery plan](design/milestone-delivery.md#11-milestone-delivery-plan).

Architecture references: [§6 Data Extraction and Iterative Acquisition](design/data-and-features.md#6-data-extraction-and-iterative-acquisition); [§4 Scope changes and stopping conditions](agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow); [§9 Governance](design/execution-and-governance.md#governance).

## Milestone 99: Future enhancements

This milestone groups enhancements that are not critical to current functionality. Inclusion records deferred scope rather than a commitment to delivery order. Unlike Milestones 0–6, this milestone is a backlog of future enhancements; stories can move into a delivery milestone when prioritized, preserving their acceptance criterion IDs.

### US-34: Establish contribution and review checks

As a contributor, I want clear contribution instructions and consistent review checks so that I understand how to submit changes and when they are ready to merge.

Acceptance criteria:

- <a id="us-34-ac-01"></a> **US-34-AC-01:** Contribution instructions describe how to prepare and submit changes and link to the development setup and verification commands.
- <a id="us-34-ac-02"></a> **US-34-AC-02:** Required CI checks and review expectations are documented, including the conditions for merging a pull request.
- <a id="us-34-ac-03"></a> **US-34-AC-03:** Branch protection enforces the documented required checks and review expectations on the default branch.
