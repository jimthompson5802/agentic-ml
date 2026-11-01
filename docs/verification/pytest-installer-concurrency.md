# uv installer concurrency profile

Date: 2026-10-31. Tested baseline: `2bb0940` on
`us-03-pytest-runtime-optimization`. Developer “go ahead” authorizes the
proposed temporary comparison and, if fixture setup consistently improves,
complete-suite validation. Permanent configuration changes remain subject to
developer review. Hardlinking remains rolled back.

## Question and boundaries

Does limiting each uv installer's threads reduce environment-creation time
while four pytest workers create independent projects? uv documents
[concurrent-installs](https://docs.astral.sh/uv/reference/settings/#concurrent-installs)
as the number of package installation/unzip threads, defaulting to available
CPU cores. This host reports 16 logical CPUs. Four concurrent installers could
compete for filesystem resources; actual thread counts and a specific kernel
contention mechanism have not been traced.

The existing [fixture profile](pytest-fixture-profile.md) supplies the real
reproduction boundary: eight existing parameterized metadata-overlap rejection
tests, with fresh independent installed projects, four workers and `loadgroup`.
They reject configuration before scientific imports and DVC/MLflow setup.
Their existing assertions and subprocess timeouts are unchanged. This measures
fixture creation, not the full successful initialization path.

No maintained Python code or configuration is changed. TDD does not apply to
temporary diagnostic instrumentation and evidence documentation. The previously
confirmed public test boundaries and installed-package isolation remain intact.

## Method and evidence

Raw scripts, per-worker events, exact commands/node IDs, logs, JUnit, input
inventory and summary JSON are retained outside the checkout at:

`/private/tmp/pytest-installer-concurrency-tvjkoiu6`

The scratch plugin is adapted from the earlier fixture profiler. During real
fixture subprocess calls it requests clone installation and either removes
`UV_CONCURRENT_INSTALLS` for the default control or sets it to 1 or 2. It records
real subprocess durations/results, child CPU time, uv's phase summaries,
project dependency versions and native-file link counts. It does not replace
subprocess results. The profiling pytest process alone receives the plugin's
scratch directory through `PYTHONPATH`; fixture subprocesses remove that path
using the existing environment isolation.

Six sequential batches use a reversed order to check repeatability and reduce
simple order/cache confounding: default, 1, 2, 2, 1, default. Each batch has
eight fresh projects and four source repositories. The shared uv cache stays
warm; no cache is cleared. Dedicated batch basetemp directories exclude
unrelated old-session retention cleanup. Counts deduplicate xdist's worker and
controller report copies by batch, node ID and phase.

Run the sequence from the repository root:

```sh
.venv/bin/python /private/tmp/pytest-installer-concurrency-tvjkoiu6/run_all.py
```

The runner invokes `run_profile.py --mode clone --installs LIMIT --label LABEL`
for each batch, which runs `uv run --locked pytest -n 4 --dist=loadgroup` with
the explicit eight node IDs, temporary plugin, JUnit and basetemp. Each
`identity.json` records its complete argv and lock/commit identity. Normal uv
cache access required execution outside the filesystem sandbox.

Platform: macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1; 16 logical CPUs and
approximately 290 GiB free storage before measurement. Parent
`UV_CONCURRENT_INSTALLS` and `UV_LINK_MODE` are unset.

## Fixture results

All **48 test invocations passed**, exit zero in all six batches. These are
eight unique cases repeated six times, not 48 different tests. All 48 project
dependency maps matched. All native-file link counts were 1, consistent with
the requested clone mode. All 53 maintained source/test/build input hashes
matched the restored, previously tested baseline.

| Batch | Installer threads | Median project fixture | Median `uv add` | Median uv installation phase | Eight-test batch wall time |
|---|---|---:|---:|---:|---:|
| Default A | Default | 15.94s | 15.88s | 13.60s | 36.48s |
| One A | 1 | 12.45s | 12.39s | 10.67s | 29.64s |
| Two A | 2 | 12.72s | 12.66s | 10.77s | 30.31s |
| Two B | 2 | 12.17s | 12.09s | 10.30s | 29.02s |
| One B | 1 | 11.98s | 11.93s | 10.20s | 28.56s |
| Default B | Default | 17.76s | 17.70s | 15.37s | 40.21s |

Pooled median project creation across 16 samples per setting: default **16.56s**,
one thread **12.05s**, two threads **12.53s**. One thread is approximately
**27% faster** than the pooled default median in this fixture workload.
Both limited settings improve both batches relative to both default controls.
The difference between one and two threads is small; this is insufficient
evidence of a universal preference for one thread.

Median child system CPU per `uv add`: default **2.83s/2.88s**, one thread
**1.70s/1.74s**, two threads **1.93s/1.80s**. User CPU remains approximately
0.42–0.44s. uv's installation phase remains the dominant cost. Resolution,
source preparation and Git setup are recorded in `comparison.json` and the
worker events; phase medians must not be added as if they were one sample.

The slow result returning in the final default batch argues against simple
monotonic cache warming as the entire explanation. The data supports reducing
installer concurrency for this workload, without identifying a particular
filesystem lock or proving whole-suite speedup.

## Complete-suite validation

Status: complete with a temporary one-thread limit, selected from the fixture
measurements. All **208 tests passed**, exit zero, with their original assertions,
grouping and timeouts. The collected case identities match the historical
208-case baseline exactly.

```sh
.venv/bin/python /private/tmp/pytest-installer-concurrency-tvjkoiu6/run_full.py --installs 1
```

The runner passes `UV_CONCURRENT_INSTALLS=1` to the full pytest process and its
children. It runs the unfiltered documented four-worker command with verbose
output, 30 durations, JUnit and a scratch progress/session-timing plugin. It
does not override fixtures or link mode: ordinary macOS installations retain
their default policy and negative installed-package probes retain their
explicit copy/private-cache isolation.

Unlike the small fixture batches, this run uses the default pytest temporary
root. Last-test teardown, controller session completion, unconfiguration and
outer process exit are timed separately to expose completion/cleanup delays.
Artifacts are under the evidence directory's `full/` subdirectory. No permanent
environment, development command, dependency, lockfile or CI setting is changed.

| Measurement | Historical default | Temporary one-thread run |
|---|---:|---:|
| Passing tests | 208 | 208 |
| JUnit session time | 785.901s (13:06) | **1229.288s (20:29)** |
| Terminal/outer completion | 1047.12s (17:27) | **1229.717s (20:30)** |
| Outer completion minus JUnit | 261.219s | **0.429s** |

The new outer duration is **3:03 longer, approximately 17% slower**, than the
historical default run. Its JUnit duration is **7:23 longer, approximately 56%
slower**. The historical comparison is not a new paired default experiment;
cache, system load and retention state differ. These numbers do not establish
that the thread limit caused the entire difference. They do establish that
this validation did not demonstrate the requested full-suite improvement.

The last test teardown reached the controller at 1229.612s, session completion
began at 1229.623s, unconfiguration ran at 1229.680s and the outer subprocess
returned about **0.101s after the last teardown**. Thus the additional time in
this run was spent before test completion, rather than in a multi-minute
post-test cleanup delay. JUnit and outer timing differ slightly in where their
clocks start; neither interval is a direct filesystem-cleanup trace.

Accumulated per-module test time, summed across workers:

| Module | Historical default | Temporary one-thread run |
|---|---:|---:|
| Initialization | 2471.036s | **3894.205s** |
| Installation verification | 102.768s | **309.227s** |
| Distribution verification | 370.714s | **498.334s** |
| Planning | 2.248s | 2.523s |
| Nested scheduling | 1.719s | 1.565s |
| CLI | 0.245s | 0.277s |

These are worker-seconds, not sequential wall time. Current public phase reports
sum to **887.60s setup**, **3818.49s test calls**, and 0.044s teardown. Successful
initialization bodies remain expensive: environment synchronization 143.70s,
project-source journal preservation 143.55s, configuration/environment preservation
137.93s and installed CLI scaffolding 136.00s. The distribution initialization
case took 386.99s. This full run recorded public phases, not the internal
import/storage stages, so it cannot assign their additional time specifically
to imports, filesystem contention or uv installation.

## Limits and review

The fixture benchmark has two batches per setting on one host with a warm cache;
samples within each batch contend with each other. Fresh project dependency
resolution is not a cross-platform reproducibility guarantee. Linux and Windows
performance remain unverified. Successful initialization imports and storage
setup may dominate the complete suite even when fixture creation improves.

The earlier default full run is **785.901s JUnit / 1047.12s terminal completion**;
see [baseline evidence](pytest-runtime-optimization.md). It was measured earlier
under different cache/system/retention state. Any comparison with it must be
identified as historical, rather than a paired full-suite benchmark.

**Recommendation: retain the existing default command and do not add a permanent
uv installer thread limit.** The small installation-only workload benefits, but
the full-suite validation does not support adopting the setting as a runtime fix.
Keep the hardlink rollback and nested-pytest directory isolation. A fresh paired
full-suite default control would be needed to determine how much of this run's
slowdown is attributable to the limit versus changing machine/cache state; it
has not been run as part of this approved comparison.

Performance attempt 1 (hardlinking) remains rolled back. Performance attempt 2
(this temporary one-thread limit) passed correctness checks but did not
establish the required full-suite reduction. No third corrective attempt or
permanent setting is applied. Further investigation awaits developer direction.

Final verification:

- All **48 fixture benchmark invocations and 208 complete-suite cases passed**.
- All 48 benchmark dependency maps matched and all 53 maintained executable/build
  input hashes remained equal to the restored baseline after the full run.
- Lock SHA-256 remains
  `90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
- `git diff --exit-code HEAD -- src tests pyproject.toml uv.lock README.md`
  passed; the only repository changes are this report and CHECKPOINTS.md.
- Local report links and `git diff --check` passed. Shared synchronization,
  lint/format/type and smoke checks were not repeated for documentation and
  temporary instrumentation with unchanged maintained executable inputs.
- Complete-suite results are in `full/analysis.json`, `full/pytest.xml` and
  `full/pytest.log`; final source/case identities are in `final-input-check.json`.

All measurement processes exited. The subsequent developer “commit” authorizes
a local report/checkpoint commit; Git history records its result. No push or
permanent configuration change is authorized.
