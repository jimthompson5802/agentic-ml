# US-03 IP3 verification

Developer authorized IP3 with “start executing ip3” (2026-10-31). Subsequently
approved the completed phase with “i approve ip3” after implementation/status review.
Issue #10 complete body/all comments refreshed: zero comments, stable updated time
2026-10-30T02:06:20Z. Milestone 1; AC-02/04, with AC-01/03 preservation.
Approved public boundaries and direct-test mapping are in the owning plan.

## TDD evidence

Focused cycles run serially for short feedback, using unique external basetemp
directories to avoid the previously observed pytest retention-cleanup delay.

- Fixed/search overlap: initial resolver test failed (incorrectly input-ready).
  First implementation rejected overlap with the exact parameter and source.
  Verification exposed a test fixture line-count error: expected 7, actual
  declaration is line 6. Corrected the literal to 6, preserving exact location
  assertion and the overlap rejection requirement. This is a test-authoring
  correction, not a relaxation of the boundary contract.

## TDD cycles and outcomes

Commands use `uv run --locked pytest tests/integration/test_planning.py::<test>`
and `--basetemp=/private/tmp/us03-ip3-cycle<N>-red` or `-green`. The first
cycle's original red used pytest's default basetemp; its process reported failure
at 100% then remained in shutdown. Subsequent unique basetemps exited normally.
The first green/corrected runs used `cycle1-green` and `cycle1-corrected`.
The initial red's test was run before any product change; it reported a failure
because overlapping fixed/search input was accepted. See the session record for
console evidence; raw red logs were not separately exported. No red result is
claimed to be a final passing check.

| Cycle | Public test / independently specified behavior | Red | Green / relevant tests |
|---|---|---|---|
| 1 | `test_fixed_parameter_cannot_also_be_tunable` | Failed, input-ready instead of blocked | First correction rejected correctly but exact line assertion exposed fixture miscount; corrected line 6: 1 passed |
| 2 | `test_invalid_search_definitions_block` | 14 failed, 2 existing parser finite-number rejections passed | 17 passed with overlap test; empty/duplicate/compound categories, numeric typing/order/scale/log positivity and unknown fields rejected |
| 3 | `test_public_checker_preserves_type_distinct_categories` | Missing public checker/types (ImportError), expected API absent | 1 passed; type-distinct JSON categories, inclusive equal bounds and invalid empty algorithms |
| 4 | `test_algorithm_selection_obeys_brief_mode` | 5 failed; temporary IP2 block prevented valid subset requests and detailed diagnostics | `-k 'algorithm_selection or fixed_parameter_cannot or invalid_search_definitions or public_checker'`: 23 passed, 76 deselected |
| 5 | `test_resolution_preserves_declared_and_narrows_effective_space` | 1 failed, valid narrowing blocked | 1 passed; literal declared/effective maps, distinct version IDs, both versions independently verify |
| 6 | `test_execution_cannot_widen_parameter_boundaries` | 16 failed, boundary changes accepted | `-k 'execution_cannot_widen or resolution_preserves_declared'`: 17 passed, 99 deselected |
| 7 | `test_execution_budget_only_lowers_explicit_ceiling` | 2 failed, 4 already-blocked cases passed | With preservation test: 7 passed; lowered/equal ceilings, explicit provenance, null/new/increased ceilings rejected |
| 8 | `test_public_checker_rejects_invalid_execution_shape` | 3 failed, 6 passed; unknown field/integral constraint bypass and malformed-map ValueError | 9 passed using installed execution schema for direct checker calls |
| 9 | `test_public_checker_rejects_non_json_fixed_values` | 3 failed, infinity/NaN/oversized integer accepted directly | With undeclared-parameter regression: 4 passed |
| 10 | `test_algorithm_selection_obeys_brief_mode` with effective allowed-list assertion | 1 failed, 4 passed: select narrowing missing from effective decisions | 5 passed; effective allowed algorithms agree with effective space |

An intermediate direct resolver regression run had **130 passed, 1 failed**:
the historical IP2 test expected `boundary_validation_pending`. IP3 replaces that
temporary diagnostic with actual validation. Renamed it to
`test_undeclared_parameter_cannot_be_silently_accepted`, retained the rejected
request and blocked assertion, and added exact parameter-field/no-plan checks.
No acceptance criterion, timeout or rejection assertion was removed. This is the
planned IP2→IP3 behavior transition, not a suppressed failure.

No unresolved corrective problem reached the three-attempt limit. Cycle 1's
test-authoring correction and every intermediate failure above remain recorded.

## Direct phase verification

Changed product modules: new `planning/boundaries.py`, `planning/resolution.py`
and `planning/__init__.py`. Direct resolver/checker tests live in
`tests/integration/test_planning.py`; the extended installed probe
`tests/installation/check_planning.py` is exercised through
`tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths`.
Public boundaries were approved in IP1; this implementation retains them.

Command:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths --basetemp=/private/tmp/us03-ip3-phase-verification-1 --junitxml=/private/tmp/us03-ip3-phase-verification-1.xml
```

**135 selected/135 passed, exit 0, 47.09 seconds**, four workers. Explicit paths
select 134 resolver/checker cases plus one installed-wheel orchestrator. No
marker-deselected case within these selectors; tests outside them were not
collected. Full collection count recorded separately below.

Both real wheel paths passed isolated `-I` probes from independent temporary
experiment projects with declared runtime dependencies and no source-path
imports. Each installed probe exercised **16 CLI/API boundary scenarios** plus
the standalone public checker. Existing installed path/cwd, classification and
regression, use/select/compare, source checksums, retention/corruption, pending
delegation and unchanged draft/project-file checks also passed.

The independently specified endpoint cases cover float 0.1/10 and integer 1/10,
just-outside float rejection, strict fixed/category/integer types, unknown names,
selection outside brief, valid/invalid range narrowing and budget lowering.
The source resolver matrix adds mode-specific pool narrowing, invalid declared
spaces and exact parameter/source diagnostics.

## Shared checks and limits

`uv sync --locked --group dev`, `uv lock --check`, `uv run --locked ruff check .`,
`uv run --locked ruff format --check .`, `uv run --locked mypy src tests`,
`uv run --locked agentic-ml --version` all passed. Format check: 103 files;
strict mypy: 32 source files; smoke: `0.1.0`. Initial combined sandbox execution
of these commands was denied uv-cache writes; each command was rerun with
escalation and returned exit zero. These infrastructure failures are not TDD reds.

No dependencies, schemas, initialization resources, suppressions, CI or test
timeouts changed. Direct tests preserve old/new inputs and exact plan hashes;
current sources are rechecked only when explicitly requested. Earlier IP2 plans
are not treated as compatibility fixtures for future checker semantics; all
newly generated versions in this phase are independently reverified.

M1-ACCEPT-VERIFY owns caller/dependent initialization, packaging-driver,
upgrade/scheduling regressions, the reserved milestone initialization test and
the full local suite (`-m ""`). IP4-T4 reuses valid direct phase evidence and
renews anything its executable changes invalidate. This phase does not claim a
full-suite run, runtime isolation, registry compatibility, training candidate
admission or budget consumption enforcement. Delegated decisions remain blocked
until IP4; input-ready does not authorize execution/data access.

Lock before and after shared verification:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

## Final identities and handoff

- Tested base: `103cdf83d07b6f279a613c5b2b20c13829d7d559`, branch
  `US-03-experiment-boundaries`, plus the uncommitted IP3 implementation/tests.
- OS: macOS 15.7.9 arm64; Python 3.12.15; uv 0.13.1; pytest 9.1.1,
  pytest-xdist 3.8.0. No Linux, Windows or remote-filesystem verification added.
- Source/test/build inventory: 54 maintained files, saved at
  `/private/tmp/us03-ip3-input-inventory.json`, SHA-256
  `bd6471f7addc21483e9ca1a9388d6281fc0b359ac976febb1722769607fa0f15`.
  All 37 packaged members in the tested wheel match final `src/agentic_ml` bytes.
- Direct wheel and genuinely sdist-rebuilt wheel both have SHA-256
  `29287a049c9e99f903ea5d2dcfd534939ebfe4983cb6a9a6961bafe4003930ba`.
- Source distribution SHA-256:
  `d84c22a0ecdfec6afb2678dc5aae802f34dca17efed68f8bc2b210c2a6c603d1`.
- Built artifacts: `/private/tmp/us03-ip3-phase-verification-1/popen-gw3/artifacts0`.
  Probe logs: adjacent `test_planning_from_both_artifa0/planning/` contains
  `distributions.log`, `direct-wheel.log`, `rebuilt-wheel.log`. Rebuilt artifact
  and isolated environments remain at
  `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-t_zngf6z`.
- XML: `/private/tmp/us03-ip3-phase-verification-1.xml`. Full collection-only
  check: **265/266**, one milestone test deselected; **130 routine tests outside
  the 135 direct cases were not run**. No broader suite claim.
- Final documentation check: 45 local links/anchors passed across checkpoint,
  plan, setup guide and this report. `git diff --check` passed. Documentation and
  approval records do not invalidate executable/artifact evidence.
- Original cycle-1 red runner (PID 75114, uv parent 75086) remained in shutdown
  at handoff after reporting one failure/100%; process inspection showed state
  `U`. Precise shutdown cause was not diagnosed. It was not cancelled or counted
  as a completed command. All subsequent focused runs and the final passing
  four-worker phase verification exited; their result is independent of this
  earlier runner. Historical pytest retention/shutdown evidence remains in
  [the runtime report](pytest-runtime-optimization.md); this phase makes no new
  shutdown-performance claim.

  Subsequent developer instruction “kill that pid” authorized termination.
  `kill -KILL 75114` succeeded; `ps -p 75114,75086` then showed neither process.
  The original tool session closed with exit **137**. The initial red is recorded
  as a reported test failure followed by developer-authorized termination, not
  a normally completed test command. Final 135-pass evidence is unchanged.

| Criterion | IP3 evidence | Remaining ownership |
|---|---|---|
| US-03-AC-01 | All three algorithm modes; effective algorithm/budget narrowing and explicit override provenance | Delegated choices and final guidance in IP4 |
| US-03-AC-02 | Declared domain validation, fixed/category/numeric subset rejection and CLI/API parity on both wheel paths | US-05 registry/candidate integration before training |
| US-03-AC-03 | Declared/effective separation, new identities, retained/reverified prior versions, installed hash checks | IP4 approval bindings and final story reconciliation |
| US-03-AC-04 | Source-located conflict diagnostics, no plan for invalid requests, unchanged blocking of delegation | IP4 matching/stale/revoked approval semantics |
| US-03-AC-05 | Existing direct/installed root/cwd and preserved-source cases pass | No new path capability introduced |

IP3-T1–T3 complete and developer approved by “i approve ip3” (2026-10-31), after
implementation, evidence, stalled-process termination and status review. IP4
execution awaits explicit authorization. Developer “commit changes” authorizes
the local IP3 commit; Git history records its result. No push, PR, whole-story
acceptance or publication authorized. Approval-record-only updates preserve the
verified executable/artifact identities; no product test rerun is needed.
