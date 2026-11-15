# US-18 / Implementation Phase 2 evidence

2026-11-15 UTC. **IP2 Complete; Gate 2 Approved, 2026-11-15 UTC.**
Issue [#28](https://github.com/jimthompson5802/agentic-ml/issues/28), M1
classification portion of AC-01; baseline fitting portion of AC-02; native
fit/predict portion of AC-03; effective metadata portion of AC-04. Recording,
persistence integration, installed verification and whole-story acceptance are
not established by this phase. See the [owning plan](../plans/milestone-1-us-18.md).

## Authorization, inputs and identity

Developer “use the suggested prompt” authorizes the previously supplied
“Start US-18 Phase 2 and stop at Gate 2 for my approval.” Gate 1 approval,
including revised constructor contract SC-02 and public test boundaries, is
recorded in the plan and `4a4f2e7`. This phase started with a clean tree at
`4a4f2e7f21693e3bf4cfafceca6da08ca61ebecd`, branch `US-18-classification`,
registered worktree `.worktrees/US-18-classification`. No branch switching,
neighboring checkout changes, fetch/merge/push or publication occurred.

Complete GitHub issue metadata/body, all comments and final metadata refresh
were saved before implementation. One unique comment matches both snapshots;
issue is open, GitHub milestone null, unchanged `updated_at`
`2026-11-07T00:29:21Z`. Body/scope comment retain M1 classification/M2
regression. No issue/spec change or new cross-story prerequisite was needed.

Verified prior instructions, approved signature and public boundaries;
development/verification/setup/worktree and records guidance, design reading
map, previously reviewed topic contracts and accepted preprocessing/strict
validation interfaces. Reused their source directly from this branch.

Environment remains story-local `.venv`; no active `VIRTUAL_ENV` or
`UV_PROJECT_ENVIRONMENT` redirected it. Locked synchronization passed:
196 packages resolved, 193 checked. Linux aarch64, Python 3.12.16; toolkit
0.1.0, scikit-learn 1.9.1, numpy 2.5.4, pandas 3.1.0, pyarrow 25.0.1.
Before/after `uv.lock` SHA-256 is unchanged:

`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`

Final tested inputs are this starting revision plus the uncommitted source,
tests, typing and documentation changes enumerated in the raw identity manifest.
No new dependency or suppression/check exclusion was introduced.

## Delivered public behavior

`src/agentic_ml/training/__init__.py` implements the approved
`agentic_ml.training.fit_classifier` interface:

- Explicit project/candidate root checks, train-only scope and live strict
  candidate validation before construction. Current selected configuration must
  describe classification with scikit-learn.
- Project-owned native class bindings; scalar parameters copied from materialized
  candidate evidence. Native constructor creates a fresh estimator. Complete
  native parameter coverage and scalar type/value agreement are checked before
  fitting, catching metadata omissions/default drift.
- Accepted `fit_preprocessing` and public partition reconstruction provide
  current-source checks, disjoint recorded memberships and training-only features.
  Training targets must be nonmissing binary/multiclass labels. Native estimator
  fit/predict errors retain their type and algorithm/stage notes.
- Returned native Pipeline has `preprocessing` and `estimator` steps, prediction
  and classes, and plain metadata with the approved exact keys. Training prediction
  compatibility checks shape, row count and membership in fitted classes.
- Two-way fitting uses no validation or final-test scoring. Caller frame,
  preprocessing and partition records remain unchanged; repeated calls produce
  independent fitted estimators and equivalent effective records.

No estimator table, persistent registry, native algorithm implementation, private
sklearn validator, tracking wrapper or workflow engine was added. A small private
Protocol describes validated native classifier operations; the stage context
manager adds notes in `finally` without swallowing exceptions. Contributor-only
sklearn stubs were extended for public classifier bindings, `is_classifier`,
`type_of_target` and Pipeline prediction/classes. These are typing declarations,
not runtime registration, adapters or check suppressions.

## TDD and independently defined outcomes

Tests exercise the Gate-1-confirmed public fitting interface with real
`resolve_plan`, `validate_configuration` and `CandidateRequest` evidence in
independent temporary declarative projects. No fake plan IDs or mocks of toolkit
collaborators are used. These existing planning fixtures do not provide normal
installed experiment identity or real tracking provenance; those remain IP3/IP4.

Raw evidence: `.dev-records/verification/us18-ip2-20261115-4a4f2e7/`.
It retains before/after issue JSON/comments, red/green logs and JUnit XML,
commands, file hashes, environment/lock identity and outcomes. Follow lifetime
retention/backup rules; disposable pytest workspaces are not the sole evidence.

Serial commands for short red–green cycles used:

```sh
uv run --locked pytest tests/integration/test_training.py::TEST_NAME
uv run --locked pytest tests/integration/test_training.py
```

The first green also selected `tests/integration/test_preprocessing.py` (85 total
passes in 1.68 seconds). Serial runs minimized worker startup during short TDD
cycles; phase regression checks below use the required four-worker loadgroup
selection. The raw command manifest gives every selector and artifact filename.

| Cycle / raw prefix | Red result | Green result |
|---|---|---|
| 01 baseline | Missing public training module, one failure | Native baseline and preprocessing regression, 85 passed |
| 02 coverage | Missing native default silently accepted, one failure | Full native parameter coverage enforced, 2 passed |
| 03 root | Different project root accepted, one failure | Explicit matching root required, 3 passed |
| 04 binding | Missing algorithm binding leaked KeyError, one failure | Actionable ValueError, 4 passed |
| 05 classifier | Regressor binding reached fitting/attribute failure, one failure | Classifier compatibility rejected early, 5 passed |
| 06 identity | Wrong validated task/library accepted, two failures | Both rejected, 7 passed |
| 07 target | Dummy classifier accepted missing training labels, one failure; tree/forest cases passed | Explicit target rejection, 10 passed |
| 08 prediction | Malformed shape/unknown class outputs accepted, two failures | Compatibility rejection, 12 passed |
| 09 context | Native constructor/fit errors lacked stage notes, two failures | Original exceptions retain algorithm/stage, 14 passed |
| 10 scalar | Nested candidate parameter raised generic blocked-evidence error, one failure | Explicit unsupported-encoding TypeError, 15 passed |
| 12 scope | Invalid fit scope reached a native constructor, one failure | Scope rejected first; boundary matrix, 44 passed |
| 13 request root | Malformed CandidateRequest root leaked AttributeError, one failure | Explicit field TypeError; final regressions, 310 passed |

`11-boundaries.xml` records the intervening 33-case training regression selection.
Already implemented generic behavior and inherited preprocessing/partition guards
were expanded with direct regression coverage without manufacturing new failures.
Every implementation change followed its observed red; green verification passed
on the first corrective implementation. Original assertions/criteria remain
intact. No repeated-problem attempt limit was reached.

Independent oracles and boundaries:

- Literal symmetric training values give mean 0/variance 5. Baseline predicts
  `[0,0]`; tree and project-only forest predict `[0,1]` on validation/inference.
  Forest settings are the approved non-bootstrap three-tree depth-1 fixture.
  Static complete scalar profile literals define expected parameters independently
  of native `get_params`; no introspection-generated expected parameter record.
- Imputation learns 2 from training values and centering learns 2; transform of
  100 is 98 and of a missing inference value is 0, tolerance 1e-12. Multiclass
  labels and two-way test-only class 99 verify correct training class membership.
- Corrupted source identity, overlapping/incomplete partitions, wrong fit scope,
  target/ID features and output width reject through the reused public guards.
- Stale evidence, changed fixed/default values, out-of-bounds and incorrectly
  typed searched values reject before construction. A deliberately incompatible
  native constructor would raise TypeError if execution crossed that boundary;
  tests instead require the evidence rejection's ValueError diagnostics.
- Prediction fault tests patch only external sklearn's public `DummyClassifier.predict`
  to supply malformed outputs. This tests the approved external prediction
  compatibility boundary, not toolkit private methods or internal call sequences;
  it does not claim those faults occur in normal native sklearn.
- Native unsupported constructor keyword and invalid tree depth retain native
  errors and context. Explicit root/request/class/type and scalar finiteness
  cases also pass. No model quality threshold or improvement requirement added.

## Final focused and regression verification

```sh
uv run --locked pytest -n 4 --dist=loadgroup \
  tests/integration/test_training.py \
  tests/integration/test_preprocessing.py \
  tests/integration/test_splitting.py \
  tests/integration/test_configuration_validation.py \
  --junitxml=.dev-records/verification/us18-ip2-20261115-4a4f2e7/logs/final-focused-regressions.xml
```

**310 passed, 0 failed, 0 skipped, 0 deselected; 9.02 seconds**, four workers
with loadgroup. Selection contains 45 new training cases and 265 relevant existing
preprocessing/partition/configuration cases, all directly marked M1. The earlier
309-case pass predates the final malformed-request-root regression and is retained
as historical evidence; the 310-case run owns final executable verification.

| Shared check | Result |
|---|---|
| `uv sync --locked --group dev` | Pass; environment remains story-local |
| `uv lock --check` | Pass after sandbox cache-lock denial on ordinary invocation; identical escalated check resolved 196 packages |
| `uv run --locked ruff check .` | Pass |
| `uv run --locked ruff format --check .` | Pass after formatting the existing contract's Python code fence; original failure retained |
| `uv run --locked mypy src tests` | Pass, 93 source files |
| `uv run --locked agentic-ml --version` | Pass, `0.1.0` matches installed distribution |
| `git diff --check` and document path checks | Pass; untracked new files also checked for trailing whitespace |
| Lock before/after SHA-256 | Identical, shown above |

The Markdown formatting correction changes no interface or executable behavior.
No test failures were hidden, assertions weakened, skips introduced or timeouts
changed. Infrastructure cache denial is not a scientific failure. Existing three
temporary skips are outside this focused selection and remain unresolved for
story/milestone reconciliation; passing these tests does not verify their coverage.

The first ad hoc identity collector used system Python and could not locate
toolkit distribution metadata. Running the saved collector with this worktree's
`.venv/bin/python` passed; the original failure summary is retained in
`logs/collector-first.log`. This required no product or test change. Final
collection verified 83 local document path links and the complete issue snapshot.

## Gate 2 and remaining owners

IP2-T1/T2/T3/T4 are technically Complete. Gate 2 is **Pending**. Changed public
behavior is only validated in-memory classification fitting. MLflow baseline
ordering, complete-model publication/failures and real committed DVC/code/config
lineage remain IP3. Both normally installed artifact paths remain IP4-T1/T2;
IP4-T3 owns final M1–6/shared checks and all unselected story regressions.
No current-milestone full run, default M1–6 acceptance run, complete suite or
standalone artifact driver was launched. No new macOS/Windows evidence exists.
M2 regression/customization/restoration, MVP milestone integration and historical
M1/M50 obligations remain unchanged.

Stop at Gate 2 for developer approval and Phase 3 authorization. No commit,
push, publication, story acceptance or later-phase execution is inferred.

## Gate 2 approval — 2026-11-15 UTC

Developer “i approve gate 2; commit” approves Phase 2 and authorizes its local
commit. Earlier pending gate and commit status above are historical and
superseded by this decision. Verification results remain unchanged. IP3 start,
push, publication and story acceptance are not authorized by this decision.
