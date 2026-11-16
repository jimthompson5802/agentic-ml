# Authored feature comparison

Status: **US-14-IP1 contract v2 Approved**, 2026-11-15 UTC, by developer
“yes i approve contract v2”, including public test boundaries. The project-owned recipe is implemented and its Phase 2 checks pass.
Both normal wheel paths and final story checks are verified in IP3;
the developer accepted all five US-14 criteria on 2026-11-16 UTC. The
[plan](plans/milestone-1-us-14.md) owns execution and approval; the
[IP1 evidence](verification/us-14-ip1.md) records bounded native feasibility.

## Project boundary and preparation

Copy the `examples/feature-comparison/` files into a separate initialized
experiment project with a normal installed toolkit dependency and its own locked
environment. Use the [installed setup](experiment-setup.md) and the accepted
[classification preparation pattern](classification-training.md#runnable-project-example).
Project source imports only installed public toolkit interfaces and native
libraries. No new toolkit API or CLI command is proposed.

The example contains these authoritative source files:

| File | Responsibility |
|---|---|
| `prepare_comparison.py` | Create the controlled input, original three-way split, complete strict 1.0 brief/search/experiment/registry inputs and settings; DVC-add input data; commit project sources/configuration/lock/input pointers; produce matching run provenance and explicit MLflow experiment ID |
| `feature_variants.py` | Authored native preprocessing declarations and the fixed DecisionTreeClassifier binding/profile |
| `compare_features.py` | Validate inputs; fit, score, persist and publish the declared variants using installed interfaces |
| `README.md` | Exact setup, preparation, invocation and native inspection instructions |

Preparation uses the project interpreter, an existing absolute initialized root
and its verified toolkit installation identity. It prints `tracking_uri` and
`experiment_id`, as in classification preparation. Its controlled fixture has
eight rows with IDs 0–7, train 0–3, validation 4–5 and final test 6–7. The plan's
independent numerical matrix specifies values and labels. Preparation is an
explicit scientist action and may create a fixture commit; comparison itself
does not commit or initialize projects. It must not overwrite existing inputs.

The complete strict inputs declare classification, one `decision_tree` algorithm,
fixed depth 1 and seed 17, no parameter search and the selected metric/direction.
All other native scalar defaults are statically authored using the accepted
US-18 tree profile; the helper still verifies them against the actual native
class. Feature include declarations cover the union of authored selected columns,
excluding ID/target. Budget values cover the explicitly selected variants;
reject a variant count exceeding either declared total or per-algorithm limit.
This is explicit iteration, without search or resource enforcement.

Preparation records code, configuration, dependency lock and source/split DVC
pointers at the real experiment commit, then writes `run-provenance.json` using
the accepted tracking provenance schema. This generated document is an input,
not fabricated strict plan evidence. Compare resolves a genuine plan and validates
configuration with public APIs before constructing CandidateRequest.

## Invocation and settings

```sh
/absolute/project/.venv/bin/python /absolute/project/prepare_comparison.py /absolute/project
/absolute/project/.venv/bin/python /absolute/project/compare_features.py \
  --project-root /absolute/project \
  --tracking-uri 'sqlite:////absolute/project/.agentic-ml/comparison.db' \
  --experiment-id 'ID_PRINTED_BY_PREPARATION' \
  --settings comparison-settings.json
```

All four comparison flags are required. The root must be an existing absolute
directory; the explicitly selected native experiment must exist and be active.
The recipe uses root for subprocess cwd and input resolution while preserving
the caller cwd. Input paths are root-relative regular files; reject absolute,
escaping, symlink and conflicting output paths. Tracking uses the explicit URI,
with local SQLite/artifact storage verified in this story.

Settings v1 have exactly these keys (unknown keys fail):

```json
{
  "schema_version": "1.0",
  "experiment": "experiment.yaml",
  "registry": "registry.yaml",
  "source": "data/input.csv",
  "split_record": "data/split.json",
  "provenance": "run-provenance.json",
  "algorithm": "decision_tree",
  "parameters": {},
  "variants": ["reference", "signal", "unchanged", "misleading"],
  "reference": "reference",
  "metric": "accuracy",
  "direction": "maximize",
  "quality_rules": [],
  "expected_outputs": ["training", "train_features", "validation_features", "derived_dvc"]
}
```

`parameters` supplies scalar candidate overrides within strict fixed settings;
the effective settings must be identical for every variant. Variant names must
be nonempty, unique names present in `feature_variants.py`; reference must be
included. Execute reference first, then the remaining selected names in settings
order. No serialized class imports, inferred candidates or custom transformers.
Declarations come from the factory defined below and contain native Pipeline,
ordered selected columns and ordered output schema. Numeric variants use StandardScaler; `unchanged` explicitly uses
`with_mean=False`. Mixed coverage uses ColumnTransformer, mean SimpleImputer,
StandardScaler and dense OneHotEncoder with predeclared categories and unknown
categories ignored. Schema discovery from fitted data is not included.

Accept only (`accuracy`, `maximize`) and (`zero_one_loss`, `minimize`), agreeing
with strict resolved evaluation settings. Use sklearn's accuracy_score and
normalized zero_one_loss with default unweighted semantics. Scores/deltas must be
finite plain JSON numbers; no quality threshold or silent epsilon. Empty quality
rules retain `not_checked`; required failures stop fitting, advisory failures
remain recorded separately from process success and model quality.

Preflight all variant names, selected declarations, strict identities, budget,
selected schema declarations,
three-way split and input availability before creating runs. Reuse accepted
public validation/fit checks for source identity, complete disjoint membership,
feature availability, ID/target exclusion, schema and native candidate errors.
No run created on preflight failure; checks requiring transformed data or native
publication can fail later and retain partial evidence. Do not claim every native
fit failure can be detected before fitting.

## Factory contract: approved decisions

Developer “let's stay with predeclared” and “i accept these recommendations”
settled these decisions on 2026-11-15 UTC. Those messages approved this factory boundary; subsequent full contract v2
approval is recorded above.

The comparison script imports `get_variants` from the fixed project file
`feature_variants.py` and calls it once, without arguments. It returns a Python
list of plain dictionaries, one per explicitly authored variant. Each call
constructs fresh, unfitted native pipelines; it does not load data, fit, score
or publish. Helpers and optional TypedDict declarations stay in that same
project file; no new toolkit type is introduced.

Each selected dictionary has exactly these fields:

| Field | Required value |
|---|---|
| `name` | Nonempty unique string, used by settings for selection |
| `selected_columns` | Nonempty ordered list of unique input column names, excluding ID/target |
| `pipeline` | Fresh, unfitted native sklearn Pipeline |
| `output_schema` | Nonempty ordered list of `{name, dtype}` dictionaries, using existing preprocessing schema rules |

Schema names are project-assigned labels mapped to transformed columns by
position; they need not match sklearn-generated feature names. They must be
unique and must not collide with the row-ID column. Width and dtypes must match
actual transformed output. Selected OneHotEncoder steps declare categories
explicitly, rather than `categories="auto"`. This keeps output width/order
predictable without learning a schema from validation or test rows.

Check the factory return is a list of dictionaries and validate every `name`
for presence, type, nonemptiness and global uniqueness. Reject unknown selected
names or an absent reference. Fully validate the remaining fields only for
selected declarations: malformed pipeline/schema/columns in an unselected
variant do not block the selected comparison. Execution order follows settings,
with reference first, rather than factory list order.

All factory code still executes to construct the list. A construction/import
exception propagates before selection, even when it originated in an unselected
variant; this interface does not provide lazy construction or fault isolation.

Verification adds factory shape/name/selection negatives, fresh unfitted
instances across calls, valid selection with malformed unselected fields,
positional output labels differing from sklearn names, and predeclared category
width/order with ignored unseen validation categories. Observe public outputs
and native fitted state; do not assert private helper sequences.

## Fit, outputs and lineage

For each variant use `run_validated_step` and `fit_classifier` with the same
frame, original partition record and CandidateRequest. Each helper call constructs
a fresh classifier and clones preprocessing. Retain unmodified training and
preprocessing records. Transform only recorded train/validation rows with fitted
preprocessing; predict/score only validation rows. Do not transform, predict or
score final-test rows. Their membership/source identity remains in the original
record. This is a supported-path rule, without OS isolation claims.

Create `.feature-comparison/<reference-run-id>/<variant>/` with exclusive file
creation. Persist `training.json` and `train_features.parquet` /
`validation_features.parquet` under a separate
`features/<reference-run-id>/<variant>/` directory. Feature files contain the original row-ID column
followed by declared feature columns in exact membership order; reject output
feature names colliding with the ID. Verify width, dtype, membership and
availability before publication. Numeric comparisons in verification use
`rtol=atol=1e-12`; IDs, labels, schema, scores and outcomes use exact expectations.

Native `dvc add` versions each `features/<reference-run-id>/<variant>/` directory separately from input
`data.dvc`; keep its pointer outside the DVC output and save a pointer copy as
`derived.dvc` for publication. Only feature data enters that output, avoiding
recursive pointer/versioning of model staging. Verify native `dvc status` and
record exactly `output_path`, `hash_name`, `hash_value`, `metadata` (a
`{path, sha256}` pointer reference), and `members` (ordered relative member paths).
Pointers reside at `features/<reference-run-id>/<variant>.dvc`, outside the
ignored staging tree; allow DVC to write its normal feature-content ignore entries.
Do not rewrite the input/source split references or claim a derived pointer is
already committed. The scientist subsequently commits new derived pointers and
ignore entries explicitly; no clean-project replay is established by this story.

Each variant has one native MLflow run with `model/pipeline`, `preprocessing`,
shared `provenance.json`, validation metric `validation_<metric>`, fixed estimator
settings and `reference_run_id` / variant name. Save the fitted model through
native MLflow sklearn skops persistence with only the US-18 reviewed
`numpy.dtype` and `sklearn.tree._tree.Tree` trust list. Preserve dependency pins.
Do not broaden deserialization trust after errors.

Use `log_preprocessing` while RUNNING, then `log_run_results` once for finalization.
Required output names above map to `outputs/<name>/<filename>`; `training`
contains `training.json`, feature names their Parquet files, and `derived_dvc`
the pointer copy. Shared provenance retains committed code/config/lock/toolkit,
source/split DVC pointers and installed library identities. The generated DVC
reference is additional output evidence, not a replacement input identity.

## Comparison artifact and completion

Hold the reference RUNNING after fitting/persistence/preprocessing publication.
Finalize each candidate with its outputs/metrics. After all candidates finish,
write `comparison.json` locally and pass it as additional required output
`comparison` to the reference's single `log_run_results` call, alongside its
normal outputs. Thus `outputs/comparison/comparison.json` is uploaded before
reference finalization, without reopening any run or adding a workflow database.

Comparison JSON v1 has exactly these top-level keys:

| Key | Value |
|---|---|
| `schema_version` | `"1.0"` |
| `reference` | `{ "variant": <name>, "run_id": <native ID> }` |
| `source` | Exact original partition record `source` object |
| `split_record` | Existing `{path, sha256}` file reference |
| `estimator` | `{algorithm, estimator_class, parameters, validation_id}` copied from the common training protocol |
| `metric`, `direction` | Selected supported strings |
| `validation_membership` | Ordered IDs from original split record |
| `rows` | Ordered objects described below, reference first |

Every row has exactly `variant`, `run_id`, `score`, `raw_delta`, `adjusted_delta`,
`outcome`, `outputs`, `artifacts`, `derived_data`. `raw_delta = score - reference
score`; `adjusted_delta` equals raw delta for maximize, its negative for minimize.
Reference has zero deltas and outcome `reference`. Other outcomes are `gain`,
`tie`, `regression` for positive, zero and negative adjusted delta respectively.
Do not report winners or final-model selection.

`outputs` maps the four required logical names to `{path, sha256}` local file
references. `artifacts` maps those names plus `model`, `preprocessing`,
`provenance` to native artifact URIs. `derived_data` contains the native DVC
output/hash/pointer/member fields defined above. The reference row uses
deterministic native artifact destinations before final publication; verify all
destinations exist before returning success. This avoids a self-referential
comparison digest or a second publication. The summary's own URI is returned
separately, not embedded in its rows.

Before writing the summary, compare actual persisted records for identical source,
split, validation IDs/membership, estimator class/effective parameters and metric
protocol; a mismatch fails. This recipe does not accept arbitrary historic runs.
Success exits zero and prints one JSON object containing `reference_run_id`,
ordered `variant_run_ids` (name to ID), and `comparison_artifact_uri`. Print a
human-readable table to stderr with variant, score, adjusted delta and outcome.

Failures exit nonzero, preserve the original exception and add run/stage/path
notes. Preserve available staging files and finished candidate runs. Attempt
diagnostic upload and FAILED for still-eligible RUNNING runs independently,
retaining secondary errors as notes. Do not reopen or mark finished candidates
FAILED. A failed reference prevents candidate execution; a later candidate,
required output, DVC or publication failure prevents a successful summary result.
There is no atomic rollback, hard-kill guarantee or automatic resume. A partial
summary upload is evidence to inspect, not proof of comparison completion.

## Approved public verification boundaries

IP2 invokes the exact copied entrypoint in a separate committed experiment,
through installed public fit/validation/tracking interfaces. Inspect native
MLflow records, model predictions, Parquet values and DVC pointers with literal
independent expectations. Do not mock internal fit/publication sequencing.
Require reference RUNNING while candidates finish and FINISHED only after summary
publication; never infer correctness from status alone.

Cover both metric directions, reference/gain/tie/regression; nondefault caller
cwd/index; unchanged caller objects; train-only scaler/imputer/category behavior;
mixed dense outputs and schema; settings/budget failures; overlap/two-way/stale
split failures; missing source, columns, committed/DVC reference or expected
output; artifact collisions; native transform and publication errors with partial
evidence. The plan owns the exact numerical matrix and negative selections.
Use actual native failures, not internal helper-call assertions.

IP3 repeats the copied recipe on direct and genuinely rebuilt-from-sdist wheels
with separate normal runtime-only project environments, independent outputs,
CLI/import/resource inventories and representative failures. IP2 does not cover
that packaging boundary; native IP1 probes cover neither installed toolkit
behavior nor acceptance. M2 restoration, native stage scheduling, final-test
evaluation and external assistant demonstrations remain with their owning stories.
