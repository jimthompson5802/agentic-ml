# Example scenario: Build a customer churn model

The intended experience is a notebook-centered ML project in the data scientist's own repository. A coding assistant helps write and improve the experiment. The harness controls execution, tracking, independent evaluation, and approvals.

This walkthrough follows the [user stories](user-stories.md) and [harness design](agentic-ml-harness-design.md). The project currently contains a proposed design, not a working tool. The setup commands below describe the intended interface; other CLI/API signatures remain undecided.

## How to read the sample prompts

**Blockquotes beginning with `>` are sample natural-language prompts that the data scientist types into a coding assistant**, such as Codex, Claude Code, or GitHub Copilot, with the experiment repository open. They are not terminal commands or defined `agentic-ml` syntax.

The assistant reads the project's brief and configuration, creates or revises notebooks and supporting code, and invokes the public harness CLI/API where available. No agent adapter is required for this interactive use.

A prompt asking the assistant to present work for approval does not itself grant approval. The scientist must record the actual decision through the harness's developer approval mechanism. That interface remains undecided; an assistant cannot approve its own work or scope expansions.

## 1. Create the experiment project

After installing Git and `uv`, the scientist runs:

```bash
mkdir customer-churn
cd customer-churn

git init
uv init
uv add "git+https://github.com/OWNER/HARNESS-REPO.git" --rev FULL_COMMIT_SHA

uv run agentic-ml init
# Open this project in VS Code and select its .venv notebook kernel.
```

The repository URL and SHA are placeholders. The harness is installed as a pinned dependency; the scientist does not maintain a separate harness checkout.

Initialization creates configuration, notebook templates, project-package scaffolding, and local defaults for DVC, MLflow, and workflow state. An illustrative project includes:

```text
customer-churn/
├── project.yaml
├── pyproject.toml
├── uv.lock
├── src/churn_experiments/
└── experiments/baseline-comparison/
    ├── experiment.md
    ├── search-space.yaml
    ├── experiment.yaml
    └── notebooks/
        ├── 01_data_assessment.ipynb
        ├── 02_features_and_baseline.ipynb
        ├── 03_model_development.ipynb
        └── 04_results.ipynb
```

Experiment and package names are user-selected. Initialization does not authorize data access or execution. Data permissions, credentials, storage settings, and approval presentation require explicit setup; credentials remain outside committed configuration.

## 2. Describe the prediction problem and boundaries

The scientist writes—or asks the assistant to draft—these inputs:

| File | What the scientist specifies |
|---|---|
| `experiment.md` | Data, target, prediction task, feature restrictions, metric, split constraints, algorithm mode, and budgets |
| `search-space.yaml` | Allowed algorithms, fixed parameters, and permitted tuning ranges |
| `experiment.yaml` | Notebook/code entrypoints, data references, feature pipeline, and execution settings |
| `project.yaml` | Project-wide storage, tracking, agent settings, and custom component declarations |

Sample coding-assistant prompt:

> Prepare a churn classification experiment using our customer dataset. Predict `churned`, exclude `customer_id` and any information unavailable at prediction time, and respect customer grouping and temporal boundaries. Propose an appropriate metric for the imbalanced target. Compare logistic regression and random forest. Limit optimization to 20 trials per algorithm and 60 minutes total. Draft the brief and configurations, explain unresolved decisions, and present the resolved plan for my approval.

For example, part of the proposed search space could be:

```yaml
schema_version: "0.1"
algorithms:
  logistic_regression:
    fixed:
      max_iter: 2000
    search:
      C:
        type: float
        min: 0.0001
        max: 100
        scale: logarithmic
      class_weight:
        type: categorical
        choices: [null, balanced]
```

This excerpt covers one algorithm; the complete configuration would also declare the approved random forest search space. The YAML is a hard boundary: the assistant cannot introduce another algorithm or extend a parameter range during the experiment. Omitted parameters use recorded registry defaults and do not become tunable.

The harness validates and records the effective, versioned plan. The scientist resolves ambiguities and approves delegated choices, access scope, evaluation protocol, and budgets before dependent execution. The exact command for submitting or approving the plan is still unspecified.

## 3. Assess the data and approve the splits

**Notebook:** `01_data_assessment.ipynb`

Sample coding-assistant prompt:

> Prepare the data-assessment notebook. Use the authorized source to create a versioned snapshot. Report missing values, distributions, target balance, anomalies, and possible leakage. Propose reproducible training, validation, and protected-test splits that respect the approved time and customer-group constraints. Present the assessment and split protocol for review.

The scientist opens the notebook in VS Code, reads its explanations, and can execute cells for exploration.

For an accepted, recorded result, the saved notebook must undergo harness-managed execution: a fresh kernel, ordered cells, explicit inputs, a locked environment, a recorded working directory, and a frozen source snapshot. Interactive execution alone does not establish acceptance.

The scientist reviews the assessment and approves the split protocol before dependent feature or modeling work. Protected-test data remains inaccessible to exploratory notebooks and the assistant.

## 4. Develop features and establish a baseline

**Notebook:** `02_features_and_baseline.ipynb`

This notebook supports two separate workflow phases, with an approval boundary between them. Its filename does not authorize executing both workflow phases together.

First, feature engineering:

> Build a reproducible preprocessing pipeline with imputation, categorical encoding, and scaling where appropriate. Fit all learned transformations on training data only. Compare the proposed features against the approved baseline feature set using the fixed reference estimator, settings, and validation metric. Show gains, ties, or regressions and preserve pipeline artifacts and lineage.

The baseline feature set, fixed reference estimator and settings, and validation metric require approval before this comparison. The scientist reviews the comparison evidence and approves the feature pipeline before proceeding to baseline modeling.

Then, baseline modeling:

> Using the approved features and split protocol, train the agreed simple baselines. Record their parameters, validation metrics, and artifacts. Present the baseline results for approval before candidate-model comparisons.

If the scientist already has preprocessing or model code, the assistant can register and invoke the project-local implementation. Supplied components are immutable by default; changing them requires authorization and a new versioned experiment configuration.

## 5. Compare models, then tune candidates

**Notebook:** `03_model_development.ipynb`

Sample model-development prompt:

> Compare the approved logistic regression and random forest candidates against the accepted baseline. Use only the declared algorithms and parameters. Diagnose errors using development data, record each candidate through the harness, and summarize the evidence at the model-development approval gate.

After reviewing the evidence and approving progression to optimization, the scientist could prompt:

> Tune the approved candidates within `search-space.yaml` and the remaining trial and runtime budgets. Preserve fixed parameters. Stop when the budget is exhausted or the approved stopping condition is met. Present the optimization summary and recommended model for final evaluation.

The assistant can revise and rerun work within the currently approved workflow phase without approval for every trial. Moving to another workflow phase, expanding the search space, or changing permissions requires authorization.

Training cells submit through harness APIs so candidate validation, budgets, tracking, and approvals apply. Concrete API calls and training/tuning CLI commands remain undecided; this walkthrough does not prescribe executable syntax for them.

Notebook-to-notebook dependencies use recorded, versioned artifact references rather than variables retained in another notebook's kernel.

## 6. Authorize independent final evaluation

**Notebook:** `04_results.ipynb` presents results and the final report.

Sample coding-assistant prompt:

> Prepare the selected model and its recorded preprocessing pipeline for independent final evaluation. Summarize the development results, reproducibility evidence, limitations, and required holdout checks. Present the candidate for my authorization.

Once authorized, the independent evaluator accesses the protected holdout. The results notebook presents its recorded findings; ordinary notebook code does not gain holdout access.

The scientist approves or rejects the final model after reviewing the independent assessment. Holdout results cannot feed another tuning, feature-improvement, or data-acquisition loop. Further development after unsuccessful final evaluation requires a separately approved evaluation protocol that preserves holdout protection.

The resulting evidence includes the selected model and preprocessing artifacts, evaluation results, and reproducibility records. Production deployment is outside this walkthrough.

## 7. Inspect, reproduce, or resume work

The scientist inspects readable notebooks alongside MLflow records containing metrics, parameters, model artifacts, logs, and executed notebook snapshots. DVC versions datasets and pipeline outputs. Harness manifests connect those records to source, configuration, environment, approvals, and data lineage.

A reproduction request to the coding assistant could be:

> Restore recorded run `<run-id>` in a clean environment, verify its source and data checksums, execute its captured entrypoint, and compare the outputs against the recorded tolerances. Report missing inputs explicitly.

Restoration uses captured source—including required uncommitted changes—and the original locked environment. Storage must be accessible, and current access and execution authorization still apply. Exact restoration commands remain undecided.

With managed orchestration, a resume request could be:

> Resume this experiment from its durable state. Reconcile existing runs before submitting work, preserve consumed budgets, and stop at the next developer approval gate.

Completed work with sufficient verified evidence is reused; active work is reattached. Uncertain execution status requires review rather than automatic duplicate submission. Durable harness state, rather than assistant conversation memory, determines where work resumes.

## Interactive and managed operation

| Interaction mode | Scientist's experience |
|---|---|
| Interactive assistant | Prompt an external coding assistant, review its edits, and have it invoke the public harness CLI/API. No agent adapter is required. The harness does not own the assistant session. |
| Managed agent | Configure a verified adapter, approve bounded work, and let the orchestrator delegate revisions and execution until a gate or stopping condition. |

Both modes use the same experiment evidence, boundaries, budgets, and approval controls. Reviewing every notebook edit is optional unless configured as an additional gate; workflow phase approvals remain mandatory.

The notebooks are the scientist's working interface. The harness supplies reproducible execution and independent evidence for assessing the resulting model.

## Delivery expectations

The complete scenario spans cumulative milestones in the user stories:

| Milestone | Capability used in this scenario |
|---|---|
| 1 | Initialize a separate project, validate and record supplied inputs, extract/version data, execute saved notebooks, inspect records, and reproduce runs without an agent dependency |
| 2 | Assess data, approve splits, build reproducible feature pipelines, and compare features using a fixed approved reference estimator |
| 3 | Compare and tune models, persist model artifacts, and obtain authorized independent final evaluation |
| 4 | Use a verified managed agent integration for notebook generation and bounded improvement within an approved workflow phase |
| 5 | Supervise and resume the durable workflow across workflow phases |
| 6 | Authorize additional data acquisition when development evidence identifies a data limitation |

An external coding assistant can help prepare project inputs and invoke available public interfaces before managed agent support arrives. If development evidence suggests acquiring more data, the scientist must authorize its source, strategy, and limits, along with a return to the affected workflow phases. Protected-test feedback cannot drive that acquisition.
