# US-26 recording Phase 1 evidence

2026-11-14 UTC; issue #17, M1 AC-01–05 design/feasibility only.
Branch US-26-mlflow, worktree .worktrees/US-26-mlflow, HEAD 131ac82.
Developer “start phase 1” follows “i approve phase 1; commit”. No product
implementation, executable behavior tests or acceptance is claimed.

## SC-01 renewal

The later [US-26 concurrence](us26-sc01-concurrence.md) supersedes this report's
complete-metadata feasibility conclusion: exact NaN/dtype encoding and full
consumer comparison are now verified as feasibility. Original observations and
failure logs below remain historical evidence; neither gate is approved.

## Scope and source reconciliation

Git worktree registration, top-level/common directory and owning plan match:
primary /workspaces/agentic-ml; common /workspaces/agentic-ml/.git.
The working tree was clean at entry. No switch, merge, rebase, fetch, push or
sibling edit occurred. The complete #17/#21 discussions were refreshed via
repository helper metadata/comments --paginate --slurp, then metadata again.
Both are open issues, null GitHub milestone; bodies assign #17 AC-01–05 to M1,
#21 AC-01–03 to M1 and AC-04 to M2. Two unique comments each match both metadata
counts; updated_at stayed 2026-11-14T18:07:56Z / 18:07:50Z respectively.
CONTRACT-01 remains accepted direction, not executable acceptance.

Raw evidence is retained at
.dev-records/verification/us26-ip1-20261114/ in this checkout: full before/after
issue JSON, paginated comments, probe scripts/logs/summaries, retained native
stores/models and command/identity manifest. Timeline/deleted comments are not
part of the export. Initial sandbox GitHub DNS/socket denial was resolved by
escalated identical reads; it was not an actual authentication failure.

Reviewed active design reading map and affected execution/tracking,
interfaces, data/features, blueprint, traceability, delivery, repository and
architecture-decision references; development/setup/verification/records/worktree
and command-approval guidance; native DVC recipe; current splitting and
initialization identity implementations. No new scope conflict found. Older
milestone-at-gates prose remains superseded by current verification policy.

| Reference surface | Reuse / conclusion |
|---|---|
| Existing split record | Preserve full 1.0 keys, original seed/protocol, memberships and bare Parquet SHA; no second split ID |
| DVC recipe | Committed .dvc pointer/output/member identity for consumed data and saved split; native hash separate from FileRef SHA |
| Initialization identity | current_identity(root) reads pyproject/lock and delegates Git or wheel validation; reusable internally in the selected experiment environment |
| Git installation | Full pin, lock, installed direct origin/version and project .venv checks retained |
| Wheel installation | Retained archive SHA/lock/origin/payload/version; missing source/build fields remain null, no fabricated SHA |
| Run ownership | Native MlflowClient/existing run; no implicit fluent run or new run database |

## Native environment and commands

Only UV_LINK_MODE=copy was present among UV_/VIRTUAL_ENV overrides;
UV_PROJECT_ENVIRONMENT and VIRTUAL_ENV were absent. No .venv existed at entry.
uv sync --locked --group dev initially failed on the default read-only cache
lock; identical escalated synchronization succeeded, installing 193 packages
into this worktree's own .venv. uv lock --check passed (196 resolved packages).
No dependency or lock edits. Before/after lock SHA-256:
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.
Linux aarch64 / Python 3.12.16; toolkit 0.1.0, MLflow 3.17.2,
scikit-learn 1.9.1, pandas 3.1.0, pyarrow 25.0.1, DVC 3.67.1, skops 0.16.0.
This editable environment proves library feasibility only, not supported normal
installed experiment identity. No macOS/Windows runtime evidence added.

Commands from this worktree (stdout/stderr retained in corresponding logs):

```sh
.venv/bin/python -I .dev-records/verification/us26-ip1-20261114/probe.py
.venv/bin/python -I .dev-records/verification/us26-ip1-20261114/composition_probe.py
.venv/bin/python -I .dev-records/verification/us26-ip1-20261114/composition_trusted_probe.py
```

| Observation | Actual outcome |
|---|---|
| Existing-run save/log/download/load | Main probe exit 0. Native pipeline saved with model.skops, MLmodel, conda.yaml, python_env.yaml and requirements.txt under preprocessing/pipeline; metadata and provenance paths exact |
| Independent fitted scaler | Training [0,2,4], mean 2; loaded transform of 2 is 0, atol 1e-12 |
| Native run values | Parameter C="1", validation_accuracy=0.75, metadata byte equality; RUNNING until explicit FINISHED |
| Process versus validation | FINISHED may retain validation_status failed; toolkit must keep these outcomes distinct |
| Parameter immutability | Conflicting C=2 raises native MlflowException |
| Storage failure | Regular file as artifact root raises NotADirectoryError; status stays RUNNING until explicit FAILED; no privilege-sensitive chmod fixture |
| Ambient fluent run | Explicit client writes requested store while a different store/run is active; unrelated run has no selected tag |
| Custom serialization failure | Main probe raises MlflowException with serialization context; native partial model output absent |
| Composed imputer/scaler/encoder, default skops | Composition probe exit 1: UntrustedTypesFoundException for numpy.dtype becomes MlflowException. Original log/script preserved |
| Explicit bounded skops configuration | Alternate probe exit 0 with serialization_format="skops", skops_trusted_types=["numpy.dtype"]; loaded native transform equals [[-1,1,0],[1,0,1],[97,0,0]], atol 1e-12 |
| Supported parameters, unserializable fitted state | Same fitted built-in composition with extra threading.Lock state raises native MlflowException naming _thread.lock; no return success |

The default composition failure remains a limitation of the native configuration.
The alternative configuration is a proposed serialization decision for Gate 1,
not a product workaround already shipped. It explicitly trusts the required
native numpy type; no automatic broad allow-list or pickle fallback is proposed.
One bounded alternative configuration was investigated and passed; no failed
corrective implementation attempts occurred. No assertions were weakened,
checks skipped, or product suppressions added. Native untrusted-type errors may
have no chained cause, so preserve their message/type as supplied.

Native MLflow does not enforce toolkit conflict/fitted-state/reference/output
preconditions or finalize failed artifact writes. IP2/IP3 must implement and
independently test those obligations. The simple probe metadata/provenance are
native files, not valid full proposed toolkit records. Neither probe tests the
future helper's metadata validator or real DVC/Git linkage.

## Producer comparison and review readiness

US-15's new [producer proposal](../../../US-15-preprocessing/docs/preprocessing.md)
and [native findings](../../../US-15-preprocessing/docs/verification/us-15-ip1.md)
were read without modifying its checkout. Its native clone/fit/transform and
recursive-JSON findings retain exactly the index's preprocessing keys/types.
Its proposed contract uses the same existing partition schema, feature order,
JSON restrictions and M1 composition. No field change is needed. Supplied
reconstruction must not replace original seeded settings/protocol. No custom
component support or M2 restoration is activated.

The producer documents were uncommitted when inspected; hashes are recorded in
the raw manifest. Its report still describes consumer findings as pending. This
report supplies those findings for its owning session to reconcile, not approval
or mutation of its plan. Both Gate 1 developer decisions remain required before
IP2. Consumer schema comparison does not claim the producer gate is complete.

[Proposed tracking contract](../experiment-tracking.md) supplies exact call and
script outline, paths, native serialization choice, lifecycle/error boundaries,
provenance/identity reuse and independent/integration verification ownership.
The shared index remains the single exact field/type specification. T1/T2/T3
are technically complete on the consumer side; joint developer review is pending.

No executable toolkit behavior changed, so TDD red/green, pytest and full
executable shared checks do not apply at this contract-only gate. Document
links/anchors/whitespace were checked: 77 local targets/anchors passed via the
retained validate.py script, and git diff --check passed. The initial inline
checker mistook an existing directory target for a missing file; its target
classification was corrected without changing any document link. Lock
consistency and native probes ran.
Lint, format, typing, CLI and focused regressions remain IP2/IP3 obligations;
M1–6 and actual direct/rebuilt installed handoff remain IP4. No build,
standalone artifact driver or broad suite ran. AC-01–05 remain unverified.
Gate 1 is Pending. Phase 2 is not authorized; historical M1/M50 and revised MVP
verification owners remain unchanged.
