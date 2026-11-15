# Development Checkpoints

Last updated: 2026-11-15 (UTC)

## Current position and next action

Phase approval policy: the developer approved replacing default manual approval
at every implementation phase with public contract review and verification-based
automatic progression. See [phase approvals](docs/development/phase-approvals.md).
Plan review and execution authorization remain distinct. Whole-story acceptance,
publication/merge/cleanup boundaries and verification obligations are preserved.
The policy covers new plans and classification of unfinished phases on resumption;
completed approvals and historical evidence are retained. No story is executing.

Updated repository instructions, planning/execution/scope skills, verification
policy and plan template together. The developer authorized committing and
pushing these changes to origin/main. All three changed skills pass
`quick_validate.py` in the isolated uv/PyYAML environment; 108 relative links
resolve and `git diff --check` passes. Next action: pilot an authorized phase
sequence.
Runtime sandbox permissions are unchanged and devcontainer behavior is unverified.
No Python behavior changed; TDD and Python tests are inapplicable.

Primary checkout: `main`; only the primary worktree remains.
US-18 M1 classification is accepted and merged in PR #69. Its worktree and
local/remote branches have been removed; verified evidence is archived below.
Issue #28 retains M2 regression scope.

CI maintenance: added workflow-level concurrency to `.github/workflows/ci.yml`
so a newer run cancels an earlier run for the same branch or pull request,
covering both jobs. Independent pull requests keep separate concurrency groups.
Static YAML validation and `git diff --check` passed. Hosted cancellation remains
unverified until successive qualifying pushes trigger CI. No Python behavior
changed, so TDD and Python tests do not apply to this configuration change.

CI maintenance is ready for the requested commit and push to `main`.
Next action: verify hosted cancellation when successive CI runs occur or select the next story.
No story implementation is in progress.
Checkpoint cleanup and evidence archive references are included in this update.
No tests were run for this documentation change; `git diff --check` passed. Historical M1/M50 verification and revised MVP acceptance obligations
remain open below.

## Completed work: authoritative records

| Work | Final status and records |
|---|---|
| US-01–03 | Accepted and merged; [US-01](docs/plans/milestone-1-us-01.md), [US-02](docs/plans/milestone-1-us-02.md), [US-03](docs/plans/milestone-1-us-03.md). |
| US-11 | Accepted and merged in PR #60; [plan](docs/plans/milestone-1-us-11.md), [IP3 evidence](docs/verification/us-11-ip3.md). |
| US-12 #19 | Accepted and squash-merged in PR #62 as `980c97f`; [plan](docs/plans/milestone-1-us-12-assessment-splits.md), [IP4 evidence](docs/verification/us-12-19-ip4.md). AC-04 deferred. |
| US-12 #15 | Accepted and merged in PR #61; [plan](docs/plans/milestone-1-us-12.md), [IP3 evidence](docs/verification/us-12-ip3.md). |
| US-13 M1 | AC-01/02 accepted and merged in PR #66 as `ecd28b1`; Gates 1–3 Approved. [Plan](docs/plans/milestone-1-us-13.md), [IP3 evidence](docs/verification/us-13-ip3.md). Issue #16 remains open for M2 AC-03/04. |
| US-15 M1 | AC-01–03 accepted and merged in PR #68; [plan](docs/plans/milestone-1-us-15.md), [IP4 evidence](docs/verification/us-15-ip4.md). M2 AC-04 remains open under #21. |
| US-18 M1 | Classification slice accepted and merged in PR #69; Gates 1–4 Approved. [Plan](docs/plans/milestone-1-us-18.md), [IP4 evidence](docs/verification/us-18-ip4.md), [publication evidence](docs/verification/us-18-publication.md). M2 regression remains under #28. |
| US-26 recording #17 | AC-01–05 accepted and merged in PR #68; [plan](docs/plans/milestone-1-us-26-recording.md), [publication evidence](docs/verification/us15-us26-publication.md). #33/#43 remain open; #17 still appeared open at the last GitHub check. |
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

The removed story worktrees' retained evidence was archived with verified
checksums, inventories and link targets during cleanup:

- US-18: `.dev-records/worktree-archives/20261115T181243Z-US-18-classification-d7916d0`.
- US-15: `.dev-records/worktree-archives/20261115T025402Z-US-15-preprocessing-459e8ba1`.
- US-26: `.dev-records/worktree-archives/20261115T025408Z-US-26-mlflow-9f100e11`.

Each archive contains `archive-manifest.json`. Preserve the contributor worktree
management evidence under
`.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/`, its
retained validation fixture and host evidence linked from the
[worktree management report](docs/verification/story-worktree-management.md).
Earlier local planning edits remain in autostash `5db8c8c`.

Raw evidence paths and detailed measurements belong in verification reports.
US-18 archive contents were verified during removal. Other historical storage
availability was not revalidated; check it before reuse. Preserve failed
verification evidence and attempt counts. Do not substitute historical story checks for current or milestone verification.

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
