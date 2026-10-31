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

When reviewing an implementation branch, check out the reviewed branch or commit before synchronization. If that commit is not yet pushed, Git can fetch it from a local harness clone: run `git fetch /absolute/path/to/harness REVIEWED_COMMIT_SHA`, then `git checkout --detach REVIEWED_COMMIT_SHA` before synchronization; replace the path and SHA with the reviewed source. This changes only how Git obtains the reviewed revision, not the Python setup steps. The package installs from this checkout in editable mode. For tooling-only work before product source exists, `uv sync --locked --group dev --no-install-project` installs dependencies without building the project; this was the US-31 IP1 bootstrap path. US-02 IP2 adds tomlkit, PyYAML and jsonschema as runtime dependencies for initialization metadata/resources. US-02 IP3 adds nbclient, ipykernel, nbformat, DVC and MLflow runtime requirements; experiment initialization declares its own ML/notebook/storage requirements and synchronizes the separate project environment. IP4 provisions project-associated local DVC, MLflow and initial durable state. Keep `uv.lock` committed. `--locked` must reject stale metadata rather than silently regenerate the lockfile. Deliberate dependency changes require `uv lock`, review of the lock diff, and renewed verification.

Bootstrap commands available now:

```sh
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pytest --version
uv run --no-sync mypy --version
```

`--no-sync` uses the environment synchronized above. It does not validate a changed lockfile; rerun locked synchronization after dependency changes. Version commands confirm tool availability, not application test coverage. The source and tests now exist; use the complete shared checks below for product verification.

## Shared development commands

The US-33 CLI slice supplies source, a console entrypoint, and behavior tests. Use the following commands from the repository root for local verification. Development CI uses the same checks but runs pytest serially.

| Purpose | Command |
|---|---|
| Install source package and development dependencies | `uv sync --locked --group dev` |
| Lock consistency | `uv lock --check` |
| Automated tests (local, four workers) | `uv run --locked pytest -n 4 --dist=loadgroup` |
| Lint | `uv run --locked ruff check .` |
| Formatting check | `uv run --locked ruff format --check .` |
| Strict type checks | `uv run --locked mypy src tests` |
| Development smoke check | `uv run --locked agentic-ml --version` |

The smoke check must exit zero and print the installed package version; version tests compare it to distribution metadata. A missing command, nonzero exit, or wrong version is a failed smoke check. US-31 Implementation Phase 2 verified all shared commands from a fresh macOS checkout and a new environment; see the [recorded results](verification/us-31-ip2.md). Wheel/source-distribution verification belongs to US-33 and is separate from this editable development install.

## Local parallel test execution

Agents must use four workers with `loadgroup` for local pytest verification,
including complete-suite runs and selected tests. After locked development
synchronization, use:

```sh
uv run --locked pytest -n 4 --dist=loadgroup
uv run --locked pytest -n 4 --dist=loadgroup --junitxml=/private/tmp/agentic-ml-parallel.xml --durations=20
```

For serial diagnosis or a short focused TDD cycle, use `uv run --locked pytest`
with the relevant selector and record why serial execution was selected.
Use two workers only for an explicit comparison or resource investigation.
Pytest configuration does not add worker flags automatically; CI continues to
invoke the serial command.

`pytest-xdist` is a development dependency. Pytest is constrained to `>=8,<9.2`
because pytest 9.2.0 silently breaks group scheduling with pytest-xdist 3.8.0.
The public subprocess regression in `test_parallel_execution.py` verifies that
marked cases share a worker. Revisit the upper bound after an upstream-compatible
pair passes that regression and complete-suite verification.

`loadgroup` keeps the installation
tests in one worker and the distribution tests in another scheduling group;
each group runs sequentially, but a worker can run other tests afterward.
Initialization and CLI cases are ungrouped and can run individually on available
workers. Grouping does not guarantee test order. Use `loadgroup` with these
commands so shared mutable installation fixtures stay together and expensive
distribution fixtures are reused. Avoid `loadfile`/`loadscope`: they place the
entire initialization module on one worker.

Each worker creates its own module fixtures. Experiment projects, source Git
fixtures, databases, storage and artifact directories use pytest temporary paths
or independently allocated temporary workspaces. Installation probes intentionally
mutate their group-local installed project and restore its contents. Cache-removal
checks remove only their own workspace cache. Keep those isolation properties
when adding tests. Do not point multiple runs at the same `--basetemp` directory.

Environment installation and MLflow initialization compete for CPU, memory and
disk. Investigate resource constraints with a recorded worker-count comparison. Keep
existing assertions and subprocess timeouts intact. Record worker count, suite
count, durations, diagnostics and platform with results. A complete unfiltered
parallel run exercises the full suite; selected runs do not replace final full
verification. Retain serial execution for diagnosis. Parallel macOS evidence
does not establish Linux or Windows support; CI remains serial until separately
validated and authorized to change.

The initial verified macOS benchmark passed 129 tests in 16m59s with two workers
and 12m06s with four. Four workers reduced elapsed time by about 29%, while some
individual tests took longer under contention. These measurements are not a
Linux performance claim. See [parallel verification](verification/parallel-test-execution.md)
for grouping checks, compatibility findings, commands and retained evidence.

## Phase and story verification

This policy applies to new implementation plans. Existing approved plans keep their recorded verification requirements until an explicit revision is authorized and recorded through [manage-plan-scope](../.agents/skills/manage-plan-scope/SKILL.md). Preserve historical results and approvals. CI continues to run its complete configured checks; local test selection does not change CI configuration.

### Development and intermediate phase gates

Use TDD for each new behavior or bug fix: reproduce the missing behavior, implement the correction, and run the new test plus relevant existing regressions. At each phase gate, verify the changed behavior and its dependent capabilities. Select tests by affected interfaces, callers, shared resources and failure boundaries, including installed-package integration tests where those boundaries are affected. Test duration alone is not a reason to defer a relevant test. Broaden selection when the impact is uncertain.

Record the following in each phase's verification section before implementation:

- Selected test files, node IDs or selectors, the acceptance criteria they cover, and why they cover the affected behavior and dependencies.
- Public test boundaries and their limits, confirmed through plan review or an explicit review; reuse confirmed boundaries while applicable.
- Unrelated checks deferred to final verification, the reason, and the final phase/task that owns them. Write `None` when none are deferred.
- Conditions that would require broader verification as the work changes.

Use the documented locked pytest command with explicit paths, node IDs or `-k` selectors. For example, these are valid targeted commands; the plan must justify the selection for its actual change:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_cli_version.py
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_initialization.py -k 'storage_cannot_overlap or unsafe_backup'
```

Confirm that the intended cases were collected and report selected/deselected counts. Selection defers unrelated coverage; it is not a passing result for deselected tests. Keep tests enabled and assertions unchanged. A known failing regression remains unresolved and cannot be hidden by narrowing the selection.

At every executable phase gate, run locked development synchronization, lock consistency, lint, formatting, strict typing and the version smoke check from the shared command table, plus `git diff --check`. Compare the lockfile hash before and after verification and explain any intentional dependency change. Complete these checks and the phase's selected tests before requesting approval. Phase approval covers the recorded verified scope; whole-story regression coverage remains pending until final verification.

Run the full suite before an intermediate phase gate when changes affect dependency declarations or the lockfile, packaging/build/resource discovery, shared public schemas, or authorization/access enforcement across entrypoints. Include applicable distribution and installation checks for those changes. Also run broader tests, up to the full suite, when shared-module changes have uncertain impact or targeted results expose cross-capability regressions. These triggers take precedence over a previously narrower selection; record the expanded checks and results in the phase evidence.

### Final verification before story acceptance

Every new plan must assign final verification to a named task in its last implementation phase. After all implementation work is complete, run `uv run --locked pytest -n 4 --dist=loadgroup` locally across the complete repository suite without selection filters, together with the shared development checks. For distribution-affecting work, verify both the directly built wheel and a wheel rebuilt from the source distribution outside the checkout, using the [distribution and installation commands](#distribution-builds-and-installed-verification). Include other story-required installed-interface, manual and platform checks. A passing complete-suite run may supply these results when it demonstrably executes the required checks; reference that evidence instead of repeating identical checks against unchanged artifacts.

Record the tested revision and working-tree changes, lockfile identity, commands, test counts, outcomes, artifact identities where applicable, platform and limitations. Reconcile all deferred checks and the acceptance-criterion matrix. Present the final phase gate only after required verification passes; request whole-story acceptance only after the gates and final verification are complete. Failing or unverified required checks remain blockers.

After subsequent executable changes, rerun affected checks and renew the full-suite result against the final implementation before acceptance. Renew distribution evidence when package contents, dependencies or build inputs change. Reuse earlier evidence only when the relevant implementation and inputs are unchanged. Documentation-only or approval-record edits need appropriate document/link/whitespace checks rather than a runtime rerun; explain that choice in the evidence. For an entirely documentation-only story, record why product tests and distribution checks are inapplicable and name its required document checks.

## Configuration, credentials, and troubleshooting

Tool configuration lives in `pyproject.toml`. Defaults are repository-local `.venv`, pytest discovery beneath `tests`, and Python 3.12 analysis. No `.env`, application configuration, service accounts, MLflow/DVC storage, model credentials, or agent adapter is required for development tooling or the minimal version CLI. Cloning requires repository access; private access requires your own GitHub authentication. Dependency synchronization requires package-index access. Use your organization's documented proxy/index configuration if necessary; never put tokens in committed configuration or logs.

If Python 3.12 is unavailable, install it before synchronization. If locked synchronization reports stale metadata, review the change and update the lock only as an intentional dependency change; do not remove `--locked` to hide the problem. If tools are missing after using `--no-sync`, repeat the documented bootstrap synchronization. When working on a historical revision before package source exists, use the tooling-only bootstrap synchronization above. Keep diagnostic logs outside Git and redact credentials before including evidence.

## Repository-local Codex command approvals

The trusted project layer loads [command rules](../.codex/rules/default.rules) for this repository. Restart Codex after changing these rules. They allow the shared locked test, type, lint, formatting and smoke commands above, plus the distribution and installation verification drivers. Ruff formatting edits and `ruff check --fix` are included. Existing bootstrap allowances remain available.

For automatic GitHub read approvals, place the repository argument immediately after the subcommand:

```sh
gh pr view --repo jimthompson5802/agentic-ml 44
gh issue list --repo jimthompson5802/agentic-ml
sh .codex/scripts/github-read.sh issues/8/comments --paginate --slurp
sh .codex/scripts/github-read.sh pulls/44/files --jq '.[].filename'
```

Allowed GitHub subcommands are issue list/view; PR list/view/diff/checks; run, workflow and release list/view; and repository view. The [API helper](../.codex/scripts/github-read.sh) fixes github.com, the repository and GET. It accepts relative issues, pulls, actions/runs, actions/workflows, releases and commits endpoints, with optional `--paginate`, `--slurp` and `--jq EXPRESSION`. It rejects query strings, traversal, other hosts/repositories and arbitrary API options.

For complete issue retrieval, use the helper for issue metadata, every comment page, and the final metadata refresh. Omit `?per_page=100`; `--paginate --slurp` still retrieves all pages and returns an array of pages. Preserve the retrieval skill's unique-comment counts and snapshot checks. For PR review reads, use the helper for PR metadata, files, reviews and comments. Unsupported lookups, including labels, continue through normal tool approval without expanding the rules.

These are command-prefix permissions, not restrictions on every trailing argument, file access or subprocess. Tests execute trusted repository code outside the sandbox. Run commands directly: shell redirections or complex wrappers can still prompt. The new rules do not grant general Python, general `uv run`, dependency installation, Git writes or GitHub publication. User-level grants still apply and can be broader; project rules do not revoke them. Save these project allowances in the repository file rather than through TUI persistent approvals, which can write user-level rules.

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
gh pr checks --repo jimthompson5802/agentic-ml PR_NUMBER
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log-failed
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log
```

Reproduce failures locally from the same revision using the shared commands, Python 3.12 and uv 0.13.1. Compare `shasum -a 256 uv.lock` before and after, then run `git diff --exit-code -- uv.lock`. A passing local run does not establish hosted event delivery. The named **Build wheel and source distribution** and **Verify isolated installed distributions** steps use the distribution commands below verbatim. Verification runs only after a successful build; both steps can run despite an unrelated development check failure. Their original nonzero exits fail the job, and the final lock comparison still runs. Expand these steps for artifact hashes, both wheel results, retained workspace paths and subprocess diagnostics. The command output is available in the Actions log archive even after the temporary runner is destroyed; the workspace files themselves are not uploaded. Branch protection remains deferred US-34 work.

## Distribution builds and installed verification

From the repository root, build into a fresh output directory and verify both paths:

```sh
uv build --out-dir dist
uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir dist
uv run --locked python tests/installation/verify_initialization.py --artifacts-dir dist
```

Use an empty output directory for each reviewed build. If `dist` already contains artifacts from an earlier version, use a new directory in both commands. The driver requires exactly one wheel and one `.tar.gz` source distribution and rejects missing or ambiguous candidates. These same commands are configured in hosted CI. Both hosted wheel paths and separate build/resource failure-and-correction cases passed verification; see the [IP3 report](verification/us-33-ip3.md).

The driver creates a unique temporary workspace outside the checkout and prints its path. For each wheel it creates an unseeded Python 3.12 environment with `uv venv --no-project --python 3.12`, installs the wheel normally with `uv pip install --python ENV/bin/python WHEEL`, and probes it from a separate minimal experiment project. The probe uses isolated Python (`-I`) and an absolute installed `agentic-ml --version` entrypoint. It verifies CLI exit/stdout/stderr, wheel and installed version agreement, public imports, import/metadata paths, absence of editable installation and contributor dependencies, and independently specified resource contents. The Python 3.12 runtime closure is explicitly checked against the reviewed inventory in each standalone probe, including notebook, DVC and MLflow dependencies. Distribution-name normalization includes dots, underscores and hyphens. Platform-specific dependencies have explicit conditions; only observed platforms count as verified. Contributor tools and type stubs must remain absent. Future runtime dependency changes require reviewing this verification contract.

The second path validates source archive members, rejects links and traversal, and extracts with Python's `data` filter. It runs `uv build EXTRACTED_SOURCE --wheel --out-dir REBUILT_DIRECTORY` with build isolation, then installs that new wheel into another fresh environment. It never substitutes the direct wheel for the rebuilt wheel. Build dependencies remain separate from both runtime environments. Python path/home and active environment overrides are removed from child commands.

The initialization driver first runs those unchanged normal-wheel checks, then uses the validated source distribution to create a temporary full-SHA Git fixture. It compares every package file in both wheels with that source and each installed pinned Git package. Separate fresh CLI and existing-package API projects exercise complete initialization and reruns, including real stores, inert notebooks, imports, lock/pin preservation, Git exclusions and absent authorization. Wheel installs retain wheel origin; pinned-project installs retain Git origin. No origin metadata is fabricated, and unpublished fixture commits are local evidence. All workspaces and logs are retained outside the checkout. The ordinary pytest suite includes this driver; no additional CI service or editor is required.

Installed resources are read with `importlib.resources.files("agentic_ml")`:

| Resource | Exact UTF-8 content (followed by one newline) |
|---|---|
| `templates/provisional.txt` | `Provisional Milestone 0 template; experiment initialization is unavailable.` |
| `runtime_guidance/provisional.md` | `Provisional Milestone 0 runtime guidance; experiment execution is unavailable.` |

These provisional files remain packaging sentinels. US-02 IP2 adds separate `templates/initialization/` resources and versioned draft schemas; the installed probe verifies their inventory, schema properties and inert notebook content. Environment synchronization is implemented in IP3 and local storage initialization in IP4; runtime guidance selection/loading remains subsequent work. Development `AGENTS.md` files are not installed runtime resources.

Diagnostics include artifact paths/SHA-256, stage commands and working directories, interpreter/platform/import paths, installed distributions and CLI output. Every subprocess also writes stdout/stderr to a named stage `.log` in its working directory beneath the printed workspace. Workspaces are retained on success and failure for inspection; remove them manually when no longer needed. A failed installation/build/probe exits nonzero and identifies its stage and artifact. A failed later path never counts as passing because the direct wheel passed. Raw logs remain outside Git.

The ordinary `uv run --locked pytest` suite builds a small real artifact fixture and checks success plus malformed wheels (missing template, altered guidance, wrong CLI version), missing/ambiguous artifacts and corrupted source archives. Source-checkout CLI regressions remain separate. Verification currently uses POSIX `bin/python` and `bin/agentic-ml` paths; Windows remains unverified. See [US-33 IP2 evidence](verification/us-33-ip2.md) for actual local results; hosted Linux/Python 3.12 package results and failure diagnostics passed in the [IP3 report](verification/us-33-ip3.md). A default-branch package run remains post-merge follow-up.
