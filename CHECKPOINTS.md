# Development Checkpoints

Last updated: 2026-11-01 (America/New_York)

## Current position and next action

US-36 IP2 is accepted on `US-36-pytest-workspaces`: developer
“i accept ip2; commit the changes”, 2026-11-01 (America/New_York). Local commit
of both accepted phases and approval records is authorized. Tested inputs were
`6b66d45` plus the story changes identified by saved executable hashes. The
[plan](docs/plans/milestone-50-us-36.md) owns tasks/gates; the
[IP2 report](docs/verification/us-36-ip2.md) owns final evidence, measurements,
corrective attempts and deferrals. IP1 was accepted on 2026-11-01: “i accept ip1”.
After workflow/status discussion, the developer explicitly resumed IP2:
“you can continue ip2”. Issue #49's complete body and every comment page were
retrieved with zero comments and stable refresh
`updated_at=2026-11-02T00:58:23Z`; scope is unchanged.

All T1–T6 tasks are complete. Verification callers use explicit owned descendants;
existing shared fixtures retain their scopes and survive until final consumers.
Real four-driver probes verify cleanup at completed teardown while a later test
remains active, outer failure retention, explicit retention and standalone
commands without pytest context. Documentation/help and local links pass.

**Final direct evidence:** 104 selected cases / 1 reserved milestone case
deselected. Main run: **103 passed, 1 failed in 852.01s**. The new shared-install
case exceeded its unchanged 45s first-report wait while the separate four-worker
comparison ran. Corrective attempt 1 isolated verification resources; the exact
node passed unchanged at four workers in **23.08s**. All 104 cases have passing
evidence across the main run and renewal; no single all-passing 104-case run is
claimed. Preserve `final.xml`, `renew-shared.xml`, the original failure log and
retained failed outer root documented in the report. No assertions/timeouts,
skips or suppressions changed. Shared sync/lock/lint/format/type/version/whitespace
checks pass; lock unchanged. Local evidence is macOS 15.7.9 / Python 3.12.15.

**Fixed-input comparison:** same wheel/sdist hashes and preserved Git revision,
six cases passed in **491.46s** (493.31s launcher). Successful test roots remaining
at completed teardown fell from six to zero; session-exit retained file bytes
fell from 1,729,629,402 to zero and environments from two to zero. Raw records:
`.dev-records/verification/us-36-ip2/fixed-8ced511a200a44c09f81db0cdf76c067/`.
Failure/explicit-retention/concurrent/repeated metrics are exported in final XML
and `identities/final.json`. Baseline and historical evidence remain intact.

**Both implementation gates are accepted; separate whole-story acceptance
remains pending.** No tests remain running. Commit the accepted changes under
the explicit instruction above; no push or publication was requested. Preserve
the deprecated public pytest
`Config.inicfg` compatibility-mapping limitation and overlapping-workload timing
limitation. M50-ACCEPT-VERIFY owns 289 deferred selectors from 393 collected cases,
including the reserved milestone test; M1-ACCEPT-VERIFY remains independent.

US-35 is accepted on 2026-11-01: “i accept us-35”. Both implementation phases
are approved and committed: `2e3bf2d` (IP1), `8ffa7d4` (IP2).
The [plan](docs/plans/milestone-50-us-35.md) owns progress and gates;
[Phase 2 evidence](docs/verification/us-35-ip2.md) records the consumer protocol,
TDD, final checks and same-input disk comparison. Issue #47 was retrieved again:
complete body, zero comments, metadata refresh unchanged. Scope is unchanged.

All four drivers now preserve durable records and remove only newly owned
environments/private caches after final consumers. Failure and explicit retention
keep environments; composed parents link child records and control final cleanup.
Final verification: **58 direct tests passed in 419.99s**, four workers; one reserved
milestone case deselected. All shared checks passed, lock/input hashes unchanged.
The exact baseline workload passed for all four commands, reducing retained
environments from 1/2/6/2 to zero; source/project files and records survive.
US-35 was squash merged in [PR #48](https://github.com/jimthompson5802/agentic-ml/pull/48)
at `2026-11-01T23:18:45Z`, commit `3cfa4310482bff5eadff35d5432d48bfc56c38be`,
authorized by “squash merge pr #48”.
The [final-head static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/48#pullrequestreview-5730714898)
found no actionable issues, covering publication head `6411db8`. Final-head hosted Linux/Python 3.12 CI passed
([run](https://github.com/jimthompson5802/agentic-ml/actions/runs/41360636508)).

Development-guide reorganization remains approved and committed; see its
[plan](docs/plans/development-guide-reorganization.md) and
[evidence](docs/verification/development-guide-reorganization.md).

Milestone 0 is accepted. Milestone 1 is in progress: US-01, US-02 and US-03
are accepted and merged; issues #8, #9 and #10 are closed. Milestone 99 remains
deferred. No next-story implementation has been authorized.

US-03 merged in [PR #46](https://github.com/jimthompson5802/agentic-ml/pull/46)
at `2026-11-01T03:39:35Z` (2026-10-31 local), squash commit
`1e28ae8efe1f4989408a08c76c91ddd46ea273f1`. The cost/currency correction was
accepted, published and its review thread resolved before merge. All US-03
implementation gates and whole-story acceptance are recorded in the
[owning plan](docs/plans/milestone-1-us-03.md#current-status).

Milestone 50 now records ongoing technical environment improvements outside
the product delivery sequence. US-35–US-38 cover successful-environment cleanup,
pytest workspace ownership, compatible installed-environment reuse, and sequential
wheel-environment release in [user stories](docs/specs/user-stories.md#milestone-50-improve-the-technical-environment).
The original request covered local documentation only. The developer subsequently
authorized creation of US-35 issue #47 and US-36 issue #49; US-37–US-38 remain
local stories. No GitHub milestone was created, and no implementation is authorized by these additions.
US-35-AC-02 now specifies `.dev-records/verification/` for raw evidence retained
for the lifetime of agentic-ml development. The development guide defines layout,
backup responsibility, and cleanup protection; `.gitignore` excludes the directory.
Installation-driver adoption is complete in US-35 Phase 1; the other three
drivers are complete and approved in Phase 2. No historical records were moved.

US-36 feature issue [#49](https://github.com/jimthompson5802/agentic-ml/issues/49)
was created at the developer's request using the user-story template and
`enhancement` label. Published title, complete body, and label were verified; all
five acceptance criteria are recorded. The developer subsequently required
successful-test workspace deletion at the end of each test. Issue #49 and the
local US-36-AC-02/05 now require teardown cleanup after final consumers, with
automated evidence while the session remains active. Failed-test retention and
explicit successful-workspace retention remain applicable. The full issue and
zero comments were retrieved with a stable metadata refresh before editing; the
published body was verified afterward. The requirements were committed and pushed
as `b10bf69`. The developer subsequently requested an implementation plan; its
approved plan is linked above. IP1 execution was subsequently authorized and its
technical work and gate are complete as recorded above; IP2 is authorized.

**Next action:** after the authorized local commit, await explicit US-36
whole-story acceptance. No implementation or publication is authorized by phase
acceptance alone.
Preserve M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY deferrals. The plan/report own
the completed phase's evidence and compatibility limitation.

## Checkout and working tree

- Current checkout: `US-36-pytest-workspaces`, tested parent `6b66d45` (approved
  planning records). Accepted IP1/IP2 work included with this checkpoint:
  pytest-only `pyproject.toml` settings, new
  `tests/conftest.py`, `tests/pytest_workspace_support.py`, direct subprocess
  module `tests/integration/test_pytest_workspaces.py`, IP1 report, owning plan
  and this checkpoint, four caller/fixture modules and three development guides.
  Product source, four drivers, verification helper,
  dependencies and lock are unchanged. The developer explicitly authorized the
  local commit: “i accept ip2; commit the changes”. No push authorized.
  Documentation/approval-only edits do not invalidate final direct evidence.

- Branch: `main`; pulled squash merge `3cfa431` from `origin/main`. Both
  implementation phases and whole-story acceptance are recorded.
- Phase 2 changes: distribution/initialization/planning drivers, shared helper,
  direct lifecycle/distribution tests, retention documentation, plan/evidence and
  checkpoint. Product source, dependencies and lock unchanged.
- Preserve baseline `.dev-records/verification/us-35-baseline-bac0e9c/`, all
  historical workspaces and Phase 1 evidence. Phase 2 raw records are in
  `us-35-ip2-checks/`, `us-35-ip2-workload/` and per-invocation record directories.
- Implementation and phase approvals are committed; acceptance is `49e3065`.
  PR/review links and this handoff are committed as documentation-only publication
  records and pushed on the story branch as `6411db8`. Merge outcome and checkout
  updates to this checkpoint and the owning plan are committed on `main` under
  “switch to main and pull and commit the recent updates” as `853171e`, then
  pushed at the developer’s request. `main` matches `origin/main`.
- Developer authorized deletion of the local and remote PR #48 branch. Both
  `US-35-verification-cleanup` copies were deleted after verifying tip `6411db8`
  and tree equality with squash merge `3cfa431`. Other branches remain intact.
  Branch-cleanup records are committed and pushed on `main` under the developer’s
  explicit “commit and push” instruction.

## Verification and outstanding obligation

Latest US-03 correction evidence: **183 direct tests passed**, four workers,
**45.72s**; direct and genuine sdist-rebuilt wheel probes each passed 18 new
CLI/API budget cases. Shared checks passed; lock unchanged. See the
[correction report](docs/verification/us-03-cost-currency-correction.md).
Local evidence is macOS 15.7.9 arm64 / Python 3.12.15; Windows is unverified.

Hosted Linux/Python 3.12 Development CI passed on reviewed PR head
`220436c0bcc31cc4905d10ea061a0dfe0d71bee3` before merge:
[run 41269363875](https://github.com/jimthompson5802/agentic-ml/actions/runs/41269363875).
This observed hosted success does not complete the deferred local full run.

**Open owner: M1-ACCEPT-VERIFY — Milestone 1 acceptance verification.**
The [approved ownership record](docs/plans/milestone-1-us-03.md#scope-change-record-local-verification-policy-2026-10-31)
assigns the full local suite, reserved milestone test, unchanged caller/initialization,
upgrade/scheduling and remaining artifact regressions to this task. At the latest
correction, 132 of 315 collected cases were outside the 183-test direct selection.
Before milestone acceptance, run the full suite with `-m ""`, shared checks and
applicable distribution/installation/manual/platform checks; reconcile all deferrals
against final milestone inputs under the
[verification policy](docs/development.md#phase-and-story-verification).

The developer stopped the additional 296-case run at 120 observed completion
markers, exit 130, without final summary/XML. It is incomplete evidence, not a
passing run. Preserve its [interruption record](docs/verification/us-03-ip4.md#additional-full-suite-run-requested-after-phase-approval)
and approved deferral; no local full-suite success is claimed for final US-03.

US-35 is an executable maintenance change. Its report owns current TDD and
verification evidence; do not substitute the historical US-03 checks above.
Full-suite and unchanged caller regressions remain deferred to their named owners.

## Supporting records

- Accepted work: [US-01 plan](docs/plans/milestone-1-us-01.md),
  [US-02 plan](docs/plans/milestone-1-us-02.md),
  [US-03 plan](docs/plans/milestone-1-us-03.md). Plans and linked reports retain
  granular approvals, scope decisions, failed attempts and verification evidence.
- Test runtime: nested-pytest isolation remains; hardlink optimization was rolled
  back. Retain default installer concurrency. The
  [concurrency report](docs/verification/pytest-installer-concurrency.md)
  preserves performance attempts 1 and 2; no third correction was applied.
- Raw evidence paths belong in verification reports. Their temporary-storage
  retention has not been revalidated by this cleanup; check availability before reuse.
  Earlier checkpoint snapshots remain in Git history.

## Maintenance rules

- Keep one current position and next action. Replace superseded resume instructions;
  use Git history and linked plans/reports for historical detail.
- Issues govern scope; plans own tasks, decisions, approvals and evidence. Resolve
  discrepancies against those sources before resuming. Link verification policy
  rather than duplicating it.
- At completed work, gates, blockers and handoff, refresh the date, checkout,
  working-tree changes, pending decisions, verification limits and deferred owners.
- Record approvals only after explicit developer decisions in the owning plan.
  Preserve failure evidence and attempt counts in linked records.
- Commit checkpoint updates alongside their work when authorized. Keep credentials
  and sensitive environment details outside this file.
