# Milestone 1 / US-03: Define experiment objectives and boundaries

## Scope and outcome

- **Milestone:** 1 — Run and record a reproducible experiment. The issue body assigns this milestone; GitHub's milestone metadata is unset.
- **User story:** [US-03 / issue #10](https://github.com/jimthompson5802/agentic-ml/issues/10).
- **User-visible outcome:** In a separate initialized experiment repository, resolve Markdown intent and YAML boundaries through installed CLI/API interfaces into an immutable, versioned, independently verifiable plan. Report unresolved decisions and conflicts before any dependent work can use the plan.
- **Acceptance criteria covered:** [US-03-AC-01–05](../specs/user-stories.md#us-03-define-experiment-objectives-and-boundaries), all five.
- **Included:** Brief/search/execution input contracts; explicit and delegated decisions; boundary narrowing; root-relative paths; source preservation and checksums; scoped approval verification for delegated decisions; plan creation and readiness verification.
- **Excluded:** Dataset reading/extraction, profiling and split generation, training/tuning, notebook execution, run lifecycle, MLflow run capture, complete workflow approvals/recovery, component registration, managed agents and runtime-guidance loading. Later entrypoints must consume and revalidate these contracts before dependent work. Resolving a plan grants no execution or data-access authorization. Milestone 99 remains deferred.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [developer inputs](../specs/design/interfaces-and-configuration.md#developer-experiment-inputs), [search boundaries](../specs/design/interfaces-and-configuration.md#algorithm-and-hyperparameter-configuration), [governance](../specs/design/execution-and-governance.md#governance), [delivery dependencies](../specs/design/milestone-delivery.md#milestone-1-dependencies-and-delivery-order), [acceptance fixtures](../specs/design/acceptance-traceability.md#reference-acceptance-test-datasets), [architecture decisions](../specs/design/architecture-decisions.md).
- **Coordinated execution index:** None. This plan owns only US-03 work; it consumes accepted US-02 capabilities and defines a handoff to US-05 without implementing that story.

## Source snapshot and current implementation

Retrieved issue #10's complete body and all comment pages on 2026-10-31; zero unique comments equals the reported count. Final metadata refresh was stable: `updated_at=2026-10-30T02:06:20Z`. No recorded discussion decisions. Issue and repository acceptance criteria agree.

Also retrieved complete bodies and all comment pages for prerequisite [issue #9](https://github.com/jimthompson5802/agentic-ml/issues/9) and adjacent [issue #11](https://github.com/jimthompson5802/agentic-ml/issues/11). Both have zero comments and stable final metadata: #9 `2026-10-31T13:05:49Z`, #11 `2026-10-30T02:06:23Z`. US-02's body includes the accepted separate VS Code editor decision. Reads succeeded despite sandbox `gh auth status` reporting an invalid token; no publication is part of this plan.

Planning starts from clean `main` at `4b3387f`, on local branch `US-03-experiment-boundaries`. US-02 is accepted and merged in PR #45. Existing CLI exposes `init` and `--version`; `agentic_ml.initialization` exposes initialization. Packaged `templates/initialization/` contains TODO brief sections, an empty algorithm map, execution marked unconfigured, and version 0.1 draft schemas. `initialization/validation.py` validates those draft shapes only. It is not a resolver or candidate validator. Runtime PyYAML/jsonschema are available; no new dependency is assumed. Existing installation and packaging probes verify initialization and resource contents through both wheel paths.

Do not silently reinterpret draft version 0.1 as a runnable configuration. Compatibility with existing initialized projects, safe reruns, and resource assertions must be settled in IP1. Proposed names and paths below are design candidates until that gate.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-02 initialized project | Public init, project root/environment, draft input files, configured storage; no implicit authority | IP2 onward | Delivered and accepted: [owning plan](milestone-1-us-02.md), IP2–IP4 and corrections; PR #45 merged |
| Machine-readable Markdown contract | Recognizable human-editable sections with deterministic explicit/delegated values, source locations, and ambiguity handling; no model interpreting prose as approval | IP2 | Pending IP1-T1 |
| ADR-002/007 input and plan schemas | CLI/API, supported versions, schema evolution, readiness states, diagnostics, root/cwd semantics, immutable storage identity | IP2–IP4 | Pending IP1-T1/T2 |
| ADR-006 delegated approval slice | Authenticated developer channel, protected approval store/trust root, exact decision/configuration binding, revocation/staleness checks; untrusted inputs cannot self-approve | IP4 | Pending IP1-T3 feasibility and developer gate; filesystem flags or editable JSON alone are insufficient |
| US-05 ownership boundary | US-03 owns input resolution, structural search constraints and execution-config subset checks. US-05 adds registry identifier/task/parameter compatibility, defaults and candidate checks at introduced training entrypoints | IP3 onward | Issue #11 inspected; IP1-T2 must document reusable contract and resolve any newly discovered prerequisite through scope review |
| Future execution integration | Consumers must verify the preserved plan and applicable approvals before execution, then apply their own authorization/access/budget enforcement | Later owning stories | No execution entrypoint introduced here; this plan cannot establish runtime isolation or budget consumption enforcement |

Important decisions belong to the bounded IP1 investigation. If authenticated approval cannot be demonstrated under a concrete threat/access model, stop and present alternatives; do not claim AC-04 complete or replace it with a user-supplied approval boolean. If US-05 code becomes a prerequisite rather than a later consumer, revise scope with separate owning tasks/plan and coordinated index before implementing that work.

## Technical approach and public test boundaries

Propose reusable `src/agentic_ml/planning/` with typed public resolve/inspect/readiness interfaces and a shared structural boundary checker. Extend `src/agentic_ml/cli/__init__.py` with corresponding commands; settle exact names/options in IP1. Store versioned schemas as installed package resources, separately from inert initialization schemas unless an explicitly reviewed migration requires otherwise. Use `importlib.resources` for resource access.

Resolution reads only explicitly selected declarative inputs; dataset references and notebook entrypoints are recorded without opening datasets, importing project code, starting kernels, fitting models or invoking adapters. Preserve original input bytes and source provenance alongside effective decisions, explicit defaults, schema/harness identity and checksum manifest. Serialize versions deterministically; preserve earlier versions, detect corruption, and prevent partial writes from becoming ready plans. A changed decision/source creates a new identity and invalidates affected approval bindings. Define whether readiness verifies preserved bytes or current source identity explicitly; never silently rebind an old plan to edited inputs.

| Public boundary | Independently observed outcomes | Limits / confirmation |
|---|---|---|
| Installed resolve/inspect CLI from a separate project and unrelated cwd | Exit codes, actionable field/source diagnostics, preserved inputs, plan bytes/checksums, absence of side effects outside allowed stores | Exact commands pending IP1; plan review confirms proposed boundary before tests |
| Installed typed Python API | Equivalent results/errors, explicit project root, failed readiness for unresolved/conflicting/stale/corrupt inputs | No private helpers, implementation call-order assertions or source-path injection |
| Public structural boundary checker used by resolver | Independently defined allowed/rejected algorithm/parameter selections and narrowed spaces | Registry semantics and training bypass tests belong to US-05 and future execution stories |
| Public approval/readiness interface under separated developer/untrusted identities | Correct scoped approval accepted; forged, stale, replayed or wrong-plan approval rejected; protected records cannot be changed by untrusted principal | Requires actual isolation/identity evidence chosen in IP1; tool permission is not approval |
| Both direct and sdist-rebuilt wheel interfaces | Same fixtures pass with declared runtime dependencies outside checkout; packaged schema inventory verified | Actual OS/tool versions recorded; no unsupported platform claims |

Use tiny classification and regression input fixtures, all three algorithm modes, categorical/integer/float spaces and explicit budget/split constraints from the reference fixture catalogue. Fixture files live in separate temporary project repositories; expected decisions and hashes are independently specified, rather than generated by the resolver under test. IP1 refines exact signatures, supported values, and cases for developer confirmation before writing tests.

## Plan review

- **Status:** Approved.
- **Developer decision:** Plan approved, including proposed public test boundaries and IP1 investigation scope. Implementation authorization and implementation gate approvals remain pending.
- **Decision reference and date:** Developer message “i approve plan; commit and push”, 2026-10-31. This also authorizes committing and pushing the plan and approval records.
- **Requested plan changes:** None recorded.
- **Review outcome:** Scope, proposed public test boundaries and IP1 investigation approved. IP1 must resolve its blocking approval feasibility question and obtain approval for refined concrete contracts before dependent code. Implementation needs explicit authorization.

## Scope-change history

None. During execution follow [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md); record change ID/date, request, scope difference, impact on tasks/evidence, requirement revisions, verification/gates, explicit decision and resume point. Preserve previous evidence and approvals.

## US-03 / Implementation Phase 1: Settle input, plan and approval contracts

- **Outcome:** Concrete contracts and refined executable tasks, with all blocking decisions resolved or explicitly reported as blockers.
- **Entry conditions:** Plan reviewed and IP1 explicitly authorized; refresh issue and accepted prerequisite records.
- **Acceptance criteria advanced:** AC-01–05 through design evidence only.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-03-IP1-T1 | Not started | Create `docs/verification/us-03-ip1.md` (proposed). Define Markdown fields/delegation markers, section parsing, duplicate/missing/contradictory prose handling, supported task/mode/budget values and versioned execution/search input shapes. Inspect existing initialization resources and define explicit transition from inert drafts. | Plan review and authorization | Examples for every brief field; drafts remain blocked; no silent natural-language inference; finalized CLI/API arguments/results/errors and refined test cases | AC-01, AC-04 |
| US-03-IP1-T2 | Not started | In report specify versioned resolved schema, preserved sources/default provenance, checksum algorithm/canonicalization, root discovery versus explicit root, notebook cwd, external references, symlink/escape rules, immutable storage and failure/concurrency behavior. Define US-05 structural-validator handoff and registry/default ownership; update bounded ADR proposals in `docs/specs/design/architecture-decisions.md`. | T1 | Complete resolution/precedence table; exact proposed file layout; stale/tamper/missing/partial-write handling and downstream readiness contract | AC-02, AC-03, AC-05 |
| US-03-IP1-T3 | Not started | Specify and assess developer-authenticated approval mechanism, protected storage and least privilege for config reads/plan writes. Use primary mechanism documentation if needed; record alternatives, deployment prerequisites and executable verification method in report. Refine `planning/` and approval component paths and tasks below. | T1–T2 | Feasible trust/access model, identity binding and revocation/replay rules; otherwise explicit blocker and revised plan before dependent code | AC-04 |
| US-03-IP1-T4 | Not started | Refine this plan and `docs/experiment-setup.md` contract references as needed; review all criterion/fixture mappings, unchanged US-02 behavior and US-05 boundary. | T1–T3 | Concrete public boundaries and implementation/verification commands ready for developer approval; no unknown mechanism hidden in later tasks | AC-01–05 |

### Verification and review evidence

- **Selected tests:** Documentation/design inspection only; no executable behavior changes, so TDD and runtime suite do not apply.
- **Public boundaries:** Table above, refined by T1–T4; confirmation required at this gate before tests.
- **Deferred checks:** All executable checks assigned to IP2–IP4; full final verification owned by IP4-T4.
- **Checks:** Local Markdown links/anchors, `git diff --check`, manual requirement/precedence/approval threat walkthrough. Expected: valid links and an implementable contract with no unresolved blocking decision. Actual: Pending.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; concrete schemas/interfaces, identity/isolation mechanism, draft transition and refined public tests accepted.
- **Evidence presented:** Pending — `docs/verification/us-03-ip1.md` and bounded ADR decisions.
- **Limitations:** Design evidence cannot establish executable AC coverage. Unresolved approval feasibility blocks affected implementation.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — stop and await explicit approval before IP2.

## US-03 / Implementation Phase 2: Resolve explicit inputs and preserve versioned plans

- **Outcome:** Installed CLI/API resolves fully explicit, structurally valid inputs; preserves versioned evidence and reports pending decisions without marking them ready.
- **Entry conditions:** IP1 gate approved; concrete contracts/test boundaries confirmed. No new unresolved schema/storage decision.
- **Acceptance criteria advanced:** AC-01, AC-03, AC-05; explicit and unresolved portions of AC-04.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-03-IP2-T1 | Not started | Add `tests/integration/test_planning.py` and input fixtures (proposed). One red–green slice at a time, implement `planning/` models/parser and installed schema resources; extend CLI. Cover required brief fields, explicit classification/regression, use/select/compare intent, delegated/TODO/missing/duplicate/conflicting values. | IP1 approval | Installed API/CLI produces expected decisions or source-located blocking diagnostics; draft input cannot become ready through defaults | AC-01, AC-04 |
| US-03-IP2-T2 | Not started | In `planning/` implement approved root/path rules. Add cases invoked from project root, nested and unrelated cwd, roots with spaces, explicit notebook cwd, external data references and unsafe symlinks/escapes per IP1 matrix. | T1 | Identical root-relative identities across caller directories; cwd explicit; data references confer no access and no dataset reads occur | AC-05 |
| US-03-IP2-T3 | Not started | Implement immutable plan/source manifest persistence in `planning/`; add public inspect/verify cases for exact byte checksums, changes producing new versions, old-version retention, missing/corrupt evidence, interrupted writes and concurrent resolution. Update installed resource inventory probes in `tests/packaging/check_installed.py`. | T1–T2 | Independently recomputed checksums match preserved bytes; partial/corrupt evidence never verifies as ready; unrelated project files/pin/lock preserved | AC-03, AC-04 |
| US-03-IP2-T4 | Not started | Record TDD and phase evidence in `docs/verification/us-03-ip2.md` (proposed), update this plan/checkpoints and run checks below. | T1–T3 | Selected tests, broad-trigger checks and shared checks pass; actual limitations/counts recorded | AC-01, AC-03–05 |

### Verification and review evidence

- **Selected tests:** `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_initialization.py tests/integration/test_cli_version.py`. New path is proposed. These cover new public interfaces plus initialization compatibility and CLI regression.
- **Public boundaries:** Installed CLI/API and inspect/verify; source-checkout API tests alone do not establish installation correctness. Add isolated installed planning probe under `tests/installation/` (proposed exact path finalized IP1), exercised by the distribution tests.
- **Deferred checks:** Unrelated installation-upgrade and scheduling tests may be deferred to IP4-T4 only if no broader trigger applies.
- **Broader-run triggers:** Shared public schema or package resource/discovery changes in this phase require the full suite and applicable distribution/installation checks before this gate. This is expected for the planned schema/resource additions; do not rely on the narrower selection alone.
- **Expected:** Explicit valid fixture resolves and verifies; pending/conflicting inputs block readiness; root/cwd and preservation checks pass. Actual results/evidence: Pending.
- Run shared checks defined below; record serial focused TDD exception only for short individual cycles, then four workers at gate.

### Developer approval gate

- **Approval criteria:** T1–T4 complete; passing criterion-mapped success/failure, preservation, installed and required broader checks.
- **Evidence presented:** Pending — IP2 report, red/green commands, artifact/source identities and counts.
- **Limitations:** Search narrowing and delegated approval completion remain IP3/IP4; intermediate output must report this truthfully.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — stop before IP3.

## US-03 / Implementation Phase 3: Enforce declared search boundaries during resolution

- **Outcome:** Brief and execution selections can narrow declared YAML boundaries; no input can widen algorithms, fixed parameters or permitted search values.
- **Entry conditions:** IP2 approved; US-05 handoff and structural rules accepted at IP1.
- **Acceptance criteria advanced:** AC-02 and conflict portion of AC-04; source/plan evidence extends AC-03.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-03-IP3-T1 | Not started | Add boundary cases in `tests/integration/test_planning.py`; implement public structural checker in `planning/` (proposed). Cover fixed/search overlap, empty choices, categorical type distinctions, finite inclusive integer/float bounds, boolean-as-number rejection, positive logarithmic limits and unknown schema fields. | IP2 approval | Well-defined spaces accepted; invalid space rejected with source/parameter diagnostics; one behavior per red–green slice | AC-02, AC-04 |
| US-03-IP3-T2 | Not started | Apply one shared checker to CLI/API resolution. Test use/select/compare, brief narrowing, fixed-value changes, extra algorithm/parameter, category/range widening, incompatible narrowing and omitted parameters. Preserve source and effective boundary separately. | T1 | Execution configuration cannot expand YAML; omission cannot create tunability; effective decisions and reasons for rejection independently verified | AC-01–04 |
| US-03-IP3-T3 | Not started | Extend isolated installed planning probe to both wheel paths; document public validation handoff to US-05 in IP3 report and setup guide. Run selected/shared checks and update evidence/checkpoints. | T1–T2 | CLI/API agree from outside checkout; no registry implementation or training implied; required broader checks pass | AC-02–04 |

### Verification and review evidence

- **Selected tests:** `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_distribution_verification.py tests/integration/test_initialization.py`. Exercises resolver, packaged schemas and preservation compatibility.
- **Public boundaries:** Installed resolver and public structural checker; registry name/type/default/combination validation and candidate admission are US-05 obligations. No claim that these tests enforce training entrypoints that do not exist.
- **Deferred checks:** Unrelated pinned-upgrade/scheduling checks to IP4-T4, only when broader triggers do not require them now.
- **Broader-run triggers:** Full suite and applicable artifact checks if shared schemas/resources change, dependency changes, access enforcement changes or uncertain shared impact. Do not defer a relevant failure.
- **Cases:** Equality at bounds and just-outside rejection; null/string/boolean distinctions; all three modes; independent effective boundary expectations; CLI/API same outcomes. Expected pass; actual results Pending in `docs/verification/us-03-ip3.md` (proposed).
- Shared checks required before gate; preserve every red/green outcome and selected/deselected count.

### Developer approval gate

- **Approval criteria:** T1–T3 complete; no widening bypass through either introduced entrypoint; evidence and compatibility reviewed.
- **Evidence presented:** Pending — IP3 report and downstream contract.
- **Limitations:** Registry/model semantics and future candidate submission remain US-05/later execution capabilities; delegated approval remains IP4.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — stop before IP4.

## US-03 / Implementation Phase 4: Verify delegated decisions and complete installed acceptance

- **Outcome:** Only authenticated, correctly scoped approved delegated decisions become usable; final installed behavior meets all US-03 criteria.
- **Entry conditions:** IP3 approved; IP1 approval mechanism remains feasible and concrete. Any changed mechanism requires scope review before dependent work.
- **Acceptance criteria advanced:** AC-04 completed; AC-01–05 integrated and verified.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-03-IP4-T1 | Not started | Implement IP1-selected authenticated developer approval interface and verifier in proposed `src/agentic_ml/approvals/`, integrated with `planning/` readiness; extend CLI and installed probe. Add regression one slice at a time for unresolved delegation, proposal without approval, approved proposal and scoped identity matching. | IP3 approval; accepted IP1 mechanism | Ready plan records effective choice, reason/source and valid protected approval evidence; approval is distinct from execution permission and story acceptance | AC-01, AC-03, AC-04 |
| US-03-IP4-T2 | Not started | Test untrusted identity cannot issue/alter approvals; forge/replay/wrong-project/wrong-decision/stale/revoked approval, source tampering, changed budgets/metric/search and retained prior version. Exercise the public readiness verifier independently of resolve via CLI/API. | T1 | Every invalid binding blocks affected use and leaves reviewable evidence; accepted old evidence is never rebound to revised configuration | AC-03, AC-04 |
| US-03-IP4-T3 | Not started | Update `docs/experiment-setup.md`, README capability wording and example inputs (proposed under `examples/` if needed); document draft transition, public commands, path semantics, approval deployment requirements, US-05/future execution integration and limitations. | T1–T2 | Runnable explicit and delegated walkthroughs through installed package; no claim of training/execution isolation or automatic agent decisions | AC-01–05 |
| US-03-IP4-T4 | Not started | Run final verification below; record criterion matrix, artifact identities and actual platform/limitations in `docs/verification/us-03-ip4.md` (proposed). Reconcile all deferred checks, plan statuses and CHECKPOINTS.md. | T1–T3 | Complete suite, shared checks, both wheel paths and installed success/adversarial fixtures pass on final implementation before final gate | AC-01–05 |

### Verification and review evidence

- **Selected tests during development:** `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py` plus finalized public approval integration test path from IP1 (proposed `tests/integration/test_plan_approvals.py`). Include actual separated-identity access tests, rather than mocks of authentication.
- **Public boundaries:** Installed CLI/API, protected approval interface and standalone readiness verification; confirm actual threat model and inaccessible trust resources. Unrestricted same-identity workspace tests do not demonstrate protection from assistant/experiment code.
- **Deferred checks:** None at gate. IP4-T4 resolves all earlier deferrals.
- **Broader-run triggers:** Cross-entrypoint authorization/access changes require full suite and applicable installed artifact verification; final verification is mandatory regardless.
- **Expected:** Valid approved decision works; all forged/stale/mismatched paths block; final complete regression suite passes. Actual: Pending.

### Developer approval gate

- **Approval criteria:** T1–T4 complete, all five ACs verified, trust/access limitations explicit and required final evidence passing.
- **Evidence presented:** Pending — IP4 report, complete verification and criterion matrix.
- **Remaining limitations:** Runtime execution, dataset acceptance, scientific validity, model quality and full workflow governance remain separate outcomes.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Pending — stop; whole-story acceptance requires an explicit developer decision after final verification and gate approval.

## Shared and final verification requirements

- **Owning final task:** US-03-IP4-T4; before final gate and story acceptance.
- At every executable gate run `uv sync --locked --group dev`, `uv lock --check`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy src tests`, `uv run --locked agentic-ml --version` and `git diff --check`. Record lock SHA-256 before/after and explain intentional dependency changes. No dependency change is assumed; a required change triggers broader verification.
- Final complete suite: `uv run --locked pytest -n 4 --dist=loadgroup`, without filters; preserve JUnit output, counts and duration. Keep tests/assertions enabled. Record any serial focused TDD exception and its rationale separately.
- Build into a fresh empty artifact directory: `uv build --out-dir /private/tmp/us-03-final-artifacts` (choose a fresh path if occupied). Then `uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir /private/tmp/us-03-final-artifacts` and `uv run --locked python tests/installation/verify_initialization.py --artifacts-dir /private/tmp/us-03-final-artifacts`. Extend the installed probe/driver to include planning and approvals for both direct and genuinely sdist-rebuilt wheels. A complete-suite run may supply identical checks when it demonstrably exercises the required final artifacts; avoid duplicate unchanged verification.
- Verify imports and public CLI/API outside the checkout, declared runtime dependencies, packaged schemas, initializer compatibility, unchanged project pin/lock, root/cwd cases, independent checksum expectations and actual protected approval identities. Separate tiny project fixtures; no source imports, fabricated origin metadata, production credentials or external dataset contents in Git.
- Record revision plus working-tree changes, lock/artifact hashes, OS/architecture/Python/uv/library versions, commands/outcomes, selected/deselected and final totals. macOS evidence does not establish Linux/Windows support; record hosted evidence if observed and distinguish unverified platforms. Manual walkthrough uses installed CLI/API; editor/kernel execution is outside this story.
- **Deferred-check reconciliation:** IP2/IP3 unrelated upgrade/scheduling regressions and all artifact checks must be accounted for by final full suite and installed evidence. No unresolved failure or missing required proof at acceptance.
- **Evidence renewal:** Executable changes after verification require affected reruns and renewed full-suite evidence; changed package/dependency/build inputs require renewed artifacts. Documentation/approval-record-only edits need document/link/whitespace checks with rationale.
- **Actual final results:** Pending. Commands here are planned, not passing evidence.

## Execution rules

Mark tasks Complete only after work and required checks pass; record actual red/green commands/results, evidence and limitations in phase reports. Partial/failed/unverified work stays incomplete. Use one behavior-focused TDD slice at a time; refactor only while green. IP1 documentation work has no executable behavior, so TDD does not apply.

Stop at every implementation phase gate. Present tasks, checks, actual results, deviations and limitations; wait for explicit developer approval and record its reference. Plan approval and tool permissions do not approve implementation gates or product decisions. Reopen invalidated tasks and evidence.

Follow the [scope-change procedure](../../.agents/skills/manage-plan-scope/SKILL.md) for changed requirements, invalidated approach or newly required cross-story work. Keep at most three corrective attempts for the same unresolved problem, recording hypothesis/change/verification. After the third failure stop and present original criteria, all attempts and diagnostics, working-tree state, uncertainties and options; await developer direction. Preserve original tests and criteria; do not suppress or weaken failures.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Required verification evidence | Result |
|---|---|---|---|
| US-03-AC-01 — brief fields and explicit delegation | IP1-T1; IP2-T1; IP3-T2; IP4-T1/T3/T4 | Classification/regression, complete fields, use/select/compare, missing/ambiguous/delegated cases through installed CLI/API | Pending |
| US-03-AC-02 — hard search boundary | IP1-T2; IP3-T1–T3; IP4-T4 | Independently defined fixed/categorical/integer/float boundaries; narrowing accepted and expansion rejected through CLI/API | Pending |
| US-03-AC-03 — versioned effective plan and source checksums | IP1-T2; IP2-T3; IP3-T2; IP4-T1/T2/T4 | Exact preserved bytes/hashes, immutable revisions, approvals/source references, missing/corrupt/partial-write rejection and readiness contract | Pending |
| US-03-AC-04 — conflicts block; delegated choices approved | IP1-T1/T3; IP2-T1/T3; IP3-T1/T2; IP4-T1/T2/T4 | Conflict/unresolved diagnostics, authenticated valid approval and independent adversarial readiness checks; no self-approval | Pending |
| US-03-AC-05 — root-relative inputs and notebook cwd | IP1-T2; IP2-T2; IP4-T3/T4 | Same identities from multiple caller directories; explicit cwd and safe path-boundary cases | Pending |

- **Remaining work:** All implementation tasks; no AC claimed complete by this plan.
- **Partial prerequisite delivery:** None. US-05 registry/candidate behavior remains its owning story; downstream entrypoints must wire this plan's readiness and boundary contracts before shipping.
- **Final verification:** Pending — IP4-T4.
- **Developer acceptance:** Pending.
- **Decision reference and date:** Pending.
