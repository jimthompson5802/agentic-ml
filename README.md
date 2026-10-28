# Agentic ML

An early-stage project exploring an agent-independent harness for machine learning experimentation and data development.

The proposed harness coordinates coding assistants and specialized ML agents, executes experiments, independently evaluates results, and tracks reproducible evidence. The design supports notebook-centered workflows, user-supplied models and feature preparation, and developer approvals at phase boundaries. It separates the reusable harness package from user-owned experiment repositories.

**This project is in its early days.** The repository currently contains an architecture proposal rather than a working implementation. Its design, interfaces, directory structure, and documentation will change as development progresses.

## Repository contents

- [Architecture proposal](docs/specs/agentic-ml-harness-proposal.md): Scope, architecture and repository diagrams, development phases, custom component support, execution and approval contracts, acceptance criteria, implementation plan, and architecture decisions.
- [Agent instructions](AGENTS.md): Repository conventions for coding agents.

## Proposed direction

- Support tabular ML and deep learning, initially with scikit-learn, LightGBM, and PyTorch.
- Provide reusable orchestration, agent integration, approval handling, execution, and independent evaluation in an installable Python package.
- Keep notebooks, experiment configuration, custom algorithms, and preprocessing in separate user experiment repositories.
- Use MLflow for experiment tracking and DVC for data versioning and reproducible pipelines.
- Support model-improvement and data-improvement loops within approved scope and budgets.

The installation commands and repository layouts in the proposal describe the intended implementation; they are not yet a runnable setup guide.
