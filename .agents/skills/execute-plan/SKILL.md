---
name: execute-plan
description: Execute or resume a supplied Markdown implementation plan, record verified task progress in its existing format, and stop at each implementation phase boundary for developer approval. Use for execution rather than plan drafting.
---

# Execute a plan

Accept a Markdown plan path supplied by the user. Execute the authorized implementation phase and maintain that file as the progress record. A request to create or edit this skill does not authorize execution of a plan.

## Establish the execution boundary

1. Resolve the working checkout from the user's working directory, independently of where this skill is installed. Read applicable repository instructions, the supplied plan, and relevant repository documentation. Follow pointers to planning terminology, templates, authoritative requirements, dependencies, verification, and gates. If no plan is identified by the request or active session, ask for its path rather than choosing a story to implement.
2. Inspect implementation, task status, recorded evidence, and developer decisions. Preserve earlier results and distinguish observed behavior from design targets. Identify the next incomplete task, its prerequisites, and any pending implementation phase gate. Keep development checkpoints distinct from any workflow phases in the product being built.
3. Treat an instruction to execute the plan as authorization for its next eligible implementation phase, subject to existing gates and scope. Plan approval alone is not execution authorization. Honor explicit prior authorization and gate decisions without asking again. If an earlier implementation phase awaits approval, stop at that gate before starting the next implementation phase.
4. Use the repository's implementation phase boundaries and identifiers. If none exist, treat the plan's executable tasks as one implementation phase with a final developer checkpoint. Resolve material conflicts or missing verification criteria before dependent work; continue independent investigation within scope where useful.

## Execute and record verified progress

- Work through dependencies within the authorized implementation phase. Preserve task identifiers, acceptance criteria, exclusions, and boundaries. Keep later stories and milestones outside the current execution scope.
- Keep progress in the supplied plan's existing format. For checkbox tasks, use `- [ ]` until completion and required verification, then `- [x]`. For task tables, update the status column using the plan's conventions; preserve its columns and structure. Add a minimal status field only when the plan lacks one, keeping reference material separate from executable tasks.
- Verify observable outcomes using the plan's checks, applicable acceptance criteria, and repository tooling. Record actual commands or manual checks, results, and relevant evidence beside tasks or in the plan's verification section. Sanitize evidence and preserve unrelated content.
- Leave partial, failed, blocked, and unverified tasks incomplete, recording the reason and remaining verification. A code edit or unrelated passing tests do not establish completion. If developer verification is part of a task's completion condition, keep that task incomplete until received. Track technical task completion separately from implementation phase gate approval when the plan separates them.
- Update the plan after each verified task. On resumption, inspect relevant changes and reuse valid evidence. Rerun checks when subsequent changes could invalidate it; reopen affected tasks and explain why when evidence becomes invalid.
- Follow retry or escalation limits actually defined by the repository or plan. If repeated failures or evidence invalidate the approach, stop affected work and report attempts, findings, and the decision needed. This skill supplies no repository-specific fixed retry count.
- When outcomes, acceptance criteria, or scope must change, pause affected work and follow the repository's scope-change procedure. Use `manage-plan-scope` when available, discovering it through the environment or repository instructions rather than a fixed installation path. If none exists, record the proposed change and impact in the plan and obtain any missing authorization before affected implementation continues. Preserve existing gate boundaries.

## Stop for developer approval

At the end of **every implementation phase, including the final one**, save progress and stop. Complete authorized tasks and verification before requesting approval; report incomplete work as blocked or partial rather than declaring the implementation phase complete.

Present the plan link, completed tasks, checks and results, evidence, deviations, blockers, and remaining limitations. Use the plan's existing gate fields and statuses. Record technical completion separately from `developer approval pending`, leaving developer acceptance unchecked or pending until explicitly given.

Request explicit developer approval, citing and linking the applicable plan or repository gate rule. If neither defines the checkpoint, cite this skill's requirement: “At the end of every implementation phase, including the final one, save progress and stop.” Explain that this is a checkpoint imposed by the invoked execution skill. Await approval before beginning the next implementation phase; silence and elapsed time are not decisions. A general execution instruction does not satisfy an implementation phase gate.

Record the developer's decision, date, and decision reference in the plan. For changes requested, keep work within the current implementation phase and resolve the requested changes before renewed review. For rejection, record it and stop progression. For approval, mark the gate accordingly and continue only if its progression decision or existing authorization covers the next implementation phase. After final approval, record acceptance without starting another plan or milestone.
