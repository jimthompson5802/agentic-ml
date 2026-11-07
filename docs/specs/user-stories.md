# User stories and delivery scope

Planning terminology follows the [README](../../README.md#planning-terminology).

**Scope revision:** MVP-SC-01 and MVP-SC-02 were approved at Gate 1 on 2026-11-06
by “i approve gate 1 and authorize phase 2”. Gate 2 was approved by
“I approve gate 2 and authorize phase 3”. Required behavior below does not imply
new delivered capabilities.
[Original dispositions](../reviews/mvp-scope-criterion-dispositions.md) preserve
every original criterion, old milestone and displaced guarantee.

**Publication:** design 0.15 and these stories were published through
[PR #57](https://github.com/jimthompson5802/agentic-ml/pull/57); Phase 4 synchronized
the issue scope and created the integration issues below. Final documentation/
backlog handoff review is separate from product implementation or acceptance.
Accepted APIs and historical evidence retain their original contracts.

## Delivery milestones

| Milestone | User-visible outcome | Stories / slices |
|---|---|---|
| **0. Establish the toolkit development foundation** | Accepted package, contributor checks and CI. | US-31–33; unchanged |
| **1. Complete one experiment** | One local classification experiment: extraction, quality/splits, features, baseline, bounded tuning, final evaluation, MLflow records and native DVC stages; scientist-directed assistant demonstration. | Accepted US-01/02/03/05; M1 slices of US-10–15/18/20/21/24/26/27; US-39 AC-01–08 |
| **2. Validate usability and reproduction** | Regression, custom components, saved notebooks, fitted-state restoration and clean committed-project reproduction with DVC cache/invalidation and assistant evidence. **MVP ends here.** | US-09/16; M2 slices of US-13/15/18/21/27/39; US-40 |
| **Uncommitted roadmap** | Deferred platform capabilities without dates or delivery order; historical M3–6 are migration context. | Deferred criteria and displaced clauses below |
| **50. Improve the technical environment** | Preserve accepted tooling and supporting backlog. | US-35–38; unchanged |
| **99. Future enhancements** | Existing deferred contribution/review story. | US-34; unchanged |

## MVP contracts and history

- Trusted local code, CPU scikit-learn, CSV/Parquet and project functions. MLflow
  owns records/artifacts; DVC owns data versions, stage execution and cache.
- Training-only preprocessing, recorded disjoint splits, consistent metrics and
  separate final testing remain required. Seeded random splits or supplied time/
  group-aware partitions are supported; no OS-protected holdout or universal
  leakage assurance.
- Scientists own external assistant sessions. Assistants edit project code and
  invoke public toolkit interfaces/DVC, inspect results and make directed
  validation-based revisions. Managed delegation/autonomous loops are deferred.
- The basic path requires explicit valid settings and a trial cap, not mandatory
  experiment approvals. Existing strict planning/approval APIs stay available.
  Their historical acceptance is not proof that simpler execution exists yet.
- Reproduction uses committed code/configuration, lockfiles, seeds and DVC data;
  automatic arbitrary dirty/untracked-source replay is deferred.
- Developer gates, public test-boundary review, TDD and verification requirements
  remain. Do not weaken tests, erase historical evidence, or close outstanding
  M1/M50 obligations through renumbering.
- IDs are stable and unique across slices. Every original ID remains once;
  reworded outcomes retain IDs and displaced clauses remain in the approved
  matrix. Entirely deferred criteria retain original wording. New US-39/40
  criteria have no implementation evidence.
- Component stories own behavior tests; integration stories own interoperability
  and assistant usability. Repeated story numbers denote distinct slices.

<a id="milestone-0-establish-the-harness-development-foundation"></a>

## Milestone 0: Establish the toolkit development foundation

Contributors set up this repository for toolkit development, run the CLI from the local source checkout, and verify changes using documented checks. Automated CI checks verify changes, and clean-environment package checks verify distributable artifacts. This milestone establishes the development foundation for the experiment-user capabilities introduced in Milestone 1.

See the design's [Milestone 0 dependencies and delivery order](design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order) for capability dependencies between these stories and recommended implementation sequencing.

<a id="us-31-set-up-the-harness-development-environment"></a>

### US-31: Set up the toolkit development environment

As a contributor, I want documented steps to set up this repository for local development so that I can make changes and verify them consistently.

Acceptance criteria:

- <a id="us-31-ac-01"></a> **US-31-AC-01:** Documented prerequisites specify Python 3.12 or newer and required tools, and identify the Python versions verified by CI. macOS is the initial verified development platform; Linux and Windows remain eligible for future verification, and platform-specific requirements and known limitations are documented.
- <a id="us-31-ac-02"></a> **US-31-AC-02:** Instructions cover cloning the toolkit repository and installing runtime and development dependencies using `uv` and the committed lockfile.
- <a id="us-31-ac-03"></a> **US-31-AC-03:** Contributors can run the toolkit CLI from the local source checkout.
- <a id="us-31-ac-04"></a> **US-31-AC-04:** Documented commands run automated tests, linting, formatting checks, and type checks.
- <a id="us-31-ac-05"></a> **US-31-AC-05:** A documented smoke check confirms that the environment is ready for development.
- <a id="us-31-ac-06"></a> **US-31-AC-06:** Setup identifies required configuration and credentials and provides local defaults where practical.
- <a id="us-31-ac-07"></a> **US-31-AC-07:** Setup instructions are verified on macOS from a fresh checkout and a new development environment using only the documented prerequisites and setup steps. Verification runs all documented development checks, including `agentic-ml --version`, and records the operating system and Python/tool versions, commands run, and results as review evidence.
- <a id="us-31-ac-08"></a> **US-31-AC-08:** The repository includes configuration for automated tests, linting, formatting, and type checking. Tool versions are controlled through the development dependencies and committed lockfile, and the documented local commands use these configurations.
- <a id="us-31-ac-09"></a> **US-31-AC-09:** Documented Python coding conventions cover naming, typing, docstrings, imports, and error handling. Automated checks enforce the conventions that the selected tools can verify.
- <a id="us-31-ac-10"></a> **US-31-AC-10:** Documented guidance defines when and how contributors may add rule suppressions and check exclusions, requiring a recorded justification for each exception so that it can be reviewed.

### US-32: Verify changes automatically in CI

As a contributor, I want automated checks on every pull request so that I receive consistent feedback before changes are merged.

Acceptance criteria:

- <a id="us-32-ac-01"></a> **US-32-AC-01:** CI runs on pull requests and updates to the default branch from a clean checkout, using Linux as the initial CI verification platform.
- <a id="us-32-ac-02"></a> **US-32-AC-02:** CI verifies Python 3.12 as the minimum supported version, documents any additional Python versions tested, installs the required tools, and synchronizes runtime and development dependencies using `uv` and the committed lockfile without modifying the lockfile.
- <a id="us-32-ac-03"></a> **US-32-AC-03:** CI runs automated tests, linting, formatting checks, type checks, and the development smoke check using the same documented commands available locally under US-31.
- <a id="us-32-ac-04"></a> **US-32-AC-04:** Failed checks produce a failing CI result, and contributors can inspect check results and diagnostic logs from the pull request.

<a id="us-33-build-and-verify-the-harness-package"></a>

### US-33: Build and verify the toolkit package

As a contributor, I want to build and verify distributable packages with a minimal CLI that reports its version so that I can confirm the toolkit installs and runs outside the source checkout.

Acceptance criteria:

- <a id="us-33-ac-01"></a> **US-33-AC-01:** A documented command builds both wheel and source distributions from the repository.
- <a id="us-33-ac-02"></a> **US-33-AC-02:** Verification installs the built wheel and its declared runtime dependencies in a clean environment and runs outside the source checkout without relying on an editable installation or development dependencies.
- <a id="us-33-ac-03"></a> **US-33-AC-03:** Installed-package checks verify the `agentic-ml` CLI, `agentic_ml` imports, and access to at least one minimal packaged template and one minimal runtime guidance file. Both files have explicitly provisional contents for Milestone 0; checks read them through the installed package and compare their contents with expected values. Usable experiment initialization resources are delivered in Milestone 1.
- <a id="us-33-ac-04"></a> **US-33-AC-04:** Verification builds a wheel from the source distribution and confirms that it passes the same installed-package checks.
- <a id="us-33-ac-05"></a> **US-33-AC-05:** CI runs package build and verification checks and reports failures with diagnostic logs; the commands are documented for local reproduction.
- <a id="us-33-ac-06"></a> **US-33-AC-06:** The Milestone 0 CLI provides `agentic-ml --version`, which prints the installed package version and exits successfully. The reported version matches the installed distribution metadata. Experiment commands are introduced in later milestones.
- <a id="us-33-ac-07"></a> **US-33-AC-07:** The installed-package checks run `agentic-ml --version` for both the directly built wheel and the wheel rebuilt from the source distribution, verifying successful exit and the expected version. The documented source-checkout smoke check also runs `agentic-ml --version`.

## Milestone 1: Complete one experiment

M1 exits when a separate installed project completes classification and ASW-01–06, with MLflow artifacts and a native DVC pipeline. Correctly recorded experiments may show no gain over baseline.

### US-01: Install a pinned toolkit version

As a developer, I want to install a pinned toolkit version into my own experiment repository so that my project has a reproducible environment.

**Existing accepted slice:** preserve its original contract/evidence. Default-path and future training integration work is separate.

Acceptance criteria:

- <a id="us-01-ac-01"></a> **US-01-AC-01:** Documented bootstrap instructions cover installing `uv` and Git, creating the user Git/Python project, and installing the toolkit from GitHub at a full commit SHA.
- <a id="us-01-ac-02"></a> **US-01-AC-02:** The toolkit is a normal installed dependency; runtime use requires no manually maintained toolkit checkout or installer cache.
- <a id="us-01-ac-03"></a> **US-01-AC-03:** The project lockfile records the resolved toolkit revision and dependencies; the installed package exposes `agentic-ml`, `agentic_ml`, templates, and runtime guidance.
- <a id="us-01-ac-04"></a> **US-01-AC-04:** An explicit toolkit upgrade changes the commit pin and lockfile, producing a new environment identity.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-02: Initialize an experiment project

As a developer, I want to initialize configuration, notebooks, dependencies, and local storage while preserving existing files so that I can start experimenting safely.

**Existing accepted slice:** preserve its original contract/evidence. Default-path and future training integration work is separate.

Acceptance criteria:

- <a id="us-02-ac-01"></a> **US-02-AC-01:** `uv run agentic-ml init` adds project configuration, ignore rules, an initial experiment brief, search-space and execution configuration, notebook templates, and required project-package scaffolding.
- <a id="us-02-ac-02"></a> **US-02-AC-02:** Initialization preserves existing files and the pinned toolkit dependency, reporting conflicts instead of silently overwriting files.
- <a id="us-02-ac-03"></a> **US-02-AC-03:** Required ML and notebook execution dependencies are declared and synchronized with the project environment and lockfile.
- <a id="us-02-ac-04"></a> **US-02-AC-04:** Project-associated DVC, MLflow, and durable-state storage are initialized with local defaults and configurable locations.
- <a id="us-02-ac-05"></a> **US-02-AC-05:** Data access, agent authentication, and approval presentation remain explicit setup choices; initialization grants no execution or data-access authorization, and credentials remain outside committed configuration.

US-39-AC-01 owns runnable defaults/draft-schema compatibility. Accepted initialization supplies drafts, not an implemented experiment runner.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-03: Define experiment objectives and boundaries

As a data scientist, I want to describe objectives and constraints in Markdown and declare search boundaries in YAML so that agents work toward my intended outcome.

**Existing accepted slice:** preserve its original contract/evidence. Default-path and future training integration work is separate.

Acceptance criteria:

- <a id="us-03-ac-01"></a> **US-03-AC-01:** The experiment brief captures data, target, task type, feature guidance, metric and direction, split constraints, algorithm mode, and budgets, including explicitly delegated decisions.
- <a id="us-03-ac-02"></a> **US-03-AC-02:** Search-space YAML declares allowed algorithms, fixed parameters, and tunable choices or ranges; execution configuration cannot expand these boundaries.
- <a id="us-03-ac-03"></a> **US-03-AC-03:** Resolved inputs produce a versioned plan containing the effective decisions, source references, and checksums before dependent execution.
- <a id="us-03-ac-04"></a> **US-03-AC-04:** Ambiguous or conflicting requirements block affected runs until resolved; delegated decisions require approval before use.
- <a id="us-03-ac-05"></a> **US-03-AC-05:** Relative input paths resolve against the experiment repository root, with the notebook working directory recorded explicitly.

Strict explicit APIs retain readiness rules and unauthenticated-record limitations under [US-03-SC-01](../plans/milestone-1-us-03.md#us-03-sc-01--unauthenticated-experiment-approvals-2026-10-31). US-39-AC-01/02 own the simpler basic workflow; accepted contracts are not silently changed.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-05: Reject invalid configurations before execution

As a data scientist, I want invalid algorithms, parameters, and search configurations rejected before training so that compute is spent on valid candidates.

**Existing accepted slice:** preserve its original contract/evidence. Default-path and future training integration work is separate.

Acceptance criteria:

- <a id="us-05-ac-01"></a> **US-05-AC-01:** Validation checks registered algorithm identifiers, task compatibility, parameter names, types, defaults, and compatible combinations.
- <a id="us-05-ac-02"></a> **US-05-AC-02:** Categorical choices are nonempty; numeric bounds are ordered and inclusive; integer ranges yield integers; logarithmic bounds are strictly positive.
- <a id="us-05-ac-03"></a> **US-05-AC-03:** Fixed values remain fixed, and omitted parameters use recorded registry defaults without becoming tunable.
- <a id="us-05-ac-04"></a> **US-05-AC-04:** Invalid inputs produce actionable validation errors before training starts.
- <a id="us-05-ac-05"></a> **US-05-AC-05:** As training entrypoints are introduced, every candidate submitted through Python, custom code, or notebooks receives the same boundary checks.

Accepted validation metadata does not establish training support. AC-05 future training/custom/notebook integrations remain open; supported-call validation does not constrain arbitrary external Python.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-10: Run and inspect local experiments

As a data scientist, I want to run local experiments and inspect logs, status and artifacts so that I can diagnose execution failures.

Acceptance criteria:

- <a id="us-10-ac-01"></a> **US-10-AC-01:** Run a local experiment and expose logs, final result status and artifact locations.
- <a id="us-10-ac-02"></a> **US-10-AC-02:** Record completion or failure with available diagnostics.
- <a id="us-10-ac-03"></a> **US-10-AC-03:** Limit search to configured maximum candidate trials through the supported runner/search path.
- <a id="us-10-ac-04"></a> **US-10-AC-04:** Unsuccessful model performance is distinguishable from execution failure when modeling is added.
- <a id="us-10-ac-05"></a> **US-10-AC-05:** Preserve available completed-trial results and failure/interruption evidence when execution can finalize.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-11: Extract local experiment data

As a data scientist, I want to prepare local CSV/Parquet files using selection, filtering and joins so that I can start with traceable data.

Acceptance criteria:

- <a id="us-11-ac-01"></a> **US-11-AC-01:** Read local CSV/Parquet and support configured column selection, filtering and joins; permit project-owned extraction functions.
- <a id="us-11-ac-02"></a> **US-11-AC-02:** Report local source schemas and metadata needed for extraction.
- <a id="us-11-ac-03"></a> **US-11-AC-03:** Execute explicitly configured local extraction operations and report their configuration.
- <a id="us-11-ac-04"></a> **US-11-AC-04:** Record source paths/content identities, extraction settings and time, and output checksum/DVC reference.
- <a id="us-11-ac-05"></a> **US-11-AC-05:** Extraction failures are reported without presenting incomplete output as a validated dataset.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-12: Validate data and define reproducible splits

As a data scientist, I want to check data quality and record distinct partitions so that training and evaluation use suitable inputs.

Acceptance criteria:

- <a id="us-12-ac-01"></a> **US-12-AC-01:** Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.
- <a id="us-12-ac-05"></a> **US-12-AC-05:** Report validation results and block supported pipeline steps when configured required checks fail.
- <a id="us-12-ac-02"></a> **US-12-AC-02:** Provide basic distributions, missingness and classification target balance.
- <a id="us-12-ac-03"></a> **US-12-AC-03:** Record seeded train/validation/test partitions; accept explicit user-supplied partitions for time/group problems and check row membership/disjointness.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-13: Version and restore datasets with DVC

As a data scientist, I want to track and restore datasets with native DVC so that experiment inputs can be identified and reproduced.

Acceptance criteria:

- <a id="us-13-ac-01"></a> **US-13-AC-01:** DVC versions source snapshots, split manifests, and derived datasets as those artifacts are introduced.
- <a id="us-13-ac-02"></a> **US-13-AC-02:** Git tracks DVC metadata and relevant manifests while dataset content resides in the configured cache/storage and is excluded from Git.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-14: Build and compare authored feature pipelines

As a data scientist, I want to execute authored feature pipelines and compare validation results so that feature changes have measurable evidence.

Acceptance criteria:

- <a id="us-14-ac-01"></a> **US-14-AC-01:** Describe authored scikit-learn pipeline steps, parameters, selected columns and training-only fit scope.
- <a id="us-14-ac-02"></a> **US-14-AC-02:** Execute authored transformations and record pipeline settings, dependencies, output references and source-data identity.
- <a id="us-14-ac-03"></a> **US-14-AC-03:** Compare authored feature variants using the same split, estimator/settings and metric; report direction-aware gains/ties/regressions.
- <a id="us-14-ac-04"></a> **US-14-AC-04:** Link feature/pipeline artifacts to source datasets and verify expected outputs through supported paths.
- <a id="us-14-ac-05"></a> **US-14-AC-05:** Use explicitly authored or supplied feature candidates.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-15: Preserve training-only preprocessing

As a data scientist, I want to fit preprocessing on training rows and preserve fitted state so that validation and inference use consistent transformations.

Acceptance criteria:

- <a id="us-15-ac-01"></a> **US-15-AC-01:** Fit preprocessing only on training rows and reuse fitted state for validation/test/inference.
- <a id="us-15-ac-02"></a> **US-15-AC-02:** Reject supported-path partition overlap and improper fit scope; test for train-only fitting with independently defined expectations.
- <a id="us-15-ac-03"></a> **US-15-AC-03:** Preserve fitted pipeline, feature settings and declared schema plus committed code/dependency references.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-18: Train scikit-learn models

As a data scientist, I want to train CPU tabular classification and regression models so that I can compare baselines and candidates.

Acceptance criteria:

- <a id="us-18-ac-01"></a> **US-18-AC-01:** Deliver classification in M1 and regression in M2 using scikit-learn on CPU.
- <a id="us-18-ac-02"></a> **US-18-AC-02:** Train and record a reproducible baseline before comparing candidates.
- <a id="us-18-ac-03"></a> **US-18-AC-03:** Use native compatible estimator/pipeline fit, predict and persistence operations.
- <a id="us-18-ac-04"></a> **US-18-AC-04:** Each run records effective parameters, framework/library identities, metrics, model artifacts, and feature/data lineage.

AC-01 spans M1 classification and M2 regression; M1 alone does not complete it. Other ML frameworks are deferred.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-20: Tune within declared search limits

As a data scientist, I want to run validated searches with a maximum trial count so that tuning stays within declared parameter and trial boundaries.

Acceptance criteria:

- <a id="us-20-ac-01"></a> **US-20-AC-01:** Candidates use only declared algorithms, fixed values, categorical choices, and numeric ranges; omitted defaults cannot be tuned.
- <a id="us-20-ac-02"></a> **US-20-AC-02:** Validate candidates before training through supported toolkit/script/notebook execution paths.
- <a id="us-20-ac-03"></a> **US-20-AC-03:** Enforce a configured maximum trial count and preserve completed trial results.
- <a id="us-20-ac-04"></a> **US-20-AC-04:** Summarize candidates, validation scores, best selection, trial count and elapsed time.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-21: Evaluate experiment outputs consistently

As a data scientist, I want to compute consistent metrics and supported split/fitting checks so that I can assess results against a baseline.

Acceptance criteria:

- <a id="us-21-ac-01"></a> **US-21-AC-01:** Compute/check status and expected outputs from execution evidence, rather than narrative claims.
- <a id="us-21-ac-02"></a> **US-21-AC-02:** Check supported split disjointness and train-only preprocessing fitting.
- <a id="us-21-ac-03"></a> **US-21-AC-03:** Compute configured metrics consistently and compare against baseline with explicit direction.
- <a id="us-21-ac-05"></a> **US-21-AC-05:** Report execution failure, configured validation failure and insufficient quality distinctly.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-24: Evaluate a selected model on a separate test partition

As a data scientist, I want to run final testing after validation-based model selection so that test scores do not drive the supported tuning workflow.

Acceptance criteria:

- <a id="us-24-ac-02"></a> **US-24-AC-02:** Evaluate the selected fitted pipeline on a separate test partition after validation-based selection.
- <a id="us-24-ac-03"></a> **US-24-AC-03:** Keep test scores out of the supported tuning/feature-selection path; document no retuning on final scores.
- <a id="us-24-ac-04"></a> **US-24-AC-04:** Report unsuccessful final evaluation as a result rather than silently resume tuning.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-26: Record and compare experiment results

As a data scientist, I want to link MLflow results to code, configuration and DVC data so that I can inspect and compare recorded experiments.

Acceptance criteria:

- <a id="us-26-ac-01"></a> **US-26-AC-01:** Record MLflow run status, parameters, metrics, outputs and artifact locations with a stable run reference.
- <a id="us-26-ac-02"></a> **US-26-AC-02:** Link MLflow results to DVC data identity, committed experiment revision and effective configuration.
- <a id="us-26-ac-03"></a> **US-26-AC-03:** Provenance includes the toolkit repository URL, full commit SHA, package version, build identity where available, and project lockfile/environment identity.
- <a id="us-26-ac-04"></a> **US-26-AC-04:** Record committed entrypoint/project code/configuration references and save the executed notebook when used.
- <a id="us-26-ac-05"></a> **US-26-AC-05:** Check expected output presence and report failures separately from successful process exit.
- <a id="us-26-ac-06"></a> **US-26-AC-06:** MLflow comparisons expose effective parameters, metrics, execution status, and model artifacts for baseline and candidate runs.
- <a id="us-26-ac-07"></a> **US-26-AC-07:** Produce a concise result summary with model, configured metrics, baseline comparison and validation outcomes.
- <a id="us-26-ac-08"></a> **US-26-AC-08:** Link model/pipeline artifacts to DVC data, committed code/configuration and locked environment references.
- <a id="us-26-ac-09"></a> **US-26-AC-09:** Link report claims to recorded numerical evaluation results/artifacts.
- <a id="us-26-ac-12"></a> **US-26-AC-12:** Allow results to locate their MLflow run and MLflow metadata to locate committed project/config/data references.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-27: Run and reproduce native DVC pipelines

As a data scientist, I want to run native DVC stages from committed experiment inputs so that I can reproduce results and reuse valid outputs.

Acceptance criteria:

- <a id="us-27-ac-05"></a> **US-27-AC-05:** DVC pipeline definitions record stage dependencies, parameters, and outputs, with resolved hashes preserved in `dvc.lock`.
- <a id="us-27-ac-06"></a> **US-27-AC-06:** Stage working directories and paths are explicit and consistent with toolkit execution.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-39: Complete an assistant-supported tabular experiment

Owning issue: [#58](https://github.com/jimthompson5802/agentic-ml/issues/58).

As a data scientist, I want a coding assistant to help prepare, run, inspect and revise an experiment through installed public interfaces so that I can reach recorded results quickly.

**New integration story; not implemented.** Component stories retain technical ownership. This slice owns ASW-01–06.

Acceptance criteria:

- <a id="us-39-ac-01"></a> **US-39-AC-01:** Starting from a separate experiment project, documented initialization and pinned installation provide a runnable local classification example without a neighboring toolkit checkout, manual draft-schema migration, managed agent adapter or toolkit source edits.
- <a id="us-39-ac-02"></a> **US-39-AC-02:** The basic experiment path accepts explicit objectives, data, metric and search settings, validates them before training and does not require formal plan resolution or delegated-decision approvals. Existing explicit planning, approval and validation APIs retain their documented strict behavior.
- <a id="us-39-ac-03"></a> **US-39-AC-03:** A scientist-directed external coding-assistant session prepares project configuration and extraction/preprocessing code, invokes installed public toolkit interfaces and native DVC stages, and locates MLflow results without private toolkit imports.
- <a id="us-39-ac-04"></a> **US-39-AC-04:** The classification walkthrough completes extraction, quality/split checks, training-only preprocessing, baseline training and bounded tuning, then exposes MLflow parameters, validation metrics and fitted artifacts linked to DVC inputs and committed configuration/code references.
- <a id="us-39-ac-05"></a> **US-39-AC-05:** Before final testing, the scientist directs at least one assistant-authored feature or parameter revision using validation evidence; a recorded rerun compares the change using consistent splits and metric. Gains, ties and regressions are valid outcomes; final-test feedback is not used for the revision.
- <a id="us-39-ac-06"></a> **US-39-AC-06:** After selection, the walkthrough executes the separate final-test step, saves the selected fitted pipeline/model and metrics, and reports the result without silently retuning from final-test scores. Quality shortfalls and execution failures are distinguishable.
- <a id="us-39-ac-07"></a> **US-39-AC-07:** Walkthrough evidence identifies at least one external assistant product, interface and version, scientist prompts, consequential edits/actions, commands/outcomes and independently checked MLflow/DVC references. A complete transcript and multiple assistant products are not required.
- <a id="us-39-ac-08"></a> **US-39-AC-08:** Installed-project checks demonstrate invalid configuration or candidate parameters and missing required local inputs fail clearly with available diagnostics, rather than being reported as a completed successful experiment.

Dependencies: component criteria in this milestone and the [assistant walkthrough](../reviews/mvp-scope-criterion-dispositions.md#assistant-supported-walkthrough). Check artifacts/metrics independently of assistant statements. No managed adapter or multiple-product claim.

## Milestone 2: Validate usability and reproduction

M2 exits when regression, customization, fresh-kernel notebook execution and committed-project reproduction pass declared checks, including ASW-07–08. Deferred platform guarantees are not implied.

### US-09: Execute saved notebooks

As a data scientist, I want to run saved notebooks from a fresh kernel with explicit inputs so that recorded results do not depend on hidden state.

Acceptance criteria:

- <a id="us-09-ac-01"></a> **US-09-AC-01:** Execute saved notebooks in the project locked environment from a fresh kernel, in cell order, with explicit inputs and working directory.
- <a id="us-09-ac-02"></a> **US-09-AC-02:** The run preserves the source notebook, parameters, environment identity, executed notebook with cell outputs, errors, and generated artifacts.
- <a id="us-09-ac-03"></a> **US-09-AC-03:** Notebook-to-notebook dependencies use recorded artifact references rather than another kernel's variables.
- <a id="us-09-ac-04"></a> **US-09-AC-04:** Record execution success or cell failure and retain available diagnostics; check expected outputs.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-13: Version and restore datasets with DVC

As a data scientist, I want to track and restore datasets with native DVC so that experiment inputs can be identified and reproduced.

Acceptance criteria:

- <a id="us-13-ac-03"></a> **US-13-AC-03:** A dataset can be restored from configured storage using its recorded metadata, and restored content hashes are verified.
- <a id="us-13-ac-04"></a> **US-13-AC-04:** Missing or mismatched content prevents the dataset from being treated as successfully restored.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-15: Preserve training-only preprocessing

As a data scientist, I want to fit preprocessing on training rows and preserve fitted state so that validation and inference use consistent transformations.

Acceptance criteria:

- <a id="us-15-ac-04"></a> **US-15-AC-04:** Restored preprocessing reproduces validation and inference transformations under declared reproducibility checks.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-16: Use compatible project components

As a data scientist, I want to use compatible project-owned transformers and estimators so that I can customize experiments without changing the toolkit.

Acceptance criteria:

- <a id="us-16-ac-01"></a> **US-16-AC-01:** Accept compatible project-owned scikit-learn transformers/functions and pinned dependencies.
- <a id="us-16-ac-02"></a> **US-16-AC-02:** Check supplied objects/functions satisfy the supported scikit-learn interface and parameter contract.
- <a id="us-16-ac-03"></a> **US-16-AC-03:** Fit/transform and persist/restore compatible supplied pipelines; verify resulting feature shape/schema.
- <a id="us-16-ac-04"></a> **US-16-AC-04:** Apply supported-path validation, train-only fitting and result tracking to supplied components.
- <a id="us-16-ac-05"></a> **US-16-AC-05:** Record committed component/dependency identity, effective parameters and fitted artifacts.
- <a id="us-16-ac-06"></a> **US-16-AC-06:** Use project-owned compatible estimators without modifying the toolkit.
- <a id="us-16-ac-07"></a> **US-16-AC-07:** Fit supplied estimators, predict and preserve/restore fitted pipelines.
- <a id="us-16-ac-08"></a> **US-16-AC-08:** Reject unsupported tasks, invalid parameters and incompatible estimator/prediction outputs through supported paths.
- <a id="us-16-ac-09"></a> **US-16-AC-09:** Tune compatible supplied estimators within configured search bounds and evaluate restored predictions.
- <a id="us-16-ac-10"></a> **US-16-AC-10:** Record code/dependency references, effective parameters and fitted artifacts.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-21: Evaluate experiment outputs consistently

As a data scientist, I want to compute consistent metrics and supported split/fitting checks so that I can assess results against a baseline.

Acceptance criteria:

- <a id="us-21-ac-04"></a> **US-21-AC-04:** Reproduce example outputs/metrics under declared tolerances.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-27: Run and reproduce native DVC pipelines

As a data scientist, I want to run native DVC stages from committed experiment inputs so that I can reproduce results and reuse valid outputs.

Acceptance criteria:

- <a id="us-27-ac-01"></a> **US-27-AC-01:** Restore pinned toolkit/project dependencies and required DVC data from committed experiment configuration/lockfiles.
- <a id="us-27-ac-02"></a> **US-27-AC-02:** Execute the recorded committed code/configuration, failing if required inputs are unavailable.
- <a id="us-27-ac-03"></a> **US-27-AC-03:** Declared output checks or tolerances determine whether the basic run reproduces successfully; metric tolerances apply when modeling is introduced.
- <a id="us-27-ac-04"></a> **US-27-AC-04:** Missing source, dependencies, or dataset content is reported explicitly instead of silently substituted.
- <a id="us-27-ac-07"></a> **US-27-AC-07:** Reproducing declared stages restores or generates the expected outputs under the recorded configuration.
- <a id="us-27-ac-08"></a> **US-27-AC-08:** Use native DVC dependency hashes for reuse and retain traceable run/data/code references; re-evaluate outputs where required.
- <a id="us-27-ac-09"></a> **US-27-AC-09:** Treat cached output as reusable data, not proof that metrics/checks pass.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-39: Complete an assistant-supported tabular experiment

Owning issue: [#58](https://github.com/jimthompson5802/agentic-ml/issues/58).

As a data scientist, I want a coding assistant to help prepare, run, inspect and revise an experiment through installed public interfaces so that I can reach recorded results quickly.

**New integration story; not implemented.** Component stories retain technical ownership. This slice extends ASW-08; US-40 owns ASW-07.

Acceptance criteria:

- <a id="us-39-ac-09"></a> **US-39-AC-09:** A tabular regression example completes the same installed-project workflow and records its baseline, candidate and final evaluation results in MLflow with DVC/code/configuration references.
- <a id="us-39-ac-10"></a> **US-39-AC-10:** A customization example uses compatible project-owned preprocessing and estimator code through supported scikit-learn interfaces, preserves/restores fitted artifacts and records results without toolkit modification or a general component registry.
- <a id="us-39-ac-11"></a> **US-39-AC-11:** The scientist-directed assistant walkthrough includes a saved notebook example executed in the project environment from a fresh kernel, with explicit paths/inputs, preserved outputs/errors and recorded artifact references instead of hidden cross-kernel state.

Dependencies: component criteria in this milestone and the [assistant walkthrough](../reviews/mvp-scope-criterion-dispositions.md#assistant-supported-walkthrough). Check artifacts/metrics independently of assistant statements. No managed adapter or multiple-product claim.

### US-40: Reproduce an experiment through DVC with assistant support

Owning issue: [#59](https://github.com/jimthompson5802/agentic-ml/issues/59).

As a data scientist, I want to reproduce committed experiments through DVC with coding-assistant help so that I can verify results and avoid unnecessary recomputation.

**New integration story; not implemented.** US-13/15/16/21/27 retain component ownership; this story owns cross-component reproduction and ASW-07.

Acceptance criteria:

- <a id="us-40-ac-01"></a> **US-40-AC-01:** A fresh checkout of committed experiment code/configuration, pinned toolkit dependencies and available DVC data can restore required inputs and execute declared stages outside the toolkit checkout using documented commands.
- <a id="us-40-ac-02"></a> **US-40-AC-02:** An unchanged pipeline demonstrates native DVC output reuse without retraining unchanged stages; evidence distinguishes cached reuse from newly executed training and retains traceable result/data/code references.
- <a id="us-40-ac-03"></a> **US-40-AC-03:** Changing a declared data, code or parameter dependency invalidates the affected native DVC stages; the demonstration records which stages rerun and verifies their regenerated outputs.
- <a id="us-40-ac-04"></a> **US-40-AC-04:** Missing required source, dependencies or DVC content, and corrupted or mismatched required data, produce explicit restoration/reproduction failures without silently substituting current or alternate inputs.
- <a id="us-40-ac-05"></a> **US-40-AC-05:** Actual reproduced execution records MLflow results and committed code/configuration, environment and DVC identities, with references to the compared experiment. Cache reuse alone is not recorded as newly executed training or proof of passing evaluation.
- <a id="us-40-ac-06"></a> **US-40-AC-06:** The data scientist directs an external coding assistant through documented DVC restoration/reproduction and result inspection; evidence records assistant product/interface/version, prompts, commands/outcomes and verified run/data references without requiring a managed adapter.
- <a id="us-40-ac-07"></a> **US-40-AC-07:** Declared output checks and metric tolerances determine reproduction success; the demonstration includes restored fitted preprocessing/model predictions as applicable and reports mismatches rather than claiming successful reproduction.

Dependencies: US-39 M1 artifacts; US-13 restoration; US-27 stages/reproduction; US-15 fitted-state restoration and US-21 output/tolerance checks. Declare concrete checks/tolerances in later implementation plans before execution.

## Uncommitted roadmap

Deferred requirements below are not active M3–6 delivery promises or new M99 scope. Entirely deferred criteria retain original wording. Stronger displaced clauses of retained criteria remain in the [original disposition matrix](../reviews/mvp-scope-criterion-dispositions.md#criterion-level-disposition-matrix), including isolation, approvals, hard quotas, full source capture and component-framework guarantees.

### US-04: Approve delegated experiment decisions

As a data scientist, I want agents to propose delegated feature, metric, and algorithm decisions for approval so that I retain control over the experiment design.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-04-ac-01"></a> **US-04-AC-01:** Agents resolve only explicitly delegated choices and record the proposed decisions and reasoning in the structured plan.
- <a id="us-04-ac-02"></a> **US-04-AC-02:** The plan identifies features, metric and direction, split protocol, allowed algorithms, and budgets.
- <a id="us-04-ac-03"></a> **US-04-AC-03:** Ambiguities and conflicts are surfaced before affected execution, and dependent work waits for approval through applicable gates.
- <a id="us-04-ac-04"></a> **US-04-AC-04:** Original inputs, resolved decisions, and their versions/checksums remain available in run lineage.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-06: Choose an algorithm execution mode

As a data scientist, I want to use one algorithm, select among allowed algorithms, or compare the allowed set so that experimentation matches my question and budget.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-06-ac-01"></a> **US-06-AC-01:** Use mode runs the specified allowed algorithm; select mode records a selection from the allowed set; compare mode evaluates every algorithm in that set within the approved plan and budgets.
- <a id="us-06-ac-02"></a> **US-06-AC-02:** All modes respect task compatibility, parameter boundaries, and trial/runtime budgets.
- <a id="us-06-ac-03"></a> **US-06-AC-03:** Comparing algorithms does not require exhaustive enumeration of parameter combinations.
- <a id="us-06-ac-04"></a> **US-06-AC-04:** Suggested algorithms or expanded ranges are recorded only as recommendations for a subsequent experiment; adopting them requires a new versioned configuration and applicable approvals.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-07: Generate reviewable experiment notebooks

As a data scientist, I want agents to generate readable notebooks and project code so that I can inspect, edit, and understand their work.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-07-ac-01"></a> **US-07-AC-01:** Generated notebooks include explanatory Markdown covering objectives, assumptions, code, results, and proposed next steps, with explicit parameter cells.
- <a id="us-07-ac-02"></a> **US-07-AC-02:** Notebooks import generic capabilities from the installed toolkit and shared project logic from the experiment package without paths into a toolkit checkout.
- <a id="us-07-ac-03"></a> **US-07-AC-03:** Saved notebooks support interactive use and fresh-kernel managed execution without hidden state.
- <a id="us-07-ac-04"></a> **US-07-AC-04:** Generated notebooks, helpers, and project code stay within the experiment repository and authorized storage; the toolkit installation/source remain unchanged.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-08: Explore interactively under the same controls

As a data scientist, I want to explore interactively in VS Code under the experiment's access rules so that exploration preserves evaluation integrity.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-08-ac-01"></a> **US-08-AC-01:** Interactive notebooks use the project environment with the required notebook dependencies; VS Code is the documented editor for manual verification.
- <a id="us-08-ac-02"></a> **US-08-AC-02:** Interactive kernels cannot access protected test data, including through arbitrary Python outside toolkit API calls.
- <a id="us-08-ac-03"></a> **US-08-AC-03:** Training cells submit through managed APIs that enforce candidate boundaries, applicable approvals, budgets, and tracking.
- <a id="us-08-ac-04"></a> **US-08-AC-04:** Interactive execution cannot establish acceptance; recorded results require managed execution of saved snapshots and independent evaluation.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-09: Execute saved notebooks reproducibly

As a data scientist, I want saved notebooks executed automatically from a fresh kernel with explicit inputs so that recorded results do not depend on hidden state.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-09-ac-05"></a> **US-09-AC-05:** Access restrictions, approvals, and budgets apply equally to notebook and Python entrypoints; unauthorized filesystem or credential access is blocked.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-12: Assess data quality and define splits

As a data scientist, I want basic data validation and review so that I can identify extraction and quality-rule failures before accepting a reproducible data run.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-12-ac-04"></a> **US-12-AC-04:** Dataset assessment and split protocol are presented for approval before dependent feature or modeling work.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-17: Respect immutable supplied components

As a data scientist, I want supplied code to remain immutable unless I approve changes so that agents respect ownership and component permissions.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-17-ac-01"></a> **US-17-AC-01:** Supplied components are immutable by default; agents may configure and invoke them only within authorized boundaries.
- <a id="us-17-ac-02"></a> **US-17-AC-02:** Attempts to modify immutable components are blocked unless recorded developer approval authorizes the change.
- <a id="us-17-ac-03"></a> **US-17-AC-03:** Approved changes to immutable code create a new versioned experiment configuration.
- <a id="us-17-ac-04"></a> **US-17-AC-04:** Modification permission does not expand algorithm, parameter, data-access, or evaluation boundaries; authorized code changes appear in run snapshots.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-19: Manage PyTorch execution

As a data scientist, I want PyTorch runs to support CPU/GPU execution, checkpoints, and cancellation so that deep-learning experiments are manageable.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-19-ac-01"></a> **US-19-AC-01:** Basic PyTorch training runs on CPU and supports GPU execution when the required hardware/backend is available.
- <a id="us-19-ac-02"></a> **US-19-AC-02:** Checkpoints are captured as run artifacts and can be restored by the model implementation.
- <a id="us-19-ac-03"></a> **US-19-AC-03:** Cancellation stops managed training and preserves available logs, checkpoints, and status.
- <a id="us-19-ac-04"></a> **US-19-AC-04:** Resource requests, hardware metadata, runtime limits, and supported quotas are recorded and enforced where supported.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-22: Improve models using development feedback

As a data scientist, I want agents to revise experiments using structured development feedback so that model improvement can proceed within approved scope.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-22-ac-01"></a> **US-22-AC-01:** The agent receives structured evaluation feedback and produces revised notebooks or code with an evidence-based explanation.
- <a id="us-22-ac-02"></a> **US-22-AC-02:** Revisions remain within the current approved workflow phase, component permissions, parameter boundaries, access scope, and budgets.
- <a id="us-22-ac-03"></a> **US-22-AC-03:** Each revision undergoes managed execution and independent evaluation, preserving its source snapshots and results.
- <a id="us-22-ac-04"></a> **US-22-AC-04:** Iteration stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or developer cancellation.
- <a id="us-22-ac-05"></a> **US-22-AC-05:** Workflow phase returns and scope expansions await authorization; protected-test feedback never enters the revision loop.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-23: Approve workflow phase progression and scope changes

undefined

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-23-ac-01"></a> **US-23-AC-01:** Initial plan approval completes problem definition; later workflow phase advancement is blocked until sufficient independent evidence and developer approval are recorded.
- <a id="us-23-ac-02"></a> **US-23-AC-02:** Each decision records an authenticated developer reviewer, reviewed plan/configuration identity and scope, decision, timestamp, and associated evidence in durable project-associated state. Agent actions and assistant tool-execution permissions cannot stand in for developer approval.
- <a id="us-23-ac-03"></a> **US-23-AC-03:** Revision authorizes work only within its recorded scope; workflow phase returns, expanded permissions, and changed evaluation criteria require authorization before execution.
- <a id="us-23-ac-04"></a> **US-23-AC-04:** Workflow phases can be skipped only when the approved plan identifies valid existing artifacts supporting the skip.
- <a id="us-23-ac-05"></a> **US-23-AC-05:** Rejection or cancellation preserves results; successful final evaluation requires explicit model approval before completion.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-24: Protect final holdout evaluation

As a data scientist, I want protected holdout evaluation reserved for the authorized final workflow phase so that final-test results do not influence development.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-24-ac-01"></a> **US-24-AC-01:** Experiment agents, training code, and exploratory kernels cannot access protected test data; protection is enforced independently of agent instructions.
- <a id="us-24-ac-05"></a> **US-24-AC-05:** Completion requires developer approval of successful final evaluation.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-25: Resume interrupted workflows

As a data scientist, I want interrupted workflows to resume from durable state without repeating completed runs so that work and approvals are preserved.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-25-ac-01"></a> **US-25-AC-01:** Project-associated durable state preserves workflow phase progress, run identifiers, evidence, approvals, budgets, and terminal or reviewable outcomes.
- <a id="us-25-ac-02"></a> **US-25-AC-02:** Recovery reconciles recorded work and resumes without duplicating completed runs or bypassing pending gates.
- <a id="us-25-ac-03"></a> **US-25-AC-03:** Resumed tasks use the preserved compatible configuration and runtime instruction bundle, even if source guidance has changed.
- <a id="us-25-ac-04"></a> **US-25-AC-04:** Cancelled, failed, budget-exhausted, and review-required outcomes retain evidence and do not silently authorize further work.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-26: Audit workflow decisions and evidence

As a data scientist, I want recorded runs linked to their exact inputs, code, and environment so that I can inspect and audit results.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-26-ac-10"></a> **US-26-AC-10:** Toolkit manifests connect runs, MLflow records, DVC state, configuration versions, runtime bundles, and approval records.
- <a id="us-26-ac-11"></a> **US-26-AC-11:** The audit trail identifies the scope authorizing each workflow phase, approved scope changes, and the evidence used for each decision.
- <a id="us-26-ac-13"></a> **US-26-AC-13:** Resumption and reuse preserve original producer provenance and the decisions authorizing subsequent use.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-28: Diagnose data gaps and propose acquisition

As a data scientist, I want evidence-backed data-gap diagnoses and acquisition proposals so that I can decide whether additional data is worth obtaining.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-28-ac-01"></a> **US-28-AC-01:** Diagnosis records evidence of data deficiencies, such as underrepresented classes or data slices, using approved data and development evaluation results.
- <a id="us-28-ac-02"></a> **US-28-AC-02:** A structured proposal records its reason, evidence, acquisition hypothesis, source, strategy, expected benefit, costs, limits, and required authorization.
- <a id="us-28-ac-03"></a> **US-28-AC-03:** Expected benefit is presented as a hypothesis rather than a guaranteed improvement.
- <a id="us-28-ac-04"></a> **US-28-AC-04:** Proposals do not use protected final-test feedback or expand access, evaluation protocols, or budgets without approval.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-29: Acquire data and measure its effect within approved limits

As a data scientist, I want authorized acquisition to enforce limits, version new data, compare outcomes, and stop at defined conditions so that data improvement remains controlled.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-29-ac-01"></a> **US-29-AC-01:** Acquisition is blocked without recorded authorization covering source, strategy, scope, and limits; approved in-scope activity need not request permission for every operation.
- <a id="us-29-ac-02"></a> **US-29-AC-02:** Execution enforces source permissions and cost, record, runtime, and compute budgets, preserving evidence when a limit is reached.
- <a id="us-29-ac-03"></a> **US-29-AC-03:** Acquired data is validated and versioned with source lineage; synthetic or augmented data is explicitly identified as distinct from observed data.
- <a id="us-29-ac-04"></a> **US-29-AC-04:** Returning to validation/EDA and downstream development requires the applicable workflow phase authorization, with complete audit records.
- <a id="us-29-ac-05"></a> **US-29-AC-05:** Before-and-after model comparisons use consistent approved evaluation protocols and link results to the corresponding dataset versions.
- <a id="us-29-ac-06"></a> **US-29-AC-06:** The acquisition loop stops on success, budget exhaustion, lack of improvement, unrecoverable failure, policy violation, or cancellation, preserving a reviewable outcome.
- <a id="us-29-ac-07"></a> **US-29-AC-07:** Resumption after acquisition retains approvals, budget usage, dataset lineage, and completed-run identities; advanced acquisition strategies remain deferred according to the design's [milestone delivery plan](design/milestone-delivery.md#11-milestone-delivery-plan).

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

### US-30: Connect the first agent with preserved runtime guidance

As a data scientist, I want an agent adapter with explicit, preserved runtime guidance so that agent behavior follows the approved experiment context.

**Deferred:** original criteria below are not MVP prerequisites or delivered behavior.

Acceptance criteria:

- <a id="us-30-ac-01"></a> **US-30-AC-01:** The first managed coding-assistant adapter verifies a concrete product/interface/version and supports capability discovery, structured task/result exchange, and documented task cancellation through the common contract. Interactive assistants can use the public toolkit CLI/API without an adapter. Acceptance demonstrates task receipt, project-code/notebook revision, managed execution, development-feedback consumption, and stopping at a developer approval boundary.
- <a id="us-30-ac-02"></a> **US-30-AC-02:** Runtime loading explicitly selects packaged shared guidance, relevant task-specific guidance, and configured project guidance, recording ownership and order.
- <a id="us-30-ac-03"></a> **US-30-AC-03:** Development `AGENTS.md` files from either repository are excluded from automatic loading by the toolkit runtime loader. Instructions independently loaded by an external assistant are outside this guarantee; observable additional context and capture limitations are recorded.
- <a id="us-30-ac-04"></a> **US-30-AC-04:** The plan snapshots toolkit-supplied guidance contents, paths, versions/checksums, and load order; subsequent tasks reference the preserved bundle, with managed adapters demonstrating delivery. This records toolkit-supplied guidance, not the assistant's complete instruction context.
- <a id="us-30-ac-05"></a> **US-30-AC-05:** Conflicting guidance or attempts to expand experiment constraints block affected execution; adopting changed guidance requires a new versioned configuration and applicable approvals.
- <a id="us-30-ac-06"></a> **US-30-AC-06:** Two adapters successfully execute tasks using the same versioned task/result contract.
- <a id="us-30-ac-07"></a> **US-30-AC-07:** Capability discovery identifies which tasks each adapter supports before delegation.
- <a id="us-30-ac-08"></a> **US-30-AC-08:** Both managed adapters meet the common cancellation, toolkit-guidance delivery, developer-approval, access, and toolkit-run budget requirements, including boundaries for assistant tools/workspaces. Agent-task cancellation is recorded separately from experiment-run cancellation; assistant usage measurement/control capabilities and limitations are explicit. Resumption uses durable task/run evidence and consumed budgets rather than assistant memory.
- <a id="us-30-ac-09"></a> **US-30-AC-09:** Agent selection does not alter independent evaluation or the experiment's allowed boundaries.

Supporting design: [overview](agentic-ml-harness-design.md) and reading map; MVP alignment in design 0.15; Gate 3 approved. Scope history: [approved dispositions](../reviews/mvp-scope-criterion-dispositions.md).

M50/M99 criteria and their original notes below are retained. References in those
historical notes to the former milestone sequence do not expand the revised MVP.

## Milestone 50: Improve the technical environment

This milestone contains ongoing improvements to the repository's development, testing, and verification environment. It is separate from the product delivery sequence in Milestones 0–6. Add user stories as improvement areas are identified; inclusion does not authorize implementation or establish a completion date for the milestone. Each story retains the repository's implementation planning, developer approval, and verification requirements.

The initial stories address the number of test environments created, retained disk usage, and peak disk usage. They preserve existing acceptance criteria, assertions, timeouts, package provenance, and installed-package isolation. They do not authorize deleting historical verification evidence or existing workspaces. Cleanup ownership and retention are separate from fixture reuse and sequential environment lifetime.

### US-35: Clean up successful verification environments

As a contributor, I want successful verification runs to remove disposable environments while preserving diagnostic records so that repeated checks do not accumulate unnecessary disk usage.

Acceptance criteria:

- <a id="us-35-ac-01"></a> **US-35-AC-01:** Successful standalone installation, distribution, initialization, and planning verification removes environments and disposable installer caches created by the invocation after all dependent checks complete.
- <a id="us-35-ac-02"></a> **US-35-AC-02:** Commands, logs, artifact identities, environment identity manifests, and verification results are preserved beneath the toolkit repository's `.dev-records/verification/` directory, separately from disposable environments and workspaces. Records are retained for the lifetime of agentic-ml development, and each verification invocation reports its absolute record location. Successful cleanup preserves these records.
- <a id="us-35-ac-03"></a> **US-35-AC-03:** Failed verification retains available diagnostic records and environments for inspection. A documented option preserves successful workspaces when explicitly requested.
- <a id="us-35-ac-04"></a> **US-35-AC-04:** Cleanup is limited to disposable paths created and owned by the invocation. Existing environments, caller-owned files, shared caches, source checkouts, and historical evidence remain intact; cleanup failure is reported without concealing the original verification outcome.
- <a id="us-35-ac-05"></a> **US-35-AC-05:** Automated checks cover default successful cleanup, failure retention, explicit retention, ownership boundaries, and cleanup failure. Before-and-after evidence records retained environment counts and disk usage for the same verification workload, including platform and filesystem measurement limits.

Notes: The verification drivers currently retain workspaces on success and failure, as documented in the [development guide](../development.md#distribution-builds-and-installed-verification). Revise that retention contract as part of implementation. Follow the [retained development records policy](../development.md#retained-development-records): `.dev-records/` holds ignored raw evidence, while `docs/verification/` holds tracked review reports. Backup and checkout replacement must preserve retained records. This policy does not require keeping large environments, caches, or datasets. US-36 governs pytest workspace placement; US-38 governs releasing environments before an entire invocation finishes.

### US-36: Give pytest ownership of verification workspaces

As a contributor, I want verification launched by pytest to create its temporary workspaces beneath the owning test directory so that pytest retention can bound disk usage across test runs.

Acceptance criteria:

- <a id="us-36-ac-01"></a> **US-36-AC-01:** Verification drivers invoked by pytest accept an explicit workspace location, and all nested verification workspaces are descendants of the owning test's temporary directory rather than independently allocated system temporary directories.
- <a id="us-36-ac-02"></a> **US-36-AC-02:** By default, each successful test's owned verification workspace, including nested workspaces, is deleted during that test's teardown after its final consumer completes, before the test reports completion; cleanup does not wait for session shutdown or a later pytest invocation. Failed-test directories are retained for one invocation. Explicit successful-workspace retention remains available. The documentation distinguishes per-test cleanup, shared fixture paths that remain in use until their final consumer completes, standalone workspaces, and interrupted runs where automatic cleanup is not guaranteed.
- <a id="us-36-ac-03"></a> **US-36-AC-03:** Concurrent workers, concurrent test sessions, and nested pytest runs use distinct workspace paths. Cleanup from one invocation cannot remove another active invocation's files.
- <a id="us-36-ac-04"></a> **US-36-AC-04:** Standalone verification remains usable outside pytest, and failed-test diagnostics identify the owning workspace. Callers can explicitly retain successful workspaces using the documented retention controls.
- <a id="us-36-ac-05"></a> **US-36-AC-05:** Automated checks verify nested workspace containment, deletion of a successful test's owned workspace at the end of that test while the pytest session is still running, explicit successful-workspace retention, failed retention across repeated invocations, and concurrent-run isolation. Evidence records workspace counts and retained disk usage without changing verification assertions or timeouts.

Notes: Merely setting pytest retention does not affect driver workspaces created independently with `tempfile.mkdtemp()`. Preserve the nested-pytest directory isolation recorded in the [runtime optimization report](../verification/pytest-runtime-optimization.md). Coordinate with US-35 so that driver cleanup and pytest retention have explicit ownership and do not conflict. US-36 can be delivered independently of environment reuse.

### US-37: Reuse installed environments across compatible tests

As a contributor, I want compatible tests to reuse an installed toolkit environment while keeping project state isolated so that verification creates fewer full dependency environments.

Acceptance criteria:

- <a id="us-37-ac-01"></a> **US-37-AC-01:** A reviewed inventory maps affected tests to their public interfaces and acceptance criteria, identifies candidates for environment reuse, and records which tests require fresh environments and why before fixture changes are implemented.
- <a id="us-37-ac-02"></a> **US-37-AC-02:** Compatible tests reuse an installed environment containing the intended toolkit revision and dependencies while retaining independent project files, configuration, stores, and durable state. Installed-package tests continue to run outside the toolkit checkout without editable installs or contributor dependency leakage.
- <a id="us-37-ac-03"></a> **US-37-AC-03:** Tests that install, synchronize, upgrade, damage, or otherwise mutate an environment retain independent environments. Clean installation, cache independence, lock/pin preservation, and genuine direct-wheel and source-distribution-rebuilt-wheel coverage remain verified.
- <a id="us-37-ac-04"></a> **US-37-AC-04:** Reuse does not introduce test-order dependence, cross-project state leakage, or concurrent mutation of a shared environment. Automated checks exercise the selected tests in differing orders and under the supported parallel scheduling configuration.
- <a id="us-37-ac-05"></a> **US-37-AC-05:** Before-and-after runs of the same selected test cases demonstrate fewer environment creations and record peak and retained disk usage, elapsed time, package identities, platform, and filesystem limitations. Existing assertions and timeouts remain unchanged, and runtime regressions are reported.

Notes: Initialization currently uses a fresh installed project for each test. Reuse candidates must preserve each test's actual public interface and project/environment association; fixture scope must not be broadened blindly. Share only where these boundaries permit it. Reuse does not authorize replacing installed-package verification with source-only tests. Previous hardlink and installer concurrency experiments are recorded in the [fixture profile](../verification/pytest-fixture-profile.md) and [concurrency report](../verification/pytest-installer-concurrency.md); changing those policies is outside this story.

### US-38: Release wheel environments between verification paths

As a contributor, I want each completed wheel verification environment released before the next independent path starts so that package verification needs less peak disk space.

Acceptance criteria:

- <a id="us-38-ac-01"></a> **US-38-AC-01:** Distribution verification completes all checks for the direct wheel, preserves its diagnostic records, and removes its disposable environment before installing the wheel genuinely rebuilt from the source distribution.
- <a id="us-38-ac-02"></a> **US-38-AC-02:** Initialization and planning verification identify every consumer of each installed environment and release it after its final dependent check, before starting the next independent artifact path. An environment is never removed while a downstream probe still needs it.
- <a id="us-38-ac-03"></a> **US-38-AC-03:** Both artifact paths retain fresh independent installations, declared runtime dependencies, correct origin metadata, and the same required installed-package checks. Success in the direct-wheel path cannot substitute for or conceal failure in the rebuilt-wheel path.
- <a id="us-38-ac-04"></a> **US-38-AC-04:** Failed paths retain available environments and diagnostics; explicit workspace retention preserves completed environments when requested. Normal cleanup removes only invocation-owned disposable paths and preserves logs and identity manifests.
- <a id="us-38-ac-05"></a> **US-38-AC-05:** Automated checks verify environment lifetime across downstream consumers, both successful paths, later-path failure, and explicit retention. Before-and-after evidence demonstrates fewer simultaneously retained full environments for the same workload and records peak disk usage and measurement limits.

Notes: This story reduces peak usage within one invocation; US-35 reduces retained usage after completion. Coordinate their cleanup and retention behavior. The initialization and planning drivers currently invoke distribution verification and then consume its installed environments, so cleanup must follow the complete consumer lifecycle rather than occur immediately after an intermediate probe.

## Milestone 99: Future enhancements

This milestone groups enhancements that are not critical to current functionality. Inclusion records deferred scope rather than a commitment to delivery order. Unlike Milestones 0–6, this milestone is a backlog of future enhancements; stories can move into a delivery milestone when prioritized, preserving their acceptance criterion IDs.

### US-34: Establish contribution and review checks

As a contributor, I want clear contribution instructions and consistent review checks so that I understand how to submit changes and when they are ready to merge.

Acceptance criteria:

- <a id="us-34-ac-01"></a> **US-34-AC-01:** Contribution instructions describe how to prepare and submit changes and link to the development setup and verification commands.
- <a id="us-34-ac-02"></a> **US-34-AC-02:** Required CI checks and review expectations are documented, including the conditions for merging a pull request.
- <a id="us-34-ac-03"></a> **US-34-AC-03:** Branch protection enforces the documented required checks and review expectations on the default branch.

## Historical link aliases

These anchors preserve prior issue/plan/design references as migration context;
they do not reinstate the old delivery sequence or superseded wording.

<a id="milestone-1-run-and-record-a-reproducible-experiment"></a>

<a id="us-10-control-and-inspect-runs"></a>

<a id="us-11-extract-approved-source-data"></a>

<a id="us-12-validate-extracted-data"></a>

<a id="us-13-version-and-restore-datasets"></a>

<a id="us-26-record-run-artifacts-and-provenance"></a>

<a id="us-27-reproduce-a-basic-run-in-a-clean-environment"></a>

<a id="milestone-2-assess-data-and-build-reproducible-feature-pipelines"></a>

<a id="us-14-generate-and-compare-feature-pipelines"></a>

<a id="us-16-register-supplied-preprocessing-components"></a>

<a id="us-27-reproduce-and-reuse-pipeline-stages"></a>

<a id="milestone-3-train-tune-and-independently-evaluate-models"></a>

<a id="us-16-register-supplied-models"></a>

<a id="us-18-train-across-supported-frameworks"></a>

<a id="us-20-tune-within-declared-limits"></a>

<a id="us-21-independently-assess-experiment-results"></a>

<a id="us-26-compare-runs-and-review-the-final-report"></a>

<a id="milestone-4-let-an-agent-improve-an-experiment"></a>

<a id="milestone-5-supervise-and-resume-the-complete-workflow"></a>

<a id="us-30-use-interchangeable-agent-adapters"></a>

<a id="milestone-6-improve-the-dataset-through-authorized-acquisition"></a>

<a id="us-01-install-a-pinned-harness-version"></a>
