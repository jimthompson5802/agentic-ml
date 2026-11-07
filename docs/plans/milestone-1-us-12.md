# Milestone 1 / US-12: Validate extracted data

## Scope and outcome

- **Milestone:** M1, complete one local classification experiment.
- **Owning issue:** [US-12 #15](https://github.com/jimthompson5802/agentic-ml/issues/15), AC-01 and AC-05 only. [Complete source](sources/us-12-issue-15.md), retrieved 2026-11-07 UTC: one unique comment, all pages fetched, count and final metadata stable. GitHub milestone unset; body assigns M1. Scope decision comment 6699586004 preserves MVP-SC-01/02.
- **User-visible outcome:** A separate experiment project checks a native pandas DataFrame against explicit quality requirements, receives actionable results, and uses a supported public boundary that prevents its dependent operation from executing when required checks fail.
- **Acceptance criteria:** [US-12-AC-01](../specs/user-stories.md#us-12-ac-01): schema, row counts, types, nulls, duplicates and configured quality rules, with mismatches/failures. [US-12-AC-05](../specs/user-stories.md#us-12-ac-05): report results and block supported steps on required-check failure.
- **Issue split:** [US-12 #19](https://github.com/jimthompson5802/agentic-ml/issues/19) separately owns AC-02 assessment/distributions/target balance and AC-03 seeded/supplied partitions. [Complete source](sources/us-12-issue-19.md) has one unique comment, all pages fetched, stable final metadata; comment 6699588996 confirms the split. These criteria need a later owning plan; this plan does not close all US-12 work. AC-04 mandatory experiment assessment approval remains deferred.
- **Exclusions:** No splitting, model fitting, feature pipeline, runner, MLflow logging, DVC integration, notebook execution, assistant walkthrough, mandatory experiment approval, arbitrary-code enforcement or new workflow store. No changes to strict configuration/candidate-validation contracts or extraction completion semantics.
- **Coordinated execution index:** None. This plan owns one issue slice and consumes accepted US-11 without adding tasks to other stories.

Supporting design: [reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority), [data and quality](../specs/design/data-and-features.md#local-extraction-and-quality), [interfaces](../specs/design/interfaces-and-configuration.md), [blueprint](../specs/design/software-blueprint.md), [execution/failure distinctions](../specs/design/execution-and-governance.md), [layout](../specs/design/repository-layout.md), [traceability and fixtures](../specs/design/acceptance-traceability.md#required-scenario-families), [delivery order](../specs/design/milestone-delivery.md#capability-order-and-owning-stories), and [ADR-007/008](../specs/design/architecture-decisions.md). Active issue and design scope agree; shared validation-approach prose mentioning splits does not move #19 criteria into #15.

## Current repository findings

Planning baseline: `cfcda77`, clean `main`; planning branch `US-12-data-validation` created and verified. No existing US-12 implementation plan was found.

`src/agentic_ml/extraction/__init__.py` exports accepted `extract_data`, returning `(DataFrame, dict)` and publishing dataset/provenance. Its `complete` status means extraction completed, not quality passed. US-11 is accepted and merged in PR #60; [owning plan](milestone-1-us-11.md) and [IP3 evidence](../verification/us-11-ip3.md) own its IP1–IP3 approvals and installed-project checks. Reuse that capability without changing its signature, output semantics or private helpers.

`agentic_ml.validation` currently exports plan-bound metadata/configuration/candidate validation. It does not check dataset contents. Keep this distinction clear in modules, naming and documentation. No data-quality public API or tests were found. Proposed new names below are review candidates, not implemented contracts.

Pandas `>=3.1,<3.2`, pyarrow `>=25,<26` and development pandas stubs are already declared. No dependency or lock change is expected. Existing distribution integration tests and `tests/installation/{verify_extraction,check_extraction,extraction_project}.py` demonstrate separate-project probes for both normally installed wheel paths. Reuse their infrastructure, identity records and cleanup rules rather than introducing another environment manager. Existing `pyproject.toml` workspace membership points to generated pytest content; preserve it and report any blocking sync issue rather than silently repairing it.

## Dependencies and decisions

| Dependency or decision | Required outcome | Work blocked | Status / evidence |
|---|---|---|---|
| Accepted local extraction | Obtain a native DataFrame and identifiable local output | External extraction-to-quality example | Satisfied by US-11 IP2/IP3 and whole-story acceptance in linked plan; no new supplier tasks |
| Public quality contract and test boundaries | Confirm rule shape, dtype semantics, failure policy and blocking interface | All executable tests and implementation | Proposed below; settle in IP1 and obtain Gate 1 approval |
| Report meaning and freshness | Distinguish invalid settings, executed failed checks and callback/process errors; check data actually consumed | IP2/IP3 | IP1-T2 decision; no caller-supplied success flag or stale report treated as authorization |
| Existing artifact infrastructure | Both direct and sdist-rebuilt normal installs exercise public quality API | IP3 | Existing drivers inspected; IP1-T3 selects minimal extension seam |
| Future pipeline adoption | US-10/14/15/18/39 consume the reviewed blocking boundary before affected work | Full experiment integration | Outside #15; document handoff, do not claim a runner exists |
| Assessment and splits | Distributions, target balance and seeded/supplied membership | #19 acceptance only | Separate issue; not prerequisites for validating an existing DataFrame |

## Plan review

- **Status:** Approved; implementation authorization and all implementation gates remain pending.
- **Developer decision:** Approved.
- **Decision reference and date:** Developer “i approve plan; commit changes”, 2026-11-07 UTC. Authorizes plan approval and a local commit of the planning changes; no IP1 execution or publication authorized.
- **Requested plan changes:** None recorded.
- **Implementation authorization:** Pending; plan approval does not approve implementation gates.

## Scope-change history

None. During execution use [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md) for material scope/approach changes; record change ID/date, request, scope difference, impacts, revisions, verification/gates, explicit decision and resume point. Preserve historical evidence and approvals.

## Proposed technical approach and public test boundaries

Use native pandas frames, ordinary configuration dictionaries and small reusable functions in proposed `src/agentic_ml/data_quality/`; keep existing `agentic_ml.validation` exports unchanged. No proprietary table, source, request or pipeline hierarchy is needed. Proposed signatures for IP1 review:

```python
validate_data(frame, *, rules) -> dict
run_validated_step(frame, step, *, rules, settings=None) -> tuple[object, dict]
```

`validate_data` checks without modifying input and returns a JSON-compatible report. `run_validated_step` validates a defensive frame snapshot immediately before passing that checked snapshot and copied settings to the project operation; on required failures it raises proposed `DataQualityError` carrying the report before invoking the operation. A passing report alone is not a reusable permission token. Callback exceptions propagate with useful stage context and original cause/type. IP1 must confirm whether this small callback helper is the preferred public enforcement boundary; a changed choice requires revised tasks and developer review before dependent tests. It is synchronous trusted-local composition, not a general runner or security boundary.

Proposed configuration covers required columns and optionally exact schema, native pandas dtype declarations, inclusive row-count bounds, per-column null limits, whole-row or declared-key duplicate limits, and named configured rules (minimum proposal: inclusive numeric range and allowed values). Explicit required versus advisory checks determine blocking; advisory failures remain visible. Consider project-owned pandas rule callbacks only if needed for AC-01; IP1 must bound their return/error semantics rather than adding an unreviewed rule language. Invalid/unknown rules, missing referenced columns, negative/impossible thresholds and unsupported types must fail explicitly. Do not silently coerce data or infer thresholds.

IP1 must settle empty frames, duplicate column names, nullable/extension dtypes, missing values in range/membership rules, duplicate counting (`keep=False` versus excess rows), all-null columns, finite numeric values and deterministic check ordering. Specify strict JSON normalization of pandas/NumPy scalars and missing values. Reports must identify checks/columns, effective expectations, actual measurements, pass/fail, required/advisory status and aggregate blocking status. Bound examples rather than dumping sensitive/full rows. This scope needs neither a generic report registry nor automatic report persistence; projects may serialize the returned dictionary. If persistence is added, review its path/conflict/failure semantics first.

Proposed public test boundaries, confirmation pending Gate 1:

| Boundary | Independently checked observations | Limits |
|---|---|---|
| `validate_data` using tiny native frames | Literal expected counts/schema/rule outcomes; JSON serialization; no mutation; invalid declarations | Does not prove fitting, scientific validity, splits or pipeline adoption |
| `run_validated_step` with project operation | A sentinel file/observable output appears only when required checks pass; failed report retained in exception; advisory-only failure proceeds; checked data equals consumed data | Trusted same-process operation; does not constrain external Python or future runners |
| Separate installed project | Import origin, CLI version, extraction-to-quality results, block/proceed outcomes and report serialization on both wheel paths from unrelated cwd | Observed OS/Python/dependency versions only; no notebook/assistant/DVC claim |
| Existing strict public APIs | Existing M1 regressions remain green | Does not extend their contract to basic experiment execution |

Fixture proposal: valid rows `id=[1,2,3,4]`, `age=[20,35,40,50]`, `group=[A,B,A,C]`; require these columns, integer id/age, four rows, zero age nulls, unique id, age 0–120 and group in A/B/C. Independently altered fixtures remove `age`, add an unexpected column under exact-schema rules, change dtype, use three/five rows, introduce one age null, duplicate id 1, set age 121 or group Z. Declare literal expected counts and mismatches before implementation. Include exact-boundary values, nullable types, empty/all-null inputs, malformed rules, required/advisory combinations and repeated calls after data changes. Confirm final fixture values and measurement semantics at Gate 1; tests must not call production helpers to derive expected results.

## US-12 / Implementation Phase 1: Settle quality and blocking contracts

- **Outcome:** Reviewed concrete interface, rule/report semantics, test boundaries and integration handoff.
- **Entry conditions:** Developer approves plan and explicitly authorizes IP1.
- **Acceptance criteria advanced:** AC-01/05 design only; no executable acceptance.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-IP1-T1 | Not started | Refresh complete #15/#19 discussions using retrieval skill; reconcile this plan and source snapshots with active stories/design and US-11 evidence | IP1 authorization | Stable full sources, confirmed criterion ownership and recorded prerequisite identity | AC-01/05 |
| US-12-IP1-T2 | Not started | Create proposed `docs/data-quality.md` contract; settle every decision above, proposed `data_quality` exports, supported rules and errors; update plan with final fixtures and public boundaries | T1 | Exact signatures, examples, literal expected reports and blocking semantics ready for developer confirmation; no unresolved executable-contract choices | AC-01/05 |
| US-12-IP1-T3 | Not started | Inspect artifact test fixture/driver seams; specify proposed `tests/integration/test_data_quality.py`, installed probe paths and future pipeline consumption in contract; reconcile relevant active design statements if needed | T2 | Concrete file/task refinements and coverage matrix; no added dependency or new runner prerequisite | AC-01/05 |
| US-12-IP1-T4 | Not started | Record proposed `docs/verification/us-12-ip1.md`, link checks, criterion/decision reconciliation and checkpoint update | T1–T3 | Documentation checks pass, contract/boundaries presented for Gate 1 | AC-01/05 |

### Verification and review evidence

Documentation-only: check all changed local links/anchors, criterion assignment, signature/report/example consistency and `git diff --check`. TDD, pytest and shared executable checks do not apply because this implementation phase changes no executable behavior. No test results claimed.

Deferred executable coverage is owned by IP2-T1–T4 and final IP3-T4. IP1-T3 must select the exact installed-probe extension and update task paths before Gate 1; no tests begin until boundaries are confirmed.

### Developer approval gate

- **Approval criteria:** All tasks complete; rules, edge cases, public boundaries, installed-probe paths and handoff reviewed; unresolved decisions closed.
- **Evidence presented:** Pending IP1 report and contract.
- **Remaining limitations:** Design only; future pipeline integration remains separately owned.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Stop. Explicit Gate 1 approval and IP2 authorization required before executable work.

## US-12 / Implementation Phase 2: Implement checks and blocking through TDD

- **Outcome:** Public dataset validation and immediate blocking boundary work against native pandas data.
- **Entry conditions:** Gate 1 approved, boundaries confirmed, IP2 authorized; implement final reviewed contract rather than treating draft signatures as settled.
- **Acceptance criteria advanced:** AC-01 and AC-05 executable behavior; installed-artifact acceptance remains IP3.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-IP2-T1 | Not started | Add proposed `tests/integration/test_data_quality.py` and `src/agentic_ml/data_quality/` exports; start with one passing-frame behavior test, then schema/type/row-count cases, one red–green slice at a time | Gate 1 | Independently expected reports, strict invalid-setting errors and unchanged native frame verified | AC-01 |
| US-12-IP2-T2 | Not started | Extend same public tests and package with null, duplicate and reviewed configured-rule checks; advisory/required aggregation and JSON normalization | T1 | Each boundary/failure case added through its own red–green cycle; full literal outcome matrix passes | AC-01/05 |
| US-12-IP2-T3 | Not started | Implement reviewed blocking function/error and public sentinel-output tests; verify pass/proceed, required fail/block, advisory fail/proceed, changed-data recheck and project exception propagation | T2 | Failed checks never invoke dependent operation; report accessible; consumed frame is checked frame; no internal collaborator mocks | AC-05 |
| US-12-IP2-T4 | Not started | Review structure after green; finalize API docstrings and contract examples; run M1/shared checks; record proposed `docs/verification/us-12-ip2.md` and checkpoint | T1–T3 | All required checks pass, actual red/green commands/results and changed modules recorded, Gate 2 evidence ready | AC-01/05 |

### Verification and review evidence

Use one public behavior test per red–green cycle, including an observed intended failure before implementation. Proposed focused command after file creation: `uv run --locked pytest tests/integration/test_data_quality.py -k <behavior>`. Short serial TDD is allowed with its rationale recorded; relevant existing regression selections follow [verification policy](../development/verification.md#phase-and-story-verification). Gate selection is the entire M1, not just these focused tests.

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Required/advisory quality cases | Reviewed public test matrix above | Literal measured results, actionable failures, no mutation | Pending |
| Blocking and error separation | Public sentinel output and raised-error tests | Required failure blocks; advisory failure proceeds; callback error stays a process failure | Pending |
| Current milestone | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass; record counts, skips and known limits | Pending |
| Shared development checks | Commands below | Pass without unintended lock change | Pending |

New product tests declare `milestone_1`. Contributor-only driver lifecycle tests, if necessary, declare `infrastructure`; do not misclassify these to obtain coverage. Existing M1 tests preserve strict validation/extraction behavior. M2–6 exclusions and installed quality scenarios are assigned to IP3-T4 and IP3-T1–T3 respectively. M0/M50/M99/infrastructure coverage remains outside automatic story selections; retain named historical milestone obligations.

### Developer approval gate

- **Approval criteria:** All tasks complete; confirmed public behavior and expected failures verified; M1/shared checks pass with unchanged assertions/skips; evidence recorded.
- **Evidence presented:** Pending IP2 report, contract and implementation diff.
- **Remaining limitations:** Installed quality behavior and final M1–6 acceptance pending IP3.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Stop. Explicit Gate 2 approval and IP3 authorization required.

## US-12 / Implementation Phase 3: Verify installed use and finalize issue acceptance

- **Outcome:** Independent installed projects verify extraction-to-quality/blocking behavior on both artifact paths; issue #15 evidence and user guidance ready.
- **Entry conditions:** Gate 2 approved and IP3 authorized; IP1-selected installation seam available.
- **Acceptance criteria advanced:** AC-01 and AC-05 fully within #15 scope.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| US-12-IP3-T1 | Not started | Add proposed `tests/installation/{data_quality_project,check_data_quality,verify_data_quality}.py` or the minimal alternative paths settled at Gate 1; reuse existing verification support | Gate 2 | Project-owned quality example imports installed public APIs; normal direct and sdist-rebuilt installs retain independent origins, runtime inventories and evidence | AC-01/05 |
| US-12-IP3-T2 | Not started | Add M1 integration case to `tests/integration/test_distribution_verification.py`; verify both paths from unrelated cwd with isolated Python, extraction output, each rule family and required/advisory sentinel outcomes | T1 | Public artifact behavior first fails as intended then passes; no source-checkout imports or editable install; malformed rules/callback failures retain context | AC-01/05 |
| US-12-IP3-T3 | Not started | Finish `docs/data-quality.md`, link from `README.md`; update affected active design status without rewriting history; document report JSON, failure recovery, future pipeline handoff and #19 exclusions | T2 | Runnable reviewed examples match API; installed resource inventory unchanged; no unsupported runner or whole-US-12 completion claim | AC-01/05 |
| US-12-IP3-T4 | Not started | Refresh complete issues, reconcile every criterion and deferred check; run M1 then final M1–6/shared checks; record proposed `docs/verification/us-12-ip3.md`, identities/platforms, final acceptance table and checkpoint | T1–T3 | All required evidence reconciled against final inputs before final gate; issue #19 remains open work | AC-01/05 |

### Verification and review evidence

| Check | Method or command | Expected result | Actual result / evidence reference |
|---|---|---|---|
| Installed project scenarios | New M1 integration case invokes reviewed artifact probe internally | Both normal wheel paths pass positive/failure/blocking cases; import/CLI/version/resource identities independently checked | Pending |
| Current milestone gate | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | Pass, counts and limits recorded | Pending |
| Final issue-slice acceptance | `uv run --locked pytest -n 4 --dist=loadgroup` | M1–6 pass against final executable changes | Pending |
| Shared checks and docs | Commands below; changed local links/anchors and examples | Pass; planned versus actual results distinguished | Pending |

No standalone artifact command or broader pytest selection is automatically authorized by this plan. Required artifact behavior is exercised inside selected M1 tests. Use new isolated owned child workspaces, preserve xdist groups/timeouts/fixture scopes, and retain raw records outside disposable trees. No executable changes after final evidence without renewal.

### Developer approval gate

- **Approval criteria:** All IP3 tasks complete; both criteria mapped to actual installed evidence; final M1–6/shared checks pass; deferrals and platforms explicit.
- **Evidence presented:** Pending IP3 report and acceptance matrix.
- **Remaining limitations:** #19 AC-02/03, deferred AC-04, downstream runner adoption, independent milestone obligations and unverified platforms remain open.
- **Developer decision:** Pending.
- **Decision reference and date:** Pending.
- **Requested changes and resolution:** None recorded.
- **Progression authorized:** Stop at final gate. Obtain explicit acceptance of issue #15 slice separately; Gate 3 may also provide that acceptance only if the developer says so. No commit, push, PR, issue edit/closure or merge authorized by this planning request.

## Shared checks and execution rules

Executable implementation phases run `uv sync --locked --group dev`, `uv lock --check`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy src tests`, `uv run --locked agentic-ml --version`, and `git diff --check`. Record `sha256sum uv.lock` before/after; CLI must match installed distribution metadata. Dependency changes require intentional review, not implicit lock regeneration. Record precise changed modules and commands, selected/deselected counts, timings, platform and any unrun checks.

Task status becomes Complete only after implementation and required verification pass and evidence is recorded. Reopen invalidated tasks. Keep technical completion separate from approval. Stop at every implementation phase gate including the final one; silence is not approval. Use small vertical red–green slices through confirmed public boundaries. Preserve original assertions, acceptance criteria, skips and timeouts. At most three corrective attempts per same unresolved problem; track hypothesis/change/original-failure verification and relevant regressions. After the third failed attempt, stop, retain logs and working-tree state, and request developer direction. Apply [scope management](../../.agents/skills/manage-plan-scope/SKILL.md) before implementing discoveries outside approved scope.

Reports belong in `docs/verification/us-12-ip*.md`; raw commands/logs/JUnit/identities belong in unique `.dev-records/verification/<timestamp>-<revision>-us12-<phase>/` directories under [records policy](../development/records.md). Preserve failure evidence, available reports and platform qualifications. Keep credentials and dataset content out of Git. Update `CHECKPOINTS.md` at task completion, gates, blockers and handoff.

## Final verification requirements

- **Owner:** US-12-IP3-T4, before final gate.
- **Final identity:** Record commit plus working-tree diff, lock SHA-256, direct/rebuilt artifact hashes and installed identities, Python/uv/pandas/pyarrow versions, OS/architecture and unrelated project cwd.
- **M1–6/shared checks:** Run against final story changes; renew after executable changes. Record counts/skips and reconcile each with its actual coverage. Documentation-only final edits use document checks.
- **Artifact boundary:** Both installed paths through selected integration tests; no standalone artifact driver or complete-suite run without explicit developer command. Existing packaged-resource checks remain unchanged and run through reused normal-wheel verification.
- **Deferred-check reconciliation:** IP2 omissions resolved by final M1–6 and installed checks. Infrastructure/M0/M50/M99 exclusions and historical skips remain named limitations, not passing evidence. Missing required #15 evidence blocks acceptance.
- **Actual results:** Pending. No product tests, builds, dependency installation or quality implementation performed during planning.

## Story completion review

| Acceptance criterion | Implementation phases / tasks | Verification evidence | Result |
|---|---|---|---|
| US-12-AC-01 (#15) | IP1-T2; IP2-T1/T2; IP3-T1/T2/T4 | Literal schema/count/type/null/duplicate/rule cases; installed positive/negative reports | Pending |
| US-12-AC-05 (#15) | IP1-T2; IP2-T2/T3; IP3-T1/T2/T4 | Required/advisory reports, absent/present downstream sentinel, project failure separation | Pending |
| US-12-AC-02/03 (#19) | Separate future plan | No acceptance claimed | Outside this plan |
| US-12-AC-04 (#19 deferred) | Future explicit scope activation | No mandatory experiment gate implemented | Deferred |

- **Remaining work:** #19 assessment/splits and consumer-story integration; no full experiment acceptance.
- **Partial prerequisite delivery:** #15 component slice only; issue acceptance does not mean all US-12 or M1 acceptance.
- **Final verification:** Pending US-12-IP3-T4.
- **Developer acceptance:** Pending, explicitly for issue #15 scope.
- **Decision reference and date:** Pending.

## Milestone acceptance handoff

**Owner:** Existing `M1-ACCEPT-VERIFY` obligation in [checkpoint](../../CHECKPOINTS.md#outstanding-verification-and-known-limitations), with US-03 ownership retained. `M50-ACCEPT-VERIFY` remains independent. Reconcile historical selections, failed/skipped cases, raw evidence availability, artifacts/manual/platform deferrals and actual final inventories before milestone acceptance. Complete-suite `uv run --locked pytest -n 4 --dist=loadgroup -m ""` and standalone artifact checks require explicit developer commands; do not run them merely because the template names milestone handoff. Preserve historical evidence and approvals; CI success is not substitute local evidence.
