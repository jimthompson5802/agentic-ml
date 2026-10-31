# Milestone 1 / US-02: Initialize an experiment project

## Scope and outcome

- **Milestone:** 1 — Run and record a reproducible experiment.
- **User story:** [US-02 / issue #9](https://github.com/jimthompson5802/agentic-ml/issues/9).
- **User-visible outcome:** From a separate Git/Python project containing a full-SHA installed harness dependency, `uv run agentic-ml init` creates reviewable experiment inputs, project-package scaffolding, a synchronized environment, and usable local storage while preserving existing work and granting no experiment authorization.
- **Acceptance criteria covered:** [US-02-AC-01–05](../specs/user-stories.md#us-02-initialize-an-experiment-project), in full.
- **Scope boundaries:** Initialization, packaged templates, dependency/environment setup, storage setup, explicit incomplete setup choices, and installed-interface verification. Input resolution/semantic validation (US-03/US-05), managed execution, extraction, dataset versioning/restoration, scientific evaluation, component registration, runtime-guidance loading, adapters, and orchestration remain with their owning stories. Storage initialization does not require a dataset, experiment run, authenticated agent, or approval-service implementation. No registry publication or Milestone 99 work.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [initialization](../specs/design/interfaces-and-configuration.md#project-initialization-and-installation), [input contracts](../specs/design/interfaces-and-configuration.md#developer-experiment-inputs), [execution and storage](../specs/design/execution-and-governance.md), [layout](../specs/design/repository-layout.md), [delivery order](../specs/design/milestone-delivery.md#milestone-1-dependencies-and-delivery-order), [acceptance fixtures](../specs/design/acceptance-traceability.md), [architecture decisions](../specs/design/architecture-decisions.md).
- **Coordinated execution index:** None. Reuse accepted US-01; no new prerequisite-story implementation is planned.

## Findings and source reconciliation

Planning baseline: main `4477162`, 2026-10-30. Created local branch `US-02-experiment-init` before requirements analysis. Preserved the pre-existing uncommitted executive-overview checkpoint entry.

Issue #9: open, enhancement, author jimthompson5802, no assignees or GitHub milestone object; its body assigns Milestone 1. Full body and all comment pages retrieved successfully; zero comments, stable refreshed `updated_at=2026-10-30T02:06:19Z`. No comment scope decisions. Prerequisite issue #8: closed, full body and all comment pages retrieved, zero comments; refreshed timestamp `2026-10-30T10:42:22Z`. US-01's owning plan records both approved implementation gates and whole-story acceptance. API reads succeeded, although local `gh auth status` reported an invalid stored token; recheck authentication if later required reads fail.

Existing package has Python >=3.12, Hatchling builds, a version-only argparse CLI in `src/agentic_ml/cli/__init__.py`, no third-party runtime dependencies, and provisional template/guidance resources. Existing installation drivers verify full-SHA dependency identity and upgrades; packaging drivers verify direct and sdist-rebuilt wheels outside the checkout. No initializer, usable experiment templates, configuration models, or storage implementation exists. The packaging probe currently expects a one-distribution runtime closure and exact provisional resource contents; extend that contract deliberately when real dependencies/resources are added, preserving meaningful independence of its assertions.

The issue and repository story agree. Design layouts and schemas are illustrative. ADR-007 settles naming and full-SHA installation, but configuration and extra CLI/API interfaces remain pending. ADR-005 storage mechanisms and the initialization-relevant portion of ADR-006 need decisions before code. IP1 produces those decisions for developer review; it does not claim to settle later execution isolation or recovery. The old pending package-name sentence in the design is superseded by ADR-007 and implemented metadata.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Installed pinned dependency | Normal installed harness, full Git SHA and project lock identity, public CLI/resources available | IP2 onward | Delivered: [US-01 plan](milestone-1-us-01.md), [IP1 evidence](../verification/us-01-ip1.md), [IP2 evidence](../verification/us-01-ip2.md); both gates approved, story accepted, PR #44 merged |
| Public init contract and schema slice | Root selection, naming, CLI/API arguments/results/errors, schema versions and template inventory; review test boundaries | IP2 | Contracts approved at IP1 gate; [IP1 report](../verification/us-02-ip1.md) |
| Existing-file and partial-failure rules | Distinguish safe edits to shared metadata from conflicts; define reruns, symlinks, interrupted setup, recovery instructions | IP2–IP4 | IP1 preservation/failure matrix approved; IP2 scaffold checks passed |
| Dependency set and ownership | Separate harness runtime needs from experiment ML/notebook/storage needs; compatible Python 3.12 versions and lock-preserving uv workflow | IP3 | IP1 dependency contract approved; parser/schema runtime closure verified in IP2; experiment resolution belongs to IP3 |
| ADR-005 storage slice | DVC metadata/cache/store, MLflow backend/artifacts, durable-state location and initialization format; local defaults and explicit overrides | IP4 | IP1 storage contract approved; actual provisioning belongs to IP4; full workflow-state/recovery schemas remain downstream |
| Setup authority boundary | Explicit path choices authorize only setup writes; no data reads, experiment execution, adapter login, or approval grants; no credentials in tracked files | IP2 onward | IP1 setup boundary approved; scaffold boundary verified in IP2; later isolation remains unresolved and unavailable |

## Technical approach and public test boundaries

Implement reusable initialization under `src/agentic_ml/initialization/` (proposed), reached by the existing CLI and a typed public Python API whose signature is settled in IP1. Package templates under `src/agentic_ml/templates/`; load them through `importlib.resources`. Keep project-owned configuration/code in the selected experiment project. Add only the minimum initialization schema/model slice; full brief resolution and search-space enforcement remain downstream.

Preflight the complete setup plan before writing: project identity/root, dependency pin, target collisions, configuration choices, and writable storage destinations. Preserve existing custom files byte-for-byte; shared files such as `pyproject.toml` and `.gitignore` need explicit, documented additive-edit rules. Never silently replace incompatible settings or user work. IP1 must define a safe rerun and failure protocol for non-atomic uv/DVC operations; do not promise cross-tool rollback without evidence. Report nonzero failures, completed steps, remaining work, and safe retry instructions while preserving diagnostics and existing state. No overwrite/force behavior is assumed.

Proposed test boundaries, subject to developer confirmation in plan review and refinement at IP1:

| Public boundary | Independent observations / coverage | Limits |
|---|---|---|
| Installed CLI, invoked in separate temporary experiment projects | Exit/stdout/stderr, generated file inventory/content, original-file hashes, pin/lock/environment identity, explicit root and storage behavior | Does not prove later managed execution, authorization enforcement for user code, or scientific validity |
| Installed public Python initialization API | Same result/error contract and filesystem outcomes as CLI; explicit root from an unrelated working directory | No assertions on private helpers or collaborator call sequences; exact signature awaits IP1 |
| uv and installed project environment | Real metadata/lock consistency, required distribution imports, project-package import, notebook kernel availability | Dependency availability does not prove model training or managed notebook execution |
| DVC, MLflow and initialized state through their public interfaces | Usable local configuration/stores and reopenable initial state; default and explicit locations; no synthetic dataset/run accepted by initialization | Setup smoke probes do not implement full provenance, data restoration, workflow approvals or recovery |
| Direct wheel and sdist-rebuilt wheel | Isolated installation and init with declared runtime dependencies, packaged resources and no harness checkout imports | Actual platforms tested must be recorded; no inferred Windows support |

Use controlled local fixture projects without real data or credentials. Sentinel secrets may test exclusion; never use actual secrets. Test successful paths and one boundary/failure at a time, using independently specified expected outputs. Resource inventories must be explicit, not derived from production generation code. Any process seam used for deterministic external-tool failure injection supplements real-tool integration; it cannot replace it. No tests are written until boundary confirmation.

## Plan review

- **Status:** Approved.
- **Developer decision:** Approved — plan and proposed public test boundaries; IP1 execution authorized.
- **Decision reference and date:** Developer message “commit changes; i approve the plan, execute us-02 ip1”, 2026-10-30.
- **Requested plan changes:** None recorded.
- **Review requested:** Confirm scope, proposed public test boundaries, and IP1's bounded design investigation. IP1 gate must approve its concrete contracts and refined tests before executable implementation.

## Scope-change history

**US-02-SC-01 — 2026-10-30:** Developer removed the mandatory notebook-editor dependency throughout delivery and selected VS Code as the documented editor, not a required dependency. Approved by “Implement the plan.” Use kernel availability probes; retain ipykernel/nbclient and editor-independent CI. Update US-02-AC-03 and US-08-AC-01 without changing IDs. No completed implementation evidence invalidated; all gates remain pending. Resume at plan review, then separately authorized IP1.

During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes; record request, difference, impacted tasks/evidence, decision and authorized resume point here.

## US-02 / Implementation Phase 1: Settle initialization contracts

- **Outcome:** Reviewable initialization design and refined implementation tasks with no unresolved decision blocking IP2–IP4.
- **Entry conditions:** Developer approves this plan and authorizes IP1. Refresh issue #9 and prerequisite status before execution.
- **Acceptance criteria advanced:** US-02-AC-01–05; design evidence only, no criterion claimed complete.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-02-IP1-T1 | Complete | Inspect existing CLI/package/probes and public tool documentation; create `docs/verification/us-02-ip1.md` (proposed). Specify CLI/API, explicit root and project/experiment/package naming, file inventory, versioned schemas/typed models and incomplete template semantics. Refine concrete files and cases in this plan. | Plan approval | Concrete interfaces, examples and independently defined expected file contents ready for review; existing project package handling specified. | AC-01, AC-02 |
| US-02-IP1-T2 | Complete | In the IP1 report define shared-file additive edits, conflict diagnostics, no-write preflight, repeat init, missing/malformed project metadata, full-SHA pin validation, nested roots, symlinks/path escape, concurrency and failure/retry boundaries. Specify setup choices for data, agents and approval presentation. | T1 | Reviewable success/failure matrix; explicit setup-write destinations, unset authority and no implicit data reads/execution; ambiguous cases block dependent implementation. | AC-01, AC-02, AC-05 |
| US-02-IP1-T3 | Complete | Inspect uv public help/docs and selected libraries' official dependency/platform requirements. Record minimum required ML, notebook (`nbclient`, `ipykernel`) and storage packages, ownership, version ranges, installation ordering and lock checks. Decide initial framework set against design scope rather than assuming all later modeling integrations are required now. | T1 | Exact dependency table and uv commands; preservation of harness source/SHA and unrelated dependencies; failures diagnosable without weakening locked checks. | AC-02, AC-03 |
| US-02-IP1-T4 | Complete | Specify local DVC/cache/store, MLflow backend/artifacts and initial durable-state representation, default paths, root-relative resolution and configurable local/external destinations. Record bounded ADR-002/005/006/007 decisions in `docs/specs/design/architecture-decisions.md` for review; refine schema/example sections only as needed. | T1–T3 | Supported local backend mechanisms and public usability probes chosen; credential-bearing URI/settings handling, existing stores and permission failures specified. Remote service provisioning stays outside scope. | AC-04, AC-05 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Contract completeness | Trace each criterion to concrete interfaces, proposed files, expected outputs and test matrix in IP1 report | No blocking implementation decision unresolved; otherwise revise plan and stop | Passed — [IP1 report](../verification/us-02-ip1.md); design completeness only, runtime checks deferred as planned |
| Source compatibility | Read installed uv help and primary documentation; cite exact versions/links in report | Feasible commands, dependency ownership and storage choices | Passed — [IP1 report](../verification/us-02-ip1.md); design completeness only, runtime checks deferred as planned |
| Documentation consistency | Local-link inspection and `git diff --check` | Valid links, consistent contracts; no executable behavior changed | Passed — [IP1 report](../verification/us-02-ip1.md); design completeness only, runtime checks deferred as planned |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; concrete contracts, public test boundaries, dependency choices and bounded architecture decisions reviewed. TDD is inapplicable to documentation-only design work.
- **Evidence presented:** [IP1 report](../verification/us-02-ip1.md), including concrete T1–T4 contracts, refined component paths/test cases, sources and limitations; bounded ADR proposals recorded. Technical work complete; gate approved.
- **Remaining limitations or blocked work:** All executable initialization remains unavailable.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve ip1; commit changes and I authorize ip2”, 2026-10-30.
- **Requested changes and resolution:** None.
- **Progression authorized:** IP2 explicitly authorized by the developer; stop at its gate before IP3.

## US-02 / Implementation Phase 2: Deliver conflict-safe installed scaffolding

- **Outcome:** Public CLI/API creates the agreed files safely from packaged resources and exposes explicit setup choices.
- **Entry conditions:** IP1 approved; refined interfaces, schemas, failure matrix and tests confirmed.
- **Acceptance criteria advanced:** AC-01, AC-02, AC-05; environment/storage completion follows.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-02-IP2-T1 | Complete | Add one failing installed CLI scaffold test in `tests/integration/test_initialization.py` (proposed), then minimal public API/CLI dispatch and installed resource loading in `src/agentic_ml/initialization/` and `src/agentic_ml/cli/__init__.py`. Add templates and minimal schema/model paths settled in IP1. | IP1 gate | New files include brief, search/execution inputs, valid output-free notebooks and importable project scaffold; version CLI regression passes. Phase evidence states dependency/storage setup is not yet complete. | AC-01 |
| US-02-IP2-T2 | Complete | Add separate red–green slices for file collisions, safe shared metadata edits, preserved custom files/pin, compatible reruns, invalid roots and path/symlink cases from IP1. Implement only required behavior. | T1 | Hash comparisons establish preservation; conflicts have useful nonzero diagnostics and agreed no-write behavior; reruns cannot silently reset files/state. | AC-02 |
| US-02-IP2-T3 | Complete | Add separate CLI/API tests for explicit root from unrelated cwd and unset data/agent/approval setup; implement agreed configuration defaults and input rejection. Extend resource probes in `tests/packaging/check_installed.py` as needed. | T1, T2 | Same public CLI/API outcomes; no raw-data reads, credentials, login, approvals or execution generated; development instructions not copied/loaded as runtime guidance. | AC-01, AC-02, AC-05 |
| US-02-IP2-T4 | Complete | Record red/green and shared checks in `docs/verification/us-02-ip2.md` (proposed); update plan/checkpoint. | T1–T3 | Required checks pass; intermediate limitations and AC coverage clearly recorded. | AC-01, AC-02, AC-05 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Scaffold/conflict/API cases | One focused failing behavior test, minimal implementation, rerun and relevant regressions; installed fixtures outside checkout | Original failure reproduced, then expected files/errors and preserved hashes | Passed — [IP2 evidence](../verification/us-02-ip2.md), 56 tests and both distribution paths; red/green and limitations recorded |
| Development checks | Shared command set below | All pass; no unexplained lock changes | Passed — [IP2 evidence](../verification/us-02-ip2.md), 56 tests and both distribution paths; red/green and limitations recorded |

### Developer approval gate

- **Approval criteria:** T1–T4 complete, red–green evidence and independent installed-interface checks reviewed.
- **Evidence presented:** [IP2 evidence](../verification/us-02-ip2.md); all 56 tests, shared checks and direct/rebuilt wheels passed on macOS/Python 3.12. Technical completion is separate from gate approval.
- **Remaining limitations or blocked work:** Dependency synchronization and storage setup remain IP3/IP4; no full-story acceptance claim. One backup test initially failed fixture setup rather than behavior; corrected without weakening assertions, disclosed in evidence. No Linux/Windows execution or VS Code manual check claimed.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve us-02 ip2”, 2026-10-30.
- **Requested changes and resolution:** None.
- **Progression authorized:** IP2 gate approved; await explicit IP3 execution authorization.

## US-02 / Implementation Phase 3: Synchronize the experiment environment

- **Outcome:** Initializer declares and installs required dependencies without changing the harness pin or unrelated project settings.
- **Entry conditions:** IP2 approved; dependency set and failure protocol from IP1 remain valid.
- **Acceptance criteria advanced:** AC-02, AC-03, AC-05.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-02-IP3-T1 | Complete | Add a real separate-project dependency/lock test, then implement dependency declarations and uv synchronization in initialization modules; update harness `pyproject.toml`/`uv.lock` only for deliberate runtime needs established in IP1. | IP2 gate | Required project dependencies declared, resolved and importable; installed project package import works; full harness SHA/source and unrelated declarations preserved. | AC-02, AC-03 |
| US-02-IP3-T2 | Complete | Add red–green slices for incompatible existing dependencies, uv resolution/sync failure and safe retry. Use deterministic external-tool failure injection plus real resolver conflict fixture; retain diagnostics outside Git. | T1 | Nonzero failures identify stage and preserved/completed changes; no false success, pin upgrades, discarded user settings or hidden lock regeneration. | AC-02, AC-03, AC-05 |
| US-02-IP3-T3 | Complete | Verify locked no-op resync, project-package imports, notebook-library imports and notebook kernel availability in clean installed projects. Extend `tests/packaging/verify_distributions.py` and probes for declared runtime closure; record `docs/verification/us-02-ip3.md` (proposed). | T1, T2 | Exact lock identity stable after normal locked verification; no harness checkout or development dependencies needed. Shared checks pass. | AC-02, AC-03 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Real environment | Installed init, then project `uv sync --locked`, `uv lock --check`, approved import probes and notebook kernel import probe | Required packages and project import usable; harness pin unchanged | Passed — [IP3 evidence](../verification/us-02-ip3.md); commands, outcomes and boundaries recorded |
| Failures and retry | Focused red–green tests, original-file/pin hashes and explicit partial-state observations | Approved failure/retry contract holds | Passed — [IP3 evidence](../verification/us-02-ip3.md); commands, outcomes and boundaries recorded |
| Development/package checks | Shared commands and both distribution paths below | Pass with intentional runtime dependency changes documented | Passed — [IP3 evidence](../verification/us-02-ip3.md); commands, outcomes and boundaries recorded |

### Developer approval gate

- **Approval criteria:** T1–T3 complete, pin preservation and real environment plus failure evidence reviewed.
- **Evidence presented:** [IP3 report](../verification/us-02-ip3.md): 62-test full suite, final focused environment-path checks, shared development checks and both fresh wheel paths passed; deliberate runtime/lock changes and retained failure evidence recorded.
- **Remaining limitations or blocked work:** Storage integration and final complete init acceptance remain IP4.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve ip3”, 2026-10-31.
- **Requested changes and resolution:** None.
- **Progression authorized:** IP3 gate approved; await separate IP4 execution authorization.

## US-02 / Implementation Phase 4: Initialize storage and verify the complete user path

Execution authorized by developer message “go ahead with ip4” (2026-10-31).
IP3 approval and commit `0830888` verified. Issue #9 refreshed with complete
body/all comment pages and stable zero-comment snapshot; no scope change.
Execution evidence: [IP4 report](../verification/us-02-ip4.md).

- **Outcome:** Complete safe initialization with usable configurable storage, documented setup choices, and criterion-mapped installed-package evidence.
- **Entry conditions:** IP3 approved; IP1 storage/authority decisions remain applicable.
- **Acceptance criteria advanced:** AC-01–05, final integrated verification.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-02-IP4-T1 | Complete | Add separate failing tests and minimal implementations for DVC initialization/configuration, MLflow backend/artifact setup and durable initial state in initialization modules. Exercise public storage interfaces from installed projects. | IP3 gate | Defaults create usable local stores; initial durable state can be reopened and grants no approval; existing DVC/MLflow/state content preserved. | AC-02, AC-04, AC-05 |
| US-02-IP4-T2 | Complete | Add red–green slices for explicit storage locations (including local paths outside project), root-relative paths, pre-existing stores, invalid/credential-bearing settings, permission errors and interrupted storage setup/retry. | T1 | Explicit setup writes restricted to selected destinations; no unrelated stores changed; diagnostics and recoverable evidence preserved; secrets excluded from tracked config/output. | AC-02, AC-04, AC-05 |
| US-02-IP4-T3 | Complete | Extend/create `tests/installation/verify_initialization.py` (proposed) and integration tests; cover fresh and existing pinned projects through complete CLI/API init with both wheel paths. Update `tests/packaging/check_installed.py` and integration coverage without removing original version/resource checks. | T1, T2 | Real CLI/API, complete inventory, notebook validity, project import, locks, stores, preservation and no implicit authorization independently verified outside checkout. | AC-01–05 |
| US-02-IP4-T4 | Complete | Update `docs/experiment-setup.md`, `docs/development.md`, README links and relevant CI/probe invocation only as needed. Record `docs/verification/us-02-ip4.md` (proposed), final matrix, plan/checkpoint. | T3 | Reproducible setup/default/override/conflict/failure guidance; no claims that unresolved inputs or initialization authorize execution. Full checks and both wheel paths pass. | AC-01–05 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Storage defaults/overrides/errors | Focused red–green public-interface cases and real DVC/MLflow/state probes | Usable/reopenable setup; independent paths and existing content preserved | Passed — real public storage probes, focused red–green cases and clean 85-test suite; [IP4 evidence](../verification/us-02-ip4.md) |
| Full installed user path | New verification driver from separate fresh/existing projects, direct wheel and sdist-rebuilt wheel | Every criterion supported; declared dependencies only; no maintained checkout | Passed — both normal wheel paths plus four matching pinned-Git CLI/API projects and byte identity checks; [IP4 evidence](../verification/us-02-ip4.md) |
| Setup authority and Git boundary | Inspect generated files and `git status`/ignore behavior with sentinel data, secret and store fixtures | Track source/config/lock/DVC metadata; exclude data, credentials and generated stores; no execution/approval records created | Passed — unreadable raw-data sentinel, empty grants/runs, preserved source/pin and Git exclusions; [IP4 evidence](../verification/us-02-ip4.md) |
| Manual VS Code notebook check | Open a small notebook, select project `.venv`, execute cells and inspect `sys.executable`; record VS Code/extension versions | Interpreter belongs to project environment; no separate notebook editor package required | Passed — developer executed project .venv Python 3.12.15; VS Code 1.135.0, Python 2026.10.0, Jupyter 2025.9.1; [IP4 evidence](../verification/us-02-ip4.md) |
| Full regression/package checks | Commands below and criterion matrix review | All pass with actual versions/platforms and limitations recorded | Passed — 85/85 clean suite, shared checks and direct/rebuilt wheels; original UTF-8 probe failure and byte-scan correction preserved in [IP4 evidence](../verification/us-02-ip4.md) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; AC-01–05 evidence, failure cases and limitations reviewed.
- **Evidence presented:** [IP4 report](../verification/us-02-ip4.md), criterion matrix, 85/85 clean full suite, both wheel paths and developer manual VS Code execution. T1–T4 technically complete; gate approved.
- **Remaining limitations or blocked work:** No current blocker. Verified on macOS/Python 3.12 only; no new Linux/Windows evidence. Later semantic validation, execution/isolation, tracking runs, dataset restoration and adapters remain outside this story. Original binary-probe failure was corrected without changing product behavior or excluding files; clean rerun passed.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve ip4”, 2026-10-31.
- **Requested changes and resolution:** None.
- **Progression authorized:** IP4 gate approved; await separate explicit whole-story acceptance. Local commit authorized by developer message “commit changes” (2026-10-31); push, publication and next-story implementation remain unauthorized.


## Shared verification and execution rules

Use [development commands and conventions](../development.md). For each executable implementation phase, record focused red/green commands/results and run `uv sync --locked --group dev`, `uv lock --check`, `uv run --locked pytest`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy src tests`, and `uv run --locked agentic-ml --version`. Record deliberate dependency/lock changes separately; checks must never silently rewrite the lock. Compare its SHA-256 before/after verification. Run `git diff --check`.

For distribution-affecting changes, use `uv build --out-dir FRESH_DIRECTORY` and `uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir FRESH_DIRECTORY`; test both the direct wheel and wheel rebuilt from the sdist. Refine the new initialization driver's command in IP1 before implementation; the proposed path is not an existing runnable check. Real pinned Git fixtures may use an isolated local committed harness repository for unpublished implementation, recording the exact full SHA and distinguishing this from live GitHub installation. Reuse US-01's live GitHub installation evidence; do not claim unpublished changes were fetched from GitHub.

Record OS, Python/uv/Git and library versions, commands, actual outcomes, artifact identities, raw diagnostic paths, limitations and AC IDs in each report. Use small temporary fixtures/storage outside Git. macOS is the local baseline; hosted Linux evidence must be observed separately, and Windows/additional Python versions remain unverified unless actually tested.

Work in small vertical TDD slices: one behavior-focused failing test, confirm the intended missing behavior, minimal implementation, rerun and relevant regressions, then next behavior. Do not batch all tests before implementation. Documentation-only work uses appropriate checks without manufactured red tests. Review refactoring after green.

Mark tasks Complete only after required verification passes and evidence is linked. Preserve incomplete/failed/blocked status and reopen invalidated evidence. At every implementation phase boundary update this plan and CHECKPOINTS.md, present outcomes/deviations/limitations, and stop for explicit developer approval. Plan approval, tool permission and silence do not approve gates. Record decisions with date and message reference. Maintain the three-attempt limit and original assertions under [AGENTS.md](../../AGENTS.md); after three unsuccessful corrective attempts stop and present hypotheses, changes, original failure, logs, tree state and next-step options.

Pause affected work for scope changes and use manage-plan-scope; new prerequisite-story implementation requires an approved scope revision and coordinated plans/index. Routine choices within approved scope can proceed. No implementation, dependency installation, publication or acceptance is authorized by drafting this plan.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| [US-02-AC-01](../specs/user-stories.md#us-02-ac-01): configuration, inputs, notebooks and scaffolding | IP1-T1/T2; IP2-T1/T3/T4; IP4-T3/T4 | [IP2](../verification/us-02-ip2.md), [IP4](../verification/us-02-ip4.md): complete installed inventory, notebooks, package import and CLI/API | Verified on macOS; accepted 2026-10-31 |
| [US-02-AC-02](../specs/user-stories.md#us-02-ac-02): preserve files and pin; report conflicts | IP1-T1/T2/T3; IP2-T2/T3/T4; IP3-T1/T2/T3; IP4-T1/T2/T3/T4 | [IP2](../verification/us-02-ip2.md), [IP3](../verification/us-02-ip3.md), [IP4](../verification/us-02-ip4.md): pin/lock/file preservation, conflicts, interrupted setup and reruns | Verified on macOS; accepted 2026-10-31 |
| [US-02-AC-03](../specs/user-stories.md#us-02-ac-03): declared and synchronized dependencies | IP1-T3; IP3-T1/T2/T3; IP4-T3/T4 | [IP3](../verification/us-02-ip3.md), [IP4](../verification/us-02-ip4.md): declarations, synchronization/imports, lock checks and developer project-kernel execution | Verified on macOS; accepted 2026-10-31 |
| [US-02-AC-04](../specs/user-stories.md#us-02-ac-04): configurable DVC/MLflow/state | IP1-T4; IP4-T1/T2/T3/T4 | [IP4](../verification/us-02-ip4.md): real DVC/cache, MLflow/artifacts and durable state, defaults/overrides and failure cases | Verified on macOS; accepted 2026-10-31 |
| [US-02-AC-05](../specs/user-stories.md#us-02-ac-05): explicit setup; no grants or committed credentials | IP1-T2/T4; IP2-T3/T4; IP3-T2; IP4-T1/T2/T3/T4 | [IP2](../verification/us-02-ip2.md), [IP4](../verification/us-02-ip4.md): explicit unconfigured choices, empty approvals/runs, credential/data/store boundaries | Verified on macOS; accepted 2026-10-31 |

- **Remaining work:** All implementation phases and corrections approved. US-02 accepted and published in PR #45. Post-acceptance static review identified one additional metadata temporary-path conflict; follow-up correction requires authorization before merge.
- **Partial prerequisite delivery:** None newly included. Accepted US-01 reused; downstream stories remain outside scope.
- **Developer acceptance:** Accepted.
- **Decision reference and date:** Developer message “i accept us-02”, 2026-10-31.


## IP2 completion record — 2026-10-30

T1–T4 technically complete; [evidence](../verification/us-02-ip2.md) records actual commands, red–green slices, corrective attempts, boundary coverage and limitations. Public CLI/API and packaged templates/schemas implemented; intermediate results explicitly report environment/storage pending. Parser/schema runtime dependencies and dev stubs deliberately added; harness lock identity changed and remained stable through verification. Existing installation/distribution probes now assert the exact required runtime closure rather than the superseded zero-dependency baseline. Complete original corruption checks retained. No IP3 synchronization or IP4 storage behavior delivered. IP2 gate and whole-story acceptance remain pending; no publication authorized.

Developer subsequently requested “commit changes”, authorizing the local IP2 commit. This does not approve the IP2 gate or authorize IP3; those decisions remain pending.

IP2 gate approved by developer message “i approve us-02 ip2” (2026-10-30). Implementation commit: `265ed5b`. IP3 execution and whole-story acceptance remain pending.


## IP3 execution authorization — 2026-10-31

Developer message “Execute US-02 IP3.” authorizes IP3 T1–T3 only, reusing IP1-approved public CLI/API, uv and installed-package test boundaries. IP2 approval verified against its completion record. Issue #9 body and all comment pages refreshed: stable zero-comment snapshot, updated 2026-10-31T01:15:38Z; Milestone 1 in body (no GitHub milestone assigned), AC-02/03/05 apply. No new scope decision. IP4, acceptance, commit and publication remain unauthorized.

IP3 technically complete; [IP3 evidence](../verification/us-02-ip3.md) records implementation, TDD, corrective attempts and verification. First behavior red: `uv run --locked pytest tests/integration/test_initialization.py -k synchronizes_required -q` failed because all eight required experiment declarations were missing. Runtime dependency lock deliberately expanded per approved IP1 table. False-success red: `... -k sync_success_requires -q` failed because init accepted a tool that installed no project package; separate-interpreter import verification added. Real impossible `numpy<2` / required `numpy>=2,<3` fixture verifies preserved bounds and failed lock. Existing IP2 assertions for an unchanged initial lock, scaffold-only journal and pending environment are superseded by IP3 synchronization obligations; original backup/pin, rerun stability and corruption checks retained. Verification complete as recorded in the IP3 report; gate subsequently approved by “i approve ip3” (2026-10-31).


## IP3 completion record — 2026-10-31

T1–T3 complete under “Execute US-02 IP3.” Required declarations, real uv resolution/locked inexact synchronization, pin preservation, separate-interpreter imports, safe failure/retry, environment override/symlink boundaries and revised installed runtime closure are verified. [IP3 report](../verification/us-02-ip3.md) records criterion-mapped evidence, red/green commands, supplemental tests, corrected intermediate IP2 expectations, attempts, lock/artifact identities and limitations. Full suite: 62 passed; final path guard: two focused tests passed, covering the added 63rd distinct test and normal synchronization. Shared checks and both final wheel paths passed after the guard. No unresolved failed check, suppression or scope change. Changes remain uncommitted on `US-02-experiment-init`. Developer approved IP3 with “i approve ip3” (2026-10-31); await separate IP4 execution authorization. Story acceptance, commit, push and publication remain unauthorized.


IP3 approval recorded on 2026-10-31 from developer message “i approve ip3”. This approval does not authorize a commit, IP4 execution, story acceptance or publication. Documentation-only approval record: `git diff --check` passed; no runtime behavior changed and no runtime rerun required.


Developer message “commit” (2026-10-31) subsequently authorizes the local commit of approved IP3 implementation and approval records, including this plan update. IP4 execution, story acceptance and publication remain unauthorized.


## IP4 completion record — 2026-10-31

Executed only IP4 under “go ahead with ip4”. T1–T4 technically complete:
configurable local DVC/cache/remote, MLflow SQLite/artifacts/experiment and durable
unconfigured state; preservation/preflight/retry controls; artifact-derived
installed CLI/API verification and setup documentation. [IP4 report](../verification/us-02-ip4.md)
maps all five criteria and preserves commands, failed probes, corrective evidence,
versions, artifacts and platform limitations.

Original full suite: 84 passed, one legacy UTF-8 scan failed on the new binary
SQLite database. The same recursive source-exclusion assertion was corrected to
scan bytes; focused verification passed. Clean full rerun with optional telemetry
disabled: **85 passed**, exit 0. Shared checks and both review wheel paths passed;
developer manual VS Code project-kernel execution verified. No dependency/lock
change, suppression, disabled test or unresolved failure. All changes remain
uncommitted. Stop at the final phase gate; whole-story acceptance and publication
remain separate developer decisions.


IP4 gate approved by developer message “i approve ip4” (2026-10-31). This is phase approval only; US-02 whole-story acceptance, commit, push and publication remain pending. Approval-record changes are documentation-only; `git diff --check` passed, and no runtime rerun is required.


Developer message “commit changes” (2026-10-31) authorizes the local IP4 commit only. Whole-story acceptance and publication remain pending. Subsequent review identified pending backup symlink/content-conflict validation (P1) and storage overlap with initialization metadata (P2); this commit preserves the reviewed implementation without resolving those findings. Earlier verification evidence does not cover those defects.


## IP4 review corrections — 2026-10-31

Authorized by developer “resolve these findings”. This is corrective work within
issue #9 / Milestone 1 / AC-02, AC-04 and AC-05, not a scope change. Reuse the
approved installed CLI/API boundaries: observe errors, original bytes and absent
scaffold/journal/lock writes in separate pinned projects. These tests do not
establish protection against concurrent hostile filesystem mutation.

- P1: Reject backup-directory symlinks/non-directories and backup file symlinks,
  non-files or conflicting bytes before durable writes; preserve matching backups.
- P2: Reject storage paths equal to, above or below journal, lock and backup paths.
- Work in separate red–green slices, retain original assertions and record evidence
  in `docs/verification/us-02-review-fixes.md`. Run shared checks and both installed
  distribution paths. Renewed IP4 correction review is approved; historical
  approval is preserved. No commit, publication or whole-story acceptance implied.

Correction status: P1/P2 implemented; 34 new installed-interface cases passed
(5 backup rejection, 28 storage overlap, 1 API rejection/corrected CLI retry).
Shared checks passed; full suite **119 passed**, exit 0 (1898.17s), including
both distribution paths. IP4-T2/T4 correction verification is complete; evidence
is in [the correction report](../verification/us-02-review-fixes.md).

Renewed correction gate: **Approved** by developer message “i approve”,
2026-10-31, in response to the correction-review request. Both review findings are
resolved and verification is complete; historical IP4 approval remains preserved.
Whole-story acceptance, commit, push and publication remain separate and pending.

Approval-record updates are documentation-only; `git diff --check` passed. The
119-test verification remains applicable; no executable changes followed it.


## Whole-story acceptance — 2026-10-31

Developer message “i accept us-02” accepts AC-01–05 after all four phase gates
and the IP4 correction gate were approved. Final full verification: 119 passed;
shared checks and both installed distribution paths passed. No executable edits
after verification. Scope limitations remain as documented in the IP4 and
[correction evidence](../verification/us-02-review-fixes.md).

The execute-plan accepted-story workflow authorizes remaining local commits,
ordinary push, PR creation and a static COMMENT review. Publication is in
progress; merge, cleanup and another story remain outside this authorization.
Acceptance-record edits are documentation-only; no runtime rerun required.


## Publication and static review — 2026-10-31

- Accepted corrections and acceptance records committed as `8fe0e8f`; ordinary
  push of `US-02-experiment-init` succeeded.
- [PR #45](https://github.com/jimthompson5802/agentic-ml/pull/45) targets `main`
  (`4477162aa688636dcbea8f0493a5793dfc8e878b`) and closes issue #9 on merge.
- [Static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/45#pullrequestreview-5722316537) published and verified against
  `8fe0e8f44e6e0cbb24625f98982018a77a212ec9`; one
  [Medium finding](https://github.com/jimthompson5802/agentic-ml/pull/45#discussion_r4431369976) remains unresolved: storage can target
  `.agentic-ml/init.tmp`, conflicting with the journal's atomic-write temporary
  file after setup has already modified the project. This is a newly identified
  AC-02/04 gap; original P1/P2 corrections and developer acceptance remain
  historical facts. The existing 119-test suite does not cover this path.
- Review was static only; no project code/checks were executed during review.
  Published thread location/body/commit and unresolved state were verified.
- Hosted Linux [CI run](https://github.com/jimthompson5802/agentic-ml/actions/runs/41192049523)
  was pending at observation. No new platform result is claimed.
- This publication-record update is documentation-only. A head review refresh
  accompanies publication of these records; the product finding remains in its
  original inline thread without duplication.
- Next action: developer direction for the new finding. Acceptance authorized
  publication, not automatic review fixes, merge, cleanup or another story.
