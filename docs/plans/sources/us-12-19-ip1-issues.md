# IP1 issue and supplier discussion refresh

Retrieved 2026-11-07 UTC for US-12 #19 contract review. Complete bodies and all
comments are below. Each final metadata refresh matched the initial update time
and reported count; all three are issues, not pull requests. Each had one unique
comment across all pages. Linked attachments/timeline/reactions were not fetched.

## Issue #19: US-12: Assess data quality and define splits

- URL: https://github.com/jimthompson5802/agentic-ml/issues/19
- State: open
- Author: jimthompson5802
- Created: 2026-10-30T02:10:21Z
- Updated: 2026-11-07T21:38:29Z
- Milestone: unset; body assigns M1
- Labels: enhancement
- Assignees: none
- Comments: 1; completeness/stability checks passed.

### Complete body

## User Story

As a data scientist, I want to check data quality and record distinct partitions so that training and evaluation use suitable inputs.

## Description

Delivery: M1. No implementation acceptance is claimed.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-12-AC-02: M1; US-12-AC-03: M1; US-12-AC-04: deferred.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Split-layout scope alignment — 2026-11-07

Developer requested support for both two-way (train/test) and three-way
(train/validation/test) splitting and authorized alignment of this issue,
US-12-AC-03 and the supporting design. This adds two-way support while retaining
three-way and supplied time/group partition requirements. The original AC-03
required recorded seeded train/validation/test partitions and explicit supplied
partitions with membership/disjointness checks. Its ID and the earlier scope
decision/comment remain preserved. No implementation acceptance or development
gate approval is claimed by this alignment.

## Acceptance Criteria

- [ ] **US-12-AC-02:** Provide basic distributions, missingness and classification target balance.
- [ ] **US-12-AC-03:** Support two-way (train/test) and three-way (train/validation/test) layouts for seeded generation and explicit user-supplied partitions, including time/group problems; record the selected layout and exact row membership, and check row membership/disjointness. Two-way layouts do not require a validation partition.

### Deferred original criteria — not MVP requirements

- [ ] **US-12-AC-04:** Dataset assessment and split protocol are presented for approval before dependent feature or modeling work.

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
- The explicitly deferred original criteria above remain roadmap work, not completed or removed history.

## Implementation Phase

**Phase:** Not specified. Define story/milestone implementation phases and granular tasks in a separate owning plan.

**Deliverables:** The assigned milestone outcomes and criterion-mapped evidence above.

**Developer Validation:** Confirm public test boundaries before executable tests. Stop at every implementation phase gate, including the final gate, for explicit developer approval.

**Exit Criteria:** Verify the assigned criteria; phase approval and whole-story/milestone acceptance remain distinct. Written-plan approval does not approve implementation gates.

## Validation Approach

### Automated Validation

- Configured data quality checks; seeded and supplied two-way and three-way membership, including time/group-aware cases; disjointness, selected-layout round-trip and layout/membership mismatch failures.
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
- [Active MVP design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md) defines the revised trusted-local scope; archived 0.14 platform contracts are historical reference. Synchronize issue scope and the reviewed source revision before product implementation.



### Comment 6699588996 — jimthompson5802

Created 2026-11-07T00:28:54Z; updated 2026-11-07T00:28:54Z.
[Direct comment](https://github.com/jimthompson5802/agentic-ml/issues/19#issuecomment-6699588996)

MVP scope decision MVP-SC-01/MVP-SC-02 — 2026-11-06

Gate 2 was subsequently approved by “I approve gate 2 and authorize phase 3”; this records scope/design context, not new executable acceptance.

Developer “i approve gate 1 and authorize phase 2” approved the criterion dispositions and milestone migration. The revised body preserves original IDs and distinguishes active outcomes from deferred scope. The issue remains open; no criterion is newly verified by this edit.

Assignments: US-12-AC-02: M1; US-12-AC-03: M1; US-12-AC-04: deferred.

[Original criterion text and displaced guarantees](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md#criterion-level-disposition-matrix) remain review history. [Revised stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md) govern the new delivery scope after synchronized publication. Existing development/testing gates and historical verification obligations remain unchanged. Managed security, approvals, recovery and broader platform capabilities are deferred only as recorded in the approved matrix.


## Issue #14: US-11: Extract local experiment data

- URL: https://github.com/jimthompson5802/agentic-ml/issues/14
- State: closed
- Author: jimthompson5802
- Created: 2026-10-30T02:06:27Z
- Updated: 2026-11-07T12:02:00Z
- Milestone: unset; body assigns M1
- Labels: enhancement
- Assignees: none
- Comments: 1; completeness/stability checks passed.

### Complete body

## User Story

As a data scientist, I want to prepare local CSV/Parquet files using selection, filtering and joins so that I can start with traceable data.

## Description

Delivery: M1. No implementation acceptance is claimed.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-11-AC-01: M1; US-11-AC-02: M1; US-11-AC-03: M1; US-11-AC-04: M1; US-11-AC-05: M1.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-11-AC-01:** Read local CSV/Parquet and support configured column selection, filtering and joins; permit project-owned extraction functions.
- [ ] **US-11-AC-02:** Report local source schemas and metadata needed for extraction.
- [ ] **US-11-AC-03:** Execute explicitly configured local extraction operations and report their configuration.
- [ ] **US-11-AC-04:** Record source paths/content identities, extraction settings and time, and output checksum/DVC reference.
- [ ] **US-11-AC-05:** Extraction failures are reported without presenting incomplete output as a validated dataset.

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

- CSV/Parquet, configured columns/filter/join behavior and deterministic expected outputs; missing/invalid sources fail.
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
- [Active MVP design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md) defines the revised trusted-local scope; archived 0.14 platform contracts are historical reference. Synchronize issue scope and the reviewed source revision before product implementation.


### Comment 6699585176 — jimthompson5802

Created 2026-11-07T00:28:37Z; updated 2026-11-07T00:28:37Z.
[Direct comment](https://github.com/jimthompson5802/agentic-ml/issues/14#issuecomment-6699585176)

MVP scope decision MVP-SC-01/MVP-SC-02 — 2026-11-06

Gate 2 was subsequently approved by “I approve gate 2 and authorize phase 3”; this records scope/design context, not new executable acceptance.

Developer “i approve gate 1 and authorize phase 2” approved the criterion dispositions and milestone migration. The revised body preserves original IDs and distinguishes active outcomes from deferred scope. The issue remains open; no criterion is newly verified by this edit.

Assignments: US-11-AC-01: M1; US-11-AC-02: M1; US-11-AC-03: M1; US-11-AC-04: M1; US-11-AC-05: M1.

[Original criterion text and displaced guarantees](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md#criterion-level-disposition-matrix) remain review history. [Revised stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md) govern the new delivery scope after synchronized publication. Existing development/testing gates and historical verification obligations remain unchanged. Managed security, approvals, recovery and broader platform capabilities are deferred only as recorded in the approved matrix.


## Issue #15: US-12: Validate extracted data

- URL: https://github.com/jimthompson5802/agentic-ml/issues/15
- State: closed
- Author: jimthompson5802
- Created: 2026-10-30T02:06:28Z
- Updated: 2026-11-07T17:40:12Z
- Milestone: unset; body assigns M1
- Labels: enhancement
- Assignees: none
- Comments: 1; completeness/stability checks passed.

### Complete body

## User Story

As a data scientist, I want to check data quality and record distinct partitions so that training and evaluation use suitable inputs.

## Description

Delivery: M1. No implementation acceptance is claimed.

Original criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.

Criterion assignment: US-12-AC-01: M1; US-12-AC-05: M1.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-12-AC-01:** Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.
- [ ] **US-12-AC-05:** Report validation results and block supported pipeline steps when configured required checks fail.

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

- Configured data quality checks, split disjointness, seeded membership and supplied time/group-aware partition cases.
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
- [Active MVP design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md) defines the revised trusted-local scope; archived 0.14 platform contracts are historical reference. Synchronize issue scope and the reviewed source revision before product implementation.


### Comment 6699586004 — jimthompson5802

Created 2026-11-07T00:28:41Z; updated 2026-11-07T00:28:41Z.
[Direct comment](https://github.com/jimthompson5802/agentic-ml/issues/15#issuecomment-6699586004)

MVP scope decision MVP-SC-01/MVP-SC-02 — 2026-11-06

Gate 2 was subsequently approved by “I approve gate 2 and authorize phase 3”; this records scope/design context, not new executable acceptance.

Developer “i approve gate 1 and authorize phase 2” approved the criterion dispositions and milestone migration. The revised body preserves original IDs and distinguishes active outcomes from deferred scope. The issue remains open; no criterion is newly verified by this edit.

Assignments: US-12-AC-01: M1; US-12-AC-05: M1.

[Original criterion text and displaced guarantees](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md#criterion-level-disposition-matrix) remain review history. [Revised stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md) govern the new delivery scope after synchronized publication. Existing development/testing gates and historical verification obligations remain unchanged. Managed security, approvals, recovery and broader platform capabilities are deferred only as recorded in the approved matrix.
