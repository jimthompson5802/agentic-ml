# US-02 journal temporary-path correction

Issue #9 / Milestone 1 / US-02-AC-02 and US-02-AC-04. Developer “i approve”
authorized the proposed correction on 2026-10-31, with diff review before commit
or push. Original acceptance and approval history remain unchanged.

The complete issue body and all comment pages were refreshed; zero comments,
stable updated timestamp 2026-10-31T01:15:38Z. No new scope decision. Applicable
contracts: initialization conflict preservation and configurable storage in
interfaces-and-configuration §8, and the accepted US-02 IP1 ADR-005/006 setup
slice. The fix reserves `.agentic-ml/init.tmp` with the existing bidirectional
containment check. Journal format and atomic-write behavior are unchanged.

## Boundaries and TDD

Approved installed public CLI/API boundaries are reused: separate experiment
projects install a full-SHA local Git dependency; tests observe rejection,
unchanged originals, absence of scaffolding/state, and corrected retry. No
private helper assertions or internal mocks. These do not establish protection
against concurrent hostile filesystem mutation.

- Red: `uv run --locked pytest tests/integration/test_initialization.py -k
  'storage_cannot_overlap and init.tmp and mlflow' -q
  --junitxml=/private/tmp/us-02-tmp-red.xml` reproduced the conflict: one failed,
  46.037s in XML. The generic failure arrived after durable writes; retained
  `.agentic-ml/init.json` and a 954368-byte `init.tmp` database demonstrate the
  defect. Pytest then lingered during default temporary-directory cleanup;
  eventual exit 1, 97 deselected, 217.32s including cleanup.
- A dedicated-fixture red rerun used the same selector with
  `--basetemp=/private/tmp/us-02-tmp-red-fixture` and
  `--junitxml=/private/tmp/us-02-tmp-red-clean.xml`: one failed, 97 deselected,
  exit 1, 70.85s. This rerun used the unfixed installed source fixture.
- Corrective attempt 1: add the journal temporary path to protected storage
  destinations. Exact-path green used the same selector with
  `--basetemp=/private/tmp/us-02-tmp-green-fixture` and
  `--junitxml=/private/tmp/us-02-tmp-green.xml`: one passed, 97 deselected,
  exit 0, 5.55s.
- After green, extend existing coverage to `init.tmp/child` and all four flags,
  plus API rejection/corrected CLI retry for `init.tmp`, retaining the existing
  `init.json` API case and all prior assertions. Ancestor `.agentic-ml` remains
  covered by the original matrix. Focused and complete verification below.

## Verification

Baseline: commit `357617c` plus the source/test diff and documentation in this
correction. macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1, Git 2.54.0. No new
Linux/Windows verification. The prior PR Linux run passed before this correction
and does not verify the changed implementation.

`uv sync --locked --group dev`, `uv lock --check`, `uv run --locked ruff check .`,
`uv run --locked ruff format --check .` (79 files), `uv run --locked mypy src tests`
(20 source files), and `uv run --locked agentic-ml --version` (0.1.0) passed.
Documented Ruff formatter adjusted the parameter signature before final checks.
Cache sandbox denials for sync/full suite and GitHub connectivity failures were
retried with escalation; these were infrastructure failures, not behavior reds.

Lock SHA-256 remains
`b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`.
No dependencies, suppressions, disabled checks or acceptance criteria changed.

Focused command: `uv run --locked pytest tests/integration/test_initialization.py
-k 'storage_cannot_overlap or rejected_storage_override' -q
--basetemp=/private/tmp/us-02-tmp-regressions
--junitxml=/private/tmp/us-02-tmp-regressions.xml`: **38 passed**, 65 deselected,
exit 0, 192.59s. This covers 36 CLI overlap cases and both API/corrected-retry
cases. Full-suite command:
`env MLFLOW_DISABLE_TELEMETRY=true DVC_NO_ANALYTICS=1 uv run --locked pytest
--basetemp=/private/tmp/us-02-tmp-full
--junitxml=/private/tmp/us-02-tmp-full.xml`.
The unfiltered suite collected 128 tests and includes direct/rebuilt wheels,
isolated installed resources and complete fresh CLI/existing API initialization.

Both normal distribution and complete installed initialization tests passed in
the full run. Retained artifacts: `/private/tmp/us-02-tmp-full/artifacts0`;
direct wheel SHA-256
`2d3b180f159c39f716cbd7bb8aebbb149a2a0e122376cfd1405dc462ec48266d`,
sdist SHA-256
`1a2dea3008550c5348de70d5f6383ea62ef1780e466a9d53b9be5864ef536d25`.
Complete installed fixtures remain under
`/private/tmp/us-02-tmp-full/test_complete_initialization_f0/initialization`.

Correction gate pending; no commit or push authorized.

Developer requested “cancel the full suite test run”. Sent interrupt to the
running session; it exited 130 after **27 passed in 728.36s**. Of 128 collected
tests, **101 did not complete**. No test failure was reported before interruption;
the cancellation traceback is not a product failure. XML remains at
`/private/tmp/us-02-tmp-full.xml`. Do not treat this partial run as final full-suite
evidence. Required full-suite verification and correction gate remain incomplete;
do not restart without developer direction. Source/test changes remain uncommitted.

Developer subsequently requested “commit changes”, authorizing the local commit
of the correction and records. This does not complete full verification or approve
the correction gate. No push authorized. Final whitespace check passed; only
documentation records changed after the recorded executable checks.

Later authorized parallel-test tooling supplied renewed complete verification:
129 passed with two workers (16m59s) and four workers (12m06s), including direct
and rebuilt wheel checks and installed initialization. All original product
assertions are unchanged. [Parallel evidence](parallel-test-execution.md) records
the approved development-only pytest compatibility constraint, final lock,
grouping regression, commands and logs. This supersedes the incomplete full-suite
status for technical verification; the cancelled serial result remains historical.
Correction gate still awaits developer review; no push or merge is authorized.
