# Milestone 1 / US-18: Train scikit-learn classification models

## Scope and outcome

- **Milestone:** M1 — Complete one experiment.
- **User story:** [US-18](../specs/user-stories.md#us-18-train-scikit-learn-models), [GitHub #28](https://github.com/jimthompson5802/agentic-ml/issues/28).
- **User-visible outcome:** A project-owned Python script in a separate installed experiment project trains a reproducible CPU classification baseline, then an explicitly authored classifier candidate, predicts validation rows, and records native fitted artifacts and inspectable MLflow results with committed code/configuration, environment, feature and DVC data references.
- **Acceptance criteria:** Advance [US-18-AC-01](../specs/user-stories.md#us-18-ac-01) for classification; verify [AC-02](../specs/user-stories.md#us-18-ac-02), [AC-03](../specs/user-stories.md#us-18-ac-03) and [AC-04](../specs/user-stories.md#us-18-ac-04) for M1. Regression completes AC-01 in M2; keep #28 open after M1 acceptance.
- **Included:** Extensible native scikit-learn classifier fitting/prediction/persistence without per-estimator toolkit changes; train-only preprocessing composition; candidate validation before fitting; one baseline and one authored candidate; validation accuracy; effective settings and installed version records; failure diagnostics; installed direct/rebuilt-wheel verification.
- **Excluded:** Search/trial orchestration (US-20), general feature comparison (US-14), general evaluation/tolerance interfaces (US-21), final-test evaluation/selection (US-24), execution service or new CLI runner (US-10), native stage scheduling (US-27), basic initialization/configuration bridge and assistant demonstration (US-39), regression/custom components/restoration (M2). No mandatory new experiment approvals, framework registry, workflow database or security/resource guarantees.
- **Coordinated execution index:** None. This plan consumes already merged capabilities and does not schedule another story's implementation. Replan if a new prerequisite capability is required.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [blueprint and pending decisions](../specs/design/software-blueprint.md#decisions-required-before-dependent-code), [interfaces](../specs/design/interfaces-and-configuration.md), [execution/tracking/evaluation](../specs/design/execution-and-governance.md), [data/features](../specs/design/data-and-features.md), [delivery order](../specs/design/milestone-delivery.md), [traceability](../specs/design/acceptance-traceability.md), [ADR-008](../specs/design/architecture-decisions.md#adr-008--local-experiment-mvp-and-externally-owned-assistant-use), [repository boundary](../specs/design/repository-layout.md).

## Workspace association

- **GitHub issue and story:** #28 / US-18.
- **Branch:** `US-18-classification`.
- **Base ref and starting commit:** Local `main`, `94e74ba38922a80b368860d53545a18f22d555e2`. No fetch/pull performed; remote freshness is not asserted.
- **Worktree:** `.worktrees/US-18-classification`, relative to the primary checkout.
- **Session ownership:** This planning session; use this checkout explicitly for subsequent work. Follow [worktree guidance](../development/worktrees.md). No environment has been created for planning.

## Sources and current findings

Issue #28's complete body and its one unique comment were retrieved on
2026-11-15 UTC. The [scope comment](https://github.com/jimthompson5802/agentic-ml/issues/28#issuecomment-6699594719)
assigns AC-01 to M1 classification/M2 regression and AC-02–04 to M1. A final
metadata refresh confirmed one comment and unchanged `updated_at`
`2026-11-07T00:29:21Z`; the issue is open with no GitHub milestone field.
The issue's automated-validation paragraph retains an older current-milestone
gate reference. Its linked repository verification policy and repository
instructions now require focused/regression checks at executable gates and
M1–6 at story acceptance; this plan follows that current policy.

Inspected source at the starting commit:

- `src/agentic_ml/preprocessing/__init__.py`: `fit_preprocessing` clones a native transformer Pipeline, validates the current frame/partition record, fits training features only, and returns fitted preprocessing plus plain metadata. It does not train an estimator.
- `src/agentic_ml/validation/`: `validate_candidate(CandidateRequest)` checks live strict validation evidence, materializes fixed/default/search parameters and rejects stale or invalid inputs. A returned result alone is not a durable execution authorization.
- `src/agentic_ml/registry/validation/1.0/builtins.json`: metadata covers dummy classifier/regressor only. Additive project metadata is supported; it does not bind algorithm names to executable classes.
- `src/agentic_ml/tracking/`: `log_preprocessing` preserves native preprocessing without finalizing a successful run; `log_run_results` records supplied metrics/outputs/provenance and finalizes a selected existing run. Neither computes scores nor trains/saves a complete classifier automatically.
- `tests/integration/test_preprocessing_tracking.py`, `tests/installation/verify_tracking.py`, `tracking_project.py` and `check_tracking.py`: established external-project/direct-wheel/genuinely-sdist-rebuilt-wheel pattern with durable evidence. Reuse fixture/evidence support rather than duplicating a packaging framework.
- `pyproject.toml`: scikit-learn and MLflow are already runtime dependencies. Its existing generated pytest workspace-member entry is a known container concern; do not silently repair it in this story. Report setup failure if it prevents the locked environment.

Some design/usage status paragraphs predate PR #68. Actual source, accepted
supplier plans and checkpoint establish preprocessing/tracking delivery; stale
paragraphs do not require reimplementation. Update only status text directly
affected by US-18 delivery during IP4.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Accepted data and partitions | Current, disjoint partition record and quality-guarded project input | IP2 fitting | Available in base: [US-12 assessment plan](milestone-1-us-12-assessment-splits.md), [quality guide](../data-quality.md); use existing APIs unchanged |
| US-15 preprocessing | Native fitted training-only transformer and its metadata | IP2/IP3 | [US-15 IP3-T1/T2 and IP4](milestone-1-us-15.md), Gates 1–4 approved; M1 accepted and merged in PR #68; [IP4 evidence](../verification/us-15-ip4.md) |
| US-26 recording | Explicit native run/store, shared provenance, output publication and failure finalization | IP3 | [US-26 IP2–4](milestone-1-us-26-recording.md), Gates 1–4 approved and #17 slice accepted in PR #68; [IP4 evidence](../verification/us-26-recording-ip4.md) |
| Native DVC identity | Real committed pointers and integrity-checked source/split artifacts | IP3/IP4 | [US-13 plan](milestone-1-us-13.md), Gates 1–3 approved; [recipe](../dataset-versioning.md); no stage engine prerequisite |
| Training contract, inventory and validation binding | Exact public signature, caller-supplied algorithm/class bindings, parameter compatibility checks and strict evidence reuse | IP2 onward | Proposed below; settle and obtain public-boundary confirmation at Gate 1 |
| Persistence and complete-pipeline compatibility | Native MLflow save/load supports the chosen estimator and fitted preprocessing without broad trust or silent serializer fallback | IP3/IP4 | Native-only feasibility investigation IP1-T2; existing bounded skops choice in [tracking guide](../experiment-tracking.md) is a starting constraint |
| Simple experiment path | No fabricated plan IDs and no changes to strict contracts | Basic-path claims only | Deferred to US-39 AC-01/02; this component example deliberately uses real strict 1.0 inputs/evidence |

### Proposed approach for Gate 1 review

All names and shapes in this subsection are proposals, not delivered APIs.

1. Add `agentic_ml.training.fit_classifier` in proposed `src/agentic_ml/training/__init__.py`. Accept a native DataFrame, partition record, selected columns/output schema, native unfitted preprocessing Pipeline and explicit project-owned algorithm/class bindings. Do not accept an estimator instance; construct the selected class from validated effective parameters. Include an explicit project root and live `CandidateRequest` for this first strict integration. Return a native fitted prediction Pipeline plus plain training/preprocessing metadata. IP1 must finalize the exact signature, error taxonomy and record keys before behavior tests.
2. Make native classifier support extensible through an explicit project-owned mapping from algorithm IDs to native sklearn estimator classes (proposed keyword `estimator_bindings`). The training implementation must not contain an estimator allowlist, algorithm switch or per-estimator adapter required to add another compatible native classifier. Resolve the selected algorithm through the supplied mapping, validate candidate parameters, construct that class with the materialized keyword arguments, and record its fully qualified class identity. Missing or incompatible class bindings and constructor failures must stop before fitting. Metadata never dynamically imports executable code. This is a local argument to the helper, not a persistent plugin registry or discovery service; callers supply trusted code. IP1 finalizes the exact mapping shape and binding checks.
3. Use `DummyClassifier` and `DecisionTreeClassifier` as the primary verified examples, then prove extension with project-supplied `RandomForestClassifier` plus additive declarative parameter metadata, without editing toolkit source, built-in registry resources or rebuilding the toolkit for that addition. Reinvoke existing public candidate validation immediately before fitting; do not trust a caller-fabricated `CandidateResult`. Existing strict evidence must be valid/current. Construct a fresh bound estimator only after validation; compare its complete native `get_params` with materialized fixed/default/search values to catch metadata omissions/default drift, preserving scalar type distinctions, and use public/native validation behavior where available. No dependence on sklearn private `_validate_params` or private parameter constraint structures. Record all effective native defaults, versions and class identity; parameters not represented by the reviewed metadata contract must not silently become tunable. IP1 settles construction/classifier/fit/predict requirements, non-scalar/nested parameter handling, deterministic seed declarations and failure timing. Unsupported parameter encodings or persistence requirements fail explicitly rather than being coerced or silently enabled. Arbitrary custom/third-party estimators and broad persistence certification remain M2 US-16; generic compatibility does not guarantee every sklearn classifier/parameter combination. If existing additive metadata cannot express this extension without validation changes, stop affected work for scope revision instead of adding a closed estimator table.
4. Reuse `fit_preprocessing` for source/membership/train-fit checks. Construct a fresh estimator from validated parameters, fit it on transformed training features/targets only, then compose the already fitted transformer and fitted estimator as a native prediction Pipeline. Do not refit preprocessing on validation/test data or call full-pipeline fit a second time. Preserve caller inputs. Reuse native sklearn operations; keep any shared validation extraction behavior-preserving and regression-covered.
5. Project script uses `run_validated_step` for configured data checks and real strict configuration evidence, trains/records the baseline first, then its authored candidate. Use three-way data for validation comparisons; support fitting with a two-way record without reading its test rows or presenting a validation comparison. No cross-validation or final-test scoring is introduced.
6. Project code owns run creation and baseline-before-candidate order. Use one native MLflow run per fit and a baseline run reference on the candidate. Record validation accuracy with native `accuracy_score`; expose both scores without a new ranking/reporting engine. Require matching data/splits/features/metric for this demonstration. No universal cross-process ordering service is claimed.
7. Save each complete fitted prediction pipeline with native MLflow sklearn persistence; upload via the explicitly selected client and existing run. Record preprocessing through the accepted helper and finalize using `log_run_results`. MLflow is the authoritative run store. Keep a compact training metadata artifact only for fit scope, effective native settings, versions and links that existing provenance does not already supply; do not duplicate data/lock bytes or introduce a second run-state manifest. IP1 settles namespace conflict checks and model-save failure handling.
8. The runnable deliverable is a documented project `train.py`, invoked with the project's installed Python and explicit root from an unrelated cwd. It uses public toolkit imports and native sklearn/MLflow/DVC. No new CLI command, mandatory assistant or initializer change.

### Proposed public test boundaries and numerical oracle

Gate 1 must confirm these boundaries before executable behavior tests are written.
Reuse accepted splitting/preprocessing/tracking boundaries; their historical
confirmation does not confirm the new training boundary automatically.

- **Fitting:** Call proposed `fit_classifier`; inspect native predictions and independently calculated preprocessing effects. Do not mock internal collaborators or assert private call order.
- **Controlled oracle:** IDs 0–7, feature `x = [-3,-1,1,3,-2,2,-100,100]`, labels `[0,0,1,1,0,1,1,0]`; training IDs `[0,1,2,3]`, validation `[4,5]`, test `[6,7]`. StandardScaler training mean is 0, variance 5. Dummy `most_frequent` predicts `[0,0]` on validation, accuracy 0.5. A fixed-seed depth-1 decision tree predicts `[0,1]`, accuracy 1.0. Expected labels/scores come from these declared values, not the implementation under test. Fit same seeds twice and require identical class predictions and effective settings, excluding run IDs/timestamps.
- **Leakage/source cases:** Independent train-only imputation/scaling oracle with held-out extremes and a missing training value; changed source identity, overlapping/missing memberships, ID/target feature inclusion and non-train fit declarations fail. Final test rows never contribute to fit/validation scoring. Input frame, candidate, bindings, validated parameter declarations, preprocessing and record remain unchanged; repeated calls construct independent estimators.
- **Validation:** Public strict planning/configuration/candidate APIs produce genuine evidence. Out-of-bound/fixed/default/type errors and stale evidence fail before estimator construction; missing/non-class/incompatible bindings, constructor errors and parameter coverage/default drift fail before any fitting. Verify pre-fit failure through an observable native fit failure sentinel or equivalent reviewed public behavior; no private-method mock assertions.
- **Recording/persistence:** Query native `MlflowClient`, download the real model and metadata, load with `mlflow.sklearn.load_model` and predict independently declared inference rows. Require exact class labels; use `rtol=1e-12, atol=1e-12` for controlled floating transforms and scalar scores. Numerical round-trip checks here prove this artifact is usable; M2 fresh-project restoration/reproduction remains separate.
- **Failures:** Missing/bad inputs, incompatible prediction shape, serialization/publication failure, artifact collision, missing output despite exit zero and nonzero training process produce actionable context and FAILED where possible, with available local diagnostics preserved. Distinguish process failure, configured-check failure and valid poor quality. No minimum gain is an acceptance condition.
- **Installed boundary:** Same documented script runs on both wheel paths in independent external projects/environments with runtime dependencies only, real Git/DVC and isolated MLflow stores, isolated Python/import-origin checks and unrelated cwd. No neighboring source imports, altered `sys.path`, editable install or fabricated installation provenance.
- **Extensibility:** Define a third binding and metadata for native `RandomForestClassifier` entirely in project fixture code after installing the same toolkit artifact. Run the unchanged public helper, inspect effective parameters/class identity, and save/load/predict through MLflow. Use an explicitly fixed `random_state`, `n_jobs=1` and reviewed forest settings. IP1 establishes a separate independently defined configuration and expected predictions for the forest before behavior tests; the proposed native forest oracle is now specified in the Phase 1 contract and awaits Gate 1 confirmation. Require this case on both wheel paths. Test absent/non-class/incompatible bindings, constructor failure, incomplete parameter metadata, fresh-instance isolation and unsupported parameter encodings. No patch to package source/resources or estimator-specific toolkit branch is allowed to make the third case pass.
- **Limits:** Trusted native estimators only; no custom-object certification, OS holdout isolation, new notebook path, automatic DVC stage execution or scientific-validity certification. Binary controlled oracle plus a multiclass smoke case are required; broader datasets are not implied.

## Plan review

- **Status:** Approved plan; IP1/Gate 1 Approved; IP2 Complete; Gate 2 Approved; IP3 Complete; Gate 3 Approved; IP4 Complete; Gate 4 Approved; M1 classification slice accepted.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve the plan”, 2026-11-15 UTC. Approval includes the extensible estimator design and RandomForestClassifier project-only proof; it does not approve implementation gates or authorize IP1.
- **Requested plan changes:** US-18-SC-01 requires extensible native estimator support; user direction recorded below. Included in the plan approval recorded above.
- Plan review covers the M1 slice and proposed investigation. IP1 finalizes interfaces and test boundaries; Gate 1 must explicitly confirm them before IP2 tests/code. Plan approval alone does not authorize implementation or any later gate.

### Drafting validation — 2026-11-15 UTC

Checked all 32 Markdown links for missing local path targets: none missing
(external URLs and fragment existence are not validated by this path check).
Confirmed four implementation phases and four approval gates, with no task
marked Complete. `git diff --check` and the new-plan whitespace check
`git diff --no-index --check /dev/null docs/plans/milestone-1-us-18.md` pass.
Only this plan and the story checkpoint changed. No executable behavior changed;
TDD/runtime checks are inapplicable to plan drafting and remain pending for
implementation. No feasibility or acceptance result is claimed.

## Scope-change history

### US-18-SC-01 — Extensible native estimators, 2026-11-15 UTC

- **Request and reason:** Developer: “I want estimator support to be extensible.” Additional compatible native sklearn classifiers must be supplied from the experiment project without toolkit source changes.
- **Scope difference:** Replace the proposed closed two-estimator class binding with caller-supplied explicit bindings and generic compatibility/parameter checks. Retain dummy/tree as primary examples; add RandomForestClassifier as an extension proof, including persistence and both installed artifact paths. Custom/third-party estimators remain M2.
- **Impact:** Refines the approach within US-18 AC-01/03/04 and native-component design; no criterion IDs or issue outcomes change. Affects IP1-T1/T2/T3, IP2-T2/T3, IP3-T2, IP4-T1/T2/T3. No completed implementation or runtime evidence exists to invalidate. No new dependency or cross-story implementation is authorized.
- **Plan and requirement revisions:** Updated scope, proposed approach, public boundaries, task completion conditions and final criterion evidence in this plan. GitHub publication is not authorized or required for this within-scope design refinement; no issue acceptance is claimed.
- **Verification and gates:** Preserve all prior checks; add explicit project-only extension coverage and negative binding/compatibility cases. Gate 1 must settle and confirm the extensible contract before tests/code. All gates remain pending.
- **Follow-up direction:** Developer: “for the project-only one use random Forest instead of the GaussianNB”. The project-only proof now uses native `RandomForestClassifier`; dummy/tree primary examples remain unchanged. IP1 must settle deterministic forest settings and its independent oracle.
- **Decision:** Approved direction for this draft revision by the developer messages above; this does not approve the full plan, implementation or a gate.
- **Resume point:** IP1 authorized by “you can use the recommended prompt” on 2026-11-15 UTC and technically completed; Gate 1 approval and IP2 authorization remain pending.


### US-18-SC-02 — Toolkit constructs validated estimators, 2026-11-15 UTC

- **Request and reason:** Developer: “I like this approach better, make the needed changes”, accepting toolkit construction from the selected class and validated parameters to remove redundant caller instance setup.
- **Scope difference:** Remove the `estimator` input. Keep project-owned class bindings and scalar parameter metadata; toolkit validates the candidate, constructs a fresh selected class with complete effective parameters, checks native parameter coverage and classifier compatibility, then fits. No additional parameter overrides or instance/factory callback.
- **Impact:** IP1-T1/T2/T3 were reopened for contract revision and targeted native constructor renewal, then completed with the linked evidence addendum. IP2-T1/T2/T3 and installed IP4-T1/T2 now require constructor/error/coverage/fresh-instance boundaries. Retire caller-instance/class-mismatch and caller-instance-immutability checks; replace them with binding validity, validate-before-construction, complete-parameter construction and fresh-instance isolation. Preserve preprocessing/input immutability, all persistence checks and original evidence. AC IDs/outcomes, milestone, scalar limits and other-story exclusions do not change.
- **Plan and requirement revisions:** This plan, exact classification training contract, IP1 report addendum and checkpoint. No GitHub issue change or product implementation required for this within-scope responsibility refinement.
- **Verification and gates:** Native-only constructor probe reuses frozen parameters and independent predictions for dummy/tree/forest and save/load checks; tests are not product behavior evidence. All earlier failure logs retained. New public test boundaries need Gate 1 confirmation; no implementation gate or story acceptance is inferred.
- **Decision:** Approved contract direction by the developer message above on 2026-11-15 UTC. Gate 1 remains Pending, including persistence review; IP2 remains unauthorized.
- **Resume point:** Revised IP1 artifacts ready for Gate 1 review after constructor probe and document checks.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for execution-time scope changes. New prerequisite work requires its owning
issue's complete discussion, separate plan/task ownership and a coordinated
execution index before dependent implementation.

## US-18 / Implementation Phase 1: Confirm native training and persistence contracts

Technical completion: **Complete**, 2026-11-15 UTC. Gate 1 **Approved**, 2026-11-15 UTC.
Exact proposed signature (revised by US-18-SC-02 for toolkit-owned construction), bindings, scalar restrictions, metadata/errors and
project script outline: [classification training contract](../classification-training.md).
Source, native probe, environment and document-check results:
[IP1 evidence](../verification/us-18-ip1.md). No product code or behavior tests changed.

- **Outcome:** Reviewable exact API/metadata/error contracts and native feasibility findings.
- **Entry conditions:** Met: developer “you can use the recommended prompt”, 2026-11-15 UTC, authorizes the previously supplied start-IP1/stop-at-Gate-1 instruction. Story checkout, issue snapshot and supplier evidence verified. Read [setup](../development/setup.md) before creating the story-local environment; check environment overrides, then `uv sync --locked --group dev`.
- **Acceptance criteria advanced:** US-18-AC-01 (M1), AC-02/03/04; no implementation acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP1-T1 | Complete | Reconcile issue/design and existing validation, preprocessing, splitting and tracking contracts; inspect locked sklearn APIs, caller-supplied bindings and additive registry support | IP1 authorization | Complete proposed inputs/outputs/binding/construction/compatibility/error matrix with no closed estimator table; no unresolved ownership conflict | AC-01–04 |
| US-18-IP1-T2 | Complete | Native-only scratch probes: baseline/tree/RandomForestClassifier fit on declared rows, project-only extension, fitted preprocessing composition, native model save/upload/load/predict, effective parameter encoding, toolkit-owned constructor renewal and deterministic failure case | T1 | Proposed `docs/verification/us-18-ip1.md` records versions, commands, outputs, serializer trust constraints and gaps; no product changes or behavior tests | AC-01/03/04 |
| US-18-IP1-T3 | Complete | Write proposed `docs/classification-training.md` exact contract/runnable script outline; refine this plan's signature, extension recipe, parameter encoding rules, record keys, fixtures and test boundaries | T2 | No unresolved contract decision before IP2; explicit reviewer confirmation requested for boundaries and strict-path scope | AC-01–04 |

### Verification and review evidence

Contract inspection and native probes are feasibility evidence, not passing
toolkit tests. TDD does not apply to IP1 documentation/investigation. Run
`git diff --check`, validate local document links and reconcile all proposal
names with actual exports. Record environment/lock identities and native probe
commands/results. No current-milestone or full-suite run. Exact executable
behavior/failure tests are deferred to IP2/IP3; installed checks to IP4-T1/T2;
all remaining story regressions to IP4-T3. Actual results: **Complete for IP1** — document path/whitespace checks pass; native bounded probe exit 0; original serializer failures retained; unchanged lock and exact commands/limits recorded in [IP1 evidence](../verification/us-18-ip1.md). No pytest or product lint/type checks apply to this contract/investigation phase.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; inventory/validation/persistence feasible; exact public boundaries confirmed; dependencies and strict-path limits explicit.
- **Evidence presented:** [IP1 report](../verification/us-18-ip1.md) and [exact proposed contract](../classification-training.md). US-18-SC-02 removes the estimator argument and requires validate-then-construct; targeted native renewal is recorded in the report addendum. Original tree serializer configuration fails; explicit bounded numpy/tree trust alternative passes native save/load/inference for dummy/tree/forest. Developer approval below confirms this persistence choice and all revised public test boundaries.
- **Remaining limitations or blocked work:** Native feasibility is not toolkit or installed-project verification. Gate 1 approves the exact revised contract and explicit tree-storage trust decision; implementation and installed checks remain pending. Unsupported encodings/classes remain clear failures; no new validation engine, private sklearn validator or broad serializer fallback is proposed.
- **Developer decision:** Approved — exact toolkit-owned construction contract (US-18-SC-02), public test boundaries and explicit `numpy.dtype` / `sklearn.tree._tree.Tree` persistence trust choice.
- **Decision reference and date / requested changes:** Developer “i approve phase 1”, 2026-11-15 UTC; no further changes requested.
- **Progression authorized:** Gate 1 satisfied; await explicit IP2 start authorization. This approval does not authorize a commit or publication.

## US-18 / Implementation Phase 2: Fit validated classifiers on training rows

Technical completion: **Complete**, 2026-11-15 UTC; Gate 2 **Approved**, 2026-11-15 UTC.
Developer “use the suggested prompt” authorized the previously supplied
start-IP2/stop-at-Gate-2 instruction. [IP2 evidence](../verification/us-18-ip2.md)
records the vertical TDD cycles, final 310-case focused/regression pass and
shared checks. Gate 2 subsequently authorized the local commit, completed as
`c74d76b`; IP3 authorization is recorded in its own section below.

- **Outcome:** Native fitted prediction pipelines and effective training metadata through the reviewed public helper.
- **Entry conditions:** Met: Gate 1 approved with revised SC-02 boundaries; IP2 authorized by developer “use the suggested prompt”, 2026-11-15 UTC.
- **Acceptance criteria advanced:** US-18-AC-01 M1, AC-02 baseline fitting, AC-03, AC-04 metadata.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP2-T1 | Complete | First baseline behavior test in proposed `tests/integration/test_training.py`; minimum helper in proposed `src/agentic_ml/training/` | Gate 1 | Recorded red fails for missing behavior; green gives independently expected baseline predictions and leaves caller inputs unchanged, with no caller estimator instance required | AC-01/02/03 |
| US-18-IP2-T2 | Complete | Add one behavior at a time for native classifiers and project-only RandomForestClassifier extension, explicit class bindings, validate-then-construct order, fresh-instance isolation, constructor errors and complete effective/default settings, fixed seeds, fit scope and prediction compatibility | T1 | Toolkit-owned construction/native fitting and preprocessing composition pass independent oracle; invalid/stale candidates fail before construction, constructor/binding/parameter-coverage errors fail before fit; binary/multiclass cases and third estimator supplied without toolkit edits | AC-01/03/04 |
| US-18-IP2-T3 | Complete | Add source/membership/feature/target/type, absent/non-class/incompatible bindings, metadata omissions/native default drift, unsupported parameter encoding and two-way-layout boundary cases; refactor only while green | T2 | Bad inputs fail clearly; two-way training does not use test rows; valid three-way predictions and metadata agree with declared source/splits | AC-01/03/04 |
| US-18-IP2-T4 | Complete | Focused/regression/shared checks; proposed `docs/verification/us-18-ip2.md`, contract and checkpoint updates | T3 | Red/green history, exact coverage/counts, lock identity, changed modules and limitations ready for review | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_configuration_validation.py`.
These cover new fitting plus the reused partition/preprocessing/strict validation
boundaries. Short individual red–green cases may run serially with a recorded
TDD rationale. Shared checks below apply. Public boundaries are those confirmed
at Gate 1. Tracking/persistence is deferred to IP3, installed use to IP4-T1/T2,
unselected M1–6 regressions to IP4-T3. Actual results: **310 passed, zero failures/skips/deselections** in 9.02 seconds; 45 training and 265 existing relevant regression cases, four workers/loadgroup. Shared checks pass, unchanged lock, full red/green and limitations in [IP2 evidence](../verification/us-18-ip2.md).

### Developer approval gate

- **Approval criteria:** T1–T4 complete; supported fits and pre-fit rejections verified; focused/regression/shared checks pass.
- **Evidence presented:** [IP2 report](../verification/us-18-ip2.md), [public contract](../classification-training.md), new `agentic_ml.training.fit_classifier`, 45 new public-interface cases and contributor typing declarations. No suppressions/dependency changes.
- **Remaining limitations:** Full classifier recording and installed verification pending.
- **Developer decision / reference and date / requested changes:** Approved — developer “i approve gate 2; commit”, 2026-11-15 UTC. Local Phase 2 commit authorized; no requested changes.
- **Progression authorized:** Gate 2 satisfied; await explicit IP3 authorization. Commit authorized; push/publication not authorized.

## US-18 / Implementation Phase 3: Record baseline and candidate model runs

Execution authorized by developer “start phase 3”, 2026-11-15 UTC, after
Phase 2 commit `c74d76b`. Initial preflight failed because GitHub CLI had no
authenticated host. Developer “try again” resumed the authorized work; the
complete issue #28 body and one unique comment were successfully retrieved,
with unchanged comment count and updated_at on final metadata refresh. The
authentication blocker is resolved. IP3 is technically Complete; Gate 3 is Approved, 2026-11-15 UTC.
Use the Gate 1-confirmed public boundaries: project execution, native MLflow
run/artifact inspection, fresh native model inference and existing public
quality/validation/fitting/tracking APIs. Normal installed direct/rebuilt final
artifact verification remains IP4; serial individual TDD checks keep each
red–green slice small, with four-worker focused/regression verification at gate.

- **Outcome:** Runnable project script records baseline before candidate, validation scores, complete native models and shared lineage, with truthful failure outcomes.
- **Entry conditions:** Met: Gate 2 approved; developer “start phase 3” authorized IP3; accepted supplier APIs remain available.
- **Acceptance criteria advanced:** US-18-AC-02/03/04 and AC-01 M1.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP3-T1 | Complete | One public integration test at a time in proposed `tests/integration/test_training_tracking.py`; project script fixture; minimal training artifact code in `src/agentic_ml/training/` only if Gate 1 justified a reusable helper | Gate 2 | Real baseline FINISHED before candidate comparison; candidate references baseline run; same rows/features/accuracy; scalar oracle scores 0.5/1.0 and both models inspectable | AC-01/02/03/04 |
| US-18-IP3-T2 | Complete | Native model save/load for primary classifiers and project-only RandomForestClassifier extension, effective parameter/version/class records and accepted tracking helper composition; project fixture uses real committed configuration/code, lock identity and DVC pointers | T1 | Downloaded model predicts declared labels; preprocessing record and source/split lineage match; one authoritative native run per fit | AC-03/04 |
| US-18-IP3-T3 | Complete | Incremental failure tests for native fit/serialization/logging failure, output conflicts, invalid refs and missing output; demonstrate no candidate comparison after failed baseline | T2 | FAILED/context/available diagnostics preserved where possible; poor validation score stays a valid completed experiment; no silent trust or serializer fallback | AC-02/03/04 |
| US-18-IP3-T4 | Complete | Complete runnable `docs/classification-training.md`; focused/shared checks and proposed `docs/verification/us-18-ip3.md`; reconcile API/status references | T3 | Script and product contract agree; no final-test feedback or new basic-path claims | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_tracking.py tests/integration/test_preprocessing.py tests/integration/test_dataset_versioning.py`.
Add `tests/integration/test_configuration_validation.py` if implementation changed
the validation integration since IP2. Inspect real native artifacts and fresh
load/predict outputs, not returned toolkit dictionaries alone. Gate 1 confirms
serialization failure fixtures and numerical tolerances. Shared checks apply.
Installed checks deferred to IP4-T1/T2 and unselected regressions to IP4-T3.
Actual results: **Complete** — 259 focused/regression cases passed in 342.66 seconds, followed by the added literal-guide case passing with four workers in 26.18 seconds. Combined valid evidence covers 260 distinct tests, zero failures/skips/deselections; no single 260-case run is claimed. Shared checks pass after formatting the guide; lock unchanged. Native artifacts, failure/context checks, fixture corrections and exact commands are recorded in [IP3 evidence](../verification/us-18-ip3.md).

### Developer approval gate

- **Approval criteria:** T1–T4 complete; baseline order, metrics, complete artifacts and lineage/failure semantics verified; focused/regression/shared checks pass.
- **Evidence presented:** [IP3 report](../verification/us-18-ip3.md), complete [executable guide](../classification-training.md), project training/binding scripts, 12 public integration cases, native run snapshots and original red/green/failure logs. No package/dependency changes or suppressions.
- **Remaining limitations:** Both installed artifact paths and final M1–6 reconciliation pending.
- **Developer decision / reference and date / requested changes:** Approved — developer “i approve gate 3; commit changes”, 2026-11-15 UTC. Local Phase 3 commit authorized; no requested changes.
- **Progression authorized:** Gate 3 satisfied; await explicit IP4 authorization. Local commit authorized; push/publication not authorized.

## US-18 / Implementation Phase 4: Verify installed classification and accept M1 slice

Execution authorized by developer “start phase 4”, 2026-11-15 UTC, after
Phase 3 commit `f5605d0`. Gate 3 is approved; owning worktree and clean HEAD
verified. Complete issue #28 body and its one unique comment were refreshed;
comment count and updated_at match the final metadata refresh. Public boundaries
remain those confirmed at Gate 1: installed project execution, native artifact/run
inspection and public fitting/validation APIs. No new product behavior is planned;
this phase adds verification of existing behavior on both distribution paths.

- **Outcome:** Same documented script verified outside the source tree on both distribution paths; criterion-mapped final evidence ready for M1-slice acceptance.
- **Entry conditions:** Gate 3 approved and IP4 authorized; final contract and selected serializers unchanged or re-reviewed.
- **Acceptance criteria covered:** US-18-AC-01 classification portion; AC-02/03/04 M1.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP4-T1 | Complete | Proposed `tests/installation/check_training.py`, `training_project.py`, `verify_training.py` and `tests/integration/test_installed_training.py`, reusing existing installation/distribution/evidence support | Gate 3 | Isolated normally installed direct-wheel project runs documented class-binding-only script from unrelated cwd; constructor/parameter-coverage/fresh-instance boundaries verified; native model predictions/metrics/lineage, unchanged-package third-estimator extension and missing/invalid input failure inspected independently | AC-01–04 |
| US-18-IP4-T2 | Complete | Run same assertions against a wheel actually rebuilt from extracted sdist in a separate fresh project/environment | T1 | Project-only third-estimator extension also passes on rebuilt wheel; both artifact identities, runtime dependencies, import locations, CLI version and packaged resource inventories verified; no direct-wheel substitution or source checkout imports | AC-01–04 |
| US-18-IP4-T3 | Complete | Final focused/M1–6/shared checks; reconcile all phase exclusions, failure/skip records, docs, this plan and `CHECKPOINTS.md` in proposed `docs/verification/us-18-ip4.md` | T2 | Final revision/dirty-file/lock/build identities and counts recorded; all required story checks resolved before final gate; regression remains explicitly M2 | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installed_training.py tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_preprocessing_tracking.py`.
The selected installed tests may build artifacts and invoke verification drivers
internally, using the documented pytest-owned workspace/retention rules. Do not
run standalone drivers or broader suite selections without an explicit developer
command. Run final M1–6 and shared commands below before presenting Gate 4.
Record direct/rebuilt installed outputs separately; neither path can substitute
for the other. Actual results: **59 focused/regression cases passed**, zero failures/skips/deselections, in 138.35 seconds. Both installed paths pass all native model, lineage, constructor/fresh-instance/parameter-coverage and failure assertions. Final M1–6: **982 passed, 1 existing skip, zero failures/errors**, 533.52 seconds; 1251 collected, 983 selected, 268 deselected. Shared checks pass; unchanged lock. See [IP4 evidence](../verification/us-18-ip4.md).

### Developer approval gate

- **Approval criteria:** T1–T3 complete; both installed paths, final M1–6 and shared checks pass; AC mapping and every exclusion/failure/skip reconciled.
- **Evidence presented:** [IP4 report](../verification/us-18-ip4.md), both installed artifact paths, 59-case focused pass and final 982 passed / 1 existing skip M1–6 run, shared checks and retained identity/failure/skip reconciliation. IP4-T1/T2/T3 technically Complete, 2026-11-15 UTC; Gate 4 Approved on the same date.
- **Remaining limitations:** AC-01 regression remains M2; no US-39 end-to-end/assistant or milestone acceptance claim.
- **Developer decision / reference and date / requested changes:** Approved — developer “i approve gate 4; commit”, 2026-11-15 UTC. Local Phase 4 commit authorized; no requested changes.
- **Progression authorized:** Gate 4 satisfied. Subsequent developer M1-slice acceptance authorizes publication as recorded below.

## Shared checks and execution rules

Every executable phase gate retains locked sync, lock check, lint, formatting,
strict typing, smoke and whitespace checks from [development](../development.md):

```sh
sha256sum uv.lock
uv sync --locked --group dev
uv lock --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked agentic-ml --version
git diff --check
sha256sum uv.lock
```

Expected: all pass, CLI version matches installed metadata and lock SHA-256
unchanged unless an intentional dependency change has been reviewed. Actual:
**Pass** at IP4: locked sync/lock check, Ruff lint/format, strict mypy (99 files), CLI `0.1.0`, whitespace; unchanged lock SHA-256 recorded in [IP4 evidence](../verification/us-18-ip4.md). Runtime dependency changes are not currently proposed. Read the
[distribution guide](../development/distribution.md) before any such change.
No suppression/check exclusion is planned; justify and obtain required direction
for any workaround to an existing failure.

Use small vertical red–green cycles: one behavior test, run and establish the
intended failure, minimum code, then relevant regressions; repeat. Do not batch
all tests before implementation. Tests directly verifying M1 get `milestone_1`;
classify contributor-only tooling as infrastructure. Retain four-worker
`loadgroup` phase checks and existing timeouts/skips/scheduling groups.

Record commands, cwd, counts, platform, versions, original failures and actual
results in phase reports; retain raw evidence under `.dev-records/verification/`
per [records policy](../development/records.md). Durable records must survive
pytest cleanup. Mark tasks Complete only after their work and checks pass;
reopen invalidated tasks and renew evidence. Do not reuse another story's Python
environment or import its checkout.

Stop at every implementation phase gate, including the final gate. Present
changes, task status, evidence, deviations and limits; await explicit developer
approval and authority for the next implementation phase. Silence and plan
approval do not approve gates. Preserve historical supplier approvals.

Apply the repository three-attempt problem limit: track hypothesis, corrective
change and verification for each attempt; after the third failed correction,
stop that problem, preserve original tests/criteria and diagnostics, and request
developer direction. Do not weaken assertions, disable checks or conceal failure.
Scope changes use the linked manage-plan-scope procedure before dependent work.

## Final verification requirements

- **Owning final phase/task:** US-18-IP4-T3, before Gate 4 and M1-slice acceptance.
- **Final implementation identity:** `f5605d0` plus the seven IP4 verification/document files recorded in [IP4 evidence](../verification/us-18-ip4.md); retained manifests give exact file, lock, direct/sdist/rebuilt hashes and separate project/environment/committed fixture identities.
- **M1–6:** `uv run --locked pytest -n 4 --dist=loadgroup` against final story inputs; renew after executable changes. Record collected/selected/deselected/passed/failed/skipped counts and the three existing temporary skip qualifications. Passing CI is not local verification evidence.
- **Shared checks:** Commands above; all required before final gate.
- **Distribution/installation:** IP4-T1/T2 selected tests cover both normal installed artifact paths, public training/persistence, CLI/import/resources and runtime-only dependencies. Standalone artifact verification and broader local pytest require explicit developer commands.
- **Deferred-check reconciliation:** IP4-T3 owns every earlier phase's excluded story regression and installed check. Required US-18 coverage cannot remain deferred at its acceptance gate. Preserve unrelated historical milestone obligations.
- **Actual results and limitations:** IP4 final M1–6 982 passed / 1 existing skip, zero failures/errors; 59 focused passed; shared checks pass, unchanged lock. Linux aarch64 / Python 3.12.16 observed; macOS/Windows not verified. The unchanged missing-planning-schema M1 skip and two deselected M50 skips retain their existing owners; historical milestone obligations remain open.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-18-AC-01 classification | IP1-T1/T2/T3; IP2-T1/T2/T3/T4; IP3-T1/T4; IP4-T1/T2/T3 | Native baseline/real classifier, binary oracle and multiclass case, installed matrix | M1 accepted; regression deferred to M2 |
| US-18-AC-02 | IP1-T3; IP2-T1; IP3-T1/T3/T4; IP4-T1/T2/T3 | Reproducible baseline recorded before candidate comparison; failed baseline prevents comparison | Accepted M1 |
| US-18-AC-03 | IP1-T2/T3; IP2-T1/T2/T3/T4; IP3-T2/T3; IP4-T1/T2/T3 | Native pipeline fit/predict/save/load, independent predictions, train-only oracle, project-only third-estimator extension on both wheel paths and failure cases | Accepted M1 |
| US-18-AC-04 | IP1-T1/T2/T3; IP2-T2/T3/T4; IP3-T1/T2/T3/T4; IP4-T1/T2/T3 | Native MLflow parameters/metrics/models, effective defaults/library versions and committed feature/data/environment references | Accepted M1 |

- **Remaining work:** M2 regression AC-01; other stories retain their own integration, tuning, final testing and reproduction obligations.
- **Partial prerequisite delivery:** This provides classification training to later feature/search/basic-path work; it does not accept US-05 training integration generally, US-14, US-20, US-21, US-24, US-27 or US-39.
- **Final verification:** Complete US-18-IP4-T3; [IP4 report](../verification/us-18-ip4.md). Gate 4 Approved; M1 classification slice accepted.
- **Developer M1-slice acceptance / decision reference and date:** Accepted — developer “i accept us-18 m1 classification slice”, 2026-11-15 UTC. All four gates approved. Authorizes accepted-slice commit, push, PR and static COMMENT review through execute-plan; merge and cleanup are not authorized. Keep issue #28 open for M2 regression.

## Milestone acceptance handoff

- **Owner:** `MVP-M1-ACCEPT-VERIFY`; later regression to `MVP-M2-ACCEPT-VERIFY`.
- **Deferred checks:** Full revised-MVP integration and assistant/native-stage demonstrations; platform/manual and historical M1/M50 reconciliation remain with their owners in [CHECKPOINTS](../../CHECKPOINTS.md). This plan closes none of them automatically.
- **Required evidence:** Reconcile final story evidence and every remaining milestone deferral. Complete-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, standalone direct/rebuilt distribution and installation checks run only on explicit developer command, with shared checks and final identity/platform qualifications. A milestone approval does not silently launch broader checks.

## Accepted-slice publication

M1 classification accepted on 2026-11-15 UTC; see [publication record](../verification/us-18-publication.md). Issue #28 stays open for M2 regression.
