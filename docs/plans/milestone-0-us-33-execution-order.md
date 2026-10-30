# Milestone 0 execution order for US-33

Target: [US-33 / #3](https://github.com/jimthompson5802/agentic-ml/issues/3), full Milestone 0 package verification. Owning [US-33 plan](milestone-0-us-33.md) controls tasks, evidence and gates. This index reuses accepted prerequisites; it introduces no tasks owned by another story.

**Plan-review decision:** Approved — developer message “i approve the plan”, 2026-10-29, covers SC-02, IP2–IP3, technical choices and public test boundaries. IP2 execution authorized by developer message “execute plan for us-33 ip2”, 2026-10-29; IP2 technical tasks complete; gate approved by developer message “i approve us-33 ip2; commit changes”, 2026-10-29. IP3 execution authorization remains separate. Prior US-31, US-32 and US-33 IP1 approvals remain valid. Plan approval does not approve any implementation gate or publication.

| Order | Owning implementation phase | Prerequisite capabilities / supplying tasks | Required evidence and approvals before progression |
|---|---|---|---|
| Prerequisite | [US-31 IP1 and IP2](milestone-0-us-31.md), each T1–T3 | Locked tools, documented shared commands and fresh macOS source smoke | Accepted gates; [IP1 evidence](../verification/us-31-ip1.md), [IP2 evidence](../verification/us-31-ip2.md) |
| Prerequisite | [US-33 IP1](milestone-0-us-33.md#us-33--implementation-phase-1-provide-the-minimal-source-installed-version-cli), T1–T3 | Public import and version CLI | Approved IP1; [correction evidence](../verification/cli-name-correction.md) |
| Prerequisite for IP3 | [US-32 IP1 and IP2](milestone-0-us-32.md), IP1-T1–T3 and IP2-T1–T4 | Linux/Python 3.12 CI, shared commands, logs, failure propagation | Accepted gates; [IP1 evidence](../verification/us-32-ip1.md), [IP2 evidence](../verification/us-32-ip2.md) |
| 1 | [US-33 IP2](milestone-0-us-33.md#us-33--implementation-phase-2-verify-both-distribution-paths-locally), T1–T5 | US-31 tooling and US-33 IP1 CLI; reviewed SC-02/boundaries and execution authorization | Both isolated wheel paths, exact resources, negative cases and shared checks in [IP2 evidence](../verification/us-33-ip2.md); T1–T5 complete; IP2 approved 2026-10-29 |
| 2 | [US-33 IP3](milestone-0-us-33.md#us-33--implementation-phase-3-run-distribution-verification-in-ci), T1–T4 | Approved US-33 IP2; accepted US-32 CI; hosted access and separate publication authorization | Hosted pass/failure diagnostics in proposed `docs/verification/us-33-ip3.md`; stop for final IP3 approval and explicit story acceptance |

Shared integration check: run the documented development commands unchanged, then the same build and distribution verification commands locally and in CI. US-31 supplies tooling/source smoke, US-32 supplies existing CI infrastructure, US-33 owns new resources and all distribution checks. No whole-story dependency cycle or new prerequisite slice is introduced.

Historical coordination remains in the [US-31 index](milestone-0-execution-order.md) and [US-32 index](milestone-0-us-32-execution-order.md). Their completed gates are not reopened. SC-02 plans the remaining US-33 work previously excluded from those indexes.

Stop at every implementation gate. Check owning evidence before dependent work. Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for scope changes, updating owning plans/index together. No Milestone 1 or Milestone 99 work is authorized.
