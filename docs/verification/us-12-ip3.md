# US-12 issue #15 — IP3 verification

IP3 authorized by developer “start ip3”, 2026-11-07 UTC, on
`US-12-data-validation`, clean baseline `1c34871`. Gate 2 was approved.
Gate 1 confirmed the public installation boundaries. Developer “i approve gate 3”, 2026-11-07 UTC, approved Gate 3. Developer “i accept issue #15”, 2026-11-07 UTC, accepted the issue slice.

## Scope and boundaries

Issue #15 owns US-12-AC-01/05; #19 owns AC-02/03 and deferred AC-04.
Complete bodies and all comment pages were refreshed: one unique comment each
(6699586004 and 6699588996); final counts/timestamps matched initial metadata.
Published scope and saved plan sources agree. GitHub milestone is unset; body
assigns M1. No GitHub writes occurred.

The new M1 distribution test reuses the existing artifact fixture/group and
invokes `verify_data_quality.py` from an unrelated cwd. The driver composes
unchanged normal distribution verification, copies project code/probe and uses
each independent installed Python with `-I`. Existing CLI, resource inventory,
runtime dependency and origin verification precedes the quality checks. No source,
dependency, lockfile or packaged-resource changes were needed.

Project code extracts literal CSV rows through `extract_data`, then uses installed
`validate_data` / `run_validated_step`. Independently specified measurements cover
all seven rule families and one failure per family. Strict JSON roundtrip,
required blocking, advisory and explicit no-check execution, consumed values,
caller data/settings/rules preservation, malformed declaration rejection and
original operation exception identity/stage note are checked. Sentinels are
project-owned files. This proves the helper boundary; future runners still need
integration tests, and arbitrary project code is trusted.

## TDD and checks

A short serial installation-boundary TDD cycle reused the approved seam.
`uv run --locked pytest tests/integration/test_distribution_verification.py -k data_quality_from_both_artifact_paths`
first failed: 1 failed, 17 deselected in 1.19s because the planned driver was
absent (artifact build succeeded). After adding the project/probe/driver it passed:
1 passed, 17 deselected in 11.95s. No product defect or corrective attempt was
needed. This is installation coverage for existing approved behavior, rather
than a new product API. Console transcripts were not retained as raw logs.

Initial installed identities and retained driver command logs:
`.dev-records/verification/20261107T154057Z-1c34871ce653-45bf3bcbc1f0411ba108b8e3861eba2a/`.
Both paths use agentic-ml 0.1.0, pandas 3.1.1 and pyarrow 25.0.1.
Per-path identity files contain reports, failure observations, extraction
provenance, project/import/cwd paths and environment versions. Child records
retain wheel/sdist/rebuilt hashes and runtime identities. Parent cleanup passed.

Shared checks passed: locked dev sync, `uv lock --check`, Ruff lint/format
(266 files), strict mypy (65 files), CLI smoke (`0.1.0`), whitespace.
Sync/lock/format initially hit sandbox read-only uv-cache errors; escalated
retries passed. No changed dependency resolution or suppressed checks.
77 local links and anchors passed; all changed-guide Python examples passed syntax checks.

M1 gate: `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1
--junitxml=.dev-records/verification/20261107-1c34871-us12-ip3/m1.xml`
passed: 528 passed, 1 existing skip in 218.88s; 529/631 selected,
102 excluded. Final M1–6: `uv run --locked pytest -n 4 --dist=loadgroup
--junitxml=.dev-records/verification/20261107-1c34871-us12-ip3/m1-6.xml`
passed: 528 passed, 1 existing skip in 220.48s; 529/631 selected,
102 excluded. The skip is the existing missing-planning-schema case.
Both selections reran the installed quality scenario successfully.

## Identities and limitations

Linux aarch64, Python 3.12.16, uv 0.13.6. Other platforms unverified.
Lock SHA-256 before/after:
`4b21570fb52b7a4eea94c5d85404e95afefe2d7c44eab014f2122fc9793d847b`.
Phase records: `.dev-records/verification/20261107-1c34871-us12-ip3/`.
Initial console-only observations are summarized in `session-evidence.json`;
raw driver command logs and identities remain in linked driver records.

M0/M50/M99/infrastructure are outside automatic phase/story selections. Preserve
historical M1-ACCEPT-VERIFY, M50-ACCEPT-VERIFY and all three existing temporary
skip obligations. No full-suite or standalone artifact command was run.
No assessment/splits, model training, DVC, notebook, assistant, or complete
experiment/milestone acceptance is claimed. No publication authorized.

## Criterion disposition and gate

US-12-AC-01 is technically verified by the literal seven-family positive/failure
reports and extraction-to-quality installed checks. US-12-AC-05 is technically
verified by required/advisory/no-check sentinels, error reports and process-error
separation. IP2 owns the broader edge-case matrix. T1–T4 are complete; Gate 3 is approved. Issue #15 accepted by developer “i accept issue #15”, 2026-11-07 UTC. #19 remains open and outside this slice.
No new suppression, skipped case, assertion weakening or product workaround.
