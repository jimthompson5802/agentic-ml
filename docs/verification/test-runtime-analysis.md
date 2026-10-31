# macOS test runtime analysis

Date: 2026-10-31. This is the original analysis and recommendation snapshot;
no executable changes were made during that investigation. The developer later
authorized priorities 1 and 2; see [implementation evidence](pytest-runtime-optimization.md)
for subsequent changes, profiling measurements and verification status.

## Evidence and limits

Developer-supplied run:
`time uv run --locked pytest -n 4 --dist=loadgroup -v --durations=30`.
macOS, Python 3.12.15, pytest 9.1.1, xdist 3.8.0; 208 cases,
207 passed, one failed. Pytest elapsed 986.89s; shell elapsed 988.11s.
Shell CPU accounting: 383.44s user, 942.36s system, 134% CPU.
About 71% of accounted CPU time was system time. This is consistent with
substantial operating-system work; it does not by itself identify disk I/O,
cleanup, memory pressure or subprocess startup as the cause.

The supplied output is the current failure baseline. No suite was rerun during
this analysis and no corrective attempt was made. The diagnosing-bugs workflow
is limited to evidence analysis and a read-only measurement here: the developer
requested review before changes, and this is not a verified fix. There is no
fast deterministic reproduction of the intermittent shutdown timeout yet.

Retained evidence inspected:

- `/private/tmp/us03-ip2-full.xml`: previous 207-case successful run.
- System temporary root `pytest-of-jim/pytest-66`: the supplied run's fixtures,
  including nested scheduling worker records and artifact initialization logs.
- Existing cleanup evidence in [US-03 IP2](us-03-ip2.md): 90.755s test execution
  versus 242.56s process completion in an earlier selected run.
- [Parallel verification](parallel-test-execution.md): previous two/four-worker
  comparison and the reasons for preserving groups.

No equivalent Linux timing artifacts were available for comparison. Linux's
reported five-minute runtime remains developer-observed evidence. Differences
in hardware, caches, filesystem, dependencies, revision and test inventory have
not been controlled. Do not attribute the difference to macOS alone.

## Findings

### The final tail includes a nested pytest timeout

The distribution group finishes at about 30% in the supplied output. Its slow
test therefore does not account for the final tail in this run. Workers
continue completing initialization tests afterward. Near the end, one worker
starts the scheduling regression, which launches another four-worker session
and times out at 120 seconds.

All eight JSON records remain in the failed test directory. Alpha cases record
`gw0`; beta cases record `gw1`. Thus all eight generated test bodies reached
their output writes with the intended grouping. That does not establish a clean
nested pytest exit or completion of teardown and final reporting.

The nested command has no `--basetemp`. Installed pytest source confirms that
its controller consequently allocates a numbered directory in the shared
user-level pytest temporary root and registers old-directory cleanup for
session finish. The outer session generates many installed environments there.
Deleting older sessions is a strong candidate for the timeout, supported by
earlier observed cleanup delays, but no stack sample proves that this failed
subprocess was deleting directories. Plugin shutdown is another possibility.

The shell elapsed time is only about 1.2 seconds longer than pytest's reported
time. Do not add a separate several-minute post-summary cleanup estimate to
this run: cleanup or waiting may already be inside the timed nested call.

### Fresh initialization dominates repeated test work

The longest test takes 328.40s and runs a four-project matrix: fresh/existing
projects through direct-wheel and sdist-rebuilt-wheel artifact paths, sequentially.
It also runs probes and initialization reruns.

Approximate stage gaps from retained command-log modification times:

| Project | First initialization | Rerun |
|---|---:|---:|
| Direct wheel, fresh | 63.29s | 5.93s |
| Direct wheel, existing | 66.38s | 6.01s |
| Rebuilt wheel, fresh | 57.80s | 5.78s |
| Rebuilt wheel, existing | 68.54s | 6.71s |

These are differences between successive log writes, not instrumented command
timings. Surrounding Python overhead is included. Nevertheless, the first
initializations account for roughly 256 seconds of the 328-second test.
Initial harness pin installation gaps are only about 1.2–3.0 seconds here.

Numerous separate initialization cases take 60–84 seconds. The code creates an
independent project per test, synchronizes its full environment on successful
initialization, imports the scientific/notebook stack, initializes DVC and
creates an MLflow SQLite backend. Current evidence does not separate these
costs; MLflow alone has not been established as the bottleneck.

Historical XML records 2459.34 accumulated seconds in initialization tests out
of 2930.41 accumulated seconds overall: approximately 84%. Dividing that total
by four gives an idealized 732.60s versus 788.72s actual wall time. These
historical durations suggest that scheduling alone has limited headroom for
that particular run; durations themselves can change with contention. They
are not a reconstruction of the new failed run.

### Preflight traverses excluded directories

`project_identity` in `src/agentic_ml/initialization/preflight.py` uses
`root.rglob("pyproject.toml")`, then ignores matches beneath `.venv`, `.git`
and `.agentic-ml`. It still traverses those trees.

A read-only comparison on the supplied run's retained DVC-initialization
project measured 0.6005s for the existing traversal and 0.0005s for an
`os.walk` traversal pruning those three root directories. Both found only
the root project metadata outside excluded directories. This is a single
warm-filesystem measurement, not a full-suite improvement estimate or proof
of equivalent behavior for symlinks, errors and nested project boundaries.

## Recommendations for approval

| Priority | Proposed change or investigation | Expected value | Verification before claiming improvement |
|---|---|---|---|
| 1 | Give the nested scheduling subprocess a dedicated `--basetemp` child beneath its own `tmp_path`. Keep four workers, grouping assertions and the 120s timeout. | Prevent this tiny test from participating in unrelated old-session cleanup; improve isolation and potentially remove the 120s tail failure. | Reproduce/sample the original timeout if feasible; verify all eight outputs, group placement and clean exit. Compare current and isolated invocations under equivalent temp-root conditions; retain evidence. Run the unfiltered suite before declaring resolved. |
| 2 | Profile one fresh initialization and one rerun, recording elapsed time for uv lock/sync, import verification, DVC, MLflow and preflight. Compare the same revision and environment on Linux. | Identify the largest repeated cost before selecting a product or fixture optimization. | Record per-stage wall time, command exit status, platform and warm/cold cache conditions. Do not record environment contents or credentials. No reduced coverage or product shortcut. |
| 3 | Prune the three already excluded root directories before searching for nested project metadata. | Small measured saving per preflight; reduced filesystem traffic across many cases. | Public installed-interface regressions for real nested projects, excluded trees, existing symlink/error semantics and pre-write rejection. Compare equivalent traversal results and representative timings. This would be a product-code change requiring the owning issue and approved implementation scope first. |
| 4 | If profiling shows environment construction dominates, reuse only immutable dependency downloads/build artifacts while preserving independent project environments, genuine full-SHA origin and independent stores. Check existing uv reuse before adding new caches. | Potentially reduce repeated installation work without sharing mutable project state. | Verify fresh initialization, installation/upgrade, cache-removal and pin/lock identity checks unchanged. Do not copy a virtualenv or reuse initialized DVC/MLflow state across tests. Benefit is currently unmeasured. |
| 5 | Consider splitting the four artifact-matrix scenarios into separately schedulable cases only after initialization profiling and isolation work. | Shorter individual scheduling units, with possible lower wall time. | Preserve both artifact paths and fresh/existing CLI/API coverage, checksums, origin and rerun checks. Measure extra build duplication and contention; preserve safe grouping for mutable installation probes. |

Recommended initial approval scope: priorities 1 and 2. Priority 3 is a smaller
follow-up; priorities 4 and 5 depend on measured results. No runtime reduction
is promised before comparative verification.

Do not increase the timeout to hide the failure, skip the slow tests, change
globally to `worksteal`, broaden a mutable fixture's scope, disable durability
checks or increase workers without measurement. Prior four-worker measurements
were faster overall than two, despite slower individual artifact initialization.

For outer-session cleanup, a unique disposable `--basetemp` is a useful separate
comparison. It avoids shared numbered-directory retention but leaves storage
management to the runner; moving cleanup outside pytest does not eliminate its
cost. Preserve failed evidence and never reuse an active base directory.

Pytest documents both [temporary-directory retention and basetemp behavior](https://pytest.org/en/latest/how-to/tmp_path.html),
including clearing a supplied base directory. Its [plugin controls](https://pytest.org/en/stable/how-to/plugins.html)
permit a later diagnostic comparison loading only xdist in the tiny nested
session if temp isolation does not resolve the timeout. That is a separate
variable, not a proposed global plugin exclusion.

## Checks and approval status

Inspection and one read-only filesystem timing comparison only. No new test
execution, fix, dependency/lock update or disabled assertion. TDD is not
applicable to this analysis document; future executable changes need approved
test boundaries and appropriate red/green or behavior-preserving verification.
The supplied full suite has one unresolved failure. Implementation, benchmark
outcomes and Linux parity remain pending. Approval requested by the developer's
instruction to review recommendations before changes; no publication requested.
