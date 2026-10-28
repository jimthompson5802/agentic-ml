---
name: manage-plan-scope
description: Revise an implementation plan when a user changes scope during execution or discovered constraints require replanning. Assess impact, preserve evidence, record decisions, and honor existing approval gates.
---

# Manage plan scope

Handle additions, removals, deferrals, and changes to outcomes in an implementation plan already being executed. Keep the revised plan and its authorization clear enough for another agent or developer to resume work.

## Establish the change

Read the active plan, applicable repository instructions, planning template, and authoritative requirements. Use the repository's terminology, plan location, identifiers, and approval rules. Where no convention exists, revise the existing plan in place and add a compact scope-change record there.

Pause work affected by the proposed change, preserving current edits and verification evidence. Unaffected work may continue only within existing authorization and gate boundaries. If the user is exploring an option, assess it without treating it as a decision to implement it.

Identify the requested outcome, the work added, removed, or deferred, and the reason. Resolve consequential ambiguity with the user while continuing independent analysis. Distinguish an implementation detail within approved scope from a change to outcomes, acceptance criteria, boundaries, or required deliverables. Routine implementation choices do not need a scope-change approval cycle.

## Make the revision reviewable

Assess effects on completed and remaining work, dependencies, acceptance criteria, verification, approval gates, and milestone or delivery commitments. Give concrete consequences; mark uncertain effort or schedule estimates as estimates.

Update the existing plan with the proposed scope, tasks, dependencies, verification, and gate criteria. Preserve stable identifiers and previous decisions. Mark removed or deferred tasks explicitly rather than erasing their history. Keep completed work and evidence; flag evidence invalidated by the new scope and specify the rework or checks needed. Previous approvals remain historical facts, with affected work marked for renewed review where required.

If the request changes authoritative stories, acceptance criteria, or architecture decisions, identify and prepare the corresponding revisions within the user's authorized editing scope. Preserve existing criterion IDs; identify added criteria explicitly. Record unresolved product decisions and the work they block. A narrower plan must explicitly identify deferred criteria rather than imply full story completion. A plan-only edit cannot silently redefine authoritative requirements.

Record the change in the plan using its existing format, or the compact record below. Completion of this step means the scope difference, affected work, required verification, and authorization status are visible in the saved plan.

## Resolve authorization and resume

Present the concrete revision and material consequences. Use the user's explicit instructions and existing authorization: a clear instruction to implement a defined change can authorize that scope without another confirmation unless repository rules require separate review. A proposal, ambiguous request, or material consequence outside the granted scope needs a decision before dependent implementation proceeds. Record approval only when explicitly given, with a reference to the message, review, or other decision source.

Honor repository approval gates independently. Approval of a revised plan does not satisfy an implementation gate. Review requested changes within the current implementation phase when that is the repository convention; await the required gate approval before progressing. If a decision is needed, state the exact decision and why, citing the applicable repository rule or this skill's authorization requirement.

For rejection or deferral, retain the decision and resume the previous scope only where it remains authorized and applicable. For approval, record the authorized revision and next task, then resume within the applicable gate boundaries. Recheck affected evidence before claiming completion; report remaining deferred work explicitly.

## Compact scope-change record

Adapt this to the plan's existing structure. Use one record per meaningful change; do not create a separate change-management system.

- **Change ID and date:** Stable local identifier and date.
- **Request and reason:** Requested outcome and decision source.
- **Scope difference:** Added, removed, deferred, or changed work.
- **Impact:** Affected tasks, requirements, dependencies, completed work, evidence, and commitments.
- **Plan and requirement revisions:** Links or identifiers for changed sections and related documents.
- **Verification and gates:** Required checks, evidence needing renewal, and gate status.
- **Decision:** Proposed, Approved, Rejected, or Deferred; explicit decision reference and date when available.
- **Resume point:** Authorized next task or the decision blocking affected work.
