## User Story

As a data scientist, I want to run local experiments and inspect logs, status and artifacts so that I can diagnose execution failures.

## Description

Delivery: M1. No implementation acceptance is claimed.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-10-AC-01: M1; US-10-AC-02: M1; US-10-AC-03: M1; US-10-AC-04: M1; US-10-AC-05: M1.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-10-AC-01:** Run a local experiment and expose logs, final result status and artifact locations.
- [ ] **US-10-AC-02:** Record completion or failure with available diagnostics.
- [ ] **US-10-AC-03:** Limit search to configured maximum candidate trials through the supported runner/search path.
- [ ] **US-10-AC-04:** Unsuccessful model performance is distinguishable from execution failure when modeling is added.
- [ ] **US-10-AC-05:** Preserve available completed-trial results and failure/interruption evidence when execution can finalize.

## Scope / Non-Goals

**In Scope:**

- The milestone slices above, through installed public interfaces in a separate experiment project.
- Trusted local code; project-owned configuration, models and preprocessing; MLflow records and native DVC stages.
- Component criteria own technical behavior; integration criteria own cross-component and assistant usability evidence.

**Out of Scope:**

- Managed agents and autonomous loops; mandatory experiment workflow approvals.
- OS-enforced filesystem/network/credential/holdout isolation and arbitrary-Python bypass prevention.
- Hard runtime/resource/cost quotas, durable workflow recovery and comprehensive dirty-source replay.
- Additional frameworks and connectors beyond the approved MVP. Displaced clauses remain in the migration record.

## Implementation Phase

**Phase:** Not specified. Define story/milestone implementation phases and granular tasks in a separate owning plan.

**Deliverables:** The assigned milestone outcomes and criterion-mapped evidence above.

**Developer Validation:** Confirm public test boundaries before executable tests. Stop at every implementation phase gate, including the final gate, for explicit developer approval.

**Exit Criteria:** Verify the assigned criteria; phase approval and whole-story/milestone acceptance remain distinct. Written-plan approval does not approve implementation gates.

## Validation Approach

### Automated Validation

- Completion/failure/logs, quality versus execution status, configured candidate cap and retained available diagnostics.
- Use independently defined outcomes through installed public interfaces and separate experiment-project fixtures; follow small vertical red–green TDD slices.
- Follow the repository verification policy: current milestone at executable gates; M1–6 selection at story acceptance; preserve failures/skips and explicit authorization requirements for broader/artifact checks.

### Developer Validation

- Review criterion-mapped evidence, failures, artifact/run/data references and platform/tool identities.
- Preserve development approval gates and separate milestone verification obligations; do not infer runtime behavior from documentation.

## Dependencies / References

- [Authoritative user stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md).
- [Approved original scope dispositions and assistant walkthrough](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md).
- [Revision plan and approval history](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md).
- [Verification policy](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/development/verification.md#phase-and-story-verification).
- Supporting design 0.14 is the previous baseline until Phase 3 reconciliation; do not implement conflicting design/issue scope. Phase 4 must publish only against reconciled source documents.
