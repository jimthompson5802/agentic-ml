# Classification training contract

Status: **Fitting implemented; Gates 1–2 approved. Project recording and native
persistence pass local IP3 checks; Gate 3 approved, 2026-11-15 UTC.**
Developer decision: “i approve phase 1”. This confirms the revised
validate-then-construct interface, public test boundaries and explicit bounded
tree-storage persistence choice. `fit_classifier` has focused local evidence in
the [IP2 report](verification/us-18-ip2.md). Project recording and native persistence passed IP3 verification. Both normal
installed wheel paths pass the [IP4 focused checks](verification/us-18-ip4.md);
final M1–6 and shared checks pass. Gate 4 is approved, 2026-11-15 UTC; explicit
M1 classification slice accepted on the same date.
The [owning plan](plans/milestone-1-us-18.md) defines the M1 slice, development
gates and acceptance criteria. [Native feasibility evidence](verification/us-18-ip1.md)
does not establish installed workflow acceptance.

## Public fitting interface

Implemented fitting export from `agentic_ml.training`:

```python
def fit_classifier(
    frame: pd.DataFrame,
    *,
    project_root: Path,
    candidate: CandidateRequest,
    estimator_bindings: Mapping[str, type[BaseEstimator]],
    preprocessing: Pipeline,
    partition_record: Mapping[str, object],
    selected_columns: Sequence[str],
    output_schema: Sequence[Mapping[str, str]],
    fit_partition: str = "train",
) -> tuple[Pipeline, dict[str, object]]: ...
```

The interface uses existing pandas/sklearn objects and existing
`agentic_ml.validation.CandidateRequest`; no new request/result class or plugin
registry is introduced. `project_root` must be an existing absolute project
directory and match the candidate's resolved project root. The helper must not
change cwd. It performs fitting in memory, reads existing strict validation
evidence, and does not create runs, output files or an experiment environment.

`frame`, partitions, selected columns and output schema follow the accepted
[preprocessing contract](preprocessing.md). The returned native Pipeline accepts
the ordered selected feature columns, not a full frame containing ID/target.
Its stable steps are `preprocessing` (the fitted transformer Pipeline) and
`estimator` (the fitted classifier). Native `.predict`, `.classes_` and
`pipeline["preprocessing"].transform` remain usable. The return does not include
final-test scores, selected-model status or a claim of quality-check success.

## Extending native estimators from the project

Project code supplies an explicit class mapping and parameter declarations. The
toolkit constructs the estimator; the project does not supply an instance:

```python
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

estimator_bindings = {
    "dummy_classifier": DummyClassifier,
    "decision_tree": DecisionTreeClassifier,
    "random_forest": RandomForestClassifier,
}
```

Project additive registry metadata describes `decision_tree` and `random_forest`
parameters through the existing [validation API](configuration-validation.md).
The existing `dummy_classifier` profile remains unchanged; its `most_frequent`
strategy must be explicitly fixed in the project configuration.

Training selects the class with `estimator_bindings[candidate.algorithm]`.
After current candidate validation succeeds, the toolkit constructs a fresh
instance with the complete materialized parameters:

```python
estimator_class = estimator_bindings[candidate.algorithm]
estimator = estimator_class(**validated_parameters)
```

Here `validated_parameters` is the successful existing validation result, including
fixed values, defaults and supplied candidate values. It is not a separate
caller-provided override dictionary. No estimator instance or factory callback is
accepted. Class identifiers in metadata do not trigger dynamic imports. Supported
bindings are native sklearn `BaseEstimator` subclasses with classifier
`fit`/`predict`/`get_params` compatibility; after construction, `is_classifier`
checks the native classifier tags. Classes outside the `sklearn` module namespace
are outside this M1 contract.
The namespace check expresses support scope, not protection against trusted
project code spoofing a class. There is no toolkit-maintained estimator list,
algorithm switch or adapter to update when a compatible native classifier is
added. Bindings are ordinary arguments; they are not persisted as executable
registrations. Record the selected class's module and qualified name instead.

The required extension proof supplies the forest binding and additive
metadata plus candidate configuration entirely from an already installed experiment project. It must work on
both direct and sdist-rebuilt wheels without package edits or a rebuild for the
new estimator. Initial certification covers dummy/tree/forest; generic interface
support is not certification of every sklearn model or parameter combination.
Custom/third-party classes, meta-estimators with object parameters and arbitrary
component persistence remain later US-16 work.

## Parameters and strict validation

1. Require `fit_partition == "train"` and a native sklearn estimator class
   binding for the requested algorithm. Preserve the mapping, candidate and
   parameter declarations; clone only caller-supplied preprocessing. No
   caller-owned estimator state is accepted or reused.
2. Inspect current strict validation evidence through public APIs. The selected
   configuration algorithm must have task `classification` and library
   distribution `scikit-learn`. Reinvoke `validate_candidate(candidate)` before
   any fitting; blocked evidence cannot be substituted with caller assertions.
3. Take a defensive copy of the candidate result's complete parameters and
   origins. Construct exactly the selected bound class with those keyword
   arguments, before any preprocessing or classifier fitting. Confirm the new
   object is a classifier, then require its `get_params(deep=False)` keys and
   values to match the complete validated set, keeping bool/int/float distinctions.
   This detects metadata omissions, native default drift or constructor changes
   rather than comparing against a caller-created instance. Never fill omitted
   metadata parameters silently, coerce values or apply extra overrides after
   validation. Constructor `TypeError`/`ValueError` remains visible with algorithm
   and construction-stage context; no preprocessing or estimator fit may follow
   a construction/coverage failure.
4. This first contract supports finite plain JSON scalars only: null, boolean,
   integer, float and string. Arrays, dictionaries, callable/object parameters,
   nested estimator parameters and random-generator objects fail explicitly.
   Consequently profiles must include every native scalar default, even if the
   scientist sets only a few parameters. Supply reviewed static project metadata;
   do not generate validation boundaries from a submitted class or newly
   constructed estimator immediately before accepting it. An added native parameter after a library
   upgrade requires explicit profile review rather than silent default drift.
5. Existing metadata constraints check declared types/domains/combinations before
   preprocessing or estimator fitting. Native sklearn `fit` remains responsible
   for intrinsic constraints not expressible in the scalar metadata schema.
   There is no public standalone whole-estimator parameter validator assumed
   here. Do not call `_validate_params` or private constraint structures. Native
   errors remain visible; no claim of pre-validating every scientific/semantic
   combination is made. Invalid candidate bounds still fail before all fitting.
6. Profiles record library reference versions; current validation evidence records
   installed identities. Actual run versions and effective values must be saved.
   Use integer seeds for stochastic examples. Nullable seed defaults may remain
   valid for a deterministic baseline; do not claim reproducibility of arbitrary
   stochastic configurations with null seeds. The example forest uses `n_jobs=1`;
   the toolkit does not silently rewrite the caller's resource/parallel settings.

The strict API consumes real 1.0 plan/validation evidence. It adds no experiment
approval record requirement and does not alter explicit strict approval APIs.
US-39 owns the later basic-path configuration bridge; no fake plan IDs or
initializer draft migration is provided here. Currentness is checked at the
supported boundary; no concurrent-writer isolation or atomic validation/fit
transaction is promised.

## Fit scope, predictions and metadata

Reuse `fit_preprocessing` to validate source identity and full recorded partition
membership/disjointness, clone and fit preprocessing only on training features,
and verify the output schema. Reconstruct training rows using the existing
public partition interface. Preserve the original record's seed/settings and
row order; do not replace it with a supplied-mode reconstruction record.

The training target must be one-dimensional, nonmissing and a native sklearn
binary or multiclass target. Multi-output/multilabel/regression targets are
outside this interface. Fit the newly constructed estimator on transformed training rows
and aligned training targets only. Compose the fitted objects without another
full-Pipeline `.fit`. Verify native training predictions have one label per row,
are one-dimensional and belong to the fitted class set. Native prediction errors
remain visible. This minimal compatibility check is not a validation score.

Both two-way and three-way records support fitting. The helper never scores or
predicts their test partition. Project development comparisons require a separate
validation partition; no fallback to test or training accuracy. Original frame,
record, candidate, bindings, parameter declarations and preprocessing must
remain unchanged. Each helper call constructs a new estimator; no fitted state
can carry over from a prior call.

Return the following exact training record keys, all finite plain JSON:

| Key | Value |
|---|---|
| `schema_version` | `"1.0"` |
| `algorithm` | Selected candidate algorithm ID |
| `estimator_class` | `{module: str, qualname: str}` for the selected class |
| `validation_id` | Existing strict candidate validation identity |
| `parameters` | Complete native scalar parameter mapping |
| `parameter_origins` | Existing candidate fixed/default/candidate origin mapping |
| `fit_partition` | `"train"` |
| `classes` | Ordered native class labels converted to finite JSON scalars |
| `preprocessing` | Unmodified accepted preprocessing metadata record |
| `versions` | Installed versions of `agentic-ml`, `scikit-learn`, `pandas`, `numpy` and `pyarrow` |

The nested preprocessing record retains schema, feature settings and source/split
membership; no new split identifier or parallel lineage service is introduced.
The record describes supported operations; claims about train-only fitting are
verified independently by behavioral tests, not certified by metadata alone.

## Project execution and MLflow ownership

The copyable project below implements this execution outline. It consumes
reviewed strict 1.0 inputs; the initializer does not create them today:

1. Load explicit project paths, reviewed strict inputs, additive metadata,
   extraction data and the saved partition record. Use current public strict
   planning/configuration APIs to obtain genuine validation identities.
2. Apply configured quality checks with `run_validated_step` around dependent
   training. Required failure blocks training; empty rules mean `not_checked`.
3. Create the baseline's native run in an explicit store. Invoke `fit_classifier` with the baseline class binding and candidate request. The toolkit
   validates, constructs and fits the baseline from its effective parameters. Predict only
   validation features; compute native `accuracy_score`.
4. Save the complete model under a fresh project-local staging directory with
   `mlflow.sklearn.save_model`. Use explicit `serialization_format="skops"` and
   the approved bounded trust list below, with explicitly pinned model dependency
   requirements from the observed environment. Native model environment files
   supplement the project lock; they do not replace it or prove a restored
   environment. No automatic dependency-inference fallback is relied upon.
5. Check native run artifact namespace `model/pipeline` is empty, then upload the
   model directory with the explicitly selected `MlflowClient.log_artifacts`.
   Do not overwrite artifacts. This check is conflict handling under trusted
   local use, not an atomic multi-writer reservation.
6. Use accepted `log_preprocessing` with
   `pipeline["preprocessing"]` and `record["preprocessing"]`; this preserves
   its established record exactly. Save the complete training record as a
   project JSON output and publish it via `log_run_results`. That existing helper
   records supplied metrics/parameters, expected outputs and shared provenance,
   then finalizes. The training output and accepted preprocessing artifact must
   agree exactly; they do not introduce separate split/data identities.
7. Only after baseline success, fit/log the authored candidate using the same
   source/splits/features/validation metric, with the baseline native run ID in
   candidate parameters. One native run per model. Repeat independently with
   project-only forest bindings for the extensibility demonstration. No new
   toolkit tracking wrapper or baseline state machine is needed.
8. On process/fitting/model-persistence failure, preserve available local logs,
   model directories and outputs. Record FAILED on an eligible native run where
   possible, preserving the original exception and any secondary logging failure
   context. Native `save_model` alone does not finalize the run. Never finalize
   success or proceed to candidate comparison after a failed baseline.

Shared committed provenance follows the accepted [tracking contract](experiment-tracking.md):
real DVC pointers for consumed source/splits, committed code and configuration,
locked environment and supported toolkit installation identity. Metadata profile
and binding source files must be included in committed project code/configuration
references. Project code creates runs; MLflow remains the authoritative run store.
Validation failure and quality shortfall remain distinct from process status;
poor accuracy does not turn correct execution into process failure.

Invoke the script with its installed project interpreter and explicit absolute
project root, including from an unrelated cwd. Native DVC stage scheduling,
automatic final-test evaluation and the basic experiment CLI remain other stories.

### Persistence choice approved at Gate 1

Use explicit skops trust entries `numpy.dtype` and
`sklearn.tree._tree.Tree` for these locally fitted native models. Existing
preprocessing's `numpy.dtype` entry alone fails for trees and forests under
MLflow 3.17.2 / skops 0.16.0. The bounded alternative passed native save,
upload/download, load and inference for all three classifiers.

Tree storage is deliberately untrusted by default: skops checks types, not the
safety of arbitrary serialized node indices. This proposal applies to models
created by the trusted local experiment, not arbitrary downloaded files. Do not
derive trust automatically from `get_untrusted_types`, trust entire modules,
switch to pickle, or retry with a broader list after failure. A different native
estimator requiring more types needs an explicit project persistence choice and
verified compatibility; no toolkit source edit is required for its binding.
Gate 1 approved this bounded choice. The project explicitly supplies the trust
list to native persistence; no automatic fallback is implemented.

## Errors and verification boundary

| Condition | Required observable outcome |
|---|---|
| Wrong argument types, non-class bindings or unsupported parameter representation | `TypeError` naming the field |
| Invalid scope, missing/non-native/non-classifier binding, task mismatch, malformed/current-source or partition inconsistency, parameter mismatch, bad target or incompatible prediction shape | `ValueError` with actionable context |
| Blocked strict candidate/configuration evidence | `ValueError` preserving public diagnostic codes/fields/messages; no fit |
| Missing project or strict input, I/O/operational validation failure | Preserve native `FileNotFoundError`/`OSError` or existing `ValidationError`, including causes |
| Native constructor failure | Preserve native exception type/cause; add algorithm and construction-stage context; no fit |
| Native fit/predict failure | Preserve native exception type/cause; add algorithm and stage context; never return success |
| Artifact collision | Project recording fails with `FileExistsError`; prior artifacts preserved |
| Model serialization/storage failure | Native exception retained, available diagnostics preserved and FAILED attempted; no silent fallback |
| Invalid quality checks / poor metric | Preserve separate configured-validation and quality outcomes; no false successful-training result after a required precheck failure |

Before IP2 behavior tests, developer Gate 1 confirmation must cover this exact
interface without an estimator argument, scalar parameter restriction, caller
class bindings, validate-then-construct order, fitted-pipeline return,
metadata keys, errors, persistence decision and the plan's numerical/failure
boundaries. Public tests must inspect native predictions and actual stored
artifacts rather than assert private collaborator calls.

The baseline/tree oracle remains in the plan. For the forest extension use the
same symmetric rows with a separately defined ensemble configuration:
`n_estimators=3`, `bootstrap=False`, `max_features=None`, `max_depth=1`,
`random_state=17`, `n_jobs=1`. Every tree sees all four training rows and the only
feature, whose separating midpoint is zero. All three trees therefore vote 0
for -2 and 1 for +2; expected validation/inference labels are `[0,1]`, accuracy
1.0. The probe observed all three thresholds at zero; implementation tests should
assert public outputs, not private tree internals. These settings exercise a
forest without relying on chance bootstrap membership. They do not certify
stochastic bootstrap configurations generally. Use exact class predictions and
`rtol=1e-12, atol=1e-12` for controlled floating outputs.

Local IP2 tests cover fitting, multiclass behavior, strict candidate rejection,
class bindings, constructor errors, fresh instances and source/partition/feature
guards. IP3 adds baseline-order recording, native persistence and configured/operational
tracking failure checks. IP4 verifies both normal installed wheel paths, including
the literal guide, constructor/parameter boundaries, native inference and lineage.
No user-story acceptance or additional platform certification is claimed.


## Runnable project example

Use a fresh, separate project initialized through the [installed setup guide](experiment-setup.md).
Keep its retained toolkit wheel or full-SHA Git dependency, native `uv.lock`,
`.venv`, `project.yaml`, `.dvc` and setup journal. Configure Git author identity
before preparing the example. Save the following three files in that project.
The preparation script writes this example's strict inputs and tiny dataset,
versions the data with native DVC, and commits the project files. It is intended
for an empty example project. It does not migrate initializer drafts or accept
uncommitted code as reproducible provenance.

This is a concrete one-feature classification example, with fixed authored
profiles and validation accuracy. Adapt its reviewed inputs and project code
together for another dataset. The native estimator binding and scalar metadata
are project files; forest support requires no toolkit source/resource edits.
Empty quality rules explicitly record `not_checked`. Required quality failures
stop fitting; advisory failures can finish while recording failed validation.
The test rows are recorded for disjointness and remain unused for comparison.

Run both scripts with the project's own interpreter and absolute paths, including
from an unrelated directory:

```sh
/absolute/project/.venv/bin/python /absolute/project/prepare_training.py /absolute/project
```

Preparation prints a JSON object with `tracking_uri` and `experiment_id`. Pass
those exact values as the last two arguments (quote the URI and paths):

```sh
/absolute/project/.venv/bin/python /absolute/project/train.py /absolute/project 'sqlite:////absolute/project/.agentic-ml/classification.db' 'EXPERIMENT_ID_FROM_PREPARATION'
```

Training prints baseline and candidate native run IDs. The baseline validation
accuracy is 0.5; tree and forest accuracies are 1.0 on this controlled fixture.
Native fitted models are under `model/pipeline`, preprocessing under
`preprocessing`, the complete training record under
`outputs/training/training.json`, and shared lineage under `provenance.json`.
Use the same explicit MLflow store when inspecting these IDs. Repeating training
creates new runs and staging directories; it does not overwrite an earlier run.
On a process error, the original exception and run/stage notes remain visible;
available local `.training/<run_id>/` files are preserved. Diagnostics and FAILED
status are attempted independently where the selected backend remains available.
A hard kill or unavailable backend cannot guarantee finalization.

The preparation script declares all native scalar defaults for the tree and
forest, using static reviewed values rather than introspecting an estimator.
The bounded native versions are still checked against the actual project lock
and installation when recording results. Model requirements pin observed
serializer/library versions and supplement that lock; loading these locally
created artifacts does not establish M2 project reproduction.

### training_bindings.py

<!-- project-file: training_bindings.py -->

```python
"""Project-owned native bindings; adding a forest needs no toolkit change."""

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

ESTIMATOR_BINDINGS = {
    "dummy_classifier": DummyClassifier,
    "decision_tree": DecisionTreeClassifier,
    "random_forest": RandomForestClassifier,
}
```

### prepare_training.py

<!-- project-file: prepare_training.py -->

```python
"""Prepare a tiny, committed classification example in an initialized project."""

import hashlib
import json
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import pandas as pd
import yaml
from mlflow import MlflowClient

from agentic_ml.splitting import create_partitions

root = Path(sys.argv[1])
if not root.is_absolute() or not root.is_dir():
    raise ValueError("Supply an existing absolute initialized project root")


def command(*args):
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def ref(name):
    return {
        "path": name,
        "sha256": "sha256:" + hashlib.sha256((root / name).read_bytes()).hexdigest(),
    }


tree = {
    "ccp_alpha": 0.0,
    "class_weight": None,
    "criterion": "gini",
    "max_depth": 1,
    "max_features": None,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "min_weight_fraction_leaf": 0.0,
    "monotonic_cst": None,
    "random_state": 17,
    "splitter": "best",
}
forest = {key: value for key, value in tree.items() if key != "splitter"} | {
    "bootstrap": False,
    "max_samples": None,
    "n_estimators": 3,
    "n_jobs": 1,
    "oob_score": False,
    "verbose": 0,
    "warm_start": False,
}
# Authored scalar declarations, never inferred from a constructed estimator.
parameters = {
    "dummy_classifier": {"strategy": "most_frequent"},
    "decision_tree": tree,
    "random_forest": forest,
}
kinds = {
    type(None): "null",
    bool: "boolean",
    int: "integer",
    float: "float",
    str: "string",
}
registry = {
    "schema_version": "1.0",
    "algorithms": [
        {
            "id": name,
            "interface_version": "1.0",
            "tasks": ["classification"],
            "adapter": {"id": "project_classifier", "version": "1.0"},
            "library": {"distribution": "scikit-learn", "reference_version": "1.9.1"},
            "parameters": {
                key: {"types": [kinds[type(value)]], "default": value}
                for key, value in values.items()
            },
            "requires_non_null": [],
        }
        for name, values in parameters.items()
        if name != "dummy_classifier"
    ],
}
(root / "registry.yaml").write_text(yaml.safe_dump(registry))
(root / "search.yaml").write_text(
    yaml.safe_dump(
        {
            "schema_version": "1.0",
            "algorithms": {
                name: {"fixed": values, "search": {}}
                for name, values in parameters.items()
            },
        }
    )
)
sections = {
    "Objective": {"schema_version": "1.0", "objective": "Compare CPU classifiers."},
    "Data": {
        "sources": ["data/input.csv"],
        "target": "label",
        "task_type": "classification",
    },
    "Features": {
        "include": ["x"],
        "exclude": ["id"],
        "guidance": "Use x.",
        "availability": "At prediction.",
    },
    "Evaluation": {
        "metric": "accuracy",
        "direction": "maximize",
        "split": {
            "strategy": "random",
            "time_column": None,
            "group_column": None,
            "validation_fraction": 0.25,
            "test_fraction": 0.25,
            "seed": 17,
            "constraints": "Fixed disjoint memberships recorded in data/split.json.",
        },
    },
    "Algorithms": {"mode": "compare", "allowed": list(parameters)},
    "Budget": {
        "max_trials_per_algorithm": 1,
        "max_total_trials": 3,
        "max_runtime_seconds": 60,
        "max_memory_mb": None,
        "max_cost": None,
        "currency": None,
    },
}
(root / "brief.md").write_text(
    "# Experiment: Classification\n\n"
    + "\n".join(
        f"## {name}\n```yaml\n{yaml.safe_dump(value, sort_keys=False)}```\n"
        for name, value in sections.items()
    )
)
(root / "notebook.ipynb").write_text(
    json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []})
)
(root / "experiment.yaml").write_text(
    yaml.safe_dump(
        {
            "schema_version": "1.0",
            "id": "classification",
            "brief": "brief.md",
            "search_space": "search.yaml",
            "notebooks": ["notebook.ipynb"],
            "working_directory": ".",
            "data": ["data/input.csv"],
            "execution": {"status": "configured"},
        }
    )
)
settings = {"candidates": ["decision_tree", "random_forest"], "quality_rules": []}
(root / "training.json").write_text(json.dumps(settings))
(root / "data").mkdir(exist_ok=True)
(root / "data/input.csv").write_text(
    "id,x,label\n0,-3.0,0\n1,-1.0,0\n2,1.0,1\n3,3.0,1\n4,-2.0,0\n5,2.0,1\n6,-100.0,1\n7,100.0,0\n"
)
_, partition = create_partitions(
    pd.read_csv(root / "data/input.csv"),
    row_id="id",
    target="label",
    layout="train_validation_test",
    memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
)
(root / "data/split.json").write_text(json.dumps(partition, allow_nan=False))
ignore = root / ".gitignore"
ignore.write_text(
    ignore.read_text() + "\n.training/\nrun-provenance.json\n__pycache__/\n"
)
command(sys.executable, "-m", "dvc", "add", "data")
command("git", "add", ".")
command("git", "commit", "-m", "feat: prepare classification example")
identity = json.loads((root / ".agentic-ml/init.json").read_text())["environment"][
    "toolkit_identity"
]
pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
provenance = {
    "schema_version": "1.0",
    "experiment": {
        "commit_sha": command("git", "rev-parse", "HEAD"),
        "entrypoint": ref("train.py"),
        "code": [ref("train.py"), ref("training_bindings.py")],
    },
    "configuration": {
        "files": [
            ref(name)
            for name in (
                "brief.md",
                "search.yaml",
                "experiment.yaml",
                "registry.yaml",
                "training.json",
            )
        ],
        "effective": settings,
    },
    "data": [
        {
            "metadata": ref("data.dvc"),
            "output_path": "data",
            "hash_name": "md5",
            "hash_value": pointer["md5"],
            "member_path": name,
        }
        for name in ("input.csv", "split.json")
    ],
    "split_record": ref("data/split.json"),
    "environment": {
        "lockfile": ref("uv.lock"),
        "python_version": sys.version.split()[0],
        "libraries": {
            name: version(name)
            for name in (
                "agentic-ml",
                "mlflow",
                "dvc",
                "pandas",
                "pyarrow",
                "scikit-learn",
                "numpy",
                "skops",
            )
        },
    },
    "toolkit": {
        "installation": identity,
        "repository_url": identity.get("url"),
        "commit_sha": identity.get("revision"),
        "build_identity": None,
    },
}
(root / "run-provenance.json").write_text(json.dumps(provenance, allow_nan=False))
uri = f"sqlite:///{root}/.agentic-ml/classification.db"
client = MlflowClient(tracking_uri=uri)
experiment = client.create_experiment(
    "classification-" + provenance["experiment"]["commit_sha"],
    artifact_location=(root / ".agentic-ml/classification-artifacts").as_uri(),
)
print(json.dumps({"tracking_uri": uri, "experiment_id": experiment}))
```

### train.py

<!-- project-file: train.py -->

```python
"""Train and record a baseline before authored classification candidates."""

import json
import sys
import traceback
from collections.abc import Mapping
from importlib.metadata import version
from pathlib import Path
from typing import cast

import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from training_bindings import ESTIMATOR_BINDINGS

from agentic_ml.data_quality import run_validated_step
from agentic_ml.planning import ResolveRequest, resolve_plan
from agentic_ml.splitting import create_partitions
from agentic_ml.tracking import log_preprocessing, log_run_results
from agentic_ml.training import fit_classifier
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    validate_configuration,
)


def record_model(
    root: Path,
    uri: str,
    run_id: str,
    candidate: CandidateRequest,
    *,
    baseline_run_id: str | None = None,
) -> None:
    """Fit, score and persist one model in the explicitly selected native run."""
    client = MlflowClient(tracking_uri=uri)
    native = client.get_run(run_id)
    if native.info.status != "RUNNING" or native.info.lifecycle_stage != "active":
        raise ValueError("Selected run must be active and RUNNING")
    stage = "inputs"
    try:
        settings = json.loads((root / "training.json").read_text())
        provenance = json.loads((root / "run-provenance.json").read_text())
        frame = pd.read_csv(root / "data/input.csv")
        partition = json.loads((root / "data/split.json").read_text())
        if partition["layout"] != "train_validation_test":
            raise ValueError(
                "Project comparison requires a separate validation partition"
            )

        def fit(
            checked: pd.DataFrame, _: dict[str, object]
        ) -> tuple[Pipeline, dict[str, object]]:
            return fit_classifier(
                checked,
                project_root=root,
                candidate=candidate,
                estimator_bindings=ESTIMATOR_BINDINGS,
                preprocessing=Pipeline([("scale", StandardScaler())]),
                partition_record=partition,
                selected_columns=["x"],
                output_schema=[{"name": "x", "dtype": "float64"}],
            )

        stage = "fit"
        (pipeline, record), quality = run_validated_step(
            frame, fit, rules=settings["quality_rules"]
        )
        partitions, _ = create_partitions(
            frame,
            row_id=partition["row_id"],
            target=partition["target"],
            layout=partition["layout"],
            memberships=partition["memberships"],
        )
        validation = partitions["validation"]
        predictions = pipeline.predict(validation[["x"]])
        score = float(accuracy_score(validation[partition["target"]], predictions))
        staging = root / ".training" / run_id
        staging.mkdir(parents=True, exist_ok=False)
        output = staging / "training.json"
        output.write_text(json.dumps(record, indent=2, allow_nan=False))
        model = staging / "pipeline"
        stage = "model serialization"
        mlflow.sklearn.save_model(
            pipeline,
            str(model),
            serialization_format="skops",
            skops_trusted_types=["numpy.dtype", "sklearn.tree._tree.Tree"],
            pip_requirements=[
                f"{name}=={version(name)}"
                for name in ("scikit-learn", "numpy", "pandas", "skops", "mlflow")
            ],
        )
        stage = "model publication"
        if client.list_artifacts(run_id, "model/pipeline"):
            raise FileExistsError("model/pipeline already contains artifacts")
        client.log_artifacts(run_id, str(model), "model/pipeline")
        stage = "preprocessing publication"
        log_preprocessing(
            run_id=run_id,
            pipeline=pipeline["preprocessing"],
            record=cast(Mapping[str, object], record["preprocessing"]),
            provenance=provenance,
            project_root=root,
            tracking_uri=uri,
        )
        parameters = {
            key: record[key]
            for key in (
                "algorithm",
                "estimator_class",
                "parameters",
                "parameter_origins",
                "versions",
                "fit_partition",
            )
        }
        if baseline_run_id is not None:
            parameters["baseline_run_id"] = baseline_run_id
        stage = "result publication"
        log_run_results(
            run_id=run_id,
            project_root=root,
            tracking_uri=uri,
            provenance=provenance,
            parameters=parameters,
            metrics={"validation_accuracy": score},
            outputs={"training": output.relative_to(root)},
            expected_outputs=["training"],
            process_exit_code=0,
            validation_passed=None
            if quality["status"] == "not_checked"
            else quality["status"] == "passed",
        )
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(
                f"classification run_id={run_id}; stage={stage}; project_root={root}"
            )
            diagnostic = root / ".training" / run_id / "failure.txt"
            try:
                diagnostic.parent.mkdir(parents=True, exist_ok=True)
                diagnostic.write_text("".join(traceback.format_exception(error)))
                error.add_note(f"Available local diagnostic: {diagnostic}")
                if not client.list_artifacts(run_id, "diagnostics"):
                    client.log_artifact(run_id, str(diagnostic), "diagnostics")
            except (OSError, ValueError, MlflowException) as secondary:
                error.add_note(f"Diagnostic retention failed: {secondary}")
            try:
                client.set_tag(run_id, "process_exit_code", "1")
                client.set_terminated(run_id, status="FAILED")
            except (OSError, ValueError, MlflowException) as secondary:
                error.add_note(f"Failed to record native FAILED status: {secondary}")


def run(root: Path, uri: str, experiment: str) -> dict[str, str | list[str]]:
    """Resolve genuine strict inputs, then finish baseline before candidates."""
    if not root.is_absolute() or not root.is_dir():
        raise ValueError("root must be an existing absolute project directory")
    plan = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    if plan.plan_id is None:
        raise ValueError(f"Plan resolution blocked: {plan.diagnostics}")
    configuration = validate_configuration(
        ConfigurationRequest(root, plan.plan_id, Path("registry.yaml"))
    )
    if configuration.validation_id is None:
        raise ValueError(f"Configuration blocked: {configuration.diagnostics}")
    client = MlflowClient(tracking_uri=uri)
    settings = json.loads((root / "training.json").read_text())
    baseline = client.create_run(experiment).info.run_id
    record_model(
        root,
        uri,
        baseline,
        CandidateRequest(root, configuration.validation_id, "dummy_classifier", {}),
    )
    candidates = []
    for algorithm in settings["candidates"]:
        run_id = client.create_run(experiment).info.run_id
        record_model(
            root,
            uri,
            run_id,
            CandidateRequest(root, configuration.validation_id, algorithm, {}),
            baseline_run_id=baseline,
        )
        candidates.append(run_id)
    return {"baseline": baseline, "candidates": candidates}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), sys.argv[2], sys.argv[3]), allow_nan=False))
```
