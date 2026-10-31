# Install the harness in an experiment project

These instructions are for experiment users. The harness is installed into your project's own Python environment; you do not need a harness checkout or the contributor environment. Contributor setup is described separately in [the development guide](development.md).

The current development revision provides `agentic-ml --version`, Python imports and draft initialization scaffolding (see the preview below). The published revisions in the bootstrap examples predate that preview and provide provisional resources only. Environment/storage initialization, notebook execution and ML services remain subsequent work.

## Prerequisites

Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [uv](https://docs.astral.sh/uv/getting-started/installation/) using their official instructions for your operating system. For example, on macOS the Git guide describes installing the Xcode command line tools; the uv guide offers its standalone installer and Homebrew installation. Verify both tools are available:

```sh
git --version
uv --version
```

Use Python 3.12 for the initially verified path. If it is unavailable, `uv python install 3.12` installs it. Installation needs access to GitHub and the configured Python package index for isolated build dependencies. For private repository access, configure Git credentials using your organization's authentication method; keep credentials outside project configuration, URLs, Git history, and diagnostic reports.

The steps below were verified on macOS 15.7.9 arm64, Python 3.12.15, Git 2.54.0 and uv 0.13.1. Windows, other Python versions, and this installation workflow on Linux remain unverified. Existing Linux package CI evidence does not establish this workflow on Linux.

## Create a separate project and install an exact revision

Run these commands from a directory outside the harness checkout, choosing a new project directory:

```sh
mkdir my-experiment
cd my-experiment
git init
uv init --no-package --python 3.12
uv add "git+https://github.com/jimthompson5802/agentic-ml.git" --rev 018e9d4bb26e121c7f9274d11e0de560b7514b95
uv sync --locked
uv lock --check
uv run --locked agentic-ml --version
```

This example installs the verified Milestone 0 package at a full 40-character commit SHA, reporting `0.1.0`. For a different reviewed revision, replace the SHA with its complete commit ID. A branch, tag, or abbreviated hash is not the required pin. `--no-package` creates a minimal application project for this bootstrap; project-package scaffolding is introduced with initialization in US-02.

`uv add` declares `agentic-ml` in project dependencies and records the Git URL and requested revision in `[tool.uv.sources]` in `pyproject.toml`. The generated `uv.lock` records the resolved commit and dependency versions. uv builds a normal, noneditable harness installation in `.venv`; it may fetch source into its own cache during installation. The harness's development lockfile is not a substitute for this project's lockfile.

Check public imports, installed Git metadata, and packaged resources:

```sh
uv run --locked python -c 'import agentic_ml; print(agentic_ml.__file__)'
uv run --locked python -c 'from importlib.metadata import distribution; print(distribution("agentic-ml").read_text("direct_url.json"))'
uv run --locked python -c 'from importlib.resources import files; print(files("agentic_ml").joinpath("templates/provisional.txt").read_text(), end="")'
uv run --locked python -c 'from importlib.resources import files; print(files("agentic_ml").joinpath("runtime_guidance/provisional.md").read_text(), end="")'
```

The import path should be under the project's `.venv`. Installed metadata must identify the expected repository and full commit, with no editable flag. The two resources contain these respective lines, each followed by one newline:

```text
Provisional Milestone 0 template; experiment initialization is unavailable.
Provisional Milestone 0 runtime guidance; experiment execution is unavailable.
```

Review and commit the project files and lockfile. uv's generated ignore rules exclude `.venv`; keep credentials and generated data/storage outside Git.

```sh
git diff -- pyproject.toml uv.lock
git add pyproject.toml uv.lock .python-version README.md main.py .gitignore
git commit -m "chore: pin harness dependency"
```

For newly created untracked files, inspect their contents directly or review `git diff --cached` after staging. Git commit requires your configured author identity and any required signing setup.

## Environment identity and normal use

Keep the repository URL, full requested/resolved commit, installed package version, exact project lockfile, and Python/platform details with installation evidence. A package version such as `0.1.0` can be shared by different Git commits. Record the lockfile's SHA-256 when comparing environments; on macOS, run `shasum -a 256 uv.lock`. This installation evidence is the foundation for later run provenance, not a complete run manifest.

Use `uv sync --locked` and `uv run --locked ...` for normal synchronization and use. `--locked` fails when declarations and lock disagree rather than rewriting the lock silently. An intentional harness upgrade explicitly changes the full commit pin and experiment lockfile; follow the upgrade steps below.

Once `.venv` is installed, public imports/resources and the CLI work without the installer source cache or a harness checkout. For a no-sync offline invocation:

```sh
uv run --no-sync --offline agentic-ml --version
```

`--no-sync` uses the existing environment without validating it against changed declarations. This command demonstrates installed runtime independence; it does not replace locked synchronization. Initial installation, restoring a removed environment, and upgrades may require network access and cache repopulation. You do not need to clear your normal uv cache.

## Explicitly upgrade the harness

Choose a reviewed full commit SHA. From the experiment project initially pinned to the example revision above, this verified example upgrades to a later published commit:

```sh
uv add "git+https://github.com/jimthompson5802/agentic-ml.git" --rev aead26e9c758878107ad72f230f9e607a9a7ecfa
uv sync --locked
uv lock --check
uv run --locked agentic-ml --version
uv run --locked python -c 'from importlib.metadata import distribution; print(distribution("agentic-ml").read_text("direct_url.json"))'
shasum -a 256 uv.lock
git diff -- pyproject.toml uv.lock
```

`uv add` intentionally updates the experiment declaration, resolves the new commit and updates the experiment lockfile/environment. Review the full source revision in `pyproject.toml`, the resolved revision in `uv.lock`, and the installed `direct_url.json` commit. Repeat the import/resource commands above. Commit the reviewed metadata together:

```sh
git add pyproject.toml uv.lock
git diff --cached -- pyproject.toml uv.lock
git commit -m "chore: upgrade harness pin"
```

For these two example commits, the CLI reports `0.1.0` before and after upgrade. The full requested/resolved commit and lockfile SHA-256 change even though the package version is unchanged. A normal locked synchronization without a declaration change must preserve the lockfile and installation identity. Keep the original pin, lockfile and installation evidence with historical experiment records; upgrading the current project does not rewrite an earlier run's identity or establish compatibility with its preserved configuration/guidance.

The upgrade was verified on the same macOS/Python baseline as bootstrap. It does not require or update the harness contributor environment. An unavailable commit or failed update is a failure to investigate; inspect the declaration, lock and installed revision before accepting the new environment.

## Verification and troubleshooting

An unknown commit, unavailable GitHub access, or failed build is an installation failure. Do not treat a partially created `.venv` as verified. If locked synchronization reports a stale lock, inspect the declaration change and restore it or deliberately review and regenerate the experiment lockfile. Do not remove `--locked` simply to hide the failure. Preserve redacted error output for diagnosis.

Contributors can reproduce the installed-project acceptance check from the harness development environment:

```sh
uv run --locked python tests/installation/verify_installation.py --repository https://github.com/jimthompson5802/agentic-ml.git --revision 018e9d4bb26e121c7f9274d11e0de560b7514b95
```

The verifier prints a fresh temporary workspace and retains stage logs and `identity.json`. It creates a separate experiment project, uses a dedicated disposable cache and copy installation mode, installs and checks the pinned dependency, removes only its own cache, and probes installed CLI/imports/resources before an offline/no-sync CLI invocation. The copied stdlib probe runs under isolated Python outside the checkout. Ordinary pytest covers the verifier using local Git fixtures; the explicit command above supplies real GitHub installation evidence. See [US-01 IP1 evidence](verification/us-01-ip1.md).

To include stable-sync and explicit-upgrade verification in a fresh disposable project:

```sh
uv run --locked python tests/installation/verify_installation.py --repository https://github.com/jimthompson5802/agentic-ml.git --revision 018e9d4bb26e121c7f9274d11e0de560b7514b95 --upgrade-revision aead26e9c758878107ad72f230f9e607a9a7ecfa
```

The verifier preserves `identity-before-sync.json`, `pyproject-before-sync.toml`, `uv-before-sync.lock` and the original `identity.json`; upgraded metadata is recorded separately in `identity-after-upgrade.json`. A passing initial installation alone does not count as a passing upgrade. Review all three PASS stages and the original exit code. See [US-01 IP2 evidence](verification/us-01-ip2.md).

## Initialization preview (US-02 IP3)

The current development revision provides `uv run agentic-ml init` for draft project scaffolding and environment synchronization. After installing that exact reviewed revision as a full-SHA dependency, run it from the experiment Git root, or pass `--project-root /absolute/project`. Use `--experiment NAME` and `--package-name IDENTIFIER` to select names; an existing src package requires explicit selection.

This intermediate implementation creates draft configuration, a brief, search/execution inputs, four inert notebooks, project-package build scaffolding and ignore rules. It declares NumPy, pandas, scikit-learn, nbclient, ipykernel, nbformat, DVC and MLflow in the experiment project, resolves its lock and synchronizes `.venv`. Existing requirement bounds remain and intersect the required ranges; unrelated installed packages are retained during setup. The harness full-SHA source stays pinned. It reports **storage setup pending**: DVC, MLflow and durable-state provisioning remain US-02 IP4 work. This preview does not satisfy the complete initialization story. Review and commit the deliberately updated experiment metadata and lock together.

Review generated files before use. Resolve reported conflicts without deleting your work; reruns preserve compatible edited drafts. The private, ignored `.agentic-ml/init.json` and metadata backups record setup progress for interrupted scaffolding and synchronization. A uv failure reports its stage and exit code without echoing potentially credential-bearing tool output. Resolve the underlying tool failure and rerun with the same options and unchanged intermediate metadata. Changes after a failed setup require review; init will not restore stale backups automatically. A setup record grants no data access, agent authentication or execution approval. Source notebooks, configuration and project code remain ordinary reviewable Git files.
