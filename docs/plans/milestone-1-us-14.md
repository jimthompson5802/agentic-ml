# Milestone 1 / US-14: Build and compare authored feature pipelines

## Scope and outcome

- **Milestone:** M1 — Complete one local classification experiment.
- **User story:** [US-14](../specs/user-stories.md#us-14-build-and-compare-authored-feature-pipelines), [GitHub issue #20](https://github.com/jimthompson5802/agentic-ml/issues/20).
- **User-visible outcome:** A separate experiment project executes explicitly authored native feature pipelines, records their outputs and lineage, and reports validation gains, ties or regressions against a named reference using identical data/splits, classifier settings and metric.
- **Acceptance criteria covered:** US-14-AC-01–05, all assigned to M1. The completion table below preserves their meanings.
- **Scope boundaries:** Native pandas/scikit-learn features and CPU classification through accepted strict APIs; native MLflow records and DVC data pointers. No new basic-run CLI, search, automatic feature generation, final-test evaluation, mandatory experiment approval, custom transformer registry, assistant demonstration, native stage scheduler or clean-project replay. US-20/21/24/27/39/40 retain those outcomes; M2 custom-component/restoration work is not activated.
- **Supporting design:** [Data/features](../specs/design/data-and-features.md#authored-feature-pipelines), [interfaces](../specs/design/interfaces-and-configuration.md), [execution/tracking](../specs/design/execution-and-governance.md), [capability order](../specs/design/milestone-delivery.md), [traceability](../specs/design/acceptance-traceability.md), [ADR-008](../specs/design/architecture-decisions.md#adr-008--local-experiment-mvp-and-externally-owned-assistant-use).
- **Coordinated execution index:** None. All supplying capabilities are already on the base; no prerequisite story implementation is proposed.

## Workspace association

- **GitHub issue and story:** #20 / US-14 (these are different identifiers).
- **Branch:** `US-14-feature-pipelines`.
- **Base ref and starting commit:** Local `main`, `9a030cfe5d6523531e386b0195f40a16599180fc`.
- **Worktree:** `.worktrees/US-14-feature-pipelines`, relative to the primary checkout.

Created for planning on 2026-11-15 UTC. Local main was used without fetching;
remote synchronization is not claimed. Follow [worktree guidance](../development/worktrees.md).
No environment was provisioned and no implementation was started.

## Source snapshot and current state

Retrieved #20's complete body and its one unique comment, then refreshed metadata:
comment count and `updated_at = 2026-11-07T00:28:59Z` were unchanged. GitHub's
milestone field is null; the issue body assigns all five criteria to M1.
[Comment 6699589877](https://github.com/jimthompson5802/agentic-ml/issues/20#issuecomment-6699589877)
preserves MVP-SC-01/MVP-SC-02: scope approval is not implementation acceptance.
Also retrieved complete bodies/all comments and stable metadata refreshes for
prerequisites #19 (1), #16 (1), #21 (2), #28 (1), and #17 (2).
Complete JSON snapshots, including metadata, authors, timestamps and comment URLs,
are retained locally under `.dev-records/planning/us-14/issue-<number>.json`.
Issue checkboxes lag accepted local plans; use the cited decisions/evidence rather
than claiming a newly completed criterion from issue text alone.

Existing implemented interfaces inspected:

- `agentic_ml.splitting.create_partitions`: native split reconstruction, membership validation and source identity; project owns JSON persistence.
- `agentic_ml.preprocessing.fit_preprocessing`: native clone/train-only fit, declared schema validation and finite JSON metadata, including ordered steps/parameters/columns and versions.
- `agentic_ml.training.fit_classifier`: real strict candidate validation, fresh native classifier construction, training-only preprocessing/classifier fit and a native prediction Pipeline plus training record. It does not score validation or test rows.
- `agentic_ml.tracking.log_preprocessing` and `log_run_results`: existing native-run artifact publication, shared provenance, output checks, metrics/status recording. Metrics are supplied, not computed by these helpers.
- [Classification guide](../classification-training.md) and `tests/installation/training_project.py`: runnable project-owned fit/score/save/log recipe. It changes algorithms between candidates, so its evidence does not establish controlled feature comparison.
- [Native DVC recipe](../dataset-versioning.md): version source/split/derived outputs without a second dataset identity service.

The active design's broad implementation-status paragraphs predate accepted
US-15/18/26 delivery. Concrete code, owning plans and final evidence establish
the capabilities above. Refresh only affected status/traceability when US-14 is
verified; do not rewrite historical decisions.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Recorded source/splits, #19 | Full original three-way record and source identity, ordered disjoint memberships | IP2 fitting/comparison | Available: [US-12-19-IP3-T1–T3 / IP4-T1–T4](milestone-1-us-12-assessment-splits.md), Gates 1–4 and acceptance; [final evidence](../verification/us-12-19-ip4.md). Revalidate current inputs. |
| Native DVC data, #16 | Source/split/derived-data pointers, excluded content, committed metadata | IP2 lineage | Available: [US-13-IP3-T1–T3](milestone-1-us-13.md), Gate 3 and M1 acceptance; [evidence](../verification/us-13-ip3.md). No M2 restore prerequisite. |
| Train-only preprocessing, #21 | Native fitted pipeline, original metadata/schema retained | IP2 variants | Available: [US-15-IP3-T1/T2 and IP4](milestone-1-us-15.md), Gates 1–4 and M1 acceptance; [evidence](../verification/us-15-ip4.md). |
| Classification, #28 | Fixed native class/effective scalar settings, genuine strict validation and fresh instances | IP2 fit/score | Available: [US-18-IP4-T1–T3](milestone-1-us-18.md), Gates 1–4 and M1 classification acceptance; [evidence](../verification/us-18-ip4.md). No regression prerequisite. |
| MLflow recording, #17 | Preserve preprocessing, supplied metrics/outputs and committed data/code/config/lock/toolkit references | IP2 publication | Available: [US-26-IP4-T1–T3](milestone-1-us-26-recording.md), Gate 4 and #17 acceptance; [evidence](../verification/us-26-recording-ip4.md). No #33/#43 work required. |
| Issue workflow wording conflicts with newer policy | Reconcile #20's old per-phase manual gates/current-milestone runs with the 2026-11-15 contract-review policy and current focused verification policy | Product implementation | Resolved on 2026-11-15 by developer request “can you update the issue for consistency”; issue body updated and reread successfully. This draft follows [phase approvals](../development/phase-approvals.md) and [verification](../development/verification.md#phase-and-story-verification). The issue now matches these policies. Acceptance criteria and existing comments were preserved. This resolves only policy synchronization, not plan approval or execution authorization. |
| Recipe versus new toolkit helper | Demonstrate native/accepted APIs suffice; identify a concrete gap before proposing another wrapper | IP2 | Proposed native project recipe below. IP1 settles contract; any new toolkit API requires revised plan and contract review before code/tests. |
| Public comparison boundary | Exact invocation, candidate declaration, artifact fields, tie/error semantics and independent fixture expectations | IP2 | Approved contract v2 and public boundaries, developer “yes i approve contract v2”, 2026-11-15 UTC; installed verification is complete in IP3. |

## Proposed technical approach and public boundaries

Deliver a copyable project-owned recipe in proposed `examples/feature-comparison/`
with `compare_features.py`, `feature_variants.py` and a README; document it in
proposed `docs/feature-pipelines.md`. The implementation lives in the experiment
project after copying; imports use the installed toolkit and native libraries.
Reusable fit/validation/tracking behavior stays in the existing installable
package. No new toolkit feature wrapper, run store or FeaturePlan language is
currently justified. Keep a single authoritative recipe source; tests copy and
execute those exact files rather than maintaining a second implementation.

Proposed invocation after installing the toolkit and preparing genuine strict
1.0 configuration/validation inputs:

```sh
/absolute/project/.venv/bin/python /absolute/project/compare_features.py \
  --project-root /absolute/project --tracking-uri sqlite:////absolute/project/mlflow.db \
  --experiment-id EXPLICIT_NATIVE_ID --settings comparison-settings.json
```

Paths in settings resolve against explicit root, independently of caller cwd.
The recipe must include complete preparation instructions; never fabricate a
plan/validation ID or claim initializer drafts are runnable strict inputs.
Reuse reviewed static project estimator profiles and bindings from US-18's
pattern, including every native scalar default. Project configuration supplies
one classifier/candidate and integer seed. A named baseline feature variant is
executed and recorded first, using that same classifier as all later variants.
It is a feature reference, not a switch from dummy to tree classification.

Explicit project code declares each named native Pipeline, ordered selected
columns and declared output schema. Use native Pipeline/ColumnTransformer,
StandardScaler, SimpleImputer and OneHotEncoder within the accepted M1 metadata
encoding; no dynamic imports from serialized class names, callable metadata
capture, arbitrary custom components or inferred feature candidates.

Load one current source and original three-way split record. Validate settings,
nonempty unique variant names, baseline membership, supported metric/direction,
expected output declarations and separate validation availability before fitting.
Run configured quality checks through `run_validated_step`. Fit each supplied
variant independently with `fit_classifier`, using the same CandidateRequest,
estimator binding/effective parameters, source and partition record. Native
validation metrics score only validation predictions. Reuse accepted MLflow
model save/upload and bounded skops trust choices; never broaden trust on error.

Propose native `accuracy_score` with maximize and `zero_one_loss` with minimize
as the initial explicit metric pairs. Reject unknown/contradictory pairs and
nonfinite scores. Compare candidate minus reference for maximize and reference
minus candidate for minimize: positive = gain, zero = tie, negative = regression.
Propose exact equality for a tie in this controlled M1 recipe; no silent epsilon
or quality threshold. IP1 must settle these choices before dependent tests.
Do not introduce a general evaluation API owned by US-21.

Each variant retains its unmodified training/preprocessing records. Save named
train/validation feature outputs with their ordered row IDs, schemas and
project-declared columns, using ordinary project persistence. Version derived
content with native DVC as introduced; preserve source/split DVC links separately
from the preprocessing source SHA-256. Do not predict, transform or score final
test rows as part of this comparison workflow.

One native MLflow run per variant owns its model/preprocessing artifacts,
effective parameters, validation metrics, training record and output references.
Log committed variant source/settings plus lock/toolkit/library identities with
the existing provenance schema. Use fresh output/artifact destinations and
native IDs. Publish a single derived comparison JSON/table into the reference
run before finalizing it; it references the already recorded variant runs rather
than becoming another run lifecycle. IP1 confirms ordering against accepted
RUNNING/finalization requirements: reference stays RUNNING until all candidates
and summary publish; no helper may reopen a finalized run. Persist successful
variant outputs if a later candidate fails, and mark eligible runs FAILED where
possible. No successful complete comparison after missing output, failed
baseline/candidate or publication failure; retain original/secondary diagnostics.

Proposed comparison JSON fields to finalize in IP1: schema version, reference
variant/run ID, source and original split reference, fixed estimator identity and
effective settings, metric/direction, validation membership, and ordered rows of
variant name/run ID/score/raw delta/direction-adjusted delta/outcome/output and
artifact references. The baseline row is identified explicitly. Reuse existing
records/references rather than duplicating pipeline serialization. Summary
presence is not itself verification of score, lineage or fit scope.

### Independent fixture matrix for contract review

Use a small DataFrame with integer row IDs, train rows 0–3, validation rows 4–5
and separate final-test rows 6–7. Train labels are `[0, 0, 1, 1]`, validation
labels `[0, 1]`. Training `signal` and `misleading` columns are both
`[-2, -1, 1, 2]`; validation `signal = [-3, 3]`, `misleading = [3, -3]`.
`constant = 0` on train/validation. Final-test values include extreme sentinels.
Use a fixed seeded DecisionTreeClassifier of depth 1 and native scaling.

| Authored variant | Selected feature | Independently expected validation labels | Accuracy / zero-one loss | Outcome against reference |
|---|---|---|---|---|
| reference | constant | `[0, 0]` | 0.5 / 0.5 | Reference |
| signal | signal | `[0, 1]` | 1.0 / 0.0 | Gain, adjusted delta +0.5 |
| unchanged | constant with explicitly authored equivalent native scaling settings | `[0, 0]` | 0.5 / 0.5 | Tie, delta 0 |
| misleading | misleading | `[1, 0]` | 0.0 / 1.0 | Regression, adjusted delta -0.5 |

Native feasibility in IP1 confirms this oracle without deriving expected values
from the implementation. Training scaler means for signal/misleading are 0;
extreme held-out rows must not alter them. Independently inspect actual feature
values/width/dtypes/row alignment, predictions, scores and native MLflow artifacts.
Add mixed numeric/categorical coverage using the accepted preprocessing literal
imputation/unseen-category expectations, without inventing new encodings.

Negatives: missing validation/two-way layout, overlap or stale source record,
target/ID feature selection, missing columns/schema mismatch, duplicate/empty
candidate declarations, unsupported metric/direction, malformed settings, missing
expected output, changed/missing committed or DVC input references, artifact
conflict and deterministic native transform/publication failure. Existing strict
candidate and fit-scope failures remain covered through public regressions.
Since this recipe executes every variant from one common protocol, it does not
accept arbitrary historical runs as comparable inputs. Verify persisted records
agree on data/split/class/settings/metric before publishing the summary.

Tests invoke the copied entrypoint with the separate project's interpreter from
an unrelated cwd and inspect native MLflow/DVC/public artifacts. No private
toolkit helpers, internal fit-call mocks or source-path injection. These checks
cover the documented workflow and supported outputs, not arbitrary project code,
OS holdout isolation, all sklearn estimators, assistant usability or M2 replay.
Public boundary confirmation: **Approved contract v2**, developer “yes i approve contract v2”, 2026-11-15 UTC; accepted preprocessing,
training and tracking contracts remain unchanged.

## Plan review

- **Status:** Approved.
- **Developer decision:** Initial plan approved separately from execution/contract decisions. Subsequent IP1/IP2 authorization and contract v2 approval are recorded below.
- **Decision reference and date:** Developer “I approve the plan”, 2026-11-15 UTC.
- **Requested plan changes:** Factory revision US-14-SC-01 incorporated. Developer “i approve the plan; commit”, 2026-11-15 UTC, approved the revised plan and authorized committing the four IP1 documents. This records plan approval; remaining contract/public-boundary approval and IP2 execution remain separate.

Planning validation on 2026-11-15: all 25 local document links, including
fragments, resolve; three phase blocks and five criterion mappings are present.
`git diff --check` passed for tracked edits, and a separate whitespace scan
checked this new untracked plan. No Python behavior changed; no environment,
pytest run or executable shared checks were needed for this planning task.

## Execution authorization

Follow [command/autonomy policy](../development/command-approvals.md).

- **Authorized phase sequence and workspace:** IP1–IP3 in the associated worktree. Developer “start phase 2”, 2026-11-15 UTC, authorizes IP2 execution once its contract-approval entry condition is satisfied. Developer “i approve phase 3”, 2026-11-15 UTC, authorizes IP3 execution; this does not claim phase completion or story acceptance.
- **Execution authorization reference and date:** Developer “start phase 1”, 2026-11-15 UTC. Earlier planning authorization and plan approval remain recorded above.
- **Verification scope:** IP1 source/dependency review and bounded probes; approved IP2 red–green slices, focused regressions and shared checks below. Developer initially authorized the retained-check runner, then explicitly directed “Stop using run-us14-check.py for test execution.” All subsequent tests use direct `uv run --locked pytest ...` commands with complete tool output saved separately. No broader suite or standalone artifact run is granted.
- **Authorized external actions:** Issue #20 policy-wording update explicitly authorized on 2026-11-15 by “can you update the issue for consistency”; published and verified. Developer “commit changes” authorized the earlier planning commit; developer “i approve the plan; commit”, 2026-11-15 UTC, authorizes committing the revised plan, checkpoint, contract document and IP1 evidence. Developer “commit changes” after Phase 2 gate approval, 2026-11-15 UTC, also authorizes committing Phase 2 implementation, tests, docs and approval records. Developer “I accept the user story; commit the changes”, 2026-11-16 UTC, accepts the whole story and authorizes the accepted-story publication sequence through execute-plan.
- **Next required gate:** Developer PR review/merge decision after accepted-story publication; explicit whole-story acceptance is recorded below. IP2 required verification passed; contract v2/public boundaries remain approved by “yes i approve contract v2”, 2026-11-15 UTC. Whole-story acceptance is complete.

## Scope-change history

IP1 refined the proposed recipe into [contract v1](../feature-pipelines.md),
including exact settings/artifacts, explicit variant budget checks and separate
derived DVC pointers. This is the planned IP1 contract refinement, with no AC,
phase verification or milestone change. V1 approval was pending at that point; v2 was subsequently approved as recorded in IP1 progression.

### US-14-SC-01: Settle project factory declaration boundary

- **Request and decision:** Developer preferred the factory, chose “let's stay with predeclared”, then stated “i accept these recommendations”, 2026-11-15 UTC. Approved the no-argument factory, project-assigned positional output labels, global names/selected-only full validation and project-owned helpers/types.
- **Scope difference:** Contract proposal v2 specifies `feature_variants.py:get_variants()` returning fresh unfitted pipeline declarations. Explicit category lists retain the predeclared schema approach. Unselected fields are not fully validated; eager factory construction errors still propagate before selection.
- **Impact:** Refines IP1-T3 and IP2-T2 for AC-01/02/05. No issue acceptance criteria, toolkit API, milestones or verification commands change. No dependent behavior tests or production implementation are authorized.
- **Verification:** Add factory/selection/fresh-object/positional-schema/predeclared-category cases to IP2-T2; retain all existing focused, regression, installed and final checks. Renew document validation. Native feasibility remains valid and is not evidence of implemented factory behavior.
- **Decision:** These factory decisions are Approved; the complete contract/public-boundary gate was pending at that decision, then approved as contract v2. Original v1 proposal and evidence remain historical records.
- **Resume point:** Review remaining contract/public test boundaries; IP2 execution requires separate authorization.

IP2 verification command refinement: check examples together with `src` using
`uv run --locked mypy src examples/feature-comparison`. Standalone example
checking found the editable toolkit untyped because it has no py.typed marker.
Including the source targets lets mypy resolve its maintained annotations and
adds coverage, without a checker exclusion/suppression or package resource
change. The required separate `mypy src tests` check remains unchanged. Retain
the initial failure under `example-mypy-initial.log`. This is an implementation
check adjustment, with no product contract or verification reduction.

During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md).

## Execution and verification rules

Mark tasks Complete only after their required checks pass and actual evidence is
recorded. Work one behavior at a time: failing public test with the intended
missing behavior, minimum implementation, green plus relevant regressions, then
the next slice. Do not batch all tests before implementation. Document-only
contract work has no new executable behavior and needs no manufactured red test.
Preserve original assertions and the repository's three-attempt limit; record
each corrective hypothesis/change/result and stop after the third failed attempt.

After execution authorization, provision only this worktree's `.venv` with
`uv sync --locked --group dev`, checking environment overrides first. Record
`uv.lock` SHA-256 before/after checks. Dependency changes require separately
reviewed scope; none are proposed. Every executable phase requires focused tests,
relevant regressions, `uv lock --check`, `uv run --locked ruff check .`,
`uv run --locked ruff format --check .`, `uv run --locked mypy src tests`,
`uv run --locked agentic-ml --version` and `git diff --check`. Ensure the example
is also included explicitly in type checking if not covered by `src tests`.
Use four workers/loadgroup; a serial single-case TDD invocation needs a recorded
short-cycle rationale. Classify direct US-14 checks as `milestone_1`; preserve
existing groups and fixture isolation. Contributor-only driver checks are
infrastructure unless they directly verify a milestone requirement.

Retain complete commands/cwd/stdout/stderr/exit codes, test counts, revision/dirty
files, lock/artifact digests and platform/library identities under
`.dev-records/verification/`, per [records policy](../development/records.md).
Summarize in proposed `docs/verification/us-14-ip<N>.md`. Use existing
verification support and owned workspaces; no historical cleanup or retention
changes. Failed, skipped, interrupted or unrun required checks block progression.
Record automatic progression as verification-based, never developer approval.
An unresolved contract change stops dependent work for review; whole-story
acceptance remains explicit. Refresh CHECKPOINTS at each boundary and handoff.

## US-14 / Implementation Phase 1: Settle the comparison recipe contract

- **Outcome:** Exact runnable recipe, artifacts and independent public boundaries ready for review.
- **Entry conditions:** Execution authorization; supplier code/evidence checked against base; issue policy discrepancy resolved before affected implementation.
- **Acceptance criteria advanced:** US-14-AC-01–05; no executable acceptance yet.
- **Approval mode:** Contract review.
- **Contract reference and decision:** [Comparison recipe contract v2](../feature-pipelines.md); Approved by “yes i approve contract v2”, 2026-11-15 UTC.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-14-IP1-T1 | Complete | Refresh #20/all comments; reconcile issue policy wording and concrete supplier records; inspect accepted APIs, training recipe and provenance output rules | Execution authorization | Scope/policy reconciliation recorded; authorized external synchronization completed and reread before code; no altered ACs or supplier reopening | AC-01–05 |
| US-14-IP1-T2 | Complete | Bounded native-only probes of fixed-tree feature matrix, both metric directions, native transforms/schema and MLflow reference-run finalization ordering; retain proposed `docs/verification/us-14-ip1.md` | T1 | Literal oracle confirmed, dependency versions recorded, no novel wrapper/encoding needed; original native errors preserved | AC-01–04 |
| US-14-IP1-T3 | Complete | Finalize proposed `docs/feature-pipelines.md`, example file/input inventory, exact comparison artifact schema and preflight/failure behavior; refine this plan's tests/tasks | T2 | Full root/cwd/settings/metric/tie/output/persistence matrix; independent fixture and public boundaries explicitly presented for developer approval | AC-01–05 |

### Verification and review evidence

No production code or dependent behavior tests in this phase. Review every AC
against inputs/outputs; inspect local links and `git diff --check`. Native probes
are feasibility evidence, not green toolkit tests or installed acceptance.
IP2 owns executable behavior; IP3 owns both-wheel/M1–6 verification. Shared
executable checks are inapplicable to document-only edits.
Actual results: [IP1 evidence](../verification/us-14-ip1.md): native numeric, mixed
transform/schema and MLflow lifecycle probes passed (exit 0). Issue snapshot
complete/stable with one comment. Lock unchanged. Final document checks recorded
below; no product behavior tests or production implementation were performed.
Final validation: all 77 local links/fragments across the four changed documents
resolve; tracked diff and all four files pass whitespace checks. The link checker
initially rejected a valid historical directory link; corrected the checker to
accept existing directory targets and retained both results.

### Phase progression

- **Required verification:** T1–T3 complete; issue alignment confirmed; feasibility and document checks pass.
- **Evidence presented:** [Contract v2](../feature-pipelines.md) and [IP1 evidence](../verification/us-14-ip1.md), 2026-11-15 UTC. T1–T3 technically complete; contract approval is separate.
- **Contract decision:** Factory decisions approved on 2026-11-15 by “let's stay with predeclared” and “i accept these recommendations”; full contract v2 and public test boundaries subsequently approved by “yes i approve contract v2”, 2026-11-15 UTC.
- **Requested changes and resolution:** None recorded.
- **Progression result:** IP1 complete and required checks passed; contract v2 approved. IP2 execution authorized by “start phase 2”, 2026-11-15 UTC; IP2-T1 starts after prerequisite refresh.
- **Next phase:** IP2 only after the contract decision and within authorized sequence.

## US-14 / Implementation Phase 2: Execute and record controlled feature comparisons

- **Outcome:** Runnable recipe reports controlled feature outcomes with complete outputs and lineage.
- **Entry conditions:** IP1 complete, contract/boundaries approved, required checks pass; IP2 execution authorized.
- **Acceptance criteria advanced:** US-14-AC-01–05.
- **Approval mode:** Automatic; implements the IP1-approved contract. Any new toolkit helper or artifact/error contract change requires review first.
- **Contract reference and decision:** Contract v2, Approved by “yes i approve contract v2”, 2026-11-15 UTC. Public boundaries: copied entrypoint in independent installed project, native outputs/MLflow/DVC inspection and literal numerical expectations; direct/rebuilt-wheel acceptance remains IP3.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-14-IP2-T1 | Complete | Add proposed `tests/integration/test_feature_comparison.py`; copy proposed `examples/feature-comparison/compare_features.py` and `feature_variants.py` to an isolated committed experiment; implement first reference/signal slice | IP1 approval | Intended red failure captured, then literal train transform, prediction, accuracy and gain pass using identical strict candidate/class/settings/source/splits and unchanged caller inputs | AC-01/02/03/05 |
| US-14-IP2-T2 | Complete | Verify approved no-argument factory, global name checks, selected-only full validation, fresh declarations, positional schema labels and predeclared categories through public outcomes; add equivalent/tie and misleading/regression variants, then minimize metric and invalid declarations through separate red–green slices; implement native metric/table logic in recipe | T1 | Literal score/delta/outcome matrix passes for both directions; missing validation and malformed/duplicate/unrecordable candidate/settings fail; no final-test predictions or feedback | AC-01/03/05 |
| US-14-IP2-T3 | Complete | Add independent transformed-output/schema and train-only oracle slices, mixed categorical case, stale-source/overlap/schema failures; persist feature outputs with row IDs using native project IO | T2 | Literal values, schemas and membership agree; held-out sentinels do not alter fitted statistics; valid output references and source identities survive persistence | AC-01/02/04 |
| US-14-IP2-T4 | Complete | Add MLflow/DVC publication slices and reference/candidate/summary inspection, using accepted tracking APIs; add missing-output/reference, collision and native failure cases individually | T3 | Same fixed protocol in actual native runs; code/config/lock/dependency/DVC links inspectable; comparison JSON uploaded before reference finalization; failures retain available evidence and never claim a complete successful comparison | AC-02/03/04 |
| US-14-IP2-T5 | Complete | Complete example README and guide; run focused/regression/shared checks; record proposed `docs/verification/us-14-ip2.md` and checkpoint | T4 | Exact copied example works without test-internal imports, focused evidence valid and all required checks pass | AC-01–05 |

### Verification and review evidence

Changed executable surface is the new project example, with tests of installed
public fit/tracking APIs and native artifact observations. No existing package
signature/schema is changed. Run the following phase selection:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_feature_comparison.py tests/integration/test_preprocessing.py tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_preprocessing_tracking.py
```

The new matrix directly covers all five ACs. Existing modules regress native
fit/schema/validation and producer/tracking/finalization compatibility affected
by the recipe. Run shared checks from execution rules, plus proposed
`uv run --locked mypy src examples/feature-comparison` once files exist. Avoid
altering shared APIs solely to simplify the recipe. Actual results are recorded below.
Both-artifact recipe execution, broader unchanged callers and M1–6 are deferred
to US-14-IP3-T1–T3. No full current-milestone run is required here.

Actual results: [IP2 evidence](../verification/us-14-ip2.md). The full planned
selection passed 183 cases. Final review added output-parent and native pandas
labeling regressions; the renewed comparison module passed all 43 cases, with
142 unchanged supplier/tracking regressions reused against unchanged relevant
inputs. No single 185-case run is claimed. Shared checks and document checks
pass; lock unchanged. No new suppressions, skips or check exclusions.

### Phase progression

- **Required verification:** T1–T5, selected tests and shared checks pass on current inputs; no unresolved contract change/failure.
- **Evidence presented:** [IP2 evidence](../verification/us-14-ip2.md), with retained red/green/correction history, native artifacts/data lineage, 43 current comparison cases and 142 valid regressions.
- **Contract decision:** Reuse approved contract v2; developer “yes i approve contract v2”, 2026-11-15 UTC. No contract change introduced.
- **Requested changes and resolution:** None recorded.
- **Progression result:** Automatic — verification passed, 2026-11-15 UTC. IP2-T1–T5 Complete. This is technical completion, not developer story acceptance.
- **Developer phase decision:** Approved — “i approve phase 2 gate”, 2026-11-15 UTC. This records the explicit phase decision alongside automatic technical completion, without granting story acceptance or IP3 execution. Developer “commit changes” authorizes committing Phase 2 work and its approval records.
- **Next phase:** IP3 execution authorized by “i approve phase 3”, 2026-11-15 UTC; IP2 prerequisites and contract v2 remain valid.

## US-14 / Implementation Phase 3: Verify installed delivery and story acceptance

- **Outcome:** Same documented project workflow verified on both normal wheel paths, final AC reconciliation ready for acceptance.
- **Entry conditions:** IP2 complete and required checks pass, IP1 approval remains applicable, IP3 authorized.
- **Acceptance criteria advanced:** US-14-AC-01–05 in full.
- **Approval mode:** Automatic; tests/docs verify the approved contract.
- **Contract reference and decision:** Approved contract v2, “yes i approve contract v2”, 2026-11-15 UTC; reuse for IP3. Execution authorized by “i approve phase 3”, 2026-11-15 UTC.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-14-IP3-T1 | Complete | Add proposed `tests/installation/check_feature_comparison.py` and `verify_feature_comparison.py`, reusing existing distribution/Invocation/owned-workspace support and US-18 installation pattern; add proposed `tests/integration/test_installed_feature_comparison.py` | IP2 complete | Normal direct wheel in separate project/runtime-only environment executes exact copied example from unrelated cwd; independent oracle, run/feature/artifact references, representative failures, import origins, CLI version/resources/dependency inventory verified | AC-01–05 |
| US-14-IP3-T2 | Complete | Run same public workflow and checks on a wheel genuinely rebuilt from extracted sdist, separate fresh environment; no direct-wheel substitution | T1 | Both artifact identities recorded with complete stdout/stderr, consistent outputs/direction tables and source lineage; default successful cleanup and failure retention follow existing policy | AC-01–05 |
| US-14-IP3-T3 | Complete | Run final focused tests, M1–6/shared checks, reconcile phase exclusions and AC evidence; finish guide/README links, affected active design/traceability/project status, plan and CHECKPOINTS; write proposed `docs/verification/us-14-ip3.md` | T2 | Final evidence tied to implementation/lock/artifacts/platform; all required US-14 checks pass, no hidden exclusions, explicit whole-story acceptance requested | AC-01–05 |

### Verification and review evidence

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_feature_comparison.py tests/integration/test_installed_feature_comparison.py tests/integration/test_installed_training.py
uv run --locked pytest -n 4 --dist=loadgroup
```

First command verifies the new installed boundary plus unchanged installed
training behavior; retain the distribution scheduling group. The installed test
may invoke its verification driver internally. Do not launch standalone artifact
drivers or broader pytest selections without an explicit developer command.
Second command resolves deferred M1–6 regressions for story acceptance. Repeat
shared checks and example typing from execution rules. Validate all new links
and exact recipe/document agreement. Actual results: [IP3 evidence](../verification/us-14-ip3.md).
The focused selection passed 45 tests. M1–6 selected 1,027 cases and finished
with 1,026 passed, one existing developer-authorized US-03 skip and no failures
or errors. Shared checks, lock consistency, document targets and whitespace pass.
No new exclusion or suppression; the skipped historical requirement is retained
under M1-ACCEPT-VERIFY and is not counted as passing US-14 evidence.

### Phase progression

- **Required verification:** T1–T3 and final requirements below pass with current evidence.
- **Evidence presented:** [IP3 evidence](../verification/us-14-ip3.md), both normal wheel identities and independent native outputs, 45 focused passes and M1–6 result (1,026 passed / 1 existing skip).
- **Contract decision:** IP1 approval reused; no separate final contract gate unless behavior changes.
- **Requested changes and resolution:** None recorded.
- **Progression result:** Automatic — verification passed, 2026-11-16 UTC. IP3-T1–T3 Complete; no developer story acceptance is implied.
- **Developer phase decision:** Approved — “I approve phase 3”, 2026-11-16 UTC, after reviewing the completed results. Whole-story acceptance followed separately as recorded below.
- **Next action:** Developer PR review/merge decision; publication is recorded below. Merge and cleanup retain separate authorization.

## Final verification requirements

- **Owning final phase/task:** US-14-IP3-T3, before presenting whole-story acceptance.
- **Final implementation identity:** Record tested revision, changed files, lock before/after hashes, direct/sdist/rebuilt artifact hashes, copied recipe identity and project commit/toolkit installation identity.
- **M1–6 and shared checks:** Run final M1–6 command above, phase regressions as needed, all shared checks and example typing; report collected/selected/deselected/pass/fail/skip counts and every nonpassing result. Renew after executable input changes.
- **Distribution/installation:** Both-wheel recipe checks in T1/T2 are required selected tests. No standalone/broader run is implicitly authorized. Preserve runtime dependency/CLI/resource/import checks and genuine rebuilt path.
- **Deferred-check reconciliation:** T3 owns both-wheel checks deferred by IP2, final unchanged-caller M1–6 coverage and all phase exclusions. Historical skips and unrelated milestone omissions remain visible, not passing evidence. An uncovered in-scope AC blocks acceptance.
- **Actual results and limitations:** [IP3 evidence](../verification/us-14-ip3.md): Linux aarch64 / Python 3.12.16; exact native versions, artifact/source/lock identities and one existing US-03 skip retained. No macOS, Windows, fresh notebook, assistant or M2 reproduction claim.

## Story completion review

All abbreviated AC labels in task tables mean the corresponding `US-14-AC-XX`.

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-14-AC-01: Describe authored scikit-learn pipeline steps, parameters, selected columns and training-only fit scope | IP1-T3; IP2-T1/T3/T5; IP3-T1–T3 | Independent scaler/schema oracle, exact existing metadata and authored settings on both installs | Verified and accepted, 2026-11-16 |
| US-14-AC-02: Execute transformations and record settings, dependencies, output references and source-data identity | IP2-T1/T3/T4; IP3-T1–T3 | Actual feature outputs and MLflow artifacts, code/lock/library/source/split/DVC links | Verified and accepted, 2026-11-16 |
| US-14-AC-03: Compare authored variants on the same split, estimator/settings and metric; report direction-aware gains/ties/regressions | IP2-T1/T2/T4; IP3-T1–T3 | Literal 0.5/1.0/0.5/0.0 accuracy and corresponding loss, actual records/table and failure matrix | Verified and accepted, 2026-11-16 |
| US-14-AC-04: Link artifacts to source datasets and verify expected outputs through supported paths | IP2-T3/T4; IP3-T1–T3 | Persisted values/schema/row IDs, artifact availability and lineage, missing/corrupt-reference/output failures | Verified and accepted, 2026-11-16 |
| US-14-AC-05: Use explicitly authored or supplied candidates | IP1-T3; IP2-T1/T2/T5; IP3-T1–T3 | Explicit project source/declarations, no generated candidates, duplicate/missing/unsupported declaration failures | Verified and accepted, 2026-11-16 |

- **Remaining work:** Developer PR review/merge decision. [PR #70](https://github.com/jimthompson5802/agentic-ml/pull/70) and its static COMMENT review are published; [publication evidence](../verification/us-14-publication.md). IP1–IP3 and all five US-14 criteria are verified and accepted. Historical milestone obligations and the existing US-03 skip remain with their named owners.
- **Partial prerequisite delivery:** None proposed; supplier capabilities reused without accepting their remaining M2 scope.
- **Final verification:** Complete US-14-IP3-T3, 2026-11-16 UTC; [IP3 report](../verification/us-14-ip3.md).
- **Developer acceptance:** Accepted — all five M1 criteria, 2026-11-16 UTC.
- **Decision reference and date:** Developer “I accept the user story; commit the changes”, 2026-11-16 UTC. Authorizes accepted-story commit/push, PR creation and static COMMENT review through execute-plan; merge and worktree cleanup remain separate.

## Milestone acceptance handoff

Publication on 2026-11-16 UTC: accepted-story commit `b02a2188755ebf4bd40ba8142ef89ea865d79f12`
was pushed to the owning branch; [PR #70](https://github.com/jimthompson5802/agentic-ml/pull/70)
targets main `9a030cfe5d6523531e386b0195f40a16599180fc` and closes #20 on merge.
The [static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/70#pullrequestreview-5913922925)
reports no actionable findings at that head. This documentation-only publication
record receives a final static head review retained in the PR timeline and raw
publication metadata. No project checks ran during review; existing verification
remains applicable. No merge or worktree cleanup was performed.

- **Owner:** `MVP-M1-ACCEPT-VERIFY`; `MVP-M2-ACCEPT-VERIFY` retains later restored-state/replay integration.
- **Deferred checks:** Native stage execution/cache invalidation (US-27), basic-path and scientist/assistant integration (US-39), M2 compatible components/notebooks/restoration/replay, unverified platforms. These are exclusions from US-14 delivery, not waived milestone obligations. Preserve historical `M1-ACCEPT-VERIFY` and independent `M50-ACCEPT-VERIFY` records.
- **Required evidence:** Reconcile final story/CI artifact identities, unresolved failures/skips and manual/platform deferrals before milestone acceptance. Complete-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, shared checks and applicable direct/rebuilt distribution/installation evidence remain policy-controlled; broader local runs and standalone drivers require explicit developer commands. Story acceptance does not establish milestone acceptance.

## Issue policy synchronization — 2026-11-15

Developer authorized updating #20 for consistency. Published contract-review and
automatic-progression wording, focused phase verification, M1–6 story acceptance,
explicit broader/artifact check authorization and the phase-policy link. Reread
the complete issue and verified the intended body; acceptance criteria and the
existing comment count were preserved. No implementation authorization is implied.
