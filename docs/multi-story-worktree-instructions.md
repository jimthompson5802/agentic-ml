# Start two independent user stories

Use two story worktrees, each with its own agent session and Python environment,
inside the existing shared devcontainer. Keep the primary checkout available for
coordination.

## 1. Select the stories

Choose two GitHub issues. Confirm during planning that they have no prerequisite
relationship, conflicting public-interface changes, or competing edits to the
same implementation. Separate worktrees isolate files; planning must establish
whether the stories are independent.

## 2. Create separate plans and worktrees

In the coordination session, request:

> Use create-implementation-plan for issues #A and #B. Create separate story
> worktrees from current main, check their scopes and dependencies for overlap,
> and prepare one plan per story. Do not begin implementation.

Replace `#A` and `#B` with the GitHub issue numbers. Issue numbers and user-story
IDs are distinct.

Planning retrieves each complete issue discussion and uses
[manage-story-worktree](../.agents/skills/manage-story-worktree/SKILL.md) to create
or reuse the story workspace. New workspaces use branches and primary-relative
directories such as:

```text
Branch: US-XX-short-slug
Path:   .worktrees/US-XX-short-slug

Branch: US-YY-short-slug
Path:   .worktrees/US-YY-short-slug
```

The planning session reports each absolute path and selected base commit. A
planning request authorizes the required local workspace creation; environment
setup and implementation require separate authorization.

## 3. Open one agent session per story

Open a separate agent session with its working directory set to each returned
worktree path. Give only one session ownership of each worktree. Each session
reads that checkout's instructions, checkpoint, and owning plan before proceeding.

Use the existing shared devcontainer. Do not create a container or rerun its
lifecycle setup for each story.

## 4. Review plans and authorize execution

Review each saved plan, including its scope, dependencies, public test boundaries,
and verification requirements. Then authorize execution in each owning session:

> Execute docs/plans/<story-plan>.md through the next eligible implementation
> phase, then stop at its approval gate.

Replace `<story-plan>` with that session's saved plan filename. Plan approval
alone does not authorize implementation.

Authorized execution sets up each worktree's own environment with
`uv sync --locked --group dev`, after checking that environment overrides do not
redirect the stories to a shared environment. Select the worktree's interpreter
in the editor.

## 5. Progress and approve each story independently

Both stories can progress concurrently. Each session maintains its own plan,
checkpoint, verification evidence, and approval gates. Explicitly name the story
and gate when approving work; one story's approval does not approve the other.

Coordinate heavy test runs when they compete for resources. Use separate
temporary paths, logs, test reports, experiment storage, and artifact directories.
Follow the repository's verification policy and retain its required worker
settings.

If work reveals a dependency or overlap, coordinate with the owning session and
use the scope-change workflow where required. Sharing Git objects does not make
another branch's changes available in a story checkout. Merging and rebasing
require separate authorization.

After explicit whole-story acceptance and completed gates and verification, the
execution skill follows that story's publication and review workflow. Merging and
worktree cleanup remain separate actions. Preserve validation fixtures and raw
evidence until explicitly authorized cleanup follows the retention rules.

See [story worktree guidance](development/worktrees.md) for the governing workspace,
environment, integration, and cleanup requirements.
