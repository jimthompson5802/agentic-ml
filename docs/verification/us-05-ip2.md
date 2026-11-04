# US-05 IP2 — Shared semantic and candidate validation

Date: 2026-11-04. Technical verification complete; developer IP2 gate approved.
Owning [plan](../plans/milestone-1-us-05.md), [issue #11](https://github.com/jimthompson5802/agentic-ml/issues/11), US-05-AC-01–05.

## Authorization and boundaries

Developer “i approve” after the IP1/interface review accepted the presented IP1
approval and IP2 authorization request. The approved [IP1 contracts](us-05-ip1.md)
D1–D7 define public test boundaries; no new boundary or scope change is required.
Baseline commit `55c03b6c1379fea7762ca0afd63f720dfbea72af` on
`US-05-configuration-validation`; IP1 report/plan/ADR/checkpoint edits were present.
No commit/push/issue changes or IP3 execution is authorized by this phase.

The installed public package now supplies `validate_registry`,
`validate_configuration`, `validate_candidate` and `inspect_validation`, with
frozen typed requests/results and operational `ValidationError`. The CLI adds
`config validate/inspect` and `candidate validate` with explicit project roots,
versioned JSON and 0/2/1 success/blocked/operational exit codes. CLI validation
uses the same public functions. Existing structural planning APIs and schemas
remain unchanged.

Built-in registry metadata covers the complete scalar parameter names/defaults
for the two approved dummy profiles, with explicit adapter metadata and library
reference versions. Additional metadata is data-only, explicitly selected and
cannot shadow built-ins or import code. Actual library observations may be null;
validation never claims a missing training adapter is executable.

Configuration checks both declared and effective domains, task compatibility,
registered parameter names/types/defaults, inclusive typed ranges and conservative
non-null implication rules without sampling or Cartesian enumeration. Candidates
materialize fixed/default values, require every tunable and reject expansion.

Separate immutable validation bundles preserve canonical configuration/registry,
exact selected registry bytes and hashes, and the existing immutable plan identity.
Descriptor-based bounded/no-follow project access, exclusive locks, fsync and
atomic publication preserve evidence; identical validations reuse existing bytes.
Inspection independently checks inventory/hashes/schemas and current plan,
source, approval, harness and library identities. Read-only candidate checks
repeat currentness checks and do not publish trial/run state.

## TDD evidence

Raw JUnit failure/success evidence is retained in
`.dev-records/verification/us05-ip2/`. Each cycle used the new public-interface
module `tests/integration/test_configuration_validation.py`. Focused serial runs
were selected for short red–green feedback as allowed by the verification policy;
the phase gate uses four workers with loadgroup.

Commands for cycles 01–10:

```text
uv run --locked pytest tests/integration/test_configuration_validation.py --junitxml=.dev-records/verification/us05-ip2/NN-red.xml
uv run --locked pytest tests/integration/test_configuration_validation.py --junitxml=.dev-records/verification/us05-ip2/NN-green.xml
```

Cycle 11 red selected only
`tests/integration/test_configuration_validation.py::test_validation_cli_matches_public_api_from_unrelated_cwd`;
its green ran the full module. Cycle 12 red selected only the new semantic-replay
regression (initially named `test_recomputed_checksums_do_not_hide_type_changed_default`,
renamed descriptively to `test_recomputed_checksums_do_not_hide_type_changed_fixed_value`
without changing its assertion); its green ran the full module. JUnit includes original assertions, failure
tracebacks and actual elapsed durations. Negative cases require explicit diagnostic
codes/parameters, independently specified defaults and no successful identity.

| Cycle | Behavior / criteria | Red | Green |
|---|---|---|---|
| 01 | Built-in defaults, AC-01/03 | Missing validation package; 1 failed | 1 passed |
| 02 | Registry schema/conflicts, AC-01/04 | Invalid declarations accepted; 4 failed, 1 passed | 5 passed |
| 03 | Unsupported interface version, AC-01/04 | Wrong diagnostic; 1 failed, 5 passed | 6 passed |
| 04 | Preserved config/defaults, AC-01/03 | Missing public configuration API; 1 failed, 6 passed | 7 passed |
| 05 | Semantic tasks/types/combinations/domains, AC-01/02/04 | Invalid configurations accepted; 6 failed, 7 passed | 13 passed |
| 06 | Candidate materialization/current inspection, AC-03/05 | Missing public candidate API; 1 failed, 13 passed | 14 passed |
| 07 | Fixed/default/search boundaries, AC-02–05 | Invalid candidates accepted or unknown-ID KeyError; 8 failed, 14 passed | 22 passed |
| 08 | Idempotent immutable publication, AC-03 | Existing bundle rename error; 1 failed, 22 passed | 23 passed |
| 09 | CLI/API parity and explicit root, AC-04/05 | Missing CLI commands; 1 failed, 23 passed | 24 passed |
| 10 | Original search diagnostic location, AC-04 | Missing source path; 1 failed, 24 passed | 25 passed |
| 11 | Candidate-file diagnostic location, AC-04 | Missing source path; 1 failed | 44 passed |
| 12 | Type-sensitive evidence replay, AC-03/04 | Forged fixed integer-to-float change accepted despite recomputed hashes; 1 failed | 57 passed |

Additional public regression coverage exercises previously green behavior without
manufacturing new red failures: corrupted/missing/wrong-root/extra evidence,
int/float endpoints, metadata types/defaults/rules, missing-library and observed
installation drift, typed categories, read-only candidate operations, symlinked
stores/registry/members, busy locks and revoked delegated approvals. Coverage
runs recorded 44, 51 and 56 passing cases (`coverage-1.xml` through
`coverage-3.xml`). No assertions, timeouts or existing skips were weakened.

Final review found Python mapping equality could conflate fixed integer and
float values during semantic replay. Cycle 12 preserves that original regression,
then changes currentness comparisons to canonical content identities. Corrective
attempt 1 passed the original regression and all focused cases; no failed
corrective attempt or weakened assertion. The first M1 run completed 369 passes
and one existing skip in 222.72s; source changed during its execution for this
correction, so it is preliminary compatibility evidence, not the final gate.
Retained `m1-gate.xml` / `m1-gate.log`; final-input renewal is recorded separately.

Environment setup first encountered the sandbox's read-only uv cache; the
approved escalated locked synchronization succeeded. The initial sandbox pytest
launch likewise could not acquire the cache lock and was repeated with approved
permissions before any behavioral result was claimed. Those setup errors are
not red evidence. First lint/type checks reported import/style and typed-JSON
issues; corrected without suppressions, then all shared checks passed. These
were tooling corrections, not repeated unsuccessful fixes of an original behavior.

## Verification and identities

Observed platform: Linux 7.0.12 linuxkit / aarch64 / glibc 2.36, Python 3.12.16,
uv 0.13.6, pytest 9.1.1 and xdist 3.8.0. `identities.json` records baseline source
and lock identities. The current lock matches the committed baseline SHA-256:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
No dependency declaration or lockfile change. Final-input executable/resource/test
SHA-256 identities and command inventory are retained in `identities.json` and
`commands.json`. `m1-collection.log` independently records 473 collected,
371 selected and 102 deselected cases.

| Check | Command | Actual result |
|---|---|---|
| Locked development sync | `uv sync --locked --group dev` | Passed; 195 packages resolved, editable harness rebuilt |
| Lock consistency | `uv lock --check` | Passed; 195 packages resolved |
| Lint | `uv run --locked ruff check .` | Passed |
| Formatting | `uv run --locked ruff format --check .` | Passed; 150 Python files |
| Strict typing | `uv run --locked mypy src tests` | Passed; 53 source files |
| CLI smoke | `uv run --locked agentic-ml --version` | Passed; `0.1.0` |
| M1 phase gate, final inputs | `uv run --locked pytest -n 4 --dist=loadgroup -m milestone_1 --junitxml=.dev-records/verification/us05-ip2/m1-final.xml --durations=20` | Passed — 370 passed, one existing skip in 218.29s, exit 0; 473 collected, 371 selected, 102 deselected; `m1-final.xml` / `m1-final.log` |
| Whitespace and document links | `git diff --check` and local link/anchor checks | Passed after final records; local file/anchor and new-file whitespace checks also passed |

## Acceptance coverage and deferred owners

| Criterion | Direct evidence | Limits / remaining work |
|---|---|---|
| US-05-AC-01 | Registry defaults/schema, registration conflicts, task/name/type/domain and combination tests | Declarative metadata, not full model or dataset validation |
| US-05-AC-02 | Configuration/domain cases and strict integer/float/category candidate checks; existing structural range regressions in M1 | No sampler or conditional search language |
| US-05-AC-03 | Explicit defaults/origins, immutable reuse, corrupt/stale identities and actual metadata drift | Version observations do not prove executable compatibility |
| US-05-AC-04 | Safe actionable CLI/API diagnostics with source locations; no validation store on semantic rejection | No training entrypoint introduced |
| US-05-AC-05 | CLI/API/helper-equivalent shared candidate boundary, readonly and revoked approval checks | Future runners/notebooks/custom training require fresh validation and independent execution controls |

IP3-T1 owns extended installed validation assertions on both wheel paths and
resource inventory; IP3-T2 owns usage documentation and execution handoff;
IP3-T3 owns final M1–6 acceptance and reconciliation. Existing M1 installed
planning regressions are compatibility checks, not evidence of the new installed
semantic matrix. No standalone artifact or broader local suite command was run.
No M1–6 story acceptance is claimed at this intermediate phase.

Preserve M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY, the three existing temporary
skips, historical timeout causes and platform limitations. Linux evidence does
not verify macOS or Windows. Checksums are not approval authentication or a
sandbox; arbitrary Python/workspace writers remain outside the validation trust
boundary. Execution budgets, protected-data access and training adapters remain
with their owning capabilities.

## Developer gate

IP2 technical completion: US-05-IP2-T1–T5 Complete. Final M1 and shared checks
passed; lock unchanged. Final executable/resource/test identities were checked
against those captured at the final run and did not change. The single M1 skip
is the existing developer-authorized missing-planning-schema distribution case;
it is not counted as passing coverage.
Developer decision: Approved by “i approve ip2; commit; do not strt ip3 yet”,
2026-11-04. Local commit authorized. IP3 explicitly remains unstarted pending
further developer direction.


Actual changed components: `src/agentic_ml/validation/` (typed models, checks,
registry, domain logic, configuration/candidates and storage), CLI registration
plus `src/agentic_ml/cli/validation.py`, packaged `registry/validation/1.0/` and
five `schemas/validation/1.0/` resources, and
`tests/integration/test_configuration_validation.py`. Owning plan, ADR approval
record and checkpoint are updated. No IP3 probe/usage work is included.
