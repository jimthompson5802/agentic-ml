# Experiment: Predict churn

## Objective
```yaml
schema_version: "1.0"
objective: Predict churn using information available at signup.
```

## Data
```yaml
sources: [data/churn.csv]
target: churn
task_type: classification
```

## Features
```yaml
include: [age]
exclude: [customer_id]
guidance: Use age as the initial feature.
availability: At signup, before the outcome.
```

## Evaluation
```yaml
metric: f1_macro
direction: maximize
split:
  strategy: random
  time_column: null
  group_column: null
  validation_fraction: 0.2
  test_fraction: 0.2
  seed: 42
  constraints: Independent rows.
```

## Algorithms
```yaml
mode: use
allowed: [logistic_regression]
```

## Budget
```yaml
max_trials_per_algorithm: 2
max_total_trials: 2
max_runtime_seconds: 60
max_memory_mb: null
max_cost: null
currency: null
```
