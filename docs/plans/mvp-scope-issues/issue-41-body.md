## User Story

As a data scientist, I want interrupted workflows to resume from durable state without repeating completed runs so that work and approvals are preserved.

## Description

Uncommitted roadmap; historical milestones retained only as migration context.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-25-AC-01: deferred; US-25-AC-02: deferred; US-25-AC-03: deferred; US-25-AC-04: deferred.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-25-AC-01:** Project-associated durable state preserves workflow phase progress, run identifiers, evidence, approvals, budgets, and terminal or reviewable outcomes.
- [ ] **US-25-AC-02:** Recovery reconciles recorded work and resumes without duplicating completed runs or bypassing pending gates.
- [ ] **US-25-AC-03:** Resumed tasks use the preserved compatible configuration and runtime instruction bundle, even if source guidance has changed.
- [ ] **US-25-AC-04:** Cancelled, failed, budget-exhausted, and review-required outcomes retain evidence and do not silently authorize further work.

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
