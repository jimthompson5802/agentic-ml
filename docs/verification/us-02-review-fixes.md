# US-02 IP4 review corrections

Issue #9, Milestone 1, AC-02/04/05. Developer authorized “resolve these findings”
on 2026-10-31. Issue body and all comment pages refreshed: zero comments;
metadata refresh confirmed unchanged `2026-10-31T01:15:38Z`. The API milestone
field is null; the issue body assigns Milestone 1. No new scope decisions.

## Boundaries and corrections

Reuse the plan's approved installed CLI/API boundaries in separate pinned
experiment projects. Observe exit status, preserved project and external bytes,
absence of scaffold/journal/lock writes, and successful corrected retry. No private
helper assertions or internal mocks. These checks do not establish isolation from
concurrent hostile filesystem mutations or verify other platforms.

P1: backup-directory symlinks/non-directories and file symlinks/non-files or
conflicting contents must be rejected before durable writes. Byte-identical
existing backups remain compatible. P2: configurable storage must not overlap
initialization journal, lock or backup destinations, including their ancestors
and descendants.

## TDD and attempt record

- P1 initial test setup failed because fresh `uv init` does not create `.gitignore`;
  fixture now explicitly supplies one. This was not a behavior red.
- P1 behavior red wrote all three originals through the backup directory symlink,
  replacing the external sentinel. The first run printed failure but was
  interrupted during pytest's slow cleanup of old temporary environments (exit
  130); the stack showed `_pytest/tmpdir.py` / `shutil.rmtree`. Five green cases
  printed 100% before the same cleanup delay. Dedicated `--basetemp` directories
  retain fixtures and avoid unrelated old-environment cleanup; no test is excluded.
- P1 corrective attempt 1: preflight directory and all three backup destinations
  before acquiring the setup lock, checking types, symlinks and original bytes.
  Clean red: `uv run --locked pytest tests/integration/test_initialization.py -k
  'unsafe_backup and directory-symlink' -q --basetemp=/private/tmp/us-02-backup-red
  --junitxml=/private/tmp/us-02-backup-red.xml`: 1 failed in 68.87s, exit 1;
  initializer incorrectly returned success (0). For this evidence rerun only the
  new preflight call was temporarily removed; it was restored before green.
  Green: `uv run --locked pytest tests/integration/test_initialization.py -k
  unsafe_backup -q --basetemp=/private/tmp/us-02-backup-green
  --junitxml=/private/tmp/us-02-backup-green-final.xml`: 5 passed, exit 0 (12.61s).
- P2 red: `uv run --locked pytest tests/integration/test_initialization.py -k
  storage_cannot_overlap -q --maxfail=1 --basetemp=/private/tmp/us-02-metadata-red
  --junitxml=/private/tmp/us-02-metadata-red.xml`: 1 failed, exit 1 (44.23s).
  Expected preflight rejection; actual MLflow failure left a stranded journal.
- P2 corrective attempt 1: add journal, lock and backups to the protected paths
  checked for equality and bidirectional containment. Same selector without
  `--maxfail=1`, `--basetemp=/private/tmp/us-02-metadata-green`, XML
  `/private/tmp/us-02-metadata-green.xml`: 28 passed, exit 0 (64.69s).
- Added a positive installed API-rejection / corrected CLI-retry check with all
  three matching backups: `uv run --locked pytest tests/integration/test_initialization.py
  -k rejected_storage_override -q --basetemp=/private/tmp/us-02-review-retry
  --junitxml=/private/tmp/us-02-review-retry.xml`: 1 passed, exit 0 (43.31s).

## Verification

macOS / Python 3.12.15. `uv sync --locked --group dev`, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked ruff format --check .` (79 files),
`uv run --locked mypy src tests` (20 source files), `uv run --locked agentic-ml
--version` (0.1.0), and `git diff --check` passed. Initial formatting check identified
two files; the documented formatter corrected them and recheck passed. Cache
sandbox denials on sync, lock check and the full-suite command were retried with
approved escalation; these are infrastructure failures, not behavior reds.

Full suite (119 collected, including normal distributions and complete
initialization from direct and sdist-rebuilt wheels) passed: **119 passed**, exit 0,
1898.17s (31:38). Command:
`env MLFLOW_DISABLE_TELEMETRY=true DVC_NO_ANALYTICS=1 uv run --locked pytest
--basetemp=/private/tmp/us-02-review-suite
--junitxml=/private/tmp/us-02-review-suite.xml`.

Both artifact paths passed normal installed checks and complete fresh CLI /
existing-package API initialization and reruns. Retained artifact workspace:
`/private/tmp/us-02-review-suite/test_complete_initialization_f0/initialization`.
All 34 added regressions passed in the full suite. The harness lock remained
`b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`; no
runtime/development dependency changes, suppressions, disabled tests or unresolved
failures. Sixty-one local Markdown link paths and final whitespace checks passed.
No new Linux/Windows evidence. Neither fix establishes concurrent hostile
filesystem isolation; initialization remains setup-only.

P1 and P2 each required one corrective implementation attempt and passed the
original regressions plus the full suite. The fixture correction, formatter pass
and infrastructure retries above are retained explicitly.

Historical IP4 approval remains recorded. Correction review approved by developer
message “i approve” (2026-10-31); whole-story acceptance remains pending.
No commit or publication authorized. Approval-record updates are documentation-only;
`git diff --check` passed and no executable changes followed full verification.


US-02 subsequently accepted by developer message “i accept us-02” (2026-10-31).
This supersedes the pending acceptance/publication status above and authorizes
the execute-plan commit/push/PR/static-review workflow. No executable changes
followed the 119-test verification.
