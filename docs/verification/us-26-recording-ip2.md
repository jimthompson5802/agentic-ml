# US-26 recording Phase 2 evidence

Status: technical work complete; Gate 2 Approved, 2026-11-14 UTC. Issue #17 / M1 AC-01–05.
Phase 1 committed as 3108645. Developer in coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a: “i approve Gate 1 in both us-15 and
us-26. commit the changes and start phase 2 in both stories”. Both Gate 1
approvals and Phase 2 authority are recorded in the owning plan. Gate 2 remains
Pending; no Phase 3, push or publication is authorized.

## Confirmed public boundary

Gate 1 approved log_run_results with explicit project_root/tracking_uri/native
run_id, separate provenance, supplied params/metrics/files and optional executed
notebook. Tests call that interface and inspect native MlflowClient results,
downloaded bytes, independently read Git blobs, native DVC metadata and the
installed project's origin/lock. No internal logging mocks or private identity
calls are used as test evidence. No training or preprocessing implementation.

The first tracer used the editable installed public helper and a minimal
provenance placeholder while only recording behavior existed. For the provenance
slice, that success test's fixture was upgraded to a genuine normally installed
wheel/project and complete provenance; its parameter/metric/status/file assertions
were retained. This is a direct-wheel component fixture, not the complete
producer/rebuilt-wheel installed integration owned by IP4.

Short TDD invocations run serial under the policy exception: each is one
component slice; xdist would multiply module fixture builds/installations. The
final focused/regression gate selection uses four workers with loadgroup.

## Red/green records

Raw logs under .dev-records/verification/us26-ip2-20261114/ contain exact selected
names/counts and original diagnostics. Common prefix: uv run --locked pytest
 tests/integration/test_tracking.py; each slice uses -k with its test name;
regression green runs include current relevant cases.

| Slice | Red | Green |
|---|---|---|
| 01 existing run/results | 01-red.log: missing public tracking module, 1 failed | 01-green.log: 1 passed |
| 02 committed run links | 02-red.log: missing experiment_commit native tag, 1 failed/1 deselected | 02-green.log: 2 passed |
| 03 committed-reference mismatch | 03-red.log: all four dirty code/config/lock/pointer cases incorrectly succeeded | 03-green-attempt2.log: all 6 current cases pass |
| 05 native DVC input integrity | 05-red.log: four mismatched/missing/changed native inputs incorrectly succeeded | 05-green.log: 5 relevant cases pass |
| 06 installed environment identity | 06-red.log: five false environment/wheel/source claims incorrectly succeeded | 06-green.log: 6 relevant cases pass |
| 07 shared provenance conflict | 07-red.log: existing artifact silently overwritten | 07-green.log: conflict and success cases pass |
| 08 explicit project root | 08-red.log: wrong exception/context for relative or missing roots | 08-green.log: 3 relevant cases pass |
| 09 directory DVC output | 09-red.log: valid directory reference rejected as non-file | 09-green.log: 6 relevant cases pass |
| 10 compatibility | Existing behavior, no manufactured red: Git full-SHA installation and missing/checksum/traversal/symlink references | 10-compatibility.log: 5 relevant cases pass |
| 04 strict provenance schema | 04-red.log: four unknown/missing/version/nonfinite cases fail their rejection assertions | 04-green.log: all 10 current cases pass |

Slices 11–22 add process/output failure retention, declaration validation,
terminal-run protection, fresh-kernel notebook success/error/missing-output
retention, notebook structure/source checks, artifact ownership, output safety,
explicit store selection, observed exit on failure, native error context and
native scalar/canonical structured parameter semantics. Numbered red/green logs
retain each selected run. Slice 23 is compatibility coverage of already
implemented behavior, not a manufactured red cycle.

The first native-selection regression expected the MLflow base class name for
an unsupported URI. Direct native construction independently established the
exact UnsupportedModelRegistryStoreURIException subtype. The test now requires
that exact native subtype, retaining context/no-mutation assertions; the product
exception type was never changed. Original 21-red/green logs remain. Unknown-run
context passed after the first implementation; unsupported subtype preservation
passed after correcting this inaccurate new test expectation.

Initial strict typing identified an untyped nbformat.read call. JSON loading plus
native nbformat.validate removes that untyped boundary without a suppression.
The native validator raises TypeError for malformed cell containers; the renewed
notebook negative test exposed that distinction in 21-green-attempt2.log
(10 passed, 1 failed). The helper now preserves its agreed invalid-notebook
ValueError boundary with the native cause. notebook-shape-correction.log passes
all 7 relevant notebook/selection cases; no assertion or acceptance criterion
was weakened. Initial lint identified two import ordering errors; formatting
and final shared-check evidence follow below.

Slice 03 first corrective verification (03-green.log) had 2 failures, 2 passes
and 2 fixture errors. Hypothesis/change: committed-blob checks should reject dirty
references; product checks exposed that fixture init changed uv.lock after its
commit. Native cached stores also reused removed parameter-case paths.
Second correction: commit the actual initialized lock before constructing
provenance, and allocate an exclusive UUID child store per case. Same original
assertions passed (6/6); no third attempt was needed. Original log retained.
No assertions were weakened or skipped and no suppression was added.

## Environment and limits

Complete #17 body/comments were refreshed and metadata rechecked: stable two
unique comments, unchanged accepted CONTRACT-01 direction. Snapshots retained.
Own locked .venv synchronization passed. No dependency declarations/lock changes.
Linux aarch64 / Python 3.12.16. Shared checks passed; final counts and identities are recorded below. Historical and revised milestone verification owners remain open.

IP2-T1–T4 are Complete; Gate 2 was subsequently Approved as recorded below.
Actual preprocessing serialization/helper integration is IP3/IP4; actual direct
and sdist-rebuilt producer handoff and final M1–6 acceptance remain IP4.

## Final-check corrections

The first four-worker selection (focused.log/focused.xml) completed with
64 passes and four failures. Each failure was in the new evidence logger:
intentional NaN/infinity arguments could not be embedded as numeric values in
its strict JSON record. The public helper had returned the expected rejection.
The logger now retains the exact argument payload as a JSON string inside the
strict record; original assertions and product rejection rules are unchanged.
The original failed XML/log remain intact. A renewed complete focused selection
verifies the same four failures and all relevant cases.

Strict typing additionally caught reuse of an exception-binding name in the
finally handler after the corrupt-provenance case was added. Renaming that local
decode exception preserves runtime behavior without suppressions. Shared format
check found the Phase 1 guide's Python example needed formatting; the example
was formatted without changing its semantics.


## Criterion coverage and exclusions

| Criterion | Verified Phase 2 boundary | Still owned elsewhere |
|---|---|---|
| US-26-AC-01 | Existing run/status, scalar/structured params, finite supplied metrics, artifact bytes/locations, explicit store and native conflicts | Fitted preprocessing IP3; actual producer integration IP4 |
| US-26-AC-02 | Strict shared provenance, committed code/config/lock/pointer bytes, native DVC hashes/members/current content, shared-record reuse/conflict | Actual producer metadata linkage IP3/IP4; native stage/replay US-27/M2 |
| US-26-AC-03 | Normally installed retained wheel and full-SHA Git, actual origin/version/payload/archive validation, Python/runtime versions and committed lock consistency | Both true wheel paths and final installed integration IP4 |
| US-26-AC-04 | Committed source/config refs; fresh-kernel executed notebook success/error/missing-output bytes, structural/source validation | Full notebook workflow and assistant usability US-09/39 |
| US-26-AC-05 | Missing outputs despite exit zero, nonzero exit, invalid declarations/references, artifact/storage failures, available diagnostics and independent validation status | Preprocessing serialization IP3 and actual handoff failures IP4 |

These are component outcomes, not story acceptance. No private initialization
identity code changed: the plan's conditional full initialization/wheel-upgrade
regression selection is therefore inapplicable. Existing public init is exercised
in both installed component fixture origins. No current-milestone/full M1–6,
complete suite, standalone distribution driver or rebuilt-wheel run was launched.
Those required final checks remain with IP4-T3 and named milestone owners.
No production/test suppressions, skips or threshold reductions were added.

## Shared checks

Commands from the owning checkout:

```sh
uv sync --locked --group dev
uv lock --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked agentic-ml --version
git diff --check
sha256sum uv.lock
```

Final lint passed; format passed for 324 files; strict typing passed for 83
source files; CLI smoke printed 0.1.0 (matching distribution/project metadata).
Final synchronization and lock checks passed (196 packages resolved; 193
installed packages checked). The focused outcome is recorded below. Native SQLAlchemy noload deprecation warnings remain visible; no
warning suppression or native dependency change was added.

The second four-worker selection (focused-renewed.log/XML) had 65 passes and
three notebook failures. An overly broad test edit intended to make the
committed-revision assertion order-independent instead changed the notebook
fixture to declare its older initialization commit. That commit lacked the new
source.ipynb, so the product correctly rejected the committed-byte mismatch.
Retained mismatch inputs/Git diagnostics show the wrong SHA; native project
Git history contains all three actual notebook commits. The fixture now declares
the actual notebook commit (HEAD immediately after its explicit commit). The
separate run-tag assertion resolves the supplied commit object. Product checks
and original notebook byte/status assertions remain unchanged. The final focused
selection repeats all 68 cases after this isolated fixture correction.

## Final verification and Gate 2 handoff

Final command, exit 0:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_tracking.py tests/integration/test_dataset_versioning.py --junitxml=.dev-records/verification/us26-ip2-20261114/focused-final.xml
```

**68 passed, zero failed/skipped/deselected, 168.01 seconds.** This includes
66 tracking component cases and two existing native dataset-versioning
regressions. The initial 64-pass/4-failure and renewed 65-pass/3-failure
invocations remain saved separately; only focused-final is the final passing
selection. No assertion, native exception type, timeout or acceptance threshold
was relaxed to obtain that result. The corrected notebook fixture declares its
actual committed source; the original byte-match requirement remains enforced.

Final lint/format/type/CLI checks pass; uv sync --locked --group dev and
uv lock --check both exit zero. git diff --check passes. Before/after and
committed uv.lock SHA-256 remains
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.
No dependency declaration, lock, initializer API, test policy or runtime resource
changed. No product or contributor suppression/skip was added.

Raw commands.json maps 56 pytest invocations to original logs; XML preserves
full failed/passing reports. Native fixture command/invocation records live
separately under .dev-records/verification/us26-ip2-native-commands/, including
installed origins/versions/digests, synthetic project inputs, public replies and
native run observations. Invalid numeric test inputs are retained verbatim as
payload strings in strict JSON records. Final document/source hashes, platform,
lock identity and working-tree patch are in the phase record manifest.

The verified source snapshot used Phase 1 commit 3108645 plus the then-uncommitted
tracking package, component tests and guide/plan/checkpoint/report changes.
The approval decision below authorizes committing that unchanged executable
snapshot and its updated approval records. Platform
is Linux aarch64 / Python 3.12.16; macOS/Windows remain unverified.
No full M1–6/complete suite, standalone artifact driver, rebuilt-wheel
integration, push, publication, sibling edit or Phase 3 implementation occurred.

Tasks IP2-T1/T2/T3/T4 are Complete. **Gate 2 is Approved** by the subsequent
decision below. The [owning gate](../plans/milestone-1-us-26-recording.md#us-26--implementation-phase-2-record-results-with-committed-provenance)
records this approval separately from Phase 3 execution authority. Phase 3
remains unstarted and requires separate direction; existing Gate 1 approvals
remain intact.
Actual fitted preprocessing and producer/consumer installed integration remain
IP3/IP4. No whole-story or milestone acceptance is claimed.

Document validation passed for 85 local paths/anchors across the five changed
Markdown documents, final newlines/trailing whitespace and git diff --check.
The retained finalize.py independently reads the final XML and records all
source/document hashes and a complete working-tree patch. Its initial inline
version mistakenly resolved the venv Python symlink to the base interpreter;
manifest-initial.log records that PackageNotFoundError. Invoking the absolute
venv path corrected identity collection without ignoring any missing package.

## Gate 2 approval and local commit authorization

2026-11-14 UTC, developer in coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a, relayed to the US-26 owning session:
“for both us-15 and us-26 i approve the phase 2 gate, commit the changes.”
This approves US-26 Gate 2 and the paired US-15 Gate 2. The user authorizes
committing the Phase 2 changes and approval records locally. No Phase 3, push,
publication, integration or cleanup is authorized. Whole-story acceptance is
not given. Only approval documentation changed after the passing verification;
the tested executable source and test identities remain unchanged.

The earlier raw manifest's Pending gate records the pre-approval verification
snapshot. Preserve it and all failed/passing logs; the current decision is owned
by this report and the plan. The resulting local commit is identified in Git
history and the session handoff.
