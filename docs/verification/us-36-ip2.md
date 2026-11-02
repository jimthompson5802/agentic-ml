# US-36 Implementation Phase 2 evidence

IP1 was accepted on 2026-11-01: developer “i accept ip1”, responding to the
request to approve IP1 to proceed to IP2. The owning plan records this progression;
whole-story acceptance and publication remain separate. IP2 is in progress.

Issue #49: full body refreshed, every comment page returned zero comments,
stable metadata refresh `updated_at=2026-11-02T00:58:23Z`. Initial metadata read
hit a network error; approved retry succeeded. Milestone 50, US-36-AC-01–05,
scope and approved boundaries are unchanged.

Public boundaries: existing driver subprocesses, reported absolute paths,
installed CLI/API/resource/provenance probes and independently expected files.
The approved IP1 subprocess/report boundary observes final cleanup. Existing
assertions, fixture scopes, grouping, installed isolation and timeouts stay in
force. Real driver completion, outer pytest outcome and post-test retention are
distinct. No changes to product source, dependencies or standalone drivers are
planned. All raw commands/evidence belong outside disposable trees.

Current status: T1–T6 complete; developer accepted the IP2 gate on 2026-11-01:
“i accept ip2; commit the changes”. Local commit authorized; whole-story
acceptance, push and publication remain separate and pending.
All 104 direct cases have passing evidence across the main run and one isolated
renewal. The main run's one resource-contention timeout is preserved below;
it is not presented as an all-passing run. No assertions/timeouts were changed.
T4 documentation/help and local links passed. T5 fixed replay passed six cases.
T1 slice 1: focused serial TDD command
`uv run --locked pytest tests/integration/test_distribution_verification.py::test_both_installed_wheel_paths_pass --basetemp /private/tmp/us36-ip2-red-distribution01`
failed (1 failed, 29.58s) only at the new expected containment assertion after
both genuine wheel paths passed. The driver used an independent system directory.
Added explicit fresh `tmp_path / "verification"`; same node passed (1 passed,
27.58s) using fresh base `/private/tmp/us36-ip2-green-distribution01`.
Raw owner: `.dev-records/verification/us-36-ip2/` and linked unique driver records.
Current partial T1 verification: distribution success containment red failed
as intended, then passed in 27.58s. Concurrent helper containment red failed
as intended, then passed in 0.11s. Child-record failure helper containment red
failed as intended, then passed in 0.10s. Explicit test descendants were added to
remaining distribution and lifecycle parent calls. A four-worker intermediate
selection passed **39 tests in 205.85s**; XML is `contained.xml`. Selection used
the two modified modules with
`-k 'not initialization_cleans and not parent_failure_after and not planning_retention and not planning_from'`
and fresh base `/private/tmp/us36-ip2-contained01`. This is partial evidence;
excluded direct cases remain required for the IP2 gate. No test process remains
running. Further implementation was paused while answering the developer's
approval-workflow/status questions. T2–T6 have not begun; no commit or push.
The developer then explicitly resumed IP2: “you can continue ip2”.

## Shared owners and real-driver boundaries

T2 red: `uv run --locked pytest tests/integration/test_pytest_workspaces.py -k 'existing_shared and test_distribution' --basetemp /private/tmp/us36-ip2-red-shared01`
selected one case, deselected 29; it failed only because the actual artifact
fixture directory still existed after both consumers/session exit (2.06s).
Adopted `owned_workspace` at existing module scope in distribution artifacts,
lifecycle artifacts, both source-repository fixtures and `installed_project`.
T2 green: four-worker `-k existing_shared` selected all five actual-fixture cases;
**5 passed in 33.10s**, XML `shared.xml`. Consumers and driver installation probes
were unchanged. No fixture scope broadening, scheduling or environment reuse.

T3 extends the approved subprocess boundary by importing actual test functions
and fixtures from their original files, preserving their genuine installed
probes, assertions and command timeouts. A later generated case blocks on a
parent release file while the parent checks the first test's completed teardown.
The new real-driver parent wait allows up to 600s to observe initialization's
existing 600s command; existing short-case defaults/timeouts are unchanged.
Distribution uses actual `--keep-workspace` probes to show that driver retention
does not override the outer successful-test outcome. Additional modes cover
outer failure after successful probes and explicit outer retention.

Standalone defaults are probed with all `PYTEST*` context removed, an unrelated
cwd and controlled `TMPDIR` beneath the outer test root. Deliberate missing
artifacts/local Git sources test failure diagnostics/default allocation and both
driver retention-flag settings without independent system-temp leaks. Real
successful installed-driver behavior is covered by the live cases and existing
driver modules. Standalone entrypoint/helper source remains unchanged.

Final JUnit properties export workspace/environment counts, logical bytes and
`du -sk` measurements for real-driver outcomes, repeated retention and concurrent
active/completed sessions. Measurements do not follow nested caller symlinks.
They are raw evidence, not physical-device reclamation claims.

## Fixed-input replay method (T5)

`run_fixed_workload.py` creates an isolated generated suite containing the same
six baseline test functions from current source, with their original driver
assertions/timeouts and the added containment assertion. The only workload
fixture overrides copy the **byte-identical baseline wheel and sdist** into fresh
owned artifact roots and copy the baseline Git source (including its original
commit) into a fresh owned source root. Every environment/cache is still newly
created by the real drivers. No interpreter or environment is reused.
Both artifact hashes are checked against IP1 identities before invocation;
the copied source commit is verified. Original ROOT constants point to actual
driver/probe source so independent installed checks remain genuine. Normal final
direct verification separately builds artifacts from final checkout inputs.

The read-only observer records filesystem state at public teardown-report
delivery, after contributor cleanup, and again at session exit. It stores the
owner path as a public report property and writes only from workers to avoid
controller/worker duplicate writes. The baseline observer's before/after wrapper
timing was immaterial before per-test cleanup existed; this observer measures
the required completed-report boundary explicitly. Raw records have unique run
IDs and remain outside generated roots.

Replay preparation initially included pytest's `.gitignore` metadata in the
artifact hash inventory and failed before starting any tests. Correction 1
selects exactly the wheel/sdist pair and verifies both hashes; no assertion or
timeout changed. The corrected run is
`fixed-8ced511a200a44c09f81db0cdf76c067/`. All six completed tests show zero
remaining owned test roots, including the driver-retention case. The replay
passed all six cases (493.31s including launcher). The session container has
zero files, environments, logical bytes and allocated KiB. It overlaps final
direct verification; elapsed differences are not interpreted as a speed result.

| Fixed workload measurement | IP1 baseline | IP2 replay |
|---|---:|---:|
| Successful test roots remaining at completed teardown | 6 | 0 |
| Parent driver roots remaining at session exit | 6 (2 independent) | 0 |
| Retained environments at session exit | 2 | 0 |
| Retained logical bytes, pytest base plus independent roots | 1,729,629,402 | 0 |
| Allocated KiB, same union | 1,885,844 | 0 |

The two baseline environments were explicitly driver-retained. IP2 removes them
only after their successful outer test's existing interpreter/identity assertions
complete. Their durable records/manifests remain in the checkout. Empty native
session directories are not counted as owned test or driver workspaces. No
historical baseline root or evidence was deleted. Exact artifact SHA-256 inputs
and preserved Git revision `dad09a68fbbc731ec1136759779748b95dddd34d` are recorded
in the replay summary; the wheel and sdist hashes match IP1. These are logical/
allocated observations on macOS/APFS, not a physical device-free-space guarantee.

## Final selection and deferred ownership

Final direct selection uses four workers/loadgroup and all cases in
`test_pytest_workspaces.py`, `test_distribution_verification.py`,
`test_installation_verification.py` and `test_verification_lifecycle.py`, plus
`test_initialization.py::test_installed_cli_creates_inert_project_scaffolding`
and `::test_versioned_planning_inputs_coexist_with_initialization`. The two
initialization nodes directly exercise the modified source fixture and its
installed consumer; they do not select unrelated initialization behavior.

Collection-only `uv run --locked pytest --collect-only -q -m ''` reports 393
cases. Final direct selection has 104 selected and one reserved milestone case
deselected. All 289 cases outside the direct selection are assigned to
**M50-ACCEPT-VERIFY**, including that reserved case. Exact selectors are saved in
`deferred-selectors.txt`; collection output is `logs/all-collection.log`.

| Deferred module | Cases |
|---|---:|
| CLI version | 3 |
| Distribution reserved complete-initialization case | 1 |
| Other initialization cases | 102 |
| Unchanged parallel scheduling | 1 |
| Plan approvals | 48 |
| Planning | 134 |

The full suite and platform follow-up remain milestone work. Preserve the
separate M1-ACCEPT-VERIFY obligation and historical interruption evidence; no
transfer or full-suite success is implied. Any known direct failure remains a
phase blocker, not a deferral. No `test_parallel_execution.py` change was needed.

## Final verification, measurements and corrective attempt (T6)

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_pytest_workspaces.py tests/integration/test_distribution_verification.py tests/integration/test_installation_verification.py tests/integration/test_verification_lifecycle.py tests/integration/test_initialization.py::test_installed_cli_creates_inert_project_scaffolding tests/integration/test_initialization.py::test_versioned_planning_inputs_coexist_with_initialization --basetemp /private/tmp/us36-ip2-final01 --junitxml=.dev-records/verification/us-36-ip2/final.xml
```

**Main run: 104 selected, 1 milestone case deselected; 103 passed, 1 failed in
852.01s.** The failed node was
`test_existing_shared_fixture_survives_consumers_then_is_removed[test_installation_verification-installed_project]`.
It exceeded the parent's unchanged 45s first-report wait while the independent
four-worker comparison ran concurrently. The nested installation completed later;
the failure was a missing completion event before the deadline, not an ownership
assertion. XML reports 98.296s including child finalization after that deadline.
Keep `final.xml`, `logs/final-first-failure.log` and the retained failed outer
root `/private/tmp/us36-ip2-final01/popen-gw3/test_existing_shared_fixture_s0`.

**Corrective attempt 1 — isolate verification resources:** After both expensive
runs completed, rerun the exact failing node, still with four workers/loadgroup,
unchanged source, assertions and timeouts:

```sh
uv run --locked pytest -n 4 --dist=loadgroup 'tests/integration/test_pytest_workspaces.py::test_existing_shared_fixture_survives_consumers_then_is_removed[test_installation_verification-installed_project]' --basetemp /private/tmp/us36-ip2-renew-shared01 --junitxml=.dev-records/verification/us-36-ip2/renew-shared.xml
```

**1 selected, 0 deselected, 1 passed in 23.08s.** No code correction, timeout
increase, skip, suppression or assertion change was applied. This supports
resource contention as the diagnosis; it does not establish arbitrary concurrent
performance guarantees. Run expensive verification workloads sequentially when
assessing the documented four-worker profile. The prior five-case shared check
also passed at four workers in 33.10s, and the live module's 44 cases passed in
326.34s before the overlapping run. Passing evidence for the other 103 final
cases remains valid against identical executable hashes. No single all-passing
104-case invocation is claimed; the named failed node was renewed separately.
No unresolved direct failure remains; preserve this timing limitation for review.

Final XML properties and `identities/final.json` preserve these observations:

| Scenario | At completed teardown | At session exit / later invocation |
|---|---|---|
| Each real driver succeeds (installation, distribution, initialization, planning) | 0 owned roots/environments/bytes | 0 owned roots/environments/bytes |
| Outer distribution test fails after successful driver-retention probes | 1 root, 2 environments, 1,702,934,784 logical bytes / 1,854,280 KiB | Same logical files/environments; 1,853,392 KiB |
| Explicit pytest retention of successful distribution test | 1 root, 2 environments, 1,702,942,443 logical bytes / 1,843,012 KiB | Same logical files/environments; 1,842,884 KiB |
| Controlled failed numbered invocation | 1 root, 18 bytes / 4 KiB | Evicted by next completed numbered invocation: 0 |
| Explicit retained numbered-test counterpart | 1 root, 18 bytes / 4 KiB | Still present after later numbered invocation |
| First invocation active while second completes | Active first: 1 root, 15 bytes / 4 KiB; completed second: 0 | First becomes 0 only after its own completion |

Allocated KiB can change between snapshots on APFS without logical file changes.
Small controlled repeat/concurrent projects test retention independently of ML
quality, package provenance and host free-space measurements. Parent-controlled
release signals prove timing; polling delay is not used as proof of ordering.

### Shared checks and identities

| Command | Actual result |
|---|---|
| `uv sync --locked --group dev` | Passed, 195 resolved / 193 checked |
| `uv lock --check` | Passed, 195 resolved |
| `uv run --locked ruff check .` | Passed; initial four import-order findings fixed with Ruff, no suppression |
| `uv run --locked ruff format --check .` | Passed, 131 files |
| `uv run --locked mypy src tests` | Passed, 42 source files |
| `uv run --locked agentic-ml --version` | Passed, `0.1.0` |
| `git diff --check` | Passed |
| Before/after lock SHA-256 | Unchanged: `90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8` |

Raw shared-check outputs are `logs/shared-*.log`; denied cache access was retried
with tool approval, not bypassed. CLI help exposes `--keep-test-workspaces`.
Final source identities are in `identities/final.json`, based on HEAD `6b66d45`
plus uncommitted IP1/IP2 work. Product source, driver/helper source, dependency
declarations, lock and scheduling-regression module are unchanged. Later edits
are documentation/approval records only and do not invalidate executable evidence.
Local evidence: macOS 15.7.9 arm64, Python 3.12.15, pytest 9.1.1, xdist 3.8.0,
uv 0.13.1. Linux/Windows and other allowed pytest versions are not established.
The IP1 deprecated public configuration-mapping limitation remains visible.

### Acceptance mapping and gate

| Criterion | Verified evidence |
|---|---|
| US-36-AC-01 | Explicit driver/helper descendants, actual shared-fixture owners, real four-driver tests, composed child identities |
| US-36-AC-02 | IP1 complete-outcome/failure/finalizer tests renewed in the final run; actual shared consumers; four real drivers observed after teardown before session exit; outer failure and both retention layers |
| US-36-AC-03 | Four real inner workers, synchronized concurrent numbered sessions and dedicated nested child bases; no scheduling/scope change |
| US-36-AC-04 | Standalone subprocess defaults/flags without pytest context and with unrelated cwd; absolute diagnostic/record paths; documented controls and interruption limits |
| US-36-AC-05 | Byte-identical six-case baseline replay; live completion, repeated retention and concurrency checks; exported counts/logical bytes/allocated KiB |

**Technical tasks T1–T6 and both implementation gates are complete. Explicit
whole-story acceptance remains pending.** Developer “i accept ip2; commit the
changes” authorizes committing the implementation and approval records locally.
No push, PR or publication was requested or performed. Full-suite deferrals
remain with M50-ACCEPT-VERIFY; preserve M1-ACCEPT-VERIFY independently.
Preserve IP1 baseline/records and failed-attempt history. Full-suite and unchanged
caller regressions remain owned by M50-ACCEPT-VERIFY; preserve separate M1 owner.
