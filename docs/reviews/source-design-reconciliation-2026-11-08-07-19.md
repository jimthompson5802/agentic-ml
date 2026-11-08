# Source and MVP design reconciliation

## Baseline and authority

Created: 2026-11-08 07:19 EST.
Baseline: `49292dffe979b57de9f813cf66db5cd74cc1b18b` on `reconcile-design`; working tree was clean before this reconciliation.
The developer requested the proposed changes before edits and then authorized
application with “ok make the changes”. This is a documentation correction,
not a product implementation phase or a new story acceptance.

[Active design](../specs/agentic-ml-harness-design.md) and its eight reading-map
[topic documents](../specs/design/software-blueprint.md), plus the
[walkthrough](../specs/example-walkthrough.md), were reconciled against public
interfaces and relevant implementations in `src/agentic_ml/`. Supporting guides:
[extraction](../extraction.md), [quality](../data-quality.md) and
[assessment/partitions](../data-assessment-and-splits.md).

[Local stories](../specs/user-stories.md) define MVP delivery/criteria; GitHub issues
govern implementation scope; owning plans/evidence establish recorded acceptance.
The prior review retrieved complete issue bodies and paginated comments for
[#14](https://github.com/jimthompson5802/agentic-ml/issues/14),
[#15](https://github.com/jimthompson5802/agentic-ml/issues/15),
[#19](https://github.com/jimthompson5802/agentic-ml/issues/19),
[#58](https://github.com/jimthompson5802/agentic-ml/issues/58) and
[#59](https://github.com/jimthompson5802/agentic-ml/issues/59).
Unique comment counts were 1/1/1/0/0; all metadata-refresh completeness checks
passed. The first three are closed, integration issues remain open. Their earlier
scope-only issue bodies/unchecked boxes are not new acceptance records; use the
[US-11 plan](../plans/milestone-1-us-11.md#story-completion-review),
[quality plan](../plans/milestone-1-us-12.md) and
[assessment/split plan](../plans/milestone-1-us-12-assessment-splits.md#story-completion-review)
for developer acceptance and evidence.

The review covers implemented public behavior descriptions and future MVP scope.
It does not execute package code or certify every private implementation, numerical
outcome, contributor tool, platform or historical criterion. Historical 0.14
catalogues, previous approvals and evidence remain preserved; their deferred
platform designs are not current MVP requirements. Linked plans/reports supply
supporting acceptance context; this is not an exhaustive audit of every document
reachable recursively from their links.

## Findings and applied corrections

All findings below are resolved in the current documentation working tree.
References identify the corrected sections and source evidence where applicable.

| ID / severity | Discrepancy, consequence and correction | Requirement / source evidence | Target |
|---|---|---|---|
| R1 / Medium | Delivered data capabilities were still described as proposed or pending, obscuring the available integration surface. Mark accepted components implemented and list current imports. | US-11 AC-01–05; US-12 AC-01/02/03/05; [extraction source](../../src/agentic_ml/extraction/__init__.py), [quality source](../../src/agentic_ml/data_quality/__init__.py), [assessment source](../../src/agentic_ml/data_assessment/__init__.py), [partition source](../../src/agentic_ml/splitting/__init__.py) | [Overview status](../specs/agentic-ml-harness-design.md#implementation-status-and-next-work), [blueprint](../specs/design/software-blueprint.md#existing-public-contracts), interfaces, layout, walkthrough and current guide summaries |
| R2 / Medium | Planned-work tables mixed delivered helpers with unfinished end-to-end behavior. Distinguish accepted components from future runner, fitted preprocessing, tracking and DVC integration; extraction provides checksums, not real DVC IDs. | US-11-AC-04; US-13/14/15/26/27/39; [publication source](../../src/agentic_ml/extraction/provenance.py) | [Planned seams](../specs/design/software-blueprint.md#planned-mvp-responsibilities), [data design](../specs/design/data-and-features.md#local-extraction-and-quality) |
| R3 / Medium | Saved-record/time-group wording could imply toolkit restoration or protocol certification. Assign persistence, saved-document checks and old/current identity comparison to project code; document membership checks and declared protocols only. | US-12-AC-03; SC-03; [partition source](../../src/agentic_ml/splitting/__init__.py), [implemented contract](../data-assessment-and-splits.md#source-identity-and-record) | [Partitions](../specs/design/data-and-features.md#reproducible-partitions), blueprint, interfaces and walkthrough |
| R4 / Medium | Traceability marked accepted extraction/quality work planned and described assessment/partitions as proving train-only fitting. Record criterion-specific evidence and retain future consumer obligations. | US-11 AC-01–05; US-12 AC-01/02/03/05; US-15; accepted owning plans above | [Criterion index](../specs/design/acceptance-traceability.md#criterion-to-design-index) |
| R5 / Medium | US-05-AC-05 was labeled accepted even though training-path integration is unfinished. Mark that criterion pending while preserving accepted metadata APIs. | US-05-AC-05; [validation source](../../src/agentic_ml/validation/configuration.py) | [Criterion index](../specs/design/acceptance-traceability.md#criterion-to-design-index) |
| R6 / Medium | Six deferred US-41 criteria were absent from a purported complete 222-criterion inventory. Add M99 rows and distinguish wheel build verification from distribution-origin initialization. Total is 228. | US-41 AC-01–06; [current Git-origin preflight](../../src/agentic_ml/initialization/preflight.py); [local story](../specs/user-stories.md#us-41-initialize-experiments-from-a-package-distribution) | Traceability, blueprint count, [installed boundary](../specs/design/interfaces-and-configuration.md#installed-project-boundary), milestone delivery and ADR note |
| R7 / Low | Seeded three-way composition remained an open design choice despite accepted implementation. Document test-first reservation, adjusted validation fraction, same seed/flags, native rounding and version-bound identity. | US-12-AC-03; [partition source](../../src/agentic_ml/splitting/__init__.py) | [Partitions](../specs/design/data-and-features.md#reproducible-partitions) |
| R8 / Low | Current summaries retained outdated gate/publication language. Refresh current summaries and links without rewriting historical scope/evidence records. | US-11/12 acceptance; MVP scope publication; no new executable acceptance | Main design, milestone delivery, extraction/quality/assessment guides |

## Scope disposition and decisions

M1 still requires a complete local classification experiment: training-only
preprocessing, baseline, bounded tuning, separate final testing, MLflow records,
native DVC stages and ASW-01–06 assistant evidence. M2 adds regression, compatible
project components, saved notebooks and committed-project reproduction including
cache/invalidation/fitted-state checks and ASW-07/08. MVP ends at M2.

Each active responsibility is requirement-backed or a supporting implementation
detail: native pandas/partition helpers implement US-11/12; native pipelines/search
support US-14/15/16/18/20; local execution/evaluation supports US-10/21/24;
MLflow/Git identity links support US-26; native DVC supports US-13/27/40;
notebook/external-assistant use supports US-09/39/40. Their detailed future API
shapes remain subject to owning contract reviews. No new product requirement was
introduced to make the design more concrete.

Managed agents, mandatory experiment approvals, OS isolation, hard quotas,
durable orchestration, dirty-source replay, acquisition and additional frameworks
remain deferred. Explicit strict plan/approval APIs and historical verification
obligations remain intact. M0/M50 contributor requirements remain separate;
M99 contains US-34 and local-only US-41. Historical designs retain their statuses
as history, without expanding MVP delivery.

No unresolved scope conflict prevents these documentation corrections. The
[existing implementation decisions](../specs/design/software-blueprint.md#decisions-required-before-dependent-code)
remain open: basic-path entrypoint/validation bridge, real estimator inventory and
custom persistence, and example output tolerances/fitted-state format. This review
does not settle them or authorize code. US-41 still needs GitHub synchronization
before implementation; no issue was published by this work.

## Criterion coverage matrix

One row per local criterion follows. “Supported” means a compatible design or
explicit deferral within this reconciliation's scope; it does not mean executable
implementation or renewed verification. The delivery/evidence columns preserve the
accepted/planned/deferred distinction from the corrected active index. Deferred
criteria are accounted for as future scope, not accepted product guarantees.

| Criterion | Delivery / implementation status | Supporting design or contract | Design coverage | Finding | Evidence boundary |
|---|---|---|---|---|---|
| [US-31-AC-01](../specs/user-stories.md#us-31-ac-01) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-02](../specs/user-stories.md#us-31-ac-02) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-03](../specs/user-stories.md#us-31-ac-03) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-04](../specs/user-stories.md#us-31-ac-04) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-05](../specs/user-stories.md#us-31-ac-05) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-06](../specs/user-stories.md#us-31-ac-06) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-07](../specs/user-stories.md#us-31-ac-07) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-08](../specs/user-stories.md#us-31-ac-08) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-09](../specs/user-stories.md#us-31-ac-09) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-31-AC-10](../specs/user-stories.md#us-31-ac-10) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted contributor setup and verified environment evidence |
| [US-32-AC-01](../specs/user-stories.md#us-32-ac-01) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted CI and shared contributor checks |
| [US-32-AC-02](../specs/user-stories.md#us-32-ac-02) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted CI and shared contributor checks |
| [US-32-AC-03](../specs/user-stories.md#us-32-ac-03) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted CI and shared contributor checks |
| [US-32-AC-04](../specs/user-stories.md#us-32-ac-04) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted CI and shared contributor checks |
| [US-33-AC-01](../specs/user-stories.md#us-33-ac-01) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-02](../specs/user-stories.md#us-33-ac-02) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-03](../specs/user-stories.md#us-33-ac-03) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-04](../specs/user-stories.md#us-33-ac-04) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-05](../specs/user-stories.md#us-33-ac-05) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-06](../specs/user-stories.md#us-33-ac-06) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-33-AC-07](../specs/user-stories.md#us-33-ac-07) | M0; accepted slice | [Contract](../development.md) | Supported | — | Accepted installed wheel/source resources/version checks |
| [US-01-AC-01](../specs/user-stories.md#us-01-ac-01) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#existing-public-contracts) | Supported | — | Pinned installation/upgrade and installed resources |
| [US-01-AC-02](../specs/user-stories.md#us-01-ac-02) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#existing-public-contracts) | Supported | — | Pinned installation/upgrade and installed resources |
| [US-01-AC-03](../specs/user-stories.md#us-01-ac-03) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#existing-public-contracts) | Supported | — | Pinned installation/upgrade and installed resources |
| [US-01-AC-04](../specs/user-stories.md#us-01-ac-04) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#existing-public-contracts) | Supported | — | Pinned installation/upgrade and installed resources |
| [US-02-AC-01](../specs/user-stories.md#us-02-ac-01) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#initialization-and-paths) | Supported | — | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-02](../specs/user-stories.md#us-02-ac-02) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#initialization-and-paths) | Supported | — | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-03](../specs/user-stories.md#us-02-ac-03) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#initialization-and-paths) | Supported | — | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-04](../specs/user-stories.md#us-02-ac-04) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#initialization-and-paths) | Supported | — | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-05](../specs/user-stories.md#us-02-ac-05) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#initialization-and-paths) | Supported | — | Conflict-safe setup and draft/default compatibility |
| [US-03-AC-01](../specs/user-stories.md#us-03-ac-01) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#strict-planning-and-approvals) | Supported | — | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-02](../specs/user-stories.md#us-03-ac-02) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#strict-planning-and-approvals) | Supported | — | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-03](../specs/user-stories.md#us-03-ac-03) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#strict-planning-and-approvals) | Supported | — | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-04](../specs/user-stories.md#us-03-ac-04) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#strict-planning-and-approvals) | Supported | — | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-05](../specs/user-stories.md#us-03-ac-05) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#strict-planning-and-approvals) | Supported | — | Strict plan/boundary/approval semantics preserved |
| [US-05-AC-01](../specs/user-stories.md#us-05-ac-01) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#semantic-validation) | Supported | — | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-02](../specs/user-stories.md#us-05-ac-02) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#semantic-validation) | Supported | — | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-03](../specs/user-stories.md#us-05-ac-03) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#semantic-validation) | Supported | — | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-04](../specs/user-stories.md#us-05-ac-04) | M1; accepted slice | [Contract](../specs/design/software-blueprint.md#semantic-validation) | Supported | — | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-05](../specs/user-stories.md#us-05-ac-05) | M1; pending training integration | [Contract](../specs/design/software-blueprint.md#semantic-validation) | Supported | R5 | Metadata/candidate APIs accepted; supported training-path integration remains pending |
| [US-09-AC-01](../specs/user-stories.md#us-09-ac-01) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-02](../specs/user-stories.md#us-09-ac-02) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-03](../specs/user-stories.md#us-09-ac-03) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-04](../specs/user-stories.md#us-09-ac-04) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-05](../specs/user-stories.md#us-09-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-10-AC-01](../specs/user-stories.md#us-10-ac-01) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Local status/logs, trial cap and available evidence |
| [US-10-AC-02](../specs/user-stories.md#us-10-ac-02) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Local status/logs, trial cap and available evidence |
| [US-10-AC-03](../specs/user-stories.md#us-10-ac-03) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Local status/logs, trial cap and available evidence |
| [US-10-AC-04](../specs/user-stories.md#us-10-ac-04) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Local status/logs, trial cap and available evidence |
| [US-10-AC-05](../specs/user-stories.md#us-10-ac-05) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Local status/logs, trial cap and available evidence |
| [US-11-AC-01](../specs/user-stories.md#us-11-ac-01) | M1; accepted 2026-11-07 | [Contract](../extraction.md) | Supported | R1/R4 | Native CSV/Parquet and project selection/filter/join outputs; both installed paths |
| [US-11-AC-02](../specs/user-stories.md#us-11-ac-02) | M1; accepted 2026-11-07 | [Contract](../extraction.md) | Supported | R1/R4 | Source schemas, rows, bytes, reader settings and identities; both installed paths |
| [US-11-AC-03](../specs/user-stories.md#us-11-ac-03) | M1; accepted 2026-11-07 | [Contract](../extraction.md) | Supported | R1/R4 | Project callback executes native operations with recorded settings; no arbitrary-code isolation |
| [US-11-AC-04](../specs/user-stories.md#us-11-ac-04) | M1; accepted 2026-11-07 | [Contract](../extraction.md) | Supported | R1/R4 | Source/code/output checksums, settings and timing; real DVC links remain US-13 work |
| [US-11-AC-05](../specs/user-stories.md#us-11-ac-05) | M1; accepted 2026-11-07 | [Contract](../extraction.md) | Supported | R1/R4 | Missing/invalid inputs and callback/publication failures; completion is not a quality-pass claim |
| [US-12-AC-01](../specs/user-stories.md#us-12-ac-01) | M1; accepted 2026-11-07 | [Contract](../data-quality.md) | Supported | R1/R4 | Seven rule families with measurements and required/advisory failures; both installed paths |
| [US-12-AC-05](../specs/user-stories.md#us-12-ac-05) | M1; accepted 2026-11-07 | [Contract](../data-quality.md) | Supported | R1/R4 | Required failure blocks supplied operation; advisory/no-check permits it; future runner integration pending |
| [US-13-AC-01](../specs/user-stories.md#us-13-ac-01) | M1; planned | [Contract](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts) | Supported | — | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-02](../specs/user-stories.md#us-13-ac-02) | M1; planned | [Contract](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts) | Supported | — | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-03](../specs/user-stories.md#us-13-ac-03) | M2; planned | [Contract](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts) | Supported | — | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-04](../specs/user-stories.md#us-13-ac-04) | M2; planned | [Contract](../specs/design/data-and-features.md#dvc-data-and-fitted-artifacts) | Supported | — | DVC versions/restore identity and missing-corrupt checks |
| [US-26-AC-01](../specs/user-stories.md#us-26-ac-01) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-02](../specs/user-stories.md#us-26-ac-02) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-03](../specs/user-stories.md#us-26-ac-03) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-04](../specs/user-stories.md#us-26-ac-04) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-05](../specs/user-stories.md#us-26-ac-05) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-27-AC-01](../specs/user-stories.md#us-27-ac-01) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-02](../specs/user-stories.md#us-27-ac-02) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-03](../specs/user-stories.md#us-27-ac-03) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-04](../specs/user-stories.md#us-27-ac-04) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-12-AC-02](../specs/user-stories.md#us-12-ac-02) | M1; accepted 2026-11-08 | [Contract](../data-assessment-and-splits.md#assessment-boundary) | Supported | R1/R4 | Native summaries/missingness/target balance and JSON scalars; both installed paths; no quality judgment |
| [US-12-AC-03](../specs/user-stories.md#us-12-ac-03) | M1; accepted 2026-11-08 | [Contract](../data-assessment-and-splits.md#partition-boundary) | Supported | R1/R4 | Seeded/supplied two-way/three-way membership, disjointness, source identity and project JSON reconstruction; protocols declared only; no fitting guarantee |
| [US-12-AC-04](../specs/user-stories.md#us-12-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-14-AC-01](../specs/user-stories.md#us-14-ac-01) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-02](../specs/user-stories.md#us-14-ac-02) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-03](../specs/user-stories.md#us-14-ac-03) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-04](../specs/user-stories.md#us-14-ac-04) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-05](../specs/user-stories.md#us-14-ac-05) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Authored fit/transform and consistent feature comparisons |
| [US-15-AC-01](../specs/user-stories.md#us-15-ac-01) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Train-only fit and usable restored state |
| [US-15-AC-02](../specs/user-stories.md#us-15-ac-02) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Train-only fit and usable restored state |
| [US-15-AC-03](../specs/user-stories.md#us-15-ac-03) | M1; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Train-only fit and usable restored state |
| [US-15-AC-04](../specs/user-stories.md#us-15-ac-04) | M2; planned | [Contract](../specs/design/data-and-features.md#authored-feature-pipelines) | Supported | — | Train-only fit and usable restored state |
| [US-16-AC-01](../specs/user-stories.md#us-16-ac-01) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-02](../specs/user-stories.md#us-16-ac-02) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-03](../specs/user-stories.md#us-16-ac-03) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-04](../specs/user-stories.md#us-16-ac-04) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-05](../specs/user-stories.md#us-16-ac-05) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-27-AC-05](../specs/user-stories.md#us-27-ac-05) | M1; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-06](../specs/user-stories.md#us-27-ac-06) | M1; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-07](../specs/user-stories.md#us-27-ac-07) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-08](../specs/user-stories.md#us-27-ac-08) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-09](../specs/user-stories.md#us-27-ac-09) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Native stages, cache invalidation/replay and output checks |
| [US-06-AC-01](../specs/user-stories.md#us-06-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-02](../specs/user-stories.md#us-06-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-03](../specs/user-stories.md#us-06-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-04](../specs/user-stories.md#us-06-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-16-AC-06](../specs/user-stories.md#us-16-ac-06) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-07](../specs/user-stories.md#us-16-ac-07) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-08](../specs/user-stories.md#us-16-ac-08) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-09](../specs/user-stories.md#us-16-ac-09) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-10](../specs/user-stories.md#us-16-ac-10) | M2; planned | [Contract](../specs/design/interfaces-and-configuration.md#paths-customization-and-notebooks) | Supported | — | Compatible project objects, output checks and fitted artifacts |
| [US-18-AC-01](../specs/user-stories.md#us-18-ac-01) | M1 classification + M2 regression; planned | [Contract](../specs/design/software-blueprint.md#planned-mvp-responsibilities) | Supported | — | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-02](../specs/user-stories.md#us-18-ac-02) | M1; planned | [Contract](../specs/design/software-blueprint.md#planned-mvp-responsibilities) | Supported | — | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-03](../specs/user-stories.md#us-18-ac-03) | M1; planned | [Contract](../specs/design/software-blueprint.md#planned-mvp-responsibilities) | Supported | — | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-04](../specs/user-stories.md#us-18-ac-04) | M1; planned | [Contract](../specs/design/software-blueprint.md#planned-mvp-responsibilities) | Supported | — | Classification M1/regression M2, baseline and native model operations |
| [US-19-AC-01](../specs/user-stories.md#us-19-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-02](../specs/user-stories.md#us-19-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-03](../specs/user-stories.md#us-19-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-04](../specs/user-stories.md#us-19-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-20-AC-01](../specs/user-stories.md#us-20-ac-01) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-02](../specs/user-stories.md#us-20-ac-02) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-03](../specs/user-stories.md#us-20-ac-03) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-04](../specs/user-stories.md#us-20-ac-04) | M1; planned | [Contract](../specs/design/execution-and-governance.md#local-execution-and-limits) | Supported | — | Declared parameter bounds, maximum trials and summary |
| [US-21-AC-01](../specs/user-stories.md#us-21-ac-01) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-02](../specs/user-stories.md#us-21-ac-02) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-03](../specs/user-stories.md#us-21-ac-03) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-04](../specs/user-stories.md#us-21-ac-04) | M2; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-05](../specs/user-stories.md#us-21-ac-05) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-24-AC-01](../specs/user-stories.md#us-24-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-24-AC-02](../specs/user-stories.md#us-24-ac-02) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Separate final-test step; no protected-storage claim |
| [US-24-AC-03](../specs/user-stories.md#us-24-ac-03) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Separate final-test step; no protected-storage claim |
| [US-24-AC-04](../specs/user-stories.md#us-24-ac-04) | M1; planned | [Contract](../specs/design/execution-and-governance.md#evaluation-and-final-testing) | Supported | — | Separate final-test step; no protected-storage claim |
| [US-24-AC-05](../specs/user-stories.md#us-24-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-06](../specs/user-stories.md#us-26-ac-06) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-07](../specs/user-stories.md#us-26-ac-07) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-08](../specs/user-stories.md#us-26-ac-08) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-09](../specs/user-stories.md#us-26-ac-09) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-04-AC-01](../specs/user-stories.md#us-04-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-02](../specs/user-stories.md#us-04-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-03](../specs/user-stories.md#us-04-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-04](../specs/user-stories.md#us-04-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-01](../specs/user-stories.md#us-07-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-02](../specs/user-stories.md#us-07-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-03](../specs/user-stories.md#us-07-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-04](../specs/user-stories.md#us-07-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-01](../specs/user-stories.md#us-08-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-02](../specs/user-stories.md#us-08-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-03](../specs/user-stories.md#us-08-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-04](../specs/user-stories.md#us-08-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-01](../specs/user-stories.md#us-17-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-02](../specs/user-stories.md#us-17-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-03](../specs/user-stories.md#us-17-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-04](../specs/user-stories.md#us-17-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-01](../specs/user-stories.md#us-22-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-02](../specs/user-stories.md#us-22-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-03](../specs/user-stories.md#us-22-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-04](../specs/user-stories.md#us-22-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-05](../specs/user-stories.md#us-22-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-01](../specs/user-stories.md#us-30-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-02](../specs/user-stories.md#us-30-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-03](../specs/user-stories.md#us-30-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-04](../specs/user-stories.md#us-30-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-05](../specs/user-stories.md#us-30-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-01](../specs/user-stories.md#us-23-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-02](../specs/user-stories.md#us-23-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-03](../specs/user-stories.md#us-23-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-04](../specs/user-stories.md#us-23-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-05](../specs/user-stories.md#us-23-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-01](../specs/user-stories.md#us-25-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-02](../specs/user-stories.md#us-25-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-03](../specs/user-stories.md#us-25-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-04](../specs/user-stories.md#us-25-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-06](../specs/user-stories.md#us-30-ac-06) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-07](../specs/user-stories.md#us-30-ac-07) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-08](../specs/user-stories.md#us-30-ac-08) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-09](../specs/user-stories.md#us-30-ac-09) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-10](../specs/user-stories.md#us-26-ac-10) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-11](../specs/user-stories.md#us-26-ac-11) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-12](../specs/user-stories.md#us-26-ac-12) | M1; planned | [Contract](../specs/design/execution-and-governance.md#tracking-and-storage-ownership) | Supported | — | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-13](../specs/user-stories.md#us-26-ac-13) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-01](../specs/user-stories.md#us-28-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-02](../specs/user-stories.md#us-28-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-03](../specs/user-stories.md#us-28-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-04](../specs/user-stories.md#us-28-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-01](../specs/user-stories.md#us-29-ac-01) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-02](../specs/user-stories.md#us-29-ac-02) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-03](../specs/user-stories.md#us-29-ac-03) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-04](../specs/user-stories.md#us-29-ac-04) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-05](../specs/user-stories.md#us-29-ac-05) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-06](../specs/user-stories.md#us-29-ac-06) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-07](../specs/user-stories.md#us-29-ac-07) | Roadmap; deferred | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Preserved original requirement; explicit future activation/evidence needed |
| [US-35-AC-01](../specs/user-stories.md#us-35-ac-01) | M50; accepted slice | [Contract](../development/records.md) | Supported | — | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-02](../specs/user-stories.md#us-35-ac-02) | M50; accepted slice | [Contract](../development/records.md) | Supported | — | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-03](../specs/user-stories.md#us-35-ac-03) | M50; accepted slice | [Contract](../development/records.md) | Supported | — | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-04](../specs/user-stories.md#us-35-ac-04) | M50; accepted slice | [Contract](../development/records.md) | Supported | — | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-05](../specs/user-stories.md#us-35-ac-05) | M50; accepted slice | [Contract](../development/records.md) | Supported | — | Accepted cleanup/records ownership; retain known limits |
| [US-36-AC-01](../specs/user-stories.md#us-36-ac-01) | M50; accepted slice | [Contract](../development/verification.md#pytest-workspace-ownership-and-retention) | Supported | — | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-02](../specs/user-stories.md#us-36-ac-02) | M50; accepted slice | [Contract](../development/verification.md#pytest-workspace-ownership-and-retention) | Supported | — | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-03](../specs/user-stories.md#us-36-ac-03) | M50; accepted slice | [Contract](../development/verification.md#pytest-workspace-ownership-and-retention) | Supported | — | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-04](../specs/user-stories.md#us-36-ac-04) | M50; accepted slice | [Contract](../development/verification.md#pytest-workspace-ownership-and-retention) | Supported | — | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-05](../specs/user-stories.md#us-36-ac-05) | M50; accepted slice | [Contract](../development/verification.md#pytest-workspace-ownership-and-retention) | Supported | — | Accepted workspace lifecycle; retain known limits |
| [US-37-AC-01](../specs/user-stories.md#us-37-ac-01) | M50; backlog | [Contract](../development/verification.md) | Supported | — | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-02](../specs/user-stories.md#us-37-ac-02) | M50; backlog | [Contract](../development/verification.md) | Supported | — | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-03](../specs/user-stories.md#us-37-ac-03) | M50; backlog | [Contract](../development/verification.md) | Supported | — | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-04](../specs/user-stories.md#us-37-ac-04) | M50; backlog | [Contract](../development/verification.md) | Supported | — | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-05](../specs/user-stories.md#us-37-ac-05) | M50; backlog | [Contract](../development/verification.md) | Supported | — | Unimplemented environment-reuse backlog; no new evidence |
| [US-38-AC-01](../specs/user-stories.md#us-38-ac-01) | M50; backlog | [Contract](../development/records.md) | Supported | — | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-02](../specs/user-stories.md#us-38-ac-02) | M50; backlog | [Contract](../development/records.md) | Supported | — | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-03](../specs/user-stories.md#us-38-ac-03) | M50; backlog | [Contract](../development/records.md) | Supported | — | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-04](../specs/user-stories.md#us-38-ac-04) | M50; backlog | [Contract](../development/records.md) | Supported | — | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-05](../specs/user-stories.md#us-38-ac-05) | M50; backlog | [Contract](../development/records.md) | Supported | — | Unimplemented environment-release backlog; no new evidence |
| [US-34-AC-01](../specs/user-stories.md#us-34-ac-01) | M99; backlog | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Existing deferred contribution/review backlog |
| [US-34-AC-02](../specs/user-stories.md#us-34-ac-02) | M99; backlog | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Existing deferred contribution/review backlog |
| [US-34-AC-03](../specs/user-stories.md#us-34-ac-03) | M99; backlog | [Contract](../specs/design/architecture-decisions.md#deferred-assurance-register) | Supported | — | Existing deferred contribution/review backlog |
| [US-39-AC-01](../specs/user-stories.md#us-39-ac-01) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-02](../specs/user-stories.md#us-39-ac-02) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-03](../specs/user-stories.md#us-39-ac-03) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-04](../specs/user-stories.md#us-39-ac-04) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-05](../specs/user-stories.md#us-39-ac-05) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-06](../specs/user-stories.md#us-39-ac-06) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-07](../specs/user-stories.md#us-39-ac-07) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-08](../specs/user-stories.md#us-39-ac-08) | M1; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-09](../specs/user-stories.md#us-39-ac-09) | M2; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-10](../specs/user-stories.md#us-39-ac-10) | M2; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-11](../specs/user-stories.md#us-39-ac-11) | M2; planned | [Contract](../specs/example-walkthrough.md) | Supported | — | Installed experiment plus assistant evidence and usability extensions |
| [US-40-AC-01](../specs/user-stories.md#us-40-ac-01) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-02](../specs/user-stories.md#us-40-ac-02) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-03](../specs/user-stories.md#us-40-ac-03) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-04](../specs/user-stories.md#us-40-ac-04) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-05](../specs/user-stories.md#us-40-ac-05) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-06](../specs/user-stories.md#us-40-ac-06) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-07](../specs/user-stories.md#us-40-ac-07) | M2; planned | [Contract](../specs/design/execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Supported | — | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-41-AC-01](../specs/user-stories.md#us-41-ac-01) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred wheel bootstrap in a separate project; no package-index publication |
| [US-41-AC-02](../specs/user-stories.md#us-41-ac-02) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred CLI/API distribution-origin initialization and compatible reruns; current initializer requires a Git pin |
| [US-41-AC-03](../specs/user-stories.md#us-41-ac-03) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred version/locked-artifact identity consistency checks |
| [US-41-AC-04](../specs/user-stories.md#us-41-ac-04) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred pre-mutation identity failures and distribution dependency preservation |
| [US-41-AC-05](../specs/user-stories.md#us-41-ac-05) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred explicit distribution upgrades and environment-identity updates |
| [US-41-AC-06](../specs/user-stories.md#us-41-ac-06) | M99; deferred, local-only | [Contract](../specs/design/interfaces-and-configuration.md#installed-project-boundary) | Supported | R6 | Deferred direct/rebuilt-wheel initialization and identity-failure evidence; preserve Git installation |

## Verification and limits

Documentation-only: no executable behavior changed, so TDD, pytest and installed
artifact runs were not applicable and were not launched. No platform support or
new story/milestone acceptance is claimed. The active execution/governance design
already matches the revised MVP and needed no change.

Document checks: exact criterion-ID set/uniqueness comparison (228 stories and
228 index rows); AST comparison of 43 public exports across eight module surfaces;
1,073 relative file/anchor checks across 14 changed/new Markdown files;
`git diff --check` and new-file whitespace checks; manual
review of changes against public source and accepted contracts. Checkpoint and
report links are included in final document checking. Historical archives,
source, tests, package resources, user stories and lockfile remain unchanged.
Lock SHA-256: `5f99c2da64eb46bc758f798f364e67eab25246253fc75315ebb404461e466a9d` (same as baseline).

Result: 228 Supported within the stated document/scope boundary; 0 Partial,
0 Missing, 0 Contradictory and 0 Decision needed. Findings: 0 High, 6 Medium,
2 Low; all eight corrected. Complete historical implementation/platform assurance
is outside the review boundary and is not inferred from these coverage counts.
