---
name: create-implementation-plan
description: Create or revise an implementation plan from a local file, GitHub feature request issue, or supplied requirements. Save concrete tasks, verification methods, and developer approval gates. Use separate workflows to implement the plan or change its scope during execution.
---

# Create an implementation plan

Create a plan that another agent can implement and verify. Base the plan on the working repository and the supplied requirements.

This skill covers investigation and plan writing. Implementation, dependency installation, environment setup, and external issue changes require separate authorization. A request to edit this skill covers only the skill itself.

## Read the repository instructions

Find the working repository from the user's working directory. The skill's installation directory does not determine the working repository.

Read the applicable agent instructions and relevant repository documents. Follow their links to planning terms, templates, requirements, existing plans, verification rules, and approval gates.

Use the repository's plan structure, save location, identifiers, and progress format. Use the defaults below only when the repository has no convention for that item.

## Prepare the planning branch

Before analyzing requirements or writing the plan, check the current Git branch.

If the branch is `main`, identify the target user story from the planning request. Resolve its identifier before creating the branch. Read enough source metadata to identify the story when necessary.

Create and switch to `US-<story-number>-<short-slug>`, for example `US-34-experiment-init`. Use the target story's number and a short, lowercase, hyphen-separated slug describing its scope. For coordinated planning across prerequisite stories, use the target story's identifier.

Verify that the branch switch succeeded before continuing requirements analysis or plan writing.

If already on another named branch, continue there.

If HEAD is detached, the proposed branch already exists, or branch creation fails, report the condition and request developer direction before continuing. Preserve existing working-tree changes.

Creating the local planning branch is part of this workflow. Publishing it requires separate authorization. Report the selected branch when delivering the plan.

## Read the source requirements

Accept any of these sources:

- A local requirements or design file. Read the file and its relevant references.
- A GitHub feature request issue, given as a URL or issue number. Get the repository from the URL. For an issue number alone, use the working checkout's GitHub repository. Read the title, body, and relevant discussion. Use an available connector or `gh issue view` with an explicit repository.
- Requirements supplied in the conversation.

Keep a source reference that a later session can use. Preserve source IDs, acceptance criteria, exclusions, dependencies, and approval rules.

If a required source is unavailable, identify the blocked work and ask for the missing content. Keep missing requirements unresolved until the source or developer supplies them.

A feature request can be the source without a formal user story. If it has no acceptance criteria, propose criteria based on its stated outcomes. Label these criteria as proposed. Keep source requirements, proposed criteria, and assumptions separate.

## Check the current state

Inspect the relevant code, configuration, dependencies, tests, and existing plans. Record what exists, what is proposed, and what remains unknown. Identify checks that exist and checks that implementation must add.

In a design-only repository, treat documented paths, APIs, schemas, and commands as proposals until implementation evidence confirms them.

Look up facts in the repository before asking the developer. Resolve questions that affect scope, observable outcomes, acceptance criteria, or the implementation approach. Continue independent investigation while waiting for answers. Mark interim plans as drafts and record their blockers.

Start detailed planning when scope and acceptance criteria are clear. Resolve important decisions first, or assign them to an initial implementation phase with a defined investigation scope.

## Coordinate prerequisite stories

A request naming one story can include planning the minimum prerequisite portions of other stories, including transitive dependencies. Keep the named story as the target outcome. Respect explicit scope limits and milestone boundaries; unresolved scope decisions remain blockers.

Read the milestone's capability dependencies and recommended delivery order. Dependencies may concern portions of stories; require the needed capability rather than whole-story completion. Retrieve the complete issue body and all comments for every affected story using the repository's issue-retrieval workflow. Reconcile issue scope, design contracts, existing implementation, and existing plans before planning dependent work.

Keep a separate plan for each story and milestone slice. Each implementation phase and task has one owning story. Reuse existing task records through links rather than duplicating them. Distinguish acceptance criteria advanced by a prerequisite slice from criteria fully verified; including a slice does not imply completion of its story.

Save a coordinated execution index alongside the story plans, using the repository's convention or `docs/plans/milestone-<number>-execution-order.md`. Record the target story, included prerequisite scope, plan-review decision, and ordered links to story implementation phases. For each entry, name prerequisite capabilities, supplying story/phase/task IDs, verification evidence, and required gate approvals. Link every participating plan to the index. The index coordinates order; owning story plans remain authoritative for tasks, evidence, and gate decisions.

Order implementation phases so required capabilities are available before dependent work. If the order contains a cycle, refine the capability slices or record a blocker. Identify shared integration checks and each story's contribution. Include applicable controls in every enabled operation. Plan review must cover the coordinated scope and all participating plans; approval leaves every implementation gate pending.

## Define implementation phases

Use the repository's planning hierarchy and terms. Preserve existing milestone boundaries, story boundaries, story slices, and criterion IDs. Add milestone or story IDs only when the repository requires them. Distinguish implementation phases from the product's workflow phases.

Use one implementation phase for small work. Add implementation phases when risk, dependencies, complexity, or developer feedback require separate results that can be verified.

If the approach is unproven, start with a feasibility implementation phase. Define its question, scope, required evidence, completion criteria, and developer checkpoint. Make later work depend on its findings. Require refinement and review before dependent implementation starts.

For each implementation phase, define:

- The expected outcome and entry conditions.
- Dependencies and acceptance criteria covered.
- Ordered granular tasks, as described below.
- Completion criteria and required review evidence.
- A separate developer approval field, initially pending.

Every implementation phase must end with a developer approval gate, including the final one. Track technical completion separately from developer approval.

### Plan verification by impact

Read the working repository's verification policy before choosing phase checks. For this repository, use [phase and story verification](../../../docs/development.md#phase-and-story-verification). New plans must specify selected test commands, affected behavior and dependencies, acceptance-criterion coverage, confirmed public boundaries, and unrelated checks deferred to a named final task. Follow early full-run triggers; duration alone does not justify deferral. Preserve stronger requirements in an existing approved plan unless an explicit revision is authorized and recorded through the scope-change procedure.

Assign final verification to a task in the last implementation phase, before its approval gate and whole-story acceptance. Require the complete unfiltered suite, shared checks and applicable distribution/installation, manual and platform evidence against the final implementation. Resolve every deferred check there. Record evidence-renewal conditions after later changes; document-only work uses appropriate document checks with a rationale. Approval of an intermediate phase covers only its verified scope.

## Define granular tasks

Give each task a stable ID and a progress field. Follow the repository template or existing plan. If neither defines a format, use unchecked Markdown tasks such as `- [ ] IP1-T01: ...`.

Start new tasks as incomplete. Preserve existing completion records only when evidence supports them.

For this repository's task tables, use columns in this order: Task ID, Status, Action and relevant files or components, Depends on, Expected output / completion condition, Acceptance criteria. Start tasks as `Not started`; use `Complete` only after work and required verification pass and evidence is recorded. Intermediate statuses remain incomplete. Preserve justified existing formats when revising plans.

For each task, specify:

- **Action and files:** Give repository-relative paths to create, modify, delete, or inspect. State the change or evidence required for each file. Mark new paths as proposed.
- **Behavior:** For software changes, describe inputs, outputs, and failure handling. Identify functions, methods, or classes when useful. Distinguish existing names from proposed names. Give enough detail to implement the behavior without prescribing each line of code or assuming unsupported APIs.
- **Dependencies:** Identify prerequisites. If investigation must determine a path or approach, require that investigation and task refinement before dependent implementation.
- **Completion condition:** State the result that shows the task is complete.
- **Verification:** State the check and its expected result. Distinguish existing commands from checks to add. Use meaningful automated tests where appropriate. Use manual checks or diagnostic evidence when automation is unsuitable. Match verification effort to the change. Avoid tests that repeat implementation details.

Map every acceptance criterion within scope to task IDs and verification evidence. Preserve each criterion's meaning. Identify deferred criteria and verification blockers explicitly.

## Add execution rules to the plan

The saved plan must include these instructions for the implementing agent.

### Record task progress

Mark a task complete only after its work and required verification pass. Record actual results and evidence. Keep partial, blocked, failed, and unverified tasks incomplete.

Follow the coordinated execution index when present and check the supplying story's evidence and gate decisions before starting dependent work. Reopen affected tasks and renew verification when changes invalidate their results.

### Stop at developer gates

Stop at the end of every implementation phase, including the final one. Present completed tasks, checks performed, actual results, evidence paths, deviations, and limitations.

Wait for explicit developer approval before progression. Record the decision and its reference. Plan approval does not approve implementation gates. Silence is not approval. Apply a prior decision only when it explicitly covers the current gate.

### Handle scope changes

Pause affected work when evidence invalidates the approach or requires a change to requirements or authorized scope. Follow the repository's scope-change procedure. Record the change, impact, and decision in the plan.

Prerequisite work discovered during execution that is outside the approved scope requires a documented scope revision and developer approval before implementation. Update affected story plans and the execution index together.

Use `manage-plan-scope` when repository instructions or available skills provide it. If no procedure is available, record the proposed revision and obtain any required authorization before dependent implementation. Routine decisions within approved scope can proceed.

### Handle repeated failures

Follow retry and escalation limits defined by the repository or plan. Link local sources relative to the saved plan. This skill sets no fixed retry count.

If repeated failures invalidate the approach, report the attempts, findings, and required decision before continuing affected work.

## Save the plan

Inspect existing plans first. Update a matching plan when appropriate. Preserve IDs, evidence, developer decisions, and history. For a plan already in execution, use the scope-change procedure for substantive revisions.

Use the repository's template and save location. If no location is specified, use `docs/plans/<story-id-or-short-slug>.md`.

Resolve repository paths from the working checkout. Resolve document links from the saved plan's location.

If no repository template exists, include:

1. Title, source reference, and plan review status. Include requirements and acceptance criteria when no lasting source reference exists.
2. Scope, exclusions, dependencies, findings with sources, assumptions, and unresolved prerequisites.
3. Technical approach and reasons for that approach.
4. Implementation phases, granular tasks, progress fields, verification, completion criteria, and developer approval gates.
5. Acceptance criteria mapped to tasks and evidence, with deferred work identified.
6. Execution rules and fields for scope changes and developer decisions.

## Review and deliver the plan

Before delivery, check that:

- Every acceptance criterion within scope maps to tasks and verification.
- Task order and dependencies are feasible.
- Cross-story prerequisites identify their owning tasks, required capabilities, evidence, and approval gates; the execution index and story plans agree.
- Every task identifies files, progress, completion conditions, and expected behavior where applicable.
- Work that depends on unresolved findings is marked as conditional.
- Every implementation phase has a stop instruction and a pending developer gate.
- Phase test selections have impact rationales and explicit deferrals; a named final task resolves them and requires complete verification before final gate approval and story acceptance.
- Local links resolve, and the plan follows the source requirements and repository template.

Record only validation actually performed. Keep planned checks distinct from passing results.

Return a link to the saved plan. Briefly describe its implementation phases and blockers, then request developer review. Finish within planning scope. Implementation requires separate authorization.
