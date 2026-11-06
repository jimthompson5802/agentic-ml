## User Story

As a data scientist, I want to reproduce committed experiments through DVC with coding-assistant help so that I can verify results and avoid unnecessary recomputation.

## Description

Delivery: M2. No implementation acceptance is claimed.

US-39 M1 supplies a recorded experiment; US-13/15/16/21/27 supply data/pipeline restoration, native DVC stages and output checks. This M2 story owns ASW-07.

This integration story references component criteria instead of duplicating implementation ownership.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-40-AC-01:** A fresh checkout of committed experiment code/configuration, pinned toolkit dependencies and available DVC data can restore required inputs and execute declared stages outside the toolkit checkout using documented commands.
- [ ] **US-40-AC-02:** An unchanged pipeline demonstrates native DVC output reuse without retraining unchanged stages; evidence distinguishes cached reuse from newly executed training and retains traceable result/data/code references.
- [ ] **US-40-AC-03:** Changing a declared data, code or parameter dependency invalidates the affected native DVC stages; the demonstration records which stages rerun and verifies their regenerated outputs.
- [ ] **US-40-AC-04:** Missing required source, dependencies or DVC content, and corrupted or mismatched required data, produce explicit restoration/reproduction failures without silently substituting current or alternate inputs.
- [ ] **US-40-AC-05:** Actual reproduced execution records MLflow results and committed code/configuration, environment and DVC identities, with references to the compared experiment. Cache reuse alone is not recorded as newly executed training or proof of passing evaluation.
- [ ] **US-40-AC-06:** The data scientist directs an external coding assistant through documented DVC restoration/reproduction and result inspection; evidence records assistant product/interface/version, prompts, commands/outcomes and verified run/data references without requiring a managed adapter.
- [ ] **US-40-AC-07:** Declared output checks and metric tolerances determine reproduction success; the demonstration includes restored fitted preprocessing/model predictions as applicable and reports mismatches rather than claiming successful reproduction.

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

- Installed-project integration, recorded outputs and failures mapped to these criteria.
- Use independently defined outcomes through installed public interfaces and separate experiment-project fixtures; follow small vertical red–green TDD slices.
- Follow the repository verification policy: current milestone at executable gates; M1–6 selection at story acceptance; preserve failures/skips and explicit authorization requirements for broader/artifact checks.

### Developer Validation

- Review criterion-mapped evidence, failures, artifact/run/data references and platform/tool identities.
- Record external assistant product/interface/version, scientist prompts, consequential actions/edits, commands/outcomes and independently checked MLflow/DVC outputs; no complete transcript or multiple-product claim is required.
- Preserve development approval gates and separate milestone verification obligations; do not infer runtime behavior from documentation.

## Dependencies / References

- [Authoritative user stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md).
- [Approved original scope dispositions and assistant walkthrough](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md).
- [Revision plan and approval history](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md).
- [Verification policy](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/development/verification.md#phase-and-story-verification).
- Supporting design 0.14 is the previous baseline until Phase 3 reconciliation; do not implement conflicting design/issue scope. Phase 4 must publish only against reconciled source documents.
