# US-05 IP1 — Registry and validation contracts

Date: 2026-11-04. Status: investigation complete; developer gate approved, 2026-11-04.
Owning [plan](../plans/milestone-1-us-05.md), [issue #11](https://github.com/jimthompson5802/agentic-ml/issues/11), Milestone 1, US-05-AC-01–05.
Authorized by developer “start ip1”; plan approved by “i approve plan, commit”.
These are proposed contracts for IP2 review, not available APIs or executable acceptance evidence.

## Investigation and reconciliation

Baseline: clean `US-05-configuration-validation` at `55c03b6`. Reviewed the
[design reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority),
[interfaces/configuration](../specs/design/interfaces-and-configuration.md),
[execution/governance](../specs/design/execution-and-governance.md),
[delivery dependencies](../specs/design/milestone-delivery.md#milestone-1-dependencies-and-delivery-order),
[acceptance fixtures](../specs/design/acceptance-traceability.md#reference-acceptance-test-datasets),
[ADRs](../specs/design/architecture-decisions.md),
[repository layout](../specs/design/repository-layout.md), prerequisite plans and
[US-03 contracts](us-03-ip1.md). US-02 and US-03 owning plans record accepted gates
and whole-story acceptance. No prerequisite changes are needed.

Refreshed issue #11's full body and all comment pages through the repository
read helper, then refreshed metadata. Every request succeeded; zero unique
comments equals the reported zero; `updated_at=2026-10-30T02:06:23Z` remained
stable. Issue remains open with no GitHub milestone object; its body assigns M1.
The planning snapshot records complete, stable prerequisite #9/#10 reads.
No issue/design conflict or new scope decision was found.

Existing `agentic_ml.planning.validate_boundaries` is structural and intentionally
registry-independent. Existing accepted fixtures use illustrative IDs and
parameters. `resolve_plan`, `inspect_plan`, `verify_plan` and all planning 1.0
resources stay compatible. Initialization 0.1 drafts remain inert. New semantic
validation consumes verified planning evidence in a separate store. Do not
retroactively add registry checks to planning, change old plan hashes, or replace
`input_ready` with a claim of executable readiness.

No trainer, framework adapter or kernel is introduced. Registry declarations are
bounded data, never instructions to import code. Full supplied-component loading
and training contracts remain US-16/US-18; execution controls remain their owning
stories. This is a bounded refinement of ADR-002/004/007, not acceptance of those
ADRs in full. Existing unauthenticated experiment approvals remain unchanged.

## D1 — Public interfaces and observable states

Add `agentic_ml.validation`, exporting frozen request/result dataclasses and the
functions below. Nested caller dictionaries are copied and validated; frozen
wrappers alone do not establish nested immutability. Inputs and returned values
must not provide mutable aliases into published evidence or registry state.
All names below are selected proposals subject to this gate.

| Interface | Inputs | Observable result |
|---|---|---|
| `validate_registry(declarations: RegistryDocument | None = None) -> RegistryResult` | Optional additive declarative registrations; built-ins always included | `status: valid/blocked`, canonical merged registry and `registry_id` on success, otherwise neither; diagnostics tuple |
| `validate_configuration(request: ConfigurationRequest) -> ConfigurationResult` | `project_root: Path`, `plan_id: str`, `registry: Path | None = None` | `status: valid/blocked`, `validation_id: str | None`, configuration mapping or None, diagnostics tuple; successful immutable publication |
| `validate_candidate(request: CandidateRequest) -> CandidateResult` | `project_root: Path`, `validation_id: str`, `algorithm: str`, `parameters: dict[str, JSONValue]` | `status: valid/blocked`, bound validation ID, algorithm, fully materialized parameters or None, diagnostics tuple |
| `inspect_validation(*, project_root: Path, validation_id: str) -> ValidationInspection` | Explicit project and existing identity | Recomputed integrity/currentness, `status: valid/blocked`, preserved configuration where readable, diagnostics; never a trusted stored success flag |

Reuse the public JSON value and Diagnostic shapes from planning. Export their
aliases if useful, without moving or removing the accepted imports. A new
`ValidationError(code, message)` exception reports operational failures such as
unavailable storage, rather than malformed scientific inputs. Invalid user
objects, unsupported versions, missing evidence and invalid identifiers return
blocked results instead of leaking KeyError/TypeError/tracebacks. Operational
errors preserve their specific cause and do not report validation success.

`ConfigurationResult.configuration` has exactly the fields defined in D6.
`RegistryResult.registry` and `.registry_id` are None on failure.
`ValidationInspection` adds `integrity: bool` and `current: bool` to its
configuration result; unreadable/corrupt evidence gives integrity false, drift
with intact evidence gives integrity true/current false/status blocked.
Candidate results never create a training run, reserve a trial, read raw data,
write approval records or sample missing tunables.

CLI forms:

```text
agentic-ml config validate --project-root ROOT --plan-id sha256:HEX [--registry PATH]
agentic-ml config inspect --project-root ROOT --validation-id sha256:HEX
agentic-ml candidate validate --project-root ROOT --validation-id sha256:HEX --candidate PATH
```

Project root is required rather than inferred from cwd. Relative registry and
candidate paths resolve against that root. Each command emits one JSON result
with `schema_version: "1.0"`, matching its API result fields, on stdout. Exit 0
means semantic validation succeeds, 2 means blocked validation/argument errors,
and 1 means operational failure (safe code/message on stderr, no partial success
JSON). Argparse usage errors may use its normal stderr output. No plain-language
success footer accompanies JSON. Candidate files contain exactly
`{schema_version: "1.0", algorithm: ID, parameters: {...}}`; validation identity
comes from the command argument, preventing an ambiguous embedded identity.

## D2 — Registry schema and bounded registration

Package `registry/validation/1.0/builtins.json` and JSON Schemas under
`schemas/validation/1.0/`: `registry.json`, `configuration.json`, `candidate.json`,
`manifest.json`, and `result.json`. Registry schema version and validation
interface version are both `1.0`; unsupported versions block. No dynamic plugin
discovery, entrypoint imports, attribute evaluation or callable constraint code.

A RegistryDocument is `{schema_version: "1.0", algorithms: [AlgorithmSpec, ...]}`.
AlgorithmSpec has exactly:

- `id`: existing planning identifier grammar; unique across built-in and supplied entries.
- `interface_version: "1.0"`.
- `tasks`: nonempty distinct subset of `classification`, `regression`.
- `adapter`: `{id: ID, version: NONEMPTY_STRING}` describing the validation metadata profile, not an implemented training adapter.
- `library`: `{distribution: NONEMPTY_STRING, reference_version: NONEMPTY_STRING}`. This identifies the library contract from which the metadata was defined.
- `parameters`: mapping of parameter identifiers to ParameterSpec.
- `requires_non_null`: list of `{if_parameter: NAME, equals: SCALAR, then_parameter: NAME}` rules; both names must exist and equals must be a legal value for the antecedent spec.

ParameterSpec has `types`: a nonempty distinct list from `null`, `boolean`,
`integer`, `float`, `string`; required `default`: a legal scalar. Optional
`choices`: a nonempty typed-distinct scalar list; optional inclusive `minimum`
and `maximum`: finite numeric limits. Choices and numeric bounds are mutually
exclusive. Bounds require numeric types apart from optional null and must be
ordered; integer-only bounds must be exact safe integers. A spec may have neither
choices nor bounds, meaning the declared scalar type domain. No arbitrary JSON
Schema, executable validators, arrays, nested objects or unbounded expressions.
Default None is valid only when null is allowed. Reject unknown fields, invalid
defaults, malformed rules and duplicate IDs/parameters before returning a registry.

Declarations are additive metadata only. Explicit `--registry` is the only
project registry selection; do not auto-load `project.yaml` component entries,
project AGENTS files, installed entrypoints or Python code. Supplied entries may
introduce metadata IDs but cannot override built-ins or confer component-execution
support. Preserve exact registry file bytes and source path; canonicalize the
combined registry for content identity. Empty supplied algorithms is allowed;
empty combined registry is impossible because built-ins remain included.

Limits: 1 MiB per selected file; maximum nesting 20; at most 100 combined
algorithms, 1,000 parameters per algorithm, 1,000 choices per parameter and 1,000
rules per algorithm. Strings are at most 4,096 Unicode code points. Reject
excess before expansion/publication. Use the existing strict YAML rules for
JSON-compatible YAML/JSON (no duplicate keys, aliases, tags, BOM, multiple
documents or nonfinite numbers); enforce the same limits on Python inputs.
Canonical evidence uses finite JSON with sorted keys and one terminal newline,
matching the existing planning canonicalization convention.

## D3 — Initial built-in inventory and version semantics

Choose two metadata profiles as the minimal classification/regression inventory:
`dummy_classifier` and `dummy_regressor`. They exercise discrete choices, integer
ranges, continuous bounds, nullable defaults and cross-parameter requirements
without introducing model training. Initial support is scalar, single-output
configuration only. Reject array-valued constants and RandomState objects;
these library capabilities are outside the current scalar search contract.
Unknown algorithm identifiers, including illustrative design examples, receive
an actionable unsupported-algorithm diagnostic from semantic validation; they
remain valid input to the separate structural planner.

The published scikit-learn 1.7.2 documentation defines the constructor defaults
and strategies for [DummyClassifier](https://scikit-learn.org/1.7/modules/generated/sklearn.dummy.DummyClassifier.html)
and [DummyRegressor](https://scikit-learn.org/1.7/modules/generated/sklearn.dummy.DummyRegressor.html).
The tables below define harness metadata profiles based on those contracts,
with scalar-only restrictions selected here. They do not assert training support
or compatibility of every installed library release.

| Algorithm / task | Parameter | Accepted metadata domain | Registry default |
|---|---|---|---|
| `dummy_classifier` / classification | `strategy` | string: `most_frequent`, `prior`, `stratified`, `uniform`, `constant` | `prior` |
| same | `random_state` | null or integer in [0, 4294967295] | null |
| same | `constant` | null, string, integer or finite float | null |
| `dummy_regressor` / regression | `strategy` | string: `mean`, `median`, `quantile`, `constant` | `mean` |
| same | `constant` | null, integer or finite float | null |
| same | `quantile` | null or float in [0.0, 1.0] | null |

Both profiles use adapter `{id: "sklearn_dummy_scalar", version: "1.0"}` and
library `{distribution: "scikit-learn", reference_version: "1.7.2"}`. This adapter
identifier means validation metadata only. Reject boolean constants in these
profiles; a separate supplied metadata fixture verifies boolean parameters.
All profiles are complete over their supported constructor parameter names;
no implicit constructor kwargs or guessed defaults exist.

Rules: classifier strategy constant requires non-null constant. Regressor
strategy constant requires non-null constant; strategy quantile requires
non-null quantile. Other supplied constant/quantile values remain type-checked
even when the selected strategy ignores them. Validation does not inspect
training labels or assert that a classifier constant exists in a dataset.
Dataset-dependent compatibility belongs to the future training boundary.

Record the observed installed library version using distribution metadata only,
without importing the framework. Missing distributions produce an explicit
`installed_version: null`; this does not invalidate a metadata-only configuration.
Record library reference version, observed installed version, adapter metadata
version and harness installed version separately. Do not infer executable
compatibility from their presence or from agreement with reference_version.
No new framework runtime dependency or lockfile change is needed for this slice.
A future training adapter must establish actual supported-library compatibility,
installation and dataset-dependent checks before execution.

On inspection or candidate validation, changed observed library presence/version,
adapter profile, registry declarations, harness identity, selected inputs or
lockfile blocks reuse with `stale_validation`; create new validation evidence
explicitly. Drift is never reconciled by replacing old recorded defaults.

## D4 — Configuration preflight and combination policy

Configuration validation first calls the current-source planning verification
contract, requiring integrity, `input_ready` and all applicable current approval
records. Preserve the plan's project/experiment binding and effective task,
algorithm set, narrowed search and budgets; nothing here expands them. Semantic
validation cannot resolve delegated choices or manufacture approval records.

Validate every algorithm and parameter in the declared search boundary against
registry task/type/domain requirements, as well as the effective boundary.
A currently unselected algorithm is not a hiding place for invalid declarations.
Run domain-combination checks on each declared and effective algorithm space;
configuration must not conceal invalid combinations by choosing one good trial.
Merge each space with defaults: every parameter absent from both fixed and search
gets its registry default as an immutable value. A search parameter remains a
domain; do not turn its registry default into a missing trial choice.

Every value in each domain must satisfy its ParameterSpec. Categorical choices
must be nonempty, typed-distinct, finite supported scalars, and all legal for the
parameter. Numeric search types are `integer`/`float`, with the existing 1.0
`min`, `max`, `scale` fields. Bounds are inclusive, ordered, and may be equal.
Integer ranges require integer bounds, integer-compatible specs and integer
candidate values; float ranges require float-compatible specs. Logarithmic
bounds are strictly positive for both range types. No sampler is introduced;
integer range validation guarantees only integral candidate values are accepted,
not a particular sampling distribution.

Use a conservative universal compatibility policy for independent domains.
For each requires_non_null rule, if the antecedent value can occur in its
fixed/default/search domain and the consequent domain can contain null, reject
the whole configuration as `incompatible_combination`. Domain intersection and
null membership are analytic; never enumerate a numeric interval or a Cartesian
product. Candidate checks apply the same rule to singleton resolved values.
No conditional-parameter language is introduced.

Examples:

- Default-only classifier and regressor configurations pass.
- Regressor fixed strategy quantile with omitted quantile fails, because its recorded default is null.
- Strategy choices mean/quantile with quantile choices null/0.5 fail, even though one pair works.
- Strategy choices mean/quantile with quantile range [0.1, 0.9] pass.
- Strategy choices prior/constant with constant null fail; a non-null fixed constant passes the metadata rule.

## D5 — Candidate materialization, typing and diagnostics

A candidate must select an algorithm in the effective allowed set. For every
parameter: fixed value is inherited and cannot change; omitted registry-default
value is inherited and cannot change; every remaining tunable requires an
explicit candidate value. An explicit fixed/default parameter is permitted only
when typed-equal to the recorded value. Reject unknown parameter names,
missing tunables, out-of-bound values and incompatible singleton combinations.
Return the full parameter mapping, including every default and fixed value;
include parameter origins (`fixed`, `default`, `candidate`) in candidate results.
Results never mutate inputs or reinterpret a default as tunable.

Scalar equality is type-sensitive: null, boolean, integer, float and string are
distinct. `true`, `1`, `1.0` and `"1"` do not substitute for each other in
categorical/fixed/default equality. Integer requires Python int excluding bool,
with magnitude at most 9007199254740991. Float requires finite Python float;
no string parsing or int-to-float coercion. Authors use `1.0` for float candidates
and float-valued categories. Float range endpoint YAML literals may be integers
or floats (excluding bool), because endpoints bound a real interval; returned
float candidates remain floats. For a spec admitting both int and float, bounds
apply numerically but fixed/default equality remains type-sensitive. Preserve
existing structural-planner rules and add semantic checks separately.

Diagnostics reuse `code`, `field`, `source_path`, `line`, `column`, `message`.
Return the first deterministic blocking diagnostic (registry, plan, declared
space, effective space, candidate order; lexical algorithm/parameter/rule order).
Messages identify the violated rule and permitted correction without echoing
arbitrary supplied values or raw file content. Source file locations use known
parser marks; Python requests and synthesized defaults use null line/column.

| Code | Example field | Required actionable message meaning |
|---|---|---|
| `unsupported_version` | `schema_version` | Use supported validation schema/interface 1.0 |
| `invalid_registry` | `algorithms.0.parameters.x.default` | Default must satisfy the declared parameter domain |
| `duplicate_algorithm` | `algorithms.0.id` | Choose an ID distinct from built-ins and other declarations |
| `unknown_algorithm` | `algorithms.name` | Select a registered algorithm or supply explicit metadata |
| `task_mismatch` | `algorithms.name` | Use an algorithm supporting the effective task |
| `unknown_parameter` | `algorithms.name.fixed.x` | Remove the unknown name or use a registered parameter |
| `invalid_parameter_type` | `parameters.x` | Supply the required scalar type without coercion |
| `invalid_domain` | `algorithms.name.search.x` | Correct empty/duplicate choices, bounds or scale to satisfy the spec |
| `incompatible_combination` | `algorithms.name` | State which antecedent parameter requires a non-null consequent |
| `missing_parameter` | `parameters.x` | Supply a value for the required tunable parameter |
| `fixed_parameter` / `default_parameter` | `parameters.x` | Retain the bound fixed/default value; revise inputs to authorize tuning |
| `outside_boundary` | `parameters.x` | Choose an allowed categorical value or inclusive numeric range value |
| `invalid_candidate` | candidate field | Correct the exact envelope/parameter mapping shape |
| `invalid_validation` | `validation_id` | Evidence is missing, corrupt, unsupported or bound to another project |
| `stale_validation` | changed input/library/approval field | Revalidate current inputs explicitly; preserved evidence remains available |
| `input_limit` / `unsafe_path` | selected path/field | Use a bounded regular project file and supported document size |

Propagate existing planning blocking diagnostics with their stable codes and
locations when the failure originates in planning verification. No rewrite of
historical Diagnostic messages is required.

## D6 — Identity, preservation and safe project access

Store successful configurations under
`.agentic-ml/validations/<64-hex-validation-digest>/`. The validation ID is
`sha256:` plus SHA-256 of canonical configuration.json bytes. That configuration
has exactly:

```text
schema_version: "1.0"
project_root: absolute canonical project root
experiment_id: preserved plan experiment ID
plan_id: immutable US-03 plan ID
registry_id: SHA-256 of canonical merged registry JSON
registry_source: null or {path: project-relative path, sha256: exact-byte hash}
harness: preserved installed version/origin identity as in planning
libraries: sorted [{distribution, reference_version, installed_version}]
algorithms: mapping ID -> {
  task, adapter: {id, version}, library_distribution,
  fixed: effective fixed values, defaults: omitted immutable registry values,
  search: effective tunable domains
}
capabilities: ["configuration_validation", "candidate_validation"]
execution_authorized: false
```

A bundle contains `configuration.json`, `registry.json`, optional `registry-source.yaml`,
and `manifest.json` mapping exact relative member names to SHA-256 digests, with
schema version and validation ID. Snapshot the entire canonical combined registry,
including rules, default domains and reference identities. Registry ID is also
`sha256:HEX`. Configuration ID excludes the manifest to avoid circular hashing;
manifest member inventory is exact, with no arbitrary extra/traversal members.
Original experiment source bytes remain preserved by the immutable referenced
US-03 plan; do not duplicate or edit those plan bundles. Use plan public inspection
and verification rather than trusting hashes alone.

Inspection/candidate validation validates schemas, inventory, hashes and IDs,
recomputes registry semantics and configuration from the preserved/current plan,
compares installed profile/harness/library identities, and requires matching
current selected source bytes and current delegated approvals. Rebuilding an
identical valid configuration reuses its ID and bundle without rewriting.
Changed registry source formatting may create a new ID because exact source
bytes are part of provenance. Missing/changed/corrupt input or revoked approval
blocks; never overwrite conflicting evidence or silently update defaults.

Before returning success, recheck selected inputs and plan verification after
materialization/publication. If inputs drift, return blocked and retain any
published immutable bundle for diagnosis, rather than asserting currentness.
This is detection at validation boundaries, not atomic authorization against an
adversarial workspace writer. Future submission must independently recheck.

Reuse planning's project-access safety conventions internally: explicit root,
regular files beneath it, symlink/traversal/overlap rejection, bounded reads,
exclusive lock, temporary publication directory and atomic final rename. New
storage locking is scoped to `.agentic-ml/validations`; do not nest conflicting
plan write locks. Reject a symlinked store/parent/member. Contention produces a
safe operational error; repeated/concurrent identical publication is idempotent
or reports busy, never conflicting overwrites. Interrupted publication preserves
available diagnostic state and cannot be inspected as a successful final bundle.
Do not import raw-data paths or open notebooks while validating configuration.

Candidate checks are read-only and return results without publishing candidate
bundles in this story. They bind the validation identity and complete parameters;
future run capture must preserve that result plus source and revalidation evidence.
All values are author-controlled metadata; checksums do not establish truth of
custom parameter specs, author identity or tamper resistance.

## D7 — Confirmable public test boundaries

IP1 gate approval confirms the following boundaries before IP2 writes tests.
Expected defaults, mappings and diagnostics must be specified independently of
registry/validator internals. No calls to private helpers to establish success.

| Boundary / planned cases | Acceptance criteria | Coverage limits |
|---|---|---|
| `validate_registry`: both built-ins and an explicit scalar fixture covering bool/int/float/string/null; duplicates, bad defaults/specs/rules, unsupported versions, invalid typed Python objects and limits | AC-01, AC-03, AC-04 | Validates metadata, not truth of arbitrary supplied declarations or callable compatibility |
| `validate_configuration`: real preserved project plans, both tasks, wrong/unknown ID/task/parameter, every supported default, supported/unsupported scalar values and combinations | AC-01, AC-03, AC-04 | No estimator constructors or dataset-dependent checks |
| Configuration/candidate domain cases: empty/type-distinct choices; lower/upper/equal/reversed endpoints; negative/zero/positive log bounds; fractional integer bounds/candidates; NaN/infinity; fixed/default preservation; missing tunables | AC-02, AC-03, AC-04 | No sampling engine/distribution guarantee |
| Configuration universal combination checks and equivalent singleton candidate checks; default-null implication failure and valid non-null domain | AC-01, AC-02, AC-04 | Only declarative requires_non_null rules; conditional search remains unsupported |
| CLI and project helper parity: same valid/invalid matrix, full effective parameters/origins, stable diagnostics and exit outcomes, unrelated cwd | AC-01–05 | Custom code invokes installed validation; arbitrary Python bypass and kernels remain outside this slice |
| Inspection/candidate reuse: source/registry/lock/library/harness/profile drift, stale/revoked approval, missing/corrupt/wrong-root bundles, changed defaults, mutation isolation, repeated publication, busy/interrupted publication and unsafe paths | AC-03–05 | Detects current mismatch; does not authenticate workspace writers or protect future training automatically |
| Real direct wheel and sdist-rebuilt wheel: resource inventory, isolated imports/metadata, same API/CLI/helper outcomes in separate experiment projects | AC-01–05 | Observed platforms only; no manually maintained harness checkout or contributor dependencies |
| Existing structural planner, init and approvals regressions unchanged | AC-04, prerequisite compatibility | Old input_ready is structural only; semantic failures are separately observable |

Use small fixtures, explicit temporary project/storage ownership and existing
installation/distribution groups. A supplied metadata fixture has a deliberately
non-importable entrypoint-like string value where appropriate; no registry field
is interpreted as an entrypoint. Test observable absence of unintended project
writes/import side effects using a project marker sentinel, not private call
counts. Candidate checks should leave an independently enumerated project/store
snapshot unchanged. No raw datasets, credentials or fitting are required.

Future US-09/US-10/US-16/US-18 entrypoints must call current candidate validation
on every submitted candidate before constructing or fitting an estimator, starting
a kernel or executing supplied training code, together with their own applicable
authorization, access, budget and evidence controls. They must add a public
regression demonstrating invalid submissions cannot start training. A cached
CandidateResult or config status is not a bearer authorization token. This
handoff is not evidence that unimplemented entrypoints satisfy AC-05 today.

## Task refinement and verification

US-05-IP1-T1: interfaces/statuses and backward compatibility settled by D1/D6.
T2: registry, complete bounded inventory, explicit missing-library semantics and
versions settled by D2/D3. T3: universal-combination policy, typing, schemas and
public cases settled by D4–D7. T4: document checks recorded below. All selections
remain proposals awaiting the developer's IP1 decision; no unresolved technical
choice blocks implementation once approved.

IP2 files: new `src/agentic_ml/validation/{__init__,models,registry,configuration,candidates,storage}.py`,
`src/agentic_ml/registry/validation/1.0/builtins.json`, the five D2 schemas,
`src/agentic_ml/cli/validation.py`, CLI dispatch registration, and new
`tests/integration/test_configuration_validation.py`. Internal shared safety
helpers may be reused without changing accepted public planning contracts.
IP2-T1 owns registry metadata/schema/resource inventory; T2 owns configuration
semantics; T3 owns candidate rules; T4 owns project evidence and CLI. Develop
vertical public behaviors across these task boundaries rather than writing all
tests first. Existing planning bundle fixtures supply project setup.

IP3 extends `tests/installation/check_planning.py` and the existing installed
planning distribution test to cover the new resource inventory and D7 cases on
both real wheel paths. Preserve the driver's provenance, retention and scheduling
contracts. Update `tests/packaging/check_installed.py` for resource inventory and
public imports, plus `README.md` / distribution docs for usage/limits.

IP1 changes documentation only. No tests, schemas, runtime metadata or Python
product implementation are written. TDD, milestone pytest and shared executable
checks are inapplicable at this gate. IP2/IP3 retain the approved M1 gate,
M1–6 acceptance, shared checks and deferred owners. The three existing skips,
M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY remain unresolved.

Actual document verification on 2026-11-04:

- Local file/anchor validator checked 78 relative links across this report, the
  owning plan, ADR document and checkpoint: zero unresolved targets.
- Plan-record validation confirmed IP1-T1–T4 Complete, all five US-05 criterion
  IDs present and all three implementation-phase decisions still Pending.
- Manual review confirmed each criterion has public cases, the initial inventory
  includes every supported parameter/default, future entrypoint limitations are
  explicit and no executable task crosses the pending IP1 gate.
- `git diff --check` passed. A separate comparison against HEAD confirmed only
  the report, plan, ADR document and checkpoint changed; no product/tests,
  packaged resources, dependencies or lockfile changed.

No executable behavior, installed framework compatibility or platform support is
verified by these document checks. No executable tests were run because IP1 is a
contract-only implementation phase. Developer IP1 approval remains pending.

IP1 approval: developer “i approve”, 2026-11-04, after the interface review; this
approves D1–D7 and their public test boundaries and authorizes IP2 as requested
at the IP1 gate. Historical pending statements above describe the review snapshot.
