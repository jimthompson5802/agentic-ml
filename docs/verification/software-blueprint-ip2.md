# Software blueprint IP2 evidence

Date: 2026-11-04. [Owning plan](../plans/software-blueprint.md).
Branch: `embellish-software-component-descriptions`; IP1 baseline `a475835`.
Developer “i approve ip1, coomit firs then move to ip2” approved IP1 and
authorized its commit before IP2. Commit completed before any M2 document edits.
No IP2 publication or executable implementation is authorized or claimed.

## Source reconciliation

Retrieved #19–23 full bodies, all comment pages via repository GET helper
`issues/N/comments --paginate --slurp`, then refreshed metadata. Each discussion
returned zero unique comments, equal to metadata; all requests succeeded.
Stable updated_at values: #19 `2026-10-30T02:10:21Z`, #20 `02:10:23Z`,
#21 `02:10:24Z`, #22 `02:10:25Z`, #23 `02:10:27Z` (same date).
GitHub milestone objects unset; bodies explicitly assign M2.
Read data/features, supplied-component contracts, delivery/ADR constraints,
M2 local acceptance criteria and accepted M1 blueprint. Issues and local criteria
agree. Existing src inventory has no implemented M2 component/feature/split APIs.

Proposed contracts preserve fixed reference-estimator comparisons in M2, authored
candidates without agents, immutable supplied code, training-only fitting and
independent scoring. Broader training/tuning and final holdout evaluation remain
M3. M1 accepted contracts are not migrated or silently extended. M2-D1 records
the unresolved protected-test enforcement mechanism and blocks affected product
implementation, not documentation review. No full ADR acceptance is implied.

## Completion checklist

| Check | Evidence and result |
|---|---|
| Public inventory | AssessmentRequest, AssessmentFinding, DatasetAssessment, SplitRequest, PartitionRef, SplitManifest, AssessmentApprovalRequest, AssessmentApprovalRecord; ParameterSpec, ComponentSpec, RegistrationRequest, ComponentRegistry, DataPartition, TransformResult, FittedComponent, PreprocessingRestoreRequest; FeatureStep, FeaturePlan, FeatureExecutionRequest, FeatureSetRef, ReferenceEstimatorSpec, MetricSpec, FeatureComparisonProtocol, FeatureApprovalRequest, FeatureApprovalRecord, ReferenceFitResult, FeatureComparisonRequest, FeatureEvaluationReport; PipelineStage, PipelineDefinition, StageRequest, StageResult, StageReuseRecord. All defined in M2 tables. |
| Protocols and errors | StatefulPreprocessor, StatelessTransformation and ReferenceEstimator have construction/method signatures and state/error semantics. AssessmentError, SplitError, ComponentError, FeatureError and PipelineError use explicitly defined common constructor/attributes. FeatureEngineeringAdapter is explicitly refined into authored-plan/execution/comparison services; FeatureContext mapped to preserved references. |
| Detail | Required fields/types, no-default rule, nullable constraints, immutable records versus mutable fitted instances, versioned serialization, content/producer identity, storage ownership, approval scope and public negative scenarios documented. Data records expressly have no behavioral methods. Component execution/persistence methods explicitly differ from service admission. |
| Reference closure | EvidenceId, RecordId, ArtifactRef, Diagnostic, JSONValue, ProjectContext, ResourceUsage, CheckResult, OutputCheck, ExecutionAssessment and M1 runner are reused from M1 definitions. Path/Mapping/tuple/Literal/Protocol are Python standard types. No in-scope M2 record is deferred merely to complete inventory. M3 model/tuning/final evaluation, M4 agent generation and M5 recovery are explicit scope exclusions. |
| Cross-milestone consistency | Separate M2 evidence bundles preserve accepted M1 schema identities. Same current authorization/reservation, captured source, environment and provenance rules apply. M2-D1 strengthens M1-D1 for sealed holdout protection, including metadata/cache exposure. Authenticated reviewers remain deferred; ordinary records alone cannot enforce isolation. |
| Criterion coverage | Matrix below maps all 22 M2 criteria to software and public verification scenarios. This is design traceability, not executed acceptance evidence. |

## Criterion traceability

| Criteria | Software contracts | Required public scenarios |
|---|---|---|
| US-12-AC-02 | AssessmentRequest/Finding, DatasetAssessment, assess_dataset | Independently known distributions, classification counts, anomalies and leakage findings; blocked assessment |
| US-12-AC-03 | SplitRequest, PartitionRef, SplitManifest, create_split | Exact membership, disjoint coverage, time/group constraints, source/hash/version drift |
| US-12-AC-04 | AssessmentApprovalRequest, AssessmentApprovalRecord, approve_assessment | Missing/wrong/stale scope prevents dependent feature work |
| US-14-AC-01 | FeatureStep/Plan, ComponentSpec | Order, schemas, fixed parameters, fit scope and permissions |
| US-14-AC-02 | FeatureExecutionRequest, FeatureSetRef, execute_features | Managed transformations with definitions/dependencies/outputs/lineage |
| US-14-AC-03 | ReferenceEstimator/Spec, MetricSpec, comparison protocol/request/approval/report | Fixed baseline/settings/split, independent gain/tie/regression, both directions, budget exhaustion |
| US-14-AC-04 | FeatureSetRef checks, FeatureEvaluationReport, M1 run evidence | Wrong dataset/split/producer, invalid artifacts, independent validity checks before advancement |
| US-14-AC-05 | Authored FeaturePlan and explicit execute/compare services | Complete feature comparison without an agent adapter |
| US-15-AC-01 | StatefulPreprocessor, DataPartition, FittedComponent | Training-only fitted statistics and unchanged validation/inference transforms |
| US-15-AC-02 | Feature service admission and M2-D1 | Reject wrong partition fit, target leakage and custom-code/kernel bypasses |
| US-15-AC-03 | FittedComponent, ComponentSpec, FeaturePlan, M1 manifests | Exact code/state/dependencies/parameters/schema evidence |
| US-15-AC-04 | PreprocessingRestoreRequest, restore_preprocessing | Independent restored transforms within declared tolerances, corrupt/missing state |
| US-16-AC-01 | RegistrationRequest, ComponentRegistry, register_components | Separate project and pinned-dependency wrappers, no toolkit edits |
| US-16-AC-02 | ComponentSpec, ParameterSpec, registry | Duplicate IDs, incompatible signatures/versions, invalid params/defaults |
| US-16-AC-03 | StatefulPreprocessor, StatelessTransformation, TransformResult | Fit/transform/save/load and stateless output schema consistency |
| US-16-AC-04 | M1 resource controls plus M2-D1 and component loading boundary | Same access/resource/leakage controls for supplied/built-in components |
| US-16-AC-05 | ComponentSpec, FittedComponent, producer references | Declarations, exact code/lock identities and effective state preserved |
| US-27-AC-05 | PipelineDefinition/Stage, StageResult | dvc.yaml dependencies/params/outputs and resolved dvc.lock hashes |
| US-27-AC-06 | Stage cwd/path rules | DVC/toolkit agree on resolution; traversal and escaping cwd rejected |
| US-27-AC-07 | StageRequest, reproduce_stage | Authorized restoration or managed execution, checked expected outputs |
| US-27-AC-08 | StageReuseRecord, StageResult | Original producer retained, current authorization/evaluation required |
| US-27-AC-09 | Reuse admission and independent approval gates | Cache hit never approves experiment or bypasses pending gate |

## Verification and limitations

Document checks only under repository verification policy: no executable behavior,
so TDD, product pytest, artifact drivers and shared Python checks do not apply.
Cached Mermaid parser executed against both blueprint diagram fences: both pass.
Local checks pass: 48 link/anchor targets, 33 table type definitions and 22
criterion entries; `git diff --check` passes. Initial inventory probe failed because
the report abbreviated paired Request/Record names; expanded both names explicitly
and reran the original check successfully (attempt 1). This changed evidence
notation, not contract coverage or assertions. Refreshed #22 timestamp against
metadata and corrected transcription to 02:10:25Z.
Diagrams parsed, not visually rendered. No new platform support,
runtime leakage enforcement, restored artifacts or scientific correctness is
verified by these document checks. No dependencies or lockfile changes.

IP2 technically complete; developer approval pending. Stop before IP3.

Review wording correction at developer request: replaced ambiguous “refined”
language for FeatureEngineeringAdapter with an explicit proposed replacement
mapping for propose/transform/evaluate and FeatureContext. This documents an
interface change, not conformance to the original protocol. No executable change
or progression to IP3; IP2 approval remains pending. Whitespace check renewed.
