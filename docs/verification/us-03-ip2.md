# US-03 IP2 — Execution evidence

Authorized by developer “execute us-03 ip2”, 2026-10-31. IP1/public boundaries
approved; [owning plan](../plans/milestone-1-us-03.md), issue #10,
Milestone 1, US-03-AC-01/03/04/05. IP2 complete; developer gate approved
by “lgtm ip2” on 2026-10-31. Earlier in-progress records are historical.

Issue #10 body and all comment pages refreshed successfully: zero unique/reported
comments; final metadata stable at `2026-10-30T02:06:20Z`. Sandbox refresh network
failure retried successfully with escalation. Scope unchanged.

Public boundaries and selection remain the approved IP1 matrix. Focused serial
pytest runs are short TDD cycles; gate verification uses four workers/loadgroup.
Resources/shared schema additions require full suite and both installed paths.
Search narrowing remains IP3 and approval completion IP4.

## TDD log

Commands below use `uv run --locked pytest tests/integration/test_planning.py -q`
unless a selector is specified. Initial uv cache denial is infrastructure, not red.

- Explicit capture: initial missing package collection failure prompted public
  interface scaffolding; actual behavior red was blocked vs input_ready, 1 failed.
  Minimal deterministic capture green: 1 passed.
- Strict brief validation: 7 failed/1 passed (TODO, task, bool budget, direction,
  duplicate key, heading and unknown field); schemas/parser green: 8 passed.
- Delegations/conflicts: 6 failed/8 passed; derived pending/proposed decisions,
  split/features/cost consistency green: 14 passed.
- Paths/config `-k unsafe`: 7 failed/14 deselected. Attempt 1 implemented bounded
  descriptors/schema checks; full focused verification: 4 failed/17 passed.
  Hypothesis: `.` stat used an empty basename and symlink reads raised operational
  errors. Attempt 2 uses fstat for root and prechecks no-follow metadata;
  verification: 21 passed. No third attempt required; original assertions intact.

No checks suppressed, disabled or weakened. Installed/full/shared verification
pending; source-checkout tests alone do not establish installed acceptance.

## Further behavior and verification

- Exact preservation slice: red 1 failed/21 deselected (missing manifest), green
  22 passed. Sources, plan and manifest use independently recomputed hashes;
  changed brief bytes create a distinct bundle and retain the old one.
- Verify/inspect slice: red 1 failed/22 deselected (readiness stub), green 23
  passed. Default verifies preserved bytes; check-current rejects current drift.
- CLI slice: red 3 failed/23 deselected (missing command). Attempt 1 failed with
  Python 3.12 eager evaluation of argparse's stub-only generic; attempt 2 deferred
  annotations, green 26 passed. Root/nested/unrelated cwd identities agree.
- Interim override guard: red 1 failed/26 deselected, green 27 passed. IP2 blocks
  nonempty execution overrides with `boundary_validation_pending`; IP3 owns
  narrowing. No override is silently dropped or claimed verified.
- Installed inventory slice: red 1 failed/10 deselected because removing plan.json
  schema did not fail installed checks. Added explicit six-schema inventory and
  public API checks: green 1 passed/10 deselected.
- Additional independent behavior checks cover missing/extra/duplicate/symlink
  bundle members, altered decisions with recomputed hashes, stale locks/partial
  staging, concurrent resolution, task/mode variants and external references.
  Combined focused run: 40 passed/10 deselected in 15.49s, including both direct
  and rebuilt installed probes. This preceded later publication refinements and
  is historical artifact evidence, not final-artifact verification.
- Prepublication staging verification refinement attempt 1 failed (19 failed,
  19 passed) because a formatted multiline signature escaped the scripted edit.
  Attempt 2 completed the staging-reader signature. Four-worker correction run:
  `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py
  --junitxml=/private/tmp/us03-planning-targeted-corrected.xml`: **38 passed**,
  0 deselected, 0.93s. Original failure XML retained at
  `/private/tmp/us03-planning-targeted.xml`. No assertions altered.
- Lint correction reported five import fixes and zero remaining errors at that
  point; formatting then changed 12 files. Subsequent edits require renewed
  lint/format checks before the gate. `git diff --check` passes.

## Blocker — strict typing, third unsuccessful corrective attempt

Original requirement: `uv run --locked mypy src tests` must pass without
suppressions before the IP2 gate. Initial diagnostic check of planning/CLI source
reported five errors: nullable YAML nodes/regex matches, recursive JSON origin
inference and CLI result union typing. All recorded attempts address this same
unresolved strict-type verification problem; the count does not reset when newly
revealed diagnostics move into the installed probe.

| Attempt | Hypothesis and corrective changes | Verification result |
|---|---|---|
| 1 | Mark the raising validation helper `NoReturn`, annotate recursive JSON origin and CLI result union; add docstrings/naming/import cleanup. | `uv run --locked mypy src tests`: 19 errors in two test files; unpacked mixed-type argument dictionary and recursive JSON indexing/return typing remained. |
| 2 | Replace mixed kwargs dictionary with explicit arguments; narrow inspection mappings; annotate probe command results with JSONValue and cast parsed JSON. A new bounded-YAML scan accompanied independent storage refinements. | Same command: four errors in two files. JSONValue import was missing; the new YAML event mark was nullable. |
| 3 | Import JSONValue and handle absent event marks explicitly. | Same command: five errors in one file, `tests/installation/check_planning.py:206,210`. Resolving the previously unknown alias exposed nested command-result indexing that still lacks type narrowing. Exit 1. |

The final unchanged diagnostic run was saved in
`/private/tmp/us03-ip2-mypy-blocker.txt`. It reports unsafe indexing of
`bool | int | float | str | list[JSONValue] | dict[str, JSONValue] | None` and
invalid integer/string index combinations in the CLI diagnostic assertion.
No product runtime failure is inferred from these type diagnostics. No further
corrective changes were made after attempt 3. Repository AGENTS.md requires
stopping and developer direction at this point.

Possible next step for developer authorization: permit another focused correction
that assigns the CLI response/diagnostics/first item to local variables, checks
their actual mapping/list types, then reruns the unchanged strict checker and
relevant tests. Alternatively the developer can edit that assertion. This is a
proposal only; it is not implemented and no check exclusion is proposed.

## Handoff and remaining obligations

IP2 is **partial**, with no task or gate declared complete. Base commit
`3c72694e52e76625a1801554e2dacee621faac150`, branch
`US-03-experiment-boundaries`; changes remain uncommitted. New planning models,
strict parser, descriptor paths, immutable storage/resolution, six schemas,
CLI dispatch and public/installed probes are in the working tree. Existing
initialization templates, dependencies and lock are unchanged. Lock SHA-256:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

Before an IP2 gate, finish strict typing under new developer direction; review
remaining IP1 matrix coverage, source-race and storage fault boundaries, public
schema/resource validation and initialization coexistence/conflict cases; renew
lint/format/shared checks and installed probes, and run the unfiltered full suite
(including both artifact paths and full installed initialization). No full suite,
final artifact identity, full phase coverage or final shared-check pass is claimed.
The two wheel paths must be renewed after subsequent source edits. Shared sync,
lock-check and smoke commands are still pending for the phase gate. No unrelated
checks are waived; IP4-T4 retains final-story verification ownership.

Local observations: macOS/darwin, Python 3.12.15, pytest 9.1.1, xdist 3.8.0.
No new Linux/Windows verification. Dataset execution, scientific validity,
registry/search narrowing and delegated approval completion remain outside IP2.
IP3 remains unauthorized. No commit, push, GitHub comment or publication made.

## Authorized correction and resumed IP2 verification

Developer “ok that makes sense make that change” explicitly authorized the
proposed fourth strict-typing attempt. Prior attempts and failure evidence remain
above. Added local `response`, `diagnostics`, and `first_diagnostic` variables,
asserting list/dictionary types before retaining the original source-path
assertion. No casts, suppressions or weaker assertions were added.

- `uv run --locked mypy src tests`: **passed, 31 files**.
- `uv run --locked pytest -n 4 --dist=loadgroup
  tests/integration/test_planning.py
  tests/integration/test_distribution_verification.py -k
  'planning or bundles or interrupted_storage or concurrent_resolvers or
  explicit_task or external_references'
  --junitxml=/private/tmp/us03-ip2-authorized-correction.xml`:
  **40 passed**, 10 deselected, 12.38s; direct/rebuilt installed planning probes
  passed. Typing blocker resolved on the one additionally authorized attempt.
- Resuming the original IP2 execution exposed nonmapping project configuration
  raising `ValueError` before schema validation. Regression red:
  `uv run --locked pytest tests/integration/test_planning.py -k
  nonmapping_project -q`: 3 failed/38 deselected. One correction validates raw
  project input before mapping access. Full planning serial regression green:
  41 passed. Serial execution was a short TDD cycle.
- Added coverage of every required brief field, incomplete delegation envelopes,
  YAML extensions/invalid scalars, exact CRLF/annotation bytes, input size/depth
  limits, unsafe stores and configured-store overlap. These check the existing
  implemented behavior without manufacturing new reds. Four-worker run
  `uv run --locked pytest -n 4 --dist=loadgroup
  tests/integration/test_planning.py --junitxml=/private/tmp/us03-ip2-coverage.xml`:
  **75 passed**, 0 deselected, 1.04s.
- Locked development sync and lock consistency passed. Repository lint passed;
  formatting passed (95 files); strict typing passed (31 files); version smoke
  printed `0.1.0`, exit 0. Later changes must renew affected evidence.

Historical handoff text above describes the earlier stop, superseded by this
explicit authorization and successful correction. Final phase verification and
approval remain pending while initialization coexistence and broad checks run.

## Initialization compatibility and final run in progress

Added an installed regression exercising planning in a fully initialized,
full-SHA Git dependency project, rather than only declarative miniature fixtures.
The standalone probe now optionally uses an existing initialized project,
preserving project metadata/dependencies and existing draft files. Expected
scientific decisions and hashes remain independently checked through installed
CLI/API; no harness source imports or test collaborator mocks are introduced.

- Red: `uv run --locked pytest tests/integration/test_initialization.py -k
  versioned_planning_inputs -q`: 1 failed/103 deselected, because the probe did not
  yet accept an existing project. Added that probe mode; same command green:
  **1 passed/103 deselected**, 49.92s. Serial run was a focused TDD cycle.
- Installed planning retains pyproject/lock/project/notebook bytes and inert
  draft bytes. Normal initialization rerun succeeds. Putting the reviewed 1.0
  execution config at an owned 0.1 draft path makes init report a conflict and
  preserves the reviewed bytes. No initialization source/template/schema changed.
- Final shared lint passed; formatting passed (95 files); typing passed (31
  files); version smoke passed (`0.1.0`). Locked sync/lock-check passed earlier
  against the same dependency inputs.
- Broad verification launched:
  `uv run --locked pytest -n 4 --dist=loadgroup
  --junitxml=/private/tmp/us03-ip2-full.xml --durations=20`.
  **207 collected**, no selection filters or exclusions. Result pending.
- Tested source/test/build-input inventory:
  `/private/tmp/us03-ip2-tested-files.json`, 52 files, inventory SHA-256
  `fc65d30df59e8bf4b1fc444fa0ae163199ef10be3c7a5959bd91975d82197f41`.
  Runtime/test edits are frozen during this full run. Documentation/approval
  records may change without invalidating unchanged executable inputs.

## Final IP2 verification and review handoff

**Technical status:** IP2-T1–T4 complete; **developer IP2 gate approved**
by “lgtm ip2”, 2026-10-31.
The strict-typing blocker is resolved by the explicitly authorized fourth attempt.
No approval of IP2, IP3 execution, whole-story acceptance or publication inferred.
Earlier pending/blocker statements above are historical records.

### Full run and narrowly affected evidence renewal

The unfiltered four-worker run completed successfully: **207 passed, 0 failed,
0 skipped, 0 deselected**, exit 0, **788.72s (13:08)**. XML:
`/private/tmp/us03-ip2-full.xml`. This includes all initialization, CLI,
distribution, pinned-installation and scheduling regressions, normal direct and
sdist-rebuilt distribution checks, full installed initialization on both paths,
and installed planning checks. No filters, exclusions or weakened assertions.

Final contract review then found a precise source-location defect: duplicate YAML
keys inside the brief reported a line relative to the fenced block (4), rather
than the original Markdown file (14). Red:
`uv run --locked pytest tests/integration/test_planning.py -k
original_markdown_line -q`: **1 failed/75 deselected**. One correction translates
strict-YAML error positions by the fence's offset while preserving code, field,
source path, column and message. Serial planning green: **76 passed**, exit 0.
Serial execution was a short focused TDD cycle; pytest's old-temporary-directory
cleanup extended process completion to 270.30s after cases finished.

Renewed affected verification against the final executable identity:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_distribution_verification.py tests/integration/test_initialization.py -k 'planning or versioned_planning_inputs' --junitxml=/private/tmp/us03-ip2-final-affected.xml
```

**79 passed, 113 deselected**, exit 0. XML records 90.755s of test execution;
including post-test cleanup the command completed in **242.56s (4:02)**.
Selected cases comprise all 76 planning cases, missing-schema and both-wheel
planning checks, and planning in a fully initialized pinned project with safe
init rerun/schema conflict. All renewed installed probes passed. Both completed
processes were observed exiting zero; no process was cancelled. Remaining-count
updates were supplied as requested, including zero while cleanup completed.

**Impact rationale:** The only changes after the full run are the planning
parser's fenced-YAML diagnostic translation and its new public regression
(`src/agentic_ml/planning/parsing.py`,
`tests/integration/test_planning.py`). Schemas, dependency/build inputs,
initialization, authorization, execution and other shared code did not change.
All planning behavior and affected installed/project interfaces were renewed;
final lint/format/types/version checks passed. This is an intermediate gate under
the impact-based policy, not a claim that the earlier 207-test run exercised the
later line-offset change. The final repository now has 208 cases. IP4-T4 must run
the unfiltered suite again against the final story implementation before its final
phase approval and story acceptance. No unrelated IP2 regression check remains
deferred; all unrelated cases passed in the full run.

### Shared checks, identity and artifacts

| Command/check | Final outcome |
|---|---|
| `uv sync --locked --group dev` | Passed; 195 resolved, 193 checked; no dependency changes |
| `uv lock --check` | Passed; 195 resolved |
| `uv run --locked ruff check .` | All checks passed |
| `uv run --locked ruff format --check .` | 95 files already formatted |
| `uv run --locked mypy src tests` | No issues in 31 files |
| `uv run --locked agentic-ml --version` | Exit 0, `0.1.0` |
| `git diff --check` | Passed |
| Local Markdown file/anchor targets | 34 checked/passed before final handoff edits; renewed below |
| Lock SHA-256 before/after | Unchanged: `90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8` |

Base `3c72694e52e76625a1801554e2dacee621faac150` plus uncommitted story changes.
Final source/test/build-input inventory (52 files):
`/private/tmp/us03-ip2-final-tested-files.json`, SHA-256
`d4f0b55bd9a1e73a922c12da5ffb7e1df5bc0c734a66abbdefb17aa13ad74b8a`.
Verified unchanged after final affected tests. Earlier full-run inventory and
hash remain above, explicitly distinct. Later documentation/approval records
have no executable impact and require document checks only.

Final reviewed artifacts/logs retained in `/private/tmp/us03-ip2-final-evidence/`:

- Direct wheel SHA-256:
  `eaac278f4f52ea872ba9ec2464c963e318ff907c91e51b431df3ffd7e3bc8bea`.
- Source distribution SHA-256:
  `3830bc2e8b79ee2f49185dc7b56bcf5b2afa765d6ad1f382f656d64c05b76f4e`.
- Independently rebuilt wheel SHA-256 matches the direct wheel; verified through
  its own normal installation/environment and isolated probe, not substituted.
- `distributions.log`, `direct-wheel.log`, `rebuilt-wheel.log` preserve both
  installed paths and PASS observations. Rebuild/runtime workspace:
  `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-050xi6cm`.
- Full-run earlier wheel/sdist hashes were respectively
  `2415fdf61fe105020f728cc81a6fd08175fadd91afd34c8e5db76d64f51ed77b` and
  `7491965f471e9176266c1e869ed1e402904622c3f16fdcf22ad307e9f73345ad`.
  Pytest retention removed that older artifact directory during later cleanup;
  full-run XML and source inventory remain, and final artifacts are copied out
  of pytest retention. No claim that the removed directory is still available.

Local platform: Darwin 24.6.0 arm64 (macOS), Python 3.12.15, uv 0.13.1,
pytest 9.1.1, xdist 3.8.0. No new Linux/Windows/remote-filesystem evidence.

### Criterion and task reconciliation

| Task / criteria | Verified observations and scope |
|---|---|
| IP2-T1 / AC-01, explicit/pending AC-04 | Required brief fields, classification/regression and use/select/compare intent; missing/TODO/unknown/duplicate/conflicting input; strict YAML/delegation envelopes; preserved pending/proposed choices; source-located diagnostics; draft/config-version blocking; CLI/API agreement |
| IP2-T2 / AC-05 | Root/nested/unrelated cwd, explicit root, spaces, explicit notebook cwd, no API chdir, root-relative input identity, absolute/escape/symlink rejection, external data references without dataset opening or kernel/code execution |
| IP2-T3 / AC-03, pending AC-04 | Exact preserved source bytes, independent hashes/member inventory, deterministic identity/reuse and new versions, retained old bundles, current drift checks, missing/extra/duplicate/symlink/corrupt evidence, rehashed effective-decision corruption, staging/stale lock recovery boundaries, concurrent writers, package resources, pin/lock/draft preservation |
| IP2-T4 / AC-01/03/04/05 evidence | TDD and attempt records, shared checks, unfiltered suite, final affected/installed renewal, platform/artifact identities and gate handoff recorded |

US-03 as a whole is **not complete**. IP3 owns detailed search-space validation
and narrowing; nonempty execution overrides currently block with
`boundary_validation_pending`. IP4 owns unauthenticated approval/revocation and
final acceptance evidence. Pending delegation is never approval, and input_ready
is not data access, execution authorization or scientific validity. No source,
tests, assertions, dependency pins, tool checks or development gates were relaxed.
No scope revision, commit, push, external comment or publication made in IP2.

Final handoff document checks renewed: **34 local Markdown file/anchor targets passed** across the checkpoint, owning plan, IP2 report and setup guide; `git diff --check` passed. No executable inputs changed.

## Developer disposition

Developer “lgtm ip2” (2026-10-31) approves IP2 after the verification/plan
summaries and runnable demo instructions. Recorded in the owning plan and
checkpoint. IP3 execution, whole-story acceptance, commit and push remain
unauthorized. This approval-record update changes documentation only; TDD,
product tests and distribution rebuilds do not apply. Existing executable
verification remains unchanged; local links/anchors and whitespace checked.

## Commit and push authorization

After IP2 approval, developer “commit and push” authorizes committing and
publishing the approved IP2 implementation, verification and approval records on
`US-03-experiment-boundaries`. Git history and the delivery response identify the
commit/push outcome. No PR, merge, whole-story acceptance or IP3 execution is
requested. Verified all 52 final executable/build-input hashes still match the
final tested inventory; subsequent changes are documentation records only.
