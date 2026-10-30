# US-33 IP3 verification

Status: T1–T4 technically complete, 2026-10-29 local date (hosted runs 2026-10-30 UTC). Final IP3 gate and explicit US-33 acceptance pending.

Issue #3 complete body and all comments retrieved and rechecked: open, one unique comment (6510671946), unchanged update time 2026-10-29T23:10:06Z. Milestone 0 is stated in its body. Approved SC-01 governs `agentic-ml` spelling.

The workflow adds named build and installed-verification steps using exactly the documented local commands. Verification requires successful build; independent development checks continue after unrelated failures. Nonzero exits are preserved, and the final always-run lock comparison is unchanged. Existing PR/main triggers, pinned actions/tools, clean setup and read-only workflow permissions remain.

Local checks on macOS 15.7.9 (24G830), arm64, Python 3.12.15, uv 0.13.1:

| Command | Result |
|---|---|
| `/tmp/us32-ip1-tools/actionlint .github/workflows/ci.yml` | Passed, actionlint 1.7.12 |
| `uv sync --locked --group dev` | Passed |
| `uv lock --check` | Passed |
| `uv run --locked pytest` | 11 passed |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | 53 files already formatted |
| `uv run --locked mypy src tests` | Passed, 6 source files |
| `uv run --locked agentic-ml --version` | 0.1.0, exit zero |
| `uv build --out-dir dist` | Wheel and sdist built into previously absent dist directory |
| `uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir dist` | PASS direct-wheel; PASS rebuilt-wheel |
| Lock SHA-256 and `git diff --exit-code -- uv.lock` | Unchanged: ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d |
| `git diff --check` | Passed |

Both runtime environments contain only agentic-ml 0.1.0; CLI stdout is `0.1.0\n`, stderr empty. Probes confirm public import, metadata/environment isolation and exact provisional resources. Retained workspace: `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-1gozxolo`; subprocess logs are beneath its separate project directories and root.

Artifact SHA-256:

- Direct wheel: `a0caba531383a9ce958c74b26a8d6b210fcf418079aff1ba8c907b409129e441`.
- Sdist: `4c74a64a82ee7bee7e63c056499393abd5eb24edf0679bd122d9949f15f644d3`.
- Wheel independently rebuilt from extracted sdist: `a0caba531383a9ce958c74b26a8d6b210fcf418079aff1ba8c907b409129e441`.

All seven acceptance criteria have local and hosted evidence as mapped below. Existing US-32 evidence remains valid. No default-branch package run, Windows or additional Python version is claimed; default-branch follow-up needs a separately authorized merge.

No product/helper behavior changed in IP3; existing IP2 TDD boundaries/regressions were reused. The hosted workflow failure cases below verify CI behavior, without new tests that mirror YAML structure. No assertions weakened or suppressions added. Initial sandbox API/cache/Git index failures succeeded through escalation. Escalated authentication succeeded via keyring and authorized writes worked. No unresolved implementation failure or scope deviation.

Publication authorized by developer message “I approve the next steps”, 2026-10-29: commit/push implementation PR and disposable hosted failure/correction cases, restore source and close disposable PR without merge. Final gate and merge remain unapproved.

## Hosted execution

Implementation PR #24 baseline revision `9f9c5f042dfb1904780a7a56fcc3dd050b456436` passed [run 40994320116](https://github.com/jimthompson5802/agentic-ml/actions/runs/40994320116). All shared checks, build, both installed paths and final lock comparison passed. Ubuntu 24.04.5 x86_64, Python 3.12.15, uv 0.13.1, pytest 9.2.0, Ruff 0.17.3, mypy 1.20.2. Setup reports image 20261025.353.1; environment variable ImageVersion reports 20261026.354.1; both recorded rather than treating them as identical.

Both Linux wheel hashes: `a0caba531383a9ce958c74b26a8d6b210fcf418079aff1ba8c907b409129e441`; sdist hash `6b46891208047435610dde08720f63a9c36d8dd15a699afae6b1eb320c32110b`. Distinct direct and rebuilt environments under `/tmp/agentic-ml-distributions-b5ksb_p6` each contained only agentic-ml 0.1.0 and passed version/import/metadata/resources checks. CLI stdout `0.1.0\n`, stderr empty. Rebuild used extracted sdist source.

Disposable PR #25 uses a separate branch. Build defect revision `9f1645c6c12f5367275fad0179b7521201515aab` changes backend to `us33_missing_backend` immediately before the build command, after shared development checks. [Run 40994406312](https://github.com/jimthompson5802/agentic-ml/actions/runs/40994406312) failed specifically at Build wheel and source distribution with `ModuleNotFoundError: No module named 'us33_missing_backend'`, process exit 2; installed verification skipped and final lock check passed. Correction revision `f3113a6be7e3999eb99bf0574d89e00e7e9e06d7` restored exact reviewed workflow; `git diff --exit-code 9f9c5f0 HEAD` confirmed entire tree equality.

Build correction [run 40994481417](https://github.com/jimthompson5802/agentic-ml/actions/runs/40994481417) passed every check and both installed wheel paths. One correction attempt, successful.

Resource defect revision `5a594bf68b4438183071a176136be5be976e5a91` replaced only provisional guidance text. [Run 40994573537](https://github.com/jimthompson5802/agentic-ml/actions/runs/40994573537) failed installed verification with `AssertionError: runtime guidance contents differ`, exit 1, affected direct-wheel artifact and workspace printed. Build succeeded despite the earlier regression test detecting the same mismatch; installed verification independently failed, proving independent check execution after a prior check failure. Final lock check passed. The rebuilt path was not reached and is not claimed as passing on this failing revision. Correction restores exact resource from reviewed revision; whole-tree diff confirms equality.

Resource correction revision `895366f68c0889ed15a44961de6d4e819adb8be9` passed [run 40994665653](https://github.com/jimthompson5802/agentic-ml/actions/runs/40994665653), including all shared checks, both wheel paths and lock comparison. One correction attempt, successful. Exact entire tree equals implementation baseline (`git diff --exit-code 9f9c5f0 HEAD`). Disposable [PR #25](https://github.com/jimthompson5802/agentic-ml/pull/25) closed without merge; mergedAt null. Defect commits exist only on disposable branch.

Raw logs and job JSON retained outside Git under `/tmp/us33-ip3-{hosted-baseline,build-failure,build-correction,resource-failure,resource-correction}.*`; permanent run links above expose diagnostic output from the PRs. GitHub log retention applies; no runner workspace upload is configured.

## Final local renewal and acceptance mapping

After exact restoration, all documented shared commands passed again: 11 tests (3.54s), Ruff lint/format, strict mypy, locked sync/check, version smoke 0.1.0; actionlint and lock hash/diff passed. Fresh `uv build --out-dir /tmp/us33-ip3-final-dist` and the same documented driver with that artifacts directory passed both paths. Probe log `/tmp/us33-ip3-final-distributions.log`, workspace ending `agentic-ml-distributions-aqw1vthw`. This verifies the same tree as the implementation branch; subsequent edits are evidence/documentation only.

| Criterion | Evidence |
|---|---|
| AC-01 | Documented build command, baseline hosted build and final local fresh build produce wheel/sdist |
| AC-02 | Baseline hosted direct-wheel probe uses unseeded environment and separate project, no editable/development distributions |
| AC-03 | Baseline both probes verify CLI/import/exact resources; resource mismatch independently fails installed check |
| AC-04 | Baseline extracted-sdist rebuild and fresh rebuilt-wheel environment pass identical probe |
| AC-05 | PR #24 hosted green, PR #25 two distinct red/green pairs, accessible logs, unchanged local commands |
| AC-06 | Both installed probes compare version 0.1.0 with artifact/installed metadata and successful CLI exit |
| AC-07 | Both installed versions and source smoke pass in baseline/corrections and renewed local checks |

No criterion is deferred. Technical verification does not record developer approval or story acceptance. Registry publication, usable initialization/guidance loading and later milestones remain excluded.
