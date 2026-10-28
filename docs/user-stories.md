| Slice | User-visible outcome | Stories |
|---|---|---|
| **1. Run and record a reproducible experiment** | Initialize a separate project, extract and validate data, execute a notebook, inspect its recorded results, and reproduce the run. | US-01, US-02, US-03, US-05, US-09, US-10, US-11, US-12, US-13; initial US-26 and US-27 |
| **2. Build and compare reproducible features** | Produce and compare feature pipelines whose fitted state and outputs can be restored. | US-14, US-15; preprocessing portion of US-16; pipeline portion of US-27 |
| **3. Train, tune, and independently evaluate models** | Compare baselines and candidate models within declared boundaries and obtain an independent assessment. | US-06, US-18, US-19, US-20, US-21, US-24; model portion of US-16; reporting portion of US-26 |
| **4. Let an agent improve an experiment** | Generate reviewable notebooks and improve a model using development feedback within an approved phase. | US-04, US-07, US-08, US-17, US-22; first-adapter portion of US-30 |
| **5. Supervise and resume the complete workflow** | Run the multi-phase workflow with durable approvals, interruption recovery, and interchangeable agents. | US-23, US-25; second-adapter portion of US-30; audit portion of US-26 |
| **6. Improve the dataset through authorized acquisition** | Diagnose a data limitation, authorize acquisition, version the resulting data, and measure the effect of retraining. | US-28, US-29 |

These candidate stories derive from the [Agentic ML Development Harness architecture proposal](specs/agentic-ml-harness-proposal.md), version 0.10. AC references identify the proposal's acceptance criteria; section references identify additional requirements. The stories describe proposed behavior, not implemented capabilities or finalized interfaces.

Slices are cumulative. Repeated story identifiers describe incremental delivery of the same user outcome. Access controls, applicable approvals, budget enforcement, independent validation, and provenance accompany each capability when introduced; Slice 5 completes their durable multi-phase orchestration. Candidate acceptance criteria below make the proposal testable without settling its pending API, configuration-schema, or isolation-design decisions.

## Slice 1: Run and record a reproducible experiment

Starting with Python and local raw data, the developer creates a separate experiment repository and completes an extraction-to-recorded-notebook run without an agent or a manually maintained harness checkout.

### US-01: Install a pinned harness version

As a developer, I want to install a pinned harness version into my own experiment repository so that my project has a reproducible environment.

Acceptance criteria:

- Documented bootstrap instructions cover installing `uv` and Git, creating the user Git/Python project, and installing the harness from GitHub at a full commit SHA.
- The harness is a normal installed dependency; runtime use requires no manually maintained harness checkout or installer cache.
- The project lockfile records the resolved harness revision and dependencies; the installed package exposes `agent-ml`, `agentic_ml`, templates, and runtime guidance.
- An explicit harness upgrade changes the commit pin and lockfile, producing a new environment identity.

Proposal references: AC-41, AC-48; §8 installation.

### US-02: Initialize an experiment project

As a developer, I want to initialize configuration, notebooks, dependencies, and local storage while preserving existing files so that I can start experimenting safely.

Acceptance criteria:

- `uv run agent-ml init` adds project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and required project-package scaffolding.
- Initialization preserves existing files and the pinned harness dependency, reporting conflicts instead of silently overwriting files.
- Required ML, notebook execution, and JupyterLab dependencies are declared and synchronized with the project environment and lockfile.
- Project-associated DVC, MLflow, and durable-state storage are initialized with local defaults and configurable locations.
- Data access, agent authentication, and approval presentation remain explicit setup choices; initialization grants no execution or data-access authorization, and credentials remain outside committed configuration.

Proposal references: AC-41, AC-49; §8 initialization.

### US-03: Define experiment objectives and boundaries

As a data scientist, I want to describe objectives and constraints in Markdown and declare search boundaries in YAML so that agents work toward my intended outcome.

Acceptance criteria:

- The experiment brief captures data, target, task type, feature guidance, metric and direction, split constraints, algorithm mode, and budgets, including explicitly delegated decisions.
- Search-space YAML declares allowed algorithms, fixed parameters, and tunable choices or ranges; execution configuration cannot expand these boundaries.
- Resolved inputs produce a versioned plan containing the effective decisions, source references, and checksums before dependent execution.
- Ambiguous or conflicting requirements block affected runs until resolved; delegated decisions require approval before use.
- Relative input paths resolve against the experiment repository root, with the notebook working directory recorded explicitly.

Proposal references: AC-33, AC-36; §8 developer experiment inputs.

### US-05: Reject invalid configurations before execution

As a data scientist, I want invalid algorithms, parameters, and search configurations rejected before training so that compute is spent on valid candidates.

Acceptance criteria:

- Validation checks registered algorithm identifiers, task compatibility, parameter names, types, defaults, and compatible combinations.
- Categorical choices are nonempty; numeric bounds are ordered and inclusive; integer ranges yield integers; logarithmic bounds are strictly positive.
- Fixed values remain fixed, and omitted parameters use recorded registry defaults without becoming tunable.
- Invalid inputs produce actionable validation errors before training starts.
- As training entrypoints are introduced, every candidate submitted through Python, custom code, or notebooks receives the same boundary checks.

Proposal references: AC-34, AC-52; §8 algorithm configuration.

### US-09: Execute saved notebooks reproducibly

As a data scientist, I want saved notebooks executed automatically from a fresh kernel with explicit inputs so that recorded results do not depend on hidden state.

Acceptance criteria:

- Managed execution uses the selected project's locked environment, a fresh kernel, cell order, explicit parameters, and a recorded working directory.
- The run preserves the source notebook, parameters, environment identity, executed notebook with cell outputs, errors, and generated artifacts.
- Notebook-to-notebook dependencies use recorded artifact references rather than another kernel's variables.
- Cell errors, timeouts, and cancellation produce the corresponding run status; successful execution remains subject to independent validation.
- Access restrictions, approvals, and budgets apply equally to notebook and Python entrypoints; unauthorized filesystem or credential access is blocked.

Proposal references: AC-11, AC-31, AC-32, AC-42; §9 notebook contract.

### US-10: Control and inspect runs

As a data scientist, I want to submit, monitor, cancel, and inspect runs so that I can control execution and understand failures.

Acceptance criteria:

- The local runner supports submission, status inspection, cancellation, logs, and artifact retrieval through the harness interfaces.
- Runs record completion, failure, timeout, or cancellation outcomes with available diagnostic evidence.
- Runtime and experiment-count limits prevent further unauthorized work; supported resource limits are enforced.
- Unsuccessful model performance is distinguishable from execution failure when modeling is added.
- Cancelled or budget-exhausted work preserves available evidence for review.

Proposal references: AC-03, AC-08, AC-32; §9 execution.

### US-11: Extract approved source data

As a data scientist, I want approved data extracted from supported local, SQL, or object-storage sources so that I can work with existing datasets.

Acceptance criteria:

- Initial connectors support local CSV/Parquet, SQL, and object storage; acceptance demonstrations extract data from at least two source types.
- Source discovery exposes permitted schema and metadata without unrestricted data exposure.
- Extraction executes only approved queries or sampling plans within source allowlists, permissions, network restrictions, and cost/record limits.
- Each snapshot records source identity, query, parameters, extraction time, checksums, and permissions metadata.
- Extraction failures are reported without presenting incomplete output as a validated dataset.

Proposal references: AC-11, AC-15, AC-17; §6 extraction.

### US-12: Assess data quality and define splits

As a data scientist, I want data-quality assessments and an explicit split protocol so that I can identify unsuitable data before modeling.

Acceptance criteria:

- Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.
- Assessment includes distributions, class balance where relevant, anomalies, and leakage diagnostics.
- A versioned split manifest records training, validation, and protected-test partitions, respecting approved time or group constraints.
- Dataset assessment and split protocol are presented for approval before dependent feature or modeling work.

Proposal references: AC-13, AC-17; §4–6.

### US-13: Version and restore datasets

As a data scientist, I want to version and restore datasets with verified content hashes so that experiments use identifiable, recoverable inputs.

Acceptance criteria:

- DVC versions source snapshots, split manifests, and derived datasets as those artifacts are introduced.
- Git tracks DVC metadata and relevant manifests while dataset content resides in the configured cache/storage and is excluded from Git.
- A dataset can be restored from configured storage using its recorded metadata, and restored content hashes are verified.
- Missing or mismatched content prevents the dataset from being treated as successfully restored.

Proposal references: AC-16; §9 data versioning.

### US-26: Record run artifacts and provenance

As a data scientist, I want recorded runs linked to their exact inputs, code, and environment so that I can inspect and audit results.

Acceptance criteria:

- MLflow records run status, effective parameters, available metrics, outputs, and artifact references, linked to the harness run identifier.
- Each run links to the exact DVC dataset state, experiment Git revision, source snapshots including uncommitted changes, and configuration checksums.
- Provenance includes the harness repository URL, full commit SHA, package version, build identity where available, and project lockfile/environment identity.
- Source snapshots include notebooks, imported helpers, project code, configuration, and applicable runtime guidance; later slices extend these records to components, pipelines, and approvals.
- Basic execution correctness is independently checked against expected artifacts; notebook completion alone does not establish experiment acceptance.

Proposal references: AC-04, AC-05, AC-36, AC-40, AC-44.

### US-27: Reproduce a basic run in a clean environment

As a collaborating data scientist, I want to reproduce an experiment on another machine so that I can independently check its results.

Acceptance criteria:

- An experiment checkout, recorded source snapshots, lockfile, and dataset metadata restore the pinned harness commit and required inputs without a maintained harness checkout.
- Reproduction executes the recorded source, including preserved uncommitted changes, rather than assuming the Git revision alone identifies it.
- Declared output checks or tolerances determine whether the basic run reproduces successfully; metric tolerances apply when modeling is introduced.
- Missing source, dependencies, or dataset content is reported explicitly instead of silently substituted.

Proposal references: AC-09, AC-45.

## Slice 2: Build and compare reproducible features

Starting with versioned data and an approved split protocol, the developer prepares features, compares alternatives, and restores fitted preprocessing and pipeline outputs.

### US-14: Generate and compare feature pipelines

As a data scientist, I want agents to generate and compare feature pipelines on consistent splits so that feature improvements have credible evidence.

Acceptance criteria:

- Feature plans identify ordered components, effective parameters, input/output schemas, fitting scope, and modification permissions.
- The harness executes candidate transformations and records their definitions, dependencies, outputs, and lineage.
- Candidate feature sets are compared against a fixed baseline using the same approved validation protocol.
- Feature artifacts trace back to their source datasets and are independently validated before phase advancement.
- This slice supports supplied or explicitly authored candidates; agent generation is exercised when agent integration arrives in Slice 4.

Proposal references: AC-18–22; §7.

### US-15: Preserve training-only preprocessing

As a data scientist, I want preprocessing fitted only on training data and preserved for reuse so that validation and inference transformations remain consistent.

Acceptance criteria:

- Stateful preprocessing fits only on the approved training partition and applies unchanged fitted state to validation, test, and inference inputs.
- Transformations that violate split boundaries or leakage rules are rejected.
- Preparation code, fitted state, dependencies, parameters, and output schemas are preserved as artifacts.
- Restored preprocessing reproduces validation and inference transformations under declared reproducibility checks.

Proposal references: AC-20, AC-21, AC-51; §7.

### US-16: Register supplied preprocessing components

As a data scientist, I want to register my existing preprocessors without changing the harness so that I can reuse domain-specific implementations.

Acceptance criteria:

- Project configuration registers stateful preprocessors and stateless transformations from project code or pinned dependencies through versioned public interfaces.
- Declarations include identifiers, entrypoints, interface versions, parameter specifications, and modification permissions; duplicate identifiers and incompatible interfaces are rejected.
- Stateful components support fitting, transformation, and fitted-state persistence/restoration; stateless components declare their output schema.
- Registered components follow the same validation, resource, access, and lineage rules as built-in components.
- Lineage records declarations, exact code snapshots or pinned dependency identities, effective parameters, and fitted artifacts.

Proposal references: AC-51, AC-52, AC-54; §8 supplied components.

### US-27: Reproduce and reuse pipeline stages

As a data scientist, I want reproducible pipeline stages and valid output reuse so that I can avoid redundant work while preserving trustworthy results.

Acceptance criteria:

- DVC pipeline definitions record stage dependencies, parameters, and outputs, with resolved hashes preserved in `dvc.lock`.
- Stage working directories and paths are explicit and consistent with harness execution.
- Reproducing declared stages restores or generates the expected outputs under the recorded configuration.
- Reused outputs retain producer provenance and remain subject to current authorization and evaluation checks.
- Cache reuse alone does not establish experiment acceptance or bypass a gate.

Proposal references: AC-39; §9 pipelines.

## Slice 3: Train, tune, and independently evaluate models

Starting with approved features, the developer establishes baselines, compares and tunes candidates within declared limits, and obtains an independent assessment and final report.

### US-06: Choose an algorithm execution mode

As a data scientist, I want to use one algorithm, select among allowed algorithms, or compare the allowed set so that experimentation matches my question and budget.

Acceptance criteria:

- Use mode runs the specified allowed algorithm; select mode records a selection from the allowed set; compare mode evaluates every algorithm in that set within the approved plan and budgets.
- All modes respect task compatibility, parameter boundaries, and trial/runtime budgets.
- Comparing algorithms does not require exhaustive enumeration of parameter combinations.
- Suggested algorithms or expanded ranges are recorded only as recommendations for a subsequent experiment; adopting them requires a new versioned configuration and applicable approvals.

Proposal references: AC-33, AC-35.

### US-16: Register supplied models

As a data scientist, I want to register my existing model implementations without changing the harness so that I can reuse domain-specific training code.

Acceptance criteria:

- Project-local or pinned-dependency models register through the public component interface without harness modifications.
- Models support training on approved inputs, evaluator-compatible prediction, and fitted-model persistence/restoration.
- Before training, validation rejects unsupported tasks, invalid parameters, incompatible interfaces, and prediction outputs incompatible with the approved metrics.
- Supplied models can be tuned within approved boundaries and independently evaluated after restoration.
- Component declarations, code/dependency identities, effective parameters, and fitted artifacts appear in run lineage.

Proposal references: AC-50, AC-52, AC-54.

### US-18: Train across supported frameworks

As a data scientist, I want to train and evaluate scikit-learn, LightGBM, and PyTorch models so that I can compare approaches across supported frameworks.

Acceptance criteria:

- End-to-end runs cover tabular classification, tabular regression, and a basic PyTorch deep-learning example.
- A simple reproducible baseline is recorded and approved before candidate improvement comparisons.
- Framework adapters expose training, prediction, and persistence operations usable by independent evaluation.
- Each run records effective parameters, framework/library identities, metrics, model artifacts, and feature/data lineage.

Proposal references: AC-02, AC-04; §4–5.

### US-19: Manage PyTorch execution

As a data scientist, I want PyTorch runs to support CPU/GPU execution, checkpoints, and cancellation so that deep-learning experiments are manageable.

Acceptance criteria:

- Basic PyTorch training runs on CPU and supports GPU execution when the required hardware/backend is available.
- Checkpoints are captured as run artifacts and can be restored by the model implementation.
- Cancellation stops managed training and preserves available logs, checkpoints, and status.
- Resource requests, hardware metadata, runtime limits, and supported quotas are recorded and enforced where supported.

Proposal references: AC-14; §9 execution.

### US-20: Tune within declared limits

As a data scientist, I want bounded tuning with enforced trial and runtime limits so that agents cannot exceed the authorized search or budget.

Acceptance criteria:

- Candidates use only declared algorithms, fixed values, categorical choices, and numeric ranges; omitted defaults cannot be tuned.
- Candidate validation rejects boundary violations before training, including submissions from custom code and notebooks.
- Experiment-count and runtime budgets stop new work and leave a reviewable summary of completed trials.
- The optimization summary identifies the search performed, resources consumed, candidate evidence, and model proposed for final evaluation.

Proposal references: AC-08, AC-34, AC-35; §5.

### US-21: Independently assess experiment results

As a data scientist, I want independent evaluation of execution, leakage, model quality, robustness, and reproducibility so that acceptance rests on evidence.

Acceptance criteria:

- The evaluator checks successful execution and required artifacts independently of agent assertions.
- Scientific-validity checks reject split violations, improper preprocessing fitting, and leakage.
- Approved metrics and baseline comparisons are computed consistently, respecting optimization direction.
- Defined folds, slices, or stress tests assess robustness; repeated runs are checked against explicit reproducibility tolerances.
- Structured evaluation results distinguish execution failure, scientific invalidity, and insufficient model quality.

Proposal references: AC-05, AC-09, AC-13; §9 independent evaluation.

### US-24: Protect final holdout evaluation

As a data scientist, I want protected holdout evaluation reserved for the authorized final phase so that final-test results do not influence development.

Acceptance criteria:

- Experiment agents, training code, and exploratory kernels cannot access protected test data; protection is enforced independently of agent instructions.
- Only the independent evaluator accesses the holdout for the authorized final evaluation.
- Protected-test results cannot drive feature, model, or acquisition improvement loops.
- Unsuccessful final evaluation ends in rejection or review; further development requires a separately approved protocol preserving holdout protection.
- Completion requires developer approval of successful final evaluation.

Proposal references: AC-13, AC-46; §4, §9.

### US-26: Compare runs and review the final report

As a data scientist, I want run comparisons and a final report linked to their evidence so that I can judge the model against the original objective.

Acceptance criteria:

- MLflow comparisons expose effective parameters, metrics, execution status, and model artifacts for baseline and candidate runs.
- The final report identifies the model, approved metrics, baseline comparison, validity/robustness/reproducibility findings, and acceptance outcome.
- Model lineage traces through component identities, fitted feature pipelines, source datasets, exact code/configuration snapshots, and environment identity.
- Reports preserve references to independent evaluation evidence rather than treating generated narrative as proof of acceptance.

Proposal references: AC-04, AC-12, AC-22, AC-40, AC-54.

## Slice 4: Let an agent improve an experiment

An agent resolves delegated choices, generates notebooks, and improves a model using development feedback while the developer retains control of phase scope and component permissions.

### US-04: Approve delegated experiment decisions

As a data scientist, I want agents to propose delegated feature, metric, and algorithm decisions for approval so that I retain control over the experiment design.

Acceptance criteria:

- Agents resolve only explicitly delegated choices and record the proposed decisions and reasoning in the structured plan.
- The plan identifies features, metric and direction, split protocol, allowed algorithms, and budgets.
- Ambiguities and conflicts are surfaced before affected execution, and dependent work waits for approval through applicable gates.
- Original inputs, resolved decisions, and their versions/checksums remain available in run lineage.

Proposal references: AC-33, AC-36.

### US-07: Generate reviewable experiment notebooks

As a data scientist, I want agents to generate readable notebooks and project code so that I can inspect, edit, and understand their work.

Acceptance criteria:

- Generated notebooks include explanatory Markdown covering objectives, assumptions, code, results, and proposed next steps, with explicit parameter cells.
- Notebooks import generic capabilities from the installed harness and shared project logic from the experiment package without paths into a harness checkout.
- Saved notebooks support interactive use and fresh-kernel managed execution without hidden state.
- Generated notebooks, helpers, and project code stay within the experiment repository and authorized storage; the harness installation/source remain unchanged.

Proposal references: AC-42–44; §9 notebook contract.

### US-08: Explore interactively under the same controls

As a data scientist, I want to explore interactively in JupyterLab under the experiment's access rules so that exploration preserves evaluation integrity.

Acceptance criteria:

- JupyterLab launches from the project environment with the required notebook dependencies.
- Interactive kernels cannot access protected test data, including through arbitrary Python outside harness API calls.
- Training cells submit through managed APIs that enforce candidate boundaries, applicable approvals, budgets, and tracking.
- Interactive execution cannot establish acceptance; recorded results require managed execution of saved snapshots and independent evaluation.

Proposal references: AC-46, AC-49; §9 notebook contract. Isolation design remains subject to ADR-006.

### US-17: Respect immutable supplied components

As a data scientist, I want supplied code to remain immutable unless I approve changes so that agents respect ownership and component permissions.

Acceptance criteria:

- Supplied components are immutable by default; agents may configure and invoke them only within authorized boundaries.
- Attempts to modify immutable components are blocked unless recorded developer approval authorizes the change.
- Approved changes to immutable code create a new versioned experiment configuration.
- Modification permission does not expand algorithm, parameter, data-access, or evaluation boundaries; authorized code changes appear in run snapshots.

Proposal references: AC-53, AC-54; §8 supplied components.

### US-22: Improve models using development feedback

As a data scientist, I want agents to revise experiments using structured development feedback so that model improvement can proceed within approved scope.

Acceptance criteria:

- The agent receives structured evaluation feedback and produces revised notebooks or code with an evidence-based explanation.
- Revisions remain within the current approved phase, component permissions, parameter boundaries, access scope, and budgets.
- Each revision undergoes managed execution and independent evaluation, preserving its source snapshots and results.
- Iteration stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or developer cancellation.
- Phase returns and scope expansions await authorization; protected-test feedback never enters the revision loop.

Proposal references: AC-06, AC-08; §4.

### US-30: Connect the first agent with preserved runtime guidance

As a data scientist, I want an agent adapter with explicit, preserved runtime guidance so that agent behavior follows the approved experiment context.

Acceptance criteria:

- The first coding-assistant adapter supports capability discovery, structured task/result exchange, and cancellation through the common contract.
- Runtime loading explicitly selects packaged shared guidance, relevant task-specific guidance, and configured project guidance, recording ownership and order.
- Development `AGENTS.md` files from either repository are excluded from automatic runtime loading.
- The plan snapshots guidance contents, paths, versions/checksums, and load order; subsequent tasks use the preserved bundle.
- Conflicting guidance or attempts to expand experiment constraints block affected execution; adopting changed guidance requires a new versioned configuration and applicable approvals.

Proposal references: AC-37, AC-38, AC-47; §8 runtime instructions.

## Slice 5: Supervise and resume the complete workflow

The developer supervises all development phases through durable, scoped approval decisions, recovers interrupted work, and can use another agent adapter without changing experiment contracts.

### US-23: Approve phase progression and scope changes

As a data scientist, I want to approve, revise, or reject phase progression using validated evidence so that I supervise consequential decisions.

Acceptance criteria:

- Initial plan approval completes problem definition; later phase advancement is blocked until sufficient independent evidence and developer approval are recorded.
- Each decision records reviewer, scope, decision, timestamp, and associated evidence in durable project-associated state.
- Revision authorizes work only within its recorded scope; phase returns, expanded permissions, and changed evaluation criteria require authorization before execution.
- Phases can be skipped only when the approved plan identifies valid existing artifacts supporting the skip.
- Rejection or cancellation preserves results; successful final evaluation requires explicit model approval before completion.

Proposal references: AC-07; §4–5, §9 governance.

### US-25: Resume interrupted workflows

As a data scientist, I want interrupted workflows to resume from durable state without repeating completed runs so that work and approvals are preserved.

Acceptance criteria:

- Project-associated durable state preserves phase progress, run identifiers, evidence, approvals, budgets, and terminal or reviewable outcomes.
- Recovery reconciles recorded work and resumes without duplicating completed runs or bypassing pending gates.
- Resumed tasks use the preserved compatible configuration and runtime instruction bundle, even if source guidance has changed.
- Cancelled, failed, budget-exhausted, and review-required outcomes retain evidence and do not silently authorize further work.

Proposal references: AC-10, AC-38; §9 workflow states.

### US-30: Use interchangeable agent adapters

As a data scientist, I want interchangeable agent adapters so that I can change assistants without redefining the experiment workflow.

Acceptance criteria:

- Two adapters successfully execute tasks using the same versioned task/result contract.
- Capability discovery identifies which tasks each adapter supports before delegation.
- Both adapters obey the same cancellation, guidance-loading, approval, access, and budget requirements.
- Agent selection does not alter independent evaluation or the experiment's allowed boundaries.

Proposal references: AC-01; §8 agent interfaces.

### US-26: Audit workflow decisions and evidence

As a reviewer, I want run lineage connected to workflow decisions so that I can reconstruct what was authorized, executed, and accepted.

Acceptance criteria:

- Harness manifests connect runs, MLflow records, DVC state, configuration versions, runtime bundles, and approval records.
- The audit trail identifies the scope authorizing each phase, approved scope changes, and the evidence used for each decision.
- Bidirectional run references allow lookup from a harness result to its MLflow run and from the tracking record to harness provenance.
- Resumption and reuse preserve original producer provenance and the decisions authorizing subsequent use.

Proposal references: AC-04, AC-36, AC-40; §3, §9.

## Slice 6: Improve the dataset through authorized acquisition

The developer reviews evidence of data limitations, authorizes a bounded acquisition, and evaluates the effect of the resulting dataset through approved downstream work.

### US-28: Diagnose data gaps and propose acquisition

As a data scientist, I want evidence-backed data-gap diagnoses and acquisition proposals so that I can decide whether additional data is worth obtaining.

Acceptance criteria:

- Diagnosis records evidence of data deficiencies, such as underrepresented classes or slices, using approved data and development evaluation results.
- A structured proposal records its reason, evidence, acquisition hypothesis, source, strategy, expected benefit, costs, limits, and required authorization.
- Expected benefit is presented as a hypothesis rather than a guaranteed improvement.
- Proposals do not use protected final-test feedback or expand access, evaluation protocols, or budgets without approval.

Proposal references: AC-23, AC-24; §6.

### US-29: Acquire data and measure its effect within approved limits

As a data scientist, I want authorized acquisition to enforce limits, version new data, compare outcomes, and stop at defined conditions so that data improvement remains controlled.

Acceptance criteria:

- Acquisition is blocked without recorded authorization covering source, strategy, scope, and limits; approved in-scope activity need not request permission for every operation.
- Execution enforces source permissions and cost, record, runtime, and compute budgets, preserving evidence when a limit is reached.
- Acquired data is validated and versioned with source lineage; synthetic or augmented data is explicitly identified as distinct from observed data.
- Returning to validation/EDA and downstream development requires the applicable phase authorization, with complete audit records.
- Before-and-after model comparisons use consistent approved evaluation protocols and link results to the corresponding dataset versions.
- The acquisition loop stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or cancellation, preserving a reviewable outcome.
- Resumption after acquisition retains approvals, budget usage, dataset lineage, and completed-run identities; advanced acquisition strategies remain deferred according to the proposal's implementation plan.

Proposal references: AC-25–30; §4, §6.
