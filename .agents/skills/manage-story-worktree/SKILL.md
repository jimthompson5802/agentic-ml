---
name: manage-story-worktree
description: Create, list, resume, or remove Git worktrees associated with user stories. Use directly for story workspace management or from planning and execution workflows; workspace operations do not authorize story implementation.
---

# Manage a story worktree

Use native Git commands to manage one branch and worktree per story. Resolve the
working repository from the user's cwd, independently of this skill's location.
Read its agent instructions and development guidance. In this repository, use
one shared devcontainer with a separate agent session per story.

## Resolve the repository and operation

Inspect `git rev-parse --show-toplevel`,
`git rev-parse --path-format=absolute --git-common-dir`, and
`git worktree list --porcelain -z`. Parse the NUL-delimited output without
splitting paths on whitespace. Identify the primary checkout from Git's worktree
records and verify that its `.git` directory is the common directory. Do not
derive the primary checkout from the current linked worktree's parent directory.
Report unsupported bare repositories, inaccessible Git metadata, missing primary
checkouts, or ambiguous associations before mutation. Do not repair paths or
prune registrations automatically.

Identify the requested operation: create, list, resume, or remove. Inspection is
read-only. A create request authorizes local branch/worktree creation; planning
or execution can supply that authorization when their workflow explicitly calls
for it. Resume locates a workspace; it does not start implementation. Removal
requires an explicit cleanup request naming the worktree or story. Do not infer
cleanup authorization from a merge, story acceptance, or a request to list.

Before mutation, recheck the relevant registration, branch, and path. Preserve
unrelated edits and report conflicts rather than overwriting them. Quote paths
and Git refs safely; pass the selected worktree as each tool command's cwd.

## Create or reuse

1. Resolve the issue and story identifier from the request and owning plan. Use
   the repository's complete issue-retrieval workflow before story planning or
   implementation. Do not equate GitHub issue numbers with story numbers. Ask
   only when the intended story remains ambiguous.
2. Use branch `US-<number>-<short-slug>` and primary-checkout-relative directory
   `.worktrees/US-<number>-<short-slug>`. Honor an explicitly supplied matching
   branch or worktree. List registrations before creating anything. If the
   branch already has a matching worktree, reuse it after checking its story
   association. If an existing branch has no worktree, attach it without resetting
   its commits. Conflicting story associations or occupied paths need resolution;
   do not add suffixes or force a second checkout of the branch.
3. For a new branch, use the explicitly selected base or local `main`. Verify the
   ref and record its commit before creation. Missing bases require direction.
   Do not fetch, pull, or claim that local `main` is synchronized without evidence.
4. Ensure the primary checkout ignores `.worktrees/` before creating the
   directory. Follow the repository's ignore convention; if it is absent, report
   the required ignore change rather than silently editing unrelated configuration.
   Create through `git worktree add -b BRANCH PATH BASE`, or
   `git worktree add PATH BRANCH` for an existing unattached branch. Substitute
   resolved arguments; do not switch the caller's branch or copy its dirty files.
5. From the selected worktree, verify its top level, branch, HEAD, common Git
   directory, and status. Report its absolute working path, primary-relative
   location, story/issue, branch, base commit for a new branch, and whether it was
   created or reused. If creation fails, inspect state before retrying; leave
   partial branches intact and report them instead of deleting them automatically.

Create and manage these worktrees inside the shared container. Their Git metadata
must resolve inside that container, including after restart. Do not assume a host
Git process can use container paths. Do not create containers, change mounts, or
rerun container lifecycle scripts as part of creating a story workspace.

Environment setup is separate. When setup or implementation is authorized, run
`uv sync --locked --group dev` in the selected worktree, with its own `.venv`.
Check environment overrides before synchronization so they cannot redirect two
stories to the same environment. Never reuse another story's editable install.

## List or resume

List each registered worktree's path, branch or detached state, HEAD, dirty state,
and upstream status. Distinguish unavailable remote information from a known
published state; these operations do not fetch. Include locked or missing paths
without attempting repairs. Link the owning story plan when identifiable from
the worktree's files; leave unknown associations explicit rather than inventing
a registry.

For resume, verify the requested story matches the branch and owning plan. Read
that checkout's `CHECKPOINTS.md`, the plan, and relevant issue decisions. Reconcile
them with actual changes, evidence, and approvals. Report the next eligible task
or pending gate and the working path for a session there. Do not infer approval
from task completion or resume another story's work.

One agent session owns a story worktree at a time. Do not move a live session's
workspace or operate on its branch from another session. Each story retains its
own gates. Read prerequisite plans and evidence before dependent work; changing
another story's scope follows the repository's scope-change procedure.

## Remove an explicitly selected worktree

1. Confirm the target is a registered linked worktree, not the primary checkout,
   current command cwd, or a workspace used by an active session or test process.
   Resolve uncertain active use before removal. Run cleanup from the primary
   checkout. A locked worktree requires direction; do not unlock it automatically.
2. Inspect tracked changes, untracked files, ignored files, and upstream state.
   Refuse removal with tracked or untracked work, unpublished commits, or unknown
   publication status. Compare HEAD against a verified remote-tracking ref; with
   no upstream, a verified remote ref containing HEAD can establish publication.
   Report the ref and limits of local remote-tracking information. Do not push,
   discard files, or weaken these checks to make cleanup succeed.
3. Follow the repository's [evidence retention rules](../../../docs/development/records.md).
   If `.dev-records/` exists, copy it into a new, uniquely named archive under the
   primary checkout's `.dev-records/worktree-archives/`, outside the target.
   Preserve the source, inventory all files and links, compare file checksums and
   link targets, and record the source path, branch, HEAD, archive path, and check
   result in the archive. Reject links whose targets would disappear with the
   worktree. Failed or incomplete preservation blocks removal. Never migrate or
   delete existing historical evidence as incidental cleanup.
4. Account for every other ignored entry. Identify disposable environments and
   caches in the cleanup report; preserve logs, experiment outputs, retained
   workspaces, or unknown content before removal. An explicit worktree cleanup
   request covers identified disposable generated files, not unidentified data.
5. After preservation succeeds, record the archive location in the primary
   checkout's checkpoint as required, then recheck status and registration. Use
   ordinary `git worktree remove PATH`, without force. Verify registration and
   path removal, branch preservation, and archive availability. Report the outcome
   and durable evidence location. If Git refuses removal, preserve the state and
   report its reason; do not substitute recursive deletion or automatic pruning.

Branch deletion, merging, rebasing, publication, Git configuration changes, and
container provisioning are separate operations. This skill does not authorize
them. Finish with the observed workspace state and any decision blocking the
requested operation.
