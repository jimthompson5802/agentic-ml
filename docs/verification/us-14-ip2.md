# US-14 Implementation Phase 2 evidence

Status: **Complete — Automatic — verification passed**, 2026-11-15 UTC. Developer “start phase 2” authorized IP2; “yes i approve
contract v2” approved the contract and public test boundaries, 2026-11-15 UTC.
[Plan](../plans/milestone-1-us-14.md), [contract](../feature-pipelines.md).

## Scope, environment and boundaries

Owning checkout: `.worktrees/US-14-feature-pipelines`, branch
`US-14-feature-pipelines`, starting revision
`a86f36f7f52f6de4f0754fe6ca68e5b17ba4f582`. The registered primary checkout and
common Git directory were verified; no fetch, merge or sibling mutation.
Only this story's `.venv` is used; inherited VIRTUAL_ENV is cleared. Locked
synchronization passed. Issue #20 body/all comments/final metadata were
refreshed: one unique comment, stable updated_at 2026-11-15T20:05:03Z, all five
criteria remain M1. No GitHub write was performed.

Tests invoke the exact copied preparation/comparison scripts in a separate normal
wheel-installed project, away from its cwd. Native MLflow APIs, model inference,
Parquet and DVC provide observations; expectations are literal, not produced by
the comparison logic. This covers the approved public boundary, not internal
call sequences. Direct/rebuilt-wheel acceptance and full final verification
remain IP3; no M2, assistant, notebook or other-platform claim.

Raw records: `.dev-records/verification/20261115T204632Z-a86f36f-us14-ip2/`.
`commands.json` records commands, cwd, exit codes and timing; `logs/` retains full
stdout/stderr and copied-recipe invocations. Per-invocation logs have unique names.
Do not delete prior red or failed evidence. All pytest runs use four workers and
loadgroup; shared installed-project fixture consumers remain in one group.

## TDD slices

| Slice | Red evidence | Green evidence | Coverage |
|---|---|---|---|
| Reference/signal | `t1-red`, one intended missing-recipe setup assertion; independent installed project setup itself succeeded | `t1-green-attempt1`, 1 passed | AC-01/02/03/05: accuracy .5/1, gain .5, predictions [0,0]/[0,1], same fixed parameters and original split, independent scaler values and row order |
| Four variants and metric directions | `t2-matrix-red`, two expected missing-variant failures; 130 other tests passed including all selected training/preprocessing regressions | `t2-matrix-green-fixture1`, 3 passed | AC-03/05: reference/gain/tie/regression for accuracy/maximize and loss/minimize |

The first slice implements its required persistence/publication happy path so
the public comparison artifact is observable. At that initial slice, IP2-T3/T4 still owned their stronger
boundary/failure verification and any corresponding missing behavior. Passing
happy-path logging alone does not establish those tasks complete. No assertions,
timeouts, suppressions or skips were weakened or added.

The sections below retain the incremental history. Final phase verification is
complete as recorded at the end; whole-story acceptance remains pending.

Fixture correction attempt 1: `t2-matrix-green` passed two cases, then failed
setup when a reused native SQLAlchemy store saw an earlier experiment after
successful owned-tree cleanup. Gave each native database/artifact root a UUID
child, matching existing tracking fixture isolation; assertions remain unchanged.
Rerun `t2-matrix-green-fixture1` passed all 3 unchanged cases.

Settings preflight: `t2-settings-red` had 10 intended failures (accepting invalid
settings or creating a run before rejection). Direct command
`uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_feature_comparison.py`
then passed all 13 cases; complete combined tool output is retained in
`logs/t2-settings-green-direct.log`. At developer direction, subsequent tests run
as direct uv commands; the check runner is no longer used.

Factory slice: `t2-factory-red` completed with 4 intended failures and 1 passing
unselected/fresh-factory case. Added global shape/name checks and selected
pipeline validation; `t2-factory-green` passed all 5 unchanged behavior cases.
Tool output is retained separately in matching `.log` files.

Mixed-feature slice: `t3-mixed-red` failed both expected missing declarations;
`t3-mixed-green` passed both mixed scaled/unscaled cases. Literal imputation,
encoding, schema names/dtypes and row order pass. Final-test infinities remain
untransformed. Added per-invocation recipe/input snapshots for subsequent cases.

Data/feature preflight: `t3-boundaries-red` had 6 intended failures and 1 passing
overlap rejection. Added three-way/source/column/schema/category checks before
run creation; `t3-boundaries-green` passed all 9 boundary and mixed cases.

Native failure lifecycle: `t4-failure-red` failed both cases because unfinished
runs stayed RUNNING. Added guarded diagnostics and FAILED finalization while
preserving finished runs and the primary error. `t4-failure-green` passed both
original cases. Evidence-damage cases additionally exercise existing happy-path
publication guards and accepted toolkit output/provenance checks; they require
no fabricated red where the required behavior is already present. Faults mutate
only copied experiment source/files and native destinations, never toolkit code
or mocked internal collaborators.

`t4-lineage-and-damage`: 5 passed, 1 failed. The existing tracking helper
preserved an available comparison JSON as partial evidence after a required
reference output was removed. Correction attempt 1: validate all required files
in the project finalization step before invoking the helper, preserving the
original no-summary-on-missing-output assertion. Local partial evidence remains
retained, with no atomicity claim. Original test and AC expectations unchanged.

Missing-output correction attempt 1 passed the original six-case selection:
`t4-lineage-damage-correction1`, 6 passed. Model collision preserved prior bytes;
missing source/DVC and corrupt committed references failed without a successful
comparison. Native artifacts, hashes, fitted/preprocessing records, committed
code/config/lock and reference/candidate finalization ordering were inspected.

Further protocol boundaries: `t4-effective-red` exposed acceptance of stale
effective settings; `t4-effective-green` passed after comparing consumed settings
to provenance. `t4-dotted-name-red` exposed suffix replacement in native DVC
pointer lookup; appending the native .dvc suffix fixed it, with both dotted-name
and effective-settings cases passing in `t4-dotted-name-green`.

`t5-explicit-store-red` exposed a blank URI falling back to the ambient store
before helper rejection. Added nonempty explicit URI preflight; its green and
quality/preparation regression evidence belong to the final focused run.

Initial example-only mypy found missing third-party metric declaration, local
type inference issues and untyped editable-package imports. Correction attempt
1: add the reviewed native zero_one_loss contributor declaration, retain explicit
record types/casts, and include src targets while checking examples. This expands
type coverage without adding a package marker, suppression or exclusion.
`example-mypy-correction1` passes 49 source files.

Shared checks on current executable files: Ruff passes; formatting passes (382
files); mypy src/tests passes (100 files); src/examples passes (49 files); CLI
version is 0.1.0. Lock check passes after runtime escalation for read-only uv
cache access; initial sandbox failure is retained. Import sorting/formatting and
two missing helper docstrings were corrected without changing behavior.

The complete planned focused selection passed 183 tests (219.69 seconds),
including 41 comparison cases and 142 unchanged supplier/tracking regressions.
Final review then added `t5-output-symlink-red`: it reproduced writes through
a symlinked staging parent before eventual helper rejection. Added output-parent
preflight for both staging and derived features. Renew the full comparison module
and shared checks; the 142 supplier/tracking regressions keep unchanged relevant
source inputs and remain reusable under verification policy. Baseline executable
source snapshots are retained under `identities/focused-baseline/`.

Output guard verification: `ip2-comparison-final` passed all 42 comparison
cases after the symlink preflight. Positional schema review added
`t5-pandas-labels-red`, which reproduced NaN feature files when native pandas
column names differed from project labels. Correction: copy pandas transformed
outputs and assign labels by position while preserving per-column dtypes; arrays
retain the original constructor path. Renew all 43 comparison cases and shared
checks. This corrects the approved positional-label contract without changing it.


## Final result and handoff

- The planned five-module focused selection passed **183 tests**, 0 failures,
  0 errors, 0 skips, in 219.69 seconds. All selected tests directly verify M1.
- After the output-parent correction, all **42 comparison cases** passed.
- After the final pandas positional-label correction, the complete current
  comparison module passed **43 tests**, 0 failures/errors/skips, in 209.82 seconds.
  The 142 unchanged supplier/tracking regressions retain passing evidence from
  the 183-case selection; their relevant package/fixture inputs did not change.
  This establishes 185 distinct selected cases across valid runs, not one
  all-passing 185-case invocation. No requirement or assertion was weakened.
- Renewed Ruff, formatting (382 files), mypy src/tests (100 files), mypy
  src/examples (49 files) and CLI version smoke (0.1.0) all pass. Lock check
  passed and SHA-256 remains
  `6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
- Final local document targets/fragments and whitespace checks pass; raw results
  are in `logs/document-check-final.json` and the retained diff-check output.

Contributor environment: Linux aarch64, Python 3.12.16 and committed lock.
Final separate installed projects observed MLflow 3.18.0, DVC 3.67.1, pandas
3.1.1, PyArrow 25.0.1, sklearn 1.9.1, NumPy 2.5.5 and skops 0.16.0. Earlier
fixtures used NumPy 2.5.4. Each fixture owns its own actual project lock and
provenance. Raw environment snapshots identify these differences; contributor
versions are not substituted for experiment versions. Native SQLAlchemy noload
warnings remain visible; no suppression was added.

| Criterion | Phase 2 evidence |
|---|---|
| US-14-AC-01 | Factory freshness, steps/settings/columns, train-only literal scaler/imputer/encoding values, mixed scaled/unscaled groups, positional schema with ndarray and pandas outputs |
| US-14-AC-02 | Exact feature Parquet values/order, native pipeline/metadata/model artifacts, effective settings and dependency identities, retained failures |
| US-14-AC-03 | Fixed classifier/source/split/protocol, accuracy and loss directions, exact reference/gain/tie/regression matrix, honest quality/process status |
| US-14-AC-04 | Actual file hashes, DVC pointer/status and source/split links, committed code/config/lock checks, output/namespace/reference failures and diagnostics |
| US-14-AC-05 | Explicit project factory declarations, global names/selected-only payload checks, unknown/duplicate/empty/budget rejection |

No package runtime implementation, dependency declaration, lock or packaged
resource changed. The contributor sklearn metric stub describes a native API
already exercised at runtime. Recipe/source, test and document hashes are
retained with command records. No new blocker or exhausted corrective attempt
remains; prior failures and their fixes remain above and in raw records.

IP2-T1–T5 are Complete. IP3 owns the recipe on both wheel paths, final M1–6 and
story reconciliation. Its execution is not yet authorized. No whole-story
acceptance, commit/push/publication, broader suite, standalone artifact driver,
M2 restoration, notebook, assistant or unverified-platform claim is made.

Developer approved Phase 2 with “i approve phase 2 gate”, 2026-11-15 UTC,
then authorized its local commit with “commit changes”. Phase 3 execution and
whole-story acceptance remain pending; push/PR publication are not authorized.
This approval-record-only update introduces no executable behavior and does
not invalidate the passing test evidence.
