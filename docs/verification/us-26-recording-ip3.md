# US-26 #17 / Phase 3: native preprocessing recording

2026-11-14 UTC. Phase 3 is technically Complete; **Gate 3 is
Approved**. [Owning plan](../plans/milestone-1-us-26-recording.md) IP3 advances
US-26-AC-01–05. Neither this component evidence nor Gate 3 accepts #17 or US-15.

## Authority and inputs

Developer direction delivered through coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a: “have both US-15 and US-26 start Phase 3”.
Gate 2 was approved and committed as 5f4947f2420e8d8beb3e7c75c0d07ff427806b27.
Own branch US-26-mlflow and registered worktree .worktrees/US-26-mlflow were
clean before implementation. Only IP3 is authorized; no source integration,
Phase 4, commit/push, publication, cleanup or sibling edits.

Issue #17 complete body and both comment pages were refreshed; two unique
comments match count 2 and final updated_at remains 2026-11-14T18:07:56Z.
The issue has no GitHub milestone; its body assigns AC-01–05 to M1.
CONTRACT-01, SC-01 and Gate 1-confirmed public test boundaries are unchanged.
One sandbox network failure on metadata refresh succeeded on the identical
escalated read. No issue edit/publication occurred.

Linux aarch64, Python 3.12.16, own .venv, no VIRTUAL_ENV or
UV_PROJECT_ENVIRONMENT override; UV_LINK_MODE=copy. Lock SHA-256 before/after:
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.
No dependency, resource or initializer-internal changes.

## Implemented boundary and evidence

The installed public log_preprocessing accepts an existing active RUNNING run,
explicit store/root, native fitted Pipeline, preprocessing metadata and shared
provenance. It uses bounded native skops save_model plus explicit-client
artifact logging at preprocessing/pipeline and preprocessing/metadata.json;
provenance.json is shared with log_run_results. Successful preprocessing leaves
RUNNING. Metadata declarations do not prove fitting scope or output dtypes.

| Criterion | Public evidence | Limits |
|---|---|---|
| AC-01 | Same requested run ID and exact native artifact URIs; native download/load of fitted scaler and composed Pipeline/ColumnTransformer/imputer/scaler/encoder; active/terminal lifecycle | No new runner or logged-model lifecycle |
| AC-02 | Exact metadata/provenance JSON; every native get_params(deep=False) key/value/order; SC-01 tags retained; same saved split, disjoint membership and source schema; shared provenance conflict/reuse | Native source hash is recorded, not independently recomputed from pipeline training rows |
| AC-03 | Required installed preprocessing versions; shared installed Git/wheel/lock identity validators and IP2 regressions | Actual US-15 output/direct plus rebuilt-wheel integration belongs to IP4 |
| AC-04 | Committed code/config/lock/DVC references reused; missing references rejected; exact documented script committed and run from unrelated cwd | Existing notebook tests remain regression evidence; no new notebook runner |
| AC-05 | Invalid schema/settings, unknown defaults, forbidden ID/target selection, fitted-state/object/inventory checks, unsafe/conflicting paths and provenance; native serialization and real storage failures | No atomic rollback, forced-kill retention, broad trust discovery or fallback |

The consumer compares declarations against native objects without importing
class-name strings or reconstructing pipelines. Only the reviewed M1 component
inventory is accepted. Canonical dtype descriptors use the exact SC-01 allowlist;
the NaN tag is restricted to built-in SimpleImputer.missing_values. Callables,
opaque objects, cycles, malformed/context-inappropriate tags and reserved literal
native maps fail. Ordinary finite numeric values stay ordinary JSON.
Output names remain project declarations; the consumer checks width with native
feature-name inspection and input names/dtypes against the saved source schema.
US-15 owns independent training-transform/dtype/fit-scope correctness.

Shared provenance publication was extracted; preprocessing and results share
that helper. A later regression found Python dictionary equality could conflate
JSON true and 1. Canonical finite JSON comparison now rejects that conflict
while preserving identical existing bytes (including different whitespace).
The guide's complete independent scaler script is extracted verbatim into a
separate normally installed experiment, committed, and executed from an unrelated
cwd. Downloaded feature bytes are independently expected as x / 0.0 / 2.0.

Serialization failure uses a supported fitted Pipeline with an extra
threading.Lock fitted-state attribute. Native MlflowException and its cause
remain visible; metadata/provenance are already available and FAILED is explicit.
Real storage failure uses a regular file as the native artifact root, yielding
NotADirectoryError without permission-bit assumptions or mocks. Local metadata
and provenance remain readable; exception notes identify run, stage and directory.
Successful staging directories are removed; failed directories remain inspectable.
No unavailable artifact is claimed as remotely retained.

## TDD and checks

Raw lifetime records: .dev-records/verification/us26-ip3-20261114/.
Each numbered log starts with the exact command and retains the complete output.
Invocation JSON records preserve supplied arguments, public exceptions/notes and
native subprocess stderr. Fixture native command logs also remain under
.dev-records/verification/us26-ip2-native-commands/; their inherited IP2 label is
historical fixture plumbing, not an IP3 acceptance claim.

Short selected TDD cycles used serial pytest to avoid worker startup for one
installed-interface slice; the final phase command uses four/loadgroup.

| Logs | Intended red behavior / unchanged green verification |
|---|---|
| 01–02 | Missing public export; native artifacts/fitted-state readability, existing results regression |
| 03–08 | Exact record keys, train declaration, consumed saved-split equality |
| 09–16 | Complete effective settings, output schema, selected/input schema, installed versions |
| 17–22 | Terminal run protection, occupied artifacts, shared provenance and IP2 provenance regressions |
| 23–28 | Full composed SC-01 tags/native load; unfitted pipeline and metadata version |
| 29–30 | Native serialization failure, context/FAILED and retained partial evidence |
| 31–40 | Artifact paths, absolute root, explicit URI, Pipeline type and output width |
| 42–45 | Supported M1 inventory and reserved native literal-map rejection |
| 48–49 | Real committed/DVC-versioned saved overlapping memberships rejected despite exact JSON match |
| 53–54 | JSON boolean/numeric shared-provenance conflict reproduced and fixed; 12 focused provenance regressions pass |

Every intended red failed because required product behavior was missing; each
correction passed its unchanged original oracle and selected relevant regressions.
Additional 41/47 boundary tests cover already implemented behavior, rather than
manufacturing new failures. Log 50 executes the exact guide script, which passed
on its first run; documentation adds no new product behavior. No assertions,
thresholds, timeouts, markers or checks were weakened, skipped or suppressed.

Initial lint found import ordering and formatting issues, corrected with the
documented formatter. Initial narrow typing found sklearn's missing typing
markers, len(object) and the existing test support module outside that narrow
selection. Correction extends existing contributor public sklearn stubs, uses
validated column names, and runs the required full mypy src tests command.
No untyped adapter, ignore or check exclusion was introduced. Logs 46/51 pass.
The first full formatting check found the guide's fenced Python formatting;
the formatter corrected it before the final guide regression executes.
Sandbox uv-cache lock failures were rerun with identical authorized escalated
commands; these are environment access failures, not failing product tests.

| Final check | Result |
|---|---|
| Initial focused.xml run | 239 passed, 1 failed; 240 selected; 327.12 seconds; guide fixture commit mismatch retained |
| uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_tracking.py tests/integration/test_splitting.py --junitxml=.dev-records/verification/us26-ip3-20261114/focused-final.xml | 241 collected/selected/passed; 0 failed/skipped/deselected; 337.62 seconds; four/loadgroup |
| uv sync --locked --group dev | Pass; 196 resolved, 193 checked |
| uv lock --check | Pass |
| uv run --locked ruff check . | Pass |
| uv run --locked ruff format --check . | Pass; 333 files |
| uv run --locked mypy src tests | Pass; 84 files |
| uv run --locked agentic-ml --version | Pass; 0.1.0 |
| git diff --check; lock before/after | Pass; lock unchanged |

## Failed final run and correction

The initial four-worker final run had 239 passes and one failure. The guide
fixture created a new script commit after an earlier negative test deliberately
committed an inconsistent uv.lock; restoring working bytes did not update the
Git index. The helper correctly rejected the new commit’s uv.lock mismatch.
Correction attempt 1 stages every currently consumed declared input before the
new guide commit, preserving the original assertions and reference checks.
Log 55 reruns the original lock-negative case, committed invalid-split case and
guide script together: all three pass. No product check was relaxed. Original
focused.xml/log 52 and native command stderr remain retained; the disposable
numbered workspace is subject to the repository’s normal retention policy.

Static review separately found the JSON true/1 conflict; log 53 is the intended
red regression and log 54 verifies the correction plus provenance cases.
Final focused/shared checks were renewed after this executable change; all
241 cases pass in one run. No unresolved correction or blocker remains.

## Gate 3 position and remaining work

T1–T4 are Complete. Final focused evidence covers 117 tracking cases
(66 existing plus 51 new) and 124 unchanged splitting regressions. Shared checks,
90 local links/anchors, whitespace and final source/guide identity checks pass.
The native SQLAlchemy noload deprecation warning remains visible, unsuppressed.
Gate 3 is Approved. No Phase 4 or source
integration is authorized. IP4 owns the actual approved US-15 handoff, direct and
genuinely sdist-rebuilt wheel matrix, M1–6 final story checks and #17 acceptance.
No broader pytest suite, standalone artifact driver, macOS/Windows support,
M2 restored transformation/replay, assistant workflow, reports/comparisons,
reverse lookup or milestone acceptance is claimed. Preserve the earlier default
skops failure, Phase 1/2 approvals/evidence and historical milestone obligations.


## Gate 3 approval and local commit authority

On 2026-11-14 UTC, after both Gate 3 reports, the developer instructed
“commit changes in both stories”. Coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a explicitly directed this owning session
to record US-26 Gate 3 approval and commit completed Phase 3. This supersedes
the initial IP3-only/no-commit authority above. It approves the implementation
phase and local commit; #17 story acceptance, Phase 4/source integration,
push/publication and cleanup remain unauthorized. Executable/test/typing files
and the guide script are unchanged from passing focused-final.xml inputs.
Approval and resulting commit verification are retained separately under
.dev-records/verification/us26-ip3-approval-20261114/; preserve the earlier
Pending-gate verification manifest as the historical review snapshot.
