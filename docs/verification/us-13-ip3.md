# US-13 IP3: Installed native dataset versioning

Date: 2026-11-14 UTC. Owning [plan](../plans/milestone-1-us-13.md),
[issue #16](https://github.com/jimthompson5802/agentic-ml/issues/16).
Gate 3 approved, 2026-11-14; M1 slice accepted, 2026-11-14. AC-01/02 only;
AC-03/04 remain M2.

## Boundaries and implementation

Developer “start ip3” authorized IP3 after approved Gate 2. Complete issue body
and all comment pages refreshed: one unique comment (6699586819), matching count
1 and stable updated timestamp 2026-11-07T00:28:44Z; no milestone field or scope
conflict. Gate 1 native-only public boundaries remain applicable.

The existing assessment/splits driver retains its direct and genuinely
source-rebuilt wheel environments and child distribution inventory probes.
It copies the guide and native dataset-versioning oracle beside the isolated
installed probe. Each installed Python executes the guide-derived project script
and native DVC in separate CSV/Parquet experiment projects; there is no pytest
or checkout import in those environments. Existing assessment, splits, extraction,
quality, CLI, import-origin and package/resource inventory checks are preserved.
No product code, dependency, lockfile or packaged resource changed.

The installed oracle reuses IP2's independently defined expectations: literal
extracted/derived rows and supplied memberships in both layouts, exact Git
inventories, independent file digests against native manifest entries, actual
commits A/B, unchanged registration, per-artifact identity sensitivity and
retained content in cache/local remote (external and in-project remote cases).
Missing targets, Git-tracked data, duplicate ownership and controlled failed
transfer preserve native diagnostics/configuration and successful local registration.
The retained identity files include original A/B hashes and real commit IDs.

TDD: no new or corrected product behavior; this extends verification of existing
native capabilities through the confirmed installed boundary. Positive/boundary
checks apply without manufacturing a missing-product-behavior red.

## Verification

Tested baseline: `658c1525ffbb234f01d4e3101563475da9b45c8a` plus IP3 working tree.
Platform: Linux aarch64, Python 3.12.16, uv 0.13.6, DVC 3.67.1. No macOS/Windows claim.

- `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py::test_assessment_splits_from_both_artifact_paths`:
  1 passed in 43.83s; both installed paths and four recipe variants passed.
- `uv sync --locked --group dev`: passed, 196 resolved; 193 checked.
- `uv lock --check`: passed, 196 resolved.
- `uv run --locked ruff check .`: all checks passed.
- `uv run --locked ruff format --check .`: 306 files already formatted.
- `uv run --locked mypy src tests`: 77 source files passed.
- `uv run --locked agentic-ml --version`: 0.1.0, exit zero.
- `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/us-13-ip3-20261114/m1.xml`:
  722 passed, 1 existing skip, 4 native NumPy warnings in 233.24s; exit zero.
  723 selected. Collection inventory remains 991 from IP2 (no added test cases),
  giving 268 excluded cases; selected count independently reported by xdist.
- `uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/us-13-ip3-20261114/m1-6.xml`:
  722 passed, 1 existing skip, 4 native NumPy warnings in 222.86s; exit zero.
  723 selected; same inventory/268 exclusions as M1. M1 and default M1–6
  currently select the same cases; neither is the complete infrastructure suite.
- Relative file-link targets checked in changed documents; `git diff --check` passed.

The selected skip is
`test_missing_planning_schema_fails_installed_inventory@distribution`, retained
under the developer's 2026-11-03 timeout-diagnosis exception. No skipped coverage
is counted as passing. Other historical infrastructure skips/exclusions remain
owned by their plans and M1/M50 milestone reconciliation. Four warnings are
native NumPy operations in the existing infinite-numeric-target assessment case;
no warning suppression was added.

## Criterion results and approval

| Criterion | Independent evidence | Result |
|---|---|---|
| US-13-AC-01 | Both installed paths, both input formats/layouts, literal extraction/partition/derived outputs, native identities and real committed A/B history | Accepted, 2026-11-14 |
| US-13-AC-02 | Exact Git inventory/exclusions, project settings and pointers, independent cache/remote bytes for both versions, native failure/configuration boundaries | Accepted, 2026-11-14 |
| US-13-AC-03/04 | M2 restoration/hash and missing/corrupt guarantees | Deferred to M2 |

IP3-T1–T3 are technically complete. Developer “i approve ip3; commit”, 2026-11-14, approved Gate 3 and authorized
committing the IP3 package. Developer “i accept the us-13”, followed by “commit”, 2026-11-14,
accepted the delivered M1 AC-01/02 slice and authorized a local record commit;
whole-story completion requires M2. Issue #16 stays open. No push/publication
is authorized. Approval-record edits change no executable behavior; retained
verification remains applicable, with renewed relative-link/whitespace checks.


Raw focused records:
`.dev-records/verification/20261114T145413Z-658c1525ffbb-56b45fe7cf3d4feb832bddc55316c320/`
(parent commands, outputs and direct/rebuilt assessment/versioning identities),
and linked child
`20261114T145413Z-658c1525ffbb-c820da7395b54fcea42d1799d3f5a034/`
(artifact digests, installed origins, inventory and CLI). Parent cleanup complete;
child environments retained until the parent finished, then removed.
Focused direct/rebuilt wheel SHA-256 (equal bytes from independently built paths):
`9fdd321a198668f50b1d0de2b6e80f6ee5582613a5baa4aa9b6fc2cd084c18b3`.
Sdist SHA-256:
`40760513c8b87659d9c195288da6349aceef8344006e522feb2f403aeeb82245`.
Both installed paths report toolkit 0.1.0 and DVC 3.67.1; separate installed
prefix/origin records remain authoritative. Lock SHA-256 before/after:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Additional final check records: `.dev-records/verification/us-13-ip3-20261114/`:
JUnit reports, lock/platform/results baseline and `installed-runs.json` linking
all three successful parent/child installed invocations. Final M1 parent:
`20261114T150018Z-658c1525ffbb-1cfae943599e4449ad194a687ed44efa`;
final M1–6 parent:
`20261114T150408Z-658c1525ffbb-bf8a32dca22b4d17872d419f5d9a3026`.
Each preserves both installed paths and reports successful cleanup.

Initial sandbox pytest and lock-check launches could not write uv's cache.
Approved unrestricted reruns succeeded; these are execution-environment failures,
not failed product verification. No corrective product attempts or suppressions.

## Limits and handoff

The [guide](../dataset-versioning.md) is linked from README, extraction and split
guidance. Active design/traceability record installed evidence with acceptance
pending. US-39 can consume its project code/settings and artifact paths; US-26
owns MLflow links and US-27 native stages. No stage/training/assistant/replay claim.
M2 restoration, historical M1/M50 acceptance obligations and revised MVP milestone
integration remain open. No broader pytest or standalone artifact driver launched.
