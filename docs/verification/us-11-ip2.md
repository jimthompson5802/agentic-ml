# US-11 / Implementation Phase 2: Pandas extraction

Date: 2026-11-07 UTC. Branch `US-11-local-data-extraction`.
Execution baseline `0543d26`; implementation is currently uncommitted.
**Status:** IP2-T1–T5 complete; developer IP2 gate approved 2026-11-07 UTC.

## Authorization and implemented boundary

Developer “i approve ip1; commit the changes; i authorize ip2” approved the revised
pandas contract/public test boundaries and authorized this phase. Committed the
approved design as `0543d26` (`docs(us-11): approve pandas extraction contract`).
No push, IP3 or whole-story acceptance is authorized.

Refreshed issue #14 body/all comments: one unique comment matches reported count;
final metadata unchanged at `2026-11-07T00:28:37Z`. Complete source discussion is
preserved in the [snapshot](../plans/sources/us-11-issue-14.md). All five criteria
remain M1 and agree with the developer-directed pandas design.

Implemented `agentic_ml.extraction.extract_data` with the approved signature.
It takes a normal project function, native DataFrames/settings and declared paths,
and returns a DataFrame/plain report dictionary. No proprietary classes,
predicate/join interpreter, custom exception or new CLI was introduced.

- Native pandas CSV/Parquet readers consume owned bytes identified by SHA-256;
  source schema/row count and actual reader options are recorded before callbacks.
- Project pandas functions perform selections, filters and merges. Native null,
  duplicate/cardinality and dtype semantics remain native pandas behavior.
- Preflight checks root/paths, JSON-compatible settings, project code declarations
  and fresh destination before invoking project code. Settings are deeply copied.
- Native output is written without an index into owned staging, independently
  re-read/checked/hashed, and published with JSON provenance as one directory.
- Input/code fingerprints are rechecked before publication. Standard/native
  exceptions retain their types and gain source/stage/root/cwd/staging notes.
  Owned staging is cleaned on handled failure; cleanup errors preserve the
  primary error and identify available evidence. No validation certificate/DVC ID.

Implementation modules: `extraction/__init__.py`, `sources.py`, `provenance.py`.
Public tests: `tests/integration/test_extraction.py`. No model/operation classes
or additional package resources. The public docstring and guide describe actual
component behavior; independent installed extraction demonstrations remain IP3.

## Dependencies and verification identity

Declared direct runtime requirements pandas>=3.1,<3.2 and pyarrow>=25,<26.
Added dev-only pandas-stubs>=3,<4, resolved to 3.1.0.261029. Existing pandas 3.1.0
and pyarrow 25.0.1 resolutions are unchanged. Both independent installed-runtime
requirement inventories were updated. Intentional lock diff: 18 inserted lines,
only root declarations plus the pandas-stubs entry; no broad dependency upgrade.

Linux aarch64, Python 3.12.16, uv 0.13.6; toolkit 0.1.0. Other platforms unverified
by this phase. The previously noted generated workspace member did not block
locked sync; it was not modified.

- Original lock: `90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
- Intentional post-resolution/pre-verification lock:
  `4b21570fb52b7a4eea94c5d85404e95afefe2d7c44eab014f2122fc9793d847b`.
- Final lock verification: same intentional post-resolution hash above; no verification mutation.

Raw records: `.dev-records/verification/20261107-0543d26-us11-ip2/`.
Phase JUnit: `m1.xml`; focused red/green output: `logs/01-*` through `logs/26-*`.
Some exploratory tool outputs (07 invalid-input red, 13 timing red, initial mypy
and collection enumeration) were tool-truncated; summaries, original command/error
information and retained output remain, and final JUnit is the complete executed
case inventory. No assertion or diagnostic was weakened to accommodate a failure.

## TDD evidence

Serial commands below are short red–green cycles through the already confirmed
public function, not a replacement for the full four-worker milestone gate.
Command base: `uv run --locked pytest tests/integration/test_extraction.py`;
append the named `::<test>` selector for red and `--tb=short` where recorded.
After each minimal change, rerun the focused module as relevant regressions.

| Slice / red selector | Actual red | Actual green and raw logs |
|---|---|---|
| CSV schema/identity `test_pandas_source_schema_and_identity` | 1 failed: explicit NotImplementedError, not import/setup failure | 1 passed; 01/02 |
| Parquet/native kwargs `test_parquet_native_reader_options` | 1 failed: CSV-only reader could not decode Parquet bytes | 2 passed; 03/04 |
| Root/cwd/path metadata `test_native_reader_options_and_paths` | 1 failed: absent project_root report field | 3 passed; 05/06 |
| Invalid sources/path/code `test_missing_and_invalid_paths` | 8 failed: missing diagnostics or invalid inputs accepted | 11 passed; 07/08 |
| Configured pandas callback `test_pandas_selection_filter_merge` | 2 failed: returned unfiltered source instead of project output | 13 passed; 09/10 |
| Complete output/provenance `test_pandas_output_provenance` | 2 failed: no persisted dataset/report bundle | 15 passed; 11/12 |
| Completion timing same selector | 2 failed: completed_at preceded actual output mtime | 15 passed after timing moved behind writing/re-read/hash; 13/14 |
| Preflight `test_preflight_before_project_code` | 11 failed: invalid configuration invoked project code or was accepted | 26 passed; 15/16 |
| Return boundary `test_invalid_callback_output` | 1 failed, 2 already passed: scalar raised AttributeError rather than required TypeError | 29 passed; 17/18 |
| Input/code mutation and destination conflict `test_changed_inputs_and_publication_conflict` | 3 failed: changed inputs accepted; destination conflict had generic OSError | 32 passed; 19/20 |
| Real write failure `test_actual_write_failure` | 1 failed: original write error retained but staging context absent | 50 passed after diagnostic addition; 22/23 |

Additional native filter/join/empty-output/exception/copy regressions were already
green using the implemented callback delegation (21). Additional null/cardinality,
external-source and native reader failure cases were also green (26). No fake
red was manufactured for pandas behavior already delegated by the earlier slice.
Final focused result: **60 passed in 0.93s**. First implementation verification
passed for each corrective slice; no unresolved repeated product failure/third
attempt exists. One patch application partially applied its first file; inspecting
and finishing the intended timing edit preceded its green verification.

## Static-check corrections and exclusions

Initial strict mypy reported four overload errors in dynamic reader/writer kwargs.
Hypothesis: mypy narrows directly assigned pandas callables to overloaded native
signatures even with a broad local annotation. Correction attempt 1: isolate the
intentional runtime reader keyword boundary behind a typed function taking
Callable[..., object], validate its concrete DataFrame result, and use explicitly
typed native writer calls for fixed options. Original `uv run --locked mypy src
tests` then passed (57 source files), as did all 50 then-existing extraction
regressions (24/25). No Any, fake stub, ignore or suppression was added.

Initial Ruff lint identified same-line statements in new tests. Formatter fixed
those; renewed repository lint passed. Repository formatting then identified the
approved guide's Python snippets; formatting that guide fixed the original check
and the repository formatting check passed (250 files). These were style changes,
with no assertion/threshold/skip change.

Sandbox uv cache writes initially failed read-only. Approved outside-sandbox
retries for synchronization, intentional lock resolution and lock check passed.
No product workaround or workspace-member change was introduced.

## Phase checks and criterion coverage

| Check | Exact command | Actual result |
|---|---|---|
| Locked synchronization | `uv sync --locked --group dev` | Passed after approved cache-access retry; new stub installed |
| Lock consistency | `uv lock --check` | Passed after approved cache-access retry; 196 packages |
| Focused TDD/regressions | `uv run --locked pytest tests/integration/test_extraction.py --tb=short` | 60 passed; serial short-cycle rationale above |
| M1 phase gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/20261107-0543d26-us11-ip2/m1.xml --durations=10` | 431 passed, 1 existing skip in 232.63s; exit 0 |
| M1 collection | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --collect-only -q` | 432/534 collected; 102 deselected |
| Lint | `uv run --locked ruff check .` | Passed |
| Format | `uv run --locked ruff format --check .` | Passed after guide formatting correction |
| Strict types | `uv run --locked mypy src tests` | Passed, 57 source files |
| CLI smoke | `uv run --locked agentic-ml --version` | Passed, stdout 0.1.0 |
| Whitespace | `git diff --check` | Passed; renew after final records |

| Criterion | Direct component evidence | Limit / remaining owner |
|---|---|---|
| US-11-AC-01 | CSV/Parquet frames, configured project selection/filter/merge, all four native joins, nulls/duplicates/cardinality | Separate installed project extraction in IP3-T1/T2 |
| US-11-AC-02 | Actual source/output dtype schemas, row/byte counts, reader options, root/cwd paths | Schema reports are not quality approval |
| US-11-AC-03 | Native reader kwargs and exact project settings recorded; independent expected rows for threshold changes | Arbitrary project code is trusted; no query/permission language |
| US-11-AC-04 | Independent source/code/output SHA-256 assertions, UTC bracketing/output timing, input mutation rejection | Real DVC versions belong to US-13; hidden imports/reads not captured |
| US-11-AC-05 | Missing/corrupt/unreadable inputs, invalid paths/configuration, callback/native failures, existing destinations, actual write failure and no completed partial output | Forced-kill/concurrent hostile-writer guarantees excluded |

No new skip, suppression, check exclusion or timeout increase. Preserve existing
three temporary skips and original M1/M50 obligations. This phase does not run
M1–6 story acceptance, broader local pytest or standalone artifact drivers.

## Deferred checks and gate

IP3-T1/T2 own independently installed project pandas customization and extraction
from direct/rebuilt wheel paths. Existing M1 installed initialization/planning
checks exercise changed dependency inventories but do not establish installed
extraction delivery. IP3-T4 owns final M1–6/criterion reconciliation and remaining
reviewed extension cases. Quality/splits, features/training, DVC integration,
notebooks, assistant use and other-platform evidence retain their owning stories.
No US-11 whole-story acceptance or milestone acceptance is claimed.

Developer “i approve ip2; commit changes; do not start ip3” approved IP2 on
2026-11-07 UTC and authorized a local commit. M1/shared checks passed and final
lock was unchanged. IP3 is explicitly not authorized and remains unstarted;
whole-story acceptance and publication remain pending. This approval-record
update changes documentation only; existing runtime evidence remains applicable.
