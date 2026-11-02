# Development Checkpoints

Last updated: 2026-11-02 (America/New_York)

## Current position and next action

Current checkout is `main`. Added the requested
[development workflow summary and Mermaid diagram](docs/development-workflow.md).
Expanded the implementation section and diagram with the red, green, refactoring,
evidence-recording and repeat steps, including the documentation-only path.
Named the behavior-change loop as closed-loop agentic TDD in the description and
diagram, explaining its feedback and autonomy boundaries.
This documentation task changes that file and `CHECKPOINTS.md`; the pre-existing
`.devcontainer/devcontainer.json` modification is unrelated and remains untouched.
Relative document links and whitespace checks passed. TDD and product tests do
not apply because this change adds no executable behavior. Mermaid rendering was
not verified. No tests are running from this session.

**Next action:** await developer direction on subsequent work.
No next-story implementation is authorized. No completed-story
implementation gates remain pending.

Milestone 0 is accepted. Milestone 1 is in progress; US-01–US-03 are accepted
and merged. Milestone 50 tracks ongoing technical environment improvements;
US-35 and US-36 are accepted and merged. US-37 and US-38 remain local stories
without implementation authorization. Milestone 99 remains deferred. See
[user stories](docs/specs/user-stories.md) for milestone context.

## Completed work and authoritative records

| Work | Status and authoritative records |
|---|---|
| US-01 and US-02 | Accepted and merged; [US-01 plan](docs/plans/milestone-1-us-01.md), [US-02 plan](docs/plans/milestone-1-us-02.md). |
| US-03 | Accepted and merged in [PR #46](https://github.com/jimthompson5802/agentic-ml/pull/46); [plan](docs/plans/milestone-1-us-03.md), [cost/currency correction evidence](docs/verification/us-03-cost-currency-correction.md). |
| US-35 | Both phases approved; story accepted and merged in [PR #48](https://github.com/jimthompson5802/agentic-ml/pull/48); [plan](docs/plans/milestone-50-us-35.md), [IP2 evidence](docs/verification/us-35-ip2.md). |
| US-36 | Both phases approved; story accepted and merged in [PR #50](https://github.com/jimthompson5802/agentic-ml/pull/50); [plan](docs/plans/milestone-50-us-36.md), [IP2 evidence](docs/verification/us-36-ip2.md). |
| Development-guide reorganization | Approved and committed; [plan](docs/plans/development-guide-reorganization.md), [evidence](docs/verification/development-guide-reorganization.md). |
| Development container | [PR #51](https://github.com/jimthompson5802/agentic-ml/pull/51) squash merged as `3a967e2`; final-head [Linux/Python 3.12 CI](https://github.com/jimthompson5802/agentic-ml/actions/runs/41389834925) passed. Local and remote `test-devcontainers` branches deleted after tree equality with the squash merge was verified. Publication and cleanup records committed and pushed through `b2917ce`. |

Plans and linked reports own granular tasks, scope decisions, approvals,
acceptance, verification commands/results, failed attempts and publication records.
Earlier checkpoint snapshots remain in Git history.

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
  remain unverified. The committed uv workspace member references a generated
  pytest directory; PR #51 records this known concern. Hosted CI does not
  establish container functionality.
- **Platform coverage:** Recorded local story evidence is macOS 15.7.9 arm64 /
  Python 3.12.15. Hosted Linux/Python 3.12 results are separate evidence;
  Windows remains unverified. Consult each report for its tested inputs and limits.
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
