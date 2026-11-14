# Development Checkpoints

Last updated: 2026-11-14 (UTC)

## Current position and next action

US-26 Phase 2 approved / local commit handoff, 2026-11-14 UTC: issue #17,
branch US-26-mlflow, worktree .worktrees/US-26-mlflow. Phase 1 baseline is
3108645; Git HEAD identifies this Phase 2 approval commit after committing.
Developer in coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a approved
both Gate 1 decisions and said “commit the changes and start phase 2 in both
stories”. Reconciled Phase 1 was committed as 3108645. The later developer
decision on 2026-11-14 UTC in the same coordination thread is:
“for both us-15 and us-26 i approve the phase 2 gate, commit the changes.”
Both Gate 2 approvals and local Phase 2 commits are authorized. This approval
commit includes only US-26 changes; Git history identifies its commit SHA.

[Owning plan](docs/plans/milestone-1-us-26-recording.md) IP2-T1–T4 are Complete;
**Gate 2 is Approved**. The [IP2 evidence](docs/verification/us-26-recording-ip2.md)
records the exact approval. Next action after this local approval commit:
await separate Phase 3 direction. Phase 3, push/publication, source integration,
cleanup and sibling edits are not authorized.

Implemented public log_run_results records native MLflow values/artifacts,
strict committed provenance/native DVC integrity, installed normal wheel/Git
identities and locked versions, required-output/process/validation outcomes,
notebook bytes and available failure diagnostics. SC-01 schema and future
preprocessing interface remain unchanged; log_preprocessing is not implemented.

Final focused tracking/DVC run: 68 passed, zero failed/skipped/deselected,
4 workers/loadgroup, 168.01 seconds. Shared sync/lock/lint/format/type/CLI and
document/whitespace checks pass. The first focused run had four evidence-logger
failures and the second had three incorrect notebook-fixture commit references;
original XML/logs, hypotheses and corrections remain in the IP2 report. No
assertion/check was weakened or suppressed. No initializer internals or package
resources/dependencies changed; lock SHA-256 remains
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.

Raw evidence: .dev-records/verification/us26-ip2-20261114/ and
.dev-records/verification/us26-ip2-native-commands/. Preserve all earlier IP1 /
SC-01 records and default-skops failure. Linux aarch64/Python 3.12.16 only.
No full suite/M1–6 acceptance, standalone driver, rebuilt-wheel producer
integration, story/milestone acceptance or publication is claimed.

The authorized commit includes the tracking package, component tests/support,
guide, shared index, owning plan, checkpoint and IP2 report. No executable file
changed after the passing Phase 2 verification. Broader installed/preprocessing and
final acceptance checks remain with IP3/IP4 and named milestone owners.

Historical obligations below remain unchanged. Preserve the contributor worktree
management plan/report, raw records under
`.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/`, the
retained worktree-validation fixture and linked host evidence described in
[its report](docs/verification/story-worktree-management.md). Their current
storage availability has not been revalidated. Historical publication/next-action
wording inherited from main is superseded by this story-specific handoff.

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
