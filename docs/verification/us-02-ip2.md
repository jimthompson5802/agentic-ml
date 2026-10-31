# US-02 IP2: Conflict-safe installed scaffolding

Status: technically complete; developer gate approved by “i approve us-02 ip2” (2026-10-30). IP1 was approved and committed as `12df741` after developer message “i approve ip1; commit changes and I authorize ip2”. No IP3 work authorized or performed.

## Delivered boundary

The installed `agentic-ml init` and public `agentic_ml.initialization` API now create draft project configuration, a brief, empty allowed-search inputs, unconfigured execution inputs, four inert notebook templates, project-package scaffolding and ignore rules. Explicit project roots work from another cwd. Data access, agent authentication and approval presentation remain visibly unconfigured. No notebook/kernel, data read, agent login, tracking run or approval is started.

CLI/API results explicitly report `environment` and `storage` pending. No environment synchronization, experiment-lock regeneration, DVC/MLflow provisioning or durable workflow state implementation is claimed. This is a phase result, not completion of US-02-AC-01–05.

Preflight checks existing Git/uv project identity, installed/declared/locked full-SHA harness identity, project/package names, existing build/source selection, file collisions, symlinks, conflicting paths/stores, credentials, ignore exceptions, permissions and setup locks. Existing custom package code/build metadata and unrelated TOML settings/comments remain preserved. Compatible reruns retain edited drafts; incompatible schema/identity/store changes or missing saved files fail explicitly.

The private setup journal and original pyproject/lock/ignore backups support safe interrupted-scaffold retry. Unchanged user source is represented by identity checksums, not copied into setup evidence. Journal/state is not execution authorization or workflow recovery. Atomic replacement and an exclusive setup lock protect cooperative initializers, not malicious filesystem mutation or experiment-kernel isolation.

## Source and acceptance traceability

Complete issue #9 metadata/body and all comment pages refreshed before implementation: open, zero comments, stable `updated_at=2026-10-31T01:15:38Z`; approved editor scope decision retained. Accepted US-01 prerequisite, IP1 public test boundaries, initialization schema/authority/storage decisions and phase dependencies checked against the [owning plan](../plans/milestone-1-us-02.md), [IP1 contracts](us-02-ip1.md) and design topic documents.

| Criterion | Evidence advanced by IP2 | Still pending |
|---|---|---|
| US-02-AC-01 | Installed CLI/API, independent inventory/content checks, schema resources, inert notebook format and normally installable project package | Complete environment/storage path in IP3/IP4 |
| US-02-AC-02 | Preserved bytes/source/build/pin; conflicting/invalid project, path and store rejection; edited rerun; interrupted-write evidence and retry | Dependency resolution failures and configured-store integration |
| US-02-AC-03 | Harness parser/schema dependency closure verified through both wheels | Experiment ML/notebook/storage dependencies and synchronization in IP3 |
| US-02-AC-04 | Explicit store paths serialized safely with internal Git exclusions | Actual store initialization and public usability probes in IP4 |
| US-02-AC-05 | Unconfigured setup, no credentials copied, no implicit execution/authentication/data access; no development AGENTS.md/runtime guidance loading | Full integrated initialization evidence in IP4; execution isolation remains downstream |

## TDD slices and attempts

Tests run through the installed entrypoint/API in independent temporary Git/uv projects. The harness fixture is a full-SHA local Git snapshot of the reviewed source, installed normally into the experiment `.venv`. This verifies unpublished changes without claiming a live GitHub installation. No internal collaborator mocks or private method assertions. The interruption fixture injects an error at the external `os.replace` filesystem boundary and exercises the installed public API.

Raw evidence directory: `/private/tmp/us-02-ip2-evidence`. For each numbered slice below, red/green output is retained as `sliceN-red.log` / `sliceN-green.log`. Commands were `uv run --locked pytest tests/integration/test_initialization.py -q` with the focused `-k` selector noted for red; green reran the new cases plus relevant prior regressions. Package slice 12 used `tests/integration/test_distribution_verification.py`.

| Slice | Behavior / red selector | Observed red | Green result |
|---|---|---|---|
| 1 | `installed_cli` (initial file had one test) | Installed CLI rejected unknown `init` | Four tests, including version regressions, passed |
| 2 | `conflicting_file` | Existing config silently replaced | Two passed |
| 3 | `shared_metadata` | Missing package build metadata | Three passed |
| 4 | `invalid_project` | Seven incompatible metadata/pin cases accepted or produced raw failures | Ten passed |
| 5 | `unsafe_destinations` | Seven path/store/lock boundaries failed | Seventeen passed |
| 6 | `public_api` | Relative explicit store option ignored | Eighteen passed |
| 7 | `rerun_rejects` | Four incompatible/missing saved-input cases accepted; malformed journal already rejected | Twenty-three passed |
| 8 | `explicit_existing` | User source treated as a collision | Twenty-four passed |
| 9 | `setup_inventory` | Invalid fixture assumed uv created `.gitignore`; not counted as behavioral red | Fixture corrected by explicitly creating the original ignore file; backup assertions pass in slices 10/16 and full suite |
| 10 | `interrupted_scaffold` | Preserved incomplete setup could not retry | Twenty-six passed, including corrected backup fixture |
| 11 | `unrelated_ignore` | Safe unrelated ignore exception rejected | Twenty-seven passed |
| 12 | `missing_initialization` | Wheel missing new schema incorrectly passed installed checks | Nine distribution tests passed |
| 13 | `custom_internal` | Configured internal store was visible to Git | Nine focused cases passed |
| 14 | `credentials_in` | Credential-bearing metadata copied to private backups | Two focused cases passed |
| 15 | `unwritable_destination` | Permission failure happened after durable config write | Eight focused cases passed |
| 16 | `existing_project_code` | Unchanged custom source duplicated into setup journal | Three focused cases passed, including interruption/backup regressions |

Verification limitations/deviations: the initial backup test was a fixture failure, not valid TDD red evidence; corrected without removing any assertion. Journal backup functionality was initially implemented before that isolated test had valid red evidence. The subsequent interruption and privacy corrections have valid behavioral red–green evidence. No assertions, thresholds or existing checks were weakened to conceal a failure.

Other corrective attempts:

- Package probes originally assumed no third-party runtime dependencies. The approved dependency change required an explicit new closure contract. First update omitted `typing-extensions`; installed verification failed. Lock metadata shows referencing requires it for Python <3.13. Second update added that required name; all 20 existing package/installation tests passed (`probes-green2.log`). Direct dependency declarations and complete runtime names remain exact, contributor tools/stubs remain excluded, all pre-existing corruption tests retained.
- Strict types initially caught reuse of a configuration-dict variable for bytes; renamed the local, then passed. Later permission-probe loop reused a string name for bytes; separate store-path variable fixed it and passed.
- The new immutability probe initially inspected unsupported dataclass metadata. Its first correction used literal `setattr`, which Ruff converted to a static read-only assignment; type verification failed. A replacement targeting the old text made no effective change and failed again. The final corrective change used an explicit dynamic attribute name for the public runtime immutability check; strict types passed. No suppression or assertion removal.
- Initial sandbox cache/Git restrictions were retried with approved escalation; these were setup restrictions, not behavioral red evidence. Raw failed and corrected outputs are retained in this evidence directory. No unresolved third-failed corrective sequence.

## Dependencies and package verification

Deliberate additions: runtime tomlkit 0.15.2, PyYAML 6.0.3, jsonschema 4.26.0; dev type stubs types-PyYAML 6.0.12.20261030 and types-jsonschema 4.26.0.20261006. Runtime closure on Python 3.12 also includes attrs 26.1.0, jsonschema-specifications 2025.9.1, referencing 0.37.0, rpds-py 2026.9.1 and typing-extensions 4.16.0. Notebook/ML/storage execution dependencies remain IP3.

The harness lock changed deliberately from `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d` to `b93c4a72c77245102372e22cf56a88557a262eaccb1c897177d8289ffcfab389`. Verification must preserve the new identity; experiment fixture locks remain byte-identical across scaffold initialization.

Both direct and sdist-rebuilt wheels are installed with declared runtime dependencies, checked outside the checkout, and independently verified for version, imports, noneditable harness, exact closure, existing provisional sentinels, new resource inventory/schema properties and output-free notebook content. Git-pin preservation is tested separately in the normal pinned-Git project fixtures; wheel installations do not pretend to have Git-origin metadata. Full end-to-end initialization for both wheel paths remains IP4.

## Final verification

Platform: macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1, Git 2.54.0. No new hosted Linux, Windows or additional Python verification; no VS Code manual check required in IP2 (it remains IP4).

| Command | Result / raw evidence |
|---|---|
| `uv sync --locked --group dev` | Passed, `sync-release.log` |
| `uv lock --check` | Passed, `lock-release.log` |
| `uv run --locked ruff check .` | Passed, `lint-release.log` |
| `uv run --locked ruff format --check .` | Passed, `format-release.log` |
| `uv run --locked mypy src tests` | Passed, `types-release.log` |
| `uv run --locked agentic-ml --version` | Passed, `0.1.0`, `smoke-release.log` |
| `uv run --locked pytest` | Passed — 56 tests, `full-release.log`; earlier 52/55-test runs also passed |
| `uv build --out-dir /private/tmp/us-02-ip2-evidence/release-artifacts` | Passed, `build-release.log` |
| `uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir /private/tmp/us-02-ip2-evidence/release-artifacts` | Passed — direct and sdist-rebuilt wheels, `distributions-release.log` |
| Local links, `git diff --check`, post-verification lock checksum | Passed — local links resolve, diff whitespace clean, lock identity remains `b93c4a72c77245102372e22cf56a88557a262eaccb1c897177d8289ffcfab389` |

## Handoff

Review installed behavior and limitations against the [IP2 gate](../plans/milestone-1-us-02.md). No complete-story acceptance, dependency synchronization, store provisioning or IP3 authorization is recorded. Developer subsequently requested “commit changes”; IP2 implementation/evidence committed with this record. The IP2 approval gate is now approved; IP3 execution remains pending.
