# Compare authored feature pipelines

The recipe passes US-14 Phase 2 checks; installed story-acceptance verification
remains pending. See the
[contract](../../docs/feature-pipelines.md) and
[phase evidence](../../docs/verification/us-14-ip2.md) for current verification.

Use a separate initialized experiment project with its own locked environment
and a normal installed `agentic-ml` dependency. Follow
[experiment setup](../../docs/experiment-setup.md); initialization drafts are
not strict comparison inputs.

Copy all three Python files from this directory into the project root. Do not
import from a toolkit source checkout. Configure Git identity in that project
before preparation; preparation creates an explicit fixture commit. It refuses
existing comparison inputs, so use a fresh project for this example.

```sh
/absolute/project/.venv/bin/python /absolute/project/prepare_comparison.py /absolute/project
```

Preparation creates a tiny controlled dataset, original train/validation/test
split, strict configuration, input DVC pointer and matching committed provenance.
It prints an explicit tracking URI and native experiment ID. Substitute those
values in this command; every flag is required:

```sh
/absolute/project/.venv/bin/python /absolute/project/compare_features.py \
  --project-root /absolute/project \
  --tracking-uri 'TRACKING_URI_PRINTED_BY_PREPARATION' \
  --experiment-id 'EXPERIMENT_ID_PRINTED_BY_PREPARATION' \
  --settings comparison-settings.json
```

Run from any cwd. Settings paths resolve against the root. Each variant uses
the same depth-1 decision tree, seed 17 and original split. The numeric reference,
signal, equivalent and misleading alternatives have validation accuracies
0.5, 1.0, 0.5 and 0.0: reference, gain, tie and regression. Model quality does
not determine process success. Final-test rows are not transformed or scored.

The script prints a comparison table to stderr and one machine-readable JSON
object to stdout, with reference/variant run IDs and the comparison artifact URI.
Use the same explicit MLflow store to inspect those runs, their metrics,
`model/pipeline`, `preprocessing`, `provenance.json` and named `outputs/` artifacts.
The reference owns `outputs/comparison/comparison.json`.

Local training/model diagnostics live under `.feature-comparison/`. Derived
feature Parquet files live under `features/<reference-run-id>/<variant>/`, with
separate adjacent native `.dvc` pointers. Inspect `dvc status` before explicitly
committing the new pointers and generated ignore entries. The recipe versions
derived content locally; it does not push DVC data, commit comparison outputs,
run a stage scheduler or demonstrate clean-project replay.

Edit `feature_variants.py:get_variants()` to author alternatives. It takes no
arguments and returns fresh unfitted pipelines plus ordered selected columns
and output schemas. A single pipeline can compose scaled/unscaled numeric
groups and predeclared categorical encoding. Select its names in settings and
update strict feature/budget declarations and committed provenance accordingly.
The factory also supplies `mixed_scaled` and `mixed_unscaled`, combining numeric
imputation with/without scaling, unscaled counts and predeclared categorical
encoding. The example's preparation script is a controlled fixture, not a converter for
arbitrary user datasets.

On failure, inspect nonzero exit output, run status and available local/native
diagnostics. A failed comparison can retain finished candidate runs; do not
interpret the presence of a partial summary as successful completion.
