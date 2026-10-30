# US-01 / Implementation Phase 2 evidence

Date: 2026-10-30. [Owning plan](../plans/milestone-1-us-01.md); [issue #8](https://github.com/jimthompson5802/agentic-ml/issues/8). IP2 technical tasks complete; final developer gate and story acceptance pending.

## Authorization and requirements

Developer message “i approve us-01 ip1; commit changes; execute ip2”, 2026-10-30, approved IP1, authorized its commit and IP2 execution. IP1 was committed as `60941af` (`feat(installation): verify pinned harness bootstrap`) before IP2 work. The commit contains the plan, approval record, IP1 evidence, guide, verification code and tests. No push or external publication occurred. Initial sandbox Git index-lock failures were resolved by the approved escalated Git commands; no source correction was needed.

Before IP2, refreshed the complete issue #8 metadata/body and all comment pages; zero comments, stable update time `2026-10-30T02:06:17Z`, open, milestone metadata unset/body Milestone 1. No new scope decision. Approved public boundaries remain applicable. Supporting installation/environment contracts and the [IP1 evidence](us-01-ip1.md) remain authoritative prerequisites.

IP2 adds an optional `--upgrade-revision` to the verification driver, preserves pre-sync metadata/evidence, checks unchanged synchronization, and verifies an explicit upgrade in the same experiment project. Three added subprocess tests cover stable identity, real two-commit local upgrades with unchanged package version, and rejection when declaration/lock claim a new revision but the old package remains installed. The experiment setup guide now includes verified upgrade/review/commit instructions. No product source, runtime resources, dependency declarations, harness lockfile, suppression or CI change.

## Host and exact identities

macOS 15.7.9 (24G830), arm64; CPython 3.12.15; uv 0.13.1; Git 2.54.0. Installation workflow on Linux/Windows or additional Python versions remains unverified. No hosted checks triggered.

Repository: `https://github.com/jimthompson5802/agentic-ml.git`. Both commits are already published; no new commit was published to support this test.

| Installation evidence | Before (A) | After (B) |
|---|---|---|
| Requested, resolved and installed full commit | `018e9d4bb26e121c7f9274d11e0de560b7514b95` | `aead26e9c758878107ad72f230f9e607a9a7ecfa` |
| Exact experiment `uv.lock` SHA-256 | `b08e29f77524c9fd70bc57e8d792e915a357e8355e122c4e1fef8e68efb80673` | `20df20851edc6ab815a1396de63bfaf0837dddc74b2beee31188732256037ac7` |
| Installed version and CLI stdout | `0.1.0` plus newline | `0.1.0` plus newline |
| Installed distributions | Only `agentic-ml==0.1.0` | Only `agentic-ml==0.1.0` |
| Project/environment path | `/private/tmp/us-01-ip2-evidence/github-upgrade/experiment` and its `.venv` | Same project and environment |

The unchanged package version cannot identify the Git source. Changed full commits plus exact project lock hashes distinguish the installation identities. Evidence also records Python implementation/version and platform. This does not introduce a product run-manifest schema or claim complete execution provenance.

The harness development lockfile stayed at SHA-256 `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`; `git diff --exit-code -- uv.lock` passed.

## T1: Red–green and regression evidence

Raw diagnostics are local, retained under [/private/tmp/us-01-ip2-evidence](/private/tmp/us-01-ip2-evidence), outside Git. Temporary evidence is not a permanent hosted artifact.

| Slice | Red command/result | Change | Green command/result |
|---|---|---|---|
| Stable synchronization | `uv run --locked pytest tests/integration/test_installation_verification.py -k locked_sync_preserves -q`: 1 failed because pre-sync identity evidence did not exist | Capture declaration/lock/identity before locked sync, assert unchanged bytes and identity after sync/cache removal, preserve snapshots | `uv run --locked pytest tests/integration/test_installation_verification.py -q`: 10 passed |
| Explicit upgrade | Same targeted pytest command with `-k explicit_upgrade`: 1 failed because `--upgrade-revision` was unrecognized | Validate distinct full upgrade SHA, explicitly add B, locked-sync, require changed declaration/lock/hash, probe installed B after cache removal, preserve A and B evidence separately | Full installation test file: 11 passed |

Logs: `red-01.log`, `green-01.log`, `red-02.log`, `green-02.log`. Both red failures were missing required verifier behavior, not setup failures. Both implementations passed their first green attempt. Added regression of the already-implemented installed revision check: independently change declaration/lock to B while retaining A in site-packages; isolated probe fails with `installed revision mismatch`. Full file then passed 12 tests (`regressions.log`). No extra fabricated red for this existing check. Formatting changes preserve behavior. No failed corrective attempts, weakened criteria, skipped tests or suppressions.

Ordinary tests use local Git fixtures with independent A/B commits, preserving version 0.1.0; they exercise the public driver/probe rather than internal call sequences. Real GitHub acceptance evidence follows separately.

## T2: Real GitHub upgrade and guide verification

Executed:

```sh
uv run --locked python tests/installation/verify_installation.py --repository https://github.com/jimthompson5802/agentic-ml.git --revision 018e9d4bb26e121c7f9274d11e0de560b7514b95 --upgrade-revision aead26e9c758878107ad72f230f9e607a9a7ecfa --workspace /private/tmp/us-01-ip2-evidence/github-upgrade
```

Exit 0; all three outcomes printed: `PASS stable synchronization`, `PASS pinned installation`, `PASS explicit upgrade`. [Combined transcript](/private/tmp/us-01-ip2-evidence/github-upgrade.log).

The driver installed A in a new separate experiment project, preserved original declaration/lock and installed metadata, ran unchanged `uv sync --locked` and checked identical declaration/lock bytes and identical JSON identity. It removed its own dedicated source/build cache and successfully probed A with isolated Python plus offline/no-sync CLI.

Then, in that same project, it ran the exact public upgrade command:

```sh
uv add "git+https://github.com/jimthompson5802/agentic-ml.git" --rev aead26e9c758878107ad72f230f9e607a9a7ecfa
uv sync --locked
```

Both exited zero. The experiment declaration and lock changed to B; the installed direct URL requested/resolved commit and lock source request/resolution all independently matched B. Package version remained 0.1.0. After removing the recreated dedicated installer cache, isolated installed CLI/import/resource/dependency-closure checks and offline/no-sync CLI passed again. The driver removed any empty cache recreated by offline uv. Harness checkout is absent from import paths; installed modules reside in experiment site-packages.

Preserved original evidence: `identity-before-sync.json`, `pyproject-before-sync.toml`, `uv-before-sync.lock`, `identity.json`. Upgraded evidence: `identity-after-upgrade.json` and current experiment declaration/lock. Original A evidence was not overwritten. Review [A identity](/private/tmp/us-01-ip2-evidence/github-upgrade/identity.json), [B identity](/private/tmp/us-01-ip2-evidence/github-upgrade/identity-after-upgrade.json), [declaration diff](/private/tmp/us-01-ip2-evidence/pyproject.toml.diff) and [lock diff](/private/tmp/us-01-ip2-evidence/uv.lock.diff). Per-stage logs in the workspace preserve actual install, locked sync and probe stdout/stderr. A failed later upgrade cannot be established by the earlier installation PASS: the original process exit and final upgrade outcome must also pass.

After updating the guide, independently ran its post-upgrade `uv sync --locked`, `uv lock --check`, locked CLI, metadata/import/resource commands, `shasum -a 256 uv.lock` and Git diff command. All exited zero (`guide-0.log` through `guide-8.log`). These follow-up commands used a separate disposable cache so the acceptance driver's cache-removal evidence remained intact. No fixture cache deletion touched shared caches or the developer's checkout. Git review/commit instructions were inspected; no experiment commit was required or claimed. The user's requested IP1 commit is separate from those documented user steps.

Limitations: installed runtime independence does not promise offline installation or recreation of a removed environment, and uv's offline option does not implement a general network isolation boundary. Initialization, experiment execution and preserved-run compatibility remain downstream work. IP1 invalid-commit, stale-lock and corrupted-resource checks remain covered by regression tests and their original report.

## T3: Final development checks

All exited zero:

| Command | Actual result | Local log |
|---|---|---|
| `uv sync --locked --group dev` | Locked development sync passed | `sync.log` |
| `uv lock --check` | Consistent harness lock | `lock-check.log` |
| `uv run --locked pytest` | 23 passed: 3 CLI, 8 distribution, 12 installation | `tests.log` |
| `uv run --locked ruff check .` | All checks passed | `lint.log` |
| `uv run --locked ruff format --check .` | 60 files already formatted | `format.log` |
| `uv run --locked mypy src tests` | Success: 9 source files | `types.log` |
| `uv run --locked agentic-ml --version` | `0.1.0` plus newline | `smoke.log` |
| Lock SHA-256 and tracked lock diff | Unchanged hash above; empty diff | Recorded here |
| Local Markdown targets and `git diff --check` | Passed after final report/plan/checkpoint updates | Recorded here |

Existing distribution tests build real distributions and verify both fresh installed wheel paths and their established negative cases. Product packaging/resources did not change, so no additional separate build run was required. No checks were skipped or excluded; no dependencies changed. New verification is macOS/Python 3.12 only.

## Acceptance and gate disposition

| Criterion | Evidence | Current technical status |
|---|---|---|
| US-01-AC-01 | IP1 bootstrap guide and successful GitHub install; IP2 upgrade guide and verified commands | Verified; IP1 approved, final IP2 gate pending |
| US-01-AC-02 | A/B noneditable installed probes outside checkout and after fixture-cache removal | Verified; final gate pending |
| US-01-AC-03 | A/B declaration, lock, installed Git metadata, exact CLI/import/resources and dependency closure | Verified; final gate pending |
| US-01-AC-04 | Stable-sync control, actual full-SHA A→B change, changed lock hashes/identity, rejected old-install substitution | Verified; final gate pending |

IP2 T1–T3 technically complete. No scope deviation or unresolved failure. The final implementation gate and developer story acceptance remain pending; stop here. IP2 working-tree changes are uncommitted pending developer review; the requested approved-IP1 commit is `60941af`. No push, PR, GitHub issue edit or next-story implementation was performed.

## Subsequent developer decision

Developer message “i approve ip2; commit the changes”, 2026-10-30, approved the final IP2 implementation gate and authorized its local commit. Earlier pending-gate statements describe the original evidence presentation. Both implementation gates are now approved; explicit story acceptance remains pending.
