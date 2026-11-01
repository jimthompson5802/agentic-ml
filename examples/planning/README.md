# Version 1.0 planning example

In an initialized experiment project, create a `planning/` directory and copy
`brief.md`, `search-space.yaml`, and `experiment.yaml` from this directory into it.
The example refers to the initialization notebook
`experiments/initial/notebooks/01_data_assessment.ipynb`; if you initialized a different
experiment name, update that path in the copied execution file.

Run from your experiment project with its installed harness dependency:

```sh
uv run --locked agentic-ml plan resolve --project-root "$PWD" --experiment planning/experiment.yaml
```

The explicit brief produces an input-ready plan without reading `data/churn.csv`
or executing the notebook. The dataset need not exist for planning. This example
selects structural algorithm names; registry/training compatibility is future
US-05 work. It does not train a model or grant data/execution permission.

For the delegated walkthrough, replace the brief's `metric: f1_macro` with:

```yaml
metric: {delegate: "Choose metric", proposal: f1_macro, rationale: "Equal weight to both classes"}
```

Resolve again; exit 2 with a plan ID is expected until you review and approve the
new preserved plan. Follow the [approval commands](../../docs/experiment-setup.md#resolve-and-approve-experiment-inputs).
Reviewer labels are self-declared; records use `authentication: none`.
