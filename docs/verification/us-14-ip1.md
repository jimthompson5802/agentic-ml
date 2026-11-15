# US-14 Implementation Phase 1 evidence

Technical status: contract review deliverable complete; developer contract
approval pending. Execution was authorized by “start phase 1”, 2026-11-15 UTC,
for IP1 only. [Plan](../plans/milestone-1-us-14.md),
[contract proposal v1](../feature-pipelines.md).

## Authority and prerequisites

Verified the registered story checkout `.worktrees/US-14-feature-pipelines`,
branch `US-14-feature-pipelines`, HEAD
`74cb1ca6884218471370dd68bf7c228f20448c40`, original base
`9a030cfe5d6523531e386b0195f40a16599180fc` and shared Git directory in the
primary checkout. No integration or fetch was performed. The working tree was
clean before recording execution authorization.

Retrieved issue #20's full body, every comment page and final metadata with
`sh .codex/scripts/github-read.sh`. One unique comment, ID 6699589877, matches
the reported count. Initial/final `updated_at` is 2026-11-15T20:05:03Z.
GitHub milestone is null; the body assigns US-14-AC-01–05 to M1. The issue's
policy wording already agrees with current focused verification and contract
approval policy. No GitHub write or acceptance change was needed.

Reviewed the active design reading map, data/features, interfaces, execution,
milestone delivery, traceability and ADR-008. The old “current milestone at phase
gates” sentence in milestone-delivery is superseded by the newer repository
verification policy and synchronized issue. It adds no phase test obligation.
Broad implementation-status prose also predates the supplying accepted stories;
specific contracts, code and final evidence establish availability.

Supplier plans retain acceptance for splits (#19), M1 DVC (#16), preprocessing
(#21), M1 classification (#28) and recording (#17). Their final reports and
actual public implementation are present in this consuming branch. Inspected
`fit_classifier`, `fit_preprocessing`, both tracking helpers and provenance
validation, including native defaults, source identity, artifact conflicts and
RUNNING-only finalization. Recorded source/report SHA-256 identities locally.
No supplier scope, package signature, resource or implementation was changed.

## Environment and commands

The inherited VIRTUAL_ENV pointed to the primary checkout. Cleared it for
`env -u VIRTUAL_ENV uv sync --locked --group dev`; UV_PROJECT_ENVIRONMENT was
unset. The resulting editable install and `.venv` belong to this story only.
Initial sandboxed setup could not write the uv cache; runtime escalation then
completed installation. Initial GitHub reads hit sandbox network denial; the
same reads succeeded with escalation. These were operational setup failures,
without corrective product changes or product-fix attempts.

Python 3.12.16, Linux aarch64, glibc 2.36. Locked versions: sklearn 1.9.1,
NumPy 2.5.4, pandas 3.1.0, PyArrow 25.0.1, MLflow 3.17.2, DVC 3.67.1,
skops 0.16.0 and toolkit 0.1.0. Lock SHA-256 before/after:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Raw records:
`.dev-records/verification/20261115T201435Z-74cb1ca-us14-ip1/`.
`commands.json` retains commands/cwd/exit codes; `logs/` contains complete
stdout/stderr from the successful native probe, renewed locked synchronization
and consistent issue retrieval. `identities/` retains the probe source, lock
digests and supplier/source digests. Initial runtime failures are retained in supplemental logs. The renewed
setup log records the successful synchronized state; original installation
progress remains in the session tool output. Native temporary MLflow storage was
disposable; printed run IDs identify feasibility runs, not retained product runs.

## Bounded feasibility results

Ran this worktree's `.venv/bin/python` against the retained `native_probe.py`.
Exit 0. Native sklearn only fits four depth-1 tree pipelines on the plan's fixed
training matrix. Independently fixed expected labels and metrics were asserted:

| Variant | Validation predictions | Accuracy | Zero-one loss | Adjusted delta, both directions |
|---|---|---|---|---|
| reference | [0, 0] | 0.5 | 0.5 | 0 |
| signal | [0, 1] | 1 | 0 | +0.5 |
| unchanged | [0, 0] | 0.5 | 0.5 | 0 |
| misleading | [1, 0] | 0 | 1 | -0.5 |

Signal/misleading scaling has training mean 0 and variance 2.5, with training
values `[-2,-1,1,2]/sqrt(2.5)` and validation values `[-3,3]/sqrt(2.5)`
(reversed for misleading). Compared numerical values at rtol/atol 1e-12.

Additional native mixed feasibility used numeric `[1, null, 3, 5]` and category
`[a,b,a,b]`: mean imputation 3, scaled numeric `[-sqrt(2),0,0,sqrt(2)]`,
category columns `[a,b]`. Held-out numeric 7/unseen category becomes
`[2*sqrt(2),0,0]`; output is dense float64. This supplements the accepted US-15
literal imputation/encoding boundaries without changing their required tests.

Native MLflow SQLite/artifact probe confirmed: reference stays RUNNING, candidate
finishes, summary uploads to `outputs/comparison/comparison.json`, reference
finishes. No run was reopened. Static inspection confirms `log_preprocessing`
leaves RUNNING and `log_run_results` uploads outputs before finalizing once.
That permits deferred reference finalization without changing toolkit APIs.

These probes establish numerical and lifecycle feasibility only. They do not
execute a comparison recipe, verify installed toolkit behavior, test source/DVC
integrity, persist a complete fitted-model handoff or satisfy any AC acceptance.
No dependent production code or new behavior tests were written. No suppressions,
skips, thresholds or assertions changed. There were no failed product corrections.

## Review and verification boundaries

US-14-IP1-T3 produces contract proposal v1: exact flags/settings, file inventory,
strict preparation, variant ordering/budget, metric/direction and zero-tie rules,
original split/source identity, feature/DVC outputs, JSON/table schema, reference
run ordering and partial-failure behavior. It reuses accepted public interfaces;
no wrapper or new package schema is proposed. The new comparison schema belongs
to the copied experiment recipe.

AC-01/02: native declarations, train-only public fit boundary, unchanged records,
actual transformed Parquet outputs and dependencies. AC-03: fixed protocol and
independent literal gain/tie/regression matrix for both directions. AC-04: native
DVC outputs/pointers, original source lineage and inspected MLflow artifacts.
AC-05: explicitly authored names/objects only. All await implementation evidence.

IP2 owns copied-entrypoint behavior tests and public fit/tracking regressions.
IP3 owns direct/rebuilt-wheel runtime-only projects, representative negatives,
M1–6 and final shared checks. No reduction to either phase's verification.
No fresh notebook, macOS/Windows, M2 restoration, final-test scoring, scheduler
or assistant integration claim is made.

Documentation validation checks local Markdown targets/fragments and whitespace,
including newly added files. No executable product behavior changed; TDD red,
pytest, Ruff/mypy and toolkit smoke runs are inapplicable to this contract-only
phase, as specified in the approved plan. Native commands are feasibility probes,
not passing toolkit regression evidence. Validation results are recorded in the
plan: all 77 local links/fragments resolve; whitespace checks pass for all four
changed files and `git diff --check` exits 0. The first link-check attempt
incorrectly required file targets for an existing historical directory link.
Corrected that checker defect, retained its first result and reran the original
link/fragment checks. Product tests and acceptance expectations were unchanged.

Next gate: explicit approval of contract proposal v1 and its public test boundaries.
IP2 additionally requires execution authorization; this phase request covered IP1.


## Factory contract refinement: US-14-SC-01

Developer approved predeclared categories and the four factory recommendations
on 2026-11-15. Contract v2 now specifies the fixed no-argument factory returning
plain dictionaries with fresh pipelines, positional project output labels,
global name checks and selected-only full validation, and project-local helpers
and optional types. Eager construction errors still propagate before selection.
This approves those decisions only, not the whole contract or Phase 2 execution.
IP2-T2 now owns explicit factory/selection/schema cases; prior verification
obligations and numerical feasibility evidence are retained. These document
changes introduce no executable behavior and need no manufactured TDD red.

Renewed validation: 77 local links/fragments resolve; all four documents pass
whitespace checks and `git diff --check` exits 0. Revision records are retained
under `.dev-records/verification/20261115T204056Z-74cb1ca-us14-factory-contract/`; original IP1 records are unchanged.

Developer “i approve the plan; commit”, 2026-11-15 UTC, approved the revised
implementation plan and authorized committing its four IP1 documents. Factory
decisions retain their specific approval; remaining contract/public-boundary
approval and IP2 execution remain pending. No additional product checks are
needed for this approval-record-only update.
