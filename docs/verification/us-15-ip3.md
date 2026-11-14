# US-15 Phase 3: metadata and installed producer evidence

Technical status: US-15-IP3-T1/T2/T3 Complete; **Gate 3 Approved**.
Owning [plan](../plans/milestone-1-us-15.md), [usage guide](../preprocessing.md),
[issue #21](https://github.com/jimthompson5802/agentic-ml/issues/21).
US-15-AC-01/02 have component evidence; AC-03 is advanced, with actual MLflow
preservation still owned by US-26 IP4. AC-04 remains M2. No story acceptance,
Phase 4, source integration, push or publication is claimed.

## Authority, boundaries and changes

On 2026-11-14 the coordination session relayed the developer's explicit direction
“have both US-15 and US-26 start Phase 3.” Gate 2 was already approved and
committed at `104172afe9c5445e9407ffb91d56b13defd098c0`. This work follows that
commit as Phase 3 changes in the owning `US-15-preprocessing` worktree.
The developer subsequently approved Gate 3 and a local commit with
“commit changes in both stories”, relayed on 2026-11-14 by the coordination
thread `01a1db6c-a225-73e0-8796-81a03c4cec7a` as explicit Gate 3 acceptance.
Issue #21's full body and both comments were refreshed; unique comment count 2
and stable final metadata match the prior scope. Null GitHub milestone; body
assigns AC-01–03 to M1 and AC-04 to M2. The newer repository phase verification
policy resolves the older generic issue wording as previously recorded.

Gate 1 confirmed the public seams: `fit_preprocessing`, native `transform`, strict
JSON output, and installed separate-project execution through both artifact
paths. Tests use literal numeric/category expectations and public errors; no
private encoder tests or mocked native fit sequences. The installed probe tests
the actual runnable guide script. Metadata cannot certify arbitrary Python or
replace numerical training-only verification.

- The producer recursively records NumPy arrays and finite scalar values, native
  dtype classes/descriptors, ordered native estimators and their defaults. SC-01's
  exact imputer-NaN/dtype tags, reserved-map rejection and ordinary finite JSON
  rules are unchanged. NumPy is already required by declared runtime dependencies
  including scikit-learn; no dependency declaration or lock change was needed.
- Input records must be finite plain JSON. Unknown methods, invalid supplied
  settings/protocols, invalid seeded keys/types/call history, source identity/type
  mismatches and tuple/native-scalar membership records are rejected. Seeded
  settings are checked through the existing native partition API, without
  replacing the consumed membership or original record. Training selection still
  uses validated supplied membership.
- Native sparse and pandas output schemas are checked without densifying in
  product code. Tests include mixed output dtypes, unchanged native all-null
  imputer dropping, and visible native failures. Caller input preservation and
  training-only oracles remain protected by earlier tests.
- `check_preprocessing.py` is copied into the external verification workspace.
  The existing assessment/splits driver runs it using isolated `-I` Python in
  each independently installed wheel environment, preserves metadata/identity
  records, and retains its existing runtime-inventory and cleanup checks.
- Contributor sklearn stubs add the exercised native `set_output` API and NumPy
  integer `max_categories` type. No suppressions, skips or checker exclusions.

Static review against the shared index and the live consumer's versioned key,
column-schema and native-parameter validation found the same eight top-level
fields, required versions, ordered nested descriptions, and SC-01 tags/allowed
dtype names. This review is not actual producer/consumer execution. No sibling
files were changed, copied into this branch, or integrated.

## Red–green evidence and corrections

Durable raw evidence: `.dev-records/verification/20261114-us15-ip3/`.
Serial focused TDD was selected for short feedback cycles; final selections use
four workers with `loadgroup` as required. Existing passing behavior received
regression tests without manufactured failures.

| Slice | Red log and observed defect | Green evidence |
|---|---|---|
| Native NumPy settings | `01-red.log`: unsupported ndarray in categories | `03-green.log`: 28 passed |
| Unknown record method | `04-red.log`: no rejection | `05-green.log`: 29 passed |
| Supplied settings | `06-red.log`: no rejection | `07-green.log`: 30 passed |
| Seeded native call history | `08-red.log`: changed random_state accepted | `09-green.log`: 31 passed |
| Plain record scalars | `10-red.log`: NumPy membership scalar accepted | `11-green.log`: 32 passed |
| Exact source count type | `14-red.log`: float row_count compared equal to integer | `15-green.log`: 71 passed |
| Installed preprocessing | `16-installed-red.log`: both existing wheel probes passed but preprocessing marker absent | `17-installed-green.log`: 1 passed, both new probes executed |
| Plain record arrays | `19-red.log`: tuple membership accepted | `20-green.log`: 83 passed |

The first ndarray green attempt (`02-green.log`) reached native output-schema
validation: the initial fixture's `min_frequency=1` grouped explicit categories
absent from training. The corrected fixture uses native NumPy integer
`max_categories=10` and retains the four-column identity oracle. This is a fixture
correction; no product workaround or assertion relaxation was used. The second
verification passed. No problem exceeded the three-attempt limit.

The initial dtype matrix (`12-matrix.log`) exposed SciPy's rejection of float16
OneHotEncoder output. The final matrix explicitly requires that native
ValueError and training-stage context; other native dtypes retain the sparse
shape/value/tag oracles. Encoding a supported descriptor does not guarantee every
native transformer/container combination. No fallback, changed native defaults,
new dtype guarantee, suppression or skip was introduced.

Initial typing found the contributor stub's missing NumPy-integer type; that
stub was corrected. First shared checks reported one stub import separation and
unformatted Python in the Markdown example. Formatting/import corrections passed
renewed checks; all original logs remain. No executable assertion was weakened.

## Final verification

Linux aarch64, Python 3.12.16, uv 0.13.6. Own `.venv`, no `VIRTUAL_ENV` or
`UV_PROJECT_ENVIRONMENT` override. Development versions: toolkit 0.1.0,
pandas 3.1.0, pyarrow 25.0.1, scikit-learn 1.9.1, NumPy 2.5.4.
Normal installed wheels resolved pandas 3.1.1, pyarrow 25.0.1 and sklearn 1.9.1;
both independently passed. This verifies those observed inputs, not other platforms.

| Command | Result |
|---|---|
| `uv sync --locked --group dev` | Passed; 196 resolved, 193 checked |
| `uv lock --check` | Passed; 196 resolved |
| `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_preprocessing.py tests/integration/test_splitting.py tests/integration/test_data_assessment.py` | **243 passed**, 0 skipped/deselected, 4.86s; 84 producer + 124 splitting + 35 assessment cases |
| `uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_distribution_verification.py -k test_assessment_splits_from_both_artifact_paths` | **1 passed**, both direct/rebuilt paths, 46.00s; inventory 19 collected, 1 selected / 18 deselected |
| `uv run --locked ruff check .` | Passed |
| `uv run --locked ruff format --check .` | Passed; 328 files |
| `uv run --locked mypy src tests` | Passed; 80 source files |
| `uv run --locked agentic-ml --version` | Passed; 0.1.0 |
| `git diff --check` and local Markdown links/anchors | Passed; final handoff inventory retained |

The four warnings are existing NumPy arithmetic warnings from the explicitly
infinite-target assessment case, not skipped or failed coverage. The focused
suite did not select full M1–6. Serial `--collect-only` recorded the artifact
selector inventory; it did not execute a broader test selection. Earlier both-
artifact runs also passed; the final run renewed the formatted guide script.

Lock SHA-256 before/after is unchanged:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
Final source/test/probe fingerprints and working-tree inventory are retained in
`handoff.json`; documentation-only final gate updates do not change tested inputs.

## Installed identities and preservation

Final parent records:
`.dev-records/verification/20261114T211548Z-104172afe9c5-3df03a45f0e54bdba3dd5c65a17b4fe6/`.
Child distribution records:
`.dev-records/verification/20261114T211548Z-104172afe9c5-6dded875443a4d7499e0dca36ef44efd/`.
Both report successful verification; parent cleanup complete. Raw commands,
cwd, logs, artifact hashes and installed identities survive successful pytest
workspace cleanup under the repository retention policy.

- Direct and genuinely sdist-rebuilt wheel SHA-256:
  `c59a70834b020f62f4fdf5dfc39cd46e4ba94f3a107544e088884a7875a606ce`.
- Source distribution SHA-256:
  `3d78a9b2e8ee9e22c700847ea68fc5b8dc3bd556c7611764c35a0745e8a72465`.
- Both exact metadata SHA-256 values:
  `9419e6c0bc6fbf310ade0c9ab6baafaa1c96ea43ce597bb1878ad488f0390f98`.
- Tested guide script SHA-256:
  `1e82f58a61ad778bbacc170d425561c33fe6d01acf9d391c5fd755ea551a534e`.

The guide's imputation/centering learns 2 from training, with literal validation
`[[98,0,0]]`, test `[[198,1,0]]` and inference `[[3,0,1]]`. A separate two-way
string-ID/reordered-index case gives `[[98],[1],[-1]]`. Both installed probes also
reject overlap and held-out fitting, check exact schema/tags/versions/strict JSON,
and verify site-packages imports under their own prefix from unrelated cwd.
There is no MLflow store in this producer probe. Existing driver-owned dataset
versioning checks retain their separate native DVC behavior.

## Gate and remaining owners

No Phase 3 blocker remains. **US-15 Gate 3 is Approved**, with local commit
authorization only, under the
[owning gate](../plans/milestone-1-us-15.md#us-15--implementation-phase-3-produce-metadata-and-verify-installed-use).
The [execute-plan skill](../../.agents/skills/execute-plan/SKILL.md) requires: “At the end of every implementation phase,
including the final one, save progress and stop.” The developer decision above satisfies this gate.
No Phase 4, integration, push or publication is authorized.

US-26 IP4 owns actual installed producer→consumer preservation with shared
committed code/dependency provenance. US-15 IP4 waits for its approved evidence
and separately authorized integration, and owns final M1–6/shared verification
and M1 slice acceptance. M2 AC-04, historical milestone obligations, full
classification/assistant workflows and macOS/Windows verification remain open.
No standalone artifact driver or broader/full pytest suite was launched.
