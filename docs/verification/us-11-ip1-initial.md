> Historical initial IP1 proposal. Superseded by US-11-SC-01 at the developer’s request to use pandas directly. No API or test-boundary approval was granted. The full original contract and plan are preserved in `.dev-records/verification/20261107-5c035cd-us11-ip1-pandas/identities/before-*`. Links to current design documents below now lead to the revised proposal.

# US-11 / Implementation Phase 1: API contract review evidence

Date: 2026-11-07 UTC. Branch: `US-11-local-data-extraction`.
Baseline: planning commit `5c035cd` (parent `03dd739`).
**Technical status:** Contract investigation/documentation complete; developer
IP1 gate and public-boundary confirmation pending. No executable implementation.

## Authorization and source agreement

Developer “I approve plan; commit changes; and authorize ip1” approved the plan,
authorized its local commit and authorized IP1 only. Planning records committed
as `5c035cd` with Conventional Commit message
`docs(us-11): approve extraction implementation plan`. No push requested.

Refreshed [issue #14](https://github.com/jimthompson5802/agentic-ml/issues/14):
complete body and all paginated comments, one unique comment 6699585176 matching
reported count. Final metadata refresh still reports updated_at
`2026-11-07T00:28:37Z`, comments 1, no assigned GitHub milestone.
Body/comment match the [saved complete snapshot](../plans/sources/us-11-issue-14.md).
Body assigns US-11-AC-01–05 to M1. Active design 0.15 agrees; no issue/spec conflict
or extra archived platform prerequisite was found.

Reviewed active data/features, interfaces, blueprint, storage/execution, layout,
milestone order, acceptance traceability, ADR-007/008 dispositions and repository
verification/dependency/evidence rules. Reusable local extraction fits the package
boundary; future US-39 configuration/runner and US-13 DVC are separate owners.

## Decisions presented for gate approval

The [API contract](../extraction.md) defines all public records, entrypoints,
defaults, operation order, path behavior, provenance and error fields.

| Question | Recommended decision and reason |
|---|---|
| API surface | Two functions, inspect_source and extract_data, with public typed records and ExtractionError. Project script usage needs no new CLI or formal plan IDs. |
| Configured operations | Small typed selections/predicates/ordered joins over native pandas; no eval or connector language. Exact input-position row order is specified. |
| Missing/duplicate join keys | Native pandas missing-to-missing key matches; explicit cardinality can reject duplicate expansion. Independent expected rows verify these choices. |
| Custom project functions | Imported module-level function receives context with copied frames and root/cwd plus copied settings. It can wrap project extraction code; declarations identify sources/code without claiming to capture hidden reads. |
| Declarative plus custom composition | Operation is a union. Custom code can compose arbitrary logic itself; no ambiguous mixed-mode ordering. |
| Existing outputs and DVC reruns | Fresh bundle only; no overwrite. Future DVC declares the entire non-persistent directory output, which it removes before execution. Ordinary reruns choose a new destination. No native DVC test or guarantee claimed here. |
| Provenance versus quality | Completed extraction/output checksum and settings/time report only. No fabricated quality validation or DVC identity. CSV output type loss is visible through separate frame/output schemas. |
| Publication failures | Owned sibling staging, output re-read and report, then whole-directory rename. No completed destination on handled failure; useful error/cleanup diagnostics. Concurrent same-destination writers and hard-kill recovery excluded. |
| Dependencies and typing | Direct pandas>=3.1,<3.2 and pyarrow>=25,<26 align with the existing lock's 3.1.0/25.0.1. pandas-stubs>=3,<4 is dev-only; actual compatibility awaits IP2 resolution/mypy. No install or suppression in IP1. |

The rerun concern identified during plan review has a concrete recommendation
consistent with native output ownership. DVC documents pre-execution output
removal except for persistent outputs; that supports the compatibility reasoning,
not an executed integration result.
[DVC repro](https://doc.dvc.org/command-reference/repro).

The pandas merge documentation supports native null matching/cardinality choices;
the toolkit positional row-order rule is an explicit additional contract to test.
[pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html).
Other primary references and the dependency/typing rationale are in the contract.

## Public test boundaries and case matrix

**Confirmation status:** Proposed for explicit developer confirmation at IP1 gate.
These are planned checks, not executed tests. IP1 does not manufacture a red test
for documentation. Tests enter through installed public functions or copied
external project probes and inspect files/results/errors. Expected values below
are literal; do not calculate them through the API or duplicate its implementation.

Base fixture: people `(id,age,group)` = `(1,20,A)`, `(2,35,B)`, `(3,40,A)`,
`(4,null,C)` in that order. Groups `(group,label)` = `(A,alpha)`, `(B,beta)`.
Create equivalent CSV/Parquet data with controlled flat types. Raw exact CSV
bytes also supply a known input digest, independently recomputed by hashlib.

| Proposed public test / parameters | Independently expected observation | Criteria | Owner |
|---|---|---|---|
| `test_inspect_source_schema_and_identity[csv,parquet]` | Four people rows, ordered id/age/group, integer/nullable numeric/string reader types, actual byte count and independently computed SHA-256; expanded reader settings | AC-01/02/04 | IP2-T2 |
| `test_source_paths_use_project_root` | Same source resolved from unrelated cwd; recorded root/cwd correct, absolute external local source allowed; traversal/symlink/nonregular inputs fail | AC-02/05 | IP2-T2 |
| `test_reader_options_and_invalid_sources` | Semicolon/encoding/dtype settings applied; missing, unreadable, zero-byte/invalid CSV, corrupt Parquet, duplicate headers, unsupported types and invalid reader options yield the specified error; no silent skipped rows | AC-01/02/03/05 | IP2-T2 |
| `test_extract_projects_columns` | id/group projection gives `(1,A),(2,B),(3,A),(4,C)` with exactly requested column order; no index column | AC-01/03 | IP2-T3 |
| `test_extract_filter_cases` | age eq35 → ids `[2]`; ne35 → `[1,3]`; lt35 → `[1]`; le35 → `[1,2]`; gt35 → `[3]`; ge35 → `[2,3]`; in[20,40] → `[1,3]`; in[] → `[]`; is_null → `[4]`; not_null → `[1,2,3]` | AC-01/03 | IP2-T3 |
| `test_filter_conjunction_and_invalid_literals` | age ge30 AND group eqA → `[3]`; unknown column/operator, null comparison, wrong kind and numeric boolean rejected | AC-01/03/05 | IP2-T3 |
| `test_join_modes[inner,left,right,full]` | Separate left `(key,l)=[(b,lb),(a,la),(x,lx)]`, right `(key,r)=[(a,ra),(b,rb),(y,ry)]`: inner `[b,a]`, left `[b,a,x]`, right `[a,b,y]`, full `[b,a,x,y]`, with null unmatched cells and literal l/r values | AC-01/03 | IP2-T3 |
| `test_join_null_duplicate_and_cardinality_cases` | One null key each → one matched pair; left a rows l1/l2 and right a rows r1/r2 → `(l1,r1),(l1,r2),(l2,r1),(l2,r2)`; same fixture one_to_one/one_to_many/many_to_one reject, many_to_many accepts | AC-01/03/05 | IP2-T3 |
| `test_join_order_suffixes_and_projection` | Fixture base filter/join/projection gives `(2,beta),(3,alpha)`; two sequential joins verified with literal rows; key/column/type/suffix collision and duplicate/unused source configuration fail | AC-01/03/05 | IP2-T3 |
| `test_empty_and_serialized_output[csv,parquet]` | Valid zero-row output keeps named columns; independently readable row/column counts, format settings and actual serialized schema; original index excluded | AC-01/02/05 | IP2-T3/T4 |
| `test_provenance_matches_inputs_and_output` | Independent input/output byte digests, full effective settings, root/cwd, UTC start/end bracketing invocation, nonnegative elapsed and matching report/result fields; no DVC ID or quality-approved claim | AC-02/03/04 | IP2-T4 |
| `test_publication_failure_preserves_existing_files` | Existing empty/nonempty destination, overlapping source/output, missing parent and invalid path fail without altering files; force a real rename conflict using a public callback that creates destination; no completed new output | AC-05 | IP2-T4, callback race IP3-T1 |
| `test_output_write_failure_has_no_completed_bundle` | Isolated POSIX subprocess imports API first, then sets RLIMIT_FSIZE=0 and ignores SIGXFSZ before calling extraction: actual output write fails, original cause is chained, destination absent, unowned files untouched | AC-05 | IP2-T4 |
| `test_custom_extraction_and_code_provenance` | Project function uses context frame/settings to return ids `[2,3]`; code path bytes independently hashed, settings and callable name reported; input frames protected by copies | AC-01/03/04 | IP3-T1 |
| `test_custom_extraction_failure_cases` | RuntimeError cause preserved; scalar/generator/async return, lambda/local function and unsupported frame rejected; missing declared source/code fails; callback mutating source triggers changed_source before publication | AC-01/04/05 | IP3-T1 |
| `test_extraction_from_both_artifact_paths` | Same controlled success and missing/corrupt cases in direct/rebuilt wheel installations; imported toolkit under clean environment, installed project function, unrelated cwd, no source checkout imports/dev dependencies | AC-01–05 | IP3-T2 |

The file-size-limit fixture uses a public process/OS boundary in its own subprocess,
without private writer mocks or privileged-user permission assumptions. The
parent writes fixtures before launching it. Import dependencies before installing
the limit and ignore SIGXFSZ so an attempted file write can surface as an error
rather than killing the probe. Establish the platform precondition first; if it
is unavailable, report the blocker and refine the boundary before the affected
test. Do not silently skip required failure coverage. This is fault injection,
not a toolkit quota feature. Python documents the
[file-size limit](https://docs.python.org/3.12/library/resource.html#resource.RLIMIT_FSIZE)
and [signal interface](https://docs.python.org/3.12/library/signal.html#signal.SIGXFSZ).
Cleanup failure remains diagnostic behavior to exercise at a separately reviewed
public fault boundary if the primary case cannot reach it.

Coverage limits: module-level API tests cover behavior in a development install;
both wheel probes separately establish declared runtime dependencies and installed
project use. They do not prove native DVC runs/replay, full dependency closure of
arbitrary custom code, quality/splits, notebook behavior, hostile-writer isolation,
scientific validity, assistant usability, or untested OS/library versions.
Required US-11 coverage cannot be deferred to unrelated story acceptance.

## Planned file ownership and sequencing

IP2: `src/agentic_ml/extraction/{__init__,models,sources,operations,execution,provenance}.py`
(new); `tests/integration/test_extraction.py` (new); intentional dependency/lock
edits; both existing independent runtime inventory declarations. Keep a small
module set; combine private files if it improves cohesion without changing the
approved public boundary. Public JSONValue must not depend on planning internals.

IP3: callback behavior, `tests/installation/check_extraction.py` (new), installed
M1 test in `tests/integration/test_distribution_verification.py`, final guide
examples/README link and criterion evidence. Existing artifact fixture builds
both paths; do not create a new automatic standalone verification obligation.
No new packaged schemas, templates or runtime guidance resources are required.

For each behavior write/run one test, confirm missing/incorrect behavior rather
than setup failure, implement minimally, rerun it and relevant existing tests,
then repeat. Focused serial pytest is only for short TDD cycles. Gate commands
remain full M1 with four workers; story acceptance remains M1–6 plus shared
checks. Both installed artifact tests run as part of M1. Infrastructure/M0/M50,
standalone artifacts and broader local suites need explicit developer commands.
No existing skips, assertions, limits or gate obligations change.

## Verification actually performed

- Complete current issue retrieval and stable refresh as above.
- Manual issue/active-design/API consistency and criterion/task coverage review.
- Automated checks passed: 30 repository-relative links/anchors, three Python
  snippets parsed without execution, 12 task records (three IP1 complete, nine
  later tasks not started), three pending gates and all five criteria mapped.
  Results retained with document identities.
- `git diff --check` passed.
- Verified no changes to product code, tests, dependencies, lockfile, existing
  resource content or active specification files. No runtime tests or package
  installation: this authorized phase changes documentation only. Shared
  executable checks and M1 are inapplicable under the documentation-phase policy.

Raw records:
`.dev-records/verification/20261107-5c035cd-us11-ip1/`.
Includes exact document-check script/output, whitespace command/result, final
document hashes, unchanged lock hash and local identity. This is Linux document
verification; no Linux/macOS/Windows extraction behavior is yet verified.

## Gate handoff

IP1-T1–T3 technical work is complete. Developer approval and public-boundary
confirmation remain pending in the [owning plan](../plans/milestone-1-us-11.md).
No substantive scope change: exact contracts/fixtures/dependency recommendations
are the authorized IP1 deliverables. No US-11 criterion is executable-verified.
IP2 must not begin until the developer approves the contract/test boundaries and
authorizes progression. IP2-T5 owns first executable M1/shared evidence;
IP3-T4 owns final M1–6/installed-path reconciliation. Historical M1/M50 and
future MVP milestone acceptance obligations remain open.
