# Milestone 1 / US-15 #21: Preserve training-only preprocessing

## Scope and outcome

- **Milestone:** M1 — Complete one local classification experiment.
- **User story:** [US-15 / issue #21](https://github.com/jimthompson5802/agentic-ml/issues/21).
- **User-visible outcome:** A separate experiment project fits a native
  scikit-learn pipeline on recorded training rows and uses it unchanged for
  validation/test/inference. It receives plain metadata accepted by US-26 for
  MLflow preservation with separately supplied committed code/dependency links.
- **Acceptance criteria covered:** [US-15-AC-01](../specs/user-stories.md#us-15-ac-01),
  [US-15-AC-02](../specs/user-stories.md#us-15-ac-02),
  [US-15-AC-03](../specs/user-stories.md#us-15-ac-03). AC-03 requires the later
  actual US-15 → US-26 integration evidence; returning an object is insufficient.
- **Scope boundaries:** M1 slice only. [AC-04](../specs/user-stories.md#us-15-ac-04)
  restored transformation/reproduction remains M2. No comparisons/search,
  general transformer registry, notebook runner, runtime approval service,
  hostile-code protection or independent Git/DVC/MLflow discovery in US-15.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
  [data/features](../specs/design/data-and-features.md#authored-feature-pipelines),
  [interfaces](../specs/design/interfaces-and-configuration.md#installed-project-boundary),
  [tracking ownership](../specs/design/execution-and-governance.md#tracking-and-storage-ownership),
  [blueprint](../specs/design/software-blueprint.md#planned-mvp-responsibilities),
  [traceability](../specs/design/acceptance-traceability.md),
  [delivery order](../specs/design/milestone-delivery.md#capability-order-and-owning-stories),
  [repository layout](../specs/design/repository-layout.md),
  [ADR-008](../specs/design/architecture-decisions.md#adr-008--local-experiment-mvp-and-externally-owned-assistant-use).
- **Coordinated execution index:** [US-15 / US-26 order and proposed exact contract](../../../US-26-mlflow/docs/plans/milestone-1-us-15-us-26-execution-order.md).
  This US-26-owned index is the single planning definition of metadata and
  provenance fields/types; review it with this plan. Sibling worktree links are
  intentional for this local planning handoff; rewrite to same-checkout links
  during separately authorized integration, preserving IDs/evidence.

## Workspace association

- **GitHub issue and story:** #21 / US-15; issue number differs from story number.
- **Branch:** US-15-preprocessing.
- **Base ref and starting commit:** local main,
  1a9864a645084af8cfcec580b1db5fa045a67859.
- **Worktree:** .worktrees/US-15-preprocessing, relative to the primary checkout.
- **Observed creation:** New branch/worktree, clean at creation on 2026-11-14.
  No fetch/pull or current remote comparison; local main is the requested base.
  No .venv was created. The pre-existing primary-checkout CHECKPOINTS.md edit was
  preserved and was not copied into this checkout.

Follow [worktree guidance](../development/worktrees.md); verify the issue,
branch, current edits and gates on resume. Use a dedicated execution session and
environment for this story. Creating the worktree does not authorize execution.

## Source snapshot and current state

Retrieved #21's entire body and all comment pages on 2026-11-14; two unique
comments matched reported count 2 and final updated_at remained
2026-11-14T18:07:50Z. Open issue, label enhancement, no assignees, null GitHub
milestone; the body explicitly assigns AC-01–03 to M1 and AC-04 to M2.
Both comments are by jimthompson5802: scope disposition
[6699590563](https://github.com/jimthompson5802/agentic-ml/issues/21#issuecomment-6699590563)
and accepted contract
[6881961026](https://github.com/jimthompson5802/agentic-ml/issues/21#issuecomment-6881961026).
Complete coordinated/prerequisite snapshots are retained locally under
.dev-records/verification/20261114-us15-us26-planning/issues.json, with comment
IDs, authors, timestamps, URLs and metadata. The index records completeness.

No matching US-15 implementation plan or preprocessing module existed at the
base. src/agentic_ml/splitting/__init__.py implements create_partitions with
the accepted [partition boundary](../data-assessment-and-splits.md#partition-boundary)
and [1.0 record](../data-assessment-and-splits.md#source-identity-and-record).
It already checks supported homogeneous IDs, nonempty complete coverage and
overlap, and hashes consumed native Parquet with version information. Project
code owns saving/loading the record. Do not invent another partition service.

scikit-learn, pandas, pyarrow and MLflow are declared runtime dependencies;
contributor lock has scikit-learn 1.9.1, MLflow 3.17.2. No new dependency is
expected. There is no implemented fitted-pipeline helper or tracking export.
Native DVC M1 versioning and Git/wheel identity support are accepted in their
owning plans. Historical evidence is not a test run against this branch.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-15-US-26-CONTRACT-01 | Native fitted Pipeline + JSON dictionary; separate shared provenance; MLflow ownership | All dependent code | Interface direction accepted in both issue bodies/comments on 2026-11-14; exact proposed fields/types and public boundaries in index await review. |
| Existing partitions, US-12 #19 | Both layouts, current source identity and memberships | IP2 | Implemented; [US-12 IP3/IP4 and Gates 1–4](milestone-1-us-12-assessment-splits.md), AC-02/03 accepted. No reopening or saved-file parser. |
| US-26 producer contract review | Same exact dictionary representation and serialization/error rules | IP2/IP3 | Both Gate 1 decisions must approve the shared contract; index coordinates revisions. |
| Native pipeline composition | clone/fit/transform supported imputer/scaler/encoder Pipeline/ColumnTransformer without replacement algorithms | IP2 | IP1 feasibility and reviewed test matrix required before production code. |
| MLflow preservation and provenance | Actual US-15 output is saved with committed references | IP4 / complete AC-03 | [US-26-IP4-T1/T2](../../../US-26-mlflow/docs/plans/milestone-1-us-26-recording.md#us-26--implementation-phase-4-installed-handoff-and-17-acceptance), consumer Gate 4 and reviewed combined revision required. No whole US-26 #33/#43 dependency. |
| Shared code available in consumer | Reviewed producer revision in US-26 branch | US-26 IP4 | Separate integration authorization needed; shared Git objects alone do not provide it. Index identifies cross-branch availability gate. |
| Feature comparisons, US-14 #20 | Fixed validation comparisons | None in this plan | Separate owner; reviewed issue overlap does not transfer its criteria here. |
| AC-04 restoration | Fresh-project restored transformation checks/tolerances | Future M2 | Explicitly deferred by #21; MVP-M2-ACCEPT-VERIFY retains integration reconciliation. |

The current [verification policy](../development/verification.md#phase-and-story-verification)
supersedes stale current-milestone-at-gates prose in issue/design boilerplate.
Use focused tests/regressions plus shared checks; M1–6 only at slice acceptance.
No product scope conflict remains; unresolved contract feasibility is bounded by IP1.

## Proposed interface and independently defined test boundary

Proposed public import: agentic_ml.preprocessing.fit_preprocessing. Its signature
and exact dictionary fields/types are defined in the coordination index under
Proposed handoff types and Proposed public boundaries. Do not implement another
public result type. Return a fitted native sklearn Pipeline and JSON-compatible
metadata. Use clone to preserve the caller's pipeline, validate membership through
native-backed create_partitions, fit only selected train columns, and preserve
recorded row-ID/source identity and original seed settings. No refit on held-out
rows. Project code calls native pipeline.transform on the selected columns.

Reject unsupported fit_partition, overlap/unknown/duplicate/missing IDs, layout
mismatch, empty train, ID/target selected as features, stale input source identity,
duplicate/missing feature columns, invalid declared schema, opaque/unrecordable
settings and non-Pipeline input before affected fitting/publication. Native
fit/transform errors remain visible with stage context. Only the consumed
in-memory selected record fields are validated; saved-document parsing, policy
for comparing historical source versions and DVC restoration remain project/M2 work.

Proposed public tests verify returned native transforms, metadata, unchanged
inputs/cwd and clear errors. They do not inspect private helpers or mock internal
fit call counts. Use literal expected numbers, direct public sklearn statistics
where useful, and a recording transformer only if needed to observe the public
fit contract, not as evidence of arbitrary code containment. Independent actual
transformations are primary evidence.

Fixture oracle for developer confirmation at Gate 1:

| Fixture | Expected independent observations |
|---|---|
| Numeric frame id [0,1,2,3,4,5], x [1,3,100,200,1000,2000], label [A,B,A,B,A,B]; supplied train [0,1], validation [2,3], test [4,5] | StandardScaler learns train mean 2 and scale 1; transforms train [-1,1], validation [98,198], test [998,1998], inference x=5 to 3. Counts/memberships/schema exact; floats abs/rel 1e-12. |
| Two-way train [0,1], test [2,3,4,5] | Same training statistics; no invented validation partition; test transform [98,198,998,1998]. |
| Training x [1,null,3] plus held-out x=100 | SimpleImputer(mean) learns 2, training output [1,2,3], held-out 100 unchanged. Held-out values cannot alter imputation. |
| Training category [a,b], validation category c, OneHotEncoder(handle_unknown="ignore", sparse_output=False) | Declared columns cat_a/cat_b; literal training [[1,0],[0,1]], validation [[0,0]]. Combined pipeline checks step order, width and settings. |
| Reordered/nondefault-index source and string IDs | Membership order and target alignment from existing record preserved; index is not row identity. |
| Corrupt membership / wrong fit scope / changed values under same IDs | Supported helper rejects before fit; copied input/pipeline unchanged; no valid fitted return or false completion metadata. |
| JSON metadata and pipeline handoff | Exact index-defined fields/types and effective defaults, source/membership equality, json.dumps(..., allow_nan=False) succeeds; no fabricated Git/DVC references. |

Developer boundary confirmation: Pending. Approval of this reviewed plan can
confirm the proposed matrix; IP1 records any refinement and Gate 1 confirms the
final contract before the first executable behavior test.

## Plan review

- **Status:** Draft.
- **Developer decision:** Pending; review this M1 slice with the US-26 plan/index.
- **Decision reference and date:** Pending.
- **Requested plan changes:** None recorded.
- **Implementation authorization:** Phase 1 execution and local commit authorized on
  2026-11-14 by “i approve phase 1; commit;”. This supersedes the earlier
  planning-only restriction for Phase 1. Later phases remain unauthorized.

## Scope-change history

None. This is a new plan carrying accepted CONTRACT-01, not an approval or scope
revision of an executing story. Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for later changes to authorized scope or approach.

## Execution and verification rules

Mark tasks Complete only when their output and required checks pass with actual
evidence. Partial/failed/unverified work stays incomplete. Use the execution index,
check supplier evidence and approvals, and reopen invalidated tasks/checks.
For behavior, take one test from the matrix, run red for the missing behavior,
implement the minimum green, rerun relevant regressions, then repeat. Do not batch
all tests before implementation. Record exact commands, red/green outcomes,
collected/selected/deselected counts, revision/dirty files, lock hashes and platform.

At every implementation phase end, including final, present evidence and stop
for explicit developer gate approval. Silence/plan approval is not gate approval.
Pause affected work for scope changes, revise owning plans/index together, and
obtain decisions before implementing new prerequisites. Follow AGENTS.md's
three-attempt limit with hypothesis/change/verification records; after three
failures stop corrective work, retain original assertions/failure evidence and
await direction. No assertion weakening, new skips or masking suppressions.

Shared commands at executable gates, from this worktree and its own environment:

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

Check environment overrides before synchronization. No environment setup is
authorized by this planning request. Retain unique logs under
.dev-records/verification/ per the [records policy](../development/records.md).
Use four workers/loadgroup for phase checks; short serial TDD selectors may use
the policy's documented exception with reason recorded. New behavior cases are
M1 by directly verified criteria. Tests below are proposed unless noted existing.

## US-15 / Implementation Phase 1: Confirm native fitting contract

- **Outcome:** Reviewed implementable API, field schema, native reuse and test matrix.
- **Entry conditions:** Separate execution authorization; refreshed complete #21/#17
  discussions and current branch/checkpoint; no earlier implementation is assumed.
- **Acceptance criteria advanced:** US-15-AC-01/02/03 design only, none verified.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP1-T1 | Complete | Reconcile this plan/index with current create_partitions contract, docs/data-assessment-and-splits.md and issue decisions | Authorization | Approved-direction/native API reuse table; confirm source/membership validation adds no new split format | AC-01/02 |
| US-15-IP1-T2 | Complete | Inspect locked sklearn APIs and run bounded native-only Pipeline/ColumnTransformer clone/fit/transform probes for matrix; save proposed docs/verification/us-15-ip1.md | T1 | Literal numeric/category expectations, schema/dtype/JSON encoding feasibility and exact error boundaries; no production helper or behavior tests written | AC-01/02/03 |
| US-15-IP1-T3 | Partial | Finalize proposed docs/preprocessing.md contract, this plan and shared index with US-26 owner | T2 and US-26-IP1-T1/T2 findings | Matching exact metadata keys/types, signature, supported M1 compositions, test matrix and file ownership ready for both Gate 1 reviews; neither story waits for the other's T3 | AC-01/02/03 |

### Verification and review evidence

Phase 1 execution: [producer evidence](../verification/us-15-ip1.md). T1/T2
complete; T3 producer proposal prepared in [contract](../preprocessing.md),
but joint finalization awaits US-26-IP1-T1/T2 findings. No sibling edits or
consumer approval are inferred. Developer authorization is recorded above.

- **Selected tests and impact rationale:** Native feasibility probes only; no
  toolkit behavior has changed. Check docs/links/whitespace with git diff --check.
- **Public boundaries and limits:** Proposed helper/native-transform boundary
  above; Gate 1 confirmation pending. Native probes do not verify helper fit scope.
- **Deferred checks:** Product red/green to IP2/IP3; installed persistence to
  US-26-IP4-T1/T2; M1–6/shared acceptance to US-15-IP4-T2.
- **Acceptance schedule:** No full milestone run for this contract-only phase.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Native feasibility / no duplicate algorithms | Exact standalone native commands and outputs in proposed IP1 report | Fixture oracle/schema/clone behavior feasible; unsupported cases identified | Native probe exit 0; see IP1 evidence; helper remains unimplemented |
| Contract/links/whitespace | Review fields against accepted issue direction; local-link scan; git diff --check | Matching types/ownership; links resolve | Producer matches index; document checks passed; joint confirmation pending |
| TDD applicability | Inspect diff | Contract/probes only; no new executable toolkit behavior requiring red | Confirmed: docs and local native probe only; no product/test code changes |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; both producers/consumers agree on exact
  contract, tests and schema; unresolved findings block dependent tasks.
- **Evidence presented:** [Producer Phase 1 evidence](../verification/us-15-ip1.md);
  T3 remains partial pending consumer feasibility. Gate 1 is not yet ready for
  joint approval.
- **Remaining limitations or blocked work:** All executable product behavior unverified.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — IP2 only after both Gate 1 contract approvals
  and authorization to execute; stop here.

## US-15 / Implementation Phase 2: Fit only recorded training rows

- **Outcome:** Public fitted Pipeline usable unchanged on held-out/inference rows.
- **Entry conditions:** Both Gate 1 contract approvals; own IP2 execution authority.
- **Acceptance criteria advanced:** US-15-AC-01/02; AC-03 preliminary native state.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP2-T1 | Not started | Add first numeric train-only test in proposed tests/integration/test_preprocessing.py; add minimum fit_preprocessing in proposed src/agentic_ml/preprocessing/__init__.py through red/green | Gate 1 | Literal scaler values pass, returned native Pipeline works; valid minimum metadata follows approved contract | AC-01 |
| US-15-IP2-T2 | Not started | Add one invalid-membership/fit-scope case per red/green cycle; reuse create_partitions supplied mode; preserve source/record identity | T1 | Reject overlaps, unknown/duplicate/uncovered IDs, layout/feature/scope/source mismatches before affected fit | AC-02 |
| US-15-IP2-T3 | Not started | Add two-way, supplied string IDs, reordered/nondefault index, imputation and categorical matrix cases one vertical slice at a time | T2 | Public transform outputs match independent expectations; original input/pipeline/cwd preserved; native errors visible | AC-01/02 |
| US-15-IP2-T4 | Not started | Review structure, run focused/regression/shared commands, record proposed docs/verification/us-15-ip2.md | T3 | Valid red/green records, counts/platform/lock identity and all required results available | AC-01/02 |

### Verification and review evidence

- **Selected tests and impact rationale:** Proposed preprocessing tests exercise
  public clone/fit/transform; existing splitting tests protect reused membership,
  source identity and both layouts. No MLflow calls in producer tests.
- **Public boundaries and limits:** Gate 1-confirmed public helper with literal
  oracle; cannot constrain arbitrary code or certify time/group protocol science.
- **Deferred checks:** Full metadata/default/error matrix to IP3;
  preservation to US-26 IP4; all excluded regressions to US-15-IP4-T2.
- **Acceptance schedule:** Focused below plus shared checks; no full M1 run.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Red then green per case | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py -k <one-case-selector> | Red is missing/incorrect behavior; green matches unchanged oracle | Pending |
| Preprocessing and partition regressions | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py | Pass; no weakened tests; current counts recorded | Pending |
| Shared development checks | Exact shared command block above | Pass; lock unchanged; correct installed CLI version | Pending |

### Developer approval gate

- **Approval criteria:** T1–T4 complete with AC-01/02 focused/regression/shared evidence.
- **Evidence presented:** Pending — proposed docs/verification/us-15-ip2.md.
- **Remaining limitations or blocked work:** Metadata completion and persisted handoff.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — IP3; stop here for explicit gate approval.

## US-15 / Implementation Phase 3: Produce metadata and verify installed use

- **Outcome:** Complete schema/settings/membership record and independently verified
  producer capability available for US-26 integration, without MLflow dependency.
- **Entry conditions:** Gate 2 approved and execution authority for IP3.
- **Acceptance criteria advanced:** US-15-AC-01/02 verified as a component; AC-03 advanced.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP3-T1 | Not started | Complete recursive effective-settings/schema/version metadata and failure cases in preprocessing module/tests, one red/green behavior at a time | Gate 2 | Exact index fields/types, order/default retention, JSON finite values, declared width/dtype checks and unsupported-setting errors | AC-03; AC-01/02 regressions |
| US-15-IP3-T2 | Not started | Add proposed tests/installation/check_preprocessing.py, register in existing verify_assessment_splits.py and selected distribution integration test; exercise direct/rebuilt installed projects from unrelated cwd | T1 | Actual normal installs return native fitted object and exact JSON; both wheel paths independently pass; no MLflow store or dev-dependency leakage | AC-01/02/03 component |
| US-15-IP3-T3 | Not started | Finish runnable docs/preprocessing.md script, inspect baseline compatibility, focused/shared checks and proposed docs/verification/us-15-ip3.md | T2 | User script is the installed tested path; approved producer revision/API/schema and evidence identified for US-26 owner | AC-01/02/03 |

### Verification and review evidence

- **Selected tests and impact rationale:** Preprocessing + splitting + assessment
  (native handoff regressions), and the existing both-artifact distribution test
  extended to call the new installed probe. Read current test ID before execution;
  adjust selector only if the actual discovered name differs, recording why.
- **Public boundaries and limits:** Noneditable installed imports, project-owned
  fixture and independent results. No source-path imports. No assertion that a
  returned metadata declaration proves fit scope; numeric cases remain required.
- **Deferred checks:** Actual MLflow handoff belongs solely to US-26-IP4-T1/T2;
  M1–6 and excluded checks belong to US-15-IP4-T2. AC-04 remains M2.
- **Acceptance schedule:** Focused tests plus shared checks; installed tests may
  invoke artifact drivers internally, not as standalone commands.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Metadata + partition regression | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_data_assessment.py | JSON/native behavior and existing accepted partition contract pass | Pending |
| Installed direct and rebuilt wheel producer | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py -k test_assessment_splits_from_both_artifact_paths | Both independent installed paths pass, actual selected counts/name recorded | Pending |
| Shared development checks | Shared command block | Pass; no accidental lock/dependency changes | Pending |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; actual installed producer capability ready,
  field parity with consumer confirmed, native and JSON evidence retained.
- **Evidence presented:** Pending — proposed docs/verification/us-15-ip3.md.
- **Remaining limitations or blocked work:** AC-03 incomplete until US-26 IP4.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — supply approved capability/evidence to
  US-26 IP4 through separately authorized integration. US-15 IP4 waits for consumer
  Gate 4; stop here without claiming M1 slice acceptance.

## US-15 / Implementation Phase 4: Review preservation and accept the M1 slice

- **Outcome:** M1 AC-01–03 reconciled with real producer/consumer preservation evidence.
- **Entry conditions:** US-15 Gate 3; US-26-IP4-T1/T2 evidence and Gate 4 approved;
  authorized relevant integration available in this branch for final checks.
- **Acceptance criteria advanced:** US-15-AC-01/02/03 complete M1 slice; not AC-04.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP4-T1 | Not started | Inspect US-26-owned installed handoff evidence against this producer revision and AC-03; link it in proposed docs/verification/us-15-ip4.md, this plan and checkpoint | US-26 IP4 and Gate 4 | Actual pipeline, exact metadata and committed code/dependency links persisted in run; no fixture-only substitute | AC-03 |
| US-15-IP4-T2 | Not started | Reconcile all M1 criteria/deferred checks, run final M1–6 and shared commands, finish docs/checkpoint and report | T1 | Final identity/lock/dirty files/counts/platform recorded, excluded/failed/skipped checks accounted for before Gate 4 | AC-01/02/03 |

### Verification and review evidence

- **Selected tests and impact rationale:** Reuse valid US-26 combined-revision
  handoff evidence; if producer code or build inputs changed, renew the US-26-owned
  selection before relying on it. No duplicate integration test implementation.
- **Public boundaries and limits:** Actual installed handoff covers preservation,
  not M2 restored numerical equivalence or full classification/assistant workflow.
- **Deferred checks:** T2 reconciles all earlier exclusions; unresolved required
  failures block M1 acceptance. AC-04 and named milestone obligations remain open.
- **Acceptance schedule:** Exact default M1–6 and shared checks against final inputs.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Preservation evidence | US-26-IP4-T1/T2 report, tested combined revision and Gate 4 | Exact pipeline/metadata/provenance artifacts and native run references | Pending |
| M1–6 story selection | uv run --locked pytest -n 4 --dist=loadgroup | Pass; record current selected/deselected/skipped counts | Pending |
| Shared development / final docs | Shared command block and local-link checks | Pass; final lock hash unchanged; all required evidence reconciled | Pending |

### Developer approval gate

- **Approval criteria:** T1/T2 complete; all M1 criterion evidence valid and required
  checks pass; explicitly distinguish M1 slice from whole #21 acceptance.
- **Evidence presented:** Pending — proposed docs/verification/us-15-ip4.md.
- **Remaining limitations or blocked work:** M2 AC-04; platform and milestone limits.
- **Developer decision:** Pending — request M1 slice acceptance explicitly.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — handoff only; do not close #21, start M2,
  commit/push/publish or remove worktrees without separate direction. Stop here.

## Final verification requirements

- **Owning final phase/task:** US-15-IP4-T2, required before final Gate 4 review.
- **Final implementation identity:** Pending — tested revision, dirty files,
  dependency/lock checksum and actual supplier revision.
- **M1–6 and shared checks:** Commands above, final results/counts Pending.
- **Distribution/installation:** Both real wheel paths in IP3 and combined
  US-26 integration. Standalone artifact drivers and broader pytest require an
  explicit developer command; they are not automatically launched.
- **Deferred-check reconciliation:** IP4-T2 owns all exclusions from IP2/IP3;
  no required failure/skip is evidence of acceptance. Historical failures/skips
  remain in their original owning plans.
- **Evidence renewal:** Renew affected focused/artifact evidence after changed
  inputs, and M1–6 after executable changes. Doc-only edits use document checks.
- **Actual results and limitations:** Pending; no executable verification performed
  during planning. Linux container paths were inspected; macOS/Windows unverified
  for this change. Environment setup and runtime behavior are not demonstrated.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-15-AC-01 | IP2-T1/T3/T4; IP3-T2; IP4-T2 | Independent train/held-out/inference oracle; both installed wheel paths | Pending |
| US-15-AC-02 | IP2-T2/T3/T4; IP3-T2; IP4-T2 | Scope/overlap/identity rejection before fitting, existing splitting regression | Pending |
| US-15-AC-03 | IP3-T1/T2/T3; US-26-IP4-T1/T2; US-15-IP4-T1/T2 | Exact metadata/native pipeline plus actual persisted code/dependency handoff | Pending |
| US-15-AC-04 | Future M2 owning plan | Fresh-project restored transformation equivalence under declared checks | Deferred M2; not accepted |

- **Remaining work:** All implementation tasks; AC-04 is a separate M2 slice.
- **Partial prerequisite delivery:** Gate 3 supplies verified fitting/metadata
  capability but does not complete AC-03 or accept this slice. Final M1 review
  follows US-26's actual integration. Whole #21 remains open for M2.
- **Final verification:** Pending — IP4-T2 report.
- **Developer acceptance:** Pending, M1 slice only.
- **Decision reference and date:** Pending.

## Milestone acceptance handoff

- **Owner:** MVP-M1-ACCEPT-VERIFY reconciles installed preservation and the later
  full classification/assistant integration. MVP-M2-ACCEPT-VERIFY owns AC-04
  restoration integration. Historical M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY remain.
- **Deferred checks:** Cross-component end-to-end classification, restored fitted
  transformations/DVC replay, manual assistant/editor evidence and unverified
  platforms remain with their owning stories; no historical deferral is closed.
- **Required evidence:** Owning milestone reconciles all deferrals and input
  identities; complete-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""`
  and standalone direct/rebuilt distribution checks only on explicit developer
  command or CI, under current policy. CI success does not establish local checks.
