# Milestone 0 execution order for US-32

Target: [US-32 / #2](https://github.com/jimthompson5802/agentic-ml/issues/2). Plan-review decision: **Approved** — developer message “i approve plan; commit changes”, 2026-10-29. Approval covers the US-32 plan and this index; implementation gates remain pending. This index reuses completed prerequisites from the [approved US-31 execution order](milestone-0-execution-order.md); their task records and approvals remain unchanged. The [US-32 plan](milestone-0-us-32.md) owns all new tasks, evidence and decisions. No additional prerequisite implementation is included.

| Order | Owning implementation phase | Prerequisite capabilities / supplying tasks | Required evidence and approvals before progression |
|---|---|---|---|
| Existing | [US-31 IP1 and IP2](milestone-0-us-31.md), T1–T3 in each | Locked tooling, configuration, documented commands and fresh-checkout macOS verification | Both gates and final acceptance approved; [fresh macOS evidence](../verification/us-31-ip2.md) |
| Existing | [US-33 IP1](milestone-0-us-33.md), T1–T3 | Source-installed version CLI, public imports and tests | Gate approved 2026-10-29; [renewed CLI evidence](../verification/cli-name-correction.md); full story not required |
| 1 | [US-32 IP1](milestone-0-us-32.md#us-32--implementation-phase-1-configure-macos-development-ci), T1–T3 | Existing capabilities above; US-32 plan/public boundaries approved and implementation authorized | Configuration/local check evidence in proposed `docs/verification/us-32-ip1.md`; explicit IP1 approval before IP2 |
| 2 | [US-32 IP2](milestone-0-us-32.md#us-32--implementation-phase-2-verify-hosted-triggers-and-failure-diagnostics), T1–T4 | US-32-IP1-T1–T3 and approved gate; authorized external publication and separately authorized merge | Actual PR/default-branch success and failing PR diagnostics in proposed `docs/verification/us-32-ip2.md`; explicit final gate/acceptance |

Shared checks: US-31 owns the commands and tool configuration; US-33 IP1 supplies the minimal tested CLI; US-32 automates those commands and verifies hosted outcomes. No cycle requires completing US-33 distribution verification. Its package CI checks remain downstream work owned by US-33.

Stop at each implementation phase gate. Plan approval does not approve implementation gates or publication/merge. Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for changed scope and update affected owning plans and this index together.
