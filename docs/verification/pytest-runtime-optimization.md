# Pytest runtime optimization: nested isolation and initialization profiling

Date: 2026-10-31. Branch: `us-03-pytest-runtime-optimization`.
Base: `ca4eb98fe6f130eaab4356a7330fd3757670ebe9`.
Status: approved priorities 1 and 2 implemented and verified; ready for review.
Changes are uncommitted; no later optimization or publication authorized.

## Authorized scope and verification boundary

Developer “implement 1 and 2 as recommended” authorizes priorities 1 and 2
of the [runtime analysis](test-runtime-analysis.md): isolate nested pytest and
measure initialization. This is test-tooling work, not US-03 IP3 or a change to
an acceptance criterion. No user-story implementation or plan scope was added.
Priorities 3–5, product optimizations, dependency changes and publication are
outside this authorization.

The existing public pytest subprocess boundary is retained. Generated test
cases use the public `tmp_path_factory.getbasetemp()` fixture interface to
record their actual worker temporary directories; the parent regression asserts
they descend from its dedicated base directory. All eight case outputs, same-worker
grouping, distinct group workers, four nested workers, clean process exit and
the original 120-second timeout remain required. This extends the approved
recommendation's directory-isolation check at the same existing public boundary.
It does not reproduce or assert the historical intermittent timeout itself.

Final verification selects the complete unfiltered four-worker suite, including
installed initialization and both distribution paths, plus all shared checks.
The change affects the nested scheduling regression; full execution checks
its operation alongside the actual expensive suite. No further unrelated checks
are deferred. The profile is a measurement, not an executable product change.

## Red and green

Added worker-base output and the containment assertion before changing the
nested command:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_parallel_execution.py -v --basetemp=/private/tmp/pytest-runtime-red-20261031 --junitxml=/private/tmp/pytest-runtime-red-20261031.xml
```

**Red:** one failure in 1.04s. Nested test bodies and grouping checks completed,
but worker base was under the shared system `pytest-of-jim/pytest-68` root,
outside the expected `nested-pytest` child. This is the intended isolation
failure, not a setup error or a reproduction of the original 120-second stall.

Corrective attempt 1 adds `--basetemp` and `tmp_path / "nested-pytest"` to the
nested subprocess command. The unique outer test directory owns this child;
no unrelated or active session directory is passed for pytest to clear.

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_parallel_execution.py -v --basetemp=/private/tmp/pytest-runtime-green-20261031 --junitxml=/private/tmp/pytest-runtime-green-20261031.xml
```

**Green:** one passed in 1.05s; clean subprocess exit, grouping and isolation
checks passed. No failed corrective attempt, timeout increase, suppression,
skipped test or weakened assertion. This establishes isolation, not an estimated
120-second saving: the intermittent stall did not occur in the focused red.

## Initialization stage measurements

Temporary script: `/private/tmp/pytest-runtime-profile-20261031.py`.
Successful workspace: `/private/tmp/pytest-runtime-profile-txp24d9c`.
The script creates an independent committed source fixture and a separate
experiment project, installs the genuine full-SHA Git dependency, and invokes
the installed public `initialize_project` API through the project's Python
with `-I`. Fixture SHA: `74a2da82bc7210b83e3613128572624d877d65cc`.
Source/resource/build inputs compared with the checkout: no differences
(generated `__pycache__` files are not source identity).

Timing uses `perf_counter` around otherwise unchanged real `subprocess.run`
calls and cProfile around public initialization. It preserves commands, results
and exceptions; no internal collaborator is substituted. Only stage labels,
elapsed times and exit codes are exported, not environment values or captured
command output. The temporary monkeypatch is measurement instrumentation,
not a regression-test seam or an installed product modification.

Preparation and measurement command:

```sh
.venv/bin/python /private/tmp/pytest-runtime-profile-20261031.py --prepare /Users/jim/Desktop/genai/agentic-ml --measure
```

This launches fresh initialization and its rerun in separate installed Python
processes. They ran sequentially before the complete pytest run. Dependencies
were available in the normal uv cache; no cache was cleared and no telemetry
setting was changed for this comparison. This is one local pair, not a
controlled cold-cache benchmark or performance threshold.

| Measured stage | Fresh | Rerun |
|---|---:|---:|
| Entire instrumented API invocation, including initial API import | 42.93s | 7.51s |
| Preflight project identity, cumulative, including Git below | 0.38s | 0.50s |
| Preflight Git subprocess | 0.02s | 0.02s |
| uv lock | 0.16s | 0.02s |
| uv sync | 0.54s | 0.05s |
| uv lock --check | 0.01s | 0.02s |
| Environment import verification | **30.32s** | **2.16s** |
| DVC commands, summed | 3.91s | 0.40s |
| MLflow existing-store check | Not invoked | 2.51s |
| MLflow setup | 6.73s | 1.49s |

Preflight cumulative timing overlaps its Git row; do not sum all table rows.
cProfile reports 41.69s of the fresh 42.93s inside subprocess calls and 6.67s
of the rerun 7.51s. It confirms where the parent waits, not the internal child
process costs. All measured subprocesses exited zero, and both public results
reported no pending setup.

**Finding:** first-use scientific/notebook/storage import verification accounts
for about 71% of fresh initialization in this sample. Its cost drops sharply
on rerun. Dependency resolution/synchronization is not the dominant cost here;
MLflow setup is a smaller distinct cost. Profile individual first-use imports
before choosing additional optimizations. Bytecode compilation, native-library
loading and filesystem effects remain candidates, not established causes.
Do not bypass the required importability checks or reuse mutable initialized
stores. Linux stage comparison remains unverified; no Linux execution
environment was used and no CI/workflow change or publication was authorized.

Two initial sandbox-denied preparations/measurements are infrastructure
failures, not behavior reds: uv could not create its cache lock
(`Operation not permitted`, exit 2). The partly initialized workspace
`/private/tmp/pytest-runtime-profile-itvq_bxt` retains its original failure
JSON/pstats. The successful pair used a newly prepared pristine project after
escalation, rather than treating recovery of that partial project as fresh init.

## Complete verification and retained evidence

Final full run:

```sh
uv run --locked pytest -n 4 --dist=loadgroup --junitxml=/private/tmp/pytest-runtime-optimization-full-20261031.xml --durations=30
```

This uses the ordinary outer temporary-root behavior; only the nested pytest
command changed. **208 passed**, zero failures/errors/skips, exit zero.
Terminal summary: **1047.12s (17:27)**. JUnit reports **785.901s (13:06)**;
the **261.219s (4:21)** difference is after JUnit's timing boundary during
session completion. All 208 pass results were observed before process exit.
A renamed `garbage-*` directory was observed in the default pytest temp root
during this wait, consistent with the installed pytest numbered-directory
retention cleanup implementation. No cleanup process was cancelled.

The nested scheduling regression passed in **1.719s** within the full suite.
Both installed wheel paths passed (16.209s), complete artifact initialization
passed (323.453s), and both-artifact planning passed (9.935s). This passing
full run establishes the current test-tooling change alongside those installed
checks; it does not establish permanent elimination of intermittent timeouts.

There is no demonstrated overall wall-time improvement against the supplied
failed run: this command took longer, with a large outer-session cleanup cost.
Recommendation 1 isolates the nested subprocess; it does not change the outer
runner's default retention behavior. Original and renewed runs are not a
controlled performance comparison. Remaining targets are first-use imports
and outer-session temporary-storage lifecycle. Further changes need review.

Shared checks passed:

- `uv sync --locked --group dev`: 195 resolved, 193 checked.
- `uv lock --check`: passed, 195 resolved.
- `uv run --locked ruff check .`: all checks passed.
- `uv run --locked ruff format --check .`: 96 files formatted.
- `uv run --locked mypy src tests`: passed, 31 source files.
- `uv run --locked agentic-ml --version`: `0.1.0`.

Sync and lock-check sandbox cache denials were rerun successfully with
escalation. No development dependencies changed. Lock SHA-256 before and after:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
All 53 inventoried maintained source/test/build inputs remained unchanged
during the full run. `git diff --check` and 14 relative Markdown link-path
checks passed (path existence, not a new comprehensive anchor check).

Durable local evidence directory:
`/private/tmp/pytest-runtime-optimization-evidence-20261031` contains copied
original eight worker records and 33 original timestamped initialization logs,
red/green and full-suite XML, final console summary, profiling script,
fresh/rerun JSON and pstats, fixture identity and tested-input inventory.
These are outside numbered pytest retention.
The inventory covers 53 maintained source/test/build files, SHA-256
`51f0f015f25c5e0e049764a073dc4dcc5bf10769febd241bb554fc0a2a55fdaa`.
Only documentation and checkpoint records changed after verification.
