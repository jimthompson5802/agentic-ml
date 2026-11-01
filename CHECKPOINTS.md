# Development Checkpoints

Last updated: 2026-11-01 (America/New_York)

## Current position and next action

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
The developer requested local documentation only; no GitHub issues or milestone
were created, and no implementation is authorized by these additions.
US-35-AC-02 now specifies `.dev-records/verification/` for raw evidence retained
for the lifetime of agentic-ml development. The development guide defines layout,
backup responsibility, and cleanup protection; `.gitignore` excludes the directory.
Driver adoption remains future US-35 work; no historical records were moved.

**Next action:** await developer direction on the next work item. Before story
implementation, retrieve its owning issue and follow applicable plan and approval
gates. No US-03 implementation gate or review finding remains pending.

## Checkout and working tree

- Branch: `main`, HEAD `41c4b86` at this documentation handoff. The working tree
  was clean before the retained-record policy edits; remote state was not revalidated.
- Developer authorized deletion of local and remote `US-03-experiment-boundaries`
  after verifying tip `220436c` and tree equality with squash merge `1e28ae8`.
  Both copies were deleted; other branches were retained.
- Milestone 50 documentation was committed and pushed as `41c4b86`.
- Handoff changes: `docs/specs/user-stories.md`, `docs/development.md`,
  `.gitignore`, and `CHECKPOINTS.md` document the retained-record policy. No driver
  behavior changed. Developer authorized a local commit; Git history records the
  resulting commit. Push and GitHub issue or milestone creation are outside scope.

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

This handoff changes documentation only. TDD and product test reruns do not
apply because no executable behavior changed. Retained-record policy validation
covers the new section link, preserved US-35 criterion ID, Git ignore matching,
and `git diff --check`; these checks passed. Driver tests were not rerun.

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
