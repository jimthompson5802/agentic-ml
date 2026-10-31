# Agentic ML

An early-stage project exploring an agent-agnostic harness for machine learning experimentation and iterative data improvement.

The proposed harness provides reusable orchestration, experiment execution, independent evaluation, and reproducible evidence tracking. Developers can use it interactively through coding assistants or delegate work to managed agents. It supports notebook-centered workflows, user-supplied models and preprocessing, and developer approvals at workflow phase boundaries. The harness is installed as a Python dependency in separate, user-owned experiment repositories.

**This project is in its early days.** The repository currently contains a proposed design rather than a working implementation. Its design, interfaces, directory structure, and documentation will change as development progresses.

For a separate experiment project, follow the [installation and initialization guide](docs/experiment-setup.md). Initialization supplies draft inputs, a synchronized environment and local storage. Managed experiment execution remains subsequent work.

## Contributor setup

Start with the [development guide](docs/development.md) for Python 3.12, uv, locked dependencies, coding conventions, and local checks. Development tooling, the minimal package, and `agentic-ml --version` are available. Fresh-checkout macOS verification passed; see the [evidence](docs/verification/us-31-ip2.md). The [development CI workflow](.github/workflows/ci.yml) is configured for Linux/Python 3.12; the [first hosted PR run passed](docs/verification/us-32-ip2.md). Failure/correction cases are verified; the [default-branch push run passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). See [CI checks and logs](docs/development.md#development-ci-and-diagnostic-logs).

## Repository contents

- [User stories](docs/specs/user-stories.md): Authoritative product requirements and acceptance criteria, covering the development foundation (Milestone 0), product increments (Milestones 1–6), and deferred enhancements (Milestone 99), with stable story and criterion IDs.
- [Harness design](docs/specs/agentic-ml-harness-design.md): Supporting architecture, workflow phases, custom component support, execution and approval contracts, acceptance-criteria traceability, milestone delivery, and architecture decisions. Start with its reading map to find the detailed topic documents.
- [Example walkthrough](docs/specs/example-walkthrough.md): A data scientist's end-to-end model-building workflow, including example commands, coding-assistant prompts, notebooks, and approval gates.
- [Reviews](docs/reviews/): Reconciliation findings and documentation dispositions assessing alignment between the user stories and design.

## Planning terminology

- **Milestone:** A cumulative, usable product increment comprising user stories. A target date is optional. Milestones 0–6 define the delivery sequence. Milestone 99 groups deferred enhancements without committing their order.
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

Build and check distributable packages using the [distribution verification commands](docs/development.md#distribution-builds-and-installed-verification). Both wheel paths pass locally on macOS and in hosted Linux/Python 3.12 CI, including verified build/resource failure diagnostics; see [US-33 evidence](docs/verification/us-33-ip3.md). US-33 is complete and developer-accepted.
