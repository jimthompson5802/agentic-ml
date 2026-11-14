# US-15 Phase 1 producer contract evidence

Date: 2026-11-14 UTC. Issue #21, M1 AC-01/02/03 design/feasibility only.
Base HEAD: `1a9864a645084af8cfcec580b1db5fa045a67859`.
Branch/worktree: US-15-preprocessing / `.worktrees/US-15-preprocessing`.

Developer instruction: “i approve phase 1; commit;”. Phase 1 had not run;
this authorizes its execution and a local commit. It does not approve unseen
results, the US-26 gate, Phase 2 or story acceptance.

## Source and workspace reconciliation

Git's NUL-delimited worktree registration identifies this checkout and branch;
the primary checkout is `/workspaces/agentic-ml` with common Git directory
`/workspaces/agentic-ml/.git`. Existing checkpoint and new plan were the only
initial edits. No branch switch, merge, rebase, fetch or sibling edit occurred.

Complete #21/#17 bodies and all paginated comments were refreshed using:

```sh
sh .codex/scripts/github-read.sh issues/21
sh .codex/scripts/github-read.sh issues/21/comments --paginate --slurp
sh .codex/scripts/github-read.sh issues/17
sh .codex/scripts/github-read.sh issues/17/comments --paginate --slurp
```

Each issue was fetched again: stable updated_at/comment counts; two unique
comments each, no pull_request field, open, null GitHub milestone. Bodies assign
the current M1 scope; #21 AC-04 stays M2. CONTRACT-01 remains accepted direction.
Full snapshots are retained in
`.dev-records/verification/20261114-us15-ip1/issues.json`.
Initial sandbox `gh auth status` failed on DNS/socket permissions; escalated
authentication verification succeeded. No authentication change was needed.

Reviewed the active design reading map, data/features, interfaces, blueprint,
tracking ownership, traceability, milestone delivery, repository layout and
ADR-008; also the development, verification, setup, records, worktrees and
command-approval guides. Issue boilerplate's older milestone-gate schedule is
superseded by the current verification policy as already recorded in the plan.

| Required behavior | Reused capability / remaining helper responsibility |
|---|---|
| Membership/coverage/layout/order | Existing public create_partitions supplied mode validates and reconstructs current partitions |
| Current source identity | Existing native Parquet hash/version record; compare current source to consumed record before fit |
| Seeded provenance | Retain original record; supplied reconstruction does not replace original settings/protocol |
| Training-only fit | Native clone + Pipeline.fit on selected training frame; public helper remains unimplemented |
| Held-out reuse | Returned native Pipeline.transform; no new transformation algorithm |
| Metadata | New ordinary JSON dictionary adapter required; no new split store or parser |
| Persistence/provenance | US-26 consumes actual output; separate provenance remains consumer/project responsibility |

## Native probe and environment

No UV_PROJECT_ENVIRONMENT, VIRTUAL_ENV, CONDA_PREFIX or UV_CACHE_DIR overrides
were present. `uv sync --locked --group dev` initially failed acquiring the
read-only default cache lock in the sandbox; the escalated identical command
succeeded, installing 193 packages in this worktree's `.venv`.

`sha256sum uv.lock` before/after:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
Linux aarch64, Python 3.12.16; toolkit 0.1.0, pandas 3.1.0, pyarrow 25.0.1,
scikit-learn 1.9.1. No dependency/lock changes.

Command (exit 0):

```sh
.venv/bin/python .dev-records/verification/20261114-us15-ip1/native_probe.py
```

The retained probe and `native-probe.log` record these independently asserted
native observations:

| Probe | Actual result |
|---|---|
| Train x=[1,3], scaler | All six rows transform to [-1,1,98,198,998,1998]; inference 5 becomes 3; abs/rel tolerance 1e-12 |
| Clone | Original scaler has no mean_ after cloned fitting |
| Imputer trained [1,null,3] | Statistic 2; transformed [1,2,3,100] |
| Nested imputer/scaler + encoder | [[-1,1,0],[1,0,1],[98,0,0]] for train a/b and held-out c |
| Native schema | numeric__x, category__cat_a, category__cat_b; float64 |
| Effective parameters | Pipeline exposes memory/steps/transform_input/verbose; ColumnTransformer includes native defaults |
| Direct parameter JSON | Expected TypeError for nested ColumnTransformer; recursive JSON conversion required |
| Missing category column | Expected native ValueError identifying missing cat |
| All-null default imputation | Native warning and output width zero; declared nonempty output must reject mismatch |

These are native feasibility probes, not public helper tests or acceptance
evidence. The numeric array can serve both layout oracles but does not verify
toolkit membership selection. No toolkit executable behavior changed, so TDD,
pytest, lint, formatting, mypy and CLI acceptance checks are not applicable to
this contract-only phase; executable shared checks remain IP2/IP3/IP4 obligations.
No full suite, build or standalone artifact driver ran. No corrective attempts
were needed for a behavior failure; sandbox retries were permission recovery.

## Review status and limits

T1 and T2 complete. [Proposed producer contract](../preprocessing.md) records
the exact interface, schema, native reuse, error ordering and public boundaries.
It retains the shared index's representation without modifying another story's
checkout. The existing plan's literal fixture matrix remains proposed for Gate 1.

T3 is partial: the producer proposal is prepared, but US-26-IP1-T1/T2 are still
Not started in its owning plan. No consumer feasibility report or joint schema
confirmation exists. Shared index finalization must wait for those findings in
the owning session. This is a dependency, not a completed joint review.

Gate 1 remains pending; Phase 2 requires both stories' Gate 1 approvals and its
execution authorization. AC-01/02 implementation and AC-03 installed integration
remain unverified. AC-04 remains M2. Historical M1/M50 and revised MVP verification
obligations remain open. This Linux probe makes no macOS/Windows claim.

## Document validation

Local path/anchor and whitespace/final-newline checks passed for all four
changed documents: 65 local links. `git diff --check` passed. The first local
link-check script incorrectly required every target to be a file and rejected
the existing directory link `docs/verification/`; correcting the validator to
accept existing directories passed without altering that link. Both the initial
diagnostic and successful result are recorded in the retained
`document-validation.json`. No project assertions or check exclusions changed.
