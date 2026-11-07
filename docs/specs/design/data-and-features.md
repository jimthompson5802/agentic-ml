# Data and Features

Active design 0.15; [authority](../agentic-ml-harness-design.md).
Owns US-11/12/13/14/15/16 requirements in the revised
[stories](../user-stories.md). These data/feature operations are planned, not
implemented by current configuration-validation APIs.

## Local extraction and quality

Read local CSV/Parquet and support configured column selection, filtering and
joins. Permit ordinary project extraction functions. Record source paths/content
identities, effective extraction settings/time and output checksum/DVC reference.
Reject missing/invalid required inputs and report failures without calling partial
outputs validated data. SQL, object storage, discovery security and source quotas
are deferred; no universal connector interface is required now.

Check configured required columns/schema/types, row counts, nulls, duplicates and
quality rules. Include basic distributions/missingness and classification target
balance. Report actionable mismatches and block dependent supported steps when
required checks fail. No mandatory dataset approval service is needed.

## Reproducible partitions

Record seeded train/validation/test membership and source-data identity. Verify
disjoint rows and target alignment. Accept explicit user-provided partitions for
time/group-sensitive tasks, with recorded constraints and overlap checks; automatic
time/group split algorithms are not required by this MVP.

Training/preprocessing receives training rows; development scores use validation
rows. Final testing occurs after validation-based selection. The supported path
does not feed final scores back into feature/tuning decisions. Arbitrary project
Python can still access files; this is not protected evaluator storage.

## Authored feature pipelines

Use native scikit-learn pipeline steps and project functions for imputation,
encoding, scaling and authored domain features as applicable. Record selected
columns, step order, effective settings, declared feature schema and fitted state.
Fit stateful transformations on training data only and reuse the fitted pipeline
unchanged for validation/test/inference.

Compare authored feature variants with a fixed split, estimator/settings and
metric/direction. Record gains, ties or regressions honestly; no gain is needed
for a valid result. There is no separate FeaturePlan permission language or
baseline/feature authorization gate.

M2 accepts compatible supplied transformers/estimators without toolkit edits or
a versioned registry. Verify supported fit/transform/predict shapes, parameters
and restored fitted state. Comprehensive leakage detection and arbitrary-code
prevention are not promised; tests independently verify supported split/fit scope.

## DVC data and fitted artifacts

DVC versions extracted data, split records and derived datasets; Git tracks DVC
metadata and native stages/lockfiles. Keep content/generated stores out of Git.
MLflow saves fitted pipelines/models and results with links to DVC identities,
committed code/configuration and environment references.

M2 restores available DVC inputs with identity verification and reproduces fitted
transforms/predictions under declared checks. Missing/corrupt required content
fails explicitly. See [execution/reproduction](execution-and-governance.md).

## Deferred acquisition and breadth

Autonomous gap diagnosis, proposals, labeling/synthetic acquisition loops,
authorization/pricing/resource reconciliation and retraining orchestration are
uncommitted roadmap work under US-28/29. Deep-learning preprocessing, tokenization,
image augmentation and general framework registration are also deferred.
The accepted historical closed-loop vision does not add these as MVP prerequisites.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](https://github.com/jimthompson5802/agentic-ml/blob/0a7b64389cf663290d3bf4fc7063aae29ef8f20c/docs/specs/design/data-and-features.md).

<a id="6-data-extraction-and-iterative-acquisition"></a>

<a id="data-extraction-requirements"></a>

<a id="acquisition-strategies"></a>

<a id="acquisition-proposal-contract"></a>

<a id="7-feature-engineering"></a>
