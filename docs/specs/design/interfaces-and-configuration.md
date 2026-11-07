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

The project owns extraction/custom transformers/estimators and notebooks. Use
pandas DataFrames and project pandas functions for extraction and authored
features, with plain dictionaries for extraction settings/metadata. Avoid
toolkit-specific tabular/request/operation classes. Use
native compatible scikit-learn objects and project functions; no general plugin
registration, framework adapter or FeaturePlan language is required for the MVP.
Validate supported estimator parameters and prediction compatibility through the
toolkit path; this cannot constrain arbitrary code outside that path.

## Existing public interfaces

The currently implemented families are initialization, planning, approvals and
validation, listed with all exports in [the blueprint](software-blueprint.md#existing-public-contracts).
The existing guides describe actual commands:
[setup](../../experiment-setup.md) and [configuration validation](../../configuration-validation.md).

Initialization creates 0.1 draft inputs and project/storage scaffolding. Strict
planning uses separately supplied 1.0 inputs and immutable plan bundles.
Existing validation binds to those plan/validation identities. Current CLI
families are `init`, `plan resolve/inspect/verify/approve/revoke-approval`,
`config validate/inspect`, and `candidate validate`, plus `--version`.
These are not training or notebook-run commands.

Dataset-content checks are a separate proposed public boundary under
[US-12 issue #15's quality contract](../../data-quality.md). IP1 has selected
function/report/rule shapes, approved by developer “i approve ip1; commit” at
Gate 1 on 2026-11-07 UTC. The API is implemented with Gate 2 approval; IP3 installed checks pass;
Gate 3 is approved; issue #15 AC-01/05 accepted on 2026-11-07 UTC. Existing plan-bound validation exports are
unchanged by this proposal.

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
[US-11 contract revision](../../extraction.md) is proposed component design,
not a delivered basic-run API or acceptance of downstream feature stories.

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
