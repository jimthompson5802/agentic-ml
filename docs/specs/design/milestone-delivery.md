# Milestone Delivery

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Milestone Delivery Plan.

**Related contracts:** Read [acceptance traceability](acceptance-traceability.md); [architecture decisions](architecture-decisions.md); [interfaces and configuration](interfaces-and-configuration.md); [execution and governance](execution-and-governance.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 11. Milestone Delivery Plan

Use the [repository planning terminology](../../../README.md#planning-terminology). Milestones 0–6 correspond to the authoritative delivery sequence; Milestone 99 groups deferred enhancements without committing their order. Detailed plans divide each user story into implementation phases with granular tasks, required evidence, and an explicit developer approval gate at the end of each implementation phase. Label them with the story ID and local phase number, plus the milestone when a story spans milestones. Workflow phases in [Sections 4–5](../agentic-ml-harness-design.md#4-hierarchical-closed-loop-workflow) describe ML experiment execution.

Current-version experiment approval scope follows
[US-03-SC-01](../../plans/milestone-1-us-03.md#us-03-sc-01--unauthenticated-experiment-approvals-2026-10-31):
use explicit scoped unauthenticated records, without reviewer authentication or
protection against fabricated approval/history. Authenticated approval remains
future work (US-23-AC-02); no separate signing identity or protected-policy host
is a current-version prerequisite. Other access/budget/evaluation controls and
all harness development/testing verification and approval gates remain required.

Each milestone delivers the controls required by its assigned user stories before the capability they govern becomes available. Early approvals may be developer-driven, but must be recorded, scoped, and enforced. Milestone 1 includes execution/extraction authorization, access restrictions, budget enforcement, and independent artifact checks. Milestone 2 adds dataset-assessment and split-protocol approval, approval of the baseline feature set and fixed reference estimator/settings and metric, training-only preprocessing/estimator fitting, independent validation scoring, and enforced protected-test isolation for predictive feature comparison. Milestone 3 adds approval of broader model baselines, authorized final evaluation using independently enforced protected-test access, and developer approval of successful final evaluation. Milestone 4 applies these controls to agent work, including component permissions, parameter boundaries, and stopping conditions. Milestone 5 completes durable coordination across workflow phases and recovery using the controls delivered earlier.

| Milestone | Deliverables | Exit criteria |
|---|---|---|
| 0. Harness development foundation | Contributor setup and conventions, locked development tools, macOS CI, minimal version CLI, wheel/source builds and isolated package verification | Documented clean-checkout setup and shared checks pass; both wheel paths pass installed-package checks with diagnostic evidence |
| 1. Data and harness foundation | GitHub-installable package pinned by full commit SHA, agentic-ml CLI/init, packaged templates/guidance, bootstrap documentation, project configuration and locked environment, validation of developer-supplied brief/configuration decisions and versioned plan recording without an agent dependency, YAML search-space validation, schemas, local Python/notebook execution, extraction, immutable source/configuration bundles and versioned run manifests, verified dataset restoration and agent-free replay, basic validation and review, recorded scoped execution/extraction approvals, filesystem/credential/source access restrictions, runtime/experiment-count and applicable resource/cost/record limits, independent expected-artifact checks, MLflow tracking, local DVC/state storage, public API | Basic validation results approved; unauthorized access and unapproved work blocked for Python and notebooks, configured limits enforced, and expected artifacts independently checked before run acceptance; clean-environment GitHub install and initialization followed by validated, versioned plan recording and repeatable extraction/notebook execution in a separate project without agents or a manually maintained harness checkout; clean second-machine replay executes captured uncommitted notebook changes and a required untracked helper, verifies required evidence/data checksums, fails explicitly for missing or corrupted inputs, and passes the recorded output checks |
| 2. EDA and feature pipelines | Dataset profiling (distributions, class balance where relevant, anomalies, and leakage diagnostics), versioned training/validation/protected-test split manifests respecting approved time/group constraints, dataset-assessment and split-protocol approval before dependent feature or modeling work, transformations, project-local registration of user-supplied stateful/stateless preparation, fitted-state persistence/restoration, DVC pipeline stages and lockfiles, lineage, minimal reference-estimator training/prediction and independent validation scoring for predictive feature comparison, approved baseline feature set and fixed estimator/settings and metric, protected-test isolation | Approved dataset assessment and split protocol; validated, reproducible feature artifacts with training-only fitting, including supplied preprocessing without harness modifications; reproducible baseline/candidate predictive comparisons under the fixed approved estimator and validation protocol with recorded gains/ties/regressions, preserved run evidence, enforced budgets, and protected-test access blocked |
| 3. Model experimentation | Broader model experimentation beyond the milestone 2 fixed reference estimator: scikit-learn, LightGBM, basic PyTorch, project-local custom model registration and parameter validation, model persistence/restoration, documented PyTorch checkpoint restoration with declared-state metadata and cancellation preservation, bounded hyperparameter evaluation, algorithm use/select/compare modes, approved baseline before candidate comparisons, independent protected-test isolation, authorized final evaluation, final-model review | Baseline approved before candidate comparisons; protected test data inaccessible to training code and exploratory kernels and accessible only to the independent evaluator for authorized final evaluation; successful final evaluation approved by the developer before completion; tabular and basic deep-learning runs tracked and assessed; emitted PyTorch checkpoints restored and verified usable through the model implementation; cancellation stops training and preserves available checkpoints, restoration metadata, logs, and terminal status, including after forced termination; supplied models run and undergo independent evaluation without harness modifications |
| 4. Agent integration | Verified first managed coding-assistant adapter and documented interactive CLI/API use, project-local notebook/code generation, packaged/project runtime instruction loading and snapshots, structured feedback, inner-loop iteration with recorded approvals, enforced component/parameter/access boundaries, budgets, and stopping conditions | Agent revisions independently evaluated within approved scope; scope expansions blocked pending authorization; a concrete managed integration receives a task, edits project code/notebooks, submits managed execution, consumes development feedback, and stops at a developer approval boundary; run/task cancellation and guidance delivery verified; agent improves a model through user-reviewable notebooks within approved harness budgets, with assistant usage coverage explicit, without modifying the harness |
| 5. Orchestration and approvals | Durable workflow spanning multiple ML workflow phases coordinating existing approvals and gates, submission identity and recovery contracts, second adapter; define concrete schemas, persistence, ownership/fencing, and runner/tracking reconciliation mechanisms | Supervised workflow spanning multiple ML workflow phases preserves and coordinates earlier controls through interruption and recovery; recovery fixtures demonstrate duplicate-free submission/completed-run reuse, safe review of uncertainty, retry-safe finalization, preserved budgets/provenance, and rejection of stale recovery owners |
| 6. Iterative data acquisition | Gap diagnosis, proposals, approved extraction, retraining comparisons | Outer-loop improvement with lineage and budgets |
| Uncommitted future ideas (not assigned delivery stories) | Ray-backed runner for parallel experiments and hyperparameter trials, followed by distributed training as needed; Optuna, active learning, labeling, augmentation, specialized agents, containers | Ray execution preserves harness governance and lineage; extensible multi-agent workflow with advanced compute/data strategies |

### Milestone 0 dependencies and delivery order

Milestone 0 covers US-31, US-32, and US-33. The dependencies below follow from their [acceptance criteria](../user-stories.md#milestone-0-establish-the-harness-development-foundation). They apply to portions of stories rather than requiring each prerequisite story to be complete. The delivery order is a recommendation, not an additional acceptance requirement.

**Prerequisites:** No earlier milestone is required. Python 3.12 or newer, `uv`, and the other documented contributor prerequisites support the initial development foundation (US-31-AC-01–02).

| Dependent work | Required capability | Acceptance criterion basis |
|---|---|---|
| US-31 source-checkout execution and fresh-environment smoke verification | US-33 minimal `agentic-ml --version` CLI | US-31-AC-03, US-31-AC-07; US-33-AC-06–07 |
| US-32 automated development checks | US-31 locked development tools, check configuration, and documented local commands | US-31-AC-02, US-31-AC-04–05, US-31-AC-08; US-32-AC-02–03 |
| US-33 local package builds and verification | Shared development environment and documented tooling established under US-31 | US-31-AC-02, US-31-AC-08; US-33-AC-01–04 |
| US-33 package verification in CI | US-32 CI infrastructure plus working US-33 build and installed-package checks | US-32-AC-01–04; US-33-AC-05 |

**Recommended delivery order:**

1. Establish the US-31 development foundation: package configuration, locked environment, coding conventions, automated check configuration, and local commands.
2. Add the US-33 minimal package foundation: `agentic_ml`, `agentic-ml --version`, and provisional template and runtime guidance resources.
3. Complete US-31 fresh-checkout macOS verification, including the version smoke check.
4. Establish US-32 CI using the shared local development commands.
5. Complete US-33 isolated verification of the directly built wheel and the wheel rebuilt from the source distribution, and run those checks in CI.

Local package verification and CI setup can proceed in parallel once their prerequisites exist. Treating these relationships as whole-story completion gates would create an apparent cycle: US-31 needs the minimal CLI from US-33, while US-33 uses the development foundation and CI from US-31 and US-32. Detailed implementation plans should stage those capabilities explicitly and retain their developer approval gates.

**Completion boundary:** All acceptance criteria for US-31, US-32, and US-33 must be verified to complete Milestone 0. No Milestone 1 capability is a prerequisite: Milestone 0 owns the minimal version CLI and provisional packaged resources; usable experiment initialization resources and experiment commands remain in later milestones (US-33-AC-03, US-33-AC-06).

### Milestone 1 dependencies and delivery order

Milestone 1 covers US-01, US-02, US-03, US-05, US-09, US-10, US-11, the validation portion of US-12, US-13, and initial US-26 and US-27. The dependencies below follow from their [acceptance criteria](../user-stories.md#milestone-1-run-and-record-a-reproducible-experiment). They apply to portions of stories rather than requiring each prerequisite story to be complete. The delivery order is a recommendation, not an additional acceptance requirement.

**Prerequisites:** Milestone 0 establishes the installable package, CLI, packaged resources, shared development checks, and CI. Milestone 1 extends that foundation with usable experiment initialization resources and execution capabilities.

| Dependent work | Required capability | Acceptance criterion basis |
|---|---|---|
| US-02 experiment initialization | US-01 installed harness and pinned project dependency | US-01-AC-01–03; US-02-AC-01–03 |
| US-03 input resolution and US-05 configuration validation | Initialized project inputs and environment; declared objectives, search boundaries, and execution configuration | US-02-AC-01–03; US-03-AC-01–05; US-05-AC-01–05 |
| US-10 managed run controls and initial US-26 capture | Configured storage, resolved inputs, environment identity, and applicable validation before execution | US-02-AC-04; US-03-AC-03–05; US-05-AC-04–05; US-10-AC-01–03; US-26-AC-02–04 |
| US-11 approved extraction | Configured sources and storage, resolved extraction requirements, and authorization, access, and limit enforcement | US-02-AC-04–05; US-03-AC-03–04; US-11-AC-02–05 |
| US-12 basic validation and US-13 source-data versioning | US-11 extracted snapshots and metadata; US-02 DVC/storage setup | US-11-AC-04–05; US-12-AC-01, US-12-AC-05; US-13-AC-01–04 |
| US-09 recorded notebook execution | Locked environment, resolved inputs and applicable validation, US-10 run controls, and US-26 source capture and evidence recording; accepted and versioned datasets where required | US-09-AC-01–05; US-10-AC-01–03, US-10-AC-05; US-12-AC-05; US-13-AC-01–02; US-26-AC-01–05 |
| US-26 complete run provenance and independent artifact checks | US-01 harness/environment identity, US-03 configuration identity, US-13 dataset state, and US-09/US-10 execution outcomes and artifacts | US-01-AC-03–04; US-03-AC-03; US-13-AC-01–02; US-26-AC-01–05 |
| US-27 clean-environment reproduction | Pinned installation, US-13 verified dataset restoration, US-26 preserved source and provenance, managed replay, and declared output checks | US-01-AC-01–03; US-13-AC-03–04; US-26-AC-02–05; US-27-AC-01–04 |

**Recommended delivery order:**

1. Establish US-01 pinned installation and US-02 conflict-safe project initialization, including the locked environment and local storage.
2. Implement US-03 resolved, versioned experiment inputs and US-05 applicable configuration and boundary validation.
3. Establish US-10 run controls and initial US-26 capture and evidence storage. Enforce the authorization, access restrictions, and budgets required by each operation before enabling it.
4. Implement US-11 approved extraction, followed by US-12 basic validation and approval and US-13 source-snapshot versioning and verified restoration.
5. Integrate US-09 saved-notebook execution with US-10 lifecycle controls and US-26 complete provenance and independent artifact checks.
6. Complete US-27 clean-environment restoration and replay against declared output checks, including missing or corrupted input failures.

Basic data validation and source-data versioning can proceed in parallel once extraction snapshots exist. US-09, US-10, and US-26 require coordinated integration slices: preserve exact source, configuration, input references, and environment identity before execution; enforce controls and expose status and cancellation during execution; then preserve available outputs and diagnostics and independently check expected artifacts before acceptance. Start with a small complete run path and extend it through failure, timeout, cancellation, and restoration behavior. Each slice must include the controls applicable to the operation it enables. Detailed story plans should name these capability prerequisites and retain their developer approval gates.

Milestone 1 already requires approved extraction within source permissions and limits, equivalent restrictions for Python and notebook execution, run budgets, and approval of basic dataset validation results (US-11-AC-03; US-09-AC-05; US-10-AC-03; US-12-AC-05). These controls accompany their capabilities rather than waiting for Milestone 5. Milestone 5 extends them into durable coordination across the complete workflow, including interruption recovery. Record and resolve authorization and isolation design decisions before implementing dependent Milestone 1 behavior.

**Completion boundary:** Verify the Milestone 1 criteria for the stories listed above through an authorized, recorded, independently checked, reproducible extraction-to-notebook run in a separate experiment project without an agent dependency. Detailed profiling and split protocols begin in Milestone 2; broader modeling, agent integration, and complete workflow orchestration remain in their assigned milestones. Later portions of US-12, US-26, and US-27 are not prerequisites for Milestone 1 completion.

### Deferred enhancements

Milestone 99 contains US-34: contribution instructions, documented merge checks and review expectations, and enforced default-branch protection. These are deferred rather than Milestone 0 exit criteria. Advanced capability ideas above do not add approved stories to Milestone 99.

Milestone 1 extends the package foundation established in Milestone 0 and delivers reproducible extraction, basic validation and review, recorded Python/notebook execution, and source-data/run restoration without requiring an agent. Developers may use external coding assistants to prepare inputs and code; harness-managed agent proposals and iteration are introduced in milestone 4. Detailed profiling and split manifests are introduced in milestone 2, before dependent feature or modeling work.

The milestone order is a product delivery sequence; workflow phases describe execution within an ML experiment. Basic PyTorch is included early; advanced distributed deep learning comes later.

