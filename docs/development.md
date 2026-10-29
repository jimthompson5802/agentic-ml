# Harness development

This guide applies to harness contributors. Experiment runtime instructions will ship separately as package resources. US-31 IP1 establishes development tooling; the US-33 prerequisite slice now supplies the minimal package and version CLI. See [CLI verification](verification/cli-name-correction.md).

## Prerequisites and platform status

Use Git, `uv`, Python 3.12 or newer, a shell, and network access to GitHub and the Python package index. Install uv using its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Install Python 3.12 yourself or use `uv python install 3.12`. The committed `.python-version` selects the 3.12 baseline; `pyproject.toml` requires Python >=3.12. Exact development dependency resolutions are in `uv.lock`.

macOS is the initial development platform. Tooling was checked on macOS 15.7.9 arm64 with Python 3.12.15 and uv 0.13.1; see [implementation-phase evidence](verification/us-31-ip1.md). This is tooling verification, not the pending fresh-checkout verification. CI has not been established: no Python version is currently verified by CI. US-32 will verify Python 3.12 and record actual CI results. Other Python versions, Linux, and Windows remain unverified. Commands below use POSIX shell syntax; Windows shell/path handling will need verification. This initial foundation needs neither GPU tooling nor ML system services.

## Clone and install the development environment

```sh
git clone https://github.com/jimthompson5802/agentic-ml.git
cd agentic-ml
uv sync --locked --group dev
uv lock --check
```

When reviewing an implementation branch, check out the reviewed branch or commit before synchronization. The package installs from this checkout in editable mode. For tooling-only work before product source exists, `uv sync --locked --group dev --no-install-project` installs dependencies without building the project; this was the US-31 IP1 bootstrap path. There are currently no third-party runtime dependencies. Keep `uv.lock` committed. `--locked` must reject stale metadata rather than silently regenerate the lockfile. Deliberate dependency changes require `uv lock`, review of the lock diff, and renewed verification.

Bootstrap commands available now:

```sh
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pytest --version
uv run --no-sync mypy --version
```

`--no-sync` uses the environment synchronized above. It does not validate a changed lockfile; rerun locked synchronization after dependency changes. Version commands confirm tool availability, not application test coverage. The source and tests now exist; use the complete shared checks below for product verification.

## Shared development commands

The US-33 CLI slice supplies source, a console entrypoint, and behavior tests. Use the following commands from the repository root; these will also be the commands consumed by US-32 CI:

| Purpose | Command |
|---|---|
| Install source package and development dependencies | `uv sync --locked --group dev` |
| Automated tests | `uv run --locked pytest` |
| Lint | `uv run --locked ruff check .` |
| Formatting check | `uv run --locked ruff format --check .` |
| Strict type checks | `uv run --locked mypy src tests` |
| Development smoke check | `uv run --locked agentic-ml --version` |

The smoke check must exit zero and print the installed package version; version tests compare it to distribution metadata. A missing command, nonzero exit, or wrong version is a failed smoke check. US-31 Implementation Phase 2 will verify all shared commands from a fresh macOS checkout and a new environment. Wheel/source-distribution verification belongs to US-33 and is separate from this editable development install.

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
