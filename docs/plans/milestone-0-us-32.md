# Milestone 0 / US-32: Verify changes automatically in CI

## Scope and outcome

- **Milestone:** 0 — Establish the harness development foundation.
- **User story:** [US-32 / issue #2](https://github.com/jimthompson5802/agentic-ml/issues/2).
- **User-visible outcome:** Pull requests and default-branch updates receive Linux/Python 3.12 development checks with visible results and failure diagnostics.
- **Acceptance criteria covered:** [US-32-AC-01–04](../specs/user-stories.md#us-32-verify-changes-automatically-in-ci), all criteria in this story.
- **Scope boundaries:** CI triggers, clean checkout/environment, locked uv synchronization, shared development checks, contributor instructions and execution evidence. Package builds, isolated wheel/sdist/resource checks remain US-33; branch protection and contribution/review policy remain US-34 in Milestone 99. No new harness runtime behavior or additional Python/platform matrix is proposed.
- **Supporting design:** [Contributor contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [delivery dependencies](../specs/design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order), [traceability](../specs/design/acceptance-traceability.md), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization).
- **Coordinated execution index:** [US-32 execution order](milestone-0-us-32-execution-order.md). Existing prerequisite tasks are reused; no additional work is assigned to US-31 or US-33.

## Findings and source reconciliation

Retrieved complete issue bodies, metadata and all comment pages on 2026-10-29. Issue #2 is open, has zero comments, and unchanged update time `2026-10-29T03:09:11Z` on recheck. Its body assigns Milestone 0; GitHub milestone metadata is unset. Issue #1 is closed, has zero comments, and unchanged update time `2026-10-29T23:03:10Z`. Issue #3 is open, has one comment, and unchanged update time `2026-10-29T23:10:06Z`. All reported counts match fetched unique comments. The [sole #3 comment](https://github.com/jimthompson5802/agentic-ml/issues/3#issuecomment-6510671946), by jimthompson5802, created/updated 2026-10-29T23:10:06Z, says: “PR #4 prematurely closed this issue, reopening.” It confirms the partial-delivery boundary.

Issue #2 and current repository criteria agree. Earlier issue #1/#3 CLI spelling is superseded by SC-01 and ADR-007: use `agentic-ml`. Older ADR-007 paragraphs still call distribution/repository selection pending; the explicit decisions in the approved prerequisite plans and current `pyproject.toml` settle those choices. Original requirements agreed at planning time. SC-01 below supersedes the original macOS CI requirement with Linux; the issue and local requirements now agree.

Inspected clean `main` at `808d4e0`: `.github` contains templates but no workflow. `pyproject.toml`, `uv.lock`, Python 3.12 selection, three public subprocess tests and all shared local commands exist. US-31 is accepted; US-33 IP1 is approved. Local macOS evidence does not establish hosted CI behavior. `gh auth status` reported an invalid default token in this environment, but every required read-only API call succeeded; verify write/run access before publication during execution, without collecting credentials.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-31 tooling and commands | US-31-IP1-T1–T3 and IP2-T1–T3 complete, gates approved | US-32 IP1 | [Owning plan](milestone-0-us-31.md), [fresh macOS evidence](../verification/us-31-ip2.md); accepted 2026-10-29 |
| US-33 minimal CLI | US-33-IP1-T1–T3 and gate approved | Source installation, tests and smoke | [Owning plan](milestone-0-us-33.md), [corrected CLI evidence](../verification/cli-name-correction.md); approved 2026-10-29; remaining story unnecessary here |
| CI implementation choices | GitHub Actions; explicit Linux runner image, Python 3.12 only, pinned uv version initially 0.13.1 | Workflow configuration | Selected ubuntu-24.04 (SC-01), checkout v5 and setup-uv v7 immutable revisions; see IP1 evidence |
| Default branch | Push trigger targets actual default branch | Workflow trigger and default-branch evidence | Repository API reports `main`; recheck before implementation |
| Hosted execution and publication | Actions enabled, hosted runner availability, repository permissions; authorize branch/PR publication and merge separately | IP2 hosted evidence | Not exercised in planning; absence of access blocks affected evidence, not configuration work |

## Technical approach and public verification boundaries

Create proposed `.github/workflows/ci.yml`. Use `pull_request` without path filters and `push` restricted to `main`; do not use a privileged pull-request trigger. Start each job with a clean checkout and new environment; do not restore a prebuilt virtual environment. Install explicit uv and Python 3.12 versions, record OS/architecture, Python, uv and resolved checker versions. Use reviewed immutable action revisions with readable version comments and minimal read permissions. Confirm current official setup syntax at implementation time. Record the runner image/version actually used; local macOS verification does not establish Linux CI behavior.

Run the existing commands verbatim from the checkout:

```sh
uv sync --locked --group dev
uv lock --check
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked agentic-ml --version
```

Compare `uv.lock` SHA-256 before synchronization and after all checks, and verify no tracked lockfile diff. Ensure the final lock check executes after failed checks where setup succeeded. Give each checker a named step, run remaining independent checks after a checker failure when installation succeeded, and preserve their original nonzero exit status. Do not mask failures with `continue-on-error` or log pipelines. Native Actions step logs provide diagnostics accessible through PR checks; document how to find and download them. Dependency/setup failures must also fail visibly with their logs; dependent checks may be skipped when setup fails.

Plan review confirms these public boundaries: event-triggered Actions runs, step/job conclusions and accessible PR logs verify automation; real existing tool commands verify source behavior. Static YAML inspection alone cannot verify event delivery or hosted execution. Disposable branch defects exercise failure propagation, followed by correction and passing reruns. Introduce one failure case at a time, keep production assertions and acceptance criteria intact, and never merge deliberate defects. Existing tests do not establish installed wheel/resource isolation, other platforms or additional Python versions.

No new harness behavior is planned, so use existing regression tests and workflow red/green evidence rather than manufacture Python unit tests for YAML. For corrected CI behavior, reproduce the failure through its public run/command boundary before the fix and retain red/green evidence. If new harness behavior becomes necessary, revise scope and confirm its TDD boundary before implementation.

## Execution rules

Mark tasks Complete only after work and required verification pass, with actual commands/results and evidence. Unverified, failed, partial or blocked tasks remain incomplete. Check the execution index and prerequisite evidence/gates before dependent work. Reopen tasks when changes invalidate results.

Stop at every implementation phase boundary, including the final one. Present task results, checks, evidence, deviations and limitations; await explicit developer approval and record its date/reference. Plan approval does not approve implementation gates or authorize publishing/merging. Silence is not approval.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes; pause affected work and update owning plans/index together. Obtain approval for added prerequisite scope before implementation. Follow the [three-attempt limit](../../AGENTS.md#problem-solving-attempt-limit): record hypothesis, change and original-failure verification per corrective attempt; after three failed attempts stop and preserve diagnostics for direction. Do not weaken checks or add suppressions to hide failure.

Keep raw logs and disposable failure fixtures outside maintained source; redact secrets. Save review evidence under proposed `docs/verification/us-32-ip1.md` and `docs/verification/us-32-ip2.md`. Update this plan, index and [checkpoint](../../CHECKPOINTS.md) at gates, blockers and handoff. Planning does not install dependencies, modify workflows or publish external changes.

## Plan review

- **Status:** Approved.
- **Developer decision:** Approved — scope, implementation phases, proposed technical choices and public verification boundaries.
- **Decision reference and date:** Developer message “i approve plan; commit changes”, 2026-10-29. Approval covers this plan and its execution index; the current instruction authorizes recording approval and committing planning changes. IP1 execution authorized by developer message “execute plan for us-32”, 2026-10-29; implementation gates remain pending.
- **Requested plan changes:** None recorded.

## Scope-change history

### SC-01 — Linux CI runner (2026-10-29)

- **Request / decision:** Approved by developer instruction “for gh action I want to use a linux host, not macos”. This authorizes revision of current IP1 work; it does not approve the IP1 gate or IP2 progression.
- **Scope difference:** Replace macOS Actions hosting with Linux, selecting `ubuntu-24.04`. Preserve macOS local development and historical evidence. Use `/etc/os-release` for hosted OS diagnostics.
- **Requirements:** Updated [issue #2](https://github.com/jimthompson5802/agentic-ml/issues/2) description, AC-01 and recorded decision, plus [US-32-AC-01](../specs/user-stories.md#us-32-ac-01) and the design contributor contract. IDs and all other criteria remain unchanged. Issue update returned `2026-10-29T23:26:24Z`; complete issue/comments were refreshed beforehand, with stable metadata and zero comments.
- **Impact:** T1 runner selection, T2 workflow/validation, T3 docs and all IP2 hosted platform expectations revised. Existing macOS local check results remain valid for unchanged shared commands; they do not verify Linux execution. Original workflow validation is historical; renewed actionlint/configuration checks are required and recorded in IP1 evidence. No dependency or runtime changes.
- **Verification / gates:** IP1 tasks re-reviewed against Linux configuration; actual Linux success/failure/event evidence remains IP2. IP1 developer gate remains pending. No additional milestone or story work is introduced.
- **Resume point:** Complete current IP1 Linux revisions and present the renewed gate evidence. External branch/PR publication and merge remain separately authorized.

## US-32 / Implementation Phase 1: Configure Linux development CI

- **Outcome:** Reviewable workflow and contributor instructions reproduce all shared commands and preserve failure status.
- **Entry conditions:** Plan/public boundaries approved and implementation explicitly authorized; prerequisite gates confirmed.
- **Acceptance criteria advanced:** US-32-AC-01–04; hosted evidence remains pending IP2.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-32-IP1-T1 | Complete | Confirm official runner/action compatibility, immutable revisions, uv installation and Python selection; inspect repository Actions availability and default branch. Record choices and source links in proposed `docs/verification/us-32-ip1.md`. | Approved plan and prerequisite records | Concrete supported configuration selected; any unavailable permission/capacity recorded before dependent work. | AC-01–02 |
| US-32-IP1-T2 | Complete | Create proposed `.github/workflows/ci.yml` with PR/default-branch triggers, Linux/Python 3.12 setup, locked synchronization, five named shared checks, version diagnostics and final lock immutability check. | T1 | Inspect valid YAML and event/job conditions; reproduce commands locally, confirm identical command text and nonzero failure propagation; dependency failure cannot produce success. No package verification added. | AC-01–04 |
| US-32-IP1-T3 | Complete | Update `docs/development.md` and README CI status/instructions; run all documented shared checks on macOS, record results and lock hash in proposed IP1 evidence; update plan/index/checkpoint. | T2 | Tests/lint/format/types/smoke and lock consistency pass; docs explain PR checks/logs, reproduction, pinned setup, pending hosted verification and platform limits. | AC-02–04 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Workflow structure | Parse YAML with a suitable Actions-aware validator available during implementation; inspect triggers, action revisions, shell failure handling and conditions | Both required events, Linux/3.12 and visible nonzero conclusions; record validator/version and limitations | actionlint 1.7.12 passed; local nonzero propagation passed; hosted conclusions pending. [Evidence](../verification/us-32-ip1.md) |
| Local shared checks | Exact seven commands above; compare lock SHA-256 and `git diff --exit-code -- uv.lock` | All pass without modifying lockfile | All seven passed, three tests; matching SHA-256 and clean lock diff. [Evidence](../verification/us-32-ip1.md) |
| Documentation | Compare workflow commands with development guide; validate Markdown links and `git diff --check` | Reproduction instructions agree; no unsupported hosted claims | Commands agree; local targets and diff check passed. [Evidence](../verification/us-32-ip1.md) |

### Developer approval gate

- **Approval criteria:** T1–T3 complete with configuration review, actual local check results and hosted-verification procedure.
- **Evidence presented:** [IP1 verification](../verification/us-32-ip1.md); T1–T3 technically complete, developer approval recorded.
- **Remaining limitations or blocked work:** Hosted triggers, PR diagnostics and default-branch run remain unverified until IP2.
- **Developer decision:** Approved, including SC-01 Linux revision.
- **Decision reference and date:** Developer message “I approve IP1. Commit the Linux changes, push the branch, and create a PR to begin IP2.”, 2026-10-29.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Begin IP2; committing/pushing the Linux changes and PR creation explicitly authorized. Merge remains separately authorized.

## US-32 / Implementation Phase 2: Verify hosted triggers and failure diagnostics

- **Outcome:** Actual successful PR/default-branch runs and inspectable failing PR checks establish all story criteria.
- **Entry conditions:** IP1 approved; permission and authorization for required branch/PR publication confirmed. Merge authorization required before default-branch update; retain pending status if unavailable.
- **Acceptance criteria advanced:** US-32-AC-01–04, full evidence required.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-32-IP2-T1 | Complete | Publish authorized review branch/PR with workflow, observe PR-triggered run; record run/event URL, commit SHA, runner/Python/tool versions, clean setup and lock hashes in proposed `docs/verification/us-32-ip2.md`. | IP1 approval and publication authorization | Actual PR check passes all documented commands on clean Linux/Python 3.12. | AC-01–03 |
| US-32-IP2-T2 | Complete | On an authorized disposable PR branch, introduce then correct isolated defects one at a time: failing pytest assertion, lint violation, formatting defect, type error, failing version smoke and dependency metadata/lock mismatch. Preserve links/log excerpts, correction commits and successful reruns in proposed IP2 evidence. | T1 | Each relevant command fails and overall CI fails with inspectable PR diagnostics; stale metadata is rejected without lock mutation. All temporary defects removed; real checks remain intact. | AC-02–04 |
| US-32-IP2-T3 | Complete | Present clean PR and failure evidence for merge authorization; after authorized merge observe `push` run on `main`. Record exact default-branch revision/run and results in proposed IP2 evidence. | T2; separate merge authorization | Actual default-branch event passes same checks on clean Linux/Python 3.12; failure evidence never merged. If merge deferred, AC-01 stays pending. | AC-01–04 |
| US-32-IP2-T4 | Complete | Update `docs/development.md`, README, both planned evidence reports as needed, this plan/index and CHECKPOINTS with actual CI coverage and acceptance mapping; rerun checks affected by any final changes. | T3 | Document only observed versions/platforms, link green PR/default-branch runs and failure logs, explain local reproduction; all final relevant checks pass and developer review is ready. | AC-01–04 |

### Verification and review evidence

T1 baseline: [PR #5](https://github.com/jimthompson5802/agentic-ml/pull/5), [successful Linux PR run](https://github.com/jimthompson5802/agentic-ml/actions/runs/40973713670); [IP2 evidence](../verification/us-32-ip2.md). T2 completed all six red/correction-green pairs on disposable draft PR #6; final tree equals clean baseline. Developer merged PR #5; [main push run](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618) passed. T3/T4 complete.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Required triggers | Inspect actual event, revision, job steps and logs through PR Checks/Actions or explicit-repo `gh run view` / `gh pr checks` | Successful PR and default-branch push runs on intended revisions | PR baseline and main push at 0a3c087 passed. [IP2 evidence](../verification/us-32-ip2.md) |
| Failure propagation | T2 isolated red/correction-green runs, step/job conclusions and accessible PR log links | Every check failure fails CI, diagnostics explain cause, restored branch passes | All six cases verified with red/green run and head records; ineffective first smoke fixture corrected on attempt 2. [IP2 evidence](../verification/us-32-ip2.md) |
| Lock integrity and setup | Logged hashes, lock diff, sync result, environment versions | Matching committed lock before/after successful and failed check runs; mismatch rejected, no silent regeneration | All red/green lock checks passed; stale metadata rejected with --locked. [IP2 evidence](../verification/us-32-ip2.md) |
| Final evidence/docs | Review all four criterion mappings, links and `git diff --check`; run affected documented checks | Complete evidence, no unsupported coverage claim or leftover defect | All four criteria verified; docs/links/command comparison, actionlint, lock and diff checks passed. [IP2 evidence](../verification/us-32-ip2.md) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete, successful real runs for both events, controlled failure diagnostics and corrected green result, actual CI versions documented.
- **Evidence presented:** [IP2 evidence](../verification/us-32-ip2.md): T1–T4 complete; successful PR/main runs and all six failure/correction pairs.
- **Remaining limitations or blocked work:** No remaining US-32 blocker. Other platforms/versions, US-33 package checks and US-34 policies remain excluded.
- **Developer decision:** Approved; final US-32 acceptance recorded.
- **Decision reference and date:** Developer message “I approve us-32 ip2”, 2026-10-29; developer previously reported “I merged pr #5”.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** US-32 complete and accepted. No downstream story implementation authorized.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-32-AC-01 — clean Linux PR/default-branch runs | IP1-T1–T2; IP2-T1,T3–T4 | [IP2 PR/main run records](../verification/us-32-ip2.md) | Verified |
| US-32-AC-02 — Python 3.12, tools, locked dependencies | IP1-T1–T3; IP2-T1–T4 | [IP2 versions, hashes and mismatch rejection](../verification/us-32-ip2.md) | Verified for PR and main push |
| US-32-AC-03 — shared development commands | IP1-T2–T3; IP2-T1–T4 | [IP1 comparison and IP2 hosted results](../verification/us-32-ip2.md) | Verified for PR and main push |
| US-32-AC-04 — failing result and PR diagnostics | IP1-T2–T3; IP2-T2–T4 | [IP2 six failure/correction pairs](../verification/us-32-ip2.md) and contributor instructions | Verified |

- **Remaining work:** None for US-32. T1–T4 complete, both implementation gates approved and final story accepted.
- **Partial prerequisite delivery:** Reuses accepted foundation only. Does not complete remaining US-33 or Milestone 0.
- **Developer acceptance:** Approved.
- **Decision reference and date:** Developer message “I approve us-32 ip2”, 2026-10-29.
