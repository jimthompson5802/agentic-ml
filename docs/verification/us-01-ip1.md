# US-01 / Implementation Phase 1 evidence

Date: 2026-10-30. Owning [plan](../plans/milestone-1-us-01.md); [issue #8](https://github.com/jimthompson5802/agentic-ml/issues/8). Technical tasks complete; developer gate pending. This report verifies US-01-AC-01–03 on macOS. AC-04 upgrade execution remains IP2.

## Authorization and requirements

Developer message “i approve the plan; execute us-01 ip1” approved the plan, public subprocess test boundaries, identity evidence and IP1 execution. It does not approve the IP1 gate or authorize IP2. Refreshed issue #8 complete body and all comment pages; zero unique comments, stable count/update time `2026-10-30T02:06:17Z`; body assigns Milestone 1 and metadata has no milestone object. No new scope decision or requirement conflict. Accepted US-33 package and gates are recorded in its [owning plan](../plans/milestone-0-us-33.md). CLI spelling follows its recorded developer correction and ADR-007.

Changes: [experiment setup guide](../experiment-setup.md), README discovery link, ADR-007 clarification of previously accepted URL/distribution identity, explicit installation driver/probe and nine subprocess regression tests. No harness product code, packaged runtime resources, dependency declarations, development lockfile, CI workflow or suppression changed. Existing installed package behavior is demonstrated rather than reimplemented; executable verification behavior was added with red–green slices.

## Environment and fixture identities

- Host: macOS 15.7.9 (24G830), arm64; CPython 3.12.15.
- Git: 2.54.0; uv: 0.13.1 (Homebrew 2026-10-14); pytest: 9.2.0.
- Repository: `https://github.com/jimthompson5802/agentic-ml.git`.
- Revision A installed from GitHub: `018e9d4bb26e121c7f9274d11e0de560b7514b95`.
- Revision B reserved for IP2: `aead26e9c758878107ad72f230f9e607a9a7ecfa`. GitHub commit/tree APIs confirmed it is published and contains the package, CLI and resources; local A→B diff for `pyproject.toml`/`src` is empty. Both report package version 0.1.0. B was not installed or used for an upgrade in IP1.
- Harness `uv.lock` SHA-256 before/after: `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`; tracked lock diff empty.
- Separate acceptance project: `/private/tmp/us-01-ip1-evidence/github-install/experiment`.
- Project lockfile SHA-256: `b08e29f77524c9fd70bc57e8d792e915a357e8355e122c4e1fef8e68efb80673`.
- Installed inventory: only `agentic-ml==0.1.0`; the virtual project is the other lock record. No contributor or ML dependencies installed in this experiment environment.

Raw local diagnostics are retained under [/private/tmp/us-01-ip1-evidence](/private/tmp/us-01-ip1-evidence). They are temporary local evidence, not permanent hosted artifacts or committed environments. Local fixture installs used temporary pytest directories; they are not GitHub acceptance evidence.

## T1: Tool/source investigation

Read installed `uv help init`, `add`, `sync`, and `run`: `--rev`, `--locked`, `--no-sync`, `--offline` and copy link mode are supported. Chose `uv init --no-package --python 3.12` to keep this bootstrap project minimal; project-package scaffolding remains US-02. uv's source table records a requested full revision, its lock URL contains requested revision plus resolved fragment, and installed `direct_url.json` records repository and requested/resolved Git commits.

Consulted official [uv installation](https://docs.astral.sh/uv/getting-started/installation/), [Git dependency sources](https://docs.astral.sh/uv/concepts/projects/dependencies/#git), [uv caching](https://docs.astral.sh/uv/concepts/cache/), and [Git installation](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) documentation. Upgrade command syntax uses the same explicit `uv add ... --rev FULL_SHA` interface; actual upgrade behavior is deliberately unverified until IP2.

An initial sandboxed GitHub installation failed DNS resolution. The same dependency installation rerun with approved network/cache access passed. The first sandboxed test invocation could not acquire the shared uv cache lock; the approved rerun reached the intended red assertion. These were environment restrictions, not product defects or passing acceptance evidence. No security exception or dependency change was used.

## T2: Bootstrap guide demonstration

Created a fresh outside-checkout project with `git init` and `uv init --no-package --python 3.12`, then ran:

```sh
uv add "git+https://github.com/jimthompson5802/agentic-ml.git" --rev 018e9d4bb26e121c7f9274d11e0de560b7514b95
uv sync --locked
uv lock --check
uv run --locked agentic-ml --version
```

All exited zero. Also ran each guide Python import, installed-metadata and `importlib.resources` command; all exited zero, import was under the project `.venv`, CLI stdout was `0.1.0` plus newline, direct URL was noneditable and pinned to A, and both resources matched the independently specified provisional contents. Logs: `git.log`, `init.log`, and `guide-0.log` through `guide-6.log` under the evidence directory; first sandbox failure retained in `add.log`, successful full installation also retained in the acceptance driver logs.

Git/uv were already installed; their installation instructions were inspected and linked, not reinstalled. User staging/commit instructions were inspected against generated files; no experiment commit was required for installation acceptance and no current-branch commit was made. The guide accurately separates unavailable initialization and future upgrade validation from the commands verified here.

## T3: Small red–green verification slices

Each red command used `uv run --locked pytest tests/integration/test_installation_verification.py ... -q`; green reran the complete installation test file after the corresponding minimal implementation. Raw logs are `red-NN.log` and `green-NN.log` in the evidence directory.

| Slice | Red selection and actual failure | Implemented check | Green result |
|---|---|---|---|
| 01 | Entire initial file: 1 failed because `verify_installation.py` did not exist | Disposable-project driver, normal install, copied isolated probe, identity output and cache-removal/offline runtime path | 1 passed |
| 02 | `-k wrong_revision`: 1 failed because wrong expected SHA was accepted (exit 0) | Compare independently supplied SHA with declaration, lock request/resolution and installed request/resolution | 2 passed |
| 03 | `-k missing_template`: 1 failed because absent template was accepted (exit 0) | Installed template presence and exact independently specified text | 3 passed |
| 04 | `-k altered_guidance`: 1 failed because altered guidance was accepted (exit 0) | Exact installed runtime guidance text | 4 passed |
| 05 | `-k source_mapping`: 1 failed because source mapping without a dependency was accepted (exit 0) | Require the experiment fixture's declared harness dependency | 9 passed, including added regression coverage |

Additional regression coverage exercises already implemented/public tool behavior: missing installed distribution metadata, a mismatched locked resolved SHA, unknown full commit failure at driver installation stage with saved logs/no PASS, and stale-lock refusal without lockfile rewrite. `regressions.log` records 8 passing tests before slice 05. No manufactured red was needed for these checks of behavior already present in Python metadata, uv, or the previous slices. Documentation-only edits used inspection rather than red tests. Each behavioral implementation passed its first corrective verification; no unresolved three-attempt problem, weakened assertions, skipped tests or suppressions.

Public boundaries: real subprocess interfaces and installed resources/metadata, independently chosen expected commit/content, no mocked internal collaborators. Local Git fixtures supply ordinary pytest checks without adding live GitHub acceptance requirements. Build-backend dependency downloads can still be required in an empty cache, as in the existing packaging tests.

## T4: Real GitHub installation and failure boundaries

Executed from the harness development environment:

```sh
uv run --locked python tests/installation/verify_installation.py --repository https://github.com/jimthompson5802/agentic-ml.git --revision 018e9d4bb26e121c7f9274d11e0de560b7514b95 --workspace /private/tmp/us-01-ip1-evidence/github-install
```

Exit 0; `PASS pinned installation`. See [combined transcript](/private/tmp/us-01-ip1-evidence/github-install.log), [identity JSON](/private/tmp/us-01-ip1-evidence/github-install/identity.json), and per-stage logs in the printed workspace.

The driver created its own experiment project and `UV_CACHE_DIR`, used `UV_LINK_MODE=copy`, cleared import/active-project overrides, and copied the stdlib probe outside the checkout. After full-SHA installation and locked synchronization, it removed only its fixture-owned installer cache. The project interpreter ran the probe with `-I`: import and metadata identities, CLI version, package resources and dependency closure all passed. Its import path contained the Python standard library and experiment site-packages, with no harness checkout. The subsequent `uv run --no-sync --offline agentic-ml --version` exited zero after cache removal; any empty cache directory recreated by uv was removed too. This is installed runtime independence, not a promise of offline installation/restoration or general code network isolation.

Real GitHub negative checks, saved by local `check_boundaries.py`:

- Driver installation at `0000000000000000000000000000000000000000` exited 1, `FAIL install`; Git reported `not our ref`. No PASS or accepted project. See [GitHub invalid-commit transcript](/private/tmp/us-01-ip1-evidence/github-invalid.log).
- Temporarily changed the accepted experiment's project version from 0.1.0 to 0.2.0 without changing its lock, ran `uv sync --locked`, and received exit 2: lockfile “needs to be updated”. Exact lock bytes/hash were preserved. Restored the original declaration in `finally`. See [stale-lock transcript](/private/tmp/us-01-ip1-evidence/github-stale-lock.log). This checks stale project metadata; A→B pin upgrades remain IP2.

No partial install, import from source, package-version-only identity, or successful notebook execution was substituted for these checks.

## Required development checks

All commands below exited zero on the host described above. Logs use the indicated names in the evidence directory.

| Command | Result | Log |
|---|---|---|
| `uv sync --locked --group dev` | Resolved 13 / checked 12 packages; development environment synchronized | `sync.log` |
| `uv lock --check` | Lock consistent | `lock-check.log` |
| `uv run --locked pytest` | 20 passed: 3 CLI, 8 distribution, 9 installation | `tests.log` |
| `uv run --locked ruff check .` | All checks passed | `lint.log` |
| `uv run --locked ruff format --check .` | 59 files already formatted | `format.log` |
| `uv run --locked mypy src tests` | Success, 9 source files | `types.log` |
| `uv run --locked agentic-ml --version` | stdout `0.1.0` plus newline | `smoke.log` |
| `git diff --exit-code -- uv.lock` and before/after SHA-256 | Empty tracked diff and unchanged hash above | Recorded here |
| Local Markdown link targets and `git diff --check` | Passed after final documentation updates | Recorded in plan/checkpoint |

The existing distribution test suite built real artifacts and passed both fresh installed wheel paths, plus all existing failure cases. Product source, package metadata and resources did not change, so a separate additional distribution run was not necessary. No hosted CI event was triggered, and no Linux/Windows or additional Python installation workflow verification is claimed.

## Acceptance and gate disposition

| Criterion | IP1 evidence | Status |
|---|---|---|
| US-01-AC-01 | Official prerequisite links, actual separate project bootstrap, full-SHA GitHub installation and guide probes | Verified on macOS/Python 3.12; developer gate pending |
| US-01-AC-02 | Noneditable installed metadata, outside-checkout import paths, removed disposable source cache and successful runtime probes | Verified; developer gate pending |
| US-01-AC-03 | Matching declared/locked/installed full SHA, installed dependency closure, CLI/import/resource checks | Verified; developer gate pending |
| US-01-AC-04 | Published A/B identified, command syntax inspected | Not complete; explicit upgrade and changed identity belong to IP2 |

No implementation scope deviation. Clarifications of minimal `uv init --no-package` and fixture-only verification/identity are within the approved plan. No new product identity API, runtime guidance loader or initialization capability was introduced. Developer approval of IP1 is pending; stop before IP2. Story acceptance remains pending.

## Subsequent developer decision

Developer message “i approve us-01 ip1; commit changes; execute ip2”, 2026-10-30, approved the IP1 gate, authorized committing these changes and executing IP2. Earlier pending-gate statements describe the original evidence presentation. IP2 gate and story acceptance remain separate.
