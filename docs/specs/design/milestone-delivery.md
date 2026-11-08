# Milestone Delivery

Active design 0.15. [Stories](../user-stories.md) define required outcomes;
[migration](../../plans/mvp-scope-story-migration.md) records old assignments and
retained/deferred clauses. The revised MVP issues were synchronized through
PR #57's publication workflow; future scope changes still require synchronization.

## Delivery outcomes and exits

| Milestone | Required outcome and exit |
|---|---|
| M0 accepted foundation | Retain US-31–33 evidence and contributor/package checks; no reopened acceptance. |
| M1 complete one experiment | Separate installed project completes local classification extraction, quality/split checks, training-only features, baseline, bounded tuning, selected-model final testing, MLflow results and actual native DVC stage execution. US-39-AC-01–08 demonstrate scientist-directed assistant use and one validation-based revision. |
| M2 validate usability/reproduction | Add regression, compatible project components, fresh-kernel saved notebook, restored fitted state and clean committed-project DVC reproduction including reuse/invalidation/missing-corrupt failures. US-39-AC-09–11 and US-40-AC-01–07 complete ASW-07/08. MVP ends here. |
| M50 | Accepted US-35/36 tooling plus US-37/38 local backlog and unimplemented US-41 distribution-based initialization ([issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64)); independent verification obligations preserved. |
| M99 | US-34 contribution/review checks remain deferred; roadmap platform scope is not silently added here. |

M1 advances US-18-AC-01 classification; M2 regression completes the criterion.
Repeated story slices have unique acceptance IDs. Feature comparison/model
training move into the first useful experiment rather than waiting for old M2/M3.

## Capability order and owning stories

1. Reuse accepted installation/setup/planning/validation; settle runnable basic
   path compatibility under US-39-AC-01/02 without breaking strict APIs.
2. Reuse accepted US-11 extraction and US-12 quality/assessment/partitions; add
   DVC data metadata under US-13 and integrated use under US-39.
3. Fit native pipelines/baselines and compare authored features: US-14/15/18.
4. Add validated bounded search, evaluation/final-test step and MLflow links:
   US-10/20/21/24/26, with staged US-05 training integration.
5. Declare/run native DVC stages under US-27 and demonstrate US-39 M1.
6. Add US-09/16 and M2 slices for regression/restored state; complete US-40 replay.

Detailed story plans must identify public interfaces, prerequisite slices, TDD
checks and developer gates. US-39 coordinates integration; component stories own
their implementation tasks. Do not require unrelated roadmap story completion.

## Verification and acceptance ownership

Follow the existing [verification policy](../../development/verification.md#phase-and-story-verification):
current milestone at executable phase gates, M1–6 at story acceptance, broader/
standalone artifact checks only on explicit developer command. This documentation
revision changes no test markers, timeouts, skips or platform claims.

Later execution plans must name `MVP-M1-ACCEPT-VERIFY` and
`MVP-M2-ACCEPT-VERIFY` owners to reconcile revised criteria, real artifacts,
assistant/manual demonstrations, platform limits and deferred checks at milestone
acceptance. These proposed owners do not replace or close historical
`M1-ACCEPT-VERIFY` or independent `M50-ACCEPT-VERIFY`. Existing owning plans
retain their obligations until an explicit recorded revision resolves them.
A renumbered milestone or narrower product scope does not silently waive prior checks.

## Uncommitted roadmap

Historical M3 framework/GPU breadth, M4 managed agents, M5 durable orchestration
and M6 acquisition are no longer scheduled MVP increments. Their original
requirements and approvals remain in [scope history](../../reviews/mvp-scope-criterion-dispositions.md)
and the [0.14 blueprint](software-blueprint-v0.14-reference.md).
Stronger authorization/isolation, comprehensive source capture/replay, registries
and hard quotas are also deferred. Activation requires an explicit owning issue/
plan scope decision and evidence for the claimed guarantee.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/milestone-delivery.md).

<a id="11-milestone-delivery-plan"></a>

<a id="milestone-0-dependencies-and-delivery-order"></a>

<a id="milestone-1-dependencies-and-delivery-order"></a>

<a id="deferred-enhancements"></a>
