# Development Checkpoints

Last updated: 2026-10-31

## Current position

US-02 IP1–IP3 are approved and committed through `0830888` on `US-02-experiment-init`. Developer message “go ahead with ip4” (2026-10-31) authorized IP4. IP4 T1–T4 are technically complete and developer-approved by “i approve ip4” (2026-10-31); [owning plan](docs/plans/milestone-1-us-02.md) and [IP4 evidence](docs/verification/us-02-ip4.md) record all five criteria and verification.

**Next action:** await separate explicit US-02 whole-story acceptance. All four implementation gates are approved. Developer message “commit changes” (2026-10-31) authorizes the local IP4 commit. Story acceptance, push and publication remain unauthorized.

## Resume here

- Review follow-up remains pending: P1 backup symlink/content-conflict validation and P2 storage overlap with initialization journal, lock and backup paths. These findings are not fixed by the authorized IP4 commit and qualify the earlier verification/completion statements below.

- Implemented configurable local DVC/cache/default remote, MLflow SQLite/artifacts/experiment and durable unconfigured JSON state. Preflight protects existing content, selected paths, permissions, exclusions and matching identities. Setup journals retain stage/exit-code evidence and safe retries; no runs or approvals are created.
- **Clean full suite: 85 passed**, exit 0, 1829.72s (30:29). Command: `env MLFLOW_DISABLE_TELEMETRY=true DVC_NO_ANALYTICS=1 uv run --locked pytest --junitxml=/private/tmp/us-02-ip4-evidence/clean-pytest.xml`. All tests remain enabled; optional telemetry settings did not materially shorten the run.
- Earlier full run had 84 passes and one legacy UTF-8 probe failure against SQLite. Corrected the same complete recursive source-sentinel exclusion to scan bytes; focused rerun and subsequent clean full run passed. Original/focused/clean XML files remain in `/private/tmp/us-02-ip4-evidence`. No product change or file exclusion accompanied the probe correction.
- Shared locked synchronization, lock consistency, lint, format (78 files), strict types (20 source files), version smoke (0.1.0), local Markdown links and whitespace passed. No dependency/lock changes, suppressions, disabled checks or unresolved failures.
- Direct and sdist-rebuilt review wheels passed normal installed checks. Artifacts: `/private/tmp/us-02-ip4-evidence/review-artifacts`; workspace `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-mchx6nbs`. Complete artifact-derived initialization passed for fresh CLI and existing-package API projects on both paths, with installed package bytes matched to wheels and genuine Git origin checks.
- Clean-run installed fixtures: system temporary `pytest-of-jim/pytest-20/test_complete_initialization_f0/initialization`, full local source SHA `ad28a3e54f2314673db7c4bf253195e1c11cb471`. These are local unpublished fixture commits, not GitHub installation claims.
- Developer manually executed the generated notebook in VS Code. Saved stdout confirms project `.venv/bin/python`, Python 3.12.15. Evidence: `/private/tmp/us-02-ip4-evidence/manual-vscode.ipynb`; VS Code 1.135.0, Python extension 2026.10.0, Jupyter 2025.9.1.
- macOS 15.7.9 arm64/Python 3.12.15/uv 0.13.1/Git 2.54.0 verified locally. No new Linux/Windows evidence. Harness lock remains `b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`.
- Issue #9 complete body/all comment pages refreshed at entry: stable zero-comment snapshot, updated `2026-10-31T01:15:38Z`; Milestone 1 / AC-01–05, no new scope decision. GitHub public reads succeeded; `gh auth status` still reports an invalid stored token. No publication attempted.
- Cache/log-directory sandbox denials were retried with approved escalation. They were infrastructure failures, not behavior reds. All granular failure/correction evidence is in the IP4 report.
- Changed source, tests, setup documentation, owning plan and checkpoint belong to IP4. No unrelated user changes were present at entry. Preserve all uncommitted work. IP4 approval records are documentation-only; whitespace validation passed and no runtime rerun was needed.

## Accepted work and supporting context

Milestone 0 is complete and accepted (US-31, US-32, US-33), merged in PR #24 as `018e9d4bb26e121c7f9274d11e0de560b7514b95`; observed main CI passed. Subsequent development rules/skills/specification work is recorded in Git history.

US-01 is accepted and merged through [PR #44](https://github.com/jimthompson5802/agentic-ml/pull/44), merge `5d662f65ed38cdca988f968164c773b3be6f84bf`; issue #8 closed. Both implementation gates, installed A→B GitHub upgrade checks, hosted Linux CI and static COMMENT review passed. See [US-01 plan](docs/plans/milestone-1-us-01.md) and its linked evidence. Later observed main CI at `4477162` passed. No US-01 decision is pending.

US-02 approved plan/public boundaries: developer “commit changes; i approve the plan, execute us-02 ip1” (2026-10-30). IP1 contracts/ADRs approved, committed `12df741`; IP2 approved, implementation commit `265ed5b`; IP3 approved by “i approve ip3”, then local commit authorized by “commit” (2026-10-31), committed `0830888`. IP4 gate subsequently approved by “i approve ip4” (2026-10-31); whole-story acceptance remains pending.

Notebook-editor scope decision SC-01 is recorded in the plan, issue #9 and issue #36: VS Code is installed separately; ipykernel/nbclient remain requirements. Manual kernel checking does not establish managed execution or isolation.

Repository-local GitHub read and development command guidance is in [docs/development.md](docs/development.md#repository-local-codex-command-approvals), with rules in `.codex/rules/default.rules`. Tool permissions do not approve implementation gates or publication. Explicit whole-story acceptance triggers the execute-plan publication workflow only after all gates and verification pass.

The requested executive overview remains outside the repository at `/Users/jim/Desktop/genai/agent-ml-overview.md`. Its creation was documentation-only; no additional product scope followed. Milestones 1–5 issues remain published; other story implementation is unauthorized. Milestone 99 remains deferred.

## Maintenance rules

- Keep this file a concise current handoff. Replace stale resume instructions and notes; Git history preserves earlier checkpoints.
- Summarize overall progress and link to authoritative records. GitHub issues govern scope; implementation plans own granular tasks, evidence, scope changes and gate decisions. Resolve discrepancies against those sources before resuming.
- Record approval only after the developer explicitly gives it, with the decision in the owning plan. Technical completion and plan approval do not approve progression.
- Update the date, current position, next action, pending decisions, working-tree state and material verification notes at completed work, gates, blockers and handoff. Preserve failure evidence.
- Commit checkpoint updates alongside their work when authorized. Keep credentials and sensitive environment details outside this file.
