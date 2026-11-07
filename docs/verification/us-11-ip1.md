# US-11 / Implementation Phase 1: Pandas design review evidence

Date: 2026-11-07 UTC. Branch: `US-11-local-data-extraction`.
Baseline `5c035cd`; current work is documentation only.
Technical design/review preparation complete; renewed IP1 gate approval pending.

## Direction, history and source agreement

The developer explicitly requested: “Instead of creating our own proprietary
classes, I'd like to use pandas for all data extraction and the basis for
feature engineering. Rework the design of data extraction to use pandas.”
This authorizes the revised design under US-11-SC-01; it does not authorize IP2
or approve the revised public test boundaries.

Original plan approval and commit `5c035cd` remain historical facts. Initial IP1
contract was never gate-approved. Its [initial evidence](us-11-ip1-initial.md)
and full pre-revision document copies remain preserved in
`.dev-records/verification/20261107-5c035cd-us11-ip1-pandas/identities/before-*`.
Earlier document-check records remain under
`.dev-records/verification/20261107-5c035cd-us11-ip1/`; they verify the earlier
proposal only, not this revision. No runtime evidence has been invalidated,
because no executable extraction work has started.

Refreshed complete [issue #14](https://github.com/jimthompson5802/agentic-ml/issues/14)
and all comment pages: one unique comment 6699585176 matches reported count;
final updated_at stays `2026-11-07T00:28:37Z`, comments 1, milestone null.
The body/comment match the [source snapshot](../plans/sources/us-11-issue-14.md)
and assign AC-01–05 to M1. Native pandas/project functions satisfy those same
outcomes. No criterion, milestone, issue body, ADR or acceptance status changed.
No issue publication is required to resolve an implementation-design conflict:
the issue already permits ordinary project extraction functions. No GitHub write
was performed or authorized by this revision.

## Revised design and impact

[Current contract](../extraction.md) defines one small recording/publication helper
using native pandas data, project functions, dictionaries and a tuple result.
Pandas owns all readers, projections, filtering and merge behavior. Source
inspection is native DataFrame inspection and ordinary report metadata. The
separate inspect_source API and all proposed proprietary classes are withdrawn.

| Initial proposal | Revised boundary |
|---|---|
| Source/request/result/schema classes | Paths, mappings, DataFrames, dictionary reports and a tuple result |
| Predicate/Join/DeclarativeExtraction interpreter | Project pandas code consumes explicit settings and calls native pandas |
| CustomExtraction/ExtractionContext | Ordinary callable receives a dictionary of DataFrames and settings |
| Restricted callback registration shape | Any synchronous callable matching the simple function signature, with declared code references |
| ExtractionError with proprietary codes | Standard/native exceptions retain their types/causes and gain stage/source notes |
| Toolkit-specific null and positional join rules | Native pandas semantics; explicit dtype/sort/validate choices in project code |
| Independent custom schema inspection API | DataFrame.dtypes/shape/info and source schema dictionaries in provenance |

Keep output identity, source-byte hashes, source metadata, actual reader and
project settings, declared code paths/hashes, time, output checks and safe bundle
publication. Fresh-destination rerun behavior and DVC ownership remain as before.
All source/failure/artifact criteria and milestone/shared verification obligations
remain. Removing tests of withdrawn types/operators does not remove corresponding
observable data/error/metadata coverage. Those tests are replaced below.

The active overview, data/features, interfaces and blueprint now explicitly name
DataFrames/project pandas functions as the foundation. Future feature functions
consume/return DataFrames; stateful preprocessing still uses native training-only
fitted pipelines. No feature, split, training or reproduction implementation was
added to US-11. This is a clarified data boundary for later owning plans.

Direct pandas>=3.1,<3.2, pyarrow>=25,<26 and dev-only pandas-stubs>=3,<4
recommendations remain; concrete resolver and strict typing checks still belong
to IP2. Both independent runtime inventory probes must be updated in IP2.
No dependency edits, installation, suppressions or test exclusions occurred.

Primary references support use of native APIs:
[pandas read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html),
[pandas DataFrame.merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)
and [FunctionTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html).
Exact first supported library behavior requires executable verification later.

## Public test boundaries and case matrix

**Status:** Revised boundary proposal, awaiting explicit IP1 confirmation.
Tests enter through installed `extract_data` plus ordinary project pandas
functions and inspect DataFrames, standard exceptions, files and dictionary
reports. Expected rows/hashes are defined independently. Do not test pandas
internals, rebuild its algorithms, mock private toolkit collaborators or create
a new proprietary settings schema to replace the withdrawn classes.

Base fixture people `(id,age,group)` = `(1,20,A)`, `(2,35,B)`, `(3,40,A)`,
`(4,null,C)`, groups `(group,label)` = `(A,alpha),(B,beta)`. CSV/Parquet variants
use explicit native reader options to make required types/null handling clear.
Output order is explicit in each project function, for example sort_values(id).

| Proposed test | Independent observable expectation | Criteria | Task owner |
|---|---|---|---|
| `test_pandas_source_schema_and_identity[csv,parquet]` | DataFrame/report exposes four source rows, ordered id/age/group, parsed dtype strings, byte count and independently computed hash of actual parsed source bytes | AC-01/02/04 | IP2-T2 |
| `test_native_reader_options_and_paths` | Native sep/encoding/dtype kwargs applied and recorded, unrelated cwd resolves explicit root, local external absolute input works; invalid paths/options/non-DataFrame reader result fail honestly | AC-01/02/03/05 | IP2-T2 |
| `test_missing_and_malformed_sources` | Missing/unreadable/zero-byte CSV/corrupt Parquet fail with original applicable exception and source note; no completed output | AC-01/02/05 | IP2-T2 |
| `test_pandas_selection_and_configured_filter` | Project .loc returns id/group `(1,A),(2,B),(3,A),(4,C)`; threshold setting 30 returns ids `[2,3]`; changing setting to 40 returns `[3]`; settings exactly recorded | AC-01/03/04 | IP2-T3 |
| `test_native_filter_boundary_cases` | Project native nullable-age expressions eq35→`[2]`, ne35→`[1,3]`, lt35→`[1]`, le35→`[1,2]`, gt35→`[3]`, ge35→`[2,3]`, isin([20,40])→`[1,3]`, isin([])→`[]`, isna→`[4]`, notna→`[1,2,3]`; no toolkit operator vocabulary | AC-01/03 | IP2-T3 |
| `test_pandas_configured_merge[inner,left,right,outer]` | Separate left keys b,a,x and right a,b,y, native how from settings and explicit key sort: inner `[a,b]`, left `[a,b,x]`, right `[a,b,y]`, outer `[a,b,x,y]` with literal matched/unmatched cell values | AC-01/03 | IP2-T3 |
| `test_native_merge_null_duplicate_and_validate` | Native null keys match; duplicate a rows expand to `(l1,r1),(l1,r2),(l2,r1),(l2,r2)` with explicit stable project sort; one_to_one/one_to_many/many_to_one reject that fixture while many_to_many accepts; native MergeError retained | AC-01/03/05 | IP2-T3 |
| `test_project_configuration_and_pandas_failures` | Missing settings/columns, native dtype/cardinality/suffix conflicts and invalid native kwargs surface native/project exceptions with notes; no alternative toolkit validation language | AC-03/05 | IP2-T3 |
| `test_dataframe_handoff_and_empty_output[csv,parquet]` | Return value is pandas.DataFrame with original in-memory index/dtypes; written file omits index, row/column structure verified and zero-row output schema visible; report is a standard dictionary | AC-01/02/05 | IP2-T3/T4 |
| `test_pandas_output_provenance` | Literal `(2,beta),(3,alpha)` final rows; independent source/code/output hashes, native reader/project settings, root/cwd, UTC bracketing and nonnegative elapsed; JSON matches report; no invented DVC/quality approval | AC-02/03/04 | IP2-T4 |
| `test_publication_conflicts_and_changed_source` | Empty/nonempty existing destination preserved; overlap/symlink/missing parent rejected; callback that changes source or creates destination causes honest failure before publication | AC-04/05 | IP2-T4 |
| `test_actual_write_failure` | Isolated POSIX subprocess imports first, then sets RLIMIT_FSIZE=0 and ignores SIGXFSZ: real write raises standard/native exception with context, destination absent and original cause/notes retained | AC-05 | IP2-T4 |
| `test_project_function_and_exception_identity` | Ordinary local/module-level/wrapped synchronous functions work with declared code paths; settings copied; RuntimeError/KeyError/native merge error retain types/causes and notes; non-DataFrame/async returns fail | AC-01/03/04/05 | IP2-T3, IP3-T1 |
| `test_separate_project_pandas_customization` | Installed project function changes a configured pandas feature/selection without toolkit edits; DataFrame handoff and declared code/settings identities match actual output | AC-01/03/04/05 | IP3-T1 |
| `test_extraction_from_both_artifact_paths` | Direct/rebuilt-wheel isolated installs run native CSV/Parquet/filter/merge/project function and failure cases from unrelated cwd; imports/runtime dependency origins valid, no developer packages or source imports | AC-01–05 | IP3-T2 |

The native-expression cases demonstrate the installed helper/project boundary;
they do not certify all pandas behavior. Fixture kwargs make nullable semantics
explicit; the toolkit must not enforce its prior custom null rules. Unknown
private enum/operator validation is withdrawn because no such interface exists.
Equivalent invalid-native/project settings and missing-schema failures remain.

File-size-limit fault injection is the same proposed public OS boundary as
initial IP1. Establish platform support before using it; if unavailable, resolve
an equivalent public write-failure boundary rather than skipping coverage.
No runtime quota product guarantee. All checks remain planned, not executed.

Uncovered guarantees remain with their owners: quality/splits, native DVC
execution/restore/cache, training-only fitted state, complete custom-code closure,
notebooks and assistant use. DataFrame feature handoff does not accept those
stories. No untested platform/library support claim.

## Task/evidence renewal and checks

IP1-T1–T3 were reopened for this revision and completed with the new contract,
active-design edits and renewed case matrix. Original completed documentation
results remain historical. Gate/public-boundary approval remains pending renewed
review; no later task has started.

Proposed product modules narrow to `extraction/__init__.py`, `sources.py`,
`execution.py`, `provenance.py` as needed; no models.py/operations.py or new
schema resources. IP2 implements reader/recording integration and project
function behavior through small vertical TDD slices. IP3 verifies independently
installed project functions and both artifact paths; no second callback adapter.

Documentation checks cover local links/anchors, Python snippet syntax without
execution, all 12 stable task IDs, five criterion mappings, three pending gates,
no proprietary public classes or operations catalogue in the active contract,
and unchanged product/tests/dependencies/resources. `git diff --check` passed.
Actual counts: 73 local links/anchors, three Python snippets parsed without
execution, 12 stable tasks (three IP1 technical completions, nine later tasks not
started) and three pending gates. Only the nine authorized documentation files
changed. Pre-revision evidence copies and the lock hash were checked unchanged.
Exact script/output, document hashes, unchanged lock identity and command results:
`.dev-records/verification/20261107-5c035cd-us11-ip1-pandas/`.

This phase changes design documents only. TDD/runtime tests, locked installation,
M1/shared executable checks are inapplicable under the documentation-phase policy.
Their required commands remain unchanged for IP2/IP3: M1 at executable gates,
M1–6 at story acceptance and both installed artifact paths before final approval.
Explicit developer command remains required for broader suites/standalone drivers.
Existing historical M1/M50 obligations and known skips/failures remain open.

## Gate handoff

Requested pandas design rework is complete for review. No dependency/runtime
feasibility is claimed from documentation checks. No commit, push, issue edit,
IP2 execution or feature implementation was performed in this revision.
The [plan's IP1 gate](../plans/milestone-1-us-11.md) still requires explicit
approval of revised contract/test boundaries before IP2. User direction already
authorizes the design change itself; it is not being requested again.
