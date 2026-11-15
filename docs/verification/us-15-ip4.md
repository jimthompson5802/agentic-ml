# US-15 Phase 4: preservation review and final M1 verification

Technical status: **US-15-IP4-T1/T2 Complete; Gate 4 Approved; M1 slice Accepted**.
[Owning plan](../plans/milestone-1-us-15.md),
[consumer evidence](us-26-recording-ip4.md),
[execution order](../plans/milestone-1-us-15-us-26-execution-order.md).
Evidence completed 2026-11-15 UTC; executable run started 2026-11-14.
The developer accepted the M1 AC-01/02/03 slice on 2026-11-15. AC-04 stays M2 and #21 stays open.

## Authorization, integration and identities

Developer first authorized Phase 4 coordination with US-26 executing first.
After its handoff the developer explicitly directed: “I approve us-26 gate 4
and authorize committing the combined revision so us-15 can complete”.
Coordination thread `01a1db6c-a225-73e0-8796-81a03c4cec7a` explicitly authorized
US-15 to integrate the committed reviewed revision and complete dependent checks.
The committed consumer plan/report record Gate 4 Approved; US-15 Gate 4 is
independent and subsequently approved by the explicit decision below. No
publication or whole-story acceptance follows.

US-15 branch `US-15-preprocessing` was fast-forwarded to combined commit
`3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1`, subject
`feat(tracking): verify installed preprocessing handoff`. Its two parents are
consumer `c2e3dec87a5782f4bdd7c61a81356feefdcb7030` and approved producer
`e63ef4b8ff700d44e5c644dd30eed92ebd62104b`. No conflict or sibling mutation
occurred. All 83 consumer-tested executable input fingerprints match this
checkout before and after verification. Producer source/tests/probes remain
unchanged. No executable behavior was added or corrected, so new TDD is not
applicable; approved earlier red/green and component evidence remain valid.

Independent preparation documents were preserved byte-for-byte with a manifest
and tracked patch under `.dev-records/verification/20261114-us15-ip4/preintegration/`
before restoring the two tracked preparation documents for integration. The
untracked preparation report survived integration and is superseded by this
report; its original bytes remain in that snapshot. CHECKPOINTS.md is restored
to US-15 ownership while preserving historical obligations.

Issue #21's full body and all comment pages were refreshed: two unique comments
match reported count 2; final metadata remains `2026-11-14T18:07:50Z`. Snapshot
`issues.json` retains complete content. An initially truncated final metadata
command was repeated with complete output before checking consistency. Scope and
US-15-US-26-CONTRACT-01/SC-01 are unchanged. No issue criteria were edited.

## Independent preservation review

Reviewed the actual installed matrix, project script, native inspection checker,
consumer report and raw final artifacts. Supplier manifest SHA-256 is
`acc5a37bc58c490af78d8bca7d7299bd9b58c4bcfba723fa41121ee471221998`.
Verified all 28 retained identity/artifact checksums and copied the raw parent
record into US-15's durable `supplier-review/` directory. Supplier parent:
`20261114T221634Z-c2e3dec87a57-50159991119e44d2a67a2f9f5071a439`.
The own final M1–6 run independently renews the same actual producer matrix.

Each normal noneditable installed project invokes actual `fit_preprocessing`,
passes its native fitted object and complete returned dictionary directly to
`log_preprocessing`, then records results in the same explicitly selected run.
No copied producer implementation, source-path import or intermediate joblib
handoff is used. Native MLflow inspection independently checks persisted JSON,
run/artifact identifiers and fitted pipeline; Git blob and native DVC checks
verify supplied committed references. Both direct and genuinely sdist-rebuilt
wheel paths run from unrelated cwd with isolated project/environment/storage.

Before logging, literal expected outputs are training
`[[-1,1,0],[0,0,1],[1,1,0]]`, validation `[[98,0,0]]`, test `[[198,1,0]]` and
inference `[[3,0,1]]`; the caller pipeline remains unfitted. Downloaded feature
CSV bytes match that oracle. Original/downloaded metadata, supplied/persisted
provenance and saved split are exactly equal. All eight top-level metadata
fields, feature order/schemas, full effective defaults, memberships/source,
versions and SC-01 tags are retained. References include full experiment commit,
entrypoint/notebook/config, effective settings, native DVC dataset/split,
lock checksum and verified wheel installation identity. Unavailable toolkit
repository/build fields remain explicitly null for this wheel installation.

Native MLflow loads the preserved pipeline: imputer statistic and scaler mean
remain 2; encoder vocabulary remains a/b. MLmodel records skops serialization
with only `numpy.dtype` trusted. This proves readability and fitted-state
preservation; M2 restored numerical transformation/reproduction is unperformed.
Fresh-kernel notebook outputs/errors are retained exactly. Process failure,
zero-exit missing output and dirty-config failures remain visible as FAILED with
available diagnostics; configured poor validation remains distinct from process
success. Consumer component regressions retain invalid metadata/reference,
serialization/storage/conflict coverage and public boundaries.

## Final checks and retained records

Own command:
`uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/20261114-us15-ip4/m1-m6.xml`.
**924 passed, 1 skipped, zero failures/errors**, 427.02 seconds, four workers
with loadgroup. JUnit accounts for all 925 selected tests. Read-only serial
collection (no executed tests) reports 1193 total, 925 selected, 268 deselected.
The skip is existing developer-authorized
`test_missing_planning_schema_fails_installed_inventory`; no skipped coverage is
claimed as passing. The two other existing timeout skips lie outside this
selection. Five unchanged warnings are four NumPy warnings for explicit
infinite-target assessment and one native SQLAlchemy noload deprecation.
No assertion, timeout, skip, suppression or dependency was changed.

Shared checks pass: `uv sync --locked --group dev` (196 resolved/193 checked),
`uv lock --check`, `uv run --locked ruff check .`,
`uv run --locked ruff format --check .` (350 files),
`uv run --locked mypy src tests` (91 files), and
`uv run --locked agentic-ml --version` (0.1.0).
Final documentation links and whitespace checks accompany the gate manifest.
Lock SHA-256 before/after remains
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.

Own actual matrix parent:
`.dev-records/verification/20261114T232528Z-3ffc7b4df557-39bfbfb93c29470b8bb8644b01822bcb/`;
child `20261114T232528Z-3ffc7b4df557-ecbcee4690ae46b4b7425d8aecffe007`.
Both verification outcomes pass and parent cleanup is complete. All 28 retained
own identity/artifact checksums pass. Native successful run IDs are
`73eac1fdb99547d2b68f50d7d2398bec` (direct) and
`870c9f6b58314cb6a5d79e6a62cd79f4` (rebuilt).
Both wheel SHA-256 values are
`1f58386b834274d272a6e030e3bc59ed16f3f71ce0161c0d9e165ab94edfd84a`;
source archive SHA-256 is
`54142f60d586c4351b16d01b9e21b5f5ff89b9f9db839f11fea44f3e13ab93aa`.
Equal wheel hashes do not substitute for the separately executed rebuild.
Documentation edits change source archive bytes while package payload remains
unchanged. Exact metadata, provenance, native commands, notebook/features and
pipeline bytes survive normal workspace cleanup in parent identities.

Own raw phase directory `.dev-records/verification/20261114-us15-ip4/` retains
preparation, integration, supplier review, command results, JUnit, own installed
review, collection counts and final manifest. It spans the UTC date boundary.
Environment: Linux aarch64, Python 3.12.16, uv 0.13.6, UV_LINK_MODE=copy; own
worktree environment with no VIRTUAL_ENV/UV_PROJECT_ENVIRONMENT override.
Development MLflow 3.17.2/pandas 3.1.0; both normal installed projects resolve
MLflow 3.18.0/pandas 3.1.1, DVC 3.67.1, sklearn 1.9.1, pyarrow 25.0.1,
toolkit 0.1.0. These are observations for named versions, not general claims.

## Criterion reconciliation and approval gate

| Criterion | Evidence | Technical result |
|---|---|---|
| US-15-AC-01 | IP2/IP3 literal train-only and native transform cases; final M1–6 renews all 84 producer cases and installed probes/matrix | Accepted M1 slice, 2026-11-15 |
| US-15-AC-02 | Public overlap/membership/scope/source/feature rejection and independent numeric fitting oracles; final partition/assessment regressions | Accepted M1 slice, 2026-11-15 |
| US-15-AC-03 | Complete metadata/default/schema checks plus actual installed native MLflow persistence, committed provenance and fitted-state inspection in both wheel paths | Accepted M1 slice, 2026-11-15 |
| US-15-AC-04 | Fresh-project restored transformation/reproduction | M2; unperformed and not accepted |

All unfinished IP2/IP3 M1 verification exclusions are reconciled by the final
selection, installed producer probes and actual consumer matrix. Infrastructure,
M0/M50/M99-only cases excluded by the default selector are not claimed verified;
existing skipped coverage retains its original owners. No full suite or
standalone artifact driver was launched. Historical M1-ACCEPT-VERIFY,
M50-ACCEPT-VERIFY and MVP-M1/M2-ACCEPT-VERIFY remain open in their owning records.
M2 restoration, broader classification/assistant integration and macOS/Windows
verification remain separately owned. Native SciPy float16 encoder limitation
and all earlier failed evidence remain visible in IP3; no fallback is added.

No unresolved Phase 4 blocker remains. US-15 Gate 4 is Approved and the M1
AC-01/02/03 slice Accepted by the 2026-11-15 developer decision: “Approve US-15 Gate 4 and accept its M1 slice; commit its remaining changes. Accept US-26’s #17 scope. Prepare and explain the PR structure before pushing or publishing.”
Source: coordination thread `01a1db6c-a225-73e0-8796-81a03c4cec7a`.
This authorizes local remaining-record commitment and a
[reviewable PR proposal](../reviews/us15-us26-pr-structure.md). The explicit
publication limit supersedes the execute-plan skill's default publication steps.
No push, PR/publication, main merge, issue closure, history rewrite, new PR
branch, cleanup or M2 execution is authorized. Earlier pending-gate manifest
remains historical evidence; a separate acceptance manifest verifies final
record changes and unchanged executable inputs. TDD/test renewal is unnecessary
for these documentation-only acceptance records.
