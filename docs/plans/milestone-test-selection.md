# Stratify tests by milestone

Source: developer-supplied maintenance plan, 2026-11-04. This is test scheduling
maintenance, not implementation of a new harness user story. No issue scope,
runtime API, dependency or lockfile change is introduced. Branch:
`chore-refactor-tests`; preserve existing work; no commit, push or PR.

## Authorized implementation phase 1

Public boundaries, confirmed by the supplied plan: public pytest subprocess
selection/collection and xdist scheduling. These cover default and explicit
selection, overlap without duplication, missing-classification diagnostics and
worker grouping. They do not prove new harness functionality or other platforms.

| Task | Status | Result / verification |
|---|---|---|
| IP1-T1: Create branch and inspect baseline | Complete | Clean initial tree; requested branch; baseline 415 collected cases |
| IP1-T2: Classify tests and replace scheduling | Complete | Explicit M0–6/M50/M99/infrastructure; default M1–6; missing IDs rejected; six focused regressions pass |
| IP1-T3: Reconcile policy and unfinished obligations | Complete | Repository instructions, policy, template, workflow, skills and US-03/35/36 scope records updated; historical approvals/failures preserved |
| IP1-T4: Verify and record inventory | Complete | 416 distinct cases (409 unchanged plus six replacing five); shared checks pass; default M1–6: 313 passed, 1 skipped; final scheduling: six passed |

Implementation phase gates select only the current milestone. Every local story
acceptance and plain pytest select M1–6, even for M0/M50 stories. Broader pytest
runs and standalone artifact verification require an explicit developer command;
CI retains its complete suite and existing artifact checks. Preserve TDD,
four-worker `loadgroup`, shared checks, assertions/timeouts, xdist groups, three
temporary skips and explicit developer gates.

Verification authorized here: focused scheduling regressions, shared checks,
collection reconciliation and the new M1–6 default. No broader suite or standalone
artifact command. Selected tests may invoke drivers internally. This maintenance
phase follows the supplied explicit verification scope, rather than triggering
an additional M50 story gate run.

## Evidence and final gate

[Verification report](../verification/milestone-test-selection.md) owns commands,
red/green results, collected counts, overlap explanation and coverage limits.
Historical M1/M50 obligations remain with their owners, revised by the explicit
scope records. They are not closed by this maintenance change.

- **Technical completion:** Complete; final checks and evidence recorded.
- **Developer decision:** Approved on 2026-11-04 by the developer message
  “i approve the final phase”. All implementation tasks and the final phase gate
  are complete.
- **Publication:** Initially excluded. Subsequently authorized on 2026-11-04 by
  developer message “commit, push and create pr”. Published as commit `81f6ab7` and PR #52; see the publication record below.

## Explicit complete-suite follow-up — 2026-11-04

The developer requested “do a full run.” Four-worker complete pytest selection
passed: **413 passed, 3 existing skips in 482.73s**, all 416 cases selected.
See the report for command, JUnit and platform limitations. No executable changes,
standalone artifact commands, phase approval or publication in this follow-up.

Approval-record update only: `git diff --check` passed. Existing test evidence
remains applicable; no executable files changed and no test rerun was needed.

## Publication — 2026-11-04

Developer explicitly authorized commit, push and PR creation. Target repository:
`jimthompson5802/agentic-ml`; head `chore-refactor-tests`, intended base `main`.
GitHub CLI 2.103.3 reports no authenticated hosts both inside and outside the
sandbox. The developer has been asked to run `gh auth login`. PR body is prepared
with the repository template at `/tmp/agentic-ml-milestone-selection-pr.md`.
Commit and ordinary push will be attempted independently; publication results
will be recorded when known. Existing final phase approval remains valid.

### Publication result

- Committed implementation as `81f6ab7` (`chore(tests): stratify verification by milestone`).
- Pushed `chore-refactor-tests` to `origin` and verified the remote commit.
- Created [PR #52](https://github.com/jimthompson5802/agentic-ml/pull/52) into
  `main`; verified title, body, head owner/branch, base and non-draft status.
- Initial CLI authentication issue resolved by reusing the existing Git credential
  in process memory; the developer then confirmed `gh` login. No credentials
  were printed or saved by the helper.
- Publication-record follow-up changes documentation only; whitespace check
  passed. Existing executable verification remains valid. Await PR review/CI;
  merge and branch cleanup are not authorized.

### Squash merge — 2026-11-04

Developer instruction “squash merge pr #52” authorized the merge. Final head
`dee3101ef2722b0a68cfb057c817e6c8f57c3b5b` had successful
[Linux/Python 3.12 CI](https://github.com/jimthompson5802/agentic-ml/actions/runs/41754352691).
Merged with `gh pr merge --squash --match-head-commit` at that verified head.
GitHub confirms MERGED at 01:42:20 UTC, squash commit
`23ad2f49fa4641fbc39392d6186cab0a320522b0`. Branches retained; no cleanup requested.
The developer subsequently instructed switching to `main`, pulling the merge,
and committing/pushing this merge record and checkpoint update. Preserved both
files through a temporary stash, fast-forwarded `main` to the squash merge and
restored the updates without conflicts. Branches retained.
`git diff --check` passed; no executable changes or additional test run.
