# Two-group test scheduling verification

## Request and scope

The developer requested that the first four test categories run after every
implementation phase, with remaining categories at story acceptance and new
Milestone 2–6 tests in the phase group. They confirmed complete-suite story
acceptance and moving the reserved initialization test into that schedule, then
instructed implementation and continuation. This is a repository verification
policy change, not implementation or acceptance of a new product story.

| Group | Modules | Collected cases |
|---|---|---:|
| Phase | CLI version, initialization, planning, plan approvals | 289 |
| Story acceptance | Installation, distribution, lifecycle, pytest workspaces, scheduling | 108 |
| Complete suite | Both groups | 397 |

The five scheduling cases include the existing xdist regression plus four new
cases. Counts include parametrization. Collection confirms no overlap, no missing
cases, and the formerly reserved initialization case in story acceptance.

## Interfaces and implementation

The public boundary is the real pytest command, its default selection and `-m`
overrides, exit codes and selected test names. Nested subprocess fixtures use
fresh child bases and the original contributor workspace plugin. PYTHONPATH
selects contributor test support only; installed product imports remain unchanged.
Expected counts and test names are independently specified. Collection checks
verify the actual repository module partition. These checks establish current
group membership; future Milestone 2–6 classification also requires review.

Acceptance modules carry `story_acceptance`; all other tests receive `phase` at
collection. Explicit conflicting group markers fail with exit code 4 before
selection. Existing xdist groups, fixtures, assertions and timeouts remain intact.
CI retains `-m ""` and runs everything. No runtime product API changes.

## Commands and results

Raw evidence: `.dev-records/verification/20261102-test-schedule/`.

| Command/check | Result |
|---|---|
| `uv run --locked pytest --collect-only -q` | 289 selected, 108 deselected |
| Same with `-m story_acceptance` | 108 selected, 289 deselected |
| Same with `-m ""` | All 397 collected |
| Set comparison of collected node IDs | Disjoint groups; union equals full suite; expected phase modules and former reserved test verified |
| `uv run --locked pytest -n 4 --dist=loadgroup -m story_acceptance tests/integration/test_parallel_execution.py` | 5 passed in 1.29s |
| `uv sync --locked --group dev` | Passed |
| `uv lock --check` | Passed |
| `uv run --locked ruff check .` | Passed after import correction |
| `uv run --locked ruff format --check .` | Passed; final check 133 files |
| `uv run --locked mypy src tests` | Passed; 42 files |
| `uv run --locked agentic-ml --version` | Passed; 0.1.0 |
| `uv run --locked pytest -n 4 --dist=loadgroup -m "" --junitxml=.dev-records/verification/20261102-test-schedule/full-suite.xml` | 394 passed, 3 failed in 1575.49s; retained log and XML |
| `git diff --check` | Passed; renew after final documentation edits |

The full run includes every phase case; default selection is independently
verified through collection and subprocess regressions. No separate duplicate
289-case execution is required for the same unchanged inputs.

Initial lock SHA-256:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
Final checksum unchanged after both renewals. Local platform: macOS arm64, Python 3.12.15,
pytest 9.1.1, xdist 3.8.0. Linux and Windows not verified by this run.

## Failures, corrections and evidence limits

The earlier turn wrote the implementation before regression tests. No proper
behavior-missing red cycle is claimed. The first regression run failed in fixture
setup (4 failures, 1 pass): copying workspace support relocated its safety root,
so nested bases were rejected as unsafe. Correction attempt 1 loaded the original
contributor plugin, copied only conftest and used one verbose invocation rather
than reusing a base. The same cases then passed. No assertion or timeout changed.
Earlier collection also exposed a missing pytest import, corrected before this
run. Import lint correction needed Ruff's fix after manual sorting left spacing;
final lint passed. Sandbox cache errors were retried with escalation.
See retained `logs/attempts.txt` for the failure summary.

Existing product story approvals remain historical facts. Scope-change records
in US-03, US-35 and US-36 retain M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY ownership;
this run does not itself close either obligation or grant acceptance. Policy,
planning template, workflow, repository instructions and planning/execution skills
now use the two-group schedule. Documentation-only updates use link and whitespace
checks. Pre-existing devcontainer changes are outside this task. No publication.

## Full-suite failure investigation

The full run completed with 394 passes and three failures. The complete
initialization test exceeded its unchanged 600-second timeout. The missing-template
probe exceeded its unchanged 120-second timeout. The distribution-success workspace
case failed before writing its completion marker; its child distribution probe
had failed. All original tracebacks are retained separately in `logs/failure-*`
and in JUnit XML. No full-suite pass is claimed.

The three original cases were rerun unchanged with four workers/loadgroup,
without the rest of the suite. This diagnoses whether heavy concurrent installation
or a transient installer delay contributed; success on renewal would not establish
that resource contention was the cause. No code correction, relaxed assertions,
timeout changes, scheduling changes or suppressions were applied. Product bug
fixes would require their owning issue and approved scope before implementation.

### Developer-directed devcontainer renewal

The isolated host rerun completed one case before the developer requested stopping
the two outstanding tests and restarting them in the devcontainer. SIGINT was
sent to the diagnostic runner and its then-active descendants. The interrupted
log is preserved; no all-passing three-case run is claimed.

The two remaining distribution cases were started in container `aa2f61daec0c`
as `vscode`, workspace `/workspaces/agentic-ml`, using locked synchronization and
`UV_PROJECT_ENVIRONMENT=/home/vscode/.cache/agentic-ml-test-schedule-venv`.
This separate environment preserves the shared macOS `.venv`. Command:

```sh
uv run --locked pytest -n 4 --dist=loadgroup -m story_acceptance tests/integration/test_distribution_verification.py::test_complete_initialization_from_both_artifact_paths tests/integration/test_distribution_verification.py::test_missing_template_reports_installed_failure --junitxml=.dev-records/verification/20261102-test-schedule/devcontainer-renewal.xml
```

Result: **2 passed in 150.59s**, with JUnit XML and output retained in
`logs/devcontainer-renewal.log`. Linux/Python 3.12.16 evidence
is separate from the macOS full run. This is a platform-directed verification
retry, not a corrective code attempt. Original assertions and timeouts remain.

## Final outcome

Implementation and selection verification are complete. Both groups together
contain 397 cases. The full macOS run had 394 passes and three failures; the
isolated host renewal completed one passing case before developer interruption,
and the two remaining cases passed in the devcontainer. There is no single
all-passing full-suite run and no claim that the macOS timeout causes are fixed.
The developer specifically directed the two-case platform renewal; no additional
full-suite restart was performed. All assertions and timeouts remain intact.

Shared checks, guidance link resolution and final whitespace checks passed.
No product code or runtime resources changed. Existing milestone verification
obligations remain open; full-suite success is still required at future story
and milestone acceptance under the new policy. No commit or publication performed.

## Interrupted complete-suite devcontainer run

The developer subsequently requested all 397 cases in the devcontainer, then
requested stopping the run. The runner and its active descendants received
SIGINT; the invocation exited 130. The interrupted run recorded 93 passes and 8 errors in 194.52s, with 296 cases
incomplete. Partial JUnit XML is retained; this is not a completed suite.
The retained `logs/devcontainer-full-suite.log` contains interruption diagnostics.
The errors have not been diagnosed; no complete passing Linux suite is claimed.
Tests will remain stopped pending developer direction.

## Developer acceptance and publication authorization — 2026-11-03

The developer supplied a completed Linux/Python 3.12.16 full-suite result:
394 passed and three 120-second subprocess timeouts in 581.14s. The failed
cases were `test_failed_installed_probe_retains_available_environment`,
`test_missing_planning_schema_fails_installed_inventory`, and
`test_rebuilt_probe_failure_retains_both_environments`. At their request,
reran those exact selectors using `uv run --locked pytest -n 4
--dist=loadgroup -m ""`; all three passed in 54.64s, exit 0.
JUnit evidence is retained at
`.dev-records/verification/20261103-three-test-retry.xml`.
No assertions, timeouts or implementation changed for the retry. The supplied
full-suite output and the selected renewal are separate evidence; no single
all-passing suite or established timeout cause is claimed.

The developer then stated, “I'm willing to claim victory right now” and
explicitly requested committing and pushing the changes. This authorizes
publication of the current scheduling, guidance and devcontainer changes and
supersedes earlier pending-direction statements. It does not close the separate
milestone acceptance obligations. Final precommit `git diff --check` passed.
