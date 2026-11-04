# US-05 IP3 — Installed validation and final verification

Date: 2026-11-04. Status: complete; IP3 approved and whole story accepted, 2026-11-04.
Owning [plan](../plans/milestone-1-us-05.md),
[issue #11](https://github.com/jimthompson5802/agentic-ml/issues/11),
Milestone 1, US-05-AC-01–05.

Developer “start ip3” authorized this phase after approved IP2. Baseline clean
`US-05-configuration-validation` at `3eefd55`. Complete issue body/metadata and
all comment pages retrieved with the repository helper; zero unique comments
matches reported count. Final refresh unchanged at `2026-10-30T02:06:23Z`.
No GitHub milestone object; body assigns M1. Scope and approved D7 boundaries
remain unchanged.

## Boundaries and implementation

The existing public distribution command checks independent installed schemas
and registry inventory. The public planning driver now invokes installed
`agentic_ml.validation` configuration/candidate/inspection APIs and CLI from a
separate project and unrelated cwd, once per direct and sdist-rebuilt wheel.
A project-owned helper runs isolated Python against installed public APIs.
Existing dependency inventory, identity manifests, group isolation and cleanup
are preserved. No product Python or dependency changes were needed.

AC-01: unsupported algorithms, task mismatch, unknown parameters, boolean/integer
confusion, incompatible constant strategy, valid classifier and regressor.
AC-02: empty categories and nonpositive log bounds rejected; integer and float
candidate bounds/types checked, inclusive valid endpoints.
AC-03: fixed strategy and omitted null defaults materialize exactly; attempts to
change fixed strategy or omit searched values rejected; lock drift blocks reuse.
AC-04: API and CLI diagnostics/blocked exits, corrupted registry evidence blocks
inspection/candidates; valid configuration explicitly denies execution authority.
AC-05: same public candidate interfaces used through CLI, API and project helper.
The IP2 public matrix supplies remaining exhaustive category/range/equality cases.
These probes never start training, read datasets or execute notebooks.

The [usage guide](../configuration-validation.md) documents reproducible examples,
registry inventory/version semantics, defaults, diagnostics and preserved evidence.
Future runners must revalidate live plan/configuration/registry/candidate before
side effects and enforce independent authorization, access and budgets. Metadata
checks do not isolate unrestricted kernels or establish training compatibility.

## TDD and corrective evidence

Raw JUnit records: `.dev-records/verification/us-05-ip3/`.
Focused serial red/green used to shorten one damaged-wheel feedback cycle; full
gates use four workers with loadgroup. This phase expands verification of existing
product behavior; no artificial failing product tests were manufactured.

1. Red: `uv run --locked pytest tests/integration/test_distribution_verification.py::test_missing_validation_schema_fails_installed_inventory -q --junitxml=.dev-records/verification/us-05-ip3/red.xml` — failed in 17.43s because a wheel missing candidate.json incorrectly passed the installed inventory (return code 0).
2. Green: same selector with `green.xml` — 1 passed in 8.51s after adding independent schema inventory/schema checks and public registry inventory. No product change.
3. Installed matrix: `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths --junitxml=.dev-records/verification/us-05-ip3/installed.xml` — failed in 17.98s: lock drift blocked but the new probe expected stale_validation instead of the existing planning stale_source diagnostic. Corrective attempt 1 changed that exact expected diagnostic to match the verified public planning contract; blocked status remained required. Same command with `installed-renewed.xml`: 1 passed in 35.52s, both paths. Subsequent corruption coverage is verified at the final gate.

Initial mypy found missing explicit case-table types and registry narrowing;
corrective attempt 1 added typed case tables and runtime narrowing, then passed.
Initial formatting check found the new Markdown example and one assertion;
formatter applied, renewed check passed. No suppressions or exclusions added.
Locked sync initially failed on read-only uv cache; approved escalation succeeded.
`gh auth status` reports an invalid stored token, but all repository GETs succeeded;
no credential changes. No incomplete issue retrieval is claimed.

## Final checks

M1: `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/us-05-ip3/m1.xml`
— **371 passed, 1 existing skip in 234.20s**, exit 0. Collection confirmation:
372 of 474 selected, 102 deselected. The skip is the existing missing-planning-schema
timeout exclusion; the other two existing skips are outside M1–6.

Final M1 installed parent records:
`.dev-records/verification/20261104T031116Z-3eefd55fa45a-730a3e9784794819bf23e42ac4849e19/`.
Its commands/summary record direct-wheel and rebuilt-wheel planning stages exit 0,
with child records for real artifact/install identities and runtime inventory.
Both semantic probe stage logs include `PASS installed semantic validation`.
`final-identities.json` under the IP3 raw directory records baseline revision,
platform, exact changed probe/test SHA-256 and lock identity. No executable inputs
changed after gate launch.

M1–6: `uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/us-05-ip3/m1-6.xml`
— **371 passed, 1 existing skip in 226.43s**, exit 0. Same 372 selected of 474,
102 deselected; no M2–6 cases currently exist. Final installed parent records:
`.dev-records/verification/20261104T031522Z-3eefd55fa45a-ec9dccc3f7ca4446952327f97f0cc6f4/`.
Both artifact stages passed again. IP2 installed and final acceptance verification
deferrals are discharged by IP3-T1/T3; developer story acceptance is pending.

Shared checks passed: locked sync, lock consistency,
Ruff lint/format (151 files), strict mypy (53 source files), CLI smoke (0.1.0),
and whitespace. Lock SHA-256 before/after:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

Linux/Python 3.12.16, pytest 9.1.1, xdist 3.8.0. macOS/Windows unverified here.
No standalone artifact driver or broader suite was requested/run. M0, M50 and
infrastructure coverage remains excluded except overlapping M1 associations.
Three existing temporary skips and M1-ACCEPT-VERIFY/M50-ACCEPT-VERIFY remain open;
this story does not resolve their historical timeout/platform obligations.


## Final gate

IP3-T1–T3 are technically complete. All five criteria have delivered-interface
evidence above and in the IP2 matrix. Changes are verification probes, regression,
usage/development documentation, plan/report and checkpoint only. No production
Python, runtime dependency, lockfile, historical assertion or skip was changed.
`verify_planning.py` needed no modification: its existing copying and independent
direct/rebuilt invocation already delivers the extended probe. No scope change.

Developer approved IP3 with “i approve ip3” on 2026-11-04. Whole-story acceptance
remains pending. No commit, push or PR was requested. Approval-record changes only;
`git diff --check` passed, and existing executable verification remains applicable.


## Developer-requested acceptance rerun — interrupted

After IP3 approval, developer requested “run the user story acceptance tests”.
Started `uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/us-05-ip3/story-acceptance-renewed.xml`.
Developer then requested “stop the tests”; interrupted with Ctrl-C, exit 130.
No completed summary or renewed passing result is claimed. Preserve available
partial records; the earlier completed M1–6 result (371 passed, one existing skip
in 226.43s) remains valid because no executable inputs changed. Do not restart
this rerun without developer direction. Whole-story acceptance remains pending.


## Whole-story acceptance

Developer “i accept user story” accepted US-05 on 2026-11-04. Earlier pending
acceptance statements above describe the historical gate/rerun state. No
executable inputs changed after the completed M1/M1–6 checks. Acceptance records
pass whitespace checks; no tests restarted. Publication proceeds under the
execute-plan workflow; milestone verification owners and historical exclusions
remain open.


## Publication

Accepted-story commit `e4b5acf` pushed with earlier IP1/IP2 commits. Standard
[PR #53](https://github.com/jimthompson5802/agentic-ml/pull/53) targets `main`.
[Static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/53#pullrequestreview-5762797927)
on `e4b5acf` found no actionable defects; no project code/checks executed during
review. Final publication-record delta is documentation only and will receive a
final-head confirmation in PR review history. Existing tests remain applicable;
no tests restarted. No merge performed.
