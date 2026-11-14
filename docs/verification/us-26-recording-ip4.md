# US-26 Phase 4: actual installed producer handoff

Technical status: IP4-T1/T2/T3 Complete. **Gate 4 Approved**.
[Owning plan](../plans/milestone-1-us-26-recording.md),
[execution order](../plans/milestone-1-us-15-us-26-execution-order.md),
[tracking guide](../experiment-tracking.md),
[supplier evidence](us-15-ip3.md).
Issue #17 owns recording AC-01–05. This phase supplies US-15 AC-03 preservation
evidence; it does not accept US-15 or US-26's separately owned #33/#43 criteria.

## Authority and integrated inputs

Developer authorized Phase 4 coordination and the required committed US-15 source
integration through thread 01a1db6c-a225-73e0-8796-81a03c4cec7a on 2026-11-14.
US-26 baseline c2e3dec87a5782f4bdd7c61a81356feefdcb7030 and approved US-15
supplier e63ef4b8ff700d44e5c644dd30eed92ebd62104b have both Gate 3 approvals.
An ordinary `git merge --no-commit --no-ff` integrates the supplier into this
consumer checkout. The developer subsequently approved Gate 4 and authorized a local combined
merge commit and handoff, as recorded below. No push, PR, publication or sibling
mutation. US-15 retains its own verification, Gate 4 and acceptance. Separate
#17 acceptance is not inferred.

Both issue bodies and every comment page were refreshed. Two unique comments
each match reported counts, with stable metadata: #17 updated_at
2026-11-14T18:07:56Z, #21 2026-11-14T18:07:50Z. Scope and SC-01 remain unchanged.
The existing public boundaries were confirmed at Gate 1: installed
fit_preprocessing, both tracking helpers, native client inspection and independent
literal checks. Integration verification adds no new toolkit behavior; existing
production implementations remain byte-identical to their approved revisions.
There is no manufactured product failure for already implemented behavior.

Expected merge conflicts were limited to CHECKPOINTS.md and contributor typing.
The consumer checkpoint remains specific to this story. Supplier plan/evidence
are preserved. sklearn declarations combine supplier constructors/clone/fit/
transform/set_output and consumer feature-name/check_is_fitted inspection;
get_params retains dict[str, object]. No suppression or runtime dependency change.
Shared links now resolve within the combined checkout. The imported historical
contract patch had whitespace in blank context lines: original bytes remain in
raw records; normalization removes optional context spaces and adds a footer.
`git apply --numstat` still parses exactly the same three-file change counts.

## Installed checks and observations

`test_preprocessing_tracking.py` builds one combined-source wheel/sdist pair.
`verify_tracking.py` invokes the existing distribution verifier as a child, keeps
its two normal environments until both dependent checks finish, and uses the
actual rebuilt wheel produced from extracted sdist. It creates two independent
normal installed experiment projects with runtime dependencies, retained wheel,
lock, Git and native DVC/MLflow storage. Isolated Python runs from unrelated cwd.
The unchanged child verifier checks CLI, public resources, runtime inventory,
normal origin and both artifact identities. Project imports resolve to their own
site-packages; contributor tools are absent. Native initialization independently
validates each wheel archive, installed payload and lock identity.

The exact documented `tracking_project.py` script is committed as experiment
`track.py`. Its native imputer/scaler/encoder pipeline goes through actual
fit_preprocessing and directly into log_preprocessing without an intermediate
serialization file, copied producer implementation or neighboring imports.
Before logging, literal training/held-out output is
`[[-1,1,0],[0,0,1],[1,1,0],[98,0,0],[198,1,0]]`; inference is `[[3,0,1]]`.
The caller's unfitted pipeline remains unfitted. Strict JSON passes for every
effective setting. The consumer accepts and preserves the exact returned record,
including partition/source, schemas, versions and SC-01 NaN/dtype tags.

Native inspection verifies stable existing run ID, artifact URIs, parameters,
metric 0.75 and FINISHED process status with separate failed validation status.
Downloaded features have independently specified exact CSV bytes. Metadata and
shared provenance equal the original producer/supplied dictionaries. Git blobs
match source/notebook/config/lock/DVC metadata; native `dvc status --json` is empty.
Downloaded model loads through native MLflow sklearn: fitted imputation and
centering retain 2 and category vocabulary is exactly a/b. This is artifact
readability/fitted-state preservation, not M2 restored numerical replay.

Each wheel also checks:

- A fresh kernel uses that project's Python. Successful notebook stream bytes
  and failed notebook error cells are retained exactly; source is committed.
- Notebook execution failure yields RuntimeError and native FAILED while keeping
  available outputs, preprocessing, notebook and provenance inspectable.
- Missing required predictions despite process exit zero yields
  FileNotFoundError and FAILED, retaining available preprocessing/features.
- Dirty committed configuration yields ValueError naming config.json, FAILED,
  and no published artifacts in that run.

Final focused parent records:
`.dev-records/verification/20261114T220529Z-c2e3dec87a57-b2bccd7171d04ddca62e599e8f981f61/`.
Its child distribution records:
`.dev-records/verification/20261114T220529Z-c2e3dec87a57-13eec2b0dd544d0696d43453440648e5/`.
Both verification outcomes are zero; parent cleanup is complete. Direct and
genuinely rebuilt wheel SHA-256 are both
`1f58386b834274d272a6e030e3bc59ed16f3f71ce0161c0d9e165ab94edfd84a`;
source distribution SHA-256 is
`f1a006380170101c4de66d046ef36fb6e4ae749a899686a8b853fbfb3380ac94`.
Equal hashes do not substitute for the separately executed rebuild. Both exact
parsed records also have canonical JSON SHA-256
`e46f1bd02aab5ce9949f02cfe11b1a43bcd371b053dbe990a58e2bed627b9c70`. Driver records preserve metadata, provenance, split, native commands,
feature bytes, both notebooks and the native pipeline files before successful
workspace cleanup. Existing IP2/IP3 tests retain full-SHA Git identity, two-store/
cwd, invalid metadata/DVC/environment, conflicts, serialization/storage failure
and diagnostics coverage. Their unchanged assertions run again in final selection.

## Failures and corrective evidence

Raw lifetime evidence: `.dev-records/verification/us26-ip4-20261114/`, plus driver
records linked below. Preserve earlier phases and the original default-skops
failure. No assertion, timeout, skip or native trust bound was weakened.

- Initial merge reported unreadable tree 4762191c53d0646eded4205fd9f8089c5e1d291e.
  Read-only inspection found the tree readable and checkout clean; the identical
  ordinary retry reached expected conflicts. No object/ref/configuration repair.
- Initial test collection used a nonpackage `tests` import; a module-owned fixture
  corrects it. Log 02 then fails as intended because the new driver is missing.
  Serial runs are short integration-harness feedback, not final gate evidence.
- Log 03 catches the new checker treating canonical file: wheel URI as a path.
  Corrective attempt 1 parses and decodes its URI. Log 06 passes both paths.
- Log 04 catches exact-script mismatch caused by formatting during the invocation.
  Inputs were synchronized before log 06, which passes. Final runs freeze inputs.
- Initial typing catches untyped notebook constructors; native notebook execution
  follows the existing subprocess fixture boundary. A remaining argparse-derived
  Any root is corrected with Path construction. Log 08 passes 91 files.
- Sandbox uv-cache denials are retained and identical commands rerun with required
  escalation. They are environment failures, not successful product checks.

## Final verification and approval boundary

Final focused command:
`uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing_tracking.py tests/integration/test_tracking.py tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_data_assessment.py --junitxml=.dev-records/verification/us26-ip4-20261114/focused.xml`.
Result: **361 passed**, zero failed/skipped/deselected, 346.90 seconds,
four workers/loadgroup. This includes 117 tracking, 84 preprocessing, 124 split,
35 assessment cases and the one actual producer matrix covering both wheels.
Five retained warnings are four known NumPy arithmetic warnings in the explicit
infinite-target assessment fixture and native SQLAlchemy noload deprecation.

M1–6 acceptance command:
`uv run --locked pytest -n 4 --dist=loadgroup --junitxml=.dev-records/verification/us26-ip4-20261114/m1-m6.xml`.
Result: **924 passed, 1 skipped**, zero failures/errors, 419.05 seconds,
four workers/loadgroup. All 925 selected cases completed. Read-only default
collection inventory counts 1193 total and 268 deselected. Serial collection
only records inventory and executes no cases. The one skip is the existing
`test_missing_planning_schema_fails_installed_inventory` timeout deferral.
The two other existing authorized skips are outside this M1–6 selection; no
skipped coverage is claimed as passing. Five known warnings match the focused run.
All final executable inputs retain their pre-run fingerprints. No broader test
selection was run.

Shared checks pass: locked sync (196 resolved/193 checked), lock consistency,
lint, formatting (348 files), strict typing (91 files), CLI 0.1.0 and whitespace.
Local document check passes 165 links/anchors. Final input hashes, full working
tree patch, source-preservation comparisons, counts and document results reside
in `manifest.json` under the raw Phase 4 directory. Both approved production
implementations and supplier tests/probes remain unchanged. A retained wheel
with the final digest matches all 72 package members against combined source.
Eight failed native staging trees from the repeated component checks are copied
with checksum verification under `failure-artifacts/`; original trees remain.
Existing component support still writes native commands/invocations into its
historical IP2/IP3 raw directories; `inherited-fixture-records.json` indexes the
394 new records, without relabeling or overwriting historical evidence. Own environment is Linux aarch64,
Python 3.12.16, uv 0.13.6, UV_LINK_MODE=copy, no VIRTUAL_ENV or
UV_PROJECT_ENVIRONMENT override. Development MLflow is 3.17.2/pandas 3.1.0;
both independently resolved runtime projects use MLflow 3.18.0/pandas 3.1.1,
DVC 3.67.1, sklearn 1.9.1, pyarrow 25.0.1 and toolkit 0.1.0. These observations
verify the named environments, not other library/platform combinations.
Lock SHA-256 is unchanged:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
The M1–6 run renews the actual matrix again. Its final parent is
`.dev-records/verification/20261114T221634Z-c2e3dec87a57-50159991119e44d2a67a2f9f5071a439/`,
child `20261114T221634Z-c2e3dec87a57-18c9b4e2a6384cfdb6378b56980a0c29/`.
Both outcomes pass and parent cleanup is complete. Both wheel digests remain
`1f58386b834274d272a6e030e3bc59ed16f3f71ce0161c0d9e165ab94edfd84a`;
its source archive digest is
`1c5e6d776ef7ecb4a0f544e4600f60f8812320bf14f457c49a82564cd10f0e6b`.
The source archive changes with documentation snapshots; installed package
payload and all tested executable inputs are identical. Final gate record edits
are documentation only. `final-matrix.json` retains exact native run references,
identities, original/downloaded metadata and both failure/success outcomes.
No unresolved product defect or Phase 4 blocker remains.

| Criterion | Final evidence | Technical result |
|---|---|---|
| US-26-AC-01 | Native same-run parameters/metrics/status and exact outputs/artifact URIs; both installed wheel paths | Verified; acceptance Pending |
| US-26-AC-02 | Real DVC directory/member identity, saved split, committed experiment and effective settings; dirty/missing/corrupt reference regressions | Verified; acceptance Pending |
| US-26-AC-03 | Normal wheel archive/payload/lock identity, full-SHA Git regression, installed versions, explicit unavailable source/build fields | Verified; acceptance Pending |
| US-26-AC-04 | Exact committed source/configuration/lock/notebook references; fresh-kernel output/error notebook preservation | Verified; acceptance Pending |
| US-26-AC-05 | Missing outputs despite exit zero, nonzero notebook execution, invalid references and native serialization/storage regressions | Verified; acceptance Pending |
| US-15-AC-03 preservation | Actual producer's fitted native composition, exact complete metadata/schema and shared committed/dependency links retained | Supplied for independent US-15 review; acceptance Pending |

Gate 4 is Approved. The
[execute-plan skill](../../.agents/skills/execute-plan/SKILL.md) requires:
“At the end of every implementation phase, including the final one, save progress
and stop.” The explicit decision below satisfies Gate 4. Separate acceptance of #17's
AC-01–05 slice remains pending. No whole US-26 acceptance,
US-15 acceptance, milestone acceptance or publication is claimed.

M2 US-15 AC-04 transformation restoration, #33/#43 reporting/lookup, actual
classification/assistant workflows and broader platforms remain separately owned.
Historical M1/M50 verification obligations and all three temporary skips remain.
No complete-suite or standalone artifact driver was launched; selected pytest
invokes artifact verification as allowed by policy.

## Gate 4 approval and combined local commit — 2026-11-14

Developer: “I approve us-26 gate 4 and authorize committing the combined revision so us-15 can complete”.
Relayed by coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a.
This approves US-26 Gate 4 and authorizes the local combined merge commit and
US-15 handoff. It does not accept whole-story publication, close issue #17,
approve US-15 Gate 4, or authorize push, PR, publication, main merge or cleanup.
The existing planning-schema skip remains recorded and is not passing coverage.
All reviewed executable inputs match the passing Phase 4 fingerprints; only
approval/checkpoint documentation changes follow verification. TDD and test
renewal do not apply to these documentation-only records. Approval checks and
commit/parent verification are retained under
.dev-records/verification/us26-ip4-approval-20261114/.
Git HEAD identifies the resulting combined commit, with both reviewed parents
c2e3dec87a5782f4bdd7c61a81356feefdcb7030 and
e63ef4b8ff700d44e5c644dd30eed92ebd62104b preserved.
