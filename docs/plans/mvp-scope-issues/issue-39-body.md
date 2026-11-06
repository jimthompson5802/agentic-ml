## User Story

As a data scientist, I want an agent adapter with explicit, preserved runtime guidance so that agent behavior follows the approved experiment context.

## Description

Uncommitted roadmap; historical milestones retained only as migration context.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-30-AC-01: deferred; US-30-AC-02: deferred; US-30-AC-03: deferred; US-30-AC-04: deferred; US-30-AC-05: deferred.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-30-AC-01:** The first managed coding-assistant adapter verifies a concrete product/interface/version and supports capability discovery, structured task/result exchange, and documented task cancellation through the common contract. Interactive assistants can use the public toolkit CLI/API without an adapter. Acceptance demonstrates task receipt, project-code/notebook revision, managed execution, development-feedback consumption, and stopping at a developer approval boundary.
- [ ] **US-30-AC-02:** Runtime loading explicitly selects packaged shared guidance, relevant task-specific guidance, and configured project guidance, recording ownership and order.
- [ ] **US-30-AC-03:** Development `AGENTS.md` files from either repository are excluded from automatic loading by the toolkit runtime loader. Instructions independently loaded by an external assistant are outside this guarantee; observable additional context and capture limitations are recorded.
- [ ] **US-30-AC-04:** The plan snapshots toolkit-supplied guidance contents, paths, versions/checksums, and load order; subsequent tasks reference the preserved bundle, with managed adapters demonstrating delivery. This records toolkit-supplied guidance, not the assistant's complete instruction context.
- [ ] **US-30-AC-05:** Conflicting guidance or attempts to expand experiment constraints block affected execution; adopting changed guidance requires a new versioned configuration and applicable approvals.

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
- Supporting design 0.14 is the previous baseline until Phase 3 reconciliation; do not implement conflicting design/issue scope. Phase 4 must publish only against reconciled source documents.
