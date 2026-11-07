# Data quality contract

**Status:** Contract approved at US-12 issue #15 Gate 1 by developer
“i approve ip1; commit”, 2026-11-07 UTC. Not implemented; IP2 authorization pending. Examples describe the future public API.
The [implementation plan](plans/milestone-1-us-12.md) owns tasks and approvals;
[IP1 evidence](verification/us-12-ip1.md) records investigation and checks.

## Purpose and scope

Check a native pandas DataFrame against explicit project quality requirements.
Return actionable measurements and stop a dependent project operation when a
required check fails. This addresses US-12-AC-01/05 from
[issue #15](https://github.com/jimthompson5802/agentic-ml/issues/15).
Assessment/distributions and train/validation/test membership belong to #19;
training, DVC stages and the basic experiment runner belong to other stories.

The [extraction API](extraction.md) returns a DataFrame and extraction provenance.
Extraction completion does not mean the data passed quality requirements.
These functions are independent of strict plan-bound `agentic_ml.validation`;
they require neither a formal experiment plan nor an approval record.

## Public interface

Proposed exports from `agentic_ml.data_quality`:

```python
from collections.abc import Callable, Mapping, Sequence

import pandas as pd


def validate_data(
    frame: pd.DataFrame,
    *,
    rules: Sequence[Mapping[str, object]],
) -> dict[str, object]: ...


def run_validated_step[T](
    frame: pd.DataFrame,
    step: Callable[[pd.DataFrame, dict[str, object]], T],
    *,
    rules: Sequence[Mapping[str, object]],
    settings: Mapping[str, object] | None = None,
) -> tuple[T, dict[str, object]]: ...


class DataQualityError(ValueError):
    report: dict[str, object]

    def __init__(self, report: dict[str, object]) -> None: ...
```

`validate_data` performs all configured checks, returning the report even if
required checks fail. It never silently fixes, coerces, drops or reorders data.
It writes no files, changes no cwd and takes no project paths.

`run_validated_step` validates configuration and copies settings, snapshots the
frame with `copy(deep=True)`, checks that snapshot, then either raises
`DataQualityError` or calls `step(snapshot, copied_settings)` and returns its
result with the pre-operation report. An advisory failure does not block.
`settings` must be a mapping with string keys and recursively JSON-compatible
values (null, strings, booleans, finite numbers, lists and string-keyed mappings);
omitting it supplies an empty dictionary. Invalid values fail before invoking
the operation. The `step` argument must be callable, otherwise `TypeError`.
The project operation may transform its private snapshot; the report describes
its input, not the operation's output. The input frame/settings remain unchanged.
Every invocation rechecks its current input; no previous report or success flag
is accepted as permission to proceed. Reports are ordinary mutable dictionaries,
not authenticated evidence or reusable permission records.

Use scalar-valued tabular data: standard pandas integer, floating, boolean,
string, datetime, timedelta and categorical columns, including nullable forms.
Object columns may contain scalar strings, booleans, numbers, dates/times,
timedeltas and missing values, but no containers, arrays or custom mutable
objects. Unsupported cell values raise `TypeError` before checking. This bounds
the copy guarantee: pandas deep copies are not promised to recursively copy
arbitrary Python object graphs. Callers must not concurrently mutate inputs or
rules during a call. Arbitrary external code is trusted, not prevented from
bypassing these functions.

The frame must have unique, nonempty string column names; invalid names or
duplicates raise `ValueError`. Row index labels need not be unique and do not
participate in checks. Non-DataFrame input raises `TypeError`. Empty frames and
zero-column frames are allowed; configured checks determine their suitability.

## Rules

`rules` is an explicitly supplied sequence of mapping objects; an empty sequence
selects no quality checks. The argument is still required, so skipping checks is
an explicit project choice rather than a hidden default. Each rule has a unique,
nonempty string `id`, a supported string `kind`, and optional boolean `required`
(default `True`). The remaining keys below are specific to the kind. Unknown
keys/kinds, duplicate IDs and missing arguments raise `ValueError`; wrong value
types raise `TypeError`. Validate the entire rule configuration before measuring
data so malformed settings cannot masquerade as a quality failure.
Empty rules return `status="not_checked"`, `blocked=False`, and `checks=[]`.
`run_validated_step` then invokes the operation with its copied snapshot. Frame
structure/type, callable and settings requirements still apply; no configured
quality rule runs. `None`, a bare string or a malformed nonempty rule list is
not a way to disable checks.

Numbers in configuration must be finite built-in integers/floats; booleans are
not numbers for thresholds. Counts must be nonnegative integers. Reject inverted
bounds. Copy the rule declarations and record all effective defaults.
Column lists are nonempty lists of unique nonempty strings. Every mentioned
column must exist to evaluate that rule; absence is a **failed check**, preserving
the rule's required/advisory status, not an uncaught pandas KeyError. Other rules
still run. Configuration remains valid if its column is absent from the data.

| Kind | Arguments and defaults | Measurement and success condition |
|---|---|---|
| `columns` | `columns`; `exact=False` | Required names must exist. With `exact=True`, extra names also fail. Compare membership, not order. Record missing/unexpected names in declaration/input order. |
| `dtypes` | `columns`: nonempty mapping of column names to pandas dtype strings | Validate declarations with pandas `pandas_dtype`; compare canonical `str(dtype)` values. `int64` and nullable `Int64` are distinct. String storage backend is not separately checked. No coercion. |
| `row_count` | Optional `min`, `max`; at least one supplied | Inclusive bounds on `len(frame)`. An omitted bound is unbounded and recorded as JSON null. |
| `nulls` | `column`; `max_count=0` | Count pandas missing values using `isna`; pass when count is at most the limit. Empty strings and infinities are not missing. |
| `duplicates` | Optional `columns` (default all frame columns); `max_count=0` | Count excess rows via pandas duplicated with `keep='first'`, ignoring index. For keys `[1,1,1,2]`, count is 2, not 3. Missing keys follow native pandas equality semantics. A zero-column frame cannot evaluate this rule and reports a failed check. |
| `range` | `column`; optional `min`, `max`, at least one supplied | Inclusive numeric bounds on nonmissing real numeric values. Require numeric dtype, excluding booleans and complex numbers; incompatible dtype is a failed check. Count out-of-range values, including positive/negative infinity. Missing values are excluded and counted separately. |
| `allowed_values` | `column`; nonempty `values` list of finite JSON scalar strings/numbers/booleans, excluding null | Native pandas `isin` membership on nonmissing values; count violations. Native equality applies, including numeric/bool equality. Missing values are excluded and counted separately. |

Each rule checks one requirement. Multiple null/range/membership checks use
separate IDs. Omitted `duplicates.columns` expands to actual input columns in
the effective report. Each `range` omitted bound becomes null in the effective
report. All omitted limits/defaults are explicit there. Allowed-value lists keep
declaration order, including repeated values. Configured dtype strings are
recorded canonically. Rule callbacks, expressions, import strings and arbitrary
operator registries are outside this contract; numeric ranges and allowed values
provide configured quality rules without another execution language.

## Results and errors

The complete report has exactly these top-level fields:

```json
{
  "schema_version": "1.0",
  "status": "not_checked",
  "blocked": false,
  "row_count": 4,
  "columns": [
    {"name": "id", "dtype": "int64"},
    {"name": "age", "dtype": "int64"},
    {"name": "group", "dtype": "str"}
  ],
  "checks": []
}
```

This is the complete no-check report for the baseline frame below. It records
shape/dtypes for context but makes no quality-passed claim. Column dtype strings
come from the actual frame, not inference from a saved file. The fixture below explicitly fixes dtypes
so tests do not depend on pandas string inference.

Checks appear in supplied rule order. Each has exactly `id`, `kind`, `required`,
`expected` (the effective rule parameters excluding those first three keys),
`actual` (measurements below), `passed` (boolean), and `message` (nonempty text
identifying the rule and result). Messages must identify missing columns, type
differences or breached limits as applicable; tests assert useful content rather
than exact prose. No row samples or dataset contents are included. Reports are
strictly JSON serializable with `json.dumps(report, allow_nan=False)`.

| Kind | `actual` shape on evaluable data |
|---|---|
| `columns` | `{"missing": [...], "unexpected": [...]}`; unexpected is empty unless exact mode |
| `dtypes` | `{"dtypes": {"column": "actual dtype", ...}}` in declaration order |
| `row_count` | `{"count": 4}` |
| `nulls` | `{"count": 0}` |
| `duplicates` | `{"count": 0}` |
| `range` / `allowed_values` | `{"invalid_count": 0, "missing_count": 0}` |

A rule referencing missing columns has `actual={"missing_columns": [...]}` and
`passed=False` instead of that normal shape (the `columns` rule uses its normal
missing/unexpected shape). A range with incompatible dtype has
`actual={"dtype": "actual dtype", "reason": "non_real_numeric"}`; a zero-column
duplicate check has `actual={"reason": "no_columns"}`. Nulls count as missing
regardless of nullable/NumPy representation; normalize measurement scalars to
built-in JSON types. Do not serialize NaN/infinity as report numbers.

`status` is `not_checked` when no rules were supplied, `passed` when a nonempty
set of checks all passes, and `failed` when any configured check fails. `blocked` is
true iff at least one **required** check fails. Thus an advisory-only failure
has `status='failed', blocked=False` and still permits the operation. A required
failure raises `DataQualityError` only in `run_validated_step`; its `.report`
contains the same report that direct validation would produce, and its message
names failed required rule IDs. This is configured data validation failure.

Invalid input/configuration raises the specified built-in error without a
partial success report. Unexpected pandas errors propagate rather than becoming
ordinary failed checks. Project operation exceptions retain their type, instance
and traceback, with a note naming the validated-operation stage; they are process
errors, not `DataQualityError`. No operation is called on input/configuration or
required-check failure. No automatic file persistence or output cleanup is
promised for project operations; project code owns its files and paths.

## Example and independently expected results

Proposed future use (Python 3.12+, not runnable before IP2):

```python
import pandas as pd

from agentic_ml.data_quality import run_validated_step, validate_data

frame = pd.DataFrame({
    "id": pd.Series([1, 2, 3, 4], dtype="int64"),
    "age": pd.Series([20, 35, 40, 50], dtype="int64"),
    "group": pd.Series(["A", "B", "A", "C"], dtype="str"),
})
rules = [
    {"id": "schema", "kind": "columns", "columns": ["id", "age", "group"], "exact": True},
    {"id": "types", "kind": "dtypes", "columns": {"id": "int64", "age": "int64"}},
    {"id": "rows", "kind": "row_count", "min": 4, "max": 4},
    {"id": "age_present", "kind": "nulls", "column": "age"},
    {"id": "unique_id", "kind": "duplicates", "columns": ["id"]},
    {"id": "age_bounds", "kind": "range", "column": "age", "min": 0, "max": 120},
    {"id": "known_group", "kind": "allowed_values", "column": "group", "values": ["A", "B", "C"]},
]
report = validate_data(frame, rules=rules)


def prepare(data, settings):
    return data.loc[:, settings["columns"]].copy()


prepared, input_report = run_validated_step(
    frame, prepare, rules=rules, settings={"columns": ["id", "age"]}
)
```

Each entry in `rules` declares one check. `id` is the project-chosen name used
in the report; `kind` selects the check to perform. The remaining fields configure
that check. Here is what each rule in this example does:

| Rule ID | Meaning in this example |
|---|---|
| `schema` | Require exactly the columns `id`, `age` and `group`. A missing or extra column fails; column order does not matter. |
| `types` | Require `id` and `age` to have pandas dtype `int64`. This rule does not check the dtype of `group` or convert any values. |
| `rows` | Require exactly four rows: both the minimum and maximum are 4. |
| `age_present` | Allow no missing ages. Omitting `max_count` uses its default of 0. |
| `unique_id` | Allow no repeated IDs. Omitting `max_count` uses 0, so every row must have a distinct `id`. |
| `age_bounds` | Require every nonmissing age to be between 0 and 120, including both endpoints. The separate `age_present` rule catches missing ages. |
| `known_group` | Require every nonmissing group value to be `A`, `B` or `C`. This rule permits missing groups; add a `nulls` rule for `group` if they must be prohibited. |

All seven checks are required because `required` defaults to `True`. Setting
`required=False` on a rule makes its failures advisory: they appear in the report
but do not prevent `prepare` from running. Supplying `rules=[]` instead runs no
quality checks, reports `not_checked`, and allows `prepare` to run.

In this example, `prepare` selects the `id` and `age` columns. The
`run_validated_step` call checks its input before calling `prepare`; a required
failure stops that call. `prepared` is the selected DataFrame, and `input_report`
describes the data checked before column selection.

The baseline has seven passing checks, `status='passed'`, `blocked=False`,
row_count 4, no missing/unexpected columns, id/age dtype `int64`, zero nulls,
zero duplicate rows and zero range/membership violations or missing values.
One complete expected check is:

```json
{
  "id": "age_present",
  "kind": "nulls",
  "required": true,
  "expected": {"column": "age", "max_count": 0},
  "actual": {"count": 0},
  "passed": true,
  "message": "age_present: age has 0 missing values; maximum 0"
}
```

The message above is illustrative; its text is not a byte-stable interface.
Alter baseline copies independently, never accumulate mutations across cases:

| Fixture change / isolated check | Literal expectation |
|---|---|
| Remove age | schema missing `["age"]`; types/age_present/age_bounds report missing_columns `["age"]`; four failed checks, blocked |
| Add extra column | schema unexpected `["extra"]`; other six checks pass |
| Cast age to float64, keeping values | types reports age `float64`; only types fails |
| Drop final row | rows actual count 3; other six checks pass |
| Add row `(5,60,A)` | rows actual count 5; other six checks pass |
| Set one age missing in an Int64 series | types fails (`Int64` versus `int64`), null count 1 fails, range invalid_count 0/missing_count 1 passes; isolate null behavior by adjusting expected dtype in that test |
| Change id 2 to id 1 | duplicate count 1; other six checks pass |
| Set one age to 121 | range invalid_count 1/missing_count 0; only age_bounds fails |
| Set one group to Z | membership invalid_count 1/missing_count 0; only known_group fails |
| Age `[0,120,40,50]` | inclusive bounds pass, zero range violations |
| Empty baseline frame, preserving dtypes | row_count 0 fails; schema/types and zero-null/duplicate/violation checks pass |
| All-null Int64 age, isolated null/range checks | null count 4; range invalid_count 0/missing_count 4; add required null check to block |
| Keys `[1,1,1,2]`, isolated duplicate check | count 2; max_count 2 passes and max_count 1 fails |
| Floating ages `[20,+inf,-inf,NaN]`, isolated range check | invalid_count 2, missing_count 1; report contains only finite measurements |
| Non-numeric age, isolated range check | dtype/reason failure, not a comparison crash |
| Explicit `rules=[]`, including data violating the usual rules | status not_checked, blocked false, empty checks; operation produces its sentinel; data is not labeled validated |
| One failure made advisory | failed status, blocked false; operation produces its sentinel |
| Mixed required/advisory failures | blocked true; no sentinel; failed required IDs available in exception |
| Mutate valid age to 121 between calls | first operation runs; next call blocks without reusing first report |

Also verify malformed/unknown rule keys, duplicate IDs, invalid dtype declarations,
negative/boolean/nonfinite thresholds, inverted limits, missing bounds, empty
column lists/allowed values, invalid frame/column labels, unsupported object
cells and missing referenced columns in advisory checks. Verify whole-row
duplicates, missing duplicate keys, nonunique index labels, exact=False extra
columns, nullable types with matching declarations, no input/settings/rules
mutation, strict JSON serialization, and original project exception identity.

## Public test boundaries and installation handoff

Developer confirmed these boundaries and literal fixtures at Gate 1 on
2026-11-07 UTC (“i approve ip1; commit”). IP2 tests call only the exported functions/error with tiny frames;
they compare literal expected dictionaries/counts and pandas frame equality.
A project operation creates a sentinel file under its explicit fixture root:
required failure must leave it absent; valid/advisory-only/no-check inputs must produce
the expected content. Assert that the consumed values match the checked data,
and that mutation inside the operation leaves caller inputs/settings unchanged.
Use real operations, not private-method tests or mocked internal collaborators.

IP3 adds these contributor-only files:

- `tests/installation/data_quality_project.py`: project functions/rules and
  sentinel operation, copied into an independent experiment directory.
- `tests/installation/check_data_quality.py`: isolated runtime-only probe loading
  the project module by file location; imports installed public APIs; verifies
  baseline and all rule families, explicit no-check operation, malformed input, advisory/required behavior,
  callback errors, JSON roundtrip and literal extraction-to-quality results.
- `tests/installation/verify_data_quality.py`: composes existing
  `tests/packaging/verify_distributions.py` through `verification_support.Invocation`,
  runs copied probes using each retained environment's Python with `-I`, and
  preserves per-path identity/check summaries before cleanup.
- `tests/integration/test_distribution_verification.py`: new M1 case
  `test_data_quality_from_both_artifact_paths` reuses the existing module artifact
  fixture and distribution xdist group; invokes the driver from an unrelated cwd.

Both direct and sdist-rebuilt normal installs must pass unchanged origin/runtime
inventory/CLI/resource checks first. Record import paths, artifact/version/tool
identities, project cwd, observations and cleanup. A probe failure on either path
fails acceptance even if the other passed. Do not import contributor tools in
installed projects, edit the toolkit checkout from them, substitute the direct
wheel for the rebuilt wheel, or require editable installs. The new driver follows
existing output/retention/error contracts; preserve current timeouts and skips.
No new dependency, runtime resource, schema registry or CLI verb is needed.

Tests prove the component boundary, not adopted enforcement in future runners,
training correctness, split quality, scientific validity or hostile-code
isolation. Future US-10/14/15/18/39 consumers must call the reviewed boundary
immediately before their affected operation and add their own integration
evidence; they may not treat extraction completion or a stored report as passing
validation. This handoff adds no tasks or acceptance claims to those stories.
