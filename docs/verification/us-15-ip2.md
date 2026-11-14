# US-15 Phase 2: training-only native fitting

2026-11-14 UTC; issue #21, M1 AC-01/02 and preliminary AC-03 metadata.
Branch US-15-preprocessing, Phase 1 commit 576bd9f; approved Phase 2 changes
are committed in this branch. Git history identifies the resulting commit.
Developer in coordination session approved both story Gate 1 decisions and
authorized local Phase 1 commits plus Phase 2 execution:
“i approve Gate 1 in both us-15 and us-26. commit the changes and start phase 2 in both stories”.
This approves the reviewed public test boundary, not Gate 2 or story acceptance.

## Scope and public evidence

Implemented agentic_ml.preprocessing.fit_preprocessing. It reconstructs supplied
memberships through existing create_partitions, compares current source identity,
clones the native Pipeline and fits only selected training columns. It validates
features, fit scope, basic record/schema/settings and training output width/dtype;
native errors retain their type and receive a preprocessing-stage note.
The return is a native fitted Pipeline and plain metadata, retaining a deep copy
of the original seeded or supplied partition record. No MLflow/Git/DVC discovery
or persistence is introduced.

Tests use the Gate 1-confirmed public helper/native transform boundary, literal
numeric/category outputs, observable errors and caller-input preservation. They
do not mock internal collaborators or inspect private toolkit helpers. The
test matrix verifies:

- Literal scaler training [-1,1], validation [98,198], test [998,1998] and
  inference 5 -> 3, with abs/rel 1e-12; original pipeline/frame/record/cwd intact.
- Rejection of validation fit scope, changed source values under valid IDs,
  duplicate/missing/empty/ID/target feature selections, invalid version and
  non-Pipeline input.
- Public helper reuse of overlap/duplicate/unknown/uncovered/empty membership
  and layout-key rejection, with source frames preserved.
- Two-way string IDs and reordered/nondefault index, train imputation statistic
  2 with held-out 100 unchanged, nested native imputer/scaler/encoder with unseen
  category zero encoding and literal combined outputs.
- Declared schema width/dtype/shape/name errors, contextual native fitting error,
  and original seeded settings retained without aliasing returned metadata.

Existing splitting regressions protect membership/source identity/both layouts.
Cases that already passed through reused native/public capabilities were recorded
as regression evidence; no artificial defect was introduced to manufacture red.

## Red / green evidence

Raw records: `.dev-records/verification/20261114-us15-ip2/`. Exact commands,
failures and passing results are preserved in numbered logs. Short serial
selectors were used for immediate TDD feedback under the verification policy's
focused-cycle exception; the final regression used four loadgroup workers.

| Logs | Selector / new behavior | Red | Green and relevant regression |
|---|---|---|---|
| 01 / 02 | scaler_fits | Required preprocessing module absent | 125 passed: first preprocessing case + existing splitting |
| 03 / 04 | validation_fit_scope | Did not raise | 2 preprocessing passed |
| 05 / 06 | changed_source | Did not raise | 3 passed |
| 07 / 08 | duplicate_features | Native error lacked selected_columns field context | 4 passed |
| 09 | Existing capability coverage | Already implemented by reuse | 15 passed: memberships/features/string-ID layout coverage |
| 10 / 11 | output_width | Did not raise | 16 passed |
| 12 / 13 | non_pipeline | Did not raise | 17 passed |
| 14 / 15 | imputation_uses | Strict JSON rejected unencoded NaN | 18 passed |
| 16 / 17 | native_composition | Strict JSON rejected numpy dtype class | 19 passed |
| 18 / 19 | unrecordable | Native parameter failure lacked metadata field context | 20 passed |
| 20 / 21 | incompatible_partition | Did not raise | 21 passed |

Red commands were `uv run --locked pytest tests/integration/test_preprocessing.py
-k <selector>` (see logs for exact selectors). Green commands ran the entire
current preprocessing module, with splitting included in log 02. Later regression
coverage brought the preprocessing module to 27 cases.

Final command, exit 0:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py
```

151 selected cases passed in 3.96s (27 preprocessing + 124 splitting), no skips
or deselections in these paths. No M1–6/full suite or artifact driver was run;
those remain US-15-IP4-T2/US-26-IP4 and named milestone obligations.

## Shared checks and identities

All required commands passed:

```sh
uv sync --locked --group dev
uv lock --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src tests
uv run --locked agentic-ml --version
git diff --check
sha256sum uv.lock
```

Sync checked 193 installed packages; lock check resolved 196; CLI printed 0.1.0;
mypy checked 79 source files; formatting checked 325 files. Before/after lock
SHA-256: 6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4.
Own worktree environment: Linux aarch64 / Python 3.12.16, sklearn 1.9.1,
pandas 3.1.0, pyarrow 25.0.1. No dependencies/lock changed or new platform claim.

Initial lint found import order/unused import, fixed by scoped Ruff formatting.
Initial strict typing found five test-helper dictionary/record-narrowing errors;
explicit test option typing and an exact membership assertion fixed them.
The first full lint also found four stub import orders and two native uppercase
parameter names. Stubs now expose positional fit/transform inputs with lowercase
local names; no suppression was added. Renewed full lint/format/mypy passed.
No behavior correction exceeded one verified corrective attempt; failures and
original assertions were retained. No skip, suppression or threshold change.

Contributor-only sklearn stubs describe public constructors/settings/clone and
Pipeline fit/transform used here because sklearn ships no typing marker. Native
output containers vary, so third-party return types use Any; toolkit inputs and
return structures remain explicit. See [typing rationale](../../typings/README.md).
No runtime behavior or distribution content is changed by these stubs.

Before implementation the complete #21 body and two unique comments were
refreshed; final metadata updated_at/count remained stable. Raw snapshots remain
in issues.json. Existing scope/CONTRACT-01/SC-01 and M2 AC-04 remain unchanged.

## Gate 2 limits

IP2-T1/T2/T3/T4 are technically Complete. Gate 2 is Approved on 2026-11-14
by coordination-session developer: “for both us-15 and us-26 i approve the phase 2 gate, commit the changes.”
This records both US-15 and paired US-26 Gate 2 approvals and authorizes the
local Phase 2 commit only. IP3 execution, push/publication, integration and
cleanup remain unauthorized. Existing verification evidence remains valid;
only approval/handoff documentation changed after the passing phase checks.
Full metadata/default/error coverage remains IP3: numpy array/scalar/dtype-object
encoding, malformed nested record fields, exhaustive tag/context/rejection matrix,
and broader output-container coverage are not claimed complete by this phase.
The implemented encoding covers the tested default M1 matrix, not all proposed
future metadata cases. Installed direct/rebuilt wheel verification remains IP3;
actual consumer handoff remains US-26 IP4/US-15 IP4. AC-03 persistence and AC-04
restored transforms are unverified. Historical M1/M50/MVP verification owners
remain open.

Final document verification passed for 73 local paths/anchors across five changed
Markdown files, whitespace/final newlines and git diff --check. Input/log checksums,
phase test counts and lock identity are recorded in summary.json and
document-validation.json under the retained phase records directory.
