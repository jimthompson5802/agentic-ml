# US-26 concurrence on US-15-US-26-SC-01

2026-11-14 UTC. **US-26 explicitly concurs with US-15-US-26-SC-01** as
specified in the [producer revision](../../../US-15-preprocessing/docs/plans/us15-us26-contract-revision.md)
and revised [producer contract](../../../US-15-preprocessing/docs/preprocessing.md).
There are no unresolved interface differences in the reviewed revision.
This is technical concurrence, not either Gate 1 approval or Phase 2 authority.

## Authority and adoption

The developer-directed owning-session handoff authorizes contract reconciliation
only: adopt the exact encodings and bounded skops choice, update this checkout's
contract/index/plan/checkpoint and verify documents. No commit, push, publication,
Phase 2 implementation or gate approval is authorized. The producer handoff
records the earlier acceptance of the revision recommendation; this report
records the independently authorized US-26 adoption.

Reviewed the revised producer contract, SC-01 plan/evidence, supplied patch,
complete-metadata probe and summary. The patch passed git apply --check against
this checkout's existing dirty documents, then was applied here. No sibling
checkout was edited and no producer implementation was imported or copied.
Owning checkout remains US-26-mlflow at HEAD 131ac82; previous Phase 1 edits
were retained. Input hashes and commands are saved under
.dev-records/verification/us26-sc01-20261114/ for lifetime retention.

## Exact agreement

| Surface | Agreed revision |
|---|---|
| Native NaN sentinel | Exactly {"kind":"missing_value","value":"nan"}, only at built-in SimpleImputer.missing_values |
| Native dtype descriptors | Exactly {"kind":"numpy_dtype","name":"float64"}, with name chosen from bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float16, float32, float64 |
| Ordinary values | Finite Python/numpy scalar instances remain ordinary JSON; other NaN, all infinity, arbitrary callables, opaque objects and cycles remain invalid |
| Reserved parameter maps | Producer rejects caller-supplied literal mappings using either reserved kind. Consumer accepts the resulting well-formed encoded tags in supported contexts; it does not reject all received tag maps |
| Tag validation | Exact keys/values and dtype allowlist; no arbitrary class imports, callable execution or reconstruction API |
| Native serialization | Explicit serialization_format="skops", skops_trusted_types=["numpy.dtype"]; no broad trust discovery or pickle/cloudpickle fallback |
| Unchanged boundaries | Same signatures, eight metadata keys/schema 1.0, existing split record, separate provenance, existing run ID, artifact layout, error ownership and IP4 installed integration |

The [shared index](../plans/milestone-1-us-15-us-26-execution-order.md) and
[tracking contract](../experiment-tracking.md) now record these same rules.
The original [IP1 findings](us-26-recording-ip1.md) remain historical evidence;
the earlier complete-metadata feasibility conclusion is superseded by this
renewal. The default skops composition failure and successful explicit-config
probe remain intact. No prior failure or approval record was removed.

## Independent consumer feasibility

Command from this worktree, exit 0:

```sh
.venv/bin/python -I .dev-records/verification/us26-sc01-20261114/probe.py
```

The throwaway script consumes the producer's full metadata and compares it
recursively with an independently configured fitted Pipeline/ColumnTransformer/
SimpleImputer/StandardScaler/OneHotEncoder. It compares all get_params(deep=False)
keys, class names, ordered steps/transformer selections and ordinary values;
checks the two literal tags, strict JSON, schema/versions/membership, and tag
shape/context/dtype rejection assertions. It then uses native MLflow to
save/log/download/load the same composition with the bounded configuration.
Downloaded metadata bytes equal the producer input; loaded effective settings
and literal transforms agree at abs/rel 1e-12:
[[-1,1,0],[1,0,1],[98,0,0],[198,1,0],[998,0,1],[1998,0,0]].

Producer input and downloaded metadata SHA-256:
37214f3bfc6d42b52532ac9059a916e301af0b4a972aed33ab295adac49ce50c.
The script, full log, summary, metadata and native store/model copy are retained
in this checkout's raw record directory. The probe passed on its first run.
Linux aarch64 / Python 3.12.16; sklearn 1.9.1, numpy 2.5.4, MLflow 3.17.2,
skops 0.16.0, pandas 3.1.0, pyarrow 25.0.1, toolkit 0.1.0.
The existing story .venv was reused; no dependency or lock edits. Lock SHA-256:
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.

This verifies descriptive contract agreement and native transport, not acceptance
by a product validator. Neither proposed toolkit helper exists yet. The negative
tag assertions are feasibility checks, not toolkit public-interface tests.
Provenance integrity and actual installed producer-to-consumer handoff remain
IP2/IP3 and IP4 obligations respectively; M2 restoration is unchanged.

## Review position

US-26 IP1-T2/T3 were reopened for SC-01 and are Complete again with renewed
consumer feasibility and reconciled documents. T1 remains Complete. Both
Gate 1 decisions remain Pending. No product source/tests or executable behavior
changed, so TDD, pytest, lint/type/CLI and full executable shared checks do not
apply to this contract revision. Document path/anchor, whitespace/final-newline
and git diff --check passed: 89 local links/anchors across six documents,
with results retained in document-validation.json.

US-15's owning session must consume this explicit concurrence and finalize its
own T3/records. That is a handoff action, not an unresolved schema difference.
Both developer Gate 1 approvals and explicit Phase 2 authorization are required
before dependent implementation. No commit/push/publication was performed.
