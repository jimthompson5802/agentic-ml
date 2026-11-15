---
name: create-implementation-plan
description: Create or revise an implementation plan from a local file, GitHub feature request issue, or supplied requirements. Save concrete tasks, verification methods, contract review gates and automatic progression criteria. Use separate workflows to implement the plan or change its scope during execution.
---

# Create an implementation plan

Create a plan that another agent can implement and verify. Base the plan on the working repository and the supplied requirements.

This skill covers investigation and plan writing. Implementation, dependency installation, environment setup, and external issue changes require separate authorization. A request to edit this skill covers only the skill itself.

## Read the repository instructions

Find the working repository from the user's working directory. The skill's installation directory does not determine the working repository.

Read the applicable agent instructions and relevant repository documents. Follow their links to planning terms, templates, requirements, existing plans, verification rules, and approval gates.

Use the repository's plan structure, save location, identifiers, and progress format. Use the defaults below only when the repository has no convention for that item.

## Select the planning worktree

Before detailed requirements analysis or plan writing, identify the target story
and inspect the current branch and registered worktrees. Read enough issue
metadata to distinguish the story identifier from its GitHub issue number.

Use the [manage-story-worktree skill](../manage-story-worktree/SKILL.md) to create
or reuse its workspace, following the repository's
[story worktree guidance](../../../docs/development/worktrees.md). A story
planning request authorizes the local branch/worktree creation needed for that
story; it does not authorize environment setup or publication. Resolve detached
HEAD or conflicting associations before writing. Do not continue on an arbitrary
named branch or switch the caller's checkout.

Read instructions and the checkpoint in the selected checkout, then perform
subsequent reads, edits, and checks there. Record story/issue, branch, base ref and
starting commit, and primary-checkout-relative worktree location in the plan.
Report the absolute session path to the developer without committing that path.
Existing in-progress story checkouts follow the guidance's resumption rules;
do not relocate their edits automatically.

For coordinated prerequisite planning, use the target story's worktree to author
the approved coordinated planning deliverables. Do not overwrite another active
story's plan; reconcile its owning session's records first. Creating these plans
does not authorize implementation of prerequisite stories.

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

For each user-facing capability, name the runnable deliverable and plan to verify that same workflow through supported interfaces. When existing tools provide the behavior, prefer their native commands and one authoritative artifact; justify each added wrapper or metadata copy against an acceptance criterion.

In a design-only repository, treat documented paths, APIs, schemas, and commands as proposals until implementation evidence confirms them.

Look up facts in the repository before asking the developer. Resolve questions that affect scope, observable outcomes, acceptance criteria, or the implementation approach. Continue independent investigation while waiting for answers. Mark interim plans as drafts and record their blockers.

Start detailed planning when scope and acceptance criteria are clear. Resolve important decisions first, or assign them to an initial implementation phase with a defined investigation scope.

## Coordinate prerequisite stories

A request naming one story can include planning the minimum prerequisite portions of other stories, including transitive dependencies. Keep the named story as the target outcome. Respect explicit scope limits and milestone boundaries; unresolved scope decisions remain blockers.

Read the milestone's capability dependencies and recommended delivery order. Dependencies may concern portions of stories; require the needed capability rather than whole-story completion. Retrieve the complete issue body and all comments for every affected story using the repository's issue-retrieval workflow. Reconcile issue scope, design contracts, existing implementation, and existing plans before planning dependent work.

Keep a separate plan for each story and milestone slice. Each implementation phase and task has one owning story. Reuse existing task records through links rather than duplicating them. Distinguish acceptance criteria advanced by a prerequisite slice from criteria fully verified; including a slice does not imply completion of its story.

Save a coordinated execution index alongside the story plans, using the repository's convention or `docs/plans/milestone-<number>-execution-order.md`. Record the target story, included prerequisite scope, plan-review decision, and ordered links to story implementation phases. For each entry, name prerequisite capabilities, supplying story/phase/task IDs, verification evidence, and required gate approvals. Link every participating plan to the index. The index coordinates order; owning story plans remain authoritative for tasks, evidence, and gate decisions.

Order implementation phases so required capabilities are available before dependent work. If the order contains a cycle, refine the capability slices or record a blocker. Identify shared integration checks and each story's contribution. Include applicable controls in every enabled operation. Plan review must cover the coordinated scope and all participating plans; approval leaves unresolved contract decisions pending.

## Define implementation phases

Use the repository's planning hierarchy and terms. Preserve existing milestone boundaries, story boundaries, story slices, and criterion IDs. Add milestone or story IDs only when the repository requires them. Distinguish implementation phases from the product's workflow phases.

Use one implementation phase for small work. Add implementation phases when risk, dependencies, complexity, or developer feedback require separate results that can be verified.

If the approach is unproven, start with a feasibility implementation phase. Define its question, scope, required evidence, completion criteria, and developer checkpoint. Make later work depend on its findings. Require contract refinement and developer review before dependent implementation when feasibility changes or leaves unresolved public contract decisions; otherwise use the phase approval policy.

For each implementation phase, define:

- The expected outcome and entry conditions.
- Dependencies and acceptance criteria covered.
- Ordered granular tasks, as described below.
- Completion criteria and required review evidence.
- An approval mode, contract references, verification prerequisites and progression record.

Follow the [phase approval policy](../../../docs/development/phase-approvals.md). Classify phases by whether they define/refine public contracts or implement approved ones. Contract decisions require explicit developer approval before dependent work. Automatic phases retain all checks and advance after their required verification passes. Keep whole-story acceptance separate from automatic completion.

### Plan verification by impact

Read the working repository's verification policy before choosing phase checks. For this repository, use [phase and story verification](../../../docs/development/verification.md#phase-and-story-verification). New plans must specify focused tests and relevant regressions for changed behavior plus shared checks at phase completion, the M1–6 command at story acceptance, changed modules and public behavior, acceptance-criterion coverage, confirmed public boundaries, and excluded checks deferred to a named story acceptance task. Full current-milestone test runs are not required at phase completion. Preserve separate milestone verification obligations. Preserve stronger requirements in an existing approved plan unless an explicit revision is authorized and recorded through the scope-change procedure.

Before selecting verification, read and follow the repository [phase and story verification policy](../../../docs/development/verification.md#phase-and-story-verification). Record exact commands, group selections, acceptance criteria, results and deferred-check owners in the plan. Preserve historical evidence, known failures and explicit approval gates.

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

Include an execution authorization record under the [command and autonomy policy](../../../docs/development/command-approvals.md): authorized phase sequence and checkout, authorization reference, verification scope, authorized external actions and next gate. Keep pending authorizations explicit; drafting or approving the plan does not record permission to execute it.

### Record task progress

Mark a task complete only after its work and required verification pass. Record actual results and evidence. Keep partial, blocked, failed, and unverified tasks incomplete.

Follow the coordinated execution index when present and check the supplying story's evidence and gate decisions before starting dependent work. Reopen affected tasks and renew verification when changes invalidate their results.

### Apply phase progression rules

At every phase completion, record tasks, verification, evidence, deviations and limitations. Follow the [phase approval policy](../../../docs/development/phase-approvals.md): request approval for unresolved public contract decisions and automatically progress through phases implementing approved contracts when required checks pass. Record automatic progression as verification-based, never as developer approval. After final verification, request whole-story acceptance. Preserve explicit developer holds and authorization boundaries.

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
- Every implementation phase has an approval mode, contract reference and verification-based progression criteria; unresolved contract decisions have a developer review gate.
- Phase test selections have impact rationales and explicit deferrals; a named final task resolves them and requires complete verification before whole-story acceptance and any applicable final contract review.
- Local links resolve, and the plan follows the source requirements and repository template.

Record only validation actually performed. Keep planned checks distinct from passing results.

Return a link to the saved plan. Briefly describe its implementation phases and blockers, then request developer review. Finish within planning scope. Implementation requires separate authorization.
