# Development Checkpoints

Last updated: 2026-11-01 (America/New_York)

## Current position and next action

US-35 Implementation Phase 1 is complete and approved on 2026-11-01
(“i approve ip1; commit changes”), following the developer's execution
instruction “execute implementaton plan for us-35”. The approved
[plan](docs/plans/milestone-50-us-35.md) owns task progress and gates;
[Phase 1 evidence](docs/verification/us-35-ip1.md) records the unchanged four-command
baseline, lifecycle TDD and direct/shared checks. Issue #47 was retrieved again:
complete body, zero comments, stable metadata; scope unchanged.

Installation verification now preserves durable records, supports
`--keep-workspace`, retains failures and removes only invocation-owned environments
and private caches after successful checks. The existing real pinned-install test
verified creation through installed probes, then environment removal and surviving
identity records. Final Phase 1 verification passed: 36 direct tests in 148.28s with four workers,
plus all shared checks. Phase 2 has not begun.
Phase 1 gate is approved; Phase 2 gate and story acceptance remain pending.

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
authorized creation of US-35 issue #47; US-36–US-38 remain local stories. No GitHub
milestone was created, and no implementation is authorized by these additions.
US-35-AC-02 now specifies `.dev-records/verification/` for raw evidence retained
for the lifetime of agentic-ml development. The development guide defines layout,
backup responsibility, and cleanup protection; `.gitignore` excludes the directory.
Installation-driver adoption is complete in US-35 Phase 1; the other three
drivers await Phase 2. No historical records were moved.

**Next action:** await direction to execute Phase 2; the Phase 1 gate is approved
and its changes are authorized for commit. See the owning plan and Phase 1 evidence. Preserve M1-ACCEPT-VERIFY and the new
M50-ACCEPT-VERIFY deferrals in their owning plans.

## Checkout and working tree

- Branch: `US-35-verification-cleanup`; HEAD `bac0e9c` is the approved planning commit.
- Approved Phase 1 commit contents: installation driver and direct test callers, new
  `tests/verification_support.py`, new lifecycle tests, Phase 1 report, plan and
  checkpoint. Product source, dependencies, lockfile and other drivers unchanged.
- Baseline raw records: `.dev-records/verification/us-35-baseline-bac0e9c/`;
  current direct-check XML/identity records: `.dev-records/verification/us-35-ip1-checks/`.
  These ignored records and all baseline workspaces must be preserved.
- Phase 1 commit is authorized. Phase 2 remains unstarted; story acceptance and
  publication are pending.

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
