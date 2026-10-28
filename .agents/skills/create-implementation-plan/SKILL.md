---
name: create-implementation-plan
description: Create or revise a repository-grounded implementation plan from a local file, GitHub feature request issue, or supplied requirements, with concrete tasks, verification, and developer approval gates. Produces a saved plan; use separate workflows for implementation or scope changes during execution.
---

# Create an implementation plan

Produce a technical plan that another implementation session can execute and verify. Investigate the repository and save the plan within the requested scope. Planning alone authorizes neither implementation nor dependency installation, environment setup, or external issue changes. A request to edit this skill does not authorize creating or executing a story plan.

## Establish requirements and repository conventions

1. Resolve the working repository from the user's working directory, independently of where this skill is installed. Read applicable agent instructions and relevant repository documentation. Follow pointers to planning terminology, templates, authoritative requirements, existing plans, evidence requirements, and approval gates. Repository conventions govern the plan's structure, location, identifiers, and progress format; use the fallback below only where conventions are absent.
2. Accept a local requirements or design file, a GitHub feature request issue (URL or issue number), or requirements supplied in the conversation. Read the local file and its relevant references. For GitHub, resolve the target repository from the issue URL or the working checkout for a bare issue number; retrieve the issue title, body, and relevant discussion through an available connector or `gh issue view` with an explicit repository. Preserve a durable source reference, source identifiers, acceptance criteria, exclusions, dependencies, and approval boundaries. If a required source is inaccessible, request its contents and identify the blocked work rather than reconstructing it. A feature request need not already be formatted as a user story: derive proposed acceptance criteria from its stated outcomes when absent, label them as proposed, and resolve material gaps with the developer before finalizing. Keep source requirements distinct from planning assumptions and proposed criteria.
3. Inspect relevant code, configuration, dependencies, tests, and existing plans. Separate observed behavior from proposals, assumptions, and unresolved decisions. Identify checks that exist and checks the work must introduce. In a design-only repository, treat documented layouts, APIs, schemas, and commands as proposed until implementation evidence establishes them.
4. Resolve material ambiguities before finalizing: conflicting requirements, unclear observable outcomes, missing acceptance criteria, scope decisions, or choices that change the approach. First look up facts available in the repository. Continue independent investigation while awaiting answers; mark saved interim plans as drafts with their blockers.

This step is complete when scope and acceptance criteria are understood and material decisions are resolved or explicitly assigned to a bounded feasibility implementation phase.

## Design implementation phases and tasks

Use the repository's planning hierarchy and terminology. Preserve milestone and story boundaries, existing slices, and criterion IDs where they exist; avoid inventing milestones or story IDs for an unnumbered feature. Distinguish implementation phases from any phases in the product's own workflow.

Use one implementation phase for small work. Add implementation phases when complexity, risk, dependencies, or developer feedback justify separate, independently verifiable outcomes. Each implementation phase ends with a developer approval gate, including the final one.

When an approach is unproven, begin with a bounded feasibility implementation phase. State the question, investigation scope, required evidence, completion criteria, and developer checkpoint. Keep dependent work conditional on the findings. Detail later work only as far as evidence supports, with refinement and review before dependent implementation begins.

For each implementation phase, specify:

- Outcome, entry conditions, dependencies, and acceptance criteria advanced.
- Ordered granular tasks with stable identifiers and progress fields matching the repository template or existing plan. If no convention exists, use unchecked Markdown tasks such as `- [ ] IP1-T01: ...`. Start new work incomplete; preserve prior completion states only where recorded evidence supports them.
- Repository-relative files to create, modify, delete, or inspect, and the intended change or evidence for each. Mark new paths as proposed. If a path depends on investigation, make that investigation a prerequisite and require refinement before dependent implementation.
- Expected behavior for software-writing tasks: relevant inputs, outputs, failure handling, and symbols to add or change where useful. Distinguish existing symbols from proposed names; give enough detail to implement without inventing unsupported APIs or prescribing line-by-line edits.
- Dependencies and an assessable completion condition for each task. Include meaningful automated tests where appropriate and manual checks or diagnostic evidence where automation is unsuitable. Specify observable expected results and distinguish existing commands from checks to introduce. Avoid unnecessary tests for low-impact, reversible changes or tests that mirror implementation details.
- Implementation phase completion criteria, review evidence, and a separate developer approval field, initially pending. Technical completion and developer acceptance are separate states.

Map every in-scope acceptance criterion to task identifiers and verification evidence. Preserve criterion meaning; technical tasks supplement requirements. Identify criteria deferred to other milestones or plans and any verification blockers rather than implying full coverage.

## Encode execution controls

The saved plan must tell the future implementing agent to:

- Mark tasks complete only after their work and required verification pass, recording actual results and evidence. Leave partial, blocked, failed, or unverified tasks incomplete.
- Stop at the end of every implementation phase, including the final one, and present completed tasks, checks actually performed and their results, evidence paths, deviations, and limitations. Await explicit developer approval before progression and record the decision and reference. Plan approval does not satisfy implementation gates; silence is not approval. Honor prior decisions only where they explicitly cover the applicable gate.
- Pause affected work when evidence invalidates the approach or changes requirements or authorized scope. Follow the repository's scope-change procedure and record the change, impact, and decision in the plan. Discover `manage-plan-scope` through repository instructions or available skills when applicable; if unavailable, record the proposed revision and obtain any required authorization before dependent implementation. Routine choices within approved scope can proceed.
- Follow retry or escalation limits actually defined by the repository or plan, linking their source relative to the saved plan when local. This skill supplies no fixed retry count. If repeated failures invalidate the approach, report the attempts, findings, and decision needed before continuing affected work.

## Save and review

Inspect existing plans first. Update the matching plan when appropriate, preserving identifiers, evidence, developer decisions, and history. For a plan already being executed, use the repository's scope-change procedure for substantive replanning rather than silently replacing it.

Save to the repository's prescribed location using its template. If none is specified, use `docs/plans/<story-id-or-short-slug>.md`. Resolve repository paths from the working checkout, and links from the saved plan's location, never from this skill's installation directory.

Where no repository template exists, include:

1. Title, source reference, and draft/review status. Include supplied requirements and acceptance criteria when no durable source exists.
2. Scope, exclusions, dependencies, current-state findings with source references, assumptions, and unresolved prerequisites.
3. Technical approach and rationale sufficient for a separate implementation session.
4. Implementation phases with granular tasks, progress fields, verification, completion criteria, and developer approval gates.
5. Acceptance-criterion mapping to tasks and evidence, with deferred work identified.
6. Execution controls, plan review status, and a place to record scope changes and developer decisions.

Before completion, verify that every in-scope acceptance criterion is mapped, dependencies are feasible, and tasks have concrete file operations, progress fields, expected behavior where applicable, and assessable outcomes. Confirm conditional work is explicit and every implementation phase has a stop instruction and pending developer gate. Check local links and consistency with authoritative requirements and the repository template. Record only validation actually performed; planned checks are not passing results.

Return a link to the saved plan, briefly describe its implementation phases and blockers, and request developer review. Finish within planning scope; implementation requires separate authorization.
