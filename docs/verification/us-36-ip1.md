# US-36 Implementation Phase 1 evidence

Execution authorized on 2026-11-01 (America/New_York): “start ip1”. Plan and
public subprocess/filesystem boundaries were already approved. IP1 gate approval
was accepted on 2026-11-01: developer “i accept ip1”, after review of the
verification summary. The owning plan records IP2 progression separately.

Issue #49 was retrieved with complete body, zero comments from every page, and
stable metadata refresh (`updated_at=2026-11-02T00:58:23Z`). Scope remains all five
US-36 criteria in Milestone 50, with driver adoption reserved for IP2.

## Allocation inventory and baseline (IP1-T1)

| Allocation | Current owner / planned adoption in IP2 |
|---|---|
| `test_distribution_verification.py` artifact `mktemp` | Module fixture; adopt explicit shared ownership without scope changes |
| Distribution success, damaged-wheel helper, missing/ambiguous artifacts, corrupted sdist and rebuilt-probe failure calls without `--workspace` | Independent driver allocation today; add fresh descendants of each `tmp_path` |
| Distribution planning, reserved initialization and explicit-retention calls | Already explicit test descendants; preserve flags/assertions |
| `test_installation_verification.py` source and probe-parent `mktemp` | Module fixtures; adopt shared ownership, preserve mutable probe grouping/restoration |
| All installation driver calls | Already explicit test/shared descendants |
| `test_initialization.py` source `mktemp` | Module fixture; adopt shared ownership at existing scope |
| Initialization/project fixture and planning driver call | Already explicit test descendants |
| `test_verification_lifecycle.py` concurrent helper test and child-record failure test | Independent `Invocation` allocation; supply fresh test descendants |
| Lifecycle artifact `mktemp` | Module fixture; adopt shared ownership |
| Lifecycle parent-failure test | Independent parent driver allocation; supply explicit child and preserve `WORKSPACE` assertions |
| Lifecycle parent-early-failure test (both drivers) | Independent parent allocation; supply fresh test descendants and preserve linked child diagnostics |
| Other lifecycle helper and initialization/planning calls | Already explicit test descendants |
| `test_parallel_execution.py` nested `--basetemp` | Already dedicated test descendant; preserve scheduling assertions and 120s timeout |
| `tests/verification_support.py` default `tempfile.mkdtemp` | Standalone owner; preserve default and flags, no helper changes intended |
| Four driver entrypoints | Standalone or explicit caller owner; composed distribution children already explicit |

Raw records: `.dev-records/verification/us-36-ip1/`. `run_workload.py` fixes six
selectors covering all four drivers, a passing negative case and driver-level
explicit retention, with four workers/loadgroup and unchanged assertions/timeouts.
The observer records per-test teardown workspace counts, logical bytes, allocated
KiB and environment counts. `baseline-summary.json`, `baseline/*.json` and
`identities/baseline.json` preserve measurements, initial input/artifact SHA-256
identities and all eight driver records (six parent invocations, two composed
children). No historical records or standalone workspaces were explicitly removed
or migrated. Initial focused TDD runs used pytest's existing numbered-root policy;
historical pytest retention was not audited. Subsequent outer checks use fresh
explicit bases; generated subprocesses use dedicated temporary roots throughout.

Initial revision: `6b66d45` (clean working tree). Lock SHA-256:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
Baseline identities were captured from the clean revision and surviving artifacts
after execution; the initial lock hash was read before execution. Existing driver
records also identify their actual initial inputs. Source, requirements, lock,
driver assertions and timeouts were unchanged during the baseline. New contributor
files were added while the baseline ran; package inputs were not edited until
its artifact-producing fixtures had completed.

The exact baseline command is in `baseline-summary.json`; reproduce it with
`uv run --locked python .dev-records/verification/us-36-ip1/run_workload.py <new-label>`.
It selects these nodes with `-n 4 --dist=loadgroup`, an exclusively new `--basetemp`
and a read-only report observer:

```text
tests/integration/test_distribution_verification.py::test_both_installed_wheel_paths_pass
tests/integration/test_distribution_verification.py::test_missing_artifacts_fail_with_selection_diagnostic
tests/integration/test_distribution_verification.py::test_explicit_distribution_retention_keeps_both_interpreters
tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths
tests/integration/test_installation_verification.py::test_pinned_project_runs_without_checkout_or_cache
tests/integration/test_verification_lifecycle.py::test_initialization_cleans_after_final_consumer[False]
```

**Baseline: 6 collected/selected, 0 deselected, 6 passed in 307.72s** (310.04s
including launcher). All six test roots existed at teardown; six parent driver
roots survived session completion, two outside the pytest tree. The composed
children remained descendants of their parents. Two retained environments are
the explicit driver-retention case, not unexplained leaks.

| Surviving parent driver root | Environments | Logical bytes | Allocated KiB |
|---|---:|---:|---:|
| Standalone distribution success | 0 | 2,787,724 | 3,108 |
| Standalone missing-artifact negative case | 0 | 0 | 0 |
| Explicit distribution retention | 2 | 1,702,864,057 | 1,854,756 |
| Planning | 0 | 3,259,750 | 5,124 |
| Pinned installation | 0 | 1,644,207 | 1,684 |
| Initialization | 0 | 16,923,396 | 18,552 |

The whole pytest base including shared artifacts retained 1,726,841,678 logical
bytes / 1,882,736 KiB / two environments. Including the two independent roots,
the union retained 1,729,629,402 logical bytes / 1,885,844 KiB. APFS allocated
sizes and logical lengths do not establish physical device reclamation or shared
cache use. Raw measurements preserve the absolute paths. These are baseline
values, not an IP2 reduction claim. Artifacts and source fixture paths survive
for replay identity checks; existing artifact-building fixtures rebuild on replay,
so IP2 must reconcile actual artifact identities before claiming equivalent inputs.

## Confirmed boundaries and TDD

Tests use real pytest subprocesses with the actual contributor plugin, public
fixture/configuration/report hooks, independently expected filesystem contents,
return codes and completion events. Parent-controlled release signals keep a
later case active while the parent observes an earlier completed teardown.
No private pytest APIs or fixture-finalizer lists are part of the implementation.
Small serial commands are focused TDD/diagnosis; the gate uses four outer workers.
Minimal projects prove ownership/timing/retention, not installed driver adoption.
IP2 owns actual driver containment and fixed-workload comparison.

### Lifecycle implementation

`tests/conftest.py` loads `pytest_workspace_support` only for contributor tests.
The `tmp_path` override and `owned_workspace(request, tmp_path_factory, name)`
allocate exclusive children using public `TempPathFactory.mktemp`. A fixture
finalizer releases ownership; the report wrapper waits until the complete
teardown report exists before removing released paths. Setup/call/teardown
failures are tracked across the owner scope. Shared owners survive active
consumers; a failed consumer/finalizer retains available diagnostics.

Failed reports include `WORKSPACE <absolute-path>`. Cleanup checks original
directory/parent identities and canonical location; root replacements and parent
redirection fail visibly. A cleanup filesystem error produces a failed teardown
report rather than an internal error. Existing caller bases, symlinks and overlap
with the checkout or durable records are rejected before native pytest clears
a base. Nested links are unlinked without following them. This is contributor
cleanup protection, not a security boundary against a hostile concurrent process
modifying filesystem objects between identity checks and removal.

Configuration requests `tmp_path_retention_count=1` and policy `failed`. The
plugin preserves the requested policy in its own typed stash and uses native
policy `all` for the **session container**. Otherwise pytest removes a successful
session's newest numbered root before eviction and an older failed root can
persist indefinitely. Successful **test/shared trees** still disappear during
teardown; the small numbered container advances normal retention and native
active-session locks. No independent age sweep or private pytest API is used.

`-o tmp_path_retention_policy=all` retains test trees within numbered-session
retention. `--keep-test-workspaces` also uses an exclusively created unnumbered
base outside numbered eviction, preserving successful trees across subsequent
normal sessions. An explicit `--basetemp` must be new; it is caller-selected
and does not acquire numbered-root eviction semantics. Driver `--keep-workspace`
remains a driver-level control; IP2 proves its distinction from pytest retention.
Forced termination cannot guarantee finalizers. Shared fixtures not yet migrated
to the explicit helper keep their existing lifetime until IP2.

**Compatibility limitation:** the native-container routing uses the public
`Config.inicfg` compatibility mapping, marked deprecated by installed pytest
9.1.1. No warning filter or check suppression was added. This phase verifies the
committed lock's pytest 9.1.1 / xdist 3.8.0; it does not establish every version
allowed by the dependency range or promise pytest 10 compatibility. This mapping
must be revisited before upgrading beyond the supported locked toolchain.

### Red–green evidence and corrective attempts

All focused commands start `uv run --locked pytest`; selectors below belong to
`tests/integration/test_pytest_workspaces.py`. Serial runs are small TDD slices,
not gate verification. Raw logs are under `logs/`; some early command outputs
were retained as concise execution notes rather than complete stdout captures.
Final XML records every direct case. No assertions/timeouts were weakened.

| Slice / ACs | Red command and observed missing behavior | Green verification |
|---|---|---|
| Late finalizer / AC-02/05 | `::test_success_is_removed_after_finalizer_before_completion`: 1 failed; native cleanup removed evidence before late finalizer | Same node: 1 passed, 0.31s; later full direct run includes it |
| Failure phases / AC-02/04 | `::test_failure_retains_available_tree_and_reports_owner`: 3 failed; missing absolute `WORKSPACE` diagnostics | Module at 4 cases: 4 passed, 1.26s |
| Cleanup refusal / AC-02/04 | `::test_cleanup_error_is_a_failed_teardown_with_remaining_path`: 1 failed; child internal error (exit 3), required failed teardown (exit 1) | Module at 5 cases: 5 passed, 1.55s |
| Explicit retention / AC-02/04 | `::test_explicit_retention_preserves_successful_workspace --basetemp /private/tmp/us36-ip1-cycle04`: 2 failed; missing CLI option and ignored `all` request | After None-safe CLI override correction, both retention controls passed in cycle07; final direct run renews them |
| Repeated retention / AC-02/05 | `::test_numbered_sessions_bound_failures_and_protect_explicit_retention --basetemp /private/tmp/us36-ip1-cycle06`: initially blocked by the CLI correction; cycle07 reproduced older failed tree surviving a newer successful invocation | Cycle10 selected this node and explicit-retention cases: 3 passed, 1.50s |
| Shared owners / AC-02/05 | `::test_shared_workspace_waits_for_final_consumer_and_retains_failures --basetemp /private/tmp/us36-ip1-cycle09`: 6 failed; missing public shared allocator | Module at 14 cases: 14 passed, 4.75s; module/session scopes, failed consumers and failed finalizers |
| Replacement boundaries / AC-02/04 | `::test_replaced_ownership_cannot_delete_caller_or_records --basetemp /private/tmp/us36-ip1-cycle12`: directory replacement incorrectly deleted (1 failed, 2 passed) | Explicit identity checks and stronger diagnostic assertion: module at 17 cases passed, 5.74s |
| Unsafe bases / AC-03/04 | `::test_unsafe_bases_are_rejected_before_pytest_clears_them --basetemp /private/tmp/us36-ip1-cycle14`: 3 failed; caller/record base accepted, symlink reached native setup error | Module at 20 cases: 20 passed, 6.59s |

Corrective attempt accounting (all resolved before the limit):

- Initial late-finalizer implementation attempt failed plugin import because
  `pytest.Node` is not publicly exported. Store owner node IDs instead; second
  attempt passed the original test.
- Explicit retention's first implementation failed because absent `override_ini`
  is `None`. None-safe handling passed both original explicit-retention cases.
- Repeated-retention correction 1 appended an option override after pytest had
  parsed its effective configuration; original repetition test still failed.
  Correction 2 used the public compatibility mapping before native factory
  configuration; all three repetition/retention cases passed. This introduces
  the deprecation limitation recorded above, without suppressing warnings.
- Initial lint/format checks reported one missing magic-method docstring and
  formatting only. Added the docstring/formatted the two new modules; lint,
  format and typing then passed. No unresolved correction attempt remains.

Concurrent-session, four-inner-worker, nested-child-base, nested-link and `all`
policy eviction tests were added as confirming regressions after their lifecycle
behavior was green; they passed without additional executable changes. File/report
handshakes establish ordering, with bounded polling only for readiness. No fixed
sleep duration is used as evidence of cleanup or isolation.

## Direct verification and AC mapping (IP1-T4/T5)

Changed executable inputs: `tests/conftest.py`,
`tests/pytest_workspace_support.py`, `tests/integration/test_pytest_workspaces.py`
and pytest-only settings in `pyproject.toml`. Product source, driver/helper source,
dependencies and lock are unchanged. All three new modules and configuration map
directly to the new subprocess integration module. No
`tests/verification_support.py` change requires its direct module at this gate.

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_pytest_workspaces.py --basetemp /private/tmp/us36-ip1-direct-final --junitxml=.dev-records/verification/us-36-ip1/direct.xml
```

**25 collected/selected, 0 deselected, 25 passed in 2.98s**, macOS 15.7.9 arm64,
Python 3.12.15, pytest 9.1.1, xdist 3.8.0, uv 0.13.1. The fresh explicit outer
base avoids touching historical numbered roots. Four outer workers include a
real four-inner-worker subprocess case. Earlier 23-case four-worker check passed
in 2.83s; the final check adds numbered `all` eviction and nested-link protection.

| Criterion | Direct phase evidence | Limit |
|---|---|---|
| AC-01 | Exclusive per-test/shared allocations, nested-child containment and four distinct worker roots | Actual driver adoption is IP2 |
| AC-02 | Live session observes removed success after late finalizer; setup/call/teardown failures retained; module/session final consumers; repeated/explicit retention | Shared fixtures in existing caller modules migrate in IP2 |
| AC-03 | Two synchronized sessions share isolated numbered parent; completed newer session cannot delete older active tree; four worker roots; nested child base preserves parent | Existing scheduling regression unchanged/deferred |
| AC-04 | Absolute owner diagnostics, visible cleanup refusal, caller/record/root/parent boundaries, explicit retention | Standalone real-driver flags remain unchanged; renewed installed evidence is IP2 |
| AC-05 | Parent observes teardown completion and deletion while later case is blocked; repeat/concurrent tests and baseline counts/disk records | Fixed-workload after comparison is IP2 |

Shared checks after final executable edits:

| Command | Result |
|---|---|
| `uv sync --locked --group dev` | Passed; recreated stale `.venv` linked to a missing interpreter; 193 packages installed, no lock/dependency update. Final sync: 195 resolved / 193 checked |
| `uv lock --check` | Passed, 195 resolved; initial sandbox cache denial was rerun with approval |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed, 130 files already formatted |
| `uv run --locked mypy src tests` | Passed, 42 source files |
| `uv run --locked agentic-ml --version` | Passed, `0.1.0`, matching package metadata |
| Before/after `shasum -a 256 uv.lock` | Same `90b77d41…84c0fd8` hash recorded above |
| `git diff --check` and changed-document local links | Passed; linked files and fragments checked during final record review |

Final executable SHA-256 identities are saved in
`.dev-records/verification/us-36-ip1/identities/final.txt`. The report/plan/checkpoint
were updated after executable checks; these record-only edits require document
checks, not another executable run. No commit or push was requested.

## Verification limits and gate

IP1 T1–T5 and technical checks are complete. Real caller migration,
contributor guide updates and disk comparison remain IP2. Unchanged caller
regressions/full suite remain assigned to
`M50-ACCEPT-VERIFY`; preserve the separate `M1-ACCEPT-VERIFY` obligation.
Linux/Windows are unverified by these local results. No full-suite success is
claimed; no publication, commit, IP2 progression or whole-story acceptance follows
from this evidence alone. The developer subsequently accepted the IP1 gate on
2026-11-01: “i accept ip1”; the owning plan records authorized IP2 progression.
