# Milestone 1 / US-11: Extract local experiment data

## Scope and outcome

- **Milestone:** M1, complete one local classification experiment.
- **Owning issue:** [US-11 #14](https://github.com/jimthompson5802/agentic-ml/issues/14).
  [Complete source snapshot](sources/us-11-issue-14.md), retrieved 2026-11-07 UTC:
  one unique comment, all pages retrieved, stable metadata refresh. GitHub's
  milestone field is unset; the issue body assigns all five criteria to M1.
- **User-visible outcome:** A separate experiment project reads local CSV and
  Parquet, inspects source schemas, executes explicit selection/filter/join rules
  or its own extraction function, and receives output plus traceable extraction
  metadata or an actionable failure.
- **Acceptance criteria covered:** [US-11-AC-01](../specs/user-stories.md#us-11-ac-01),
  [AC-02](../specs/user-stories.md#us-11-ac-02),
  [AC-03](../specs/user-stories.md#us-11-ac-03),
  [AC-04](../specs/user-stories.md#us-11-ac-04),
  [AC-05](../specs/user-stories.md#us-11-ac-05), in full for the reviewed contract.
- **Scope boundaries:** Local files and trusted project Python only. No SQL or
  remote connectors, acquisition, general adapter registry, mandatory experiment
  approval, runner, MLflow lifecycle, data-quality certification, splits, training,
  notebook execution or reproduction service. Extraction completion must not be
  described as US-12 quality validation.
- **Supporting design:** Design 0.15 [reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
  [data contracts](../specs/design/data-and-features.md),
  [interfaces](../specs/design/interfaces-and-configuration.md),
  [blueprint](../specs/design/software-blueprint.md),
  [execution/storage](../specs/design/execution-and-governance.md),
  [layout](../specs/design/repository-layout.md),
  [traceability](../specs/design/acceptance-traceability.md),
  [capability order](../specs/design/milestone-delivery.md) and
  [ADR-007/008 dispositions](../specs/design/architecture-decisions.md).
- **Coordinated execution index:** None. This plan includes no implementation
  tasks owned by other stories. US-39 later consumes this component; its full
  experiment configuration and runner are not prerequisites for a callable
  extraction API.

## Current repository findings

Planning baseline: `03dd739` on `US-11-local-data-extraction`, created from clean
`main`. Existing public modules provide initialization, strict planning, approvals
and metadata/candidate validation. No extraction package or extraction tests
exist. Existing draft 0.1 and strict 1.0 schemas are separate accepted contracts;
neither is silently extended or converted here.

`pyproject.toml` does not directly declare pandas or pyarrow, although both appear
in `uv.lock`. Using them for extraction requires intentional direct dependency
declarations and reviewed lock changes, rather than reliance on MLflow transitives.
The independent runtime inventories are in `tests/packaging/check_installed.py`
and `tests/installation/check_project.py`; dependency changes must update both.
Existing installed-project verification infrastructure includes
`tests/packaging/verify_distributions.py`, `tests/installation/verify_planning.py`,
and M1 tests in `tests/integration/test_distribution_verification.py`.

`agentic_ml.planning.paths.ProjectAccess` has planning-specific errors and a
one-MiB read limit. It is not a general dataset reader. Preserve that contract;
review useful path principles without importing its private helper as a data API.
The stale generated workspace member in `pyproject.toml` is a known unrelated
environment concern. If it blocks locked synchronization, report it and obtain
scope direction rather than deleting it as an incidental extraction change.

The issue body/comment, revised stories and active design agree. Historical
platform contracts are not additional requirements. No product implementation
or passing runtime checks are claimed by this plan.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Current owning issue and scope comment | Complete stable discussion, all criteria assigned to M1 | Detailed planning | Satisfied; source snapshot above, comment 6699585176 |
| Extraction contract and public test boundaries | Developer confirms names, settings, operation semantics, provenance and failure rules | All executable work | Proposed below; IP1 gate pending |
| CSV/Parquet implementation dependencies | Choose compatible pandas/pyarrow constraints, strict typing strategy and intentional lock update | IP2 | IP1-T2 owns review; no installation during planning |
| US-39 basic-path settings | Later adapt reviewed component request into basic workflow without requiring formal plan IDs | Future integration only | Outside this plan; no US-39 tasks or acceptance claim |
| DVC ownership | Extraction provides a real output checksum; US-13 owns native DVC versioning/storage and US-27 stages | DVC integration claims | No DVC prerequisite included; AC-04 uses output checksum, never a fabricated DVC ID |
| Quality and splits | Extraction success means readable completed output, not quality-approved training data | Future US-12 consumption | Separate owner; no dependency on US-12 implementation |

## Plan review

- **Status:** Approved; IP1 authorized, implementation gates remain pending.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “I approve plan; commit changes; and
  authorize ip1”, 2026-11-07 UTC. Authorizes a local planning commit followed by
  IP1 contract/document work; no push or IP2 authorization.
- **Requested plan changes:** None recorded.
- Plan approval authorizes only the agreed plan; implementation requires separate
  direction and each implementation gate remains pending.

## Scope-change history

None. During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for material scope/approach changes. Record change ID/date, request, scope
difference, impacted tasks/criteria/evidence/gates, decision reference and resume
point here. No inferred approval from silence or command permissions.

## Proposed public contract for IP1 review

All names and paths in this section are **proposed**, not existing exports.
Keep reusable helpers in `src/agentic_ml/extraction/` with exports from its
`__init__.py`. Prefer native pandas file/merge behavior behind a small typed API;
do not create a connector framework or expression language based on Python eval.

1. `inspect_source(SourceRequest) -> SourceInspection`: explicit absolute
   `project_root`, local source path and format/reader settings. Return ordered
   column names and logical types, parsed row count, file byte count, resolved
   source path, SHA-256 content identity, and effective reader settings. Relative
   paths resolve from project root regardless of caller cwd; record cwd separately.
   CSV reports parsed/inferred types; Parquet reports the reader's schema. No
   promise that inference is a data-quality check or that inspection is free of
   full-file reads.
2. `extract_data(ExtractionRequest) -> ExtractionResult`: ordered named sources,
   explicit operations, destination and format. Return output path/schema/row count,
   output SHA-256 and a serializable provenance report. No plan/approval ID or
   training validation record is required. Do not add a new CLI family in this
   story; project scripts call Python and can print/save the returned report.
3. Typed declarative operations: source projections, filters and ordered joins,
   with an optional final projection. Propose conjunction of `eq`, `ne`, `lt`,
   `le`, `gt`, `ge`, `in`, `is_null`, `not_null` predicates; reject unknown columns,
   operators and incompatible literals before producing a success record.
   Missing values do not match ordinary comparisons; explicit null predicates
   select them. Propose inner/left/right/full joins with explicit keys, collision
   suffixes and optional declared cardinality checked through native merge.
   Record effective join mode, keys, cardinality and ordered settings. Freeze
   null-key matching, duplicate-key expansion and row ordering at IP1 with
   concrete examples; do not let incidental backend behavior become undocumented
   product guarantees. Empty outputs are extractable with schema/row count;
   required nonempty data is a later quality rule.
4. Optional project callable mode: pass an ordinary imported project function
   with named loaded frames and JSON-compatible settings; receive a dataframe
   for the same serialization/provenance checks. No dynamic import registry.
   Require declared local inputs and a project code reference; record callable
   module/qualified name and declared code path/hash/settings. Do not claim to
   discover arbitrary hidden reads or capture all imported helpers. In IP1,
   settle whether callable and declarative operations are exclusive; the proposed
   minimal contract makes them exclusive and rejects ambiguous mixed requests.
5. Provenance: resolved and supplied source paths, byte hashes, actual reader and
   operation settings, project root/cwd, UTC start/completion times, elapsed time,
   output path/format/schema/row count/hash and relevant library/toolkit versions.
   The request/result/report shapes and timestamp representation are frozen at IP1.
   Hash bytes actually consumed; reject detectable source change during reading.
   Do not claim OS isolation or an immutable source store. Output checksum is
   always real; DVC references remain absent until supplied by native integration.
6. `ExtractionError`: actionable source/operation/output location and stage/code,
   preserving the original cause. Reject missing/unreadable/unsupported/malformed
   inputs, duplicate/ambiguous source names, invalid operations, incompatible
   callback returns, callback failures, output conflicts and write failures.
   Validate destinations before invoking callbacks; never overwrite source or
   existing destination files. Write output/report to a fresh owned destination
   bundle and expose completion only after both are ready; a returned success
   requires independently readable complete output and matching metadata. Failed
   writes leave no new completed bundle; retain useful diagnostics and preserve
   pre-existing files. No hard-kill recovery guarantee or cleanup of arbitrary
   callback side effects. Final publication semantics must be reviewed at IP1.

## US-11 / Implementation Phase 1: Confirm extraction contracts and test boundaries

- **Outcome:** Reviewable, settled component contract and examples before tests.
- **Entry conditions:** Plan review accepted and IP1 separately authorized.
- **Acceptance criteria advanced:** AC-01–05 design only; none verified executable.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP1-T1 | Not started | Refresh #14 and all comments; verify active design/source agreement. Refine the proposed public contract in this plan and proposed `docs/extraction.md`. | Authorization | Exact signatures, reader options/defaults, path policy, join/filter/null/order rules, custom function contract and publication/failure semantics documented with examples; unresolved items block dependent tasks. | AC-01–05 |
| US-11-IP1-T2 | Not started | Review pandas/pyarrow runtime requirements, typing and packaging impact in `pyproject.toml`, `uv.lock` and both independent inventory probes. Record chosen constraints and any necessary reference consultation. | T1 | Dependency/typing proposal and precise touched-file list; no dependency installation or Python implementation in this phase. No blanket suppressions. | AC-01/02/05 |
| US-11-IP1-T3 | Not started | Freeze fixtures and public test boundaries below; refine IP2/IP3 tasks and proposed test selectors against the settled API. | T1, T2 | Developer can approve exact observable tests and coverage limits; document/link/whitespace checks pass and IP1 evidence is recorded in this plan. | AC-01–05 |

### Verification and review evidence

Inspect issue/spec alignment, local links, task/criterion coverage and
`git diff --check`. No executable changes: TDD, milestone tests and shared
executable checks are inapplicable to this documentation-only phase.
Actual results/evidence: Pending implementation-phase execution.

**Public boundaries proposed for confirmation:** public extraction Python API
and persisted outputs/reports; separate experiment project invoking a normally
installed package from an unrelated cwd; project function imported from its own
installed project code. Assert independent row/schema/hash expectations, not
private helper calls. No internal collaborator mocks. A controlled public callback
may raise or modify a declared source to exercise failure behavior. Filesystem
publication failure uses a real conflicting/unwritable destination where reliable;
review any necessary fault boundary before using injection.

**Controlled fixture:** `people.csv`: `(id, age, group)` rows `(1,20,A)`,
`(2,35,B)`, `(3,40,A)`, `(4,null,C)`. `groups.parquet`: `(group,label)` rows
`(A,alpha)`, `(B,beta)`. Filter `age >= 30`, left join on `group`, select
`id,label`: expected `(2,beta)`, `(3,alpha)` in the reviewed ordering. CSV and
Parquet variants must produce equivalent logical rows; compare types according
to the reviewed schema policy. Create separate fixtures for every join mode,
unmatched/null/duplicate keys, cardinality rejection, suffix collisions, empty
results and malformed input. Expected rows are literal independently specified
values, never computed by calling the operation under test. File hashes use an
independent standard-library digest over actual input/output bytes; do not demand
byte equality between separate Parquet serializations. No statistical tolerance
is needed for these integer/string outcomes.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; API, dependency approach, all operation
  edge semantics, fixture expectations and public test boundaries explicitly confirmed.
- **Evidence presented:** Pending; contract diff and document checks.
- **Remaining limitations or blocked work:** No runtime behavior yet.
- **Developer decision / reference / date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP2 only after explicit IP1 gate approval.

## US-11 / Implementation Phase 2: Implement local extraction and provenance

- **Outcome:** Public inspection and declarative extraction complete or fail honestly.
- **Entry conditions:** IP1 approved, including test boundaries and dependency scope.
- **Acceptance criteria advanced:** AC-01 built-in portion, AC-02–05.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP2-T1 | Not started | Add reviewed direct requirements/dev typing support in `pyproject.toml`, intentionally update `uv.lock`; update independent direct requirement inventories in both probes. Add proposed public models/errors/exports under `src/agentic_ml/extraction/`. | IP1 gate | Locked environment and both inventory declarations agree; typed interface skeleton enables first meaningful red test without unrelated import/setup failure. | AC-01/02/05 |
| US-11-IP2-T2 | Not started | In proposed `tests/integration/test_extraction.py`, add one CSV inspection/identity test; implement inspection under proposed `extraction/sources.py`. Repeat separately for Parquet and missing/malformed/schema/path cases. | T1 | Each behavior has observed red then green; public results match literal schemas/rows and independent hashes; unrelated cwd resolves root correctly. | AC-01/02/05 |
| US-11-IP2-T3 | Not started | Add vertical tests and implementation for no-op read/output, projections, each filter, then joins under proposed `extraction/operations.py` and `extraction/execution.py`. | T2 | Reviewed operations and edge cases produce independently expected rows; ambiguous/invalid configuration fails before publication. Each added behavior has its own red–green cycle. | AC-01/03/05 |
| US-11-IP2-T4 | Not started | Add vertical tests and implementation for effective settings, timestamps, source/output identities and complete destination publication under proposed `extraction/provenance.py`; test malformed/changed source, destination conflict and write failure. | T3 | Persisted metadata matches actual output, timestamps bracket execution, old files remain intact and failure never returns a completed dataset/report. | AC-02/03/04/05 |
| US-11-IP2-T5 | Not started | Run M1 and shared checks below; record red/green commands, results, selected counts, platform and lock identities in proposed `docs/verification/us-11-ip2.md`; update plan/checkpoint. | T1–T4 | Required verification passes; limitations and exclusions explicitly assigned to IP3-T4. | AC-01–05 built-in scope |

### Verification and review evidence

Public boundaries: reuse IP1-confirmed API/output boundaries. During short serial
TDD cycles use `uv run --locked pytest tests/integration/test_extraction.py::<case>`;
record why serial execution is appropriate. Cases are proposed until IP1 freezes
their names. Declare direct M1 requirements with `pytest.mark.milestone_1`.
Focused cycles do not replace the gate command.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Native data operations and failures | One behavior-focused red–green test at a time, using the confirmed API/fixture | Independent rows, metadata, diagnostics and no incomplete success | Pending |
| Current milestone gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | All selected M1 checks pass; counts and existing skips reported | Pending |
| Shared development checks | `uv sync --locked --group dev`; `uv lock --check`; `uv run --locked ruff check .`; `uv run --locked ruff format --check .`; `uv run --locked mypy src tests`; `uv run --locked agentic-ml --version`; `git diff --check` | Pass; capture SHA-256 of `uv.lock` before/after verification; intentional dependency update distinguished from check mutation | Pending |

Impact: new extraction modules/dependencies, input paths, operation configuration,
output serialization/provenance and failure semantics. M1 retains accepted
initialization/planning/approval/validation regressions. Excluded M2–6 coverage,
custom callable checks, both installed artifact paths and final criterion
reconciliation are owned by IP3-T1–T4. Infrastructure/M0/M50 suites and standalone
artifact drivers are not automatically run; broader commands need explicit
developer direction. No exemption for a required slow M1 test.

### Developer approval gate

- **Approval criteria:** T1–T5 complete; red/green and M1/shared evidence passes.
- **Evidence presented:** Pending; `docs/verification/us-11-ip2.md` when created.
- **Remaining limitations:** Project callable and installed artifact evidence pending IP3.
- **Developer decision / reference / date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP3 only after explicit IP2 gate approval.

## US-11 / Implementation Phase 3: Verify project extraction functions and installed delivery

- **Outcome:** All criteria verified through installed public interfaces; usage documented.
- **Entry conditions:** IP2 gate approved; confirmed IP1 callable/installed boundaries.
- **Acceptance criteria advanced:** AC-01–05 complete subject to developer acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP3-T1 | Not started | Add one callback behavior test then minimal implementation in `extraction/execution.py`; repeat for settings/code provenance, invalid return, raised exception and missing declared input. | IP2 gate | Ordinary project function produces literal expected rows; failures preserve causes and publish no completed output; undeclared-read capture is not claimed. | AC-01/03/04/05 |
| US-11-IP3-T2 | Not started | Add proposed `tests/installation/check_extraction.py` and an M1 installed test in `tests/integration/test_distribution_verification.py`, reusing its artifact fixture and distribution driver; extend probe inventory/resource checks only as needed. | T1 | Normally install direct wheel and wheel rebuilt from sdist into separate clean environments; copied project probe imports only installed API/project code, checks unrelated cwd, CSV/Parquet/filter/join/custom output, provenance and missing/corrupt-input failure. Assert imports are outside source checkout and runtime dependencies suffice. Observe red/green for new behavior. | AC-01–05 |
| US-11-IP3-T3 | Not started | Finish proposed `docs/extraction.md`, link it from `README.md`; include explicit root/cwd, settings, metadata/failure example and project callable use. Verify newly shipped resources through installed API if any are added by approved contract. | T2 | Commands/API examples match verified behavior; extraction success distinguished from quality validation; checksum/DVC ownership and trusted-code limits stated. No unrelated runtime resource rewrite. | AC-01–05 |
| US-11-IP3-T4 | Not started | Final verification and criterion/deferred-check reconciliation in proposed `docs/verification/us-11-ip3.md`; update this plan and `CHECKPOINTS.md`. | T1–T3 | Final M1 gate, M1–6 acceptance and shared checks pass against final executable changes; both wheel paths and all criterion evidence recorded before final gate. | AC-01–05 |

### Verification and review evidence

- **Selected tests and impact rationale:** All M1 tests at gate, including proposed
  installed extraction test; M1–6 at story acceptance. New installed callback
  checks cover package/project separation and normal dependencies rather than
  editing a toolkit checkout. Preserve existing scopes, xdist groups and timeouts;
  give the new expensive test a separately justified timeout if required.
- **Public boundaries and limits:** IP1 confirmation required. Use actual files,
  normal installed dependencies and import-location assertions. No private-helper
  assertions. These checks do not prove notebook behavior, DVC restoration,
  quality/split correctness, hostile code isolation or assistant usability.
- **Deferred checks:** IP3-T4 owns all IP2 story deferrals. Cross-story integration
  and platform/manual milestone checks retain owners below; no required US-11
  criterion may be deferred while claiming full story acceptance.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Callback success/failure and both artifact paths | Focused reviewed TDD selectors; then installed test included in M1 | Correct external-project outputs, dependency/import origins and honest failures | Pending |
| Final phase gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass, counts/skip limitations recorded | Pending |
| Story acceptance | `uv run --locked pytest -n 4 --dist=loadgroup` | M1–6 pass against final implementation; all deferrals reconciled | Pending |
| Shared development checks | All exact shared commands from IP2 table | Pass with intentional lock changes reviewed and verification immutability recorded | Pending |
| Documentation | Local path/anchor and API/example review; `git diff --check` | Links/examples match tested installed behavior | Pending |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; all five criteria have passing evidence,
  both artifact paths verified, no unresolved required behavior or concealed failures.
- **Evidence presented:** Pending; `docs/verification/us-11-ip3.md` when created.
- **Remaining limitations or blocked work:** Pending actual verification; external
  quality/DVC/runner/assistant integration and untested platforms identified separately.
- **Developer decision / reference / date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Stop for final gate; whole-story acceptance must be
  explicit, whether given with this gate or separately. No automatic publication.

## Final verification requirements

- **Owning final phase/task:** US-11-IP3-T4, before final gate presentation.
- **Final implementation identity:** Record commit, dirty-tree diff identity,
  lock hash, Python/OS/tool/library versions and wheel/sdist/rebuilt-wheel hashes.
- **M1–6 and shared checks:** Commands above; record exact counts/outcomes,
  failure evidence, temporary skips and public boundaries. Renew M1–6 after
  executable changes; documentation-only final changes use document checks.
- **Distribution/installation:** Both normal wheel installations are exercised
  by the new M1 pytest case; standalone drivers and broader selections require
  an explicit developer command. Verify no editable/source-path fallback and
  no undeclared contributor dependency. Preserve existing packaged resources.
- **Deferred-check reconciliation:** Every IP2 deferral resolved or explicitly
  identified as an acceptance blocker. Existing three skips remain documented
  limitations; do not disable checks or imply skipped coverage passed.
- **Evidence storage:** Tracked reports above link raw commands/logs/identities
  under `.dev-records/verification/<timestamp>-<commit>-us11-<unique>/`, following
  [records policy](../development/records.md). Preserve failures and diagnostics.
- **Actual results and limitations:** Pending. No runtime verification performed
  during plan drafting; no platform delivery claim.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-11-AC-01 | IP1-T1/T3; IP2-T1–T3; IP3-T1/T2 | CSV/Parquet rows, configured operations, actual project callable in both installations | Pending |
| US-11-AC-02 | IP1-T1/T3; IP2-T2/T4; IP3-T2 | Ordered schemas, types, row/byte counts and source identities | Pending |
| US-11-AC-03 | IP1-T1/T3; IP2-T3/T4; IP3-T1/T2 | Independently expected operations plus actual effective settings report | Pending |
| US-11-AC-04 | IP1-T1/T3; IP2-T4; IP3-T1/T2 | Input/output independent SHA-256 checks, paths/settings/time/code references; checksum satisfies output identity branch | Pending |
| US-11-AC-05 | IP1-T1/T3; IP2-T2–T4; IP3-T1/T2 | Invalid/missing/malformed inputs, ambiguous operations, callback and publication failure; no incomplete success | Pending |

- **Remaining work:** All implementation tasks; no partial prerequisite delivery claimed.
- **Final verification:** Pending US-11-IP3-T4.
- **Developer acceptance / reference / date:** Pending.

## Milestone acceptance handoff

- **Owner:** `MVP-M1-ACCEPT-VERIFY`, coordinated by future US-39 M1 plan; supplies
  extraction evidence to ASW-02. US-13 owns native DVC data identity/storage,
  US-12 quality/splits, US-27 stage execution, US-39 assistant/basic workflow and
  US-40 M2 replay. This plan does not accept or implement those stories.
- **Deferred checks:** Integrated MLflow/DVC/classification/assistant scenario,
  relevant milestone manual/platform checks. Linux evidence is distinct from
  historical macOS evidence; Windows remains unverified unless actually checked.
- **Required evidence:** Reconcile component results and cross-story dependencies
  against final milestone inputs. Complete-suite `uv run --locked pytest -n 4
  --dist=loadgroup -m ""` and standalone artifacts only on explicit developer
  command; follow [verification policy](../development/verification.md#phase-and-story-verification).
  Preserve independent historical `M1-ACCEPT-VERIFY` and `M50-ACCEPT-VERIFY`
  obligations and evidence; story acceptance does not close them.

## Execution rules

Mark a task Complete only after its required work/checks pass and actual evidence
is linked. Keep partial/failed/unverified tasks incomplete; renew invalidated
evidence. Work in small vertical red–green slices, one behavior at a time, and
review refactoring after green. Record command, expected failure reason, actual
red/green outcome and relevant regressions per slice. Do not batch all tests
before implementation. Preserve public expectations and acceptance criteria.

Stop after every implementation phase, including final, and present changes,
commands/results, criterion evidence, deviations and limitations. Wait for
explicit developer approval before progression and record its reference/date.
Plan review, command permissions and prior unrelated approvals do not approve
these gates. Update checkpoints at gates, blockers and handoff.

Apply the repository's three-attempt limit per unresolved problem: track each
hypothesis, corrective change and verification against the original failure.
After three unsuccessful attempts stop, preserve logs/tree state, report all
attempts and remaining uncertainty, and await developer direction. Never weaken
assertions, suppress failures, change thresholds or add a workaround without
explicit direction. Use scope-change procedure for invalidated approaches or
out-of-scope prerequisites; preserve historical decisions and evidence.
