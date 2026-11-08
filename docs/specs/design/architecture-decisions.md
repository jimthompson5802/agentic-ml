# Architecture Decisions

Active design 0.15; [authority](../agentic-ml-harness-design.md).
The [0.14 decision record](architecture-decisions-v0.14-reference.md) preserves
all previous text and accepted bounded contracts. Current scope is defined by
MVP-SC-01/MVP-SC-02 and the approved revised [stories](../user-stories.md).

## ADR-008 — Local experiment MVP and externally owned assistant use

**Scope and design: Accepted**, 2026-11-06. Gates 1–2 approved scope and stories;
Gate 3 approved this supporting design. This accepts scope/design, not unfinished
code or all future interface choices.

Deliver two MVP milestones: complete a local classification experiment, then
validate regression, compatible custom components, saved notebooks and committed-
project reproduction. Assume trusted local code. Keep training-only fitting,
disjoint recorded splits, consistent metrics, declared tuning bounds/trial cap,
separate final testing, MLflow records and native DVC versions/stages/reuse.

The scientist owns the external coding-assistant session; assistant-supported
preparation, invocation, result inspection, validation-based revision and DVC
replay are explicit US-39/40 acceptance scenarios. Record concrete product/
interface/version and verified outputs; no toolkit-managed adapter is required.

MLflow owns run records and fitted artifacts; DVC owns data versions, stage
execution and cache. Toolkit helpers connect them; no general orchestrator,
second workflow database or comprehensive evidence-manifest service is required.

**Consequences:** supersede mandatory runtime experiment gates, hostile-code/OS
isolation, hard runtime/resource/cost quotas, dirty-source replay, durable recovery,
managed agent loops/adapters, acquisition and additional frameworks as MVP
obligations. Preserve explicit strict planning/approval APIs and their limitations.
Toolkit development/testing gates and existing verification obligations are unchanged.
[Rationale and full disposition](../../reviews/mvp-scope-criterion-dispositions.md);
[approval history](../../plans/mvp-scope-revision.md).

## Earlier ADR dispositions

| Record | Current disposition |
|---|---|
| ADR-001 hierarchical closed loops, previously accepted | Accepted history preserved; autonomous inner/outer-loop delivery and mandatory experiment approvals superseded for MVP by ADR-008. Scientist-directed validation iteration remains supported. |
| ADR-002 public API/CLI and adapters, previously pending broadly | Preserve implemented interfaces; new basic-path shape awaits owning story review. Managed adapters/MCP deferred. |
| ADR-003 durable orchestrator, previously pending | Deferred; native DVC executes stages. No workflow store/recovery prerequisite. |
| ADR-004 hybrid sandbox/component framework, previously pending | Native compatible scikit-learn/project functions retained; sandbox, permission and general registry/version protocols deferred. |
| ADR-005 stores, accepted initialization slice and pending broader mechanism | Preserve local DVC/MLflow defaults and setup evidence. Use MLflow/DVC ownership; broader workflow storage deferred. |
| ADR-006 isolation/authorization, previously pending | Trusted local MVP; retain supported input/path checks, defer independently enforced boundaries. Explicit current approval records remain unauthenticated. |
| ADR-007 installation decisions, accepted | Preserve full SHA GitHub install, normal dependency, separate project, CLI `agentic-ml`, import `agentic_ml`, installed resources and lock identity. No PyPI or extra initializer required. |
| US-02 accepted initialization slice | Preserve conflict-safe setup, 0.1 drafts, local stores and journal; US-39-AC-01 adds runnable defaults later. |
| US-03 accepted strict input/approval slice and SC-01 | Preserve 1.0 bundles, readiness/boundaries, scoped unauthenticated approvals and revocations. US-39-AC-02 owns optional basic-path usage, not weakening existing strict APIs. |
| US-05 accepted semantic validation slice | Preserve plan/validation evidence, metadata/defaults and candidate checks. Real training integrations remain open; no runtime boundary is proved by metadata. |

The CLI spelling correction from `agent-ml` to `agentic-ml` stays accepted.
Python 3.12 remains the minimum; additional verified versions/platforms require
their own evidence. Archived examples are not current schema alternatives.

US-41 extends ADR-007 with retained local wheel dependencies, locked artifact
integrity and explicit upgrades alongside existing full-SHA Git pins. IP2/IP3
implement the approved contract; passing final verification and developer
acceptance on 2026-11-08 are tracked in the [M50 plan](../../plans/milestone-50-us-41.md) for
[issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64).
Package-index publication remains outside scope.

## US-41 / ADR-007 extension at Gate 1

**Contract approved at Gate 1 (2026-11-08); implemented in IP2/IP3.** Developer decision:
“i approve ip1; commit changes”. Use retained local purelib wheels
with native locked SHA-256, installed origin/version and independent payload
comparison. Native uv does not record the installed archive hash, even for the
probed hashed direct URL. Do not claim that it does. Gate 1 accepted the
[bounded identity and journal contract](interfaces-and-configuration.md#us-41-wheel-contract-proposed-at-gate-1)
and its inability to distinguish identical payloads in differently encoded ZIPs,
as recorded in the owning plan. URL support is excluded from the first
implementation; local wheels already supply locked integrity without hosting.
Keep the full-SHA Git path, existing public initializer and 0.1 journal. Completed
wheel setups may refresh after explicit native upgrades; incomplete operations
retain identity/checksum recovery guards. Final verification passed and developer
accepted US-41 on 2026-11-08; see the owning plan.
See [IP1 evidence](../../verification/us-41-ip1.md) and
[owning plan](../../plans/milestone-50-us-41.md).

## Deferred assurance register

All eight former blocker/assurance records retain their histories. They block
claims about their future guarantees, not the narrower trusted-code MVP.

| Historical record | Deferred guarantee |
|---|---|
| M1-D1 | OS filesystem/network/credential and source access enforcement |
| M2-D1 | Protected partition/cache/metadata isolation |
| M3-D1 | Evaluator-only final access and restricted feedback delivery |
| M4-D1 | Assistant/tool/workspace/kernel isolation and immutable-code enforcement |
| M4-D2 | First concrete managed adapter product/interface/version certification |
| M5-D1 | Authenticated reviewer/channel/history assurance |
| M5-D2 | Second managed adapter and interchangeability acceptance |
| M6-D1 | Source pricing/resource/retry and acquisition reconciliation |

Current bounded implementation decisions and owners are in the
[blueprint](software-blueprint.md#decisions-required-before-dependent-code).
Developer approval of design scope never supplies missing executable evidence.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](architecture-decisions-v0.14-reference.md).

<a id="14-architecture-decision-records"></a>

<a id="adr-001--hierarchical-closed-loop-ml-development"></a>

<a id="adr-007--github-package-installation-and-project-initialization"></a>

<a id="pending-decisions"></a>

<a id="us-02-ip1--initialization-specific-decision-proposals"></a>

<a id="us-03-ip1--input-resolution-and-delegated-approval-proposals"></a>

<a id="us-05-ip1--semantic-configuration-and-candidate-validation-proposals"></a>
