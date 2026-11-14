# Story worktree management — Phase 3 verification

Date: 2026-11-14. Owner: [contributor workflow plan](../plans/story-worktree-management.md).
Authorization: developer message, “i approve gate 2.” This is contributor-tooling
verification, not product-story or milestone acceptance.

## Outcome and boundaries

The native Git walkthrough passed, and two concurrent process sessions in the
existing shared devcontainer used separate story worktrees and editable Python
environments. Their Git metadata and environments remained usable after an
actual container restart, without repair or setup.

This validates native commands and a policy-guided application of the skill.
The skill is agent instructions, not an executable enforcement layer. Refusal
decisions were made from observed Git/file state; no tool automatically enforces
them. No independent assistant evaluation or real story implementation was run.
Archive verification used ordinary files; symlink cleanup rules remain statically
reviewed rather than demonstrated. Windows, host use of container Git paths,
container recreation, and automatic VS Code startup remain unverified.

## Retained records and source identities

Raw commands, outputs, scripts, checksums, and results are retained under:

```text
.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/
```

The host record root is the above path under
`/Users/jim/Desktop/genai/agentic-ml`; inside the container it is under
`/workspaces/agentic-ml`. Back up the records and retained fixtures according to
the [records policy](../development/records.md).

- Source checkout: `main` at `e0b7471`, with the uncommitted workflow changes.
  The container fixture snapshots tracked and nonignored new files; per-file
  SHA-256 identities are in `identities/container-source-snapshot.json`.
- Host: Darwin arm64, Git 2.39.5. `fixture_git.py` uses host Python 3.12.
- Container: existing `48e07bf725be`, image
  `vsc-agentic-ml-18253f941d7676006bbb93ad666044533ac608197677c70f77448dfbc3e63900`,
  user `vscode`, Linux aarch64, Python 3.12.16, uv 0.13.6, Git 2.56.0.
- The container was initially stopped. It was started and restarted for these
  checks without rebuilding, rerunning lifecycle setup, or changing mounts.
  After verification and an idle-process check it was returned to its original
  stopped state; retained files and fixtures remain available on the bind mount.
  Initial sandbox Docker inspection failed with socket permission denied;
  escalated inspection succeeded. This was an access limitation, not a failed
  worktree check.
- Synthetic fixture stories use distinct story and issue numbers. No GitHub
  issues, real story branches, or remotes were changed. The host fixture's bare
  remote is a local filesystem directory, not GitHub publication.

## Commands and observed checks

The retained scripts contain the exact argument arrays and assertions. Their
command manifests record cwd, exit status, stdout, and stderr, including expected
negative Git results. These scripts are verification artifacts, not installed
skill helpers or toolkit APIs.

| Demonstration | Invocation | Result |
|---|---|---|
| Native Git walkthrough | `python3.12 <record-root>/fixture_git.py` | 28 checks passed; details in `commands.json`, `host-checks.json`, `host-result.json`, and `logs/host-*.json` |
| Shared-container sessions | `docker exec -u vscode -w /workspaces/agentic-ml 48e07bf725be python <record-root>/container_demo.py` | 21 checks passed; details in `container-commands.json`, `container-checks.json`, and `container-result.json` |
| Container restart | `docker restart 48e07bf725be` | Exit 0; only idle shell/sleep processes were present before restart |
| Persistence after restart | `docker exec -u vscode -w /workspaces/agentic-ml 48e07bf725be python <record-root>/restart_check.py` | 15 checks passed; exact commands and outcomes in `restart-commands.json` and `restart-result.json` |

For the invocations above, replace `<record-root>` with the retained record path
relative to the checkout. Docker control invocations and environment inspection
are additionally recorded in `container-control.json`.

### Native Git lifecycle

An isolated primary checkout under a temporary directory whose name contains
spaces had two nested worktrees. Verification covered:

- Correct branch/base, top level, shared Git directory, and unchanged caller branch.
- NUL-delimited listing and selection of an existing workspace from both primary
  and linked checkouts. Reuse was a selection decision without another creation.
- Independent edits to the same file, separate plans/checkpoints, and one story's
  gate record remaining pending when another was marked approved in the fixture.
- Git rejection of duplicate branch checkout and an occupied target path. The
  existing path's contents and partial branch from failed creation were retained.
- Policy refusal of cleanup for tracked/untracked changes, unpublished commits,
  and an intentionally corrupted evidence archive. Removal was not invoked for
  those states; the inputs and negative evidence remain available.
- Copying retained diagnostics to the primary fixture's archive, matching file
  inventories/checksums, recording the archive, ordinary worktree removal, and
  survival of the branch, evidence, and other dirty story workspace.

The host fixture remains at `/private/tmp/story worktree phase3-7axwbdbx`.
Only its synthetic beta worktree was removed during the authorized cleanup
demonstration, after verified preservation. Its primary checkout, local bare
remote, dirty alpha workspace, occupied path, and archives are retained.

### Shared-container environments and discovery

A separate repository snapshot was created under the original checkout's ignored
`.worktrees/worktree-validation-d4026fb0/primary/`. This fixture has its own Git
repository; the real checkout still has only its original registered worktree.
Synthetic worktrees are `.worktrees/US-991-alpha` and `.worktrees/US-992-beta`
inside that fixture's primary checkout.

Both sessions ran `uv sync --locked --group dev`, `uv lock --check`, and
`uv run --locked agentic-ml --version` in their own cwd. Python probes verified
different `.venv` prefixes and package paths pointing to each worktree's own
`src/agentic_ml`. Version output matched installed metadata (`0.1.0`). Both lock
hashes matched the source snapshot before/after setup and after restart.
No active-environment overrides were present to remove.

Each story ran:

```sh
uv run --locked pytest -n 4 --dist=loadgroup --collect-only -q
```

The primary fixture ran the equivalent `python -m pytest` command using alpha's
installed interpreter, without creating a third environment. Each collected
991 total cases, selected 723 and deselected 268. The selected node counts were
equal. Sentinel modules under ignored nested worktrees were absent from collection
and were not imported. Collection is not test execution: no passing product-test
count or xdist execution result is claimed.

After restart, the primary fixture and both worktrees resolved their original
paths, common Git directory, and all three registrations. Both editable installs
and CLI commands still worked, with unchanged lock hashes. No repair, resync, or
container setup was performed for the persistence check.

The container fixture and its two environments occupy about 1.8 GB and are
retained for review; removing
them is a separate explicit cleanup operation. Restart persistence does not
establish persistence across container deletion/recreation.

## Final document verification

Skill validation, metadata/local-file-link/whitespace checks, ignore-rule checks,
and `git diff --check` are recorded in the owning plan and raw final-check logs.
No product source, dependency declarations, lockfile, tests, or devcontainer
configuration changed. Full product tests, lint/type checks, and distribution
drivers are outside this instruction-only change's verification boundary.

Gate 3 was approved on 2026-11-14 by the developer's message, “I approve gate 3.”
The approval accepts this evidence and its recorded limitations; it does not
authorize publication or fixture cleanup.

The developer subsequently authorized publication with “commit and push” on
2026-11-14. This publishes the approved workflow instructions and evidence report;
raw evidence and validation fixtures remain outside Git and retained. The owning
plan records publication authorization; Git history and remote verification own
the resulting commit identity and synchronization status.
