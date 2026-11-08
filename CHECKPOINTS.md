# Development Checkpoints

Last updated: 2026-11-08 (UTC)

## Current position and next action

Checkout: `US-12-assessment-splits`, IP4 baseline `ffd5322`, initially clean.
Developer “start ip4”, 2026-11-08 UTC, authorized final installed verification.
Developer “i approve ip4; commit”, 2026-11-08 UTC, approves Gate 4 and
authorizes a local IP4 commit.
Developer “i accept issue #19”, 2026-11-08 UTC, accepts AC-02/03 and both layouts.
Developer “resolve this review comment”, 2026-11-08 UTC, authorizes correction
of discussion r4504392360.
**Next action:** await PR #62 merge direction. Review correction is complete;
no subsequent story work is authorized.
IP1–IP4 technical tasks Complete; Gates 1–4 Approved.
IP4 adds installed project/probe/driver and M1 regression, README/guide/design
status updates, plan/evidence/checkpoint. No toolkit runtime behavior changed.
Both normal direct and sdist-rebuilt wheels pass assessment/partition matrices,
installed identity/inventory/resource/CLI checks and cleanup. M1 and final M1–6
each pass 713 tests with one existing skip (714 selected). Shared checks, guide
demo and local document checks pass. Lock hash is unchanged from IP3 below.
The [IP4 evidence](docs/verification/us-12-19-ip4.md) owns commands, raw records,
probe corrections, actual counts and Linux aarch64 limits. macOS/Windows remain
unverified. Issue #19 accepted and published as
[PR #62](https://github.com/jimthompson5802/agentic-ml/pull/62) against `main`;
acceptance commit `a672dca` pushed.
[Static review](https://github.com/jimthompson5802/agentic-ml/pull/62#pullrequestreview-5815831258)
published and verified, with one
[Low finding](https://github.com/jimthompson5802/agentic-ml/pull/62#discussion_r4504392360)
for stale current status in active data/interface design pages was addressed
in pushed commit `23b260d`; thread resolution was verified on GitHub. The requested
correction updates both pages and links completed identity/installed evidence,
preserving the old heading anchor. Document checks pass: 101 local links/anchors,
status/acceptance consistency, legacy anchor and whitespace. No executable
changes or product tests; prior evidence remains applicable.
Static review was renewed at `6df5c1b` (review 5815835314).
Issue closure awaits merge; no merge or branch cleanup authorized.
IP4 is committed as `600f49e`. Acceptance-record edits preserve test evidence;
no executable changes follow the final verification.

The [approved contract](docs/data-assessment-and-splits.md) retains two optional
helpers, native pandas assessment/scikit-learn splits and project-owned JSON
persistence. IP2 implements `assess_data`; IP3 adds `create_partitions` with seeded
and supplied two-way/three-way layouts, complete disjoint ordered membership,
source identity and contextual failures. Project-owned JSON reconstruction and
extraction/quality/preparation composition pass. Time/group protocols remain
declarations; identity is version-bound native Parquet.

M1 passed 712 tests with one existing skip (713/815 selected, 102 deselected).
All 124 focused cases pass. Locked synchronization, lint, formatting, strict
typing, lock consistency and version smoke pass. The intentional lock update adds
only direct scikit-learn metadata; final SHA-256 is
`5f99c2da64eb46bc758f798f364e67eab25246253fc75315ebb404461e466a9d`.
The [IP3 evidence](docs/verification/us-12-19-ip3.md) owns red/green commands,
attempts, raw records and limits. IP4 subsequently completed both installed matrices and final M1–6; Linux aarch64 is the only platform verified in IP3.

Issue #19 complete body and all comments refreshed with stable final timestamp
`2026-11-07T21:38:29Z`, one unique comment and open state. Scope is unchanged:
M1 AC-02/03 active, AC-04 deferred. Configured-token status failed but required
GET reads succeeded. Accepted suppliers #14/#15 and their historical evidence
remain intact. [IP1 evidence](docs/verification/us-12-19-ip1.md) owns Gate 1.

US-12 issue [#15](https://github.com/jimthompson5802/agentic-ml/issues/15)
is accepted and closed. PR #61 squash-merged as `1f9eb86`; local and remote
`US-12-data-validation` branches were deleted after tree equality was verified.
The [plan](docs/plans/milestone-1-us-12.md) and
[final correction evidence](docs/verification/us-12-pr61-r1.md) own approvals,
failed attempts and verification. Final M1 and M1–6 selections each passed
553 tests with one existing skip (554/656 selected); shared checks passed.
Evidence is Linux aarch64 only; installed regressions passed, with new edge
cases checked through editable public APIs. Issue #19 separately owns assessment
and partitions; AC-04 remains deferred. Closing #15 does not complete all US-12.

Current delivery scope: M1 local classification experiment, M2 usability and
committed-project reproduction; M0 accepted, M50 ongoing, M99 deferred.
[Stories](docs/specs/user-stories.md) govern milestone context; GitHub issues
govern implementation scope. No subsequent story implementation is authorized.

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
| US-12 #15 | Accepted and merged in PR #61; [plan](docs/plans/milestone-1-us-12.md), [IP3 evidence](docs/verification/us-12-ip3.md), correction linked above. |
| MVP scope revision | Accepted and published; PR #57 merged; US-39 #58 and US-40 #59 created. [Plan](docs/plans/mvp-scope-revision.md), [publication evidence](docs/verification/mvp-scope-revision-ip4.md). This accepts scope documents, not an implemented MVP. |
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
