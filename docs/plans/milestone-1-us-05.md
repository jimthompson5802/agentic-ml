# Milestone 1 / US-05: Reject invalid configurations before execution

## Scope and outcome

- **Milestone:** 1 — Run and record a reproducible experiment.
- **User story:** [US-05 / issue #11](https://github.com/jimthompson5802/agentic-ml/issues/11).
- **User-visible outcome:** An experiment user validates algorithm/task/parameter configurations and individual candidates through installed CLI/API interfaces. Invalid inputs receive actionable diagnostics; accepted candidates contain explicit effective parameters, registry defaults and version identities, without granting execution authority.
- **Acceptance criteria covered:** [US-05-AC-01–05](../specs/user-stories.md#us-05-reject-invalid-configurations-before-execution). AC-05 covers every applicable entrypoint introduced here and establishes an integration obligation for future training entrypoints; it does not claim that future runners or unrestricted kernels are protected today.
- **Scope boundaries:** Registry metadata, semantic configuration validation, candidate validation, default resolution, immutable validation evidence and installed-interface checks. Preserve US-03 structural boundary behavior. No training, candidate sampling/optimization engine, data reads, kernel execution, general component loading, model persistence, splits, managed agents or orchestration. Conditional search schemas remain deferred under the design; incompatible configurations must still be rejected. Milestone 99 remains deferred.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [algorithm configuration](../specs/design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration), [supplied components](../specs/design/interfaces-and-configuration.md#user-supplied-ml-components), [execution](../specs/design/execution-and-governance.md#execution), [notebooks](../specs/design/execution-and-governance.md#notebook-development-and-execution-contract), [governance](../specs/design/execution-and-governance.md#governance), [delivery order](../specs/design/milestone-delivery.md#milestone-1-dependencies-and-delivery-order), [acceptance fixtures](../specs/design/acceptance-traceability.md#reference-acceptance-test-datasets), [ADRs](../specs/design/architecture-decisions.md), [layout](../specs/design/repository-layout.md).
- **Coordinated execution index:** None. Consume accepted prerequisites; no new prerequisite-story implementation is included.

## Source snapshot and current implementation

Planning date: 2026-11-04. Started from clean `main` at `4602fa6`; created and verified local branch `US-05-configuration-validation` before requirements analysis. The original request authorized planning only. The developer subsequently approved and committed the plan, then authorized IP1 with “start ip1” on 2026-11-04; IP1 and its public test boundaries were then approved by developer “i approve” after the review discussion on 2026-11-04, accepting the presented request to approve IP1 and authorize IP2. Publication remains unauthorized.

Retrieved issue #11's complete metadata/body and all comment pages using the repository GitHub read helper. It is an open enhancement by jimthompson5802, unassigned, with no GitHub milestone object; its body assigns Milestone 1. Zero unique comments match its reported count; final refresh remained `updated_at=2026-10-30T02:06:23Z`. No discussion scope decisions. Issue and repository criteria agree.

Also retrieved complete prerequisite issue bodies and all comment pages: #9 and #10 are closed, each with zero comments; refreshed timestamps remain `2026-10-31T13:05:49Z` and `2026-11-01T03:39:36Z`, respectively. #9 records the separate VS Code editor decision. Accepted plans and ADR records also govern delivered capabilities. GitHub reads succeeded although `gh auth status` reports an invalid stored token; no credentials were changed.

Existing `src/agentic_ml/planning/boundaries.py` exports `validate_boundaries`, `SearchSelection`, `SearchSpace` and `BoundaryResult` via `agentic_ml.planning`. It checks search shape, scalar types, finite bounds, narrowing and fixed values without registry access or execution. `resolution.py` preserves exact inputs and immutable version 1.0 plan bundles. `resolve_plan`, `inspect_plan` and `verify_plan` are installed public interfaces; `plan resolve/inspect/verify` expose them through the CLI. Readiness is `input_ready`, not execution permission. Initialization resources remain version 0.1 drafts. Existing tests intentionally use synthetic algorithm/parameter names (including `seed`, `count` and `kind`); globally imposing registry validation on historical structural planning would break that accepted contract.

There is no algorithm registry, registry-default resolver, candidate validator or training submission interface in the current package. Runtime dependencies include YAML/JSON-schema and notebook/storage packages; this story should not add a training framework dependency merely to validate static metadata. Reuse installed planning probes in `tests/installation/check_planning.py` and `verify_planning.py` and existing direct/rebuilt-wheel integration coverage. New paths and API names below are proposals until IP1 approval.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-02 project/environment | Installed project-root configuration and explicit setup semantics | IP2 onward | Accepted and merged; [US-02 plan](milestone-1-us-02.md), approved IP1–IP4 and story acceptance |
| US-03 declared boundaries and preserved plans | Versioned inputs, effective narrowing, source identity and approval verification | IP2 onward | Accepted and merged; [US-03 plan](milestone-1-us-03.md), approved IP1–IP4, [contract evidence](../verification/us-03-ip1.md) |
| Registry contract and initial inventory | Exact supported IDs/tasks, parameter specs/defaults, allowed combinations, registry/interface/library version semantics | IP2 registry implementation | Defined in [IP1 D2/D3](../verification/us-05-ip1.md#d2--registry-schema-and-bounded-registration); Approved at IP1, 2026-11-04 |
| Semantic validation integration | Add a distinct validation layer without changing structural plan identity/readiness or reinterpreting 0.1 drafts | IP2/API integration | Defined in [IP1 D1/D6](../verification/us-05-ip1.md#d1--public-interfaces-and-observable-states); Approved at IP1, 2026-11-04 |
| Compatible search combinations | Conservative preflight policy for independent ranges/choices and cross-parameter constraints without exhaustive enumeration | IP2 search validation | Conservative universal-domain checks selected in [IP1 D4](../verification/us-05-ip1.md#d4--configuration-preflight-and-combination-policy); Approved at IP1, 2026-11-04 |
| Project component metadata | Define how future supplied registrations use the same metadata validator; reject duplicate IDs/unsupported interface versions without importing user code | Any registration exposure | Explicit additive metadata only, [IP1 D2](../verification/us-05-ip1.md#d2--registry-schema-and-bounded-registration); loaders/training stay with US-16; Approved at IP1, 2026-11-04 |
| Future training integration | Revalidate current candidate, plan and registry at submission before any training side effect | Future execution capabilities | Handoff to US-10/US-09 and training stories; no executable runner introduced here |

Accepted US-03-SC-01 unauthenticated experiment approval semantics remain applicable. Validation cannot create approvals or turn approval into execution authorization. No execution, acquisition or kernel-isolation decision is required to perform pure configuration validation. Any proposal to invoke supplied code or start work requires scope review and resolution of applicable ADR-004/006 mechanisms first.

## Plan review

- **Status:** Approved.
- **Developer decision:** Plan approved; IP1/IP2/IP3 subsequently approved; whole story accepted on 2026-11-04.
- **Decision reference and date:** Developer message “i approve plan, commit”, 2026-11-04.
- **Requested plan changes:** None recorded.
- Plan approval confirms the proposed investigation scope. IP1 must produce and obtain approval of the concrete public test boundaries before executable tests are written.

## IP1 execution record

Authorized by developer “start ip1”, 2026-11-04; baseline clean branch at `55c03b6`. IP1 technical work is complete in the [contract report](../verification/us-05-ip1.md); IP1 and public test boundaries approved by developer “i approve”, 2026-11-04, following the explicit IP1/IP2 progression request. IP2 authorized; no IP2 gate approval or publication authorization implied.

## IP2 execution record

IP2 authorized by developer “i approve”, 2026-11-04, accepting the IP1 gate request
after interface review. Tests use the approved D7 public boundaries. Registry,
configuration and candidate behavior has focused red/green evidence; currentness
review passed after the cycle-12 correction. Final M1: 370 passed, one existing
skip, 218.29s; all shared checks passed and lock unchanged. See the
[IP2 report](../verification/us-05-ip2.md) and retained JUnit records. IP2 approved by developer “i approve ip2; commit; do not strt ip3 yet”,
2026-11-04. Local commit authorized; IP3 progression explicitly withheld and story
acceptance remains pending.

## IP3 execution record

Authorized by developer “start ip3”, 2026-11-04, superseding the prior
IP3 hold. Baseline clean `US-05-configuration-validation` at `3eefd55`.
Refreshed issue #11 metadata, full body and all comment pages: zero comments,
stable `updated_at=2026-10-30T02:06:23Z`; no changed scope. Approved D7 public
boundaries remain applicable. Installed probe and documentation work are in
progress; final M1 and M1–6 passed (each 371 passed, one existing skip); final developer gate approved by “i approve ip3”, 2026-11-04; whole-story acceptance remains pending.
Evidence: [IP3 report](../verification/us-05-ip3.md).
Developer-requested acceptance rerun subsequently stopped at developer request
“stop the tests”, exit 130; incomplete, no replacement result. Earlier completed
acceptance evidence remains applicable. Do not restart without direction.

## Scope-change history

None. During execution use the [manage-plan-scope procedure](../../.agents/skills/manage-plan-scope/SKILL.md); record change ID/date, request, scope difference, affected tasks/criteria/evidence, decision and authorized resume point. New prerequisite implementation outside this scope requires approved revision and an execution index if multiple owning plans become necessary.

## Execution and evidence rules

Mark tasks Complete only after their work and required verification pass and actual evidence is recorded. Unstarted implementation tasks remain Not started; completed IP1 tasks have their evidence linked below. Reopen invalidated work and renew evidence. Preserve existing approvals and failures.

Use small vertical red–green TDD slices, one behavior-focused failing test followed by minimal implementation and relevant regressions. Keep independently specified expectations and public outcomes. Record exact red/green commands, intended failure diagnostics and actual results in the owning implementation-phase report. Focused serial TDD is permitted with a recorded short-cycle rationale; milestone gates use four workers. Do not batch all tests before implementation.

At every implementation-phase gate, present completed tasks, changed files, criterion coverage, checks/results/counts, evidence identities, deviations and limitations. Stop and await explicit approval, including at the final gate. Plan approval does not approve these gates; silence is not approval. Scope changes pause dependent work. After three failed corrective attempts on the same problem, stop and report hypotheses, changes, original failure, verification output and working-tree state; await direction without weakening criteria or tests.

Reports are proposed `docs/verification/us-05-ip1.md`, `us-05-ip2.md` and `us-05-ip3.md`. Raw evidence belongs under `.dev-records/verification/`, following the [records policy](../development/records.md), outside disposable pytest trees. Retain commands, stdout/stderr, source/installed identities, lock hashes, selected/deselected counts, skips and OS/Python/tool versions. Update [CHECKPOINTS.md](../../CHECKPOINTS.md) at completed work, gates and handoff.

## US-05 / Implementation Phase 1: Settle registry and validation contracts

- **Outcome:** Concrete, reviewable interfaces, schemas, supported inventory, compatibility rules and test boundaries.
- **Entry conditions:** Developer approves this plan and authorizes IP1.
- **Acceptance criteria advanced:** US-05-AC-01–05 through contract definition; no executable delivery claimed.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-05-IP1-T1 | Complete | Inspect planning interfaces/schemas and existing fixtures; write proposed `docs/verification/us-05-ip1.md`; inventory affected installed API/CLI paths | Plan approval | State exact input/output/error contracts and preserve US-03 structural API, version 1.0 bundles and 0.1 drafts; propose `agentic_ml.validation` and `agentic-ml config validate` / `candidate validate` commands | AC-01–05 |
| US-05-IP1-T2 | Complete | In the contract report and bounded additions to `docs/specs/design/architecture-decisions.md`, specify registry metadata and semantic validation evidence | T1 | Choose initial built-in IDs/tasks, complete supported parameter specs/defaults, adapter/library identity and compatibility policy; cover classification and regression; decide project metadata scope, duplicates, unsupported versions, source binding and defaults under environment changes; no callable loading | AC-01, AC-03, AC-04 |
| US-05-IP1-T3 | Complete | Define public test matrix and proposed schema/files for configuration and candidates; refine IP2/IP3 tasks with settled names | T2 | Approve typed equality, null/bool/int/float handling, finite numerics, range endpoints, nonempty choices, compatible combinations, immutable default evidence, candidate materialization and diagnostics; include fail-closed stale/corrupt evidence and a documented future submission contract | AC-01–05 |
| US-05-IP1-T4 | Complete | Validate contract links, criterion mapping and decisions; record report and checkpoint | T3 | No unresolved decision blocks executable tasks; identify every assurance limit and present IP1 review evidence | AC-01–05 |

### Verification and review evidence

Document/link and whitespace checks only; TDD and executable checks do not apply to this contract-only implementation phase. Public test boundaries remain proposed until this gate:

- Public metadata/configuration validation takes explicit task, declared/effective boundaries and versioned registry metadata; returns a fully specified accepted configuration or stable, actionable field/algorithm/parameter diagnostics. It must not execute constructors or supplied imports.
- Public candidate validation checks explicit parameters against a verified configuration, reconstitutes fixed/default values, rejects unsupported or out-of-bound values and reports effective parameters. Checksums identify evidence; they do not authenticate approvals or constrain arbitrary Python.
- Installed CLI/API integration runs from a separate experiment project and unrelated cwd on both wheel paths. A project-owned helper invokes the installed API without source-path access. This covers custom-code callers of validation; future training and interactive-kernel enforcement remain unverified until introduced.
- Do not infer semantic support from US-03's structural `input_ready`. Choose explicit separate status and evidence semantics in IP1. Diagnostics must explain the failure and valid corrective options without reading raw data or exposing credentials.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Contracts and coverage | Review report against issue #11 and accepted US-02/03 contracts | All five criteria mapped; proposed APIs, inventory and boundary limitations explicit | Passed — [IP1 D1–D7](../verification/us-05-ip1.md); manual criterion/task/gate review, 2026-11-04 |
| Document integrity | Resolve relative links/anchors; `git diff --check` | Valid links and clean whitespace | Passed — local link/anchor checks and `git diff --check`, 2026-11-04; [IP1 report](../verification/us-05-ip1.md#task-refinement-and-verification) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; concrete inventory, combination policy, compatibility/evidence semantics and public test boundaries approved before tests.
- **Evidence presented:** [IP1 contract report](../verification/us-05-ip1.md), [bounded ADR proposal](../specs/design/architecture-decisions.md#us-05-ip1--semantic-configuration-and-candidate-validation-proposals), refined plan and checkpoint. T1–T4 technically complete; document checks passed; no executable checks applicable.
- **Remaining limitations or blocked work:** IP1 contracts and public test boundaries approved. Static metadata validation does not provide training adapters, dataset-dependent checks or kernel isolation; see report D3/D7.
- **Developer decision:** Approved, including public test boundaries.
- **Decision reference and date:** Developer “i approve”, 2026-11-04, after the IP1 review and interface explanations.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP2, accepting the presented IP1 approval and IP2 authorization request.

## US-05 / Implementation Phase 2: Implement shared semantic and candidate validation

- **Outcome:** Reusable typed validation with registry identity/default evidence and equivalent public Python/CLI behavior.
- **Entry conditions:** Approved [IP1 contracts and public boundaries](../verification/us-05-ip1.md); paths below are refined by report D2/D7. IP1 gate approved and IP2 authorized on 2026-11-04.
- **Acceptance criteria advanced:** US-05-AC-01–05 for introduced validation interfaces.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-05-IP2-T1 | Complete | Add proposed `src/agentic_ml/validation/{__init__,models,registry}.py` and `tests/integration/test_configuration_validation.py` through vertical TDD | IP1 approval | Implement report D2/D3 and packaged `registry/validation/1.0/builtins.json`: two complete scalar profiles plus additive metadata, strict versions/defaults/rules, no code imports; observed library drift blocks reuse under D6 | AC-01, AC-04 |
| US-05-IP2-T2 | Complete | Add proposed `validation/configuration.py` and the five report D2 schemas under `schemas/validation/1.0/`; reuse `planning/boundaries.py` through its public contract | T1 | Validate parameter types/defaults/combinations and every declared domain; reject empty choices, nonfinite or reversed bounds, fractional integer bounds, nonpositive logarithmic limits; endpoints and equal bounds follow approved contract; existing structural tests pass unchanged | AC-01, AC-02, AC-04 |
| US-05-IP2-T3 | Complete | Add proposed `validation/candidates.py` and independent candidate cases in new test module | T2 | Materialize all fixed/default values without widening search; reject fixed/default changes, extra parameters, type-confused choices, unsupported algorithms and range violations; valid integer-range candidates remain integers; cross-parameter combinations include omitted defaults | AC-01–05 |
| US-05-IP2-T4 | Complete | Add proposed `validation/storage.py`, `src/agentic_ml/cli/validation.py` and CLI registration in `cli/__init__.py`; extend tests | T2/T3 | CLI/API return equivalent effective parameters/diagnostics; preserve source/plan, effective configuration, registry checksum and adapter/library versions; stale, corrupted, unsupported or wrong-plan evidence blocks; reads/writes use explicit project paths; errors never start training or grant authority | AC-01, AC-03–05 |
| US-05-IP2-T5 | Complete | Record TDD and gate evidence in proposed `docs/verification/us-05-ip2.md`; run required checks; update checkpoint | T1–T4 | Full M1 and shared checks pass, lock identity recorded, unresolved/skipped coverage explained; developer review packet complete | AC-01–05 |

T1–T4 describe outcomes, not a license to batch test writing. Complete each behavior's red–green cycle before the next. Proposed registry fixtures must have independently defined parameter expectations rather than deriving expected results from the registry under test.

### Verification and review evidence

- **Selected tests and rationale:** New semantic/candidate tests plus existing M1 planning, approval and initialization tests verify reusable validation without breaking accepted public contracts. Mark tests `milestone_1` when they directly verify this story. Run the entire M1 selection at this gate.
- **Public boundaries:** Use IP1-confirmed API/CLI; independently assert outputs, diagnostics, no input mutation, source preservation and default/version identities. No private call-count or internal-helper assertions.
- **Deferred checks:** Both-wheel installed semantic coverage and final M1–6 acceptance belong to US-05-IP3-T1/T3. Non-M1 selections belong to IP3-T3's reconciliation; unrelated M0/M50/infrastructure tests require an explicit developer command. Future runner/kernel integration and milestone platform/artifact obligations remain separate.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Focused red–green | `uv run --locked pytest tests/integration/test_configuration_validation.py::<approved_test>` (new selector; short serial TDD rationale recorded) | First fails for missing required behavior, then passes with relevant public regressions | Passed — 12 red/green cycles; final focused 57 passed; [IP2 evidence](../verification/us-05-ip2.md#tdd-evidence) |
| M1 implementation-phase gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | All selected tests pass; skips/deselections explicitly reconciled | Passed — 370 passed, one existing skip; 473 collected / 371 selected / 102 deselected, 218.29s; [IP2 evidence](../verification/us-05-ip2.md#verification-and-identities) |
| Shared checks | Commands in Shared verification below | Pass; committed lock unchanged unless an intentional dependency decision was approved | Passed — sync, lock, lint, format, strict types, version and whitespace; lock SHA-256 unchanged; [IP2 evidence](../verification/us-05-ip2.md#verification-and-identities) |

### Developer approval gate

- **Approval criteria:** T1–T5 complete, criterion-mapped red/green evidence, M1/shared checks and no unresolved implementation defects.
- **Evidence presented:** Implementation diff, [IP2 report](../verification/us-05-ip2.md), retained command/JUnit/source identities under `.dev-records/verification/us05-ip2/`, and checkpoint. T1–T5 complete; IP2 approved on 2026-11-04.
- **Remaining limitations or blocked work:** Installed semantic checks and final story verification remain IP3 work; no managed training/kernel enforcement claimed.
- **Developer decision:** Approved; local commit authorized, IP3 explicitly not authorized.
- **Decision reference and date:** Developer “i approve ip2; commit; do not strt ip3 yet”, 2026-11-04.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** None. Await a new explicit instruction before starting IP3.

## US-05 / Implementation Phase 3: Verify installed use and complete story review

- **Outcome:** Both-wheel separate-project evidence, usage documentation and reconciled final acceptance packet.
- **Entry conditions:** IP2 approved and IP3 authorized.
- **Acceptance criteria advanced:** US-05-AC-01–05 for all delivered interfaces; future-entrypoint obligations retained.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-05-IP3-T1 | Complete | Extend `tests/installation/check_planning.py`, `verify_planning.py`, `tests/packaging/check_installed.py` and `tests/integration/test_distribution_verification.py` as needed; add focused installed probe cases through TDD | IP2 approval | Direct wheel and wheel rebuilt from sdist independently expose validation API/CLI/resources outside checkout with declared runtime dependencies; separate project/custom helper verifies valid and invalid tasks, types, combinations, defaults, bounds and stale evidence; no source imports or development dependencies; preserve identity, retention and group isolation | AC-01–05 |
| US-05-IP3-T2 | Complete | Update `README.md`, `docs/development/distribution.md` and applicable public usage docs; record API/runner handoff in proposed `docs/verification/us-05-ip3.md` | T1 | Reproducible configuration/candidate validation examples, supported registry inventory and versions, diagnostics, default evidence and no-authority semantics; explicitly state future submission revalidation and unrestricted-kernel limits | AC-01–05 |
| US-05-IP3-T3 | Complete | Run final M1 gate and M1–6 acceptance/shared checks; reconcile criteria, all phase deferrals, temporary skips, final tested identity and checkpoint | T1/T2 | Final results and known limitations recorded; no skipped test treated as passing; both artifact paths evidenced through selected integration test; final gate ready | AC-01–05 |

### Verification and review evidence

- **Selected tests and impact rationale:** M1 includes installed planning distribution integration; extend its assertions to semantic validation rather than adding an automatic standalone-driver run. Preserve existing initializer/structural/approval coverage and pytest workspace/scheduling contracts.
- **Public boundaries and limits:** Approved IP1 interfaces in fresh installed projects with isolated cwd/environment. Custom helpers exercise validation calls, not a future sandbox or runner. No new kernel starts or training operations are required by this story.
- **Deferred checks:** IP3-T3 owns the M1–6 selection and reconciliation of phase deferrals; M0/M50/infrastructure, standalone artifact commands and full-suite execution require explicit developer command. Keep M1-ACCEPT-VERIFY and historical unresolved timeouts separate.
- **Acceptance schedule:** Run M1 at the executable gate and M1–6 against final story inputs before this final gate; record both commands and outcomes even if their selections currently overlap.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Installed validation | Extended M1 `test_planning_from_both_artifact_paths` via M1 selection; independent probe expectations | Both installed paths pass all required success/failure cases with real identities | Passed — [IP3 report](../verification/us-05-ip3.md), M1 installed probe records |
| M1 gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Passing selected cases, documented skips and counts | Passed — 371 passed, one existing skip; 372/474 selected, 102 deselected; 234.20s |
| M1–6 story acceptance | `uv run --locked pytest -n 4 --dist=loadgroup` | Passing final selected cases, deferred coverage reconciled | Passed — 371 passed, one existing skip in 226.43s; 372/474 selected, 102 deselected; [IP3 report](../verification/us-05-ip3.md) |
| Shared checks and docs | Commands below, relative-link/anchor and example review | Pass; final lock and working-tree identity recorded | Passed — shared checks, document links, unchanged lock and final probe hashes in [IP3 report](../verification/us-05-ip3.md) |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; all in-scope criteria have evidence, installed checks cover both artifacts, final M1/M1–6/shared checks pass and limitations are explicit.
- **Evidence presented:** [IP3 report](../verification/us-05-ip3.md), final probe/test identities, criterion matrix and checkpoint. T1–T3 technically complete; M1 and M1–6 each 371 passed/one existing skip; shared checks pass. Developer approved IP3 on 2026-11-04.
- **Remaining limitations or blocked work:** Future training/kernel enforcement and independent milestone acceptance remain separate; platform limits and historical skips explicitly retained.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve ip3”, 2026-11-04.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** IP3 gate closed. Await explicit whole-story acceptance. No commit or publication requested.

## Shared verification

At each executable gate and final acceptance, record `uv.lock` SHA-256 before/after and run:

```sh
uv sync --locked --group dev
uv lock --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked agentic-ml --version
git diff --check
```

No dependency change is presumed. If IP1 establishes a necessary runtime dependency, record its justification, intentionally update declarations/lock together and independently update installed requirement inventories. Do not silently rewrite the lock during checks. Record each failed check, corrective attempt and renewed result without deleting original evidence.

## Final verification requirements

- **Owning final phase/task:** US-05-IP3-T3; required before final gate presentation.
- **Final implementation identity:** Baseline `3eefd55` plus IP3 probe/test changes; exact SHA-256 in `.dev-records/verification/us-05-ip3/final-identities.json`, direct/rebuilt installed manifests in linked driver records; lock unchanged.
- **M1–6 and shared checks:** Commands above against final story changes; renew after executable changes. Documentation-only follow-ups use document checks when executable evidence remains applicable.
- **Distribution/installation:** Both direct and sdist-rebuilt wheel validation through selected M1 integration checks. Broader local tests and standalone artifact drivers run only on explicit developer command.
- **Deferred-check reconciliation:** IP2 installed checks resolve in IP3-T1; IP2 final acceptance resolves in IP3-T3. Record excluded milestone associations, the three existing temporary skips and their relevance without changing or claiming resolution of them.
- **Actual results and limitations:** Linux/Python 3.12.16 only; M1 371 passed/one existing skip in 234.20s, M1–6 same counts in 226.43s. No macOS/Windows, full suite or standalone artifacts run; historical skips and milestone acceptance remain open.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-05-AC-01: registered algorithms/tasks/parameter names/types/defaults/combinations | IP1-T2/T3; IP2-T1/T2/T3; IP3-T1/T3 | Public config/candidate matrix and both installed probes | Verified for delivered interfaces — [IP3](../verification/us-05-ip3.md) |
| US-05-AC-02: categories and numeric/integer/logarithmic boundaries | IP1-T3; IP2-T2/T3; IP3-T1/T3 | Empty/type-sensitive categories; inclusive/equal/reversed/nonfinite numeric bounds; integer and positive-log cases | Verified for delivered interfaces — [IP3](../verification/us-05-ip3.md) |
| US-05-AC-03: fixed values and recorded untunable defaults | IP1-T2/T3; IP2-T3/T4; IP3-T1/T3 | Explicit effective/default parameters and version identities; reject undeclared tuning and stale registry evidence | Verified for delivered interfaces — [IP3](../verification/us-05-ip3.md) |
| US-05-AC-04: actionable rejection before training | IP1-T1/T3; IP2-T1–T4; IP3-T1/T2/T3 | Installed CLI/API diagnostics; validation remains inert and grants no authority; future submission obligation documented | Verified for delivered interfaces — [IP3](../verification/us-05-ip3.md) |
| US-05-AC-05: shared checks across introduced entrypoints | IP1-T3; IP2-T3/T4; IP3-T1/T2/T3 | Same candidate matrix via CLI/API/project helper; no introduced training entrypoint; later Python/notebook/custom training must revalidate before execution | Verified for delivered interfaces — [IP3](../verification/us-05-ip3.md) |

- **Remaining work:** IP1 approved; IP2 approved and committed locally; IP3 complete and approved; whole story accepted on 2026-11-04. New training entrypoints must consume current validation contracts and independently enforce authorization, access and budgets; this story cannot establish arbitrary-code isolation.
- **Partial prerequisite delivery:** None planned. Existing US-02/03 contracts are consumed without reopening accepted story tasks.
- **Final verification:** Complete — US-05-IP3-T3; M1/M1–6 and shared checks passed, with explicit limitations in IP3 report.
- **Developer acceptance:** Accepted.
- **Decision reference and date:** Developer “i accept user story”, 2026-11-04.
- **Publication:** Accepted-story commit, push, PR and static review authorized by the execute-plan workflow. Published in PR #53; no merge authorized.

## Milestone acceptance handoff

- **Owner:** Existing M1-ACCEPT-VERIFY, recorded in [CHECKPOINTS.md](../../CHECKPOINTS.md) and the [US-03 owning plan](milestone-1-us-03.md).
- **Deferred checks:** Preserve historical artifact/manual/platform obligations, three unresolved temporary timeout skips and all acceptance evidence qualifications. US-05 story acceptance does not close milestone acceptance.
- **Required evidence:** Reconcile criterion coverage, input identities, historical deferrals and current counts under the [verification policy](../development/verification.md#milestone-acceptance). Any complete-suite `-m ""` or standalone artifact/platform command requires explicit developer direction; existing CI does not replace unperformed local checks.


## Story acceptance and publication record

Developer “i accept user story” accepted US-05 on 2026-11-04 after approving IP3.
All three implementation gates are approved; prior M1–6 evidence remains valid.
The requested repeat was stopped at developer direction and is not a passing run.
Only approval/acceptance records changed since final verification; no tests were
restarted. Acceptance authorizes the execute-plan publication sequence. Prepare
accepted-story changes on `US-05-configuration-validation` for a PR into `main`.
Published story commit `e4b5acf` on `origin/US-05-configuration-validation`
with prior commits `55c03b6` and `3eefd55`. Opened standard
[PR #53](https://github.com/jimthompson5802/agentic-ml/pull/53) into `main`;
verified title/body, branch ownership and non-draft status.
[Static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/53#pullrequestreview-5762797927)
verified on `e4b5acf`: no actionable findings. Review executed no project code or
checks. These publication records are a documentation-only follow-up; existing
executable evidence remains valid. Publish these records, then review the final
head's record-only delta and retain that confirmation in the PR review history.
No merge, branch cleanup or other story work authorized. Authentication succeeded
outside the network sandbox; no credential changes required.
