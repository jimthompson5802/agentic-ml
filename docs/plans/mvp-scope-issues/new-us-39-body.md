## User Story

As a data scientist, I want a coding assistant to help prepare, run, inspect and revise an experiment through installed public interfaces so that I can reach recorded results quickly.

## Description

Delivery: M1 and M2. No implementation acceptance is claimed.

US-10/11/12/13/14/15/18/20/21/24/26/27 supply M1 components; US-09/16/18 supply M2 notebook/custom/regression extensions. M1 owns AC-01–08; M2 owns AC-09–11. US-39 covers ASW-01–06/08.

This integration story references component criteria instead of duplicating implementation ownership.

Scope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by
“i approve gate 1 and authorize phase 2”. This scope revision does not claim
new implementation acceptance. Preserve the scope-decision comment and original
issue history.

## Acceptance Criteria

- [ ] **US-39-AC-01:** Starting from a separate experiment project, documented initialization and pinned installation provide a runnable local classification example without a neighboring toolkit checkout, manual draft-schema migration, managed agent adapter or toolkit source edits.
- [ ] **US-39-AC-02:** The basic experiment path accepts explicit objectives, data, metric and search settings, validates them before training and does not require formal plan resolution or delegated-decision approvals. Existing explicit planning, approval and validation APIs retain their documented strict behavior.
- [ ] **US-39-AC-03:** A scientist-directed external coding-assistant session prepares project configuration and extraction/preprocessing code, invokes installed public toolkit interfaces and native DVC stages, and locates MLflow results without private toolkit imports.
- [ ] **US-39-AC-04:** The classification walkthrough completes extraction, quality/split checks, training-only preprocessing, baseline training and bounded tuning, then exposes MLflow parameters, validation metrics and fitted artifacts linked to DVC inputs and committed configuration/code references.
- [ ] **US-39-AC-05:** Before final testing, the scientist directs at least one assistant-authored feature or parameter revision using validation evidence; a recorded rerun compares the change using consistent splits and metric. Gains, ties and regressions are valid outcomes; final-test feedback is not used for the revision.
- [ ] **US-39-AC-06:** After selection, the walkthrough executes the separate final-test step, saves the selected fitted pipeline/model and metrics, and reports the result without silently retuning from final-test scores. Quality shortfalls and execution failures are distinguishable.
- [ ] **US-39-AC-07:** Walkthrough evidence identifies at least one external assistant product, interface and version, scientist prompts, consequential edits/actions, commands/outcomes and independently checked MLflow/DVC references. A complete transcript and multiple assistant products are not required.
- [ ] **US-39-AC-08:** Installed-project checks demonstrate invalid configuration or candidate parameters and missing required local inputs fail clearly with available diagnostics, rather than being reported as a completed successful experiment.
- [ ] **US-39-AC-09:** A tabular regression example completes the same installed-project workflow and records its baseline, candidate and final evaluation results in MLflow with DVC/code/configuration references.
- [ ] **US-39-AC-10:** A customization example uses compatible project-owned preprocessing and estimator code through supported scikit-learn interfaces, preserves/restores fitted artifacts and records results without toolkit modification or a general component registry.
- [ ] **US-39-AC-11:** The scientist-directed assistant walkthrough includes a saved notebook example executed in the project environment from a fresh kernel, with explicit paths/inputs, preserved outputs/errors and recorded artifact references instead of hidden cross-kernel state.

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
