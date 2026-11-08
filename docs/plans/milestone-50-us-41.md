# Milestone 50 / US-41: Initialize experiments from a package distribution

## Scope and outcome

- **Milestone:** 50 — Improve the technical environment.
- **Owning issue:** [US-41 #64](https://github.com/jimthompson5802/agentic-ml/issues/64), open, enhancement. Retrieved complete body and all comment pages on 2026-11-08: zero comments; refreshed metadata confirmed unchanged `updated_at=2026-11-08T18:02:47Z` and count zero.
- **User-visible outcome:** A scientist installs a normal wheel dependency in a separate Git/Python project, initializes through installed CLI or Python, reruns safely, and explicitly upgrades while retaining verifiable artifact identity.
- **Acceptance criteria:** All [US-41-AC-01–06](../specs/user-stories.md#us-41-initialize-experiments-from-a-package-distribution), unchanged from the issue. No criterion is deferred.
- **Included:** Distribution identity, bootstrap, US-02 scaffolding/environment/local stores, compatible reruns, explicit upgrades, both wheel paths and full-SHA Git regressions.
- **Excluded:** Index publication/hosting, arbitrary dependency forms, unrelated MVP behavior, changes to strict planning/approval interfaces, new assistant/runtime guidance delivery.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [installed project boundary](../specs/design/interfaces-and-configuration.md#installed-project-boundary), [ADRs](../specs/design/architecture-decisions.md), [blueprint](../specs/design/software-blueprint.md), [layout](../specs/design/repository-layout.md), [delivery](../specs/design/milestone-delivery.md), [traceability](../specs/design/acceptance-traceability.md).
- **Coordinated execution index:** None. Reuse accepted US-01/02/33 capabilities; no new prerequisite story slice is planned. Discovering one requires scope revision and complete retrieval of its owning issue.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Accepted US-01/02/33 | Normal installed dependency, initializer and genuine wheel builds available | IP2–IP4 | Existing [US-01](milestone-1-us-01.md), [US-02](milestone-1-us-02.md), [US-33](milestone-0-us-33.md) evidence; acceptance preserved, executable results must be renewed for this change |
| Supported wheel source and integrity | Demonstrate an installer-supported declaration with locked SHA-256 and installed archive identity | IP2 | Proposed local wheel or direct wheel URL; exact supported syntax and availability of locked hashes remain IP1 decisions |
| Explicit upgrade and journal compatibility | Define refresh of completed identity without bypassing incomplete-operation checks or file/store conflicts | IP3 | Proposed native uv upgrade followed by ordinary init; settle at Gate 1 |
| Public test boundaries | Developer confirms the boundaries below and exact IP1 contracts before new tests | IP2 | Pending plan review and Gate 1 |
| Installer/dependency availability | Python 3.12+, Git and uv; dependencies available to independent project environments | Executable verification | Check at execution; planning did not install dependencies |

### Current repository findings

`src/agentic_ml/initialization/preflight.py:project_identity` currently requires `tool.uv.sources.agentic-ml` with exactly `git`/`rev`, a full SHA, matching lock Git source and installed `direct_url.json` VCS identity in the project `.venv`.
`environment.py` repeats Git source assumptions when synchronizing, adds requirements, runs `uv lock`, `uv sync --locked --inexact`, checks the pin and writes checksums to `.agentic-ml/init.json`.
`__init__.py` owns conflict-safe scaffolding and resume checks; `storage.py` checks incomplete-operation checksums and existing stores. Identity extension must preserve these safeguards.
`tests/installation/verify_initialization.py` currently creates pinned Git projects from validated source; direct/rebuilt wheel equivalence does not currently prove wheel-origin initialization. `check_initialization.py` also assumes Git metadata.
`docs/experiment-setup.md` documents Git bootstrap/upgrades. Current active design correctly labels US-41 unimplemented; there is no issue/design scope conflict.

### Proposed approach and decisions for Gate 1

Reuse the existing installed `agentic-ml init` and `initialize_project(InitOptions(...)) -> InitResult` interfaces and `InitializationError` diagnostics. Prefer a small internal identity module (proposed `src/agentic_ml/initialization/identity.py`) shared by preflight and synchronization over a second initializer or a new public identity framework.

Propose supporting a normal, noneditable wheel dependency with an explicit artifact locator and SHA-256 in the project lock. A locally supplied wheel is the preferred bootstrap because it requires no hosting; IP1 must establish whether uv records the required locked integrity for this form. If not, investigate a direct wheel URL with independently supplied hash, using a local HTTP fixture for tests. No registry service or publication is required. Do not silently invent a companion integrity file or accept version-only consistency as equivalent to AC-03. If neither form meets the criterion, stop at Gate 1 with findings and a revised proposal.

Gate 1 must specify exact accepted declaration/lock/installed metadata examples, relative-path resolution, normalized package name/version, artifact locator and digest comparison, missing metadata and unsupported-source errors. Bind the installed archive's origin/hash to the lock and verify available artifact bytes against the locked digest; document limits when original bytes are unavailable. Reject editable/directory/source archive installs and ambiguous/multiple toolkit declarations unless separately approved. Preserve the existing full-SHA Git branch and its diagnostics. No new packaging dependency is presumed; review declarations and lock intentionally if needed.

Record a discriminated toolkit identity (Git or wheel) plus version, artifact SHA-256/locator for wheels and environment checksums in the existing private setup journal. Gate 1 settles exact field names/versioning and backward compatibility with accepted Git journals. Do not fabricate Git metadata for wheel installs or retrofit unrelated strict plan records.

Propose explicit upgrade via native `uv add` selecting a different reviewed wheel, locked synchronization, then init to refresh a completed journal after current declaration/lock/install validation. Ordinary init must preserve the selected artifact even if its internal `uv lock` changes unrelated dependency resolution. Incomplete setup with changed metadata must still require recovery review. Gate 1 settles how a completed prior identity is distinguished from an interrupted operation and how refresh preserves user edits/stores/backups. Tests must distinguish both a new version and a different artifact with the same version; a version alone is insufficient identity.

## Plan review

- **Status:** Approved.
- **Developer decision:** Plan accepted; phase execution not yet requested. All implementation gates remain Pending.
- **Decision reference and date:** Developer message “i accept plan”, 2026-11-08 (UTC).
- **Requested plan changes:** None recorded.
- Plan approval confirms the proposed public boundaries and authorizes only the explicitly requested execution; it does not approve any implementation gate. Exact dependency/identity/upgrade choices require Gate 1 review before IP2.

## Scope-change history

None. Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for changes during execution.

## Execution rules

Follow [planning terminology](../../README.md#planning-terminology), [verification policy](../development/verification.md#phase-and-story-verification), [distribution guidance](../development/distribution.md) and [records policy](../development/records.md).
Mark tasks Complete only after required work and checks pass with actual evidence; partial/blocked work stays incomplete. Reopen invalidated tasks and renew evidence. Stop at every gate, including the final gate, present results, deviations and limitations, and wait for explicit developer approval. Silence and plan approval do not approve gates.
Use one public behavior test per red–green slice, prove the intended failure, implement the minimum, rerun relevant checks, then review refactoring. Preserve independent expected results and existing assertions, timeouts, skips and xdist groups. Track at most three corrective attempts per unresolved failure with hypothesis/change/result; after the third failure stop and present diagnostics/tree state for direction. Scope changes pause affected work until recorded and approved.
Retain raw logs/manifests under `.dev-records/verification/`; proposed tracked reports are `docs/verification/us-41-ip1.md` through `us-41-ip4.md`. No credential-bearing metadata in evidence.

### Public boundaries for confirmation

Tests invoke the installed CLI and installed `agentic_ml.initialization` exports in isolated experiment projects, including API calls with explicit root from an unrelated cwd. Assert result/error fields, subprocess exit/diagnostics, scaffold bytes, dependency/lock contents, installed metadata, journal identity, usable DVC/MLflow stores and compatible reruns. Snapshot project files and external stores before rejected init; assert no persistent modifications, including no new journal/backups/locks. Prepare identity damage before the snapshot and invoke `.venv` entrypoints directly or isolated Python, so uv cannot repair the defect before initialization sees it.
Use real installed distributions and independently computed SHA-256 values; do not mock internal identity collaborators. Native metadata/lock mutation is controlled fixture setup. Test through both CLI/API, both direct/rebuilt artifacts, fresh and compatible existing projects; distribute expensive cases deliberately while retaining both interface success/rerun coverage on both wheel paths. Local fixtures verify identity consistency, not hostile-code isolation, registry trust, every uv source format, or untested platforms. Installed metadata cannot prove that arbitrary local writers have not modified package files; no such guarantee is claimed.

## US-41 / Implementation Phase 1: Settle wheel identity and upgrade contracts

- **Outcome:** Reviewable exact contracts and feasible fixture strategy; no product implementation.
- **Entry:** Developer authorizes plan execution; inspect actual tree and issue snapshot again.
- **Acceptance criteria advanced:** AC-01–06; none fully verified.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-41-IP1-T1 | Not started | Inspect native uv declaration/lock/install metadata in disposable external projects; record local wheel and, if needed, hashed direct URL findings in proposed `docs/verification/us-41-ip1.md` | Execution authorization | Exact commands, metadata and independent hashes show a supported form meeting locked integrity; failed options recorded | AC-01/03/04 |
| US-41-IP1-T2 | Not started | Specify identity checks, pre-mutation order, journal compatibility, explicit upgrade/rerun/recovery behavior in this plan and `docs/specs/design/interfaces-and-configuration.md` / `architecture-decisions.md` | T1 | Exact source forms, schema examples and failure matrix proposed; accepted Git behavior preserved | AC-02–05 |
| US-41-IP1-T3 | Not started | Refine IP2–IP4 tasks and test matrix using findings; record developer boundary review requirements and report | T2 | No dependent code rests on unresolved syntax, identity or refresh decisions | AC-01–06 |

### Verification and review evidence

Document/relative-link checks, manual issue/design reconciliation and `git diff --check`. Native installer inspection is feasibility evidence only; it requires execution authorization and is not a passing product test. No product behavior changes, so TDD/current-milestone/shared executable checks are inapplicable to this documentation phase. No standalone verification driver or broader pytest invocation is authorized here.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; exact supported form, hash semantics, backward compatibility, upgrade/recovery rules and public boundaries explicitly accepted. If feasibility fails, refine the plan before dependent work.
- **Evidence presented:** Pending — `docs/verification/us-41-ip1.md`.
- **Remaining limitations:** Exact uv forms and journal refresh unverified until T1/T2.
- **Developer decision / reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP2 only after Gate 1 approval. Stop and await approval.

## US-41 / Implementation Phase 2: Initialize with consistent wheel identity

- **Outcome:** Supported wheel installs pass init and reruns; invalid identities fail before writes.
- **Entry:** Gate 1 approved, contracts and public boundaries confirmed.
- **Acceptance criteria advanced:** AC-02/03/04/06.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-41-IP2-T1 | Not started | Add proposed `tests/integration/test_distribution_initialization.py` installed-project fixture; first red–green CLI success slice using `preflight.py` and proposed `identity.py` | Gate 1 | Selected wheel accepted without Git-origin metadata; version/source/digest independently agree | AC-02/03 |
| US-41-IP2-T2 | Not started | Successive public API, synchronization and compatible-rerun slices in the same test module; adapt `environment.py`, `__init__.py`, journal handling as required | T1 | Full US-02 scaffold, dependency synchronization, imports and stores work; user edits survive; selected artifact stays fixed after locking | AC-02/03/04 |
| US-41-IP2-T3 | Not started | One red–green failure slice at a time: absent/malformed metadata, ambiguous declaration/lock, wrong version/source/hash, replaced/corrupt wheel, wrong environment and unsupported editable/directory/source forms | T2 | API raises InitializationError and CLI exits nonzero with recovery; project/store snapshots unchanged; no artifact substitution | AC-03/04 |
| US-41-IP2-T4 | Not started | Run M50 and shared checks below; preserve current Git initialization regression evidence for final renewal; write IP2 report | T3 | Passing selected checks, red/green logs, counts, lock identity and limitations recorded | AC-02/03/04/06 |

### Verification and review evidence

Use serial focused `uv run --locked pytest tests/integration/test_distribution_initialization.py -m milestone_50 -k <case>` during short TDD slices, recording why serial was chosen. New US-41 behavior tests carry `milestone_50`; contributor-only lifecycle checks use infrastructure. Gate command is `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_50`.
Public boundaries are those above, confirmed at Gate 1. M1–6/Git regressions and the complete direct/rebuilt matrix are deferred to **US-41-IP4-T3**; focused success does not establish AC-06.

### Developer approval gate

- **Approval criteria:** T1–T4 complete, M50/shared checks pass and no invalid identity causes durable project writes.
- **Evidence presented:** Pending — `docs/verification/us-41-ip2.md`.
- **Remaining limitations:** Explicit upgrade and full artifact matrix await IP3/IP4.
- **Developer decision / reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP3 only after Gate 2 approval. Stop and await approval.

## US-41 / Implementation Phase 3: Explicit upgrades and stable ordinary use

- **Outcome:** A scientist deliberately changes wheels and refreshes environment evidence without losing compatible work.
- **Entry:** Gate 2 approved.
- **Acceptance criteria advanced:** AC-01/04/05/06.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-41-IP3-T1 | Not started | Red–green ordinary init and `uv sync --locked` stability cases in distribution initialization tests, with a newer/different wheel available | Gate 2 | Artifact/declaration preserved, no silent upgrade; stale declaration/lock fails | AC-04/05 |
| US-41-IP3-T2 | Not started | Red–green explicit upgrade slices through native uv and init; adapt `environment.py`, journal/preflight/storage checks only under Gate 1 contract | T1 | New-version and same-version/different-artifact transitions recorded accurately; installed/declared/locked identity consistent; compatible code/stores preserved | AC-03/05 |
| US-41-IP3-T3 | Not started | Red–green interrupted/failed upgrade and init cases; update `docs/experiment-setup.md` with exact bootstrap and upgrade commands | T2 | Unsupported/inconsistent transitions rejected before init writes, interrupted-operation checks preserved; instructions distinguish native installer changes from initialization | AC-01/04/05 |
| US-41-IP3-T4 | Not started | Run M50/shared checks; record example execution and IP3 evidence | T3 | Passing results and upgrade identities saved; documentation claims match observed behavior | AC-01/04/05 |

### Verification and review evidence

Same focused TDD form and M50 command as IP2; public boundaries add native uv transitions and independently compared before/after artifact/journal identities. Native installer commands intentionally modify metadata during an explicit upgrade; pre-mutation assertions apply to initialization after that preparation. Errors during environment synchronization retain existing stage/retry diagnostics, not a newly claimed transaction rollback. M1–6 and full installed matrix remain owned by IP4-T3.

### Developer approval gate

- **Approval criteria:** T1–T4 complete, stable ordinary use and explicit upgrade/recovery evidence, M50/shared checks passing.
- **Evidence presented:** Pending — `docs/verification/us-41-ip3.md`.
- **Remaining limitations:** Both artifact paths and final regressions await IP4.
- **Developer decision / reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP4 only after Gate 3 approval. Stop and await approval.

## US-41 / Implementation Phase 4: Verify both installed artifact paths and accept the story

- **Outcome:** Complete, independent installed-project evidence for all six criteria and preserved Git behavior.
- **Entry:** Gate 3 approved.
- **Acceptance criteria verified:** AC-01–06, subject to passing results and developer acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-41-IP4-T1 | Not started | Extend `tests/installation/verify_initialization.py`, `check_initialization.py`, `tests/integration/test_initialization.py` and/or proposed distribution test module; reuse `tests/packaging/verify_distributions.py` genuine build outputs | Gate 3 | Direct wheel and actually sdist-rebuilt wheel each initialize CLI/API fresh and compatible projects and rerun; wheel-origin metadata remains genuine; full-SHA Git cases retained | AC-01/02/03/06 |
| US-41-IP4-T2 | Not started | Add missing installed identity/failure/upgrade matrix cases through red–green slices; review `tests/packaging/check_installed.py` only if inventory changes require it | T1 | Both wheel paths cover negative identities and explicit upgrade; independently verified hashes, imports/resources/store results, unchanged damaged-project snapshots | AC-03/04/05/06 |
| US-41-IP4-T3 | Not started | Final story verification, deferred-check reconciliation, update setup/design/traceability status and `CHECKPOINTS.md`; save `docs/verification/us-41-ip4.md` | T2 | Final M50, M1–6 and shared checks pass, all criteria mapped, known skips/platform gaps qualified; no false milestone completion | AC-01–06 |

### Verification and review evidence

Run both `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_50` and `uv run --locked pytest -n 4 --dist=loadgroup` on final inputs. Installed US-41 matrix tests must be selected by M50 and may invoke artifact drivers internally; retain real Git regressions under their existing directly covered milestones in M1–6. Preserve scheduling groups, independent environment ownership and cleanup/retention behavior; do not activate US-37/38 optimizations.

Both interface/artifact success and rerun coverage is mandatory. Partition negative cases and native upgrade checks across both paths explicitly in the report; do not treat direct-wheel checks as rebuilt-wheel evidence. Confirm installed runtime dependencies and absence of source-checkout imports; genuine source rebuilds use the extracted sdist, never the direct wheel. M0/infrastructure-only tests and standalone artifact drivers are excluded from automatic story checks; required US-41 artifact evidence comes from selected M50 tests. Any additional selection/standalone invocation requires an explicit developer command.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; final checks pass, all ACs have evidence, remaining limitations accurately stated.
- **Evidence presented:** Pending — `docs/verification/us-41-ip4.md` and linked durable records.
- **Remaining limitations:** Historical milestone obligations and unverified platforms remain separate.
- **Developer decision / reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Stop for final gate approval; whole-story acceptance requires explicit developer acceptance, which may be given with this gate. No publication authorized by plan drafting.

## Final verification requirements

- **Owning final phase/task:** US-41-IP4-T3.
- **Final implementation identity:** Record revision, dirty changes, OS/Python/uv versions and lock SHA-256 before/after. Renew after executable/artifact-input changes.
- **Shared checks at executable gates:** `uv sync --locked --group dev`; `uv lock --check`; `uv run --locked ruff check .`; `uv run --locked ruff format --check .`; `uv run --locked mypy src tests`; `uv run --locked agentic-ml --version`; `git diff --check`. Version must match installed distribution metadata. Lock changes require intentional dependency review.
- **M1–6:** Exact default command above; counts/outcomes and all skips recorded. Neither selected-out tests nor existing skips establish coverage.
- **Distribution/installation:** Selected M50 tests must verify normal installed wheels outside the checkout with only declared runtime dependencies, CLI/API/resources/import origins, direct and truly rebuilt artifacts. Record build and artifact hashes plus manifests/logs and cleanup results.
- **Deferred-check reconciliation:** IP2/IP3 M1–6, Git regressions and full artifact matrix owned here. Report failures instead of claiming completion. Standalone/full-suite checks only if explicitly requested; no need to broaden just because selected tests passed.
- **Actual results and limitations:** Pending. Planning ran no product tests, installer probes or build drivers. Test platform must be stated; Linux or macOS observations do not establish the other or Windows support.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-41-AC-01 documented normal wheel bootstrap outside checkout | IP1-T1/T2; IP3-T3/T4; IP4-T1/T3 | Executed setup instructions and isolated project identity | Pending |
| US-41-AC-02 installed CLI/API init and compatible files | IP2-T1/T2; IP4-T1/T3 | Both interfaces, both wheels, scaffold/env/stores and reruns | Pending |
| US-41-AC-03 declared/locked/installed identity with version and integrity | IP1-T1/T2; IP2-T1–T3; IP3-T2; IP4-T2/T3 | Independent digests, genuine origin metadata and journal | Pending |
| US-41-AC-04 pre-change identity failures and dependency preservation | IP2-T2/T3; IP3-T1/T3; IP4-T2/T3 | Failure matrix snapshots, diagnostics and artifact preservation | Pending |
| US-41-AC-05 explicit distribution upgrade and no silent upgrade | IP3-T1–T4; IP4-T2/T3 | Native upgrade transitions and stable locked/init controls | Pending |
| US-41-AC-06 both wheel paths, reruns/failures and preserved Git | IP4-T1–T3 | Genuine rebuild provenance, installed matrix and M1–6 regressions | Pending |

- **Remaining work:** All implementation and verification; exact contracts await IP1 and Gate 1. No partial prerequisite story delivery or deferred US-41 criterion.
- **Final verification:** Pending — IP4-T3.
- **Developer acceptance / decision reference and date:** Pending.

## Milestone acceptance handoff

- **Owner:** Existing M50-ACCEPT-VERIFY, preserved in [US-35](milestone-50-us-35.md), [US-36](milestone-50-us-36.md) and [CHECKPOINTS](../../CHECKPOINTS.md).
- **Deferred checks:** Historical full-suite, unchanged-caller, reserved milestone, standalone distribution/installation and applicable manual/platform obligations remain open; US-41 acceptance does not close them or M1-ACCEPT-VERIFY.
- **Required evidence:** Reconcile historical/final inputs, actual selected/deselected counts, temporary skips, platform gaps and artifact identities. Full suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""` and standalone artifact drivers require explicit developer commands under current policy. Preserve historical approvals/results, without treating CI as local evidence.
