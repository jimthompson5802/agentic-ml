# US-18 / Implementation Phase 1 evidence

2026-11-15 UTC. Issue #28, M1 classification portion of AC-01 and design/
feasibility for AC-02/03/04. **IP1 Complete; Gate 1 Approved, 2026-11-15 UTC.**
The approval record at the end supersedes historical pending status below.
No product implementation or executable behavior tests were added. The
[proposed contract](../classification-training.md) needs developer confirmation
before IP2. The [plan](../plans/milestone-1-us-18.md) remains authoritative for
tasks, gate decisions and deferred verification.

## Authorization and source reconciliation

The developer authorized the previously recommended prompt by “you can use the
recommended prompt”: start US-18 IP1 in its story worktree and stop at Gate 1.
Plan approval was recorded separately and committed as `52dcc27`. Execution
started at `52dcc272cb30b5a9c2da4c03cdbb11c3664bf469` on
`US-18-classification`; `.worktrees/US-18-classification` is the registered owning
checkout and shares the primary Git metadata. Initial working tree was clean.
No neighboring checkout or branch was modified, no fetch/pull/merge/push occurred.

Issue #28 was retrieved with its complete body and all comments through the
repository GitHub helper. One unique comment matches both snapshots' count;
`updated_at` stayed `2026-11-07T00:29:21Z`. State is open, milestone field null;
body and scope comment assign classification to M1 and regression to M2. No
new issue scope or implementation acceptance was published. The current
repository phase-verification policy supersedes its older gate-selection prose.

Reviewed repository instructions/development, setup, worktrees, command approval,
records and verification guidance; active design reading-map references for
interfaces, data/features, blueprint, delivery, traceability and ADR-008;
accepted validation/preprocessing/tracking source and their guides. Accepted
US-15 IP3/IP4, US-26 IP2–4 and US-13 IP3 capabilities/approvals are available
in the starting branch, with supporting plans/reports retained. Native probes
consume no other story's source environment. No new cross-story implementation
prerequisite was found.

## Environment and retained evidence

Raw records live in this checkout at:

`.dev-records/verification/us18-ip1-20261115-52dcc27/`

They include complete issue snapshots/comments, original and bounded probe
scripts, stdout/stderr logs, generated additive metadata, native summaries,
command records and source/lock/environment identities. Native temporary model
stores are identified in each summary and remain available under `/tmp`; they
are disposable probe outputs, not the sole evidence. Original failure logs and
scripts are retained. No historical evidence was deleted. Raw records require
the repository's normal contributor backup/retention.

| Identity | Observed |
|---|---|
| Platform | Linux aarch64, kernel `7.0.14-linuxkit`, glibc 2.36 |
| Python | 3.12.16 |
| Toolkit | 0.1.0, editable from this story checkout |
| sklearn / MLflow / skops | 1.9.1 / 3.17.2 / 0.16.0 |
| numpy / pandas / pyarrow | 2.5.4 / 3.1.0 / 25.0.1 |
| Lock SHA-256 before/after | `6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4` |

No `UV_PROJECT_ENVIRONMENT`, `VIRTUAL_ENV` or `CONDA_PREFIX` redirected the
environment. `uv sync --locked --group dev` initially failed on the read-only
default uv cache lock. Identical escalated synchronization succeeded: 196
resolved packages, 193 installed into this worktree's own `.venv`. No lock or
dependency edits; the pre-existing generated workspace-member entry did not
block this synchronization. `uv lock --check` passed; direct installed CLI
`.venv/bin/agentic-ml --version` returned `0.1.0`.

This development environment establishes native library feasibility only. It
is not a normal installed experiment fixture, does not pass strict installed
project identity, and adds no macOS/Windows or distribution acceptance evidence.

## Native probe commands and outcomes

Commands ran from the story checkout; each probe uses isolated Python:

```sh
.venv/bin/python -I .dev-records/verification/us18-ip1-20261115-52dcc27/probe.py
.venv/bin/python -I .dev-records/verification/us18-ip1-20261115-52dcc27/probe_bounded.py
```

`logs/probe.log` retains the initial sandboxed run; `logs/probe-escalated.log`
retains the same original probe with cache access. Both reached the native tree
trust failure. `logs/probe-bounded.log` and `bounded-summary.json` retain the
explicit bounded alternative, exit 0. The latter pins observed native model
requirements explicitly rather than relying on MLflow environment inference.

| Question / criterion | Observed result |
|---|---|
| Can additive metadata represent a tree and forest? AC-01/04 | Existing public `validate_registry` accepted complete scalar profiles for both; registry ID `sha256:3965af073f625f1ef6c7a3974d4379a4ff29985c5ecc093af35284598e81bcc9` |
| Generic classifier operations? AC-01/03 | Caller bindings, exact class equality, `is_classifier`, `clone`, `get_params`, native fit/predict work for dummy/tree/forest; originals remain unfitted |
| Training-only composition? AC-03 | Native preprocessing fitted on x = -3,-1,1,3, mean 0/variance 5; already fitted transformer/classifier compose without another fit |
| Independent baseline/tree oracle? AC-02/03 | Validation labels 0,1 at x=-2,+2; dummy most-frequent predicts 0,0 / accuracy 0.5, depth-1 tree predicts 0,1 / accuracy 1.0 |
| Independent forest oracle? AC-01/03 | Three depth-1 trees, no bootstrap, all features, seed 17, one worker. Every tree's separating midpoint is 0; predicted 0,1 / accuracy 1.0. Same-seed repeated fit gives same labels |
| Native complete-model persistence? AC-03/04 | All three models saved, client-uploaded/downloaded, reloaded and predicted validation plus separate inference rows; native parameters, accuracy and FINISHED visible |
| Missing-value composition? AC-03 | Native imputer learns 2 from [1, missing, 3], centering learns 2; loaded preprocessing transforms 100 to 98, tolerance 1e-12; prediction 1 |
| Unsupported intrinsic parameter? AC-01 | Native forest `n_estimators=0` raises `InvalidParameterError` during native fit validation; no standalone public validator is assumed |
| Serialization failure fixture? AC-03/04 | Fitted otherwise-valid native Pipeline with extra `threading.Lock` state raises native `MlflowException`, identifying `_thread.lock`; no fallback or success return |

The registry scratch generator derives profiles from native configured scalars
only to investigate representability. It is **not** the production validation
recipe or independent behavioral oracle. IP2/IP4 fixtures must use explicitly
reviewed static project metadata and genuinely resolved strict evidence. The
probe does not prove candidate currentness, toolkit class/parameter enforcement,
real DVC/code/config links or installed-project behavior.

## Persistence finding and proposed decision

The initial explicit trust list `numpy.dtype` was sufficient for the dummy model
but failed for `sklearn.tree._tree.Tree`. Locked skops source deliberately omits
that internal tree storage type from default trust because arbitrary serialized
node indices can be unsafe when later used in native prediction. This was a
native serializer configuration finding, not a toolkit regression.

One bounded alternative was investigated: explicit
`skops_trusted_types=["numpy.dtype", "sklearn.tree._tree.Tree"]` for locally
created trusted experiment models. It passed the original full tree/forest
save/download/load/predict assertions without changing expectations. No broad
trust discovery, pickle/cloudpickle fallback, suppression or skipped assertion
was added. A tree-storage entry is a proposed extension to the accepted
preprocessing setting; it is **not approved or implemented** by these probes.
Gate 1 must review this choice and its trusted-local limitation.

The sandboxed original also produced uv dependency-inference cache failures and
MLflow fallback warnings. The escalated original removes the sandbox restriction
and still exposes tree trust failure. The bounded probe supplies explicit pinned
native requirements as part of the model format proposal, not a claim that
MLflow inference resolved the experiment environment. The project lock remains
authoritative. The expected `_thread.lock` failure still occurs under the bounded
configuration and is preserved.

Problem-attempt accounting: original configuration observed failing; unchanged
escalated rerun reproduced it; one explicitly proposed bounded alternative
passed original assertions. No failed corrective product changes occurred and
no third corrective attempt was needed. Future unsupported serializer types
remain explicit failures requiring a reviewed project choice.

## Contract decisions prepared for Gate 1

See the exact [proposed signature and contract](../classification-training.md):

- One fitting helper, native inputs/outputs, explicit project root and live
  strict `CandidateRequest`; no new orchestration or tracking API.
- Project-owned algorithm/class bindings; native classifiers extensible without
  package edits. Scalar parameter metadata must cover all `get_params(deep=False)`
  values; nested/non-scalar parameters rejected explicitly in M1.
- Public candidate validation precedes any fitting. Native fit handles intrinsic
  constraints beyond the declared metadata; no private sklearn validator usage
  and no universal pre-fit semantic guarantee.
- Reuse accepted preprocessing/partitions; train-only fitting; two-way fit with
  no test scoring; three-way validation for the project comparison.
- Fixed record keys, error taxonomy and native complete-model pipeline steps;
  shared provenance remains owned by accepted tracking, not a new run store.
- Project script owns baseline ordering and native model artifact upload;
  accepted recording helpers preserve exact producer records and finalize runs.
- Explicit bounded serializer choice and forest oracle need Gate 1 approval.

These choices refine the approved native-extensibility plan rather than changing
issue outcomes. No custom-estimator, simple-path, tuning or final-test scope was
added. Requested public-boundary confirmation remains **pending** at Gate 1.

## Checks, completion and remaining verification

IP1-T1/T2/T3 are technically Complete: source reconciliation, native findings,
exact proposed contract, script outline and revised test boundaries are saved.
Whitespace and local document-path checks pass. Lock unchanged; normal source
and test trees unchanged. No behavior tests, focused pytest, M1–6, complete suite,
artifact driver or product lint/type run was performed. TDD and executable-phase
checks are inapplicable to this contract/native-investigation phase; no runtime
toolkit behavior changed. There are no pytest counts to report for IP1.

IP2 owns actual fitting, class/bounds/currentness and shape failure tests through
the confirmed public API; IP3 owns baseline-order/tracking failures and real
lineage; IP4-T1/T2 own direct/rebuilt normal installations; IP4-T3 owns final
M1–6/shared checks and all earlier excluded story regressions. M2 owns regression
and broad customization/restoration. `MVP-M1-ACCEPT-VERIFY`, historical M1 and
M50 obligations remain open independently. No story or milestone is accepted.

**Gate 1:** Pending developer approval of the contract, persistence choice and
public test boundaries. Stop here; IP2 is not authorized by IP1 completion.

## US-18-SC-02 constructor contract renewal — 2026-11-15 UTC

Developer “I like this approach better, make the needed changes” directs the
revised responsibility: project supplies the class binding and metadata; toolkit
validates and constructs the estimator. The revised contract removes `estimator`
from `fit_classifier`. IP1-T1/T2/T3 were reopened for this revision and completed
again after targeted native renewal and document checks. Original probe scripts,
logs, results and serializer failures remain historical evidence unchanged.
The exact contract and plan's SC-02 record supersede caller-instance requirements.

New native-only command, from the same worktree/environment:

```sh
.venv/bin/python -I .dev-records/verification/us18-ip1-20261115-52dcc27/probe_construction.py
```

`logs/probe-construction.log` and `construction-summary.json` record exit 0.
Frozen full effective parameters from the earlier probe were passed directly to
selected bound classes with `cls(**parameters)`: dummy (3 parameters), tree (13),
forest (19). All preserve exact parameter values/types, produce the previously
independently declared predictions and pass complete-model skops save/load with
the same explicit trust setting. The input parameter dictionaries remain
unchanged. An unknown forest constructor keyword raises native `TypeError`.
No product fitting helper or genuine strict candidate execution was tested.

The revised boundaries require public candidate validation before construction,
valid native class bindings, a fresh estimator each call, complete parameter
coverage/default-drift checks after construction but before fitting, and native
constructor errors retaining construction-stage context. Caller-instance matching
and immutability checks are retired because that input no longer exists;
preprocessing, frame, candidate, binding and parameter immutability remain.
Persistence, numerical predictions, installed checks and final regression
obligations are unchanged. Native probes show construction feasibility, not the
future helper's validation order or fresh-call isolation; IP2 and installed IP4
checks must establish those behaviors. No executable behavior changed, so no new
TDD/product test run is applicable to this contract revision.

Document whitespace and local-link checks pass after revision. The lock is
unchanged. **Gate 1 remains Pending** for the revised public boundaries and the
previously proposed explicit tree-storage trust choice; no IP2 authorization,
commit or publication is inferred from this contract-edit instruction.

## Gate 1 approval — 2026-11-15 UTC

Developer “i approve phase 1” approves IP1, the SC-02 revised toolkit-owned
construction contract, public test boundaries and explicit numpy.dtype/tree-storage
trust setting for locally fitted models. Earlier Pending/proposed status above
is retained as historical evidence and superseded by this decision. No product
implementation, story acceptance, IP2 start authorization, commit or publication
is inferred. IP2 tasks remain Not started.
