# Repository and Resource Layout

Active design 0.15; [authority](../agentic-ml-harness-design.md).
Paths below distinguish current resources from illustrative future experiment files.

## Toolkit product repository

Current reusable package is `src/agentic_ml/`, including `initialization/`,
`planning/`, `approvals/`, `validation/`, `extraction/`, `data_quality/`,
`data_assessment/`, `splitting/` and `cli/`.
Templates, runtime guidance, schemas and registry metadata are package resources
under that same package. Preserve their locations; no resource move or new
root-level runtime/development instruction loading is authorized.

Docs and tests stay contributor-owned. Future experiment/tracking helpers
belong in the installable package when reusable; exact module seams are reviewed
in owning story plans. A general orchestrator/framework/agent directory tree is
not required just to match the archived platform layout.

Current extraction publishes a project-owned directory containing `dataset.csv`
or `dataset.parquet` plus `extraction.json`. Quality/assessment/partition APIs
return plain dictionaries; project code selects paths and saves/loads reports or
split records. These files do not imply current DVC stages or MLflow run logging.

## Separate experiment project

Illustrative MVP project, not an implemented initializer output promise:

```text
experiment-project/
  pyproject.toml
  uv.lock
  project.yaml
  .gitignore
  .dvc/
  data.dvc
  dvc.yaml
  dvc.lock
  src/project_experiments/
  experiments/
    baseline/
      experiment.md
      experiment.yaml
      search-space.yaml
      notebooks/
  data/                 # DVC content; excluded from Git
```

Project package/name and stage paths are user-selected. Current initialization
already creates project/scaffolding/storage with 0.1 drafts; it does not yet create
a runnable end-to-end experiment or these DVC stage files. US-39 supplies that gap.
M2 demonstrates compatible project preprocessing/model code and saved notebooks.

Track source/notebooks, reviewed configuration, lockfiles, DVC metadata/stages and
nonsecret run/data references in Git. Store datasets via DVC and fitted models/
results via configured MLflow artifacts. Exclude local generated stores, dataset
content and credentials from Git. Current private setup journal/state remains
setup evidence, not a mandatory durable experiment state machine.

Resolve paths against the explicit project root and honor declared DVC stage
working directories. Reproduction uses committed required source and available
versioned inputs; no automatic untracked/helper snapshot collection is promised.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/repository-layout.md).

<a id="repository-layout"></a>

<a id="12-proposed-repository-layout"></a>

<a id="separate-user-experiment-repository"></a>

<a id="harness-product-repository"></a>
