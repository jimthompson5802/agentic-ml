# Repository Layout

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Proposed Repository Layout.

**Related contracts:** Read [interfaces and configuration](interfaces-and-configuration.md); [execution and governance](execution-and-governance.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 12. Proposed Repository Layout

### Harness product repository

This repository contains the installable product, templates, examples, and product tests. Example projects and fixtures demonstrate usage; user experiment repositories are created separately.

```text
agentic-ml-harness/
├── AGENTS.md
├── README.md
├── pyproject.toml             # Build metadata, dependencies, agentic-ml entrypoint
├── uv.lock
├── docs/
│   └── specs/
├── templates/                # Separate-project and notebook scaffolding
├── runtime_guidance/         # Included as resources in the distribution
│   ├── AGENTS.md
│   ├── data/AGENTS.md
│   ├── features/AGENTS.md
│   └── modeling/AGENTS.md
├── src/agentic_ml/
│   ├── AGENTS.md
│   ├── contracts/
│   ├── orchestrator/
│   │   └── AGENTS.md
│   ├── agents/adapters/
│   ├── approvals/            # Approval service and scoped decision handling
│   ├── data/
│   │   ├── sources/
│   │   ├── acquisition/
│   │   └── validation/
│   ├── features/
│   │   └── AGENTS.md
│   ├── harness/
│   │   ├── execution/
│   │   ├── evaluation/
│   │   └── resources/
│   ├── frameworks/
│   │   ├── sklearn/
│   │   ├── lightgbm/
│   │   └── pytorch/
│   ├── tracking/
│   ├── storage/
│   └── cli/
├── examples/
│   ├── tabular-classification/
│   │   ├── experiment.md
│   │   ├── search-space.yaml
│   │   ├── experiment.yaml
│   │   └── notebooks/
│   ├── tabular-regression/
│   └── image-classification/
└── tests/
    ├── unit/
    ├── integration/
    ├── acceptance/
    └── fixtures/
```

### Separate user experiment repository

The following is an illustrative initialized project, not a directory inside the harness repository. Its project package name and experiment names are user-selected.

```text
customer-churn/
├── README.md
├── AGENTS.md                 # Project development conventions
├── pyproject.toml            # Project package and harness Git dependency/full SHA
├── uv.lock                   # Resolved experiment environment
├── project.yaml              # Storage, tracking, state, agent, guidance, components
├── .gitignore
├── .dvc/
├── data/                     # DVC-managed content; excluded from Git
├── data.dvc                  # Illustrative data-version metadata tracked in Git
├── runtime_guidance/         # Optional explicitly mapped project practices
├── src/churn_experiments/    # Shared project code, custom models/preprocessors
└── experiments/
    └── baseline-comparison/
        ├── experiment.md
        ├── search-space.yaml
        ├── experiment.yaml   # Entrypoints, data, feature pipeline, execution
        ├── dvc.yaml
        ├── dvc.lock
        ├── notebooks/
        │   ├── 01_data_assessment.ipynb
        │   ├── 02_features_and_baseline.ipynb
        │   ├── 03_model_development.ipynb
        │   └── 04_results.ipynb
        └── helpers/          # Optional experiment-specific Python
```

Project configuration and experiment-input paths resolve against the user repository root. DVC stage paths follow DVC's declared stage working-directory semantics; pipeline templates must make those paths explicit and consistent with harness execution. Raw sources may remain outside the repository under approved access rules; `data/` represents versioned project snapshots.

Executed notebook snapshots, model artifacts, DVC content/cache, and durable workflow state live in configured project-associated storage and are excluded from Git when stored beneath the project root. Track source notebooks, generated Python, briefs, configuration, project dependency lockfiles, DVC metadata/pipeline definitions, and artifact references in the experiment repository. Preserve immutable source snapshots for runs even when the working tree has uncommitted changes.

