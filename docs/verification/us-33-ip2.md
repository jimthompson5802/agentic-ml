# US-33 IP2 verification

Date: 2026-10-29. Story: [issue #3](https://github.com/jimthompson5802/agentic-ml/issues/3). [Owning plan](../plans/milestone-0-us-33.md). Execution authorized by developer message “execute plan for us-33 ip2”. Technical tasks complete; developer approved IP2 with “i approve us-33 ip2; commit changes”, 2026-10-29. No IP3 work, publication, or merge performed.

## Scope and environment

Issue body and all comment pages retrieved successfully; one unique comment, ID 6510671946, confirms reopening after premature closure. Metadata recheck unchanged: open, one comment, updated 2026-10-29T23:10:06Z. Approved SC-01 supersedes historical CLI spelling. Existing prerequisite task/gate records were inspected; US-31 and US-33 IP1 remain accepted.

Verified on macOS 15.7.9 (24G830), arm64; Python 3.12.15; uv 0.13.1 (Homebrew); pytest 9.2.0; Ruff 0.17.3; mypy 1.20.2. Hatchling uses the declared isolated build requirement `>=1.27,<2`; its exact resolved version was not captured. An optional contributor-environment metadata query for Hatchling returned PackageNotFoundError because it is absent there; package builds themselves passed in isolated build environments. Linux package checks belong to IP3; Windows and other Python versions are unverified.

Public boundaries remain those approved in the plan: actual installed entrypoint/import/metadata/resources, real wheel builds, and driver subprocess results. These checks do not establish initialization, runtime guidance loading/selection/restoration, experiment execution, or hosted CI.

## TDD and diagnostics

Commands used the committed lockfile. Each resource slice used `uv build --out-dir /tmp/us33-ip2/NAME`, `uv pip install [--reinstall] --python /tmp/us33-ip2/resource-env/bin/python WHEEL`, and the isolated probe. Initial resource-only probe had no arguments; the final probe requires explicit environment and expected version from its driver.

| Slice | Red evidence | Green evidence |
|---|---|---|
| Template | Baseline installed wheel: FileNotFoundError for installed `templates/provisional.txt` | Added exact provisional template; rebuilt/reinstalled; probe exit 0 |
| Guidance | Template wheel: FileNotFoundError for installed `runtime_guidance/provisional.md` | Added exact provisional guidance; rebuilt/reinstalled; probe exit 0 |
| Direct driver | `uv run --locked pytest tests/integration/test_distribution_verification.py -q`: absent driver command | Implemented direct install/probe; 1 passed |
| Rebuilt driver | Same command: direct success present, rebuilt success absent | Added safe extraction, rebuild and second environment; distribution plus CLI tests: 4 passed |
| Missing template diagnostic | Targeted subprocess test: resource failure lacked `template resource missing` | Added explicit resource-existence assertion; 2 distribution tests passed |
| Altered guidance | Independently damaged wheel failed installed `runtime guidance contents differ` assertion | Original artifact passed both paths; 3 distribution tests passed |
| Wrong CLI | Independently damaged wheel printed `9.9.9`; installed probe failed `CLI version mismatch` | Original artifact passed both paths; 4 distribution tests passed |
| Missing artifacts | Empty directory produced IndexError instead of selection diagnostic | Exact candidate-count validation; 5 distribution tests passed |
| Ambiguity | Extra wheel and extra sdist independently rejected before installation | 7 distribution tests passed, including original artifacts |
| Corrupt archive diagnostics | Good direct wheel passed, unreadable sdist failed without stage identification | Added stage/artifact context; 8 distribution tests passed |

Malformed wheels are generated outside production source and have regenerated RECORD hashes. Expected contents are independent literals. Failures retain nonzero exit; no skipped tests, suppressions, weakened assertions, or dependency changes were introduced. First mypy check reported an importlib metadata `SimplePath` typing mismatch; corrective attempt 1 converted its public path representation to `str` before `Path`. Original mypy check and all tests passed. No unresolved corrective problem or failed corrective attempt remains. Initial uv cache access and one issue metadata recheck hit sandbox restrictions and succeeded through approved escalation.

## Fresh distribution evidence

Commands (both exit 0):

```sh
uv build --out-dir /tmp/us33-ip2/final
uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir /tmp/us33-ip2/final
```

Raw aggregate log: `/tmp/us33-ip2/final-verification.log`. Retained workspace: `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-i4sia78k`. These local temporary paths may expire; findings and identities below are durable review evidence. Artifacts represent executable code and contributor documentation before final evidence/checkpoint updates.

| Artifact | SHA-256 |
|---|---|
| Direct `agentic_ml-0.1.0-py3-none-any.whl` | `a0caba531383a9ce958c74b26a8d6b210fcf418079aff1ba8c907b409129e441` |
| Source `agentic_ml-0.1.0.tar.gz` | `2d9a43ced5158190cd4f6eba270cdb6409856b8c191fea653999315c5d516fba` |
| Rebuilt `agentic_ml-0.1.0-py3-none-any.whl` | `a0caba531383a9ce958c74b26a8d6b210fcf418079aff1ba8c907b409129e441` |

Direct and rebuilt checks both print PASS. The latter runs `uv build WORKSPACE/source/agentic_ml-0.1.0 --wheel --out-dir WORKSPACE/rebuilt`, after validating/extracting the supplied sdist. Matching hashes do not imply reuse: distinct build commands, artifact locations, environments and project directories are recorded in the log.

For each path, runtime prefix is `WORKSPACE/direct-wheel` or `WORKSPACE/rebuilt-wheel`; cwd is the corresponding `*-project` directory. Both use Python 3.12.15 and contain exactly `agentic-ml==0.1.0`, with no pytest, Ruff, mypy or build backend. Import and metadata paths are beneath that path's environment; sys.path contains the interpreter standard library and that environment's site-packages only, with no checkout. No editable metadata is accepted. Absolute installed CLI exits 0, stdout `0.1.0\n`, stderr empty; wheel and installed metadata agree. Both resources equal the exact UTF-8 literals specified in the plan, including final newline. Standard-library `importlib.resources` reads the installed files. No product loader or development guidance is added.

Subprocess logs remain inside each retained workspace: environment/install/probe logs within the appropriate project directory and `sdist-rebuild.log` at workspace root. Build tools are isolated from runtime environments. Normal wheel installation retains declared dependency resolution; current empty runtime dependency declarations are asserted explicitly and require contract review when changed.

## Required contributor checks

| Command | Result |
|---|---|
| `uv sync --locked --group dev` | Pass; 13 resolved, 12 checked |
| `uv lock --check` | Pass |
| `uv run --locked pytest` | 11 passed (3 existing CLI, 8 distribution cases) |
| `uv run --locked ruff check .` | Pass |
| `uv run --locked ruff format --check .` | Pass; 52 files already formatted |
| `uv run --locked mypy src tests` | Pass; 6 source files |
| `uv run --locked agentic-ml --version` | Pass; `0.1.0` |
| `git diff --check` | Pass |
| `git diff --exit-code -- uv.lock` | Pass |

Before/after lock SHA-256: `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`. No lock mutation.

## Acceptance mapping and gate

| Criterion | IP2 evidence |
|---|---|
| US-33-AC-01 | Documented wheel/sdist build command passes |
| US-33-AC-02 | Two independent unseeded runtime environments and separate experiment projects; declared runtime dependencies only |
| US-33-AC-03 | CLI/import and independent exact provisional resource checks pass for both wheels; malformed resource fixtures rejected |
| US-33-AC-04 | Actual build from extracted sdist followed by identical installed probe passes |
| US-33-AC-05 | Local reproduction and stage-specific diagnostics verified; hosted CI portion remains IP3 |
| US-33-AC-06 | CLI/wheel/installed metadata version agreement passes; wrong-version fixture rejected |
| US-33-AC-07 | Both wheel version checks and documented source smoke pass |

IP2 tasks T1–T5 complete. IP2 developer gate approved 2026-10-29. US-33 remains incomplete pending separately authorized IP3 execution/hosted evidence; no story acceptance implied.
