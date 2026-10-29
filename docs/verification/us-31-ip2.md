# US-31 Implementation Phase 2 verification

Date: 2026-10-29. Source: [US-31 / issue #1](https://github.com/jimthompson5802/agentic-ml/issues/1). Owning tasks: US-31-IP2-T1–T3 in the [implementation plan](../plans/milestone-0-us-31.md). Developer authorized this implementation phase by “start the next phase” in this conversation. US-31 IP1 and US-33 IP1 prerequisite tasks and developer gates were verified complete/approved before starting.

## Requirements and boundaries

Refreshed the complete issue #1 body and all paginated comments before execution. It remains open with zero comments, no GitHub milestone object, and body-assigned Milestone 0. Repeated metadata retained zero comments and updated_at 2026-10-29T03:08:20Z. Its old CLI spelling is superseded by the developer's explicit correction, recorded in SC-01 and ADR-007; the verified CLI is agentic-ml. No other scope conflict or new decision was found.

Public boundaries remain the approved contributor commands and CLI/import subprocess tests. This implementation phase changes documentation and records verification, not executable behavior; TDD therefore does not require a new failing test. Existing behavior tests were run unchanged. No suppression, skipped check, changed assertion or workaround was added.

## Fresh-checkout method

Verified committed source revision `c9fbb758c9ee6a85974de0a30783199338ef80df` on macOS 15.7.9 (24G830), arm64. The working tree was clean before starting; no existing environment was copied.

Source preparation used only Git:

```sh
git clone https://github.com/jimthompson5802/agentic-ml.git /tmp/us31-ip2-5w99njqw/agentic-ml
cd /tmp/us31-ip2-5w99njqw/agentic-ml
git fetch /Users/jim/Desktop/genai/agentic-ml c9fbb758c9ee6a85974de0a30783199338ef80df
git checkout --detach c9fbb758c9ee6a85974de0a30783199338ef80df
```

All preparation commands exited zero. GitHub cloning succeeded; fetching from the original checkout supplied the exact locally reviewed commit without requiring a push. This is review-source preparation, as distinct from dependency setup. The guide's reviewed-revision instruction now gives the concrete local-fetch form for unpushed commits. No product/configuration/source files were copied or patched into the fresh clone, and no extra dependency setup was required.

The fresh clone resolved to `/private/tmp/us31-ip2-5w99njqw/agentic-ml`. It had no .venv and no tracked/untracked working changes before synchronization. Documented `uv sync --locked --group dev` created a new .venv and installed the source package plus 11 development dependencies. Existing host Python/uv installations and uv's dependency cache were available; this is a fresh checkout/environment on the same machine, not a new-machine or cold-cache claim. The diagnostic runner cleared inherited VIRTUAL_ENV, PYTHONPATH, PYTHONHOME and UV_PROJECT_ENVIRONMENT overrides for subprocesses, used the clone as cwd, and recorded command exits/output. It did not add runtime configuration, credentials, services or dependencies.

Host/tool versions: Git 2.54.0; uv 0.13.1; CPython 3.12.15; pytest 9.2.0; Ruff 0.17.3; mypy 1.20.2. All core commands and documented bootstrap/version checks below exited zero. Package import diagnostics resolve agentic_ml to this new clone, and installed distribution metadata reports 0.1.0.

## Acceptance-criterion review

| Criterion | Verification evidence | Technical result |
|---|---|---|
| US-31-AC-01 | Guide specifies Python >=3.12, Git/uv/shell/network prerequisites, actual macOS baseline and unverified versions/platforms; CI explicitly not established | Verified within local scope; no CI success claimed |
| US-31-AC-02 | GitHub clone plus exact reviewed source checkout; locked runtime/development synchronization creates fresh .venv | Passed |
| US-31-AC-03 | Fresh source-installed agentic-ml CLI and version subprocess regression | Passed |
| US-31-AC-04 | Documented pytest, Ruff lint/format and strict mypy commands all executed | Passed |
| US-31-AC-05 | Documented agentic-ml --version exits zero, reports 0.1.0 | Passed |
| US-31-AC-06 | Fresh setup uses documented local defaults without .env, service accounts, tracking/data services or agent configuration | Passed |
| US-31-AC-07 | Fresh macOS clone/new .venv, source/OS/tool identities and complete command/results below | Passed |
| US-31-AC-08 | Committed tool configuration and exact lock resolutions used; lock hash unchanged | Passed |
| US-31-AC-09 | [Guide](../development.md) maps naming, typing, docstrings, imports and errors to automated checks/manual review; [IP1 probes](us-31-ip1.md) exercised invalid and corrected examples; fresh shared checks pass | Passed |
| US-31-AC-10 | Guide defines narrow exceptions, nearby reasons and exception register; inspected source/tests/config for suppressions/exclusions; none added | Passed |

Technical verification is separate from final developer acceptance. All ten criteria have evidence; final US-31 IP2 approval and story acceptance remain pending.

## Command results from the fresh clone

### `sw_vers`

Exit: 0.

```text
ProductName:		macOS
ProductVersion:		15.7.9
BuildVersion:		24G830
```

### `uname -m`

Exit: 0.

```text
arm64
```

### `git --version`

Exit: 0.

```text
git version 2.54.0
```

### `uv --version`

Exit: 0.

```text
uv 0.13.1 (Homebrew 2026-10-14 aarch64-apple-darwin)
```

### `uv sync --locked --group dev`

Exit: 0.

```text
Using CPython 3.12.15 interpreter at: /opt/homebrew/opt/python@3.12/bin/python3.12
Creating virtual environment at: .venv
Resolved 13 packages in 3ms
   Building agentic-ml @ file:///private/tmp/us31-ip2-5w99njqw/agentic-ml
      Built agentic-ml @ file:///private/tmp/us31-ip2-5w99njqw/agentic-ml
Prepared 1 package in 617ms
Installed 12 packages in 131ms
 + agentic-ml==0.1.0 (from file:///private/tmp/us31-ip2-5w99njqw/agentic-ml)
 + iniconfig==2.3.1
 + librt==0.16.0
 + mypy==1.20.2
 + mypy-extensions==1.1.0
 + packaging==26.3
 + pathspec==1.1.1
 + pluggy==1.7.0
 + pygments==2.21.0
 + pytest==9.2.0
 + ruff==0.17.3
 + typing-extensions==4.16.0
```

### `uv lock --check`

Exit: 0.

```text
Resolved 13 packages in 3ms
```

### `uv run --locked pytest`

Exit: 0.

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.2.0, pluggy-1.7.0
rootdir: /private/tmp/us31-ip2-5w99njqw/agentic-ml
configfile: pyproject.toml
testpaths: tests
collected 3 items

tests/integration/test_cli_version.py ...                                [100%]

============================== 3 passed in 0.26s ===============================
```

### `uv run --locked ruff check .`

Exit: 0.

```text
All checks passed!
```

### `uv run --locked ruff format --check .`

Exit: 0.

```text
42 files already formatted
```

### `uv run --locked mypy src tests`

Exit: 0.

```text
Success: no issues found in 3 source files
```

### `uv run --locked agentic-ml --version`

Exit: 0.

```text
0.1.0
```

### `uv run --no-sync ruff check .`

Exit: 0.

```text
All checks passed!
```

### `uv run --no-sync ruff format --check .`

Exit: 0.

```text
42 files already formatted
```

### `uv run --no-sync pytest --version`

Exit: 0.

```text
pytest 9.2.0
```

### `uv run --no-sync mypy --version`

Exit: 0.

```text
mypy 1.20.2 (compiled: yes)
```

### `uv run --locked python --version`

Exit: 0.

```text
Python 3.12.15
```

### `uv run --locked ruff --version`

Exit: 0.

```text
ruff 0.17.3
```

### `uv run --locked python -c import agentic_ml; from importlib.metadata import version; print(agentic_ml.__file__); print(version("agentic-ml"))`

Exit: 0.

```text
/private/tmp/us31-ip2-5w99njqw/agentic-ml/src/agentic_ml/__init__.py
0.1.0
```

### `git diff --check`

Exit: 0.

```text

```

## Integrity and documentation review

uv.lock SHA-256 before and after every check: `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`. This matches the earlier implementation-phase evidence. `git status --porcelain` was empty after setup/checks; no source or lockfile changes were needed. A new .venv/pyvenv.cfg exists. Raw diagnostic JSON is temporarily retained at `/tmp/us31-ip2-5w99njqw/results.json`; the durable outputs are preserved above.

T1 finalizes README/guide verification status, exact setup/shared commands, troubleshooting, local defaults, platform/CI limits and local reviewed-commit selection. T2 completes fresh setup and checks. T3 reviews all criterion evidence and updates owning plan/index/checkpoint. The verified source revision already contains the executable package, tests, configurations, lockfile and working shared commands. Current changes only clarify source selection and record results; no executable behavior, check configuration or dependency changed after verification.

Final local documentation checks: Ruff formatting, git diff --check, and Markdown file-target validation passed. No failed setup or corrective attempt occurred during this implementation phase. The temporary clone is retained for review; no repository cleanup or push was performed.

## Remaining limitations and gate

CI remains US-32 work, so no Python version is claimed CI-verified. Other Python versions, Linux and Windows remain unverified. Wheel/sdist isolation, provisional resources and package verification in CI remain US-33 work; this evidence does not close that story or Milestone 0. Additional production experiment features are excluded.

Stop at the [US-31 IP2 final gate](../plans/milestone-0-us-31.md#us-31--implementation-phase-2-verify-documented-macos-setup-and-source-smoke-check). Developer approval/story acceptance are pending. Changes are uncommitted.

## Subsequent developer acceptance

Developer message “i approve us-31 ip2”, 2026-10-29, approved the final implementation gate following the explicit US-31 story-completion review. The [owning plan](../plans/milestone-0-us-31.md#us-31--implementation-phase-2-verify-documented-macos-setup-and-source-smoke-check) records final gate approval and story acceptance. Pending statements above describe the evidence-presentation state. No downstream story work is authorized by this acceptance.
