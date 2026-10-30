# Milestone 0 / US-33: Build and verify the harness package

## Scope and outcome

- **Milestone:** 0 — Establish the harness development foundation.
- **User story:** [US-33 / issue #3](https://github.com/jimthompson5802/agentic-ml/issues/3).
- **User-visible outcome:** Both distributable wheel paths install and expose the version CLI, public import, and provisional resources from a clean separate project outside the harness checkout.
- **Acceptance criteria covered:** US-33-AC-01–07 in full; approved IP1 preserves its source-install subset evidence.
- **Scope boundaries:** IP1 delivered the minimal CLI prerequisite. Proposed IP2–IP3 add wheel/sdist builds, clean installed checks, provisional resources and CI. Exclude usable initialization, experiment commands, guidance selection/loading, registry publication, pinned GitHub experiment installation, and Milestone 99.
- **Supporting design:** [contributor contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization), [traceability](../specs/design/acceptance-traceability.md), [delivery order](../specs/design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order).
- **Coordinated execution index:** [US-33 execution order](milestone-0-us-33-execution-order.md); [historical US-31 coordination](milestone-0-execution-order.md).

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-31 foundation | US-31-IP1-T1–T3 with approved IP1 gate; locked tools and metadata | All tasks below | [Owning plan](milestone-0-us-31.md#developer-approval-gate); T1–T3 complete with [evidence](../verification/us-31-ip1.md), gate approved 2026-10-29 |
| Package choices | `agentic-ml`, `agentic_ml`, `agentic-ml`; Hatchling, version `0.1.0`, argparse, no third-party runtime dependencies | CLI configuration | Distribution name developer-approved 2026-10-29; remaining implementation choices proposed in US-31 plan |
| Requirements snapshot | Full #3 body and zero comments; repeated metadata unchanged | Planning | Retrieved 2026-10-29; see [US-31 source findings](milestone-0-us-31.md#findings-and-source-reconciliation) |

## Technical approach and public boundaries

Proposed files: `src/agentic_ml/__init__.py`, `src/agentic_ml/cli/__init__.py`, `tests/integration/test_cli_version.py`; extend shared `pyproject.toml` with `agentic-ml` entrypoint. The proposed CLI callable uses argparse and `importlib.metadata.version("agentic-ml")`; metadata is the single version source. Do not add experiment commands or fallback hardcoded versions that conceal missing installation.

Plan review must confirm subprocess CLI tests with independent expectations from installed metadata: zero exit, version stdout, and importability. These source-install tests do not verify wheel contents, runtime resource loading, sdist completeness, clean runtime dependency isolation, or CI. Follow TDD in small vertical slices: one failing behavior test, confirm missing behavior is the cause, implement minimally, rerun relevant tests, then add the next behavior. Record red/green commands and results. Tests must use public commands and imports, not mocked CLI internals.

## Execution rules

Mark tasks Complete only after required work and checks pass; record commands, actual results, and evidence. Keep partial, failed, blocked, and unverified tasks incomplete. Reopen tasks when later changes invalidate evidence. Follow the [execution index](milestone-0-execution-order.md); verify supplying tasks and gate decisions before dependent work.

Stop at every implementation phase boundary, including the final one. Present tasks, results, evidence paths, deviations, and limitations; await explicit developer approval and record its date and reference. Plan approval does not approve implementation gates. Silence is not approval.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes; pause affected work, revise owning plans and the index together, and obtain approval before implementing newly discovered prerequisite scope. Follow the [three-attempt limit](../../AGENTS.md#problem-solving-attempt-limit): record hypothesis, change, and original-failure verification for each corrective attempt; after three failures preserve diagnostics and stop for direction. Never weaken acceptance assertions or suppress failures.

Record evidence in proposed `docs/verification/` Markdown reports; keep temporary environments, logs containing sensitive data, and generated storage outside Git. Update [CHECKPOINTS.md](../../CHECKPOINTS.md) at gates, blockers, and handoff.

## Plan review

- **Current revision:** Approved — full-story extension SC-02, IP2–IP3, technical choices and public test boundaries approved by developer message “i approve the plan”, 2026-10-29. Historical IP1 approval remains valid. IP2 execution authorized 2026-10-29; technical tasks complete and IP2 approved 2026-10-29. IP3 execution authorized by developer message “execute plan for us-33 ip3”, 2026-10-29; T1–T4 technically complete; hosted evidence recorded; final IP3 approval and story acceptance pending.
- **Status:** Approved for the full plan; original IP1 decisions below remain historical.
- **Developer decision:** Approved — coordinated scope, proposed tooling choices, and public test boundaries.
- **Decision reference and date:** Developer message “i approve the plan” in this conversation, 2026-10-29. US-33 IP1 progression authorized by developer message “i approve” at the US-31 IP1 gate, 2026-10-29. US-33 IP1 gate subsequently approved as recorded below.
- **Requested plan changes:** Complete remaining US-33 planning, developer request “create plan for us-33”, 2026-10-29.

## Scope-change history

- **Change ID and date:** SC-01, 2026-10-29.
- **Request and reason:** Developer explicitly requested correction of ADR-007 and generated code/documents: CLI should be `agentic-ml` for consistent package naming.
- **Scope difference:** Replace the CLI name `agent-ml` with `agentic-ml`; distribution `agentic-ml` and import `agentic_ml` stay as selected. No legacy alias or additional experiment command is added.
- **Impact:** US-31 CLI/smoke expectations (AC-03,05,07) and US-33 CLI/import/version expectations (AC-03,06,07) require renewed evidence; stable task and criterion IDs retained. US-33-IP1-T2–T3 were reopened and are complete again after renamed command checks passed; see correction evidence. US-31 IP1 approval remains historical; its tooling checks remain valid, while renamed guidance is reviewed in this correction. No milestone or prerequisite changes.
- **Plan and requirement revisions:** ADR-007, current user stories, harness design/examples, README, contributor guide, repository instructions, both story plans, and execution index. GitHub issue bodies still contain the old spelling; this explicit developer direction overrides that spelling for implementation. Historical reports retain original results and link the correction evidence.
- **Verification and gates:** Rename the public CLI regression first and confirm failure for the absent required command, then correct entrypoint and verify version/import/help plus all shared checks and lock immutability. US-33 IP1 gate stays pending; US-31 IP2 does not start.
- **Decision:** Approved — developer instruction requesting this correction in this conversation, 2026-10-29, authorizes the scope revision and implementation without another approval cycle.
- **Resume point:** Correct and reverify US-33 IP1 within its existing gate; see [CLI correction evidence](../verification/cli-name-correction.md).


## US-33 / Implementation Phase 1: Provide the minimal source-installed version CLI

- **Outcome:** Version CLI and public import work from the locked contributor environment.
- **Entry conditions:** Coordinated plan/boundaries approved and implementation authorized; US-31 IP1 gate approved.
- **Acceptance criteria advanced:** US-33-AC-03, 06–07; source-install subset only.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-33-IP1-T1 | Complete | Add first behavior test in proposed `tests/integration/test_cli_version.py` for CLI exit and version; create package skeleton only as needed for installation/test discovery. | US-31 IP1 approved | A real subprocess fails because version entrypoint/behavior is absent, rather than dependency/setup failure; preserve red output. | US-33-AC-06 |
| US-33-IP1-T2 | Complete | Implement proposed `src/agentic_ml/cli/__init__.py`, package init and `[project.scripts]` in `pyproject.toml`; sync locked environment. | T1 | `agentic-ml --version` exits zero and reports installed distribution version; first regression test and relevant checks pass. Resolve legitimate metadata/lock changes explicitly, never through verification's silent update. | US-33-AC-06 |
| US-33-IP1-T3 | Complete | Add next public import behavior test red–green if missing; run shared checks, record source version/import evidence in proposed `docs/verification/us-33-ip1.md`; update owning plans/checkpoint. | T2 | Tests/lint/format/types and source smoke pass; independently checked metadata version and import result; no wheel/resource claims. | US-33-AC-03, 06–07 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| TDD | `uv run --locked pytest tests/integration/test_cli_version.py` per slice | Red missing behavior followed by green; import test added only after first slice green | Passed; [TDD sequence](../verification/us-33-ip1.md#tdd-sequence) |
| CLI and metadata | `uv run --locked agentic-ml --version`; subprocess test compares stdout version with metadata | Zero exit, expected installed version, import succeeds | Passed after SC-01; version 0.1.0, public import and renamed help; [renewed evidence](../verification/cli-name-correction.md) |
| Regression/tooling | Shared US-31 test, lint, format and type commands | All pass; lock remains consistent and unchanged during checks | Passed after SC-01; 3 tests, lint, format, types, smoke and lock consistency; [renewed evidence](../verification/cli-name-correction.md) |

### Developer approval gate

- **Approval criteria:** T1–T3 complete with red/green and shared-check evidence reviewed.
- **Evidence presented:** [US-33 IP1 evidence](../verification/us-33-ip1.md); T1–T3 technically complete. SC-01 correction reverified in [renewed evidence](../verification/cli-name-correction.md). Developer gate approved.
- **Remaining limitations or blocked work:** No wheel/sdist/resource/CI verification; US-33 remains incomplete.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “I appove us-33 ip1; commit changes” in this conversation, 2026-10-29.
- **Requested changes and resolution:** None.
- **Progression authorized:** Prerequisite gate satisfied for US-31 IP2. Current request is to record approval and commit; US-31 IP2 remains unstarted pending execution instruction.

## Findings and source reconciliation for the remaining work

Retrieved the complete body and all comment pages for issue #3 on 2026-10-29. Repeated metadata is stable: open, updated `2026-10-29T23:10:06Z`, one unique comment, milestone metadata unset; the body specifies Milestone 0. The sole [comment](https://github.com/jimthompson5802/agentic-ml/issues/3#issuecomment-6510671946), by jimthompson5802, created/updated at that same time, states “PR #4 prematurely closed this issue, reopening.” Full bodies and all comment pages for prerequisite issues #1 and #2 were also retrieved: both closed, zero comments, stable update times `2026-10-29T23:03:10Z` and `2026-10-29T23:56:06Z`, respectively. No new prerequisite implementation is needed.

Issue #3's old `agent-ml` spelling is superseded by approved SC-01, repository instructions and ADR-007: use `agentic-ml`. ADR-007's older pending distribution-name wording and overview references to macOS CI are historical; approved plans settle distribution `agentic-ml`, import `agentic_ml`, and Ubuntu CI. Do not reopen these decisions. The issue and current local criteria otherwise agree.

Inspected `pyproject.toml`, `uv.lock`, existing source, three subprocess tests, contributor commands, workflow and owning evidence. Hatchling, version 0.1.0, argparse, and no third-party runtime dependencies exist. There are no packaged template/guidance resources or distribution-verification scripts/tests. Existing tests use the contributor environment and cannot establish wheel isolation. Existing CI verifies Linux/Python 3.12 development checks only. `gh auth status` reported an invalid default token, while required API reads succeeded; one metadata recheck encountered a network error and succeeded on an escalated retry. Hosted publication/run permissions remain an execution prerequisite. Pre-existing edits to CHECKPOINTS.md are preserved.

### SC-02 — Complete US-33 planning (2026-10-29)

- **Request and reason:** Developer request “create plan for us-33”; plan the remaining issue-defined Milestone 0 outcomes.
- **Scope difference:** Extend the IP1-only plan with IP2 local distribution/resource verification and IP3 CI integration. No acceptance criteria or product scope changed.
- **Impact:** Preserve IP1 task IDs, evidence and approval. Add US-33-owned tasks only; reuse accepted US-31/US-32 capabilities through the new execution index. No prior evidence is invalidated; new distribution evidence is required.
- **Plan revisions:** This plan, new US-33 execution index, historical index cross-link and checkpoint. Authoritative requirements need no revision.
- **Verification and gates:** Plan review confirms the public boundaries below; IP2 and IP3 each have a separate pending implementation gate. All new checks are planned, not executed.
- **Decision:** Approved — developer message “i approve the plan”, 2026-10-29, approves SC-02, IP2–IP3, technical choices, public test boundaries and coordinated execution index. No implementation gate approval or publication authorization is implied.
- **Resume point:** IP2 execution authorized by developer message “execute plan for us-33 ip2”, 2026-10-29. IP2 tasks complete and approved 2026-10-29; IP3 execution authorized 2026-10-29; publication authorized and hosted checks complete; final gate pending.

## Remaining dependencies and technical approach

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-31 tooling and contributor commands | IP1-T1–T3 and IP2-T1–T3, accepted gates | IP2 | [Plan](milestone-0-us-31.md), [fresh macOS evidence](../verification/us-31-ip2.md); complete and accepted |
| US-33 version CLI | IP1-T1–T3 and approved gate | IP2 | Approved above; retain existing CLI behavior and version |
| US-32 workflow | IP1-T1–T3 and IP2-T1–T4, approved gates | IP3 | [Plan](milestone-0-us-32.md), [hosted evidence](../verification/us-32-ip2.md); complete and accepted |
| Runtime resource layout | Proposed package-local files below, read with standard-library resources API | IP2 resource tests | Proposed implementation choice for plan review; illustrative top-level design directories do not mandate physical placement |
| Hosted access | Actions and branch/PR publication permission, reviewed revision available remotely | Hosted IP3 evidence | Recheck during execution; this planning request authorizes no publication or merge |

Propose `src/agentic_ml/templates/provisional.txt` and `src/agentic_ml/runtime_guidance/provisional.md`. Exact UTF-8 contents, including final newline, are respectively `Provisional Milestone 0 template; experiment initialization is unavailable.\n` and `Provisional Milestone 0 runtime guidance; experiment execution is unavailable.\n`. Tests define these expected literals independently; never obtain expected values by reading source resources. Access via `importlib.resources.files("agentic_ml").joinpath(...)`. Do not create a guidance loader or new Python resource API. Package-local resources are reusable product assets; verification helpers remain development tooling. No development AGENTS.md becomes a runtime resource, and provisional text provides no experiment-use instructions.

Propose `tests/packaging/check_installed.py` as a standard-library-only probe and `tests/packaging/verify_distributions.py` as the command-line verification driver. Running a probe by absolute file path is acceptable; it must import product code only from the installed environment. Extend mypy coverage by keeping helpers under `tests`; pytest need not rebuild artifacts on every ordinary source test run. Add focused public-command tests in proposed `tests/integration/test_distribution_verification.py` where necessary for driver failure behavior. Exact helper names are proposed, not existing APIs.

Proposed local commands after implementation:

```sh
uv build --out-dir dist
uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir dist
```

The driver accepts a fresh artifact directory with exactly one direct wheel and one sdist, creates unique temporary directories outside the checkout, unpacks the sdist safely into a distinct source directory, and uses `uv build --wheel` on that extracted source to produce the second wheel. It must never rebuild from the original checkout or reuse the direct wheel as the rebuilt result. Resolve exact uv options using installed CLI help before implementation; document any refined commands. Keep build isolation and build requirements separate from runtime test environments. Do not add a runtime dependency for development verification. Any deliberate dependency change must update/review the lock explicitly before checks.

For each wheel independently, create a new Python 3.12 environment without inherited site packages, install that wheel normally with its declared dependencies through uv, then execute its absolute `agentic-ml` entrypoint and isolated Python probe from a separate minimal experiment-project directory. Clear PYTHONPATH/PYTHONHOME, avoid editable installs, and do not use `uv run` to resynchronize the runtime environment. Assert imported package and metadata locations belong to that environment, installed distributions match harness plus declared runtime dependency closure (currently just harness), and no editable harness metadata or checkout source path is used. Do not install pytest, Ruff, mypy, Hatchling or the development dependency group into these runtime environments. Build tools may exist in a separate build environment.

The probe checks CLI exit zero, stdout equal to installed metadata version and artifact metadata version, empty stderr, public import, and exact contents of both resources. Capture artifact identities/checksums, commands, cwd, interpreter/site paths, installed distributions, platform/tool versions and stdout/stderr for each path. Installation, build, missing/corrupt resource, unexpected version, and probe failures must terminate nonzero with the affected stage/artifact identified. Preserve available diagnostics on failure; never report an unrun path as passing.

### Public test boundaries for developer confirmation

- Exercise installed entrypoint, public import, metadata and `importlib.resources` from separate projects. These verify distribution contents and independence from contributor dependencies; they do not verify initialization, guidance loading/selection/restoration, experiment execution, or other Python/platform combinations.
- Exercise the driver as a subprocess using independently constructed malformed artifact fixtures: missing template, altered guidance and wrong CLI version. Test one failure and its correction at a time. Each must fail at the intended installed check; build/setup errors are not substitutes for a behavior red. Fixture defects remain outside production source; keep original assertions intact.
- Use real direct-wheel and rebuilt-sdist-wheel installs rather than internal mocks. Capture separate results for both paths; changing only cwd in the editable environment is insufficient.
- CI evidence uses hosted job conclusions and accessible step logs. Static YAML validation cannot establish hosted behavior. Add no Python tests that merely mirror workflow text.

## US-33 / Implementation Phase 2: Verify both distribution paths locally

- **Outcome:** Reproducible wheel/sdist builds and both clean installed paths pass on local macOS, with provisional resources and actionable failures.
- **Entry conditions:** SC-02 plan/public boundaries reviewed and execution authorized; US-31 and US-33 IP1 gates approved.
- **Acceptance criteria advanced:** US-33-AC-01–04, 06–07; local reproduction portion of AC-05.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-33-IP2-T1 | Complete | Inspect installed uv build/venv/pip help and Hatchling configuration; refine proposed driver commands and isolation checks in this plan. Inspect `pyproject.toml`, `uv.lock`, `.gitignore` and current package contents. | Reviewed plan/boundaries | Concrete command options, artifact selection and safe extraction strategy recorded; no unsupported CLI assumption remains. Re-review if findings change scope or boundaries. | AC-01–04 |
| US-33-IP2-T2 | Complete | Start one direct-wheel resource behavior slice in proposed `tests/packaging/check_installed.py`; build/install existing artifact to demonstrate missing template red. Add proposed template and only necessary `pyproject.toml` packaging changes; rerun green. Then repeat red–green for proposed runtime guidance file. | T1 | Independent exact-content assertions pass through installed resources; each initial failure identifies the missing resource. No development guidance is substituted. | AC-02–03 |
| US-33-IP2-T3 | Complete | Add proposed `tests/packaging/verify_distributions.py`; incrementally add clean environment, CLI/version/import/path checks, then sdist extraction/rebuild and identical second-path probe. Retain existing source CLI tests. | T2 | Both artifact paths run in distinct runtime environments and project directories outside checkout. Wheel metadata/version and resource assertions pass; installed dependencies/path diagnostics demonstrate isolation. | AC-01–04,06–07 |
| US-33-IP2-T4 | Complete | Add public subprocess failure cases in proposed `tests/integration/test_distribution_verification.py` for missing template, altered guidance and wrong CLI version, plus missing/ambiguous artifacts; implement diagnostic/failure behavior one red–green slice at a time. | T3 | Each malformed fixture fails for the intended reason; corrected artifacts pass. Driver does not conceal failure or reuse an earlier passing install. Preserve original acceptance assertions. | AC-02–05,06–07 |
| US-33-IP2-T5 | Complete | Document exact build/verification commands, isolation, resource contents and diagnostics in `docs/development.md`; link from `README.md`. Run fresh macOS artifact checks and shared development checks. Record proposed `docs/verification/us-33-ip2.md`, update plan/index/checkpoint. | T4 | Both wheel paths and documented source smoke pass; all shared checks pass, lock SHA/diff unchanged. Report actual versions/platform, TDD sequence, artifact checksums and limitations. | AC-01–07; AC-05 local portion |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Build and installed checks | Proposed commands above from fresh output directory; rebuild from extracted sdist only | Wheel and sdist built; separate direct/rebuilt wheel probes both pass on Python 3.12/macOS | Passed locally; [IP2 evidence](../verification/us-33-ip2.md) |
| TDD and failure diagnostics | One public behavior red–green per slice; malformed artifact subprocess fixtures | Correct missing/incorrect behavior red, then green; stage-specific nonzero failures and logs | Passed; [IP2 evidence](../verification/us-33-ip2.md) |
| Contributor regression | `uv sync --locked --group dev`, `uv lock --check`, `uv run --locked pytest`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy src tests`, `uv run --locked agentic-ml --version` | All pass; before/after lock SHA-256 and `git diff --exit-code -- uv.lock` unchanged | Passed; [IP2 evidence](../verification/us-33-ip2.md) |

### Developer approval gate

- **Approval criteria:** T1–T5 complete; review both artifact identities, real isolation, exact provisional contents, red/green diagnostics and shared-check results.
- **Evidence presented:** [IP2 evidence](../verification/us-33-ip2.md): T1–T5 complete; both isolated paths pass on macOS/Python 3.12.15; 11 tests and all shared checks pass; lock unchanged.
- **Remaining limitations or blocked work:** Hosted Linux package checks and failure diagnostics remain IP3; Windows/additional Python versions remain unverified.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve us-33 ip2; commit changes”, 2026-10-29.
- **Requested changes and resolution:** None.
- **Progression authorized:** IP2 gate satisfied; approval recording and commit authorized. IP3 awaits separate execution authorization; publication permissions remain separate.

## US-33 / Implementation Phase 3: Run distribution verification in CI

- **Outcome:** Existing Linux CI runs the same build/installed commands and exposes failures and diagnostics for package checks.
- **Entry conditions:** IP2 approved; US-32 workflow/gates accepted; reviewed helpers available for hosted execution.
- **Acceptance criteria advanced:** US-33-AC-05; renew AC-01–04,06–07 on hosted Linux/Python 3.12.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-33-IP3-T1 | Complete | Extend `.github/workflows/ci.yml` with named build and isolated verification steps using IP2 documented commands; keep shared development commands, clean setup, pinned tools/actions and final always-run lock comparison. Update `docs/development.md` diagnostic instructions. | IP2 gate; US-32 approved | Existing PR/main triggers cover package checks; independent diagnostics remain inspectable and original failure exit is preserved. Validate workflow with actionlint and inspect command parity. | AC-01–05,07 |
| US-33-IP3-T2 | Complete | Run shared checks and artifact verification locally; when publication is authorized, publish reviewed revision for hosted PR checks. Record actual OS/image/Python/uv, both artifact paths and immutable revision/run URLs in proposed `docs/verification/us-33-ip3.md`. | T1; hosted access/publication authorization | Passing hosted build and both isolated wheel results on Ubuntu/Python 3.12, with logs accessible from PR. No local-only CI claims. | AC-01–07 |
| US-33-IP3-T3 | Complete | On an authorized disposable branch/PR, demonstrate package build failure and an installed resource mismatch failure separately, then restore exact reviewed source and obtain passing reruns. Preserve stage/job conclusions and logs; close disposable work without merging defects when authorized. | T2; explicit publication authorization | Both failures reach intended stages, fail CI and expose diagnostics; each correction passes. No defect enters production or assertions are weakened. | AC-03,05 |
| US-33-IP3-T4 | Complete | Reconcile all seven criteria, source smoke and macOS/Linux evidence in this plan, proposed IP3 report, `docs/development.md`, index and `CHECKPOINTS.md`; run final required checks after corrections. | T3 | Every criterion has actual evidence, no fabricated platform coverage or pending failed checks; final gate review can explicitly accept US-33. Default-branch package run recorded only after separately authorized merge; if not yet available disclose it as follow-up evidence. | AC-01–07 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Workflow validity and parity | `actionlint .github/workflows/ci.yml` when available; inspect documented commands vs workflow | Valid workflow; same build/probe commands; package failure fails job; lock check still runs | Passed actionlint 1.7.12 and command/control-flow inspection; [IP3 evidence](../verification/us-33-ip3.md). Hosted failure propagation verified in T3. |
| Hosted successful artifacts | PR Actions run, build and verification step logs, actual revision and both wheel checksums | Python 3.12/Linux success for both wheel paths; source smoke retained | Passed; [IP3 evidence](../verification/us-33-ip3.md) |
| Hosted negative cases | Disposable build defect and resource mismatch, followed separately by exact restoration/passing reruns | Intended failure reason, nonzero job result and accessible diagnostics for each | Passed; two separate red/green pairs in [IP3 evidence](../verification/us-33-ip3.md) |
| Final regression | IP2 shared commands, both artifact paths, lock SHA/diff and `git diff --check` | All pass; production source restored; no lock mutation | Passed; final local renewal and exact tree comparison in [IP3 evidence](../verification/us-33-ip3.md) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete, all AC evidence reviewed, success/failure hosted logs accessible, limitations explicit.
- **Evidence presented:** T1–T4 technically complete; [IP3 evidence](../verification/us-33-ip3.md), PR #24 and disposable PR #25 (closed without merge), two red/green pairs and final local renewal.
- **Remaining limitations or blocked work:** No required technical task remains. Final developer approval/acceptance pending. Default-branch package run follows separately authorized merge; Windows/additional Python versions unverified. Registry publication, usable experiment resources and later milestones excluded.
- **Developer decision:** Pending. Stop and await explicit approval, including at this final gate.
- **Decision reference and date:** None.
- **Requested changes and resolution:** None.
- **Progression authorized:** Final US-33 acceptance only if explicitly stated; no later milestone implementation or merge implied.

## Story completion review

All IDs below have prefix US-33-. Planned checks are not passing evidence.

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| AC-01 — documented wheel/sdist build | IP2-T1,T3,T5; IP3-T1,T2,T4 | [IP2/macOS evidence](../verification/us-33-ip2.md); [IP3/Linux evidence](../verification/us-33-ip3.md) | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-02 — clean wheel install outside checkout | IP2-T2–T5; IP3-T2,T4 | Separate runtime environments, installed distribution/path reports | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-03 — CLI/import and exact provisional resources | IP1-T3; IP2-T2–T5; IP3-T2–T4 | Existing source evidence; both installed probe results and negative cases passed | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-04 — rebuild wheel from sdist, same checks | IP2-T3–T5; IP3-T2,T4 | Extracted sdist identity, rebuilt wheel and independent probe results | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-05 — CI checks/logs and local reproduction | IP2-T4,T5; IP3-T1–T4 | Contributor commands, [hosted pass/failure logs](../verification/us-33-ip3.md) | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-06 — version matches metadata | IP1-T1–T3; IP2-T3–T5; IP3-T2,T4 | [Approved source behavior](../verification/cli-name-correction.md); both artifact checks passed | Verified on macOS and hosted Linux; developer acceptance pending |
| AC-07 — both wheel versions and source smoke | IP1-T3; US-31-IP2-T2; IP2-T3–T5; IP3-T1,T2,T4 | [Fresh source smoke](../verification/us-31-ip2.md); both wheel results passed | Verified on macOS and hosted Linux; developer acceptance pending |

- **Remaining work:** Final IP3 developer approval and explicit story acceptance only. Technical tasks complete; [IP3 evidence](../verification/us-33-ip3.md). Default-branch package run is post-merge follow-up. No Milestone 0 acceptance criterion deferred.
- **Partial prerequisite delivery:** IP1 remains accepted as a prerequisite slice; it cannot close US-33. US-31 and US-32 are accepted independently.
- **Developer acceptance:** Pending.
- **Decision reference and date:** None.

### IP2 execution record

Execution authorized by developer message “execute plan for us-33 ip2”, 2026-10-29. Issue #3 body and all comments refreshed: one unique comment (6510671946), stable updated_at 2026-10-29T23:10:06Z; SC-01 spelling correction applies. Public boundaries remain approved.

T1: uv 0.13.1 help confirms `uv build --out-dir PATH`, `uv build SOURCE --wheel --out-dir PATH`, `uv venv --no-project --python 3.12 PATH`, and `uv pip install --python PATH WHEEL`. Venv is unseeded with no system site packages; install retains normal dependency resolution. Select exactly one *.whl and *.tar.gz; validate archive members as regular files/directories within one root before extraction with Python 3.12 data filter. Distinct retained temporary workspaces preserve logs. Existing Hatchling package selection includes package-local data; no dependency/configuration change anticipated. Lock baseline SHA-256: ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d.

T2: Built baseline via `uv build --out-dir /tmp/us33-ip2/baseline`; installed with `uv pip install --python /tmp/us33-ip2/resource-env/bin/python WHEEL`. `python -I tests/packaging/check_installed.py` failed with installed template FileNotFoundError. Added exact template, rebuilt/reinstalled, probe passed. Added independent guidance assertion; same probe failed with installed guidance FileNotFoundError. Added exact guidance, rebuilt/reinstalled, probe passed. All runs Python 3.12.15; no Hatchling configuration or dependency changes. Temporary artifacts under `/tmp/us33-ip2/`.

T3: Public driver success test first failed because driver did not exist; implemented direct wheel environment/probe and observed green. Added rebuilt-wheel success assertion, observed red (direct passed but rebuilt absent); implemented safe extraction and isolated uv rebuild from extracted source, then 4 tests passed including existing CLI tests. Probe checks Python 3.12, artifact/installed/CLI version agreement, import and metadata locations, sys.path/cwd outside checkout, noneditable metadata, exact sole installed distribution and both exact resources. Each path has a unique environment/project; stdlib build tools remain outside runtime environments.

T4: Missing-template subprocess test initially failed for absent human-readable resource diagnostic; added explicit installed resource existence assertion and 2 tests passed. Altered guidance and wrong CLI version wheels then failed at their intended installed assertions while the original artifact success test passed after each slice (3 then 4 tests). Empty directory diagnostic test initially failed with IndexError; added exact artifact-count validation, 5 tests passed. Added wheel/sdist ambiguity cases; 7 tests passed. Independently mutated wheels have recomputed RECORD hashes; no production defects or weakened assertions. Driver retains each subprocess stdout/stderr in stage logs under its printed workspace. No failed corrective attempt: each minimal correction passed its original failure.

T5: Contributor documentation and README link added. Fresh artifacts and both installed paths passed; 11 tests, lint, formatting, mypy, locked sync/check, version smoke and lock checksum/diff passed. See [IP2 report](../verification/us-33-ip2.md) for hashes, versions, commands, TDD/failure evidence and limitations. All technical tasks complete; developer approval recorded 2026-10-29.


### IP3 execution record

Developer message “execute plan for us-33 ip3”, 2026-10-29, authorizes IP3 execution. Complete issue #3 body and all comment pages refreshed with stable metadata: open, one unique comment 6510671946, updated_at 2026-10-29T23:10:06Z, milestone metadata unset/body Milestone 0. SC-01 still governs CLI spelling. IP2 and accepted prerequisite evidence checked; working tree initially clean.

T1 complete: named build and installed-verification steps use documented commands verbatim; verification depends on successful build, independent development checks remain runnable, original exit codes propagate and final lock comparison remains always-run. Documentation explains step logs and temporary-workspace lifetime. actionlint 1.7.12 and manual command parity passed.

Initial publication checkpoint (superseded below): T2 partial: all shared commands and both installed paths passed locally on macOS; [report](../verification/us-33-ip3.md). Hosted publication requires explicit authorization under T2/T3 and the execution index; no commit, push, PR, failure fixture or merge performed. T3 and T4 remain incomplete. This is a publication checkpoint, not technical completion or final implementation gate approval.

Publication authorized by developer message “I approve the next steps”, 2026-10-29: commit/push implementation PR and disposable hosted failure/correction cases, restore source and close disposable PR without merge. Final gate and merge remain unapproved.


T2 complete: authorized publication produced implementation PR #24 and passing baseline run 40994320116 at 9f9c5f0; Ubuntu/Python 3.12 both wheel paths, all shared checks and final lock comparison passed. Versions, image observations, artifact identities and logs recorded in [IP3 report](../verification/us-33-ip3.md).

T3 complete: disposable PR #25 build-backend defect failed run 40994406312; exact restoration passed 40994481417. Separate resource-content defect failed installed verification in 40994573537; exact restoration passed 40994665653. Final tree equality verified; PR closed without merge. Each correction passed on attempt 1, no weakened checks or unresolved failure.

T4 complete: all seven criteria reconciled against local/macOS and hosted/Linux evidence; final local 11 tests and all shared/tool/package checks passed after exact restoration. Plan/index/checkpoint/contributor guidance updated. No deviations; default-branch package run remains explicitly post-merge follow-up. Final gate and story acceptance pending; publication approval does not approve either or authorize merge.
