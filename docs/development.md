# Harness development

Contributor instructions apply to the harness checkout. Experiment runtime guidance ships separately as package resources. Use Python 3.12 or newer with the committed uv lockfile. Dependency changes require an intentional lock update and review; verification must not silently regenerate it.

## Task reading map

Read this core guide before Python changes. Read each applicable reference before performing its task; additional references are mandatory when their triggers apply.

| Task | Required reference |
|---|---|
| Create or repair a contributor environment | [Setup](development/setup.md) |
| Plan verification, conduct TDD, run tests, or prepare an approval gate | [Verification](development/verification.md) |
| Read GitHub or troubleshoot command approvals | [Command approvals](development/command-approvals.md) |
| Inspect, modify or troubleshoot CI | [CI](development/ci.md) |
| Change packaging, dependencies, packaged resources or installation; verify artifacts | [Distribution](development/distribution.md) |
| Plan, collect, retain or clean development evidence | [Records](development/records.md) |

## Prerequisites and platform status

See [Prerequisites and platform status](development/setup.md#prerequisites-and-platform-status).

## Clone and install the development environment

See [Clone and install the development environment](development/setup.md#clone-and-install-the-development-environment).

## Shared development commands

The US-33 CLI slice supplies source, a console entrypoint, and behavior tests. Use the following commands from the repository root for local verification. Development CI uses the same checks, including four-worker pytest execution with `loadgroup`.

| Purpose | Command |
|---|---|
| Install source package and development dependencies | `uv sync --locked --group dev` |
| Lock consistency | `uv lock --check` |
| Phase tests (local, four workers) | `uv run --locked pytest -n 4 --dist=loadgroup` |
| Complete suite (story and milestone acceptance) | `uv run --locked pytest -n 4 --dist=loadgroup -m ""` |
| Lint | `uv run --locked ruff check .` |
| Formatting check | `uv run --locked ruff format --check .` |
| Strict type checks | `uv run --locked mypy src tests` |
| Development smoke check | `uv run --locked agentic-ml --version` |

The smoke check must exit zero and print the installed package version; version tests compare it to distribution metadata. A missing command, nonzero exit, or wrong version is a failed smoke check. US-31 Implementation Phase 2 verified all shared commands from a fresh macOS checkout and a new environment; see the [recorded results](verification/us-31-ip2.md). Wheel/source-distribution verification belongs to US-33 and is separate from this editable development install.


## Verification schedule

See [Verification schedule](development/verification.md#verification-schedule).

## Local parallel test execution

See [Local parallel test execution](development/verification.md#local-parallel-test-execution).

## Phase and story verification

See [Phase and story verification](development/verification.md#phase-and-story-verification).

## Configuration, credentials, and troubleshooting

See [Configuration, credentials, and troubleshooting](development/setup.md#configuration-credentials-and-troubleshooting).

## Repository-local Codex command approvals

See [Repository-local Codex command approvals](development/command-approvals.md#repository-local-codex-command-approvals).

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

Temporary pytest skips authorized by the developer on 2026-11-03 apply only to
`test_failed_installed_probe_retains_available_environment` in
`tests/integration/test_installation_verification.py` and
`test_missing_planning_schema_fails_installed_inventory` and
`test_rebuilt_probe_failure_retains_both_environments` in
`tests/integration/test_distribution_verification.py`. Each exceeded its
120-second subprocess timeout in the Linux full-suite run and passed on the
selected retry; the cause remains unresolved. Remove these skips when the
timeout cause is resolved or the developer directs re-enablement. Assertions
and timeouts remain unchanged. Skipped coverage does not satisfy the existing
story or milestone verification obligations.


## Development CI and diagnostic logs

See [Development CI and diagnostic logs](development/ci.md#development-ci-and-diagnostic-logs).

## Retained development records

See [Retained development records](development/records.md#retained-development-records).

## Distribution builds and installed verification

See [Distribution builds and installed verification](development/distribution.md#distribution-builds-and-installed-verification).
