# Milestone 1 / US-11: Extract local experiment data

## Scope and outcome

- **Milestone:** M1, complete one local classification experiment.
- **Owning issue:** [US-11 #14](https://github.com/jimthompson5802/agentic-ml/issues/14).
  [Complete source snapshot](sources/us-11-issue-14.md), retrieved 2026-11-07 UTC:
  one unique comment, all pages retrieved, stable metadata refresh. GitHub's
  milestone field is unset; the issue body assigns all five criteria to M1.
- **User-visible outcome:** A separate experiment project reads local CSV and
  Parquet, inspects source schemas, executes a project pandas function using explicit settings and native
  selection/filter/merge operations, and receives a DataFrame plus traceable extraction
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

### US-11-SC-01 — Pandas extraction foundation — 2026-11-07 UTC

- **Request and reason:** Developer “Instead of creating our own proprietary
  classes, I'd like to use pandas for all data extraction and the basis for
  feature engineering. Rework the design of data extraction to use pandas.”
- **Scope difference:** Replace proposed request/result/schema/source/operation/
  context classes and ExtractionError with native pandas DataFrames, ordinary
  project pandas functions, built-in mappings/tuples and standard/native
  exceptions. Remove the separate inspect_source API and toolkit predicate/join
  interpreter. Source inspection uses pandas directly and the extraction report.
  Retain one small recording/publication helper. Clarify DataFrames as the basis
  for future authored features while retaining training-only learned transforms.
- **Impact:** Reopened IP1-T1–T3 for design/test-boundary rework, now technically
  complete with revised evidence. IP2/IP3 tasks refined in place with stable IDs;
  no executable work started or accepted. Prior IP1 class-contract evidence is
  historical only; its gate was never approved. Original plan approval and
  planning commit 5c035cd remain historical facts.
- **Plan and requirement revisions:** This plan, [contract](../extraction.md),
  [current IP1 evidence](../verification/us-11-ip1.md), active overview/data/
  interfaces/blueprint. All US-11 criterion IDs/outcomes and milestone assignments
  retained; no issue/story text or ADR changed. Feature implementation remains
  outside US-11; no cross-story task added. Current issue #14 remains consistent
  with ordinary project extraction functions and configured operations.
- **Verification and gates:** Renew document/example/link/task/criterion checks.
  Preserve all five criterion families, public installed boundaries, failure and
  identity checks, both wheel paths, M1 phase and M1–6 story commands and shared
  checks. Replace tests of withdrawn toolkit-specific types/semantics with
  observable native pandas/project-function cases. No reduction in milestone or
  artifact evidence; no invented testing of nonexistent proprietary APIs.
- **Decision:** Approved for this design revision by the explicit developer
  instruction above, 2026-11-07 UTC. This does not approve revised IP1 gate or IP2.
- **Resume point:** Revised IP1 contract and public case matrix ready for renewed
  developer gate review; stop before executable implementation.
- **History:** [Initial IP1 evidence](../verification/us-11-ip1-initial.md);
  full pre-revision documents retained under
  `.dev-records/verification/20261107-5c035cd-us11-ip1-pandas/identities/`.

 During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for material scope/approach changes. Record change ID/date, request, scope
difference, impacted tasks/criteria/evidence/gates, decision reference and resume
point here. No inferred approval from silence or command permissions.

## Public contract for IP1 gate review

[Pandas extraction contract](../extraction.md) replaces the original class-based
proposal under US-11-SC-01. Public data is pandas DataFrame, settings/report are
plain dictionaries, and project functions use native pandas operations. One
proposed extract_data recording helper returns a DataFrame/report tuple;
inspect_source and all proposed proprietary extraction classes are withdrawn.
Native pandas semantics replace the custom predicate catalogue/row-order rules.

[Current IP1 evidence and public case matrix](../verification/us-11-ip1.md)
maps the revised boundary to all five criteria. Original proposal/evidence is
preserved as history; it is not current test-boundary confirmation. Proposed
pandas>=3.1,<3.2, pyarrow>=25,<26 and dev-only pandas-stubs>=3,<4 constraints stay
unchanged, with resolution/strict typing pending IP2. Existing strict APIs,
packaged resources, verification commands and developer gates remain unchanged.

## US-11 / Implementation Phase 1: Confirm extraction contracts and test boundaries

- **Outcome:** Reviewable pandas-based component contract and examples before tests.
- **Entry conditions:** Plan review accepted and IP1 separately authorized.
- **Acceptance criteria advanced:** AC-01–05 design only; none verified executable.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP1-T1 | Complete | Refresh #14 and all comments; verify active design/source agreement. Refine the proposed public contract in this plan and proposed `docs/extraction.md`. | Authorization | One native-object helper signature, pandas readers/operations, plain report/settings, path/provenance/publication/failure rules and feature handoff documented with examples; unresolved items block dependent tasks. | AC-01–05 |
| US-11-IP1-T2 | Complete | Review pandas/pyarrow runtime requirements, typing and packaging impact in `pyproject.toml`, `uv.lock` and both independent inventory probes. Record chosen constraints and any necessary reference consultation. | T1 | Dependency/typing proposal and precise touched-file list; no dependency installation or Python implementation in this phase. No blanket suppressions. | AC-01/02/05 |
| US-11-IP1-T3 | Complete | Renew fixtures and public test boundaries for US-11-SC-01; refine stable IP2/IP3 task records and proposed test selectors against native pandas/project functions. | T1, T2 | Developer can approve exact observable tests and coverage limits; document/link/whitespace checks pass and IP1 evidence is recorded in this plan. | AC-01–05 |

### Verification and review evidence

Inspect issue/spec alignment, local links, task/criterion coverage and
`git diff --check`. No executable changes: TDD, milestone tests and shared
executable checks are inapplicable to this documentation-only phase.
Actual results/evidence: [Revised IP1 report](../verification/us-11-ip1.md).
Complete stable issue refresh and active-design comparison retained all criteria.
Pandas/native-object contract and renewed public case matrix replace the initial
proposal. Document/link/anchor/syntax/whitespace checks passed; no product,
test, dependency, lock or packaged-resource changes. Active design documents
were intentionally refined by the developer instruction. No runtime checks run.

**Public boundaries proposed for confirmation:** The function/standard/native
objects in [the contract](../extraction.md), and literal rows/metadata/error
expectations in [the revised public matrix](../verification/us-11-ip1.md#public-test-boundaries-and-case-matrix).
All tests enter through project pandas functions and the installed recording
helper; no private-helper mocks or proprietary predicate/type tests. Native join,
filter and dtype behavior is demonstrated with explicit project settings and
independently specified outputs. Boundary approval remains pending renewed review.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; revised pandas design, native-object helper, dependency
  approach, fixture expectations and public test boundaries explicitly confirmed.
- **Evidence presented:** [API contract](../extraction.md), [IP1 evidence](../verification/us-11-ip1.md), public case matrix and retained document checks.
- **Remaining limitations or blocked work:** No runtime behavior; dependency/typing resolution and actual filesystem behavior await IP2. Contract and public test-boundary confirmation pending.
- **Developer decision / reference / date:** Approved — developer “i approve ip1; commit the changes; i authorize ip2”, 2026-11-07 UTC. Revised contract and public test boundaries confirmed; local commit and IP2 authorized, not IP3 or push.
- **Requested changes and resolution:** US-11-SC-01 requested pandas directly; revised design and evidence presented for renewed review. Gate approval remains pending.
- **Progression authorized:** IP2 authorized by the approval above. Stop at IP2 gate.

## US-11 / Implementation Phase 2: Integrate native pandas extraction and provenance

- **Outcome:** Project pandas extraction and recording/publication helper complete or fail honestly.
- **Entry conditions:** IP1 approved, including test boundaries and dependency scope.
- **Acceptance criteria advanced:** AC-01–05 component behavior; installed-project delivery verified in IP3.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP2-T1 | Complete | Add reviewed direct requirements/dev typing support in `pyproject.toml`, intentionally update `uv.lock`; update independent direct requirement inventories in both probes. Add only the proposed public function export under `src/agentic_ml/extraction/`; no extraction request/result/operation/exception classes. | IP1 gate | Locked environment and both inventory declarations agree; native-object function boundary enables first meaningful red test without unrelated import/setup failure. | AC-01/02/05 |
| US-11-IP2-T2 | Complete | In proposed `tests/integration/test_extraction.py`, add one CSV identity/schema-report test through the helper and a project pandas function; implement native pandas reading under proposed `extraction/sources.py`. Repeat for Parquet, native reader kwargs and missing/malformed/schema/path cases. | T1 | Each behavior has observed red then green; public results match literal schemas/rows and independent hashes; unrelated cwd resolves root correctly. | AC-01/02/05 |
| US-11-IP2-T3 | Complete | Add vertical native-pandas project-function examples/tests for no-op output, selection, filters and merge modes through proposed `extraction/execution.py`. Implement callback invocation and native return validation; do not create `operations.py` or a toolkit query engine. | T2 | Project functions using native pandas and explicit settings produce independent expected rows; native/project errors retain context and no completed output. Each added behavior has its own red–green cycle. | AC-01/03/05 |
| US-11-IP2-T4 | Complete | Add vertical tests and implementation for effective settings, timestamps, source/output identities and complete destination publication under proposed `extraction/provenance.py`; test malformed/changed source, destination conflict and write failure. | T3 | Persisted metadata matches actual output, timestamps bracket execution, old files remain intact; standard/native failures never return a completed dataset/report; no custom exception class. | AC-02/03/04/05 |
| US-11-IP2-T5 | Complete | Run M1 and shared checks below; record red/green commands, results, selected counts, platform and lock identities in proposed `docs/verification/us-11-ip2.md`; update plan/checkpoint. | T1–T4 | Required verification passes; limitations and exclusions explicitly assigned to IP3-T4. | AC-01–05 component scope |

### Verification and review evidence

Execution baseline `0543d26`, approved IP1 contract/test boundaries. IP2-T1–T4
have passing focused evidence (60 cases); no public proprietary classes,
operation interpreter or suppressions introduced. Native-object API and report
are implemented in extraction/__init__.py, sources.py and provenance.py. Direct
requirements/probe inventories and an intentional 18-line lock addition agree.
M1 gate passed: 431 passed, 1 existing skip in 232.63s (432/534 selected;
102 deselected). All shared checks passed and the intentional lock hash remained
unchanged. IP2-T5 is technically complete. Actual evidence is owned by
[IP2 report](../verification/us-11-ip2.md); no gate approval yet.

Public boundaries: reuse IP1-confirmed API/output boundaries. During short serial
TDD cycles use `uv run --locked pytest tests/integration/test_extraction.py::<case>`;
record why serial execution is appropriate. Case names and public expectations are listed in the IP1 case matrix;
implementation starts only after its gate approval. Declare direct M1 requirements with `pytest.mark.milestone_1`.
Focused cycles do not replace the gate command.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Native data operations and failures | One behavior-focused red–green test at a time, using the confirmed API/fixture | Independent rows, metadata, diagnostics and no incomplete success | 60 passed; [IP2 evidence](../verification/us-11-ip2.md) |
| Current milestone gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | All selected M1 checks pass; counts and existing skips reported | 431 passed, 1 existing skip in 232.63s; 432/534 selected, 102 deselected; [IP2 evidence](../verification/us-11-ip2.md) |
| Shared development checks | `uv sync --locked --group dev`; `uv lock --check`; `uv run --locked ruff check .`; `uv run --locked ruff format --check .`; `uv run --locked mypy src tests`; `uv run --locked agentic-ml --version`; `git diff --check` | Pass; capture SHA-256 of `uv.lock` before/after verification; intentional dependency update distinguished from check mutation | All passed; intentional lock hash 4b21570f… unchanged during verification; [IP2 evidence](../verification/us-11-ip2.md) |

Impact: new extraction modules/dependencies, input paths, operation configuration,
output serialization/provenance and failure semantics. M1 retains accepted
initialization/planning/approval/validation regressions. Excluded M2–6 coverage,
external-project pandas customization, both installed artifact paths and final criterion
reconciliation are owned by IP3-T1–T4. Infrastructure/M0/M50 suites and standalone
artifact drivers are not automatically run; broader commands need explicit
developer direction. No exemption for a required slow M1 test.

### Developer approval gate

- **Approval criteria:** T1–T5 complete; red/green and M1/shared evidence passes.
- **Evidence presented:** [IP2 evidence](../verification/us-11-ip2.md), 60 focused passes, final M1 result (431 passed, 1 existing skip), passing shared checks, unchanged verification lock identity and raw JUnit/logs.
- **Remaining limitations:** External-project pandas function and installed artifact evidence pending IP3.
- **Developer decision / reference / date:** Approved — developer “i approve ip2; commit changes; do not start ip3”, 2026-11-07 UTC. Local commit authorized; no IP3 or push authorization.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Originally none. Superseded by developer “start us-11 ip3”, 2026-11-07 UTC; IP3 now authorized, stop at its final gate.

## US-11 / Implementation Phase 3: Verify native project pandas functions and installed delivery

- **Authorization:** Developer “start us-11 ip3”, 2026-11-07 UTC; baseline `0d74c21`, clean tree. IP2 approved and committed; final gate and whole-story acceptance remain pending.
- **Outcome:** All criteria verified through installed public interfaces; usage documented.
- **Entry conditions:** IP2 gate approved; confirmed IP1 callable/installed boundaries.
- **Acceptance criteria advanced:** AC-01–05 complete subject to developer acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-11-IP3-T1 | Complete | Extend public integration tests with a separately installed project pandas function using configured native operations; verify copied settings/code provenance, invalid return, original pandas/project exception types and missing declared input. Reuse IP2 callback support; no second custom-function adapter. | IP2 gate | Ordinary project function produces literal expected rows; failures preserve causes and publish no completed output; undeclared-read capture is not claimed. | AC-01/03/04/05 |
| US-11-IP3-T2 | Complete | Add proposed `tests/installation/check_extraction.py` and an M1 installed test in `tests/integration/test_distribution_verification.py`, reusing its artifact fixture and distribution driver; extend probe inventory/resource checks only as needed. | T1 | Normally install direct wheel and wheel rebuilt from sdist into separate clean environments; copied project probe imports only installed API/project code, checks unrelated cwd, CSV/Parquet/native filter/merge/project-function output, provenance and missing/corrupt-input failure. Assert imports are outside source checkout and runtime dependencies suffice. Observe red/green for new behavior. | AC-01–05 |
| US-11-IP3-T3 | Complete | Finish proposed `docs/extraction.md`, link it from `README.md`; include explicit root/cwd, settings, metadata/failure example and project callable use. Verify newly shipped resources through installed API if any are added by approved contract. | T2 | Commands/API examples match verified behavior; extraction success distinguished from quality validation; checksum/DVC ownership and trusted-code limits stated. No unrelated runtime resource rewrite. | AC-01–05 |
| US-11-IP3-T4 | Complete | Final verification and criterion/deferred-check reconciliation in proposed `docs/verification/us-11-ip3.md`; update this plan and `CHECKPOINTS.md`. | T1–T3 | Final M1 gate, M1–6 acceptance and shared checks pass against final executable changes; both wheel paths and all criterion evidence recorded before final gate. | AC-01–05 |

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
| Callback success/failure and both artifact paths | Focused reviewed TDD selectors; then installed test included in M1 | Correct external-project outputs, dependency/import origins and honest failures | Focused installed test passed in 12.00s; [IP3 evidence](../verification/us-11-ip3.md) |
| Final phase gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass, counts/skip limitations recorded | 432 passed, 1 existing skip in 223.52s; 433/535 selected, 102 deselected; [IP3 evidence](../verification/us-11-ip3.md) |
| Story acceptance | `uv run --locked pytest -n 4 --dist=loadgroup` | M1–6 pass against final implementation; all deferrals reconciled | 432 passed, 1 existing skip in 208.91s; 433/535 selected, 102 deselected; [IP3 evidence](../verification/us-11-ip3.md) |
| Shared development checks | All exact shared commands from IP2 table | Pass with intentional lock changes reviewed and verification immutability recorded | All passed; unchanged lock 4b21570f…; [IP3 evidence](../verification/us-11-ip3.md) |
| Documentation | Local path/anchor and API/example review; `git diff --check` | Links/examples match tested installed behavior | 63 local links/anchors and Python fence syntax passed; [IP3 evidence](../verification/us-11-ip3.md) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; all five criteria have passing evidence,
  both artifact paths verified, no unresolved required behavior or concealed failures.
- **Evidence presented:** [IP3 report](../verification/us-11-ip3.md), both normal wheel paths, 432 passes/1 existing skip in each M1 and M1–6 run, passing shared/document checks and retained source/artifact identities.
- **Remaining limitations or blocked work:** No required US-11 behavior blocker. Existing missing-planning-schema skip and historical obligations remain open; quality/DVC/runner/assistant integration belongs to other stories. Linux aarch64 verified; other platforms unverified by IP3.
- **Developer decision / reference / date:** Approved — developer “i approve ip3”, 2026-11-07 UTC. Final implementation phase approved; whole-story acceptance remains pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Whole-story acceptance subsequently given by developer “i accept us-11”, 2026-11-07 UTC. Publish accepted story under execute-plan; no merge authorized.

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
- **Actual results and limitations:** [IP3 evidence](../verification/us-11-ip3.md) records final source/diff/lock/platform/artifact identities, M1/M1–6/shared checks and all criterion outcomes. Both installed wheel paths passed. Existing skip, historical obligations and other-platform/cross-story limits remain explicit. No story acceptance inferred.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-11-AC-01 | IP1-T1/T3; IP2-T1–T3; IP3-T1/T2 | CSV/Parquet rows, configured operations, actual project callable in both installations | Accepted |
| US-11-AC-02 | IP1-T1/T3; IP2-T2/T4; IP3-T2 | Ordered schemas, types, row/byte counts and source identities | Accepted |
| US-11-AC-03 | IP1-T1/T3; IP2-T3/T4; IP3-T1/T2 | Independently expected operations plus actual effective settings report | Accepted |
| US-11-AC-04 | IP1-T1/T3; IP2-T4; IP3-T1/T2 | Input/output independent SHA-256 checks, paths/settings/time/code references; checksum satisfies output identity branch | Accepted |
| US-11-AC-05 | IP1-T1/T3; IP2-T2–T4; IP3-T1/T2 | Invalid/missing/malformed inputs, native/project configuration errors, callback and publication failure; no incomplete success | Accepted |

- **Remaining work:** Accepted-story publication and static review; all technical tasks and implementation phase gates complete.
- **Final verification:** Complete under US-11-IP3-T4; [IP3 evidence](../verification/us-11-ip3.md).
- **Developer acceptance / reference / date:** Accepted — developer “i accept us-11”, 2026-11-07 UTC. All five criteria accepted; execute-plan accepted-story publication workflow authorized.

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
