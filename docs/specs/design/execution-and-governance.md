# Execution and Governance

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Execution, Evaluation, and Governance.

**Related contracts:** Read [interfaces and configuration](interfaces-and-configuration.md); [data and features](data-and-features.md); [acceptance traceability](acceptance-traceability.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 9. Execution, Evaluation, and Governance

### Execution

- Declare dependencies separately in the harness and experiment repositories' `pyproject.toml` files and commit their respective `uv.lock` files. Execute user experiments in the selected experiment project's environment, including its installed harness version and project package.
- Support local Python subprocesses, followed by containerized and GPU execution.
- Support automatic execution of Jupyter notebooks as experiment entrypoints using `nbclient` and an `ipykernel` kernel in the experiment's `uv`-managed environment; provide JupyterLab for interactive development.
- Execute notebooks from a fresh kernel, in cell order, with explicit input parameters and a recorded working directory. Apply experiment timeouts, cancellation, resource budgets, and filesystem/network restrictions to notebook execution.
- Preserve the source notebook, supplied parameters, executed notebook with cell outputs, execution errors, and generated artifacts in the run record. Cell errors fail execution; successful notebooks remain subject to independent evaluation and protected-data rules.
- Keep experiment-specific preprocessing, models, and training logic in the experiment repository's notebooks, helpers, or project package. Both notebook and Python entrypoints import generic capabilities from the installed harness public API; they must not import through paths into the harness source checkout.
- Enforce timeouts, cancellation, experiment counts, memory/GPU quotas where supported.
- Cancellation stops managed training and preserves already available checkpoints, logs, and terminal status under the original run identity. Record the outcome using the cancellation contract below. Forced termination does not promise a new checkpoint; already emitted checkpoints remain retrievable with the restoration metadata defined in [§8](interfaces-and-configuration.md#8-interfaces-and-contracts).
- Capture logs, exit status, project environment/lockfile identity, experiment Git revision, exact executed notebook/code snapshots including uncommitted changes, harness repository URL/full commit SHA/package version, build identity where available, datasets, checkpoints, and artifacts.
- Treat unsuccessful model performance as a valid experiment result, distinct from execution failure.
- Restrict filesystem, network, and credential access for agent-generated code. Separately define access for the assistant process, its tools, and its workspace in each integration mode; restrictions on a notebook subprocess alone do not constrain the assistant.
- Resolve paths against the selected experiment project and record the working directory. Explicitly authorize writable project paths, storage locations, and access to external raw data. Routine experiment execution must not modify the harness installation or source repository.

### Execution backend evolution

The proof of concept executes experiments locally through the `ExperimentRunner` interface, covering submission, status monitoring, cancellation, resource limits where supported, and artifact collection. Keep orchestration and independent evaluation separate from backend-specific scheduling and transport. Implement the local runner first; introduce additional backend abstractions when integration requires them.

Ray is the planned backend for later distributed and parallel execution. Initial Ray support will run independent experiments and hyperparameter trials in parallel. Distributing a single model-training job is a separate, subsequent capability requiring framework-specific design as needed.

Ray dependencies, integration, cluster provisioning, distributed scheduling, and distributed training are outside proof-of-concept scope. Future Ray execution must preserve the existing search boundaries, aggregate experiment budgets, approval gates, cancellation semantics, and provenance requirements. The proof of concept does not require Ray installation or a cluster to execute or validate its local workflow.

### Experiment tracking, data versioning, and pipelines

- Use **MLflow** as the experiment tracking system for Python and notebook runs. Record effective parameters, metrics, execution status, model artifacts, and references to dataset, feature, environment, and instruction provenance.
- Use **DVC** to version raw datasets, extracted snapshots, split manifests, and derived feature datasets. Use `dvc.yaml` to declare pipeline stages and their dependencies, parameters, and outputs; preserve resolved dependency/output hashes in `dvc.lock`.
- Track DVC metadata, pipeline definitions, and lockfiles in the experiment repository's Git history. Exclude dataset contents and large generated artifacts from Git. Configure DVC storage for sharing and restoring versioned data; support local storage initially and choose remote backends/access configuration during implementation.
- The workflow orchestrator retains responsibility for agent delegation, approvals, budgets, and recovery. DVC executes reproducible data and training stages under harness control; it does not replace workflow governance or independent evaluation.
- Link each MLflow run to the experiment Git revision, exact executed notebook/helper/project-code snapshots, harness repository URL/full commit SHA/package version and build identity where available, project lockfile/environment identity, DVC data/output hashes, applicable stage definitions and lockfile snapshot, and harness run identifier. Preserve uncommitted source and resolved metadata in immutable run snapshots. Record the MLflow run identifier in the harness result for bidirectional lookup.
- Keep ownership explicit: DVC manages versioned data and pipeline outputs, MLflow manages experiment records and model artifacts, and harness manifests connect both to approvals and runtime instruction bundles.
- Store executed notebook snapshots and model artifacts in configured MLflow artifact storage, versioned datasets in DVC storage, and durable workflow state in configured project-associated state storage. These locations may be local or external; preserve references and nonsecret configuration in the experiment repository and exclude generated stores from Git.
- DVC stage reuse must preserve producer provenance and remain subject to current evaluation and authorization checks. A cached stage does not establish that an experiment meets acceptance criteria.

### Run evidence capture and restoration

Every recorded Python or notebook run has a schema-versioned harness manifest connecting immutable input evidence to its execution and results. MLflow artifact storage holds manifests, source/configuration bundles, and result evidence; DVC storage holds versioned dataset content. Git retains project sources, DVC metadata, and nonsecret storage configuration. The manifest records artifact locations and content checksums so restoration can verify content rather than trust a location or Git revision alone.

Capture these evidence groups:

| Evidence | Required record |
|---|---|
| Source and configuration | Saved notebook or Python entrypoint, project helpers/package code, effective configuration, and required external file dependencies; preserve project-relative paths and file checksums, including modified and required untracked files. Retain the experiment Git revision as context, not as a substitute for the snapshot. |
| Environment | Harness repository URL/full commit SHA/package version and build identity where available; snapshots of project `pyproject.toml` and `uv.lock`; Python version and relevant platform details. Resolve project-local package code from the captured source. |
| Data | DVC metadata snapshots, dataset content identities, nonsecret configured storage references, and mappings from logical inputs to execution paths. Required dataset content must be available in configured DVC storage. Include stage definitions and `dvc.lock` when pipelines are introduced. |
| Execution | Harness run identifier, recorded entrypoint, working directory relative to the restored project, effective parameters, seeds, and declared nonsecret environment settings. Credentials are supplied separately through authorized access and are never embedded in the evidence bundle. |
| Guidance and authorization | Applicable runtime guidance snapshots, recorded scope/order and checksums, and references to scoped approval evidence. External assistant context is captured only where observable; this does not claim complete external instruction capture. |
| Results and verification | Execution status, exit information, logs, executed notebook where applicable, output artifact references and checksums, declared output checks/tolerances, and independent check results. Metric tolerances apply when modeling is introduced. |

The harness owns this lifecycle:

1. **Prepare:** Resolve required inputs, verify dataset content hashes, and freeze the source/configuration bundle and declared output checks. Persist the immutable input manifest and referenced evidence before launching execution. For milestone 1, snapshot declared project source roots rather than infer coverage through Python import tracing. Exclude credentials, datasets, environments, and generated stores from the source bundle; required external code/file inputs must be explicitly registered and captured or versioned. Failure to resolve or preserve a required input blocks execution.
2. **Execute:** Materialize the frozen bundle in a separate execution directory and execute that source with the recorded environment and verified dataset inputs. The input bundle remains immutable; outputs go to declared writable locations. Later edits to the developer's working tree do not change the submitted run. Apply current execution authorization, access boundaries, and budgets to this directory and its inputs.
3. **Finalize:** Preserve available results and verification evidence in MLflow artifact storage. Write an immutable terminal manifest referencing the input manifest by checksum, output evidence, harness run identifier, and MLflow run identifier. Failed or cancelled runs retain available evidence and their outcome; incomplete evidence must not be reported as successful verification. The input manifest remains available if execution is interrupted before finalization; reconcile submission and finalization through the [§8](interfaces-and-configuration.md#8-interfaces-and-contracts) submission identity contract and [§9](execution-and-governance.md#9-execution-evaluation-and-governance) workflow recovery rules.
4. **Restore:** Starting from an experiment checkout and recorded run manifest, retrieve the pinned harness revision, project dependency files, source/configuration bundle, applicable guidance, and DVC inputs. Verify required evidence checksums and restored dataset content hashes before execution. Rebuild the locked environment without a manually maintained harness checkout and materialize the recorded source, including preserved uncommitted changes. Missing source, dependencies, dataset content, or mismatched required evidence produces an explicit restoration failure identifying the affected input; never substitute a current working-tree file, newer dependency, or alternate dataset silently. Access credentials and current execution authorization remain required; historical approval evidence does not grant new access.
5. **Compare:** Execute the recorded entrypoint from its recorded relative working directory as a new run linked to the original manifest. Independently assess the new outputs against the original declared checks/tolerances, recording comparison results and retaining both runs. Output checksums identify evidence; declared checks determine whether reproduction succeeds when byte equality is not required.

Milestone 1 provides this restoration path without an agent. Demonstrate it in a clean second-machine environment with an uncommitted notebook edit and a required untracked helper, verify that working-tree edits after capture cannot affect execution, and verify explicit failures for removed or corrupted required inputs. Configured storage must be accessible from the second machine; initially local stores may be transferred with their recorded content identities preserved. Exact manifest serialization and CLI/API signatures remain implementation decisions.

### Notebook development and execution contract

- Use `experiments/<name>/notebooks/` in the user repository as the primary interface for data assessment, feature/baseline work, model development, and results analysis. Agents generate and revise these notebooks; users inspect, edit, and run them in JupyterLab. Python entrypoints remain available for advanced use.
- Provide numbered notebook templates for these activities; allow fewer or additional notebooks as appropriate. Include explanatory Markdown describing objectives, assumptions, generated code, results, and proposed next steps.
- Declare JupyterLab and `ipykernel` in the experiment project's dependencies or an explicitly installed interactive dependency group managed by `uv`. Include `nbclient` and `ipykernel` in the installed harness notebook-execution dependencies. Users do not need the harness development environment.
- Use an explicit parameter cell for dataset/configuration references and run identifiers. Require saved notebooks to execute from a fresh kernel in cell order with a defined working directory and locked environment; do not depend on hidden interactive state.
- Exchange artifacts across notebooks through recorded versioned references rather than variables in another notebook's kernel. Snapshot imported experiment helpers and project code with each recorded run.
- Import project-specific shared logic from the experiment repository's own Python package and generic capabilities from the installed harness. Promoting project code into the harness requires a separate development review.
- Users may execute cells interactively for exploration. Recorded experiment results require harness-managed execution of saved source snapshots and independent evaluation; successful interactive execution alone does not establish acceptance.
- Training cells submit work through harness APIs so candidate validation, budgets, approvals, and tracking apply. Interactive and automated work follow the same split, protected-test, and acquisition rules.
- Define the interactive-kernel isolation and protected-data boundary under ADR-006. API checks alone cannot constrain arbitrary Python in an unrestricted kernel. Protected test data must remain inaccessible to experiment-agent and exploratory kernels; approved final evaluation occurs through the independent evaluator.
- Record notebook runs in MLflow with the same configuration, source snapshots, dual harness/experiment identities, dataset versions, feature lineage, and environment provenance as Python entrypoints.

### Independent evaluation

1. **Execution correctness:** code completes and expected artifacts exist.
2. **Scientific validity:** split boundaries, preprocessing fitting, and leakage rules are respected.
3. **Model quality:** agreed metrics and baseline comparisons are computed consistently.
4. **Generalization/robustness:** folds, data slices, or stress tests satisfy defined criteria.
5. **Reproducibility:** reruns meet explicit metric tolerances, acknowledging GPU nondeterminism where applicable.

### Workflow states

`Planned → Running → Evaluating → AwaitingApproval → Approved → NextPhase/Completed`.

Additional terminal or reviewable states: `Failed`, `Cancelled`, `BudgetExhausted`, and `NeedsReview`. A rejection or revision request returns work to an authorized workflow phase; it does not silently bypass gates.

#### Recovery and reconciliation

On restart, acquire exclusive recovery ownership for the workflow and reconcile its durable records with runner submission/execution status and MLflow evidence before issuing new work or accepting results. State transitions and submission authority must reject stale owners, for example through an ownership epoch checked at submission and state update; a lock timeout alone must not allow an old owner to continue advancing work. Exact locking, fencing, and transaction mechanisms remain milestone 5 design decisions.

| Reconciled finding | Required action |
|---|---|
| Completed run with sufficient independently verified evidence | Reuse the original run identity and evidence; continue through any remaining evaluation and approval gates. Do not rerun completed work. |
| Active run | Reattach and monitor the existing run. |
| Submission definitively never accepted | Recheck applicable authorization and budget reservation, then retry using the original submission key and identical inputs. |
| Failed or cancelled run | Preserve its outcome and available evidence. A retry requires permission under existing policy/scope and remaining budgets, and creates a new linked attempt. |
| Unknown submission/execution status, conflicting identities, or insufficient completion evidence | Enter `NeedsReview`; block automatic resubmission and dependent advancement. Reconcile available evidence without rerunning completed execution. |

Preserve consumed budgets across restart and account for each usage record once. Keep reservations for uncertain work until reconciliation establishes actual usage or non-execution; uncertainty must not release capacity for duplicate spending. Settling a reservation into consumed usage must not count both against the budget. Cancellation, failure, budget exhaustion, and review do not silently authorize further work. Any review decision and subsequent authorized action are durable and auditable.

Reused evidence retains its original producer, configuration/input and guidance identities, dataset lineage, artifacts, and approval history. Record the decisions authorizing subsequent use separately. Recovery grants no additional authorization, does not bypass pending gates, and applies current access restrictions. Results from stale, cancelled, or superseded attempts cannot silently advance the workflow. Apply these rules to recovery after acquisition as well as other workflow phases.

### Agent cancellation, usage, and resumption

Cancelling an experiment run and cancelling a managed agent task are distinct operations. Record both outcomes, including whether cancellation was requested, acknowledged, or confirmed terminal. Interactive mode can stop harness-managed work and reject further unauthorized submissions; it does not promise to terminate an externally owned assistant session. Managed adapters document and verify their cancellation behavior, including handling of child work and late results. Results from cancelled or superseded attempts cannot silently advance the workflow.

Enforce harness-run runtime, trial, and resource budgets independently of assistant usage. Record assistant token/cost usage and enforce configured assistant limits where the integration supports measurement and control; label unavailable accounting explicitly rather than claiming a complete assistant cost bound. Admission of new managed tasks requires remaining applicable budgets. Reaching a limit stops the relevant work and preserves a reviewable outcome.

Resume from durable task/attempt and run identities, approved plan and guidance references, captured artifacts, recorded approvals, and consumed budgets. Reconcile in-flight work under the submission identity and workflow recovery contracts before retrying or accepting results; a conversation transcript or assistant memory is not the workflow state. Concrete persistence and coordination mechanisms remain implementation decisions subject to those contracts.

### Governance

Controls are rules and checks enforced by the harness to govern what an experiment may do and whether its results are accepted. They include developer approvals, access restrictions, runtime/trial/resource budgets, independent validation of expected artifacts and results, and boundaries on agent revisions. For example, an execution authorization may permit a notebook to read a specified dataset for at most ten minutes; the harness records that authorization and enforces both limits. Instructions alone do not establish enforcement.

- Approvals are durable, scoped, and auditable. Bind each decision to an authenticated developer and the reviewed plan/configuration and scope. Agent requests and assistant tool-execution permissions do not establish experiment approval. The approval channel must distinguish developer decisions from agent actions; agents cannot approve their own scope expansions or final acceptance.
- Approval records, evaluator credentials, and protected-test data must be inaccessible for unauthorized reading or modification by assistant tools as well as experiment code. Define accessible resources for both modes under ADR-006. An unrestricted assistant workspace cannot be described as enforcing these boundaries; instruction text and CLI/API validation alone do not provide isolation.
- New data sources, expanded permissions, changed evaluation criteria, and workflow phase transitions require authorization.
- Protected test sets cannot be used for iterative tuning or data acquisition decisions.
- Resource limits and stopping conditions apply to both inner and outer loops.

