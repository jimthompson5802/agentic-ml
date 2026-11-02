# Milestone 50 / US-36: Give pytest ownership of verification workspaces

## Scope and outcome

- **Milestone:** 50 — Improve the technical environment; separate from product delivery Milestones 0–6.
- **Authoritative issue:** [#49](https://github.com/jimthompson5802/agentic-ml/issues/49). Complete body and metadata retrieved on 2026-11-01 (America/New_York); all comment pages returned zero unique comments, matching metadata. Refresh confirmed stable `updated_at=2026-11-02T00:58:23Z`. Open, `enhancement`, no assignee or GitHub milestone; the body assigns Milestone 50.
- **User story:** [US-36](../specs/user-stories.md#us-36-give-pytest-ownership-of-verification-workspaces).
- **User-visible outcome:** Pytest-launched verification workspaces descend from their owning test directory. By default, each successful test's workspace and nested workspaces disappear during that test's teardown, after final consumers and before completion is reported. Failure diagnostics and explicitly retained workspaces survive.
- **Acceptance criteria covered:** [US-36-AC-01](../specs/user-stories.md#us-36-ac-01), [AC-02](../specs/user-stories.md#us-36-ac-02), [AC-03](../specs/user-stories.md#us-36-ac-03), [AC-04](../specs/user-stories.md#us-36-ac-04), [AC-05](../specs/user-stories.md#us-36-ac-05), in full.
- **Scope boundaries:** Contributor pytest configuration/support, explicit driver workspace plumbing at test call sites, lifecycle tests, retention documentation and measurements. Preserve failure evidence, standalone driver contracts, package provenance, existing assertions/timeouts and installed-package isolation. Exclude historical workspace/evidence deletion, environment reuse (US-37), sequential release between wheel paths (US-38), dependency/installer concurrency/hardlink changes, product runtime behavior and Milestone 99.
- **Supporting design:** [Reading map and authority](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [contributor verification contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [repository boundary](../specs/design/repository-layout.md), [milestone delivery](../specs/design/milestone-delivery.md), [acceptance traceability](../specs/design/acceptance-traceability.md), [architecture decisions](../specs/design/architecture-decisions.md). These product documents have no US-36-specific lifecycle mapping; issue #49 and development policies supply this maintenance contract. No conflicting requirement identified; no product ADR change proposed.
- **Coordinated execution index:** None. US-35 is already accepted and merged; no new cross-story prerequisite slice is included.

## Current implementation and technical approach

Inspected base `b10bf697fe8f0e171f19e9a5cf8cdaaa13a5db3e` on planning branch `US-36-pytest-workspaces`. No earlier US-36 plan exists. Findings are source inspection, not new verification results.

All four existing commands accept `--workspace` and `--keep-workspace`: `tests/installation/verify_installation.py`, `tests/packaging/verify_distributions.py`, `tests/installation/verify_initialization.py`, and `tests/installation/verify_planning.py`. Their shared `tests/verification_support.py` allocates a system temporary directory only when no workspace is supplied. Initialization and planning already pass explicit child paths to distribution verification. Planning creates a unique child when given an existing directory. Preserve those standalone behaviors.

US-35 finalization removes registered environments/private caches after driver consumers finish, preserving source/project files in the workspace and durable records in `.dev-records/verification/`. US-36 adds a later owner: the successful pytest test can remove its entire exclusively owned temporary tree after assertions and fixture finalizers. Driver completion alone does not establish test success. A driver may intentionally fail inside a passing negative test: preserve its diagnostics through that test, then apply the outer test outcome. An outer failure must retain what remains available; this story does not recreate environments already removed by a successful driver.

Uncontained calls remain in `test_distribution_verification.py` and `test_verification_lifecycle.py`, including the concurrent helper test and the parent-failure test that reads the driver's allocated `WORKSPACE` line. Most installation calls already use `tmp_path`. `installed_project` in `test_installation_verification.py` is an existing module-scoped mutable fixture, retained for multiple public rejection probes. Artifact and Git source fixtures also use `tmp_path_factory`. Preserve current scopes, scheduling groups, mutation restoration and fresh installation boundaries; do not implement US-37 reuse.

`test_parallel_execution.py` already passes a dedicated `tmp_path / "nested-pytest"` as nested `--basetemp`. Preserve that isolation and its grouping assertions and 120-second timeout. See the [runtime optimization report](../verification/pytest-runtime-optimization.md). Never give nested pytest an active parent's or sibling's directory to clear.

### Proposed lifecycle contract for plan review

1. Configure `tmp_path_retention_count = 1` and `tmp_path_retention_policy = "failed"` in `pyproject.toml`. These settings bound completed-session retention; they alone do not contain independently allocated driver paths or guarantee complete-outcome cleanup.
2. Add contributor support at proposed `tests/conftest.py`, with a typed lifecycle helper at proposed `tests/pytest_workspace_support.py` if separating logic keeps hooks small. Use public pytest hooks, fixtures and configuration interfaces; do not import pytest internals or inspect private fixture finalizer lists. Keep this tooling outside the installable package and installed probes.
3. Own per-test temporary roots explicitly. Candidate: supply the repository's `tmp_path` fixture using public `tmp_path_factory.mktemp`, track setup/call/teardown reports, and finalize only after all fixture teardown has run, before delivering the completed teardown report. This avoids native `tmp_path` removal before a later teardown error. Public hook ordering and xdist behavior must be proved in Implementation Phase 1 before adoption; an unsuccessful approach requires refinement and review, not relaxed acceptance criteria.
4. Stock installed pytest source inspection shows its `tmp_path` finalizer uses the call outcome and best-effort removal. Therefore test setup and teardown failures explicitly. Delete only exclusively allocated test-owned roots after a successful complete outcome. A removal failure must be visible as unsuccessful cleanup with the remaining absolute path; preserve original failures and report evidence. Reject ownership replacement, symlink redirection and overlap with caller paths or durable records. No broad scan/delete of temporary directories.
5. Propose `--keep-test-workspaces` as the explicit pytest-level retention control. It must protect the owning tree from both per-test and session retention cleanup, using public configuration, with documented interaction with `-o tmp_path_retention_policy=all`. A driver's `--keep-workspace` retains its data for the test's remaining consumers; post-test preservation requires the pytest-level control too. Test this distinction rather than silently treating an internal child-driver flag as global retention.
6. Shared fixture paths remain available until their last consumer/finalizer. Give existing shared fixtures explicit ownership and success/failure retention at their existing scope; a failed consumer or failed shared finalizer retains their available diagnostic tree. Do not delete a module/session fixture at the first test's completion. Document this AC-02 exception separately from per-test roots.
7. Distinct worker/session roots and exclusively created children protect concurrent invocations. Use pytest's numbered-root/active-session protection; do not implement an age-based cleanup sweep. Retain failed directories for one completed invocation subject to active-session protection; explicit retention and interrupted runs are documented exceptions. Verify actual repeated-session behavior rather than assuming `--basetemp` has numbered-root retention semantics.
8. Keep real raw commands, manifests, logs and measurements under `.dev-records/verification/`, outside disposable roots. Minimal generated regression projects may use controlled sentinel records outside the generated test's owned tree. Do not delete or migrate historical records/workspaces. Record interrupted runs as incomplete; forced termination cannot guarantee finalizers.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Authoritative scope | End-of-test deletion, failure retention and explicit retention remain distinct | All implementation | Settled by developer request “I want the deletion to be at the end of the test”; issue #49 AC-02/05 and local story agree |
| Plan review and public boundaries | Confirm proposed lifecycle, pytest option and boundaries below | Executable work | Approved with plan on 2026-11-01 (“i approve plan; commit”); execution requires separate authorization |
| US-35 lifecycle | Durable records outside workspaces; driver flags and composed-parent final consumers preserved | Both implementation phases | [US-35 plan](milestone-50-us-35.md), IP1-T2–T4 and IP2-T1–T6; both gates approved, whole story accepted; [IP2 evidence](../verification/us-35-ip2.md); issue #47 re-retrieved, zero comments and stable refresh `2026-11-01T23:18:46Z` |
| Public pytest teardown ordering | Complete-outcome cleanup before test completion, including setup/teardown failure retention and xdist | Broad fixture migration in Implementation Phase 2 | Feasibility obligation owned by US-36-IP1-T2–T4; stop and replan if not demonstrated |
| Shared fixture ownership | Retain shared paths while active; cleanup only at final consumer; failures retained | US-36-IP2-T2 | Proposed contract above; no fixture scope broadening |
| Product design decisions | Preserve installed-package boundaries without changing product controls | None | No pending product ADR blocks contributor-only cleanup |

## Plan review

- **Status:** Approved
- **Developer decision:** Approved, including proposed public test boundaries and lifecycle/retention decisions. Implementation gates were pending at plan review; later gate decisions are recorded below.
- **Decision reference and date:** 2026-11-01 (America/New_York), developer: “i approve plan; commit”
- **Requested plan changes:** None recorded.
- **Execution authorization:** Developer “start ip1”, 2026-11-01
  (America/New_York), authorizes Implementation Phase 1. The earlier “i approve
  us-36 ip1” did not approve an unimplemented gate; the developer clarified
  execution intent. IP1 technical work is complete and its gate was accepted
  on 2026-11-01: “i accept ip1”, responding to the request to approve IP1 to
  proceed to IP2. This authorizes IP2 progression, not whole-story acceptance
  or publication.

## Scope-change history

None. End-of-test deletion is part of the initial authoritative scope, not a later execution change. During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md); record stable change ID/date, request/reason, scope difference, task/AC/evidence/gate impact, revisions, explicit decision and resume point before dependent work.

## US-36 / Implementation Phase 1: Prove complete-outcome pytest workspace cleanup

- **Outcome:** A directly tested contributor lifecycle removes owned successful-test trees before completion and preserves failed/retained trees and active shared consumers. Establish feasibility before migrating all existing verification callers.
- **Entry conditions:** Developer review confirms the plan, proposed public boundaries and retention contract; separate authorization to implement. Re-retrieve issue #49 and reconcile changes before starting.
- **Acceptance criteria advanced:** US-36-AC-02–05, and the owner-path portion of AC-01. Driver adoption is incomplete until Implementation Phase 2.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-36-IP1-T1 | Complete | Inventory all pytest driver/helper allocations and shared fixture owners in `tests/integration/`, `tests/verification_support.py` and four driver scripts. Save exact selectors, input hashes, proposed ownership and a reproducible pre-change workload in proposed `docs/verification/us-36-ip1.md`; raw records under `.dev-records/verification/`. | Plan review and execution authorization | Each independent allocation has a test/shared/standalone owner and planned action. Baseline workspace counts and disk measurements captured without changing assertions, timeouts or existing workspaces. | AC-01–05 |
| US-36-IP1-T2 | Complete | Add one failing subprocess test at a time in proposed `tests/integration/test_pytest_workspaces.py`; implement proposed `tests/conftest.py` and optional `tests/pytest_workspace_support.py` in red–green slices. Start with successful-test deletion after finalizers while a later case in the same session is blocked on a parent-controlled signal. | T1; confirmed public boundaries | The parent observes the first test's completed teardown report and absent owned/nested paths before releasing the later case. Add setup, call and teardown failures; available diagnostic trees survive each failure and cleanup failures are reported. Each red fails for missing behavior, not plugin/setup failure. | AC-02, AC-04, AC-05 |
| US-36-IP1-T3 | Complete | Add retention settings to `pyproject.toml`, implement explicit pytest retention control and minimal shared-fixture lifecycle using the same support. Extend direct subprocess tests incrementally for repeated default numbered-root sessions, explicit retention, shared final consumers and ownership boundaries. | T2 | One-invocation failure retention proved with isolated temporary roots; `--keep-test-workspaces` protects successful roots beyond session exit. Setup/teardown failure, shared-finalizer failure, caller sentinel, redirected/replaced root and durable-record sentinels covered. | AC-02–05 |
| US-36-IP1-T4 | Complete | Extend `test_pytest_workspaces.py` with synchronized concurrent sessions and four-worker cases, plus nested pytest with dedicated child bases; record hook-order feasibility in IP1 report. Preserve `test_parallel_execution.py` assertions and timeout. | T2–T3 | Distinct paths and no removal of another active invocation while cleanup occurs. No sleeps used as proof of ordering; use events/files or pipe handshakes with bounded waits. If complete-outcome cleanup cannot meet AC-02, stop and revise the approach before migration. | AC-01, AC-03, AC-05 |
| US-36-IP1-T5 | Complete | Run direct tests and shared checks below; record lock/input identity, TDD commands/results, counts, failure attempts and limitations in IP1 report; update this plan and `CHECKPOINTS.md`. | T1–T4 | Required checks pass; raw evidence outside cleanup roots, review report complete, technical progress separate from pending gate. | AC-01–05, partial until adoption |

### Verification and review evidence

- **Selected tests and impact rationale:** `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_pytest_workspaces.py`. This proposed module directly tests new pytest lifecycle/configuration/support through real subprocess runs, filesystem observations and published reports. If implementation changes `tests/verification_support.py`, add `tests/integration/test_verification_lifecycle.py` as direct coverage before this gate; no such helper change is currently intended.
- **Public boundaries and limits:** Proposed boundaries require developer confirmation through plan review. Generated subprocess projects load the actual contributor plugin/helper and use public pytest fixture/configuration/report interfaces. Independently defined expected existence, contents, return codes and completion events test observable behavior. Include four nested workers under unique child bases; do not replace xdist with mocks. Minimal fixtures prove lifecycle and concurrency, not package installation provenance or actual driver containment; Implementation Phase 2 owns those checks. Tests of cleanup failure may inject a narrowly scoped filesystem failure; do not mock the cleanup policy or final outcome.
- **Deferred checks:** Existing tests that are only callers of the new repository-wide `tmp_path` behavior, product initialization/planning/approvals/version regressions, real driver integration and full suite go to `M50-ACCEPT-VERIFY`, except driver checks expressly required by Implementation Phase 2. New direct lifecycle cases cannot be deferred for cost.
- **Broader-run triggers:** No automatic broader local run. If direct impact changes, update the module-to-test mapping and scope record; assign remaining uncertainty to the named milestone owner.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Lifecycle and timing | Four-worker direct command above; serial `uv run --locked pytest tests/integration/test_pytest_workspaces.py::<node>` only for recorded short red–green cycles/diagnosis | Complete-outcome cleanup, failure/retention and concurrency tests pass; exact counts recorded | [IP1 report](../verification/us-36-ip1.md): 25 collected/selected, 0 deselected, 25 passed in 2.98s; XML/raw records outside disposable roots |
| Shared development checks | Before/after `shasum -a 256 uv.lock`; `uv sync --locked --group dev`; `uv lock --check`; `uv run --locked ruff check .`; `uv run --locked ruff format --check .`; `uv run --locked mypy src tests`; `uv run --locked agentic-ml --version`; `git diff --check` | All pass, CLI reports installed metadata version, lock unchanged | Passed; lock SHA-256 `90b77d41…84c0fd8`, CLI `0.1.0`; see IP1 report for sandbox retries and initial lint/format corrections |
| Review records | Inspect proposed `docs/verification/us-36-ip1.md`, raw records, relative links and task status | AC mappings, feasible ownership protocol and pending gate accurately recorded | [IP1 report](../verification/us-36-ip1.md) records baseline, TDD, hook-order feasibility, native-container retention refinement, deprecated public compatibility mapping and IP2 limits; final local links/whitespace checked |

### Developer approval gate

- **Approval criteria:** T1–T5 complete with direct timing/failure/concurrency evidence and shared checks. Review complete-outcome hook behavior, explicit retention and shared-path ownership. No weakened tests, suppressed failures, changed timeouts or unresolved direct failures.
- **Evidence presented:** [IP1 report](../verification/us-36-ip1.md), complete
  direct XML and raw evidence under `.dev-records/verification/us-36-ip1/`.
  T1–T5 complete; baseline six tests passed in 307.72s and final 25 direct cases
  passed in 2.98s with four workers. Shared checks passed, lock unchanged.
- **Remaining limitations or blocked work:** Real driver call-site migration and disk comparison remain in Implementation Phase 2; platform coverage recorded from actual runs.
- **Developer decision:** Accepted.
- **Decision reference and date:** Developer “i accept ip1”, 2026-11-01
  (America/New_York), after the verification summary and request to approve IP1
  to proceed to IP2.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** US-36 IP2; stop at its final implementation gate.
  Preserve IP1 evidence and its pytest 9.1 compatibility/baseline limitations.
  After approval-workflow/status discussion, the developer explicitly resumed:
  “you can continue ip2”, 2026-11-01 (America/New_York).

## US-36 / Implementation Phase 2: Adopt test-owned paths across verification and prove retention

- **Outcome:** All pytest-launched verification workspaces are contained, cleaned at the correct owner boundary and covered by direct driver and lifecycle evidence; standalone behavior remains usable.
- **Entry conditions:** Implementation Phase 1 technical completion and explicit developer gate approval. Refine call-site inventory from approved IP1 evidence before migration.
- **Acceptance criteria advanced:** US-36-AC-01–05 in full.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-36-IP2-T1 | Complete | In red–green slices, add explicit fresh `--workspace` children to all uncontained pytest calls in `tests/integration/test_distribution_verification.py` and `test_verification_lifecycle.py`; audit `test_installation_verification.py`, `test_initialization.py` and other driver callers. Supply explicit paths to helper `Invocation` tests currently relying on allocation defaults. Preserve standalone default allocation in helper/driver source. | IP1 gate; IP1 inventory | Every nested driver `WORKSPACE` output descends from the owning test root or documented active shared fixture root. Existing success/failure/provenance assertions still run before test cleanup. Real installation, distribution, initialization and planning paths covered, including composed children and negative cases. | AC-01, AC-03–05 |
| US-36-IP2-T2 | Complete | Adopt shared-fixture ownership at existing scopes for `installed_project`/source fixtures in `test_installation_verification.py`, artifact fixtures in `test_distribution_verification.py` and `test_verification_lifecycle.py`, and any additional owners identified in T1. Update `test_parallel_execution.py` only if needed to record direct ownership behavior. Add direct shared-consumer regressions in `test_pytest_workspaces.py`. | T1; approved IP1 shared protocol | No active consumer loses files; mutable fixture scopes/grouping/restoration unchanged. Last successful consumer/finalizer releases shared paths; failed consumer/finalizer retains diagnostics. Nested grouping/isolation assertions and timeout intact. | AC-01–03, AC-05 |
| US-36-IP2-T3 | Complete | Extend direct lifecycle coverage to observe real four-driver workspace trees after the owning test's completed teardown but before session exit, and to exercise standalone allocation/flags from an unrelated cwd. Use installed artifacts/local Git fixture with independent expectations; preserve existing parent failure and retention tests. | T1–T2 | Successful owned trees absent at completion; failed outer tests/explicitly retained roots survive; driver diagnostic output identifies absolute workspace/records. Both actual wheel paths and parent consumers remain genuine, outside the checkout. | AC-01–05 |
| US-36-IP2-T4 | Complete | Update `docs/development/verification.md`, `distribution.md` and `records.md` for default teardown timing, one-invocation failure retention, shared-path lifetimes, per-test/driver retention flags, interrupted runs, nested bases, active-session protection and durable evidence. | T1–T3 | Documented commands match implemented public help/configuration; no claim that standalone driver cleanup removes all source/project files. Preserve historical reports and records. | AC-02, AC-04 |
| US-36-IP2-T5 | Complete | Replay the IP1 fixed workload with the same selected tests/artifacts, worker count, assertions and timeouts; save raw measurements under `.dev-records/verification/` and proposed `docs/verification/us-36-ip2.md`. | T1–T3; IP1 baseline | Record workspace counts, environment counts, logical bytes and allocated disk (`du -sk`) at test completion, session completion and across repeated invocations. Include successful, failed, explicit-retention and concurrent cases. Record elapsed time, platform/filesystem limits, artifacts and input identities; distinguish shared/active paths from leaks. Delete only newly owned measurement roots. | AC-05 |
| US-36-IP2-T6 | Complete | Complete final direct/shared verification, reconcile all ACs, renew invalidated IP1 evidence, update plan/checkpoint and IP2 report; hand off every deferred check to `M50-ACCEPT-VERIFY`. | T1–T5 | Final tested identity and lock hash recorded, direct tests/shared checks pass, all five ACs have evidence, limitations and deferrals explicit before final gate. | AC-01–05 |

### Verification and review evidence

- **Selected tests and impact rationale:** Start with `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_pytest_workspaces.py tests/integration/test_distribution_verification.py tests/integration/test_installation_verification.py tests/integration/test_verification_lifecycle.py`. These directly exercise the changed ownership call sites, shared fixtures, four driver commands and lifecycle. The reserved `test_complete_initialization_from_both_artifact_paths` stays deselected by normal configuration; existing nonreserved lifecycle coverage and new T3 tests verify initialization timing directly. Never unmark the reserved test or substitute its milestone scheduling for required direct tests.
- Add `tests/integration/test_parallel_execution.py` if its behavior/source is changed; otherwise its unchanged scheduling regression is a milestone deferral. For any other modified fixture/call site (for example in `test_initialization.py`), select the exact affected nodes as direct tests and record them before the gate; do not select the whole unrelated product module automatically.
- **Public boundaries and limits:** Reuse approved IP1 subprocess/filesystem boundaries. Real driver CLI flags, reported paths/status, external project interpreters, artifact identities and persistent records establish installed integration. Test-local driver `--keep-workspace` protects assertions, not an implicit request to retain the outer test tree. Minimal failure tests do not prove physical filesystem reclamation; measurements report allocated/logical sizes and APFS/cache limitations separately.
- **Deferred checks:** Unchanged product callers, CLI/API initialization/planning/approval regressions, unchanged scheduling checks, reserved milestone initialization case and full suite remain owned by `M50-ACCEPT-VERIFY`. Preserve the independent `M1-ACCEPT-VERIFY` obligation and historical interruption evidence; no transfer or closure is implied.
- **Broader-run triggers:** None automatically. Required direct cases run despite cost; record uncertain effects and explicit milestone ownership rather than broadening local phase tests.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Final direct behavior | Four-worker selection above, plus exact changed-fixture nodes | All required direct cases pass with selected/deselected counts and AC mapping | 104 selected / 1 reserved case deselected: 103 passed in 852.01s; one 45s completion-event timeout renewed unchanged at four workers, 1 passed in 23.08s. See IP2 report; no single all-passing 104-case invocation claimed. |
| Driver containment and installed contracts | Public four-driver cases in T1/T3, independent cwd, actual direct wheel and genuinely sdist-rebuilt wheel | Correct containment, preserved origins and independent probes; records survive teardown | Passed: real four-driver installed probes, both genuine wheel paths, live teardown observation and shared-fixture cases; final XML properties and identities in IP2 records. |
| Timing and retention comparison | T5 replay of IP1 workload, synchronized live-session observations and repeated/concurrent invocations | Successful owned trees removed at test completion; expected failures/retention/shared activity explained; measured counts/bytes recorded | Passed: same wheel/sdist hashes and preserved Git source; six replay tests passed, zero retained file bytes/environments; failure/keep/repeat/concurrent metrics exported in final XML. |
| Shared development checks | Same complete shared command list as Implementation Phase 1, before/after lock hashes | Pass; unchanged lock/dependencies and correct CLI version | All passed; lock SHA-256 unchanged, CLI 0.1.0; IP2 report records commands, output and sandbox retries. |
| Documentation and final evidence | Resolve changed local links, inspect CLI/help/examples and `git diff --check` | Instructions agree with actual lifecycle; no fabricated results or acceptance | Passed: CLI help, 53 local links/anchors across 32 files and diff whitespace; record-only edits checked at handoff. |

### Developer approval gate

- **Approval criteria:** T1–T6 complete, all five ACs mapped to passing direct evidence, fixed-workload measurements and shared checks pass; required tests/failures unresolved means this gate remains blocked.
- **Evidence presented:** [IP2 report](../verification/us-36-ip2.md), T1–T6
  complete. Records under `.dev-records/verification/us-36-ip2/`: final XML,
  isolated renewal XML, exported measurements, final identity and preserved
  original failure. Fixed-input comparison passed six cases with zero retained
  file bytes/environments; all shared checks passed.
- **Remaining limitations or blocked work:** Record actual macOS/Python/tool versions; Linux/Windows remain unverified by local evidence. Milestone deferrals remain explicitly owned.
- **Developer decision:** Accepted.
- **Decision reference and date:** Developer “i accept ip2; commit the changes”,
  2026-11-01 (America/New_York).
- **Requested changes and resolution:** No implementation changes requested;
  commit accepted IP1/IP2 changes and approval records.
- **Progression authorized:** Local commit authorized. Whole-story acceptance
  remains separate and pending; no push or publication authorized.

## Execution rules

- Mark tasks `Complete` only after required verification passes and actual evidence is recorded; keep partial/failed/blocked/unverified tasks incomplete. Reopen tasks and renew evidence invalidated by later changes.
- Use one behavior-focused red–green slice at a time through confirmed public boundaries. Record exact red/green commands, intended failure, results and AC IDs in the owning phase report. Refactor only with relevant behavior green. Do not write a batch of all tests before implementation.
- Follow [repository instructions](../../AGENTS.md), [development guide](../development.md) and [verification policy](../development/verification.md#phase-and-story-verification). Preserve lock identity and existing assertions/timeouts. Explain every suppression/exclusion; do not conceal failures.
- Stop after each implementation phase and present tasks, checks, actual evidence, deviations and limitations. Wait for explicit developer approval; plan approval is not implementation-gate approval. Preserve all historical approvals and evidence.
- Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) if feasibility changes scope/approach or new prerequisite work is required. Pause affected work until the required scope decision is recorded.
- Make at most three corrective attempts for the same unresolved problem, counting across turns. Record hypothesis/change/original-failure verification each time. After the third failed attempt, stop and present all attempts, commands/output, current tree and options; await developer direction. Do not weaken acceptance/tests or change timeouts to pass.

## Final verification requirements

- **Owning final phase/task:** US-36-IP2-T6, required before the final gate.
- **Final implementation identity:** HEAD `6b66d45` plus uncommitted story work;
  executable hashes and macOS/Python/tool identities in IP2
  `identities/final.json`. Lock SHA-256 `90b77d41…84c0fd8` unchanged. Fixed replay
  verifies byte-identical original artifacts and Git revision; normal direct
  tests also build and probe final checkout artifacts.
- **Direct tests and shared checks:** Reuse valid IP1 evidence; renew lifecycle/configuration evidence after migration changes it. Run the final direct selection and complete shared command list. No story-level automatic full suite.
- **Distribution/installation and other required checks:** T3 direct tests must demonstrate the four drivers, direct wheel and wheel genuinely rebuilt from the source distribution with declared runtime dependencies, public CLI/import/resources and actual origin identities. Installed probes remain outside checkout, without editable installs/contributor dependency leakage. If these checks are already performed by selected tests against identical final inputs, link that evidence rather than duplicate costly standalone runs. Changes to build/resource/dependency inputs require rebuilding affected artifacts and renewed probes. Product runtime changes are outside scope.
- **Deferred-check reconciliation:** 393 total collected, 104 direct cases
  covered; 289 selectors (including the reserved milestone case) saved in IP2
  `deferred-selectors.txt`, owner `M50-ACCEPT-VERIFY`. See IP2 report for module
  counts. Preserve independent M1 ownership; no full-suite success claimed.
- **Evidence renewal:** Later executable changes renew affected direct evidence; later milestone changes renew full-suite evidence at milestone acceptance. Documentation/approval-only edits use document/link/whitespace checks with rationale.
- **Actual results and limitations:** [IP2 report](../verification/us-36-ip2.md)
  records all commands, baseline comparison, live/failure/retention metrics and
  the original overlapping-run timeout plus unchanged isolated renewal. All
  selected cases have passing evidence; no single all-passing 104-case invocation
  claimed. macOS 15.7.9/Python 3.12.15 only; Linux/Windows and other pytest
  versions unverified locally. Deprecated public compatibility mapping remains.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-36-AC-01: explicit contained workspace trees | IP1-T1/T4; IP2-T1–T3/T6 | Allocation inventory, four real driver paths and nested/concurrent containment | Verified; developer accepted US-36 |
| US-36-AC-02: end-of-test cleanup and retention distinctions | IP1-T2–T5; IP2-T2–T4/T6 | Live-session completion observation, setup/call/teardown failures, final consumers and documentation | Verified; developer accepted US-36 |
| US-36-AC-03: worker/session/nested isolation | IP1-T4/T5; IP2-T1–T3/T6 | Concurrent active-session sentinels and distinct roots under four workers | Verified; developer accepted US-36 |
| US-36-AC-04: standalone use, diagnostics and explicit retention | IP1-T2/T3/T5; IP2-T1/T3/T4/T6 | Unrelated-cwd standalone commands, retained paths, published diagnostics and help | Verified; developer accepted US-36 |
| US-36-AC-05: automation, counts and retained disk usage | IP1-T1–T5; IP2-T3/T5/T6 | Red–green records, repeated-session automation and fixed-workload measurements | Verified; developer accepted US-36 |

- **Remaining work:** No story implementation work. Publication and review
  records are below; milestone acceptance verification remains separately owned.
- **Partial prerequisite delivery:** None. US-35 evidence is reused as an existing capability, not duplicated or reopened.
- **Final verification:** US-36-IP2-T6 complete; IP2 report owns reused/renewed
  direct evidence, shared checks, all five ACs and exact milestone deferrals.
- **Developer acceptance:** Accepted.
- **Decision reference and date:** Developer “I accept us-36”, 2026-11-01
  (America/New_York). Both implementation gates and required direct verification
  are complete. Approval-only edits preserve executable input identity; reuse
  the phase evidence and retain all milestone deferrals and platform limits.
  Issue #49 was refreshed with its complete body and all comment pages: zero
  comments, unchanged `updated_at=2026-11-02T00:58:23Z`.

## Publication

- Accepted implementation commit: `2a566d1`; acceptance records: `030c883`.
  Both are pushed on `origin/US-36-pytest-workspaces`.
- [PR #50](https://github.com/jimthompson5802/agentic-ml/pull/50):
  `test: give pytest ownership of verification workspaces`, standard PR to
  `main`, closes #49. Published body/head/base/ownership verified.
- [Static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/50#pullrequestreview-5731480753)
  covers `030c883`: no actionable findings. Complete 15-file diff, requirements,
  lifecycle code, direct coverage and evidence inspected; no project code/checks
  run during review. Record-only publication edits receive final-head follow-up.
- Acceptance/publication edits pass whitespace and document-link inspection;
  no executable inputs changed, so valid phase evidence is reused. CI outcome
  remains separate from local verification; no hosted success is claimed here.
- Developer “squash merger the pr” authorized squash merge. PR #50 merged at
  `2026-11-02T03:47:31Z`, squash commit
  `26da686f74126957b866f3c49e13ca6a6cc8f259`.
- Final-head [static review](https://github.com/jimthompson5802/agentic-ml/pull/50#pullrequestreview-5731483694)
  covered `e9fbcb4` with no actionable findings. Hosted Linux/Python 3.12
  [CI run](https://github.com/jimthompson5802/agentic-ml/actions/runs/41377467477)
  passed at that head before merge. This does not close local milestone deferrals.
- Publication and merge are complete. Branch cleanup and further implementation
  require separate authorization. Local merge records remain uncommitted.

## Milestone acceptance handoff

- **Owner:** `M50-ACCEPT-VERIFY` — Milestone 50 acceptance verification task, Not started. The [existing US-35 handoff](milestone-50-us-35.md#milestone-acceptance-handoff) and this record retain their deferrals until a milestone execution plan supplies the corresponding task. Milestone 50 is ongoing; story acceptance does not imply milestone acceptance.
- **Deferred checks:** Every unchanged caller/dependent regression, full suite, existing reserved complete-initialization case, unchanged scheduling regression, and any remaining artifact/platform checks. IP2-T6 records exact selectors/counts and uncertainty. Preserve separate M1 ownership.
- **Required evidence:** `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, shared checks above, applicable direct/rebuilt-wheel and installation verification, manual retention review and actual platform limits against final milestone inputs. Reconcile every deferral and renew full-suite evidence after later executable changes; use identical artifact evidence only when input identity and actual checks establish equivalence.
