# Milestone 1 / US-01: Install a pinned harness version

## Scope and outcome

- **Milestone:** 1 — Run and record a reproducible experiment.
- **User story:** [US-01 / issue #8](https://github.com/jimthompson5802/agentic-ml/issues/8).
- **User-visible outcome:** A developer creates a separate Git/Python experiment project, installs a full-SHA GitHub dependency, uses installed CLI/imports/resources without a maintained harness checkout or installer cache, and explicitly upgrades the pin with a changed lockfile/environment identity.
- **Acceptance criteria covered:** [US-01-AC-01–04](../specs/user-stories.md#us-01-install-a-pinned-harness-version), in full.
- **Scope boundaries:** Bootstrap documentation, real installed-project verification, revision/environment evidence, and upgrades. Initialization and usable initialization templates belong to US-02; managed execution, runtime guidance selection, run manifests/tracking, data restoration, and agent adapters remain in their owning stories. Existing provisional resources satisfy resource accessibility here; do not describe them as usable experiment templates. No registry publication or Milestone 99 work.
- **Supporting design:** [Reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [installation](../specs/design/interfaces-and-configuration.md#project-initialization-and-installation), [execution/environment boundary](../specs/design/execution-and-governance.md#execution), [delivery order](../specs/design/milestone-delivery.md#milestone-1-dependencies-and-delivery-order), [traceability and fixtures](../specs/design/acceptance-traceability.md), [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization), [layout](../specs/design/repository-layout.md).
- **Coordinated execution index:** None. Reuse accepted Milestone 0 work; no new prerequisite-story implementation is included.

## Findings and source reconciliation

Planning baseline: `aead26e`, clean main before creating local branch `US-01-pinned-installation` on 2026-10-30. Retrieved issue #8 complete metadata/body and all comment pages; open, enhancement, author jimthompson5802, no assignees or GitHub milestone object (body assigns Milestone 1), zero comments. Repeated metadata retained `updated_at=2026-10-30T02:06:17Z` and count zero. No recorded comment scope decisions or conflicts with US-01 repository criteria.

Retrieved prerequisite issue #3 complete body and all comment pages: closed, one unique comment `6510671946`, stable `updated_at=2026-10-30T03:11:48Z`. Its historical comment records an earlier premature closure; the owning plan's subsequent approvals, acceptance, merge and successful main CI govern current completion. Historical `agent-ml` spelling is superseded by the developer-approved correction in ADR-007 and US-33 SC-01; use `agentic-ml` everywhere new.

Existing package: Hatchling, `agentic-ml` 0.1.0, Python >=3.12, `agentic_ml` import, version CLI, provisional template/guidance, no third-party runtime dependencies. `tests/packaging/check_installed.py` and `verify_distributions.py` already verify both wheel paths. They do not establish full-SHA GitHub installation, experiment lock provenance, cache-independent operation, or upgrades. Existing `tests/integration/test_distribution_verification.py` exercises wheel verification. No US-01 plan or experiment bootstrap guide exists.

Design examples still contain placeholders and future init commands; the plan uses the repository URL already present in package metadata and prior accepted plans. Do not execute `agentic-ml init` or claim it exists in US-01. ADR-007's older pending distribution-name text is reconciled by the explicit acceptance recorded in the US-31 plan and implemented metadata; broader pending configuration/isolation decisions do not block package installation alone.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Accepted package foundation | US-33 IP1 minimal CLI/resources, IP2 both wheel paths, IP3 hosted verification and gates approved | All tasks | [US-33 owning plan](milestone-0-us-33.md), [IP3 evidence](../verification/us-33-ip3.md); accepted and merged as `018e9d4bb26e121c7f9274d11e0de560b7514b95` |
| Installation source and names | `https://github.com/jimthompson5802/agentic-ml.git`; distribution/CLI `agentic-ml`, import `agentic_ml` | Bootstrap and assertions | Existing metadata and accepted naming; no registry or editable installation |
| Two published revisions | Select two distinct GitHub-reachable full 40-character commits containing the CLI/resources, record both independently before tests | Upgrade demonstration | Verified published A: `018e9d4bb26e121c7f9274d11e0de560b7514b95`; B: `aead26e9c758878107ad72f230f9e607a9a7ecfa`. Both package versions 0.1.0; actual upgrade verified in [IP2 evidence](../verification/us-01-ip2.md). [IP1 investigation](../verification/us-01-ip1.md#t1-toolsource-investigation) |
| Environment identity | Record repository URL, requested/resolved full SHA, installed distribution version, SHA-256 of exact project `uv.lock`, Python implementation/version/platform | AC-03/04 verification | Evidence contract approved in plan review and verified in IP1/IP2. Compare revision and lock hash, not package version alone; this is installation evidence, not a new public run-manifest schema or CLI/API |
| Tool and platform baseline | Python 3.12, Git, uv; record actual versions and network/auth requirements | Real GitHub acceptance checks | macOS initial verification; existing Linux CI is prerequisite evidence only. Windows/additional Python versions unverified |
| Bootstrap/upgrade syntax | Validate against installed uv help and official documentation before writing runnable commands | IP1 documentation, IP2 upgrade | Verified bootstrap uses `uv init --no-package --python 3.12`, `uv add "git+https://github.com/jimthompson5802/agentic-ml.git" --rev FULL_SHA`, `uv sync --locked`, `uv run --locked agentic-ml --version`; do not silently relax locked checks; [IP1 evidence](../verification/us-01-ip1.md) |

## Technical approach and public test boundaries

Plan review must confirm these boundaries before tests are written:

1. **Installed user interfaces:** Real Git/uv subprocesses create an experiment project outside the harness checkout and install a noneditable dependency from GitHub. Probe the environment's Python with `-I`, absolute installed CLI, `importlib.metadata`, and `importlib.resources`. Expected SHA values and resource text are independent inputs, not obtained from the result under test. Assert CLI zero exit, exact metadata version stdout, empty stderr, package path inside the project environment, and exact resource contents. Check project declaration and parsed `uv.lock` agree with the independently selected repository/revision and dependency closure.
2. **Checkout/cache independence:** Copy only the stdlib probe into temporary storage; clear import-path/environment overrides. Use a dedicated disposable uv cache, with link mode set to copy when supported, then remove only that fixture-owned cache before probing with network disabled for uv and without synchronization (`uv run --no-sync --offline` plus direct installed Python/CLI). The ordinary harness checkout must not appear on import paths. Do not delete or rename the developer's checkout, shared cache, or environment. This proves installed runtime independence; it does not promise an offline first installation or offline recreation of a deleted environment.
3. **Explicit upgrade:** Snapshot project declaration, lockfile bytes/hash, resolved metadata and probe results at A; unchanged locked synchronization must preserve identity. Explicitly select B, allow intentional lock regeneration in the disposable experiment only, verify declared/resolved/installed revision B, changed lock hash and recorded identity, and repeat installed probes. Both commits may report 0.1.0; version equality must not hide a revision change. No change to the harness development lockfile is expected.
4. **Failure boundaries:** Unknown full commit fails installation with nonzero exit; stale experiment declaration versus lock fails locked synchronization without rewriting the lock. Missing metadata/resources or wrong resolved SHA must make the verifier fail. Preserve diagnostic output and do not count a partially installed project as passing. Network/authentication failures are setup failures, not the expected red test or proof of invalid-pin handling.

Proposed new verification paths: `tests/installation/check_project.py` (stdlib installed-environment probe), `tests/installation/verify_installation.py` (explicitly invoked network acceptance driver), and `tests/integration/test_installation_verification.py` (focused subprocess tests of driver/probe failures). Final command/options are established and documented in IP1 before IP2 uses them. Keep real GitHub acceptance runs explicit so ordinary pytest remains reproducible without additional live GitHub requirements; use isolated fixture repositories for focused driver cases and never present them as GitHub acceptance evidence. Reuse existing wheel checks without changing their established assertions. No new product identity API is required by this plan; any discovered reusable harness behavior belongs under `src/agentic_ml` and requires scope review if it changes this approach.

New or corrected executable behavior follows one-test-at-a-time red–green TDD through the confirmed public subprocess boundary, including verifier failure handling. Documentation and passing demonstrations of existing package behavior require inspection/regression evidence rather than manufactured failing tests. Record this distinction in each report.

## Plan review

- **Status:** Approved.
- **Developer decision:** Approved — includes scope, proposed identity evidence, public test boundaries, and two implementation phases.
- **Decision reference and date:** Developer message “i approve the plan; execute us-01 ip1”, 2026-10-30. Authorizes IP1 execution only.
- **Requested plan changes:** None recorded.

## Scope-change history

None. Use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for changes during execution.

## Execution rules

Refresh the complete owning issue discussion and [CHECKPOINTS.md](../../CHECKPOINTS.md) before execution. Read [development conventions](../development.md) before Python changes. Mark tasks Complete only after required verification passes and actual criterion-mapped evidence is recorded; partial/failed/blocked/unverified tasks stay incomplete. Reopen invalidated results.

Stop at every implementation phase gate, including the final gate; present results, evidence, deviations and platform limitations, then await explicit developer approval. Plan approval does not approve implementation gates or authorize execution. Record each decision with its source/date. No publication, issue edits, commit, push, or merge is included in this planning request.

Use the repository three-attempt limit: record each hypothesis, corrective change and verification against the original failure; after three failed attempts stop and preserve diagnostics for developer direction. Never weaken assertions or add suppressions to hide failure. Pause affected work for scope changes and record the decision before dependent implementation.

Store raw logs, environments and generated projects outside Git in isolated temporary storage; redact credentials. Proposed tracked reports are `docs/verification/us-01-ip1.md` and `us-01-ip2.md`. Run the documented shared commands at each implementation gate: `uv sync --locked --group dev`, `uv lock --check`, `uv run --locked pytest`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy src tests`, `uv run --locked agentic-ml --version`. Record exit codes and lock checksum/diff before/after. For distribution changes run both documented wheel verification paths; otherwise retain existing regression checks and explain applicability. Report checks that could not run; network/permissions blockers remain unresolved until actual checks pass.

## US-01 / Implementation Phase 1: Verify pinned bootstrap and installed independence

- **Outcome:** A usable bootstrap guide and automated evidence of full-SHA installation and installed runtime independence.
- **Entry conditions:** Plan/public boundaries approved, implementation separately authorized; accepted US-33 prerequisites verified; GitHub/package-index access available.
- **Acceptance criteria advanced:** US-01-AC-01–03; groundwork for AC-04.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-01-IP1-T1 | Complete | Inspect uv/Git versions/help and official uv/Git installation documentation; select and verify published A/B; record decisions in proposed `docs/verification/us-01-ip1.md` | Entry conditions | Actual full SHAs and package/resource availability recorded; exact bootstrap, lock, cache isolation and upgrade commands validated; unresolved findings block dependent tasks | AC-01–04 |
| US-01-IP1-T2 | Complete | Add proposed `docs/experiment-setup.md`; link from `README.md`; clarify ADR-007 source/name details in `docs/specs/design/architecture-decisions.md` using existing accepted evidence | T1 | Guide covers Git/uv installation links, Python 3.12, separate Git/uv project, full-SHA dependency, locked sync, CLI/import/resource examples, committing project metadata/lock, credentials and provisional-resource/init boundary. Commands reproduced in T4; docs inspection recorded | AC-01, AC-03 |
| US-01-IP1-T3 | Complete | Add proposed installation driver/probe and focused tests under `tests/installation/` and `tests/integration/test_installation_verification.py`, in small red–green slices | T1; confirmed boundaries | Public checks accept correct install and reject wrong SHA, missing required resource/metadata, invalid revision and stale-lock cases; independently expected values; stage-specific nonzero errors and retained diagnostics. Real invalid-pin/stale-lock cases also exercised in T4 | AC-02–03 |
| US-01-IP1-T4 | Complete | Execute guide and driver against real GitHub A from a temporary separate project; remove only disposable installer cache; write `docs/verification/us-01-ip1.md`; update checkpoint | T2–T3 | Real full-SHA lock/install evidence; cache-independent offline/no-sync CLI/import/resource passes; actionable invalid-pin and stale-lock failures; all shared checks pass with harness lock unchanged | AC-01–03 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Bootstrap and GitHub provenance | Follow guide in fresh project; invoke new driver using documented A/options | Declared/resolved/installed A agree; no editable install or contributor dependencies required | Passed — [IP1 evidence](../verification/us-01-ip1.md) |
| Runtime independence/resources | Copied probe, direct environment Python/CLI, offline/no-sync uv after removal of dedicated cache | Correct import location, CLI and exact template/guidance; no checkout/cache dependency | Passed — [IP1 evidence](../verification/us-01-ip1.md) |
| Failure cases | Focused subprocess tests plus real unknown SHA and stale-lock fixtures | Expected nonzero diagnostics; stale-lock check preserves lock bytes | Passed — [IP1 evidence](../verification/us-01-ip1.md) |
| Regression and quality | Shared commands above; existing wheel regressions; both fresh wheel paths if distribution changes | All applicable checks pass; no harness lock mutation or unexplained suppression | Passed — [IP1 evidence](../verification/us-01-ip1.md) |

### Developer approval gate

- **Approval criteria:** T1–T4 complete, AC-01–03 evidence and negative cases reviewed; A/B and exact upgrade commands settled; no unresolved installation failure.
- **Evidence presented:** [IP1 report](../verification/us-01-ip1.md): T1–T4 complete, real GitHub installation, cache-removed probes, negative cases, 20 tests and all shared checks passed; harness lock unchanged. Technical completion 2026-10-30; developer gate pending.
- **Remaining limitations or blocked work:** AC-04 awaits IP2; no init, execution, tracking or other-platform claims.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve us-01 ip1; commit changes; execute ip2”, 2026-10-30.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** US-01 IP2 explicitly authorized by the same developer message after committing IP1 changes.

## US-01 / Implementation Phase 2: Verify explicit upgrade and complete acceptance evidence

- **Outcome:** The same experiment explicitly upgrades A to B and records a changed environment identity with intact installed interfaces.
- **Entry conditions:** IP1 gate explicitly approved; A/B remain GitHub-reachable; IP2 execution authorized.
- **Acceptance criteria advanced:** US-01-AC-04; renewed AC-01–03 across upgrade.

### Granular tasks

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-01-IP2-T1 | Complete | Extend proposed driver/probe and focused subprocess tests for stable synchronization and explicit A→B upgrade, one red–green slice at a time | IP1 gate | No-op locked sync preserves identity; explicit upgrade changes declaration, resolved/installed commit, lock hash and evidence tuple; wrong retained revision fails verification even if version strings match | AC-03–04 |
| US-01-IP2-T2 | Complete | Extend `docs/experiment-setup.md` with verified upgrade, review and commit instructions; perform actual GitHub A→B in same disposable project; write `docs/verification/us-01-ip2.md` | T1 | Before/after pins, lock hashes/diff and installed metadata show change; post-upgrade CLI/import/resources and cache-independent operation pass; explain identity versus package version and preserve original A evidence | AC-01–04 |
| US-01-IP2-T3 | Complete | Run shared checks, inspect links/diff, reconcile AC table, update checkpoint and completion record | T2 | Gate report includes commands, versions, actual results, TDD evidence where applicable and limitations; harness lock unchanged; no claim of story acceptance before developer decision | AC-01–04 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Stable identity | Locked synchronization without declaration change | Same resolved SHA and exact lock hash | Passed — [IP2 evidence](../verification/us-01-ip2.md) |
| Explicit upgrade | Documented uv revision change and intentional experiment lock update, followed by locked sync | Different A/B, changed declaration/lock/environment evidence, correct installed B | Passed — [IP2 evidence](../verification/us-01-ip2.md) |
| Upgrade regressions | Repeat isolated CLI/import/resource probes and disposable cache removal; focused verifier failure tests | Interfaces available; wrong revision rejected; no checkout/cache runtime reliance | Passed — [IP2 evidence](../verification/us-01-ip2.md) |
| Final checks | Shared commands; existing packaging regressions; fresh both-wheel checks if distribution changed | Pass with criterion-mapped report and unchanged harness lock | Passed — [IP2 evidence](../verification/us-01-ip2.md) |

### Developer approval gate

- **Approval criteria:** T1–T3 complete; all four criteria have actual installation/upgrade evidence; limitations explicitly reviewed.
- **Evidence presented:** [IP2 evidence](../verification/us-01-ip2.md) and [approved IP1 evidence](../verification/us-01-ip1.md). T1–T3 complete; actual GitHub A→B upgrade and stable-sync control passed; 23 tests and all shared checks passed; harness lock unchanged.
- **Remaining limitations or blocked work:** macOS/Python 3.12 verification scope; Windows/additional Python and any unrun Linux installation checks remain unverified. Initial installation requires network/GitHub access. Initialization and run provenance are downstream work.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer message “i approve ip2; commit the changes”, 2026-10-30.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Final story review only; IP2 approved and local commit authorized. US-02 requires separate planning/execution authorization.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-01-AC-01 — documented prerequisites, separate project and full-SHA GitHub install | IP1-T1,T2,T4; IP2-T2,T3 | Bootstrap transcript and reviewed guide in proposed IP1/IP2 reports | Verified by [IP1](../verification/us-01-ip1.md) and renewed in [IP2](../verification/us-01-ip2.md); IP1 and IP2 approved; story acceptance pending |
| US-01-AC-02 — normal installed dependency without maintained checkout/cache | IP1-T3,T4; IP2-T2 | Noneditable metadata, isolated import paths and cache-removed runtime probes | Verified by [IP1](../verification/us-01-ip1.md) and renewed in [IP2](../verification/us-01-ip2.md); IP1 and IP2 approved; story acceptance pending |
| US-01-AC-03 — resolved revision/dependencies locked; CLI/import/resources available | IP1-T2–T4; IP2-T1–T3 | Independently checked declaration, parsed lock, installed metadata and resource/CLI results | Verified by [IP1](../verification/us-01-ip1.md) and renewed in [IP2](../verification/us-01-ip2.md); IP1 and IP2 approved; story acceptance pending |
| US-01-AC-04 — explicit upgrade changes pin, lockfile and environment identity | IP1-T1; IP2-T1–T3 | [IP2 report](../verification/us-01-ip2.md): A/B metadata, exact lock hashes/diff, stable-sync control and upgraded installed probes | Verified; IP2 approved, story acceptance pending |

- **Remaining work:** IP1 approved; IP2 T1–T3 technically complete and all four criteria verified on macOS/Python 3.12. Both implementation gates approved; explicit story acceptance pending. No US-01 criteria deferred.
- **Partial prerequisite delivery:** Accepted US-33 foundation reused; no prerequisite story reopened. US-02 remains downstream.
- **Developer acceptance:** Pending; final gate serves as story acceptance only if explicitly stated.
- **Decision reference and date:** Pending.

## IP1 execution record — 2026-10-30

Developer message “i approve the plan; execute us-01 ip1” approved the plan and confirmed public test boundaries, authorizing IP1 only. Issue #8 complete body/all comment pages refreshed with stable zero-comment metadata. T1–T4 completed with [criterion-mapped evidence](../verification/us-01-ip1.md). Five red–green slices passed; all 20 tests, lint, format, strict types, locked sync/check and smoke passed. Real GitHub A installation, fixture-cache removal, offline/no-sync runtime, unknown GitHub commit and stale-lock refusal verified. No product code/dependency/lock/resource changes or suppressions. Local links and diff whitespace checked. No commit, push, PR, issue edit or hosted CI triggered. Stop at IP1 developer gate; IP2 and story acceptance remain pending.

IP1 gate approved 2026-10-30 by developer message “i approve us-01 ip1; commit changes; execute ip2”. Commit IP1 changes, then execute IP2; final IP2 gate and story acceptance remain pending.

## IP2 execution record — 2026-10-30

IP1 committed as `60941af` after the explicit approval/commit request. Complete issue #8 body/all comments refreshed, stable zero-comment metadata `2026-10-30T02:06:17Z`; no new scope decisions. IP2 T1–T3 complete with [evidence](../verification/us-01-ip2.md): two red–green slices, retained-old-install regression, actual GitHub A→B upgrade in one experiment, unchanged locked-sync control, preserved A evidence, changed B pin/lock/identity and post-upgrade cache-independent installed interfaces. All 23 tests, lint, format, strict types, locked sync/check and smoke passed; harness lock unchanged. Local documentation targets and diff whitespace verified. No scope deviation, dependency change, suppression or unresolved failure. IP2 changes remain uncommitted for gate review; no push/publication. Final gate and story acceptance pending; stop here.

IP2 gate approved by developer message “i approve ip2; commit the changes”, 2026-10-30. Local commit authorized. This approves the implementation phase; explicit story acceptance remains pending under the separate completion-review field. No push or next-story execution authorized.
