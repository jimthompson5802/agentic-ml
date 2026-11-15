# US-18 Implementation Phase 3 evidence

2026-11-15 UTC. **IP3 technically Complete; Gate 3 Approved, 2026-11-15 UTC.**
Owning [plan](../plans/milestone-1-us-18.md), [issue #28](https://github.com/jimthompson5802/agentic-ml/issues/28),
and [runnable contract](../classification-training.md). This advances AC-01's M1
classification portion and AC-02/03/04; it does not accept the story or regression.

## Authorization, scope and public boundaries

Developer “start phase 3” authorized this phase after Phase 2 commit `c74d76b`.
The initial issue refresh failed because GitHub CLI lacked authentication.
Developer “try again” resumed the same authorization. The full issue body and
one unique comment were retrieved successfully, with unchanged count and
`updated_at` (`2026-11-07T00:29:21Z`) on the final metadata refresh. The issue
is open, with no GitHub milestone field; its body assigns classification to M1,
regression to M2 and AC-02–04 to M1. The current repository verification policy
supersedes the issue's older current-milestone gate wording, as already recorded
in the approved plan. No scope change was needed.

Gate 1 confirmed these boundaries: genuine strict plan/configuration/candidate
APIs, `fit_classifier`, configured quality checks, public tracking APIs, native
MLflow run/artifact inspection and fresh native model load/predict. Project code
owns run creation, baseline order, scoring, full model persistence and failures.
No new toolkit tracking wrapper, estimator-specific branch, resource, dependency,
registry service, run state machine or CLI was added.

`tests/installation/training_project.py` is copied into the experiment as
`train.py`; `training_bindings.py` supplies dummy/tree/forest native classes.
The guide contains the identical scripts plus a complete, executable preparation
recipe for strict inputs, static scalar profiles, DVC data and committed
provenance. Tests execute the literal guide blocks in the separate project.
Source/configuration/lock/data references are real, rather than fabricated
installation identities or caller assertions.

## Observable results

- Baseline and candidate each have one authoritative native run. Baseline is
  FINISHED before the candidate starts; the candidate records its baseline ID.
  The same rows/features and accuracy metric produce literal scores 0.5 and 1.0.
  A completed low baseline score remains a valid FINISHED experiment.
- Dummy, tree and project-only forest fitted Pipelines are saved with native
  MLflow/skops, downloaded and loaded in fresh experiment interpreter processes.
  Predictions are exactly `[0, 0]`, `[0, 1]`, `[0, 1]`. The restored training-only
  scaler transforms `[0, 100]` to `[0, 100/sqrt(5)]`, with `rtol=atol=1e-12`.
  Complete effective parameters, class identities, origins and versions match
  the native run and restored estimator. Forest adds no toolkit wiring/rebuild.
- Native model flavors record skops and the explicitly approved bounded trust
  list, `numpy.dtype` and `sklearn.tree._tree.Tree`. Requirements pin observed
  libraries, including skops/MLflow. No broader trust or pickle fallback exists.
- The training record's nested preprocessing record equals the separately
  downloaded preprocessing metadata. Saved partition memberships, feature/schema
  declarations and source identity agree. Shared provenance equals independently
  hashed files and real committed Git blobs, with native DVC pointer/content and
  locked installed-package identities checked by the existing public consumers.
- Native baseline fit failure becomes FAILED with original exception/stage
  context and no candidate run. Real serialization failure, model/output
  collisions, missing output, invalid committed reference and a filesystem
  upload failure also remain FAILED. Prior artifacts retain their exact bytes;
  available local model/record/diagnostic files remain available. A secondary
  diagnostic-upload error does not replace the original storage error.
- Required quality failure prevents fitting/model publication and candidate
  creation. Advisory failure permits FINISHED execution tagged with failed
  validation. Explicit empty rules record `not_checked`. No test-partition score
  or feedback into fitting/comparison is introduced.

## TDD and failure history

Individual serial checks were used for small TDD slices and diagnosis; the gate
checks below use four workers/loadgroup. Original failures remain in raw logs.

| Slice / log | Red or initial observation | Change and verified outcome |
|---|---|---|
| `01-red.log` | Script absent; public invocation could not open `train.py` | Added minimum baseline/candidate composition and native publication |
| `01-green.log` | Source identity mismatch during first green check | Fixture had generated splits with development pandas 3.1.0, while its native project resolved 3.1.1. Generate the split from saved CSV using the owning experiment interpreter; `01-green-source-renewal.log`: 1 passed |
| `02-native-persistence.log` | Regression/extension checks of the just-implemented persistence path | 1 passed: complete dummy/tree/forest artifacts, fresh native inference, independent parameters/lineage; no artificial red introduced for existing behavior |
| `03-red-fit.log` | Initial test expected different capitalization in native error text | Corrected to the exact native ValueError wording without changing the fit/status criteria |
| `03-red-fit-native-message.log` | Genuine required-behavior red: baseline remained RUNNING after native fit error | Added project-level staged failure/diagnostic finalization; `03-green-fit.log`: 2 passed, including normal recording regression |
| `04-serialization.log` | Test initially expected TypeError; MLflow actually wraps the skops untrusted-lock failure in MlflowException | Assert exact native wrapper and `_thread.lock` cause; no serializer change. `04-serialization-native-message.log`: 1 passed |
| `05-collision.log`, `06-publication-failures.log`, `08-output-collision.log` | Additional failure regressions against implemented finalization | 1, 3 and 1 passed respectively; native filesystem failures, original errors and artifact retention inspected |
| `07-quality.log` | Required case passed; next parametrized case hit cached SQLite URI reuse during fixture setup | Give each case a unique native store, following existing tracking fixture isolation; `07-quality-isolated-store.log`: 2 passed |
| `09-red-documentation.log` | Copyable complete recipe absent | Added complete executable guide blocks |
| `09-green-documentation.log` | Recipe trained correctly, but inspection used development MLflow against the newer experiment-created schema | Inspect using the experiment's own native MLflow in a fresh process; `09-green-documentation-native-inspection.log`: 1 passed; four-worker renewal below also passed |

Each identified fixture/assertion correction took one corrective attempt and
passed renewal against its original requirements. No unresolved three-attempt
problem, changed acceptance threshold, skipped test, suppression, mock of an
internal collaborator or broadened persistence trust was introduced.

Serial commands used the form `uv run --locked pytest SELECTORS -q`, from this
worktree, with stdout/stderr saved to the table's log. Exact selectors were:

```text
01: tests/integration/test_training_tracking.py::test_records_baseline_before_candidate
02: tests/integration/test_training_tracking.py::test_loads_native_models_and_records_project_forest
03 red: tests/integration/test_training_tracking.py::test_failed_baseline_blocks_candidate_comparison
03 green: tests/integration/test_training_tracking.py::test_failed_baseline_blocks_candidate_comparison tests/integration/test_training_tracking.py::test_records_baseline_before_candidate
04: tests/integration/test_training_tracking.py::test_serialization_failure_preserves_training_output
05: tests/integration/test_training_tracking.py::test_model_collision_preserves_existing_artifacts
06: tests/integration/test_training_tracking.py::test_missing_training_output_fails_run tests/integration/test_training_tracking.py::test_invalid_provenance_fails_without_candidate tests/integration/test_training_tracking.py::test_native_upload_failure_retains_model_and_original_error
07: tests/integration/test_training_tracking.py::test_configured_quality_is_distinct_from_process_status
08: tests/integration/test_training_tracking.py::test_training_output_collision_preserves_prior_bytes
09: tests/integration/test_training_tracking.py::test_documented_recipe_runs_from_unrelated_cwd
```

The three `01` invocations additionally used `--keep-test-workspaces`. Subsequent
checks used normal workspace retention; durable logs remain outside those roots.

The initial strict type check found an inferred heterogeneous profile mapping
and missing upstream sklearn metric typing. Added an explicit JSON profile type
and the exercised public `accuracy_score` signature in contributor-only stubs;
these do not ship in the wheel. Renewed strict checks pass. Initial lint import
ordering was corrected. Initial shared formatting found the guide's preparation
code fence unformatted; native Ruff formatted it, then the full formatting check
passed. All three guide blocks retain identical Python ASTs after formatting;
train/bindings still exactly match the tested source files.

## Gate verification

From `.worktrees/US-18-classification`:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_tracking.py tests/integration/test_preprocessing.py tests/integration/test_dataset_versioning.py --junitxml=.dev-records/verification/us18-ip3-20261115-c74d76b/focused.xml
```

**259 collected/selected, 259 passed, 0 failed/errors/skipped/deselected**, 342.66
seconds. This run preceded addition of the executable-guide case. Module counts:
training 45, preprocessing 84, dataset versioning 2, tracking 117, new training
tracking 11. Validation integration itself did not change; IP2's configuration
regressions remain valid and no extra validation selection was needed.

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training_tracking.py::test_documented_recipe_runs_from_unrelated_cwd --junitxml=.dev-records/verification/us18-ip3-20261115-c74d76b/documentation.xml
```

**1 collected/selected, 1 passed, 0 failed/errors/skipped/deselected**, 26.18
seconds. Combined valid gate evidence covers **260 distinct tests** across these
two invocations; no single 260-test run is claimed. Later guide-only formatting
preserved executable ASTs and did not invalidate passing behavior evidence.
The full regression run emitted two upstream SQLAlchemy deprecation warnings;
no warnings were suppressed.

Shared checks: locked development synchronization, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked mypy src tests` (96 source files),
`uv run --locked agentic-ml --version` (`0.1.0`) and `git diff --check` all passed.
`uv run --locked ruff format --check .` passed on renewal after formatting the
guide. Exact commands/results are in `shared-commands.json` and logs; the initial
format failure remains recorded. No checks were disabled. Local document paths,
executable block compilation, source/block equality and post-format AST equality
also pass; external links and anchor existence were not independently checked.

Lock SHA-256 before/after:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
No dependency/lock changes. Development platform: Linux aarch64, Python 3.12.16,
pytest 9.1.1, xdist 3.8.0, sklearn 1.9.1, MLflow 3.17.2, skops 0.16.0,
pandas 3.1.0, numpy 2.5.4, pyarrow 25.0.1, DVC 3.67.1. Separate normal-wheel
projects resolve and record their own locked runtime versions; they are not
assumed identical to this editable development environment. This evidence does
not establish macOS/Windows behavior or cross-version database compatibility.

## Retained evidence and implementation identity

Raw records:
`.dev-records/verification/us18-ip3-20261115-c74d76b/`.
The directory retains red/green/failure/gate logs, JUnit XML, native invocation
snapshots (including run status/parameters/metrics), issue snapshots, shared
commands, lock/platform/version identities and guide-format evidence. Reused
native fixture-command support additionally retains commands/stdout/stderr under
`.dev-records/verification/us26-ip2-native-commands/`; its inherited US-26 label
identifies the helper's origin, not ownership of this phase. Pytest fixture
workspaces follow normal retention and are not durable evidence locations.

Base implementation is `c74d76b6ad5d38db19b35a46e727b35b9616654c`. Phase changes:
project training/bindings scripts, integration tests, metric contributor typing
and its register, runnable contract, this report, owning plan and checkpoint.
No installable-package code or packaged resource changed in IP3. The developer authorized the local Phase 3 commit with Gate 3 approval;
no push/publication occurred.

## Gate 3 and remaining owners

IP3-T1/T2/T3/T4 are technically Complete. **Gate 3 is Approved**, 2026-11-15 UTC.
Developer “i approve gate 3; commit changes” approved the phase and authorized
its local commit, with no requested changes. Verification evidence remains
unchanged. IP4 start and push/publication are not authorized.

IP4-T1/T2 still own final direct-wheel and genuinely sdist-rebuilt-wheel installed
verification, including the same script/extension and required installed fitting
boundaries. IP3's native wheel fixtures do not substitute for that matrix.
IP4-T3 owns final M1–6 selection and story-check reconciliation. No M1–6 acceptance
run, complete suite, standalone artifact driver, notebook execution, DVC stage
scheduling, assistant walkthrough, final-test evaluation, M2 restoration or
milestone/story acceptance is claimed. Regression AC-01 remains M2 and #28 stays
open. Historical M1/M50 obligations remain unchanged.
