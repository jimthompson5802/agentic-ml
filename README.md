# Agentic ML

An early-stage project exploring an agent-independent harness for machine learning experimentation and data development.

The proposed harness coordinates coding assistants and specialized ML agents, executes experiments, independently evaluates results, and tracks reproducible evidence. The design supports notebook-centered workflows, user-supplied models and feature preparation, and developer approvals at workflow phase boundaries. It separates the reusable harness package from user-owned experiment repositories.

**This project is in its early days.** The repository currently contains a proposed design rather than a working implementation. Its design, interfaces, directory structure, and documentation will change as development progresses.

## Repository contents

- [User stories](docs/specs/user-stories.md): Authoritative product requirements and acceptance criteria, organized into six milestones with stable story and criterion IDs.
- [Harness design](docs/specs/agentic-ml-harness-design.md): Supporting architecture, workflow phases, custom component support, execution and approval contracts, acceptance-criteria traceability, implementation plan, and architecture decisions.
- [Agent instructions](AGENTS.md): Repository conventions for coding agents.
- [User-story implementation-plan template](docs/templates/user-story-implementation-plan.md): Detailed task planning, verification evidence, and developer approval gates.

## Planning terminology

- **Milestone:** A cumulative, usable product increment comprising user stories. A target date is optional. Milestones 1–6 define the committed product scope; Milestone 7 is an optional future roadmap item.
- **Implementation phase:** A group of granular tasks within a user story's implementation plan, ending with an explicit developer approval gate.
- **Workflow phase:** A stage of an ML experiment run through the harness, such as feature engineering or final evaluation.
- **Approval gate:** A developer decision permitting progression after reviewing the required evidence.

Implementation plans follow **milestone → user story → implementation phase → tasks**. Identify each implementation phase by story and local phase number, for example, **US-11 / Implementation Phase 2: Build extraction**. For stories delivered across milestones, also identify the milestone and acceptance criteria covered by the plan.

Each implementation phase specifies its tasks, required review evidence, and approval criteria. Complete the tasks and present the evidence, then pause until the developer explicitly approves progression. Requested changes remain within the current implementation phase. These development approvals are separate from the workflow phase approvals enforced by the harness during an experiment. Always qualify “phase” as “implementation phase” or “workflow phase” in prose.

## Proposed direction

- Support tabular ML and deep learning, initially with scikit-learn, LightGBM, and PyTorch.
- Provide reusable orchestration, agent integration, approval handling, execution, and independent evaluation in an installable Python package.
- Keep notebooks, experiment configuration, custom algorithms, and preprocessing in separate user experiment repositories.
- Use MLflow for experiment tracking and DVC for data versioning and reproducible pipelines.
- Support model-improvement and data-improvement loops within approved scope and budgets.

The installation commands and repository layouts in the design document describe the intended implementation; they are not yet a runnable setup guide.
