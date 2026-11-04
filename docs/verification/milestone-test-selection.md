# Milestone test selection — 2026-11-04

Branch: `chore-refactor-tests`, based on `main` at the start of the developer's
maintenance request. Initial working tree was clean. No harness runtime,
dependency or lockfile changes; no commit, push or PR is authorized.

## Scope and public boundaries

The supplied “Stratify tests by milestone” plan is the maintenance scope, rather
than a new harness user story. One implementation phase covers classification,
selection, policy reconciliation and verification. Final developer gate pending.
The developer explicitly selected public pytest subprocess tests: these verify
selection, deduplication, missing-classification diagnostics and xdist grouping;
they do not establish harness runtime behavior or additional platform support.

Uniform CLI tests directly verify M0 US-33 installed CLI/import requirements.
Initialization, planning and approvals verify M1 US-01–03. Installation and
artifact modules use function/parameter markers: installed Git requirements are
M1, wheel inventory/build requirements M0, and driver cleanup/retention M50
US-35. Workspace ownership/lifecycle modules verify M50 US-35/36. Scheduling
policy regressions are infrastructure. Incidental fixture use adds no milestone.
The two success tests that explicitly assert both functional installation and
cleanup/evidence persistence carry both their functional milestone and M50.

## Reconciled inventory

| Classification | Collected cases |
|---|---:|
| M0 | 18 |
| M1 | 314 |
| M2 | 0 |
| M3 | 0 |
| M4 | 0 |
| M5 | 0 |
| M6 | 0 |
| M50 | 80 |
| M99 | 0 |
| Infrastructure | 6 |
| Distinct complete collection | 416 |
| Default M1–6 | 314 |
| Excluded by default | 102 |

Marker counts sum to 418 because two cases have two associations. Pytest runs
selected cases once. Baseline was 415: 409 cases outside scheduling are retained;
the five old scheduling cases become six (one additional selection parameter).
No non-scheduling function body changed, verified by AST comparison to HEAD;
assertions, timeouts, xdist groups and three existing skip decorators remain.

## Red–green evidence

- Default selection red: `uv run --locked pytest -n 4 --dist=loadgroup -m ''
  tests/integration/test_parallel_execution.py -k selects_expected_group
  --maxfail=1`: 1 failed, 3 passed. The old hook automatically assigned phase;
  nested pytest ran 11 cases instead of the independently expected seven.
  Fixture marker registration was added before this valid red run. An earlier
  unknown-infrastructure-marker setup error is not counted as red evidence.
- Missing classification red: same four-worker command with
  `-k rejects_missing_classification` and classification validation absent:
  1 failed. Nested pytest exited 5 (all deselected), rather than the required
  actionable collection error. The initial run with the obsolete phase-adding
  hook hit an unknown-marker internal error and is not valid red evidence.
- Green: `uv run --locked pytest -n 4 --dist=loadgroup -m infrastructure
  tests/integration/test_parallel_execution.py
  --junitxml=.dev-records/verification/20261104-milestone-selection/scheduling.xml`:
  **6 passed in 4.09s**. Checks default M1–6, explicit M1, explicit M50, explicit
  all classifications, overlapping M1/M2 case executing once, missing test ID
  diagnostic even when deselected, and existing worker grouping/isolation.
  Earlier focused green also passed all six in 3.04s. Final renewal after
  strengthening exact selected-ID assertions: **6 passed in 2.97s**, recorded
  in `scheduling-final.xml`.

No corrective attempt failed after either behavior implementation. Setup errors
above are preserved as setup evidence, not asserted to be valid behavior reds.

## Verification

- `uv sync --locked --group dev`: passed, 195 resolved / 192 checked.
- `uv lock --check`: passed.
- `uv run --locked ruff check .`: first found import-spacing introduced beside
  the new approvals module marker; one formatter correction, then passed.
- `uv run --locked ruff format --check .`: passed (final check: 137 files).
- `uv run --locked mypy src tests`: passed (43 source files).
- `uv run --locked agentic-ml --version`: passed, `0.1.0`.
- `git diff --check`: passed.
- Collection only: `PYTHONPATH=/tmp uv run --locked pytest --collect-only -q
  -m '' -p milestone_inventory`: 416 cases; temporary reporting plugin only
  records public collected item IDs and markers, without running tests.
- `uv run --locked pytest -n 4 --dist=loadgroup
  --junitxml=.dev-records/verification/20261104-milestone-selection/default.xml`:
  **313 passed, 1 skipped in 234.32s**, 314 selected / 102 excluded. The selected
  skip is the existing missing-planning-schema timeout exclusion. The two other
  temporary skips are outside the default selection. No failures. Later changes
  only strengthened excluded infrastructure regression assertions and documentation;
  default-selected test bodies and behavior were unchanged.

Raw final inventory, collection and JUnit records:
`.dev-records/verification/20261104-milestone-selection/`.
Lock SHA-256 before/after:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

## Limits and gate

Linux / Python 3.12.16, pytest 9.1.1, xdist 3.8.0. No new macOS or Windows
verification. The initial implementation verification ran no broader local suite or standalone
artifact command; the explicitly requested complete-suite follow-up below passed;
selected tests can invoke those drivers. CI's complete suite and standalone
artifact checks are unchanged. The three temporary skips and original unresolved
timeout causes remain; excluded or skipped cases do not establish passing
coverage. M1/M50 owners retain unresolved evidence and reconciliation duties,
with explicit scope records superseding automatic full-suite/artifact execution.

Technical tasks complete; **final phase approved** on 2026-11-04 by the developer
message “i approve the final phase”, recorded in the
[saved plan](../plans/milestone-test-selection.md).
No further verification or publication is automatically authorized.

## Explicit complete-suite follow-up — 2026-11-04

Developer command: “do a full run.” Running
`uv run --locked pytest -n 4 --dist=loadgroup -m ''
--junitxml=.dev-records/verification/20261104-milestone-selection/full-suite.xml`.
416 cases selected; no standalone artifact-driver command requested. This request
does not constitute final phase approval or publication authorization.
**Result: 413 passed, 3 skipped in 482.73s (8m02s), exit 0.** All 416 cases
selected, none deselected. JUnit independently confirms 416 testcase records,
three skips and no failures/errors. These are the unchanged developer-authorized
temporary skips; their timeout causes remain unresolved. No standalone artifact
driver command was run; selected tests exercised their internal artifact drivers.
Linux/Python 3.12.16, pytest 9.1.1, xdist 3.8.0. Lock SHA-256 unchanged:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
`git diff --check` passed after the evidence update. No executable files changed
during this follow-up. This passing run does not approve the final phase, close
skipped coverage or establish milestone acceptance.
