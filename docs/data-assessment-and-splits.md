# Data assessment and recorded partitions — approved IP1 contract

**Status:** IP1 contract approved for [issue #19](https://github.com/jimthompson5802/agentic-ml/issues/19),
M1 / US-12-AC-02 and US-12-AC-03. None of the functions below exists yet.
Developer selected only `assess_data` and `create_partitions` in this conversation;
“make the update” authorizes the corresponding documentation revision.
Developer “i approve ip1; commit changes”, 2026-11-07 UTC, confirms the contracts,
policies, dependency scope and public test boundaries below at Gate 1 in the
[owning plan](plans/milestone-1-us-12-assessment-splits.md).

## Selected helper scope and confirmed contract choices

| Choice | Recommendation and reason | Alternative |
|---|---|---|
| Assessment | Retain `assess_data` to assemble native pandas results into plain JSON values. It computes no replacement statistics. | Report/scalar policies below confirmed at Gate 1. |
| Seeded layouts | Retain `create_partitions` to compose native calls and record effective settings beside membership. | Signature, composition and settings below confirmed at Gate 1. |
| Supplied membership | Retain pandas duplicate, membership and intersection checks within `create_partitions`. | ID domain, nonempty/complete coverage and protocol limits below confirmed at Gate 1. |
| Persistence/identity | Project code saves/loads JSON records; no toolkit read/write helpers. `create_partitions` returns source identity and exact membership. | Native Parquet identity contract confirmed; executable stability evidence remains IP3 work. |

The two-helper surface and project-owned persistence are selected under
US-12-19-SC-03 in the owning plan. Row-ID, coverage and source-identity policies
below are confirmed for implementation at Gate 1. Using either helper is optional for project scripts;
running an experiment does not require saving or loading a record. The issue
still requires recorded membership/disjointness and installed verification.
No new manifest service,
custom split/statistics algorithm or runtime approval mechanism is proposed.

## Proposed assessment boundary

```python
from agentic_ml.data_assessment import assess_data

report = assess_data(frame, target="label")  # -> dict[str, object]
```

Input is a native DataFrame with unique, nonempty string column names and an
existing target. Return `schema_version="1.0"`, `row_count`, `target`, ordered
`columns`, and `target_balance`. Each column entry contains `name`, `dtype`,
`missing_count`, `missing_rate`, and either `summary` or `frequencies`.

Use [`Series.describe`](https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html)
on real numeric columns with percentiles `[0.25, 0.5, 0.75]`; retain fields
`count`, `mean`, `std`, `min`, `25%`, `50%`, `75%`, `max`. Other supported columns
use [`value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
with `sort=False, dropna=True`, represented as ordered lists of
`{value, count, proportion}` rather than JSON object keys. Use native normalized
counts for proportions, with the nonmissing denominator. The target always gets
this frequency representation, even when numeric. Preserve categorical order
and zero-count categories as returned by pandas; do not truncate high cardinality.

Missingness uses [`isna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html)
and column sums; rates use all rows. Empty-frame rates are `null`. Missing target
count is separate from observed target balance; an all-missing target has no
observed values (declared categorical levels may have zero counts).

Adapter scalar policy: Python JSON scalars; timestamps use ISO 8601 with timezone
offset when present; pandas missing values and nonfinite numeric summary results
become `null`. Preserve infinity frequency values through explicit strings
`"Infinity"`/`"-Infinity"` only for float columns, identified by their dtype.
Report no quality-pass flag. Numeric infinity is not missing under native `isna`.
This encoding choice is confirmed at Gate 1; it is a toolkit policy.

Support real integer/float, nullable equivalents, boolean, string, categorical
with supported scalar levels, datetime and timezone-aware datetime columns.
Object columns must contain only strings and missing values; reject nested,
mixed or arbitrary Python objects, complex, timedelta and unsupported extension
dtypes with `TypeError` identifying the column. Reject invalid names/target with
`ValueError`; non-DataFrame input gives `TypeError`. Preserve input data, dtypes,
index and caller cwd. No implicit coercion, imputation or statistical approval.

Literal oracle: `value=[1,3,5,null]`, `label=[A,A,B,null]` gives row count 4,
missing counts 1/rates 0.25 in both columns; numeric count 3, mean 3, sample std 2,
min 1, quartiles 2/3/4, max 5. Target entries A=2 at 2/3 and B=1 at 1/3;
missing target count 1. Compare finite floats with `rel_tol=1e-12,
abs_tol=1e-12`; counts/names/memberships are exact. Singleton numeric std and
empty/all-missing numeric summaries have `null` where pandas returns missing.
Test boolean/string/category/datetime, unused levels, null targets, infinities,
empty frames and each rejected type separately; `json.dumps(..., allow_nan=False)`
must succeed. Assert the caller frame is unchanged.

Project code owns report persistence using standard JSON/file operations in
an explicit project path. The toolkit provides no assessment or partition
read/write functions.

## Proposed partition boundary

```python
from agentic_ml.splitting import create_partitions

parts, record = create_partitions(
    frame, row_id="id", target="label", layout="train_test",
    seed=42, test_size=0.4, shuffle=True, stratify=False,
)
# Three-way: layout="train_validation_test", validation_size=0.2
# Supplied: memberships={"train": [1, 2, 3, 4], "test": [5, 6]},
#           protocol={"kind": "time", "column": "observed_at"}
```

Proposed keyword contract: required `row_id: str`, `target: str`,
`layout: Literal["train_test", "train_validation_test"]`; optional
`seed: int | None = None`, `test_size: float | None = None`,
`validation_size: float | None = None`, `shuffle: bool = True`,
`stratify: bool = False`, `memberships: Mapping[str, Sequence[str | int]] | None
= None`, `protocol: Mapping[str, object] | None = None`.
Return `(dict[str, DataFrame], dict[str, object])`. No new request/result classes.

Generation requires an explicit seed and test fraction; three-way also requires
validation fraction, both expressed relative to the original frame. Fractions
must be finite and positive with sum below 1. Two-way forbids validation size.
Supplied mode forbids seed/fractions and requires default shuffle/stratify flags;
record those flags as inapplicable rather than implying shuffling supplied rows.
Seed excludes booleans and follows the native accepted integer range. No silent
stratification: it is an explicit boolean selecting the named target series.

Use native [`train_test_split`](https://scikit-learn.org/1.9/modules/generated/sklearn.model_selection.train_test_split.html):
reserve test first; in three-way mode split the remainder with
`test_size=validation_size/(1-test_size)`. Each call uses the same integer
`random_state=seed` and explicit shuffle/stratification choice; the second call
uses the remainder's aligned target. Keep native size/error behavior. Store
actual results; requested proportions need not equal realized proportions.
Native small-data/class-size failures remain errors, with stage context added
without replacing their exception type. No retry/fallback or allocation repair.

Row IDs must be unique/nonmissing homogeneous strings or integers, excluding
booleans; do not use the DataFrame index as identity. Normalize integer scalars
to Python ints without float coercion. Require exact keys `train,test` or
`train,validation,test` for the layout, nonempty partitions, complete source
coverage, no unknown IDs, duplicates within partitions or intersection across
partitions. These stronger coverage/nonempty policies are confirmed at Gate 1.
Use native pandas checks and index lookup; preserve supplied order and generated
native order. Return independent copies with original columns/target/index.
Reject unsupported argument types with `TypeError`; invalid values/layouts or
membership with contextual `ValueError`.

Supplied protocol is a recorded JSON declaration: `kind` is `supplied`, `time`
or `group`; time/group require an existing named column. Optional `description`
is a string. Protocol defaults to `{"kind":"supplied"}` in supplied mode and
is prohibited in generated mode. Validate declaration shape, then record it.
Generic membership checks do not certify chronological separation or group
separation. Tests assert those properties independently on controlled fixtures;
automatic protocol inference/generation/certification is outside #19.

## Source identity and record proposal

Partition record version `1.0` contains exactly `schema_version`, `layout`,
`row_id`, `target`, `source`, `method`, `settings`, `protocol`, `memberships`.
`method` is `seeded` or `supplied`; protocol is null for seeded records.
Membership values are ordered JSON arrays retaining scalar types.
Seeded settings store the requested seed/fractions/flags and a `calls` array
containing each effective native call's sizes/random state/stratification target.
Supplied settings are empty, with no fabricated seed or library calls.

`source` contains row count, ordered name/dtype schema, SHA-256, identity format
`pandas-parquet-v1`, and exact toolkit/pandas/pyarrow/scikit-learn versions.
For the hash, take a copy with cleared `attrs`, serialize through native
[`to_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html)
with `engine="pyarrow", index=False, compression=None`, then SHA-256 those bytes.
Record native dtype metadata (including categorical levels/order and datetime
timezone) in the serialized payload; compare ordered schema separately.
No caller checksum or extraction report substitutes for hashing consumed rows.
The index and attrs are intentionally excluded; row/column order and all column
values, including target and IDs, participate. Unsupported serialization fails.

This is version-bound native serialization, not universal canonical hashing.
`create_partitions` computes identity for the frame it actually receives. It does
not accept an entire saved record or verify its old checksum/library versions.
Comparing saved/current identities belongs to project code and requires matching
serialization versions for meaningful byte comparisons. Recorded versions are
provenance, not a toolkit restoration compatibility gate.
IP3 must test repeat serialization, supported dtype sensitivity and JSON round-trip;
any failure invalidating this proposal reopens IP1 before dependent changes.
External file/DVC identity remains the project/US-13 responsibility. This local
record is not authenticated against a writer who changes both data and record.

## Project-owned persistence and reconstruction

The following is proposed project code; it is not an additional toolkit API.
Here `root` is the project's explicit absolute path and `records/` already exists.

```python
import json

path = root / "records/split.json"
with path.open("x", encoding="utf-8") as stream:
    json.dump(record, stream, allow_nan=False)
with path.open(encoding="utf-8") as stream:
    saved = json.load(stream)

# Project code checks the saved document's shape/version and any required
# source identity before selecting these arguments.
reconstructed, new_record = create_partitions(
    frame,
    row_id=saved["row_id"],
    target=saved["target"],
    layout=saved["layout"],
    memberships=saved["memberships"],
    protocol=saved["protocol"],
)
```

Reconstruction uses supplied mode, so a formerly seeded record produces a new
`method="supplied"` record; keep the original record for generation provenance.
Do not pass saved seed/fractions to supplied mode. `create_partitions` checks
layout/keys, IDs, coverage and disjointness against the current frame. Existing
IDs with changed feature/target values do not fail membership validation; project
identity comparison can detect that change separately. Record-shape/version
checks, JSON parsing, missing/corrupt files, paths, write conflicts and partial
writes are project responsibilities. No toolkit file parser, atomic publication,
old-source validation or saved-record restoration guarantee is delivered.

## Independent partition and installation matrix

| Case | Literal expected observations | Boundary/limit |
|---|---|---|
| Seeded two-way | IDs 0–4 in source order, seed 42, test 0.4, unstratified/shuffle true: train `[2,0,3]`, test `[1,4]` | First split agrees with the documented native example; no validation key. |
| Seeded three-way | Same source/settings plus validation 0.2: train `[0,3]`, validation `[2]`, test `[1,4]` | Independently confirmed through native scikit-learn 1.9.1 calls during IP1 completion; no toolkit code invoked. |
| Native rounding | 5 rows and test 0.3 gives 2 test/3 train rows | No custom rounding implementation. |
| Impossible sizes | One row/two-way and two rows/three-way at the above fractions fail | Preserve native exception; no fallback. |
| Stratification | Balanced controlled labels; assert literal class counts and aligned rows for both layouts | Add rare-class, missing-target and shuffle-false conflict failures; no quality guarantee. |
| Supplied two-way | IDs 1–6; train `[1,2,3,4]`, test `[5,6]` | No validation frame or placeholder. |
| Supplied three-way | Train `[1,2]`, validation `[3,4]`, test `[5,6]` | Exact rows, target alignment and order. |
| Time/group | For each layout, timestamps ascending by ID; groups assigned separately per partition | Independently assert time order/group separation; record declared protocol only. |
| Membership failure | Separate mutations: overlap, repeated ID, unknown ID, omitted source row, empty member list, missing/extra/unknown partition key | Fail through `create_partitions`, including arguments selected from project-loaded JSON. |
| Declaration failure | Bad names/layout, duplicate/null/mixed/bool source IDs, wrong fractions/mode settings | Separate failure per mutation; no source mutation. |
| Source identity | Same values/dtypes/order with a new index retains identity; supported value/target/dtype/order changes yield a different identity; missing source members fail membership checks | Independently hash native bytes; no comparison against a prior record is performed by the helper. |
| Project JSON round-trip | For both layouts, save/load the record with project JSON code, verify layout/ordered IDs/provenance, then pass selected fields to supplied mode; mismatched layout/keys fails | Reconstruct exact rows with a new supplied record. Project parsing/shape/source checks stay outside the toolkit boundary. |

Removed from toolkit verification under SC-03: dedicated saved-record reader
validation, incompatible-version restoration failures and write-path/conflict/
symlink/partial-publication guarantees. No existing tests are disabled; none of
these proposed helpers/tests had been implemented. Native JSON failure behavior
may be demonstrated in project examples without treating it as toolkit behavior.

Public tests observe returned reports/frames, strict JSON, actual files and
exceptions. They do not mock internal collaborators. Repeated seeds alone are
insufficient evidence. Installed probes repeat all critical families for each
normal direct wheel and sdist-rebuilt wheel, from a separate project and unrelated
cwd under isolated Python. Exercise both retained helpers, supplied time/group cases
for both layouts and required-quality failure blocking preparation through
`run_validated_step`. Retain existing runtime/resource/CLI/origin checks.

## Dependency proposal and review limits

The current lock already contains scikit-learn 1.9.1 transitively. Propose direct
`scikit-learn>=1.9.1,<1.10` in IP3, an intentional lock update, and independent
`scikit-learn<1.10,>=1.9.1` inventory entries in
`tests/packaging/check_installed.py` and `tests/installation/check_project.py`.
The [1.9 API reference](https://scikit-learn.org/1.9/modules/generated/sklearn.model_selection.train_test_split.html)
is the proposed support line, not a claim that future minor releases pass.
No dependency declaration, lock or inventory changes occur in IP1.

IP2 owns assessment TDD and M1/shared checks; IP3 owns partitions/records/dependency
TDD and M1/shared checks; IP4 owns both installed matrices and final M1–6/shared
checks. Gate 1 approves this contract and its test boundaries; IP2 still needs
separate execution authorization. No implementation, notebook, fitting, MLflow/DVC replay or platform
acceptance is established by this proposal. See [IP1 evidence](verification/us-12-19-ip1.md).
