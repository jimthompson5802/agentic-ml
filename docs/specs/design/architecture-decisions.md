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

**Installation source/name resolution (2026-10-30):** The accepted US-31 plan and implemented package metadata establish `https://github.com/jimthompson5802/agentic-ml.git` and distribution `agentic-ml`; these are settled implementation inputs for US-01. Full-SHA installation verification is recorded in [US-01 IP1 evidence](../../verification/us-01-ip1.md).

**Remaining decisions:** Additional Python versions to verify beyond the required Python 3.12 baseline, API compatibility/versioning policy, project/experiment configuration schemas, and CLI/API details beyond `agentic-ml init`.

**Milestone 0 scope clarification (2026-10-29):** Development and testing may install the package from the harness repository. Publishing to PyPI or another package registry is not required. Milestone 0 demonstrates a minimal package: `agentic-ml --version`, `agentic_ml` imports, provisional template and runtime guidance resources, wheel/source-distribution builds, and isolated verification of both the directly built wheel and a wheel rebuilt from the source distribution. This preserves US-31–US-33's acceptance criteria; full-commit-pinned GitHub installation and usable experiment initialization remain Milestone 1 work.

Python 3.12 is the required initial verification baseline; additional verified versions may remain pending. Record the distribution name and repository installation source in the Milestone 0 implementation plan before dependent package configuration. The distribution name `agentic-ml` was explicitly accepted in the US-31 plan; the older pending-name statement is superseded by that recorded decision. Build backend, initial version, and development-tool choices are implementation-plan decisions. Configuration schemas, broader API compatibility/versioning, initialization behavior, and remaining experiment commands do not block Milestone 0 and must be resolved before their dependent capabilities are implemented. Pending ADR-002–006 mechanisms do not block the minimal Milestone 0 package foundation.

### Pending decisions

- **ADR-002:** Expose harness through Python API and CLI initially for developer and interactive coding-assistant use without an adapter. Managed delegation uses verified adapters; consider an MCP server later. Exact commands and managed product/interface choices remain pending.
- **ADR-003:** Start with a lightweight durable state-machine orchestrator; evaluate agent orchestration frameworks if complexity requires.
- **ADR-004:** Hybrid ML operations: standardized capabilities plus sandboxed custom Python code, with project-local registration of user-supplied algorithms and feature preparation through versioned public interfaces. Components may come from project code or pinned dependencies; using them requires no harness modifications. Supplied code is immutable by default, with explicit developer approval required to change immutable components. This proposed decision remains pending.
- **ADR-005:** Choose configurable project-associated DVC storage, MLflow backend/artifact storage, and durable workflow-state configuration, including single-machine local defaults; DVC data versioning/pipelines and MLflow experiment tracking are selected stack components.
- **ADR-006:** Define the authorization and isolation model for data connectors, generated code, and interactive notebook kernels, including protected-test isolation, project/harness filesystem boundaries, assistant-process/tool/workspace access in interactive and managed modes, protected evaluator resources and approval channels. For the current toolkit experiment version, use unauthenticated scoped approval records under US-03-SC-01 below; authenticated approval is deferred. Development/testing gates are unchanged. Other mechanisms remain pending; it must enforce each milestone’s required access and authorization controls before the governed capability is delivered. Milestone 1 requires execution/extraction boundaries; Milestone 2 requires protected-test isolation for predictive feature comparison; Milestone 3 adds authorized independent final evaluation; Milestone 4 extends boundaries to managed agent and interactive work.
- **ADR-007 remaining details:** Verify additional Python versions to verify beyond the required Python 3.12 baseline, API compatibility/versioning, configuration schemas, and remaining CLI/API commands; GitHub installation, full commit pinning, and the agentic-ml CLI/init sequence are selected above.


### US-02 IP1 — Initialization-specific decision proposals

**Status: Initialization slice accepted at the US-02 IP1 gate, 2026-10-30 (“i approve ip1; commit changes and I authorize ip2”).** These bounded refinements do not accept ADR-002/005/006/007 in full. The [IP1 contract report](../../verification/us-02-ip1.md) supplies concrete interfaces, shapes, alternatives resolved and verification boundaries.

- **ADR-002/007 interface slice:** Keep `agentic-ml init` and expose a typed `agentic_ml.initialization` API with explicit project root, conflict diagnostics and stage results. Use schema version 0.1 for draft initialization configuration. Prefer explicit unconfigured choices over guessed experiment decisions. Preserve existing project files and the full-SHA harness source; use lossless additive TOML edits and a setup journal because external tools cannot participate in one filesystem transaction.
- **ADR-005 storage slice:** Local DVC metadata/cache and a configured local filesystem remote; explicit SQLite MLflow backend and filesystem artifact root; initial durable JSON state that grants no approval. Support explicit external local paths. This avoids service provisioning while retaining project-associated configuration. Remote deployments and complete workflow recovery remain pending.
- **ADR-006 setup slice:** Setup flags authorize only validated project/store writes. No implicit raw-data reads, kernel starts, agent authentication, experiment runs or approval grants. Reject symlink/overlap/conflict destinations and credential-bearing URI settings. A setup journal/lock is not execution isolation or an approval service; those enforcement mechanisms remain pending before their governed capabilities ship.
- **Milestone dependency slice:** Initialize CPU tabular/scikit-learn and notebook/storage dependencies; later framework stories supply LightGBM/PyTorch integrations. Retain nbclient/ipykernel; editor tooling is installed separately. Joint resolution and installed behavior must be verified in subsequent phases, not inferred from this design record.

**Consequences:** IP2–IP4 implement only after the IP1 gate approves the linked contracts and refined public test boundaries. Invalidated contracts require scope review. No current executable capability or broader accepted decision changes here.

### US-03 IP1 — Input-resolution and delegated-approval proposals

**Status: Bounded IP1 contracts approved by developer “i approve the changes” (2026-10-31).
Unauthenticated experiment approval scope approved by US-03-SC-01.** These bounded
decisions do not accept ADR-002/006/007 in full. The
[US-03 contract report](../../verification/us-03-ip1.md) specifies exact fields,
public interfaces, precedence, preservation and verification boundaries.

- **ADR-002/007 input slice:** Add `plan resolve/inspect/verify`, typed
  `agentic_ml.planning` interfaces and strict version 1.0 Markdown/YAML/schema
  contracts. Resolve structured decisions without natural-language inference.
  Keep initialization 0.1 drafts unchanged; users supply reviewed 1.0 inputs at
  separate paths. Store exact sources and a deterministic SHA-256 plan identity
  in immutable local bundles. Readiness is recomputed and grants no execution
  permission; registry/default/candidate validation remains US-05.
- **ADR-006 experiment approval slice — scope approved 2026-10-31:** Replace the
  initial SSH-signature/protected-policy/distinct-OS-identity proposal with
  project-local unauthenticated approval/revocation records. Preserve exact
  project/experiment/plan/decision binding and current revocation/staleness
  checks; record `authentication: none` and self-declared reviewer. No keys,
  protected system directory or special host. An agent or other workspace writer
  can fabricate records or alter history; authorship and tamper resistance are
  not established by checksums or record validation. Authenticated approval is
  deferred future hardening; future US-23-AC-02 remains undelivered.
- **Verification:** IP4 must test matching/missing/malformed/stale/revoked and
  wrong-scope records through installed CLI/API on both wheel paths. Removed
  signature and separate-principal tests are deferred assurance, not passing
  evidence. Full-suite/distribution and other applicable checks remain required.
- **Development/testing boundary:** The developer clarified that unauthenticated
  approval applies only when a data scientist uses the toolkit in an experiment.
  All existing harness development/testing approval gates, test-boundary review,
  verification, story acceptance and publication requirements remain unchanged.
  General execution/kernel and protected-test isolation stay with their owning
  capabilities; experiment approval records cannot approve harness changes.

**Decision references:** Developer “Authenticated approval is a bit much for this
version of the toolkit. For now let's use unauthenticated approval in
experiments.” and “The change in authentication is only for when a data scientist
is using the toolkit in an experiment. I still want the existing approval gates
currently in place for development and testing.” See
[US-03-SC-01](../../plans/milestone-1-us-03.md#us-03-sc-01--unauthenticated-experiment-approvals-2026-10-31).

**Consequences:** Revised concrete contract and public test boundaries approved.
IP2 execution awaits explicit authorization. No executable behavior or future authenticated capability is delivered here.
