# US-41 IP2 — Wheel initialization and identity

Status: Complete; Gate 2 approved on 2026-11-08 (“I approve ip2; commit changes”). Owning issue: [#64](https://github.com/jimthompson5802/agentic-ml/issues/64), M50.
Developer authorized “yes, I meant implement ip2” on 2026-11-08 UTC.
[Plan and Gate 1 contract](../plans/milestone-50-us-41.md) govern this phase.
Issue retrieval and final metadata refresh confirmed unchanged body, zero comments
across all pages and `updated_at=2026-11-08T18:02:47Z`.

## Implementation and public boundaries

`agentic_ml.initialization.initialize_project(InitOptions(...))` and the installed
`agentic-ml init` now accept a retained, normal local purelib wheel. Shared source,
lock and installed identity checks run before scaffold, journal, backups, locks,
writable probes or storage setup. Source names and dependency names are normalized;
PEP 440 versions, archive filename, lock locator/hash, archive METADATA and installed
origin/version/payload must agree. Relative paths resolve against explicit root.
The original full-SHA Git checks remain in the shared identity module.

The additive `environment.toolkit_identity` uses the approved 0.1 journal contract.
It is present in initial scaffold evidence and retained through environment setup.
Unknown, missing wheel or conflicting saved identity is rejected before rerun writes.
Legacy Git journals can acquire the additive identity after current Git validation.
Ordinary lock/sync stages recheck identity and retain the selected artifact.
Shared filesystem path checks moved to `initialization/paths.py`; public exports
and packaged resource paths are unchanged.

Tests install a genuinely built current wheel into separate experiment projects.
They invoke installed CLI and isolated Python API, including explicit root from
unrelated cwd, and assert actual scaffold, imports/resources, usable storage,
setup state and preservation of scientist edits, backups and wheel selection.
Failure tests damage native metadata before snapshots and call installed entrypoints
directly, without a uv wrapper that could repair the input. Snapshots include
project directories/files, Git files and installed toolkit payload/metadata;
installer bytecode and unrelated dependency files are excluded. No internal identity
collaborators are mocked. These are consistency checks in trusted local projects.

## Red–green evidence

Focused commands use serial pytest for short, isolated public-boundary TDD slices:
`uv run --locked pytest tests/integration/test_distribution_initialization.py -m milestone_50 -k SELECTOR`.
Raw logs and initial summaries live in
`.dev-records/verification/us-41-ip2-20261108/`. Expected missing-behavior red tests
are not failed corrective attempts. No problem exhausted the three-attempt limit.

| Slice / selector | Observed red | Green evidence |
|---|---|---|
| `cli_initializes` | 1 failure: valid wheel rejected by Git-only preflight | 1 passed; then CLI/API 2 passed in 17.65s |
| `api_rerun` | 1 failure: normalized `AGENTIC.ML` source key caused KeyError | CLI/API 2 passed in 17.65s |
| `payload_tampering` | 1 failure: changed installed resource accepted | All first 3 passed in 21.25s |
| `missing_archive` | 1 failure: reached sync after writes | Payload/archive 2 passed in 5.27s |
| `contradictory` | 4 failures: wrong/malformed archive hashes reached acceptance or sync | 5 archive cases passed in 12.41s |
| `unsupported_declaration and duplicate-dependency` | 1 failure: duplicate normalized dependency accepted | All 12 declaration cases passed in 28.86s |
| `invalid_installed and duplicate` | 1 failure: duplicate installed distribution accepted | All 10 installed metadata cases passed in 24.14s |
| `unsupported_wheel_layout and duplicate` | 1 failure: reached sync on duplicate ZIP member | All 7 layout cases passed in 19.77s |
| `invalid_locked and source` | 1 failure: generic error lacked wheel recovery | All 11 lock/archive cases passed in 28.81s |
| `wheel_symlink` | 1 failure: diagnostic did not identify symlink boundary | 1 passed in 2.71s |
| `saved_toolkit and unknown-kind` | 1 failure: invalid journal identity overwritten | All 4 journal cases passed in 38.65s |
| `project_identity_is_actionable and missing-pyproject` | 1 failure: no native wheel recovery guidance | All 6 metadata cases passed in 14.47s |
| `wheel_filename` | 1 failure: foreign filename reached lock after writes | Filename/CLI/wrong-environment 3 passed in 16.34s |
| `invalid_wheel_metadata and missing-name` | 1 failure: missing Name caused AttributeError | All 5 archive-metadata cases passed in 19.63s |

Additional matrix coverage includes editable/directory/sdist/URL/registry/source-list
rejection; duplicate normalized source and lock identities; missing or malformed
origin JSON and archive_info; wrong installed name/version/origin/environment;
missing/replaced/corrupt retained wheels; wrong filename/hash/version/locator;
unsafe traversal, absolute, backslash, symlink, duplicate, relocated `.data` and
non-purelib members; missing or inconsistent wheel Name/Version; completed reruns.
The native empty archive_info succeeds through independent payload comparison.

## Dependencies and checks

Product PEP 440 parsing imports `packaging`, now explicitly declared `>=24,<27`.
Both independent installed requirement inventories were updated. The intentional
`uv lock` changed only the root package dependency and requires-dist entries;
no resolved package version or artifact changed (196 packages). Original lock SHA-256:
`5f99c2da64eb46bc758f798f364e67eab25246253fc75315ebb404461e466a9d`.
Updated lock SHA-256:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Linux aarch64, Python 3.12.16, uv 0.13.6, pytest 9.1.1 / xdist 3.8.0.
Source baseline `dfd344d` plus the IP2 phase changes. macOS and Windows
were not verified.

| Command | Result |
|---|---|
| `uv sync --locked --group dev` | Passed; 196 resolved, 193 checked |
| `uv lock --check` | Passed; 196 resolved |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; 296 files |
| `uv run --locked mypy src tests` | Passed; 75 source files |
| `uv run --locked agentic-ml --version` | Passed; 0.1.0, matching wheel and installed metadata |
| `git diff --check` | Passed, including final documentation |
| `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_50` | Passed: 144 passed, 2 skipped; 146 selected; 345.03s; exit 0 |

Initial sandbox invocations of `uv lock`, locked sync and lock consistency could
not write the external uv cache; approved escalated reruns passed. One shell-wrapped
focused run failed before pytest for the same reason; direct documented invocation
ran successfully. A narrow mypy invocation omitted the tests helper search context;
the required complete `mypy src tests` command passed after correcting imports for
the shared paths module. Ruff import ordering and an unused import were corrected;
no check suppression or test exclusion was introduced.

Final M50 input was unchanged during executable verification. A subsequent
same-selection collection-only command,
`uv run --locked pytest --collect-only -q -m milestone_50`, did not run tests and
confirmed **882 collected, 146 selected, 736 deselected** in 1.25s. All 66 new
US-41 cases passed. Raw final output: `m50-gate.log` and `m50-collection.log`.
The two existing developer-authorized skips are
`test_failed_installed_probe_retains_available_environment` and
`test_rebuilt_probe_failure_retains_both_environments`; their unresolved timeout
coverage remains owned by the existing US-35/36/M50 records. The third existing
skip is outside this M50 selection. No assertion, timeout, scheduling group, skip
or marker policy was weakened.

Final relative file-target checks passed for this report, the plan and checkpoint.
No scope deviation or new unresolved implementation decision was required.
T1–T4 are technically Complete; Gate 2 was approved by the developer on 2026-11-08 (“I approve ip2; commit
changes”). Approval recording and this phase commit are authorized. No push or PR
is authorized; IP3 execution awaits direction. Approval recording changes only
documentation, so the existing executable verification remains applicable.

## Criteria and remaining verification

AC-02/03/04 have focused installed direct-wheel evidence. AC-06 is advanced by
this direct-wheel fixture only. Genuine sdist rebuilds, both artifact/interface
matrices and renewed Git/M1–6 regressions are deferred to **US-41-IP4-T1–T3**.
Explicit upgrade/refresh and incomplete-operation transition cases remain
**US-41-IP3-T1–T4**. The bootstrap/upgrade user guide remains IP3.
No standalone artifact driver or broader local pytest selection was run.

The approved archive-history limitation remains: installed payload/origin consistency
cannot distinguish two ZIP encodings with identical payload. Retained original wheel
bytes are mandatory; uv's empty installed archive hashes are not fabricated or
claimed to prove an archive hash. Existing historical M1/M50 milestone obligations
remain open; this phase does not accept the story or complete either milestone.
