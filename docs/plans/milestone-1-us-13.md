# Milestone 1 / US-13: Version datasets with native DVC

## Scope and outcome

- **Milestone:** M1 — Complete one local classification experiment.
- **User story:** [US-13 / issue #16](https://github.com/jimthompson5802/agentic-ml/issues/16).
- **User-visible outcome:** A separate experiment project versions local source
  snapshots, extraction outputs, saved split manifests and derived datasets with
  native DVC through one complete runnable recipe in `docs/dataset-versioning.md`.
  Git records metadata and relevant manifests, while dataset bytes
  remain excluded and are stored in the configured local cache/remote.
- **Acceptance criteria covered:** [US-13-AC-01](../specs/user-stories.md#us-13-ac-01)
  and [US-13-AC-02](../specs/user-stories.md#us-13-ac-02).
- **Scope boundaries:** This is the M1 slice. Restoration/hash verification and
  missing/mismatched restoration failures, AC-03/04, remain M2. Native pipeline
  stages/replay belong to US-27; MLflow links to US-26; assistant and complete
  experiment integration to US-39/40. No training, scheduler, mandatory experiment
  approvals, new workflow database, cloud connector or source-capture service.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
  [data ownership](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts),
  [interfaces](../specs/design/interfaces-and-configuration.md),
  [native DVC](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction),
  [layout](../specs/design/repository-layout.md),
  [ADR-008](../specs/design/architecture-decisions.md#adr-008--local-experiment-mvp-and-externally-owned-assistant-use),
  [traceability](../specs/design/acceptance-traceability.md), and
  [capability order](../specs/design/milestone-delivery.md#capability-order-and-owning-stories).
- **Coordinated execution index:** None. Accepted prerequisites are reused;
  no new tasks owned by another story are included.

### Authoritative issue snapshot

Retrieved complete issue body and every comment page on 2026-11-13 UTC.
Issue is open, author `jimthompson5802`, label `enhancement`, no assignees,
and no GitHub milestone field. Its body explicitly assigns AC-01/02 to M1 and
AC-03/04 to M2. Created 2026-10-30T02:06:29Z; updated
2026-11-07T00:28:44Z. One unique comment was retrieved, matching the reported
count; the final metadata refresh had the same count/update time. This is an
issue, not a pull request. Initial sandbox network reads failed; successful
reads outside the sandbox supplied the complete stable snapshot.

The [scope-decision comment](https://github.com/jimthompson5802/agentic-ml/issues/16#issuecomment-6699586819)
is by `jimthompson5802`, ID `6699586819`, created/updated
2026-11-07T00:28:44Z. It preserves MVP-SC-01/MVP-SC-02 approvals and milestone
assignments without claiming executable acceptance. The issue and current local
stories agree. Refresh the full discussion before execution and resolve changes
before affected work. This planning request authorizes no GitHub edits.

The two criteria retain their issue meaning:

- **AC-01:** DVC versions source snapshots, split manifests, and derived datasets
  as those artifacts are introduced.
- **AC-02:** Git tracks DVC metadata and relevant manifests while dataset content
  resides in the configured cache/storage and is excluded from Git.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Installed package and DVC storage | Normal dependency, Git project, local DVC cache/default remote | IP2/IP3 | Existing `pyproject.toml` declares DVC 3; `src/agentic_ml/initialization/storage.py` configures stores. [US-02 plan](milestone-1-us-02.md) accepted; [US-41 plan](milestone-50-us-41.md) accepts local wheel setup. Initialization does not yet version data. |
| Extraction source/output identities | Published CSV/Parquet plus `extraction.json` | IP2 composition | [US-11 plan](milestone-1-us-11.md), IP2/IP3 complete, Gates 1–3 approved, story accepted. [Extraction contract](../extraction.md) provides SHA-256, not a DVC identity. |
| Recorded partitions | Native frame partitions and project-persisted JSON | IP2 composition | [Issue #19 plan](milestone-1-us-12-assessment-splits.md), IP3/IP4 complete, Gates 1–4 approved, AC-02/03 accepted. [Contract](../data-assessment-and-splits.md) leaves persistence to the project. |
| Native commands versus toolkit integration | Establish the smallest missing reusable behavior, if any | All executable work | Default: native `dvc add`/`push` with a documented project recipe; no new toolkit API. IP1-T1/T2 settle this. Any required reusable capability belongs in the installable package and requires reviewed signatures/errors/test boundaries first. |
| Split manifest ownership | DVC versions exact saved membership; Git retains relevant readable manifests without conflicting ownership | IP2 | One authoritative DVC-versioned split record; Git tracks native pointers, project configuration and relevant existing manifests. No duplicate split record by default; confirm at Gate 1. |
| Stable source snapshots and identity links | Sources consumed by extraction match the DVC-versioned bytes; extraction SHA-256 and native DVC hashes remain distinct | IP2 | Project snapshots and references proposed below; confirm at Gate 1. No mutation-proof or hostile-code guarantee. |
| M2 restoration | Separate milestone plan for AC-03/04 | Future restoration acceptance | Deferred by issue, not a prerequisite to M1. Leave #16 open after M1 acceptance. |

## Current state and proposed technical approach

Planning baseline: `4a4fb97` on local branch `US-13-dataset-versioning`.
No matching US-13 plan existed. The working tree was clean before planning.
There is no implemented dataset-versioning public toolkit API. Existing
`extract_data` publishes a fresh output bundle; `create_partitions` returns a
record, and project code saves it. Their accepted schemas and behavior remain
the compatibility baseline.

Reuse DVC's own implementation: [add](https://doc.dvc.org/command-reference/add)
records file/directory outputs and populates its cache;
[push](https://doc.dvc.org/command-reference/push) transfers cached content to the
configured remote. Native [.dvc metadata](https://doc.dvc.org/user-guide/project-structure/dvc-files)
records output paths and hashes. These official references were checked on
2026-11-13; IP1 must confirm behavior against the project's installed version.
No external dependency installation or executable probe was performed during planning.

Proposed experiment layout, to finalize in IP1:

| Project path | Owner and storage |
|---|---|
| `data/source/` | Project copies of explicit local CSV/Parquet inputs; DVC content, excluded from Git. Extraction reads these snapshots. External original inputs remain untouched. |
| `data/extracted/` | Complete published extraction bundle, including `dataset.*` and `extraction.json`; DVC content. Do not modify an accepted extraction report to insert DVC hashes after publication. |
| `data/partitions/` | Project-written partition files and exact saved split record; DVC content. Cover two-way and three-way layouts. |
| `data/derived/` | Small project-authored deterministic pandas output, introduced to verify generic derived-data versioning; no new feature-pipeline capability. |
| Project configuration and relevant existing project manifests | Git tracks input/output paths, extraction/split settings and nonsecret references. Native `.dvc` metadata identifies versioned content. Gate 1 identifies the concrete files and checks AC-02 coverage. |
| `data/*.dvc`, generated `.gitignore` files, `.dvc/config` | Git metadata; commit nonsecret configuration only. `.dvc/config.local`, cache, remote bytes and local credentials remain excluded. |

One authoritative split record lives in `data/partitions/` and is versioned
with DVC. Git tracks its native pointer and the relevant project configuration/
existing manifests; a duplicate record and custom `data-references.json` are not
baseline deliverables. Gate 1 must identify any uncovered consumer need before
adding either. Native hashes and accepted extraction/source identities remain
separate, inspectable records rather than a new metadata service.

The recipe must include every required project Python fragment and shell command:
prepare source snapshots, invoke installed extraction and partition helpers, save
records, register artifacts, push to local storage and commit metadata. Its test
adapter may supply temporary paths and capture results but must execute the same
documented code/commands. It must not substitute a parallel test-only workflow.
US-39 receives this recipe and artifact paths for later experiment integration.

Run project scripts and native DVC with explicit project root/cwd and the selected
project environment. Use an isolated local filesystem remote, including an
externally located remote case; no cloud account is needed. Dataset publication
and remote transfer are separate outcomes. A failed command must expose its
nonzero status/output. Successful local versioning remains valid if a later
remote transfer fails; report the transfer as failed without claiming remote
availability. Do not
promise rollback across separate DVC/Git commands or automatic commits.

IP1 must specify input/path validation, already-Git-tracked data handling,
existing DVC ownership conflicts, repeated registration, changed data, failed
transfer. Use native diagnostics and existing input checks; do not add a generic
validation, transaction or publication-state layer. Never silently untrack user
data or rewrite their remotes. Native behavior that already meets a requirement
needs integration evidence, not a redundant wrapper or a manufactured failing test.

## Plan review

- **Status:** Approved — M1 slice only.
- **Developer decision:** Approved plan; commit planning changes.
- **Decision reference and date:** Developer “i approve plan; commit changes”,
  2026-11-13. IP1 execution was subsequently authorized; see the execution record
  below. Gate 1 is Approved; IP2/IP3 remain Not started.
- **Requested plan changes:** Developer authorized the four MVP-focused recommendations
  with “ok make the update” on 2026-11-13. Applied below; this authorizes draft
  revision only, not plan approval or implementation.
- **Public boundaries:** Confirmed at Gate 1 on 2026-11-13 by developer
  “i approve gate 1; commit changes”. Later implementation gates remain Pending.

### IP1 execution authorization — 2026-11-13

Developer “I approve ip1” authorizes execution of IP1 only. Because IP1 tasks
have not started and no Gate 1 evidence exists, this is not recorded as approval
of completed work or confirmation of the proposed public boundaries. Gate 1
remains Pending; IP2 is not authorized.

The initial issue refresh was blocked by missing GitHub authentication
(`gh auth status`: 1; repository helper: 4). Developer “resume” continued IP1
on 2026-11-13; authentication is now available. Complete body/all comment pages
and final metadata were refreshed: one unique comment matched count 1; unchanged
update timestamp 2026-11-07T00:28:44Z. No issue/design conflict was found.
IP1-T1/T2/T3 are complete with [evidence](../verification/us-13-ip1.md) and the
[candidate recipe/contract](../dataset-versioning.md). No new toolkit API is
needed. Developer “i approve gate 1; commit changes” approved the completed
review package, native-only contract and public boundaries on 2026-11-13, and
authorized committing IP1 changes. IP2 remains Not started; this request is
limited to recording approval and committing changes.

## Scope-change history

### US-13-PLAN-REV-01 — MVP-focused draft revision, 2026-11-13

- **Request and decision:** Developer “ok make the update” authorized the four
  recommendations following the [gap review](../reviews/us-13-m1-plan-review.md).
- **Changes:** Require one runnable user recipe; default to one DVC-owned split
  record and native metadata; verify committed versions A/B and retained content;
  use native DVC and existing installed verification infrastructure by default.
- **Impact:** Refines IP1 contracts, IP2 tasks/scenarios and IP3 installed checks.
  AC-01/02 and M1/M2 boundaries are unchanged. No executed tasks or evidence exist
  to invalidate. All tasks remain Not started and all gates Pending.
- **Resume point:** Draft plan review; implementation is not authorized.

During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md)
for substantive revisions; record impact, decision, verification renewal and resume point.

## US-13 / Implementation Phase 1: Settle native DVC integration contracts

- **Outcome:** A concrete, reviewed file/identity/failure contract and confirmed
  public test boundaries, with a decision on whether reusable package code is needed.
- **Entry conditions:** Developer authorizes this implementation phase; refresh issue #16.
- **Acceptance criteria advanced:** AC-01/02 design and verification definition only.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-13-IP1-T1 | Complete | Inspect installed DVC public CLI/help and accepted source/split contracts; write proposed `docs/verification/us-13-ip1.md`. Inspect `src/agentic_ml/initialization/storage.py`, native configuration and existing installed probe infrastructure. | Issue refresh | Record exact DVC version, command/cwd forms, local file/directory support, store ownership and any library gap. Native feasibility commands use disposable projects, not the checkout. No product code or executable tests yet. | AC-01/02 |
| US-13-IP1-T2 | Complete | Finalize proposed `docs/dataset-versioning.md` contract and this plan: the runnable recipe outline, paths, authoritative split record, Git-owned manifests, native hash domains, version-history/transfer checks and any demonstrated package gap. | T1 | Identify exact recipe commands and copyable project code, native versus new behavior, relevant Git manifests and US-39 handoff. Any new API needs a demonstrated requirement gap, exact signature and reviewed boundaries. Refine IP2 task paths before approval; scope changes use the owning procedure. | AC-01/02 |
| US-13-IP1-T3 | Complete | Review test scenario matrix and boundaries below; record decisions/evidence and update `CHECKPOINTS.md`. | T2 | Gate 1 review package identifies every planned executable boundary, expected result and limit; no implementation acceptance claimed. | AC-01/02 |

### Verification and review evidence

Documentation/contract phase: check relative links and `git diff --check`.
TDD and milestone pytest are inapplicable until executable behavior is changed.
Native feasibility observations are recorded as observations, not acceptance tests.
No standalone artifact drivers or broader pytest runs are authorized by this plan.

**Gate 1:** Approved, 2026-11-13. Developer decision:
“i approve gate 1; commit changes”. T1–T3 are complete. Approval confirms the
[IP1 evidence](../verification/us-13-ip1.md),
[recipe contract](../dataset-versioning.md), native-only approach, single-record
ownership and public test boundaries. Native DVC 3.67.1 feasibility, relative-file
links and `git diff --check` provide IP1 evidence; no executable acceptance is
claimed. Requested changes: None. Progression: commit this review package;
IP2 remains Not started pending execution direction.

## US-13 / Implementation Phase 2: Version project artifacts and verify Git ownership

- **Outcome:** A working project-owned native DVC workflow with criterion-based
  integration checks and actionable failure evidence.
- **Entry conditions:** Gate 1 approved; exact contract and boundaries confirmed.
- **Acceptance criteria advanced:** AC-01/02.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-13-IP2-T1 | Not started | Develop the complete runnable recipe in proposed `docs/dataset-versioning.md` and integration checks in proposed `tests/integration/test_dataset_versioning.py`; version explicit local source snapshots and extraction bundles with native DVC. | Gate 1 | Users can copy all required code/commands into a separate installed project without test-file imports. Tests execute the same documented recipe, not a separately maintained workflow. CSV/Parquet bytes and independent hashes agree with native metadata; extraction consumes recorded snapshots. Use red–green slices for new/corrected supported behavior; record results. Existing native capabilities use positive/boundary evidence without artificial red claims. | AC-01/02 |
| US-13-IP2-T2 | Not started | Extend the documented recipe and checks for one authoritative saved split record, native DVC pointers and deterministic derived data; implement only any package seam justified and approved at Gate 1. | T1 | Both layouts preserve literal supplied membership and JSON round-trip in the single DVC-owned record. Git retains native metadata, project settings and relevant manifests; no duplicate split copy or custom reference schema by default. Native references match actual outputs; changed source, split or derived bytes produce changed corresponding identities; unchanged registration retains identity. No training or stage execution claim. | AC-01/02 |
| US-13-IP2-T3 | Not started | Add real fixture commits A/B, Git index checks, cache/local-remote retention and native failure cases through the documented recipe. | T2 | Commit A records original content; B records changed content. Inspect both commits’ native metadata/manifests through Git and compare independently expected identities. Both versions remain in cache and configured local storage after their respective transfers. Dataset/cache/remote bytes are absent from `git ls-files`. Missing targets, tracked-data/ownership conflicts and controlled transfer failure preserve native diagnostics and existing configuration; failed push does not imply failed local registration. | AC-01/02 |
| US-13-IP2-T4 | Not started | Run phase/shared checks, record proposed `docs/verification/us-13-ip2.md`, update this plan and checkpoint. | T3 | M1 and shared checks pass; actual counts, red/green results, identities, attempts and limitations recorded. | AC-01/02 |

### Public boundaries and independently defined scenarios

Gate 1 must confirm these boundaries before tests are written. The
[IP1 review](../verification/us-13-ip1.md) proposes the concrete files and oracles;
duplicate native pointers supply the ownership-conflict fixture (adding an
existing directory member instead updates its owner). The single recipe source
is the named configuration, project-script and shell fragments in the guide:

| Boundary | Observable check | Coverage limit |
|---|---|---|
| Documented recipe using installed `extract_data`, `create_partitions`, project persistence and native DVC CLI | Execute the same copyable code/commands from the guide in a separate root/cwd; real files, native metadata/status and command exit/stdout/stderr; no DVC-internal mocks or test-only workflow dependency | No hostile concurrent mutation or OS isolation guarantee |
| Source/extraction | Literal small CSV and equivalent Parquet data; independent byte SHA-256 and native file hash comparison; extraction report identifies consumed snapshots | Native DVC hash and extraction SHA-256 are separate identities; no cross-version Parquet canonicalization |
| Partitions/derived output | Five rows with IDs 0–4 and labels A–E; supplied two-way train `[0,2,4]`, test `[1,3]`; three-way train `[0,2,4]`, validation `[1]`, test `[3]`. Project-derived output selects IDs `[0,2,4]`. Compare exact records/rows and saved bytes | No new splitting algorithm, feature model, fitted state or test-driven tuning |
| Git/DVC ownership | Real fixture commits A/B and `git ls-files`/`git check-ignore`; one DVC-owned split record, Git-owned configuration/relevant manifests, native pointers and actual stored content | No toolkit repository publication; Git operations occur only in disposable experiment fixtures |
| Version retention | Read native metadata/manifests from commits A/B; compare independent expected content identities and verify both versions remain in isolated cache and local remote after update/push | No checkout/pull/restoration test; AC-03/04 remain M2 |
| Failures/changes | Missing target, existing Git data, conflicting DVC ownership, bad local remote, source/split/derived changes, unchanged repetition; report local registration and remote transfer separately | Missing/corrupt restoration and native stage invalidation are M2/US-27 work |
| Installed artifacts (IP3) | Same project workflow under direct and sdist-rebuilt normal wheel installations, Python `-I`, clean runtime dependencies and unrelated cwd | No editable import, toolkit-source path injection, notebook or assistant certification |

Use independently specified expected rows, byte hashes and Git file inventories;
do not derive expectations solely from the recipe’s observed outputs. For directory
outputs verify their member references/content through native DVC and independent
file bytes; do not implement a second DVC directory-hash algorithm.

### Verification and review evidence

- Focused red–green command after Gate 1: `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_dataset_versioning.py -k <reviewed-case>`.
- Phase gate: `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1`.
- Mark tests `milestone_1` only for directly verified M1 criteria. Preserve
  existing groups, isolation, assertions, timeouts and skips.
- Shared checks at every executable gate: `uv sync --locked --group dev`,
  `uv lock --check`, `uv run --locked ruff check .`,
  `uv run --locked ruff format --check .`,
  `uv run --locked mypy src tests`, `uv run --locked agentic-ml --version`,
  `git diff --check`. Record `uv.lock` SHA-256 before/after; no dependency change
  is anticipated. Any intentional change requires review and consistent declarations.
- Actual results/evidence: Pending. Record collected/selected/deselected/pass/fail/skip
  counts, environment/tool versions, commands/cwd and failure output. Raw records
  follow [retention policy](../development/records.md).
- Deferred checks: IP3-T1/T3 own both installed wheel paths and final M1–6 checks.
  Other milestone/infrastructure checks remain with their existing owners.

**Gate 2:** Pending. Stop after T1–T4 and present criterion-mapped evidence,
changes, deviations and limitations. Await explicit approval before IP3.
Decision reference/date, requested changes and progression authorization: Pending.

## US-13 / Implementation Phase 3: Verify installed workflow and accept M1 slice

- **Outcome:** Independently verified installed data-versioning workflow and a
  finished user guide, without claiming M2 restoration or whole-issue completion.
- **Entry conditions:** Gate 2 approved.
- **Acceptance criteria verified:** AC-01/02 only.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-13-IP3-T1 | Not started | Extend the installed project probe in `tests/installation/check_assessment_splits.py` and its existing `verify_assessment_splits.py` driver, with milestone-1 coverage in `tests/integration/test_distribution_verification.py`; reuse their direct/rebuilt environments, scheduling group and retained records. Copy guide-derived recipe/configuration into both environments, extend the existing assessment/splits probe and its both-artifact test to require US-13 results; preserve current checks/identities. No new independent build/install driver. | Gate 2 | Pytest builds/installs both wheel paths and runs project code outside the checkout with declared runtime dependencies. Each path executes the documented recipe and independently verifies success, Git exclusions, both committed versions and retained content, repeated/changed identities and representative failures. Preserve identities, records and import origins for both. | AC-01/02 |
| US-13-IP3-T2 | Not started | Finish proposed `docs/dataset-versioning.md`; link from `README.md`, `docs/extraction.md`, `docs/data-assessment-and-splits.md`; update affected active design/traceability status only after evidence. | T1 | The complete copyable recipe matches installed evidence and requires no toolkit checkout/test internals; explicit root/cwd, ownership, add versus push, recovery, two-version history and M2 handoff are documented. Identify the recipe/artifact paths US-39 can reuse without adding training or assistant work here. Existing packaged resources remain unchanged unless separately reviewed. | AC-01/02 |
| US-13-IP3-T3 | Not started | Complete final verification below, write proposed `docs/verification/us-13-ip3.md`, update owning plan, `docs/project-status.md` and `CHECKPOINTS.md`. | T2 | Final M1, M1–6 and shared checks pass; exclusions/skips reconciled. Present M1-slice acceptance with #16 still open for M2; do not mark unapproved acceptance as complete. | AC-01/02 |

### Verification and review evidence

Use IP2's confirmed boundaries and shared checks. Run both phase M1 and final
M1–6 commands below. Installed tests may invoke the artifact drivers internally;
do not launch standalone drivers or broader local pytest without an explicit
developer command. Reuse existing ownership/cleanup helpers and isolated bases;
raw evidence must survive successful temporary-workspace cleanup.

Actual results, platform, command logs, artifact identities and limitations: Pending.

**Gate 3:** Pending. Stop after T1–T3. Present both installed paths, final test
results, user guidance and AC-01/02 mapping. Explicitly request acceptance of the
M1 slice; whole US-13 remains incomplete. Decision reference/date, requested
changes, evidence and any publication authorization: Pending.

## Final verification requirements

- **Owning final phase/task:** US-13-IP3-T3, before Gate 3.
- **Final identity:** Record tested revision, working-tree diff, lock hashes,
  source/wheel identities, Python/uv/DVC versions and OS/architecture.
- **M1 gate:** `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1`.
- **M1–6 acceptance:** `uv run --locked pytest -n 4 --dist=loadgroup`.
- **Shared checks:** All IP2 commands; record actual results and exact selected counts.
- **Installed verification:** IP3-T1 tests exercise direct and source-rebuilt
  wheels independently. CLI version, import origins and any changed resources
  must be checked from outside the source checkout. No platform inference from
  Linux to macOS/Windows, or editable checks to installed behavior.
- **Reconciliation:** Resolve every failed required check; retain and identify
  historical skips and exclusions without calling them passes. AC-03/04 remain
  M2; stages/MLflow/assistant behavior remain their owning stories.
- **Renewal:** Executable changes renew applicable focused, M1 and final M1–6
  evidence; document-only corrections use link/whitespace checks. Standalone
  artifact/full-suite commands require explicit developer direction.
- **Actual results and limitations:** Pending; no tests were run while drafting.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-13-AC-01 | IP1-T1/T2; IP2-T1/T2; IP3-T1/T3 | Documented recipe, native source/extraction/split/derived identities, committed A/B references and retained content, both installed wheels | Pending |
| US-13-AC-02 | IP1-T2; IP2-T3/T4; IP3-T1/T2/T3 | Actual fixture Git commits/inventory, excluded bytes, single split-record ownership, Git-owned manifests and both versions in local cache/remote | Pending |
| US-13-AC-03 | M2 owning plan to be defined | Restoration from recorded metadata and verified content hashes | Deferred to M2 |
| US-13-AC-04 | M2 owning plan to be defined | Missing/mismatched restoration fails explicitly | Deferred to M2 |

- **M1-slice developer acceptance:** Pending; final Gate 3 can serve only if explicit.
- **Whole-story developer acceptance:** Pending until M2 AC-03/04 delivery.
- **Decision reference and date:** Pending.
- **Publication:** This planning request authorizes no commit, push, PR or issue
  update. Later authorized execution follows its selected skill's publication
  workflow only after the required acceptance decisions.

## Milestone acceptance handoff

`MVP-M1-ACCEPT-VERIFY` owns integration reconciliation against final revised M1
inputs, actual DVC stages and assistant evidence with the other story plans.
Preserve historical `M1-ACCEPT-VERIFY` under [US-03](milestone-1-us-03.md)
and independent `M50-ACCEPT-VERIFY`; this slice closes neither. Broader full-suite
(`uv run --locked pytest -n 4 --dist=loadgroup -m ""`) and standalone distribution/
installation checks require explicit developer commands under the
[verification policy](../development/verification.md#phase-and-story-verification).
Reconcile applicable manual/platform limits and historical deferrals before
milestone acceptance. `MVP-M2-ACCEPT-VERIFY` will own later restoration integration.

## Execution rules

Mark tasks Complete only after work and required checks pass with linked evidence.
Keep failed/partial/unverified work incomplete. At every implementation-phase
boundary, present actual results and stop for explicit approval; plan approval
does not approve gates. Reopen tasks if later changes invalidate their evidence.
Use small vertical TDD slices for new/corrected executable behavior; do not weaken
existing tests or manufacture failures for documentation/native functionality.
Track each corrective hypothesis/change/verification; after three failed attempts
on the same problem, stop and present all evidence for developer direction under
[repository instructions](../../AGENTS.md#problem-solving-attempt-limit).
