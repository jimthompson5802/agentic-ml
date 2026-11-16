# US-14 Implementation Phase 3 verification

Status: **Complete — Automatic — verification passed**; whole story accepted
on 2026-11-16 UTC. Developer “i approve phase 3”, 2026-11-15 UTC, authorizes
execution. It does not approve unfinished results or whole-story acceptance.
[Plan](../plans/milestone-1-us-14.md), [contract v2](../feature-pipelines.md),
[IP2 evidence](us-14-ip2.md).

## Boundary and prerequisites

Owning checkout: `.worktrees/US-14-feature-pipelines`, branch
`US-14-feature-pipelines`, starting HEAD `762aa237d9b5` (Phase 2 implementation
and approval). Registered worktrees, primary/common Git directory and clean
starting state were verified. No fetch, merge or sibling change. Contract v2
and IP2 prerequisites retain their approvals and passing results.

Issue #20 body, all comment pages and final metadata were refreshed. One unique
comment matches the reported count; updated_at remains 2026-11-15T20:05:03Z.
GitHub milestone is null; the body assigns all five criteria to M1. Scope and
current verification policy agree. No GitHub write was performed.

Locked synchronization uses this worktree's own `.venv`; uv explicitly ignores
the inherited primary-checkout VIRTUAL_ENV. Initial sandbox cache writes failed;
the same synchronization passed with runtime escalation. Retain the unchanged
lock digest and actual environment identities in raw records.

The public test boundary is unchanged: copy the exact project recipes, invoke
their entrypoints through installed interfaces from an unrelated cwd, and inspect
native outputs independently. No toolkit runtime behavior is added in this phase,
so no manufactured product red is required. The new contributor verifier is
checked first: the initial installed test failed because its driver was missing,
after successfully building real artifacts. Its implementation extends existing
verification support without changing assertions, timeouts, skips or exclusions.

## Installed matrix

The new `test_installed_feature_comparison.py` uses the existing real artifact
fixture and distribution xdist group. Its driver invokes the unchanged
distribution verifier, retains the actual wheel rebuilt from extracted sdist,
and independently installs each wheel into a fresh runtime-only project. The
child retains CLI/import/resource/dependency checks. No direct-wheel substitution,
editable install or toolkit checkout import is allowed.

`check_feature_comparison.py` runs under isolated Python outside the project,
initializes the normal installed project and executes the copied preparation and
comparison scripts. It verifies literal predictions, accuracy/loss outcomes,
mixed numeric/categorical feature values, row order/dtypes, native models,
committed provenance and DVC status. Native failure probes cover missing input,
unknown variant, invalid committed provenance and artifact storage failure.
Completed outputs and original native diagnostics are retained in the invocation
records before owned environments are removed after success.

Initial mypy check found one untyped JSON return in the contributor verifier.
Correction: annotate its validated provenance mapping explicitly; no suppression
or checker exclusion. Final verification passed as recorded below.

## Results and acceptance

The results below retain incremental history. Installed matrix, focused checks,
M1–6/shared checks and final document reconciliation are now complete.
Whole-story acceptance remains explicitly pending.

Initial installed verification: `installed-matrix-red` failed only because the
new driver was absent; `installed-matrix-green-attempt1` passed the complete
both-wheel matrix in 146.44 seconds. The contributor provenance return annotation
was made explicit after mypy identified it; no runtime behavior changed.
The final focused run additionally asserts the copied recipe hashes, independent
normal wheel identities/prefixes and the logged genuine rebuild command.

Final focused selection passed **45 tests**, 0 failures/errors/skips, in 244.60
seconds. It includes all 43 recipe cases, both-wheel comparison verification and
the unchanged both-wheel installed training regression. Shared checks pass:
Ruff, formatting (386 files), mypy src/tests (103 files), source/examples (49 files),
CLI version 0.1.0 and lock consistency. M1–6 story verification is now running.

The M1–6 run selected 1,027 cases. One existing developer-authorized skip
is visible: `test_missing_planning_schema_fails_installed_inventory` (US-03
AC-03), retained for its unresolved 120-second timeout investigation. The two
other documented temporary skips are M50 and outside this selection. No new skip
was added or re-enabled. The omitted damaged-planning-resource check remains
with historical M1-ACCEPT-VERIFY, not passing US-14 evidence. Current US-14
normal-wheel resource inventories are positively verified by the nested driver.
The final session result is recorded below; the skipped case is not passing evidence.


## Final commands and outcomes

| Command | Result |
|---|---|
| `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_installed_feature_comparison.py --tb=short` | 1 passed; both artifact paths; 146.44s |
| `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_feature_comparison.py tests/integration/test_installed_feature_comparison.py tests/integration/test_installed_training.py --tb=short` | 45 passed, 0 failures/errors/skips; 244.60s |
| `uv run --locked pytest -n 4 --dist=loadgroup` | M1–6: 1,026 passed, 1 existing skip, 0 failures/errors; 670.56s |
| `uv lock --check` | Passed; initial sandbox cache failure retained |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; 386 files |
| `uv run --locked mypy src tests` | Passed; 103 source files |
| `uv run --locked mypy src examples/feature-comparison` | Passed; 49 source files |
| `uv run --locked agentic-ml --version` | Passed; 0.1.0 |
| Local links/fragments and `git diff --check` | Passed; including new/untracked files |

The M1–6 run reported 1,027 selected items and completed all of them. xdist did
not emit a pre-filter collection/deselection count; those counts are unavailable,
not inferred from historical inventories. M0/M50/M99/infrastructure-only cases
remain excluded by the unchanged default expression. Seven native warnings were
visible: SQLAlchemy noload deprecation and the existing intentional infinite-target
NumPy assessment case. No warning or test suppression was added.

## Final artifacts and installed evidence

Final M1–6 comparison driver records:
`20261116T000223Z-762aa237d9b5-12f73ee427fb46d6939abd8a9879a475`.
Its actual distribution/rebuild child is
`20261116T000223Z-762aa237d9b5-57b0061fbb42483e864283a24d4d5b06`.
Both are under `.dev-records/verification/` in this checkout. Earlier focused
identities remain historical; final M1–6 identities are:

| Artifact | SHA-256 |
|---|---|
| Direct wheel | `f510508b8487616d982252b8c0e3c574e1ed0c0f369860836ea438b5ac3e229e` |
| Source distribution | `36d16692212d42b2cfaebcaf10aac229ead17b90166ed7c7c3b15cefbd891527` |
| Wheel actually rebuilt from extracted sdist | `f510508b8487616d982252b8c0e3c574e1ed0c0f369860836ea438b5ac3e229e` |

Equal wheel hashes are accompanied by distinct artifact paths, the logged native
rebuild command, separate installed project prefixes and initializer-verified
normal wheel origins. No direct-wheel substitution is inferred or permitted.
The exact copied recipe hashes match the repository source on both paths.

Both final projects used Python 3.12.16, toolkit 0.1.0, MLflow 3.18.0, DVC 3.67.1,
pandas 3.1.1, NumPy 2.5.5, sklearn 1.9.1, PyArrow 25.0.1 and skops 0.16.0.
The contributor environment uses its committed lock; its SHA-256 before/after is
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
Linux aarch64 only; no new macOS/Windows claim. Fresh runtime resolution is not
substituted for recorded project locks and library identities.

The session record directory is
`.dev-records/verification/20261115T233328Z-762aa23-us14-ip3/`.
It retains full combined tool output separately from direct test execution,
shared-check output, issue snapshots, executable hashes, final installed manifests
and command/outcome summaries. Nested driver records retain their complete native
stdout/stderr, model/feature/provenance observations and child resource/inventory
checks. The reused comparison test fixture appends unique native invocation logs
to its existing IP2 record location; no historical record was overwritten or removed.
Successful owned environments were cleaned by the established driver/pytest policy.

## Acceptance-criterion reconciliation

| Criterion | Independent final evidence |
|---|---|
| US-14-AC-01 | Authored native factory steps, parameters/columns, training-only scaler/imputer/category oracles and declared schema on both normal installs; complete recipe regressions also cover pandas positional labels |
| US-14-AC-02 | Real feature files, unmodified fit/preprocessing records, native model reload/predictions, effective dependencies and source identities on both paths |
| US-14-AC-03 | Identical split/classifier/settings; exact accuracy [0.5,1,0.5,0] and loss [0.5,0,0.5,1], gains/ties/regressions and reference-finalization ordering |
| US-14-AC-04 | Actual file hashes, committed code/config/lock and native DVC links/status; missing input, invalid provenance and native artifact failure on each path; full recipe failure/boundary regressions passed |
| US-14-AC-05 | Exact copied no-argument project factory; explicit numeric and mixed alternatives, validated name selection and fresh declarations |

IP3-T1–T3 are Complete. No in-scope US-14 requirement is deferred. The existing
US-03 damaged-resource skip stays with historical M1-ACCEPT-VERIFY; M50 exclusions,
MVP-M1-ACCEPT-VERIFY and MVP-M2-ACCEPT-VERIFY obligations remain unchanged.
Native stage execution/cache reuse, final-test evaluation, M2 restoration and
scientist/external-assistant integration retain their existing story owners.

No public contract or toolkit runtime implementation changed in IP3. No failing
assertion, threshold, timeout or skip was weakened. There were no failed runtime
corrective attempts beyond the expected missing-verifier red; the single typing
issue was corrected and verified. Explicit whole-story acceptance is requested;
no acceptance, commit, push, PR, merge or cleanup authorization is manufactured.

Developer “I approve phase 3”, 2026-11-16 UTC, explicitly approved the completed
Phase 3 results. This is distinct from the earlier execution authorization.
Whole-story acceptance and commit/publication remain pending. These approval
record edits change no executable input and do not invalidate test evidence.

## Whole-story acceptance

Developer “I accept the user story; commit the changes”, 2026-11-16 UTC, accepts
US-14-AC-01–05 with the verification and existing skip qualification above.
This authorizes local commit, ordinary push, PR creation and a static COMMENT
review under execute-plan. Merge, cleanup and other stories are not authorized.
Acceptance edits change no executable input; prior passing evidence remains valid.
