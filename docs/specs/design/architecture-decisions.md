# Architecture Decisions

Part of the [harness design](../agentic-ml-harness-design.md). Scope: Architecture Decision Records.

**Related contracts:** Read [interfaces and configuration](interfaces-and-configuration.md); [execution and governance](execution-and-governance.md); [data and features](data-and-features.md); [milestone delivery](milestone-delivery.md) when changing behavior that crosses these boundaries. Consult the [reading map and authority rules](../agentic-ml-harness-design.md#reading-map-and-document-authority) and [architecture decisions](architecture-decisions.md) before implementation.

## 14. Architecture Decision Records

### ADR-001 — Hierarchical Closed-Loop ML Development

**Status: Accepted**

**Decision:** The harness will implement a model-improvement inner loop and data-improvement outer loop. The orchestrator coordinates both, while the harness executes and independently validates actions. Developers approve workflow phase boundaries and acquisition scope changes.

**Rationale:** Poor model performance can reflect insufficient or unrepresentative data, not just inadequate features, architecture, or hyperparameters. Feedback must support both model and dataset improvement.

**Consequences:** Requires data-gap diagnostics, acquisition contracts, dataset versioning, authorization, consistent before/after evaluation, and termination conditions for both loops.

### ADR-007 — GitHub Package Installation and Project Initialization

**Status: Installation decisions accepted; remaining interface details pending**

**Decision:** Initially install the harness as a normal Python package directly from its GitHub repository using `uv`, pinned to a full commit SHA. Use `agentic-ml` as the installed CLI name and retain `agentic_ml` as the Python import name. Users install `uv` and Git, initialize a separate Git/Python project, install the harness into that project's environment, and then run `uv run agentic-ml init`. No separate initializer-tool installation is required. Package-registry distribution is future work.

**CLI naming correction (2026-10-29):** The developer corrected the original CLI spelling to `agentic-ml`, matching the distribution name; the Python import remains `agentic_ml`. This supersedes the earlier `agent-ml` spelling in issue bodies and historical reviews/evidence. Update current entrypoints, tests, guidance, and acceptance-criterion wording without changing criterion IDs or capability scope. No legacy alias is required for this initial implementation.

**Rationale:** Direct GitHub installation supports the separate-repository workflow without requiring package-registry publishing. A full commit pin identifies the exact harness source used by an experiment.

**Consequences:** The repository must build an installable package containing the CLI, templates, and runtime guidance. The initializer preserves existing project files and the pinned dependency. Run provenance records the harness repository URL, full commit SHA, package version, and project lockfile identity. Users need GitHub access at installation/restoration time; the installer may fetch source into its cache, but runtime use requires no manually maintained harness checkout.

**Remaining decisions:** Actual GitHub URL and distribution name, additional Python versions to verify beyond the required Python 3.12 baseline, API compatibility/versioning policy, project/experiment configuration schemas, and CLI/API details beyond `agentic-ml init`.

**Milestone 0 scope clarification (2026-10-29):** Development and testing may install the package from the harness repository. Publishing to PyPI or another package registry is not required. Milestone 0 demonstrates a minimal package: `agentic-ml --version`, `agentic_ml` imports, provisional template and runtime guidance resources, wheel/source-distribution builds, and isolated verification of both the directly built wheel and a wheel rebuilt from the source distribution. This preserves US-31–US-33's acceptance criteria; full-commit-pinned GitHub installation and usable experiment initialization remain Milestone 1 work.

Python 3.12 is the required initial verification baseline; additional verified versions may remain pending. Record the distribution name and repository installation source in the Milestone 0 implementation plan before dependent package configuration. The proposed distribution name `agentic-ml` has not yet been explicitly accepted. Build backend, initial version, and development-tool choices are implementation-plan decisions. Configuration schemas, broader API compatibility/versioning, initialization behavior, and remaining experiment commands do not block Milestone 0 and must be resolved before their dependent capabilities are implemented. Pending ADR-002–006 mechanisms do not block the minimal Milestone 0 package foundation.

### Pending decisions

- **ADR-002:** Expose harness through Python API and CLI initially for developer and interactive coding-assistant use without an adapter. Managed delegation uses verified adapters; consider an MCP server later. Exact commands and managed product/interface choices remain pending.
- **ADR-003:** Start with a lightweight durable state-machine orchestrator; evaluate agent orchestration frameworks if complexity requires.
- **ADR-004:** Hybrid ML operations: standardized capabilities plus sandboxed custom Python code, with project-local registration of user-supplied algorithms and feature preparation through versioned public interfaces. Components may come from project code or pinned dependencies; using them requires no harness modifications. Supplied code is immutable by default, with explicit developer approval required to change immutable components. This proposed decision remains pending.
- **ADR-005:** Choose configurable project-associated DVC storage, MLflow backend/artifact storage, and durable workflow-state configuration, including single-machine local defaults; DVC data versioning/pipelines and MLflow experiment tracking are selected stack components.
- **ADR-006:** Define the authorization and isolation model for data connectors, generated code, and interactive notebook kernels, including protected-test isolation, project/harness filesystem boundaries, assistant-process/tool/workspace access in interactive and managed modes, protected approval/evaluator resources, and a developer-authenticated approval channel. The mechanism remains pending; it must enforce each milestone’s required access and authorization controls before the governed capability is delivered. Milestone 1 requires execution/extraction boundaries; Milestone 2 requires protected-test isolation for predictive feature comparison; Milestone 3 adds authorized independent final evaluation; Milestone 4 extends boundaries to managed agent and interactive work.
- **ADR-007 remaining details:** Finalize the repository URL/distribution name, additional Python versions to verify beyond the required Python 3.12 baseline, API compatibility/versioning, configuration schemas, and remaining CLI/API commands; GitHub installation, full commit pinning, and the agentic-ml CLI/init sequence are selected above.

