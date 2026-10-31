# US-02 IP3: Experiment environment synchronization

Status: IP3 T1–T3 complete; developer gate approved by “i approve ip3” (2026-10-31). No IP4 execution or publication authorized.

## Scope and boundaries

Developer authorized “Execute US-02 IP3.” on 2026-10-31. [Issue #9](https://github.com/jimthompson5802/agentic-ml/issues/9) governs Milestone 1 / US-02. Complete body and all comment pages retrieved: zero comments, stable `updated_at=2026-10-31T01:15:38Z`, including the approved VS Code/editor scope decision; no GitHub milestone assigned. Final metadata refresh agrees. Prerequisite #8 remains closed at `2026-10-30T10:42:22Z`; accepted US-01 and approved IP2 gates verified in their owning records.

Reused [approved IP1 contracts and public test boundaries](us-02-ip1.md): installed CLI/API in separate projects, real uv lock/sync and interpreter imports, external-tool failure injection supplementing real resolver conflicts, and isolated distribution/resource probes. These verify AC-02/03/05 for this increment, not storage, managed execution, authorization enforcement or full-story acceptance. Local full-SHA Git fixtures contain unpublished reviewed source; no claim of GitHub delivery. Wheel probes verify packaging separately from Git origin metadata; full wheel initialization remains IP4.

## Implementation

- Added the approved direct experiment requirements: NumPy `>=2,<3`, pandas `>=2,<4`, scikit-learn `>=1.6,<2`, nbclient `>=0.10,<1`, ipykernel `>=6,<8`, nbformat `>=5,<6`, DVC `>=3,<4`, MLflow `>=3,<4`.
- Preserve existing requirement strings and append missing required bounds. uv intersects duplicate named requirements rather than replacing existing constraints. Preserve comments, custom metadata and harness Git source/SHA. Required notebook/storage libraries are also declared as harness runtime dependencies per IP1; editor software is excluded.
- Run argument-list `uv lock --project ROOT`, `uv sync --locked --inexact --project ROOT`, then `uv lock --check --project ROOT`. Pin checks follow each command and precede sync. No upgrade flags; setup uses `.venv` despite inherited active-environment overrides. A separate isolated interpreter checks required library and project-package imports without starting kernels or notebooks.
- Exclusive setup lock protects the environment stage. Private journal records metadata hashes, stages and exit codes; original metadata backups survive. Failed tool stages return nonzero and retain incomplete setup. Retry requires unchanged interrupted metadata and the same setup identity/options. No automatic rollback or hidden retry. Raw child output is not echoed or stored because it can contain credentials; safe stage/exit diagnostics remain available.
- Initialization reports storage pending. Existing draft inputs and unconfigured access/agent/approval choices remain intact. No DVC store, MLflow experiment/run, workflow approval or data access is introduced.
- Standalone installation and wheel probes assert exact reviewed runtime inventories, installed origin/resources and absence of contributor distributions. Retained original corruption and substitution checks. Platform name normalization includes dots/underscores/hyphens.

## TDD and attempts

1. Red: `uv run --locked pytest tests/integration/test_initialization.py -k synchronizes_required -q`: one failure because none of eight direct experiment requirements existed. Minimal environment declaration/lock/sync implementation followed. First green: one passed in 38.92s. Independently assert actual imports, unchanged pin and stable subsequent locked synchronization.
2. Red: `... -k sync_success_requires -q`: one failure because a substituted uv returning zero without installing the project was incorrectly accepted. Added separate-interpreter postcondition; green with the real environment test: two passed in 69.61s.
3. Red completion-record regression: `... -k sync_success_requires -q` failed because the rejected import check appeared in completed stages (one failure in 42.65s). Move completion acknowledgement after successful imports. Green: `uv run --locked pytest tests/integration/test_initialization.py -k 'sync_success_requires or setup_inventory or sync_failure_retry' -q --junitxml=/private/tmp/us-02-ip3-evidence/final-environment-regressions.xml`: four passed in 163.05s, covering failed imports, successful inventory and both sync retry paths. First corrective attempt passed.
4. Red path-boundary regression: `uv run --locked pytest tests/integration/test_initialization.py -k symlink_environment -q` failed because init returned zero for `.venv` linked outside the project (one failure in 126.85s). Add `.venv` to the existing symlink preflight. Green: `uv run --locked pytest tests/integration/test_initialization.py -k 'symlink_environment or synchronizes_required' -q --junitxml=/private/tmp/us-02-ip3-evidence/final-path-regressions.xml`: two passed in 39.41s. Reject before scaffold/journal writes; normal real synchronization remains successful. First corrective attempt passed.

Supplemental regression tests cover already implemented generic failure/preservation behavior: real impossible `numpy<2` intersected with `numpy>=2,<3`, deterministic sync exit 73 with secret-output sentinel, unchanged retry, edited-metadata rejection, preserved existing compatible NumPy bounds/unrelated dependency and undeclared installed package, explicit root/API and inherited environment override handling. These cases are not claimed as independent failing TDD slices.

Initial initialization regression run: 36 passed, one failed in 807.23s; failure evidence retained at `/private/tmp/us-02-ip3-evidence/initial-initialization-result.txt`. It identified a remaining IP2 expectation that an existing package pyproject remained byte-identical. IP3 necessarily appends dependencies; retain all existing declarations and compare the entire parsed metadata after removing only the approved additive dependency entries. Source bytes, backend and all other settings remain asserted. Focused verification passed (one test in 67.26s). The earlier concurrently running full suite, which had already collected the old assertion, completed with 61 passed / one failure in 995.38s; retained JUnit evidence is `/private/tmp/us-02-ip3-evidence/pytest.xml`. Final corrected-source results are recorded separately in `final-pytest.xml`. This updates the intermediate-phase expectation, not the preservation requirement.

Updated phase-specific IP2 expectations: initial experiment lock now changes deliberately, journal records environment stages, and pending setup becomes storage only. Original backup byte checks, source/pin checks, no-op rerun stability and corruption assertions remain. No assertions were disabled, skipped or suppressed.

Runtime inventory correction: initial broader package/installation run failed because the draft inventory incorrectly excluded runtime `pathspec` and normalized underscores but not dots (`flufl.lock`, `ruamel.yaml`, `zc.lockfile`). One corrective change retained pathspec and normalized distribution names, preserving exact-set assertions. Original distribution criterion then passed: nine tests in 28.78s; installation criterion passed: 12 tests in 114.51s. No second/third corrective attempt required. Initial diagnostics preserved under `/private/tmp/us-02-ip3-evidence/initial-closure-*.log`.

Sandbox cache/network failures were retried with approved escalation; they were not behavioral reds. No dependency ranges were relaxed. No suppressions, skipped checks or disabled tests added.

## Verification

Observed macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1, Git 2.54.0. Resolved: NumPy 2.5.4, pandas 3.1.0, scikit-learn 1.9.1, nbclient 0.11.0, ipykernel 7.4.0, nbformat 5.11.1, DVC 3.67.1, MLflow 3.17.2. Exact full closure is in `uv.lock` and isolated probe stage logs.

| Command / criterion | Result |
|---|---|
| `uv sync --locked --group dev` | Passed |
| `uv lock --check` | Passed |
| `uv run --locked pytest --junitxml=/private/tmp/us-02-ip3-evidence/final-pytest.xml` | Passed: 62 tests in 995.37s |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed |
| `uv run --locked mypy src tests` | Passed |
| `uv run --locked agentic-ml --version` | Passed: `0.1.0` |
| `uv build --out-dir /private/tmp/us-02-ip3-evidence/review-artifacts` | Passed |
| `uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir /private/tmp/us-02-ip3-evidence/review-artifacts` | Passed direct and sdist-rebuilt wheels |
| `git diff --check`, local documentation links | Passed; 67 targets resolve |

The full suite passed before the final one-line `.venv` preflight guard. After that guard, reran the added boundary test and the existing real synchronization test (two passed), all shared non-test checks, and rebuilt/reverified both wheel paths. Across the full run and focused path run, all 63 distinct current tests are covered; a single 63-test full-suite run was not repeated. Preserved completion-record/failure regressions separately passed four tests. Full console output remained in the tool session; JUnit files preserve structured results, while wheel stage logs retain subprocess output.

Deliberate harness lock change: original `b93c4a72c77245102372e22cf56a88557a262eaccb1c897177d8289ffcfab389`; new `b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`. Locked checks preserve the new identity.

Fresh wheel SHA-256: `463a93c8f5916b81fb5458b0cb20f05de22425f28cf6c11c348e1baeed7dadb7`; sdist: `a7d2ba532273be7eb63a294c96404bc12976ade59d91176ec4ca77f23f0f2dde`. Distribution workspace: `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-khv_h56f` (independent environments, build and stage logs retained).

| Acceptance criterion | Evidence boundary | Increment result |
|---|---|---|
| US-02-AC-02 | Existing bounds/settings/source identity, conflicts, backups, failure/retry, no-op locked sync | Verified for IP3; final integrated init remains IP4 |
| US-02-AC-03 | Real declarations/resolution/sync, ML/notebook/kernel imports and project imports; isolated runtime closure | Verified for IP3; final integrated init remains IP4 |
| US-02-AC-05 | Unconfigured choices, secret-output exclusion, selected environment and setup destinations, no storage/run/approval creation | Verified for IP3; final integrated init remains IP4 |

No new Linux/Windows, additional Python or manual VS Code verification. Importing ipykernel proves kernel availability only; no kernel execution/isolation claim. Full storage and final installed initialization are IP4. Whole-story acceptance, commit, push and publication are not authorized.
