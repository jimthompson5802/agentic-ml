# Software blueprint IP5 evidence

Date: 2026-11-05 UTC. [Owning plan](../plans/software-blueprint.md).
Branch `embellish-software-component-descriptions`; baseline `df2d32a`.
Developer “i approve ip4; commit and start ip5” approved IP4 and authorized commit
before IP5. Commit completed first. No product code, dependency or schema changes.

## Sources and scope reconciliation

Retrieved full issue bodies #40–43, all comments using repository GET helper
`issues/N/comments --paginate --slurp`, then refreshed metadata. All reads succeeded;
zero unique comments each match reported counts, updated timestamps unchanged.
Issues assign M5 in bodies; GitHub milestone objects unset. Read local M5 criteria,
ADR exceptions, submission identity, recovery/reconciliation, state, approval,
tracking/provenance and agent cancellation/usage contracts, plus earlier blueprint.

Issue #40 retains authenticated authorship in US-23-AC-02. Local stories and
US-03-SC-01 expressly retain it as future scope while current experiment records
are unauthenticated. Blueprint accounts for required durable bindings now and
explicitly marks authentication as partial/deferred M5-D1, never satisfied.
#42's developer-only approval wording does not establish agent-resistant identity
under this exception. Existing actual access controls and all toolkit development
approval gates remain required. No issue/criterion wording altered or new scope
exception invented. No implemented orchestrator or second adapter present in src.

## Inventory and detail checklist

| Check | Evidence / result |
|---|---|
| Workflow types | WorkflowPhase alias, PhasePlan, WorkflowPlan, WorkflowStatus alias, PhaseProgress, WorkflowState, WorkflowStartRequest, WorkflowAdvanceRequest, WorkflowCancelRequest |
| Decision types | WorkflowScope, WorkflowGateRequest, WorkflowGate, WorkflowDecisionRequest, WorkflowDecision |
| Recovery types | RecoveryOwnership, OwnershipRequest, WorkflowCommit, SubmissionIntent, UsageMeasurement, WorkflowRecoveryRecord, RecoveryRequest, ReconciliationItem, RecoveryResult |
| Adapter types | AdapterRegistry, AdapterSelectionRequest, AdapterSelection; SecondManagedAgentAdapter explicitly reuses M4 constructor/five-method contract |
| Audit types | AuditEvent, WorkflowManifest, EvidenceReuseRecord, TrackingPublication, AuditLookupRequest, AuditLookupResult |
| Classes/protocols | WorkflowOrchestrator constructor and start/advance/inspect/cancel/recover; WorkflowStore and SQLiteWorkflowStore share constructor and read/claim_owner/renew_owner/commit; conceptual ApprovalService explicitly replaced by request_gate/decide_gate functions |
| Service functions | approvals.workflow.request_gate, approvals.workflow.decide_gate, agents.registry.select_adapter, tracking.audit.lookup, tracking.audit.finalize_publication: all typed signatures and observable/failure behavior |
| Errors | WorkflowError, WorkflowStoreError, WorkflowDecisionError, RecoveryError, AdapterSelectionError, AuditError: M1 code/message/evidence_ids signature, no operational methods |
| Detail | All 32 table types/aliases accounted for with exact fields, required/default/nullability rules, state/identity constraints, persistence and negative scenarios. Plain records expressly have no methods. Versioned envelopes, immutable snapshots and schema rejection use M1 conventions. |
| Reference closure | Reuse M1 EvidenceId/RecordId/ProjectContext/ArtifactRef/Diagnostic/ResourceLimits/ResourceUsage/AccessScope, M4 AgentIntegrationSpec/Capabilities/Usage and task/result/adapter contract, M3 ModelDecision and earlier runner/tracking evidence. New nested state/event/intent/measurement records all locally defined; no required M5 type silently deferred. Python Path/tuple/Literal are standard types. |
| Cross-milestone reconciliation | Separate SQLite workflow DB does not overwrite M1 JSON initialization state or mutate accepted schema identities. M1/M4 submission signatures retain intent-key gateway checks. M4 single-phase evidence expands into multi-phase recovery; producer provenance stays original. Second concrete integration remains M5-D2 selection/verification blocker, not claimed supported. |

## Criterion coverage and public scenarios

| Criterion | Contracts and required scenarios | Current design coverage |
|---|---|---|
| US-23-AC-01 | WorkflowPlan/PhasePlan, WorkflowGate and advance: initial approval, sufficient independent evidence, blocked pending gate | Specified |
| US-23-AC-02 | WorkflowDecision binds reviewer label, scope/configuration/plan, decision/time/evidence durably; reject tool permission as substitute | Partial: authenticated reviewer assurance explicitly deferred M5-D1 |
| US-23-AC-03 | WorkflowScope exact revision/return/change/criteria/access limits; wrong-scope/version denied | Specified |
| US-23-AC-04 | PhasePlan skip_artifacts and approved skip scope; missing/invalid artifacts cannot skip | Specified |
| US-23-AC-05 | Rejection/cancellation retain state/evidence; successful final evaluation still needs M3 ModelDecision | Specified |
| US-25-AC-01 | WorkflowState/RecoveryRecord, local SQLite transaction durability: progress/run/evidence/approval/budget/outcomes | Specified |
| US-25-AC-02 | Ownership epoch, WorkflowCommit, SubmissionIntent, ReconciliationItem, TrackingPublication: crash-window/concurrent recovery, no duplicates, pending gates blocked | Specified |
| US-25-AC-03 | WorkflowPlan/RecoveryRecord preserved configuration/bundle IDs: drift cannot substitute live guidance | Specified |
| US-25-AC-04 | Terminal status and unknown acceptance rules: preserve evidence/reservations, no silent restart | Specified |
| US-30-AC-06 | AdapterRegistry, first/second concrete adapter contracts, common task/result version | Specified; concrete product selection/verification remains blocked M4-D2/M5-D2 |
| US-30-AC-07 | AdapterSelectionRequest/Selection: reject unsupported capability before delegation | Specified |
| US-30-AC-08 | M4 adapter/guidance/cancel/access/usage contracts plus durable task/run reconciliation; no assistant-memory reliance | Specified with current unauthenticated approval limitation; no identity assurance claimed |
| US-30-AC-09 | Adapter selection cannot alter experiment criteria/boundaries/evaluator | Specified |
| US-26-AC-10 | WorkflowManifest joins runs, MLflow/DVC, configuration/bundles/decisions | Specified |
| US-26-AC-11 | AuditEvent and WorkflowScope/Decision preserve authorizing phase scope/change/evidence | Specified |
| US-26-AC-12 | AuditLookupRequest/Result, unique TrackingPublication and MLflow tags/reverse index | Specified |
| US-26-AC-13 | EvidenceReuseRecord keeps producer input/config/bundle/run separate from subsequent authorization | Specified |

## Verification and limitations

Document-only checks: inventory 32 table types, five services and nine shared
orchestrator/store methods; all 17 criterion mappings; local links/anchors,
Mermaid parser and `git diff --check`. Results: 67 local links/anchors, 32 types,
five functions, nine methods and all 17 criteria pass inventory checks, including
explicit partial authentication coverage. All five Mermaid fences parse and
whitespace passes. Diagrams parsed, not visually rendered.
No executable behavior, so no TDD/runtime
tests/artifact drivers/shared Python checks. SQLite durability/fencing and remote
publication reconciliation are proposals requiring fault-injection verification
through installed public boundaries before implementation acceptance.

No live workflows, remote writes, product selections, runtime authentication,
platform support or second-adapter evidence claimed. No suppression/lockfile
change; earlier evidence/deferrals preserved. IP5 documentation technically
complete. Developer approved IP5 with “i approve ip5”, recorded 2026-11-05 UTC.
IP6 remains unstarted pending execution authorization; no commit/push requested.
