# User-story implementation-plan template

Use this template when creating or revising a detailed implementation plan. Follow the [repository planning terminology](../../README.md#planning-terminology) and the authoritative [user stories and acceptance criteria](../specs/user-stories.md). Save completed plans under `docs/plans/`, using a name such as `milestone-1-us-11.md`; adjust relative links for the saved location.

Replace placeholders with concrete work. Repeat the implementation phase block as needed and use story-qualified identifiers. For a story delivered across milestones, scope this plan to the identified milestone and acceptance criteria. Preserve existing story and criterion IDs. Record unresolved decisions and the work they block rather than silently settling product requirements.

During execution, complete the current implementation phase's tasks and verification, present review evidence, and pause for explicit developer approval before progressing. Record requested changes within that implementation phase. Plan approval and implementation gate decisions are separate; an approved plan leaves its implementation gates awaiting review. Record approvals only when explicitly given by the developer, with a reference to the decision.

---

# Milestone <number> / US-<ID>: <story title>

## Scope and outcome

- **Milestone:** <number and title>
- **User story:** <link to the authoritative story>
- **User-visible outcome:** <observable result this plan delivers>
- **Acceptance criteria covered:** <links to the existing criterion IDs>
- **Scope boundaries:** <included work, exclusions, and portions deferred to other milestones>
- **Supporting design:** <relevant sections or accepted architecture decisions>

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| <prerequisite or unresolved question> | <what must be available or decided> | <implementation phase or task> | <status and reference> |

## Plan review

- **Status:** Draft
- **Developer decision:** Pending
- **Decision reference and date:** <record when given>
- **Requested plan changes:** <record if applicable>

## Scope-change history

Follow the [manage-plan-scope procedure](../../.agents/skills/manage-plan-scope/SKILL.md) when scope changes during execution. Initially record "None"; repeat the record below for each meaningful change. Link requested changes in the affected implementation phase to their scope-change record.

- **Change ID and date:** <stable local identifier and date>
- **Request and reason:** <requested outcome, reason, and request reference>
- **Scope difference:** <work added, removed, deferred, or changed>
- **Impact:** <affected tasks, acceptance criteria, dependencies, completed work, evidence, and commitments>
- **Plan and requirement revisions:** <links or identifiers for revised sections and authoritative documents>
- **Verification and gates:** <required checks, evidence needing renewal, and affected gate status>
- **Decision:** Proposed — <record Approved, Rejected, or Deferred with an explicit decision reference and date when given>
- **Resume point:** <authorized next task or decision blocking affected work>

## US-<ID> / Implementation Phase 1: <concrete objective>

- **Outcome:** <reviewable result of this implementation phase>
- **Entry conditions:** <prerequisites and dependencies>
- **Acceptance criteria advanced:** <existing criterion IDs>

### Granular tasks

Order tasks by dependency. Each task should identify an action and a checkable result; mark completion only after producing that result.

| Task ID | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria | Status |
|---|---|---|---|---|---|
| US-<ID>-IP1-T1 | <concrete action> | <prerequisite or none> | <observable result> | <criterion IDs> | Not started |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| <behavior or requirement to verify> | <appropriate test, demonstration, or inspection> | <checkable success condition> | Pending |

### Developer approval gate

- **Approval criteria:** <required task results, verification outcomes, and review evidence>
- **Evidence presented:** <links to changes, artifacts, and verification results>
- **Remaining limitations or blocked work:** <state explicitly>
- **Developer decision:** Pending — record Approved, Changes requested, or Rejected when explicitly given.
- **Decision reference and date:** <record the developer's decision>
- **Requested changes and resolution:** <record if applicable>
- **Progression authorized:** <next implementation phase, or final story acceptance; pending until approved>

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| <each criterion covered by this plan> | <identifiers> | <evidence reference> | Pending |

- **Remaining work:** <limitations and any story portions assigned to later milestones>
- **Developer acceptance:** Pending
- **Decision reference and date:** <record when given; the final implementation gate may also serve as story acceptance if explicitly stated>
