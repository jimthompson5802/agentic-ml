## User Story

As a data scientist, I want supplied code to remain immutable unless I approve changes so that agents respect ownership and component permissions.

## Description

Uncommitted roadmap; historical milestones retained only as migration context.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-17-AC-01: deferred; US-17-AC-02: deferred; US-17-AC-03: deferred; US-17-AC-04: deferred.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-17-AC-01:** Supplied components are immutable by default; agents may configure and invoke them only within authorized boundaries.
- [ ] **US-17-AC-02:** Attempts to modify immutable components are blocked unless recorded developer approval authorizes the change.
- [ ] **US-17-AC-03:** Approved changes to immutable code create a new versioned experiment configuration.
- [ ] **US-17-AC-04:** Modification permission does not expand algorithm, parameter, data-access, or evaluation boundaries; authorized code changes appear in run snapshots.

## Scope / Non-Goals

**In Scope:**

- Preserve the original criteria as deferred scope; no MVP implementation is authorized.

**Out of Scope:**

- Managed agents and autonomous loops; mandatory experiment workflow approvals.
- OS-enforced filesystem/network/credential/holdout isolation and arbitrary-Python bypass prevention.
- Hard runtime/resource/cost quotas, durable workflow recovery and comprehensive dirty-source replay.
- Additional frameworks and connectors beyond the approved MVP. Displaced clauses remain in the migration record.

## Implementation Phase

**Phase:** Not specified. Define story/milestone implementation phases and granular tasks in a separate owning plan.

**Deliverables:** Deferred requirement record only; no current product delivery.

**Developer Validation:** Confirm public test boundaries before executable tests. Stop at every implementation phase gate, including the final gate, for explicit developer approval.

**Exit Criteria:** A later explicit scope decision is required before implementation.

## Validation Approach

### Automated Validation

- Future checks must be planned when this roadmap scope is activated; deferral is not evidence of acceptance.

### Developer Validation

- Review criterion-mapped evidence, failures, artifact/run/data references and platform/tool identities.
- Preserve development approval gates and separate milestone verification obligations; do not infer runtime behavior from documentation.

## Dependencies / References

- [Authoritative user stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md).
- [Approved original scope dispositions and assistant walkthrough](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md).
- [Revision plan and approval history](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md).
- [Verification policy](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/development/verification.md#phase-and-story-verification).
- [Active MVP design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md) defines the revised trusted-local scope; archived 0.14 platform contracts are historical reference. Synchronize issue scope and the reviewed source revision before product implementation.
