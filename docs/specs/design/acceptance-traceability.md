# Acceptance Traceability

Active design 0.15; criteria are in [user stories](../user-stories.md).
This index covers all **228** local criteria: **204 original IDs, 18 US-39/40 criteria,
and six planned M50 US-41 criteria**.
A supporting contract is design coverage, not executable verification/acceptance.
Scope and supporting design were approved at Gates 1–3.

## Coverage status and verification boundaries

Accepted M0/US-01/02/03/05, US-11, US-12 AC-01/02/03/05 and US-35/36
retain owning-plan evidence. US-12-AC-04 remains deferred.
US-05-AC-05 training integration and US-39's default/basic path remain new work;
do not infer training support from accepted metadata or storage setup.

Planned MVP criteria need installed public-interface tests, explicit failure/
boundary cases, locked project environments and public test-boundary approval in
owning story plans. Manual ASW evidence proves assistant usability, not numerical
correctness. Record actual outputs and one concrete assistant/version.
Roadmap/backlog criteria are explicitly deferred/unimplemented, not missing
requirements or claims that their stronger guarantees were verified.

## Criterion-to-design index

| Criterion | Delivery / status | Supporting contract | Public verification outcome / limits |
|---|---|---|---|
| [US-31-AC-01](../user-stories.md#us-31-ac-01) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-02](../user-stories.md#us-31-ac-02) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-03](../user-stories.md#us-31-ac-03) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-04](../user-stories.md#us-31-ac-04) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-05](../user-stories.md#us-31-ac-05) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-06](../user-stories.md#us-31-ac-06) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-07](../user-stories.md#us-31-ac-07) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-08](../user-stories.md#us-31-ac-08) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-09](../user-stories.md#us-31-ac-09) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-31-AC-10](../user-stories.md#us-31-ac-10) | M0; accepted slice | [Contract](../../development.md) | Accepted contributor setup and verified environment evidence |
| [US-32-AC-01](../user-stories.md#us-32-ac-01) | M0; accepted slice | [Contract](../../development.md) | Accepted CI and shared contributor checks |
| [US-32-AC-02](../user-stories.md#us-32-ac-02) | M0; accepted slice | [Contract](../../development.md) | Accepted CI and shared contributor checks |
| [US-32-AC-03](../user-stories.md#us-32-ac-03) | M0; accepted slice | [Contract](../../development.md) | Accepted CI and shared contributor checks |
| [US-32-AC-04](../user-stories.md#us-32-ac-04) | M0; accepted slice | [Contract](../../development.md) | Accepted CI and shared contributor checks |
| [US-33-AC-01](../user-stories.md#us-33-ac-01) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-02](../user-stories.md#us-33-ac-02) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-03](../user-stories.md#us-33-ac-03) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-04](../user-stories.md#us-33-ac-04) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-05](../user-stories.md#us-33-ac-05) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-06](../user-stories.md#us-33-ac-06) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-33-AC-07](../user-stories.md#us-33-ac-07) | M0; accepted slice | [Contract](../../development.md) | Accepted installed wheel/source resources/version checks |
| [US-01-AC-01](../user-stories.md#us-01-ac-01) | M1; accepted slice | [Contract](software-blueprint.md#existing-public-contracts) | Pinned installation/upgrade and installed resources |
| [US-01-AC-02](../user-stories.md#us-01-ac-02) | M1; accepted slice | [Contract](software-blueprint.md#existing-public-contracts) | Pinned installation/upgrade and installed resources |
| [US-01-AC-03](../user-stories.md#us-01-ac-03) | M1; accepted slice | [Contract](software-blueprint.md#existing-public-contracts) | Pinned installation/upgrade and installed resources |
| [US-01-AC-04](../user-stories.md#us-01-ac-04) | M1; accepted slice | [Contract](software-blueprint.md#existing-public-contracts) | Pinned installation/upgrade and installed resources |
| [US-02-AC-01](../user-stories.md#us-02-ac-01) | M1; accepted slice | [Contract](software-blueprint.md#initialization-and-paths) | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-02](../user-stories.md#us-02-ac-02) | M1; accepted slice | [Contract](software-blueprint.md#initialization-and-paths) | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-03](../user-stories.md#us-02-ac-03) | M1; accepted slice | [Contract](software-blueprint.md#initialization-and-paths) | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-04](../user-stories.md#us-02-ac-04) | M1; accepted slice | [Contract](software-blueprint.md#initialization-and-paths) | Conflict-safe setup and draft/default compatibility |
| [US-02-AC-05](../user-stories.md#us-02-ac-05) | M1; accepted slice | [Contract](software-blueprint.md#initialization-and-paths) | Conflict-safe setup and draft/default compatibility |
| [US-03-AC-01](../user-stories.md#us-03-ac-01) | M1; accepted slice | [Contract](software-blueprint.md#strict-planning-and-approvals) | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-02](../user-stories.md#us-03-ac-02) | M1; accepted slice | [Contract](software-blueprint.md#strict-planning-and-approvals) | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-03](../user-stories.md#us-03-ac-03) | M1; accepted slice | [Contract](software-blueprint.md#strict-planning-and-approvals) | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-04](../user-stories.md#us-03-ac-04) | M1; accepted slice | [Contract](software-blueprint.md#strict-planning-and-approvals) | Strict plan/boundary/approval semantics preserved |
| [US-03-AC-05](../user-stories.md#us-03-ac-05) | M1; accepted slice | [Contract](software-blueprint.md#strict-planning-and-approvals) | Strict plan/boundary/approval semantics preserved |
| [US-05-AC-01](../user-stories.md#us-05-ac-01) | M1; accepted slice | [Contract](software-blueprint.md#semantic-validation) | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-02](../user-stories.md#us-05-ac-02) | M1; accepted slice | [Contract](software-blueprint.md#semantic-validation) | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-03](../user-stories.md#us-05-ac-03) | M1; accepted slice | [Contract](software-blueprint.md#semantic-validation) | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-04](../user-stories.md#us-05-ac-04) | M1; accepted slice | [Contract](software-blueprint.md#semantic-validation) | Metadata/candidate checks; future training integration remains open |
| [US-05-AC-05](../user-stories.md#us-05-ac-05) | M1; pending training integration | [Contract](software-blueprint.md#semantic-validation) | Metadata/candidate APIs accepted; supported training-path integration remains pending |
| [US-09-AC-01](../user-stories.md#us-09-ac-01) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-02](../user-stories.md#us-09-ac-02) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-03](../user-stories.md#us-09-ac-03) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-04](../user-stories.md#us-09-ac-04) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Fresh kernel, explicit artifacts and saved diagnostics |
| [US-09-AC-05](../user-stories.md#us-09-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-10-AC-01](../user-stories.md#us-10-ac-01) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Local status/logs, trial cap and available evidence |
| [US-10-AC-02](../user-stories.md#us-10-ac-02) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Local status/logs, trial cap and available evidence |
| [US-10-AC-03](../user-stories.md#us-10-ac-03) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Local status/logs, trial cap and available evidence |
| [US-10-AC-04](../user-stories.md#us-10-ac-04) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Local status/logs, trial cap and available evidence |
| [US-10-AC-05](../user-stories.md#us-10-ac-05) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Local status/logs, trial cap and available evidence |
| [US-11-AC-01](../user-stories.md#us-11-ac-01) | M1; accepted 2026-11-07 | [Contract](../../extraction.md) | Native CSV/Parquet and project selection/filter/join outputs; both installed paths |
| [US-11-AC-02](../user-stories.md#us-11-ac-02) | M1; accepted 2026-11-07 | [Contract](../../extraction.md) | Source schemas, rows, bytes, reader settings and identities; both installed paths |
| [US-11-AC-03](../user-stories.md#us-11-ac-03) | M1; accepted 2026-11-07 | [Contract](../../extraction.md) | Project callback executes native operations with recorded settings; no arbitrary-code isolation |
| [US-11-AC-04](../user-stories.md#us-11-ac-04) | M1; accepted 2026-11-07 | [Contract](../../extraction.md) | Source/code/output checksums, settings and timing; real DVC links remain US-13 work |
| [US-11-AC-05](../user-stories.md#us-11-ac-05) | M1; accepted 2026-11-07 | [Contract](../../extraction.md) | Missing/invalid inputs and callback/publication failures; completion is not a quality-pass claim |
| [US-12-AC-01](../user-stories.md#us-12-ac-01) | M1; accepted 2026-11-07 | [Contract](../../data-quality.md) | Seven rule families with measurements and required/advisory failures; both installed paths |
| [US-12-AC-05](../user-stories.md#us-12-ac-05) | M1; accepted 2026-11-07 | [Contract](../../data-quality.md) | Required failure blocks supplied operation; advisory/no-check permits it; future runner integration pending |
| [US-13-AC-01](../user-stories.md#us-13-ac-01) | M1; planned | [Contract](data-and-features.md#dvc-data-and-fitted-artifacts) | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-02](../user-stories.md#us-13-ac-02) | M1; planned | [Contract](data-and-features.md#dvc-data-and-fitted-artifacts) | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-03](../user-stories.md#us-13-ac-03) | M2; planned | [Contract](data-and-features.md#dvc-data-and-fitted-artifacts) | DVC versions/restore identity and missing-corrupt checks |
| [US-13-AC-04](../user-stories.md#us-13-ac-04) | M2; planned | [Contract](data-and-features.md#dvc-data-and-fitted-artifacts) | DVC versions/restore identity and missing-corrupt checks |
| [US-26-AC-01](../user-stories.md#us-26-ac-01) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-02](../user-stories.md#us-26-ac-02) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-03](../user-stories.md#us-26-ac-03) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-04](../user-stories.md#us-26-ac-04) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-05](../user-stories.md#us-26-ac-05) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-27-AC-01](../user-stories.md#us-27-ac-01) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-02](../user-stories.md#us-27-ac-02) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-03](../user-stories.md#us-27-ac-03) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-04](../user-stories.md#us-27-ac-04) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-12-AC-02](../user-stories.md#us-12-ac-02) | M1; accepted 2026-11-08 | [Contract](../../data-assessment-and-splits.md#assessment-boundary) | Native summaries/missingness/target balance and JSON scalars; both installed paths; no quality judgment |
| [US-12-AC-03](../user-stories.md#us-12-ac-03) | M1; accepted 2026-11-08 | [Contract](../../data-assessment-and-splits.md#partition-boundary) | Seeded/supplied two-way/three-way membership, disjointness, source identity and project JSON reconstruction; protocols declared only; no fitting guarantee |
| [US-12-AC-04](../user-stories.md#us-12-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-14-AC-01](../user-stories.md#us-14-ac-01) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-02](../user-stories.md#us-14-ac-02) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-03](../user-stories.md#us-14-ac-03) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-04](../user-stories.md#us-14-ac-04) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Authored fit/transform and consistent feature comparisons |
| [US-14-AC-05](../user-stories.md#us-14-ac-05) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Authored fit/transform and consistent feature comparisons |
| [US-15-AC-01](../user-stories.md#us-15-ac-01) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Train-only fit and usable restored state |
| [US-15-AC-02](../user-stories.md#us-15-ac-02) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Train-only fit and usable restored state |
| [US-15-AC-03](../user-stories.md#us-15-ac-03) | M1; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Train-only fit and usable restored state |
| [US-15-AC-04](../user-stories.md#us-15-ac-04) | M2; planned | [Contract](data-and-features.md#authored-feature-pipelines) | Train-only fit and usable restored state |
| [US-16-AC-01](../user-stories.md#us-16-ac-01) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-02](../user-stories.md#us-16-ac-02) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-03](../user-stories.md#us-16-ac-03) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-04](../user-stories.md#us-16-ac-04) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-05](../user-stories.md#us-16-ac-05) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-27-AC-05](../user-stories.md#us-27-ac-05) | M1; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-06](../user-stories.md#us-27-ac-06) | M1; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-07](../user-stories.md#us-27-ac-07) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-08](../user-stories.md#us-27-ac-08) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-27-AC-09](../user-stories.md#us-27-ac-09) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Native stages, cache invalidation/replay and output checks |
| [US-06-AC-01](../user-stories.md#us-06-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-02](../user-stories.md#us-06-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-03](../user-stories.md#us-06-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-06-AC-04](../user-stories.md#us-06-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-16-AC-06](../user-stories.md#us-16-ac-06) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-07](../user-stories.md#us-16-ac-07) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-08](../user-stories.md#us-16-ac-08) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-09](../user-stories.md#us-16-ac-09) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-16-AC-10](../user-stories.md#us-16-ac-10) | M2; planned | [Contract](interfaces-and-configuration.md#paths-customization-and-notebooks) | Compatible project objects, output checks and fitted artifacts |
| [US-18-AC-01](../user-stories.md#us-18-ac-01) | M1 classification + M2 regression; planned | [Contract](software-blueprint.md#planned-mvp-responsibilities) | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-02](../user-stories.md#us-18-ac-02) | M1; planned | [Contract](software-blueprint.md#planned-mvp-responsibilities) | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-03](../user-stories.md#us-18-ac-03) | M1; planned | [Contract](software-blueprint.md#planned-mvp-responsibilities) | Classification M1/regression M2, baseline and native model operations |
| [US-18-AC-04](../user-stories.md#us-18-ac-04) | M1; planned | [Contract](software-blueprint.md#planned-mvp-responsibilities) | Classification M1/regression M2, baseline and native model operations |
| [US-19-AC-01](../user-stories.md#us-19-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-02](../user-stories.md#us-19-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-03](../user-stories.md#us-19-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-19-AC-04](../user-stories.md#us-19-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-20-AC-01](../user-stories.md#us-20-ac-01) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-02](../user-stories.md#us-20-ac-02) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-03](../user-stories.md#us-20-ac-03) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Declared parameter bounds, maximum trials and summary |
| [US-20-AC-04](../user-stories.md#us-20-ac-04) | M1; planned | [Contract](execution-and-governance.md#local-execution-and-limits) | Declared parameter bounds, maximum trials and summary |
| [US-21-AC-01](../user-stories.md#us-21-ac-01) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-02](../user-stories.md#us-21-ac-02) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-03](../user-stories.md#us-21-ac-03) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-04](../user-stories.md#us-21-ac-04) | M2; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-21-AC-05](../user-stories.md#us-21-ac-05) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Expected artifacts/metrics, supported validity checks and tolerances |
| [US-24-AC-01](../user-stories.md#us-24-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-24-AC-02](../user-stories.md#us-24-ac-02) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Separate final-test step; no protected-storage claim |
| [US-24-AC-03](../user-stories.md#us-24-ac-03) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Separate final-test step; no protected-storage claim |
| [US-24-AC-04](../user-stories.md#us-24-ac-04) | M1; planned | [Contract](execution-and-governance.md#evaluation-and-final-testing) | Separate final-test step; no protected-storage claim |
| [US-24-AC-05](../user-stories.md#us-24-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-06](../user-stories.md#us-26-ac-06) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-07](../user-stories.md#us-26-ac-07) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-08](../user-stories.md#us-26-ac-08) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-09](../user-stories.md#us-26-ac-09) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-04-AC-01](../user-stories.md#us-04-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-02](../user-stories.md#us-04-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-03](../user-stories.md#us-04-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-04-AC-04](../user-stories.md#us-04-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-01](../user-stories.md#us-07-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-02](../user-stories.md#us-07-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-03](../user-stories.md#us-07-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-07-AC-04](../user-stories.md#us-07-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-01](../user-stories.md#us-08-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-02](../user-stories.md#us-08-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-03](../user-stories.md#us-08-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-08-AC-04](../user-stories.md#us-08-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-01](../user-stories.md#us-17-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-02](../user-stories.md#us-17-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-03](../user-stories.md#us-17-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-17-AC-04](../user-stories.md#us-17-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-01](../user-stories.md#us-22-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-02](../user-stories.md#us-22-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-03](../user-stories.md#us-22-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-04](../user-stories.md#us-22-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-22-AC-05](../user-stories.md#us-22-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-01](../user-stories.md#us-30-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-02](../user-stories.md#us-30-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-03](../user-stories.md#us-30-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-04](../user-stories.md#us-30-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-05](../user-stories.md#us-30-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-01](../user-stories.md#us-23-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-02](../user-stories.md#us-23-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-03](../user-stories.md#us-23-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-04](../user-stories.md#us-23-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-23-AC-05](../user-stories.md#us-23-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-01](../user-stories.md#us-25-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-02](../user-stories.md#us-25-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-03](../user-stories.md#us-25-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-25-AC-04](../user-stories.md#us-25-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-06](../user-stories.md#us-30-ac-06) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-07](../user-stories.md#us-30-ac-07) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-08](../user-stories.md#us-30-ac-08) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-30-AC-09](../user-stories.md#us-30-ac-09) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-10](../user-stories.md#us-26-ac-10) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-11](../user-stories.md#us-26-ac-11) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-26-AC-12](../user-stories.md#us-26-ac-12) | M1; planned | [Contract](execution-and-governance.md#tracking-and-storage-ownership) | MLflow evidence linked to DVC/committed code/config/environment |
| [US-26-AC-13](../user-stories.md#us-26-ac-13) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-01](../user-stories.md#us-28-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-02](../user-stories.md#us-28-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-03](../user-stories.md#us-28-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-28-AC-04](../user-stories.md#us-28-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-01](../user-stories.md#us-29-ac-01) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-02](../user-stories.md#us-29-ac-02) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-03](../user-stories.md#us-29-ac-03) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-04](../user-stories.md#us-29-ac-04) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-05](../user-stories.md#us-29-ac-05) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-06](../user-stories.md#us-29-ac-06) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-29-AC-07](../user-stories.md#us-29-ac-07) | Roadmap; deferred | [Contract](architecture-decisions.md#deferred-assurance-register) | Preserved original requirement; explicit future activation/evidence needed |
| [US-35-AC-01](../user-stories.md#us-35-ac-01) | M50; accepted slice | [Contract](../../development/records.md) | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-02](../user-stories.md#us-35-ac-02) | M50; accepted slice | [Contract](../../development/records.md) | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-03](../user-stories.md#us-35-ac-03) | M50; accepted slice | [Contract](../../development/records.md) | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-04](../user-stories.md#us-35-ac-04) | M50; accepted slice | [Contract](../../development/records.md) | Accepted cleanup/records ownership; retain known limits |
| [US-35-AC-05](../user-stories.md#us-35-ac-05) | M50; accepted slice | [Contract](../../development/records.md) | Accepted cleanup/records ownership; retain known limits |
| [US-36-AC-01](../user-stories.md#us-36-ac-01) | M50; accepted slice | [Contract](../../development/verification.md#pytest-workspace-ownership-and-retention) | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-02](../user-stories.md#us-36-ac-02) | M50; accepted slice | [Contract](../../development/verification.md#pytest-workspace-ownership-and-retention) | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-03](../user-stories.md#us-36-ac-03) | M50; accepted slice | [Contract](../../development/verification.md#pytest-workspace-ownership-and-retention) | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-04](../user-stories.md#us-36-ac-04) | M50; accepted slice | [Contract](../../development/verification.md#pytest-workspace-ownership-and-retention) | Accepted workspace lifecycle; retain known limits |
| [US-36-AC-05](../user-stories.md#us-36-ac-05) | M50; accepted slice | [Contract](../../development/verification.md#pytest-workspace-ownership-and-retention) | Accepted workspace lifecycle; retain known limits |
| [US-37-AC-01](../user-stories.md#us-37-ac-01) | M50; backlog | [Contract](../../development/verification.md) | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-02](../user-stories.md#us-37-ac-02) | M50; backlog | [Contract](../../development/verification.md) | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-03](../user-stories.md#us-37-ac-03) | M50; backlog | [Contract](../../development/verification.md) | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-04](../user-stories.md#us-37-ac-04) | M50; backlog | [Contract](../../development/verification.md) | Unimplemented environment-reuse backlog; no new evidence |
| [US-37-AC-05](../user-stories.md#us-37-ac-05) | M50; backlog | [Contract](../../development/verification.md) | Unimplemented environment-reuse backlog; no new evidence |
| [US-38-AC-01](../user-stories.md#us-38-ac-01) | M50; backlog | [Contract](../../development/records.md) | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-02](../user-stories.md#us-38-ac-02) | M50; backlog | [Contract](../../development/records.md) | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-03](../user-stories.md#us-38-ac-03) | M50; backlog | [Contract](../../development/records.md) | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-04](../user-stories.md#us-38-ac-04) | M50; backlog | [Contract](../../development/records.md) | Unimplemented environment-release backlog; no new evidence |
| [US-38-AC-05](../user-stories.md#us-38-ac-05) | M50; backlog | [Contract](../../development/records.md) | Unimplemented environment-release backlog; no new evidence |
| [US-34-AC-01](../user-stories.md#us-34-ac-01) | M99; backlog | [Contract](architecture-decisions.md#deferred-assurance-register) | Existing deferred contribution/review backlog |
| [US-34-AC-02](../user-stories.md#us-34-ac-02) | M99; backlog | [Contract](architecture-decisions.md#deferred-assurance-register) | Existing deferred contribution/review backlog |
| [US-34-AC-03](../user-stories.md#us-34-ac-03) | M99; backlog | [Contract](architecture-decisions.md#deferred-assurance-register) | Existing deferred contribution/review backlog |
| [US-39-AC-01](../user-stories.md#us-39-ac-01) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-02](../user-stories.md#us-39-ac-02) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-03](../user-stories.md#us-39-ac-03) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-04](../user-stories.md#us-39-ac-04) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-05](../user-stories.md#us-39-ac-05) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-06](../user-stories.md#us-39-ac-06) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-07](../user-stories.md#us-39-ac-07) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-08](../user-stories.md#us-39-ac-08) | M1; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-09](../user-stories.md#us-39-ac-09) | M2; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-10](../user-stories.md#us-39-ac-10) | M2; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-39-AC-11](../user-stories.md#us-39-ac-11) | M2; planned | [Contract](../example-walkthrough.md) | Installed experiment plus assistant evidence and usability extensions |
| [US-40-AC-01](../user-stories.md#us-40-ac-01) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-02](../user-stories.md#us-40-ac-02) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-03](../user-stories.md#us-40-ac-03) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-04](../user-stories.md#us-40-ac-04) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-05](../user-stories.md#us-40-ac-05) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-06](../user-stories.md#us-40-ac-06) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-40-AC-07](../user-stories.md#us-40-ac-07) | M2; planned | [Contract](execution-and-governance.md#native-dvc-pipeline-and-reproduction) | Committed replay, native cache behavior, assistant and tolerance checks |
| [US-41-AC-01](../user-stories.md#us-41-ac-01) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned wheel bootstrap in a separate project; no package-index publication |
| [US-41-AC-02](../user-stories.md#us-41-ac-02) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned CLI/API distribution-origin initialization and compatible reruns; current initializer requires a Git pin |
| [US-41-AC-03](../user-stories.md#us-41-ac-03) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned version/locked-artifact identity consistency checks |
| [US-41-AC-04](../user-stories.md#us-41-ac-04) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned pre-mutation identity failures and distribution dependency preservation |
| [US-41-AC-05](../user-stories.md#us-41-ac-05) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned explicit distribution upgrades and environment-identity updates |
| [US-41-AC-06](../user-stories.md#us-41-ac-06) | M50; planned, [issue #64](https://github.com/jimthompson5802/agentic-ml/issues/64) | [Contract](interfaces-and-configuration.md#installed-project-boundary) | Planned direct/rebuilt-wheel initialization and identity-failure evidence; preserve Git installation |

## Required scenario families

| Scenario | Planned public evidence |
|---|---|
| Local classification M1 | Controlled CSV/Parquet/filter/join outputs, missing inputs, schema failures, recorded disjoint splits, train-only fit, baseline/candidates and separate final scores |
| Bounded tuning | Invalid estimator/parameter rejection before fit; fixed/default values unchanged; maximum trial count and truthful summary |
| MLflow/DVC integration | Inspect actual run status/parameters/metrics/fitted artifacts and content/code/configuration references; verify native stage definitions and output identities |
| Reproduction M2 | Fresh committed project with pinned dependencies, restored DVC content, expected outputs/predictions/transforms within reviewed tolerances; missing/corrupt failures |
| Native cache | Unchanged reuse versus real execution, declared data/code/parameter invalidation, traceable original references; cache hit alone is not evaluation success |
| Notebook/custom/regression | Fresh-kernel outputs/errors, artifact dependencies, compatible project objects, restored fitted state and regression results |
| Scientist-directed assistant | ASW-01–08 under US-39/40: one recorded product/interface/version, prompts/actions, actual edit/rerun from validation evidence and independently checked results |

Use small controlled datasets and isolated project/storage fixtures. Exact fixture
values, split memberships and metric/output tolerances belong in reviewed owning
implementation plans, not invented passing claims here. Existing historical test
fixtures/evidence remain preserved. The [walkthrough](../example-walkthrough.md)
maps ASW steps to concrete criterion ownership.

## Historical coverage and verification ownership

The [previous 160-criterion index](../../verification/software-blueprint-final-coverage.md)
describes the old M1–6 blueprint and links to its
[historical catalogue](software-blueprint-v0.14-reference.md). It is not the revised
MVP inventory. Historical M1/M50 obligations, failures/skips and platform limits
remain with owning plans. Follow existing verification policy; no marker or test
selection changes are made by this document.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/acceptance-traceability.md).

<a id="10-acceptance-criteria-traceability"></a>

<a id="reference-acceptance-test-datasets"></a>
