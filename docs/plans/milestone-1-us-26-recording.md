# Milestone 1 / US-26 #17: Record experiment runs in MLflow

## Scope and outcome

- **Milestone:** M1 — Complete one local classification experiment.
- **User story:** [US-26 recording / issue #17](https://github.com/jimthompson5802/agentic-ml/issues/17).
- **User-visible outcome:** A separate installed experiment project records native
  MLflow run status, parameters, supplied metrics, outputs and fitted preprocessing
  with traceable committed code/configuration, DVC data and locked environment
  references. Available failures remain inspectable and cannot count as successful
  output recording because a process exited zero.
- **Acceptance criteria covered:** [US-26-AC-01](../specs/user-stories.md#us-26-ac-01),
  [AC-02](../specs/user-stories.md#us-26-ac-02),
  [AC-03](../specs/user-stories.md#us-26-ac-03),
  [AC-04](../specs/user-stories.md#us-26-ac-04),
  [AC-05](../specs/user-stories.md#us-26-ac-05).
- **Scope boundaries:** Only #17's recording criteria; not the whole US-26 story.
  #33 owns comparison/report AC-06–09; #43 owns reverse lookup AC-12 and deferred
  auditing AC-10/11/13. No training/search/metric algorithm, workflow database,
  managed runner, mandatory runtime approval, automatic dirty-source replay,
  DVC stage/reproduction engine or broad notebook execution service.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
  [execution/tracking](../specs/design/execution-and-governance.md),
  [installed identities and notebooks](../specs/design/interfaces-and-configuration.md),
  [data/fitted artifacts](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts),
  [blueprint](../specs/design/software-blueprint.md#planned-mvp-responsibilities),
  [traceability](../specs/design/acceptance-traceability.md),
  [delivery order](../specs/design/milestone-delivery.md#capability-order-and-owning-stories),
  [layout](../specs/design/repository-layout.md),
  [ADR-008 and installation decisions](../specs/design/architecture-decisions.md).
- **Coordinated execution index:** [Order, overlap and proposed exact contract](milestone-1-us-15-us-26-execution-order.md).
  This plan owns the shared index. Review its exact record/provenance fields and
  proposed public signatures with [US-15's plan](../../../US-15-preprocessing/docs/plans/milestone-1-us-15.md).
  Cross-worktree links are intentional for local planning; rewrite during
  separately authorized integration rather than duplicating task ownership.

## Workspace association

- **GitHub issue and story:** #17 / US-26 recording; numbers are different.
- **Branch:** US-26-mlflow.
- **Base ref and starting commit:** local main,
  1a9864a645084af8cfcec580b1db5fa045a67859.
- **Worktree:** .worktrees/US-26-mlflow, relative to primary checkout.
- **Observed creation:** New branch/worktree, clean at creation on 2026-11-14.
  No fetch/pull or current remote comparison; no environment created. The existing
  primary-checkout checkpoint change was preserved, not copied here.

Follow [worktree guidance](../development/worktrees.md). Resume in this story's
own execution session/environment; inspect association, edits, supplier revisions,
evidence and gates. Workspace creation does not start implementation.

## Source snapshot and current state

#17 complete body/all comment pages were retrieved on 2026-11-14. Two unique
comments matched count 2, final updated_at remained 2026-11-14T18:07:56Z. Open
issue, enhancement label, no assignees, null GitHub milestone; body assigns
AC-01–05 to M1. Comments by jimthompson5802 record
[scope disposition 6699587594](https://github.com/jimthompson5802/agentic-ml/issues/17#issuecomment-6699587594)
and [CONTRACT-01 decision 6881962234](https://github.com/jimthompson5802/agentic-ml/issues/17#issuecomment-6881962234).
Complete snapshots of #21/#19/#16/#20/#33/#43/#58/#64 and their comments were
also retrieved and refreshed; counts/completeness are recorded in the index.
Raw metadata/body/comment exports reside locally in
.dev-records/verification/20261114-us15-us26-planning/issues.json.

At the base there is no tracking module or matching #17 plan. Existing
src/agentic_ml/initialization/storage.py initializes local MLflow SQLite/artifact
storage but supplies no experiment-recording API. Existing identity.py validates
Git and retained-wheel identities; these internal helpers are not experiment
exports. src/agentic_ml/splitting/__init__.py returns an existing plain 1.0 record.
The [native DVC recipe](../dataset-versioning.md) is accepted for M1 US-13 #16,
including data/split metadata and committed content versions. Reuse these native
records, not a second run or data identity service.

Runtime dependencies already include MLflow 3, DVC 3, sklearn, pandas/pyarrow,
nbclient/nbformat and packaging. Contributor lock records MLflow 3.17.2,
DVC 3.67.1, sklearn 1.9.1. New dependencies are not expected. Direct/rebuilt-wheel
testing already exists in tests/integration/test_distribution_verification.py
and contributor installation drivers. No product test was run during planning.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-15-US-26-CONTRACT-01 | Native pipeline/plain metadata, separate provenance, MLflow ownership | Dependent implementation | Direction accepted in #17/#21 on 2026-11-14; exact SC-01 contract and boundaries in index approved at both Gate 1 decisions. |
| Native MLflow serialization/artifact behavior | Existing-run logging with exact preprocessing/pipeline, metadata and provenance paths under locked MLflow 3.17.2 | IP2/IP3 | [IP1 findings](../verification/us-26-recording-ip1.md) confirm existing-run layout; SC-01 adopts explicit numpy.dtype trust; renewed consumer feasibility passes; both Gate 1 decisions Approved. |
| Existing DVC data/splits, US-13 #16 M1 | Real pointer/hash/data links, no fake SHA-as-DVC identity | IP2, IP4 | [US-13 IP2/IP3, Gate 3 and M1 acceptance](milestone-1-us-13.md); do not require M2 restoration. |
| Git/wheel identity, US-41 #64 | Preserve normal installed origin, lock and artifact identity | IP2/IP4 | [Accepted US-41 plan](milestone-50-us-41.md); Git source SHA required when applicable, unavailable wheel SHA/build remains explicit null. |
| Real US-15 producer | fit_preprocessing output with final reviewed metadata/schema | IP4 only | [US-15-IP3-T1/T2 and Gate 3](../../../US-15-preprocessing/docs/plans/milestone-1-us-15.md#us-15--implementation-phase-3-produce-metadata-and-verify-installed-use) required. IP2/IP3 use independently fitted fixture and do not wait for US-15 completion. |
| Branch availability | Approved producer source integrated into consumer branch | IP4 | Separate integration direction needed. Do not import another worktree, copy live files or silently merge/rebase. |
| Notebook artifact | Already executed notebook + committed source reference | IP2/IP4 | Native nbclient fixture creates fresh-kernel outputs/errors; US-09/39 workflow delivery remains separate. |
| #33/#43, US-14 #20, US-39 #58 | Keep ownership boundaries for reports/comparisons/basic path/assistant | None for component implementation | Complete discussions reviewed; consumers of recording, not whole-story prerequisites. No additional story implementation in this plan. |

The index resolves older generic current-milestone-at-gates wording using the
newer [verification policy](../development/verification.md#phase-and-story-verification)
and current AGENTS.md. Focused/regression/shared gate checks preserve product
criteria; no issue scope change is inferred. Unresolved native feasibility stays
bounded in IP1, with dependent work conditional on reviewed findings.

## Proposed public interfaces and test boundaries

Proposed exports: agentic_ml.tracking.log_preprocessing and log_run_results,
with exact signatures, return fields, paths, failure semantics and provenance
representation in the [coordination index](milestone-1-us-15-us-26-execution-order.md#proposed-public-boundaries).
MLflow run_id is the only run identifier. Use an explicit tracking URI/client
and project_root; do not depend on ambient active run or cwd. No custom run store.

Execution code creates a native MLflow run and supplies committed experiment
provenance once. Both helpers reuse provenance.json; conflicting input fails.
log_preprocessing saves the native fitted object plus metadata. log_run_results
records supplied parameters/metrics/files, preserves executed notebooks when
used, checks named required outputs and records terminal native status with
separate process-exit/configured-validation information. Missing references,
serialization/logging failures and missing outputs remain visible and cannot
return success. Native metrics are recorded, not computed or scientifically
certified. Native parameter immutability is retained; no silent conflicting update.

Developer confirmation of these public test boundaries was given at Gate 1
on 2026-11-14, including SC-01; the exact decision is recorded below. Proposed tests
invoke the installed/public helpers then inspect native MlflowClient records and
downloaded artifacts, compare JSON/bytes with independent inputs and actual
Git/DVC/lock metadata, and check exceptions/available diagnostics. Do not test
private helper calls or use a mocked internal logging sequence as success evidence.
External storage failure may be induced through a controlled unavailable artifact
destination; serialization failure through a minimal independently fitted object
whose native serialization fails. IP1 must confirm a deterministic failure
fixture rather than weakening error assertions or relying on privileged-user
permission bits. Use native storage/client fault injection only at the public
external-library boundary if filesystem simulation is unreliable, and disclose
that limit. Independent real-store success and installed integration remain required.

| Public case | Independent expected result | Criterion / limit |
|---|---|---|
| Existing run, params {C:1}, metric {validation_accuracy:0.75}, required predictions file | Same run ID; exact parameter/metric values, downloadable file bytes and native artifact locations; terminal FINISHED | AC-01/05; does not certify model quality |
| Process exit 0 with missing predictions | FAILED recording/output outcome and raised contextual error despite exit 0; available stdout/stderr files retained | AC-05 |
| Nonzero process and available partial outputs/logs | Native FAILED with true exit code; available files preserved; no completed-success return | AC-01/05; no forced-kill guarantee |
| Process success, outputs present, configured validation_passed=False | Process completion remains distinct from validation_status failed; no success/quality conflation | AC-01/05 |
| Real DVC dataset/split + committed entrypoint/config + effective settings | provenance.json fields and native run tags/links agree with independently read Git blobs, DVC metadata and current consumed bytes | AC-02/04 |
| Git identity and wheel identity matrix | Full Git SHA/origin/version when applicable; supported wheel retains locked digest/version/payload evidence with unavailable source/build fields null | AC-03; no fabricated source identity |
| Wrong metadata type/version/NaN, missing file, dirty declared code/config/lock, wrong DVC hash/member, conflicting shared provenance | Clear failure before successful publication; existing run/artifacts inspectable, no overwrite or silent fallback | AC-02/03/04/05 |
| Independent fitted scaler and representative preprocessing record | Native MLflow pipeline directory plus exact metadata and shared provenance, linked to requested existing run | AC-01/02/03; not producer-fit correctness |
| Unfitted/incompatible object or real serialization/storage failure | Raised error with run/stage/context and retained available diagnostics; no misleading successful artifact return | AC-05 |
| Two local stores / different ambient active run / unrelated cwd | Only explicitly selected run/store changes; project-relative references resolve from project_root | AC-01/02/05 |
| Executed notebook success/error fixtures | Logged supplied notebook retains outputs/error cells and committed notebook reference; failed process remains failed | AC-04/05; no general notebook runner acceptance |
| Actual US-15 output in both installed wheel paths | Exact producer metadata/native artifact preserved with real DVC/code/config/environment links | Joint AC-03 evidence for US-15; US-26 AC-01–05 |

## Plan review

- **Status:** Phases 1 and 2 approved; Phase 3 is not authorized.
- **Developer decision:** Gate 1 Approved by the coordination-session instruction recorded below.
- **Decision reference and date:** 2026-11-14 coordination-session approval of both Gate 1 decisions, recorded in the IP1 gate below.
- **Requested plan changes:** SC-01 encoding/serialization reconciliation adopted; see scope-change history.
- **Implementation authorization:** US-26 IP1 authorized on 2026-11-14 by
  developer message “i approve phase 1; commit”. This supersedes the earlier
  prohibition on starting IP1. Commit of the planning documents is authorized.
  IP1 execution was reaffirmed by “start phase 1”. T1–T3 were technically
  Complete before SC-01; T2/T3 were reopened and are Complete again with
  [renewed evidence](../verification/us26-sc01-concurrence.md). Gate 1 remains Pending.
  No US-15 execution or later phase is authorized by this decision.

## Scope-change history

### US-15-US-26-SC-01 — Native parameter encoding reconciliation

Developer accepted the joint revision on 2026-11-14: “I accept your
recommendation.” Add exact native missing-value/dtype parameter tags and
complete-metadata feasibility; adopt bounded skops configuration. Signatures,
criteria, milestone assignments, integration ownership and gates are unchanged.
Producer [evidence](../../../US-15-preprocessing/docs/verification/us15-us26-contract-revision.md)
confirms complete JSON and native persistence, not toolkit validator acceptance.
Earlier native transforms and default skops failure remain valid historical
observations; broad metadata-feasibility conclusions need renewal. IP1-T2/T3
were reopened for this owning session's schema/probe/document verification.
US-26 adoption was explicitly authorized by the developer-directed SC-01 handoff
(contract reconciliation only; no gate approval, IP2, commit or publication).
The [renewal/concurrence](../verification/us26-sc01-concurrence.md) now completes
that verification: US-26 explicitly concurs with the exact producer SC-01
revision; no unresolved interface differences remain. US-15 retains ownership
of finalizing its T3/records. Signatures, criteria and verification gates stay
unchanged; both gates remain Pending and no IP2 authorization is inferred.

## Execution and verification rules

Use one public-interface test per vertical red/green slice; confirm red is the
intended missing/incorrect behavior, implement minimum green, run relevant
regressions, then proceed to the next case. Refactor only while green. Record
exact commands and selected/deselected/collected counts, actual outcomes,
revision/dirty files, lock identity, installed library versions and platform.
Tasks become Complete only with passing evidence, independently of gate approval.
Reopen affected tasks if later changes invalidate evidence.

Stop after every implementation phase, including final, and present evidence,
limitations and deviations for explicit developer approval. Plan approval neither
starts execution nor approves a phase's work. Follow the index and check supplier
evidence/approvals/source availability. Pause dependent work when new scope or an
invalidated approach requires manage-plan-scope; obtain decisions before new
prerequisite implementation. Follow the three-attempt limit in AGENTS.md,
preserving hypothesis/change/verification evidence and stopping after the third
failure. Never lower thresholds, weaken tests, hide failures or add unauthorized
skips/suppressions/workarounds.

Shared commands at executable phase gates, from this story's own environment:

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

Before sync inspect UV_PROJECT_ENVIRONMENT/VIRTUAL_ENV and other uv overrides
so this story cannot use another editable environment. Setup needed for the
authorized IP1 probes is permitted. Preserve records under this checkout's .dev-records/verification/ under the
[records policy](../development/records.md); each store/log/temp base is exclusive.
Use small local fixtures, no external datasets/credentials, existing fixture
retention/groups/timeouts and four-worker loadgroup. Short serial TDD uses the
documented policy exception only with a recorded reason. New product tests
are milestone_1 by directly verified requirements; contributor-only checks are
infrastructure. No standalone driver or broader suite runs without explicit command.

## US-26 / Implementation Phase 1: Confirm native artifact and provenance contract

- **Outcome:** Feasible existing-run MLflow paths/identity handling and confirmed
  exact shared contract/public test matrix before production code or behavior tests.
- **Entry conditions:** Separate IP1 execution authorization; complete current issue
  refresh; verified own branch/checkpoint and US-15 contract coordination.
- **Acceptance criteria advanced:** US-26-AC-01–05 design only; none verified.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-26-IP1-T1 | Complete | Reconcile #17/#21 contract, this index, native DVC recipe and accepted installation identity code | Authorization | Exact reference/type/path/error matrix; no extra split/run store or contradictory distribution SHA rule | AC-01/02/03/04/05 |
| US-26-IP1-T2 | Complete | Inspect installed locked MLflow/sklearn APIs; native-only save_model/client-log/download/load probes in isolated store; inspect Git/wheel identity access and deterministic failure fixture | T1 | Actual run artifact layout and namespace, native error/context behavior and identity reuse approach recorded in proposed docs/verification/us-26-recording-ip1.md; no product module or behavior tests yet | AC-01/03/05 |
| US-26-IP1-T3 | Complete | Finalize proposed docs/experiment-tracking.md contract, this plan/index, paired US-15 schema/test boundaries | T2 and US-15-IP1-T1/T2 findings | Reviewable runnable-script outline, exact schemas/signatures, native failure fixture and integration ownership; resolve feasibility findings before dependent code; neither story waits for the other's T3 | AC-01/02/03/04/05 |

### Verification and review evidence

- **SC-01 renewal:** [Explicit consumer concurrence](../verification/us26-sc01-concurrence.md) verifies full effective settings, canonical tags and native persistence; T2/T3 re-completed, no product validator acceptance claimed.

- **IP1 evidence:** [Native findings and source reconciliation](../verification/us-26-recording-ip1.md), 2026-11-14. T1–T3 technically complete; both Gate 1 reviews remain pending.

- **Selected tests and impact rationale:** Bounded native library probes only;
  documentation/link/whitespace checks. No executable toolkit behavior changes,
  so TDD red and full executable checks do not apply to this contract-only phase.
- **Public boundaries and limits:** Confirm exact index APIs/schema and matrix at
  Gate 1. Native feasibility is not implementation success evidence.
- **Deferred checks:** Behavior TDD IP2/IP3; installed actual handoff IP4;
  all final/excluded regression reconciliation US-26-IP4-T3.
- **Acceptance schedule:** No complete milestone run at this gate.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Existing-run/native artifacts and failure feasibility | Exact native commands/stdout/stderr retained in proposed IP1 report | Layout feasible; explicit run/store selected; failure fixture deterministic | Pass with SC-01 bounded serialization configuration; renewed complete-metadata probe passes; original default failure retained |
| Metadata/reference/identity parity | Field-by-field index and accepted source-contract inspection | No drift from CONTRACT-01 or supported Git/wheel identity | Pass: prior issue refresh plus SC-01 full-metadata consumer comparison; both gate reviews pending |
| Documentation review | Local-link scan and git diff --check | Links/whitespace pass; pending findings explicitly block code | Pass: document validation recorded in IP1 report/raw records |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; native artifact feasibility and provenance
  semantics confirmed; both story Gate 1 reviews agree on shared contract.
- **Evidence presented:** [IP1 report](../verification/us-26-recording-ip1.md), [SC-01 concurrence](../verification/us26-sc01-concurrence.md) and [tracking contract](../experiment-tracking.md).
- **Remaining limitations or blocked work:** All product behavior unimplemented/unverified.
- **Developer decision:** Approved.
- **Decision reference and date:** 2026-11-14, coordination-session developer: “i approve Gate 1 in both us-15 and us-26. commit the changes and start phase 2 in both stories”. Source thread 01a1db6c-a225-73e0-8796-81a03c4cec7a; relayed to this owning session.
- **Requested changes and resolution:** SC-01 complete; exact tag/schema and bounded serialization concurrence recorded in the renewal report.
- **Progression authorized:** US-26 IP2 authorized by the same instruction. Paired US-15 Gate 1 Approved by that exact decision; its owner records it separately. Stop at Gate 2; no push/publication.

## US-26 / Implementation Phase 2: Record results with committed provenance

- **Outcome:** Existing native run receives supplied results, committed references,
  output checks and notebook artifacts with truthful completion/failure behavior.
- **Entry conditions:** Both Gate 1 contract approvals and own IP2 authority.
- **Acceptance criteria advanced:** US-26-AC-01/02/03/04/05, without preprocessing integration.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-26-IP2-T1 | Complete | First native-run/results test in proposed tests/integration/test_tracking.py, then minimum log_run_results in proposed src/agentic_ml/tracking/ through red/green | Gate 1 | Explicit existing run, exact parameters/metrics/files/URI and required zero-exit successful-output case recorded | AC-01/05 |
| US-26-IP2-T2 | Complete | Add committed Git/config/DVC/split/environment reference cases and validation one behavior at a time; use existing identity implementation internally where appropriate | T1 | Actual committed blobs/pointers and installed origins verified; provenance.json matches separate supplied dictionary; missing/mismatch/dirty declared-reference failures | AC-02/03/04 |
| US-26-IP2-T3 | Complete | Add process/output/configured-validation, explicit-store/cwd and already-executed notebook success/error cases through red/green | T2 | Missing output despite exit 0 fails; nonzero process preserves diagnostics; configured validation distinct; notebook outputs/error cells and committed reference saved | AC-01/04/05 |
| US-26-IP2-T4 | Complete | Review module boundaries, run focused/regression/shared checks and save proposed docs/verification/us-26-recording-ip2.md | T3 | Criterion-mapped red/green records and native inspection evidence with counts/lock/platform; no initializer API change | AC-01/02/03/04/05 |

### Verification and review evidence

[Phase 2 evidence](../verification/us-26-recording-ip2.md) records completed T1–T4, vertical red/green evidence and retained failed/corrected verification. Final four-worker tracking/DVC regression: 68 passed, zero failed/skipped/deselected, 168.01 seconds. Shared and document checks pass; Gate 2 was subsequently Approved by the decision recorded below.

- **Selected tests and impact rationale:** New public tracking results tests;
  existing native dataset-versioning tests protect DVC reference assumptions.
  If private installation identity code changes, run all current public
  initialization tests plus wheel identity/upgrade tests explicitly selected
  with -m "milestone_1 or milestone_50"; this is a focused affected regression
  selection, not a full M50 run. Do not change existing contracts for convenient reuse.
- **Public boundaries and limits:** Helpers plus native client/Git/DVC inspectors;
  no training, metric calculation, complete source capture or durable recovery.
- **Deferred checks:** Preprocessing serialization/failure IP3; actual installed
  producer handoff and final regressions US-26-IP4-T1/T2/T3.
- **Acceptance schedule:** Focused/regression + shared checks, no full M1 suite.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Red/green selected behavior | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_tracking.py -k <one-case-selector> | Intended red then green, unchanged independent expectations | Numbered raw red/green logs and commands.json; native exception fixture corrections and initial failures retained |
| Results/provenance/DVC regressions | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_tracking.py tests/integration/test_dataset_versioning.py | Real records and mismatch/failure matrix pass | Pass: final 68/68 with 4 workers/loadgroup, focused-final.log/XML; initial two failed invocations preserved |
| Identity impact if internals change | uv run --locked pytest -n 4 --dist=loadgroup -m "milestone_1 or milestone_50" tests/integration/test_initialization.py tests/integration/test_distribution_initialization.py | Git/wheel initialization/upgrades preserved; actual counts/conditional reason recorded | Not applicable: no private identity code changed; native normal wheel/Git initialization is exercised in the component fixtures |
| Shared development checks | Exact shared command block | Pass; unchanged lock or reviewed intentional change | Pass: sync/lock, lint, formatting (324 files), typing (83 files), CLI 0.1.0, whitespace; uv.lock SHA-256 unchanged |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; run records/links/notebooks and distinct
  failures demonstrated, public regressions/shared checks pass.
- **Evidence presented:** [Phase 2 report](../verification/us-26-recording-ip2.md); final focused XML/log, shared checks and document/source identities under .dev-records/verification/us26-ip2-20261114/.
- **Remaining limitations or blocked work:** Fitted preprocessing and actual handoff.
- **Developer decision:** Approved.
- **Decision reference and date:** 2026-11-14 UTC, developer in coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a, relayed to this owning session: “for both us-15 and us-26 i approve the phase 2 gate, commit the changes.” Paired US-15 Gate 2 approval is recorded by this same decision; its owning session maintains its records.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Local commit of Phase 2 changes and approval records only. Phase 3, push/publication, integration and cleanup are not authorized; await separate direction.

## US-26 / Implementation Phase 3: Persist fitted preprocessing and recording failures

- **Outcome:** Existing run owns fitted native pipeline, exact metadata and shared
  provenance at reviewed paths; invalid/partial recording cannot return success.
- **Entry conditions:** Gate 2 approval and own IP3 execution authority. Does not
  require actual US-15 implementation; use independently fitted representative fixture.
- **Acceptance criteria advanced:** US-26-AC-01/02/03/04/05 component evidence.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-26-IP3-T1 | Not started | First independently fitted pipeline recording test; minimum log_preprocessing via native MLflow save/log operations in tracking module | Gate 2 | Native run artifact paths pipeline/metadata/provenance exact; same run_id and JSON/effective settings retained | AC-01/02/03 |
| US-26-IP3-T2 | Not started | Add wrong metadata/fit declaration/schema/split linkage, required-reference and artifact-conflict cases individually through red/green | T1 | Invalid handoff rejected; shared provenance reused identically; conflict cannot overwrite prior artifacts | AC-02/03/04/05 |
| US-26-IP3-T3 | Not started | Add reviewed deterministic serialization/logging failure and unavailable diagnostics cases individually through red/green | T2 | Native exceptions/context and available partial artifacts preserved; neither helper claims successful recording after failure | AC-01/05 |
| US-26-IP3-T4 | Not started | Complete docs/experiment-tracking.md runnable public script, focused/shared verification and proposed docs/verification/us-26-recording-ip3.md | T3 | Script uses native existing run and separate provenance, no producer/import dependency; full independent consumer matrix passes | AC-01/02/03/04/05 |

### Verification and review evidence

- **Selected tests and impact rationale:** Entire public tracking matrix includes
  IP2 regressions because shared provenance/output code is affected. Splitting
  regression checks representative record assumptions; no private US-15 imports.
- **Public boundaries and limits:** Independent native object and representative
  metadata are necessary consumer evidence, not actual producer integration or
  proof metadata declarations describe correct fitting.
- **Deferred checks:** Actual installed handoff both wheel paths to IP4-T1/T2;
  all excluded regressions/current M1–6 to IP4-T3. US-15 AC-04 stays M2.
- **Acceptance schedule:** Focused + shared; no full current milestone run.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Independent consumer and failures | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_tracking.py tests/integration/test_splitting.py | Exact artifacts/settings/schema; clear errors and diagnostics; native records inspectable | Pending |
| Red/green each new case | Same command with appropriate one-case -k selector | Intended failure before minimal fix, then passing unchanged oracle | Pending |
| Shared development checks | Exact shared command block | Pass; no regression or silent lock change | Pending |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; native serialization/path and failure
  evidence retained; required focused/regression/shared results valid.
- **Evidence presented:** Pending — proposed docs/verification/us-26-recording-ip3.md.
- **Remaining limitations or blocked work:** Actual US-15 installed handoff and acceptance.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — IP4 after supplier US-15 Gate 3 and source
  availability; stop here even if producer is already ready.

## US-26 / Implementation Phase 4: Installed handoff and #17 acceptance

- **Outcome:** Real producer output works through installed consumer and native
  stores; all five #17 recording criteria have final evidence. Supply US-15 AC-03.
- **Entry conditions:** Own Gate 3; US-15-IP3-T1/T2 evidence and Gate 3; reviewed
  approved producer revision incorporated through separately authorized integration.
  Reconcile shared fixture/checkpoint edits; recheck complete issues/contracts.
- **Acceptance criteria advanced:** US-26-AC-01–05 complete #17 slice;
  US-15-AC-03 preservation evidence supplied, not independent US-15 acceptance.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-26-IP4-T1 | Not started | Add proposed tests/integration/test_preprocessing_tracking.py and project-owned tests/installation/tracking_project.py/check_tracking.py; actual fit_preprocessing output goes to both tracking helpers | Own Gate 3, US-15 Gate 3 and source availability | Real independent scaler oracle before logging; exact returned metadata persisted, native artifacts loadable, DVC/code/config/lock/identity links agree; no neighboring checkout imports | AC-01/02/03/04/05; supplies US-15-AC-03 |
| US-26-IP4-T2 | Not started | Add proposed tests/installation/verify_tracking.py using existing distribution/evidence support, and installed matrix in test_preprocessing_tracking.py; execute same documented script on direct and genuinely sdist-rebuilt wheels | T1 | Each normal install in separate project/environment with runtime-only dependencies, unrelated cwd, separate native stores, notebook/error/reference failures and intact CLI/import/resources | AC-01/02/03/04/05; supplies US-15-AC-03 |
| US-26-IP4-T3 | Not started | Run final focused handoff, M1–6 and shared checks; reconcile criteria/exclusions and docs/checkpoint in proposed docs/verification/us-26-recording-ip4.md | T2 | Final combined implementation/build/lock identities, platform/counts, supplier revision and deferred ownership ready before Gate 4/#17 acceptance | AC-01/02/03/04/05 |

### Verification and review evidence

- **Selected tests and impact rationale:** Joint installed matrix owns actual
  producer/consumer preservation; unit/component fixtures cannot substitute.
  Each wheel originates in the same reviewed combined source; rebuilt path is
  rebuilt from extracted sdist, never a renamed direct wheel. Separate projects
  contain their own code/config/lock/Git/DVC/MLflow state. Match input/source,
  JSON settings/membership, native pointer IDs and Git blobs independently.
- **Public boundaries and limits:** Installed public imports, native MLflow client,
  normal runtime dependencies. Artifact download/load verifies readable fitted
  object preservation; no fresh-project restored numerical equivalence or DVC
  replay claimed under US-15 AC-04. Fresh-kernel tiny notebook fixture checks
  notebook artifact preservation, not full US-09/39 UX/editor/assistant acceptance.
- **Deferred checks:** IP4-T3 owns all earlier required regression exclusions;
  broader/standalone and separate milestone/manual/platform obligations remain named.
- **Acceptance schedule:** M1–6 plus shared checks on final inputs; renew after
  executable changes. No automatic complete-suite or standalone artifact runs.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Actual installed producer/consumer matrix | uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing_tracking.py tests/integration/test_tracking.py | Direct/rebuilt paths independently pass; artifacts and metadata/refs match actual producer and independent oracle | Pending |
| M1–6 story acceptance | uv run --locked pytest -n 4 --dist=loadgroup | Final #17 changes pass; actual collected/selected/deselected/skipped outcomes recorded | Pending |
| Shared development and document checks | Shared command block; local-link check; review actual documented project script | Pass; lock hash preserved; docs execute the same supported path | Pending |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; all five #17 criteria verified, final
  shared/M1–6 checks and real integration evidence valid; explicitly request
  acceptance of #17's recording slice, not the entire US-26 story.
- **Evidence presented:** Pending — proposed docs/verification/us-26-recording-ip4.md.
- **Remaining limitations or blocked work:** #33/#43 criteria, US-15 M2 restoration,
  full MVP integration and unverified platforms remain outside this acceptance.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — supply evidence to US-15 IP4; stop here.
  No other story execution, issue closure, publication, commit/push, merge/rebase
  or worktree removal is authorized by completing the phase.

## Final verification requirements

- **Owning final phase/task:** US-26-IP4-T3, before final Gate 4.
- **Final implementation identity:** Pending — combined tested revision/dirty files,
  wheel/sdist/rebuilt identities, source supplier revision, lock SHA before/after.
- **M1–6 and shared checks:** Exact blocks above; actual counts/results Pending.
- **Distribution/installation:** Direct and genuinely rebuilt normal installs in
  IP4-T2, runtime-only environments outside toolkit checkout; retain Git and wheel
  identity coverage. Selected pytest may call artifact drivers; standalone drivers
  and all-tests/broader runs require explicit developer commands.
- **Deferred-check reconciliation:** IP4-T3 accounts for all required phase
  exclusions, failures, temporary skips and actual outcomes; no required failure
  may silently pass into acceptance. Preserve historic evidence/owners.
- **Evidence renewal:** Renew affected installed-artifact checks when code/build/
  resource/lock inputs change; renew M1–6 after executable edits. Documentation-only
  edits use appropriate link/whitespace checks, not a manufactured TDD failure.
- **Actual results and limitations:** Final product verification Pending. IP1 and
  SC-01 record native-library feasibility in the own locked environment; no
  product behavior tests, build or installed integration ran. Linux aarch64
  feasibility does not establish macOS/Windows support or AC acceptance.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-26-AC-01 | IP2-T1/T3/T4; IP3-T1/T3; IP4-T1/T2/T3 | Native existing-run parameters/metrics/status/outputs/artifact URIs and stable run ID | Pending |
| US-26-AC-02 | IP2-T2; IP3-T1/T2; IP4-T1/T2/T3 | Actual DVC data/split IDs, committed revision and effective configuration preserved | Pending |
| US-26-AC-03 | IP2-T2; IP3-T1/T2; IP4-T1/T2/T3 | Git/full-SHA and supported-wheel identity matrix; installed versions and lock/environment evidence | Pending |
| US-26-AC-04 | IP2-T2/T3; IP3-T2; IP4-T1/T2/T3 | Committed source/entrypoint/config references plus executed notebook outputs/errors when used | Pending |
| US-26-AC-05 | IP2-T1/T3; IP3-T2/T3; IP4-T1/T2/T3 | Missing outputs despite zero exit, nonzero process, invalid refs and serialization/logging failure cases | Pending |

- **Remaining work:** IP2–IP4 and Gate 1 review; #33/#43 remain separately owned.
- **Partial prerequisite delivery:** IP3 supplies independently verified consumer;
  only IP4 supplies actual US-15 preservation evidence. Neither accepts US-15 by
  proxy or claims full classification/assistant workflow delivery.
- **Final verification:** Pending — US-26-IP4-T3.
- **Developer acceptance:** Pending — #17 slice only; whole US-26 not claimed.
- **Decision reference and date:** Pending.

## Milestone acceptance handoff

- **Owner:** MVP-M1-ACCEPT-VERIFY for real classification, reporting, DVC stages
  and assistant integration; MVP-M2-ACCEPT-VERIFY for restoration/reproduction.
  Historical M1-ACCEPT-VERIFY/M50-ACCEPT-VERIFY obligations remain unchanged.
- **Deferred checks:** Later #33/#43 reporting/lookup evidence, US-39/40 assistant
  and replay checks, custom/regression/notebook UX and additional platforms retain
  their own plans. No historical failure/skip is removed by this plan.
- **Required evidence:** Reconcile final identities and every deferred obligation;
  full-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, shared checks
  and standalone direct/rebuilt artifact/installation verification only under
  explicit developer command or CI. CI evidence is not an unperformed local check.
