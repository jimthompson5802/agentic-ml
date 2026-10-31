# User-story implementation-plan template

Use this template when creating or revising a detailed implementation plan. Follow the [repository planning terminology](../../README.md#planning-terminology) and the authoritative [user stories and acceptance criteria](../specs/user-stories.md). Save completed plans under `docs/plans/`, using a name such as `milestone-1-us-11.md`; adjust relative links for the saved location.

Replace placeholders with concrete work. Repeat the implementation phase block as needed and use story-qualified identifiers. For a story delivered across milestones, scope this plan to the identified milestone and acceptance criteria. Preserve existing story and criterion IDs. Record unresolved decisions and the work they block rather than silently settling product requirements.

During execution, complete the current implementation phase's tasks and verification, present review evidence, and pause for explicit developer approval before progressing. Record requested changes within that implementation phase. Plan approval and implementation gate decisions are separate; an approved plan leaves its implementation gates awaiting review. Record approvals only when explicitly given by the developer, with a reference to the decision.

For new plans, follow the [phase and story verification policy](../development.md#phase-and-story-verification). Use impact-based phase checks and assign complete-suite verification to the last implementation phase before story acceptance. Existing approved plans retain their requirements unless explicitly revised. Adjust relative links for the saved plan.

---

# Milestone <number> / US-<ID>: <story title>

## Scope and outcome

- **Milestone:** <number and title>
- **User story:** <link to the authoritative story>
- **User-visible outcome:** <observable result this plan delivers>
- **Acceptance criteria covered:** <links to the existing criterion IDs>
- **Scope boundaries:** <included work, exclusions, and portions deferred to other milestones>
- **Supporting design:** <relevant sections or accepted architecture decisions>
- **Coordinated execution index:** <link when cross-story prerequisites are included; otherwise None>

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| <prerequisite or unresolved question> | <what must be available or decided> | <implementation phase or task> | <status and reference> |

For cross-story prerequisites, link the supplying story plan and implementation phase/task IDs. State the required capability, verification evidence, and developer gate approval. Require only the needed story portion. Keep task and gate records in their owning plan; use the execution index to coordinate order across plans.

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

Use `Not started` initially and `Complete` only after the work and required verification pass and actual evidence is recorded. Partial, blocked, failed, and unverified tasks remain incomplete. Reopen affected tasks and repeat verification when requested changes invalidate results. Task completion is separate from developer approval of the implementation phase.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-<ID>-IP1-T1 | Not started | <concrete action> | <prerequisite or none> | <observable result> | <criterion IDs> |

### Verification and review evidence

- **Selected tests and impact rationale:** <exact paths/node IDs/selectors; changed behavior, callers and dependent capabilities; criterion IDs>
- **Public boundaries and limits:** <interfaces, coverage gaps, and developer confirmation reference; reuse applicable confirmed boundaries>
- **Deferred checks:** <unrelated checks, reason, and owning final phase/task; None if none>
- **Broader-run triggers:** <apply the development-guide triggers and any phase-specific impact conditions>

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| <behavior or requirement to verify> | <appropriate test, demonstration, or inspection> | <checkable success condition> | Pending |
| Shared development checks (executable phases) | <locked sync/lock, lint/format/types/version and whitespace commands from development guide> | Pass; lock identity preserved or intentional change explained | Pending |

Record actual selected/deselected test counts and limitations. Tests required by this phase are not deferred because they are slow. Follow early full-run triggers even if the original selection was narrower. For documentation/design-only phases, name the appropriate document checks and explain why executable checks are inapplicable.

### Developer approval gate

- **Approval criteria:** <required task results, verification outcomes, and review evidence>
- **Evidence presented:** <links to changes, artifacts, and verification results>
- **Remaining limitations or blocked work:** <state explicitly>
- **Developer decision:** Pending — record Approved, Changes requested, or Rejected when explicitly given.
- **Decision reference and date:** <record the developer's decision>
- **Requested changes and resolution:** <record if applicable>
- **Progression authorized:** <link to the next implementation phase in the coordinated order, possibly in another story plan, or final acceptance; pending until approved>

## Final verification requirements

Assign this work to a named task in the last implementation phase above; this section defines its completion evidence rather than an extra approval gate.

- **Owning final phase/task:** <identifier; required before presenting the final phase gate>
- **Final implementation identity:** <tested revision, working-tree changes and lock hash>
- **Complete suite and shared checks:** <unfiltered locked pytest and shared commands; for a documentation-only story, explain inapplicability and list document checks>
- **Distribution/installation and other required checks:** <direct and sdist-rebuilt wheels, installed public interfaces, manual/platform checks as applicable; justify inapplicable checks>
- **Deferred-check reconciliation:** <every deferred check and actual result/evidence; remain Pending until verified>
- **Evidence renewal:** <rerun affected checks and full suite after executable changes; renew artifacts when inputs change; document-only edits use document checks>
- **Actual results and limitations:** Pending — <commands, counts, outcomes, evidence, platform and uncovered scope>

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| <each criterion covered by this plan> | <identifiers> | <evidence reference> | Pending |

- **Remaining work:** <limitations and any story portions assigned to later milestones>
- **Partial prerequisite delivery:** <criteria advanced versus fully verified; identify remaining work in this milestone without implying full story completion>
- **Final verification:** Pending — <evidence reference; all required checks must pass before whole-story acceptance>
- **Developer acceptance:** Pending
- **Decision reference and date:** <record when given; the final implementation gate may also serve as story acceptance if explicitly stated>
