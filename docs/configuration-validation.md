# Configuration and candidate validation

Install a reviewed validation-capable revision in your experiment project using
[the setup guide](experiment-setup.md). Initialization produces 0.1 drafts;
complete and migrate them to the planning 1.0 contract before resolving a plan.
The structural planner permits illustrative algorithm names. Semantic validation
requires registered metadata.

The built-in registry and validation interface are version 1.0. They provide
`dummy_classifier` for classification and `dummy_regressor` for regression,
using the `sklearn_dummy_scalar` 1.0 metadata profile based on scikit-learn 1.7.2.
These profiles describe scalar parameters; they do not supply training adapters.
The classifier parameters are `strategy` (default `prior`), `random_state`
(default null), and `constant` (default null). The regressor parameters are
`strategy` (default `mean`), `constant` and `quantile` (both default null).
Constant strategies require a non-null constant; quantile strategy requires a
non-null quantile. Booleans are distinct from integers; integer ranges require
integer candidate values. Bounds include their endpoints, categories cannot be
empty, and logarithmic bounds must be positive.

For example, select `dummy_classifier` in your brief and use this search file:

```yaml
schema_version: "1.0"
algorithms:
  dummy_classifier:
    fixed: {strategy: prior}
    search:
      random_state: {type: integer, min: 1, max: 2, scale: linear}
```

Resolve the completed experiment inputs, then use the returned `plan_id` below.
Replace `/absolute/project`, `sha256:PLAN_HEX` and `sha256:VALIDATION_HEX` with your
project and returned identities. Run the installed environment's executable:

```sh
/absolute/project/.venv/bin/agentic-ml plan resolve --project-root /absolute/project --experiment experiments/baseline/experiment.yaml
/absolute/project/.venv/bin/agentic-ml config validate --project-root /absolute/project --plan-id sha256:PLAN_HEX
/absolute/project/.venv/bin/agentic-ml config inspect --project-root /absolute/project --validation-id sha256:VALIDATION_HEX
/absolute/project/.venv/bin/agentic-ml candidate validate --project-root /absolute/project --validation-id sha256:VALIDATION_HEX --candidate candidate.json
```

Save this as project-relative `candidate.json`:

```json
{"schema_version":"1.0","algorithm":"dummy_classifier","parameters":{"random_state":1}}
```

The accepted candidate contains `strategy: prior`, `random_state: 1` and
`constant: null`. Missing searched parameters are rejected. Fixed values cannot
change, and omitted registry defaults remain untunable. A candidate with
`random_state: 1.0` is rejected with an actionable field diagnostic.

Equivalent public Python calls work from project code or notebooks:

```python
from pathlib import Path
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    inspect_validation,
    validate_candidate,
    validate_configuration,
    validate_registry,
)

root = Path("/absolute/project")
registry = validate_registry()
configuration = validate_configuration(ConfigurationRequest(root, "sha256:PLAN_HEX"))
if configuration.status == "valid":
    assert configuration.validation_id is not None
    candidate = validate_candidate(
        CandidateRequest(
            root, configuration.validation_id, "dummy_classifier", {"random_state": 1}
        )
    )
    print(candidate.status, candidate.parameters, candidate.diagnostics)
    inspection = inspect_validation(
        project_root=root, validation_id=configuration.validation_id
    )
else:
    print(configuration.diagnostics)
```

Configuration and candidate commands emit JSON: exit 0 is valid, 2 is blocked,
and 1 is an operational failure reported on stderr. Diagnostics identify the
field, cause and correction. Optional `config validate --registry metadata.yaml`
selects additive declarative metadata relative to the explicit project root;
registrations cannot override built-ins or load project code. Project component
settings and entrypoints are not automatically loaded. `validate_registry()`
exposes the complete parameter specifications and compatibility rules.

Immutable bundles under `.agentic-ml/validations/` preserve effective parameters,
registry defaults/checksum, selected source bytes, plan/environment identities,
harness origin, metadata adapter version, library reference version and observed
installed library version. Missing libraries are recorded explicitly; validating
metadata does not install or import a training framework. Inspection and candidate
validation recheck integrity and currentness. Source, lock, registry or observed
environment drift blocks reuse; explicitly resolve/revalidate current inputs
instead of editing preserved evidence.

Validation sets `execution_authorized: false`. It creates no training run or
execution approval. Future Python, notebook and custom-code submission entrypoints
must revalidate the current plan, registry, configuration and candidate before
training side effects, and independently enforce authorization, access and budgets.
Calling these APIs from an unrestricted kernel does not isolate arbitrary code or
prevent users bypassing them. Dataset-dependent compatibility remains future work.
