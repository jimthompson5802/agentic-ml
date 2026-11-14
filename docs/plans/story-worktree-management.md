# Story worktree management — contributor workflow

## Scope and decisions

Source: developer conversation on 2026-11-14, including the approved three-phase
plan and subsequent instruction, “Implement the plan.” This is contributor
tooling, not a product user story; no milestone or product acceptance is claimed.
The implementation instruction authorized Phase 1. The developer's subsequent
message, “I approve Gate 1,” authorized Phase 2. The developer's later message,
“i approve gate 2,” authorized Phase 3. The developer's final message,
“I approve gate 3,” approved the completed validation and its recorded limitations
on 2026-11-14. All phases and gates are complete. Publication and fixture cleanup
remain separate actions; no product-story acceptance is implied.

Defaults selected by the developer: repository-local skill, separate environment
setup, per-story checkpoints, and one shared devcontainer. Worktrees live under
the primary checkout's ignored `.worktrees/` directory, with one branch, agent
session, and Python environment per story. Use native Git; add no toolkit API,
scripts, or workspace registry. Host-side Git interoperability and separate
containers per story are excluded.

## Phases and granular tasks

| Task ID | Status | Action / component | Depends on | Completion condition |
|---|---|---|---|---|
| WT-IP1-T1 | Complete | Add `manage-story-worktree` skill and UI metadata | None | Create/list/resume/remove instructions cover association, reuse, authorization, container paths, and evidence preservation |
| WT-IP1-T2 | Complete | Validate skill and record review evidence | WT-IP1-T1 | Skill validator, metadata and relative-link checks, whitespace check, and static review pass |
| WT-IP2-T1 | Complete | Integrate planning and execution skills | Gate 1 approved | Delegate worktree selection; verify story association; preserve independent gates |
| WT-IP2-T2 | Complete | Update agent/development guidance, ignore rules, and plan template | WT-IP2-T1 | Define nested worktree convention, per-story checkpoint reconciliation, separate environments and output paths |
| WT-IP3-T1 | Complete | Exercise workflows in an isolated temporary Git repository | Gate 2 approved | Independent changes, creation reuse/conflicts, list/resume, and cleanup refusal/preservation demonstrated |
| WT-IP3-T2 | Complete | Demonstrate two story sessions in shared devcontainer | WT-IP3-T1 | Separate editable environments, independent gates, test discovery, and metadata accessibility after restart verified |
| WT-IP3-T3 | Complete | Final validation and handoff | WT-IP3-T2 | Skill/link/whitespace checks and observed platform limitations recorded |

## Gates

| Gate | Required result | Developer decision / reference | Progression |
|---|---|---|---|
| 1 | Skill and Phase 1 validation reviewable | Approved — developer message “I approve Gate 1,” 2026-11-14 | Phase 2 authorized; stop at Gate 2 |
| 2 | Integrated workflow and documentation reviewable | Approved — developer message “i approve gate 2,” 2026-11-14 | Phase 3 authorized; stop at Gate 3 |
| 3 | Validation evidence and limitations presented | Approved — developer message “I approve gate 3,” 2026-11-14 | Workflow work complete; no automatic publication or cleanup |

## Verification boundaries and evidence

Phase 1 changes agent instructions and metadata only. TDD and executable product
checks do not apply; no toolkit behavior is changed. Static checks cannot prove
agent decisions, Git lifecycle behavior, or container persistence; those remain
Phase 3 obligations. Existing repository verification obligations are unchanged.

- Phase 1 technically complete on 2026-11-14; Gate 1 approved by the developer's
  subsequent message, “I approve Gate 1.”
- `PYTHONPATH=.venv/lib/python3.12/site-packages python3 -S /Users/jim/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/manage-story-worktree`:
  passed, `Skill is valid!`. The path is the installed validator used on this host.
- UI metadata, relative links, final newlines, and new-file whitespace: passed
  using an inline Python document check with the same interpreter invocation.
  It parsed `agents/openai.yaml`, checked the short-description length and skill
  prompt reference, resolved Markdown file links, and checked line endings and
  trailing whitespace in the skill, metadata, and this plan.
- `git diff --check`: passed. New files were also inspected by the document check
  because untracked files are not covered by `git diff`.
- Static review: create/list/resume/remove, branch/path reuse and conflicts,
  workspace-only authorization, no automatic environment setup, container-only
  Git paths, evidence copy/checksums, cleanup refusals, and branch preservation
  are covered. No companion workflow or container configuration was changed.
- Initial validation commands using `.venv/bin/python` could not start (exit 127):
  its symlink points to absent `/usr/local/bin/python3.12`. Host Python also lacked
  PyYAML on its default path. The successful commands used host Python 3.15.2
  with `-S` and the existing pure-Python PyYAML files via `PYTHONPATH`; no package
  installation, environment repair, or compiled Linux extension was used.
- Observed host: Darwin arm64. These document checks are not locked toolkit
  checks and do not establish Python 3.12 or devcontainer functionality.
- No devcontainer restart, worktree lifecycle demonstration, environment setup,
  product tests, or platform support claims in Phase 1.

### Phase 2 — integrated workflow review

Technically complete on 2026-11-14; Gate 2 approved by the developer's subsequent
message, “i approve gate 2.” The changes are agent
instructions, contributor documentation/template, and an ignore rule. TDD and
executable product checks do not apply; no Python or toolkit behavior changed.

- Planning delegates workspace creation/reuse to the new skill rather than
  switching branches. Execution verifies the issue, plan, branch, and workspace
  before changes and publication. Existing gates and acceptance rules remain.
- Added `docs/development/worktrees.md`, linked from agent instructions and the
  development reading map. Updated the story plan template, checkpoint maintenance
  rules, and records guide. Added `/.worktrees/` to `.gitignore`.
- Static review covered new vs. existing story checkouts, detached/conflicting
  associations, coordinated prerequisite ownership, per-story checkpoints and
  integration reconciliation, separate environments and outputs, evidence
  preservation, and unchanged test-worker obligations. Contributor-only work may
  remain in its existing checkout. No companion PR skill change was needed.
- Skill validation passed for `manage-story-worktree`,
  `create-implementation-plan`, and `execute-plan`. Command:
  `PYTHONPATH=.venv/lib/python3.12/site-packages python3 -S -`, with an inline
  Python check loading the installed `quick_validate.py` via `runpy.run_path`
  and calling `validate_skill` for each of the three directories. Each returned
  `Skill is valid!`.
- File-link, line-ending, whitespace, and UI metadata validation passed across
  all 12 changed/new files. The same inline Python invocation enumerated
  `git diff --name-only` and `git ls-files --others --exclude-standard`, checked
  local Markdown file targets, final newlines and trailing whitespace, and parsed
  the new UI YAML. It checked description length and the invocation reference.
  Anchor resolution and behavioral correctness are outside this static check.
- `git diff --check`: passed.
- `git check-ignore -v .worktrees/probe`: passed; matched `.gitignore` line 68.
  This checks the rule without creating a worktree or probe file.
- Host/interpreter limitations from Phase 1 remain. No environment was repaired,
  no dependency installed, and no container configuration or lifecycle changed.
  New worktrees will need the workflow's committed files available in their base
  or branch; uncommitted integration files are not inherited automatically.
- Phase 3 retains Git lifecycle, environment isolation, test discovery, and shared
  devcontainer restart demonstrations. No Phase 3 task was executed, and no
  remote synchronization, commits, publication, or cleanup was performed.

### Phase 3 — behavioral demonstration and final checks

Technically complete on 2026-11-14; Gate 3 subsequently approved by the developer's
message, “I approve gate 3.” The
[verification report](../verification/story-worktree-management.md) owns detailed
commands, results, source identities, fixture locations, and limits. Raw evidence
is retained in `.dev-records/verification/20261114T173007Z-e0b7471-worktrees-d4026fb0/`.

- `python3.12 <record-root>/fixture_git.py`: 28 host checks passed. Native Git
  operations and policy-guided decisions covered creation/reuse, listing/resume,
  conflicting paths/branches, independent files and gate records, refusal of
  unsafe cleanup, and verified evidence preservation before ordinary removal.
  Negative Git results and intentionally mismatched archive evidence are retained.
- `docker exec -u vscode -w /workspaces/agentic-ml 48e07bf725be python <record-root>/container_demo.py`:
  21 checks passed using two concurrent story process sessions in the existing
  shared devcontainer. Each had a distinct editable environment and package path;
  locked setup, lock consistency, and CLI smoke checks passed. No real story was
  implemented and no independent assistant evaluation was performed.
- Default collection selected 723 of 991 cases, deselecting 268, in each story
  worktree and the primary fixture. Nested sentinel modules were excluded. This
  was collection only, not a product-test run or story acceptance.
- `docker restart 48e07bf725be`, followed by
  `docker exec -u vscode -w /workspaces/agentic-ml 48e07bf725be python <record-root>/restart_check.py`:
  15 checks passed. Original worktree paths, registrations, common Git metadata,
  editable environments, CLI commands, and lock hashes survived restart without
  repair or setup. Only idle shell/sleep processes were present before restart.
- The container was already present but stopped. Docker inspection initially
  required sandbox escalation; approved Docker commands then started/restarted
  it. It was returned to its original stopped state after idle-process checks.
  No rebuilding, lifecycle setup, mount changes, or container provisioning occurred.
- Final skill validation passed for all three skills. Metadata, local file-link,
  line-ending, and whitespace checks passed across 13 changed/new files;
  `git diff --check` and worktree ignore checks passed. Commands and final results
  are retained with the raw records. Local link checks do not resolve anchors.
- The real checkout remains `main` at `e0b7471` with only its original registered
  worktree. Its source and lockfile were not changed. Changes remain uncommitted
  workflow instructions, documentation, metadata, checkpoint, and ignore rules.
- Demonstration fixtures are retained separately from raw records. The container
  fixture, including two environments, occupies about 1.8 GB under the ignored
  `.worktrees/worktree-validation-d4026fb0/` directory. Cleanup requires a separate
  explicit request. The host fixture and its archive remain at the report's path.
- These are instruction-only changes, not toolkit executable changes; TDD,
  product suite execution, lint/type checks, and artifact drivers do not apply.
  Native operations and walkthrough decisions do not establish automatic skill
  enforcement. Symlink archive cases, container recreation, automatic VS Code
  startup, and Windows remain unverified. Existing historical obligations remain.

In the commands above, `<record-root>` is the retained record path relative to
the checkout. Host checks used Darwin arm64/Git 2.39.5; container checks used
Linux aarch64/Python 3.12.16/uv 0.13.6/Git 2.56.0. No verification criteria or
existing assertions were reduced, and no corrective implementation attempts
were needed. Gate 3 is approved. Its approval alone did not authorize publication
or real-story cleanup; the later publication instruction is recorded below.

## Publication authorization

The developer's subsequent message, “commit and push,” on 2026-11-14 authorizes
committing the approved workflow changes and pushing the current `main` branch
to `origin`. Before publication, `git ls-remote origin refs/heads/main` confirmed
the remote still matched local parent `e0b7471`. Commit identifiers and completed
publication are established by Git history, remote verification, and retained raw
publication records. No PR, branch cleanup, or fixture removal was requested.

## Scope-change history

None. The saved plan records the approved conversation plan for resumability;
it does not add product scope or authorize subsequent gates.
