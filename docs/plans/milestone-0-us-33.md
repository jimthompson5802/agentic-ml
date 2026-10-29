# Milestone 0 / US-33: Minimal CLI prerequisite for US-31

## Scope and outcome

- **Milestone:** 0 — Establish the harness development foundation.
- **User story:** [US-33 / issue #3](https://github.com/jimthompson5802/agentic-ml/issues/3).
- **User-visible outcome:** Source-installed `agent-ml --version` prints distribution metadata version and exits zero.
- **Acceptance criteria covered:** US-33-AC-06 source-install behavior; advances AC-03 imports and AC-07 source smoke. Full installed-distribution evidence is deferred.
- **Scope boundaries:** Only source package, version entrypoint and behavior tests needed by US-31. Wheel/sdist builds, isolated installed checks, provisional resources and CI are not needed for US-31 and remain unplanned work in this story. This slice cannot close US-33 or Milestone 0.
- **Supporting design:** [contributor contract](../specs/design/interfaces-and-configuration.md#contributor-development-and-package-verification-milestone-0), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization), [traceability](../specs/design/acceptance-traceability.md), [delivery order](../specs/design/milestone-delivery.md#milestone-0-dependencies-and-delivery-order).
- **Coordinated execution index:** [US-31 execution order](milestone-0-execution-order.md).

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| US-31 foundation | US-31-IP1-T1–T3 with approved IP1 gate; locked tools and metadata | All tasks below | [Owning plan](milestone-0-us-31.md); pending |
| Package choices | `agentic-ml`, `agentic_ml`, `agent-ml`; Hatchling, version `0.1.0`, argparse, no third-party runtime dependencies | CLI configuration | Distribution name developer-approved 2026-10-29; remaining implementation choices proposed in US-31 plan |
| Requirements snapshot | Full #3 body and zero comments; repeated metadata unchanged | Planning | Retrieved 2026-10-29; see [US-31 source findings](milestone-0-us-31.md#findings-and-source-reconciliation) |

## Technical approach and public boundaries

Proposed files: `src/agentic_ml/__init__.py`, `src/agentic_ml/cli/__init__.py`, `tests/integration/test_cli_version.py`; extend shared `pyproject.toml` with `agent-ml` entrypoint. The proposed CLI callable uses argparse and `importlib.metadata.version("agentic-ml")`; metadata is the single version source. Do not add experiment commands or fallback hardcoded versions that conceal missing installation.

Plan review must confirm subprocess CLI tests with independent expectations from installed metadata: zero exit, version stdout, and importability. These source-install tests do not verify wheel contents, runtime resource loading, sdist completeness, clean runtime dependency isolation, or CI. Follow TDD in small vertical slices: one failing behavior test, confirm missing behavior is the cause, implement minimally, rerun relevant tests, then add the next behavior. Record red/green commands and results. Tests must use public commands and imports, not mocked CLI internals.

## Execution rules

Mark tasks Complete only after required work and checks pass; record commands, actual results, and evidence. Keep partial, failed, blocked, and unverified tasks incomplete. Reopen tasks when later changes invalidate evidence. Follow the [execution index](milestone-0-execution-order.md); verify supplying tasks and gate decisions before dependent work.

Stop at every implementation phase boundary, including the final one. Present tasks, results, evidence paths, deviations, and limitations; await explicit developer approval and record its date and reference. Plan approval does not approve implementation gates. Silence is not approval.

Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes; pause affected work, revise owning plans and the index together, and obtain approval before implementing newly discovered prerequisite scope. Follow the [three-attempt limit](../../AGENTS.md#problem-solving-attempt-limit): record hypothesis, change, and original-failure verification for each corrective attempt; after three failures preserve diagnostics and stop for direction. Never weaken acceptance assertions or suppress failures.

Record evidence in proposed `docs/verification/` Markdown reports; keep temporary environments, logs containing sensitive data, and generated storage outside Git. Update [CHECKPOINTS.md](../../CHECKPOINTS.md) at gates, blockers, and handoff.

## Plan review

- **Status:** Approved.
- **Developer decision:** Approved — coordinated scope, proposed tooling choices, and public test boundaries.
- **Decision reference and date:** Developer message “i approve the plan” in this conversation, 2026-10-29. Implementation authorization and all implementation gate decisions remain pending.
- **Requested plan changes:** None.

## Scope-change history

None.

## US-33 / Implementation Phase 1: Provide the minimal source-installed version CLI

- **Outcome:** Version CLI and public import work from the locked contributor environment.
- **Entry conditions:** Coordinated plan/boundaries approved and implementation authorized; US-31 IP1 gate approved.
- **Acceptance criteria advanced:** US-33-AC-03, 06–07; source-install subset only.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-33-IP1-T1 | Not started | Add first behavior test in proposed `tests/integration/test_cli_version.py` for CLI exit and version; create package skeleton only as needed for installation/test discovery. | US-31 IP1 approved | A real subprocess fails because version entrypoint/behavior is absent, rather than dependency/setup failure; preserve red output. | US-33-AC-06 |
| US-33-IP1-T2 | Not started | Implement proposed `src/agentic_ml/cli/__init__.py`, package init and `[project.scripts]` in `pyproject.toml`; sync locked environment. | T1 | `agent-ml --version` exits zero and reports installed distribution version; first regression test and relevant checks pass. Resolve legitimate metadata/lock changes explicitly, never through verification's silent update. | US-33-AC-06 |
| US-33-IP1-T3 | Not started | Add next public import behavior test red–green if missing; run shared checks, record source version/import evidence in proposed `docs/verification/us-33-ip1.md`; update owning plans/checkpoint. | T2 | Tests/lint/format/types and source smoke pass; independently checked metadata version and import result; no wheel/resource claims. | US-33-AC-03, 06–07 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| TDD | `uv run --locked pytest tests/integration/test_cli_version.py` per slice | Red missing behavior followed by green; import test added only after first slice green | Pending |
| CLI and metadata | `uv run --locked agent-ml --version`; subprocess test compares stdout version with metadata | Zero exit, expected installed version, import succeeds | Pending |
| Regression/tooling | Shared US-31 test, lint, format and type commands | All pass; lock remains consistent and unchanged during checks | Pending |

### Developer approval gate

- **Approval criteria:** T1–T3 complete with red/green and shared-check evidence reviewed.
- **Evidence presented:** Pending; proposed `docs/verification/us-33-ip1.md`.
- **Remaining limitations or blocked work:** No wheel/sdist/resource/CI verification; US-33 remains incomplete.
- **Developer decision:** Pending.
- **Decision reference and date:** None.
- **Requested changes and resolution:** None.
- **Progression authorized:** Pending approval, return to US-31 IP2. Stop here.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-33-AC-01 — wheel and sdist build command | Outside prerequisite slice | Deferred to full US-33 plan | Not covered |
| US-33-AC-02 — clean wheel install outside checkout | Outside prerequisite slice | Deferred | Not covered |
| US-33-AC-03 — CLI, imports, provisional resources | IP1-T3 advances import/CLI only | Source evidence pending; resources and installed checks deferred | Incomplete |
| US-33-AC-04 — rebuilt sdist wheel | Outside prerequisite slice | Deferred | Not covered |
| US-33-AC-05 — CI and local reproduction | Outside prerequisite slice | Deferred; depends on US-32 | Not covered |
| US-33-AC-06 — version matches metadata | IP1-T1–T3 | Source behavior pending; both distribution paths deferred | Incomplete |
| US-33-AC-07 — two wheel paths and source smoke | IP1-T3; US-31-IP2-T2 | Source smoke pending; wheel checks deferred | Incomplete |

- **Remaining work:** Full US-33 planning and verification after this prerequisite slice.
- **Partial prerequisite delivery:** No whole-story completion implied by the IP1 gate.
- **Developer acceptance:** Pending.
- **Decision reference and date:** None.
