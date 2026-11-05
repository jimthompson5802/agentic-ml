# Software blueprint IP4 evidence

Date: 2026-11-04. [Owning plan](../plans/software-blueprint.md).
Branch `embellish-software-component-descriptions`, IP3 baseline `7b00662`.
Developer “i approve ip3; commit and start ip4” approved IP3 and authorized commit
first. Commit completed before IP4 edits. No executable implementation or new
integration support is claimed.

## Source reconciliation

Retrieved #34–39 full bodies, all comment pages through repository GET helper
`issues/N/comments --paginate --slurp`, and refreshed metadata. All reads succeeded;
zero unique comments each equals reported count, timestamps unchanged. Milestone
objects unset; bodies explicitly assign M4. Read M4 acceptance criteria, runtime
guidance and audience boundary, AgentAdapter conceptual protocol, notebook/editor,
agent cancellation/usage/resumption contracts, governance and earlier blueprint.
Source inventory contains provisional guidance only, no implemented managed adapter.

#37 scope/test prose retains authenticated approval and rejection of agent-authored
approvals. Recorded developer US-03-SC-01 and ADR-006 supersede that assurance for
this experiment version: scoped records remain unauthenticated, workspace writers
can fabricate history. This does not relax actual immutable-source/access controls
or toolkit development gates. Current issue ACs are preserved; no issue edits.
No other scope conflict found. Complete workflow recovery/second adapter is M5.

## Inventory, detail and reference closure

| Check | Result |
|---|---|
| Guidance types | GuidanceSource, GuidanceSelectionRequest, PreservedGuidance, GuidanceConflict, RuntimeInstructionBundle, GuidanceSelectionResult, ExternalContextRecord, GuidanceDeliveryReceipt all defined with exact fields/order/snapshot/delivery and capture limitations |
| Agent types | AgentIntegrationSpec, AgentCapabilities, AgentTask, AgentBudget, AgentUsage, AgentTaskStatus alias, AgentTaskHandle, AgentResult, AgentCancellation defined with task/attempt bindings, capability/usage limits and separate run cancellation |
| Decision/revision types | DecisionProposal, DecisionProposalRequest, DecisionProposalResult, ProposedFileChange, NotebookRevisionRequest, NotebookRevision, ComponentChangeRequest, ComponentChangeApproval defined with exact-scope hashes, proposed plan lineage and current permissions |
| Interactive/iteration types | InteractiveKernelRequest, InteractiveKernelSession, DevelopmentFeedback, IterationPolicy, IterationRequest, IterationStep, IterationResult defined, including externally supplied iteration UUID for cancellation before blocking call returns |
| Protocol and concrete slot | AgentAdapter proposed replacement exposes capabilities/submit/status/result/cancel with five typed methods; FirstManagedAgentAdapter has explicit constructor/common method contract. Concrete product/version selection is M4-D2, not falsely claimed verified. |
| Functions | select_guidance, inspect_bundle, record_proposals, approve_component_change, apply_revision, start_kernel, stop_kernel, prepare_feedback, improve_experiment, cancel_iteration have module ownership and typed signatures |
| Errors | GuidanceError, AgentError, DecisionError, RevisionError, ComponentPermissionError, InteractiveError, IterationError use M1 code/message/evidence_ids constructor and explicit failure/evidence semantics |
| Required detail | All 32 table types (including status alias) plus protocol/concrete adapter slot/errors accounted for. Required/default/nullable constraints, immutable records, serialized identity envelopes, persistent scope/accounting, effects/lifecycle and verification scenarios specified. No behavioral methods on plain records. |
| Reference closure | Reuse M1 EvidenceId, RecordId, ArtifactRef, Diagnostic, JSONValue, ProjectContext, PlanResult, approval/plan/validation and runner services. Reuse M3 development EvaluationReport/CheckResult and train_model; no final report allowed in feedback. Standard Path/Mapping/tuple/Literal/Protocol are Python types. Every M4 request/result/nested record is locally defined or referenced; no required record deferred merely to satisfy coverage. |
| Cross-milestone reconciliation | M1 guidance refs remain valid, M4 adds separate versioned loader/delivery evidence. Proposed synchronous AgentAdapter.execute is explicitly replaced, not claimed conformed to unchanged. Full M5 state/fencing and second adapter are deferred; M4 task identities, budgets, safe cancellation and uncertainty stopping still required. |

## Criterion coverage and public verification scenarios

Inclusive ranges enumerate all 26 M4 criteria; these are future test boundaries,
not executed product acceptance.

| Criteria | Contract / required scenario |
|---|---|
| US-04-AC-01–04 | DecisionProposal and record_proposals: delegated fields only with rationale; resolver/FeaturePlan/selection/criteria retain features/metric/direction/split/algorithms/budgets; ambiguous or unapproved plans block; original/proposed source identities retained |
| US-07-AC-01–04 | NotebookRevision/apply_revision: explanatory Markdown/tagged parameters; installed toolkit/project imports; saved fresh-kernel replay and helper capture; boundary rejects toolkit/unauthorized writes |
| US-08-AC-01–04 | InteractiveKernelRequest/Session/start/stop: declared project environment and manual VS Code versions; arbitrary Python protected-data denial; common managed training admission/budgets/tracking; interactive completion grants no acceptance |
| US-17-AC-01–04 | ComponentChangeRequest/Approval and expected-before hashes: immutable default; unauthorized direct writes denied; approved change yields new configuration; modification does not expand algorithm/parameter/data/evaluation permissions, and code captured |
| US-22-AC-01–05 | DevelopmentFeedback, IterationRequest/Policy/Step/Result: evidence-based revision; same approved phase/permissions/budgets; each revision captured/managed/evaluated; success/exhaustion/stagnation/failure/policy/cancel stops; phase returns wait and protected feedback rejected |
| US-30-AC-01–05 | AgentIntegrationSpec/Capabilities/Task/Result/Adapter: exact product/interface/version plus task→revision→execution→feedback→gate; explicit shared/task/project guidance mapping/order; development AGENTS exclusions and observable context limits; preserved bundle/checksum delivery; conflicts/constraint expansion block and changed guidance requires new approved configuration |

## Verification and limitations

Document-only checks pass: 32 table-type definitions and 10 service functions
match the evidence inventory; all six story ranges cover 26 criteria. Checked
65 local links/anchors, all four blueprint diagrams with cached Mermaid parser,
and `git diff --check`: pass. Diagrams parsed, not visually rendered.
No new behavior so TDD, runtime tests, artifact drivers or shared Python checks
are inapplicable. No dependency/lockfile edits, suppressions, platform support or
complete assistant instruction capture claimed. Actual installed end-to-end adapter
and VS Code demonstrations remain future story acceptance evidence.

M4-D1 blocks product implementation until assistant/workspace/kernel isolation is
chosen and verified; M4-D2 blocks concrete adapter implementation until the first
product/interface/version is selected and verified. These explicit blockers are
documentation outputs, not proof of an implemented or supported integration.
IP4 technically complete; developer approval pending. Stop before IP5.
