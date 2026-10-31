# US-02 IP4 verification

Status: technically complete; developer gate approved by “i approve ip4” (2026-10-31). Authorized by “go ahead with ip4”,
2026-10-31. IP3 approved and committed as `0830888`.

Issue #9 complete body and all comment pages refreshed: zero unique comments,
matching reported count; final metadata unchanged at `2026-10-31T01:15:38Z`.
Milestone 1 in body; AC-01–05 govern this phase. No new scope decision.
GitHub CLI 2.102.0. `gh auth status` still reports an invalid stored token, as
previous phases recorded; public issue GETs and complete snapshot checks
succeeded. No publication or authentication change was attempted.

Reusing IP1-approved installed CLI/API, real DVC/MLflow and JSON reopening,
separate project environment, and both distribution boundaries. These cover
setup usability and preservation, not subsequent execution isolation or approval
enforcement. Developer manual VS Code kernel verification passed; see evidence below.

## TDD evidence

- DVC defaults red: `uv run --locked pytest tests/integration/test_initialization.py -k initializes_usable_dvc -q`:
  one failed, 39 deselected; init returned zero but public `dvc remote list`
  returned empty stdout instead of the required `agentic-ml-store` remote.
  Fixture retained in system temporary `pytest-of-jim/pytest-17`.
- Minimal DVC implementation first verification configured the expected remote
  and directory, but the final test incorrectly expected an absolute `dvc root`
  result. Installed `dvc root --help` explicitly documents relative output.
  Corrected the probe to resolve that output against its cwd; the same root
  identity requirement remains. This is test correction, not a passing green.
  Original failure retained at `/private/tmp/us-02-ip4-dvc-green`.
- DVC corrected verification: one passed, 39 deselected (35.97s),
  `--basetemp /private/tmp/us-02-ip4-dvc-green2`.
- MLflow red: `uv run --locked pytest tests/integration/test_initialization.py -k initializes_mlflow -q --basetemp /private/tmp/us-02-ip4-mlflow-red`:
  one failed, 40 deselected; expected MLflow database was absent.
- MLflow/DVC green: `uv run --locked pytest tests/integration/test_initialization.py -k 'initializes_mlflow or initializes_usable_dvc' -q --basetemp /private/tmp/us-02-ip4-mlflow-green`:
  two passed, 39 deselected (89.05s). Reopened experiment has the explicit
  artifact URI and zero runs.
- State red: `uv run --locked pytest tests/integration/test_initialization.py -k initializes_durable_state -q --basetemp /private/tmp/us-02-ip4-state-red`:
  one failed, 41 deselected; `state/project.json` absent (45.46s).
- State green: same focused test with `--basetemp /private/tmp/us-02-ip4-state-green`:
  one passed, 41 deselected (46.24s). Reopened JSON matches the independent
  initial state literal; journal complete and no setup stages pending.

No lock change made. Full development/distribution verification passed as recorded below.

## Manual VS Code check

Developer ran a cell in the generated notebook and supplied its saved path on
2026-10-31. Inspected saved notebook: executed cell `import sys; print(sys.executable)`
has execution count 1 and stdout
`/private/tmp/us-02-ip4-state-green/test_initializes_durable_state0/experiment/.venv/bin/python`.
Notebook metadata identifies Python 3.12.15. Copied unchanged evidence to
`/private/tmp/us-02-ip4-evidence/manual-vscode.ipynb`. Local VS Code application
metadata version 1.135.0; successful `code --list-extensions --show-versions`
reports Python 2026.10.0 and Jupyter 2025.9.1. Initial sandbox listing emitted
EPERM creating a VS Code log directory; approved retry completed without error.
This proves the developer's manual project-kernel selection, not managed execution
or notebook isolation. Screenshot was supplied as Base64 text and was not used as
visual evidence; the saved notebook output supplies directly inspectable evidence.

## Preservation regression

Existing `shared_metadata_is_additive` red (`--basetemp /private/tmp/us-02-ip4-rerun-red`):
second init rejected duplicate DVC remote (exit 251), one failed/41 deselected
(52.66s). First corrective change reuses completed DVC stage rather than adding
the remote again; original preservation assertions unchanged. Green: one passed,
41 deselected (54.23s), `/private/tmp/us-02-ip4-rerun-green`.

Unowned-store conflict red: `... -k 'existing_unowned and state' -q --basetemp /private/tmp/us-02-ip4-conflict-red`:
one failed/45 deselected (45.14s); initializer overwrote unrelated state and
reported success. Added no-write storage preflight; all four store variants
verification: four passed/42 deselected (11.05s), `/private/tmp/us-02-ip4-conflict-green`. This reproduces missing IP4 preservation behavior;
original fixture retained.

Changed completed state red: `... -k changed_completed_state -q --basetemp /private/tmp/us-02-ip4-state-conflict-red`:
one failed/46 deselected (51.45s); rerun reset altered state and returned success.
Added state validation before any writes and preserved existing compatible JSON.
Green with original rerun regression: two passed/45 deselected (91.95s),
`/private/tmp/us-02-ip4-state-conflict-green`.

Superseded IP2/IP3 intermediate assertions now require complete storage,
empty pending setup, complete journal, and actual configured store directories.
Preservation, pin, backup, failure and corruption assertions remain intact.

External stores red: `... -k external_storage_reopens -q --basetemp /private/tmp/us-02-ip4-external-red`:
one failed/47 deselected (42.13s); second init rejected its recorded external
stores. Recognize only matching saved external destinations; green one passed
(53.64s), `/private/tmp/us-02-ip4-external-green`.

Existing DVC default red: `... -k 'preserves_existing_dvc_default and False' -q --basetemp /private/tmp/us-02-ip4-dvc-conflict-red`:
one failed/49 deselected (47.57s); initializer replaced unrelated default.
Added public `dvc config --list` preflight and matching-default reuse. Green:
two passed/48 deselected (55.18s), `/private/tmp/us-02-ip4-dvc-conflict-green`.

Storage failure red: `... -k 'storage_failure and state' -q --basetemp /private/tmp/us-02-ip4-retry-red`:
one failed/52 deselected (46.37s); public error mislabeled state-write failure
as preflight and omitted completed stages. Added exclusive storage setup lock,
stage persistence and safe failure journal; green all three injected boundaries:
three passed/50 deselected (140.09s), `/private/tmp/us-02-ip4-retry-green`.
Subprocess and `os.replace` seams supplement real DVC/MLflow integration;
injected sentinel stderr is not surfaced. Retry preserves/reuses earlier stages.

Cache red: `... -k initializes_usable_dvc -q --basetemp /private/tmp/us-02-ip4-cache-red`:
one failed/52 deselected (45.25s); empty cache directory absent.
Create local cache; green one passed (42.72s),
`/private/tmp/us-02-ip4-cache-green`, including actual write/read/removal probe.

Replaced MLflow database red: `... -k replaced_mlflow -q --basetemp /private/tmp/us-02-ip4-db-conflict-red`:
one failed/53 deselected (51.62s); empty replacement database silently recreated.
Preflight now reopens completed MLflow storage through its public client with a
read-only SQLite URI and verifies experiment/artifact identity before any setup
writes. Green plus external-rerun regression: two passed/52 deselected (102.23s),
`/private/tmp/us-02-ip4-db-conflict-green`.

Storage path boundary red: `... -k storage_boundary -q --basetemp /private/tmp/us-02-ip4-boundary-red`:
four failed/54 deselected (182.45s): cache symlink, externally configured cache,
unwritable selected artifact directory and conflicting custom-store ignore
negation all incorrectly accepted. Added cache path/config checks, permission
probes inside selected directories and selected-store ignore checks. Green:
four passed/54 deselected (18.52s), `/private/tmp/us-02-ip4-boundary-green`.
No assertions weakened; checks now fail before any durable setup writes.

Interrupted metadata red: `... -k 'storage_failure and True' -q --basetemp /private/tmp/us-02-ip4-retry-metadata-red`:
one failed/58 deselected (51.08s); retry accepted edited metadata after DVC
failure. Added no-write comparison against synchronized metadata checksums.
Green one passed (39.70s), `/private/tmp/us-02-ip4-retry-metadata-green`.

Artifact-driver red: `uv run --locked pytest tests/integration/test_distribution_verification.py -k complete_initialization -q --basetemp /private/tmp/us-02-ip4-driver-red`:
one failed/9 deselected (1.33s); required verifier command did not exist.
Added stdlib-only driver/probe; both normal-wheel paths keep all existing checks,
then source-distribution fixtures provide matching installed Git packages for
fresh CLI and existing-package API initialization. Every installed package file
must match each original wheel byte-for-byte. Git metadata is not fabricated;
the report distinguishes wheel-install evidence from complementary pinned-Git
initialization. Initial green: one passed/9 deselected (234.64s),
`/private/tmp/us-02-ip4-driver-green`. Both normal wheel checks and all four
complete fresh/existing pinned project checks passed. No GitHub fetch of
unpublished implementation is claimed. Fixture source and full SHA are printed
in the driver log.

Final recovery review red: `... -k environment_journal_does_not_adopt -q --basetemp /private/tmp/us-02-ip4-ownership-red`:
one failed/59 deselected (47.57s); an environment-only journal incorrectly
allowed an unrelated database inserted before storage began. Store reuse now
requires recorded entry into the corresponding storage stage; interrupted
metadata checks also cover abrupt interruptions with no caught failure record.
Green with all storage failure/retry cases: five passed/55 deselected (183.00s),
`/private/tmp/us-02-ip4-ownership-green`.

## Platform and verification

macOS 15.7.9 (24G830), arm64; Python 3.12.15, uv 0.13.1, Git 2.54.0.
Harness development environment: DVC 3.67.1, MLflow 3.17.2, NumPy 2.5.4,
pandas 3.1.0, scikit-learn 1.9.1, nbclient 0.11.0, ipykernel 7.4.0,
nbformat 5.11.1. Separate project resolution identities remain in retained
project lockfiles. No new Linux/Windows evidence claimed.

Initial shared checks passed: locked dev synchronization, lock consistency,
lint, formatting (78 files), strict mypy (20 source files), version smoke (0.1.0),
and whitespace. Sandbox cache-access denials were retried with approval; these
were infrastructure failures, not behavior reds. Focused type checks initially
found two probe path typing errors; fixed with concrete Path conversion and
explicit non-None assertion, no suppressions. Final static checks also passed after the binary-probe correction.

Harness lock SHA-256 before/after all verification:
`b7ca45a27ad337812eff5555bf2a74edee3bfb637ca7c756e382fc82f867ab66`.
No dependencies, lock entries, suppressions or disabled checks added.

Final storage diagnostics red: `... -k 'storage_failure and DVC and False' -q --basetemp /private/tmp/us-02-ip4-diagnostic-red`:
one failed/59 deselected (36.53s); persistent failure record omitted the tool
exit code. Added stage-specific safe exit-code recording and reporting (null for
filesystem errors); green all four cases: four passed/56 deselected (181.49s),
`/private/tmp/us-02-ip4-diagnostic-green`.

Final build: `uv build --out-dir /private/tmp/us-02-ip4-evidence/final-artifacts`.
Final isolated verification:
`uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir /private/tmp/us-02-ip4-evidence/final-artifacts`:
both direct/rebuilt wheel paths passed. Workspace:
`/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-mhirdvb9`.
Direct wheel SHA-256:
`7248fc509fff862f33ee1f29cd69ce72e485d1d3ef4a07e6290aef75a09ba792`;
source distribution:
`a2cfbe80f1834fe4bd0f08c5cbecb56fff76b4e4589d736778ddc3c9a78d2a55`.
Original full-run JUnit (preserved failure):
`/private/tmp/us-02-ip4-evidence/final-pytest.xml`. Clean final result is recorded below.
All 85 local Markdown targets in changed documentation, including the checkpoint, resolve.

The complete installed initialization test also passed in the final full suite.
Its source fixture is
`/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/pytest-of-jim/pytest-19/test_complete_initialization_f0/initialization/source`,
full local SHA `bcda7299dd4c8437c89929f98a9a8df112019071`.
The sibling `direct-wheel` and `rebuilt-wheel` directories each retain fresh
and existing projects and command logs. This is installed local-Git evidence
with package bytes independently compared against the normal wheel artifacts.

## Full-suite probe correction

The full run exposed an IP2 probe assumption in
`test_existing_project_code_is_not_copied_into_setup_journal`: its recursive
scan decoded every setup file as UTF-8. IP4 adds a binary SQLite database, so
the scan raised `UnicodeDecodeError` before evaluating the source-preservation
assertion. Focused reproduction: one failed/59 deselected (43.14s),
`/private/tmp/us-02-ip4-regression-original`; original traceback preserved in
`/private/tmp/us-02-ip4-evidence/regression-original.xml`.

Corrective attempt 1: retain the complete recursive file set and the same
source sentinel exclusion, using `b"source-sentinel" not in path.read_bytes()`.
No file is excluded and no product code or expected preservation behavior
changes. Corrected focused result: one passed/59 deselected (44.85s),
`/private/tmp/us-02-ip4-regression-corrected`; JUnit
`/private/tmp/us-02-ip4-evidence/regression-corrected.xml`.
Original full run: 84 passed, one failed in 1826.69s (30:26), retaining the
original loaded assertion; JUnit `final-pytest.xml` preserves that failure.
All 85 distinct current cases have passing coverage across those runs.

To satisfy the clean full-run check, repeat all 85 with optional MLflow/DVC
telemetry disabled in the controlled test environment:
`env MLFLOW_DISABLE_TELEMETRY=true DVC_NO_ANALYTICS=1 uv run --locked pytest --junitxml=/private/tmp/us-02-ip4-evidence/clean-pytest.xml`.
This disables unrelated telemetry traffic, not tests, assertions, isolation or
authorization controls. No source/dependency change accompanies the environment
choice. Result: **85 passed in 1829.72s (30:29)**, exit 0. All 85 cases remained enabled. IP4-T1–T4 are technically complete; developer phase approval is recorded below; whole-story acceptance remains pending. Telemetry settings did not materially shorten this run.

Rebuilt review artifacts after the test-only correction at
`/private/tmp/us-02-ip4-evidence/review-artifacts`; both normal direct/rebuilt
wheel checks passed at
`/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-mchx6nbs`.
Wheel SHA-256 remains unchanged because product package bytes did not change.

| Criterion | Evidence |
|---|---|
| US-02-AC-01 | IP2 inventory/schema/inert notebook checks; complete CLI/API artifact driver and final regression suite |
| US-02-AC-02 | Preserved pin/lock/custom package/edits/backups; no-write store conflicts; rerun/retry and replaced-state/database tests |
| US-02-AC-03 | IP3 synchronization/import checks retained; artifact-derived fresh/existing project resolution/import/lock probes; developer VS Code project-kernel execution |
| US-02-AC-04 | Real DVC remote/cache, MLflow experiment/artifact/no-run probes, durable JSON reopening; relative/external stores, existing defaults and interrupted stages |
| US-02-AC-05 | Explicit unconfigured choices, empty approvals/runs, unreadable raw-data sentinel during installed init, credentials/store Git exclusions, unsafe path/URI/permission checks |

Initialization is setup only. Later semantic validation, managed execution,
authorization/isolation, provenance, datasets, workflow recovery and adapters
remain with their owning stories. This phase does not verify those capabilities.


## Final verification and handoff

| Command or check | Outcome |
|---|---|
| `uv sync --locked --group dev` | Passed; 193 resolved, 191 installed packages checked |
| `uv lock --check` | Passed; no lock mutation |
| Clean full pytest command above | Passed: 85/85, exit 0; `clean-pytest.xml` retained |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; 78 files |
| `uv run --locked mypy src tests` | Passed; 20 source files |
| `uv run --locked agentic-ml --version` | Passed; 0.1.0 |
| Review artifact build / isolated distribution command | Passed both wheel paths after the test-only correction |
| Local Markdown targets / `git diff --check` | Passed; 85 local Markdown targets |

Review source-distribution SHA-256:
`afbfc9623dd8bfa099f4effccee3cf22476dd4330829fb04be155f1ad74f45e0`.
Review wheel hash remains `7248fc509fff862f33ee1f29cd69ce72e485d1d3ef4a07e6290aef75a09ba792`.

The clean run retains equivalent artifact-derived installed projects under
system temporary `pytest-of-jim/pytest-20/test_complete_initialization_f0/initialization`,
with full local fixture SHA `ad28a3e54f2314673db7c4bf253195e1c11cb471`.
Package files were compared against both wheels, and installed Git origin was
checked independently. The existing normal-wheel resource/version/corruption
checks remain unchanged; no dependency inventory change required editing
`check_installed.py`. Existing CI discovers the new driver test through ordinary
pytest, so no CI workflow edit was required.

No unresolved failed assertion, suppression, disabled test or scope change.
Earlier failed runs and corrective evidence remain available above. All source,
tests, setup documentation and progress records remain uncommitted on
`US-02-experiment-init`; no push or publication. IP4 gate subsequently approved; whole-story acceptance remains pending.


Developer approved IP4 with “i approve ip4” on 2026-10-31. Approval is recorded in the owning plan and checkpoint. No commit or publication authorized. Documentation-only approval record: `git diff --check` passed; existing runtime verification remains valid.
