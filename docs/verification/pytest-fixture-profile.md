# Fixture creation profile

Date: 2026-10-31. Baseline: `4207086`, with the hardlink candidate rolled back.
Developer “do the profile” authorizes measurement, not another implementation.
Status: paired measurements complete; all 32 valid profiling runs passed.
Repository executable code/configuration remains unchanged.

## Method

A temporary pytest plugin wraps real `subprocess.run` calls only while the
existing `project`, `source_repository` and `tmp_path` fixtures are being created.
It records wall/child CPU time, command exit status, uv's own phase summaries,
fixture duration and public pytest phase reports. It changes only the clone/
hardlink mode passed to fixture uv subprocesses for each comparison; it does
not substitute subprocess results or alter assertions.

Each batch runs the same eight existing parameterized metadata-overlap rejection
cases with `-n 4 --dist=loadgroup`. They create independent projects and exercise
the normal installed CLI but reject configuration before scientific imports,
DVC/MLflow setup or execution. Thus the profile measures environment creation
separately from the earlier import costs. This is eight unique tests repeated
four times, not a full-suite run or a runtime improvement claim.

Batch order is clone, hardlink, hardlink, clone to reduce simple warm-cache/order
confounding. Each batch has eight fresh projects and four per-worker source
repositories. The normal shared uv package cache is reused; no cache is cleared.
Native-file link counts verify the requested installation mode. Dependency
versions are recorded for comparison. Dedicated temporary roots avoid unrelated
pytest retention cleanup.

Temporary plugin and runner:
`/private/tmp/pytest-fixture-profile-1262ov7g/fixture_profile.py` and
`/private/tmp/pytest-fixture-profile-1262ov7g/run_profile.py`.
The scratch directory alone is added to the profiling pytest process's
`PYTHONPATH` to load the explicit plugin. The real fixture already removes
`PYTHONPATH` before launching experiment subprocesses, preserving the installed
package boundary. The plugin is not installed or added to repository config.

Raw artifacts live beneath `/private/tmp/pytest-fixture-profile-1262ov7g`:
per-batch identity/command JSON, worker events, pytest console logs, JUnit and
stage summaries. The runner records commit, platform, lock identity and exact
node IDs. Tests retain their existing assertions and 180-second command timeout.

## Instrumentation correction

Initial `clone-a` was rejected: the temporary plugin accessed `request.module`
for a session-scoped fixture before checking its name. Eight setup errors,
zero project samples; this was an instrumentation error, not a product failure
or a performance sample. The hypothesis was confirmed by
`AttributeError: module not available in session-scoped context`.

Instrumentation attempt 1 moved the fixture-name filter before module access.
The same eight cases then passed as `clone-a-valid`; no repository code or
test assertion changed. Original failed logs/XML remain preserved and excluded
from timing statistics. No further instrumentation correction was made.

xdist forwards reports to the controller, so raw report events include both
worker and controller copies. Live counts and final outcome statistics are
deduplicated by batch, node ID and phase; fixture/command events are worker-only.

## Measurements

This is macOS arm64 / Python 3.12.15 / uv 0.13.1 evidence, with 16 logical CPUs.
No Linux or Windows comparison is implied. About 291 GiB disk space was free
during the comparison, so the filesystem was not nearly full.

Commands, in order:

```sh
.venv/bin/python /private/tmp/pytest-fixture-profile-1262ov7g/run_profile.py --mode clone --label clone-a-valid
.venv/bin/python /private/tmp/pytest-fixture-profile-1262ov7g/run_profile.py --mode hardlink --label hardlink-a
.venv/bin/python /private/tmp/pytest-fixture-profile-1262ov7g/run_profile.py --mode hardlink --label hardlink-b
.venv/bin/python /private/tmp/pytest-fixture-profile-1262ov7g/run_profile.py --mode clone --label clone-b
```

Each runner launches `uv run --locked pytest -n 4 --dist=loadgroup -p
fixture_profile` with its eight exact node IDs, dedicated basetemp, JUnit and
duration output. Exact argv/node IDs are in each batch's `identity.json`.
Normal uv cache access required execution outside the filesystem sandbox.

| Batch | Median project fixture | Median `uv add` | Median `uv init` | Eight-test batch wall time |
|---|---:|---:|---:|---:|
| Clone A | **16.60s** | 16.15s | 0.030s | 38.74s |
| Hardlink A | **44.82s** | 44.76s | 0.026s | 92.78s |
| Hardlink B | **45.10s** | 45.04s | 0.026s | 93.06s |
| Clone B | **15.51s** | 15.46s | 0.027s | 35.65s |

All four batches: eight passed, exit zero, four workers. Native-file link counts
were 1 for every clone project and greater than 1 for every hardlink project,
confirming the actual modes rather than trusting the requested environment flag.
Resolved dependency version maps matched across all **32** projects.

Git setup is small: combined source and project `git init` command medians
were 0.030–0.040s; source preparation's `git add`, commit and revision commands
were each approximately 0.02–0.10s. These command samples include module source
fixtures, while the project-fixture timing is only the per-test fixture.
`uv add` dominates the per-test creation cost.

uv's own reported phase medians:

| Batch | Resolution | Preparation/build | Installation |
|---|---:|---:|---:|
| Clone A | 0.229s | 0.804s | **14.12s** |
| Hardlink A | 0.111s | 0.772s | **43.41s** |
| Hardlink B | 0.119s | 1.085s | **43.25s** |
| Clone B | 0.102s | 2.929s | **13.07s** |

Every installation reports 182 packages; resolution reports 185. Resolution
and installation timings are available for all eight commands in each batch.
Preparation is reported only for the four first-wave commands in each batch,
so its median is over four observations. Independent phase medians should not
be summed to reconstruct a command's median wall time.

Median child CPU seconds for each `uv add` call:

| Batch | User CPU | System/kernel CPU |
|---|---:|---:|
| Clone A | 0.44s | **3.06s** |
| Hardlink A | 0.53s | **130.92s** |
| Hardlink B | 0.55s | **133.72s** |
| Clone B | 0.43s | **2.87s** |

CPU time sums execution across the child process's threads and waited-for
children, so it can exceed elapsed wall time. It is not an additional 131s
of waiting after a 45s command. The system-time increase is strong evidence
of expensive kernel work during hardlinked package installation, rather than
Python test assertions or the resolver consuming the extra time.

## Findings and recommendation

1. **The slow fixture phase is package installation inside `uv add`.** Git,
   project skeleton creation, resolution and source preparation are much smaller.
   A faster resolver or reusing the small source Git fixture would not address
   the dominant measured cost.
2. **Four-worker hardlink creation reproduces the 45–47s setup regression.**
   Median project setup is roughly 2.7–2.9 times the paired clone median.
   The repeated ABBA comparison supports the rollback; this is not inferred
   from the earlier whole-suite run alone.
3. **Import savings and setup costs are different.** These cases never reach
   scientific import verification. They pay the more expensive hardlinked
   installation without receiving the first-import saving. That explains why
   the isolated import result was insufficient to justify the broad policy.
4. **The precise kernel/filesystem contention mechanism remains unmeasured.**
   The data locates the cost and shows much greater system CPU. It does not
   identify a particular APFS lock or syscall as the verified cause.

Keep the restored installation policy. The next bounded diagnostic would retain
clone mode and four pytest workers while comparing uv installer thread limits
such as `UV_CONCURRENT_INSTALLS=1` and `2` against the default. uv documents
[installer thread control](https://docs.astral.sh/uv/configuration/environment/#uv_concurrent_installs)
and a [CPU-count-based default](https://docs.astral.sh/uv/reference/settings/#concurrent-installs).
Four outer workers each invoke a multithreaded installer, so nested parallelism
is a testable hypothesis. Actual installer thread counts and gains from limiting
them have **not** been measured. No thread limit, link-mode policy or runtime
optimization was applied to repository code or configuration.

## Limits and final verification

There are two batches per mode on one host, with warm shared package caches;
the samples within a batch contend with each other. This is not a broad
statistical or platform performance guarantee. Clone setup here was 15–17s,
not the historical 2–3s recorded for some earlier full-suite cases. Cache/system
state differs; do not project these absolute timings directly onto that suite.

The profile covers fixture creation for rejection tests. It excludes successful
initialization bodies, scientific import verification, DVC/MLflow setup and
old-session cleanup. It does not establish a new complete-suite runtime.

Final checks:

- All **32 valid test invocations passed**; original assertions/timeouts intact.
- All **32 dependency version maps matched**.
- All **53 maintained source/test/build hashes matched** the restored baseline.
- `git diff --exit-code HEAD -- src tests pyproject.toml uv.lock README.md`
  passed. Parent `UV_LINK_MODE` and `UV_CONCURRENT_INSTALLS` remained unset.
- Aggregate data is saved at
  `/private/tmp/pytest-fixture-profile-1262ov7g/comparison.json`; initial invalid
  instrumentation logs and all four valid batches remain in that same debug root.

Only this report and CHECKPOINTS.md changed. TDD and a new full-suite run are
inapplicable to documentation and temporary measurement with no maintained
executable change. No further performance correction, commit or push was made.
