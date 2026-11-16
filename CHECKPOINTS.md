# Development Checkpoints

Last updated: 2026-11-16 (UTC)

## Current position and next action

US-14 / issue #20 is accepted; IP3 is complete in branch
`US-14-feature-pipelines`, worktree `.worktrees/US-14-feature-pipelines`,
Accepted-story implementation and verification commit: `b02a218`.
Developer “i approve phase 3”, 2026-11-15 UTC, authorized execution only.
The [plan](docs/plans/milestone-1-us-14.md) records IP3-T1–T3 Complete,
`Automatic — verification passed`, 2026-11-16 UTC. Developer “I approve phase 3”,
2026-11-16 UTC, subsequently approved the completed phase. Contract v2 remains approved.
Developer “I accept the user story; commit the changes”, 2026-11-16 UTC,
accepted all five criteria and authorized accepted-story publication through
execute-plan. Published [PR #70](https://github.com/jimthompson5802/agentic-ml/pull/70)
against main. The [static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/70#pullrequestreview-5913922925)
covers `b02a218` with no actionable findings. The publication-record commit
receives a final static head review; its URL/identity are retained in the PR
timeline and raw publication record. Next: developer PR review/merge decision.

[IP3 evidence](docs/verification/us-14-ip3.md): direct and genuinely sdist-rebuilt
wheel recipes pass in separate runtime-only projects; final focused selection
45 passed; M1–6 completed 1,026 passed / 1 existing developer-authorized US-03
skip / 0 failures or errors. The skipped damaged-planning-schema check remains
with M1-ACCEPT-VERIFY and is not passing US-14 evidence. Other historical
obligations below remain unchanged. Shared checks, lock identity, CLI smoke,
local links and whitespace pass. No new suppression, skip or contract change.
Linux aarch64 / Python 3.12.16; unverified platforms and M2 remain outside claims.

Run pytest directly; save full tool output separately. Do not use the old runner.
Raw records: `.dev-records/verification/20261115T233328Z-762aa23-us14-ip3/`,
with nested driver records linked from the report. Preserve all earlier evidence.
Implementation, tests and acceptance records are committed and pushed;
this final update records publication outcomes only. See
[publication evidence](docs/verification/us-14-publication.md).
Whole-story acceptance is recorded in the plan; publication is authorized by
that explicit acceptance. Merge and cleanup remain separate.

Local integration, 2026-11-16 UTC: developer requested merging `main` into
`US-14-feature-pipelines`. Merged local `main` at `03914ed`; resolved the
checkpoint conflict by retaining this story's status and historical obligations.
Incoming documentation clarifies direct command execution and complete evidence
capture in AGENTS.md, the command policy and records guide. No executable
behavior changed, so TDD and Python tests do not apply. Merge validation:
`git diff --check` and staged whitespace/conflict-marker checks pass.
The integration is committed locally; pushing this merge remains pending.

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
