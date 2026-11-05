# Software blueprint IP3 evidence

Date: 2026-11-04. [Owning plan](../plans/software-blueprint.md).
Branch `embellish-software-component-descriptions`; baseline IP2 commit `4d38afd`.
Developer “i approve ip2, commit then start ip3” approved IP2 and authorized
commit before IP3; commit completed first. No product code/dependencies changed.

## Source reconciliation

Retrieved complete issue bodies #26–33, every comment page using repository GET
helper `issues/N/comments --paginate --slurp`, and refreshed metadata. Every
request succeeded, all zero unique comments match reported counts, timestamps
stable. GitHub milestone objects unset; bodies assign M3. updated_at timestamps
on 2026-10-30: #26 03:40:49Z, #27 03:40:50Z, #28 03:40:52Z,
#29 03:40:53Z, #30 03:40:55Z, #31 03:40:56Z, #32 03:40:57Z,
#33 03:40:59Z. Read local M3 requirements, conceptual ModelAdapter/Evaluator,
checkpoint-restoration contract, execution/independent evaluation/governance and
ADR exceptions. Source inventory has no implemented M3 model/evaluator APIs.

#32 dependency prose retains authenticated approval wording. Recorded developer
US-03-SC-01 and current ADR-006 explicitly supersede that assurance for the current
experiment version; blueprint preserves unauthenticated reviewer labels and future
US-23-AC-02 as undelivered. No issue body or acceptance criterion was edited.
Actual protected-test isolation remains mandatory, with M3-D1 naming its blocked
implementation mechanism. Checkpoint scope follows #29: declared-state usability,
not guaranteed exact training continuation.

## Inventory and detail checklist

| Check | Evidence / result |
|---|---|
| Record inventory | ModelSpec, ModelRegistrationRequest, ModelRegistry, AlgorithmSelectionRequest, AlgorithmSelection, SearchRecommendation; ComputeRequest, ComputeObservation, TrainingRequest, TrainingContext, FittedModel, PredictionResult, TrainingResult, ModelRestoreRequest, CheckpointRecord, CheckpointRestoreRequest, CheckpointRestoration; BaselineApprovalRequest, BaselineApprovalRecord, TuningRequest, TrialRecord, OptimizationSummary; EvaluationCheckSpec, AcceptanceCriteria, EvaluationRequest, EvaluationReport, FinalEvaluationApprovalRequest, FinalEvaluationApproval, FinalEvaluationRequest, ModelDecisionRequest, ModelDecision; RunComparisonRequest, RunComparison, FinalReportRequest, FinalReport. All 35 have field/type/constraint definitions. |
| Protocols and concrete classes | Typed ModelAdapter replacement with train/predict/save/load; CheckpointRestorer.restore_checkpoint. SklearnModelAdapter, LightGBMModelAdapter, PyTorchModelAdapter have explicit common constructor/method contract; PyTorch adds checkpoint restoration. Evaluator is explicitly proposed to be replaced by separate development/final services, not claimed unchanged. |
| Functions | register_models, select_algorithms, train_model, restore_model, restore_checkpoint, approve_baseline, tune_models, evaluate_model, authorize_final_evaluation, evaluate_final, decide_model, compare_runs, build_final_report. Each has typed request/result and module owner in blueprint. |
| Errors | ModelError, SelectionError, CheckpointError, TuningError, EvaluationError, ReportError follow explicit M1 constructor/attributes; safe diagnostics, evidence preservation and operational failures described. |
| Detail standard | Required/no-default/nullable rules, immutable descriptors versus worker-private instances, versioned evidence serialization, producer identity, persistence, approvals, effects and lifecycle defined. Records have no methods; protocols do. Future verification includes negative/boundary cases. |
| Reference closure | Reuse M1 EvidenceId/RecordId/ArtifactRef/JSONValue/Diagnostic/RunStatus/RunRecord/ResourceUsage/CheckResult and M2 ProjectContext notation, ParameterSpec/TransformResult/MetricSpec/FeatureSetRef/split/fitted-state evidence. CandidateRequest/Result stay M1 validation interfaces. EvaluationCheckSpec defines nested robustness/reproduction inputs. Python Path/Mapping/Protocol/Literal/tuple are standard types. No required M3 type deferred to make checklist pass. |
| Cross-milestone consistency | M2 preprocessing ComponentSpec remains unchanged; ModelSpec is separate. Fixed M2 ReferenceEstimator does not gain tuning authority. M1 runner/admission and common validation remain mandatory for every trial. Extra M3 evidence is versioned separately from accepted schemas. Old Any-based model/evaluator conceptual protocols explicitly reconciled. |

## Criterion coverage and required public scenarios

Ranges include each criterion in order; all 35 criteria are mapped. This is
documentation coverage, not verification of implemented behavior.

| Criteria | Contracts and scenarios |
|---|---|
| US-06-AC-01–04 | AlgorithmSelectionRequest/Selection: use/select/compare and partial coverage; common task/budget validation; finite non-exhaustive TuningRequest candidates; SearchRecommendation never mutates active bounds |
| US-16-AC-06–10 | ModelSpec/RegistrationRequest/Registry: project/pinned models without toolkit changes; ModelAdapter training/prediction/save/load and restore_model; reject task/parameter/signature/output mismatches before training; tune then independently restore/evaluate; FittedModel preserves declarations/code/parameters/artifacts |
| US-18-AC-01–04 | Framework adapters and TrainingRequest/Result: tabular classification/regression plus PyTorch image fixtures; BaselineApprovalRecord before candidate comparisons; common train/predict/persist operations; FittedModel/compute/MLflow evidence records parameters/library/model/feature/data identities |
| US-19-AC-01–04 | ComputeRequest/Observation: CPU and available GPU, no implicit fallback; CheckpointRecord/Restorer usability checks; M1 cancel preserves emitted checkpoints/logs/status including forced kill; hardware and enforced/unsupported quotas explicit |
| US-20-AC-01–04 | TuningRequest/TrialRecord: fixed/default/category/range constraints and common validate_candidate through notebook/custom code; atomic aggregate budget admission, stop/preserve summaries; OptimizationSummary search/usage/evaluation/model proposal |
| US-21-AC-01–05 | EvaluationRequest/AcceptanceCriteria/Report: independent execution/artifacts; split/fitting/leakage checks; known metrics/baseline directions; EvaluationCheckSpec folds/slices/stress/repeats with tolerances; separate execution/scientific validity/model quality including failures and missing evidence |
| US-24-AC-01–05 | M3-D1 arbitrary code/kernel/tool denial; scoped FinalEvaluationApproval/Request evaluator-only access; final-report delivery excluded from development inputs; unsuccessful final reject/review and separately approved continuation; ModelDecision explicit approve after sufficient successful final evidence |
| US-26-AC-06–09 | RunComparisonRequest/Comparison: MLflow params/status/metrics/models; FinalReportRequest/Report objective/baseline/validity/robustness/repro/acceptance; FittedModel→features→datasets→code/config/environment lineage; independent evidence references remain authoritative over generated narrative |

## Verification and limits

Documentation-only: TDD, product tests, artifact drivers and Python shared checks
inapplicable because no executable behavior changes. At gate, verify local
links/anchors, 35 table type inventory entries, 13 service signatures, all 35
criterion references and Mermaid parser for all three diagrams; run whitespace
check. Results: 60 local links/anchors, 35 table types, 13 services and all 35
criteria pass inventory checks; all three Mermaid fences parse; `git diff --check`
passes. No renderer or platform/runtime/model-quality evidence claimed. Earlier
executable evidence/deferrals unchanged. No new suppressions or lockfile changes.
Developer review must confirm these proposed public boundaries; owning story plans
must use TDD and milestone verification before executable implementation.

IP3 technically complete; approval pending. Stop before IP4. No IP3 commit or push.
