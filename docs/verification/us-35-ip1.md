# US-35 Implementation Phase 1 evidence

Issue: [#47](https://github.com/jimthompson5802/agentic-ml/issues/47).
Plan: [Milestone 50 / US-35](../plans/milestone-50-us-35.md).
Execution authorized by developer: “execute implementaton plan for us-35”.
Plan and public boundaries approved 2026-11-01. Phase 1 gate approved on 2026-11-01: “i approve ip1; commit changes”.

## Scope, inventory and confirmed boundaries

Only installation verification and its development lifecycle helper change in this
phase. US-35-AC-01–05 are advanced for that slice. Product source, fixture reuse,
pytest retention/placement and early environment release remain unchanged.

| Existing command/component | Created paths and consumers | Cleanup boundary |
|---|---|---|
| `tests/installation/verify_installation.py` | Unique workspace; `experiment/.venv`, private `cache`; independent copied probe. Before-sync, post-sync, offline CLI and optional upgrade consume environment. | Final command after all consumers; preserve experiment files, pinned source and records; remove only registered environment/cache. Existing cache-independence deletions remain. |
| `tests/packaging/verify_distributions.py` | Independent workspace; direct/rebuilt environments and project logs; extracted sdist source and rebuilt wheel. Uses inherited shared uv cache. | Phase 2: outermost owner, never intermediate distribution subprocess completion for composed runs. Shared cache untouched. |
| `tests/installation/verify_initialization.py` | Parent workspace, copied Git source fixture, four initialized projects/environments; separate distribution workspace. Consumes extracted source/rebuilt wheel and checks installed pinned origins. | Phase 2: after final initialization/rerun probes. Source fixture is not a disposable environment. |
| `tests/installation/verify_planning.py` | Parent workspace, copied probe, projects without new environments; separate distribution workspace's two interpreters run planning checks. Existing `--workspace` accepts pre-existing directory. | Phase 2: after both installed planning probes; never adopt caller directory for deletion. |
| `check_project.py`, `check_installed.py` | Emit installed identity JSON; invoke installed CLI; do not create independent environments. | Preserve output before cleanup. |
| `check_initialization.py`, `check_planning.py` | Check existing project/interpreter, create controlled project/state, run public interfaces. Planning subprocess commands need outer captured stdout/stderr. | Do not delete while any probe is running. |
| Installation test callers | Successful-workspace readers in basic pinned-install, locked-sync and upgrade tests; `installed_project` fixture feeds mutation probes. Failure test reads `install.log`. | Evidence-only checks move to records; actual environment consumers explicitly request retention. Preserve assertions/timeouts. |
| Distribution test callers | Real wheel success, damaged artifacts, reserved complete initialization test and ordinary planning test. | Phase 2 adapts explicit retention where callers inspect projects. Reserved test stays reserved locally. |
| `.github/workflows/ci.yml` | Runs standalone distribution driver after `uv build`; no downstream workspace consumer. | Default success cleanup compatible; CI configuration unchanged. |

Proposed public helper API within the approved lifecycle seam: `Invocation` creates
an exclusive workspace and record directory, `create_disposable(relative)` creates
and owns a disposable directory, `run(stage, command, cwd, env)` records process
results, `preserve(source, name)` copies explicitly selected evidence and
`finish(verification_code)` persists outcomes then conditionally cleans owned paths.
Driver uses the helper through an explicit file-location import of the development
module; no harness source path is added to installed interpreters. Helper tests use
the same file import and public methods. Real temporary trees establish ownership;
filesystem fault injection tests failures. Real driver subprocesses establish
installed provenance, environment creation and cleanup. Tiny helper cases alone do
not verify package validity. Boundaries were confirmed through plan approval.

## Baseline protocol

Before changing any driver, run all four unchanged standalone commands sequentially
from one separate temporary cwd with fixed wheel/sdist and local full-SHA source
fixture. Capture commands/stdout/stderr, artifact hashes, environment paths/counts,
logical bytes and `du -sk` allocated usage after each command. Preserve all baseline
workspaces and copy diagnostic records; do not delete historical evidence.

Raw baseline: `.dev-records/verification/us-35-baseline-bac0e9c/` in this checkout.
The orchestrator and exact literal commands are retained there. Compare against the
same inputs in Phase 2; do not substitute a different source/artifact revision.
macOS/APFS allocated usage includes rounding, hardlink/clone/compression effects;
logical bytes are not physical unique storage. Shared caches and durable record
sizes are separate from disposable environment counts. No peak-usage or runtime
improvement claim is made.

Baseline results: all four commands exited zero on macOS 15.7.9 arm64,
Python 3.12.15. Baseline source fixture SHA `5b4717c8c6ab4c56866ddf909cd9a83686ef22da`.
The raw summary includes artifact hashes, exact workspace/environment paths and
both parent and nested distribution workspaces (initialization hides child stdout
in `distributions.log`, which was inspected separately).

| Command | Retained environments | Logical workspace bytes | Allocated KiB (`du -sk`) | Command elapsed |
|---|---|---|---|---|
| installation | 1 | 546756987 | 591388 | 24.82s |
| distribution | 2 | 1092870887 | 1185752 | 6.79s |
| initialization | 6 | 3516923616 | 3815600 | 243.59s |
| planning | 2 | 1093357756 | 1187800 | 28.11s |

All baseline paths remain intact. Baseline helper source and child-measurement
script are retained alongside raw records for exact replay. These are workspace
sizes, not sums of unique physical environment storage. Private installation
cache was already absent after its built-in cache-independence checks.

## TDD and verification

Serial focused tests are used only for short red–green slices; the phase gate uses
four workers with `loadgroup`. Record each red result and its green result below.
No regression assertions or timeouts may be weakened.

All focused TDD commands below use `uv run --locked pytest <selection> -q`.
Serial selection avoided worker startup during short red–green cycles. Full raw
baseline records are retained; focused test results below were observed in tool
output and are summarized here rather than claimed as saved raw pytest logs.

| Slice / selector | Red observation | Green observation |
|---|---|---|
| `test_verification_lifecycle.py::test_success_removes_only_created_disposable_paths` | Initial missing module was scaffolding, not accepted as behavioral red. With a no-cleanup skeleton, the environment-exists assertion failed (1 failed). | Remove registered directory only: 1 passed. |
| `test_failure_or_explicit_retention_keeps_environment` | Missing retention argument: 2 failed, 1 passed. | Retention supported: 3 passed. |
| `test_disposable_paths_cannot_escape_workspace` | Escapes reached filesystem instead of ownership rejection: 3 failed, 3 passed. No external path was created. | Reject absolute/traversal paths before writes: 6 passed. |
| `test_replaced_environment_cannot_redirect_cleanup` | Symlink cleanup raised instead of reporting separate outcome: 1 failed, 6 passed. | Ownership validation and separate cleanup error result: 7 passed. |
| `test_stage_records_commands_outputs_and_identity_before_cleanup` | Evidence preservation API missing: 1 failed, 7 passed. | Durable command/stdout/stderr/identity evidence: 8 passed. |
| `test_record_write_failure_retains_environment_and_original_failure` | Summary write errors escaped instead of returning original/nonzero status: 2 failed, 8 passed. | Fail closed, keep environment: 10 passed. |
| `test_workspace_cannot_overlap_checkout_or_records` | Checkout and records could be used as workspaces: 3 failed, 11 passed. | Reject overlap before allocation: 14 passed. |
| `test_invocation_reports_records_and_source_identity` | Absolute record location not printed: 1 failed, 14 passed. | Location and source/platform/tool identities: 15 passed. |
| Existing `test_installation_verification.py::test_pinned_project_runs_without_checkout_or_cache` | Real installed verification succeeded, but `.venv` remained: 1 failed in 23.79s. Original pin/dependency/import assertions preserved. | Same test plus 17 helper cases: 18 passed in 29.23s. It checks genuine installed identity followed by `.venv` absence and durable identity presence. |
| `test_command_created_environment_is_owned_only_if_initially_absent` | Missing reserve-before-installer option: 1 failed, 15 passed. | Reserve absent directory, capture installer-created identity: 16 passed. |
| `test_private_cache_can_be_released_and_recreated_by_next_stage` | Owned intermediate release API missing: 1 failed, 16 passed. | Release/reserve/recreation verified: 17 passed. |
| `test_spawn_failure_records_attempted_command_and_retains_partial_environment` | Attempted command absent from records: 1 failed, 17 passed. | Record unavailable executable and retain partial environment: 18 passed. |

Additional coverage for already-green behavior: cleanup permission failure and
original nonzero outcome, existing directory and symlink/shared-cache sentinels,
and two concurrent invocations yielded 22 helper tests passing in 0.83s.
The implementation passed every behavioral correction on its first verification;
no three-attempt escalation was reached. Early direct lint/type inspection found
unsorted imports and a fault-injection function with overly broad arguments;
import sorting and a precise `Path.write_text` signature corrected both. No
suppression, timeout change, test skip or relaxed assertion was introduced.

Additional incomplete-run TDD slice:
`test_unfinished_invocation_has_an_incomplete_durable_summary` failed because
`summary.json` did not exist before finalization (1 failed). Initialization now
writes an incomplete summary before verification begins; all 23 helper cases then
passed in 0.87s. This preserves available status if a process is interrupted,
without promising cleanup or complete child stdout after forced termination.

The real `test_failed_installed_probe_retains_available_environment` passed in
33.41s. Its independently damaged fixture removes the packaged sentinel resource;
installation completes, the installed probe fails with `template resource missing`,
and the environment plus failed probe log remain. This adds boundary coverage of
already-green failure retention rather than manufacturing another red result.

The first four-worker direct selection passed **34 tests in 130.85s**, before the
last two added cases and the incomplete-summary change. Its XML is retained as
`direct.xml`; it is historical evidence, not the final-input gate result.
The final selection passed **36 tests in 148.28s** with four workers and
`loadgroup`, against all final executable changes. No failures or deselections.

## Phase gate verification

Changed executable modules are `tests/verification_support.py` and
`tests/installation/verify_installation.py`. Direct behavior tests reside in
`tests/integration/test_verification_lifecycle.py` (23 helper cases) and
`tests/integration/test_installation_verification.py` (13 real installed/probe
cases). No unrelated product tests are selected. The explicit two-file selection
collects 36 cases, with zero deselected within those files; it is not full-suite
coverage. All existing installation assertions and timeouts remain intact.

| Check | Command / result |
|---|---|
| Final direct tests | `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_verification_lifecycle.py tests/integration/test_installation_verification.py --junitxml=.dev-records/verification/us-35-ip1-checks/final-direct.xml --durations=20` — **36 passed in 148.28s**, four workers, 0 deselected |
| Locked environment | `uv sync --locked --group dev` — passed; replaced the existing unusable environment whose interpreter `/usr/local/bin/python3.12` no longer existed with available Python 3.12.15. |
| Lock consistency | `uv lock --check` — passed, 195 packages resolved. |
| Lint | `uv run --locked ruff check .` — passed. |
| Formatting | `uv run --locked ruff format --check .` — passed, 124 files already formatted. |
| Strict typing | `uv run --locked mypy src tests` — passed, 39 source files. |
| CLI smoke | `uv run --locked agentic-ml --version` — passed, `0.1.0`. |
| Whitespace / lock diff | `git diff --check`; `git diff --exit-code -- uv.lock` — passed. |

Lock SHA-256 before the gate tests and after checks:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
No dependency, lock, product source, packaging metadata or runtime guidance change.
Sandbox-denied uv cache access was retried through normal command escalation;
these were environment permission failures, not behavioral red results.

Raw final check records are under the absolute directory
`/Users/jim/Desktop/genai/agentic-ml/.dev-records/verification/us-35-ip1-checks/`.
It holds JUnit XML, selected executable input SHA-256 identities, shared-check
outputs and an index of installation command records. Driver records contain their
own exact commands/cwd/output, source revision `bac0e9c` plus dirty paths,
platform/tool identities, retained pin/lock/declaration/installed identities and
checksums, and independent verification/cleanup outcomes. Successful default
command records remain after the environment is removed. Helper boundary tests
use isolated fake checkout directories; their durable-location assertions do not
claim those fixture records survive pytest's eventual retention policy.

## Phase outcome

US-35-IP1-T1–T4 are complete. Developer approved the Phase 1 gate on
2026-11-01: “i approve ip1; commit changes”.
The final direct selection, shared checks, local document links and whitespace
checks passed. Phase 2 remains unstarted. All four unchanged
baseline command results are available; the final same-input before/after disk
comparison for all four commands is Phase 2 task US-35-IP2-T5. No full-story or
milestone acceptance is claimed. The other drivers retain their original behavior
until that approved implementation phase; their documentation update is also
scheduled there. No unresolved implementation design blocker or scope change was
found in Phase 1.

## Deferred verification

`M50-ACCEPT-VERIFY` owns unchanged product initialization/planning/approval caller
regressions, parallel scheduling regressions, full suite and the reserved complete
initialization test. Phase 2 directly tests its changed drivers. Existing
`M1-ACCEPT-VERIFY` ownership is preserved. Linux/Windows remain unverified locally.
