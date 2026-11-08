# Development Checkpoints

Last updated: 2026-11-08 (UTC)

## Current position and next action

Checkout: `US-41-distribution-init`; IP2 approved and committed as `404ba53`.
Developer “start ip3”, 2026-11-08 UTC, authorizes IP3 execution only. Gate 2
is Approved; Gate 3 Approved on 2026-11-08: developer “i approve ip3; commmit”. Issue #64 complete body/all comment pages and
final metadata refreshed: zero comments; scope unchanged. Current work adds
explicit completed-wheel upgrades and incomplete-operation recovery guards,
installed public CLI/API tests and setup instructions. See the
[plan](docs/plans/milestone-50-us-41.md) and
[IP3 evidence](docs/verification/us-41-ip3.md) for progress and attempts.
Raw logs: `.dev-records/verification/us-41-ip3-20261108/`.

IP3 T1–T4 are technically Complete; **Gate 3 Approved**; IP3 commit authorized.
M50: 899 collected, 163 selected, 736 deselected; **161 passed, 2 existing skips
in 397.20s**, exit 0. All 83 US-41 cases passed. Shared sync/lock/lint/format/
strict typing/smoke, document links and diff checks passed on Linux aarch64 /
Python 3.12.16 / uv 0.13.6. Retained upgrade replay: 2 passed, 81 deselected;
new-/same-version digests, installed origins and checksums saved in raw records.
Its exclusive `/tmp/us41-ip3-upgrade-evidence-20261108-1` is retained for review.

Current changes: identity/journal upgrade guards, incomplete synchronization
status, 17 added installed test cases, wheel bootstrap/upgrade instructions,
plan/evidence/checkpoint. Failed attempts and fixture corrections are preserved
in [IP3 evidence](docs/verification/us-41-ip3.md); original assertions remain.
No suppression, scope deviation or lock change. Lock SHA-256:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
The approved archive-history limitation and platform limits remain. Both-artifact/
Git/M1–6 renewal remains IP4. No standalone artifact driver or broader local
suite was run. Developer authorized the IP3 commit, including approval records;
no push or PR publication is authorized. Approval recording is documentation only;
existing executable evidence remains applicable. Final document/link checks and
`git diff --check` passed.
**Next action:** await direction to execute IP4.

Previous publication context follows; it does not authorize US-41 implementation.
Developer authorized squash merge and pull on 2026-11-08.
[PR #63](https://github.com/jimthompson5802/agentic-ml/pull/63) was
squash-merged as `a3d342337ac5cf72850efc2236b89eaeed7cf4ed` at
2026-11-08T12:39:49Z; local main pulled by fast-forward. Hosted
Linux / Python 3.12 CI passed before merge. Developer subsequently authorized
deleting the PR branches; local and remote `reconcile-design` were deleted after
verifying tree equality with the squash commit.

Developer authorized committing and pushing the CI documentation filters,
published as `0bc0ef7`. Both pull-request and main-push triggers ignore changes
limited to `docs/**` and root Markdown files; workflow changes still trigger CI.
Main has no required branch protection or applicable branch rules at the time
checked. Developer then authorized committing and pushing this checkpoint.
`git diff --check` passed; no executable product behavior changed, so TDD and
product tests do not apply. Hosted verification of the CI change is not claimed.
**Next action:** await developer direction.

Developer requested moving US-41 from Milestone 99 to Milestone 50 in
`docs/specs/user-stories.md`. The story placement, milestone assignment and
delivery table now reflect M50; all six acceptance criteria are unchanged.
Developer authorized committing and pushing this documentation change.
Published as `63608f4`. Developer subsequently authorized issue publication and
active design alignment; see the US-41 record below. Verification: placement/criterion preservation checks and
`git diff --check` passed. TDD and executable tests do not apply.

The design now records accepted US-11 extraction and US-12 quality/assessment/
partitions, exact split composition and project-owned persistence/identity checks.
The criterion index contains all 228 local IDs, with US-05-AC-05 integration pending
and US-41 now assigned to M50. M1/M2 outcomes, strict APIs and historical evidence are
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

## Story addition and reassignment: US-41

Developer requested US-41, distribution-based experiment initialization, locally
in `docs/specs/user-stories.md` under Milestone 99, then authorized commit and
push. Six criteria cover wheel bootstrap, initialization, identity validation,
failures, explicit upgrades and both wheel verification paths while preserving
Git installs. No implementation is authorized. Developer subsequently authorized
publication: [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64)
now owns all six unchanged criteria, labeled `enhancement` and assigned to the
new GitHub milestone “Milestone 50: Improve the technical environment”.
The published body and metadata were verified against the prepared template.
Active interfaces, ADR, delivery, blueprint and traceability documents now assign
US-41 to M50 and link its owning issue. Story criteria remain unchanged.
Developer authorized committing and pushing these documentation changes.
At publication, no implementation plan had been created; the subsequent draft is linked above. Verification: unchanged story criteria, six
M50 traceability rows, issue links, relative file targets and `git diff --check`
passed. No executable behavior changed; TDD and product tests do not apply.
The developer subsequently moved the local story to Milestone 50 on 2026-11-08.
The empty GitHub milestone “Milestone 99: Future enhancements” was created before
the developer limited story publication to the local specification. GitHub issue
synchronization for US-41 is complete. Contract review, confirmed public test
boundaries and an implementation plan remain before dependent code. This is documentation
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
