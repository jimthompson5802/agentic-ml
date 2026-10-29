# US-32 IP1 verification

Date: 2026-10-29. Scope: issue [#2](https://github.com/jimthompson5802/agentic-ml/issues/2), Milestone 0, tasks US-32-IP1-T1–T3, criteria US-32-AC-01–04. Configuration/local evidence advances these criteria; hosted acceptance remains pending IP2. Base commit: `2d1b9b6`; workflow and documentation are included in the IP1 implementation commit; developer gate approval remains pending.

## Requirements and prerequisites

Retrieved the full issue twice with `gh api repos/jimthompson5802/agentic-ml/issues/2`, with all comment pages using `gh api --paginate --slurp 'repos/jimthompson5802/agentic-ml/issues/2/comments?per_page=100'`. Both snapshots report update time `2026-10-29T03:09:11Z`, zero comments, open issue, no PR marker and no assigned GitHub milestone. The body assigns Milestone 0. No scope changes or conflicts were found. The owning US-31 plan records both approved gates and acceptance; US-33 records approved CLI prerequisite IP1. Their evidence still matches the current source/tool configuration.

Repository API confirms `main`, Actions enabled, all actions allowed and authenticated admin/push permissions. Capacity and hosted execution have not been exercised. These read results do not authorize publication or merge.

## Original configuration choices (T1; runner superseded by SC-01)

- Runner: `macos-15`, explicit supported image label; [official image inventory](https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md). Hosted image version will be captured from job setup and environment diagnostics in IP2.
- [checkout v5](https://github.com/actions/checkout/tree/fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09): pin `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`, resolved from the official v5 Git ref. Supports Node 24 on hosted runners. Credential persistence disabled; token permissions limited to contents read.
- [setup-uv v7](https://github.com/astral-sh/setup-uv/tree/37802adc94f370d6bfd71619e3f0bf239e1f3b78): pin `37802adc94f370d6bfd71619e3f0bf239e1f3b78`, resolved by dereferencing annotated tag `94527f2e458b27549849d47d273a16bec83a01e9`. Official action metadata confirms Node 24 and version/python-version/cache inputs. uv is pinned to 0.13.1, Python selector is 3.12, dependency caching disabled. `uv python install 3.12` installs the interpreter before locked synchronization.
- [Status conditions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions): explicit `!cancelled()` overrides the implicit success condition for independent checks, guarded by successful synchronization. Final checksum uses `always()` and successful initial checksum capture, including synchronization failure.

Official sources were inspected during implementation, along with the design reading map, contributor contract, delivery dependencies, traceability and ADR-007. No new prerequisite or runtime capability is required.

## Original workflow inspection and local failure boundary (T2)

`/tmp/us32-ip1-tools/actionlint -version`: 1.7.12, Go 1.26.1, darwin/arm64. Downloaded official release archive; SHA-256 `aba9ced2dee8d27fecca3dc7feb1a7f9a52caefa1eb46f3271ea66b6e0e6953f` matches the [release checksum](https://github.com/rhysd/actionlint/releases/tag/v1.7.12).

`/tmp/us32-ip1-tools/actionlint .github/workflows/ci.yml`: exit 0, no diagnostics. No validator exclusions were added. Optional shellcheck was unavailable; shell behavior was inspected and directly exercised. Inspection confirms PR event without path filters, push to main, macos-15, immutable action revisions, read permissions, new environment check, locked sync, seven exact shared commands, named diagnostics and final hash/diff checks. No `continue-on-error` or log pipeline masks a nonzero result. Setup steps use normal success dependencies; a failed setup retains a failed job and prevents dependent checks. Static validation cannot establish GitHub event delivery or actual runner availability.

Disposable `/tmp/us32-ip1-evidence/lint_failure.py` contains `print(undefined_us32_name)`. Executing Ruff with `--select F821` followed by a sentinel printf under `/bin/bash --noprofile --norc -e -o pipefail -c` returned 1, reported F821 at line 1, and did not print the sentinel. This verifies real tool/shell nonzero propagation locally; GitHub job conclusions and continuation after failure require IP2. The defect is outside maintained source. No production assertions were changed. No corrective attempts were needed.

No new Python behavior was introduced: existing regression checks and workflow validation apply, rather than manufactured Python tests. IP2 will introduce and correct each planned defect individually through hosted PR boundaries.

## Local checks (T3)

Host: macOS 15.7.9 (24G830), arm64; Python 3.12.15; uv 0.13.1; pytest 9.2.0; Ruff 0.17.3; mypy 1.20.2. New environment `/tmp/us32-ip1-evidence/venv`, selected with `UV_PROJECT_ENVIRONMENT`; source is this checkout. Existing uv cache was used. This is local command verification, not a fresh hosted checkout or installed-wheel isolation test.

| Exact command | Result |
|---|---|
| `uv sync --locked --group dev` | Exit 0; fresh environment installed source and 12 packages; subsequent sync passed |
| `uv lock --check` | Exit 0; 13 packages resolved |
| `uv run --locked pytest` | Exit 0; 3 passed |
| `uv run --locked ruff check .` | Exit 0; all checks passed |
| `uv run --locked ruff format --check .` | Exit 0; 45 files already formatted |
| `uv run --locked mypy src tests` | Exit 0; 3 source files, no issues |
| `uv run --locked agentic-ml --version` | Exit 0; `0.1.0` |

Before/after lock SHA-256: `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`. `git diff --exit-code -- uv.lock`: exit 0. Raw command outputs and results JSON are under `/tmp/us32-ip1-evidence/`; durable results are summarized here. Initial sandbox sync failed on uv cache temporary-file permissions; authorized retry succeeded. A GitHub DNS failure and validator download DNS failure likewise succeeded after approved network retries. These are environment access retries, not corrective implementation attempts.

README/development guide now describe configured coverage, local reproduction, check/log navigation, download instructions, pinned setup and pending hosted evidence. All seven workflow commands match the guide. Local Markdown file targets and `git diff --check` pass. No dependencies, lock contents, runtime source, suppressions or package verification changed.

## Acceptance and gate

| Criterion | IP1 evidence | Remaining IP2 evidence |
|---|---|---|
| AC-01 | Required triggers and clean environment configured | Successful PR/default-branch events and runner details |
| AC-02 | 3.12/uv setup configured; local locked checks and matching hashes | Actual hosted versions, setup, immutability and stale-lock rejection |
| AC-03 | Seven exact commands configured and passing locally | Successful hosted checks |
| AC-04 | Named steps, preserved exits, local shell/tool failure and contributor log instructions | Each planned hosted failure/correction and accessible PR diagnostics |

T1–T3 technically complete. IP1 developer approval pending. No hosted run, publication or merge occurred. Other Python versions/platforms, US-33 distribution verification and US-34 policy remain excluded. After explicit IP1 approval and publication authorization, IP2 will collect a successful PR run, six isolated failure/correction cases, an authorized merge/default-branch run and final criterion mappings.

## SC-01 renewal — Linux CI (2026-10-29)

Developer instruction “for gh action I want to use a linux host, not macos” authorizes changing current IP1 to Linux. [Issue #2](https://github.com/jimthompson5802/agentic-ml/issues/2) now records that decision, with revised description and AC-01. The local story criterion, contributor design contract, plan, execution index, README and development guide agree. Prior macOS configuration results above are historical; local macOS test evidence remains valid for the unchanged seven shared commands.

T1: Selected `ubuntu-24.04`, confirmed against the [official Ubuntu 24.04 runner inventory](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md). Using an explicit image label avoids relying on `ubuntu-latest`. Actual hosted image/architecture/tool versions will be recorded in IP2. Existing immutable checkout/setup-uv revisions support the Linux hosted runner; Python 3.12/uv 0.13.1 choices remain unchanged.

T2: Workflow job is now **Linux / Python 3.12**, on `ubuntu-24.04`. Replaced macOS `sw_vers` with `cat /etc/os-release`. Bash, checksum capture/verification, permissions, events, independent-check conditions and all seven shared commands are unchanged. `/tmp/us32-ip1-tools/actionlint .github/workflows/ci.yml` passes with actionlint 1.7.12. Configuration inspection confirms the explicit Linux runner and absence of macOS-specific diagnostics. No suppressions or new executable harness behavior; appropriate verification is workflow validation and existing regression evidence. Hosted Linux execution cannot be verified on this macOS host and remains IP2 work.

T3: Development guide and README describe configured Linux CI and pending hosted verification while preserving macOS development status. Local Markdown file targets, exact shared command comparison, shell syntax and `git diff --check` pass. No fresh Python test run was needed: no Python source, tests, dependencies or shared command text changed. The original seven passing local checks remain applicable to macOS only. Lock hash remains `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`; tracked lock diff is empty.

T1–T3 complete for the revised configuration, IP1 gate pending renewed developer review. AC-01 now targets Linux PR/default-branch runs; all four criteria still require IP2 hosted evidence. No Linux execution, branch/PR publication, merge or IP1 approval is claimed.

## Developer approval

Developer approved IP1 including the Linux revision on 2026-10-29: “I approve IP1. Commit the Linux changes, push the branch, and create a PR to begin IP2.” Historical pending-gate statements above describe evidence preparation before this decision. IP2 entry and branch/PR publication are authorized; merge remains separately authorized.

## Final hosted follow-up

IP2 now verifies successful Linux PR and main push runs plus all six failure/correction cases; see [final IP2 evidence](us-32-ip2.md). Developer approved IP2 and accepted US-32 on 2026-10-29. Earlier pending-hosted statements in this report describe the IP1 checkpoint.
