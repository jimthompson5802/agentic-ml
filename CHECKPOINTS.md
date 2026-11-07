# Development Checkpoints

Last updated: 2026-11-07 (UTC)

## Current US-12 PR #61 squash-merged — 2026-11-07 UTC

Branch `US-12-data-validation`, baseline `32efc2f`. Developer approved the initial
recommendation and, after comparison overflow was discovered, “I approve”
authorized the additional comparison fix. Float-only finiteness checking and
temporary object comparisons for huge integer bounds now pass all 120 quality
cases, including null/infinity and caller-data preservation. Attempt 1 failure
is retained; attempt 2 passed. [Plan](docs/plans/milestone-1-us-12.md#post-review-correction-pr61-r1--2026-11-07-utc)
and [evidence](docs/verification/us-12-pr61-r1.md) own details.
M1: 553 passed, one existing skip in 220.76s; final M1–6: 553 passed, one existing
skip in 226.65s; each 554/656 selected, 102 deselected. Shared checks, 104 local
link targets and whitespace pass; lock unchanged. Installed quality regressions
pass; new edge cases exercised via editable public API tests. Linux aarch64 only.
Raw evidence: `.dev-records/verification/20261107-32efc2f-pr61-r1/`.
Developer “i approve the fix; commit and push” approved the correction and
authorized commit/push on 2026-11-07 UTC. Correction committed and pushed as
`4022775` to PR #61. This publication-record update follows that successful push.
Developer “squash merge the pr; commit; switch to main; pull the latest changes
and commit and push” authorized merge and record publication. PR #61 squash-merged
as `1f9eb86` at 2026-11-07T17:40:11Z; switched to `main` and fast-forward pulled.
Merged tree equals approved PR head `8f71b2e` (empty diff). Overflow review thread
was already resolved when checked. This documentation-only merge record is ready
and published as `99c91f5`; no product edits or new executable checks needed.
Developer requested PR branch cleanup: local and remote `US-12-data-validation`
deleted after confirming its `8f71b2e` tree equals squash merge `1f9eb86`.
Historical approvals/skips and independent M1/M50 obligations remain unchanged;
#19 remains separate. **Next action:** await developer direction on subsequent work.

## Previous US-12 IP2 approved — 2026-11-07 UTC

Developer “i approve ip2 and commit” approved Gate 2 and authorized a local
commit of the completed IP2 work. The [plan](docs/plans/milestone-1-us-12.md)
and [evidence](docs/verification/us-12-ip2.md) record 95 focused passes, final
M1 527 passed and one existing skip, and passing shared checks. Recording the
decision before the authorized commit. IP3, story acceptance, push and PR are
not authorized. **Next action:** complete the local commit, then await separate
IP3 direction. Earlier gate-pending and provisional entries below are historical.

## Current US-12 IP2 developer gate — 2026-11-07 UTC

Gate preparation found the advisory test lacked the approved file sentinel.
Added that assertion; all 95 focused cases pass. Renewed final M1: 527 passed,
one existing skip, 528/630 selected in 219.54 seconds. Shared checks passed
after the change; final JUnit is `m1-gate.xml` in the records directory linked
below. IP2-T1–T4 are technically complete; developer Gate 2 approval is pending.
Stop before IP3. The preceding-run details below are historical.

### Earlier gate preparation

US-12 #15 IP2-T1–T4 are technically complete; developer Gate 2 approval is
pending. The [plan](docs/plans/milestone-1-us-12.md) and
[IP2 evidence](docs/verification/us-12-ip2.md) record the public quality rules,
blocking boundary, TDD and corrections. Focused tests: 95 passed. Final M1:
527 passed, one existing skip; 528/630 selected. Locked sync, lock consistency,
lint, format, strict typing, CLI smoke and whitespace checks passed; lock hash
unchanged. Raw final JUnit is in `.dev-records/verification/20261107-ec82d75-us12-ip2/`;
red/green console transcripts were not retained as raw logs. Linux aarch64 only.
Installed direct/rebuilt wheel quality verification and final M1–6 remain IP3;
existing historical M1/M50 obligations and skip remain open. No IP3, story
acceptance, commit or publication authorized. **Next action:** developer Gate 2
review and explicit approval; stop before IP3.

### Earlier IP2 progress

Developer “start ip2” authorized IP2 on `US-12-data-validation`, clean baseline
`ec82d75`, after IP1 approval. Five initial public TDD slices and their results
are recorded in the [plan](docs/plans/milestone-1-us-12.md). The provisional
`agentic_ml.data_quality` module and tests are incomplete: configuration and
frame validation, remaining quality rules, blocking, full matrix and phase checks
remain. No IP2 task or approval gate is complete. Continue the approved contract
one red–green slice at a time; do not treat current code as a usable boundary.
No milestone/shared verification, IP3, acceptance, commit or publication yet.
Developer “contineu us-12 ip2” resumed work. Three further red–green slices
cover invalid row-count thresholds, null counts and excess duplicate counts;
the focused file now has 10 passing cases. All tasks remain incomplete and the
provisional module does not yet implement the full approved contract.
Further continuation covers initial range/membership, required blocking, missing
columns, non-scalar cells, duplicate IDs and snapshot/settings cases; 18 focused
cases pass. One initial missing-column correction failed and the second passed;
the plan records the attempt. Full contract and phase checks remain outstanding.

## Current US-12 issue #15 IP1 approved — 2026-11-07 UTC

Developer “start ip1” authorized IP1 of the approved
[M1 US-12 plan](docs/plans/milestone-1-us-12.md). Branch
`US-12-data-validation`, baseline `2cf6b33`, clean at entry. IP1-T1–T4 are
complete; developer “i approve ip1; commit” approved Gate 1 and authorized
a local commit on 2026-11-07 UTC. IP2 authorization remains pending.
[Concrete contract](docs/data-quality.md) specifies public pandas functions,
seven quality-rule kinds, report/error/required-advisory semantics, checked
snapshot blocking, literal fixtures and installed probe files. Contract/API/test
boundaries are approved contracts; executable delivery remains pending.

Refreshed complete #15/#19 discussions: one unique comment each, all pages,
matching counts and stable metadata; planning snapshots unchanged. #15 owns
AC-01/05; #19 retains AC-02/03 and deferred AC-04. Accepted US-11 extraction
supplier evidence inspected. Plan, contract, active design links and
[IP1 evidence](docs/verification/us-12-ip1.md) record decisions and handoff.
Raw refresh/check records: `.dev-records/verification/20261107-2cf6b33-us12-ip1/`.

Documentation-only work; no product source/tests/dependencies/lock/resources
changed. Document/source checks passed: 48 local links/anchors, four Python/JSON
syntax blocks, source snapshot parity, task/gate/criterion states and whitespace;
source/tests/dependencies/resources and lock unchanged. Results are recorded in
the IP1 report and raw checks log. No executable tests, builds, dependency installation or runtime
support claim; TDD does not apply to this contract-only implementation phase.
Developer “I want to support "no checks"” authorized US-12-SC-01: explicit
empty rules report not_checked and permit the operation; malformed rules still
error. Contract/fixtures/future tests revised within IP1 and approved at Gate 1.
Original document checker misread Python type brackets as Markdown links;
corrective attempt 1 excludes fenced code, preserving original failure evidence.
Scope ownership and verification obligations remain unchanged.

Developer review clarification: the contract example now explains each of its
seven rules beside the code, including defaults, missing-value handling and
required/advisory/no-check behavior. Documentation-only clarification; renewed
document/source checks passed. Gate 1 approved; IP2 authorization remains pending.

Working-tree changes: plan, contract, IP1 evidence, two active design references
and this checkpoint. Recording approval before the authorized local commit;
no push, PR or GitHub writes requested.
**Next action:** await explicit IP2 authorization; stop before IP2. Independent M1/M50 obligations/skips remain open.

## Previous US-11 accepted and squash-merged — 2026-11-07 UTC

Branch `US-11-local-data-extraction`, baseline `0d74c21`; clean at phase entry.
Developer “start us-11 ip3” authorized IP3 after approved/committed IP2.
IP3-T1–T4 technically complete in the [plan](docs/plans/milestone-1-us-11.md).
[IP3 evidence](docs/verification/us-11-ip3.md) owns the complete stable #14 issue/
one-comment refresh, confirmed boundaries, red/green/correction records,
criterion reconciliation and source/platform/artifact identities.

Separate projects run actual pandas extraction code through normally installed
direct and sdist-rebuilt wheels, using isolated Python and unrelated cwd. Verified
literal CSV/Parquet/configured filter/select/merge output, copied settings,
schemas, input/code/output hashes, timing and persisted report. Invalid return,
original project exception, native pandas failure, missing input and corrupt
Parquet preserve context without completed failure output. Both normal runtime
inventories/resources and environments passed; cleanup complete. Guide finished
and linked from README. Product source, dependencies and lock unchanged in IP3.

Verification: M1 432 passed, 1 existing skip in 223.52s; final M1–6 432 passed,
1 existing skip in 208.91s; both 433/535 selected, 102 deselected, four loadgroup
workers, exit 0. All locked sync/lock/lint/format/mypy (60 files)/CLI 0.1.0 and
whitespace checks passed. Guide Python syntax and 63 local links/anchors passed.
Lock SHA-256 4b21570f… unchanged. Linux aarch64 / Python 3.12.16 / uv 0.13.6;
normal wheel installs pandas 3.1.1 / pyarrow 25.0.1; other platforms unverified.
Raw logs/JUnit/commands/identities:
`.dev-records/verification/20261107-0d74c21-us11-ip3/` plus linked child records.

Original intended red and initial probe-exception/type-check/checker failures
retained; each correction passed on attempt 1, with no suppressions/skips or
weakened assertions. Sandbox cache/network failures passed on approved retries.
Existing missing-planning-schema skip, other two historical skips and independent
M1/M50 obligations remain open. Quality, DVC, runners and assistant integration
retain their other-story owners; no end-to-end experiment acceptance claimed.

US-11 accepted by developer “i accept us-11” after all implementation gates.
Committed `f2c215c` plus publication records `1557ce1`; pushed and opened
[PR #60](https://github.com/jimthompson5802/agentic-ml/pull/60).
Static review found one Low stale design-status issue; the records-only head
received a verified [supplemental review](https://github.com/jimthompson5802/agentic-ml/pull/60#pullrequestreview-5811978935).

Developer requested resolving [comment r4501540084](https://github.com/jimthompson5802/agentic-ml/pull/60#discussion_r4501540084).
Updated the active overview to identify the implemented API, all phase approvals
and whole-story acceptance, with links to the contract and acceptance record.
Historical evidence preserved. Documentation-only status correction; link/anchor,
status and whitespace checks pass; no executable behavior requires TDD/test reruns.
Correction committed/pushed as `0fe1af0`; requested thread resolved and verified.
Developer “squash merge PR #60” authorized merging. Latest-head hosted CI
[run 42369843959](https://github.com/jimthompson5802/agentic-ml/actions/runs/42369843959)
passed (11m29s). Squash-merged PR #60 into main as
`5772fe5888751dfff05638a98f8be216e08e28c5` at 2026-11-07 12:01:58 UTC;
verified PR MERGED and issue #14 CLOSED. Branches retained. Raw CI log and merge
metadata are in the IP3 records directory. No additional local tests run.
Developer “switch to main; pull from origin; commit changes;” authorized local
synchronization and the merge-record commit. Switched to `main`, fast-forwarded
from origin to `5772fe5`, and restored this checkpoint update; existing feature
branch retained. Committing this documentation-only record with no push requested.
Whitespace check passed; runtime evidence remains applicable. **Next action:**
await developer direction; no new story authorized.

## Current MVP scope revision — Accepted — 2026-11-07 UTC

Developer “yes i approve” approved the final documentation/backlog gate on
2026-11-07 UTC. All IP1–IP4 tasks and gates are complete; scope revision accepted.
No product/MVP implementation acceptance or new implementation authorization.

IP4 publication and verification complete on `refactor-milestones-user-stories`.
Developer “execut phase 4” authorized publication and separately approved
squash merge of PR #57 after passing checks. Published reviewed head `4d8b398`;
[PR #57](https://github.com/jimthompson5802/agentic-ml/pull/57) merged as
`cef75068e1fd161b97507b0afb038a752f68b615` at 00:28 UTC. Branches retained.
Hosted Linux/Python 3.12 CI: 471 passed, three existing skips; lint, formatting,
typing, smoke, package paths and lock immutability passed. No local runtime tests
or new platform/MVP functionality claimed.

Verified 32 issue edits, 35 scope comments and two new integration issues:
[US-39 #58](https://github.com/jimthompson5802/agentic-ml/issues/58) and
[US-40 #59](https://github.com/jimthompson5802/agentic-ml/issues/59).
All 43 complete discussions are stable; existing states, metadata and history
preserved. Six no-action accepted issues untouched. Remote criteria 209 plus
13 local-only US-34/37/38 criteria equals 222. Source documents were on main and
matched reviewed blobs before any issue writes. No draft URL rewrite, duplicate
creation, issue closure/reopening or blind retry.

[Plan](docs/plans/mvp-scope-revision.md),
[IP4 evidence/action links](docs/verification/mvp-scope-revision-ip4.md) and
[published package](docs/plans/mvp-scope-issues/README.md) own actual results.
Raw snapshots, per-command ledger, CI logs and verification:
`.dev-records/verification/20261107-mvp-scope-ip4-25544e5/`.
Historical 11 external evidence-path limitations, M1/M50 obligations, failures/
skips and platform limits remain open; no assertions or checks weakened.

Developer “I like this, run those commands” explicitly authorized stashing the
accepted final records, switching to main, pulling with fast-forward only,
restoring the stash, committing and pushing directly to main without another PR.
Recording direction before publication; preserve the feature branch and existing
stashes. Product source, tests, dependencies, resources and verification policy
unchanged. **Next action:** complete the authorized direct-main publication,
then await separately authorized product planning.
This does not accept an implemented MVP.
Next product step after separate authorization: coordinated US-39 M1 implementation
plans with supplying story slices and confirmed public test boundaries; US-40 is
the M2 reproduction integration owner. Historical Phase 1–3 decisions/evidence
remain in owning plans, reports and Git history.

## Historical Phase 2 review — 2026-11-06

Developer “i approve gate 1 and authorize phase 2” approved scope and authorized
IP2. IP2-T1–T5 are technically complete on `refactor-milestones-user-stories`,
baseline `0a7b643`: [revised stories](docs/specs/user-stories.md),
[migration/follow-up ownership](docs/plans/mvp-scope-story-migration.md),
[issue drafts](docs/plans/mvp-scope-issues/README.md),
[plan](docs/plans/mvp-scope-revision.md) and
[IP2 evidence](docs/verification/mvp-scope-revision-ip2.md).

Preserved 204 original IDs and accepted/deferred/backlog wording; added 18 criteria
for US-39/40 with ASW-01–08 ownership. Prepared 32 edit/comment actions, three
accepted-issue comments, six no-actions and two new issue drafts. All 41 issue
timestamps/states match complete IP1 snapshots. Initial sandbox inventory read
failed; escalated read succeeded. No issue writes, commits, pushes or PRs.

Document checks pass: criterion/milestone mapping, body/template/manifest parity,
local/intended-source links and all 913 repository-relative incoming story links;
source/tests/lock/design/development instructions unchanged. No executable tests
or assistant walkthrough run. IP2 raw records:
`.dev-records/verification/20261106-mvp-scope-ip2-0a7b643/`.
Working-tree changes: revised stories, plan/report/checkpoint records, migration,
IP2 evidence and unpublished issue package; pre-existing IP1 work preserved.
**Next action:** developer Gate 2 review/approval. Stop before IP3 design edits
or GitHub publication; remote source-link publication requires separate direction.
M1/M50 verification obligations, skips, failures and platform limits remain open.

Developer “commit changes” authorized a local Conventional Commit of the current
Phase 1–2 documentation, revised stories and unpublished issue package. Recording
direction before committing. Gate 2 remains pending; no Phase 3, push, PR or
GitHub issue publication authorized. Next action remains developer Gate 2 review.

## Historical Phase 1 review and assistant refinement — 2026-11-06

Developer “Implement the plan” authorized IP1 of the
[MVP revision plan](docs/plans/mvp-scope-revision.md) on
`refactor-milestones-user-stories`, baseline `0a7b643`. IP1-T1–T4 technically
complete; [criterion dispositions](docs/reviews/mvp-scope-criterion-dispositions.md)
and [IP1 evidence](docs/verification/mvp-scope-revision-ip1.md) are ready for Gate 1.
Retrieved 41 complete stable issue snapshots (one comment), mapped all 204 local
criteria and recorded milestone/decision/owning-plan impacts. Scope reductions
remain proposed; authoritative stories/design/issues unchanged. Development
gates, historical evidence, M1/M50 verification obligations and three skips preserved.

Document/source checks pass: complete criterion mapping, local links/anchors,
whitespace and unchanged source/stories/lock identities. One copied relative link
failed initial validation; corrective attempt 1 rebased it and renewed validation
passed. No executable tests, dependency changes, commit/push/PR or issue writes.
Raw records under `.dev-records/verification/20261106-mvp-scope-ip1-0a7b643/`.
Working-tree changes: plan, disposition report, evidence and this checkpoint,
including the pre-existing reassessment entry. **Next action:** developer Gate 1
review/approval; stop before IP2 and authoritative requirements edits.

Developer “make the assistant-support walkthrough explicit” authorized plan/report
refinement MVP-SC-02. Added ASW-01–08 for scientist-directed external assistant
setup, extraction, features, baseline/tuning, MLflow inspection and validation-based
revision, final testing, DVC reproduction and notebook/regression/customization.
Mapped future story/design ownership and concrete assistant/version plus output
evidence requirements. Existing criterion dispositions preserved; no walkthrough
executed, authoritative story/design edits or managed-agent scope added. Renewed
document/source checks and whitespace pass; Gate 1 remains pending.

## Historical MVP reassessment — 2026-11-06

On `refactor-milestones-user-stories`, baseline `0a7b643`, reviewed the milestone
and story definitions, design overview/topic contracts and decision register,
public package/CLI implementation, recorded acceptance, and live GitHub issue
states against the developer's original lightweight ML experiment MVP intent.
M0 and US-01/02/03/05 are delivered; M1 execution/tracking and M2–6 remain planned.
Recommended a narrower local tabular end-to-end delivery and explicit deferral
of managed agents, durable orchestration and stronger isolation guarantees.
This is advice, not an approved scope change. Existing requirements and gates
remain in force. No product/specification/plan edits or tests; static assessment
only. Working-tree change: this checkpoint. Next action: developer scope decision.

## Walkthrough software reference — 2026-11-05

Developer requested appending the class/function explanation to
`docs/specs/example-walkthrough.md` and integrating short descriptions in sections
1–7, then asked whether all interfaces were accounted for. Added scenario-local
descriptions and an appendix covering public services, protocol methods, 213
blueprint table entries, inline records/aliases, 37 error classes, conceptual-name
replacements, and remaining implementation decisions. Corrected stale claims that
implemented APIs were unspecified. Blueprint remains authoritative for fields and
signatures; private helpers are explicitly outside this inventory.

Documentation only; TDD and executable checks do not apply. Type-table coverage,
error-name coverage, local link targets, and `git diff --check` pass. Developer
authorized commit and push of the walkthrough and this checkpoint on the existing
`embellish-software-component-descriptions` branch. Recording authorization before
publication; next action: developer review of the updated branch. No merge requested.

## Blueprint formatting correction — 2026-11-05

Developer requested `uv run --locked ruff format --check .` and fixes. Initial
check found one unformatted file: Python fences in the software blueprint.
Ran `uv run --locked ruff format docs/specs/design/software-blueprint.md`;
renewed exact full check passes, 161 files already formatted. `git diff --check`
passes. Documentation formatting only; no executable behavior or lock change.
Developer “commit and push” authorized committing the blueprint formatting fix
and this checkpoint and pushing to the existing PR #56 branch.
Next action: developer PR review. No merge requested.

## Current software blueprint IP6 final review — 2026-11-05

Developer “push and create pull request” authorized publication. Pushed approved
branch and opened [PR #56](https://github.com/jimthompson5802/agentic-ml/pull/56)
into `main`; verified title/body, ownership, base/head, non-draft and initial
head `62ecce2`. Renewed six diagram parses, 889 links/anchors, 160-criterion
equality and branch whitespace checks pass. Publication-record follow-up only;
committing/pushing plan and checkpoint records to the same PR. Next action:
developer PR review. No merge authorized. Earlier no-publication statements below
are historical; unresolved product decisions remain unchanged.

Developer “commit” authorized committing approved IP6 documentation and final
reconciliation. Recording direction and creating the local Conventional Commit;
next action await developer direction. No push or PR requested.

Developer “i approve ip6” approved the final documentation phase on 2026-11-05 UTC.
All IP1–IP6 tasks/gates are complete; approval recorded in plan/evidence and current
design status. Changes remain uncommitted; next action await developer direction.
No commit/push/PR requested. Earlier pending statements below are historical;
implementation blockers and deferred authentication remain unchanged.

Developer “commit then start ip6” authorized IP5 commit first, completed as
`0db2ded`, then IP6. On `embellish-software-component-descriptions`, IP6 T1–T6
technically complete in [plan](docs/plans/software-blueprint.md).
[IP6 evidence](docs/verification/software-blueprint-ip6.md) records complete stable
issue #54–55 bodies/comments/metadata (zero comments), 23 M6 table records,
five services, three protocol methods and source-limit/recovery contracts.
[Final coverage index](docs/verification/software-blueprint-final-coverage.md)
maps every one of 160 M1–6 criteria; all nine original protocols reconciled.
US-23-AC-02 authentication remains partial/deferred; eight named decision/assurance
records preserve implementation blockers and owners. No product delivery implied.

Design 0.14 updates overview/date/reading map, topic/API/resource-path authority
and stale interface/name/implementation statements. Checks pass: 889 relative
links/anchors, 160 unique source criteria, 27 public source classes (two private
helpers excluded), M6 inventory, nine protocols, six Mermaid parses and whitespace.
No executable/source/dependency/lock changes, runtime tests or new platform evidence.
Uncommitted work: blueprint/overview/topic docs/plan, IP6 report, final index and
this checkpoint. IP6 final approval pending; next action developer review and
approval or changes. No IP6 commit/push/PR requested. Earlier snapshots historical.

## Historical software blueprint IP5 review — 2026-11-05

Developer “commit then start ip6” authorized IP5 commit before IP6 execution.
Recording direction and committing approved M5 documentation first; next action
IP6. No push/PR requested. Earlier execution holds below are historical.

Developer “i approve ip5” approved IP5 on 2026-11-05 UTC. Approval recorded in
plan and evidence; changes remain uncommitted. Next action: await developer
direction to commit and/or start IP6. IP6 unstarted; no publication authorized.
Earlier pending-approval statements in this snapshot are historical.

Developer “i approve ip4; commit and start ip5” approved IP4, committed first as
`df2d32a`, then authorized IP5. On `embellish-software-component-descriptions`,
IP5 T1–T6 complete in [plan](docs/plans/software-blueprint.md), with
[evidence](docs/verification/software-blueprint-ip5.md). M5 catalogue contains
32 table types/aliases, five services, nine orchestrator/store methods plus
concrete store/adapter slots and error contracts. All 17 criteria mapped;
US-23-AC-02 authenticated authorship explicitly partial/deferred under US-03-SC-01.
No source requirement removed or claimed satisfied through unauthenticated labels.
Full bodies/all comments/refreshed metadata #40–43 stable, zero comments.

Document checks pass: 67 local links/anchors, type/function/method/criterion inventory,
five Mermaid parses and whitespace. SQLite local state/epoch fencing and durable
reconciliation are proposed contracts; second concrete integration remains M5-D2.
No runtime tests/code/dependency/lock changes or platform support evidence.
Uncommitted work: blueprint/plan/overview/interface/execution links, IP5 report
and checkpoints. IP5 approval pending; next action review, await approval before
IP6. No IP5 commit/push/PR requested. Earlier checkpoints below are historical.

## Milestone 6 issue publication — 2026-11-05

At developer request, created feature issues from the local M6 stories using the
repository user-story template: [US-28 #54](https://github.com/jimthompson5802/agentic-ml/issues/54)
and [US-29 #55](https://github.com/jimthompson5802/agentic-ml/issues/55).
Checked open/closed issues and story searches before publication. Verified exact
published bodies, enhancement labels and all 11 unchanged acceptance criteria;
removed only task-owned temporary issue files after verification. No implementation
or phase progression authorized by issue creation. IP4 remains awaiting developer
approval; prior blueprint state and uncommitted documentation preserved.

## Historical software blueprint IP4 review — 2026-11-04

Developer “i approve ip4; commit and start ip5” approved IP4 on 2026-11-05 UTC,
authorizing commit before IP5. Recording approval and committing reviewed M4
documentation plus the M6 issue publication checkpoint; next action IP5.
No push or PR requested. Earlier pending approval statements are historical.

Developer “i approve ip3; commit and start ip4” approved IP3, committed first as
`7b00662`, then authorized IP4. On `embellish-software-component-descriptions`,
IP4 T1–T5 complete in [plan](docs/plans/software-blueprint.md), with
[evidence](docs/verification/software-blueprint-ip4.md). Added M4 catalogue:
32 table types/status alias, 10 service functions, proposed five-method AgentAdapter,
first concrete adapter slot and seven errors; all 26 criteria mapped. Issues
#34–39 bodies/all comment pages/refreshed metadata stable, zero comments.
#37's older authentication assurance explicitly superseded by US-03-SC-01.

Checks pass: 65 local links/anchors, type/function/criterion inventory, four Mermaid
parses and whitespace. No executable changes/tests, lockfile edits or support
claims. M4-D1 assistant/kernel isolation and M4-D2 first concrete product/interface/
version remain implementation blockers. Uncommitted work: blueprint/plan/overview,
interfaces/execution links, IP4 report and this checkpoint. IP4 approval pending;
next action review, await approval before IP5. No IP4 commit/push/PR requested.

## Historical software blueprint IP3 review — 2026-11-04

Developer “i approve ip3; commit and start ip4” approved IP3 and authorized commit
before IP4. Recording approval and committing reviewed M3 documentation first;
next action IP4. No push or PR requested.

Developer “i approve ip2, commit then start ip3” approved M2 and directed commit
before IP3. Published local commit `4d38afd` first; no push. IP3 T1–T5 complete
in the [plan](docs/plans/software-blueprint.md), with
[evidence](docs/verification/software-blueprint-ip3.md). M3 blueprint documents
35 table types, 13 service functions, model/checkpoint protocols and concrete
framework adapter contracts, distinct evaluation/acceptance outcomes and final
review flow. Full bodies/all comments/refreshed metadata #26–33: stable, zero
comments. #32's older authentication dependency is explicitly superseded by
recorded US-03-SC-01; holdout enforcement remains required under M3-D1.

Checks pass: 60 local links/anchors, 35 types, 13 services, all 35 criterion
references, three Mermaid parses and whitespace. No executable change/tests,
lockfile changes or new platform evidence. Current uncommitted work is M3
blueprint/plan/overview/topic links, IP3 report and checkpoints. IP3 approval
pending; next action is review and await approval before IP4. No IP3 commit,
push or PR requested. Earlier pending-gate snapshots below are historical.

## Historical software blueprint IP2 review — 2026-11-04

Developer “i approve ip2, commit then start ip3” approved IP2 and authorized
commit before IP3. Recording approval and committing M2 documentation first;
next action is IP3. Earlier pending-gate statements below are historical.
No push or PR requested.

Developer approved IP1 and directed commit first, then IP2. Committed approved
M1 documentation as `a475835` on `embellish-software-component-descriptions`.
IP2 tasks T1–T5 are complete in the [plan](docs/plans/software-blueprint.md);
[evidence](docs/verification/software-blueprint-ip2.md) records source reconciliation,
inventory/detail/reference closure and all 22 M2 criterion mappings. Blueprint
adds 33 proposed table types, preprocessing/reference-estimator protocols, errors,
services and lifecycle diagram. Issues #19–23 full bodies/all comment pages and
metadata refreshed: stable, zero comments. M2-D1 holdout isolation remains a
blocking implementation decision. No executable changes or runtime verification.

Both Mermaid fences parse. Document checks pass: 48 local links/anchors, 33 type
inventory entries, 22 criteria, whitespace. Initial inventory check rejected
abbreviated paired record names in evidence; expanded names and renewed check
passes. Changes since commit: blueprint, plan, overview/data-feature links, IP2
report and this checkpoint. IP2 approval pending; next action is developer review,
then await authorization before IP3. No IP2 commit/push/PR requested.
At developer request, clarified that M2 proposes replacing FeatureEngineeringAdapter
with authored FeaturePlan and execute/compare services, rather than implementing
the original protocol. Explicit replacement mapping added; IP2 gate still pending.

## Historical software blueprint IP1 review — 2026-11-04

Developer “i approve ip1, coomit firs then move to ip2” approved IP1 and authorized
commit before IP2 execution. Recording approval and committing the reviewed
documentation; next action is IP2. Earlier pending-gate statements below are
historical. No push or PR requested.

Developer “Implement the plan” authorized documentation work through IP1, with
separate later phase gates. Created `embellish-software-component-descriptions`
first, from clean `main` at `59e4beb`. Added the
[plan](docs/plans/software-blueprint.md),
[M1 blueprint](docs/specs/design/software-blueprint.md),
[evidence](docs/verification/software-blueprint-ip1.md) and design navigation links.
Issues #8–18 bodies/comment pages/metadata refreshed; all zero comments, stable.
No executable changes, dependency changes or tests; document checks only.
M1-D1 isolation remains an explicit owning-story decision. IP1 developer gate
review refinement now specifies ExperimentSpec fields, construction, manifest
authority, immutability and submission checks at developer request. Document-only.
Developer “i agree complete m1 first” authorized extending the same precision to
all M1 public and referenced records. Catalogue now includes existing fields and
defaults plus proposed types/methods/lifecycle/negative cases, with explicit
later-milestone deferrals. Document checks renewed; no executable changes.
IP1 gate remains pending; next action is review, then await approval before IP2.
No commit/push/PR.
Developer “make that update to the plan” authorized recording the M1 detail
standard for IP2–IP6. The plan now requires per-phase type inventories, complete
contract descriptions, reference closure, cross-milestone reconciliation and
criterion checklists, with explicit completeness tasks at every remaining gate.
Documentation-only plan refinement; IP1 approval still pending, IP2 unstarted.
Fixed developer-reported Mermaid parse failure: reproduced line-20 error, removed
semicolon from sequence note, and verified the same cached Mermaid parser passes.
Attempt 1 successful; whitespace passes. Evidence appended to IP1 report.
Historical executable evidence and milestone obligations below remain unchanged.

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
