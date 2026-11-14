# US-13 IP2: project dataset versioning

Date: 2026-11-13 UTC. Owning issue: #16; M1 US-13-AC-01/02 only.
Developer “start ip2” authorized this phase after approved Gate 1.
**IP2-T1–T4 Complete; Gate 2 Approved, 2026-11-13.**

## Scope and implementation

The issue's complete body, one unique comment (6699586819), and final metadata
were refreshed with the repository helper. Count 1 and update timestamp
2026-11-07T00:28:44Z remained stable. No scope change was found. Initial sandbox
network calls failed; approved outside-sandbox reads succeeded. These failures
do not indicate invalid authentication: the successful issue reads establish access.

`tests/integration/test_dataset_versioning.py` extracts the guide's configuration
and Python script and executes its project invocation, registration, push and cloud
status shell commands after path substitution. The adapter creates isolated Git/DVC
projects, literal source fixtures and Git identities/commits. Environment setup
is reused from the locked development environment; this phase does not establish
normal wheel installation. No package code, dependencies or runtime resources change.
The guide script ran successfully without correction. Native existing functionality
and documentation use positive/boundary evidence as approved at Gate 1; no new
product behavior was implemented and no failing TDD test was manufactured.

## Independently checked outcomes

- AC-01: CSV and equivalent Parquet snapshots produce literal IDs 0–4 and labels
  A–E in version A, with Z replacing A for ID 0 in B. Extraction source SHA-256
  matches actual snapshot bytes. Output frames agree with independent literal rows.
- AC-01: Both split layouts retain configured ordered membership in the single
  JSON result, strict JSON round-trip and matching saved Parquet rows. Derived
  rows are exactly IDs 0/2/4 with labels A/C/E, then Z/C/E.
- AC-01/02: Real commits A/B expose native pointers and the readable project
  manifest. Unchanged registration retains identities. All four directory
  identities change across A/B; independent source, split-record and derived-byte
  edits change only the corresponding pointer. No model/stage execution is claimed.
- AC-02: Exact Git inventories contain project code/configuration and native
  metadata/ignores, excluding all datasets, result manifests, caches and remote
  bytes. CSV uses an external local remote; Parquet uses an explicitly excluded
  in-project remote. Fixture dependency declarations/lock are not synthesized:
  normal project setup and both installed artifact paths remain IP3 obligations.
- AC-01/02: Each native directory manifest is inspected; every referenced member
  in cache and remote matches the original bytes and independent MD5. Both A/B
  versions remain addressable after transfer, including replaced source A bytes.
  This is retention evidence without checkout/pull or M2 restoration acceptance.
- Native boundaries: missing target, already Git-tracked data, duplicate output
  declarations and a remote beneath a regular file all fail visibly. Source/index
  ownership survives conflicts; failed transfer preserves local pointers/status
  and nonsecret default configuration. No automatic repair or rollback is added.

## Verification records

Source revision: `baa8920d11104e228db67cce4708c0e6f3ad7160` plus the guide,
integration test, plan, checkpoint and this report. Platform: Linux aarch64,
Python 3.12.16, DVC 3.67.1, uv 0.13.6, pytest 9.1.1, xdist 3.8.0.
No macOS or Windows verification is inferred.

Durable records: `.dev-records/verification/20261113-us13-ip2-baa8920/`.
`commands.json`, `summary.json`, `logs/` and `identities/` retain phase check
commands, output and representative committed native metadata/configuration.
Early successful retained focused workspaces remain under `/tmp/pytest-of-vscode/pytest-0/`;
durable identities were copied before any cleanup. Temporary workspace retention
is not a substitute for durable evidence. Expected native failure diagnostics are
asserted in the integration checks; the durable pytest log reports test outcomes.

Focused command:
`uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_dataset_versioning.py -k guide`.
Initial source/split/retention slice: 2 passed (11.83s); added native failure cases:
2 passed (18.19s); final guide shell adapter: 2 passed (18.77s).
The first sandbox invocation could not write the uv cache; approved escalation
resolved it. No product corrective attempts, suppressions or weakened assertions.

| Check | Result |
|---|---|
| `uv sync --locked --group dev` | Pass; 196 resolved / 193 checked, no dependency changes |
| `uv lock --check` | Pass |
| Focused recipe after format correction | 2 passed, 18.90s; 2 collected, none deselected |
| `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1` | 722 passed, 1 existing skip, 4 warnings; 217.97s |
| `uv run --locked ruff check .` | Pass |
| `uv run --locked ruff format --check .` | Initial guide block format failure; corrected, renewed pass (305 files) |
| `uv run --locked mypy src tests` | Pass, 76 source files |
| `uv run --locked agentic-ml --version` | Pass, `0.1.0` |
| `git diff --check` | Pass |

M1 inventory collection (`uv run --locked pytest --collect-only -q -m milestone_1`):
991 total, 723 selected, 268 deselected. Collection only used no workers because
it executes no tests. M1's skip is the existing developer-authorized
`test_missing_planning_schema_fails_installed_inventory` timeout case; the other
two documented M50 skips are outside this selection. Four warnings are native NumPy operations on the intentional
infinite-value assessment fixture. No new skip or suppression was added.

Formatting correction attempt 1: hypothesis was that the candidate guide's line
wrapping did not match Ruff; `uv run --locked ruff format docs/dataset-versioning.md`
changed only the `.loc`/`.to_csv` expression wrapping. Renewal passed formatting,
focused recipe and all shared checks. Original failed output remains `logs/05.log`.
No semantic behavior changed, so the M1 run remains applicable; focused recipe
renewal additionally verified the exact reformatted block. Renewal records:
`.dev-records/verification/20261113-us13-ip2-renewal/`.

Lock SHA-256 before/after both check sets:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
All 61 relative file links in guide/plan/report/checkpoint resolve after the
final documentation edits. The single formatting attempt succeeded; no unresolved
failure or product corrective attempt remains.

## Gate and remaining work

Developer “I approve this gate; commit”, 2026-11-13, approved Gate 2 and
authorized committing the IP2 package. Requested changes: None. IP3 awaits
execution direction and owns both normal wheel paths, final guide links/design status
and M1–6 story acceptance. AC-03/04 remain M2; US-26/27/39/40 own tracking,
stages and full experiment/assistant integration. Historical M1/M50 verification
obligations remain open. The approval authorizes a local commit only; no push, PR or issue edit.
