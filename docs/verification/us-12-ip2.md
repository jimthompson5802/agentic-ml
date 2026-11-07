# US-12 #15 IP2 verification

## Scope and boundaries

Developer “start ip2” authorized IP2 after the IP1 gate confirmed the public
boundaries in [the contract](../data-quality.md). Baseline `ec82d75`; branch
`US-12-data-validation`. AC-01/05 cover native-frame checks and the synchronous
blocking boundary. Installed direct/rebuilt wheel probes remain IP3-T1–T3;
final M1–6 verification and excluded coverage reconciliation remain IP3-T4.
No runner, assessment, partition, notebook, DVC or assistant integration is claimed.

Changes introduce `agentic_ml.data_quality` and public-interface tests in
`tests/integration/test_data_quality.py`. Seven rule kinds report effective
parameters and measurements; required failures prevent a step, while advisory and
explicit no-check modes proceed. The step receives a fresh snapshot and copied
settings. Invalid declarations, unsupported cells and project failures remain
distinct from configured failed checks. The approved contract describes limits.

## TDD and correction evidence

Each new missing behavior was exercised through the public interface with
`uv run --locked pytest tests/integration/test_data_quality.py -k <behavior>`
before its implementation, then through the whole focused file. The plan records
the initial slices. Subsequent intended failures covered range/membership,
blocking, missing columns, non-scalar values, duplicate IDs, copied settings,
nonfinite and non-string-key settings, exception notes, unknown keys, bad frame
columns, inverted bounds, nonnumeric ranges, zero-column duplicates, malformed
rule parameters, invalid range bounds and column lists, invalid IDs and kinds,
report aliasing, invalid allowed values and dtypes, noncallable steps, unsupported
object/categorical values, row-limit diagnostics and scalar booleans. Tests for
already established behavior were added as passing regressions, including the
seven-rule literal baseline, empty and nullable inputs, changed-data recheck,
mixed required/advisory failures, no-check sentinel and input preservation.
The latest complete focused run selected all 95 cases and passed. Serial
execution keeps these small public-interface cycles short. The contract's
Python example was executed with `.venv/bin/python` and produced the expected
passing report and selected columns. A separate public-interface probe verified
duplicate count 2 passes maximum 2 and fails maximum 1, native boolean/numeric
membership, and strict JSON serialization.

```sh
.venv/bin/python -c 'import json,pandas as pd; from agentic_ml.data_quality import validate_data; frame=pd.DataFrame({"key":[1,1,1,2],"value":[0,120,40,50]}); a=validate_data(frame,rules=[{"id":"dup","kind":"duplicates","columns":["key"],"max_count":2}]); b=validate_data(frame,rules=[{"id":"dup","kind":"duplicates","columns":["key"],"max_count":1}]); assert a["checks"][0]["actual"] == {"count":2} and a["status"] == "passed"; assert b["checks"][0]["actual"] == {"count":2} and b["blocked"]; c=validate_data(pd.DataFrame({"key":[1,2]}),rules=[{"id":"membership","kind":"allowed_values","column":"key","values":[True,2]}]); assert c["status"] == "passed"; json.dumps(c,allow_nan=False); print("duplicate threshold and native membership: passed")'
.venv/bin/python -c 'import pandas as pd; from agentic_ml.data_quality import validate_data; f=pd.DataFrame({"age":[20.0,float("inf"),float("-inf"),float("nan")]}); r=validate_data(f,rules=[{"id":"r","kind":"range","column":"age","min":0,"max":120}]); assert r["checks"][0]["actual"]=={"invalid_count":2,"missing_count":1}; f=pd.DataFrame({"age":pd.Series([1,None],dtype="Int64")}); r=validate_data(f,rules=[{"id":"n","kind":"nulls","column":"age"},{"id":"r","kind":"range","column":"age","min":0}]); assert r["checks"][0]["actual"]=={"count":1} and r["checks"][1]["actual"]=={"invalid_count":0,"missing_count":1}; print("infinite bounds and nullable missing values: passed")'
```

The focused commands used the exact prefix
`uv run --locked pytest tests/integration/test_data_quality.py -k` followed by
these selectors (each initially failed for the behavior described by its test,
then the whole focused file passed): `passing_row_count`, `explicit_no_checks`,
`schema_reports`, `dtype_mismatch`, `unknown_rule`,
`invalid_row_count_minimum`, `null_rule`, `duplicate_rule`, `range_counts`,
`allowed_values`, `required_failure_blocks`, `missing_referenced`, `non_scalar`,
`duplicate_rule_ids`, `step_mutations`, `invalid_settings`, `project_exception`,
`unknown_rule_key`, `invalid_frame_column`, `inverted_row_count`,
`range_on_string`, `duplicate_rule_on_zero`, `missing_rule_parameters`,
`wrong_rule_parameter`, `invalid_range_bounds`, `invalid_duplicate_column`,
`missing_or_empty_rule_id`, `nested_settings`, `invalid_rule_container`,
`report_does_not_alias`, `invalid_allowed_values`, `dtype_rule_accepts`,
`invalid_column_argument`, `noncallable_step`, `non_boolean_exact`,
`wrong_dtype_declaration`, `non_string_rule_id`, `invalid_pandas_dtype`,
`non_dataframe_is_rejected`, `non_string_rule_kind`, `nested_read_only`,
`complex_object`, `none_rule_parameter`, `unsupported_period`, `decimal_object`,
`custom_object_with_datetime`, `row_count_failure_message`,
`numpy_boolean_scalar`, `custom_categorical`, and `unused_custom_category`.
Some parameterized selectors include several independently checked values; all
selected cases passed after their implementation. Passing regressions were run
without claiming a new red phase for behavior already implemented.
The red/green console transcripts were not saved as raw log files; commands,
observed failure categories and correction attempts are recorded here and in
the plan. The gate's M1 JUnit is retained separately.

The initial missing-column correction put the check in the configuration loop;
the original test still raised `KeyError`. The second attempt moved the check to
measurement and passed the original test and focused regressions. A later mypy
failure in the seven-rule fixture took three corrections: removing a redundant
cast and annotating a different rule list did not fix its inferred `list[object]`;
annotating the actual fixture list passed mypy and focused regressions. Other
type/format issues found by development checks were corrected on their first
attempt. Further focused red–green cases covered object and categorical scalar
handling, row-limit diagnostics and nested mapping settings. No assertions were
weakened and no suppressions or skips were added.

## Verification

Linux aarch64, Python 3.12.16, uv 0.13.6. The first M1 run passed 503 with one
existing skip (504 selected), a later run passed 511 with one existing skip
(512 selected), and a third passed 526 with one existing skip (527 selected);
subsequent changes invalidate these as gate evidence. The third run's JUnit is
`.dev-records/verification/20261107-ec82d75-us12-ip2/m1.xml`.
Final `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/20261107-ec82d75-us12-ip2/m1-final.xml`
passed: 527 passed, one existing skip in 224.89 seconds. Collection via
`uv run --locked pytest --collect-only -q -m milestone_1` selected 528 of 630,
with 102 deselected. The final JUnit is retained at the indicated path.
Gate review subsequently added the advisory file sentinel assertion, making
that run historical. The renewed final run used
`uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/20261107-ec82d75-us12-ip2/m1-gate.xml`:
527 passed and one existing skip in 219.54 seconds, with 528/630 selected and
102 deselected. Its JUnit is retained at the indicated path. The focused suite
and shared checks were renewed after the sentinel assertion and passed.
Locked sync and lock check initially
failed because the sandbox could not write the uv cache; approved retries passed
(196 resolved, 193 checked on sync). Lock SHA-256 before checks:
`4b21570fb52b7a4eea94c5d85404e95afefe2d7c44eab014f2122fc9793d847b`.
Final shared checks passed: `uv run --locked ruff check .`,
`uv run --locked ruff format --check .` (263 files),
`uv run --locked mypy src tests` (62 files),
`uv run --locked agentic-ml --version` (0.1.0), and `git diff --check`.
The lock hash after verification matched the hash above. No separate artifact
driver or broader local suite was run. Existing historical M1/M50 obligations
and skips remain open; Linux evidence does not establish other platform support.
The M1 skip is the existing developer-authorized
`test_missing_planning_schema_fails_installed_inventory`, pending diagnosis of
the historical 120-second timeouts; it does not establish that coverage.
