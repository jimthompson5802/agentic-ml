# US-41 IP3 verification

Issue [#64](https://github.com/jimthompson5802/agentic-ml/issues/64), M50;
AC-01/03/04/05 advanced. Developer authorized “start ip3”, 2026-11-08 UTC.
Gate 3 Approved — developer “i approve ip3; commmit”, 2026-11-08 UTC. Public installed CLI/API and native uv boundaries are those
approved at Gate 1. Both-artifact/Git/M1–6 renewal remains IP4-T3.

Raw evidence: `.dev-records/verification/us-41-ip3-20261108/`.
Source base `404ba53`; Linux aarch64, Python 3.12.16. Lock before:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

## TDD and corrective attempts

Focused runs use serial pytest to isolate one installed transition and avoid
four copies of its wheel build. All use
`uv run --locked pytest tests/integration/test_distribution_initialization.py
-m milestone_50 -k SELECTOR --junitxml=RECORD/NAME.xml`, with stdout/stderr in
the corresponding `.log`. RECORD is the raw evidence directory above.

- `explicit_new_version`, `new-version-red`: 1 failed, 66 deselected; native
  upgrade succeeded but init rejected changed saved identity. Ordinary init and
  locked sync retained the old selection while a newer wheel was available.
  Initial sandbox invocation could not write uv cache; rerun with approval
  produced the intended behavioral failure.
- Attempt 1: permit a completed wheel journal to refresh after validating its
  shape and completion steps. `explicit_new_version or saved`,
  `new-version-green`: 4 passed, 1 failed, 62 deselected. Existing unchanged
  journal-tampering assertion detected acceptance of a changed digest at the
  same locator. Original failure/assertions preserved.
- Attempt 2: require a different locator for a changed completed identity.
  `explicit_new_version or saved`, `new-version-green-2`: 5 passed,
  62 deselected; exit 0. No suppression, skip, timeout or threshold change.
- `same_version_upgrade or verified_but_incomplete`, `incomplete-red`: same-version
  API upgrade passed. The interruption fixture initially retained completed
  stores and reached an unrelated storage ownership conflict. Corrected only
  fixture preparation to remove its owned stores before the snapshot.
- `verified_but_incomplete`, `incomplete-red-2`: 1 failed, 68 deselected;
  expected metadata rejection was absent and initialization succeeded. Added
  preflight checksums for incomplete operations even after environment verification.
  `incomplete-green`: 1 passed, 68 deselected, exit 0 (first corrective attempt).
- `failed_sync_marks`, `sync-red`: 1 failed, 69 deselected; a native uv shim
  returned 73 at sync and the old complete status survived. Added an incomplete
  status/pending-finalization record before synchronization writes. Renewal:
  `sync-green`, selector `failed_sync_marks or verified_but_incomplete or
  explicit_new_version or same_version_upgrade`: 4 passed, 66 deselected,
  exit 0 in 56.67s (first corrective attempt). This shim replaces
  only the external uv process boundary; installed toolkit code is unmodified.

- `malformed_prior_version`, `prior-version-red`: 1 failed, 70 deselected;
  a completed record with a different locator concealed an invalid prior version.
  Canonical PEP 440 validation now rejects it. `prior-version-green`: 1 passed,
  70 deselected, exit 0 (first corrective attempt).
- Four-worker public transition matrix, `transition-matrix`:
  `uv run --locked pytest -n 4 --dist=loadgroup
  tests/integration/test_distribution_initialization.py -m milestone_50
  -k 'incomplete_setup_cannot or stale_upgrade or recorded_git'
  --junitxml=RECORD/transition-matrix.xml`: 12 passed in 46.59s, exit 0.
  These are additional boundaries of the now-green behavior; no implementation
  change followed them. Staged journal fixtures represent interruption points,
  not proof of OS crash durability. The sync shim is an actual process failure.

## Coverage and commands

- IP3-T1 / AC-04/05: ordinary init and native locked sync preserve lock/artifact
  with a newer wheel present; a stale declaration fails pre-write API/CLI checks.
- IP3-T2 / AC-03/05: native `uv add REVIEWED_WHEEL`, `uv sync --locked`, then
  installed init refresh new-version (`0.1.1`) and same-version (`0.1.0`) identities
  from independently computed wheel hashes. CLI and unrelated-cwd API paths work.
  Same-version behavior was already green after the new-version slice; no
  artificial failing test was manufactured. Compatible project work and stores
  remain; original backups remain unchanged.
- IP3-T3 / AC-01/04/05: interrupted scaffold, lock, sync, environment-check, DVC,
  MLflow and state journal fixtures reject another artifact. Pending/missing
  finalization and unverified environment do not count as complete. Verified
  incomplete setup rejects metadata drift; failed sync resumes unchanged input.
  All rejections snapshot damaged inputs before invoking installed API/CLI.
  Recorded Git-to-wheel transitions fail. Genuine Git-to-wheel and reverse
  installed source fixtures remain part of IP4's Git/artifact renewal, rather
  than being inferred from this controlled journal fixture.
  `docs/experiment-setup.md` gives exact local-wheel bootstrap/upgrade commands,
  source limits, retained-artifact recovery and native mutation/rollback limits.

## Phase checks

- `uv sync --locked --group dev`: exit 0 (`sync.log`).
- `uv lock --check`: exit 0 (`lock.log`).
- `uv run --locked ruff check .`: exit 0 (`lint-final.log`).
- `uv run --locked ruff format --check .`: exit 0 (`format-final.log`).
- `uv run --locked mypy src tests`: exit 0; 75 source files (`typing-final.log`).
- `uv run --locked agentic-ml --version`: exit 0; `0.1.0` (`smoke.log`), matching
  installed project metadata and declared version.
- `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_50
  --junitxml=RECORD/m50.xml`: **161 passed, 2 existing skips in 397.20s**, exit 0.
  All 83 distribution initialization cases passed without skips/failures.
  Same-selection `--collect-only`: 899 collected, 163 selected, 736 deselected
  (`m50-collection.log`). Existing skips are
  `test_failed_installed_probe_retains_available_environment` and
  `test_rebuilt_probe_failure_retains_both_environments`; unchanged timeout
  ownership is documented in the development guide. Skips do not satisfy coverage.
- Relative file targets in all four changed documents passed; `git diff --check`
  passed. No new rule suppression or check exclusion.

Lock after is unchanged:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Retained focused replay, exit 0: **2 passed, 81 deselected in 32.95s**
(`retained-upgrades.log/xml`). Command:
`uv run --locked pytest tests/integration/test_distribution_initialization.py
-m milestone_50 -k 'explicit_new_version or same_version_upgrade'
--keep-test-workspaces --basetemp /tmp/us41-ip3-upgrade-evidence-20261108-1
--junitxml=RECORD/retained-upgrades.xml`.
Serial execution captures the two review examples without changing product inputs;
no implementation changed after M50. `upgrade-identities.json` retains five
wheel-file hashes and two completed installed identities, native origins,
environment metadata checksums and original-backup hashes. Independently rehashed
wheel bytes match both completed journals and installed origin locators.

| Retained example | Version | Artifact SHA-256 |
|---|---|---|
| New version | 0.1.1 | `7935fd21594c2c0acdc699225ca7076c7c7142f0b1c9ee7a40810b84fb7d1b14` |
| Same-version replacement | 0.1.0 | `b473228493ded7fbf0fa87001ee28d3c9ef38cce4bf4d805cd94a2f3a7f936d5` |

Ordinary pytest success trees were cleaned under repository policy. The focused
replay's exclusive `/tmp/us41-ip3-upgrade-evidence-20261108-1` is deliberately
retained for inspection; durable manifests are separately in the raw records.
`context.json`, `commands.json` and `summary.json` capture input identity,
commands, outcomes and cleanup. Gate 3 is **Approved** — developer “i approve ip3; commmit”, 2026-11-08 UTC;
T1–T4 are technically Complete. No story acceptance/publication is implied.

No dependency or lock change. Both genuine toolkit wheel paths, full-SHA Git
and M1–6 final renewal remain IP4-T1–T3; no standalone artifact driver or broader
local selection was run. Existing temporary skips and historical milestone
verification ownership remain unchanged. Linux observations do not establish
macOS/Windows support. The Gate 1 archive-history limitation remains accepted.
No scope deviation or new suppression/exclusion.

Approval recording changes documentation only; existing executable evidence remains
applicable. TDD and product test renewal do not apply to this approval record.
Final document/link checks and `git diff --check` passed. Developer authorized the
IP3 commit only; IP4 execution, story acceptance and publication remain pending.
