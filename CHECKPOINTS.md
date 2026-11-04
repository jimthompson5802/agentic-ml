# Development Checkpoints

Last updated: 2026-11-04 (UTC)

## Current US-05 accepted — PR #53 squash merged — 2026-11-04

On `US-05-configuration-validation`, baseline `3eefd55`, developer “start ip3”
authorized the final phase, superseding the earlier hold. All IP3 tasks are
technically complete in the [owning plan](docs/plans/milestone-1-us-05.md) and
[IP3 report](docs/verification/us-05-ip3.md). Issue #11 full body/all comment pages
refreshed; unchanged, zero comments. Approved public test boundaries reused.

Added installed semantic CLI/API/project-helper checks for direct and sdist-rebuilt
wheels, schema inventory and damaged-wheel regression, usage guide and evidence.
M1: **371 passed, one existing skip in 234.20s**. M1–6: **371 passed, one existing
skip in 226.43s**. Each selected 372/474, excluding 102. Shared checks, document
links and whitespace pass; lock unchanged. Linux/Python 3.12.16 only. Original
failed probe diagnostic expectation and corrective evidence preserved in report;
no product Python/dependency changes or new exclusions.

Working tree: probes/regression, README/usage/distribution docs, plan/report and
this checkpoint. Developer approved IP3 with “i approve ip3” on 2026-11-04.
Approval records updated; `git diff --check` passed, existing executable evidence
remains applicable. Developer “i accept user story” accepted US-05 on 2026-11-04.
Published commit `e4b5acf` on `origin/US-05-configuration-validation` and opened
[PR #53](https://github.com/jimthompson5802/agentic-ml/pull/53) into `main`.
[Verified static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/53#pullrequestreview-5762797927)
found no actionable findings. Publication records are documentation only; final-head
confirmation is recorded in the
[final-head review](https://github.com/jimthompson5802/agentic-ml/pull/53#pullrequestreview-5762803501).
Developer “squash merge pr #53” authorized the merge on 2026-11-04. Final-head
Linux/Python 3.12 CI passed; GitHub confirms MERGED at 03:40:36 UTC as
`05ad81f68bbd3197f7b0f7345719df6993e08ee4`. **Next action:** await developer
direction after the requested final-record publication. Developer “switch main;
pull; commit and push” authorized checkout synchronization and publication on
2026-11-04. Switched to `main`, pulled the squash merge and restored these merge
records. Branches retained. Publishing this documentation-only update; whitespace
checks pass and existing executable evidence remains valid.
Earlier no-publication statements are historical. No executable changes or
renewed tests in acceptance/publication recording.
Developer-requested M1–6 repeat run was stopped by “stop the tests”, exit 130.
No completed renewal claimed; earlier passing evidence remains valid. Do not
restart tests without direction.
Preserve M1-ACCEPT-VERIFY, M50-ACCEPT-VERIFY and the three historical temporary skips;
no broader suite or standalone artifact driver run. IP2 installed/final verification
deferrals resolved by IP3 evidence; historical timeout/platform limits remain open.

## Historical US-05 IP2 approved — 2026-11-04

On `US-05-configuration-validation`, baseline `55c03b6`, developer “i approve”
after the interface review approved IP1/D1–D7/public boundaries and accepted the
presented IP2 progression request. IP2 tasks are complete and the developer approved the gate with
“i approve ip2; commit; do not strt ip3 yet” on 2026-11-04. The local commit
contains the approved IP1/IP2 work and approval records. IP3 remains unstarted
and explicitly not authorized.
The [owning plan](docs/plans/milestone-1-us-05.md) and
[IP2 evidence](docs/verification/us-05-ip2.md) record progress and verification.

Implemented the four semantic validation APIs and CLI bindings, packaged scalar
registry metadata/schemas, immutable validation evidence and public behavior
regressions. Twelve focused red–green cycles and additional public coverage
recorded 57 passing cases. Lint, formatting, strict typing, lock consistency and
version smoke checks passed. Final M1: **370 passed, one existing skip in
218.29s**, exit 0; 473 collected, 371 selected, 102 deselected. Preliminary M1
369-pass evidence is retained separately; final evidence includes the
type-sensitive replay correction. No executable/resource/test identities changed
after final gate launch; lock SHA-256 unchanged. No full-story or milestone acceptance claimed. No dependencies or
lock changes; no standalone artifact command or broader suite run.

The approved local commit includes IP1 documentation, IP2 package/CLI,
registry/schema resources, tests, report and progress records. Approval-record
updates pass document/whitespace checks; existing executable evidence remains
applicable. **Next action:** await explicit IP3 authorization. No push requested.
Preserve M1-ACCEPT-VERIFY, M50-ACCEPT-VERIFY, three temporary skips and historical
failures. The following publication next-action record is historical.

## Milestone test selection publication record — 2026-11-04

Branch `chore-refactor-tests`; initial working tree clean. The developer's
supplied maintenance plan authorizes milestone classification and policy updates,
without commit, push or PR. This entry supersedes older next-action and automatic
local full-suite/artifact requirements below. Historical evidence and failures
remain preserved. Current milestone at phase gates; M1–6 at all story acceptance;
other local pytest selections and standalone artifact drivers require an explicit
developer command. CI remains complete-suite plus existing artifact checks.

Inventory: M0 18, M1 314, M2–6 0 each, M50 80, M99 0, infrastructure 6;
416 distinct cases, 314 default-selected and 102 excluded. Two associations overlap.
The baseline 415 comprises 409 unchanged non-scheduling cases and five scheduling
cases, replaced by six. Three temporary skips, assertions/timeouts and groups
remain. See [plan](docs/plans/milestone-test-selection.md) and
[evidence](docs/verification/milestone-test-selection.md).
Scope-change records in US-03, US-35 and US-36 revise unfinished M1/M50
verification obligations without changing historical approvals or resolving failures.

Focused scheduling regressions: six passed (final renewal 2.97s). Default M1–6:
313 passed, one existing skip in 234.32s, 102 excluded. Shared checks passed after
one import-format correction; lock unchanged. Linux/Python 3.12.16 only;
macOS/Windows remain unverified; the full-suite follow-up below covers the
previously excluded selection except for the three temporary skips.
Developer-requested complete suite (2026-11-04): **413 passed, 3 existing skips
in 482.73s**, exit 0, all 416 selected. JUnit confirms no failures/errors; lock
unchanged. No standalone artifact command or executable changes in this follow-up.
The three original timeout causes remain unresolved.
Final phase approved on 2026-11-04 by developer message “i approve the final
phase”; all implementation tasks and gates are complete. Approval-record changes
only; `git diff --check` passed, and existing executable evidence remains valid.
The developer authorized commit, push and PR creation on 2026-11-04. Published
implementation commit `81f6ab7` on `origin/chore-refactor-tests` and opened
[PR #52](https://github.com/jimthompson5802/agentic-ml/pull/52) into `main`.
Verified PR title, description, branch ownership and non-draft status. Initial
GitHub CLI authentication was unavailable; existing Git credentials enabled
creation, and the developer subsequently confirmed `gh` login.
PR #52 was squash merged at the developer's explicit request on 2026-11-04,
as `23ad2f49fa4641fbc39392d6186cab0a320522b0` after final-head Linux/Python 3.12 CI
passed. GitHub confirms MERGED at 01:42:20 UTC. At the developer's subsequent
request, switched to `main`, pulled the squash merge, and authorized committing
and pushing these final merge records. Branches have been retained.
**Next action:** publish this documentation-only final update on `main`, then
await developer direction. No branch cleanup authorized. The
three original timeout causes and separate milestone acceptance obligations
remain open. Publication-record follow-up only; `git diff --check` passed and
existing executable evidence remains applicable.

## Historical checkpoints (superseded resume instructions)

## Devcontainer GPG configuration — 2026-11-04

Added the requested global Git signing configuration to
`.devcontainer/post-create.sh`: OpenPGP, `/usr/bin/gpg`, automatic commit
signing, and the existing signing-key fingerprint recorded in the diagnosis
below. This supersedes that diagnosis's pending Git-configuration action;
host-agent access and public-key availability still require container validation.
`bash -n .devcontainer/post-create.sh` and `git diff --check` passed on macOS.
No harness behavior changed, so harness TDD and product tests do not apply.
The developer authorized commit and push on 2026-11-04. Linux shell syntax
and whitespace checks also passed before publication on `main`. Next action:
recreate the container and verify signing with the forwarded host agent.
Existing milestone obligations remain open.

## Devcontainer setup commit — 2026-11-04

The developer authorized committing `.devcontainer/Dockerfile` and
`.devcontainer/post-create.sh`, together with this checkpoint. Changes add
`gnupg2` to the container utilities and the Codex terminal reminder below.
Linux verification: `bash -n .devcontainer/post-create.sh` and
`git diff --check` passed. Container build and creation remain unverified.
No harness behavior changes; harness TDD and product tests do not apply.
Next action: commit these changes locally; no push requested. Existing milestone
obligations remain open. This supersedes the reminder's pending-review status.

## Devcontainer Codex reminder — 2026-11-03

On `main`, added the developer-requested echo as the final command in
`.devcontainer/post-create.sh`: start Codex with `codex --no-alt-screen`
for terminal scrollback and copying text. Shell syntax (`bash -n`), isolated
execution of the final echo, and `git diff --check` passed on macOS.
Full container creation was not run. This informational setup message changes
no harness behavior, so harness TDD and product tests do not apply.
Working-tree changes are the script and this checkpoint; no publication requested.
Next action: developer review. Existing milestone obligations remain open.

## Workflow diagram update — 2026-11-03

Replaced the opening development-workflow diagram with a five-stage overview
and five detail diagrams. Each detail uses a matching named subgraph with
before/after context nodes. Correction loops, scope decisions, phase approval,
story acceptance and milestone checks are preserved.

Verification: all six diagrams rendered successfully with Mermaid CLI on macOS
using an approved browser invocation outside the sandbox; the sandbox browser
launch failed. Whitespace checks passed. This documentation-only presentation
change requires no harness TDD or product tests. The developer approved the diagrams and authorized commit and push on
2026-11-03. Publication includes `docs/development-workflow.md` and this
checkpoint on `main`. Existing milestone obligations remain open.

## Current correction and next action — 2026-11-03

On `main`, completed the developer-requested dependency-inventory correction.
Both isolated probes now validate installed requirement metadata with platform
markers, extras and version constraints, rather than fixed transitive lists.
Direct harness requirements, provenance, resource checks and developer-tool
exclusions remain enforced. Universal lock validation checks reachability and
installed versions; the copied Git probe includes its shared contributor helper.
Added 18 probe/lock regressions and strengthened the approval-schema failure
check with its own diagnostic. Existing three temporary skips remain unchanged.

Verification: original two failures reproduced and passed after correction;
approval diagnostic and lock-root injection each have red/green evidence.
Phase group: 289 passed in 157.87s. The first full-suite run recorded 337 passes,
70 failures, 5 errors and 3 skips after the checkout `.venv` Python symlink
changed to an unavailable macOS Homebrew path. Preserved its XML and grouped
failure evidence; the process responsible is unconfirmed. Renewed the complete
suite with `UV_PROJECT_ENVIRONMENT=/tmp/agentic-ml-linux-dependency-checks-20261103`:
**412 passed, 3 skipped in 418.34s**, exit 0, Linux/Python 3.12.16. The isolated
Linux environment avoids changing the shared checkout `.venv`. Locked sync,
lock consistency, lint, formatting, strict typing, CLI smoke and whitespace
checks passed; lock hash unchanged. macOS/Windows remain unverified by this run.

Evidence and scope: [dependency correction](docs/verification/dependency-inventory-correction.md),
covering US-33 AC-02–05 and US-01 AC-02–04 while preserving US-35 driver
contracts. Raw XML is retained under
`.dev-records/verification/20261103-dependency-closure/`.
Working-tree changes: both probes, installation driver, new dependency helper,
the two integration test modules, distribution guide, correction report and
this checkpoint. The developer authorized committing and pushing this correction
on 2026-11-03. Publication is proceeding on `main`; existing milestone
obligations and skipped coverage remain open.


## Temporary three-test skips — 2026-11-03

On `main`, the developer explicitly requested temporary skips for the three
Linux full-suite timeout cases named below. Added individual `pytest.mark.skip`
decorators to those tests in the installation/distribution integration modules,
with a reason identifying the developer request and unresolved 120-second
timeouts. Registered the exclusions and removal condition in
`docs/development.md`. Test bodies, assertions and timeouts remain unchanged.
This changes test selection only; TDD does not apply because no harness behavior
is introduced or corrected.

Verification: `uv run --locked pytest -n 4 --dist=loadgroup -m "" -rs` with
the three explicit selectors reported 3 skipped in 1.02s on Linux/Python
3.12.16, exit 0. Targeted Ruff lint and formatting checks and
`git diff --check` passed. The full suite was not rerun; skipped coverage does
not close existing milestone verification obligations or resolve the timeouts.
The developer authorized committing and pushing these four files on 2026-11-03.
This publication supersedes earlier pending-publication instructions for these
changes. Next action: re-enable when the timeout cause is resolved or the
developer directs it; milestone verification obligations remain open.

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
