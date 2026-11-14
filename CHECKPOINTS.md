# Development Checkpoints

Last updated: 2026-11-14 (UTC)

## Current position and next action

Checkout: `main`; implementation parent `e0b7471`. Before publication,
`git ls-remote origin refs/heads/main` confirmed that remote `main` matched that
parent. Contributor worktree management Gate 1
was approved by “I approve Gate 1,” Gate 2 by “i approve gate 2,” and Gate 3 by
“I approve gate 3,” all developer messages on 2026-11-14. All three phases and
gates are complete in the
[owning plan](docs/plans/story-worktree-management.md).
Changes include the new skill/metadata, planning and execution integration,
worktree ignore rule, agent/development guidance, plan template, saved plan, and
this checkpoint and the new verification report. The developer's subsequent
“commit and push” authorizes committing this change set and pushing `main` to
`origin`; Git history and remote refs establish the resulting commit and
synchronization status. No PR or cleanup was requested. The real checkout
retains only its original registered worktree.

Validation passed for all three skills, metadata/file-link and whitespace checks
across 13 files, `git diff --check`, and the `.worktrees/` ignore rule. The
[Phase 3 report](docs/verification/story-worktree-management.md) records 28 host
Git/walkthrough checks, 21 shared-container session checks, and 15 checks after
container restart. Two synthetic story sessions used separate editable
environments. Each worktree and the primary fixture collected 723 of 991 cases
(268 deselected); no product tests were executed. The host `.venv` remains unusable
outside Linux; container Python and the new isolated environments worked. The
existing container was returned to its initial stopped state after validation.
No environment repair or automatic assistant-policy enforcement is claimed.
See the report for command records and verification limits. Product verification
obligations and the [verification policy](docs/development/verification.md#phase-and-story-verification)
remain unchanged. No product implementation is active.

US-13 M1 AC-01/02 is accepted and merged through
[PR #66](https://github.com/jimthompson5802/agentic-ml/pull/66), squash `ecd28b1`.
Gates 1–3 are Approved. Issue #16 remains open for M2 restoration AC-03/04;
whole-story and milestone acceptance are not claimed. Story branches were deleted.
The [owning plan](docs/plans/milestone-1-us-13.md) and
[IP3 evidence](docs/verification/us-13-ip3.md) retain the detailed decisions and
verification: M1 and M1–6 each recorded 722 passes and one existing skip on Linux
aarch64. Those are historical results, not a fresh test inventory.

Skill maintenance is merged through
[PR #67](https://github.com/jimthompson5802/agentic-ml/pull/67), squash `7d2d657`.
Local and remote `skill-refactoring` branches were deleted; merge/cleanup records
were pushed as `bdb871c`. Both PR CI jobs were cancelled, so no passing CI result
is claimed for that head. The separate policy update followed as `b03afb3`.

**Next action:** complete authorized publication, then await development
direction. Keep validation fixtures and raw evidence; cleanup remains separate.
Retain raw evidence under
`.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/`, the
1.8 GB container fixture under `.worktrees/worktree-validation-d4026fb0/`, and
the host fixture linked from the report. TDD and executable product checks do
not apply to these instruction and ignore-rule changes. Container recreation,
automatic VS Code startup, independent assistant evaluation, symlink cleanup
demonstrations, and Windows support remain unverified.
Historical verification obligations below remain open.

## Completed work: authoritative records

| Work | Final status and records |
|---|---|
| US-01–03 | Accepted and merged; [US-01](docs/plans/milestone-1-us-01.md), [US-02](docs/plans/milestone-1-us-02.md), [US-03](docs/plans/milestone-1-us-03.md). |
| US-11 | Accepted and merged in PR #60; [plan](docs/plans/milestone-1-us-11.md), [IP3 evidence](docs/verification/us-11-ip3.md). |
| US-12 #19 | Accepted and squash-merged in PR #62 as `980c97f`; [plan](docs/plans/milestone-1-us-12-assessment-splits.md), [IP4 evidence](docs/verification/us-12-19-ip4.md). AC-04 deferred. |
| US-12 #15 | Accepted and merged in PR #61; [plan](docs/plans/milestone-1-us-12.md), [IP3 evidence](docs/verification/us-12-ip3.md). |
| US-13 M1 | AC-01/02 accepted and merged in PR #66 as `ecd28b1`; Gates 1–3 Approved. [Plan](docs/plans/milestone-1-us-13.md), [IP3 evidence](docs/verification/us-13-ip3.md). Issue #16 remains open for M2 AC-03/04. |
| MVP scope revision | Accepted and published; PR #57 merged; US-39 #58 and US-40 #59 created. [Plan](docs/plans/mvp-scope-revision.md), [publication evidence](docs/verification/mvp-scope-revision-ip4.md). This accepts scope documents, not an implemented MVP. |
| US-41 | All six criteria accepted; issue #64 closed; PR #65 squash-merged as `5d5781c`. [Plan](docs/plans/milestone-50-us-41.md), [IP4 evidence](docs/verification/us-41-ip4.md). Historical M50 verification remains open. |
| US-35/36 | Accepted and merged in PRs #48/#50; [US-35](docs/plans/milestone-50-us-35.md), [US-36](docs/plans/milestone-50-us-36.md). US-37/38 remain local stories without implementation authorization. |
| Skills and verification policy | PR #67 merged the planning-deliverable and polling edits. `b03afb3` removed automatic full-milestone phase-gate runs. [Policy](docs/development/verification.md#phase-and-story-verification); Git history preserves authorizations and checks. |
| Contributor tooling | Development guide reorganization, scheduling, dependency inventory and container work are recorded in [verification reports](docs/verification/) and Git history; container limitations remain below. |

Plans and reports own granular tasks, approvals, commands, failures and publication
records. Earlier checkpoint snapshots remain in Git history; superseded gate and
resume instructions have been removed. Historical records are not current authority
to proceed past a gate.

## Outstanding verification and known limitations

- **M1-ACCEPT-VERIFY — Milestone 1 acceptance verification:** Open. The
  [approved ownership record](docs/plans/milestone-1-us-03.md#scope-change-record-local-verification-policy-2026-10-31)
  retains reconciliation of excluded suite coverage, reserved milestone tests,
  unchanged caller/initialization regressions, upgrade/scheduling and artifact
  checks under its later scope revisions. Broader runs need explicit commands.
  The historical US-03 snapshot deferred 132 of 315 collected cases. The
  [interrupted additional run](docs/verification/us-03-ip4.md#additional-full-suite-run-requested-after-phase-approval)
  is incomplete evidence, not a passing full run. Hosted CI success does not
  close this obligation.
- **M50-ACCEPT-VERIFY — Milestone 50 acceptance verification:** Not started.
  The [US-35 handoff](docs/plans/milestone-50-us-35.md#milestone-acceptance-handoff)
  and [US-36 plan](docs/plans/milestone-50-us-36.md) retain reconciliation of
  excluded suite coverage, unchanged callers, reserved milestone tests and
  applicable platform/manual deferrals under their later scope revisions. The
  historical US-36 snapshot deferred 289 of 393 collected cases. This obligation
  remains independent of M1-ACCEPT-VERIFY.
- **Revised MVP verification owners:** `MVP-M1-ACCEPT-VERIFY` owns final M1
  integration reconciliation; `MVP-M2-ACCEPT-VERIFY` owns later restoration
  integration, as recorded in the [US-13 handoff](docs/plans/milestone-1-us-13.md#milestone-acceptance-handoff).
  These do not close historical M1/M50 obligations.
- **Milestone evidence reconciliation:** Before milestone acceptance, reconcile
  deferrals, known failures, evidence identities, counts and platform/manual
  limits against final inputs. Milestone acceptance does not automatically
  launch a local full suite or standalone artifact checks; broader verification
  requires explicit developer commands under the
  [verification policy](docs/development/verification.md#phase-and-story-verification).
  Historical counts are not current inventories. Story acceptance and CI results
  do not establish milestone acceptance or unperformed local verification.
- **US-36 evidence qualification:** The final direct run had 103 passes and
  one failure; the unchanged failing case passed on renewal after isolating
  verification resources. All 104 selected cases have passing evidence across
  those runs; no single all-passing 104-case run is claimed. Preserve the
  deprecated public pytest `Config.inicfg` compatibility-mapping limitation
  and overlapping-workload timing limitation documented in the
  [IP1 report](docs/verification/us-36-ip1.md) and
  [IP2 report](docs/verification/us-36-ip2.md).
- **Development container:** Build, startup and container development checks
  require report-specific evidence. A direct lifecycle-runner invocation succeeded,
  but automatic VS Code creation handoff remains unresolved. PR #51 records the
  generated pytest workspace-member concern. Hosted CI does not establish
  container functionality.
- **Platform coverage:** Coverage varies by report: earlier local evidence includes
  macOS arm64; recent US-11/12 evidence is Linux aarch64 / Python 3.12.16.
  Windows remains unverified. Consult each report for tested inputs and limits.
- **Test runtime:** Retain nested-pytest isolation and default installer
  concurrency. Hardlink optimization was rolled back. The
  [concurrency report](docs/verification/pytest-installer-concurrency.md)
  preserves performance attempts 1 and 2; no third corrective attempt was applied.

## Evidence preservation

Preserve historical baselines, failure logs, retained diagnostic workspaces,
input identities and verification records referenced by the owning reports.
Do not delete them as part of checkpoint cleanup. US-35 requires raw evidence
under `.dev-records/verification/` to be retained for the lifetime of agentic-ml
development; follow the [records guide](docs/development/records.md) for layout,
backup responsibility and cleanup protection.

Raw evidence paths and detailed measurements belong in verification reports.
Their storage availability has not been revalidated by this cleanup; check it
before reuse. Preserve failed verification evidence and attempt counts. Do not
substitute historical story checks for current or milestone verification.

## Maintenance rules

- Keep one current position and next action. Replace superseded resume instructions;
  use Git history and linked plans/reports for historical detail.
- In a story worktree, keep that summary specific to its story and checkout.
  Reconcile inherited base-branch summaries against the owning plan before
  resuming. During authorized integration to `main`, reconcile incoming checkpoint
  edits against current `main` and existing obligations; do not replace its
  summary blindly. Follow the [worktree guidance](docs/development/worktrees.md#checkpoints-integration-and-removal).
- Issues govern scope; plans own tasks, decisions, approvals and evidence. Resolve
  discrepancies against those sources before resuming. Link verification policy
  rather than duplicating it.
- At completed work, gates, blockers and handoff, refresh the date, checkout,
  working-tree changes, pending decisions, verification limits and deferred owners.
- Record approvals only after explicit developer decisions in the owning plan.
  Preserve failure evidence and attempt counts in linked records.
- Commit checkpoint updates alongside their work when authorized. Keep credentials
  and sensitive environment details outside this file.
