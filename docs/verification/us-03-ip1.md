# US-03 IP1 — Experiment input and approval contracts

Date: 2026-10-31. Status: design investigation complete; developer IP1 gate approved.
Owning [plan](../plans/milestone-1-us-03.md); [issue #10](https://github.com/jimthompson5802/agentic-ml/issues/10), Milestone 1, US-03-AC-01–05.
The unauthenticated approval scope was explicitly approved in US-03-SC-01; the
remaining IP1 contracts were approved by “i approve the changes” (2026-10-31). These are not available commands or
executable acceptance evidence. IP1 was authorized by “execute us-03 ip1”.

## Sources and reconciliation

Baseline: clean `US-03-experiment-boundaries`, commit `4a2882b`. Read the design
reading map, interfaces/configuration, execution/governance, repository layout,
delivery dependencies, acceptance fixtures, architecture decisions, US-03 criteria
and accepted US-02 plan. Initialization's 0.1 schemas accept only inert empty
search/data and unconfigured execution. They cannot be used as resolved inputs.

Refreshed complete bodies and all comment pages using
`sh .codex/scripts/github-read.sh issues/NUMBER` and
`sh .codex/scripts/github-read.sh issues/NUMBER/comments --paginate --slurp`,
then refreshed metadata. Every request succeeded; unique comments = reported
comments = 0 for #10, #9 and #11. Stable timestamps respectively:
`2026-10-30T02:06:20Z`, `2026-10-31T13:05:49Z`, `2026-10-30T02:06:23Z`.
#9 is closed and its owning plan records acceptance; #10/#11 are open. The issue
body assigns Milestone 1; GitHub milestone metadata is unset. No issue discussion
decisions at retrieval. The subsequent developer scope decision US-03-SC-01 below supersedes the authenticated approval proposal.
`gh` 2.102.0 reads succeeded despite sandbox `gh auth status` exit 1. No write to
GitHub is required. US-03 criteria require approval without prescribing
authentication. The general governance authentication requirement is revised for this version under SC-01;
future US-23-AC-02 remains deferred. Illustrative 0.1 design examples
are superseded only for this proposed resolver slice, subject to this gate.

## T1 — Input language and public interfaces

### Scope decision US-03-SC-01

On 2026-10-31 the developer directed: “Authenticated approval is a bit much for
this version of the toolkit. For now let's use unauthenticated approval in
experiments.” This approves replacing the initial SSH-signature, protected-system
policy and distinct-OS-identity proposal with explicit project-local approval
records. It removes keys, trust roots, policy epochs, expiry and separate-account
host prerequisites from current delivery. Approval binding and revocation checks
remain; reviewer labels and timestamps are descriptive, not authenticated.

US-03-AC-04 still requires approval before using a delegated choice. Its evidence
now establishes correct record matching and pending/stale/revoked outcomes, not
who issued the record. A workspace writer can fabricate an approval or alter
approval/revocation history. This limitation is accepted for this version.
Authentication and tamper-resistant approval history remain deferred future
hardening; this change does not satisfy future US-23-AC-02. Separate data access,
execution budgets and protected-test obligations remain with their capabilities.
The developer explicitly clarified: “The change in authentication is only for
when a data scientist is using the toolkit in an experiment. I still want the
existing approval gates currently in place for development and testing.” All
harness development/testing gates, confirmed public test boundaries, verification
requirements, attempt limits, story acceptance and publication requirements
remain unchanged. Runtime approval records cannot authorize harness development.

This change reworked T1 approval signatures/API, T2 approval storage/readiness,
T3 entirely and T4 security fixtures; unauthenticated formats below supersede the
initial proposal. The earlier design-only document checks remain historical;
revised document checks are recorded at the end. No executable work is invalidated.

### Brief format 1.0

UTF-8 Markdown, optional BOM rejected, LF or CRLF accepted and original bytes
preserved. Exactly one `# Experiment: TITLE`, then exactly one each of `## Objective`,
`## Data`, `## Features`, `## Evaluation`, `## Algorithms`, `## Budget`, in that
order. Each section contains exactly one fenced `yaml` mapping. Empty lines and
explicit `> Note: ...` annotations may surround it; annotations are preserved,
non-authoritative commentary. Other prose, unknown/duplicate headings, extra
fences, duplicate mapping keys, YAML aliases/anchors/tags/merge keys or multiple
documents are blocking diagnostics. The Objective mapping carries
`schema_version: "1.0"`. No natural-language model or project code interprets
the document. Natural-language guidance is captured in explicit string fields.
Existing free-form/TODO briefs require author conversion, never guessed parsing.

Each required decision field accepts its concrete value or a delegation object:
`{delegate: "reason/question", proposal: VALUE, rationale: "reason"}`.
`proposal` and `rationale` are optional together; without them the decision is
unresolved. Empty delegation text, a lone rationale, nested delegations and
unknown keys fail. Concrete proposal values obey the same field schema. A
delegation remains delegated after a proposal; editing a proposal never approves
it. Required fields cannot be omitted, null or `TODO`; null is allowed only at
explicitly nullable fields below. Empty guidance strings fail. Strings are data,
never executable expressions. No defaults fill scientific decisions.

The complete explicit example below also defines required field names:

````markdown
# Experiment: Churn baseline

## Objective
```yaml
schema_version: "1.0"
objective: Predict churn using information available at signup.
```

## Data
```yaml
sources: [data/customers.parquet]
target: churned
task_type: classification
```

## Features
```yaml
include: [age, signup_month]
exclude: [customer_id, cancellation_date]
guidance: Use only signup-time observations.
availability: All included predictors must exist at signup time.
```

## Evaluation
```yaml
metric: f1_macro
direction: maximize
split:
  strategy: time
  time_column: signup_date
  group_column: null
  validation_fraction: 0.2
  test_fraction: 0.2
  seed: 42
  constraints: Validation and test follow training chronologically.
```

## Algorithms
```yaml
mode: compare
allowed: [random_forest_classifier, logistic_regression]
```

## Budget
```yaml
max_trials_per_algorithm: 10
max_total_trials: 20
max_runtime_seconds: 600
max_memory_mb: 2048
max_cost: null
currency: null
```
````

Concrete domains: task `classification|regression`; metric a nonempty identifier
(registry compatibility later); direction `minimize|maximize`; mode
`use|select|compare`. `allowed` is a nonempty unique list of opaque identifiers;
use requires exactly one, select records a permitted selection pool, compare
requires every member of the effective pool. Selection/training is later work.
Features include/exclude are unique string lists with no overlap; include may be
empty only with explicit guidance that selection awaits a later feature plan.
The harness records guidance/availability/constraints verbatim and cannot certify
their scientific satisfiability without datasets and later validation.

Split is one decision object: `random|stratified|time|group`; time requires a
nonempty time column, group a group column, others require those columns null.
Stratified requires classification. Fractions are finite numbers strictly between
0 and 1 with sum < 1; seed a nonnegative integer. These are proposed constraints,
not a generated or approved split manifest. Budgets require positive integers
except nullable positive `max_memory_mb`, nullable positive finite `max_cost`, and
nullable three-uppercase-letter `currency`; cost and currency must both be set or
both null. Booleans are never numbers. A null limit explicitly records “not
specified here”, never unlimited execution permission. Total trials may be less
than per-algorithm cap times count; both are ceilings, not promised allocations.
All numeric values must be finite and within JSON-safe integer bounds where
integer; non-finite YAML numbers fail. Input limits: 1 MiB per file, six brief
sections, YAML nesting <= 20, <= 100 algorithms, <= 1000 parameters per algorithm,
<= 1000 choices per parameter. Fail without partial plan publication on excess.

Delegation examples: `metric: {delegate: "Choose a classification metric"}`
blocks; `metric: {delegate: "Choose a classification metric", proposal: f1_macro,
rationale: "Equal weight to both classes"}` still needs an explicit scoped approval record.
The same envelope can delegate `sources`, `target`, `task_type`, feature fields,
`split`, algorithm fields or a budget field. Objective and schema version are
required literal author statements. Sources must be resolved before capture;
unresolved sources yield a reviewable blocked plan without data access.

### Search and execution schemas 1.0

All objects reject unknown fields. YAML uses JSON-compatible scalars, the strict
loader rules above and schema Draft 2020-12. Search shape:

```yaml
schema_version: "1.0"
algorithms:
  random_forest_classifier:
    fixed: {random_state: 42}
    search:
      n_estimators: {type: integer, min: 100, max: 1000, scale: linear}
      max_depth: {type: categorical, choices: [null, 5, 10]}
  logistic_regression:
    fixed: {max_iter: 2000}
    search:
      C: {type: float, min: 0.001, max: 1.0, scale: logarithmic}
```

Algorithms nonempty; fixed/search required maps (either may be empty). Fixed
values are JSON scalars; compound parameters await an owned schema revision.
Categorical values are nonempty unique JSON scalars with type-aware equality:
`true`, `1`, `1.0`, `"1"` differ. Numeric ranges use inclusive ordered bounds,
integer endpoints for integer, finite int/float endpoints for float, and explicit
`linear|logarithmic`; logarithmic requires both endpoints > 0. No fixed/search
overlap or conditional schema. Empty identifiers fail. Registry existence,
parameter compatibility and defaults remain US-05.

```yaml
schema_version: "1.0"
id: churn
brief: experiments/churn/experiment.md
search_space: experiments/churn/search-space.yaml
notebooks: [experiments/churn/notebooks/01_data_assessment.ipynb]
working_directory: .
data: [data/customers.parquet]
execution:
  status: configured
  algorithm_subset: [random_forest_classifier, logistic_regression]
  parameters: {}
  search_overrides: {}
  budget_overrides: {}
```

All displayed keys required except the four override maps/list inside execution;
omission means inherit, with provenance. Notebook list is nonempty unique paths.
`data` must equal effective brief sources (order retained); unresolved source
delegation blocks this check. `parameters` maps algorithm IDs to fixed scalar
selections; `search_overrides` maps IDs to parameter search definitions of the
same shapes above. `budget_overrides` maps budget names to concrete ceilings.
No model imports, feature pipeline, adapters, network connectors, arbitrary code
or execution backend are enabled by schema 1.0. Future fields need versioned
schema changes, not silent acceptance. Version strings must match exactly;
unknown versions block. Project configuration remains the accepted init 0.1
schema; the planning store is a fixed separate namespace below.

### Draft transition and initialization compatibility

Leave all packaged init templates and 0.1 schemas byte-for-byte unchanged. Users
write reviewed 1.0 files at new explicit paths, e.g.
`experiments/churn/inputs-v1/{experiment.md,search-space.yaml,experiment.yaml}`,
and pass the new configuration path to resolve. References remain root-relative.
This leaves US-02 drafts and its safe reruns intact. No auto-migration command.
Replacing old files manually is possible but init 0.1 may report a preserved
schema conflict on rerun; it must never downgrade them. Installed regressions
cover both separate-file coexistence and this safe conflict. No new init
capability or schema reinterpretation is needed.

### Public commands and Python types

```
agentic-ml plan resolve --project-root ROOT --experiment ROOT_RELATIVE_YAML
agentic-ml plan inspect --project-root ROOT --plan sha256:HEX
agentic-ml plan verify --project-root ROOT --plan sha256:HEX
agentic-ml plan verify --project-root ROOT --plan sha256:HEX --check-current
```

All output is one versioned JSON object on stdout, diagnostics included; concise
human explanation on stderr for nonzero exits, without file content/secrets.
Exit 0 = captured/valid plan with no unresolved decision; exit 2 = malformed,
conflicting, unresolved, unapproved, stale or corrupt input; exit 3 = I/O, lock,
tool or storage-configuration failure; argparse usage errors remain exit 2.
Resolve writes a blocked plan for structurally valid unresolved delegations.
Malformed/conflicting documents produce diagnostics without a final plan.
Explicit-only plans need no approval record, but input readiness
does not authorize execution. In IP2/IP3 proposed delegations are always blocked.

`agentic_ml.planning` exports frozen typed dataclasses `ResolveRequest(project_root:
Path, experiment: Path)`, `PlanResult(plan_id: str | None, status: PlanStatus,
diagnostics: tuple[Diagnostic, ...])`, `PlanInspection`, `VerificationResult`;
`PlanStatus` values `blocked|input_ready`; `Diagnostic` fields `code`, `field`,
`source_path`, `line`, `column`, `message` (line/column nullable for storage errors).
Functions `resolve_plan(request) -> PlanResult`, `inspect_plan(*, project_root,
plan_id) -> PlanInspection`, `verify_plan(*, project_root, plan_id,
check_current=False) -> VerificationResult`. Validation is returned as diagnostics;
operational failures raise typed `PlanningError` with stable code and safe message.
Inspection returns evidence and integrity status, never bypasses verification.
`validate_boundaries(declared: SearchSpace, requested: SearchSelection) ->
BoundaryResult` is the shared public structural checker. Versioned JSON output
mirrors these typed results; enums serialize as their string values.

## T2 — Resolution, paths, identity and preservation

### Precedence and conflict table

| Source | Effective rule | Rejection example |
|---|---|---|
| YAML declared search | Absolute upper boundary, preserved unchanged | Duplicate or empty algorithm map |
| Brief allowed/mode | Narrow YAML algorithm keys; use exactly one; compare all effective keys | Brief adds an algorithm |
| Execution subset | May narrow select pool; must equal brief pool for use/compare | Compare silently drops a member |
| Fixed parameters | Must retain exact type/value in all sources | Change fixed seed or make it tunable |
| Tunable search | May narrow choices/range or fix an allowed value | Widen range, change type/scale, invent parameter |
| Omitted search override | Inherit declared space; omission never adds tunability | Tune a name absent from YAML |
| Budgets | Execution can lower explicit finite ceilings; cannot replace null with a claim of authority | Raise 600 seconds to 601 |
| Brief/config data | Same ordered references after path normalization | Config substitutes another dataset |
| Delegation proposal | Value checked against every bound; remains blocked until approved | Approved choice outside YAML |
| Defaults | Structural inheritance only, provenance recorded | Invent metric, runtime limit or registry default |
| Annotations/guidance | Preserve exact text; no implicit executable interpretation | Unmarked prose outside brief blocks |

Numeric float bounds may use integer endpoints, but integer spaces never narrow
to float; categorical subsets retain exact scalar types. A requested scalar
float value accepts a finite int or float, excluding bool, compared numerically.
Unknown algorithm/parameter in any override fails. Search narrowing cannot add a
new tuning key even if a future registry provides a default. Registry defaults
will be recorded by US-05's execution configuration, not fabricated in this plan.
Null budget ceilings cannot be filled by an execution override; revise the brief
or resolve its delegation. Currency cannot be overridden; a cost ceiling retains
the brief's currency. Trial/runtime ceilings may only decrease; a nullable memory
or cost ceiling may decrease only when already finite. No execution limits are
consumed in US-03.

### Paths and input access

CLI root omitted: walk upward from cwd to nearest directory containing both a
regular `project.yaml` and `.git` directory/file. Stop there; invalid config does
not fall back to a parent. API requires explicit root. Explicit root must be
absolute, existing and canonical, with matching project markers; reject symlink
components supplied in root or selected input paths. Do not invoke Git hooks.
`--experiment` is root-relative, never cwd-relative; reject absolute paths, `..`,
NUL, URI schemes and escapes. Apply this rule to brief/search/notebook/cwd paths.
Normalize `.` and separators to POSIX project-relative strings. Spaces supported.
Notebooks must exist as regular files; record path without opening contents or
starting a kernel. Working directory must exist and be inside root; store it
explicitly, never inferred from notebook location. No `chdir` in the API.

Data references may be root-relative paths or explicit absolute local paths;
store original and normalized absolute reference, `external: true` when outside
root. Do not stat, resolve symlinks, glob or open datasets. No URI credentials,
network discovery or implicit allowlist follows. Future access enforcement must
check actual targets under its authorization; this plan does not certify source
existence. Data references record location, not data-content checksums.

Only project.yaml, selected execution/brief/search, pyproject.toml, uv.lock and
installed harness distribution metadata are opened. No dataset, notebook content,
project module, environment variables, credential store, AGENTS.md or runtime
guidance loader is read. Bounded input reads and descriptor-based no-follow path
validation must fail closed on replacement/race; recheck captured descriptor and
path identities before publication. Project/lock bytes join preserved sources;
installed direct_url metadata identifies full Git SHA when present, otherwise
record wheel provenance explicitly without inventing a Git revision.

### Immutable plan format 1.0

Fixed store `<root>/.agentic-ml/plans/`; no arbitrary output override. Reject
overlap with configured US-02 stores, protected metadata, symlinks, non-directory
ancestors and unsafe destination files before writing. No change to init journal,
DVC/MLflow/state, dependency files or Git. Least privilege is read selected inputs,
create planning directories and write new bundles only. No subprocess is needed for planning or approval. Declaration of source paths authorizes only those
bounded configuration reads and plan writes, never dataset access.

```
.agentic-ml/plans/
  resolve.lock
  .pending-UUID/
  HEX/
    plan.json
    manifest.json
    sources/experiment.md
    sources/search-space.yaml
    sources/experiment.yaml
    sources/project.yaml
    sources/pyproject.toml
    sources/uv.lock
    sources/harness-origin.json
```

`plan.json` contains `schema_version`, `project` (canonical root and project name),
`experiment_id`, `inputs` (logical names, original/root-relative paths, hashes),
`effective` (objective/data/features/evaluation/algorithms/budgets/notebooks/cwd),
`declared_search`, `effective_search`, `decisions` (field path, explicit/delegated/
inherited origin, source line/column, original/proposed/effective value, rationale),
`defaults` (field, value, source or empty), `pending_decisions`, `diagnostics`,
`harness` (package version/origin/full SHA when available), `capabilities`
(`input_resolution` only). Required unavailable delegated values are represented
as pending, never executable defaults. No ready boolean from user inputs.

Serialize JSON deterministically with Python 3.12 `json.dumps(sort_keys=True,
separators=(",", ":"), ensure_ascii=False, allow_nan=False)` plus one LF,
UTF-8; reject duplicate JSON keys on reads. No Unicode normalization. Persist
native finite JSON numbers; checksum identity is byte identity, not mathematical
equivalence. `plan_id = "sha256:" + sha256(plan.json bytes).hexdigest()`.
Store directory is the hex suffix. Manifest lists exact relative filenames,
lengths and SHA-256 for plan and every source. It excludes itself; reject extra
members, links, invalid paths, missing members or duplicate names. Manifest is
canonical too; verify plan id and all hashes independently. Hashes detect damage;
they do not establish authorship or prevent deliberate rewriting. Delegated approvals bind the plan id
and therefore its preserved source hashes. Approval records live separately and
do not create a circular plan hash. Repeated identical resolution reuses the same
verified bundle; source-byte, path, harness or decision changes create a new id.
No timestamps, UUIDs or ephemeral approval status in identity-bearing plan bytes.

Acquire atomic exclusive lock using O_EXCL/no-follow, fail with `plan_busy` rather
than wait or steal. Write private staging directory, flush/fsync files and
directory, validate whole bundle, publish via atomic same-filesystem rename,
then release owned lock. Existing final directory must verify byte-identical;
never replace it. Reader ignores staging. Interrupted writes/stale locks are
reported for explicit operator review; no automatic stale lock deletion. Retain
staging evidence. Concurrent identical requests yield one success and busy/reuse,
different requests never overwrite each other. Strong durability guarantees are
limited to local filesystems supporting these operations; remote stores unsupported.

Verify checks preserved integrity, supported schema, derived decisions/boundaries,
current project-local approval records when required, and never trusts stored readiness.
Default verification describes the preserved configuration; `--check-current`
also compares current selected-source bytes and canonical root to captured
identity, returning `stale_source` on edits/missing files. Downstream execution
must choose this check when consuming current inputs, or materialize and execute
the preserved version under its own authorized restoration path. No automatic
rebinding to live files. Relocating a root produces a new plan; historical bundles
can be inspected but delegated approval is not transferable across projects.
Later consumers must perform their own registry, access, workflow and budget
checks; `input_ready` is never permission to run or proof of scientific validity.

### Components and ownership

Implement `planning/{__init__,models,parsing,boundaries,storage,resolution}.py`;
versioned resources `schemas/planning/1.0/{brief,search-space,experiment,plan,
manifest,result}.json` loaded with importlib.resources. Keep schema/API public
exports typed; internal file layout is routine implementation choice. Approval
module `approvals/{__init__,models,storage,verification}.py` and resources
`schemas/approvals/1.0/{approval,revocation}.json` arrive only in IP4.
CLI dispatch remains `cli/__init__.py`.

US-05 consumes `SearchSpace`, `SearchSelection`, `BoundaryResult` and verified
plan identity, adds registry names/tasks/prediction compatibility, parameter
types/combinations/defaults and candidate checks. It may reject structurally valid
US-03 plans. No US-05 implementation prerequisite was found. Future training
entrypoints must run the shared checker plus US-05 checks for every candidate.

## T3 — Unauthenticated experiment approval records

### Selected mechanism and assurance

Use explicit versioned JSON records in project-associated local storage. No
signatures, key management, authenticated reviewer, protected `/etc` policy,
separate users, approval service or OpenSSH dependency. Any caller with workspace
write access can invoke approval commands. Reviewer is a self-declared label;
record `authentication: none` in every record and verification result involving
approval. No security claim that agent-authored approvals are distinguishable or
prevented. Operational usage expects approval issued by the data scientist; enforcement
checks the presence and scope of a record, not the human behind it.

The proposal remains part of the immutable plan before approval. One approval
covers the complete list of delegated field paths, values and rationales for
that exact plan. Missing proposals, malformed/conflicting plans and choices
outside declared boundaries cannot be made ready by any approval. Approval
records grant no data access, execution permission or whole-story acceptance.

### Payload, storage and public interfaces

Approval schema 1.0 required fields: `schema_version`, `approval_id` (UUID),
`authentication: none`, `reviewer` (nonempty self-declared string), `reason`
(nonempty string), `project_root`, `experiment_id`, `plan_id`,
`purpose: delegated_input_decisions`, `decision: approve`, `decisions` (complete
ordered field/value/rationale list matching proposed delegations), `recorded_at`
(UTC RFC3339 seconds). Generate UUID/time in the harness. Neither field proves
identity or trusted time. Reject unknown/duplicate fields and invalid types using
the strict JSON rules. Canonical JSON serialization is the same as for plans.

Store under `<root>/.agentic-ml/plan-approvals/HEX/`:

```
approval.lock
approvals/APPROVAL_UUID.json
revocations/REVOCATION_UUID.json
```

Each revocation has `schema_version`, `revocation_id`, `authentication: none`,
`approval_id`, exact `project_root`, `experiment_id`, `plan_id`, `reviewer`,
`reason`, `recorded_at`. It references an existing approval for that same bundle.
These ordinary project-local files are excluded from Git by existing
`.agentic-ml` ignore coverage. No dependency on init's configured state store and
no migration of init state. Preserve prior records; normal interfaces append and
never edit them. This is an API convention, not tamper resistance against a
workspace writer.

Public commands:

```
agentic-ml plan approve --project-root ROOT --plan sha256:HEX --reviewer NAME --reason TEXT
agentic-ml plan revoke-approval --project-root ROOT --plan sha256:HEX --approval UUID --reviewer NAME --reason TEXT
```

Invoking either command explicitly records that action; no additional identity
verification or interactive confirmation. Tool-execution permission alone creates
no record. `approve` loads and verifies preserved plan integrity and structural
boundaries, requires every delegation proposal/rationale, derives scope/values
from the preserved plan, then writes the record. It never accepts caller-provided
replacement decisions or approval booleans. No delegations returns a diagnostic
rather than an unnecessary approval. Revocation appends a scoped record after
checking the target approval. New approval after revocation creates a new UUID.
Repeated commands may create multiple records; readiness needs at least one
matching unrevoked approval, and revocation applies to its specified UUID.

`agentic_ml.approvals` exports frozen `ApprovalRequest(project_root: Path,
plan_id: str, reviewer: str, reason: str)`, `RevocationRequest(project_root: Path,
plan_id: str, approval_id: str, reviewer: str, reason: str)`, `ApprovalRecord`,
`RevocationRecord`, and functions `approve_plan(request) -> ApprovalRecord`,
`revoke_approval(request) -> RevocationRecord`. Typed `ApprovalError` carries
stable code/safe message: CLI exit 2 for invalid records/scope and 3 for I/O/lock
failures. Successful commands return versioned JSON on stdout, exit 0. API and
CLI provide equivalent scope and readiness outcomes.

Use descriptor-based no-follow path checks, a per-plan exclusive approval lock,
private staging file, flush/fsync and atomic publication to a new record path.
Readers ignore staging; stale locks require operator review. Publication cannot
replace another record. Readiness snapshots approval/revocation files under the
same lock for cooperating API users; unexpected file replacement during a read
fails verification. These measures address accidental corruption and concurrent
operations, not malicious writes. Reuse existing path/size limits and require
regular files. Preserve records separately from plan.json so approval does not
change the reviewed plan identity.

### Readiness, revocation and failure cases

`verify_plan` and `plan verify` independently recompute preserved checksums and
boundaries, then load current records. A delegated plan is input-ready only with
a schema-valid, matching, unrevoked approval for all proposed decisions. Missing
approval remains blocked. Unknown fields, wrong project/experiment/plan/purpose,
wrong decision/value/rationale, malformed UUID/date or missing referenced approval
block with source-located diagnostics. Malformed final records fail closed;
partial staging is ignored. Default verification uses preserved source bytes;
`--check-current` additionally rejects drift. A changed source, budget, metric,
search boundary or delegation creates a new plan identity needing new approval.
A copied record cannot satisfy a different id/root without being edited.

Revocation blocks that approval's use. Missing approval records also block;
there is no cached ready flag. Deliberate record fabrication, rewriting reviewer
labels or deletion of revocation history cannot be detected reliably without an
external trust boundary. Hashes alone cannot remedy that limitation. Tests must
not imply forgery rejection when a fabricated record exactly matches the public
schema and plan. No authentication or protected storage prerequisite remains for
IP4; ordinary separate experiment-project fixtures are sufficient for the defined
record semantics.

### Historical proposal and deferred hardening

The initial IP1 proposal selected SSH Ed25519 signatures, fixed protected system
policy, signer/experiment OS separation, live revocation policy and a disposable
security host. The developer replaced that proposal under SC-01 before
implementation. The previous OpenSSH capability inspection (9.9p2; sign usage
exit 1) was exploratory, not security evidence, and is no longer a prerequisite.
The superseded design produced no code, keys or provisioned accounts.

Future authenticated approval requires a separate scope decision and design;
future US-23-AC-02 in issue #40 is not delivered by these unauthenticated records.
Issue #40's full body and every comment page were retrieved for this assessment:
zero comments, stable refreshed `updated_at=2026-10-30T03:43:56Z`; its Milestone 5
requirement is retained. No GitHub discussion was changed or published here.

## T4 — Verification matrix and phase handoff

| Criterion | Independent public observations required in later phases |
|---|---|
| US-03-AC-01 | Full classification/regression briefs; every missing/duplicate/unknown field; all three modes; explicit/delegated feature/metric/split/budget values; exact source-located diagnostics |
| US-03-AC-02 | Declared and effective boundary compared to independent expected maps; equality/just-outside bounds, typed categories, boolean rejection, logarithmic positivity, fixed/search overlap, narrowing and forbidden widening through CLI/API |
| US-03-AC-03 | Independently recompute exact source/plan hashes; inspect retained old/new ids; tampered/missing/extra members, partial writes, lock/concurrency; no data/kernel/store side effects |
| US-03-AC-04 | TODO/free prose/duplicates/conflicts fail; proposals block before approval; explicit unauthenticated approval plus wrong root/plan/value, stale/revoked/malformed record failures; readiness independently rechecked; reviewer identity not verified |
| US-03-AC-05 | Root/nested/unrelated cwd and explicit root, paths with spaces; escape/symlink/race rejection; explicit notebook cwd; external data recorded without access |

Use `tests/integration/test_planning.py`, `tests/integration/test_plan_approvals.py`,
`tests/installation/check_planning.py` (isolated `-I` installed probe) and
`tests/installation/verify_planning.py` (both wheel orchestration), wired into
`tests/integration/test_distribution_verification.py`. Extend explicit installed
resource inventory in `tests/packaging/check_installed.py`. Run the installed
probe from an unrelated directory with separate experiment fixtures and direct/
sdist-rebuilt wheels, no source-path imports. Retain US-02 fixtures unchanged.
Approval cases run through `check_planning.py` and `verify_planning.py` on both
wheel paths using ordinary same-user project fixtures. The separate-principal
driver `tests/installation/verify_plan_approvals.py` is removed from current scope
under SC-01; identity-isolation evidence is deferred, not claimed passing. Add each behavior one red–green slice at a time.

IP2 adds all six planning schemas/resources, so its full-suite/distribution trigger
is expected. IP3 runs selected resolver/init/distribution tests plus shared checks,
expanding on trigger. IP4 adds approval-record validation and must run full suite,
both wheel paths, installed record/revocation matrix and shared checks. Runtime
commands are those in the owning plan/development guide; final task IP4-T4 owns
all deferred regressions. No executable acceptance is established here.

IP1 document checks: all changed local Markdown links/anchors and `git diff
--check`; manual walkthrough of each criterion, precedence row, source type,
draft transition, immutable identity and unauthenticated approval limitations. No Python,
schema resource, dependency, lockfile, CI or product test changed. TDD, runtime
tests, distribution rebuilds and shared executable checks do not apply to this
design-only phase.

### Historical IP1 document verification before SC-01

- Local Python Markdown link/heading-ID scan: **40 local links/anchors checked
  across five changed/new Markdown files, zero failures**, exit 0. Remote links
  were excluded; the OpenSSH primary page was retrieved separately.
- `git diff --check`: passed, exit 0. Reviewed the new untracked report separately
  for trailing whitespace because Git diff omits untracked files.
- Manual criterion/precedence/threat walkthrough: every AC maps to later public
  evidence above; deliberate conflict, proposed delegation, dataset path,
  source change, forged approval and missing trust deployment outcomes were
  specified. US-02 preservation and US-05 ownership retained; no scope deviation.
- `git status --short` confirms only the five reported documentation files.
  `uv.lock` SHA-256 remains
  `90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
- No tests, installed wheels, cryptographic success or OS access-denial cases
  were run. Local OpenSSH capability inspection is macOS-only; no new platform
  support is established. Executable verification remains in IP2–IP4.

### SC-01 document verification and review disposition

Revised document verification passed:

- Local Markdown scan: **448 local links/anchors across 10 changed/new files,
  zero errors**, including whitespace inspection of the untracked report.
- `git diff --check`: exit 0.
- Manual requirement consistency review: explicit plan-bound records still
  required by US-03-AC-04; original authenticated proposal marked superseded;
  future US-23-AC-02 preserved; no claim of reviewer authentication or protection
  from fabricated records. No separate-account host prerequisite remains.
- `git diff --name-only -- AGENTS.md .agents .codex docs/development.md uv.lock
  pyproject.toml src tests .github`: empty. Development/test instructions, skills,
  tool permissions, required checks, source, tests and CI were not changed.
  At SC-01 verification the IP1 gate was pending; subsequent approval is recorded below.
- Lock hash unchanged from the historical record above. No GitHub publication.

Runtime/TDD/distribution checks remain inapplicable to this change:
only design, scope and requirement documentation changed; no code, dependencies,
lockfile, tests or existing assertions were modified.

T1–T4 design deliverables reworked for approved SC-01. IP1 gate approved by developer “i approve the changes” (2026-10-31);
no executable criterion claimed passed. No separate-account deployment blocker
remains. Approval authorship and resistance to deliberate history manipulation
are explicitly unverified capabilities deferred beyond this version. General
input schemas/public boundaries are approved. IP2 execution awaits explicit
authorization; no commit/push or whole-story acceptance was requested.
