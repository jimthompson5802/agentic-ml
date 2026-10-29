# Milestone 0 execution order for US-31

Target: [US-31 / #1](https://github.com/jimthompson5802/agentic-ml/issues/1). Included prerequisite: the minimal source CLI portion of [US-33 / #3](https://github.com/jimthompson5802/agentic-ml/issues/3). This index coordinates owning plans; it does not own tasks or evidence.

**Plan-review decision:** Approved for both linked plans and this coordinated scope, including proposed tooling and public test boundaries. Reference: developer message “i approve the plan” in this conversation, 2026-10-29. Distribution name `agentic-ml` previously approved on the same date. All implementation gates remain pending. Implementation requires separate authorization.

| Order | Owning implementation phase | Prerequisite capabilities / supplying tasks | Required evidence and approvals before progression |
|---|---|---|---|
| 1 | [US-31 IP1](milestone-0-us-31.md#us-31--implementation-phase-1-establish-locked-tooling-and-contributor-conventions), T1–T3 | No earlier milestone; reviewed tool and public-boundary decisions | Tool/lock/convention evidence in proposed `docs/verification/us-31-ip1.md`; explicit US-31 IP1 approval |
| 2 | [US-33 IP1](milestone-0-us-33.md#us-33--implementation-phase-1-provide-the-minimal-source-installed-version-cli), T1–T3 | US-31-IP1-T1–T3 tooling, metadata and documented checks | CLI red/green, metadata and shared-check results in proposed `docs/verification/us-33-ip1.md`; explicit US-33 IP1 approval |
| 3 | [US-31 IP2](milestone-0-us-31.md#us-31--implementation-phase-2-verify-documented-macos-setup-and-source-smoke-check), T1–T3 | US-33-IP1-T1–T3 version CLI, public import and tests; both prior gates approved | Fresh macOS clone/environment results in proposed `docs/verification/us-31-ip2.md`; explicit final US-31 gate/acceptance |

Shared integration check: US-33 supplies CLI and its public behavior tests; US-31 supplies locked tooling and fresh-clone setup plus smoke evidence. Cross-links reuse owning tasks, avoiding whole-story dependency cycles. Check owning evidence and decisions before each entry. Stop at every gate; plan approval never approves implementation progression.

US-32 and the remainder of US-33 are downstream work and excluded. Completing this index completes neither CI nor Milestone 0. US-32 must later consume the same documented check commands and update documentation with actual verified CI versions. Full US-33 planning must add provisional resources and both isolated distribution paths before its acceptance can be claimed.

Changes to prerequisite scope during execution require [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md), updates to both owning plans and this index, and developer approval before added implementation.
