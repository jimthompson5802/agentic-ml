# Optional parallel development tests

Developer “implement the change” authorizes the preceding parallel-test proposal:
development-only pytest-xdist, installation/distribution groups, individually
scheduled initialization/CLI cases, explicit invocation, two/four-worker
verification. This is repository test tooling, not a new harness user story or
change to product acceptance criteria. No CI-default change, commit or publication
is authorized. Existing US-02 correction review remains a separate gate.

## Verification scope and isolation

No new or corrected harness behavior: TDD does not require a manufactured failing
product test. Existing public installed CLI/API and distribution boundaries are
unchanged. Verify scheduling through real pytest collection/execution, compare
the 128 collected cases against serial collection, confirm all execute once, and
run existing assertions with two workers then four. Keep all tests and timeouts.
Both full runs include installed direct/rebuilt wheel checks. No tests deferred.

Module-level xdist groups keep 12 installation cases and 10 distribution cases
together. The 103 initialization and three CLI cases remain individual units.
Each worker has isolated module fixtures; project fixtures are per test. Source
repositories, built artifacts, stores, databases and writable installation probes
are temporary. Installation cache deletion is scoped to its newly created
workspace. No shared product source is modified. Global uv cache may contend;
do not delete it or bypass locking.

Dependency change deliberately adds pytest-xdist 3.8.0 and execnet 2.1.2 to the
development lock; runtime declarations are unchanged. Existing commands and CI
remain serial unless explicit parallel flags are supplied.

## Results

Serial collection: 128 tests. Two-worker full run: **128 passed**, zero failures,
errors or skips, exit 0 in **1054.36s (17m34s)**. JUnit contains 128 unique case
IDs: 103 initialization, 12 installation, 10 distribution, three CLI.
Command: `uv run --locked pytest -n 2 --dist=loadgroup
--basetemp=/private/tmp/agentic-ml-parallel-two
--junitxml=/private/tmp/agentic-ml-parallel-two.xml --durations=20`.
Four-worker full run: **128 passed**, zero errors/failures/skips, exit 0 in
**788.09s (13m08s)**, same flags with `-n 4` and `parallel-four` paths. Both XML
case sets exactly match serial collection and contain no duplicates. However,
these timings do **not** validate the required grouping (see blocker below).

Locked sync, lock check, lint, formatting (81 files), strict types (20 source
files), version smoke (0.1.0) and whitespace passed. Verification lock SHA-256:
`62b0e6a88853bf3d5ea5d648c5665a4c20e678c76c528b50a67723b2ada04391`.
Baseline source commit `3a5fd84` plus this tooling diff. Platform: macOS 15.7.9
arm64 / Python 3.12.15 / uv 0.13.1. Linux and Windows parallel execution unverified.
Initial dependency installation encountered uv cache sandbox denial and succeeded
with escalation; this is infrastructure evidence, not a behavior failure.

Previous serial timing is historical (119 cases, 31m38s); the final 128-case
serial suite was cancelled at developer request. Benchmark comparisons must
disclose the different case counts and cache conditions.

## Grouping incompatibility — unresolved

Final fixture inspection found distribution artifacts under all four workers.
The focused verbose diagnostic (three missing/ambiguous artifact cases) confirmed
the marked cases ran on gw0/gw1/gw2. Temporary collection instrumentation confirmed
`loadgroup=True` and markers present, but no group suffix in node IDs. Installed
xdist 3.8.0 writes `_nodeid`; installed pytest 9.2.0 reads `_id` instead. Thus the
128-test passes establish behavior outcomes, but not correct grouped scheduling.

Added `test_parallel_execution.py` at the public pytest subprocess boundary to
detect the exact defect: eight tiny marked cases write their public worker IDs;
each of two groups must remain on one worker, and groups use different workers.
Red command: `uv run --locked pytest tests/integration/test_parallel_execution.py
-q --basetemp=/private/tmp/agentic-ml-group-regression-red
--junitxml=/private/tmp/agentic-ml-group-regression-red.xml`.
Result: **1 failed**, exit 1, 10.87s; alpha split across all four workers.
Lint, formatting and strict typing for the new test passed. Suite is now 129 cases.
No corrective implementation attempt has yet been made for this incompatibility.
The original grouping assertions are retained.

Proposed dependency correction: constrain pytest from `>=8,<10` to `>=8,<9.2`
while retaining pytest-xdist 3.8.0, regenerate lock, verify the regression green,
and renew two/four-worker suite evidence. Developer approval required by the
repository rule against introducing a workaround without explicit direction.
No constraint applied, no assertions weakened, no check disabled. Implementation
is incomplete; do not present the earlier timings as verified grouped benchmarks.

Diagnostic plugin `/private/tmp/group_diag.py` and `group-diag-gw*.json` remain
outside Git as evidence; no diagnostic plugin is loaded by repository commands.

## Approved compatibility correction

Developer “yes” approves the proposed pytest `>=8,<9.2` constraint and renewed
verification. Corrective attempt 1 changes the declaration and lock from pytest
9.2.0 to 9.1.1; xdist remains 3.8.0. No assertions, test boundaries or timeouts
changed. Preserve the prior failed regression and invalid grouping benchmark
evidence above. Green regression: same command as red with `green` paths,
**1 passed**, exit 0 in 2.95s. Separate verbose three-case artifact check shows
`@distribution` suffixes and all three cases on gw0, **3 passed** in 1.46s.
Attempt 1 resolves the original failure. Renewed complete runs use
`uv run --locked pytest -n N --dist=loadgroup -v
--basetemp=/private/tmp/agentic-ml-grouped-LABEL
--junitxml=/private/tmp/agentic-ml-grouped-LABEL.xml --durations=20`, where
N/LABEL are 2/two and 4/four. Two-worker renewed run: **129 passed**, exit 0,
**1019.79s (16m59s)**. Verbose reports confirm all 12 installation cases on gw0
and all 10 distribution cases on gw1. Four-worker renewed result follows below.

Updated locked sync, lock check, lint, formatting (82 files), strict types (21
source files), version smoke and whitespace passed. Final verification lock:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
This deliberate change supersedes the earlier lock identity for final evidence.

## Final results

Four-worker renewed run: **129 passed**, exit 0, **726.44s (12m06s)**.
Both renewed runs have zero failures/errors/skips. Each XML contains exactly
129 unique cases matching serial collection (after removing xdist group suffixes):
103 initialization, 12 installation, 10 distribution, three CLI, one scheduling
regression. Verbose logs confirm all 12 installation cases stayed on gw0 and all
10 distribution cases on gw1 in both runs. Only gw1 has an artifact build fixture
in either retained run, unlike the incompatible-version benchmarks.

| Workers | Cases | Elapsed time | Result |
|---|---|---|---|
| 2 | 129 | 1019.79s / 16m59s | All passed; groups verified |
| 4 | 129 | 726.44s / 12m06s | All passed; groups verified |

Four workers were about 29% faster than two in this local measurement. Contention
increases individual durations (complete artifact initialization: 240.94s with
two versus 322.41s with four), so elapsed time is not simply serial time divided
by worker count. Repeated performance stability, Linux/Windows parallel support,
and interruption cleanup of parallel worker descendants have not been verified.
No new serial full run was performed; serial collection and the standalone
scheduling regression passed, while both complete runs used explicit parallel
flags. Default invocation and CI remain serial as authorized.

Raw verbose logs and JUnit XML: `/private/tmp/agentic-ml-grouped-two.log`,
`/private/tmp/agentic-ml-grouped-two.xml`, `/private/tmp/agentic-ml-grouped-four.log`,
`/private/tmp/agentic-ml-grouped-four.xml`. Experiment fixtures and built artifacts
remain under matching `agentic-ml-grouped-two` / `agentic-ml-grouped-four` directories.
These use unpublished local full-SHA fixture repositories, not a GitHub fetch of
the uncommitted tooling changes. Both direct/rebuilt wheel checks and complete
fresh CLI/existing API initialization passed in both full runs.

Compatibility correction required one attempt; regression and relevant full
suites passed with original assertions intact. No suppressions or check exclusions
were added. Only documentation/checkpoint records changed after final execution.
Tooling is implemented and verified locally; changes remain uncommitted and
unpublished. US-02 correction review/acceptance remains a separate developer gate.

## Local agent command policy update

Developer requested updating the instruction file linked from AGENTS.md to use
four workers locally. The development guide now requires the explicit
`uv run --locked pytest -n 4 --dist=loadgroup` command for local verification,
including complete-suite evidence and selected tests. Serial execution remains
available for short focused TDD and diagnosis with a recorded reason; two workers
remain available for explicit resource/performance comparisons. CI and pytest
configuration are unchanged. This is documentation-only, so no failing product
test or full-suite rerun is required. Existing runtime results remain applicable.

Developer “commit change” subsequently authorizes the local commit of parallel
tooling, local-command instructions and verification records. Final documentation
checks verified 33 local link paths, the AGENTS.md development-guide pointer and
preserved policy anchors; whitespace passed. No executable changes followed the
two/four-worker full-suite verification. No push authorized.

## GitHub Actions parallel command

Developer requested parallel workers for GitHub Actions automated tests.
The workflow test step now runs `uv run --locked pytest -n 4 --dist=loadgroup`,
matching the verified local four-worker command. Development guidance now reflects
this CI setting. Runner, timeout, conditions, remaining checks and package-build
steps are unchanged. This is a workflow configuration change with no new harness
behavior; TDD does not require a manufactured product failure. Existing local
129-test parallel evidence applies to the command, not hosted Linux execution.
Hosted verification remains pending publication and observation of a CI run.
No commit or push authorized for this change.

Static verification passed: parsed workflow YAML, exact four-worker test command,
existing sync-success condition, 20-minute timeout and main-branch push trigger;
final workflow diff is one command-line change. Local documentation links and
whitespace checks passed. `actionlint` is not installed, so its validation was
not run. No product suite rerun: no source, tests, dependencies or lock changed.

Developer “commit changes” authorizes the local commit of the CI command and
documentation records. Hosted verification remains pending; no push authorized.
