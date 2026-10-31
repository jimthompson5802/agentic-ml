# Development Checkpoints

Last updated: 2026-10-31

## Current position

US-02 accepted by “i accept us-02” (2026-10-31); all implementation gates and
original corrections approved. Accepted changes committed as `8fe0e8f` and pushed
on `US-02-experiment-init`. [PR #45](https://github.com/jimthompson5802/agentic-ml/pull/45)
is open against `main`; [static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/45#pullrequestreview-5722316537) is published.

**Current tooling work:** Optional parallel tests implemented and verified under
developer “implement the change” and “yes” for the compatibility constraint.
Development pytest-xdist 3.8.0 / pytest 9.1.1 (`>=8,<9.2`); installation and
distribution groups stay together, initialization/CLI cases distribute individually.
Developer subsequently requested agent instructions to use four workers locally.
The development guide now requires `uv run --locked pytest -n 4 --dist=loadgroup`
for local verification, with recorded exceptions for focused TDD/diagnosis and
resource comparisons. Pytest configuration and CI remain serial. Final complete runs: **129 passed** with
two workers in **16m59s**, four in **12m06s**; group placement and unique case sets
verified. New public scheduling regression caught pytest 9.2.0 silently ignoring
groups; approved compatibility correction passed on its first attempt. Earlier
128-case benchmarks are historical and do not establish grouping correctness.
Shared checks passed; final lock SHA-256
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
Evidence: [parallel tests](docs/verification/parallel-test-execution.md).
Developer “commit change” authorizes the local commit of parallel tooling,
four-worker local instructions and verification records. Push remains unauthorized.
Next action: developer review. macOS verified; Linux/Windows parallel execution
and cancellation descendant cleanup remain unverified.

Local-command instruction update is documentation-only: no executable behavior,
dependencies, lock or CI changed in that update. TDD and runtime reruns do not
apply. Local Markdown link/anchor and whitespace checks verify the edited guidance.

**US-02 status:** temporary-path correction committed as `3a5fd84`, focused
regressions passed. The later complete tooling runs renew TMP-T3 verification,
including installed initialization and distribution checks. Correction gate
remains pending; no push or merge authorized. Historical cancellation follows:
developer requested cancellation of the full suite
for the approved temporary-path correction. Source guard and nine added cases
are implemented and committed as `3a5fd84`. Focused regressions: 38 passed. Shared checks and
both distribution/complete installed initialization paths passed. Full suite
cancelled at developer request: 27/128 passed, 101 incomplete, exit 130;
`/private/tmp/us-02-tmp-full.xml`. Do not restart without direction. Correction
gate remains pending. Developer “commit changes” authorized the local correction
commit; push remains unauthorized. See
[correction evidence](docs/verification/us-02-temp-path-fix.md) and
[owning plan](docs/plans/milestone-1-us-02.md).

Original
[Medium review finding](https://github.com/jimthompson5802/agentic-ml/pull/45#discussion_r4431369976): storage override
`.agentic-ml/init.tmp` conflicts with the journal temporary file. The 119-test
suite was historical and did not cover this path. Original acceptance remains
recorded; the follow-up is implemented but full verification/review is incomplete.
No merge, cleanup or next-story work is authorized. Hosted Linux CI passed before
this correction; it does not cover the new uncommitted source.

## Development verification policy — 2026-10-31

Developer “Ok make this change” authorized impact-based testing for future plans.
Updated AGENTS.md, the [development policy](docs/development.md#phase-and-story-verification),
the plan template and create-implementation-plan / execute-plan / manage-plan-scope
skills. Intermediate gates use justified affected/dependent tests and shared
checks; final verification requires the full suite and applicable installed
distribution checks before final gate approval and story acceptance. Broad
changes trigger earlier full runs. Existing approved plans, including US-02,
retain their recorded requirements unless explicitly revised.

Documentation/workflow changes only: TDD and the product suite do not apply;
no executable behavior changed. All three edited skills passed `quick_validate.py`
using the existing project interpreter; 34 local Markdown links/anchors and
`git diff --check` passed. Manual policy walkthrough covered narrow phase scope,
slow relevant tests, broad-change triggers, known failures, existing approved
plans, deferred-check reconciliation, and executable versus document-only
evidence renewal. No source, tests, dependencies, lock, CI or story-plan changes.
Developer “commit changes” authorizes the local commit of these policy edits
and this checkpoint on `US-02-experiment-init`. Push/publication of this separate
workflow change is not requested. The US-02 review finding above remains pending
and is outside this change.

## Resume here

- P1/P2 focused regressions passed: 5 unsafe-backup cases, 28 metadata overlap cases, and installed API rejection/corrected CLI retry with matching backups. Shared sync/lock/lint/format/types/version checks passed. Full suite passed: **119 passed**, exit 0, 1898.17s (31:38), including direct/rebuilt distribution checks and full installed initialization. Retained fixtures at `/private/tmp/us-02-review-suite`; XML `/private/tmp/us-02-review-suite.xml`. Earlier evidence below is historical IP4 evidence and does not by itself cover these defects.

- Implemented configurable local DVC/cache/default remote, MLflow SQLite/artifacts/experiment and durable unconfigured JSON state. Preflight protects existing content, selected paths, permissions, exclusions and matching identities. Setup journals retain stage/exit-code evidence and safe retries; no runs or approvals are created.
- **Clean full suite: 85 passed**, exit 0, 1829.72s (30:29). Command: `env MLFLOW_DISABLE_TELEMETRY=true DVC_NO_ANALYTICS=1 uv run --locked pytest --junitxml=/private/tmp/us-02-ip4-evidence/clean-pytest.xml`. All tests remain enabled; optional telemetry settings did not materially shorten the run.
- Earlier full run had 84 passes and one legacy UTF-8 probe failure against SQLite. Corrected the same complete recursive source-sentinel exclusion to scan bytes; focused rerun and subsequent clean full run passed. Original/focused/clean XML files remain in `/private/tmp/us-02-ip4-evidence`. No product change or file exclusion accompanied the probe correction.
- Shared locked synchronization, lock consistency, lint, format (78 files), strict types (20 source files), version smoke (0.1.0), local Markdown links and whitespace passed. No dependency/lock changes, suppressions, disabled checks or unresolved failures.
- Direct and sdist-rebuilt review wheels passed normal installed checks. Artifacts: `/private/tmp/us-02-ip4-evidence/review-artifacts`; workspace `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-mchx6nbs`. Complete artifact-derived initialization passed for fresh CLI and existing-package API projects on both paths, with installed package bytes matched to wheels and genuine Git origin checks.
- Clean-run installed fixtures: system temporary `pytest-of-jim/pytest-20/test_complete_initialization_f0/initialization`, full local source SHA `ad28a3e54f2314673db7c4bf253195e1c11cb471`. These are local unpublished fixture commits, not GitHub installation claims.
- Developer manually executed the generated notebook in VS Code. Saved stdout confirms project `.venv/bin/python`, Python 3.12.15. Evidence: `/private/tmp/us-02-ip4-evidence/manual-vscode.ipynb`; VS Code 1.135.0, Python extension 2026.10.0, Jupyter 2025.9.1.
- macOS 15.7.9 arm64/Python 3.12.15/uv 0.13.1/Git 2.54.0 verified locally. No new Linux/Windows evidence. Harness lock remains `b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`.
- Issue #9 complete body/all comment pages refreshed at entry: stable zero-comment snapshot, updated `2026-10-31T01:15:38Z`; Milestone 1 / AC-01–05, no new scope decision. GitHub public reads succeeded. Publication-time authentication succeeds outside the sandbox; the earlier invalid-token result was sandbox-specific.
- Cache/log-directory sandbox denials were retried with approved escalation. They were infrastructure failures, not behavior reds. All granular failure/correction evidence is in the IP4 report.
- Original IP4 implementation and approval records are committed as `b6a353c`. Accepted source, tests, correction evidence and acceptance records are committed as `8fe0e8f` and pushed. Publication outcome records are documentation-only and will be committed/pushed under acceptance authorization; no unrelated changes were present at entry.

## Accepted work and supporting context

Milestone 0 is complete and accepted (US-31, US-32, US-33), merged in PR #24 as `018e9d4bb26e121c7f9274d11e0de560b7514b95`; observed main CI passed. Subsequent development rules/skills/specification work is recorded in Git history.

US-01 is accepted and merged through [PR #44](https://github.com/jimthompson5802/agentic-ml/pull/44), merge `5d662f65ed38cdca988f968164c773b3be6f84bf`; issue #8 closed. Both implementation gates, installed A→B GitHub upgrade checks, hosted Linux CI and static COMMENT review passed. See [US-01 plan](docs/plans/milestone-1-us-01.md) and its linked evidence. Later observed main CI at `4477162` passed. No US-01 decision is pending.

US-02 approved plan/public boundaries: developer “commit changes; i approve the plan, execute us-02 ip1” (2026-10-30). IP1 contracts/ADRs approved, committed `12df741`; IP2 approved, implementation commit `265ed5b`; IP3 approved by “i approve ip3”, then local commit authorized by “commit” (2026-10-31), committed `0830888`. IP4 gate subsequently approved by “i approve ip4”, corrections approved by “i approve”, and whole story accepted by “i accept us-02” (2026-10-31).

Notebook-editor scope decision SC-01 is recorded in the plan, issue #9 and issue #36: VS Code is installed separately; ipykernel/nbclient remain requirements. Manual kernel checking does not establish managed execution or isolation.

Repository-local GitHub read and development command guidance is in [docs/development.md](docs/development.md#repository-local-codex-command-approvals), with rules in `.codex/rules/default.rules`. Tool permissions do not approve implementation gates or publication. Explicit whole-story acceptance triggers the execute-plan publication workflow only after all gates and verification pass.

The requested executive overview remains outside the repository at `/Users/jim/Desktop/genai/agent-ml-overview.md`. Its creation was documentation-only; no additional product scope followed. Milestones 1–5 issues remain published; other story implementation is unauthorized. Milestone 99 remains deferred.

## Maintenance rules

- Keep this file a concise current handoff. Replace stale resume instructions and notes; Git history preserves earlier checkpoints.
- Summarize overall progress and link to authoritative records. GitHub issues govern scope; implementation plans own granular tasks, evidence, scope changes and gate decisions. Resolve discrepancies against those sources before resuming.
- Record approval only after the developer explicitly gives it, with the decision in the owning plan. Technical completion and plan approval do not approve progression.
- Update the date, current position, next action, pending decisions, working-tree state and material verification notes at completed work, gates, blockers and handoff. Preserve failure evidence.
- Commit checkpoint updates alongside their work when authorized. Keep credentials and sensitive environment details outside this file.
