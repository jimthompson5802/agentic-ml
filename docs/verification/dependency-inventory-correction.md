# Installed dependency inventory correction — 2026-11-03

The developer requested this correction after two real installed-package tests
failed because `tzdata` was absent from fresh Linux environments. Development
`uv.lock` selects Kombu 5.6.2, which requires `tzdata` unconditionally. Fresh
installations selected Kombu 5.7.0, whose installed metadata requires `tzdata`
only on Windows. Both probes incorrectly required the same hardcoded transitive
inventory in either case.

## Scope and public boundaries

Owning requirements are [US-33 / #3](https://github.com/jimthompson5802/agentic-ml/issues/3)
AC-02–05 (isolated installations, both wheel paths and diagnostic failures) and
[US-01 / #8](https://github.com/jimthompson5802/agentic-ml/issues/8)
AC-02–04 (normal pinned installations, recorded dependencies, stable identities
and explicit upgrades). US-35 / #47 AC-01–05 supplies the preserved driver
cleanup/retention contract. These issues remain historically accepted; this
maintenance correction does not reopen product delivery or accept a milestone.

Retrieved #3's full body, its one comment (6510671946), and stable refreshed
metadata (`updated_at=2026-10-30T03:11:48Z`). Retrieved #8's full body, zero
comments, and stable refreshed metadata (`updated_at=2026-10-30T10:42:22Z`).
Also retrieved #47's body, zero comments and refreshed metadata. GitHub milestone
objects are unset; issue bodies assign Milestones 0, 1 and 50 respectively.
The approved ADR-007 naming correction supersedes #3's historical CLI spelling.
The contributor verification contract requires declared runtime dependencies,
not an invariant list of transitive package names.

The developer's instruction “make the correction” authorizes the described
metadata-based inventory and lock validation. Reuse the existing approved
subprocess probe/driver boundaries in the US-33, US-01 and US-35 plans. The
interfaces under test are isolated `check_installed.py` and `check_project.py`
commands plus the real wheel and pinned-Git installation drivers. Assertions
observe exit status, stderr diagnostics, resources, identities and filesystem
outcomes. Metadata/lock mutation fixtures exercise invalid installations without
mocking internal collaborators; synthetic metadata-only distributions do not
establish that their code can be imported. Real baseline installations cover
actual resolution, CLI/import/resource access and both wheel paths.

No product runtime behavior, dependency declarations, lockfile, existing
timeouts or skip markers change. The independently specified direct harness
requirements, source provenance and resource assertions remain. The existing
approval-schema negative test is strengthened to require its own diagnostic.

## Implementation and TDD evidence

Raw XML and full driver records are retained beneath
`.dev-records/verification/20261103-dependency-closure/` and the individual
timestamped driver directories reported in those XML files.

All pytest invocations use `uv run --locked pytest -n 4 --dist=loadgroup`.
Acceptance-module selections additionally use `-m ""`. Every command supplies
`--junitxml=.dev-records/verification/20261103-dependency-closure/<file>.xml`.

| Slice | Selection / evidence file | Result |
|---|---|---|
| Original red | `test_both_installed_wheel_paths_pass` and `test_pinned_project_runs_without_checkout_or_cache`; `red.xml` | Both failed on the dependency inventory, 11.55s |
| Original green | Same unchanged tests; `green.xml` | 2 passed, 13.66s |
| Additional probe regression coverage | `test_dependency_inventory_uses_active_runtime_requirements` and `test_runtime_lock_matches_dependency_graph`; `metadata-lock.xml` | 17 passed, 13.35s, before adding the lock-root injection case |
| Approval diagnostic red | `test_missing_approval_schema_fails_installed_inventory`; `approval-red.xml` | Failed because missing resource had no specific diagnostic, 9.22s |
| Approval diagnostic green | Same test after adding the missing-resource message; `approval-green.xml` | 1 passed, 8.63s |
| Lock-root injection red | `test_runtime_lock_matches_dependency_graph[injected]`; `lock-root-red.xml` | Failed because a tampered root could introduce an unrelated locked package, 11.11s |
| Lock-root injection green | All four lock-graph cases; `lock-root-green.xml` | 4 passed, 12.99s |

The original two failures were corrected on the first implementation attempt.
The lock-root slice and approval diagnostic each passed after their first
corrective change. An initial strict-type check found a normalized-name dictionary
annotation mismatch; adding its explicit `dict[str, str]` annotation resolved it.
No suppressions or relaxed assertions were added. Regression coverage added
after the initial green validates existing corrected behavior; it is not claimed
as additional red–green evidence.

The shared helper walks active installed requirements from `agentic-ml`, revisits
packages when additional extras are requested, validates versions, and rejects
unreachable distributions and contributor tools. Lock validation follows all
universal marker branches and requested optional dependencies, rejects missing
edges/unreachable entries, checks installed version agreement, and requires the
locked experiment root to declare only the harness. The helper loads explicitly
without adding the harness checkout to installed Python import paths.

## Final verification

Platform: Linux / Python 3.12.16. The complete phase group passed: 289 tests
in 157.87s (`phase.xml`). The first complete-suite run finished with 337 passes,
70 failures, 5 setup errors and 3 skips in 203.97s (`full-suite.xml`). All 70
failures reported unavailable checkout executables: 66 for `.venv/bin/python`
and 4 for `.venv/bin/agentic-ml`. During the run, the checkout Python symlink
changed to `/opt/homebrew/opt/python@3.12/bin/python3.12`, which is unavailable
in Linux. The five setup errors were failed artifact-build commands. The
JSON summary `environment-interruption.json` preserves the failure grouping
and observed symlink target. This is failed verification, not a passing suite,
and the process responsible for the environment replacement is unconfirmed.

Created an independent Linux environment using
`UV_PROJECT_ENVIRONMENT=/tmp/agentic-ml-linux-dependency-checks-20261103 uv sync --locked --group dev`.
The complete suite passed with the same environment override and
`uv run --locked pytest -n 4 --dist=loadgroup -m ""`: **412 passed, 3 skipped
in 418.34s**, exit 0, recorded in `full-suite-isolated.xml`. All 18 added
regression cases passed, along with the existing driver, fixture, initialization,
planning, lifecycle and workspace consumers. The shared checkout environment is left unchanged.
This is an environment-isolation retry, not another corrective code change.
Existing three timeout-related skips remain developer-authorized exclusions;
they do not provide passing coverage or resolve their underlying timeouts.

Lock SHA-256 before and after final verification (unchanged):
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

Shared checks passed: `uv sync --locked --group dev`, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked ruff format --check .`
(135 files), `uv run --locked mypy src tests` (43 files),
`uv run --locked agentic-ml --version` (`0.1.0`), and `git diff --check`.
Lint, formatting, typing and smoke were repeated successfully in the isolated
Linux environment using the override above after the shared environment changed.
Formatting corrections followed the initial layout check; no suppression was
added. macOS and Windows are not verified by this Linux correction run.


The correction is ready for developer review. No commit, push, PR, milestone
acceptance or closure of existing deferred obligations is authorized or claimed.
The original shared-environment failure remains retained as separate evidence;
the successful isolated run does not identify who replaced the shared environment.
