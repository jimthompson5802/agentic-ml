# Contributor setup

## Prerequisites and platform status

Use Git, `uv`, Python 3.12 or newer, a shell, and network access to GitHub and the Python package index. Install uv using its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Install Python 3.12 yourself or use `uv python install 3.12`. The committed `.python-version` selects the 3.12 baseline; `pyproject.toml` requires Python >=3.12. Exact development dependency resolutions are in `uv.lock`.

macOS is the initial development platform. Fresh-checkout setup and all documented development checks were verified on macOS 15.7.9 arm64 with Python 3.12.15 and uv 0.13.1; see [fresh-checkout evidence](../verification/us-31-ip2.md). Earlier tool enforcement evidence is in the [IP1 report](../verification/us-31-ip1.md). The development CI workflow is configured for Linux (Ubuntu 24.04) and Python 3.12; a hosted PR run passed on Ubuntu 24.04.5 x86_64 with Python 3.12.15 and uv 0.13.1; see [IP2 evidence](../verification/us-32-ip2.md). Six hosted failure/correction cases are verified; the [default-branch push run passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). Other Python versions and Windows remain unverified. Commands below use POSIX shell syntax; Windows shell/path handling will need verification. This initial foundation needs neither GPU tooling nor ML system services.


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


## Configuration, credentials, and troubleshooting

Tool configuration lives in `pyproject.toml`. Defaults are repository-local `.venv`, pytest discovery beneath `tests`, and Python 3.12 analysis. No `.env`, application configuration, service accounts, MLflow/DVC storage, model credentials, or agent adapter is required for development tooling or the minimal version CLI. Cloning requires repository access; private access requires your own GitHub authentication. Dependency synchronization requires package-index access. Use your organization's documented proxy/index configuration if necessary; never put tokens in committed configuration or logs.

If Python 3.12 is unavailable, install it before synchronization. If locked synchronization reports stale metadata, review the change and update the lock only as an intentional dependency change; do not remove `--locked` to hide the problem. If tools are missing after using `--no-sync`, repeat the documented bootstrap synchronization. When working on a historical revision before package source exists, use the tooling-only bootstrap synchronization above. Keep diagnostic logs outside Git and redact credentials before including evidence.

