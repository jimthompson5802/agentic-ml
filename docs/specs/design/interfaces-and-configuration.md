# Interfaces and Configuration

Active design 0.15; see the [authority/reading map](../agentic-ml-harness-design.md).
[Stories](../user-stories.md) define required behavior; the
[blueprint](software-blueprint.md) owns implemented API status and future seams.

## Installed project boundary

Use Python 3.12+, uv and the committed lockfile. Install the normal toolkit
dependency at a full Git SHA into a separate experiment project. Preserve
`agentic-ml` as CLI and `agentic_ml` as import name. Source imports or paths into
a neighboring toolkit checkout are not experiment interfaces. Load shipped
templates/runtime resources with installed-package resource APIs.

Distribution-based initialization is planned under
[US-41](../user-stories.md#us-41-initialize-experiments-from-a-package-distribution)
in M50, owned by [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64).
It remains unimplemented. Current initialization still requires matching Git-origin metadata and a
full-SHA dependency pin. US-33's wheel build/import checks do not establish
distribution-origin initialization support; package-index publication is outside US-41.

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
