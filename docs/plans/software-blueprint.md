# Software blueprint documentation plan

## Scope and decisions

Source: developer conversation, 2026-11-04, “Implement the plan.” Documentation
maintenance across M1–6; no invented story ID or executable delivery. Use the
[planning template](../templates/user-story-implementation-plan.md) task/gate
conventions. Branch: `embellish-software-component-descriptions`, created as the
first execution step. Initial working tree clean. Plan approved by execution
request; every implementation gate remains separately pending.

Deliver [software blueprint](../specs/design/software-blueprint.md), overview/topic
links, reconciled interface status and criterion ownership. Each entry records
module, APIs/types/errors, inputs/outcomes, authorization/enforcement, persistence,
recovery, verification boundaries and implemented/accepted/proposed/blocked status.
Preserve accepted interfaces and issue decisions. Changes to governed scope use
[manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md).

## IP1 — Inventory and Milestone 1

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP1-T1 | Complete | Create requested branch; inspect working tree | None | Correct branch, clean initial tree | Documentation requirement |
| IP1-T2 | Complete | Save this plan; inventory exports, schemas and accepted contract reports | T1 | Existing/proposed distinctions in blueprint | M1 criteria below |
| IP1-T3 | Complete | Retrieve issues #8–18 including all comments and refresh metadata | T2 | M1 source reconciliation | M1 criteria below |
| IP1-T4 | Complete | Establish blueprint format and criterion matrix | T3 | All M1 criterion slices assigned | M1 criteria below |
| IP1-T5 | Complete | Describe existing and proposed M1 components | T4 | Public contracts and explicit blocking decision | M1 criteria below |
| IP1-T6 | Complete | Add execution interaction diagram and document checks | T5 | Reviewable execution/evidence flow | M1 criteria below |

Criteria: US-01-AC-01–04, US-02-AC-01–05, US-03-AC-01–05,
US-05-AC-01–05 (future entrypoints retain integration obligations),
US-09-AC-01–05, US-10-AC-01–05, US-11-AC-01–05,
US-12-AC-01/05, US-13-AC-01–04, US-26-AC-01–05, US-27-AC-01–04.
Mapping is design coverage, never executable acceptance.

**IP1 developer approval: Approved, 2026-11-04.** Developer “i approve ip1,
coomit firs then move to ip2” approves IP1, authorizes its commit first, and then
IP2 execution. Review covered concrete proposed contracts, ownership,
verification boundaries and M1-D1 isolation blocker. Stop before IP2. Scope-change
history: None. Exact future wire schemas and isolation mechanism require owning
story contract gates; this documentation does not authorize implementation.

### IP1 requested refinement

Developer “can you make it more precise” requested explicit ExperimentSpec
attributes and responsibilities. Refined IP1-T5 within existing scope: required
fields/types, manifest authority, immutable nested parameters, preparation and
submission checks, and failure cases. Documentation checks renewed; IP1 approval
remains pending and IP2 remains unstarted. No executable API implemented.

Developer “i agree complete m1 first” further requested the same precision for
all remaining M1 public classes and referenced request/result types. IP1-T5 now
includes the complete M1 record catalogue: implemented field/default inventory,
proposed field/type/constraint tables, service methods, lifecycle and verification
scenarios. This refines the existing deliverable without adding executable scope
or advancing IP2. Existing source contracts are preserved; proposed typed runner
results explicitly refine the conceptual protocol. IP1 gate remains pending.

## Remaining phases

### IP2 execution record

Entry: IP1 committed as `a475835` before IP2 began, as directed by developer
“i approve ip1, coomit firs then move to ip2”. This authorizes IP2 only; IP3 awaits
its separate gate. The earlier IP1 pending statements are historical snapshots.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP2-T1 | Complete | Retrieve #19–23 bodies/comments and reconcile M2 source contracts | IP1 approval/commit | Complete discussions, stable metadata and scope recorded | All M2 slices below |
| IP2-T2 | Complete | Blueprint assessment/splits, preprocessing and pipeline records/services | T1 | Concrete types/constraints/lifecycle and ownership | US-12-AC-02–04; US-15-AC-01–04; US-16-AC-01–05; US-27-AC-05–09 |
| IP2-T3 | Complete | Fixed estimator and feature comparison protocol | T2 | Approved baseline/settings/metric/split bindings and distinct outcomes | US-14-AC-01–05 |
| IP2-T4 | Complete | Fit/transform/restore diagram and document checks | T2/T3 | Diagram parses; checks recorded | All M2 slices |
| IP2-T5 | Complete | Inventory/detail/reference/coverage checklist | T4 | Evidence checklist passes; implementation blocker explicit | All M2 slices |

**IP2 developer approval: Approved, 2026-11-04.** Developer “i approve ip2,
commit then start ip3” approved the M2 contracts and directed commit before IP3.
Review covered the proposed M2 software contracts,
public test boundaries and explicit M2-D1 isolation blocker in the
[IP2 evidence](../verification/software-blueprint-ip2.md). No executable acceptance
claimed. Next action: developer review; stop before IP3. No IP2 commit or push
authorized by the IP1-only commit instruction.

### IP3 execution record

Entry: IP2 approved by developer “i approve ip2, commit then start ip3” and
committed first as `4d38afd`. IP3 refines software documentation only.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP3-T1 | Complete | Retrieve/reconcile #26–33 bodies/all comments and M3 design | IP2 approval/commit | Source requirements and superseded #32 authentication reference recorded | All M3 criteria below |
| IP3-T2 | Complete | Model/selection/framework/checkpoint/tuning/final/reporting catalogue | T1 | Exact attributes, services, lifecycle and scoped approval rules | All M3 criteria below |
| IP3-T3 | Complete | Independent outcome model | T2 | Execution, validity, quality and acceptance are separate | US-21-AC-01–05; US-24-AC-01–05 |
| IP3-T4 | Complete | Training/evaluation diagram and document checks | T2/T3 | All diagrams parse and document checks pass | All M3 criteria below |
| IP3-T5 | Complete | Inventory/detail/reference/coverage checklist | T4 | Complete type/function inventory and criterion mapping | All M3 criteria below |

Criteria: US-06-AC-01–04, US-16-AC-06–10, US-18-AC-01–04,
US-19-AC-01–04, US-20-AC-01–04, US-21-AC-01–05,
US-24-AC-01–05 and US-26-AC-06–09. These 35 criteria have design coverage,
not executable acceptance. [IP3 evidence](../verification/software-blueprint-ip3.md)
records the inventory and public boundaries. **IP3 developer approval: Approved,
2026-11-04.** Developer “i approve ip3; commit and start ip4” authorizes the IP3
commit followed by IP4 execution. Earlier pending statements are historical.
Review proposed contracts, protocol replacements and M3-D1 enforcement blocker;
stop before IP4. No IP3 commit/push/PR requested.

### IP4 execution record

Developer “i approve ip3; commit and start ip4” approved IP3 and authorized its
commit before IP4. Baseline commit `7b00662` completed first. Scope remains
documentation-only, with the same detail/completeness standard.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP4-T1 | Complete | Retrieve #34–39 bodies/all comments, refresh metadata, reconcile design | IP3 approval/commit | Complete source discussion, scope exceptions explicit | All M4 slices below |
| IP4-T2 | Complete | Delegation/notebooks/guidance/immutability/interactive/iteration contracts | T1 | Required fields, types, lifecycle and enforcement ownership | US-04-AC-01–04; US-07-AC-01–04; US-08-AC-01–04; US-17-AC-01–04; US-22-AC-01–05 |
| IP4-T3 | Complete | Typed adapter task/capability/result/cancel/usage contract | T2 | Explicit replacement of synchronous conceptual protocol; first-product blocker recorded | US-30-AC-01–05 |
| IP4-T4 | Complete | Feedback-loop diagram and document checks | T2/T3 | Diagrams parse and links/whitespace pass | All M4 slices |
| IP4-T5 | Complete | Inventory, reference closure and criterion checklist | T4 | Complete classes/functions and all 26 criteria mapped | All M4 slices |

**IP4 developer approval: Approved, 2026-11-05 (UTC).** Developer “i approve ip4;
commit and start ip5” authorizes commit before IP5 execution. Review covered proposed interfaces and public
verification boundaries, M4-D1 assistant/kernel isolation and M4-D2 concrete
product/interface/version selection blockers. [IP4 evidence](../verification/software-blueprint-ip4.md)
records checks and limitations. Stop before IP5; no IP4 commit/push/PR requested.

### Mandatory detail and completeness standard for IP2–IP6

Use the M1 ExperimentSpec definition and M1 record catalogue as the minimum
detail standard. This requirement applies to each remaining phase's contract
tasks and developer approval gate, not only to final reconciliation.

For each class, protocol, request/result type, exception and nested record:

- Record purpose, owning module, milestone, story and acceptance-criterion IDs.
- Specify every attribute's exact type, required/optional status, default and
  constraints; distinguish nullable values from omitted fields.
- Specify method signatures, construction/preparation boundaries, observable
  outcomes, errors and side effects. Explicitly state when records have no methods.
- Define validation, immutability, serialization, persistence, identity/version,
  lifecycle, authorization and recovery rules where applicable. Mark inapplicable
  items with a reason rather than leaving ambiguous omissions.
- Identify authoritative records, cross-record bindings, dependencies and
  verification scenarios, including relevant failure and boundary cases.
- Distinguish implemented, accepted, proposed and blocked contracts. Preserve
  accepted behavior; explicitly document extensions and incompatibilities.

Each phase must produce a completeness checklist in its verification report:

| Required evidence | Completion condition |
|---|---|
| Public type/interface inventory | Includes all types introduced by the phase, types mentioned only in signatures, nested records, aliases and relevant exceptions. Each item links to its definition. |
| Detail checklist | Every inventory item satisfies the standard above or states a justified inapplicable item. |
| Reference closure | Every referenced type is defined locally, linked to an earlier definition, or explicitly deferred with its owning milestone/story, reason and blocked work. An in-scope required type cannot be deferred merely to pass this check. |
| Cross-milestone reconciliation | Earlier definitions are reused by reference; extensions, conflicting signatures, identity conventions and changed assumptions are explicitly reconciled. |
| Criterion coverage | Every in-scope acceptance criterion maps to software owners, contract definitions and public verification scenarios. Mapping does not claim executable acceptance. |

Add these stable tasks to the existing sequences below: IP2-T5, IP3-T5, IP4-T5,
IP5-T6 and IP6-T6 each perform their phase's inventory, detail, reference-closure,
cross-milestone and criterion checklist review after all other tasks in that phase.
IP2-T5, IP3-T5 and IP4-T5 are Complete as recorded above; IP5-T6 and IP6-T6 are **Not started**.
IP6-T6 also verifies the combined M1–6 inventory
and is the final verification owner, extending IP6-T5's document checks.

Missing definitions or checklist failures leave the affected contract tasks and
completeness task unfinished. Do not present a phase as technically complete until
its checklist passes and evidence is recorded. Each gate requires both the
phase-specific deliverables below and this checklist; developer approval remains
a separate explicit decision.

**Plan refinement authorization:** Developer “make that update to the plan”
approved recording this standard for all remaining milestones. This strengthens
documentation completion criteria without authorizing executable work or advancing
past IP1. Existing historical evidence is preserved; IP1 approval remains pending.

Each row below preserves the planned sequence. IP2 completion is recorded above;
IP3/IP4 completion is recorded above; IP5–IP6 remain **Not started / Pending**.
Entry condition is approval of the preceding phase.

| Phase | Ordered tasks | Completion and gate |
|---|---|---|
| IP2 / M2 | T1 retrieve/reconcile owning issues; T2 assessment/splits, features, preprocessing registration/fit/persist/restore and pipeline reuse; T3 minimal estimator/evaluator contracts; T4 fitting/restoration diagram and checks | All M2 criterion slices mapped; developer approval |
| IP3 / M3 | T1 retrieve/reconcile issues; T2 algorithm modes, supplied models/frameworks, tuning, checkpoints, holdout and reporting; T3 distinct execution/validity/quality/acceptance outcomes; T4 training/evaluation diagram and checks | All M3 slices mapped; developer approval |
| IP4 / M4 | T1 retrieve/reconcile issues; T2 delegation/notebooks/guidance/immutability/interactive controls/iteration; T3 concrete agent task/result/capability/cancellation contracts and usage limitations; T4 feedback-loop diagram and checks | All M4 slices mapped; developer approval |
| IP5 / M5 | T1 retrieve/reconcile issues; T2 orchestration/approvals/state/audit/adapters; T3 recovery/uncertainty/deduplication/accounting; T4 preserve unauthenticated exception and deferred authentication; T5 recovery diagram and checks | All M5 slices mapped; developer approval |
| IP6 / M6 and final reconciliation | T1 retrieve/reconcile issues; T2 gap diagnosis/acquisition/limits/lineage/comparison/recovery; T3 acquisition diagram; T4 all nine protocols and all M1–6 criteria reconciled; T5 overview/topic stale wording, version/date/ADR references, final evidence and checkpoints | Complete coverage matrix, links and contract status checked; final developer acceptance |

Every phase uses concrete proposed contracts for future software. Preserve issue
scope and accepted APIs; resolve conflicts before affected contracts proceed.
Existing topic documents own product rules; blueprint owns software seams.
Keep M0/50/99 outside scope except prerequisite references. No commit, push or PR
is authorized. Record actual progress, evidence and approval references; reopen
invalidated tasks. Follow the repository three-attempt limit for failed fixes.

## Verification and final acceptance

Documentation-only: no new executable behavior, so TDD, runtime suites and artifact
drivers do not apply under the [verification policy](../development/verification.md).
Each phase checks links/anchors, source symbols/signatures, criterion coverage,
success/failure/boundary scenarios, implemented versus proposed labels and
`git diff --check`. Manual Mermaid review does not establish renderer validation.
Record evidence in [IP1 report](../verification/software-blueprint-ip1.md), with
later phase reports alongside it. Refresh checkpoints at handoff and gates.

Final task IP6-T5 owns final document verification: every M1–6 criterion has a
software owner, contract reference and public verification boundary; every original
protocol is retained/refined/superseded explicitly; unresolved decisions have owners,
affected criteria and blocked work. Preserve historical evidence, pending ADRs,
platform limitations and separate milestone acceptance obligations. Final technical
completion and developer acceptance remain separate. Actual final results: Pending.
