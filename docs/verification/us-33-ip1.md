# US-33 Implementation Phase 1 verification

> Historical CLI spelling: this report preserves the original `agent-ml` references. The developer corrected the CLI to `agentic-ml` on 2026-10-29; see [ADR-007](../specs/design/architecture-decisions.md#adr-007--github-package-installation-and-project-initialization) and the [correction verification](../verification/cli-name-correction.md). Original results below are historical evidence, not verification of the renamed command.

Date: 2026-10-29. Source: [US-33 / issue #3](https://github.com/jimthompson5802/agentic-ml/issues/3). Tasks US-33-IP1-T1–T3 are owned by the [CLI prerequisite plan](../plans/milestone-0-us-33.md). Progression was authorized by developer message “i approve” after the US-31 IP1 review and convention questions; the [US-31 gate record](../plans/milestone-0-us-31.md#developer-approval-gate) records approval. The earlier gate-review request explicitly asked for approval to authorize progression to this CLI prerequisite.

## Scope and prerequisites

US-31-IP1-T1–T3 were complete with [tooling evidence](us-31-ip1.md) before this implementation phase; their developer gate is approved. Plan approval confirmed public subprocess/import boundaries. The execute-plan and TDD skills governed execution. No additional seams or scope were introduced.

Before implementation, issue #3's complete body and all comment pages were refreshed. It remains open with zero comments; repeated metadata retained updated_at `2026-10-29T03:09:12Z` and zero comments. Its body assigns Milestone 0; no GitHub milestone object is set. There are no new scope decisions or conflicts with the approved plan.

Host remains macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1, pytest 9.2.0, Ruff 0.17.3, mypy 1.20.2. Product code uses standard-library argparse and importlib.metadata; no new dependencies or lock regeneration were required. `agentic-ml` distribution version is 0.1.0; CLI is agent-ml and import is agentic_ml.

## TDD sequence

1. Wrote `tests/integration/test_cli_version.py::test_version_reports_installed_distribution_version`. Its expected version comes from installed distribution metadata; it invokes the real console entrypoint from a temporary working directory and checks successful exit, stdout version, and empty stderr.
2. Created only the installable package/console skeleton needed for test execution, with an empty CLI callable. Ran `uv sync --locked --group dev` successfully, followed by `uv run --locked pytest tests/integration/test_cli_version.py`.
3. **Red:** one test collected, one failed. Console entrypoint ran successfully but printed no version. The failure was missing required behavior, not setup/dependency failure:

```text
assert result.stdout.strip() == expected_version
AssertionError: assert '' == '0.1.0'
1 failed in 0.24s
```

4. Added argparse's version action using the installed distribution metadata, with no fallback constant. **Green:** reran the identical pytest command; `1 passed in 0.05s`.
5. After the first slice was green, added `test_package_imports_from_outside_checkout`, using the environment's Python with `-I -c 'import agentic_ml'` from a temporary directory. This behavior already existed in the installable skeleton; the plan allows a regression test without manufacturing a red when behavior is already present. Both tests passed (`2 passed in 0.07s`). No mocks, source-path manipulation or private-interface assertions are used.

## Shared checks and corrective attempt

The first shared lint run reported I001 (test imports not sorted); format, type and version checks passed. Corrective attempt 1: `uv run --locked ruff check --fix tests/integration/test_cli_version.py` fixed import ordering (`1 fixed, 0 remaining`). Reran the original lint command and all shared checks; all passed. No suppression, exclusion, skipped test, assertion weakening, or workaround was introduced. Review found no further refactoring needed for the minimal behavior.

| Command | Actual result |
|---|---|
| `uv sync --locked --group dev` | Exit 0; source package built and installed as agentic-ml 0.1.0 |
| `uv run --locked pytest` | Exit 0; 2 tests collected and passed |
| `uv run --locked ruff check .` | Exit 0; All checks passed |
| `uv run --locked ruff format --check .` | Exit 0; 40 files already formatted at initial final verification |
| `uv run --locked mypy src tests` | Exit 0; no issues in 3 source files |
| `uv run --locked agent-ml --version` | Exit 0; stdout `0.1.0` |
| `uv lock --check` | Exit 0; resolved 13 packages |
| `git diff --check` | Passed |
| Local Markdown file-target validation | Passed for changed guidance, plans, checkpoint and verification reports |

Lock SHA-256 remains `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`, identical to the US-31 IP1 checksum. Adding the console script required no dependency resolution change. Existing Python code-block formatting corrections from US-31 remain in the working tree; no further product contracts were changed.

## Acceptance coverage and limits

- US-33-AC-06: source-installed version behavior verified; expected version independently read from distribution metadata.
- US-33-AC-03: public import/CLI subset advanced. Provisional resources and isolated distribution checks remain deferred.
- US-33-AC-07: source smoke advanced; both wheel paths and US-31 fresh-checkout smoke remain pending.

This is editable source-install evidence, even though subprocesses run from temporary directories. It does not establish wheel/sdist completeness, installation without development dependencies, packaged resources, fresh-clone setup, CI success, or other-platform support. Full US-33 acceptance and Milestone 0 completion are not claimed. Stop for the US-33 IP1 developer gate before US-31 IP2; that gate remains pending. Changes remain uncommitted.

## Subsequent developer gate decision

On 2026-10-29, the developer approved US-33 IP1 and requested a commit (“I appove us-33 ip1; commit changes”). The [owning plan](../plans/milestone-0-us-33.md#developer-approval-gate) records approval. Earlier pending-gate statements describe the evidence-presentation state. US-31 IP2 remains unstarted.
