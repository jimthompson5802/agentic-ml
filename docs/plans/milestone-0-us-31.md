# Milestone 0 / US-31: Set up the harness development environment

## Scope and outcome

- **Milestone:** 0 — Establish the harness development foundation.
- **User story:** [US-31 / issue #1](https://github.com/jimthompson5802/agentic-ml/issues/1).
- **User-visible outcome:** Contributors can follow a reproducible macOS setup and run source CLI, tests, lint, format, type, and smoke checks through the locked environment.
- **Acceptance criteria covered:** US-31-AC-01–10 in full; criterion meanings are preserved in the completion review below.
- **Scope boundaries:** Local foundation only. CI execution belongs to US-32; full distribution verification belongs to US-33. Include only the [US-33 prerequisite slice](milestone-0-us-33.md) needed for the source CLI. No experiment initialization, ML dependencies, services, agent adapters, publishing, or Milestone 99 work.
- **Supporting design:** [reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [contributor contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [delivery dependencies](../specs/design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order), [traceability](../specs/design/acceptance-traceability.md), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization), and [layout](../specs/design/repository-layout.md).
- **Coordinated execution index:** [Milestone 0 order for US-31](milestone-0-execution-order.md).

## Findings and source reconciliation

On 2026-10-29, retrieved complete bodies and all comment pages for issues #1 and #3. Both are open, authored by jimthompson5802, with no assignees and no GitHub milestone object; their bodies assign Milestone 0. Each reported zero comments; successful paginated responses contained zero comments, and repeated metadata reads retained the original counts and update times (#1: `2026-10-29T03:08:20Z`; #3: `2026-10-29T03:09:12Z`). No comment scope decisions exist. Issue requirements agree with repository story criteria and ADR-007; no scope conflict found.

The inspected tree at `c5d5d37` has documentation and skills, with no Python package, lockfile, tests, tool configuration, workflows, or existing plans. Paths and commands below are proposals, not working facilities. CHECKPOINTS.md's prior commit note predates the actual handoff commit; this plan uses the inspected tree. US-32 is a downstream consumer, not a prerequisite; no US-32 implementation is included.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Distribution identity | `agentic-ml` distribution, `agentic_ml` import, `agentic-ml` CLI | Package metadata | Distribution name explicitly approved by developer in this conversation, 2026-10-29; CLI/import settled in ADR-007 |
| Repository source | `https://github.com/jimthompson5802/agentic-ml.git`; editable local repository install for development | Setup documentation | Confirmed origin; full-SHA experiment installation remains Milestone 1 |
| Build/version choices | Hatchling backend; static initial version `0.1.0` in pyproject metadata; standard-library argparse CLI | US-33 prerequisite | Proposed implementation choices for plan review; no runtime third-party dependencies initially |
| Tools | Python 3.12 baseline; uv; pytest, Ruff, mypy in dev dependency group | US-31 IP1 | Proposed; resolve compatible releases at implementation, commit exact resolutions in uv.lock, record uv version; do not invent unverified version pins |
| Minimal CLI | US-33-IP1-T1–T3 and approved US-33 IP1 gate | US-31 IP2 | [Renamed CLI tasks complete with evidence](../verification/cli-name-correction.md); owning US-33 IP1 gate approved 2026-10-29 |
| CI status | Document Python 3.12 target separately from versions actually verified in CI | AC-01 final status | US-32 deferred; initially state CI not yet established, no claimed CI success; future CI evidence must update docs |
| macOS host and clean source snapshot | Fresh clone of reviewed commit, new .venv, recorded prerequisite versions | IP2 verification | Available and verified; [fresh macOS report](../verification/us-31-ip2.md). New clone and .venv, no copied environment |

## Technical approach and public test boundaries

Use a src-layout installable project, `requires-python = ">=3.12"`, committed `uv.lock`, `.python-version` selecting 3.12, and `.gitignore` excluding environments, caches, build outputs and generated evidence. US-31 owns tool/build configuration; US-33 owns product source, entrypoint declaration, and product tests. IP1 may configure packaging before product files exist; do not claim the empty package is runnable. Before US-33 supplies package files, use `uv sync --locked --group dev --no-install-project`, then `uv run --no-sync ruff check <temporary-path>`, `uv run --no-sync ruff format --check <temporary-path>`, and `uv run --no-sync mypy --strict <temporary-path>` for tool configuration checks. These bootstrap-only commands do not claim a runnable package or collected product tests.

Proposed shared commands after the package exists:

- Setup: `uv sync --locked --group dev`.
- Tests: `uv run --locked pytest`.
- Lint: `uv run --locked ruff check .`.
- Formatting: `uv run --locked ruff format --check .`.
- Types: `uv run --locked mypy src tests`.
- Smoke: `uv run --locked agentic-ml --version`.

Configure pytest discovery, Ruff Python 3.12 target with naming/import/docstring/error rules selected individually, Ruff formatting, and strict mypy for typed source/tests. Document snake_case functions/modules, PascalCase classes, UPPER_CASE constants, explicit public types, Google-style public docstrings, grouped imports, specific exceptions, contextual errors, and no silent exception swallowing. Document which conventions are automated and which require review. Each suppression/exclusion needs a nearby specific reason and a reviewable exception record (rule, path, rationale, scope, removal condition) in proposed `docs/development.md`; no blanket exclusions to make checks pass.

Plan review explicitly confirms these boundaries before executable changes: the source CLI is exercised as a subprocess with exit code and stdout compared to installed distribution metadata, not mocked internal functions. Fresh-checkout verification exercises contributor commands and lock immutability; it does not establish wheel isolation, CI success, other-platform support, or experiment behavior. Tool enforcement is checked with temporary invalid examples through public tool commands, not tests mirroring configuration. Docs/config-only work has no new harness behavior and uses inspection and tool checks rather than manufactured red tests. New product behavior in US-33 follows one-test-at-a-time TDD.

## Execution rules

Mark tasks Complete only after required work and checks pass; record commands, actual results, and evidence. Keep partial, failed, blocked, and unverified tasks incomplete. Reopen tasks when later changes invalidate evidence. Follow the [execution index](milestone-0-execution-order.md); verify supplying tasks and gate decisions before dependent work.

Stop at every implementation phase boundary, including the final one. Present tasks, results, evidence paths, deviations, and limitations; await explicit developer approval and record its date and reference. Plan approval does not approve implementation gates. Silence is not approval.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes; pause affected work, revise owning plans and the index together, and obtain approval before implementing newly discovered prerequisite scope. Follow the [three-attempt limit](../../AGENTS.md#problem-solving-attempt-limit): record hypothesis, change, and original-failure verification for each corrective attempt; after three failures preserve diagnostics and stop for direction. Never weaken acceptance assertions or suppress failures.

Record evidence in proposed `docs/verification/` Markdown reports; keep temporary environments, logs containing sensitive data, and generated storage outside Git. Update [CHECKPOINTS.md](../../CHECKPOINTS.md) at gates, blockers, and handoff.

## Plan review

- **Status:** Approved.
- **Developer decision:** Approved — coordinated scope, proposed tooling choices, and public test boundaries.
- **Decision reference and date:** Developer message “i approve the plan” in this conversation, 2026-10-29. US-31 IP1 and US-33 IP1 gates subsequently approved in their owning records. US-31 IP2 execution authorized by developer message “start the next phase”, 2026-10-29; its final gate remains pending.
- **Requested plan changes:** None.

## Scope-change history

- **Change ID and date:** SC-01, 2026-10-29.
- **Request and reason:** Developer explicitly requested correction of ADR-007 and generated code/documents: CLI should be `agentic-ml` for consistent package naming.
- **Scope difference:** Replace the CLI name `agent-ml` with `agentic-ml`; distribution `agentic-ml` and import `agentic_ml` stay as selected. No legacy alias or additional experiment command is added.
- **Impact:** US-31 CLI/smoke expectations (AC-03,05,07) and US-33 CLI/import/version expectations (AC-03,06,07) require renewed evidence; stable task and criterion IDs retained. US-33-IP1-T2–T3 were reopened and are complete again after renamed command checks passed; see correction evidence. US-31 IP1 approval remains historical; its tooling checks remain valid, while renamed guidance is reviewed in this correction. No milestone or prerequisite changes.
- **Plan and requirement revisions:** ADR-007, current user stories, harness design/examples, README, contributor guide, repository instructions, both story plans, and execution index. GitHub issue bodies still contain the old spelling; this explicit developer direction overrides that spelling for implementation. Historical reports retain original results and link the correction evidence.
- **Verification and gates:** Rename the public CLI regression first and confirm failure for the absent required command, then correct entrypoint and verify version/import/help plus all shared checks and lock immutability. US-33 IP1 gate stays pending; US-31 IP2 does not start.
- **Decision:** Approved — developer instruction requesting this correction in this conversation, 2026-10-29, authorizes the scope revision and implementation without another approval cycle.
- **Resume point:** Correct and reverify US-33 IP1 within its existing gate; see [CLI correction evidence](../verification/cli-name-correction.md).


## US-31 / Implementation Phase 1: Establish locked tooling and contributor conventions

- **Outcome:** Reviewable tool configuration and contributor guide, ready to receive the minimal package.
- **Entry conditions:** Coordinated plan approved, public boundaries confirmed, implementation separately authorized.
- **Acceptance criteria advanced:** US-31-AC-01–02, 04, 06, 08–10; source CLI and fresh setup remain pending.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-31-IP1-T1 | Complete | Create proposed `pyproject.toml`, `.python-version`, `uv.lock`, `.gitignore`: build backend/version metadata and dev tools; Python >=3.12, baseline 3.12. Lock once during setup; subsequent verification must use locked mode. | Approved decisions | Metadata parse and lock consistency checks pass; exact tool versions recorded; no empty-package execution claim. | US-31-AC-02, 08 |
| US-31-IP1-T2 | Complete | Configure pytest, Ruff lint/format, and strict mypy in proposed `pyproject.toml`; create proposed `docs/development.md` conventions and exception policy. | T1 | Each documented convention mapped to automated rule or manual review; temporary naming/import/docstring/type/format violations are rejected by applicable tools and corrected examples pass. Keep fixtures outside tracked source and record commands/results. | US-31-AC-04, 08–10 |
| US-31-IP1-T3 | Complete | Update `README.md` and proposed `docs/development.md`: clone URL, Git/uv/Python prerequisites, macOS notes, locked setup, shared commands, no-service local defaults, credential/access needs for cloning/dependency downloads; no MLflow/DVC/model credentials for minimal checks. | T1–T2 | Guide distinguishes future CLI verification from available tooling and Python 3.12 CI target from actual CI evidence (none yet). Linux/Windows explicitly unverified. | US-31-AC-01–02, 04, 06, 09–10 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Metadata/lock | `uv lock --check`; record selected tools with uv environment/version diagnostics | Lock matches metadata; verification leaves uv.lock unchanged | Passed; [IP1 evidence](../verification/us-31-ip1.md) records versions and unchanged checksum |
| Tool configuration | Bootstrap tool commands above from locked dev group before source exists; record exact commands in `docs/verification/us-31-ip1.md` (proposed) | Invalid temporary examples fail relevant checks; corrected examples pass; no suppression hides failure | Passed; six invalid examples rejected and corrected examples pass; [IP1 evidence](../verification/us-31-ip1.md) |
| Documentation | Review commands, prerequisites, rule mapping, credential requirements and justified exceptions | All IP1 criterion portions documented; no claims of completed CLI/CI/package verification | Passed; [guide](../development.md) and [IP1 review](../verification/us-31-ip1.md) |

### Developer approval gate

- **Approval criteria:** T1–T3 complete and evidence reviewed; proposed public boundaries confirmed.
- **Evidence presented:** [IP1 verification](../verification/us-31-ip1.md); T1–T3 technically complete. Gate approved.
- **Remaining limitations or blocked work:** No runnable CLI or fresh-checkout evidence yet.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve” after IP1 review and convention questions, 2026-10-29.
- **Requested changes and resolution:** None.
- **Progression authorized:** US-33 IP1 in the coordinated index; approval responds to the request to authorize this progression.

## US-31 / Implementation Phase 2: Verify documented macOS setup and source smoke check

- **Outcome:** A fresh contributor environment passes every documented development check.
- **Entry conditions:** Approved US-31 IP1 and US-33 IP1 gates, minimal CLI and meaningful tests present; macOS host available.
- **Acceptance criteria advanced:** US-31-AC-01–10, completing local setup verification.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-31-IP2-T1 | Complete | Finalize `README.md`, `docs/development.md` with exact shared commands including version smoke, setup troubleshooting, platform limits and honest CI verification status. | US-33-IP1-T1–T3 and approved gate | All commands executable; smoke success means version output and zero exit; missing setup or CLI failures produce nonzero status. No experiment services required. | US-31-AC-01–06, 08–10 |
| US-31-IP2-T2 | Complete | From a new macOS clone of the reviewed source revision and a new environment, follow only documented setup and run all six commands above; create proposed `docs/verification/us-31-ip2.md`. | T1 | Record revision, OS/architecture, Python/Git/uv/dev-tool versions, commands, exit codes and results; tests actually collected, all checks pass, version agrees with metadata, uv.lock unchanged before/after. Record any extra steps as defects requiring guide correction and rerun. | US-31-AC-02–05, 07–08 |
| US-31-IP2-T3 | Complete | Review complete criterion evidence and update this plan plus `CHECKPOINTS.md`. | T2 | Each criterion has evidence and limitations; macOS verification separated from unverified Linux/Windows and pending CI; no US-33 completion claim. | US-31-AC-01–10 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Fresh setup | Documented clone, Python selection and `uv sync --locked --group dev` | New environment installs only documented prerequisites and dependencies | Passed; [fresh setup and diagnostics](../verification/us-31-ip2.md) |
| Shared checks | Tests, lint, format, types and version smoke commands above | Every command exits zero; collected tests exercise public CLI; stdout version matches metadata | Passed; 3 tests, lint, format, types and smoke; [command outputs](../verification/us-31-ip2.md#command-results-from-the-fresh-clone) |
| Reproducibility | Compare lockfile checksum and Git diff before/after; record host/tool diagnostics | No lock update or undocumented setup edits; macOS evidence reproducible | Passed; unchanged lock checksum and clean fresh clone; [integrity evidence](../verification/us-31-ip2.md#integrity-and-documentation-review) |
| Coverage | Review criterion mapping and source docs | AC-01–10 supported without claiming CI execution | Verified; [criterion review](../verification/us-31-ip2.md#acceptance-criterion-review), developer acceptance pending |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; fresh macOS evidence and every criterion reviewed.
- **Evidence presented:** [Fresh macOS verification](../verification/us-31-ip2.md); T1–T3 technically complete. Final developer gate approved.
- **Remaining limitations or blocked work:** CI and full distribution checks belong to other stories; additional platforms unverified.
- **Developer decision:** Approved — final IP2 gate and US-31 acceptance.
- **Decision reference and date:** Developer message “i approve us-31 ip2” following the final US-31 acceptance review in this conversation, 2026-10-29.
- **Requested changes and resolution:** None.
- **Progression authorized:** US-31 accepted; coordinated scope complete. Stop here. No downstream story implementation authorized.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-31-AC-01 — Python/tools, CI version status, platform limits | IP1-T3; IP2-T1, T3 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-02 — clone and locked dependencies | IP1-T1, T3; IP2-T2 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-03 — source CLI | IP2-T1–T2; US-33 IP1 prerequisite | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-04 — documented check commands | IP1-T2–T3; IP2-T2 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-05 — readiness smoke | IP2-T1–T2 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-06 — configuration, credentials, defaults | IP1-T3; IP2-T1–T2 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-07 — fresh macOS verification and diagnostics | IP2-T2–T3 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-08 — configured locked tools | IP1-T1–T2; IP2-T2 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-09 — conventions and enforcement | IP1-T2–T3; IP2-T3 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |
| US-31-AC-10 — justified exceptions | IP1-T2–T3; IP2-T3 | [IP2 criterion evidence](../verification/us-31-ip2.md#acceptance-criterion-review) | Verified and accepted |

- **Remaining work:** All US-31 tasks and technical checks complete. Final IP2 gate and story acceptance approved. No US-31 criterion deferred; no later-story implementation authorized.
- **Partial prerequisite delivery:** US-33 slice supplies CLI only; its distribution and CI criteria remain open.
- **Developer acceptance:** Approved through the final IP2 gate after the explicit story-completion review.
- **Decision reference and date:** Developer message “i approve us-31 ip2” following the final US-31 acceptance review in this conversation, 2026-10-29.
