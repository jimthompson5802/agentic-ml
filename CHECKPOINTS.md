# Development Checkpoints

Last updated: 2026-10-29

## Current position

- Milestone: 0 — Harness development foundation.
- Active work: US-32 IP1 Linux revision approved; IP2 beginning with authorized branch/PR publication.
- Branch: `us-32-setup-gh-action-ci`; last commit `14527c1` (original IP1 configuration).
- Current uncommitted revision switches CI to Linux (Ubuntu 24.04), updates requirements/design/docs and records SC-01 in the plan and issue #2. Linux execution remains pending IP2.
- Previous commit scope: new CI workflow and IP1 evidence; updated README, development guide, owning plan, execution index and checkpoint. Developer message “commit changes” authorizes this local commit. IP1 approval is recorded; no publication performed. No runtime/dependency changes.

## Progress overview

| Story | Implementation plan | Implementation | Developer gate |
|---|---|---|---|
| US-31 / #1 | [Approved](docs/plans/milestone-0-us-31.md) | Complete and accepted | IP1/IP2 approved |
| US-32 / #2 | [Approved](docs/plans/milestone-0-us-32.md) | IP1 T1–T3 complete; IP2 starting | IP1 approved |
| US-33 / #3 | [CLI prerequisite approved](docs/plans/milestone-0-us-33.md) | CLI prerequisite complete; remainder unplanned | IP1 approved |

## Resume here

Developer message “execute plan for us-32” authorized IP1 on 2026-10-29. Review [IP1 evidence](docs/verification/us-32-ip1.md) and the [owning gate](docs/plans/milestone-0-us-32.md#us-32--implementation-phase-1-configure-linux-development-ci). Developer approved IP1 and authorized commit/push/PR creation to begin IP2 on 2026-10-29. Follow the [execution order](docs/plans/milestone-0-us-32-execution-order.md); merge authorization remains separate.

## Pending developer decisions

- IP1 approved by developer 2026-10-29; IP2 and branch/PR publication authorized. No story acceptance claimed.
- Default-branch evidence still requires explicit merge authorization.
- Remaining US-33 requires separate planning/authorization; Milestone 99 stays deferred.

## Handoff notes

- Refreshed full issue #2 and every comment page: zero comments, stable metadata, Milestone 0 in body, no scope conflict. Existing US-31/US-33 prerequisite approvals/evidence checked against current tree.
- Actions enabled; main is default branch. Configured ubuntu-24.04/Python 3.12/uv 0.13.1 with immutable checkout/setup-uv commits, locked setup, named independent checks and final checksum/diff. Hosted capacity/events remain unverified.
- actionlint 1.7.12 passed; disposable local lint defect propagated exit 1 under CI shell options. All seven documented commands passed on macOS 15.7.9 arm64/Python 3.12.15; three tests. Lock SHA-256 unchanged. Local file-target/command comparison and diff checks passed.
- No runtime behavior added: existing regression checks and workflow validation apply. Hosted red/correction-green cases remain IP2. No corrective attempts or suppressions. SC-01 records the authorized Linux CI change in issue #2 and the owning plan. Sandbox cache/network failures succeeded on authorized retries. Raw local results remain `/tmp/us32-ip1-evidence/`; durable results are in the evidence report.

## Maintenance rules

- Keep this file a concise current handoff. Replace stale resume instructions and notes; Git history preserves earlier checkpoints.
- Summarize overall progress and link to authoritative records. GitHub issues govern scope; implementation plans own granular tasks, verification evidence, scope changes, and developer gate decisions. Resolve discrepancies against those sources before resuming.
- Record approval only after the developer explicitly gives it, and link to the decision recorded in the owning plan. Task completion and plan approval do not approve implementation-phase progression.
- At each update, refresh the date, current position, progress summary, next action, pending decisions, and material working-tree or verification notes. Include failed checks, blockers, and relevant evidence links when present.
- Commit checkpoint updates alongside the work they describe when practical. Keep credentials and sensitive environment details outside this file.
