# Milestone 1 / US-12: Assess data and record reproducible partitions

## Scope and outcome

- **Milestone:** M1, complete one local classification experiment.
- **Owning issue:** [#19](https://github.com/jimthompson5802/agentic-ml/issues/19).
  [Current complete source snapshot](sources/us-12-issue-19-layout-alignment.md)
  retrieved after authorized scope alignment on 2026-11-07 UTC: complete body,
  one unique comment across all pages, matching count and stable final
  `updated_at=2026-11-07T21:38:29Z`. The [original snapshot](sources/us-12-issue-19.md)
  remains historical. This is an issue, not a PR; milestone unset, body assigns M1.
- **User-visible outcome:** A separate installed experiment project obtains
  basic distribution, missingness and classification balance reports; creates
  seeded two-way (train/test) or three-way (train/validation/test) partitions,
  or supplies memberships for either layout, including time/group problems;
  records exact membership
  and source identity; and rejects invalid or overlapping membership.
- **Acceptance criteria covered:**
  [US-12-AC-02](../specs/user-stories.md#us-12-ac-02), basic distributions,
  missingness and classification target balance;
  [US-12-AC-03](../specs/user-stories.md#us-12-ac-03), recorded seeded
  two-way (train/test) and three-way (train/validation/test) layouts for seeded
  generation and explicit supplied partitions, including time/group problems;
  record layout/exact membership and check membership/disjointness. Two-way
  layouts require no validation partition.
- **Developer-requested extension:** Also support train/test without a validation
  partition. US-12-19-SC-02 records the extension and subsequent alignment of
  issue #19, repository AC-03 and supporting design, authorized by developer
  “make the alignment”. Criterion ID and original three-way obligations/history
  are preserved. No executable implementation or gate approval is implied.
- **Scope boundaries:** AC-01/05 remain accepted under
  [issue #15's plan](milestone-1-us-12.md). AC-04 mandatory experiment assessment
  approval remains deferred by MVP-SC-01/02 and comment 6699588996. No automatic
  time/group split algorithms, learned preprocessing, model fitting, runner,
  MLflow logging, native DVC versioning/stage execution, notebook execution,
  assistant walkthrough or protected holdout service is delivered here.
  US-13/27/39/40 own subsequent integration. No strict API/schema/resource changes.
- **Supporting design:** Active 0.15 [reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
  [data and features](../specs/design/data-and-features.md),
  [interfaces](../specs/design/interfaces-and-configuration.md),
  [blueprint](../specs/design/software-blueprint.md),
  [execution and storage](../specs/design/execution-and-governance.md),
  [layout](../specs/design/repository-layout.md),
  [traceability/scenario families](../specs/design/acceptance-traceability.md#required-scenario-families),
  [capability order](../specs/design/milestone-delivery.md#capability-order-and-owning-stories)
  and [ADR-007/008](../specs/design/architecture-decisions.md).
- **Coordinated execution index:** None. No new prerequisite story slices are
  needed; this plan consumes accepted components and owns only #19 tasks.

## Current repository findings

Planning baseline is `bce7ccc`, on existing branch `US-12-assessment-splits`.
The initial working tree contains a developer checkpoint update; preserve it and
refresh its current-position section. No matching #19 plan or assessment/split
module/test was found. The existing `milestone-1-us-12.md` belongs to #15 and
retains its historical task IDs, approvals, evidence and correction attempts.
This plan uses `US-12-19-` task IDs to avoid collisions.

`agentic_ml.extraction.extract_data` returns a native pandas DataFrame and plain
provenance dictionary. `agentic_ml.data_quality` exports `validate_data`,
`run_validated_step` and `DataQualityError`; required failure prevents a supported
dependent callback from running. Reuse these public interfaces; do not import
their private helpers or treat an old quality report as permission for new data.
Extraction completion and assessment statistics do not imply quality passed.

Pandas and pyarrow are direct runtime dependencies. The developer's 2026-11-07
refinement requires scikit-learn's native split capabilities; the earlier
standard-library splitter proposal is superseded. Scikit-learn is not currently
a direct toolkit runtime declaration; IP1 must identify the supported version and
propose its direct dependency/lock/runtime-inventory changes before code.
Do not rely on its presence through a transitive dependency.
Existing `tests/installation/{verify_data_quality,
check_data_quality,data_quality_project}.py`, `tests/verification_support.py` and
`tests/integration/test_distribution_verification.py` supply the pattern for
separate project probes against direct and sdist-rebuilt wheels. Retain normal
install origins, runtime inventories, resources, fixture scopes and xdist groups.
The existing generated workspace membership in `pyproject.toml` is unrelated;
report a blocking sync failure rather than silently repairing it.

Issue body/comment, active stories and design agree on AC ownership. The generic
issue validation paragraph about quality checks means consuming #15's accepted
behavior, not reimplementing it. The traceability index's shared description of
train-only fitting does not move US-15's fitting implementation into #19.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Native extraction | DataFrame plus persisted source/output identity | Installed extraction-to-assessment example | Satisfied: [US-11 plan](milestone-1-us-11.md), IP2-T1–T5/IP3-T1–T4 and approvals/acceptance; [IP3 evidence](../verification/us-11-ip3.md), PR #60 merged. Supplying task records checked during planning; refresh before execution. |
| Required quality checks | Public checks and synchronous blocking helper | Supported preparation example | Satisfied: [#15 plan](milestone-1-us-12.md), IP2-T1–T4/IP3-T1–T4, approved gates and explicit #15 acceptance; [final correction](../verification/us-12-pr61-r1.md), PR #61 merged. |
| Scope synchronization | Active issues agree with design | Dependent implementation | #14/#15 complete bodies and one comment each fetched on 2026-11-07; final counts/timestamps stable, both closed. #19 open, one comment, stable snapshot. No new upstream implementation required. |
| Assessment and partition contract | Concrete signatures, data/report schemas, error semantics and literal expected cases | All executable tests and implementation | Confirmed at Gate 1 by developer “i approve ip1; commit changes”; contract remains unimplemented. |
| Native capability reuse / custom integration discussion | Use scikit-learn splitters and pandas descriptions; discuss toolkit-specific gaps before approval | Dependent contract approval and executable work | SC-03 selects two helpers and project persistence; exact policies/test boundaries confirmed at Gate 1. |
| Two-way/three-way issue alignment | Record additive layout choice in issue #19 and repository AC-03 before product implementation | Dependent executable work | Satisfied by developer “make the alignment”; issue body published and verified on 2026-11-07, current source snapshot linked above. Executable gates remain pending. |
| Source identity and persistence | Return consumed-frame identity/membership; project code owns JSON save/load and old-source checks | IP3/IP4 | Native Parquet identity contract confirmed at Gate 1; stability/type sensitivity need IP3 evidence. No toolkit read/write/filesystem guarantees. |
| Downstream workflow | Future consumers use recorded splits and train-only fitting | End-to-end experiment acceptance | Outside #19; US-15/24/39 own adoption. Callable component needs no future runner. |

The #14 final refresh was `2026-11-07T12:02:00Z`, comment 6699585176;
#15 final refresh was `2026-11-07T17:40:12Z`, comment 6699586004. Existing source
snapshots preserve their scope discussions; refreshed closed state is recorded
here without rewriting historical exports. GitHub GET reads succeeded;
`gh auth status` reported an invalid configured token. Repository identity was
confirmed with `gh repo view`; publication authentication is unverified.

## Plan review

- **Status:** Approved plan — contract-only IP1 complete and Gate 1 approved.
- **Developer decision:** Approved plan, including native library reuse and
  two-way/three-way scope alignment; implementation gates remain pending.
- **Decision reference and date:** Developer “i approve the plan” in this
  conversation, 2026-11-07 UTC.
- **Requested plan changes:** None recorded.
- Approval of this plan does not confirm unresolved IP1 contract details, approve
  an implementation gate or authorize publication. Begin IP1 only when authorized.

Execution authorization: developer “start ip1”, 2026-11-07 UTC, authorizes
contract-only IP1 on clean baseline `c0dcaa1`. All four gates were Pending at entry.
Developer “i approve ip1; commit changes”, 2026-11-07 UTC, subsequently confirms
the revised two-helper contract/policies/test boundaries and approves Gate 1 and
a local commit. Developer “start ip2” authorizes IP2 execution in this conversation
on 2026-11-07 UTC, baseline `37ffe7d` with a clean tree. Gate 2 is now approved by developer “i approve ip2; commit changes”,
2026-11-07 UTC; a local IP2 commit is authorized. Developer “start ip3”,
2026-11-07 UTC, authorizes IP3 on clean baseline `43cd770`. Developer “i approve ip3; commit”, 2026-11-07 UTC,
approves Gate 3 and authorizes a local IP3 commit. Gate 4 is approved by developer “i approve ip4; commit”, 2026-11-08 UTC,
authorizing a local IP4 commit. Issue #19 accepted by developer “i accept issue #19”, 2026-11-08 UTC. Developer “start ip4”, 2026-11-08 UTC, authorizes
IP4 on clean baseline `ffd5322`; installed and final verification is complete.
Historical pending statements in scope records below describe their original
decisions, not the current approval state.
The earlier all-Not-started counts below are historical planning evidence.

Planning validation on 2026-11-07 UTC: `git diff --check` passed; a read-only
Python document check passed 47 local file/directory links and anchors across
this plan and `CHECKPOINTS.md`. Task structure check confirmed 15 unique task
IDs, all Not started, and four developer gates. Manual review mapped both active
criteria to tasks and installed evidence, with executable checks still planned.
The first link-check script incorrectly treated an existing directory link as a
file; correcting that validation assumption produced zero errors without changing
the linked document. No executable verification was run for this planning edit.

## Scope-change history

### US-12-19-SC-01 — Native library reuse, 2026-11-07 UTC

- **Request and reason:** Developer requested design documentation requiring
  scikit-learn wherever it supplies functionality, and discussion of any custom
  assessment/partition support before building it.
- **Scope difference:** Replace proposed custom/standard-library splitting with
  scikit-learn public APIs; reuse pandas assessment operations. Proposed toolkit
  wrappers, membership/source records, supplied-membership checks and report
  adapters are discussion items, not approved deliverables in their current form.
- **Impact:** IP1-T2/T3/T4 must settle minimum library integration and whether new
  public helpers are needed. IP2/IP3 module paths and API shapes remain conditional;
  their behavior tasks and IDs are retained pending discussion/refinement.
  Dependency work now includes a proposed direct scikit-learn declaration, lock
  update and both independent installed runtime inventories. No completed task or
  executable evidence is invalidated; no implementation has begun.
- **Plan and requirement revisions:** AC-02/03 unchanged. Active
  [data design](../specs/design/data-and-features.md#reuse-existing-assessment-and-partition-capabilities),
  overview, interfaces and blueprint updated locally. No issue publication or
  acceptance-criterion changes authorized or performed.
- **Verification and gates:** All four gates pending; M1, final M1–6, shared
  checks and both installed paths retained. IP1 must revise dependent tasks and
  test boundaries before executable work; custom integration discussion is an
  additional prerequisite, not satisfaction of a gate.
- **Decision:** Native-library reuse/documentation revision authorized by the
  developer's request in this conversation. Specific custom integration choices
  remain Proposed — discussion pending.
- **Resume point:** Discuss the concrete gaps below; IP1 authorization and
  contract/boundary review remain required before dependent code.
- **Documentation validation:** Native API behavior checked against official
  scikit-learn/pandas references linked in the data design. Documentation-only;
  no TDD, product tests, dependency installation or executable changes. Local
  link/anchor check passed 93 local links/anchors across six documents; task/gate
  check passed 15 unique Not started tasks and four gates; `git diff --check`
  passed. No executable capability or gate approval is claimed by these checks.

### US-12-19-SC-02 — Two-way and three-way layouts, 2026-11-07 UTC

- **Request and reason:** Developer “update the plan so that two-way and
  three-way splits are supported”; some experiments need train/test only.
- **Scope difference:** Explicitly select train/test or train/validation/test
  for seeded generation and supplied memberships. A two-way result has no
  validation partition or placeholder. Record and validate the selected layout.
- **Impact:** IP1-T1/T3/T4 settle scope alignment, layout selection/configuration
  and test boundaries; IP3-T1–T3 implement both layouts and record validation;
  IP4-T1–T4 verify both installed paths and documentation. Existing task IDs,
  accepted suppliers and all Not started statuses remain unchanged.
- **Plan and requirement revisions:** Three-way AC-03 coverage is retained;
  two-way support is an additive developer requirement. Original issue/criterion
  text is not silently rewritten. Reconcile the active design and synchronize
  issue #19 through separately authorized publication before product code.
- **Verification and gates:** Add separate seeded and supplied oracles for both
  layouts, persisted-layout round-trip and malformed layout/name combinations.
  Keep all four pending gates, M1, final M1–6/shared checks and both wheel paths.
- **Decision:** Plan revision authorized by the quoted request in this
  conversation on 2026-11-07 UTC. No implementation gate or new custom API approved.
- **Resume point:** Draft plan review; issue synchronization and IP1 public
  contract/integration decisions remain prerequisites to executable work.
- **Documentation validation:** `git diff --check` passed; 49 local links/anchors,
  15 unique incomplete tasks and four gates checked. Reviewed both-layout task
  coverage and removal of the obsolete three-only rule. No executable behavior
  changed; TDD/product tests are inapplicable to this plan-only revision.

#### SC-02 alignment publication — 2026-11-07 UTC

Developer “make the alignment” authorizes matching edits to repository AC-03,
supporting design and GitHub issue #19. Updated `docs/specs/user-stories.md`,
`docs/specs/design/data-and-features.md` and the ownership reference in
`docs/data-quality.md`. The issue body now uses the same AC-03 text, adds a dated
scope-history note and covers both layouts in automated validation. Original
scope comment 6699588996 and the pre-alignment source snapshot are preserved;
AC-02 and deferred AC-04 are unchanged. Earlier publication-pending statements
in this scope-change history describe the prior authorization state.

`gh issue edit --repo jimthompson5802/agentic-ml 19 --body-file
/tmp/agentic-ml-issue-19-layout-body.md` succeeded after retrying outside the
network-restricted sandbox. Published body verified against prepared content
(the file adds a final newline); all pages still contain one unique comment.
Final metadata refresh stable at `2026-11-07T21:38:29Z`.
[Complete updated source](sources/us-12-issue-19-layout-alignment.md) records the
body, metadata and full discussion. Local docs remain uncommitted on this branch;
this publishes the issue alignment, not repository commits or a PR. No executable
work, contract confirmation, phase approval or story acceptance is authorized.

Alignment checks passed: identical local/published AC-03 text; one preserved
comment; 189 local links/anchors across nine affected documents; 15 unique
Not started tasks and four gates; `git diff --check`. This is documentation and
issue-scope work only, so TDD/product tests were not run. No new behavior or
platform support is claimed.

During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for further changes to requirements, approach or approved boundaries. Preserve
supplier approvals/evidence. New upstream work requires a scope decision and,
if needed, separate owning plans and a coordinated execution index.

### US-12-19-SC-03 — Retain two helpers; project-owned persistence, 2026-11-07 UTC

- **Request and reason:** Developer “I only want to keep 1 and 2” selects
  `assess_data` and `create_partitions`; subsequent “make the update” authorizes
  revising the plan, contract, design references, evidence and checkpoint.
- **Scope difference:** Remove proposed `write_partition_record` and
  `read_partition_record`. Project code owns report/record JSON save/load,
  saved-document validation and optional old/current source identity comparison.
  Retain native assessment/splitting, supplied membership validation, source
  identity and JSON-compatible layout/exact membership records. Helpers and
  persistence are optional for simply running an experiment.
- **Impact:** IP1-T2/T3 retain the selected adapters but exact policies/boundaries
  remain unconfirmed. IP3-T3 now verifies project-owned JSON round-trip and
  reconstruction through `create_partitions` supplied mode. IP4 repeats that
  path on both wheels. Reconstruction produces a new supplied record; it does
  not validate the entire old record or automatically reject changed content
  under still-valid IDs. No task IDs or completed supplier evidence are removed.
- **Verification revision:** Remove toolkit saved-file parser/version-restore
  and filesystem conflict/path/symlink/partial-publication test obligations.
  Retain JSON-compatible reports/records, layout/key mismatch and membership
  failures, consumed-frame identity sensitivity, project JSON round-trip,
  both installed matrices, M1 at executable gates, M1–6 at acceptance and all
  shared checks. This explicitly narrows proposed API verification, not AC-02/03.
  No executable tests exist to disable; initial document evidence remains historical.
- **Plan and requirement revisions:** Current approach, boundaries, IP3-T3,
  IP4-T2 and evidence below reflect the change. The contract, active data/interface
  design and blueprint reflect the selected surface. GitHub #19, authoritative
  criteria and immutable source snapshots need no change: none prescribes
  dedicated persistence functions; saved-layout round-trip remains covered.
- **Decision:** Approved scope direction/document revision by the quoted user
  instructions, 2026-11-07 UTC. Exact policies, test boundaries, Gate 1 and
  later implementation authorization remain Pending.
- **Resume point:** Finish IP1 contract-policy/test-boundary review. T1 stays
  Complete; T2–T4 remain In progress. All four gates stay Pending.
- **Documentation verification:** See the renewed checks in
  [IP1 evidence](../verification/us-12-19-ip1.md#two-helper-scope-revision).

## Proposed technical approach and public boundaries

**IP1 approved contract:** [concrete contract and matrix](../data-assessment-and-splits.md),
[evidence](../verification/us-12-19-ip1.md). SC-03 selects two helpers and
project-owned persistence; exact signatures, fields, split composition, identity
and validation policies confirmed at Gate 1 on 2026-11-07 UTC. These
policies are not all independently required by AC-03.

Use native pandas frames and plain dictionaries, with no new dataset wrapper,
operation language or approval service. Proposed modules are
`agentic_ml.data_assessment` and `agentic_ml.splitting`; proposed guide is
`docs/data-assessment-and-splits.md`. IP1 selects exact names/signatures and
refines affected tasks before executable work. Proposed operations:

**Refinement constraint (US-12-19-SC-01):** The operations below describe the
earlier draft and required observable outcomes; their custom signatures, modules,
record schema and extra policies are not selected architecture. First map the
outcomes to native pandas and scikit-learn public calls. Prefer direct use; retain
a proposed toolkit helper only after discussing its specific gap with the
developer. Use native splitting/rounding/stratification/error semantics rather
than writing substitutes. Support one native split for two-way layout and a
documented composition of native splits for three-way layout; decide effective
random states for each call. IP1 must also revisit the proposed stable-ID domain,
complete-coverage/nonempty policies, canonical frame hashing and persistence
surface instead of treating them as acceptance-criterion requirements.

Selected: two native adapters, with project-owned persistence. Remaining
discussion items: report/scalar schema, split settings, minimal recorded
membership/source identity and supplied-membership policies. These refine the
[design gap register](../specs/design/data-and-features.md#proposed-toolkit-integration-requiring-discussion).
No custom statistical or splitting algorithm is currently justified.

1. `assess_data(frame, *, target)` returns a JSON-compatible descriptive report.
   Include row count, schema, per-column missing counts/rates, numeric summaries,
   categorical frequencies and target counts/proportions with explicit missing
   target handling. No mutation, learned imputation, pass/fail quality label or
   implicit statistical certification. Define finite/nonfinite, nullable,
   all-missing, empty, categorical, datetime and unsupported object semantics.
2. `create_partitions(frame, *, row_id, target, ...)` accepts either explicit
   seed/fractions or a supplied mapping of row IDs, with an explicit two-way or
   three-way layout selection whose exact parameter shape is settled in IP1. Return
   independent native partition frames plus a serializable membership record.
   Use an explicit unique, nonmissing stable row-ID column, not the pandas index.
   Proposed initial ID domain is homogeneous strings or integers excluding booleans;
   IP1 must decide supported types, ordering and JSON round-trip rules. Require
   exactly `train` and `test` for two-way layout, or `train`, `validation` and
   `test` for three-way layout. Do not create an empty validation placeholder.
   Reject partition names/settings inconsistent with the selected layout,
   including validation fractions supplied for two-way generation. The proposed
   nonempty and complete-coverage policies apply to the selected partitions;
   their exact rules remain subject to IP1 discussion. Reject unknown, duplicate,
   missing or overlapping row IDs as reviewed. Preserve feature/target alignment
   and caller inputs.
3. Record schema version, selected layout, source content identity, row-ID/target declarations,
   ordered membership/counts, effective seed/fractions/algorithm/version or
   supplied protocol/settings, and relevant toolkit/library versions. Seeded
   behavior must specify input order, rounding/remainder allocation and minimum
   size errors. No implicit stratification guarantee. Supplied time/group fixtures
   preserve exact project membership and recorded protocol; explicitly distinguish
   membership validation from certifying scientific suitability or inferring
   group/time constraints.
   Project records persist only the selected partition names; supplied mode
   validates layout against actual membership keys and rejects inconsistencies. Do not infer a
   third partition, manufacture validation membership or silently reinterpret
   a saved layout. Two-way support prepares train/test data; it does not authorize
   downstream tuning/selection on final-test rows or add cross-validation execution
   to this issue's scope.
4. Project code owns JSON save/load of reports and membership records, using
   explicit paths and unchanged caller cwd. No toolkit read/write functions,
   saved-file parser or filesystem guarantees remain under SC-03. A project
   selects saved layout/ID/target/membership/protocol fields and passes them to
   `create_partitions` supplied mode for current-frame membership validation and
   reconstruction. It retains the original record for provenance and handles
   saved-document/source checks itself. The helper returns actual consumed-frame
   identity with reviewed dtype/order sensitivity; same IDs with changed values
   produce new identity rather than an automatic restoration error. No private
   extraction seam, DVC identity fabrication or workflow store is introduced.

| Public boundary | Independently defined observations | Coverage limits / confirmation |
|---|---|---|
| Assessment function | Literal counts, summaries and rates; explicit JSON values and errors; input unchanged | Proposed; IP1 Gate 1 must confirm precise matrix before tests. No quality-rule or model acceptance claim. |
| Partition creation | Both two-way and three-way layouts, exact names/membership, complete/disjoint sets, target alignment, reproducible seed settings, preserved supplied ordering and invalid-layout/input errors | Proposed; Gate 1 confirms native calls/rounding and separate fixed oracles. No fitted pipeline or protected holdout claim. |
| Project JSON round-trip into supplied mode | Saved layout/ordered IDs/provenance survive project save/load; `create_partitions` rejects mismatched keys or invalid membership; returned identity reflects consumed data | Project owns parsing/file/old-source checks. No public record-reader/writer, restoration compatibility or publication guarantees. Exact helper policies need Gate 1 confirmation. |
| Installed project | Project code uses all reviewed public functions with separate cwd and both normal wheel installations; independent expected outputs and import/runtime identities | Reuse installation infrastructure; new behavioral boundaries need Gate 1 confirmation. No assistant/notebook/DVC replay claim. |
| Existing extraction/quality/strict APIs | Existing M1 regressions and positive/required-failure preparation examples | Reuse confirmed supplier boundaries; no signature or semantics changes. |

Initial assessment oracle for IP1 refinement: four rows with `value=[1,3,5,null]`
and `target=[A,A,B,null]` give one missing value in each column, missingness 0.25,
numeric count 3, min 1, max 5, mean/median 3, and observed target counts A=2/B=1.
Proposed target proportions use nonmissing denominator 3 and report missing count
separately. Gate 1 settles quantiles, variance convention, frequency ordering,
truncation/high cardinality, nonfinite JSON policy and dtype normalization.

For supplied two-way cases, use row IDs 1–6 with literal membership
train=[1,2,3,4], test=[5,6], and assert that no validation key/frame exists.
For three-way cases, use train=[1,2], validation=[3,4], test=[5,6]. Each layout
has a time fixture with increasing declared timestamps and a group fixture with
distinct groups across selected partitions. Assert those independent
properties alongside exact rows/targets. Add separate mutations for overlaps,
unknown IDs, within-partition duplicates, missing coverage and invalid source IDs.
IP1 must add a fixed seeded oracle and impossible-small-data case for each layout,
plus missing/extra/unknown partition names, mismatched recorded layouts and
incompatible fraction settings before approval;
do not compute expected membership by calling the implementation under test.

## US-12 / Implementation Phase 1: Confirm assessment and partition contracts

- **Outcome:** Concrete documented APIs and independently expected test matrix,
  with source identity, project persistence ownership and supplied-protocol limits settled.
- **Entry conditions:** Plan reviewed and IP1 explicitly authorized.
- **Authorization:** Developer “start ip1”, 2026-11-07 UTC; baseline `c0dcaa1`,
  clean branch `US-12-assessment-splits`. Scope synchronization already satisfied.
- **Acceptance criteria advanced:** AC-02/03 design only.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-19-IP1-T1 | Complete | Refresh #19 and supplier discussions/evidence; reconcile two-way/three-way scope with active design and inspect exports/installation seams | IP1 authorization | Stable complete [source refresh](sources/us-12-19-ip1-issues.md); supplier approvals/acceptance verified; existing SC-02 synchronization unchanged; see IP1 evidence | AC-02/03; SC-02 |
| US-12-19-IP1-T2 | Complete | Refine selected `assess_data` contract, native pandas options, schema/scalar policies and literal oracle | T1; SC-03 helper selection | Report contract/policies and public matrix confirmed by developer IP1 approval | AC-02 |
| US-12-19-IP1-T3 | Complete | Refine selected `create_partitions`, supplied/identity policies, project-owned JSON reconstruction, direct dependency and both inventories | T1; SC-03 helper selection | Both-layout/dependency/identity/coverage contracts confirmed; independent native 1.9.1 calls match fixed two-way/three-way oracles | AC-03; SC-02/03 |
| US-12-19-IP1-T4 | Complete | Refine dependent tasks/boundaries; record `docs/verification/us-12-19-ip1.md` and update checkpoint | T2/T3 | Contract, evidence and checkpoint reconciled; document checks pass; Gate 1 approved | AC-02/03 |

### Verification and review evidence

Document-only: inspect issue/design consistency, required fields and literal
fixture arithmetic, confirm existing file references, check local links/anchors
and run `git diff --check`. TDD, builds, dependency synchronization and executable
checks do not apply: this implementation phase changes no executable behavior.
All executable checks are deferred to IP2/IP3 and finally IP4-T4, not claimed passed.
**Actual results:** [IP1 report](../verification/us-12-19-ip1.md): source refresh,
native API references, supplier/probe inspection and document checks. T1–T4
complete; native scikit-learn 1.9.1 reference calls independently confirm both
seeded oracles. Developer “i approve ip1; commit changes” confirms contracts,
policies and public boundaries, 2026-11-07 UTC. No toolkit execution evidence.

Proposed dependent refinement: IP2-T1/T2 use the draft's explicit report and
dtype/finite-value matrix. IP3-T1 uses the direct `scikit-learn>=1.9.1,<1.10`
declaration, both independent inventories and effective native calls;
IP3-T2 uses reviewed membership/protocol policies; IP3-T3 uses project-owned
JSON round-trip and supplied-mode reconstruction with consumed-frame identity.
IP4-T1/T2 repeat the draft's critical families independently on both wheel paths.
Project code writes assessment and partition JSON; only the two selected helpers
are proposed public exports. All these
refinements are confirmed at Gate 1, retain task IDs and existing
M1/M1–6/shared/installed obligations, and authorize no later implementation phase.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; exact public interfaces, input/error
  policies, identity/record semantics and independent test boundaries confirmed;
  any new toolkit-specific support has a recorded developer discussion/decision,
  native library reuse is explicit, and dependency/inventory changes are reviewed.
- **Evidence presented:** [IP1 report](../verification/us-12-19-ip1.md) and
  [approved contract](../data-assessment-and-splits.md); T1–T4 complete with
  document checks and independent native split-oracle confirmation.
- **Remaining limitations:** No toolkit executable behavior or installed evidence.
  Native Parquet identity stability and full type/failure matrix await IP3.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve ip1; commit changes”,
  2026-11-07 UTC; confirms two-helper contracts/policies/test boundaries,
  native reuse and dependency/inventory approach, and authorizes a local commit.
- **Requested changes and resolution:** SC-03 selects two helpers; documentation
  revised; exact contract/test-boundary confirmation received in the approval above.
- **Progression authorized:** Local IP1 commit only. Await explicit IP2 execution
  authorization; do not begin executable implementation or tests.

## US-12 / Implementation Phase 2: Implement descriptive assessment

- **Outcome:** Public descriptive reports match reviewed independent expectations.
- **Entry conditions:** Gate 1 approved, boundaries confirmed and IP2 authorized.
- **Acceptance criteria advanced:** AC-02.
- **Execution:** Authorized by developer “start ip2”, 2026-11-07 UTC.
  T1–T3 technically complete; 35 focused cases pass. M1: 588 passed, 1 existing
  skip (589/691 selected). Shared checks pass; Gate 2 approved on 2026-11-07 UTC.
  Red/green history and limitations: [IP2 evidence](../verification/us-12-19-ip2.md).

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-19-IP2-T1 | Complete | Add proposed `tests/integration/test_data_assessment.py` and `src/agentic_ml/data_assessment/`; start with one numeric/missingness test; implement through individual red–green cycles | Gate 1 | Literal summaries and schema; unchanged caller frame; intended missing-behavior red observed before green | AC-02 |
| US-12-19-IP2-T2 | Complete | Extend same public boundary with categorical/target counts, proportions and reviewed empty/nullable/nonfinite/type/error matrix | T1 | Every case independently expected; JSON serializable under strict finite JSON policy; no target omission or silent coercion outside contract | AC-02 |
| US-12-19-IP2-T3 | Complete | Review refactoring after green; finalize docstrings/examples; run M1/shared checks and record proposed `docs/verification/us-12-19-ip2.md` and checkpoint | T1/T2 | Reviewed assessment contract implemented; all phase checks pass with exact evidence and limitations | AC-02 |

### Verification and review evidence

Focused serial red–green command after file creation:
`uv run --locked pytest tests/integration/test_data_assessment.py -k <behavior>`.
Record serial selection as short TDD feedback. Reuse Gate 1 boundaries; no private
collaborator mocks or expectations derived from toolkit helpers. New tests declare
`milestone_1`. Changed modules: proposed assessment package and public tests.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Assessment matrix | Reviewed public cases, one red–green slice at a time | Exact counts/missingness/balance; numeric tolerance specified at Gate 1; actionable errors | Passed; [IP2 evidence](../verification/us-12-19-ip2.md) |
| Current milestone | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass with counts/skips recorded | Passed; [IP2 evidence](../verification/us-12-19-ip2.md) |
| Shared checks | All commands in shared execution rules below | Pass; lock identity unchanged | Passed; [IP2 evidence](../verification/us-12-19-ip2.md) |

Installed assessment coverage and M2–6 regressions defer to IP4-T1/T2/T4.
Other milestone/tooling exclusions retain their owning obligations below.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; AC-02 editable public behavior verified;
  M1/shared checks pass and red/green evidence recorded.
- **Evidence presented:** [IP2 report](../verification/us-12-19-ip2.md), public
  implementation/tests and guide. 35 focused cases and M1/shared checks pass.
- **Remaining limitations:** Installed verification and AC-03 remain pending.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve ip2; commit changes”,
  2026-11-07 UTC.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Local IP2 commit only. Await explicit IP3 execution
  authorization; no push or PR authorized.

## US-12 / Implementation Phase 3: Implement recorded and validated partitions

- **Outcome:** Seeded and supplied partitions retain exact usable membership and
  identity, with project JSON round-trip/supplied-mode reconstruction and clear
  invalid-input errors through `create_partitions`.
- **Entry conditions:** Gate 2 approved and IP3 authorized; Gate 1 split/identity
  choices remain valid. Reopen contract review before code if they do not.
- **Acceptance criteria advanced:** AC-03.
- **Execution:** Developer “start ip3”, 2026-11-07 UTC, authorizes this phase
  on clean baseline `43cd770`. All four technical tasks are complete through
  the confirmed public boundary. 124 focused cases pass;
  M1 passes 712 tests with one existing skip (713/815 selected, 102 deselected).
  [IP3 evidence](../verification/us-12-19-ip3.md) records all red/green results,
  dependency/typing changes and current verification; Gate 3 Approved.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-19-IP3-T1 | Complete | Add reviewed public tests and approved integration surface (draft paths `tests/integration/test_splitting.py`, `src/agentic_ml/splitting/` remain conditional); declare scikit-learn runtime dependency, intentionally update lock and both inventories; implement native seeded generation for each layout through separate red–green slices | Gate 2; IP1 dependency/integration decisions; synchronized issue scope | Two-way and three-way fixed seed oracles, effective settings, exact names/alignment; no validation placeholder for two-way; incompatible layout/settings fail; direct dependency/inventories agree | AC-03; SC-02 |
| US-12-19-IP3-T2 | Complete | Extend reviewed public boundary/tests for supplied two-way and three-way time/group membership and each invalid membership/layout mutation | T1 | Exact supplied rows/order/protocol retained in either layout; overlaps/duplicates/unknown IDs/reviewed coverage failures and missing/extra/wrong names rejected; no automatic time/group algorithm implied | AC-03; SC-02 |
| US-12-19-IP3-T3 | Complete | Verify JSON-compatible records and consumed-frame identity; add project-owned JSON round-trip and supplied-mode reconstruction for both layouts; update guide; toolkit read/write/filesystem work removed under SC-03 | T1/T2 | Saved layout/ordered membership/provenance survive; supplied mode reconstructs exact rows and rejects layout/key/membership mismatch; changed values/target/dtypes/order change returned identity; project owns file/old-record checks | AC-03; SC-02/03 |
| US-12-19-IP3-T4 | Complete | Compose project extraction and existing `run_validated_step` with assessment/splitting; add sentinel cases in public tests; refactor after green; run M1/shared checks; record proposed `docs/verification/us-12-19-ip3.md` and checkpoint | T1–T3 | Required failure never reaches preparation; valid/advisory/no-check behavior preserves #15 semantics; report and memberships refer to consumed frame; Gate 3 evidence ready | AC-02/03; regression AC-05 |

### Verification and review evidence

Focused command: `uv run --locked pytest tests/integration/test_splitting.py -k <behavior>`;
short serial TDD rationale as IP2. Assert independent literal row/target outcomes
and error classes/context through reviewed public calls. Repeated seeds alone
are insufficient; retain the fixed oracle and saved memberships. New product
cases declare `milestone_1`. Changed modules: selected split package and public
tests/project fixtures; no assessment or partition persistence API.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Seeded/supplied/record matrix | Public `create_partitions` cases and project JSON round-trip with isolated project paths | Literal memberships, JSON-compatible records, source-identity sensitivity and unchanged inputs; invalid supplied membership fails; project persistence is outside toolkit guarantees | Passed; [IP3 evidence](../verification/us-12-19-ip3.md), 124 public cases |
| Required-check composition | Public `run_validated_step`, project sentinel and independent consumed values | Required failure blocks; accepted quality semantics preserved | Passed; [IP3 evidence](../verification/us-12-19-ip3.md), four policy/sentinel cases |
| Current milestone | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass, actual counts/skips recorded | Passed; 712 passed, 1 existing skip; 713/815 selected, 102 deselected; [IP3 evidence](../verification/us-12-19-ip3.md) |
| Shared checks | Commands below | Pass without unintended lock changes | Passed; intentional direct scikit-learn metadata update only; [IP3 evidence](../verification/us-12-19-ip3.md) |

Both installed paths and final M2–6 regressions remain owned by IP4-T1/T2/T4.
Train-only model fitting and actual DVC/MLflow consumers remain their owning
stories, not deferred #19 tests.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; both seeded/supplied layouts, persisted
  layout round-trip through project code and supplied-mode validation, AC-03 public behavior and regression
  composition verified; M1/shared checks pass; identity limits documented.
- **Evidence presented:** [IP3 report](../verification/us-12-19-ip3.md), public
  splitting implementation/tests, guide and dependency/inventory/typing changes.
  124 public cases and M1/shared checks pass; all raw red/green evidence retained.
- **Remaining limitations:** Installed/final acceptance evidence pending IP4.
  Source identity is version-bound native Parquet; project code owns old/current
  identity comparisons and persistence. Time/group protocols are declarations.
  Linux aarch64 only; existing skip and broader milestone obligations remain.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve ip3; commit”,
  2026-11-07 UTC.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Local IP3 commit only. Await explicit IP4
  execution authorization; no push or PR authorized.

## US-12 / Implementation Phase 4: Verify installed projects and issue acceptance

- **Outcome:** Both installed artifact paths verify all #19 public behavior;
  final guidance/evidence supports explicit issue-slice acceptance.
- **Entry conditions:** Gate 3 approved and IP4 authorized.
- **Execution:** Developer “start ip4”, 2026-11-08 UTC. Baseline `ffd5322`;
  T1–T4 technically complete; M1 and final M1–6 each passed 713 tests
  with one existing skip. Shared/document checks pass; Gate 4 Approved. [IP4 evidence](../verification/us-12-19-ip4.md).
- **Acceptance criteria advanced:** AC-02/03 fully within #19 scope.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-19-IP4-T1 | Complete | Add proposed `tests/installation/{assessment_splits_project,check_assessment_splits,verify_assessment_splits}.py`; reuse `verification_support.Invocation` and normal distribution verifier | Gate 3 | Separate project uses only installed public interfaces, declared runtime dependencies and its own code; direct and rebuilt installs retain independent origins/identities | AC-02/03 |
| US-12-19-IP4-T2 | Complete | Add M1 case in `tests/integration/test_distribution_verification.py`; TDD both installed helpers, seeded/supplied two-way/three-way time/group cases, project JSON round-trip/supplied reconstruction and invalid layout/membership cases | T1 | Each wheel exercises both retained helpers and revised positive/negative matrix from unrelated cwd using isolated Python; source identity, import origins, resources, CLI version, runtime inventory and cleanup/evidence checked; no toolkit filesystem/restoration claims | AC-02/03; SC-02/03 |
| US-12-19-IP4-T3 | Complete | Finish guide and README link with explicit two-way/three-way examples and saved layouts; update active design status/traceability without rewriting history | T2 | Runnable examples show optional validation partition and both native split patterns; record schema/downstream handoff documented; no tuning on final-test data, fitting/DVC/assistant acceptance claim | AC-02/03; SC-02 |
| US-12-19-IP4-T4 | Complete | Refresh #19, reconcile criteria/deferrals; run M1, final M1–6/shared checks and document validation; record proposed `docs/verification/us-12-19-ip4.md`, final table and checkpoint | T1–T3 | Final identities, actual counts/skips/platforms and all required #19 evidence reconciled before final gate; no executable change after evidence without renewal | AC-02/03 |

### Verification and review evidence

Reuse Gate 1 confirmed installed boundaries, existing module artifact fixture and
distribution xdist group; new owned child workspaces and isolated Python `-I`.
No editable install, checkout imports or modified origin metadata. Installed
probes must exercise each new public function and critical success/failure
families; don't rely only on editable tests for malformed membership or source
identity. A new installed behavioral test starts red before adding its missing
probe behavior. Preserve existing driver cleanup/logging and runtime inventory.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Installed criteria and integrity | New selected M1 distribution integration case invokes both artifact probes | Direct wheel and wheel rebuilt from sdist pass independently; complete outputs and failures retained | Passed; [IP4 evidence](../verification/us-12-19-ip4.md) |
| Final phase milestone | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass with counts and skip limits | Passed; 713 passed, 1 skipped; [IP4 evidence](../verification/us-12-19-ip4.md) |
| Final issue-slice acceptance | `uv run --locked pytest -n 4 --dist=loadgroup` | M1–6 pass against final executable inputs | Passed; 713 passed, 1 skipped; [IP4 evidence](../verification/us-12-19-ip4.md) |
| Shared checks and documentation | Commands below plus changed links/anchors and guide examples | Pass; no unintended lock changes or false capability claims | Passed; [IP4 evidence](../verification/us-12-19-ip4.md) |

No broader local selection or standalone artifact command is automatic. Selected
M1 tests invoke artifact drivers internally. Unverified operating systems and
historical skips remain explicit limitations; CI cannot substitute local evidence.

### Developer approval gate

- **Approval criteria:** T1–T4 complete, AC-02/03 mapped to actual installed
  evidence, M1/M1–6/shared checks pass and required deferrals reconciled.
- **Evidence presented:** [IP4 report](../verification/us-12-19-ip4.md), installed
  project/probe/driver and regression, guide/README/design status updates. Both
  wheel paths, M1 and final M1–6 pass; shared and document checks pass.
- **Remaining limitations:** Deferred AC-04; downstream fitting/stage/tracking
  adoption, milestone acceptance and unverified platforms remain separate.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve ip4; commit”,
  2026-11-08 UTC.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Local IP4 commit under Gate 4. Subsequent explicit
  issue acceptance authorizes the execute-plan publication/review sequence.

## Shared checks and execution rules

Executable implementation phases retain `uv sync --locked --group dev`,
`uv lock --check`, `uv run --locked ruff check .`,
`uv run --locked ruff format --check .`, `uv run --locked mypy src tests`,
`uv run --locked agentic-ml --version`, and `git diff --check`.
Record `sha256sum uv.lock` before/after; version output must agree with installed
distribution metadata. Unexpected dependency/lock edits need intentional review.
Follow [verification policy](../development/verification.md#phase-and-story-verification).

Mark a task Complete only after its work and required checks pass with actual
evidence. Partial, failed and unverified tasks remain incomplete. Reopen tasks
whose evidence is invalidated. Keep technical completion separate from approval.
Use one behavior-focused red–green slice at a time; keep expected values
independent of implementation, preserve assertions, skips and timeouts, and
refactor only after green. Record all commands, counts, selected/deselected cases,
timings, changed modules, AC IDs and boundary confirmation references.

Stop at every implementation phase gate including the final one. Present tasks,
diff, checks, failures, evidence paths, deviations and limitations. Wait for
explicit approval and record its reference/date; silence is not approval. A
prior decision applies only when it explicitly covers that gate. Pause affected
work and use scope management when evidence invalidates an approved approach.

Make at most three corrective attempts on the same unresolved problem. Record
each hypothesis, change, original-failure verification and relevant regression
results. After the third unsuccessful verification, stop corrective work, preserve
logs and working-tree state, report all attempts and uncertainties, and await
developer direction. Never weaken tests or conceal a failure.

Use [records policy](../development/records.md): reports at the proposed paths
above, durable commands/logs/JUnit/input identities in unique
`.dev-records/verification/<timestamp>-<revision>-us12-19-<phase>/` directories.
Keep generated experiment content/storage/credentials outside Git. Preserve
failed evidence and historical records; pytest temporary paths are not durable
records. Update `CHECKPOINTS.md` at completions, gates, blockers and handoff.

## Final verification requirements

- **Owning final phase/task:** US-12-19-IP4-T4, before the final gate.
- **Final implementation identity:** Tested revision plus working-tree diff,
  lock SHA-256, direct/rebuilt artifact hashes and installed identities, Python,
  uv, pandas/pyarrow/toolkit versions, OS/architecture, project roots/cwds.
- **M1–6/shared checks:** Exact commands above, actual outcomes/counts and skip
  analysis. Renew after executable changes; document-only final edits use document
  checks. Current milestone is also required at IP4's gate.
- **Distribution/installation:** Both normal wheel paths within selected M1 tests;
  unchanged CLI/import/resource/runtime inventories. Standalone artifact drivers
  and complete suite require an explicit developer command.
- **Deferred-check reconciliation:** IP2/IP3 installed omissions resolve in
  IP4-T1/T2; excluded M2–6 regressions resolve in IP4-T4. Existing temporary skips
  and M0/M50/M99/infrastructure exclusions do not establish passing coverage.
  Missing required #19 evidence blocks acceptance.
- **Actual results and limitations:** [IP4 evidence](../verification/us-12-19-ip4.md)
  reconciles both installed paths and final M1/M1–6/shared checks. Linux aarch64
  only; existing skip and deferred milestone owners remain. Acceptance pending.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-12-AC-02 (#19) | IP1-T2/T4; IP2-T1–T3; IP4-T1–T4 | Reviewed literal distribution/missingness/target matrix, both installed paths, final M1–6 | Verified; accepted 2026-11-08 |
| US-12-AC-03 (#19) | IP1-T3/T4; IP3-T1–T4; IP4-T1–T4 | Fixed seeded oracle; supplied time/group membership; invalid layout/membership, consumed-frame identity and project JSON round-trip/reconstruction, both installed paths | Verified; accepted 2026-11-08 |
| Developer extension US-12-19-SC-02: two-way and three-way layouts | IP1-T1/T3/T4; IP3-T1–T3; IP4-T1–T4 | Both layouts generated and supplied, no two-way validation placeholder, recorded layout round-trip/mismatch errors, both installed paths | Verified; accepted 2026-11-08 |
| US-12-AC-01/05 (#15) | Existing supplier plan; IP3-T4/IP4-T2 reuse regressions | Supplier acceptance retained; new composition passes in IP3/IP4 | Accepted supplier scope; no reopening or new acceptance claimed |
| US-12-AC-04 | Explicit future activation required | None claimed | Deferred |

- **Remaining work:** IP1/IP2 tasks Complete; Gates 1–2 approved.
  IP3 complete and Gate 3 approved. IP4 technically complete; Gate 4 approved; issue-slice accepted on 2026-11-08 UTC.
  No full experiment, DVC reproduction or assistant
  acceptance is implied.
- **Partial prerequisite delivery:** No new supplier slices; #19 consumes
  accepted #14/#15 and supplies future consumers with reports and split records.
- **Final verification:** IP4-T4 Complete; M1 and M1–6 each pass 713 tests
  with one existing skip. Shared/document checks and both installed paths pass.
- **Developer acceptance:** Accepted for issue #19 AC-02/03 and both-layout extension.
- **Decision reference and date:** Developer “i accept issue #19”, 2026-11-08 UTC.

## Milestone acceptance handoff

**Owner:** `MVP-M1-ACCEPT-VERIFY`, coordinated by the future US-39 M1 plan.
Preserve historical `M1-ACCEPT-VERIFY` under
[US-03](milestone-1-us-03.md) and independent `M50-ACCEPT-VERIFY` in
[checkpoints](../../CHECKPOINTS.md#outstanding-verification-and-known-limitations).
Reconcile historical selections/skips/failures, raw evidence availability,
artifact/manual/platform deferrals and final criterion inventories before
milestone acceptance. Complete-suite
`uv run --locked pytest -n 4 --dist=loadgroup -m ""`, standalone direct/rebuilt
distribution/installation checks and other broader checks require explicit
developer commands. Preserve their obligations without running them merely
because a template mentions them. Issue acceptance is not milestone acceptance.

## Acceptance and publication

Developer “i accept issue #19”, 2026-11-08 UTC, accepts AC-02/03 and SC-02's
both-layout extension after Gates 1–4 and final verification. AC-04 remains
deferred; milestone acceptance and downstream integration are separate.
Under the execute-plan workflow, this acceptance authorizes committing remaining
records, ordinary push, PR creation and a published static COMMENT review.
Publication completed through [PR #62](https://github.com/jimthompson5802/agentic-ml/pull/62),
base `main` / `bce7ccc`, initial head/acceptance commit `a672dca`.
The branch was pushed normally with upstream tracking.
[Static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/62#pullrequestreview-5815831258)
was published and verified at that head. One
[Low documentation-status finding](https://github.com/jimthompson5802/agentic-ml/pull/62#discussion_r4504392360)
remains open: active data/interface topic pages retain stale pre-implementation
status. No executable defect was identified in inspected changes. Findings
require separate fix authorization. No project code/checks ran during review;
existing IP2–IP4 evidence supplied execution results. Historical source/evidence
was context, not independently re-audited.
Publication-record changes are documentation only; the static review will be
renewed on their resulting head without duplicating the existing finding.
CI Linux/Python 3.12 was pending when inspected. Merging and branch cleanup
remain unauthorized; issue #19 stays open until the PR is merged.


### PR #62 review correction — 2026-11-08 UTC

Developer “resolve this review comment” with discussion r4504392360 authorizes
correcting the active data/interface design status, committing/pushing the fix,
replying to the thread and resolving it. This changes no scope, public contract,
executable behavior or historical approval. Both pages now record completed
IP2/IP3 implementations, both installed IP4 paths, approved Gates 1–4 and issue
acceptance. Native identity evidence links IP3/IP4; the former heading anchor
remains available for existing links. TDD/product tests do not apply to this
documentation-only correction. Document links/anchors, literal stale-status
checks, acceptance-record consistency and `git diff --check` are the verification
boundary; existing executable evidence remains applicable.

Verification passed: read-only Python document check resolved 101 local
links/anchors across the four changed Markdown files, rejected the stale status
phrases, confirmed both pages' approval/acceptance/evidence references and the
legacy heading anchor. `git diff --check` passed. No product tests or dependency
commands were run; executable evidence is unchanged.
