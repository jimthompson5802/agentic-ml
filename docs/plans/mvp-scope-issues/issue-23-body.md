## User Story

As a data scientist, I want to run native DVC stages from committed experiment inputs so that I can reproduce results and reuse valid outputs.

## Description

Delivery: M1 and M2. No implementation acceptance is claimed.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-27-AC-05: M1; US-27-AC-06: M1; US-27-AC-07: M2; US-27-AC-08: M2; US-27-AC-09: M2.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-27-AC-05:** DVC pipeline definitions record stage dependencies, parameters, and outputs, with resolved hashes preserved in `dvc.lock`.
- [ ] **US-27-AC-06:** Stage working directories and paths are explicit and consistent with toolkit execution.
- [ ] **US-27-AC-07:** Reproducing declared stages restores or generates the expected outputs under the recorded configuration.
- [ ] **US-27-AC-08:** Use native DVC dependency hashes for reuse and retain traceable run/data/code references; re-evaluate outputs where required.
- [ ] **US-27-AC-09:** Treat cached output as reusable data, not proof that metrics/checks pass.

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

- Native stage dependencies/parameters/working directories, cache reuse/invalidation and committed-project reproduction.
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
