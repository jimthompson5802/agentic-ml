# US-11 IP3: Installed project extraction

Status: IP3-T1–T4 complete; developer approved IP3 on 2026-11-07 UTC. Whole-story accepted by developer “i accept us-11”, 2026-11-07 UTC.
Authorization: developer “start us-11 ip3”, 2026-11-07 UTC.
Owning [plan](../plans/milestone-1-us-11.md), [issue #14](https://github.com/jimthompson5802/agentic-ml/issues/14),
[approved contract](../extraction.md) and [IP2 evidence](us-11-ip2.md).

## Scope and public boundaries

Baseline `0d74c214c22b9f985e77bb1b6e5f3a72d9d30d80` on
`US-11-local-data-extraction`, clean at entry. IP1/IP2 gates approved.
Refreshed complete issue body, one unique comment and stable final metadata:
`updated_at=2026-11-07T00:28:37Z`. Issue body assigns AC-01–05 to M1;
GitHub milestone field remains unset. All current criteria/scope decisions agree
with the plan, pandas refinement and active design. No scope revision needed.

Reuse the IP1-confirmed native function/DataFrame/report boundary. The new M1
`test_extraction_from_both_artifact_paths` invokes contributor verification with
real artifacts, normal installs and an actual project module outside the checkout.
`verify_extraction.py` composes the existing distribution verifier and copies
`check_extraction.py` plus project-owned `extraction_project.py` into the workspace.
It runs each probe using that wheel environment's Python with `-I`, from an
unrelated cwd, and saves project/API/report identities before cleanup. Existing
normal-install dependency, CLI, origin, inventory and resource checks run first.
No source-path insertion, editable fallback, internal mocks or adapter added.

The installed API processes semicolon CSV and Parquet, native configured
selection/filter/merge, returning literal rows `(2, beta), (3, alpha)`. The probe
checks source schemas/counts/bytes, native reader option, settings copied despite
callback mutation, callable/code identity, time bounds, independent input/output
SHA-256, serialized rows and persisted JSON report. Invalid return, original
project RuntimeError identity, native pandas KeyError, missing input and corrupt
Parquet fail with context and no completed destination or staging remnants.
Imports resolve inside the independent environment's site-packages; pytest and
mypy are absent. Both environments use declared runtime dependencies only.

These boundaries cover component delivery, not notebook/kernel behavior, hidden
callback reads, hostile code isolation, quality validation, splits, DVC replay,
MLflow or assistant usability. Those retain US-12/13/27/39/40 ownership. No
packaged resources, toolkit implementation, dependency declarations or lock changed.

## Red–green and correction evidence

Raw records: `.dev-records/verification/20261107-0d74c21-us11-ip3/`.
Logs/JUnit preserve failures and passing retries. Child distribution commands,
installed inventories, artifact identities and cleanup summaries live in the
linked driver record directories, outside disposable pytest workspaces.

One focused serial TDD slice exercises the expensive artifact boundary without
four-worker startup; full gates retain four workers with loadgroup.

- Red: `uv run --locked pytest tests/integration/test_distribution_verification.py::test_extraction_from_both_artifact_paths --junitxml=.dev-records/verification/20261107-0d74c21-us11-ip3/red.xml`.
  One failed in 9.31s. The initial driver successfully verified distributions
  but had no extraction probe, so the required `PASS extraction direct-wheel`
  assertion failed. This was missing verification behavior, not an installation
  or import setup error. `logs/red.log` retains the original failure.
- Green implementation: added the copied project/probe and both isolated calls.
  First run failed in 10.30s (`green.xml`, `logs/green.log`): the test incorrectly
  expected OSError for corrupt Parquet. The unchanged toolkit correctly propagated
  pyarrow ArrowInvalid. Corrective attempt 1 used that exact native exception;
  `green-retry.xml`, `logs/green-retry.log`: one passed in 12.00s. No product
  correction or assertion weakening; expected native exception made precise.
- Strict typing initially rejected a direct pyarrow import because pyarrow ships
  no typing metadata (`logs/mypy-initial.log`). Corrective attempt 1 dynamically
  imports the native exception and casts the class, without suppressions or new
  dependencies. Renewed `mypy src tests` passed (60 files).
- Locked sync and the first focused command encountered sandbox read-only uv
  cache errors; approved outside-sandbox retries passed. Snapshot-file GitHub
  reads encountered sandbox network errors; approved retries saved the complete
  stable snapshots. These environment failures are separate from test failures.

The new expensive test uses a 180-second subprocess timeout, matching the existing
installed planning test: two normal runtime environments, isolated sdist rebuild,
existing full inventories and two new probes. Existing timeouts, assertions,
xdist groups and three historical skips remain unchanged.

## Verification results

M1 gate passed: 432 passed, 1 existing skip in 223.52s; 433 selected from
535 collected, 102 deselected. Four loadgroup workers, exit 0 (`m1.xml`,
`logs/m1.log`). M1–6 passed: 432 passed, 1 existing skip in 208.91s,
exit 0 (`m1-6.xml`, `logs/m1-6.log`), again 433 selected, 102 deselected.
The total collection is 535 (IP2 534 plus this one new installed test); both
executed selections contain the same 433 cases in the current repository.
All required IP3 component/installed/story evidence is reconciled.
Shared checks pass with exact repository commands:
`uv sync --locked --group dev`, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked ruff format --check .`,
`uv run --locked mypy src tests`, `uv run --locked agentic-ml --version`,
and `git diff --check`. Results:
locked sync, lock consistency, repository lint, formatting (255 files), strict
mypy (60 files), CLI version `0.1.0`, and whitespace. Commands and final counts
will be recorded before the gate.

Platform: Linux aarch64, Python 3.12.16, uv 0.13.6. Contributor lock SHA-256:
`4b21570fb52b7a4eea94c5d85404e95afefe2d7c44eab014f2122fc9793d847b`.
Both focused normal installations resolved toolkit 0.1.0, pandas 3.1.1 and
pyarrow 25.0.1, demonstrating the declared runtime range independently of the
contributor pandas 3.1.0 lock. Other platforms remain unverified by this phase. Normal artifact installations
resolve declared dependency ranges separately from the contributor lock; their
actual versions and paths are in retained extraction/child inventory manifests.

## Criterion and deferral reconciliation

| Criterion | Evidence | Result |
|---|---|---|
| US-11-AC-01 | IP2 operations matrix; both installed projects' literal CSV/Parquet/filter/merge results and project module | Accepted |
| US-11-AC-02 | IP2 schema/boundary cases; installed ordered schemas, row/byte counts and original metadata after callback mutation | Accepted |
| US-11-AC-03 | Explicit native project settings and reader option, copied configuration in returned/persisted reports | Accepted |
| US-11-AC-04 | Independent source/code/output SHA-256, declared paths, time bounds, callable and library versions | Accepted |
| US-11-AC-05 | IP2 failure matrix; both installations' standard/native errors, preserved project exception and no completed failure outputs | Accepted |

IP3-T4 resolves IP2's installed-project, both-artifact and M1–6 story verification
deferrals. The selected existing skip is
`test_missing_planning_schema_fails_installed_inventory`; it does not verify
missing-schema behavior. The other two previously authorized skips remain in
excluded M0/M50/infrastructure coverage. No assertions/skips/timeouts changed.
Existing skipped coverage does not pass by exclusion.
Historical M1/M50 obligations, cross-story integration/manual checks and platform
limits remain open. Broader local suites/standalone artifact invocations were
not requested; artifact verification runs internally through the M1 test.

Guide Python fences parse and 63 local links/anchors resolve. The first checker
incorrectly required a file for README's valid `docs/reviews/` directory link;
corrective attempt 1 permitted directory targets and validation passed, without
changing repository links. Full command/outcome ledger is `commands.json`;
`summary.json`, `driver-records.json` and `identities/source.json` retain results,
source/platform identities and complete stable issue snapshots.

Final installed extraction records:
`.dev-records/verification/20261107T112643Z-0d74c214c22b-4c74bcadb81f414aa2a27030aed48daa/`;
child distribution records:
`.dev-records/verification/20261107T112643Z-0d74c214c22b-6b5b067336bf44378af2f91300e16ec4/`.
Both report successful verification and complete cleanup. Final artifact SHA-256:

| Artifact | SHA-256 |
|---|---|
| Direct wheel | `367312c1422f2bd6331f35cd4e397c1551cb15f6b47b54e1fb2117a3e1ef5f66` |
| Source distribution | `1390fec3c1a2c5c815b5af0c6e1faba34be850b800d341028c8d6c6bd7f1af1f` |
| Rebuilt wheel | `367312c1422f2bd6331f35cd4e397c1551cb15f6b47b54e1fb2117a3e1ef5f66` |

Executable verification file bytes/hashes and full final dirty-tree patch/hash
are retained under `identities/`. `uv.lock` matches its entry and committed
baseline SHA-256 after all verification. Documentation-only final record edits
do not invalidate executed behavior evidence. Guide now
includes fixture preparation, explicit root/unrelated cwd, real project code,
settings/report inspection and a standard-error example, plus quality/DVC/trusted
code limits. README links the guide. Documentation-only changes need no new
behavior test; toolkit behavior is unchanged in this phase.

## Developer gate

Developer “i approve ip3” approved the final implementation phase on
2026-11-07 UTC. All IP3 tasks and phase gates are complete. Whole-story
acceptance given by developer “i accept us-11”, 2026-11-07 UTC.
Accepted-story commit/publication/static review now authorized under execute-plan.
Approval-record edits are documentation-only; runtime evidence remains applicable.
`git diff --check` passed; no new executable behavior requires TDD or test reruns.
