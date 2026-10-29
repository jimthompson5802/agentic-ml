# Milestone 0 / US-33: Minimal CLI prerequisite for US-31

## Scope and outcome

- **Milestone:** 0 — Establish the harness development foundation.
- **User story:** [US-33 / issue #3](https://github.com/jimthompson5802/agentic-ml/issues/3).
- **User-visible outcome:** Source-installed `agentic-ml --version` prints distribution metadata version and exits zero.
- **Acceptance criteria covered:** US-33-AC-06 source-install behavior; advances AC-03 imports and AC-07 source smoke. Full installed-distribution evidence is deferred.
- **Scope boundaries:** Only source package, version entrypoint and behavior tests needed by US-31. Wheel/sdist builds, isolated installed checks, provisional resources and CI are not needed for US-31 and remain unplanned work in this story. This slice cannot close US-33 or Milestone 0.
- **Supporting design:** [contributor contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization), [traceability](../specs/design/acceptance-traceability.md), [delivery order](../specs/design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order).
- **Coordinated execution index:** [US-31 execution order](milestone-0-execution-order.md).

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

- **Status:** Approved.
- **Developer decision:** Approved — coordinated scope, proposed tooling choices, and public test boundaries.
- **Decision reference and date:** Developer message “i approve the plan” in this conversation, 2026-10-29. US-33 IP1 progression authorized by developer message “i approve” at the US-31 IP1 gate, 2026-10-29. US-33 IP1 gate remains pending.
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

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-33-AC-01 — wheel and sdist build command | Outside prerequisite slice | Deferred to full US-33 plan | Not covered |
| US-33-AC-02 — clean wheel install outside checkout | Outside prerequisite slice | Deferred | Not covered |
| US-33-AC-03 — CLI, imports, provisional resources | IP1-T3 advances import/CLI only | [Renamed source evidence passed](../verification/cli-name-correction.md); resources and installed checks deferred | Incomplete |
| US-33-AC-04 — rebuilt sdist wheel | Outside prerequisite slice | Deferred | Not covered |
| US-33-AC-05 — CI and local reproduction | Outside prerequisite slice | Deferred; depends on US-32 | Not covered |
| US-33-AC-06 — version matches metadata | IP1-T1–T3 | [Renamed source behavior passed](../verification/cli-name-correction.md); both distribution paths deferred | Incomplete |
| US-33-AC-07 — two wheel paths and source smoke | IP1-T3; US-31-IP2-T2 | [Renamed source smoke passed](../verification/cli-name-correction.md); fresh-clone and wheel checks deferred | Incomplete |

- **Remaining work:** Full US-33 planning and verification after this prerequisite slice.
- **Partial prerequisite delivery:** No whole-story completion implied by the IP1 gate.
- **Developer acceptance:** Pending.
- **Decision reference and date:** None.
