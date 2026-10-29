# Data and Features

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Data Extraction and Iterative Acquisition, Feature Engineering.

**Related contracts:** Read [interfaces and configuration](interfaces-and-configuration.md); [execution and governance](execution-and-governance.md); [acceptance traceability](acceptance-traceability.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 6. Data Extraction and Iterative Acquisition

### Data extraction requirements

- Connect to local CSV/Parquet, SQL, and object storage initially; add APIs later.
- Discover source schemas and metadata without unrestricted data exposure.
- Execute approved extraction queries and sampling plans.
- Version extracted datasets with DVC; capture source identity, query, parameters, extraction time, checksums, and permissions metadata in associated manifests. Commit DVC metadata to Git; store dataset content in the DVC cache and configured remote storage.
- Validate schema, row counts, nulls, types, duplicates, and other configured quality rules.
- Enforce least-privilege access, source allowlists, network restrictions, and cost/record limits.

### Acquisition strategies

- Additional observations from approved sources.
- Targeted sampling for underrepresented classes or data slices.
- Additional feature columns or related datasets.
- Human or external labeling workflows.
- Active learning: select informative unlabeled examples.
- Data augmentation and synthetic data, explicitly labeled and tracked as distinct from observed data.

### Acquisition proposal contract

```yaml
proposal:
  id: acquisition-001
  reason: underrepresented_class
  evidence:
    affected_class: minority_class
    current_samples: 250
    observed_recall: 0.61
  acquisition:
    strategy: targeted_sampling
    source: approved_training_database
    target_additional_samples: 500
  expected_benefit:
    hypothesis: improve_minority_class_recall
    metric: recall
  constraints:
    max_records: 500
    max_runtime_minutes: 15
  approval:
    required: true
```

The predicted benefit is a hypothesis, not a guarantee. Compare before/after training with consistent evaluation protocols. Never use protected final-test feedback to guide acquisition. Changes to evaluation protocols require separate approval.

## 7. Feature Engineering

The feature engineering engine must:

- Propose and execute missing-value handling, encoding, scaling, feature construction, selection, and dimensionality reduction.
- Support domain-specific transformations and custom code.
- Track feature definitions, fitted preprocessors, parameters, versions, and dependencies.
- Fit stateful transformations only on training data; apply unchanged to validation/test data.
- Compare candidate feature sets for predictive performance against a fixed approved baseline feature set using the same fixed approved reference estimator, estimator settings, metric, and split protocol. Record gains, ties, or regressions according to the metric optimization direction.
- Support deep-learning preprocessing, image augmentation, tokenization, and PyTorch datasets where relevant.
- Make transformations reusable for inference without requiring model deployment in the initial release.

Milestone 2 supplies the minimal estimator training, prediction, and independent validation-metric computation needed for feature comparison. Approve and record the baseline feature set, reference estimator/settings, metric/direction, and split protocol before candidate comparison. Fit preprocessing and the estimator only on approved training partitions, score only on approved validation partitions, and enforce protected-test isolation for experiment code and exploratory kernels. Apply execution authorization, resource budgets, independent leakage/result checks, and existing run-evidence contracts to these runs. Preserve baseline/candidate feature identities, estimator code/dependency identities and settings, fitted artifacts, predictions, scores, and data/split lineage so comparisons can be reviewed and reproduced. A candidate need not improve to produce a valid comparison; an improvement claim must follow the recorded metric direction. Algorithm selection and hyperparameter search remain in Milestone 3.

Experiment-specific transformations belong in the experiment repository's notebooks or helper modules. Code shared across experiments in that repository belongs in its own Python package. Generic feature-engineering capabilities belong in the harness package; promoting project code into the harness is a separate development change.

Feature preparation supports user-supplied stateless transformations and stateful preprocessors. Stateful preprocessors expose separate fitting and transformation operations: fitting receives only the approved training partition, and the fitted state is reused unchanged for validation, test, and inference.

Users may require a supplied preparation pipeline or explicitly delegate selection and modification to the agent. The resolved feature plan records component order, effective parameters, input/output schemas, fitting scope, and whether agent modifications are permitted.

Preserve the preparation code, fitted state, dependencies, and output feature schema as run artifacts. Supplied pipelines must satisfy the same leakage, reproducibility, and lineage checks as generated pipelines.

