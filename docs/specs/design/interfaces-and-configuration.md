# Interfaces and Configuration

Active design 0.15; see the [authority/reading map](../agentic-ml-harness-design.md).
[Stories](../user-stories.md) define required behavior; the
[blueprint](software-blueprint.md) owns implemented API status and future seams.

## Installed project boundary

Use Python 3.12+, uv and the committed lockfile. Install the normal toolkit
dependency at a full Git SHA or from a supported retained local wheel into a
separate experiment project. Preserve
`agentic-ml` as CLI and `agentic_ml` as import name. Source imports or paths into
a neighboring toolkit checkout are not experiment interfaces. Load shipped
templates/runtime resources with installed-package resource APIs.

Distribution-based initialization is implemented under
[US-41](../user-stories.md#us-41-initialize-experiments-from-a-package-distribution)
in M50, owned by [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64).
The supported form is a retained local purelib wheel, with native locked SHA-256,
installed origin/version and independent payload comparison as specified below.
Full-SHA Git dependencies remain supported. Passing final verification and developer acceptance on 2026-11-08 are tracked in the [plan](../../plans/milestone-50-us-41.md);
package-index publication is outside US-41.

The project owns extraction/custom transformers/estimators and notebooks. Use
pandas DataFrames and project pandas functions for extraction and authored
features, with plain dictionaries for extraction settings/metadata. Avoid
toolkit-specific tabular/request/operation classes. Use
native compatible scikit-learn objects and project functions; no general plugin
registration, framework adapter or FeaturePlan language is required for the MVP.
Validate supported estimator parameters and prediction compatibility through the
toolkit path; this cannot constrain arbitrary code outside that path.

Assessment and partitioning reuse native pandas descriptive outputs and
scikit-learn split APIs. Developer selected `assess_data` and `create_partitions`
as the only new helpers under US-12-19-SC-03. Developer “i approve ip1; commit
changes”, 2026-11-07 UTC, confirmed exact contracts/test boundaries at Gate 1;
IP2/IP3 implemented both helpers, and IP4 verified both installed wheel paths.
Gates 1–4 are approved; developer “i accept issue #19”, 2026-11-08 UTC, accepted
AC-02/03 and both layouts. See the [final IP4 evidence](../../verification/us-12-19-ip4.md).
Project code owns JSON save/load and any
saved-source comparison. No toolkit record read/write interface is included.
Supplied mode validates selected loaded layout/membership against the current
frame, without providing a saved-file parser or full restoration guarantee. See
[native capability reuse and approved integration](data-and-features.md#reuse-existing-assessment-and-partition-capabilities).

### US-41 wheel contract proposed at Gate 1

**Status:** Contract approved at Gate 1 on 2026-11-08; implemented in IP2/IP3.
IP4 verification passed; Gates 1–4 Approved. Developer accepted US-41 on
2026-11-08 (“i accept the story”); see the owning plan.
Developer decision: “i approve ip1; commit changes”. Native uv 0.13.6
feasibility evidence and limitations are in [IP1 evidence](../../verification/us-41-ip1.md).

Support one unconditional, extra-free `agentic-ml` dependency and one
`tool.uv.sources` entry whose normalized name is `agentic-ml`, with exactly
`{ path = "../artifacts/agentic_ml-1.0.0-py3-none-any.whl" }`.
Normalize names by lowercasing and collapsing runs of `-`, `_`, `.` to `-`;
reject duplicate normalized declarations/source keys, markers, source lists,
editable/directory/sdist, registry and URL wheel forms in this first contract.
The existing full-SHA Git branch retains its accepted forms and diagnostics.
Resolve relative wheel paths against the explicit experiment root, never cwd;
absolute local paths are allowed. Require a readable regular wheel retained at
that location. Reject symlink components using existing path checks.

Native uv output for that declaration is:

```toml
[[package]]
name = "agentic-ml"
version = "1.0.0"
source = { path = "../artifacts/agentic_ml-1.0.0-py3-none-any.whl" }
wheels = [
  { filename = "agentic_ml-1.0.0-py3-none-any.whl", hash = "sha256:<64 lowercase hex digits>" },
]
```

Require exactly one normalized toolkit lock package and one wheel; resolve its
source path against root and compare the resolved locator. Match filename,
wheel METADATA Name/Version, lock name/version and installed Name/Version.
Compare versions using PEP 440 semantics (reuse runtime `packaging` intentionally;
if imported by product code, declare it directly and review the lock in IP2).
Validate SHA-256 syntax and independently hash retained archive bytes against the
lock. Installed metadata must be in the selected root's `.venv`, with a matching
canonical `file:` URL in `direct_url.json`, `archive_info` present, no VCS or
editable/directory metadata, and no duplicate installed toolkit distribution.
If installed `archive_info.hashes.sha256` or legacy `hash` exists, it must agree;
malformed or contradictory hash metadata fails. uv 0.13.6 emits an empty
`archive_info`, so absence alone cannot be treated as evidence of a matching hash.

For uv's empty archive hash, compare installed wheel payload bytes with the
independently hash-verified retained wheel. Use the wheel's root-purelib layout:
reject unsafe/duplicate archive paths, links, `.data` relocation and non-purelib
wheels for this bounded contract. Compare all regular wheel members except its
`.dist-info/RECORD` (rewritten by installers); installer-generated entrypoints,
bytecode and added metadata are outside this comparison. Do not use the installed
RECORD as the expected digest source. Toolkit wheels are purelib; IP4 must verify
actual direct/rebuilt wheels, not infer this from the synthetic probe.
This establishes current payload/origin consistency with the locked artifact,
not proof that the originally installed ZIP had the identical archive digest.
Two archives with identical payload but different ZIP encoding cannot be
separated by this check. Developer accepted this limitation at Gate 1 on 2026-11-08. No companion integrity
file or fabricated installed archive hash is proposed. Missing original wheel
bytes fail with instructions to restore the locked wheel; no network fallback.

Identity validation runs before writable probes, scaffold/journal/backups/locks
or store changes. Errors use existing InitializationError/CLI diagnostics naming
the failed declaration, lock, install or wheel check and recovery: restore the
reviewed artifact and run native locked synchronization, or deliberately select
a new artifact. Initialization must not repair inconsistent input automatically.
Snapshot rejected inputs after fixture damage and invoke installed entrypoints
directly, so uv cannot repair metadata before the check.

Retain setup journal `schema_version = "0.1"`. Add optional
`environment.toolkit_identity` with `kind = "wheel"`, normalized `name`, canonical
`version`, resolved file `locator`, `sha256` (bare lowercase hex), and
`verification = "locked-archive-and-installed-payload"`. Git identity uses
`kind = "git"`, `name`, `version`, `url`, `revision`; preserve existing Git journal
fields/checksum behavior. Legacy complete Git journals without the additive
identity are validated against current Git inputs before populating it. Reject
unknown discriminators or malformed existing identity; do not rewrite unrelated
strict planning records. Initial/incomplete operations must record the selected
identity before writes and retain it through retries.

A completed journal means `status == "complete"`, empty `pending_steps`, all
required steps including `finalize` completed, and verified environment; other
states are incomplete. For incomplete setup, require unchanged recorded identity
and environment checksums before any retry writes, including the interval after
environment verification but before storage completion. Preserve legacy
scaffold-resume checks when environment evidence does not yet exist; never infer
an upgrade from partial work. Legacy Git incomplete journals retain their existing
checksum/recovery safeguards and cannot switch source kinds during recovery.

Explicit upgrade is native `uv add /reviewed/new/agentic_ml-V-py3-none-any.whl`,
then `uv sync --locked`, then installed init. Both new-version and same-version
new-locator/new-digest transitions are supported. A fully complete prior wheel
journal may refresh identity after all current identity, project/file/storage
compatibility checks pass; keep original backups, custom compatible files and
stores. Do not claim rollback of native installer changes or a failed sync.
A source-kind switch from a recorded Git identity to wheel (or reverse) is outside
this upgrade contract and fails with recovery guidance. Ordinary init must retain
the current declaration/locator/hash through its lock/sync stages; compare identity
after locking and after installed synchronization, before downstream store writes.
Ordinary init and `uv sync --locked` select no newer artifact automatically.

## Existing public interfaces

The currently implemented families are initialization, planning, approvals,
metadata/candidate validation, extraction, data quality, assessment and partitions,
listed with all exports in [the blueprint](software-blueprint.md#existing-public-contracts).
The guides describe actual commands and Python interfaces:
[setup](../../experiment-setup.md), [configuration validation](../../configuration-validation.md),
[extraction](../../extraction.md), [quality](../../data-quality.md) and
[assessment/partitions](../../data-assessment-and-splits.md).

Initialization creates 0.1 draft inputs and project/storage scaffolding. Strict
planning uses separately supplied 1.0 inputs and immutable plan bundles.
Existing validation binds to those plan/validation identities. Current CLI
families are `init`, `plan resolve/inspect/verify/approve/revoke-approval`,
`config validate/inspect`, and `candidate validate`, plus `--version`.
These are not training or notebook-run commands.

Dataset-content checks are implemented separately from plan-bound metadata
validation under [US-12 issue #15's quality contract](../../data-quality.md).
Gates 1–3 and AC-01/05 were accepted on 2026-11-07 UTC. The Python APIs accept
DataFrames and explicit rules without plan IDs. Required failures block the
operation passed to `run_validated_step`; advisory failures and explicit empty
rules permit it. Empty rules record `not_checked`. Future experiment entrypoints
still need their own integration. Existing plan-bound validation exports retain
their strict contracts.

Preserve their accepted request/result shapes, integrity/currentness checks,
conflict handling, recorded defaults, revocation/staleness rules and diagnostics.
Formal plan approval remains required when using the explicit delegated-decision
path; the revised MVP does not silently alter that existing API.

## Proposed basic experiment path

US-39-AC-01/02 require runnable initialization defaults and validated explicit
settings without mandatory formal plans or experiment approvals. This is new
behavior. The future interface must bridge the draft/strict-contract difference
without changing existing APIs or fabricating plan IDs/validation evidence.

Before implementation, the owning story plan must settle the public basic-path
entrypoint/configuration and its reuse of validation, review compatibility and
confirm public test boundaries. This document deliberately does not invent a
`run` verb, wire schema or new request class. Do not call existing plan-bound
validation with an invalid or absent plan.

Required experiment information: local data/extraction settings, target/task,
feature/preprocessing selection, split seed or supplied partitions, metric and
direction, selected estimators, fixed/search parameters and maximum trial count.
Record effective values and library/environment references. Missing/ambiguous
required settings or invalid candidates must fail before affected training.
Extraction settings feed ordinary project pandas code; no proprietary
predicate/join configuration language is required. The
[US-11 extraction contract](../../extraction.md) is implemented and accepted;
the basic-run API and downstream fitted feature behavior remain future work.

## Paths, customization and notebooks

Resolve experiment inputs against the explicit project root and record execution
working directories. Native DVC stage dependencies/outputs follow their declared
working-directory semantics; examples must be consistent. Ordinary invalid paths
and unsafe initialization destinations still fail; trusted-code scope does not
remove existing conflict/symlink checks.

Project transformers/estimators must satisfy supported scikit-learn interfaces.
Preserve fitted state with the model/pipeline; inspect compatible output shapes
and parameters through the supported path. General component versions,
modification permissions and hostile serialized-model isolation are deferred.

M2 saved notebooks use the project environment, explicit inputs and a fresh kernel
in saved cell order. Preserve executed outputs/errors and use artifact references
across notebooks. Editor installation is separate; no toolkit-owned interactive
kernel/assistant process is required. Tests must not depend on hidden state.

## Runtime guidance and assistant use

The scientist owns the external coding-assistant session. It uses documented
public interfaces and native DVC and edits project files. Developer instructions
for this toolkit stay separate from packaged experiment-use guidance.

Current resources remain shipped and loadable. A versioned task-specific guidance
loader, conflict governance, complete assistant-context capture and managed
delivery are roadmap capabilities. Changes to existing packaged resources still
need installed-resource verification; this design does not alter the resources.
Concrete assistant acceptance is manual evidence under US-39/40, not adapter
certification. See the [walkthrough](../example-walkthrough.md).

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/interfaces-and-configuration.md).

<a id="8-interfaces-and-contracts"></a>

<a id="contributor-development-and-package-verification-milestone-0"></a>

<a id="pytorch-checkpoint-restoration"></a>

<a id="primary-contracts"></a>

<a id="submission-identity-and-recovery-contracts"></a>

<a id="user-supplied-ml-components"></a>

<a id="projectyaml"></a>

<a id="search-spaceyaml"></a>

<a id="experimentyaml--additional-fields"></a>

<a id="project-initialization-and-installation"></a>

<a id="after-installing-uv-and-git"></a>

<a id="open-this-project-in-vs-code-and-select-its-venv-notebook-kernel"></a>

<a id="developer-experiment-inputs"></a>

<a id="experiment-predict-customer-churn"></a>

<a id="data"></a>

<a id="features"></a>

<a id="evaluation"></a>

<a id="algorithms"></a>

<a id="budget"></a>

<a id="development-and-runtime-agent-instructions"></a>

<a id="algorithm-and-hyperparameter-configuration"></a>

<a id="resolved-experiment-example"></a>
