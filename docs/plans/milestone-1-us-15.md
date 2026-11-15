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
- **Coordinated execution index:** [US-15 / US-26 order and proposed exact contract](milestone-1-us-15-us-26-execution-order.md).
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
expected. At the base there was no implemented fitted-pipeline helper or tracking export.
Native DVC M1 versioning and Git/wheel identity support are accepted in their
owning plans. Historical evidence is not a test run against this branch.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-15-US-26-CONTRACT-01 | Native fitted Pipeline + JSON dictionary; separate shared provenance; MLflow ownership | All dependent code | Interface direction accepted in both issue bodies/comments on 2026-11-14; exact fields/types and public boundaries approved at Gate 1 after SC-01 reconciliation. |
| Existing partitions, US-12 #19 | Both layouts, current source identity and memberships | IP2 | Implemented; [US-12 IP3/IP4 and Gates 1–4](milestone-1-us-12-assessment-splits.md), AC-02/03 accepted. No reopening or saved-file parser. |
| US-26 producer contract review | Same exact dictionary representation and serialization/error rules | IP2/IP3 | Both Gate 1 decisions approved the same SC-01 contract; IP3 retains field parity. |
| Native pipeline composition | clone/fit/transform supported imputer/scaler/encoder Pipeline/ColumnTransformer without replacement algorithms | IP2 | IP1 feasibility and Gate 1-reviewed matrix satisfied; IP2/IP3 native evidence passes. |
| MLflow preservation and provenance | Actual US-15 output is saved with committed references | IP4 / complete AC-03 | [US-26-IP4-T1/T2](milestone-1-us-26-recording.md#us-26--implementation-phase-4-installed-handoff-and-17-acceptance), consumer Gate 4 and reviewed combined revision required. No whole US-26 #33/#43 dependency. |
| Shared code available in consumer | Reviewed producer revision in US-26 branch | US-26 IP4 | Fulfilled: explicit developer integration authority and approved combined commit `3ffc7b4` are verified in IP4; no neighboring source imports. |
| Feature comparisons, US-14 #20 | Fixed validation comparisons | None in this plan | Separate owner; reviewed issue overlap does not transfer its criteria here. |
| AC-04 restoration | Fresh-project restored transformation checks/tolerances | Future M2 | Explicitly deferred by #21; MVP-M2-ACCEPT-VERIFY retains integration reconciliation. |

The current [verification policy](../development/verification.md#phase-and-story-verification)
supersedes stale current-milestone-at-gates prose in issue/design boilerplate.
Use focused tests/regressions plus shared checks; M1–6 only at slice acceptance.
No product scope conflict remains; IP1 feasibility and SC-01 concurrence resolved the contract questions.

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

Developer boundary confirmation: Gate 1 approved the refined matrix and final
SC-01 contract before the first executable behavior test. IP2/IP3 reused these
confirmed public boundaries.

## Plan review

- **Status:** Phase 3 Complete and Gate 3 Approved; awaiting Phase 4 prerequisites/direction.
- **Developer decision:** Gates 1–3 Approved; local Phase 3 commit authorized.
- **Decision reference and date:** 2026-11-14 coordination-session developer message:
  “i approve Gate 1 in both us-15 and us-26. commit the changes and start phase 2 in both stories”.
- **Requested plan changes:** SC-01 encoding revision approved; see scope history.
- **Implementation authorization:** Phase 1 execution and local commit authorized on
  2026-11-14 by “i approve phase 1; commit;”. This supersedes the earlier
  planning-only restriction for Phase 1. Gates 1/2 and Phase 2/3 authorization
  are recorded below. Subsequent developer direction authorizes Phase 4 and integration of the
  approved combined revision, as recorded below. US-15 Gate 4 and M1 AC-01/02/03 slice are Approved/Accepted; publication remains withheld.

## Scope-change history

### US-15-US-26-SC-01 — Native parameter encoding reconciliation

- **Date / decision:** 2026-11-14 UTC, Approved revision by developer
  “I accept your recommendation.” following the five-part contract-revision
  recommendation in this session. This does not approve either Gate 1.
- **Reason:** Effective defaults include SimpleImputer NaN and OneHotEncoder's
  numpy dtype class, contradicting finite-only JSON and callable rejection.
- **Scope:** Add narrow missing-value/dtype tags, full-metadata feasibility and
  explicit bounded skops choice; reconcile consumer findings and stale status.
  No acceptance criterion, public signature, milestone or product behavior is added.
- **Impact:** T2 native fitting observations remain valid, but its prior broad
  metadata-feasibility conclusion was incomplete. Renew encoding evidence under
  [revision report](../verification/us15-us26-contract-revision.md).
  T3 is now Complete after consumer adoption/renewed evidence and
  [explicit producer acknowledgement](../verification/us15-sc01-concurrence.md).
  Consumer T2/T3 were reopened and completed with renewed schema evidence;
  their earlier default serialization failure remains preserved.
- **Verification / gates:** Strict JSON on complete effective settings, literal
  tags, rejection boundaries, native MLflow metadata/model save/log/load, and
  document checks. No toolkit implementation/tests or installed integration
  acceptance is claimed. Both Gate 1 approvals and later phase authorization
  remain mandatory; M1–6, shared executable checks and installed integration
  retain their existing owners.
- **Resume point:** Joint technical reconciliation complete; present both
  Gate 1 results for explicit developer decisions before dependent work.

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

Check environment overrides before synchronization. Phase 1 authorization
covered its own environment setup; later phase execution remains unauthorized. Retain unique logs under
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
| US-15-IP1-T3 | Complete | Finalize proposed docs/preprocessing.md contract, this plan and shared index with US-26 owner | T2 and US-26-IP1-T1/T2 findings | Matching exact metadata keys/types, signature, supported M1 compositions, test matrix and file ownership ready for both Gate 1 reviews; neither story waits for the other's T3 | AC-01/02/03 |

### Verification and review evidence

Phase 1 execution: [initial evidence](../verification/us-15-ip1.md),
[SC-01 renewal](../verification/us15-us26-contract-revision.md) and
[producer acknowledgement of consumer concurrence](../verification/us15-sc01-concurrence.md).
T1/T2/T3 are Complete. Current producer contract and consumer index/contract
agree; independent consumer evidence checks the producer metadata. No sibling
edits or developer gate approvals are inferred.

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
| Contract/links/whitespace | Review fields against accepted issue direction; local-link scan; git diff --check | Matching types/ownership; links resolve | SC-01 adopted by consumer and acknowledged by producer; no interface differences; document checks passed |
| TDD applicability | Inspect diff | Contract/probes only; no new executable toolkit behavior requiring red | Confirmed: docs and local native probe only; no product/test code changes |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; both producers/consumers agree on exact
  contract, tests and schema; unresolved findings block dependent tasks.
- **Evidence presented:** [Producer Phase 1 evidence](../verification/us-15-ip1.md);
  [SC-01 renewal](../verification/us15-us26-contract-revision.md) and
  [joint reconciliation acknowledgement](../verification/us15-sc01-concurrence.md).
  T1–T3 technically Complete; developer approved both Gate 1 decisions.
- **Remaining limitations or blocked work:** All executable product behavior unverified.
- **Developer decision:** Approved, including paired US-26 Gate 1.
- **Decision reference and date:** 2026-11-14 coordination-session developer:
  “i approve Gate 1 in both us-15 and us-26. commit the changes and start phase 2 in both stories”.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP2 execution and local Phase 1 commit authorized;
  no push/publication. Stop at Gate 2 for explicit developer approval.

## US-15 / Implementation Phase 2: Fit only recorded training rows

- **Outcome:** Public fitted Pipeline usable unchanged on held-out/inference rows.
- **Entry conditions:** Both Gate 1 contract approvals; own IP2 execution authority.
- **Acceptance criteria advanced:** US-15-AC-01/02; AC-03 preliminary native state.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP2-T1 | Complete | Add first numeric train-only test in proposed tests/integration/test_preprocessing.py; add minimum fit_preprocessing in proposed src/agentic_ml/preprocessing/__init__.py through red/green | Gate 1 | Literal scaler values pass, returned native Pipeline works; valid minimum metadata follows approved contract | AC-01 |
| US-15-IP2-T2 | Complete | Add one invalid-membership/fit-scope case per red/green cycle; reuse create_partitions supplied mode; preserve source/record identity | T1 | Reject overlaps, unknown/duplicate/uncovered IDs, layout/feature/scope/source mismatches before affected fit | AC-02 |
| US-15-IP2-T3 | Complete | Add two-way, supplied string IDs, reordered/nondefault index, imputation and categorical matrix cases one vertical slice at a time | T2 | Public transform outputs match independent expectations; original input/pipeline/cwd preserved; native errors visible | AC-01/02 |
| US-15-IP2-T4 | Complete | Review structure, run focused/regression/shared commands, record proposed docs/verification/us-15-ip2.md | T3 | Valid red/green records, counts/platform/lock identity and all required results available | AC-01/02 |

### Verification and review evidence

[Phase 2 evidence](../verification/us-15-ip2.md) records all red/green cycles,
27 public preprocessing cases plus 124 splitting regressions (151 passed),
shared checks, source/lock/platform identities and remaining IP3/IP4 obligations.

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
| Red then green per case | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py -k <one-case-selector> | Red is missing/incorrect behavior; green matches unchanged oracle | Passed ten red/green cycles; numbered logs in IP2 report |
| Preprocessing and partition regressions | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py | Pass; no weakened tests; current counts recorded | 151 passed, 0 skipped/deselected, four loadgroup workers |
| Shared development checks | Exact shared command block above | Pass; lock unchanged; correct installed CLI version | All passed; CLI 0.1.0, mypy 79 files, Ruff format 325 files |

### Developer approval gate

- **Approval criteria:** T1–T4 complete with AC-01/02 focused/regression/shared evidence.
- **Evidence presented:** [IP2 report](../verification/us-15-ip2.md); all four tasks
  technically Complete; developer Gate 2 approval recorded below.
- **Remaining limitations or blocked work:** Metadata completion and persisted handoff.
- **Developer decision:** Approved for US-15; paired US-26 Gate 2 also approved.
- **Decision reference and date:** 2026-11-14 coordination-session developer:
  “for both us-15 and us-26 i approve the phase 2 gate, commit the changes.”
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Phase 2 committed at `104172a`. On 2026-11-14, the developer
  separately directed both stories to start Phase 3 (coordination thread
  `01a1db6c-a225-73e0-8796-81a03c4cec7a`). Only IP3 execution is authorized;
  stop at Gate 3. No Phase 4, push, publication or source integration.

## US-15 / Implementation Phase 3: Produce metadata and verify installed use

- **Outcome:** Complete schema/settings/membership record and independently verified
  producer capability available for US-26 integration, without MLflow dependency.
- **Entry conditions:** Gate 2 approved and execution authority for IP3.
- **Acceptance criteria advanced:** US-15-AC-01/02 verified as a component; AC-03 advanced.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP3-T1 | Complete | Complete recursive effective-settings/schema/version metadata and failure cases in preprocessing module/tests, one red/green behavior at a time | Gate 2 | Exact index fields/types, order/default retention, JSON finite values, declared width/dtype checks and unsupported-setting errors | AC-03; AC-01/02 regressions |
| US-15-IP3-T2 | Complete | Add proposed tests/installation/check_preprocessing.py, register in existing verify_assessment_splits.py and selected distribution integration test; exercise direct/rebuilt installed projects from unrelated cwd | T1 | Actual normal installs return native fitted object and exact JSON; both wheel paths independently pass; no MLflow store or dev-dependency leakage | AC-01/02/03 component |
| US-15-IP3-T3 | Complete | Finish runnable docs/preprocessing.md script, inspect baseline compatibility, focused/shared checks and proposed docs/verification/us-15-ip3.md | T2 | User script is the installed tested path; approved producer revision/API/schema and evidence identified for US-26 owner | AC-01/02/03 |

### Verification and review evidence

[IP3 evidence](../verification/us-15-ip3.md) records eight red/green slices,
243 focused passes (84 preprocessing, 124 splitting, 35 assessment), both real
installed artifact paths, exact metadata/guide identities and all shared checks.
Only Phase 3 was executed in this turn. Gate 3 approval and local commit direction are recorded below.

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
| Metadata + partition regression | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_data_assessment.py | JSON/native behavior and existing accepted partition contract pass | 243 passed, 0 skipped/deselected, four loadgroup workers |
| Installed direct and rebuilt wheel producer | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py -k test_assessment_splits_from_both_artifact_paths | Both independent installed paths pass, actual selected counts/name recorded | 1 passed (direct/rebuilt); 1 of 19 selected, 18 deselected |
| Shared development checks | Shared command block | Pass; no accidental lock/dependency changes | All passed; lock unchanged, CLI 0.1.0, mypy 80 files, format 328 files |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; actual installed producer capability ready,
  field parity with consumer confirmed, native and JSON evidence retained.
- **Evidence presented:** [IP3 report](../verification/us-15-ip3.md); T1–T3 technically Complete.
  Public native/JSON/installed evidence and static consumer-contract parity verified.
- **Remaining limitations or blocked work:** No Phase 3 blocker. AC-03 incomplete
  until US-26 IP4. Native float16 OneHotEncoder output remains unsupported by
  SciPy and fails visibly; no fallback or general dtype compatibility claimed.
- **Developer decision:** Approved; local Phase 3 commit authorized.
- **Decision reference and date:** 2026-11-14 coordination-session developer:
  “commit changes in both stories”. The coordination delegation explicitly
  records this as Gate 3 acceptance and commit authorization for each owning checkout.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Local Phase 3 commit only. No Phase 4, sibling source
  integration, push or publication. US-15 IP4 still waits for consumer Gate 4 and
  separately authorized integration; no M1 slice acceptance is claimed.

## US-15 / Implementation Phase 4: Review preservation and accept the M1 slice

- **Authorization and fulfilled dependencies:** Developer authorized US-26-first
  Phase 4 coordination, then explicitly directed “I approve us-26 gate 4 and
  authorize committing the combined revision so us-15 can complete”. Coordination
  thread `01a1db6c-a225-73e0-8796-81a03c4cec7a` authorized US-15 integration and
  dependent final checks. Verified committed consumer Gate 4 approval and combined
  revision `3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1`; fast-forwarded this branch
  without conflicts or executable edits. Own preparation preserved in raw records.
  This supersedes earlier Phase 3-only progression restrictions. Subsequent
  Gate 4 approval/M1 slice acceptance and local commit authority are recorded
  below; publication and M2 remain unapproved.

- **Outcome:** M1 AC-01–03 reconciled with real producer/consumer preservation evidence.
- **Entry conditions:** US-15 Gate 3; US-26-IP4-T1/T2 evidence and Gate 4 approved;
  authorized relevant integration available in this branch for final checks.
- **Acceptance criteria advanced:** US-15-AC-01/02/03 complete M1 slice; not AC-04.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-15-IP4-T1 | Complete | Inspect US-26-owned installed handoff evidence against this producer revision and AC-03; link it in proposed docs/verification/us-15-ip4.md, this plan and checkpoint | US-26 IP4 and Gate 4 | Actual pipeline, exact metadata and committed code/dependency links persisted in run; no fixture-only substitute | AC-03 |
| US-15-IP4-T2 | Complete | Reconcile all M1 criteria/deferred checks, run final M1–6 and shared commands, finish docs/checkpoint and report | T1 | Final identity/lock/dirty files/counts/platform recorded, excluded/failed/skipped checks accounted for before Gate 4 | AC-01/02/03 |

### Verification and review evidence

[IP4 report](../verification/us-15-ip4.md) records independent consumer-artifact
review, approved combined-source integration, renewed actual installed handoff,
924 passes/one existing skip in final M1–6, shared checks and criterion mapping.
T1/T2 are Complete; US-15 Gate 4 is Approved and its M1 slice Accepted by the
subsequent explicit developer decision below.

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
| Preservation evidence | US-26-IP4-T1/T2 report, tested combined revision and Gate 4 | Exact pipeline/metadata/provenance artifacts and native run references | Verified consumer Gate 4 approval; all 28 retained artifact/identity hashes and exact JSON/reference checks pass; renewed in own M1–6 |
| M1–6 story selection | uv run --locked pytest -n 4 --dist=loadgroup | Pass; record current selected/deselected/skipped counts | 924 passed, 1 existing skip, 0 failures/errors; 925 selected/268 deselected of 1193, four/loadgroup, 427.02 seconds |
| Shared development / final docs | Shared command block and local-link checks | Pass; final lock hash unchanged; all required evidence reconciled | All shared checks pass; final document checks in raw gate manifest; no lock changes |

### Developer approval gate

- **Approval criteria:** T1/T2 complete; all M1 criterion evidence valid and required
  checks pass; explicitly distinguish M1 slice from whole #21 acceptance.
- **Evidence presented:** [Completed IP4 report](../verification/us-15-ip4.md);
  T1/T2 technically Complete with final tests, installed preservation and shared checks.
- **Remaining limitations or blocked work:** No Phase 4 blocker; M2 AC-04,
  existing planning-schema skip, Linux-only coverage and named milestone limits remain.
- **Developer decision:** Approved; M1 AC-01/02/03 slice explicitly Accepted.
- **Decision reference and date:** 2026-11-15, developer adopted: “Approve US-15 Gate 4 and accept its M1 slice; commit its remaining changes. Accept US-26’s #17 scope. Prepare and explain the PR structure before pushing or publishing.”
  Relayed by coordination thread `01a1db6c-a225-73e0-8796-81a03c4cec7a`.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Commit remaining owning records locally and prepare
  a reviewable PR structure. Explicitly stop before push, PR/publication, main
  merge, issue closure, history rewrite/new PR branches or cleanup. #21 remains
  open for M2 AC-04; no whole #21 or milestone acceptance is implied.

## Final verification requirements

- **Owning final phase/task:** US-15-IP4-T2, required before final Gate 4 review.
- **Final implementation identity:** Combined `3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1`,
  approved supplier `e63ef4b8ff700d44e5c644dd30eed92ebd62104b`; all 83 tested
  executable fingerprints preserved. Final edits are this plan, checkpoint,
  coordination index, IP4 report and PR-structure proposal only. Lock hash unchanged; see IP4 report/manifest.
- **M1–6 and shared checks:** All passed; 924 passes, one existing authorized skip,
  zero failures/errors, 925 selected/268 deselected. Full results in IP4 report.
- **Distribution/installation:** Both real wheel paths in IP3 and combined
  US-26 integration. Standalone artifact drivers and broader pytest require an
  explicit developer command; they are not automatically launched.
- **Deferred-check reconciliation:** IP4-T2 owns all exclusions from IP2/IP3;
  no required failure/skip is evidence of acceptance. Historical failures/skips
  remain in their original owning plans.
- **Evidence renewal:** Renew affected focused/artifact evidence after changed
  inputs, and M1–6 after executable changes. Doc-only edits use document checks.
- **Actual results and limitations:** IP2/IP3 reports contain executable focused,
  installed and shared evidence on Linux aarch64/Python 3.12.16. IP4 final checks
  pass as recorded in the IP4 report; macOS/Windows are unverified for this change.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-15-AC-01 | IP2-T1/T3/T4; IP3-T2; IP4-T2 | Independent train/held-out/inference oracle; both installed wheel paths | Accepted M1 slice, 2026-11-15 |
| US-15-AC-02 | IP2-T2/T3/T4; IP3-T2; IP4-T2 | Scope/overlap/identity rejection before fitting, existing splitting regression | Accepted M1 slice, 2026-11-15 |
| US-15-AC-03 | IP3-T1/T2/T3; US-26-IP4-T1/T2; US-15-IP4-T1/T2 | Exact metadata/native pipeline plus actual persisted code/dependency handoff | Accepted M1 slice, 2026-11-15 |
| US-15-AC-04 | Future M2 owning plan | Fresh-project restored transformation equivalence under declared checks | Deferred M2; not accepted |

- **Remaining work:** Review the [PR-structure proposal](../reviews/us15-us26-pr-structure.md)
  before any publication; AC-04 remains a separate M2 slice.
- **Partial prerequisite delivery:** Actual US-26 integration and final US-15
  review now verify AC-03. M1 AC-01/02/03 are explicitly accepted;
  whole #21 remains open for M2.
- **Final verification:** Complete — [IP4-T2 report](../verification/us-15-ip4.md);
  924 passes, one existing skip, all shared checks and final evidence reconciled.
- **Developer acceptance:** Accepted M1 AC-01/02/03 slice only, 2026-11-15.
- **Decision reference and date:** Same explicit Gate 4/M1 slice decision above;
  no issue closure or publication authority.

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
