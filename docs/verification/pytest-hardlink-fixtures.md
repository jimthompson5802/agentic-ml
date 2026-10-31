# Scoped hardlink fixture verification

Date: 2026-10-31. Branch: `us-03-pytest-runtime-optimization`.
Base: `861b2db`. Status: candidate rolled back at developer direction.
The experiment passed 210 tests but regressed full-suite runtime. Its code and
results are preserved below; the hardlink policy is no longer active.

## Scope and approved boundaries

Developer “i approve” authorizes the proposed scoped hardlink implementation,
mutation-isolation regression, affected verification and full-suite benchmark.
This is test tooling, not US-03 IP3 or a product acceptance-criterion change.
The [import measurements](pytest-import-profile.md) motivate this work; the
[isolation benchmark](pytest-runtime-optimization.md) supplies the 208-case
baseline: 785.901s JUnit, 1047.12s terminal completion, including ~261s after
JUnit's timing boundary. No further commit/push is requested.

Approved public boundaries, reiterated before adding tests:

- Installed initialization fixture files: a native dependency must actually
  share its installed file with the cache (link count >1); no mocks or timing
  thresholds. This tests installation policy, not a guaranteed runtime.
- Real installation verifier subprocess under a hardlink-requesting parent:
  existing negative mutations must still be rejected, and copied mutable files
  must not change read-only peers or a subsequent cache-derived installation.
- Complete artifact-initialization CLI: all four fresh/existing projects across
  direct and rebuilt artifacts retain their existing checks and expose actual
  hardlinked native dependencies. Installed package integrity remains required.

Only initialization-test subprocess environments and the artifact driver's
per-project environment will request hardlinks. The mutation driver retains its
explicit copy override/private cache; no global mode, product code, dependency,
pytest scheduler, timeout, assertion or retention policy changes.

## Verification selection and sequence

1. Add one real native-file sharing regression to ordinary initialization;
   observe its failure before enabling that fixture's hardlink mode, then green.
2. Exercise existing mutation guards under a hardlink-requesting parent and
   add peer/cache isolation coverage. These protect existing correct behavior;
   no artificial defect is required to manufacture a red for that guard.
3. Extend the existing complete artifact-initialization case with native-file
   sharing assertions, observe red, then enable its per-project hardlink mode.
4. Run the complete unfiltered four-worker suite as the final green and
   regression benchmark, including the artifact case, copy-isolated negative
   tests, both wheel paths, planning and scheduling. Run all shared checks,
   compare lock/input identities, and report execution versus cleanup timing.

Focused commands use four workers/loadgroup and dedicated outer temporary
directories to keep TDD evidence separate from unrelated retention cleanup.
The final benchmark retains the baseline's ordinary outer temporary-root policy.
No checks are deferred beyond final verification. Affected behavior and all
prior assertions must pass; Linux/Windows and cross-filesystem performance are
not established by a local macOS run. Actual hardlink assertions require cache
and temporary environments on a hardlink-capable shared filesystem.

Red/green outcomes, attempt tracking, final counts, timings, identities and
limitations follow. No full-suite performance gain was achieved.

## Ordinary fixture and mutation isolation evidence

`uv run --locked pytest -n 4 --dist=loadgroup
tests/integration/test_initialization.py::test_initialization_dependencies_reuse_cached_files
-v --basetemp=/private/tmp/pytest-hardlink-fixture-red-20261031
--junitxml=/private/tmp/pytest-hardlink-fixture-red-20261031.xml`:
**one intended failure, 3.70s**. The actual installed NumPy extension had link
count 1. Enabling hardlink mode only in that module's subprocess environment
made the same regression green, **one passed, 9.92s**, with `green` artifact paths.
These focused times are not performance benchmarks; the behavior assertion is
actual file sharing, not a timing threshold. Corrective attempt 1 passed.

Mutation guard command:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installation_verification.py -k 'mutating_installed_guidance or altered_guidance or missing_template or missing_metadata' -v --basetemp=/private/tmp/pytest-hardlink-mutation-20261031 --junitxml=/private/tmp/pytest-hardlink-mutation-20261031.xml
```

**Four passed, 44.43s.** The existing installed-project fixture now explicitly
launches its copy-forcing driver with a hardlink-requesting parent. Missing
template, altered guidance and missing metadata rejection checks remain intact.
The new regression proves, while the copied guidance is actively corrupted:

- The mutation target has a single link and differs from the read-only peer.
- The normal installed verifier rejects the altered contents.
- The pre-existing hardlinked peer still contains the independently expected
  provisional guidance bytes.
- Another real full-SHA installation from cache during the corruption still
  contains those expected bytes and shares file identity with the first peer.
- The mutation target is restored in `finally`.

This is regression coverage for an already correct copy/private-cache guard;
no fault was inserted to manufacture a red. No installed shared file was
mutated. Initial format check requested one routine reformat of the new helper;
Ruff applied it. Lint and strict typing passed; all shared checks were renewed
before the final benchmark.

## Artifact red and final green launch

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py::test_complete_initialization_from_both_artifact_paths -v --basetemp=/private/tmp/pytest-hardlink-artifact-red-20261031 --junitxml=/private/tmp/pytest-hardlink-artifact-red-20261031.xml
```

**One intended failure, 240.40s (4:00).** The real driver completed all four
project setups and exited zero; the new assertion found a native file with
link count 1. Corrective attempt 1 adds a copied per-project environment with
`UV_LINK_MODE=hardlink` only within `verify_project`. The caller's environment,
normal artifact-verification driver and copy-isolated mutation driver are not
changed. The unfiltered full suite below is its green plus dependent coverage.

All shared checks passed before launch: locked dev sync (195 resolved,
193 checked), lock consistency, lint, formatting (99 files), strict types
(31 source files), version `0.1.0`, and whitespace. No check exclusions or
suppressions added. Lock SHA-256 before:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

Final command:

```sh
uv run --locked pytest -n 4 --dist=loadgroup --junitxml=/private/tmp/pytest-hardlink-full-20261031.xml --durations=30
```

Expected count: 210 (208 baseline plus two new regressions). No selection,
skips or scheduler changes. Final result: **210 passed**, zero failures/errors/
skips, exit zero. Maintained executable inputs remained frozen during the full
run; only documentation changed afterward.

The final run uses ordinary outer pytest temporary retention, as the baseline
did. The retained history differs: the prior baseline deleted a large old run,
while current roots before launch are 67, 68 and 69. Cleanup time is not a
controlled matched comparison. Assess the optimization primarily against
JUnit's test-execution/reporting timing, and report the terminal completion
time separately; do not attribute changes in old-directory deletion costs to
hardlink installation.

Raw evidence and frozen input inventory:
`/private/tmp/pytest-hardlink-evidence-20261031` (outside pytest retention).
Inventory: 53 maintained source/test/build files, SHA-256
`030729e7ba248e52ee117bb45c59e156acab94f38c7e03b73b5668cd8b442c6a`.

## Final benchmark: performance objective not achieved

| Measure | Baseline, 208 cases | Candidate, 210 cases |
|---|---:|---:|
| JUnit execution/reporting time | 785.901s / 13:06 | **1434.532s / 23:54** |
| Terminal completion time | 1047.12s / 17:27 | **1434.54s / 23:54** |
| Time after JUnit timing boundary | 261.219s / 4:21 | ~0.008s |
| Result | All passed | All passed |

Execution/reporting was **82.5% slower**; terminal completion was **37.0% slower**.
The candidate had essentially no post-JUnit delay, so old-directory cleanup
does not explain this regression. Cleanup histories differ, and these are
single local runs, not a randomized performance study. The two new regression
cases add coverage and cost, but common-case comparisons also show substantial
regressions.

Accumulated worker seconds (not elapsed wall time):

| Module | Baseline | Candidate |
|---|---:|---:|
| Initialization | 2471.036 | 4697.757 |
| Distribution | 370.714 | 606.876 |
| Installation | 102.768 | 280.792 |

Examples of the same case's total recorded time, including setup:

| Case | Baseline | Candidate |
|---|---:|---:|
| Reject storage at `init.tmp`, state store | 2.819s | **48.402s** |
| Reject storage at `init.tmp`, artifact store | 2.876s | **48.282s** |
| Reject storage at `init.tmp`, MLflow backend | 2.751s | **48.143s** |
| Reject incompatible saved schema | 69.735s | **30.961s** |
| Require importable project after sync | 54.885s | **17.120s** |

The console report shows many initialization fixture **setup** phases at
45–47 seconds. Some cases performing initialization benefited, while many
preflight rejection cases incurred much greater setup costs before reaching
their assertions. Forcing hardlinked dependency creation across the entire
module therefore failed to deliver the expected aggregate improvement.
The exact uv/filesystem/contention mechanism is not yet profiled; do not claim
that hardlinks are intrinsically slower on every system.

Complete artifact initialization passed its native-sharing assertions for all
four projects but took **399.094s**, versus **323.453s** baseline. The new
mutation isolation test passed in **71.475s**; ordinary native-sharing regression
passed in **33.703s**, and nested scheduling passed in **9.565s**. Both wheel
paths, planning and original negative checks passed. Original assertions,
timeouts and full-suite coverage remain intact.

**Decision for review:** functional safety is verified locally; performance
acceptance is not. Do not commit/adopt this broad policy as a demonstrated
runtime optimization. Next work should measure fixture creation under four
workers and consider hardlinks only for cases that perform full initialization,
retaining cheap setup for preflight-only cases. That narrower fixture contract
and another implementation/benchmark require developer direction. No second
performance correction was made during or after this run.

Performance attempt 1: scoped hardlink installation plus isolation regressions;
functional verification passed, original runtime-reduction objective failed.
Preserve this failure evidence and the current working tree for review.
The earlier isolated 30.12s-to-7.28s import result remains valid for that probe,
but it is not a full-suite performance prediction.

Final input inventory comparison: no changes across all 53 maintained files.
Lock SHA-256 unchanged:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
All shared checks passed before the benchmark. Only reports, guide and checkpoint
records changed afterward; another runtime rerun is not needed for those edits.
macOS verified; Linux/Windows, other filesystems and cache states remain unverified.

Retained evidence includes the red/green XML, mutation XML, artifact red console,
full console/XML, baseline XML, `comparison.json`, `sharing-identities.json` and
the frozen input inventory in the evidence directory above. Actual identities
record four shared artifact-project native files, a single-link mutation copy,
and two peers sharing the guidance file. Final document checks passed:
31 local Markdown link paths and `git diff --check`.

## Rollback at developer direction

Developer “do the rollback” (2026-10-31) authorizes removal of the failed
optimization while retaining this experiment's documentation. The executable
candidate is archived in [the replayable patch](experiments/pytest-hardlink-candidate.patch).
Patch SHA-256:
`d95fec06fc86bb37e628c3b81b6e7f0c72e4c5896100b52a7a7f451cbce6cb2e`.
Its empty context lines are stored without trailing whitespace; `git apply
--check` verifies that it applies to the restored baseline without changing it.

The four modified Python files were restored exactly to `861b2db`: ordinary
initialization fixtures, installation-verification tests, distribution tests,
and the artifact-initialization driver. This removes the link-mode overrides,
parent override, experimental sharing assertions, and two new experiment tests.
Original test assertions and timeouts are byte-for-byte unchanged. The committed
nested-pytest temporary-directory isolation fix remains in place.

`git diff --exit-code 861b2db -- src tests pyproject.toml uv.lock` passed.
All **53** source/test/build hashes match the earlier verified baseline inventory
at `/private/tmp/pytest-runtime-optimization-evidence-20261031/tested-inputs.json`.
That exact executable identity passed the unfiltered **208-case** four-worker
suite (785.901s JUnit / 1047.12s terminal completion). This is reused evidence,
not a new rollback runtime measurement. No new behavior was introduced requiring
a manufactured TDD red, and no fresh full-suite run is claimed.

Rollback verification:

- `uv run --locked pytest -n 4 --dist=loadgroup --collect-only -q`:
  **208 collected**, exit zero, 0.26s.
- `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_parallel_execution.py -v --basetemp=/private/tmp/pytest-hardlink-rollback-scheduling-20261031 --junitxml=/private/tmp/pytest-hardlink-rollback-scheduling-20261031.xml`:
  **one passed**, exit zero, 1.12s.
- Locked lint, format (99 files), strict types (31 source files), and version
  smoke (`0.1.0`) passed again.

All reports, raw XML/console logs, comparisons, identities and the candidate
inventory remain preserved. The previously requested fixture-creation profile
can use temporary instrumentation against this restored baseline; it does not
require reactivating the archived candidate.
