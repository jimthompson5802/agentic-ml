# Development Checkpoints

Last updated: 2026-11-08 (UTC)

## Current position and next action

Checkout: `reconcile-design`, baseline `49292df`, initially clean for this review.
Developer “ok make the changes”, 2026-11-08, authorized the proposed source/design
documentation reconciliation. Developer “commit changes” subsequently authorized
the local documentation commit. Corrections are complete: active
design topics/walkthrough, three linked usage guides, the
[reconciliation report](docs/reviews/source-design-reconciliation-2026-11-08-07-19.md)
and this checkpoint are included in that commit. Developer “create pull request”,
2026-11-08, authorizes branch publication and a PR from `reconcile-design` to
`main`. [PR #63](https://github.com/jimthompson5802/agentic-ml/pull/63) is open;
title, body, branch ownership, base/head and non-draft status were verified.
No product implementation is authorized. **Next action:** await developer PR
review and merge direction. Publication checks passed `git diff --check`;
the prior documentation evidence below remains the validation boundary.

The design now records accepted US-11 extraction and US-12 quality/assessment/
partitions, exact split composition and project-owned persistence/identity checks.
The criterion index contains all 228 local IDs, with US-05-AC-05 integration pending
and US-41 deferred to M99. M1/M2 outcomes, strict APIs and historical evidence are
preserved. Verification is documentation-only: criterion set/uniqueness, 43 public
exports across eight module surfaces, relative links/anchors, manual diff/source
review and `git diff --check`. No executable behavior changed; TDD/product tests
and artifact checks do not apply. Lockfile unchanged. Existing milestone/platform
limitations below remain open; this review supplies no renewed runtime evidence.

US-12 issue [#19](https://github.com/jimthompson5802/agentic-ml/issues/19)
AC-02/03 and both split layouts are accepted; IP1–IP4 Complete and Gates 1–4
Approved. [PR #62](https://github.com/jimthompson5802/agentic-ml/pull/62)
squash-merged as `980c97f34e4dcac3d13086825641b821e13f80d4` at
2026-11-08T01:12:16Z; issue #19 closed at 01:12:17Z. Local `main` pulled by
fast-forward. Developer subsequently requested deleting the PR branches;
local and remote `US-12-assessment-splits` were deleted after verifying their
head `a018794` had the same tree as squash commit `980c97f`. The owning
[plan](docs/plans/milestone-1-us-12-assessment-splits.md) and
[IP4 evidence](docs/verification/us-12-19-ip4.md) preserve acceptance,
publication/review, resolved documentation finding and verification limits.
The requested completion records are documentation only; existing executable
evidence remains applicable. No product tests were rerun for merge records.

Assessment and partitions use native pandas/scikit-learn through two optional
helpers. Project code owns JSON persistence and old/current identity comparisons.
Time/group protocols remain declarations; source identity is version-bound
native Parquet. Both installed wheel paths passed. Final M1 and M1–6 each passed
713 tests with one existing skip (714 selected); shared checks and guide demo
passed on Linux aarch64 / Python 3.12.16. macOS/Windows remain unverified here.
Pre-merge hosted Linux/Python 3.12 CI passed at head `a018794`;
[run 42432054301](https://github.com/jimthompson5802/agentic-ml/actions/runs/42432054301)
does not close historical milestone verification obligations. Lock SHA-256:
`5f99c2da64eb46bc758f798f364e67eab25246253fc75315ebb404461e466a9d`.
AC-04 remains deferred; downstream fitting, tracking, DVC and assistant
integration remain separately owned. No subsequent story implementation authorized.

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

## Deferred story addition: US-41

Developer requested US-41, distribution-based experiment initialization, locally
in `docs/specs/user-stories.md` under Milestone 99, then authorized commit and
push. Six criteria cover wheel bootstrap, initialization, identity validation,
failures, explicit upgrades and both wheel verification paths while preserving
Git installs. No implementation is authorized and no GitHub issue was published.
The empty GitHub milestone “Milestone 99: Future enhancements” was created before
the developer limited story publication to the local specification. GitHub issue
synchronization remains required before implementation. This is documentation
only; TDD and executable checks do not apply. Verification: reviewed the story
placement and criteria; `git diff --check` passed. Next action: await direction.

## Completed work: authoritative records

Refreshed [MVP project status](docs/project-status.md) against current GitHub
issue states, the US-12 #19 plan and final evidence. The overview now uses a UTC
date and explicitly records delivered criteria, both split layouts, deferred
AC-04 and separately owned integration. Documentation only: TDD and executable
tests do not apply; relative links and `git diff --check` verified. This handoff
changes only the status overview and this checkpoint; no implementation authorized.

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
