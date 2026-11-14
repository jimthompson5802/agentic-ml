# US-15 / US-26 complete-metadata feasibility revision

2026-11-14 UTC; approved revision US-15-US-26-SC-01. HEAD at execution:
864a37706e772e7de8f243cbb44d799c36a19d38, branch US-15-preprocessing.
This is renewed Phase 1 feasibility, not executable toolkit implementation.

The previous US-15 native probe verified transforms but did not serialize all
effective settings. Default SimpleImputer.missing_values is NaN and default
OneHotEncoder.dtype is the numpy.float64 class. Earlier broad metadata-feasibility
claims were incomplete. Preserve the original observations and report; this
revision supplies the missing evidence and supersedes their contract conclusion.

Reviewed the current producer/consumer contracts, consumer native composition
failure/success scripts and report, shared index, owning plans/checkpoints,
registered worktrees, verification policy and evidence-retention rules.
The prior complete issue discussions remain the scope source; no new issue
criterion or external issue change is introduced by the representation revision.

## Verification

Command, exit 0:

```sh
.venv/bin/python -I .dev-records/verification/20261114-us15-contract-revision/probe.py
```

The retained script is a throwaway representation feasibility probe, not the
proposed fit_preprocessing/log_preprocessing implementation. It calls existing
public create_partitions, native sklearn and native MLflow; it does not introduce
product code or public behavior tests. The metadata is assembled in the probe
using the proposed eight exact top-level fields and existing partition record.

| Check | Actual result |
|---|---|
| Recursive native effective settings | Complete nested Pipeline/ColumnTransformer/imputer/scaler/encoder settings encoded, including defaults |
| Literal missing-value tag | SimpleImputer.missing_values becomes exactly {kind: missing_value, value: nan}, as strings |
| Literal dtype tag | OneHotEncoder.dtype becomes exactly {kind: numpy_dtype, name: float64} |
| Strict JSON round trip | json.dumps(..., allow_nan=False) and json.loads preserve complete record |
| Ordinary numpy values | Finite scalar and numeric array become ordinary JSON values; dtype object becomes tagged descriptor |
| Rejection boundaries | NaN outside imputer parameter, both infinities, callable, opaque object, literal reserved-tag map and cycle all rejected |
| Native existing-run logging | Explicit client records metadata/model at preprocessing/metadata.json and preprocessing/pipeline |
| Metadata download | Exact bytes and parsed record equal input |
| Native serialization | Explicit skops with only numpy.dtype trust saves and loads successfully |
| Loaded model | Literal transforms [[-1,1,0],[1,0,1],[98,0,0],[198,1,0],[998,0,1],[1998,0,0]] agree at abs/rel 1e-12; encoded settings unchanged |

Probe passed on first execution. Linux aarch64 / Python 3.12.16; sklearn 1.9.1,
numpy 2.5.4, MLflow 3.17.2, skops 0.16.0, pandas 3.1.0, pyarrow 25.0.1,
toolkit 0.1.0. Existing story-specific locked environment reused. No dependencies
changed; before/after lock SHA-256 remains
6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.
Native warnings: no predict flavor for transformation-only pipeline; pip absent
from the editable environment, so generated conda pip requirement was unpinned.
Neither changes project lock requirements or claims installed-environment support.

Raw script, full metadata, summary/version/platform/run identities and downloaded
metadata SHA-256 are retained under
`.dev-records/verification/20261114-us15-contract-revision/`.
The native store/model workspace is `/tmp/us15-contract-4pds_xe_`; lifetime
records retain the metadata and identities independently of that temporary store.
No historical failure logs or evidence were removed.

## Contract reconciliation and limits

The [producer contract](../preprocessing.md) now states exact tags, native dtype
allowlist, reserved parameter-map semantics and bounded serialization. The
[handoff](../plans/us15-us26-contract-revision.md) supplies a patch for consumer
adoption; read-only applicability verification passed against current sibling
files. Those sibling files were not edited by this session. Subsequently US-26
adopted/verified the revision in its own session; US-15 now explicitly
[acknowledges concurrence](us15-sc01-concurrence.md). T3 is Complete and
both Gate 1 decisions remain Pending. The patch remains historical evidence.

Native logging confirms transport preserves the proposed record. No implemented
US-26 validator exists to certify its acceptance; its owning session must renew
schema review. No claimed fit_preprocessing behavior, provenance integrity,
direct/rebuilt-wheel integration or M2 restoration has been verified here.
Original native default-skops failure remains preserved by US-26; explicit
configuration success does not erase it.

TDD and executable shared checks do not apply to this document/native-probe
revision. Public red/green cases belong to IP2/IP3; actual installed handoff
belongs to US-26 IP4. No pytest, distribution driver, full suite or build ran.
No suppression, assertion weakening or product workaround was introduced.

Document validation passed for 74 local paths/anchors across six changed
Markdown documents, whitespace/final newlines, and git diff --check. Consumer
patch applicability passed without applying it. Commands and outcomes are saved
in commands.json; document-validation.json records the link count and lock hash.
