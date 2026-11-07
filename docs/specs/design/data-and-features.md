# Data and Features

Active design 0.15; [authority](../agentic-ml-harness-design.md).
Owns US-11/12/13/14/15/16 requirements in the revised
[stories](../user-stories.md). These data/feature operations are planned, not
implemented by current configuration-validation APIs.

## Local extraction and quality

Developer-directed design refinement, 2026-11-07: use pandas DataFrame as the
native tabular representation for extraction and the basis for feature
engineering. Project-owned pandas functions use read_csv/read_parquet, column
selection, boolean masks and merge/join directly. Do not introduce toolkit
source/request/result classes, predicate/join classes or a separate operation
language. Toolkit helpers may record provenance and publish output using native
objects and ordinary dictionaries. The proposed component interface and review
status are in [the extraction contract](../../extraction.md) and
[US-11-SC-01](../../plans/milestone-1-us-11.md#scope-change-history).

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

US-12 issue #15's [concrete quality contract](../../data-quality.md) was approved
at Gate 1 on 2026-11-07 UTC by developer “i approve ip1; commit”. It specifies pandas-based checks,
plain reports and a synchronous helper that blocks a dependent project operation
on required-check failure. The public `agentic_ml.data_quality` API is implemented with Gate 2 approval;
IP3 installed checks pass; Gate 3 is approved; issue #15 AC-01/05 accepted on 2026-11-07 UTC. Assessment and
partitions retain issue #19 ownership; this proposal does not change that scope.
Developer-directed US-12-SC-01 also permits explicit empty rules: report
`not_checked` and allow the operation, without claiming quality validation passed.

## Reuse existing assessment and partition capabilities

Developer-directed refinement, 2026-11-07: use scikit-learn wherever it provides
the required functionality. Do not implement custom splitting, shuffling,
stratification, allocation/rounding, preprocessing or model-selection algorithms
that duplicate scikit-learn. Use its public APIs and document the effective
parameters and installed version. New toolkit-specific functionality for
assessment or partitioning must be identified with its requirement, the existing
library capability considered, and the remaining gap, then discussed with the
developer before its contract or implementation is approved.

Use pandas' existing descriptive capabilities for assessment of native DataFrames:
[`describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
for summaries,
[`isna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html)
with native aggregations for missingness, and
[`value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
for categorical/target counts and proportions. Reuse native semantics and make
selected options explicit. Do not create a custom statistics engine or force
these descriptive operations into an unrelated scikit-learn estimator interface.
Selecting report fields and handling their serialization are separate integration
decisions, not authorization for a new assessment API or reporting framework.

### Proposed toolkit integration requiring discussion

Developer selected only `assess_data` and `create_partitions` under
[US-12-19-SC-03](../../plans/milestone-1-us-12-assessment-splits.md#us-12-19-sc-03--retain-two-helpers-project-owned-persistence-2026-11-07-utc).
Project code owns JSON save/load. Developer “i approve ip1; commit changes”,
2026-11-07 UTC, approved detailed contracts/policies and public test boundaries
at Gate 1; implementation remains unstarted. The confirmed integration is:

| Requirement | Existing capability to reuse | Remaining decision for developer discussion |
|---|---|---|
| Recorded two-way (train/test) or three-way (train/validation/test) partitions | scikit-learn `train_test_split` supplies two subsets; `create_partitions` composes native calls for three-way layout | Settings, split order, sizes and random states confirmed in the IP1 contract. Native rounding/errors remain authoritative. |
| Record exact membership and source identity (AC-03) | Native split rows, project JSON files and subsequent DVC ownership | `create_partitions` returns the record; project owns save/load, saved-document validation and old/current identity comparison. Native Parquet identity confirmed for implementation; stability evidence remains IP3. |
| Validate explicit supplied membership (AC-03) | Native pandas index/set operations for membership, duplicates and intersections | String/integer IDs, complete/nonempty coverage and membership/disjointness policies confirmed in the IP1 contract. |
| Present assessment results (AC-02) | Native pandas outputs and serialization | `assess_data` fields/scalar conversion confirmed at Gate 1. Project owns persistence. |

No custom statistical or splitting algorithm has been identified as necessary.
The owning [issue #19 plan](../../plans/milestone-1-us-12-assessment-splits.md)
owns the approved contract and separate authorization before executable work.
Existing accepted extraction/quality APIs and their evidence remain intact.
Project-loaded layout/membership can enter `create_partitions` supplied mode for
validation/reconstruction. This does not validate the entire saved record or
automatically detect changed values under valid IDs. Saved-layout JSON round-trip
remains required project evidence; toolkit file/restoration guarantees are removed.

## Reproducible partitions

Support explicitly selected two-way (train/test) and three-way
(train/validation/test) layouts for both seeded generation and supplied
memberships. Record the selected layout, exact membership and source-data
identity. Two-way layouts contain only train and test; no validation partition
or empty placeholder is required. Validate partition names against the selected
layout, disjoint rows and target alignment; saved records retain the selected
layout and reject layout/membership mismatches. Accept explicit user-provided
partitions for time/group-sensitive tasks, with recorded constraints and overlap
checks; automatic time/group split algorithms are not required by this MVP.

Generate ordinary seeded holdouts using
[`sklearn.model_selection.train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
or the appropriate native scikit-learn splitter. Use explicit integer
`random_state` values; expose/record native `shuffle` and `stratify` choices
without silently adding a policy. Two-way layout uses a native split directly.
For three partitions, a documented composition
of native splits can reserve test rows and then split the remainder into train
and validation. Exact composition/ratios are subject to the discussion above;
do not invent a replacement allocation or rounding algorithm. Record actual
membership as well as settings, input order/identity and library version; a seed
alone does not identify the original partitioned data.

Project-owned time/group partition generation may use appropriate native
scikit-learn capabilities such as `GroupShuffleSplit` or `TimeSeriesSplit`.
These address different protocols: group-aware holdouts and ordered time-series
cross-validation respectively. Do not assume successive split outputs form three
disjoint partitions or silently reinterpret cross-validation folds as final
train/validation/test sets. See the
[scikit-learn splitting guide](https://scikit-learn.org/stable/modules/cross_validation.html).
Toolkit-managed automatic time/group generation remains outside this issue's
required scope; accept explicit memberships as already specified.

Training/preprocessing receives training rows. Three-way experiments use
validation rows for development; two-way preparation does not introduce a
validation set or authorize tuning against final-test rows. Experiments requiring
selection need an appropriate development evaluation strategy within training
data or a separate validation partition, defined by the consuming story.
This component does not add cross-validation execution. Final testing follows
development/selection where applicable. The supported path
does not feed final scores back into feature/tuning decisions. Arbitrary project
Python can still access files; this is not protected evaluator storage.

## Authored feature pipelines

Use DataFrames as the extraction-to-feature boundary and ordinary pandas
functions for authored tabular features. Native pandas operations retain their
own semantics; there is no toolkit dataframe or feature wrapper. This design
foundation does not authorize feature implementation under US-11.

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
