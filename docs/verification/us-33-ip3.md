# US-33 IP3 verification

Status: Partial, 2026-10-29. T1 complete; T2 local checks passed. Hosted T2/T3 and final T4 reconciliation remain incomplete pending explicit publication authorization. No final gate approval or story acceptance is recorded.

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

AC-01–04,06–07 retain IP2 macOS evidence and pass this local renewal. AC-05 is configured and documented; hosted execution and deliberate failure diagnostics remain unverified. Existing US-32 Linux evidence covers development checks only. No hosted package run, revision URL, default-branch package run, Windows or additional Python version is claimed.

No product/helper behavior changed; existing IP2 TDD boundaries and regression tests were reused. Workflow behavior requires the planned hosted build-defect and installed-resource mismatch tests followed by exact restoration and green runs; these are pending publication authorization. No assertions were weakened and no suppressions added. Initial sandbox API/cache failures succeeded through escalation; no failed corrective implementation attempt occurred. Sandboxed `gh auth status` reported invalid credentials, while escalated issue reads succeeded; hosted write access remains untested.

Next authorized publication proposal: commit and push the reviewed implementation to a PR; create a disposable PR to demonstrate a build-backend failure and an altered installed guidance resource separately, restore exact reviewed files and obtain passing corrections, then close disposable work without merging. Preserve immutable run/revision links and logs. No merge or registry publication is included.

Publication authorized by developer message “I approve the next steps”, 2026-10-29: commit/push implementation PR and disposable hosted failure/correction cases, restore source and close disposable PR without merge. Final gate and merge remain unapproved.
