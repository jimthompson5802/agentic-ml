# Software blueprint IP6 and final reconciliation evidence

Date: 2026-11-05 UTC. [Owning plan](../plans/software-blueprint.md).
Branch `embellish-software-component-descriptions`; IP5 baseline `0db2ded`.
Developer “commit then start ip6” authorized commit before IP6. IP5 was committed
first; no executable behavior, schema resource or dependency changes authorized.

## Requirements and scope

Retrieved #54–55 full bodies, all comment pages through repository GET helper
`issues/N/comments --paginate --slurp`, and refreshed metadata. All reads succeeded;
zero unique comments each equal reported count. updated_at stable: #54
2026-11-05T02:39:49Z; #55 2026-11-05T02:40:01Z. GitHub milestone objects unset;
bodies explicitly assign M6. Compared all 11 criteria to local stories; unchanged.
Read acquisition design, workflow/source-limit/lineage and deferred-strategy scope.
No new source conflict found. Earlier phase issue snapshots and decisions remain
in their owning reports; final criterion index uses those source references.

Initial acquisition is approved extraction/additional observations and bounded
targeted sampling. Synthetic/augmented source identification preserves lineage,
not a claim of advanced generation/active learning/labeling-service support.
No Milestone 99 capability introduced. Source pricing/record/compute/runtime
enforcement and external acceptance/retry semantics must be verified before
enabling a connector (M6-D1). No source contract is inferred from a generic class.

## Inventory, detail and reference closure

| Check | Evidence / result |
|---|---|
| Planning records | DataGapRequest, DataGapFinding, DataGapReport, AcquisitionLimits, AcquisitionStrategy, DataOrigin, AcquisitionProposalRequest, DataAcquisitionProposal |
| Execution records | AcquisitionApprovalRequest, AcquisitionApproval, AcquisitionRequest, AcquisitionLineage, AcquisitionResult, AcquisitionCancellation, AcquisitionAccounting |
| Comparison/loop records | AcquisitionComparisonProtocol, AcquisitionComparisonRequest, AcquisitionComparison, AcquisitionLoopPolicy, AcquisitionLoopRequest, AcquisitionLoopStep, AcquisitionLoopResult, AcquisitionResumeRequest |
| Protocols/concrete classes | DataAcquisitionPlanner diagnose/propose and DataAcquisitionExecutor execute typed request replacements; EvidenceBasedAcquisitionPlanner and ApprovedSourceAcquisitionExecutor explicitly share their respective constructor/method contracts, no unlisted public attributes |
| Service functions | approve_acquisition, cancel_acquisition, compare_acquisition, run_acquisition_loop, resume_acquisition_loop each has module ownership, typed signature and lifecycle/error behavior |
| Errors | AcquisitionError, AcquisitionApprovalError, AcquisitionComparisonError, AcquisitionRecoveryError follow M1 code/message/evidence_ids contract and have no operational methods |
| Required detail | All 23 table records, two protocols/three methods, two concrete class slots, four errors and five services accounted for. Required/default/nullable rules, immutable records, identity/schema/serialization, authority, persistent accounting, cancellation/recovery and negative cases explicit. |
| Reference closure | Reuse M1 ProjectContext/EvidenceId/RecordId/JSONValue/ArtifactRef/Diagnostic/ResourceLimits/ResourceUsage/DatasetRef/CheckResult; M2 MetricSpec/ReferenceEstimatorSpec; M5 WorkflowScope/Decision/RecoveryOwnership and durable intent/gate/accounting. New AcquisitionAccounting preserves compute ceilings without mutating ResourceUsage. No in-scope request/result/nested type deferred merely to complete inventory. |
| Cross-milestone reconciliation | Acquisition remains an activity inside the seven-phase workflow. Before/after comparison explicitly allows distinct training split IDs only under approved invariant development cohort/scoring/settings; no relaxation of M3 same-protocol comparison. No holdout feedback. Reuse original producer/run identities and current approval/accounting through M5 recovery. |

## M6 criterion coverage and future public scenarios

| Criterion | Contract and required public scenario |
|---|---|
| US-28-AC-01 | DataGapRequest/Finding/Report: known deficiencies in approved data and verified development evaluation; reject protected reports |
| US-28-AC-02 | DataAcquisitionProposal: reason/evidence/hypothesis/source/strategy/benefit/cost/limits/required scope preserved |
| US-28-AC-03 | benefit_is_hypothesis true, explicit rationale; outcome never guaranteed |
| US-28-AC-04 | Authorizations/WorkflowScope and proposal validation reject protected signals and unapproved access/protocol/budget expansion |
| US-29-AC-01 | AcquisitionApproval/Request: missing/wrong/stale source/strategy/scope/limit record blocks; no repetitive approval inside scope |
| US-29-AC-02 | AcquisitionLimits/Accounting and source preflight: hard cost/record/runtime/compute ceilings, consumed/uncertain usage retained |
| US-29-AC-03 | AcquisitionResult/Lineage, DataOrigin and M1 validation/DVC: source/version/hash and synthetic/augmented distinction; partial content not accepted |
| US-29-AC-04 | Current M5 return/assessment/downstream gate decision required, audit links preserved |
| US-29-AC-05 | AcquisitionComparisonProtocol/Request/Comparison: fixed validation cohort/metric/settings, independently known gain/tie/regression and before/after dataset links |
| US-29-AC-06 | LoopPolicy/Result: all success/exhaustion/stagnation/failure/policy/cancel conditions, reviewable partial outcomes and pending gate stop |
| US-29-AC-07 | ResumeRequest plus M5 ownership/reconciliation: preserved approvals/usage/data/bundle/run identities, no duplicate acquisition/accounting; advanced strategies deferred |

## Final M1–6 reconciliation

- [Coverage index](software-blueprint-final-coverage.md) enumerates every source
  criterion once: M1 49, M2 22, M3 35, M4 26, M5 17, M6 11; 160 total.
  Each links to owning issue, software owner, contract and public verification
  scenarios. US-23-AC-02 explicitly partial for authentication; integration and
  isolation limitations remain visible. Design coverage is not executable acceptance.
- Blueprint reconciles all original nine protocols with retained/replaced/extended
  contracts and owning milestones. No original protocol disappears silently.
- Open register names eight decisions/assurance gaps with owner, missing evidence
  and blocked behavior: source/execution, protected test, assistant/kernel,
  first/second product, authentication and acquisition source limits/retry safety.
- Existing initialization/planning/approval/validation APIs remain unchanged.
  Public source record inventory is 27 existing model/error classes; private
  ProjectAccess and InputError remain intentionally outside public blueprint scope.
- Design 0.14 updates overview/date/reading map, links topic documents and removes
  stale “toolkit/CLI still require implementation” and settled name/URL statements.
  Exact reviewed APIs/persistence now link to blueprint; old examples are identified
  as illustrative and not competing schema authority. Repository resource paths
  distinguish current packaged src locations from historical proposed tree.
- ADR references describe approved documentation slices, not wholesale pending-ADR
  acceptance. Existing development gates, historical failures, platform limitations,
  deferred assurance and separate milestone acceptance obligations preserved.

## Document verification and limitations

Final checks: relative links/anchors for changed design/plan/reports; inventory
and criterion index equality against source; all nine protocols; all six Mermaid
fences through cached parser; `git diff --check`; product/lockfile diff inspection.
Results: 889 relative links/anchors pass across overview, all topic documents,
plan, IP6 evidence and coverage index. All 23 M6 table records, five services and
three protocol methods match the inventory. Coverage index equals all 160 unique
source criteria exactly once, preserving M5-D1's partial assurance. All nine
conceptual protocols appear in the disposition table; all 27 public source
model/error classes are referenced, with only the two private helpers excluded.
All six Mermaid fences parse with cached Mermaid; `git diff --check` passes.
Tracked product/dependency/lock diff is empty; all edits are documentation.
No runtime/model/framework/source
or platform tests: documentation-only work has no new executable behavior, so TDD,
product pytest/artifact drivers and Python shared checks are inapplicable under
repository verification policy. Diagrams parsed, not visually rendered.

IP6-T1–T6 are technically complete; developer approved IP6 with “i approve ip6”,
recorded 2026-11-05 UTC. All documentation phase gates are now approved.
No product
story/milestone acceptance, live integration/connector support, authenticated
reviewer protection or external publication claimed. No IP6 commit/push/PR requested.
