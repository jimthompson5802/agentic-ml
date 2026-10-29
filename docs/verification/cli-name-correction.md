# CLI name correction verification

Date: 2026-10-29. Change: SC-01 in the [US-31 plan](../plans/milestone-0-us-31.md#scope-change-history) and [US-33 plan](../plans/milestone-0-us-33.md#scope-change-history).

## Authority and impact

The developer explicitly corrected ADR-007 and requested corresponding code/document changes: the CLI is `agentic-ml`, matching distribution `agentic-ml`, with Python import `agentic_ml`. This instruction authorizes the correction and supersedes the old CLI spelling in GitHub issues and previous instructions. Current user-story text retains every acceptance-criterion ID. GitHub issue bodies have not been edited; their old spelling is governed by this recorded developer decision. Historical review matrices and verification transcripts preserve their original wording and now link this correction.

Updated: root AGENTS.md; README and contributor guide; ADR-007; current user stories; harness design, interfaces, delivery dependencies, layouts, traceability and walkthrough; both owning plans and execution index; console script metadata and argparse program name; public subprocess tests. No legacy alias or experiment command was added. No dependency or version change was required. US-31 IP1's approval remains recorded; US-33 IP1 gate remains pending and US-31 IP2 has not started.

## TDD evidence

The already-approved subprocess test boundary was reused; no private interfaces or mocks were introduced.

1. Renamed the version regression to invoke `agentic-ml`, adding an explicit check that this required command is installed. Ran `uv run --locked pytest tests/integration/test_cli_version.py -k version_reports` before changing package metadata.

   **Red:** exit 1, one failed/one deselected, `AssertionError: Required CLI is not installed`; `shutil.which("agentic-ml")` was None. This demonstrates the missing requested command, not unrelated environment setup.

2. Renamed `[project.scripts]` to `agentic-ml`, ran `uv sync --locked --group dev` (exit 0, rebuilt/reinstalled source package), then `uv run --locked pytest tests/integration/test_cli_version.py`.

   **Green:** exit 0, two tests passed. Version still comes from installed distribution metadata; public import is unchanged.

3. Added `test_help_uses_corrected_cli_name` after the first slice was green. Ran `uv run --locked pytest tests/integration/test_cli_version.py -k help` before changing argparse's program name.

   **Red:** exit 1, one failed/two deselected. Expected stdout prefix `usage: agentic-ml `; actual help began `usage: agent-ml [-h] [--version]`.

4. Corrected argparse's program name to `agentic-ml`. Full regression suite passed: three tests, including version, public import and help. Original expectations were preserved; no suppression, exclusion or workaround was used. No failed corrective attempt remains.

## Final checks

Host: macOS 15.7.9 arm64; Python 3.12.15, uv 0.13.1, pytest 9.2.0, Ruff 0.17.3, mypy 1.20.2.

| Command | Result |
|---|---|
| `uv sync --locked --group dev` | Exit 0; refreshed source install with corrected entrypoint |
| `uv run --locked pytest` | Exit 0; 3 passed |
| `uv run --locked ruff check .` | Exit 0; all checks passed |
| `uv run --locked ruff format --check .` | Exit 0; all files formatted |
| `uv run --locked mypy src tests` | Exit 0; no issues in 3 source files |
| `uv run --locked agentic-ml --version` | Exit 0; `0.1.0`, matching metadata through regression assertion |
| `uv run --locked agentic-ml --help` | Exit 0; `usage: agentic-ml [-h] [--version]` |
| `uv lock --check` | Exit 0; 13 packages resolved |
| `git diff --check` | Passed |
| Markdown file-target validation | Passed |
| Remaining old-name audit | Only annotated historical reports, historical correction records and the superseded spelling in ADR-007; no current command example or entrypoint uses it |

Lock SHA-256 remains `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`, identical to the original IP1 evidence. Editable installation replaced the old console entrypoint; distribution/import names remain unchanged.

## Acceptance coverage and limitations

Renewed source-install evidence for US-33-AC-03 (CLI/import subset), AC-06 (metadata version) and AC-07 (source smoke subset), and updated future US-31-AC-03/05/07 expectations. Both reopened US-33-IP1-T2–T3 tasks are complete again. No isolated wheel/sdist/resource verification, CI execution or fresh-clone macOS verification is claimed. Historical reports alone do not verify the corrected CLI. Changes remain uncommitted; the pending US-33 IP1 developer gate still requires review before US-31 IP2.

## Subsequent developer gate decision

On 2026-10-29, the developer approved US-33 IP1 and requested a commit (“I appove us-33 ip1; commit changes”). The [owning plan](../plans/milestone-0-us-33.md#developer-approval-gate) records approval. Earlier pending-gate statements describe the evidence-presentation state. US-31 IP2 remains unstarted.
