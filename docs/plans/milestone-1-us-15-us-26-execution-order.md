# M1 / US-15 #21 and US-26 #17: coordinated execution order

Current execution authority: developer explicitly authorized Phase 4 coordination
and committed US-15 source integration into US-26 on 2026-11-14 via thread
01a1db6c-a225-73e0-8796-81a03c4cec7a. US-26 IP4 is Complete and Gate 4 is Approved; [evidence](../verification/us-26-recording-ip4.md) records the real
producer matrix, 361 focused passes, 924 M1–6 passes/1 authorized skip and shared checks. Developer approved Gate 4 and authorized a local combined commit so US-15 can
complete its separately owned dependent verification. No gate approval, publication,
push, sibling edits or cleanup is inferred. Earlier Phase 3-only direction below
is historical and superseded only within this expressly authorized boundary.

## Review status and authority

Coordinated execution record, 2026-11-14. Both Gate 1 and Gate 2 decisions
are Approved. The developer authorized both Phase 3 executions through
coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a. US-26 IP3 is
Complete and Gate 3 is Approved; its owning plan/report hold
the verified task and test records. US-15 retains its independent owning records.
Historical Phase 1/2 and SC-01 decisions remain below and in the owning plans.
At that historical decision, Phase 4/source integration remained unauthorized;
the current authority above supersedes that limit for US-26 IP4 only.

Targets: [US-15 M1 plan](milestone-1-us-15.md)
and [US-26 #17 plan](milestone-1-us-26-recording.md). US-26 owns this index;
the owning plans retain all task, evidence and approval records. Both plans and
this proposed contract must be reviewed together. Plan approval confirms proposed
public test boundaries but does not approve completed implementation or start it.

Both branches start at local `main`, `1a9864a645084af8cfcec580b1db5fa045a67859`.
No fetch/pull or current remote-main comparison was performed. Workspace links now resolve within the authorized combined checkout. Preserve
the independently owned source plans and
reconcile each checkpoint. Do not copy another session's live edits or assume
shared Git objects make its code available in the consumer's branch.

Accepted direction: **US-15-US-26-CONTRACT-01**, recorded in the complete bodies
of [#21](https://github.com/jimthompson5802/agentic-ml/issues/21) and
[#17](https://github.com/jimthompson5802/agentic-ml/issues/17), with decision comments
[6881961026](https://github.com/jimthompson5802/agentic-ml/issues/21#issuecomment-6881961026)
and [6881962234](https://github.com/jimthompson5802/agentic-ml/issues/17#issuecomment-6881962234).
The field/type and API details below are proposals within that accepted direction.
They are not existing exports or new accepted requirements.

## Scope reconciliation and overlap

| Capability or shared surface | Single implementation owner | Other story's use / limit |
|---|---|---|
| Validate supported partition membership and fit training rows | US-15 IP2 | US-26 records supplied evidence; metadata does not prove fit correctness. |
| Produce native fitted Pipeline and plain metadata | US-15 IP3 | US-26 IP3 consumes independently fitted fixture first. No intermediate joblib file. |
| MLflow run, artifacts and shared provenance | US-26 IP2/IP3 | US-15 makes no Git/DVC/MLflow discovery calls. |
| Actual producer-to-consumer installed test | US-26-IP4-T1/T2 | Supplies US-15 AC-03 preservation evidence before US-15 IP4 acceptance. |
| Split schema/source identity | Existing US-12 #19 | Reuse create_partitions and its 1.0 record; project still owns JSON save/load. |
| Dataset identities/storage | Existing US-13 #16 M1 | Use native .dvc pointers and data; restoration is M2. No new DVC wrapper. |
| Toolkit installation identity | Existing US-01/02 and US-41 #64 | Preserve full-SHA Git and retained-wheel contracts. No invented wheel source SHA. |
| Authored feature comparison | US-14 #20 | US-15 supplies fitting, not variant comparison/search. No #20 implementation prerequisite. |
| Baseline/candidate reports and comparisons | US-26 #33, AC-06–09 | #17 records supplied parameters/metrics; it does not compute rankings or accept #33. |
| Reverse result lookup / workflow auditing | US-26 #43, AC-12 / deferred AC-10/11/13 | Stable native run ID in #17 is necessary, not acceptance of #43. |
| Runnable initializer/basic path, full classification and assistant walkthrough | US-39 #58 | Independent small project scripts here; no runner, formal-plan bridge or assistant certification. |
| Restored transformation equivalence | US-15 AC-04, M2 | M1 checks artifact presence/readability only; no M2 replay acceptance. |

No conflict was found between the two issue scopes and active design ownership.
Both issues have null GitHub milestone fields; their bodies assign M1 and
US-15 AC-04 to M2. Their older generic validation wording and milestone-delivery
prose still say current-milestone checks at phase gates. Apply the newer
[2026-11-14 verification policy](../development/verification.md#phase-and-story-verification),
also required by current AGENTS.md: focused behavior/regression evidence plus
shared checks at executable gates; M1–6 at story acceptance. No issue edit is
needed to expand or reduce product criteria. Historical publication draft bodies
under docs/plans/mvp-scope-issues predate CONTRACT-01 and are not current scope.

## Proposed handoff types

Use native objects and ordinary dictionaries, without new public dataclasses,
TypedDict contracts, a feature DSL, a metadata database or run identifiers.
`Json` below means null, bool, str, int, finite float, list[Json] or
dict[str, Json]. JSON numeric values must be finite. Encode the narrow native parameter
sentinels/dtypes below as tagged records; reject other unsupported objects
with field context.
Integers exclude booleans where they represent counts/status codes. Require
exact versioned keys except explicitly variable parameter/library dictionaries.

### Preprocessing record 1.0

| Required key | Exact type / semantics |
|---|---|
| schema_version | str, exactly "1.0" |
| fit_partition | str, exactly "train" |
| partition_record | dict, the existing create_partitions 1.0 record; exact keys schema_version, layout, row_id, target, source, method, settings, protocol, memberships |
| selected_columns | nonempty list[str], unique ordered feature names; excludes row ID and target |
| input_schema | list[{name: str, dtype: str}], actual selected input columns in order |
| output_schema | nonempty list[{name: str, dtype: str}], unique declared output names in order, checked against native training transform width/dtypes |
| pipeline | {class_name: str, parameters: dict[str, Json]}, effective native estimator settings encoded as below |
| versions | dict[str, str], required distribution keys agentic-ml, pandas, pyarrow, scikit-learn |

`partition_record.source` retains row_count:int, schema:list[{name,dtype}],
sha256:bare 64 lowercase hex, identity_format:"pandas-parquet-v1", and its
existing versions dictionary. Do not prefix or rewrite this existing native
serialization identity. Memberships retain ordered homogeneous string/integer IDs,
excluding bool. Layout is train_test or train_validation_test, with its exact
nonempty, disjoint, full-coverage memberships. There is no new split ID or second
membership representation. Source identity plus train membership identifies the
rows consumed; fit correctness also requires the independent numeric tests.

Encode native estimator settings recursively from get_params(deep=False):
an estimator becomes {class_name: fully qualified class str, parameters: map};
lists/tuples become lists; string-keyed maps recurse; ordinary/numpy scalar
booleans, integers and finite floats become corresponding JSON scalars. A numpy
array of supported values becomes a list. Pipeline steps and ColumnTransformer
transformer triples therefore retain their original order/names and effective
settings. Native parameter tags (SC-01, developer accepted 2026-11-14):

- SimpleImputer.missing_values NaN becomes exactly
  {"kind":"missing_value","value":"nan"}; this is the only supported NaN
  parameter context. Other NaN and all infinity values remain invalid.
- Supported numpy scalar type/dtype descriptors become exactly
  {"kind":"numpy_dtype","name":"float64"}, with canonical allowed names
  bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float16,
  float32, float64. Finite scalar instances remain ordinary JSON values.
- These two kind values are reserved in parameter maps. Producer encoding rejects caller-supplied
  literal maps using them. Consumer validation accepts canonical encoded tags
  in supported contexts and rejects malformed/extra tag keys or unsupported
  dtype names; it does not reject all received tag maps.
  The consumer validates/retains tags; no arbitrary import, callable execution
  or new pipeline reconstruction API is introduced. Metrics/provenance numeric
  values remain finite.

No repr/pickle strings masquerade as reproducible settings. Unsupported
callables, opaque objects and cyclic settings fail clearly. Built-in sklearn
imputation/scaling/encoding compose the M1 fixture; custom component compatibility
and callable capture belong to M2/US-16. Do not expand support silently.

### Shared experiment provenance 1.0

`FileRef` is exactly {path:str, sha256:str}; path is normalized project-relative
POSIX syntax, no absolute path, empty component, '.' or '..'; sha256 is
"sha256:" plus 64 lowercase hexadecimal digits. Check file bytes independently.
Code/configuration/lock/DVC metadata FileRefs must match their bytes at the
declared experiment commit as well as the consumed current files. The saved
split file may be DVC-owned rather than a Git blob. Relative paths resolve
against an explicit absolute existing project_root, independently of cwd. Keep
required symlink/path-conflict checks; do not claim OS isolation.

`DvcRef` is exactly {metadata:FileRef, output_path:str, hash_name:str,
hash_value:str, member_path:str|null}. metadata names a committed native .dvc
pointer in this M1 recipe; output_path selects its native output; hash_name/value
match native fields (for example md5 and its .dir identity). member_path names
a file within a directory output, or null for the output itself. Resolve/check
the member through native DVC metadata, not a fabricated SHA-256 DVC ID. Native
dvc.lock stage references can be added when US-27 settles them; they are not an
extra prerequisite here. Data references must include consumed dataset and the
saved split record. No restore/download side effect is performed by logging.

| Required key | Exact type / semantics |
|---|---|
| schema_version | str, "1.0" |
| experiment | {commit_sha:str, entrypoint:FileRef, code:list[FileRef]}; full 40-hex SHA, nonempty code list including entrypoint |
| configuration | {files:list[FileRef], effective:dict[str, Json]}; nonempty committed files list |
| data | nonempty list[DvcRef], with references for consumed dataset and saved split |
| split_record | FileRef for the saved existing partition record; must match preprocessing.partition_record after JSON load |
| environment | {lockfile:FileRef, python_version:str, libraries:dict[str,str]}; uv.lock required, include preprocessing libraries and mlflow/dvc |
| toolkit | {installation:dict[str,str], repository_url:str|null, commit_sha:str|null, build_identity:str|null} |

`toolkit.installation` reuses accepted identities: Git has exactly kind:"git",
name:"agentic-ml", version, url, revision; wheel has kind:"wheel", name,
version, locator, sha256 (bare digest), verification:
"locked-archive-and-installed-payload". Git repository_url/revision agree with
installation url/revision and installed origin. Wheel locator/hash/payload/version
agree with lock and installed origin; source repository metadata may be recorded
if available, full source SHA/build_identity are null unless independently
available. Missing optional distribution source/build information is explicit,
not fabricated and not grounds to reject an otherwise supported wheel.
Package version, lock checksum and installed dependency versions are required.
US-26 may reuse internal identity validation without making its private functions
an experiment interface or changing initializer contracts.

Execution code prepares this provenance once, separately from preprocessing,
and supplies the identical dictionary to both tracking helpers. One
provenance.json per run; identical repeat input reuses it, different content
fails instead of overwriting. This rule is not general retry/durable recovery.

## Proposed public boundaries

Gate 1 approved these names, signatures and public test boundaries before
executable tests. Implementation status belongs to the owning plans. Signature annotations may use Mapping/Sequence internally while outputs
remain plain dictionaries.

- US-15: agentic_ml.preprocessing.fit_preprocessing(frame, *, partition_record,
  pipeline, selected_columns, output_schema, fit_partition="train") ->
  tuple[sklearn.pipeline.Pipeline, dict[str, object]]. Frame is native pandas;
  pipeline is a native sklearn Pipeline of supported transformers. Clone it,
  validate/reconstruct the declared membership through create_partitions supplied
  mode, compare current source identity with the supplied current record, fit only
  selected training columns, and check a training transform against output_schema.
  Project code still parses saved JSON and chooses its old/current identity policy;
  this helper validates the consumed in-memory handoff, not a restoration file API.
  Preserve the original seed/settings record, frames, input pipeline and cwd.
  Reject fit_partition other than train before fit. Output is directly usable
  through native transform on selected validation/test/inference columns.
- US-26: agentic_ml.tracking.log_preprocessing(*, run_id:str, pipeline:Pipeline,
  record:Mapping[str,object], provenance:Mapping[str,object], project_root:Path,
  tracking_uri:str, artifact_path:str="preprocessing") -> dict[str,object].
  Require an existing selected MLflow run; never create/redirect an implicit run.
  Return exactly run_id:str and artifacts:dict[str,str] of native run artifact
  URIs keyed pipeline, metadata, provenance. Validate record/provenance links;
  serialization does not certify training correctness. Leave success lifecycle
  finalization to native MLflow or log_run_results.
- US-26: agentic_ml.tracking.log_run_results(*, run_id:str, project_root:Path,
  tracking_uri:str, provenance:Mapping[str,object], parameters:Mapping[str,Json],
  metrics:Mapping[str,float], outputs:Mapping[str,Path],
  expected_outputs:Sequence[str], process_exit_code:int,
  validation_passed:bool|null, executed_notebook:Path|null=None) -> dict[str,object].
  Record in an existing native run; return exactly run_id:str,
  artifacts:dict[str,str], process_exit_code:int, validation_status:str
  (passed/failed/not_checked). JSON parameter structures are logged with stable
  JSON text using native MLflow parameter semantics, metrics must be finite.
  outputs maps safe unique names to existing files; expected_outputs lists
  required names and cannot be empty. Native run status FINISHED requires zero
  process exit, required outputs present and successful recording. Configured
  validation failure is a separate validation_status tag and can accompany a
  completed process. No quality improvement is inferred. Process/recording/output
  failure sets native FAILED where possible, preserves available logs/artifacts,
  and raises a contextual standard exception; it never returns success.

Both tracking helpers use an explicit client/store, independent of ambient active
run/cwd. Reject unknown/incompatible runs and artifact path conflicts; no overwrite
of another completed artifact. Accepted default layout:

```text
preprocessing/pipeline/     # native MLflow sklearn saved model directory
preprocessing/metadata.json
provenance.json
outputs/<name>/<filename>  # caller-supplied outputs, including available logs
notebooks/executed.ipynb   # only when a notebook was used
```

Use native sklearn model serialization through MLflow, with client artifact
logging to the specified run. US-26 IP1 must verify MLflow 3.17.2's actual
save/log/load behavior and run artifact paths before depending on this layout;
do not accidentally replace it with an unrelated logged-model namespace. Record
MLflow package behavior as feasibility evidence, then refine/review any needed
contract change before code. No standalone joblib handoff or new result database.

US-26 IP1 confirms this layout with save_model plus explicit-client
log_artifacts. Proposed locked configuration is serialization_format="skops",
skops_trusted_types=["numpy.dtype"] for the supported composed M1 fixture.
The default composed save fails on numpy.dtype; the bounded explicit type
configuration passes native save/load. See the [preserved failure and alternate
probe](../verification/us-26-recording-ip1.md). SC-01 adopts this bounded choice; Gate 1 still reviews the renewed evidence
and public boundaries. No automatic pickle/cloudpickle fallback or arbitrary
trust list is permitted.

TypeError/ValueError reject invalid values with field context; missing required
references use FileNotFoundError; existing artifact conflicts use FileExistsError.
Preserve native serialization/storage exception types and cause/context, including
run ID, stage and available artifacts. If diagnostics cannot be logged, retain
local available evidence and report that failure too. No atomic remote rollback,
forced-kill retention or arbitrary code containment is claimed.

Executed notebook input is already executed by project code, not a new toolkit
runner. Validate nbformat structure, preserve output/error cells byte-for-byte
as supplied, and link its committed source notebook in experiment.code. A fresh
kernel test fixture creates a tiny executed notebook using native nbclient;
US-09/39 retain notebook workflow/editor/assistant acceptance.

## Ordered capabilities and developer gates

| Order | Owning phase / tasks | Required prerequisite and evidence | Required gate before dependent work |
|---|---|---|---|
| 1 | Both IP1 contract/feasibility phases | Current issue refresh, proposed fields/boundaries, native feasibility reports | Both Gate 1 approvals; reconcile shared contract once before either IP2 |
| 2a | US-15 IP2, then IP3 | Gate 1; accepted create_partitions; train-only red/green and metadata evidence | US-15 Gate 2 before IP3; Gate 3 exports component capability |
| 2b | US-26 IP2, then IP3 | Gate 1; native run/DVC/Git/wheel fixtures; independently fitted pipeline | US-26 Gate 2 before IP3; Gate 3 before integration |
| 3 | US-26-IP4-T1/T2 | US-15-IP3-T1/T2 and Gate 3, US-26 Gate 3; actual approved producer revision available in tracking branch through separately authorized integration | US-26 Gate 4 after real installed handoff, final checks and #17 acceptance review |
| 4 | US-15-IP4-T1/T2 | US-26-IP4-T1/T2 evidence and Gate 4; actual consumer revision available through separately authorized integration if needed | US-15 Gate 4 / M1 slice acceptance; AC-04 remains M2 |

This is acyclic: US-26 integration needs the approved US-15 component, not final
US-15 slice acceptance. US-15 final acceptance needs integration evidence, not
another producer implementation. Neither plan requires whole-story completion
of US-14/18/20/27/39. In each story use one owning execution session and .venv;
coordinate heavy checks and preserve independent stores/log paths.

## File overlap and integration controls

US-15 owns proposed src/agentic_ml/preprocessing/, tests/integration/test_preprocessing.py,
tests/installation/check_preprocessing.py and docs/preprocessing.md.
US-26 owns proposed src/agentic_ml/tracking/, tests/integration/test_tracking.py,
tests/integration/test_preprocessing_tracking.py, tests/installation/check_tracking.py,
tests/installation/tracking_project.py, tests/installation/verify_tracking.py and
docs/experiment-tracking.md. Public integration tests belong only to US-26.

Likely shared edits are existing tests/installation/verify_assessment_splits.py,
tests/integration/test_distribution_verification.py (US-15 installed probe),
installation identity internals if reuse requires extraction (US-26), root README
links and branch-local CHECKPOINTS.md. No dependency change is expected: sklearn,
MLflow, DVC and nbclient are already runtime dependencies. If pyproject/uv.lock or
shared fixtures must change, coordinate ownership before editing and use scope
management for changed requirements. Preserve existing checks/timeouts/markers.
Integrate US-15's installed-probe registration before US-26 modifies shared build
support, or avoid shared edits with US-26's separate installed driver.

## Shared integration check and acceptance limits

US-26-IP4-T1/T2 owns one test matrix that builds the actual combined reviewed
revision into a direct wheel and a wheel rebuilt from its source distribution.
Each uses separate noneditable environments and experiment projects, runtime
dependencies only, explicit project root and unrelated cwd, isolated MLflow
SQLite/artifact paths and native DVC data/split references. Use the numeric
fixture in the US-15 plan. Invoke actual fit_preprocessing, log_preprocessing
and log_run_results; inspect via MlflowClient and downloaded JSON/model files,
not helper-return assertions alone. Require native pipeline files/metadata/
provenance at the declared paths, exact settings/membership/reference retention,
and independently expected transformed training/validation values before logging.
Download/load as an artifact integrity check; M2 fresh-project restored transform
equivalence and DVC replay remain outside this check. No component fixture alone
closes US-15 AC-03.

Mark new cases by directly verified M1 criteria. Phase checks are focused plus
shared commands; final task in each plan owns M1–6 and deferred-check reconciliation.
Standalone drivers, all-tests -m "" and broader runs need explicit developer
commands. Preserve MVP-M1-ACCEPT-VERIFY, MVP-M2-ACCEPT-VERIFY and historical
M1/M50 verification owners; these two stories do not close them.

## Planning evidence and resume

Full issue snapshots #17/#21/#19/#16/#20/#33/#43/#58/#64, including all comments
and stable final metadata refreshes, are saved locally in each worktree at
.dev-records/verification/20261114-us15-us26-planning/issues.json. #17/#21 each
have two unique comments; #19/#16/#20/#33/#43 one each; #58/#64 zero. No partial
retrieval is being used as a complete discussion. Linked pages/timeline/deleted
comments are outside that export. Historical owning plans establish acceptance
of already merged prerequisites, despite old unchecked issue-body criteria.

Current result: US-26 explicitly concurs with **US-15-US-26-SC-01**;
[consumer renewal and concurrence](../verification/us26-sc01-concurrence.md)
confirm the exact tags, full effective settings and bounded native persistence.
The [producer revision report](../verification/us15-us26-contract-revision.md)
and renewed consumer evidence agree. US-26 IP1-T1/T2/T3 are technically Complete.
US-15's owning session must finalize its own T3/records using this concurrence;
no sibling approval is inferred. Both Gate 1 reviews were subsequently Approved and Phase 2 authorized; see
the decision below. Current component execution/evidence belongs to each owning
plan. No installed producer integration or story acceptance is claimed.

## Gate 1 decision and Phase 2 authority

2026-11-14, developer in coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a: “i approve Gate 1 in both us-15 and
us-26. commit the changes and start phase 2 in both stories”. Both Gate 1
decisions are Approved and both Phase 2 executions authorized. Earlier pending
statements describe the historical handoff and are superseded by this decision.
Each owner records its own gate/tasks; stop at Gate 2 with no push/publication.

## US-26 Phase 2 handoff

US-26's [owning Phase 2 evidence](../verification/us-26-recording-ip2.md) records
component implementation/verification and the final 68-case tracking/DVC
regression pass. Gate 2 is Approved by the later decision below; subsequent Phase 3 authority
is recorded at the end of this index. US-15 keeps its
own task/gate records. Schema 1.0/SC-01, integration ownership and the later
producer-source availability gate remain unchanged.

## Gate 2 approval and local commit

2026-11-14 UTC, developer in coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a: “for both us-15 and us-26 i approve
the phase 2 gate, commit the changes.” Both Gate 2 decisions are Approved.
Each owner records and commits its own Phase 2 changes; no sibling edits or
Phase 3 execution, push/publication, integration or cleanup are authorized.


## Phase 3 execution authorization — 2026-11-14

Developer direction delivered by coordination thread
01a1db6c-a225-73e0-8796-81a03c4cec7a: “have both US-15 and US-26 start Phase 3”.
US-26 starts from approved Gate 2 commit 5f4947f. Its owning plan and
[IP3 evidence](../verification/us-26-recording-ip3.md) own progress and verification.
This authorizes only each story's independent Phase 3. Gate 3 review remains
required. No Phase 4, source integration, push/publication or cleanup is authorized.

US-26 IP3 is technically Complete: 241 tracking/splitting cases pass, with
shared checks and retained failure/correction evidence. Its Gate 3 is Approved;
no actual producer-to-consumer integration or US-15 acceptance is inferred.


## US-26 Gate 3 approval and local commit — 2026-11-14

After both Gate 3 reports, the developer instructed “commit changes in both
stories”. Coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a explicitly
directed the owning US-26 session to record Gate 3 approval and commit Phase 3.
This authorizes the local US-26 approval commit only; US-15 owns its corresponding
record/commit. No Phase 4/source integration, push, publication or cleanup is
authorized. The owning plan/report retain exact approval and verification evidence.

Developer subsequently approved US-26 Gate 4 and local combined commit/handoff:
“I approve us-26 gate 4 and authorize committing the combined revision so us-15 can complete”.
Source: coordination thread 01a1db6c-a225-73e0-8796-81a03c4cec7a, 2026-11-14.
US-15 retains its own Gate 4; no publication or whole-story acceptance is inferred.

On 2026-11-15 the developer explicitly accepted US-26 #17 AC-01–05 and
approved US-15 Gate 4/M1 acceptance; each owning session records its decision.
The shared combined implementation is 3ffc7b4. Only local acceptance commits
and a PR-structure proposal are authorized; publication/history changes wait.
Two independent main-based PRs would duplicate the combined implementation.
The proposal must include both acceptance records without repeating that diff.
