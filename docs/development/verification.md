# Development verification

## Local milestone acceptance selection

Normal local pytest runs exclude the single `milestone_acceptance` test,
`test_complete_initialization_from_both_artifact_paths`. Run it at final milestone
acceptance. CI overrides the default selection and runs every test on each run.

```sh
# Final milestone acceptance: every test
uv run --locked pytest -n 4 --dist=loadgroup -m ""
# Only the milestone acceptance test
uv run --locked pytest -n 4 --dist=loadgroup -m milestone_acceptance
```

Local phase and story verification may defer this test until final milestone
acceptance, including under existing plans. This developer-authorized exception
changes only this test's local scheduling; preserve its assertions and historical
evidence. All other required distribution and installation checks still apply.
Record this deferral in verification evidence. Default runs cover the routine
suite; only the explicit all-tests command establishes complete-suite coverage.


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
count, durations, diagnostics and platform with results. A parallel run with `-m ""` exercises the full suite; selected runs do not replace final full
verification. Retain serial execution for diagnosis. Parallel macOS evidence
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
uv run --locked pytest -n 4 --dist=loadgroup --keep-test-workspaces tests/integration/test_distribution_verification.py
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

Use TDD for new behavior and bug fixes. At every phase gate, including the last
phase of a story, run only direct tests of modules created or modified by that
phase's tasks. Select by the public behavior tested, whether the test lives in a
unit or integration directory. Exclude tests selected solely because an unchanged
caller depends on a changed module. Use explicit paths, node IDs or selectors:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_cli_version.py
```

Record changed modules, exact selectors, module-to-test mappings, acceptance
criteria, public boundaries and limits, selected/deselected counts, results and
platform. Manual selection is sufficient. Record missing direct coverage and
uncertain impact explicitly. Preserve assertions, timeouts and known failures;
selection must not conceal a failing check. Documentation-only work uses document,
link and whitespace checks with a rationale instead of product tests.

Keep locked synchronization, lock consistency, lint, formatting, strict typing,
CLI version smoke and `git diff --check` at executable phase gates. Record the
lock hash before and after verification and explain intentional changes.

Defer caller/dependent regressions and the full local suite to milestone
acceptance. Packaging, dependencies, schemas, security controls and uncertain
impact do not trigger an earlier full local run. Direct distribution/installation
tests remain phase checks when they directly test changed modules; the existing
`milestone_acceptance` test remains reserved for milestone acceptance locally.
Record each deferral and its owning milestone acceptance task before the gate.

### Story acceptance

Reuse valid phase evidence. Rerun direct tests when later changes invalidate it;
renew affected artifact evidence when its inputs change. Reconcile acceptance
criteria and identify deferred regression coverage without claiming full-suite
verification. Keep developer approval gates and explicit story acceptance.
Unresolved required direct tests or known failures remain blockers.

### Milestone acceptance

Assign a named milestone acceptance verification task before requesting acceptance.
That task owns every deferred check from the milestone's stories. Run:

```sh
uv run --locked pytest -n 4 --dist=loadgroup -m ""
```

Include shared checks, applicable direct-wheel and sdist-rebuilt-wheel distribution
and installation verification, and required manual/platform checks. Reconcile
all deferrals with actual results; reuse identical artifact checks only when the
suite demonstrably performed them against unchanged inputs. Record revision,
working-tree changes, lock hash, artifacts, commands, counts, outcomes and limits.
Full-suite evidence and required checks must pass before milestone acceptance.
After later executable changes, renew full-suite evidence against the final
milestone implementation; renew artifacts when their inputs change. Document-only
or approval-record edits require document checks with a rationale.

