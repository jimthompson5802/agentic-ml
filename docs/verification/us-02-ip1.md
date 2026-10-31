# US-02 IP1: Initialization contracts

Status: technically complete; developer gate approved by “i approve ip1; commit changes and I authorize ip2” (2026-10-30). These are approved contracts, not implemented interfaces. No US-02 acceptance criterion is yet verified as delivered.

## Sources and execution evidence

- Developer approved the plan/test boundaries and authorized IP1 with “commit changes; i approve the plan, execute us-02 ip1”. Approved documentation committed as `3d69d0b`.
- Issue #9 complete body and all comment pages refreshed: open, zero comments, stable `updated_at=2026-10-31T01:15:38Z`. Body includes the approved notebook-editor scope decision. Prerequisite issue #8 is closed, zero comments, stable `updated_at=2026-10-30T10:42:22Z`; [owning plan](../plans/milestone-1-us-01.md) records accepted prerequisite and both approved gates.
- Inspected package metadata, version CLI, installation/probe drivers and [development guidance](../development.md). No initializer exists. Runtime dependencies remain empty.
- Observed macOS 15.7.9 arm64, Git 2.54.0, uv 0.13.1. Read `uv add --help`, `uv sync --help`, `uv lock --help`: deliberate lock generation and subsequent locked synchronization are distinct operations. No dependencies installed or resolved during this documentation phase. Python/library compatibility is a planned IP3 verification, not an observed result here.
- [uv dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) documents declarative dependencies and Git sources. Preserve the existing full-SHA source entry when adding requirements.
- [DVC init](https://doc.dvc.org/command-reference/init) and [remote add](https://doc.dvc.org/command-reference/remote/add) supply project metadata and local remote configuration. Use no force or no-SCM initialization.
- [MLflow client](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html) supplies public experiment operations. [MLflow metadata](https://pypi.org/project/mlflow/) and [DVC metadata](https://pypi.org/project/dvc/) were inspected; exact compatible versions must be locked and tested in IP3.
- [scikit-learn installation](https://scikit-learn.org/stable/install.html) describes environment/import checks. [nbclient](https://nbclient.readthedocs.io/en/latest/) supplies automated notebook execution. Primary documentation establishes API feasibility, not joint dependency/platform verification.

## T1 — Public interfaces, resources and schemas

### Invocation and results

CLI: `agentic-ml init [--project-root PATH] [--experiment NAME] [--package-name IDENTIFIER] [--dvc-store PATH] [--mlflow-backend PATH] [--artifact-store PATH] [--state-store PATH]`.

Default root is cwd, resolved once; require it to be the Git top-level directory and contain a valid `pyproject.toml` and `uv.lock`. Do not search upward silently. Explicit root works from an unrelated cwd. Reject bare Git repositories, workspaces, nested project metadata and a root containing the harness source/package itself. Existing Git worktrees are valid. No agent adapter or terminal interaction required.

Experiment default: `initial`; identifier matches `[a-z][a-z0-9-]*`. New package default: normalized project distribution name (hyphens to underscores); require a valid non-keyword Python identifier, otherwise require explicit `--package-name`. Never infer an arbitrary existing package. Existing package projects require explicit package name and an existing `src/<package>/__init__.py`; preserve build metadata and source. Minimal nonpackage uv projects receive a new package with Hatchling `>=1.27,<2`, version retained from project metadata, and explicit wheel package path. Existing contradictory build settings are conflicts, not conversion opportunities.

Public Python import: `from agentic_ml.initialization import InitOptions, InitResult, InitializationError, initialize_project`.

- `InitOptions`: frozen dataclass, fields `project_root: Path`, `experiment: str = "initial"`, `package_name: str | None = None`, `dvc_store: Path | None = None`, `mlflow_backend: Path | None = None`, `artifact_store: Path | None = None`, `state_store: Path | None = None`.
- `initialize_project(options: InitOptions) -> InitResult`: same validation, setup, errors and outcomes as CLI; no cwd/global tracking mutation.
- `InitResult`: frozen dataclass; `project_root: Path`, `created: tuple[str, ...]`, `updated: tuple[str, ...]`, `unchanged: tuple[str, ...]`, `setup_pending: tuple[str, ...]`. Paths are root-relative for project files and absolute for external stores; sorted within each collection. Successful creation and compatible rerun both succeed.
- `InitializationError`: public exception with `stage: str`, `conflicts: tuple[str, ...]`, `completed_steps: tuple[str, ...]`, `recovery: str`. Safe diagnostics omit secrets and external tool environment values. Preserve specific underlying causes.
- CLI prints a readable ordered summary and pending choices; exit 0 complete setup, 1 initialization/conflict/tool failure, 2 invalid command syntax. No JSON wire format or force option in this slice. `--version` remains unchanged.

During IP2 only the scaffold stage is available: result/CLI must explicitly report environment and storage setup pending. Full init success is required by IP4; this intermediate state is never acceptance evidence for complete US-02.

### Exact generated inventory

Packaged resources are loaded through `importlib.resources.files("agentic_ml")`; proposed `templates/initialization/` contains configuration, brief, ignore block, package and notebook templates plus JSON Schemas. Keep existing provisional guidance until its owning story replaces it; no runtime loader or development AGENTS.md copying.

| Destination | Content contract |
|---|---|
| `project.yaml` | Initialization schema below; project/environment, storage and explicit unset setup choices |
| `experiments/<name>/experiment.md` | Sections Data, Features, Evaluation, Algorithms, Budget; every experiment-specific choice marked `TODO`, no inferred dataset or approved choice |
| `experiments/<name>/search-space.yaml` | `schema_version: "0.1"`, `algorithms: {}`; empty draft boundary grants no algorithm use |
| `experiments/<name>/experiment.yaml` | `schema_version: "0.1"`, `id: <name>`, root-relative brief/search-space paths, list of four notebook paths, `working_directory: "."`, `data: []`, `execution: {status: unconfigured}` |
| `experiments/<name>/notebooks/01_data_assessment.ipynb` | Assessment guidance, parameter cell, inert example code |
| `.../02_features_and_baseline.ipynb` | Feature/baseline guidance, parameter cell, inert example code |
| `.../03_model_development.ipynb` | Modeling guidance, parameter cell, inert example code |
| `.../04_results.ipynb` | Results/review guidance, parameter cell, inert example code |
| `src/<package>/__init__.py` | Module docstring only for newly created package; existing file preserved |
| `.gitignore` | Append owned block described below; preserve existing bytes |
| `pyproject.toml`, `uv.lock` | Additive package/dependency configuration and deliberate experiment lock update |
| `.dvc/config`, `.dvc/.gitignore`, `.dvcignore` | DVC-managed initialization and local-store configuration |

All notebooks: nbformat 4/minor 5; Python 3 kernelspec (`python3`), language Python, explanatory Markdown; parameter code cell tagged `parameters` defines `project_config = "project.yaml"`, `experiment_config = "experiments/<name>/experiment.yaml"`, `run_id = None`. Other code cells contain comments only. All code execution counts null and outputs empty. No data reads, training, execution submission or synthetic result cells. The templates remain deliberate incomplete experiment inputs; US-03/05 will resolve/reject them before execution.

`project.yaml` initialization schema 0.1 fields: `schema_version`, `project: {package, environment: .venv}`, `storage: {dvc_store, mlflow_backend, artifacts, state}`, `setup: {data_access: unconfigured, agent: unconfigured, approval_presentation: unconfigured}`, `guidance: {}`, `components: {}`. All paths resolve against selected root, with `.` representing root; never serialize a machine-specific project root. No credentials, data source URLs, access grants or approved status. Store paths under root relatively and external paths absolutely.

Add JSON Schemas under `templates/initialization/schemas/` for project, draft experiment, search-space and initial state, plus corresponding frozen typed Python models under `initialization/models.py`. Validate initializer-produced fields/types and reject unknown initialization schema versions. Use `additionalProperties: false` for these minimal initialization shapes; empty components/guidance/algorithms are placeholders, not implementations of their future contracts. Semantic objective, component and search validation belongs to later stories. Schema expansion must be versioned rather than silently treating draft inputs as executable plans.

## T2 — Preservation, authority and failure protocol

Require an existing declared `agentic-ml` dependency and `[tool.uv.sources].agentic-ml` Git source with a full 40-hex SHA; reject branch/tag/path/editable sources and inconsistent lock revision. For local unpublished Git verification, a file Git URL is allowed and recorded as local evidence; normal bootstrap uses the settled GitHub URL. Installed metadata must match the selected project pin; prevent use of an unrelated project's environment. Never upgrade or replace that source. Snapshot original pyproject/lock bytes and compare source/dependency identity after resolution.

Preserve TOML comments/order with `tomlkit`; add missing dependency entries, package build sections and explicit package path only under the above rules. Existing compatible dependency specifiers are retained and intersected with required constraints during resolution; conflicting bounds produce an error, never a replacement. Preserve unrelated tool/index/source declarations. Resolve with the existing lock as preference, no upgrade flags. Appended ignore block has fixed markers and anchored rules for `/.venv/`, `/.agentic-ml/`, `/data/`, `/.env`, `/.env.*`, exceptions for `/.env.example`, and per-project configured internal store roots. Reject ignore negations that would expose these generated store roots rather than rewriting user patterns. Preserve DVC's own ignore files. Do not add patterns that hide briefs, notebooks, project code, locks or DVC metadata.

Before writes, validate all inputs, metadata, target paths and collisions; inspect parent paths without following symlinks. Reject symlink targets/parents for generated files and stores, path overlap with `.git`, `.venv`, source/config trees, and external store roots containing unrelated existing content. Store destinations must be distinct, with no ancestor overlap. Permission probes create/remove only a private temporary file in the selected existing parent after validation; never chmod user paths. A failed preflight makes no durable project change. External locations require explicit flags on first setup, not environment-variable discovery.

New target files may be absent, exact generated matches (no-op), or existing compatible project-package files explicitly selected above. A differing target file is a conflict. A completed rerun validates its saved inventory rather than overwriting edits: preserve edited user inputs and report them unchanged if schemas/paths still match project identity; incompatible config is a conflict. New experiment names on initialized projects are not supported by init: report conflict and retain all files. Different storage options require explicit future reconfiguration, not a rerun migration.

Use exclusive creation of root `.agentic-ml/init.lock` to reject concurrent initializers. Record PID/hostname but do not infer that a lock is stale automatically. Error instructs developer to confirm no live initializer before manually removing the lock. Do not use this setup lock as an execution/recovery lock. Recheck target identities immediately before writes; use atomic replacement for owned metadata after comparing original hashes. This protects cooperative setup operations, not hostile concurrent filesystem mutation or an execution sandbox.

Persistent `.agentic-ml/init.json` journal (schema 0.1) records options, original metadata backup references, planned paths/checksums, created paths, completed stage names and `status` (`incomplete`/`complete`). Stages: preflight → scaffold → lock → sync → DVC → MLflow → state → finalize. Restrict journal/backups to owner access and Git-ignore them. Backup only pyproject/lock/ignore metadata; never copy secrets or source data. Journal is setup progress, not provenance or authorization evidence. No claim of atomicity across uv/DVC/MLflow.

On failure preserve journal, original metadata backups and completed stores; report exact stage and safe retry command. Do not automatically delete user changes, restore stale backups, or claim setup success. Before retry require matching options and unchanged owned intermediate files/metadata hashes; changed user data blocks automatic retry for review. Re-run idempotent stages after interrupted acknowledgements, checking DVC settings and MLflow experiment identity before creating anything. Never log raw subprocess output that may contain credentials; retain only redacted diagnostics and exit code. No automatic dependency retry loop.

Setup choices remain visibly unconfigured. No prompt asks for tokens. Init neither reads raw data nor starts kernels, notebooks, agent logins, tracking runs or experiment approvals. Explicit setup writes authorize only the selected project/store destinations. Kernel/assistant isolation and developer-authenticated approvals remain pending downstream mechanisms; initialization is not evidence of their enforcement.

## T3 — Dependency and uv contract

These are chosen requirement ranges, not versions proven installed in IP1. IP3 must lock actual compatible releases, record versions and test on Python 3.12; resolution failure is a visible failure, not grounds to relax checks silently.

| Owner | Required declarations | Reason |
|---|---|---|
| Harness runtime | `tomlkit>=0.13,<1`, `PyYAML>=6,<7`, `jsonschema>=4,<5` | Lossless TOML editing, YAML and schema validation |
| Harness runtime | `nbclient>=0.10,<1`, `ipykernel>=6,<8`, `nbformat>=5,<6` | Design's notebook execution dependency contract and template validation |
| Harness runtime | `dvc>=3,<4`, `mlflow>=3,<4` | Initializer invokes DVC in the project environment and public MLflow APIs; use local dependencies only, no cloud extras |
| Experiment direct dependencies | `numpy>=2,<3`, `pandas>=2,<4`, `scikit-learn>=1.6,<2`, `nbclient>=0.10,<1`, `ipykernel>=6,<8`, `nbformat>=5,<6`, `dvc>=3,<4`, `mlflow>=3,<4` | Explicit project-owned ML, notebook and storage tool declarations |

Initial ML setup is CPU tabular scikit-learn; LightGBM/PyTorch training dependencies belong to their later framework story, not silently installed now. This is a milestone-scoped initialization choice; no removal of later framework requirements. Editor and extensions are installed separately. No editor package in either dependency set. Existing user packages remain installed: use inexact sync for setup.

Run subprocesses with an argument list, cwd selected root, selected project uv executable, no shell interpolation. Ignore inherited `UV_PROJECT_ENVIRONMENT`/active-venv overrides; use root `.venv`. Preserve configured nonsecret package index choices without copying credentials to files/logs. Write approved additive metadata, then `uv lock --project ROOT` (intentional experiment lock change), verify pinned source/SHA, then `uv sync --locked --inexact --project ROOT`, `uv lock --check --project ROOT`. Do not use `uv add` to rewrite existing specifiers or upgrade flags. Reject changed pin before synchronization. Installed public postcondition probes run in a separate interpreter; syncing dependencies during the initializer must not rely on importing freshly installed packages into its already-running process.

IP2 installs only its newly required parser/schema libraries in the harness; IP3 introduces the remaining selected runtime closure and experiment declarations. Record deliberate harness lock changes in their owning phase; IP1 does not edit either lockfile. Package probes must replace the old one-distribution assumption with required declared runtime closure checks, still excluding contributor tools and editable harness installation. A project package may use uv's normal editable project install; the harness itself must remain noneditable.

## T4 — Storage and state contract

Defaults under the root: DVC cache `.dvc/cache`, DVC local remote `.agentic-ml/dvc-store`, MLflow SQLite backend `.agentic-ml/mlflow.db`, artifact root `.agentic-ml/artifacts`, state directory `.agentic-ml/state`. SQLite database URI is constructed from the resolved local path by the implementation, not accepted as arbitrary user URI. Four store flags override the named paths; DVC cache stays under `.dvc`. Relative flags resolve against project root. This slice configures local paths, including explicit external filesystem paths; remote service deployment/authentication is not introduced. Reject URI schemes and credential-bearing values before logging.

DVC: `uv run --locked --no-sync --project ROOT dvc init` for a new repo, then `... dvc remote add --default agentic-ml-store PATH`. Preserve existing DVC setup: accept a matching default remote; add only when no default is configured; conflicting defaults or remote names fail preflight. Do not add data, run pipelines or push content. Probe with public `dvc root`, `dvc remote list`, `dvc config cache.dir` (unset means default), plus directory write/read probe. Disable DVC analytics in initializer child environment.

MLflow: create parent/artifact directories and use `MlflowClient(tracking_uri=<absolute sqlite URI>)`. Create experiment `agentic-ml:<experiment>` with the explicit file artifact URI, or reuse it only if artifact location matches. `get_experiment_by_name` verifies its identity; no tracking run is created. Let supported MLflow APIs initialize its database, not handwritten MLflow SQL. New external DB must not already be an unrelated file; existing initialized project reruns reuse only the recorded DB and compatible experiment identity. Never auto-migrate an existing unrelated store.

Durable state is a schema-versioned JSON file `state/project.json` with `schema_version: "0.1"`, experiment name, `status: "unconfigured"`, `approvals: []`, `runs: []`; write atomically, reopen and validate. Existing differing state is a conflict, never truncated. This initializes durable storage without inventing a complete workflow state machine/recovery schema. Approval, task, run and recovery records are downstream capabilities.

## Refined implementation and verification map

| Owning task | Concrete components and independent expected outcomes |
|---|---|
| IP2-T1/T3 | `src/agentic_ml/initialization/__init__.py`, `models.py`, `scaffold.py`; existing CLI dispatch; packaged initialization resources/schemas. Independently assert generated inventory, fixed minimal YAML keys, notebook format/outputs and importable package. API and installed CLI agree for explicit root/unrelated cwd. |
| IP2-T2 | Proposed `initialization/preflight.py` and `journal.py`; test absent/identical/conflicting targets, edited completed rerun, invalid pin, nested project, package naming/build conflicts, symlink/overlap and concurrent lock. Original hashes remain intact on conflicts. |
| IP3-T1/T2/T3 | Proposed `initialization/environment.py`; actual dependency resolution/imports, lock/hash stability, preserved pin/unrelated packages and existing bounds. Real impossible dependency plus deterministic subprocess failure seam verifies original failure/retry contract. Packaging probes assert declared runtime closure independently. |
| IP4-T1/T2 | Proposed `initialization/storage.py`; real DVC/MLflow public probes and initial state reopening for defaults/external overrides; test incompatible pre-existing stores, permission failures, credential URI rejection, interrupted stages and safe retry. |
| IP4-T3/T4 | Proposed driver `uv run --locked python tests/installation/verify_initialization.py --artifacts-dir FRESH_DIRECTORY`; both independent wheel paths, fresh/existing project fixtures, complete CLI/API outcomes, package imports, ignore checks, no data reads/runs/approvals. Manual VS Code project-kernel test remains final-phase evidence. |

Installed tests use a separate temp Git/uv project and local full-SHA Git harness fixture when implementation is unpublished. Pin checks are separately exercised through installed Git metadata. For the direct/rebuilt wheel init path, the driver must produce a matching full-SHA local Git source fixture from the exact reviewed tree, with wheel metadata/resource identity checked against that fixture; do not claim a wheel install has Git direct_url metadata. Use pinned-Git projects for pin preservation acceptance and wheel projects for packaged-resource/init coverage; record these complementary boundaries explicitly rather than faking a wheel's origin.

Each behavior remains a separate red–green slice, not a batch of all tests. No private helper assertions; injected external-tool errors supplement real tools. Full development commands and both distribution paths run in executable phases. IP1 has no new executable behavior, so TDD/runtime checks do not apply.

## Completion and limitations

T1–T4 contract/design outputs are prepared for review. IP1 gate must approve these concrete API/schema, dependency/storage choices and refined boundaries before IP2. Nothing here implements init, proves dependency joint resolution, verifies storage APIs on installed selected releases, or certifies kernel isolation. Those planned checks belong to IP2–IP4. No full AC-01–05 delivery claim, new suppressions, lock changes, or platform-support claim.
