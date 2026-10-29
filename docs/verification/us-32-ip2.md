# US-32 IP2 hosted verification

Date: 2026-10-29. Issue [#2](https://github.com/jimthompson5802/agentic-ml/issues/2), Milestone 0, US-32-AC-01–04. IP1 including Linux SC-01 approved by developer message “I approve IP1. Commit the Linux changes, push the branch, and create a PR to begin IP2.” This authorized publication and IP2 entry. Developer subsequently merged PR #5 and approved IP2; final decisions are recorded below.

## T1 — Pull-request baseline

[PR #5](https://github.com/jimthompson5802/agentic-ml/pull/5), branch `us-32-setup-gh-action-ci`, base `main`, same repository owner; verified open/non-draft with intended body and refs #2 (no closing keyword). Commit `6e7c389158728598e29ab2e311286177f7133891` contains the Linux revision and IP1 approval.

[Baseline run 40973713670](https://github.com/jimthompson5802/agentic-ml/actions/runs/40973713670): `pull_request`, success, exact head above. All named steps passed: checkout, initial lock checksum/no existing .venv, uv and Python installation, locked synchronization, environment diagnostics, lock consistency, automated tests, lint, formatting, strict types, version smoke and final lock verification. PR checks expose step conclusions and diagnostics.

Observed runner: Ubuntu 24.04.5 LTS, x86_64, `ubuntu-24.04` image `20261025.353.1`, runner 2.338.0. Downloaded CPython 3.12.15; uv 0.13.1; pytest 9.2.0; Ruff 0.17.3; mypy 1.20.2. New virtual environment; no restored project environment/dependency cache. Tests: 3 passed. Formatting: 45 files; strict types: 3 source files; version: 0.1.0. All seven shared commands passed.

Initial lock SHA-256 `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`; final verification reports `uv.lock: OK`, and tracked lock diff exits 0. No silent regeneration occurred.

Evidence retrieved with explicit-repository `gh run view 40973713670 --json databaseId,event,headSha,conclusion,jobs,url` and `gh run view 40973713670 --log`. Raw baseline JSON/log and subsequent fixture evidence live outside Git under `/tmp/us32-ip2-evidence/`; run URLs preserve accessible hosted evidence. Complete issue/comments refreshed before implementation: zero comments, stable snapshots, Linux SC-01 present.

## T2 — Controlled failures and corrections

[Disposable draft PR #6](https://github.com/jimthompson5802/agentic-ml/pull/6), branch `us-32-ci-failure-verification`, is dedicated to planned failure/correction evidence. Deliberate defects must never merge. Original production assertions, thresholds and checks remain intact; each fixture is removed or source restored before its green correction run and before the next case.

| Case / controlled defect | Failed run and head commit | Diagnostic | Correction run and head commit |
|---|---|---|---|
| pytest: Added standalone assertion `1 == 2` fixture; original tests untouched. | [failed run 40973933494](https://github.com/jimthompson5802/agentic-ml/actions/runs/40973933494), `599284a9a9864449ea67366013fd5effbc9e585b` | Automated tests exit 1; AssertionError. Strict types also detects comparison-overlap. | [passed run 40973996177](https://github.com/jimthompson5802/agentic-ml/actions/runs/40973996177), `01cd07ff90c1f49e6a235f91e07ce7d71e4bca43` |
| lint: Added top-level undefined-name fixture. | [failed run 40974042345](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974042345), `fba798f9c4243db5b52cfa38248bf8f6794d6ef1` | Lint exit 1; F821 undefined_us32_name. | [passed run 40974079530](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974079530), `94049a874459c40551c467a6b15ebbf1438604f4` |
| format: Added unformatted `VALUES=[1,2]` fixture. | [failed run 40974144727](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974144727), `9f82442664427caf165c1b7916142ed676786ab4` | Formatting check exit 1; fixture requires formatting. | [passed run 40974197015](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974197015), `6bd812a106b46bbcfaa2b9e85e1e7ca422ac4c6d` |
| types: Added typed function returning str where int declared. | [failed run 40974247434](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974247434), `1ec407cb4fd9c9c227c1578a20c54c3875b9926f` | Strict type checks exit 1; incompatible return-value. | [passed run 40974461133](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974461133), `8dd81bf05e00fa87453a5ecb799ccb8d44c1280a` |
| smoke: Temporarily exit 17 before CLI argument parsing. | [failed run 40974682445](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974682445), `dc377cf766f6a0a152d74c1104a6002b93ff7f7d` | Development smoke check exit 17; existing CLI subprocess tests also fail. | [passed run 40974731993](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974731993), `df1a99ce6cb7a4e99c59cdbdd6b816d7b08d902a` |
| lock: Add packaging>=26 runtime metadata without changing uv.lock. | [failed run 40974785800](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974785800), `6e08207cb0b0acdea3abdfb80b36d031d37ddd4e` | Synchronize locked dependencies exit 1: lockfile needs updating but --locked provided; dependent checks skipped. | [passed run 40974827277](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974827277), `3ba80c949cdb64ed7a90dcb7c8839f5ccc39e192` |

Every intended failed command and overall job concluded failure. After successful synchronization, all five independent checks ran, including after failures; cross-check detection is listed above. Each case was followed by a separate all-green correction run before the next case. Every red and green run passed final lock immutability with `uv.lock: OK` and a clean tracked diff. Stale metadata failed setup, skipped dependent check steps and still passed final lock verification. `Post Install uv` was skipped on failed jobs by the upstream action's post condition; this did not skip the workflow's lock verification.

Final disposable commit `3ba80c949cdb64ed7a90dcb7c8839f5ccc39e192` matches clean baseline `6e7c389` exactly (`git diff 6e7c389 --` empty). No deliberate defects are in PR #5. Raw per-case JSON/logs preserve complete step conclusions and diagnostics. Hosted run links are reachable from draft PR #6's Checks tab. The fixture PR is closed after verification, without merge.


## T3 — Default-branch merge and push verification

Developer reported “I merged pr #5” on 2026-10-29. GitHub confirms PR #5 merged at `2026-10-29T23:47:14Z`, merge commit `0a3c087f8b0273be9cd3fb4b2f57a9846614fd86`. The merge tree `65c29788effbad87c78a0c0c8f167af1296ba6ce` exactly matches the reviewed local PR head tree. No disposable defect was merged.

[Default-branch run 40975472618](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618): event `push`, branch `main`, exact merge SHA above, conclusion success. Every job step passed, including clean checkout/new environment, locked setup, all seven shared commands and final checksum/diff verification. Observed Ubuntu 24.04.5 x86_64, image `20261025.353.1`, Python 3.12.15, uv 0.13.1, pytest 9.2.0, Ruff 0.17.3 and mypy 1.20.2. Three tests passed; formatting checked 47 files; strict types checked 3 source files; CLI printed 0.1.0. Lock checksum remained `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`; final `uv.lock: OK`, tracked lock diff exit 0.

Retrieved with explicit-repository `gh pr view 5 --json state,mergedAt,mergeCommit,url`, `gh run list --branch main`, and `gh run view 40975472618 --json databaseId,event,headSha,conclusion,jobs,url` / `--log`. Raw metadata/logs preserved as `main.json/.log` alongside other IP2 evidence. Issue #2 complete body/comments refreshed again: stable snapshots, open issue, zero comments, Linux scope decision retained.

## T4 — Final documentation and verification

README and development guide now link successful PR/default-branch runs and the six failure/correction pairs. Plans/index/checkpoint distinguish technical verification, IP2 approval and remaining US-33 scope. Final changes are documentation only: no new or corrected executable behavior, so existing hosted regression evidence applies instead of manufacturing a failing test. actionlint 1.7.12, local Markdown file-target checks, exact seven-command comparison, unchanged lock hash/tracked diff and `git diff --check` pass. Historical IP1 pending-hosted statements describe that earlier checkpoint; this report supplies final hosted evidence. Other Python versions/platforms and isolated wheel/sdist checks remain outside this evidence.

## Fixture correction attempt record

Smoke fixture attempt 1 placed `raise SystemExit(17)` after `parser.parse_args()`, expecting the version smoke to exit 17. [Run 40974507244](https://github.com/jimthompson5802/agentic-ml/actions/runs/40974507244), commit `1a82b0bc1a594d187c7764d306cf957065e98a28`, passed: argparse's version action exits successfully before that line. The evidence verifier correctly rejected this as failure evidence (`AssertionError: data['conclusion']=='failure'`); no CI failure was established. Raw metadata/log preserved as `smoke-ineffective.json/.log` outside Git. This was an ineffective disposable fixture, not a product defect. Corrective hypothesis: moving the exit before parsing reaches the real `--version` invocation. Attempt 2 moved the exit before parsing: run 40974682445 failed the smoke step with exit 17; restoring the exact baseline CLI produced passing run 40974731993. The original failure-verification assertion now passes. Two fixture attempts total; no product fix was required. No assertions, thresholds or workflow checks were weakened.

## Final acceptance mapping

| Criterion | Evidence | Result |
|---|---|---|
| AC-01 | Real clean Linux pull-request baseline and all fixture runs | Verified for PR and main push |
| AC-02 | Actual Python/uv/tool versions, locked install, matching checksum and stale-lock rejection | Verified for PR and main push |
| AC-03 | All seven documented commands pass in real hosted Linux runs | Verified for PR and main push |
| AC-04 | Six failed jobs/step diagnostics, independent checks continue, six green corrections; contributor PR/log instructions | Verified |

IP2-T1–T4 complete. Evidence commit `7661e1e6581c70a9da8390d35365c2c30796d78a` passed [PR run 40975072117](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975072117); final PR head `e6f0bd98452d02470fccd7c336d19797a9d75e7f` passed [run 40975167938](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975167938). The merge push run above completes both event requirements.

## Developer decision

Developer message “I approve us-32 ip2”, 2026-10-29, approves the final IP2 gate and accepts US-32 after all four criteria were verified. US-32 is complete and accepted. No downstream story or remaining US-33 implementation is authorized by this approval. Milestone 0 remains incomplete.
