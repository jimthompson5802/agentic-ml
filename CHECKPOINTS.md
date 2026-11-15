# Development Checkpoints

Last updated: 2026-11-15 (UTC)

## Current position and next action

Primary checkout update (2026-11-15 UTC): PR #68 was squash-merged as
`a2c6262701a34773d1b9ab50cfb1d958a82768b7`; both hosted Linux CI jobs passed.
Primary `main` was fast-forwarded to that revision. Issue #21 remains open for M2.
Publication/merge-pending wording below is historical. Earlier local planning
checkpoint edits are preserved in autostash `5db8c8c`; the newer accepted-story
checkpoint takes precedence.

The developer explicitly authorized deleting the related local/remote branches
and committing/pushing this checkpoint. Local `US-15-preprocessing` and
`US-26-mlflow` and remote `US-15-preprocessing` were deleted; the remote branch
list confirms neither story branch remains. No remote US-26 branch existed.
Both owning sessions verified clean worktrees with no active tests and detached
their own checkouts before deletion. Worktrees and all raw verification evidence
remain in place:

- `.worktrees/US-15-preprocessing`: detached at
  `b4a02216f1e7962d2a5bb44992264b18844b88dd`.
- `.worktrees/US-26-mlflow`: detached at
  `ecbceb2aa213da8f3e3f1d902eb9f730eca6bbb7`.

No worktree, evidence, stash, or unrelated branch was removed. Next action:
await development direction; #21 M2 restoration work remains open.

US-15 Phase 4 approved / M1 slice accepted, #21, branch `US-15-preprocessing`.
The approved implementation baseline is combined
`3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1`, integrated by authorized fast-forward.
Current HEAD after local commitment identifies the final acceptance-record commit.
Both approved parents remain in history. Consumer
Gate 4 approval and explicit combined integration/execution authority are recorded
in the owning plans. US-15-IP4-T1/T2 are Complete; US-15 Gate 4 is Approved and
M1 AC-01/02/03 explicitly Accepted on 2026-11-15. No M2 or whole-story acceptance.

[IP4 report](docs/verification/us-15-ip4.md) records independent preservation
review and renewed actual producer handoff through direct and genuinely rebuilt
installed wheels. All 28 retained artifact/identity hashes pass in supplier and
own final matrix; metadata/provenance/split and feature bytes match exactly.
All 83 consumer-tested executable fingerprints and producer implementation/tests
remain unchanged. Own preparation and reviewed supplier evidence are preserved
under `.dev-records/verification/20261114-us15-ip4/`, spanning the UTC boundary.

Own final M1–6: 924 passed, one existing authorized planning-schema skip, zero
failures/errors, 427.02 seconds, four workers/loadgroup. Collection: 1193 total,
925 selected, 268 deselected. Shared locked sync/lock/lint/format (350 files)/
strict typing (91 files)/CLI 0.1.0 pass. Final document/whitespace checks are
recorded in the gate manifest. Lock unchanged at
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
No assertion/timeout/skip/suppression changes or new product defect. Linux aarch64 /
Python 3.12.16 only; native float16 limitation and all earlier failures preserved.

Both stories' acceptance records are integrated for one combined PR. US-26 #17
AC-01–05 and US-15 #21 M1 AC-01/02/03 are Accepted; M2 AC-04 remains open.
Developer authorized the [PR structure](docs/reviews/us15-us26-pr-structure.md),
ordinary push, one PR to main and a static COMMENT review through coordination
thread `01a1db6c-a225-73e0-8796-81a03c4cec7a`. Publication owner: this US-15
checkout. [PR #68](https://github.com/jimthompson5802/agentic-ml/pull/68) is Open
against main after ordinary push; both accepted record tips are preserved in
merge `638eb35`. The final-head static COMMENT review and verification are
recorded in the publication raw outcome. Next action after this handoff: await
developer direction on the open PR; no merge is authorized. Initial hosted Linux CI jobs
are queued, not passing evidence. Final head/review/CI snapshot is retained
in the publication raw records, linked from
[publication evidence](docs/verification/us15-us26-publication.md).
No force push, history rewrite, PR merge, main merge, issue closure or cleanup.
All executable inputs and lock remain unchanged; no tests need renewal for
acceptance/documentation integration. Preserve both owners' raw evidence.

Historical obligations below remain unchanged. Preserve the contributor worktree
management plan/report, raw records under
`.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/`, the
retained worktree-validation fixture and linked host evidence described in
[its report](docs/verification/story-worktree-management.md). Their current
storage availability has not been revalidated. Historical publication/next-action
wording inherited from main is superseded by this story-specific handoff.


Worktree removal authorized on 2026-11-15 UTC. Before removal, both detached
worktrees were clean, with no active processes in their directories. Their tips
were verified against merged PR #68 (US-26 is an ancestor of its published head).
All retained evidence was copied and file checksums, directory inventories and
link targets verified in these primary-checkout archives:

- `US-15-preprocessing` → `.dev-records/worktree-archives/20261115T025402Z-US-15-preprocessing-459e8ba1`
- `US-26-mlflow` → `.dev-records/worktree-archives/20261115T025408Z-US-26-mlflow-9f100e11`

Each archive contains `archive-manifest.json` with original paths, commit and
verified inventories. Other ignored entries are disposable `.venv`, tool caches
and Python bytecode. Prior retained-worktree wording above is historical.
Removal status: both worktrees removed with ordinary `git worktree remove`;
only the primary checkout remains registered. Archive manifests remain available.
No forced removal, pruning or historical evidence deletion was used.

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
