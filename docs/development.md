# Harness development

This guide applies to harness contributors. Experiment runtime instructions will ship separately as package resources. US-31 IP1 establishes development tooling; the US-33 prerequisite slice now supplies the minimal package and version CLI. See [CLI verification](verification/cli-name-correction.md).

## Prerequisites and platform status

Use Git, `uv`, Python 3.12 or newer, a shell, and network access to GitHub and the Python package index. Install uv using its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Install Python 3.12 yourself or use `uv python install 3.12`. The committed `.python-version` selects the 3.12 baseline; `pyproject.toml` requires Python >=3.12. Exact development dependency resolutions are in `uv.lock`.

macOS is the initial development platform. Fresh-checkout setup and all documented development checks were verified on macOS 15.7.9 arm64 with Python 3.12.15 and uv 0.13.1; see [fresh-checkout evidence](verification/us-31-ip2.md). Earlier tool enforcement evidence is in the [IP1 report](verification/us-31-ip1.md). The development CI workflow is configured for Linux (Ubuntu 24.04) and Python 3.12; a hosted PR run passed on Ubuntu 24.04.5 x86_64 with Python 3.12.15 and uv 0.13.1; see [IP2 evidence](verification/us-32-ip2.md). Six hosted failure/correction cases are verified; the [default-branch push run passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). Other Python versions and Windows remain unverified. Commands below use POSIX shell syntax; Windows shell/path handling will need verification. This initial foundation needs neither GPU tooling nor ML system services.

## Clone and install the development environment

```sh
git clone https://github.com/jimthompson5802/agentic-ml.git
cd agentic-ml
uv sync --locked --group dev
uv lock --check
```

When reviewing an implementation branch, check out the reviewed branch or commit before synchronization. If that commit is not yet pushed, Git can fetch it from a local harness clone: run `git fetch /absolute/path/to/harness REVIEWED_COMMIT_SHA`, then `git checkout --detach REVIEWED_COMMIT_SHA` before synchronization; replace the path and SHA with the reviewed source. This changes only how Git obtains the reviewed revision, not the Python setup steps. The package installs from this checkout in editable mode. For tooling-only work before product source exists, `uv sync --locked --group dev --no-install-project` installs dependencies without building the project; this was the US-31 IP1 bootstrap path. There are currently no third-party runtime dependencies. Keep `uv.lock` committed. `--locked` must reject stale metadata rather than silently regenerate the lockfile. Deliberate dependency changes require `uv lock`, review of the lock diff, and renewed verification.

Bootstrap commands available now:

```sh
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pytest --version
uv run --no-sync mypy --version
```

`--no-sync` uses the environment synchronized above. It does not validate a changed lockfile; rerun locked synchronization after dependency changes. Version commands confirm tool availability, not application test coverage. The source and tests now exist; use the complete shared checks below for product verification.

## Shared development commands

The US-33 CLI slice supplies source, a console entrypoint, and behavior tests. Use the following commands from the repository root; these are also the commands configured in development CI:

| Purpose | Command |
|---|---|
| Install source package and development dependencies | `uv sync --locked --group dev` |
| Lock consistency | `uv lock --check` |
| Automated tests | `uv run --locked pytest` |
| Lint | `uv run --locked ruff check .` |
| Formatting check | `uv run --locked ruff format --check .` |
| Strict type checks | `uv run --locked mypy src tests` |
| Development smoke check | `uv run --locked agentic-ml --version` |

The smoke check must exit zero and print the installed package version; version tests compare it to distribution metadata. A missing command, nonzero exit, or wrong version is a failed smoke check. US-31 Implementation Phase 2 verified all shared commands from a fresh macOS checkout and a new environment; see the [recorded results](verification/us-31-ip2.md). Wheel/source-distribution verification belongs to US-33 and is separate from this editable development install.

## Configuration, credentials, and troubleshooting

Tool configuration lives in `pyproject.toml`. Defaults are repository-local `.venv`, pytest discovery beneath `tests`, and Python 3.12 analysis. No `.env`, application configuration, service accounts, MLflow/DVC storage, model credentials, or agent adapter is required for development tooling or the minimal version CLI. Cloning requires repository access; private access requires your own GitHub authentication. Dependency synchronization requires package-index access. Use your organization's documented proxy/index configuration if necessary; never put tokens in committed configuration or logs.

If Python 3.12 is unavailable, install it before synchronization. If locked synchronization reports stale metadata, review the change and update the lock only as an intentional dependency change; do not remove `--locked` to hide the problem. If tools are missing after using `--no-sync`, repeat the documented bootstrap synchronization. When working on a historical revision before package source exists, use the tooling-only bootstrap synchronization above. Keep diagnostic logs outside Git and redact credentials before including evidence.

## Python conventions and enforcement

Use Python 3.12 syntax or later only when compatible with the 3.12 baseline. Use reusable product code under `src/agentic_ml` and public-interface tests under `tests`. Avoid source-path manipulation that conceals installation problems.

| Area | Convention | Automated enforcement / review |
|---|---|---|
| Naming | snake_case modules/functions/variables, PascalCase classes, UPPER_CASE constants | Ruff N checks supported names; module names and constant semantics require review |
| Typing | Annotate public functions and their returns, use specific types, avoid untyped escape paths | Strict mypy checks annotated and untyped definitions; reviewers assess meaningful domain types |
| Docstrings | Google-style module/class/public-function docstrings; describe inputs, outputs, raised errors where useful | Ruff D with Google convention checks presence/style; reviewers check accuracy and useful contract detail |
| Imports | Standard library, third-party, then local imports; remove unused imports | Ruff I sorting and F unused/undefined checks |
| Formatting | Ruff formatter, 88-column target | `ruff format --check`; formatter does not promise a hard limit for every string |
| Errors | Catch specific exceptions, preserve causes with `raise ... from ...`, provide useful context, never silently swallow errors | Ruff BLE001 rejects blind exception catches and B checks supported bug patterns; reviewers check context, chaining and semantics |

Ruff also checks E4/E7/E9 syntax/style errors. Tool checks enforce only their documented rule coverage; they do not replace behavior tests or code review. Format intentionally with `uv run --no-sync ruff format .` during bootstrap, or `uv run --locked ruff format .` after the package exists, then rerun check commands.

## Suppressions and check exclusions

Prefer correcting code or configuration over adding an exception. An exception is acceptable only for a specific documented limitation or intentional behavior that the rule cannot represent. Use the narrowest rule and location, add a nearby reason, and add an entry below with rule/tool, file or pattern, rationale, affected scope, and removal condition. The same policy applies to `noqa`, `type: ignore`, per-file ignores, test skips/xfails, and checker exclusions. Reviewers must assess each justification. Never use blanket suppressions, disable failing tests, or weaken assertions to conceal a failure. Repository instructions require explicit developer direction for a workaround or suppression of an existing verification failure.

### Exception register

No source-rule suppressions or custom checker exclusions exist. Tools retain their default generated-directory exclusions; `.gitignore` excludes reproducible environments/caches/build products, local secrets and generated runtime state because those are not maintained source. Review reports in `docs/verification/` remain tracked; raw diagnostic `*.log` files stay local to avoid accidental sensitive-output commits. Add future exceptions here and beside the affected code/configuration.

## Development CI and diagnostic logs

[Development CI](../.github/workflows/ci.yml) runs on pull requests and pushes to `main`, without path filters. It selects `ubuntu-24.04`, uv 0.13.1 and Python 3.12. Checkout and setup-uv actions use immutable commit revisions. Each hosted job checks out source, verifies that no virtual environment exists, installs Python, and creates the environment using locked synchronization. Dependency caching is disabled. Runner images and Python 3.12 patch releases can change; the job records the actual image, OS, architecture and tool versions. See [configuration and local evidence](verification/us-32-ip1.md); the hosted PR baseline and six failure/correction cases passed verification; the [default-branch push run also passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). See the [hosted evidence](verification/us-32-ip2.md).

The workflow runs the seven shared commands above verbatim, with a separate step for every check. After successful synchronization, independent checks still run when an earlier check fails. Original nonzero exits fail the job. If setup fails, dependent checks are skipped and setup logs explain the failure. A final step compares the lockfile SHA-256 and tracked diff even after a setup/check failure, provided the initial checksum was captured. No command may silently regenerate the lockfile.

On a pull request, open **Checks**, select **Linux / Python 3.12**, and expand the failed step. Alternatively, open **Actions → Development CI → run → job**. The **Set up job** log records the hosted runner image. Use the run menu's **Download log archive** option to save diagnostics; repository access and GitHub sign-in may be needed. GitHub documents [viewing and downloading logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).

With GitHub CLI, replace the placeholders below with the PR number and run ID:

```sh
gh pr checks PR_NUMBER --repo jimthompson5802/agentic-ml
gh run view RUN_ID --repo jimthompson5802/agentic-ml --log-failed
gh run view RUN_ID --repo jimthompson5802/agentic-ml --log
```

Reproduce failures locally from the same revision using the shared commands, Python 3.12 and uv 0.13.1. Compare `shasum -a 256 uv.lock` before and after, then run `git diff --exit-code -- uv.lock`. A passing local run does not establish hosted event delivery. Package builds and isolated installation checks remain US-33 work; branch protection remains deferred US-34 work.

## Distribution builds and installed verification

From the repository root, build into a fresh output directory and verify both paths:

```sh
uv build --out-dir dist
uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir dist
```

Use an empty output directory for each reviewed build. If `dist` already contains artifacts from an earlier version, use a new directory in both commands. The driver requires exactly one wheel and one `.tar.gz` source distribution and rejects missing or ambiguous candidates. These are local contributor checks; adding them to hosted CI is US-33 IP3 work.

The driver creates a unique temporary workspace outside the checkout and prints its path. For each wheel it creates an unseeded Python 3.12 environment with `uv venv --no-project --python 3.12`, installs the wheel normally with `uv pip install --python ENV/bin/python WHEEL`, and probes it from a separate minimal experiment project. The probe uses isolated Python (`-I`) and an absolute installed `agentic-ml --version` entrypoint. It verifies CLI exit/stdout/stderr, wheel and installed version agreement, public imports, import/metadata paths, absence of editable installation and contributor dependencies, and independently specified resource contents. Currently the runtime dependency closure is only `agentic-ml`; future runtime dependencies require updating that explicit verification contract.

The second path validates source archive members, rejects links and traversal, and extracts with Python's `data` filter. It runs `uv build EXTRACTED_SOURCE --wheel --out-dir REBUILT_DIRECTORY` with build isolation, then installs that new wheel into another fresh environment. It never substitutes the direct wheel for the rebuilt wheel. Build dependencies remain separate from both runtime environments. Python path/home and active environment overrides are removed from child commands.

Installed resources are read with `importlib.resources.files("agentic_ml")`:

| Resource | Exact UTF-8 content (followed by one newline) |
|---|---|
| `templates/provisional.txt` | `Provisional Milestone 0 template; experiment initialization is unavailable.` |
| `runtime_guidance/provisional.md` | `Provisional Milestone 0 runtime guidance; experiment execution is unavailable.` |

These provisional files do not implement initialization or guidance selection/loading. Development `AGENTS.md` files are not installed runtime resources.

Diagnostics include artifact paths/SHA-256, stage commands and working directories, interpreter/platform/import paths, installed distributions and CLI output. Every subprocess also writes stdout/stderr to a named stage `.log` in its working directory beneath the printed workspace. Workspaces are retained on success and failure for inspection; remove them manually when no longer needed. A failed installation/build/probe exits nonzero and identifies its stage and artifact. A failed later path never counts as passing because the direct wheel passed. Raw logs remain outside Git.

The ordinary `uv run --locked pytest` suite builds a small real artifact fixture and checks success plus malformed wheels (missing template, altered guidance, wrong CLI version), missing/ambiguous artifacts and corrupted source archives. Source-checkout CLI regressions remain separate. Verification currently uses POSIX `bin/python` and `bin/agentic-ml` paths; Windows remains unverified. See [US-33 IP2 evidence](verification/us-33-ip2.md) for actual local results; hosted package results remain IP3.
