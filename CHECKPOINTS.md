# Development Checkpoints

Last updated: 2026-11-08 (UTC)

## Current position and next action

Checkout: `main` at `2b7268a` (`docs: record US-41 merge and branch cleanup`).
The working tree was clean before this status review; this handoff changes only
`CHECKPOINTS.md` and `docs/project-status.md`. No implementation or publication
is authorized by this documentation task.

US-41 is accepted and merged. [Issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64)
is closed in M50; its complete body, all comment pages (zero comments) and stable
final metadata were verified on 2026-11-08 UTC. All six criteria are accepted in
the [owning plan](docs/plans/milestone-50-us-41.md); Gates 1–4 are Approved.
[PR #65](https://github.com/jimthompson5802/agentic-ml/pull/65) squash-merged as
`5d5781c` at 20:51:51Z. Local main was pulled; local and remote
`US-41-distribution-init` branches were deleted after tree equality was verified,
as recorded in `2b7268a`.

Hosted [run 42520936609](https://github.com/jimthompson5802/agentic-ml/actions/runs/42520936609)
completed successfully at head `1532ba2`. The independent default and other-test
jobs both started at 20:35:51Z, finishing at 20:44:38Z and 20:50:27Z respectively.
This supersedes earlier pending-CI and open-PR snapshots in the publication
records; those records preserve their historical context. The contributor CI
split is complete, approved and merged with PR #65. Collection verification
recorded default 721, complement 268 and all 989, with disjoint complete coverage;
raw records are in `.dev-records/verification/ci-split-20261108/`.

US-41 [IP4 evidence](docs/verification/us-41-ip4.md) records 166 passing installed
cases (83 through each wheel path), seven legacy Git/source-switch regressions,
M50 **244 passed / 2 existing skips**, and M1–6 **720 passed / 1 existing skip**.
Shared checks passed on Linux aarch64 / Python 3.12.16 / uv 0.13.6. Existing
archive-history, timeout-skip and platform limitations remain; story acceptance
and hosted CI do not close historical milestone verification obligations below.

The MVP issue states in `docs/project-status.md` were checked against GitHub's
complete current issue inventory. US-12 remains the latest accepted M1 delivery;
US-41 is the newer M50 delivery outside the MVP table. No subsequent story
implementation is authorized. Superseded resume instructions and intermediate
publication snapshots were removed from this checkpoint; Git history and linked
plans/reports retain them.

Documentation only: TDD and executable tests do not apply. Relative file links
and `git diff --check` passed; no renewed runtime or artifact evidence is claimed.
**Next action:** await developer direction; US-41 publication and branch cleanup
are complete. Developer authorized committing and pushing this status refresh.
The documentation commit includes both status files; `git diff --check` and
relative-file link checks passed. No executable tests were needed.

## Completed work: authoritative records

Contributor skill added: `.agents/skills/report-test-progress/` monitors an
existing pytest session in the current chat and reports remaining/total,
completed and failed counts approximately every minute. It never launches tests;
unavailable counts remain explicitly unknown. Documentation-only instructions
and UI metadata add no executable behavior, so TDD does not apply. No pytest run
was started for this work. Existing US-12 changes and Gate 2 status are unchanged.

| Work | Final status and records |
|---|---|
| US-01–03 | Accepted and merged; [US-01](docs/plans/milestone-1-us-01.md), [US-02](docs/plans/milestone-1-us-02.md), [US-03](docs/plans/milestone-1-us-03.md). |
| US-11 | Accepted and merged in PR #60; [plan](docs/plans/milestone-1-us-11.md), [IP3 evidence](docs/verification/us-11-ip3.md). |
| US-12 #19 | Accepted and squash-merged in PR #62 as `980c97f`; [plan](docs/plans/milestone-1-us-12-assessment-splits.md), [IP4 evidence](docs/verification/us-12-19-ip4.md). AC-04 deferred. |
| US-12 #15 | Accepted and merged in PR #61; [plan](docs/plans/milestone-1-us-12.md), [IP3 evidence](docs/verification/us-12-ip3.md), correction linked above. |
| MVP scope revision | Accepted and published; PR #57 merged; US-39 #58 and US-40 #59 created. [Plan](docs/plans/mvp-scope-revision.md), [publication evidence](docs/verification/mvp-scope-revision-ip4.md). This accepts scope documents, not an implemented MVP. |
| US-41 | All six criteria accepted; issue #64 closed; PR #65 squash-merged as `5d5781c`. [Plan](docs/plans/milestone-50-us-41.md), [IP4 evidence](docs/verification/us-41-ip4.md). Historical M50 verification remains open. |
| US-35/36 | Accepted and merged in PRs #48/#50; [US-35](docs/plans/milestone-50-us-35.md), [US-36](docs/plans/milestone-50-us-36.md). US-37/38 remain local stories without implementation authorization. |
| Contributor tooling | Development guide reorganization, scheduling, dependency inventory and container work are recorded in [verification reports](docs/verification/) and Git history; container limitations remain below. |

Plans and reports own granular tasks, approvals, commands, failures and publication
records. Earlier checkpoint snapshots remain in Git history; superseded gate and
resume instructions have been removed. Historical records are not current authority
to proceed past a gate.

## Outstanding verification and known limitations

- **M1-ACCEPT-VERIFY — Milestone 1 acceptance verification:** Open. The
  [approved ownership record](docs/plans/milestone-1-us-03.md#scope-change-record-local-verification-policy-2026-10-31)
  owns the full local suite, reserved milestone test, unchanged caller and
  initialization regressions, upgrade/scheduling and remaining artifact checks.
  The historical US-03 snapshot deferred 132 of 315 collected cases. The
  [interrupted additional run](docs/verification/us-03-ip4.md#additional-full-suite-run-requested-after-phase-approval)
  is incomplete evidence, not a passing full run. Hosted CI success does not
  close this obligation.
- **M50-ACCEPT-VERIFY — Milestone 50 acceptance verification:** Not started.
  The [US-35 handoff](docs/plans/milestone-50-us-35.md#milestone-acceptance-handoff)
  and [US-36 plan](docs/plans/milestone-50-us-36.md) own full-suite, unchanged
  caller, reserved milestone and applicable platform/manual deferrals. The
  historical US-36 snapshot deferred 289 of 393 collected cases. This obligation
  remains independent of M1-ACCEPT-VERIFY.
- **Milestone evidence reconciliation:** Before milestone acceptance, reconcile
  all deferrals, selections and actual counts against final milestone inputs;
  run the full suite, shared checks and applicable distribution, installation,
  manual and platform checks under the
  [verification policy](docs/development/verification.md#phase-and-story-verification).
  Historical counts are not current test inventories. Story acceptance does
  not imply milestone acceptance.
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
- Issues govern scope; plans own tasks, decisions, approvals and evidence. Resolve
  discrepancies against those sources before resuming. Link verification policy
  rather than duplicating it.
- At completed work, gates, blockers and handoff, refresh the date, checkout,
  working-tree changes, pending decisions, verification limits and deferred owners.
- Record approvals only after explicit developer decisions in the owning plan.
  Preserve failure evidence and attempt counts in linked records.
- Commit checkpoint updates alongside their work when authorized. Keep credentials
  and sensitive environment details outside this file.
