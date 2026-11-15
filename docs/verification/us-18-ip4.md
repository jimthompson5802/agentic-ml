# US-18 Implementation Phase 4 verification

Status: **Complete; Gate 4 Approved; M1-slice acceptance pending**. Developer “start phase 4” authorized execution on
2026-11-15 UTC after Gate 3 approval and commit `f5605d0`. Developer “i approve gate 4; commit” approved Gate 4 and authorized its local
commit on 2026-11-15 UTC. M1-slice acceptance remains pending. Issue #28
remains open for M2 regression.

## Scope and boundaries

The complete issue body and one unique comment were refreshed successfully.
Final metadata matches the initial update time and comment count; the issue has
no GitHub milestone field, while its body assigns classification to M1 and
regression to M2. AC-01 is only partially delivered by M1. AC-02/03/04 belong to
M1. The Gate 1-confirmed boundaries remain installed public APIs, project scripts,
native MLflow inspection and native fitted-model inference.

This phase adds contributor verification, not executable toolkit behavior.
The package, runtime resources, dependency declarations and lockfile are unchanged.
Existing behavior is checked with independent numerical oracles rather than
manufacturing a product regression. The new verifier's first run failed because
the driver did not yet exist; subsequent corrections and native failures are
retained below. No mocks, check exclusions, skips or suppressions were added.

## Installed matrix

`tests/integration/test_installed_training.py` builds a real direct wheel and
source archive. `tests/installation/verify_training.py` invokes the existing
distribution driver, which validates the archive, extracts it and actually builds
the second wheel. Separate fresh normally installed projects use each artifact;
no direct-wheel substitution or source-checkout imports are permitted.

The unchanged distribution probes check CLI version, public import locations,
runtime dependency closure and independently specified packaged resources.
The training probe runs under isolated Python in each project's environment,
from an unrelated cwd. It initializes the project through the installed CLI,
copies the literal three guide scripts, creates real strict planning inputs,
commits code/configuration/lock/DVC pointers and executes the guide. Project forest
support uses only its native class binding and authored configuration.

| Criterion | Independent evidence on each wheel path |
|---|---|
| AC-01 M1 classification | DummyClassifier, DecisionTreeClassifier and project-bound RandomForestClassifier fit and predict on CPU |
| AC-02 | Baseline FINISHED before either candidate starts; exact validation accuracies 0.5, 1.0, 1.0; candidate baseline references; failed baseline prevents candidates |
| AC-03 | Native skops pipeline persistence/load; exact predictions `[0,0]`, `[0,1]`, `[0,1]`; fresh estimator/preprocessing instances; unchanged caller pipeline; native constructor error; incomplete parameter-profile rejection |
| AC-04 | Effective native parameters, origins, classes and installed library versions; native MLflow metrics/status/artifacts; exact preprocessing record; matching provenance and code/configuration/lock Git blobs; split digest and committed DVC content pointer |

Restored preprocessing transforms `[0,100]` to `[0,100/sqrt(5)]`, using
`rtol=atol=1e-12`. Model flavor explicitly declares skops and the approved
`numpy.dtype` / `sklearn.tree._tree.Tree` trust list. Missing source input and
invalid committed-code digest each leave exactly one FAILED baseline and a local
diagnostic, with no candidate comparison. The independent probe does not score
the held-out test rows.

The focused matrix's composed driver record is
`20261115T164833Z-f5605d066447-f817f2e3019e449299884630df15658b`.
Its child record retains the real rebuild command and both independent installed
inventories. Both wheel paths produced SHA-256
`51a6a55627daa98efbaf4ad6cdf3f71f3526b3079de1562f86a2725d6af45d28`;
the sdist was
`68525f510d69e0b764667683ff4dd57342bc7e75e8ae67819615fe612e149286`.
Identical wheel hashes result from actual separate builds; the logged rebuild,
separate artifact paths and separate environments establish both paths.
Both training projects used MLflow 3.18.0, pandas 3.1.1, scikit-learn 1.9.1,
NumPy 2.5.4, skops 0.16.0, DVC 3.67.1 and PyArrow 25.0.1. The contributor
lock used MLflow 3.17.2 and pandas 3.1.0; native inspection runs inside each
experiment environment to avoid substituting a different store schema/version.

## Commands and results

All commands run from the owning worktree unless a retained command record
specifies its separate project cwd. Pytest uses four workers and `loadgroup`.

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installed_training.py
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installed_training.py tests/integration/test_training.py tests/integration/test_training_tracking.py tests/integration/test_preprocessing_tracking.py --junitxml=.dev-records/verification/us18-ip4-20261115-f5605d0/focused.xml
uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/us18-ip4-20261115-f5605d0/m1-6.xml
uv run --locked pytest --collect-only -q
```

Initial installed success: **1 passed in 69.25 seconds**, zero failures/skips.
The focused run adds the explicit incomplete-profile assertion: **59 passed**,
zero failures/errors/skips/deselections, in 138.35 seconds. One native SQLAlchemy
`noload` deprecation warning is unsuppressed. Final M1–6: **982 passed, 1 existing skip, zero failures/errors**, six native
warnings, in **533.52 seconds**; exit status 0, all 983 selected cases completed.
Collection-only inventory reports **1251 collected, 983 selected, 268 deselected**
under the default M1–6 expression. Final run includes the new installed matrix;
its second passing driver record is
`20261115T165729Z-f5605d066447-fe8501a45f254e089f472034bf774ff9`.
Earlier phase story-regression and installed deferrals are resolved; required
US-18 M1 training coverage has no remaining deferred check. The existing
missing-planning-schema skip retains its separate historical obligation.

Shared checks pass: locked sync (196 resolved / 193 checked), `uv lock --check`,
Ruff lint and formatting (371 files), strict mypy (99 source files), CLI version
`0.1.0`, and `git diff --check`. The lock hash remains unchanged. Captured outputs
are in `shared-commands.json`; final documentation bookkeeping also passes
formatting/whitespace checks. Native warnings comprise the existing
SQLAlchemy deprecation and NumPy nonfinite-assessment warnings, not failed tests.
No check remains blocked. The final identity manifest records all seven dirty
files and their SHA-256 values at handoff; no executable change followed the
passing final M1–6 run.

## Corrections and retained failures

1. The first new test reported the absent verifier, 1 failed in 2.12 seconds.
   Implemented the contributor driver using existing distribution/evidence
   support. This is verification tooling, with no new toolkit behavior.
2. The first implemented probe incorrectly tried to read DVC-owned split content
   as a Git blob, after all three native models/scores had passed. One correction
   checks its actual content digest, committed DVC metadata and native status.
   The renewed run passed those Git/digest assertions and reached the next check.
3. The added native status command incorrectly supplied `--cd` to `dvc status`.
   One correction supplies the explicit subprocess cwd instead. The renewed
   matrix passed on both paths. Original errors and stack traces remain in driver
   logs; assertions for Git-owned code/configuration/lock bytes remain intact.
4. Mypy found reuse of an exception variable after its `except` scope. Renamed
   the later stderr variable; strict checks pass. Ruff import/format fixes add no
   suppressions. No problem exhausted three corrective attempts.

Raw phase records:
`.dev-records/verification/us18-ip4-20261115-f5605d0/`.
`driver-records.json` links each composed driver invocation, including failures.
Their `commands.json`, logs, identity manifests and child records retain complete
native outputs and direct/sdist/rebuilt artifact SHA-256 values outside disposable
pytest workspaces. Failed environments follow existing pytest retention; durable
records are retained for the lifetime of toolkit development.

The first two implemented failures are retained under
`20261115T164312Z-f5605d066447-bfb35bda6fab40de98ac8539f84439fa` and
`20261115T164546Z-f5605d066447-a8a229038a414d8e8d10dfed251bfd8f` below
`.dev-records/verification/`. The initial passing matrix is
`20261115T164641Z-f5605d066447-07ee9fc7e7de4ac0ba6d8ddcfc5e318d`.

## Qualifications and deferred owners

Observed platform: Linux aarch64, Python 3.12.16. macOS and Windows were not
verified by this phase. Separate projects resolve their own declared runtime
dependencies and lockfiles; contributor versions cannot stand in for theirs.
Lock SHA-256 before verification:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

AC-01 regression remains M2. Native stage scheduling/reuse, final-test evaluation,
assistant walkthroughs, notebooks and full committed-project reproduction retain
their owning stories. Historical M1/M50 and revised MVP milestone reconciliation
remain open in CHECKPOINTS.md. No complete-suite or standalone artifact-driver
run is claimed; artifact drivers are invoked inside selected pytest cases.
The three existing temporary skips remain unchanged.
`test_missing_planning_schema_fails_installed_inventory` is an M1-selected skip;
`test_failed_installed_probe_retains_available_environment` and
`test_rebuilt_probe_failure_retains_both_environments` are M50 and deselected.
Their timeout-related coverage remains with the existing historical story and
milestone owners; no skipped check proves acceptance. The 268 deselected cases
cover other milestones and contributor infrastructure, not additional US-18
training acceptance requirements. Gate approval and M1-slice acceptance are separate decisions.
