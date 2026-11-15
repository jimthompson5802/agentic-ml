# Classification training contract

Status: **Contract approved at US-18 Gate 1; fitting implemented with local IP2
verification, 2026-11-15 UTC. Gate 2 approved, 2026-11-15 UTC.**
Developer decision: “i approve phase 1”. This confirms the revised
validate-then-construct interface, public test boundaries and explicit bounded
tree-storage persistence choice. `fit_classifier` has focused local evidence in
the [IP2 report](verification/us-18-ip2.md). Project recording, persistence
integration and normal installed wheel verification remain IP3/IP4 work.
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

Phase 3 will deliver the complete copyable `train.py`. The following is its
required execution outline, not a runnable initializer output today:

1. Load explicit project paths, reviewed strict inputs, additive metadata,
   extraction data and the saved partition record. Use current public strict
   planning/configuration APIs to obtain genuine validation identities.
2. Apply configured quality checks with `run_validated_step` around dependent
   training. Required failure blocks training; empty rules mean `not_checked`.
3. Create the baseline's native run in an explicit store. Invoke the proposed
   helper with the baseline class binding and candidate request. The toolkit
   validates, constructs and fits the baseline from its effective parameters. Predict only
   validation features; compute native `accuracy_score`.
4. Save the complete model under a fresh project-local staging directory with
   `mlflow.sklearn.save_model`. Use explicit `serialization_format="skops"` and
   the proposed bounded trust list below, with explicitly pinned model dependency
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

### Proposed persistence decision requiring Gate 1 approval

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
This is a proposed bounded serialization decision, not an implemented workaround.

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
guards. Normal installed wheel paths, baseline-order recording, persistence
integration and configured/operational tracking failures remain IP3/IP4 work.
No user-story acceptance or additional platform certification is claimed.
