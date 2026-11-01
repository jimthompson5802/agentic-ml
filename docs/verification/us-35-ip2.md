# US-35 Implementation Phase 2 evidence

Issue: [#47](https://github.com/jimthompson5802/agentic-ml/issues/47).
Plan: [US-35](../plans/milestone-50-us-35.md).
Execution authorized 2026-11-01: “you can start ip2”. Issue body retrieved,
all comment pages returned zero comments, metadata refresh unchanged.

## Consumer inventory and public boundaries

The approved subprocess CLI and lifecycle API boundaries remain applicable.
Direct selectors: `tests/integration/test_verification_lifecycle.py` and
`tests/integration/test_distribution_verification.py`; renew installation tests
if the shared helper changes. Four-worker `loadgroup` at the gate; serial focused
red/green cycles avoid worker startup. Existing marked initialization acceptance
test stays reserved for M50-ACCEPT-VERIFY.

Distribution owns direct-wheel, rebuilt-wheel and its private cache. It preserves
extracted source, rebuilt artifact and project files. Its final consumer is the
second installed probe for standalone use. Parents request `--keep-workspace`
and an exclusive `--workspace` beneath their own workspace. Before launching the
child, the parent reserves only those three known disposable paths; it never
claims the entire source-containing child workspace. `Invocation.run` captures
created directory identities even on command failure. Child records name their
parent records and parents preserve/report the child record location. Only parent
finalization removes those paths, after every downstream consumer.

Initialization additionally reserves each of four fresh/existing project `.venv`
paths before uv creates them. Its last consumers are the rerun probes. Preserve
Git source fixture and project/store files. Planning creates no extra environments;
its final consumers are both installed planning probes. An existing caller planning
directory gets a uniquely created child; its sentinel/files are never adopted.
All commands use private invocation caches; inherited shared cache sentinels stay
untouched. No early wheel release, environment reuse or pytest retention changes.

Existing distribution tests inspect output only; the reserved initialization test
also inspects surviving project files (these are preserved by selective cleanup).
CI has no downstream workspace consumer. New real parent tests cover lifecycle
success/retention and failures after a successful child, without replacing the
reserved complete-initialization acceptance test. Filesystem fault injection at
the public helper boundary covers ownership and cleanup failures.

## TDD and checks

Focused commands use `uv run --locked pytest <node-id> -q`, serial for short
TDD diagnosis. Permission-denied uv cache attempts were retried through normal
escalation; they are not behavioral failures.

| Slice | Red | Green |
|---|---|---|
| Distribution `test_both_installed_wheel_paths_pass` | 1 failed in 10.01s: real verification passed, direct environment remained | 1 passed in 37.04s; both environments absent and identities survive |
| Distribution explicit retention | Already supported after integration; added CLI boundary coverage | 1 passed in 27.68s; both interpreters, parent link and three artifact hashes |
| Helper `test_child_record_locations_survive_child_failure` | 1 failed in 0.14s: missing `child_records` | All 24 helper cases passed in 5.95s |
| Distribution `test_rebuilt_probe_failure_retains_both_environments` | 1 failed in 23.55s: both environments retained, but incomplete rebuilt identity absent | 1 passed in 22.69s after persisting an explicit unavailable manifest before the probe |
| Distribution `test_planning_from_both_artifact_paths` | 1 failed in 29.77s: child cleaned interpreter before downstream probe | 1 passed in 45.51s; final parent cleanup, preserved linked child records |

Initialization `test_initialization_cleans_after_final_consumer`: red **1 failed
in 247.97s** after every original initialization/rerun probe passed; four project
environments remained. Green: **1 passed in 273.39s**, all six environments removed after final probes, four pinned project identities and child wheel identities preserved. Final four-worker checks passed: 58 tests in 419.99s.


Additional planning matrix: explicit retention/caller/shared-cache test and early
failure passed. Downstream-failure test initially selected the child summary
instead of the parent (1 failed, 2 passed in 75.83s): TextIO `readline` read-ahead
hid the parent RECORDS line from `communicate`. Correction attempt 1 changes
only the subprocess test reader to unbuffered descriptor bytes; original outcome
and retention assertions remain intact. Reverification: all four parent early/downstream failure cases passed in 50.70s. No assertion or probe changed.

## Phase gate verification

Changed executable modules: `tests/verification_support.py`,
`tests/packaging/verify_distributions.py`, `tests/installation/verify_initialization.py`
and `tests/installation/verify_planning.py`. Product source and installed probes
are unchanged. Shared helper renewal includes all installation driver tests.

The final direct command is:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_verification_lifecycle.py tests/integration/test_distribution_verification.py tests/integration/test_installation_verification.py --junitxml=.dev-records/verification/us-35-ip2-checks/final-direct.xml --durations=20
```

Collection: **59 cases, 58 selected, 1 deselected** (existing reserved milestone
initialization test). Selection maps 31 lifecycle/helper/parent cases, 14 direct
distribution/parent cases and 13 installation/probe cases. These directly cover
changed command lifecycles and helper behavior; they do not establish full-suite
coverage. The real probes retain every original assertion and subprocess timeout.
Parent initialization tests independently exercise lifecycle success and explicit
retention; they do not unmark or replace the reserved acceptance test.

Final result: **58 passed in 419.99s (6m59s)**, four workers, no failures.
Collection separately confirmed one reserved case deselected. Raw records:
`/Users/jim/Desktop/genai/agentic-ml/.dev-records/verification/us-35-ip2-checks/`.
Input hashes are in `input-identities.json`, JUnit in `final-direct.xml`, shared
command outputs in named JSON files. Per-invocation records include exact args/cwd,
stdout/stderr, platform/tool versions, source revision `2e3bf2d` with changed paths,
artifact checksums, installed manifests and independent verification/cleanup status.

| Shared check | Result |
|---|---|
| `uv sync --locked --group dev` | Passed; 193 packages checked |
| `uv lock --check` | Passed; 195 packages resolved |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; 125 files |
| `uv run --locked mypy src tests` | Passed; 39 source files |
| `uv run --locked agentic-ml --version` | Passed; `0.1.0` |
| `git diff --check` | Passed again after final record edits |

Lock SHA-256 before checks:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
Final hash comparison passed; every recorded executable/test input hash also
matched after the final run. No dependency, packaging metadata, lockfile,
product source or runtime guidance changes. Documentation-only edits use local
link/usage/whitespace inspection; TDD does not apply to prose. All 47 local
document links resolve, and all four driver `--help` commands passed from
`/private/tmp` with workspace/retention flags present.

## Fixed-workload comparison

Replay uses the exact baseline commands, cwd, local source fixture SHA
`5b4717c8c6ab4c56866ddf909cd9a83686ef22da` and original wheel/sdist. The replay
asserts every original artifact hash and the source fixture HEAD before execution;
it never rebuilds or substitutes inputs. Source/artifacts were revalidated as
available. Baseline workspaces and raw evidence are preserved.

Baseline records: `.dev-records/verification/us-35-baseline-bac0e9c/`.
Replay script, literal commands, logs, measurements and new record links:
`.dev-records/verification/us-35-ip2-workload/`.

All four replay commands exited zero. Both owned private caches and every
registered environment were absent at completion; all parent/child records and
identity checksum sidecars survived and matched. Historical baseline roots remain.

| Command | Retained environments before → after | Logical workspace bytes before → after | Allocated KiB before → after | Durable record bytes after | Replay elapsed |
|---|---|---|---|---|---|
| installation | 1 → 0 | 546756987 → 1643807 | 591388 → 1684 | 834073 | 25.21s |
| distribution | 2 → 0 | 1092870887 → 2670767 | 1185752 → 2984 | 41832 | 18.35s |
| initialization | 6 → 0 | 3516923616 → 16644454 | 3815600 → 18252 | 3357483 | 360.51s |
| planning | 2 → 0 | 1093357756 → 3134389 | 1187800 → 5000 | 53047 | 51.98s |

Measurements enumerate `pyvenv.cfg`, sum logical file sizes
excluding symlinks, and run `du -sk` after each sequential command. Nested child
workspaces now live under parents, so only outer roots are summed to avoid double
counting. Durable parent and child records are measured separately. MacOS/APFS
allocated KiB include block rounding, clones/hardlinks, compression and sparse-file
effects; logical bytes are not unique physical storage. Shared cache size is
outside the comparison. The old workload inherited shared caches; new commands
use private caches and remove them on success. Elapsed times are observations
under concurrent verification load, with no runtime or peak-disk improvement claim.

## Acceptance and limits

US-35-AC-01: per-command success reaches every real downstream probe before
owned environment/cache removal. AC-02: absolute durable records preserve commands,
logs, artifact checksums and installed identities; parent/child records link both
ways. Initialization adds four pinned-origin/dependency manifests and preserves
locks/declarations; distribution records both genuine wheel paths. Incomplete
identities are explicit. AC-03: all four commands support explicit successful
retention and retain available failed environments. AC-04: ownership is reserved
before creation, includes exact directory identities, rejects replacement/symlink
redirection and never adopts source/caller/shared-cache roots. Helper filesystem
fault injection checks cleanup and record-write failures separately from original
verification outcomes. AC-05: automated matrix plus fixed-input disk comparison.
All five criteria are verified by the final direct tests, shared checks, fixed-input measurements and retained records.

Only observed macOS 15.7.9 arm64 / Python 3.12.15 behavior is claimed. Linux and
Windows were not run locally. Forced termination can leave incomplete records,
buffered output and environments; no automatic finalization guarantee. Backups of
ignored durable records remain the contributor's responsibility. No historical
cleanup, pytest retention, environment reuse or early path release was implemented.

`M50-ACCEPT-VERIFY` owns unchanged product initialization/planning/approval caller
regressions, parallel scheduling regressions, full local suite and the existing
reserved milestone acceptance test. Existing `M1-ACCEPT-VERIFY` obligations remain
in their owning plan. No full-suite or milestone acceptance claim is made.

Phase 2 gate approved on 2026-11-01: “i approve ip2; commit”. Whole-story
developer acceptance remains pending. No scope change,
suppression, skipped test, assertion relaxation or timeout change was introduced.

## Phase outcome

US-35-IP2-T1–T6 are technically complete. All required direct/shared checks and
fixed-input replay passed. The one test-reader correction passed on its first
corrective attempt; no unresolved failed problem or scope deviation remains.
Final-input JUnit, shared command outputs, an invocation index and hash audit are
retained in the checks directory. This is selected phase verification, not a full
local suite. Developer approved Phase 2 and authorized its commit on 2026-11-01:
“i approve ip2; commit”. Whole-story acceptance and publication remain pending.
Approval-record edits change no executable behavior; existing test evidence is
reused, with local link and whitespace checks renewed.
