# First-use import profiling

Date: 2026-10-31. Branch: `us-03-pytest-runtime-optimization`.
Committed baseline: `861b2db` (`test: isolate nested pytest temporary directories`).

Developer “first lets commit current changes. Then run the recommended profile
imports” authorized the commit followed by this diagnostic investigation.
The prior isolation change, analysis, evidence and checkpoint were committed
first. No push, further maintained executable change or US-03 IP3 work followed.

Subsequent [full-suite hardlink verification](pytest-hardlink-fixtures.md)
passed all 210 functional cases but regressed execution/reporting from 13:06
to 23:54. The isolated import savings below did not predict aggregate suite
performance; the broad fixture policy is not recommended for adoption.
The developer subsequently requested rollback; the executable candidate has
been removed while its report and replayable patch remain available there.

## Method and boundaries

Five separate fresh experiment environments were created using genuine
full-SHA local Git installations of the current harness. Each ran the installed
public initialization API through its own Python with `-I`. When initialization
reached its import-verification subprocess, temporary instrumentation measured
each original import, in the original order:

`numpy`, `pandas`, `sklearn`, `nbclient`, `ipykernel`, `nbformat`, `dvc`, `mlflow`,
and the generated experiment package.

The same command then ran in a second Python process **before** initialization
continued to DVC or MLflow setup. Consequently, later setup could not warm the
second probe. Import failures remained failures; all nine imports were required.
Per-package timings are incremental in this order, not independent cold imports:
earlier packages may load dependencies used by later ones.

Experiments ran sequentially, without a concurrent pytest suite:

1. Default installation, normal imports, two consecutive processes.
2. Another fresh default installation, both probes using `-B`.
3. Another fresh default installation, both probes using `-X importtime`.
4. Fresh hardlinked installation, normal imports, two processes.
5. A second fresh hardlinked installation reusing the same package cache,
   normal imports, two processes.

`-B` prevents bytecode writes but does not prohibit reading existing bytecode.
`-X importtime` reports self and cumulative import timing. See the
[Python 3.12 command-line reference](https://docs.python.org/3.12/using/cmdline.html).
The timing loop itself adds only `time` to the original probe's standard-library
imports. Trace output introduces additional measurement overhead; it is a
separate comparison rather than the default timing baseline.

The temporary hardlink driver set `UV_LINK_MODE=hardlink` only in its own process
and descendants, beginning before dependency installation. Repository/user
configuration and the ordinary pytest command were not changed. uv documents
this [installation setting](https://docs.astral.sh/uv/reference/settings/#link-mode).
The original tool environment had no `UV_LINK_MODE` override.

Source/resource/build-file comparisons against the checkout matched for all
five fixtures. Resolved dependency versions matched across all five projects:
NumPy 2.5.4, pandas 3.1.0, SciPy 1.18.1, scikit-learn 1.9.1,
MLflow 3.17.2 and PyArrow 25.0.1. These experiment resolutions are distinct
from the harness development lockfile, which remained unchanged.

Platform: local macOS arm64, Python 3.12.15, uv 0.13.1. The package-download
cache was reused. No operating-system cache reset was attempted; “fresh” means
a newly installed environment, not a cold machine. No security settings changed.

## Results

| Installation / probe mode | First process | Second process | New bytecode files in first probe |
|---|---:|---:|---:|
| Default | **30.12s** | **4.23s** | 2,018 |
| Default, bytecode writing disabled | **27.54s** | **2.97s** | 0 |
| Default, import trace | **29.09s** | **4.12s** | 2,018 |
| First hardlinked installation | **28.46s** | **4.29s** | 2,018 |
| Recreated hardlinked installation | **7.28s** | **4.49s** | 2,018 |

Every probe exited zero and completed all nine imports. Every instrumented
initialization then finished with no pending setup. The parent API duration
includes the extra diagnostic probe and bytecode inventories; it is not an
ordinary initialization benchmark.

Default-mode breakdown:

| Package | First process | Second process |
|---|---:|---:|
| NumPy | 0.76s | 0.12s |
| pandas | **10.63s** | **0.70s** |
| scikit-learn, including newly loaded dependencies | **12.82s** | **1.41s** |
| nbclient | 1.22s | 0.29s |
| ipykernel | 0.006s | 0.003s |
| nbformat | <0.001s | <0.001s |
| DVC | 0.06s | 0.02s |
| MLflow | 4.47s | 1.55s |
| Experiment package | <0.001s | <0.001s |

pandas and scikit-learn account for about 78% of the default first-probe wall
time. Total accounted child CPU time was only 5.76s during the 30.12s first
probe, versus 1.69s during the 4.23s second probe. Much of the first-probe wall
time is therefore outside that child's accounted CPU execution; this alone
does not identify the waiting mechanism.

The trace identified 160 imported modules corresponding to installed `.so`
files. Their summed **self** times dropped from **18.14s to 0.37s** between
processes. This avoids summing overlapping cumulative times. The largest
individual first-use native self time was `pyarrow.lib` at 1.88s; many pandas,
SciPy, scikit-learn and other extensions contributed smaller repeated costs.
These self times include extension loading/initialization, not solely disk reads
or a direct measurement of security scanning.

Native-file identity checks found all **323** `.so` files in the two hardlinked
environments shared device and inode, despite separate project environments.
Default installations had distinct native-file identities. The recreated
hardlink environment's first probe was about **76% faster** than the default
first probe in this sample, while still creating the same number of bytecode
files. The first hardlink environment did not avoid the initial native-file
first-use cost.

## Interpretation and next recommendation

Bytecode creation occurs, but it does not explain most of the first-use delay:
the no-write probe remained slow, then became fast in another process without
creating additional bytecode. Native-extension first-use costs are the larger
observed component, and reusing native-file identities substantially reduced
them in a new environment.

An [upstream uv report](https://github.com/astral-sh/uv/issues/18577) describes
macOS security scanning cached by file identity, with cloned installations
incurring repeated native-library assessments and hardlinks permitting reuse.
Our timings and inode comparisons are consistent with that explanation.
**Local `syspolicyd` activity was not traced**, so attribution to that specific
service remains an inference, not directly verified causality. Bytecode,
filesystem and native-loader caches may contribute additional differences.

The next proposed optimization is a **scoped test-fixture experiment using
hardlinked installations for read-only initialization dependencies**, followed
by affected checks and a complete four-worker benchmark. Retain independent
project environments, stores and genuine Git origin. Do not globally enable
hardlinks without reviewing the mutation boundary: for example,
`test_altered_guidance_is_rejected` in
`tests/integration/test_installation_verification.py` writes an installed package
resource in place. With shared hardlinks that write could affect cache contents
and other environments. Those mutation probes need isolated file copies or
clone installations. This investigation did not change their installation mode.

This is a candidate optimization with local evidence, not a measured full-suite
speedup. Five paired measurements are not a statistical performance study.
Linux parity, cold package-cache behavior, cache replacement, mutation isolation
and four-worker contention remain unverified for the proposed change. Outer
pytest retention cleanup remains separate and unchanged.

## Reproduction and retained artifacts

Temporary diagnostic commands, executed after commit `861b2db`:

```sh
.venv/bin/python /private/tmp/pytest-import-profile-20261031.py --checkout /Users/jim/Desktop/genai/agentic-ml
.venv/bin/python /private/tmp/pytest-import-hardlink-profile-20261031.py
```

Both drivers exited zero. Normal uv cache/local initialization access required
execution outside the filesystem sandbox; no new sandbox-denied attempt occurred
in this investigation.

Evidence: `/private/tmp/pytest-import-profile-evidence-20261031` contains both
drivers, their preparation helper, per-environment identities, ten per-probe
JSON files, stderr/import traces, final initialization summaries and an aggregate
`summary.json` with dependency/source comparisons and native-file identities.
`/private/tmp/pytest-import-profile-workspaces-20261031.json` and
`/private/tmp/pytest-import-hardlink-workspaces-20261031.json` identify the five
retained full experiment projects. Artifacts are outside numbered pytest cleanup.

Only this report and checkpoint records changed after the verified tooling
commit. TDD and another full pytest run are inapplicable to documentation and
temporary diagnostic measurements; no maintained executable behavior changed.
Document checks passed: 11 local link paths, `git diff --check`, identical
dependency version maps across all five fixtures, and an empty diff for
`src`, `tests`, `pyproject.toml` and `uv.lock` against the committed baseline.
The prior complete suite result remains **208 passed**
for the committed isolation implementation, not for a proposed hardlink change.
