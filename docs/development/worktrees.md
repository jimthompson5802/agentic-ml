# Story worktrees in a shared devcontainer

Use the [manage-story-worktree skill](../../.agents/skills/manage-story-worktree/SKILL.md)
to create, list, resume, or explicitly remove story workspaces. Git's worktree
records are the workspace inventory; owning plans contain story associations,
tasks, evidence, and gate decisions. No separate registry is required.

## Layout and session ownership

Keep the primary checkout open in the existing devcontainer. Create story
worktrees inside it at `.worktrees/US-<number>-<short-slug>`, using branches named
`US-<number>-<short-slug>`. The primary checkout's `.gitignore` excludes this
directory. Discover the primary checkout through Git rather than assuming the
current directory is the primary checkout. Worktrees share Git objects and refs;
their files, indexes, and HEADs are separate.

Create worktrees through container Git so their metadata paths resolve there.
The primary checkout, common `.git` directory, and all story worktrees must remain
visible at the same container paths after restart. Host Git interoperability and
separate containers per story are outside this workflow. Do not change mounts or
rerun `.devcontainer/post-create.sh` for each worktree. Existing container startup
limitations in `CHECKPOINTS.md` remain open until demonstrated.

Start each agent session with its cwd set to its story worktree and re-read its
instructions and checkpoint. Give only one session ownership of a worktree.
Creating a workspace does not transfer another session into it; report the path
for opening a session or use that path explicitly as the command cwd. Keep the
primary checkout available for coordination. Do not switch branches in another
session's checkout.

New worktrees contain committed files from their selected base or existing
branch. Uncommitted skills, plans, and guidance in another checkout do not appear
there. Make the workflow changes available in the selected branch through an
authorized commit/integration before relying on them in a new story session;
do not copy dirty files or auto-publish them.

## Planning, execution, and resumption

A story planning request authorizes creating or reusing that story's local
workspace. Use the explicitly requested base or local `main`, report its commit,
and do not assume it is current with the remote. Environment setup is separate.
Record branch, base/starting commit, issue/story, and primary-relative worktree
location in the owning plan. Keep absolute machine paths in local session output.

Before execution, match the issue and plan to the actual branch and worktree;
inspect edits, evidence, and pending gates. A newly created checkout inherits a
checkpoint from its base: reconcile that summary to the new story before using
it as a resume instruction. Old plans without workspace fields can be associated
after verifying their existing branch, issue, and changes; record unknown branch
provenance rather than inventing it.

An existing in-progress story checkout may continue when its ownership is clear.
Record its location, including `.` for the primary checkout. Do not relocate it
or switch its branch automatically. If it belongs to another story, find or
create the requested story's workspace instead. Contributor-only plans without
a user story may remain in their existing checkout.

Story gates remain independent. Check prerequisite tasks' evidence, approvals,
and availability in the consuming branch before dependent implementation.
Sharing Git objects does not incorporate another branch's changes. Coordinate
overlapping plans and code with their owning session; merges, rebases, and scope
changes retain their separate authorization requirements.

## Environments and concurrent verification

When environment setup or implementation is authorized, run
`uv sync --locked --group dev` from that story's worktree. Each worktree owns its
`.venv` and editable installation. Check `UV_PROJECT_ENVIRONMENT` and active
environment selection before setup; do not let them redirect separate stories
to the same environment. Select that worktree's interpreter in the editor.

Run checks from the selected worktree with the existing
[verification policy](verification.md). Retain the required four-worker
`loadgroup` commands; concurrency does not authorize changing workers, assertions,
or timeouts. Coordinate heavy runs if they compete for resources. Use distinct
temporary bases, JUnit files, logs, experiment storage, and artifact directories
for each invocation. Never share a `--basetemp` path between runs.

The default pytest command targets `tests` in the current worktree; type checks
target `src tests`. The `.worktrees/` ignore rule keeps nested checkouts out of
normal ignore-aware scans. Do not explicitly point checks at another story or
the primary checkout's entire worktree directory. Phase 3 must verify discovery
before claiming the integrated workflow is validated.

## Checkpoints, integration, and removal

Each branch's `CHECKPOINTS.md` describes that checkout's story, current changes,
next task or gate, and verification limits. Keep detailed approvals and evidence
in owning plans and reports. Preserve historical obligations and other stories'
records; do not maintain a shared mutable story-status index.

When an authorized integration brings checkpoint edits to `main`, reconcile its
summary against current `main`, the integrated plan, and existing obligations.
Do not blindly take the incoming story's current-position block, which may refer
to a different branch or obsolete gate. Link the owning plan for historical
detail. This reconciliation does not approve another story or authorize merging.

Keep raw evidence under each checkout's `.dev-records/`, following the
[records guide](records.md). Before explicitly authorized worktree removal, the
management skill copies evidence to a unique archive under the primary checkout's
`.dev-records/worktree-archives/`, verifies it, and records the durable location.
Preserve original evidence path references with the archive's source mapping.
Check all ignored files too: ignored worktrees, environments, and logs can contain
valuable state. Never remove the parent `.worktrees/` directory wholesale.

Removal preserves the branch. It refuses dirty work, unpublished commits,
uncertain publication, active or locked workspaces, or failed evidence
preservation. Do not force removal or infer cleanup authorization from acceptance
or merge. Contributors remain responsible for backing up all retained archives.
