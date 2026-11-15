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

1. Add `agentic_ml.training.fit_classifier` in proposed `src/agentic_ml/training/__init__.py`. Accept a native DataFrame, partition record, selected columns/output schema, native unfitted preprocessing Pipeline and native estimator and explicit project-owned algorithm/class bindings. Include an explicit project root and live `CandidateRequest` for this first strict integration. Return a native fitted prediction Pipeline plus plain training/preprocessing metadata. IP1 must finalize the exact signature, error taxonomy and record keys before behavior tests.
2. Make native classifier support extensible through caller-supplied estimator objects and an explicit project-owned mapping from algorithm IDs to native sklearn estimator classes (proposed keyword `estimator_bindings`). The training implementation must not contain an estimator allowlist, algorithm switch or per-estimator adapter required to add another compatible native classifier. Resolve the selected algorithm through the supplied mapping, verify the supplied estimator has exactly the declared class, and record its fully qualified class identity. Metadata never dynamically imports executable code. This is a local argument to the helper, not a persistent plugin registry or discovery service; callers supply trusted code. IP1 finalizes the exact mapping shape and binding checks.
3. Use `DummyClassifier` and `DecisionTreeClassifier` as the primary verified examples, then prove extension with project-supplied `RandomForestClassifier` plus additive declarative parameter metadata, without editing toolkit source, built-in registry resources or rebuilding the toolkit for that addition. Reinvoke existing public candidate validation immediately before fitting; do not trust a caller-fabricated `CandidateResult`. Existing strict evidence must be valid/current. Compare the estimator's native `get_params` with materialized fixed/default/search values, preserving scalar type distinctions, and use public/native validation behavior where available. No dependence on sklearn private `_validate_params` or private parameter constraint structures. Record all effective native defaults, versions and class identity; parameters not represented by the reviewed metadata contract must not silently become tunable. IP1 settles clone/classifier/fit/predict requirements, non-scalar/nested parameter handling, deterministic seed declarations and failure timing. Unsupported parameter encodings or persistence requirements fail explicitly rather than being coerced or silently enabled. Arbitrary custom/third-party estimators and broad persistence certification remain M2 US-16; generic compatibility does not guarantee every sklearn classifier/parameter combination. If existing additive metadata cannot express this extension without validation changes, stop affected work for scope revision instead of adding a closed estimator table.
4. Reuse `fit_preprocessing` for source/membership/train-fit checks. Clone estimator inputs, fit the estimator on transformed training features/targets only, then compose the already fitted transformer and fitted estimator as a native prediction Pipeline. Do not refit preprocessing on validation/test data or call full-pipeline fit a second time. Preserve caller inputs. Reuse native sklearn operations; keep any shared validation extraction behavior-preserving and regression-covered.
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
- **Leakage/source cases:** Independent train-only imputation/scaling oracle with held-out extremes and a missing training value; changed source identity, overlapping/missing memberships, ID/target feature inclusion and non-train fit declarations fail. Final test rows never contribute to fit/validation scoring. Input frame, estimator, preprocessing and record remain unchanged.
- **Validation:** Public strict planning/configuration/candidate APIs produce genuine evidence. Out-of-bound/fixed/default/type/class mismatch and stale evidence fail before native fit. Verify pre-fit failure through an observable native fit failure sentinel or equivalent reviewed public behavior; no private-method mock assertions.
- **Recording/persistence:** Query native `MlflowClient`, download the real model and metadata, load with `mlflow.sklearn.load_model` and predict independently declared inference rows. Require exact class labels; use `rtol=1e-12, atol=1e-12` for controlled floating transforms and scalar scores. Numerical round-trip checks here prove this artifact is usable; M2 fresh-project restoration/reproduction remains separate.
- **Failures:** Missing/bad inputs, incompatible prediction shape, serialization/publication failure, artifact collision, missing output despite exit zero and nonzero training process produce actionable context and FAILED where possible, with available local diagnostics preserved. Distinguish process failure, configured-check failure and valid poor quality. No minimum gain is an acceptance condition.
- **Installed boundary:** Same documented script runs on both wheel paths in independent external projects/environments with runtime dependencies only, real Git/DVC and isolated MLflow stores, isolated Python/import-origin checks and unrelated cwd. No neighboring source imports, altered `sys.path`, editable install or fabricated installation provenance.
- **Extensibility:** Define a third binding and metadata for native `RandomForestClassifier` entirely in project fixture code after installing the same toolkit artifact. Run the unchanged public helper, inspect effective parameters/class identity, and save/load/predict through MLflow. Use an explicitly fixed `random_state`, `n_jobs=1` and reviewed forest settings. IP1 must establish a separate independently defined fixture and expected predictions for the forest before behavior tests; do not assume the depth-1 tree oracle applies to a bootstrapped ensemble. Require this case on both wheel paths. Test absent/mismatched binding, incompatible estimator and unsupported parameter encodings. No patch to package source/resources or estimator-specific toolkit branch is allowed to make the third case pass.
- **Limits:** Trusted native estimators only; no custom-object certification, OS holdout isolation, new notebook path, automatic DVC stage execution or scientific-validity certification. Binary controlled oracle plus a multiclass smoke case are required; broader datasets are not implied.

## Plan review

- **Status:** Approved plan; implementation not yet authorized.
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
- **Resume point:** Plan approved on 2026-11-15 UTC; separate IP1 authorization remains pending.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for execution-time scope changes. New prerequisite work requires its owning
issue's complete discussion, separate plan/task ownership and a coordinated
execution index before dependent implementation.

## US-18 / Implementation Phase 1: Confirm native training and persistence contracts

- **Outcome:** Reviewable exact API/metadata/error contracts and native feasibility findings.
- **Entry conditions:** Developer authorizes IP1; verify story checkout, issue snapshot and supplier evidence. Read [setup](../development/setup.md) before creating the story-local environment; check environment overrides, then `uv sync --locked --group dev`.
- **Acceptance criteria advanced:** US-18-AC-01 (M1), AC-02/03/04; no implementation acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP1-T1 | Not started | Reconcile issue/design and existing validation, preprocessing, splitting and tracking contracts; inspect locked sklearn APIs, caller-supplied bindings and additive registry support | IP1 authorization | Complete proposed inputs/outputs/binding/compatibility/error matrix with no closed estimator table; no unresolved ownership conflict | AC-01–04 |
| US-18-IP1-T2 | Not started | Native-only scratch probes: baseline/tree/RandomForestClassifier fit on declared rows, project-only extension, fitted preprocessing composition, native model save/upload/load/predict, effective parameter encoding and deterministic failure case | T1 | Proposed `docs/verification/us-18-ip1.md` records versions, commands, outputs, serializer trust constraints and gaps; no product changes or behavior tests | AC-01/03/04 |
| US-18-IP1-T3 | Not started | Write proposed `docs/classification-training.md` exact contract/runnable script outline; refine this plan's signature, extension recipe, parameter encoding rules, record keys, fixtures and test boundaries | T2 | No unresolved contract decision before IP2; explicit reviewer confirmation requested for boundaries and strict-path scope | AC-01–04 |

### Verification and review evidence

Contract inspection and native probes are feasibility evidence, not passing
toolkit tests. TDD does not apply to IP1 documentation/investigation. Run
`git diff --check`, validate local document links and reconcile all proposal
names with actual exports. Record environment/lock identities and native probe
commands/results. No current-milestone or full-suite run. Exact executable
behavior/failure tests are deferred to IP2/IP3; installed checks to IP4-T1/T2;
all remaining story regressions to IP4-T3. Actual results: **Pending**.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; inventory/validation/persistence feasible; exact public boundaries confirmed; dependencies and strict-path limits explicit.
- **Evidence presented:** Pending `docs/verification/us-18-ip1.md` and contract.
- **Remaining limitations or blocked work:** Any unresolved feasibility decision blocks IP2 and requires plan refinement/review.
- **Developer decision:** Pending.
- **Decision reference and date / requested changes:** Pending.
- **Progression authorized:** Pending — stop for approval and IP2 authorization.

## US-18 / Implementation Phase 2: Fit validated classifiers on training rows

- **Outcome:** Native fitted prediction pipelines and effective training metadata through the reviewed public helper.
- **Entry conditions:** Gate 1 approved, boundaries explicitly confirmed and IP2 authorized.
- **Acceptance criteria advanced:** US-18-AC-01 M1, AC-02 baseline fitting, AC-03, AC-04 metadata.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP2-T1 | Not started | First baseline behavior test in proposed `tests/integration/test_training.py`; minimum helper in proposed `src/agentic_ml/training/` | Gate 1 | Recorded red fails for missing behavior; green gives independently expected baseline predictions and leaves caller inputs unchanged | AC-01/02/03 |
| US-18-IP2-T2 | Not started | Add one behavior at a time for native classifiers and project-only RandomForestClassifier extension, explicit class bindings, strict candidate checks, effective/default settings, fixed seeds, fit scope and prediction compatibility | T1 | Clone/native fitting and preprocessing composition pass independent oracle; invalid or stale candidates and class mismatches fail before fit; binary/multiclass cases and third estimator supplied without toolkit edits | AC-01/03/04 |
| US-18-IP2-T3 | Not started | Add source/membership/feature/target/type, absent/mismatched bindings, incompatible estimators, unsupported parameter encoding and two-way-layout boundary cases; refactor only while green | T2 | Bad inputs fail clearly; two-way training does not use test rows; valid three-way predictions and metadata agree with declared source/splits | AC-01/03/04 |
| US-18-IP2-T4 | Not started | Focused/regression/shared checks; proposed `docs/verification/us-18-ip2.md`, contract and checkpoint updates | T3 | Red/green history, exact coverage/counts, lock identity, changed modules and limitations ready for review | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_configuration_validation.py`.
These cover new fitting plus the reused partition/preprocessing/strict validation
boundaries. Short individual red–green cases may run serially with a recorded
TDD rationale. Shared checks below apply. Public boundaries are those confirmed
at Gate 1. Tracking/persistence is deferred to IP3, installed use to IP4-T1/T2,
unselected M1–6 regressions to IP4-T3. Actual results: **Pending**.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; supported fits and pre-fit rejections verified; focused/regression/shared checks pass.
- **Evidence presented:** Pending `docs/verification/us-18-ip2.md`.
- **Remaining limitations:** Full classifier recording and installed verification pending.
- **Developer decision / reference and date / requested changes:** Pending.
- **Progression authorized:** Pending — stop for approval and IP3 authorization.

## US-18 / Implementation Phase 3: Record baseline and candidate model runs

- **Outcome:** Runnable project script records baseline before candidate, validation scores, complete native models and shared lineage, with truthful failure outcomes.
- **Entry conditions:** Gate 2 approved and IP3 authorized; accepted supplier APIs remain available.
- **Acceptance criteria advanced:** US-18-AC-02/03/04 and AC-01 M1.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP3-T1 | Not started | One public integration test at a time in proposed `tests/integration/test_training_tracking.py`; project script fixture; minimal training artifact code in `src/agentic_ml/training/` only if Gate 1 justified a reusable helper | Gate 2 | Real baseline FINISHED before candidate comparison; candidate references baseline run; same rows/features/accuracy; scalar oracle scores 0.5/1.0 and both models inspectable | AC-01/02/03/04 |
| US-18-IP3-T2 | Not started | Native model save/load for primary classifiers and project-only RandomForestClassifier extension, effective parameter/version/class records and accepted tracking helper composition; project fixture uses real committed configuration/code, lock identity and DVC pointers | T1 | Downloaded model predicts declared labels; preprocessing record and source/split lineage match; one authoritative native run per fit | AC-03/04 |
| US-18-IP3-T3 | Not started | Incremental failure tests for native fit/serialization/logging failure, output conflicts, invalid refs and missing output; demonstrate no candidate comparison after failed baseline | T2 | FAILED/context/available diagnostics preserved where possible; poor validation score stays a valid completed experiment; no silent trust or serializer fallback | AC-02/03/04 |
| US-18-IP3-T4 | Not started | Complete runnable `docs/classification-training.md`; focused/shared checks and proposed `docs/verification/us-18-ip3.md`; reconcile API/status references | T3 | Script and product contract agree; no final-test feedback or new basic-path claims | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_tracking.py tests/integration/test_preprocessing.py tests/integration/test_dataset_versioning.py`.
Add `tests/integration/test_configuration_validation.py` if implementation changed
the validation integration since IP2. Inspect real native artifacts and fresh
load/predict outputs, not returned toolkit dictionaries alone. Gate 1 confirms
serialization failure fixtures and numerical tolerances. Shared checks apply.
Installed checks deferred to IP4-T1/T2 and unselected regressions to IP4-T3.
Actual results: **Pending**.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; baseline order, metrics, complete artifacts and lineage/failure semantics verified; focused/regression/shared checks pass.
- **Evidence presented:** Pending `docs/verification/us-18-ip3.md`.
- **Remaining limitations:** Both installed artifact paths and final M1–6 reconciliation pending.
- **Developer decision / reference and date / requested changes:** Pending.
- **Progression authorized:** Pending — stop for approval and IP4 authorization.

## US-18 / Implementation Phase 4: Verify installed classification and accept M1 slice

- **Outcome:** Same documented script verified outside the source tree on both distribution paths; criterion-mapped final evidence ready for M1-slice acceptance.
- **Entry conditions:** Gate 3 approved and IP4 authorized; final contract and selected serializers unchanged or re-reviewed.
- **Acceptance criteria covered:** US-18-AC-01 classification portion; AC-02/03/04 M1.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-18-IP4-T1 | Not started | Proposed `tests/installation/check_training.py`, `training_project.py`, `verify_training.py` and `tests/integration/test_installed_training.py`, reusing existing installation/distribution/evidence support | Gate 3 | Isolated normally installed direct-wheel project runs documented script from unrelated cwd; native model predictions/metrics/lineage, unchanged-package third-estimator extension and missing/invalid input failure inspected independently | AC-01–04 |
| US-18-IP4-T2 | Not started | Run same assertions against a wheel actually rebuilt from extracted sdist in a separate fresh project/environment | T1 | Project-only third-estimator extension also passes on rebuilt wheel; both artifact identities, runtime dependencies, import locations, CLI version and packaged resource inventories verified; no direct-wheel substitution or source checkout imports | AC-01–04 |
| US-18-IP4-T3 | Not started | Final focused/M1–6/shared checks; reconcile all phase exclusions, failure/skip records, docs, this plan and `CHECKPOINTS.md` in proposed `docs/verification/us-18-ip4.md` | T2 | Final revision/dirty-file/lock/build identities and counts recorded; all required story checks resolved before final gate; regression remains explicitly M2 | AC-01–04 |

### Verification and review evidence

Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installed_training.py tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_preprocessing_tracking.py`.
The selected installed tests may build artifacts and invoke verification drivers
internally, using the documented pytest-owned workspace/retention rules. Do not
run standalone drivers or broader suite selections without an explicit developer
command. Run final M1–6 and shared commands below before presenting Gate 4.
Record direct/rebuilt installed outputs separately; neither path can substitute
for the other. Actual results: **Pending**.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; both installed paths, final M1–6 and shared checks pass; AC mapping and every exclusion/failure/skip reconciled.
- **Evidence presented:** Pending `docs/verification/us-18-ip4.md`.
- **Remaining limitations:** AC-01 regression remains M2; no US-39 end-to-end/assistant or milestone acceptance claim.
- **Developer decision / reference and date / requested changes:** Pending.
- **Progression authorized:** Pending — stop at final gate. Request explicit M1-slice acceptance separately or in the same explicit decision. Publication is outside this planning request.

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
**Pending**. Runtime dependency changes are not currently proposed. Read the
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
- **Final implementation identity:** Pending revision, exact dirty files, lock hash and direct/sdist/rebuilt artifact hashes; identify installed project/environment and committed fixture references separately.
- **M1–6:** `uv run --locked pytest -n 4 --dist=loadgroup` against final story inputs; renew after executable changes. Record collected/selected/deselected/passed/failed/skipped counts and the three existing temporary skip qualifications. Passing CI is not local verification evidence.
- **Shared checks:** Commands above; all required before final gate.
- **Distribution/installation:** IP4-T1/T2 selected tests cover both normal installed artifact paths, public training/persistence, CLI/import/resources and runtime-only dependencies. Standalone artifact verification and broader local pytest require explicit developer commands.
- **Deferred-check reconciliation:** IP4-T3 owns every earlier phase's excluded story regression and installed check. Required US-18 coverage cannot remain deferred at its acceptance gate. Preserve unrelated historical milestone obligations.
- **Actual results and limitations:** Pending. No tests or native feasibility probes were run during plan drafting; no Linux/macOS/Windows runtime support is newly verified.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-18-AC-01 classification | IP1-T1/T2/T3; IP2-T1/T2/T3/T4; IP3-T1/T4; IP4-T1/T2/T3 | Native baseline/real classifier, binary oracle and multiclass case, installed matrix | Pending M1 portion; regression deferred to M2 |
| US-18-AC-02 | IP1-T3; IP2-T1; IP3-T1/T3/T4; IP4-T1/T2/T3 | Reproducible baseline recorded before candidate comparison; failed baseline prevents comparison | Pending |
| US-18-AC-03 | IP1-T2/T3; IP2-T1/T2/T3/T4; IP3-T2/T3; IP4-T1/T2/T3 | Native pipeline fit/predict/save/load, independent predictions, train-only oracle, project-only third-estimator extension on both wheel paths and failure cases | Pending |
| US-18-AC-04 | IP1-T1/T2/T3; IP2-T2/T3/T4; IP3-T1/T2/T3/T4; IP4-T1/T2/T3 | Native MLflow parameters/metrics/models, effective defaults/library versions and committed feature/data/environment references | Pending |

- **Remaining work:** M2 regression AC-01; other stories retain their own integration, tuning, final testing and reproduction obligations.
- **Partial prerequisite delivery:** This provides classification training to later feature/search/basic-path work; it does not accept US-05 training integration generally, US-14, US-20, US-21, US-24, US-27 or US-39.
- **Final verification:** Pending US-18-IP4-T3.
- **Developer M1-slice acceptance / decision reference and date:** Pending. Keep issue #28 open for regression.

## Milestone acceptance handoff

- **Owner:** `MVP-M1-ACCEPT-VERIFY`; later regression to `MVP-M2-ACCEPT-VERIFY`.
- **Deferred checks:** Full revised-MVP integration and assistant/native-stage demonstrations; platform/manual and historical M1/M50 reconciliation remain with their owners in [CHECKPOINTS](../../CHECKPOINTS.md). This plan closes none of them automatically.
- **Required evidence:** Reconcile final story evidence and every remaining milestone deferral. Complete-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, standalone direct/rebuilt distribution and installation checks run only on explicit developer command, with shared checks and final identity/platform qualifications. A milestone approval does not silently launch broader checks.
