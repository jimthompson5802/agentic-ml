# US-41 IP4 verification

Issue [#64](https://github.com/jimthompson5802/agentic-ml/issues/64), M50,
US-41-AC-01–06. Developer “start ip4”, 2026-11-08 UTC, authorizes IP4 only.
Gate 3 is approved and committed as `a1f0b15`; Gate 4 Approved — developer “I approve ip4; commit”, 2026-11-08 UTC.
Developer accepted US-41 on 2026-11-08 — “i accept the story”. Complete issue body and all comment pages refreshed: zero
comments, unchanged update timestamp `2026-11-08T18:02:47Z`.

## Boundaries and changes

Public boundaries remain those approved at Gate 1: isolated installed CLI/API,
explicit project root from unrelated cwd, native declaration/lock/origin and
independent retained-artifact digests, project/store preservation and pre-write
failure snapshots. No product implementation changes. Existing behavior is
verified with additional artifact and legacy regression coverage; no artificial
failing test is appropriate. Historical red–green evidence remains in IP2/IP3.

The wheel fixture now builds genuine wheel/sdist outputs in an isolated source
copy. The rebuilt variant extracts that sdist with the data filter and builds
from the extracted source. Every existing US-41 case runs separately against
each variant, including both interface successes/reruns, identity/layout/payload
failures and native new-version/same-version upgrades. No origin is fabricated.
Raw build commands/output and independent sdist/wheel hashes are retained in
`.dev-records/verification/us-41-ip4-<unique-id>/commands.json` and
`artifacts.json` for each worker fixture. Ordinary successful pytest workspace
cleanup remains active; durable records are outside it.
The phase `artifacts.json` aggregates eight worker manifests: four per path.
All produced wheel SHA-256 values are
`3eb1f07bc6e159551dacb7227e639a39566fddb1f513a8d2d1ab11d71d9163c5`.
Matching reproducible bytes do not substitute for the rebuild: each rebuilt
manifest has a separate successful build command with extracted-source cwd.

Git regressions additionally exercise complete journals without the additive
identity and incomplete storage-stage legacy journals, including metadata drift.
Existing modern journal cases, assertions, timeouts and failure injection remain.
Two further installed regressions use native uv to switch actual Git/wheel
installations in both directions, retaining the completed prior journal. They
assert an actionable source-kind error and unchanged project-file snapshots.

## Checks and attempts

Raw phase records: `.dev-records/verification/us-41-ip4-20261108/`.
Linux aarch64 / Python 3.12.16 / uv 0.13.6; source base `a1f0b15` plus
verification/document changes. Lock before:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Initial uv commands could not write the sandbox-external cache; approved
execution succeeded. Locked synchronization and lock consistency passed.
Initial lint detected import ordering; corrected with Ruff. Initial formatting
check of the added Git regression required wrapping one assertion; formatted.
Renewed lint, formatting and strict mypy passed (75 source files); CLI smoke
printed `0.1.0`. No product failure or corrective implementation attempt so far.
No suppression, timeout, skip, assertion, dependency or lock change.

M50 passed: `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_50`:
**244 passed, 2 skipped in 546.05s**, exit 0; 246 selected. All 166 US-41
cases (83 per genuine artifact path) passed. Output retained in `m50.log`.
The final seven additional Git regression cases were added after M50 collection;
they carry only M1 and do not affect its selection or wheel inputs.
M1–6 passed: `uv run --locked pytest -n 4 --dist=loadgroup
--junitxml=.dev-records/verification/us-41-ip4-20261108/m1-6.xml`:
**720 passed, 1 skipped, 4 warnings in 268.87s**, exit 0; 721 selected.
The four warnings are native NumPy invalid arithmetic in the existing
`test_infinite_numeric_target_retains_explicit_frequency_values`; no test failed.
JUnit and `m1-6.log` preserve the results, including complete/incomplete legacy
Git cases and both real installed source-kind switches.

Final-input collection-only commands use the same selections with
`--collect-only -q`: **989 total**, M50 **246 selected / 743 deselected**;
M1–6 **721 selected / 268 deselected**. Both exited zero. Combined collection
output was truncated; the separate M50 capture preserves its full inventory.

Shared final commands (exit zero; `shared.log`):

- `uv sync --locked --group dev`
- `uv lock --check`
- `uv run --locked ruff check .`
- `uv run --locked ruff format --check .`
- `uv run --locked mypy src tests` (75 source files)
- `uv run --locked agentic-ml --version` (`0.1.0`, matching distribution metadata)
- `sha256sum uv.lock` (same before/after digest above)
- `git diff --check`

581 relative documentation file targets and final `git diff --check` passed. No executable
package or artifact inputs changed during this phase. Only verification fixtures
and documentation changed; source-wheel and final default regression evidence
therefore refer to the same product bytes.

## Acceptance reconciliation

| Criterion | Passing evidence |
|---|---|
| AC-01 | `docs/experiment-setup.md` native Git/uv init and local `uv add` bootstrap reproduced by each independent wheel project fixture; no toolkit checkout dependency |
| AC-02 | CLI and public API success plus compatible reruns on both wheel paths; explicit root/unrelated cwd, custom files, original backup, scaffolds and real local stores |
| AC-03 | Both paths compare independent retained-wheel digests with native lock, origin, installed payload/version and completed journal; missing/contradictory identities fail |
| AC-04 | Both paths' declaration/lock/install/layout/payload damage matrix snapshots inputs before direct installed CLI/API; no automatic identity repair; selected dependency preserved |
| AC-05 | Both paths run native new-version and same-version upgrades; ordinary init/locked sync retain selection; custom work/stores/backups survive; incomplete states reject drift |
| AC-06 | All 83 cases pass for each artifact path; genuine extracted-sdist rebuild commands retained; full-SHA Git installed driver and initialization regressions pass in M1–6, including legacy complete/incomplete journals and actual source switches |

No criterion is deferred. Technical evidence satisfies the planned scope;
Gate 4 Approved on 2026-11-08 — developer “I approve ip4; commit”.
Developer accepted US-41 on 2026-11-08 — “i accept the story”.
All planned IP4 tasks are technically Complete.

M50 skips remain `test_failed_installed_probe_retains_available_environment`
and `test_rebuilt_probe_failure_retains_both_environments`. M1–6 skips
`test_missing_planning_schema_fails_installed_inventory`. These are the three
pre-existing authorized timeout skips documented in the development guide;
none covers a US-41 matrix case. M0/infrastructure-only tests and standalone
artifact drivers were not run separately. The selected tests invoke real
artifact verification internally, with their own durable records/cleanup.
Historical milestone-wide obligations remain with their existing owners.

## Limits and approval

Gate 4 is Approved; developer accepted the story on 2026-11-08. Historical M1-ACCEPT-VERIFY
and M50-ACCEPT-VERIFY obligations remain open. Existing temporary skips retain
their owners and do not establish coverage. Linux observations do not verify
macOS/Windows. The Gate 1 archive-history limitation remains: matching installed
payload/origin cannot distinguish ZIP encodings with identical payloads.
No standalone artifact invocation or broader local suite is authorized here.

Approval recording is documentation only; existing executable evidence remains
applicable. Relative-link and `git diff --check` checks passed. Developer
authorized committing IP4 and approval records. Subsequent developer story
acceptance authorizes publication under execute-plan; publication results are
recorded in the owning plan.
