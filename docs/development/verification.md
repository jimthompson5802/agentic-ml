# Development verification

## Verification schedule

Tests declare every milestone whose requirements they directly verify. Incidental
use of a capability does not establish coverage. Use module markers for uniform
coverage and function or parameter markers for mixed modules. Registered markers
are `milestone_0` through `milestone_6`, `milestone_50`, `milestone_99`, and
`infrastructure` for contributor tooling without direct milestone requirements.
Collection fails with test IDs when any case lacks classification, even if a
selector would exclude it. Multiple selected associations execute a case once.

```sh
# Implementation phase gate: substitute the current milestone
uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1

# Story acceptance for any milestone, and default local selection: M1–6
uv run --locked pytest -n 4 --dist=loadgroup

# Complete suite: explicit developer command or CI
uv run --locked pytest -n 4 --dist=loadgroup -m ""
```

The default expression is `milestone_1 or milestone_2 or milestone_3 or
milestone_4 or milestone_5 or milestone_6`. A phase gate selects only its current
milestone; it does not automatically select earlier milestones. Every story
acceptance selects M1–6, including stories in M0 and M50. Other local pytest
selections and standalone artifact drivers require an explicit developer command.
Selected tests may invoke artifact drivers internally. CI keeps the complete
suite and its existing standalone artifact verification. Preserve assertions,
timeouts, xdist groups and the three documented temporary skips.

## Local parallel test execution

Agents must use four workers with `loadgroup` for local pytest verification,
including complete-suite runs and selected tests. After locked development
synchronization, use:

```sh
uv run --locked pytest -n 4 --dist=loadgroup
uv run --locked pytest -n 4 --dist=loadgroup --junitxml=/private/tmp/agentic-ml-parallel.xml --durations=20
```

For serial diagnosis or a short focused TDD cycle, use `uv run --locked pytest`
with the relevant selector and record why serial execution was selected.
Use two workers only for an explicit comparison or resource investigation.
Pytest configuration does not add worker flags automatically; local and CI test
commands explicitly select four workers with `loadgroup`.

`pytest-xdist` is a development dependency. Pytest is constrained to `>=8,<9.2`
because pytest 9.2.0 silently breaks group scheduling with pytest-xdist 3.8.0.
The public subprocess regression in `test_parallel_execution.py` verifies that
marked cases share a worker. Revisit the upper bound after an upstream-compatible
pair passes that regression and complete-suite verification.

`loadgroup` keeps the installation
tests in one worker and the distribution tests in another scheduling group;
each group runs sequentially, but a worker can run other tests afterward.
Initialization and CLI cases are ungrouped and can run individually on available
workers. Grouping does not guarantee test order. Use `loadgroup` with these
commands so shared mutable installation fixtures stay together and expensive
distribution fixtures are reused. Avoid `loadfile`/`loadscope`: they place the
entire initialization module on one worker.

Each worker creates its own module fixtures. Experiment projects, source Git
fixtures, databases, storage and artifact directories use explicitly owned pytest
temporary paths. Installation probes intentionally
mutate their group-local installed project and restore its contents. Cache-removal
checks remove only their own workspace cache. Keep those isolation properties
when adding tests. Do not point multiple runs at the same `--basetemp` directory.

A scoped hardlink experiment was rolled back after its full-suite runtime
regressed. Fixtures again use their prior installation configuration, including
the installation-verification driver's copy mode and private cache for mutation
tests. The [experiment report](../verification/pytest-hardlink-fixtures.md) preserves
the measurements and a replayable candidate patch; its hardlink policy is not
active.

Environment installation and MLflow initialization compete for CPU, memory and
disk. Investigate resource constraints with a recorded worker-count comparison. Keep
existing assertions and subprocess timeouts intact. Record worker count, suite
count, durations, diagnostics and platform with results. A parallel run with `-m ""` exercises the full suite; broader local runs require an explicit developer command. Retain serial execution for diagnosis. Parallel macOS evidence
does not establish Linux or Windows support. The Linux CI workflow now requests
four workers; hosted parallel verification remains pending until a run is observed.

The initial verified macOS benchmark passed 129 tests in 16m59s with two workers
and 12m06s with four. Four workers reduced elapsed time by about 29%, while some
individual tests took longer under contention. These measurements are not a
Linux performance claim. See [parallel verification](../verification/parallel-test-execution.md)
for grouping checks, compatibility findings, commands and retained evidence.


## Pytest workspace ownership and retention

Repository `tests/conftest.py` loads contributor workspace support. Tests that
request `tmp_path` receive an exclusive root. Pass a fresh child to verification
drivers, for example `--workspace str(tmp_path / "verification")`; let the driver
create that child. Composed drivers pass fresh descendants to their children.
Standalone default allocation is tested with a controlled `TMPDIR` beneath the
owning test root, an unrelated cwd and pytest context removed.

By default, a successful test's entire owned tree is removed after every fixture
finalizer has finished, before its completed teardown report is delivered. This
includes nested workspaces and driver-retained environments. Setup, call and
teardown failures preserve available diagnostics and report
`WORKSPACE <absolute-path>`. A cleanup error fails teardown and reports the
remaining path. Original test failures remain visible.

Shared fixtures use `owned_workspace(request, tmp_path_factory, name)` from
`pytest_workspace_support` at their existing scope. Their paths remain available
until the last consumer and fixture finalizer finish. Failed consumers or shared
finalizers retain the available tree. A direct `tmp_path_factory.mktemp` allocation
does not register this ownership; use the helper for maintained shared fixtures.
Keep existing fixture scopes, mutable-probe restoration and scheduling groups.

Default numbered-session retention is one completed invocation:
`tmp_path_retention_count = 1`, requested policy `failed`. A failed tree survives
its invocation and is eligible for eviction when the next numbered invocation
completes. Native pytest session locks protect active invocations. Empty session
containers may remain to advance numbered retention even though successful test
trees are already gone. The support routes native container retention separately
from test-tree retention; effective native configuration can therefore show `all`.
Its public `Config.inicfg` compatibility mapping is deprecated in locked pytest
9.1.1; revisit that routing before a toolchain upgrade. The
[US-36 IP1 report](../verification/us-36-ip1.md) records the reason and limits.

| Retention control | Effect |
|---|---|
| No override | Remove successful test/shared trees during teardown; retain failures for one numbered invocation |
| `-o tmp_path_retention_policy=all` | Retain successful trees within ordinary numbered-session retention |
| `--keep-test-workspaces` | Retain test/shared trees; without an explicit base, use a unique unnumbered root outside later numbered-session eviction |
| Driver `--keep-workspace` | Retain driver environments for remaining test consumers; outer pytest cleanup still applies |

To inspect successful pytest workspaces, run, for example:

```sh
uv run --locked pytest -n 4 --dist=loadgroup -m milestone_0 --keep-test-workspaces tests/integration/test_distribution_verification.py
```

An explicit `--basetemp` must name a new, exclusively owned directory. Existing
bases, symlinks and overlap with the harness checkout or durable records are
rejected before pytest clears files. Explicit bases do not have numbered-session
eviction semantics. Retained explicit bases and `--keep-test-workspaces` roots
need deliberate contributor cleanup; subsequent invocations must use new paths.

Use a dedicated child base for nested pytest, such as
`tmp_path / "nested-pytest"`. Never supply an active parent's or sibling's base.
Workers, independent sessions and nested runs must not share workspace roots.
Interrupted runs may leave incomplete trees and records; forced termination cannot
guarantee fixture finalizers or cleanup. Preserve available diagnostics when
investigating them. These lifecycle rules do not change standalone driver
cleanup, which preserves source/project files after removing owned environments.

Raw verification records belong in checkout `.dev-records/verification/`, outside
disposable pytest paths. Never use that directory as a temporary base. Follow the
[records policy](records.md) for lifetime retention and backups.

## Phase and story verification

This policy governs local verification, including unfinished work in approved plans.
Record revisions to those plans through [manage-plan-scope](../../.agents/skills/manage-plan-scope/SKILL.md).
Preserve completed evidence and approvals. CI continues running all tests.

### Implementation phase gates

Use TDD for new behavior and bug fixes, with focused public-interface checks for
red–green cycles. At each executable phase gate, run the entire current milestone
using `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_N` (substitute N).
Focused checks do not replace that selection. Preserve developer approval gates.

Record changed modules, confirmed public boundaries, applicable acceptance
criteria, exact commands, collected/selected/deselected counts, outcomes and
platform. Preserve assertions, timeouts and known failures. Identify excluded
coverage and its owning task; excluded tests and skips do not prove acceptance.
Documentation-only phases use document/link/whitespace checks with a rationale.

Retain locked synchronization, lock consistency, lint, formatting, strict typing,
CLI version smoke and `git diff --check`. Record the lock hash before and after.

### Story acceptance

For every milestone, run `uv run --locked pytest -n 4 --dist=loadgroup` against
final story changes: M1–6 only. Renew that evidence after executable changes.
Reconcile acceptance criteria, excluded coverage, temporary skips and unresolved
failures. Retain shared checks and explicit developer story acceptance. Broader
pytest runs and standalone artifact checks require the developer's explicit
command; they are not automatic acceptance requirements. Documentation-only
stories use appropriate document checks with a rationale.

### Milestone acceptance

Keep a named milestone verification owner to reconcile historical deferrals,
known failures, evidence identities, counts and platform/manual limitations.
Milestone acceptance does not automatically trigger a local full suite or
standalone artifact drivers. Broader verification requires the developer's
explicit command. Preserve historical approvals and evidence without treating
excluded coverage or CI results as proof of a local check.

## Scheduling policy revision — 2026-11-04

The developer's supplied “Stratify tests by milestone” plan explicitly authorizes
this replacement of phase/story scheduling and revision of unfinished M1/M50
verification obligations. Owning plans record the scope changes. Historical
results, approvals, unresolved failures and the three temporary skips remain.
