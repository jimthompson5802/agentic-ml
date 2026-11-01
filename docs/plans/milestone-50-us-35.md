# Milestone 50 / US-35: Clean up successful verification environments

## Scope and outcome

- **Milestone:** 50 — Improve the technical environment; independent of product delivery sequencing.
- **Authoritative issue:** [#47](https://github.com/jimthompson5802/agentic-ml/issues/47). Retrieved complete body and metadata on 2026-11-01; paginated comments returned zero unique comments, matching the reported count. Metadata refresh confirmed unchanged `updated_at=2026-11-01T22:05:29Z`. Open, enhancement label, no assignees or GitHub milestone; the body assigns Milestone 50.
- **User story:** [US-35](../specs/user-stories.md#us-35-clean-up-successful-verification-environments); all US-35-AC-01–05 are in scope.
- **Outcome:** Each successful standalone installation, distribution, initialization or planning verification removes its disposable environments and private caches after its last consumer, while durable diagnostic records survive. Failures and explicitly retained successful runs preserve their workspaces.
- **Exclusions:** Historical cleanup/migration, pytest placement or retention policy (US-36), environment reuse (US-37), early release between wheel paths (US-38), installer concurrency/hardlink changes, product behavior and Milestone 99.
- **Supporting contracts:** [Records](../development/records.md), [distribution verification](../development/distribution.md), [verification policy](../development/verification.md#phase-and-story-verification), [design reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [repository boundary](../specs/design/repository-layout.md), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization).
- **Coordinated execution index:** None. No new capability from US-36–US-38 is required or included.

## Current implementation and technical approach

Planning inspected revision `2527034` on branch `US-35-verification-cleanup`; the pre-existing checkpoint edit is preserved. No matching US-35 plan existed. The delivery and acceptance design documents describe product milestones; the issue and development policies supply this maintenance story's lifecycle contract. No conflicting product requirement was found.

Existing executable interfaces are `tests/installation/verify_installation.py`, `tests/packaging/verify_distributions.py`, `tests/installation/verify_initialization.py`, and `tests/installation/verify_planning.py`. All allocate independent temporary workspaces; the installation, initialization and planning commands also accept `--workspace`. Planning currently accepts an existing directory, unlike installation/initialization. Distribution has no workspace option. Installation already deletes its private cache during its cache-independence checks; preserve those checks. Other drivers inherit installer cache behavior; shared cache contents must remain untouched.

Initialization and planning launch distribution verification and parse its `WORKSPACE` line. Initialization needs its extracted source and rebuilt wheel as well as installed checks; planning uses both installed interpreters. Simply deleting the distribution workspace when its subprocess exits would break these consumers. Existing installation fixtures and assertions also read or mutate successful workspaces after the command returns.

Propose a development-only lifecycle module, `tests/verification_support.py` (new path), with an explicitly typed public interface for invocation ownership, stage recording and finalization. Keep it outside the installable product. Direct script execution must resolve this contributor helper explicitly without adding the harness source package to installed probes' import paths. Record the chosen import arrangement before implementation; all four scripts must remain executable from another working directory. No dependency or package-resource change is intended.

Proposed command contract, subject to plan review:

- Add `--keep-workspace` to all four commands. Default successful finalization removes registered owned environments and private caches; the flag retains successful workspaces. Preserve original validation failures and nonzero status.
- Keep `WORKSPACE` diagnostics and add `RECORDS <absolute-path>` for each invocation. Resolve records from the harness script checkout, never the experiment working directory. Allocate collision-resistant records using the existing policy layout. Child records link their parent and are reported through the outer command too.
- Outer initialization/planning invocations own the full consumer lifecycle. Pass an explicit child workspace created by distribution under an invocation-owned location and request child retention. Register that newly created child as disposable under the parent. Parent success finalizes only after all downstream probes; parent failure preserves all available children. Do not expose a general option authorizing deletion of arbitrary external paths.
- Existing caller directories are never adopted for recursive deletion. For planning's existing-directory use, preserve the directory and its files; allocate a unique owned child or reject a conflict before writing. Explicit new workspace paths can be owned only if created exclusively by this invocation. Additive workspace option plumbing does not implement pytest ownership or retention policy.
- Record commands, cwd, stdout/stderr, exit codes, source commit/working-tree identity, platform/tool versions, artifact checksums, interpreter/package/origin identities and results before cleanup. Use `summary.json`, `commands.json`, `identities/` and `logs/`. Preserve pre/post synchronization and upgrade identities. Mark unavailable or incomplete identities rather than inventing successful probes. Do not copy secrets, entire environments, or datasets into records.
- Persist records successfully before deletion. Record-write failure prevents cleanup and makes the invocation unsuccessful. Represent verification outcome and cleanup outcome separately. Proposed exit policy: original nonzero status takes precedence; otherwise cleanup failure exits nonzero with verification recorded as passed and cleanup as failed. Emit remaining workspace and records locations.
- Remove only registered newly created disposable roots, never glob-discovered environments. Reject ownership mismatches, overlaps with checkout/artifacts/records and symlink redirection. Do not follow symlinks into external targets. Preserve shared caches; delete private caches only where ownership is proven. Keep source fixture/checkouts and unrelated workspace files intact; selective environment/cache deletion is sufficient and safer than deleting an entire source-containing workspace.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Plan review and public boundaries | Confirm proposed command flags, ownership, failure status and test boundaries below | All executable work | Approved with plan on 2026-11-01; execution requires separate direction |
| Existing package verification | Preserve genuine direct and sdist-rebuilt installations, pinned origins, isolated probes and all assertions/timeouts | Both implementation phases | Existing scripts and tests inspected; no prerequisite story slice needed |
| Consumer and fixture inventory | Enumerate every command caller, returned path and environment consumer before adapting it | Driver cleanup | US-35-IP1-T1 / IP2-T1 |
| Baseline availability | Record unchanged workload before changing drivers | Final disk comparison | Complete: US-35-IP1-T1; [Phase 1 report](../verification/us-35-ip1.md) retains fixed inputs and four passing command measurements |
| Evidence destination writable | Durable records outside disposable roots with unique IDs | Any cleanup | Fail closed and retain workspaces if unavailable |
| Related stories | Preserve seams for future ownership and early release without implementing them | None | US-36–US-38 excluded |

## Plan review

- **Status:** Approved.
- **Developer decision:** Plan and proposed public test boundaries approved; implementation gates remain pending.
- **Decision reference and date:** Developer message, 2026-11-01: “i approve the plan; commit the changes”.
- **Requested plan changes:** None recorded.

## Scope-change history

None. During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md); record request, impact, affected tasks/evidence/gates, decision and resume point here. Prerequisite work outside this plan requires a reviewed scope revision before implementation.

## Execution rules

Mark tasks complete only after required verification passes and actual evidence is linked. Keep incomplete/failed work incomplete; reopen invalidated tasks. Use one behavior-focused red–green slice at a time, independently specified expected outcomes and public interfaces. Record red and green commands, failure reasons and results; do not batch all tests before implementation. Follow the repository's three-attempt limit for the same unresolved failure and preserve failure evidence.

Stop at every implementation phase gate, including the final gate. Present tasks, commands, results, limitations and deviations; wait for explicit approval and record its reference. Plan approval confirms proposed boundaries but does not approve any implementation gate. Story acceptance is explicit. No implementation, commit, push or publication is authorized by creation of this plan.

## US-35 / Implementation Phase 1: Durable records and installation cleanup

- **Outcome:** Installation verification demonstrates the complete safe lifecycle and leaves inspectable records after successful cleanup.
- **Entry conditions:** Satisfied. Plan/public-boundary approval on 2026-11-01; execution authorized by developer message “execute implementaton plan for us-35”.
- **Acceptance criteria advanced:** US-35-AC-01–05, installation slice; no whole-story completion claim.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-35-IP1-T1 | Complete | Inventory all four scripts, `tests/installation/check_*.py`, `tests/packaging/check_installed.py`, their callers and `.github/workflows/`; save inventory, fixed baseline protocol and results in proposed `docs/verification/us-35-ip1.md`. Record helper import arrangement and owned path categories. | Plan approval | Consumer map includes nested allocations and private/shared caches. Run each unchanged standalone command once against the same fixed artifacts/local Git fixture; capture exact args, environment counts and disk sizes before any driver changes. Copy required raw evidence into unique `.dev-records/verification/` baseline records; never delete historical paths. | AC-01, AC-04, AC-05 |
| US-35-IP1-T2 | Complete | Create proposed `tests/verification_support.py` and `tests/integration/test_verification_lifecycle.py`; integrate `tests/installation/verify_installation.py` in vertical TDD slices. | T1 | Unique absolute records, ownership registry, successful cleanup, explicit retention and failed/incomplete retention work. Record identity/log failures before safe finalization; test record-write failure and cleanup failure as distinct outcomes. | AC-01–04 |
| US-35-IP1-T3 | Complete | Update `tests/integration/test_installation_verification.py` callers that need surviving environments to explicitly retain them; redirect evidence-only assertions to records. Add default-cleanup and failure cases without removing original pin/cache/upgrade assertions. | T2 | Existing installed-project mutation fixtures remain usable; default standalone success removes its environments, identities survive, invalid revision/install failure retains available diagnostics. | AC-01–05 |
| US-35-IP1-T4 | Complete | Complete direct checks, shared checks, report and checkpoint. | T2, T3 | Exact selectors, counts, red/green results, lock hashes, platform, limitations and deferrals recorded; present gate. | AC-01–05 |

### Verification and review evidence

- **Changed modules/direct selection:** `tests/verification_support.py`, installation driver and its call-site tests. Run `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_verification_lifecycle.py tests/integration/test_installation_verification.py`.
- **Public boundaries for confirmation:** lifecycle module's documented invocation/finalization API with tiny real temporary trees and subprocess commands; driver CLI via real local full-SHA Git fixtures and external experiment projects. Assert filesystem state, machine-readable records, stderr/stdout and exit codes, not internal call order. Deterministic failure injection at the filesystem boundary may exercise cleanup errors; real installed-command cases establish integration and provenance. Tiny lifecycle tests do not establish package validity or platform support.
- Cover caller-owned and existing environments, shared-cache sentinels, checkout/artifact/record overlap, symlink targets, distinct concurrent invocations, partial setup failure, explicit retention, durable record failure and cleanup failure. Do not use a network failure as the intended red result.
- **Deferred checks:** unchanged product CLI/API, initialization/planning and parallel scheduling caller regressions, full suite and reserved milestone test belong to `M50-ACCEPT-VERIFY`. Phase 2 directly tests the other changed drivers; no automatic full local run.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Installation lifecycle | Direct selection above; serial `uv run --locked pytest <node-id>` permitted for short TDD diagnosis with reason recorded | Correct pass/fail retention and ownership; real pinned install checks preserved | 36 passed in 148.28s, four workers; 23 helper + 13 installed-command/probe cases; [report](../verification/us-35-ip1.md) |
| Shared checks | `uv sync --locked --group dev`; `uv lock --check`; `uv run --locked ruff check .`; `uv run --locked ruff format --check .`; `uv run --locked mypy src tests`; `uv run --locked agentic-ml --version`; `git diff --check` | Pass; record SHA-256 of `uv.lock` before/after, unchanged unless reviewed | All passed; lock unchanged; [report](../verification/us-35-ip1.md#phase-gate-verification) |
| Baseline | T1 fixed workload and filesystem protocol | Comparable per-driver environment counts and retained bytes with identities | All four baseline commands passed; retained counts 1 / 2 / 6 / 2; [report](../verification/us-35-ip1.md#baseline-protocol) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete; installation slice and helper boundaries verified; baseline retained; direct and shared checks pass.
- **Evidence presented:** [Phase 1 report](../verification/us-35-ip1.md), including baseline, red/green cycles, final direct/shared results and absolute raw record links. Tasks T1–T4 technically complete on 2026-11-01; developer approved the gate on 2026-11-01.
- **Remaining limitations:** Other three commands not yet delivered; macOS evidence establishes only observed platform behavior.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message, 2026-11-01: “i approve ip1; commit changes”.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Phase 1 gate satisfied. Current instruction authorizes committing Phase 1; Phase 2 execution authorized 2026-11-01: “you can start ip2”.

## US-35 / Implementation Phase 2: Composed driver cleanup and story acceptance

- **Outcome:** All four commands preserve records, retain failures and clean only owned disposable environments after the final consumer; comparable workload evidence quantifies retained disk reduction.
- **Entry conditions:** Phase 1 gate approved; baseline protocol available.
- **Acceptance criteria covered:** US-35-AC-01–05 in full.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-35-IP2-T1 | Complete | Refine Phase 1 consumer map for `tests/packaging/verify_distributions.py`, initialization/planning drivers, probes and every successful-workspace consumer. Record proposed child protocol and any new direct-test selectors before tests. | IP1 gate | Explicit final-consumer points cover extracted source, rebuilt wheel, both interpreters and probe-created environments. No source/checkouts or caller paths classified as disposable environments. | AC-01, AC-04 |
| US-35-IP2-T2 | Complete | Adapt distribution driver to the lifecycle helper; add explicit child workspace plumbing and retention flag; record all stage logs, wheel/sdist/rebuilt checksums and installed identities. Add direct cases in `tests/integration/test_distribution_verification.py` and new lifecycle module tests. | T1 | Standalone success cleans owned environments after both paths; malformed artifact and later rebuilt-path failures retain available environments and records. Retained child succeeds without deleting resources needed by its parent. | AC-01–05 |
| US-35-IP2-T3 | Complete | Adapt initialization and planning drivers to parent ownership and linked child records; extend proposed `tests/integration/test_verification_lifecycle.py` with direct command cases for both parents. Adjust existing distribution-driver callers for explicit retention where needed. | T2 | Both parents finish every real downstream probe before cleanup. Failure after child success retains child environments. Explicit retention preserves both paths. Existing planning workspace sentinel is untouched; probes do not write durable evidence into disposable-only storage. | AC-01–05 |
| US-35-IP2-T4 | Complete | Update `docs/development/distribution.md`, `docs/development/records.md` and relevant command guidance with default cleanup, `--keep-workspace`, records lookup, child ownership, cleanup status, failure/interruption limits and backup duty. | T2, T3 | Retention contract matches all four commands; documentation says no historical deletion and no guarantee after forced process termination. | AC-02–04 |
| US-35-IP2-T5 | Complete | Repeat T1 baseline workload using identical artifacts/source fixtures and args except required new flags; write proposed `docs/verification/us-35-ip2.md`. | T2, T3 | Per-driver before/after retained environment counts and disk sizes, record sizes and elapsed observations with platform/measurement limits; no unsupported peak-usage or speed claim. | AC-05 |
| US-35-IP2-T6 | Complete | Reconcile all five criteria, renew invalidated direct evidence, run shared checks, update this plan and `CHECKPOINTS.md`, present final gate/story review. | T4, T5 | All required direct checks pass, every deferred regression has an owner, raw records exist after cleanup, review report links evidence; no full-suite success claimed. | AC-01–05 |

### Verification and review evidence

Consumer/child protocol and focused red–green evidence: [Phase 2 report](../verification/us-35-ip2.md). Distribution task T2 complete after real default/retained/later-failure CLI checks; final combined phase verification passed: 58 tests and all shared checks.

- **Changed modules/direct tests:** distribution, initialization and planning drivers plus lifecycle helper. Select `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_verification_lifecycle.py tests/integration/test_distribution_verification.py`. If helper/installation behavior changes, renew `tests/integration/test_installation_verification.py` too.
- **Public boundaries:** Four subprocess CLIs with independently built wheel/sdist artifacts and local Git source fixture; independent cwd; installed interpreters, original probe assertions, reported path/output/status and durable manifests. Public helper tests provide deterministic ownership/cleanup-failure cases. No private collaboration mocks substitute for installed verification.
- New direct lifecycle cases must exercise initialization cleanup without repurposing or unmarking `test_complete_initialization_from_both_artifact_paths`. That existing marked test remains reserved for milestone acceptance. New parent-command tests directly exercise changed lifecycle behavior; retain existing subprocess timeouts and assertions. Explicitly retain workspaces in old tests that inspect them after return.
- For each command cover default success, explicit retention and verification failure. Include later-path failure, downstream failure after distribution success, unrelated cwd, private/shared cache boundaries, records surviving removal and original failure plus cleanup-error reporting. Verify both direct-wheel and genuinely rebuilt-wheel identities survive. Add missing machine-readable probe identity output only if required; any changed probe must have its direct tests mapped and included before its gate.
- **Deferred checks:** unchanged product initialization/planning/approval behavior, parallel scheduling regressions and full suite to `M50-ACCEPT-VERIFY`. The existing `M1-ACCEPT-VERIFY` obligation remains with its owning story and is neither closed nor transferred here. Uncertain impacts are recorded and assigned; no automatic broader local run.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Direct lifecycle/distribution/parent commands | Four-worker direct selection above, including installation renewal for helper changes | Pass; exact selected/deselected counts, AC mappings and platform recorded | 58 passed in 419.99s; 59 collected, 1 reserved case deselected; [report](../verification/us-35-ip2.md#phase-gate-verification) |
| Real standalone workload | Exact original commands/cwd and fixed inputs replayed; see [report](../verification/us-35-ip2.md#fixed-workload-comparison) | Both package paths/consumers pass, zero owned retained environments on default success; private caches removed and records intact | All four commands passed; retained environments 1/2/6/2 → 0/0/0/0; private caches absent, durable identities/checksums verified |
| Retention/ownership/failure matrix | Public CLI tests and helper boundary cases | Available failure environments retained; caller sentinels/shared caches/source/evidence unchanged; cleanup errors visible | Passed in final direct selection; all four commands have default/retained/failure evidence; [report](../verification/us-35-ip2.md) |
| Before/after measurement | Exact original T1 inputs/commands, environment enumeration, logical bytes and `du -sk`; separate records | Reduced retained environment count/usage with filesystem limits | All four passed; 1/2/6/2 → zero environments; [comparison](../verification/us-35-ip2.md#fixed-workload-comparison) |
| Shared checks | All Phase 1 shared commands, lock hashes and whitespace check | Pass; no silent lock update | All passed; lock and executable/test hashes unchanged; [report](../verification/us-35-ip2.md#phase-gate-verification) |
| Documentation | Resolve local links, inspect help/examples and `git diff --check` | Consistent retention contract; planned versus actual evidence distinguished | Retention contract updated; local links, CLI help and final whitespace checks passed |

### Developer approval gate

- **Approval criteria:** T1–T6 complete; all criteria verified with real command and boundary evidence; documentation and measurements reviewed; required direct/shared checks pass.
- **Evidence presented:** [Phase 2 report](../verification/us-35-ip2.md), Phase 1 report and absolute raw record paths. T1–T6 technically complete on 2026-11-01; 58 direct tests and shared checks passed, fixed-input replay retained zero environments for all four commands. Developer approved this gate on 2026-11-01.
- **Remaining limitations:** Report actual macOS/tool versions; Linux/Windows unverified unless observed. Full suite and reserved test deferred to milestone acceptance. Interruption may leave disposable workspaces; never claim automatic forced-termination cleanup.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message, 2026-11-01: “i approve ip2; commit”.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Commit Phase 2 changes. Whole-story acceptance and publication remain pending.

## Final verification requirements

- **Owning task:** US-35-IP2-T6, required before final gate presentation.
- **Identity:** Tested revision, dirty changes, lock hash, input fixture SHA, wheel/sdist/rebuilt artifact hashes and tool/platform identities in reports and records.
- **Direct/shared checks:** Reuse valid Phase 1 evidence and renew invalidated tests; run Phase 2 selections and shared checks. Required direct failures remain blockers.
- **Distribution/installation:** Real direct-wheel and sdist-rebuilt-wheel commands are required because their drivers change. Probe existing installed public interfaces outside checkout with declared runtime dependencies; no editable installs or contributor dependency leakage. No product distribution change is planned, but driver evidence must cover both artifact paths.
- **Deferred-check reconciliation:** Enumerate caller/full-suite deferrals for `M50-ACCEPT-VERIFY`; this reconciliation assigns ownership, not a passing result. Keep unrelated M1 acceptance obligations intact.
- **Evidence renewal:** Later executable changes renew invalidated direct evidence; artifact input changes renew artifact probes; documentation-only approval edits use link/whitespace checks and explain why TDD is inapplicable.
- **Actual results and limitations:** Phase 1: 36 direct tests and shared checks passed; unchanged four-command baseline captured. See [Phase 1 report](../verification/us-35-ip1.md). Phase 2: 58 direct tests in 419.99s and all shared checks passed; fixed-input four-command replay passed. See [Phase 2 report](../verification/us-35-ip2.md). No full-suite or cross-platform verification claimed.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-35-AC-01: all four commands clean after final consumers | IP1-T2–T4; IP2-T1–T3, T6 | Real four-command success and composed-consumer cases | Verified; [Phase 2 evidence](../verification/us-35-ip2.md) |
| US-35-AC-02: retained complete records and absolute locations | IP1-T2–T4; IP2-T2–T4, T6 | Manifest/log/identity/checksum assertions after cleanup; unique parent/child records | Verified; [Phase 2 evidence](../verification/us-35-ip2.md) |
| US-35-AC-03: failure and explicit successful retention | IP1-T2–T4; IP2-T2–T4, T6 | Per-command success retention and early/later/downstream failure matrix | Verified; [Phase 2 evidence](../verification/us-35-ip2.md) |
| US-35-AC-04: ownership and cleanup errors | IP1-T1–T4; IP2-T1–T4, T6 | Sentinels, symlink/overlap rejection, shared-cache preservation and independent outcome checks | Verified; [Phase 2 evidence](../verification/us-35-ip2.md) |
| US-35-AC-05: automation and before/after disk evidence | IP1-T1–T4; IP2-T2–T3, T5–T6 | Direct test results and fixed-workload environment/disk comparison with limits | Verified; [Phase 2 evidence](../verification/us-35-ip2.md) |

- **Remaining work:** Both implementation phases approved. Await explicit whole-story acceptance. US-36–US-38 remain separate backlog work.
- **Partial prerequisite delivery:** None claimed for another story.
- **Final verification:** Required phase/direct/shared checks and fixed-workload comparison passed; milestone deferrals retain their named owner.
- **Developer acceptance:** Pending.
- **Decision reference and date:** Pending.

## Milestone acceptance handoff

- **Owner:** `M50-ACCEPT-VERIFY` — Milestone 50 acceptance verification task; Not started. This record owns this story's deferrals until a milestone execution plan supplies the corresponding task.
- **Deferred checks:** All unchanged caller regressions, full suite and existing marked initialization test; remaining platform/manual checks reported explicitly.
- **Required evidence:** `uv run --locked pytest -n 4 --dist=loadgroup -m ""`, shared checks, applicable direct/rebuilt-wheel and installation checks against final milestone inputs. Reconcile every deferral and actual counts/results before milestone acceptance; later executable work invalidates full-suite evidence. Milestone 50 is ongoing; story acceptance does not imply milestone acceptance.
