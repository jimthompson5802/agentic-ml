# Development Checkpoints

Last updated: 2026-11-03 (UTC)

## Requested three-test rerun — 2026-11-03

On `main`, the developer requested renewal of the three timeout failures from
the supplied Linux full-suite output. Ran `uv run --locked pytest -n 4
--dist=loadgroup -m ""` with the explicit selectors
`test_failed_installed_probe_retains_available_environment`,
`test_missing_planning_schema_fails_installed_inventory`, and
`test_rebuilt_probe_failure_retains_both_environments` in their integration
modules. All three passed in 54.64s on Linux / Python 3.12.16; exit 0.
JUnit output: `/tmp/agentic-ml-three-retry.xml`. No test code, assertions or
timeouts changed. This selected rerun does not establish a passing complete
suite or explain the earlier timeouts. Existing uncommitted scheduling,
development guidance, test and devcontainer changes remain; this rerun adds
only this checkpoint entry. Next action: developer direction; milestone
verification obligations below remain open.

## Current position and next action

2026-11-03 container commit-signing diagnosis: recent commits `1024918`,
`bc8ed5d` and `e52b800` have no signatures (`git log` reports `N`). Container
Git configuration has author identity but no `commit.gpgsign` or
`user.signingkey`. Earlier commit `2100c74` contains a GPG signature using
fingerprint `062B6663BE256CD6C7BCD421514503114FA7366E`. Container GPG home
contains an agent socket but no public keyring; local verification cannot
check that earlier signature. Signing through the host agent has not been
verified. Next action for this follow-up: configure signing and make the host
public key available before validating a signed temporary commit. No signing
configuration, commits or remote history changed. Pre-existing script and
checkpoint edits remain. This diagnosis changes no executable harness behavior;
TDD and harness tests do not apply.

2026-11-03 Git identity follow-up: updated `.devcontainer/post-create.sh` at
the developer's request to set container-user global Git identity to
`Jim Thompson <jimthompson5802@gmail.com>` during creation. Shell syntax,
an isolated temporary Git-config probe of the exact added commands, and
`git diff --check` passed. The probe confirmed both identity values and
repeat execution. Full container creation remains unverified. This is
environment setup with no new harness behavior, so harness TDD does not apply.
Pending changes are the script and this checkpoint; no publication requested
for this follow-up. Next action: developer review or container recreation to
apply the setup. Existing milestone verification obligations remain open.

2026-11-03 container security follow-up: current checkout is `main`.
The latest `.devcontainer/devcontainer.json` change adds top-level `runArgs`
with `--security-opt=seccomp=unconfined`; the AppArmor option remains commented
out and is inactive. The file uses JSON with comments. In the current Linux
container, a sandboxed `pwd` command succeeded (exit 0) and returned
`/workspaces/agentic-ml`. This verifies basic sandbox command execution;
container rebuild behavior and broader sandbox operations remain unverified.
This configuration-only change does not require harness TDD. Pending changes:
the devcontainer configuration and this checkpoint. The developer authorized
committing and pushing this follow-up on 2026-11-03; `git diff --check` passed
before publication. Published as `1024918` to `origin/main`; the working tree
was clean afterward. Existing milestone verification obligations remain open.
Earlier publication and verification records below describe prior work.

2026-11-03 publication decision: the developer accepted the current changes
after supplying a completed Linux run (394 passed, three 120-second timeouts
in 581.14s) and observing all three selected retries pass in 54.64s.
They explicitly authorized committing and pushing all pending changes, including
the recorded devcontainer follow-up. This supersedes the pending-direction and
no-publication statements below. No single all-passing complete suite or resolved
timeout cause is claimed. Existing milestone obligations remain open. Publication
completed: commit `e52b800` was pushed to `origin/main`. Final whitespace and
shell syntax checks passed. Next action: developer direction; see the scheduling
report for the final verification record.

Current checkout is `main`. Completed the developer-requested test scheduling
change: 289 phase cases and 108 acceptance cases (397 total). Default collection
selects CLI, initialization, planning and approval tests; other tests carry
`story_acceptance`. New tests default to phase; new Milestone 2–6 tests must stay
there. Story acceptance runs both groups, including the former milestone-only
initialization case. CI remains all-tests. Policy, template, workflow, skills
and owning historical plans have been reconciled; approvals remain intact.

Verification: five scheduling regressions and all shared checks passed. The full
macOS run finished with 394 passes and three failures. The isolated host renewal
completed one pass before developer-requested interruption; the two outstanding
distribution cases then passed in devcontainer aa2f61daec0c (Linux/Python 3.12.16),
2 passed in 150.59s. No single all-passing full suite is claimed; macOS timeout
causes remain unresolved. Lock checksum unchanged. See [evidence](docs/verification/test-scheduling-groups.md)
and retained `.dev-records/verification/20261102-test-schedule/` logs/XML.

**Next action:** developer direction. The complete-suite devcontainer invocation
was stopped at the developer's request (exit 130). The interrupted run recorded 93 passes and 8 errors (101 reported cases),
leaving 296 cases incomplete; this is not a completed suite. Logs are retained in `logs/devcontainer-full-suite.log`. Do not
restart tests without direction. Scheduling changes remain uncommitted; existing
milestone verification obligations remain open. No publication requested.


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

## Pre-existing development container follow-up

Current checkout is `main`. Updated `.devcontainer/devcontainer.json` so
`postCreateCommand` copies host Codex config, skills and rules from read-only
staging mounts into the persistent container Codex directory. Matching files are
overwritten; container-only files are retained. Ordinary restarts do not copy.
The pre-existing devcontainer edits were incorporated and their missing comma fixed.

Verification: a Python standard-library fixture probe parsed the JSON, ran
`bash -n -c` on the complete creation command, and executed its copy prefix
against temporary directories twice. Config replacement, nested/hidden files,
updated host contents and retained container-only files passed.
`git diff --check` passed. Container creation/restart and Linux copy behavior
remain unverified; verification ran on macOS. No harness Python behavior changed,
so harness TDD and product checks do not apply to this environment configuration
change. Working-tree changes are the devcontainer configuration and this checkpoint.

Follow-up refactor: moved the same sequential creation steps into
`.devcontainer/post-create.sh`, invoked with Bash by `postCreateCommand`.
The script stops on errors. JSON parsing, script-reference validation,
`bash -n .devcontainer/post-create.sh` and `git diff --check` passed.
This preserves behavior, so no new TDD cycle applies. The additional working-tree
file is `.devcontainer/post-create.sh`; container lifecycle remains unverified.

Container diagnosis follow-up: VS Code rebuild and reload did not invoke the
lifecycle script in the supplied logs. Direct invocation of the installed
Dev Containers CLI 0.89.0 `run-user-commands` against container `aa2f61daec0c`
ran `postCreateCommand`, installed Codex and completed locked uv sync with
`{"outcome":"success","result":"done"}`. This verifies the lifecycle runner
and script together, but does not resolve why VS Code omitted the handoff.
A host extension PendingMigrationError was observed; causality is unproven.
No corrective repository change was made during this diagnosis.

Container follow-up remains: investigate the VS Code extension lifecycle handoff
on the next rebuild; automatic creation setup is not established. No publication performed.
