# Agentic ML

A local ML experimentation toolkit for scientist-directed Python and notebook work,
including help from an external coding assistant. The MVP targets tabular
classification/regression with scikit-learn, MLflow results and native DVC data/
pipeline reproduction in a separate experiment project.

“Toolkit” and “harness” name the same software; new documentation uses “toolkit”.

**Current implementation:** pinned installation, conflict-safe initialization with
draft configuration/local stores, strict versioned planning and scoped
unauthenticated approvals, semantic configuration/candidate validation, and
local pandas extraction with provenance.
Training, tuning, integrated run tracking, DVC stages/reproduction and the complete
assistant walkthrough remain planned. Initialization does not yet create a
runnable end-to-end experiment.

**Revised delivery:** M1 completes a classification experiment with assistant help;
M2 adds regression, customization, fresh-kernel notebooks and committed-project
reproduction. The scientist owns the assistant session; managed agents, required
experiment phase approvals, OS isolation and durable orchestration are deferred.
Toolkit development/testing gates remain required. Gate 2 approved this scope;
design and story scope were published through
[PR #57](https://github.com/jimthompson5802/agentic-ml/pull/57), and the GitHub
backlog is synchronized. Publication does not deliver unfinished experiment APIs.

Start with the [current installation/setup guide](docs/experiment-setup.md),
[configuration validation guide](docs/configuration-validation.md), and
[pandas extraction guide](docs/extraction.md) for implemented
commands and Python APIs. The [assistant-supported walkthrough](docs/specs/example-walkthrough.md)
describes the required MVP scenario and explicitly marks planned operations.

## Contributor setup

Start with the [development guide](docs/development.md) for Python 3.12, uv, locked dependencies, coding conventions, and local checks. Development tooling, the minimal package, and `agentic-ml --version` are available. Fresh-checkout macOS verification passed; see the [evidence](docs/verification/us-31-ip2.md). The [development CI workflow](.github/workflows/ci.yml) is configured for Linux/Python 3.12; the [first hosted PR run passed](docs/verification/us-32-ip2.md). Failure/correction cases are verified; the [default-branch push run passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). See [CI checks and logs](docs/development/ci.md#development-ci-and-diagnostic-logs).

## Repository contents

- [User stories](docs/specs/user-stories.md): Authoritative product and technical environment requirements and acceptance criteria, covering the development foundation (Milestone 0), revised MVP increments (Milestones 1–2), the uncommitted platform roadmap, ongoing technical environment improvements (Milestone 50), and deferred enhancements (Milestone 99), with stable story and criterion IDs.
- [Toolkit design](docs/specs/agentic-ml-harness-design.md): MVP architecture, implemented/planned interfaces, data/features, execution/tracking/reproduction, decisions and criterion coverage. Start with its reading map.
- [Example walkthrough](docs/specs/example-walkthrough.md): Required scientist-directed assistant scenario, with prompts, expected evidence and explicit implemented-versus-planned commands.
- [Reviews](docs/reviews/): Reconciliation findings and documentation dispositions assessing alignment between the user stories and design.

## Planning terminology

- **Milestone:** A group of user stories. A target date is optional. M0 records the accepted development foundation; M1–2 define the revised MVP delivery order. Historical M3–6 remain migration context for the uncommitted roadmap. Milestone 50 collects ongoing technical environment improvements as they are identified, outside the product delivery sequence. Milestone 99 groups deferred enhancements without committing their order.
- **Implementation phase:** A group of granular tasks within a user story's implementation plan, ending with an explicit developer approval gate.
- **Workflow phase:** An activity within an ML experiment, such as feature engineering or final evaluation. The basic MVP does not require toolkit approval between these activities.
- **Approval gate:** A developer decision permitting progression after reviewing the required evidence.

Implementation plans follow **milestone → user story → implementation phase → tasks**. Identify each implementation phase by story and local phase number, for example, **US-11 / Implementation Phase 2: Build extraction**. For stories delivered across milestones, also identify the milestone and acceptance criteria covered by the plan.

Each implementation phase specifies its tasks, required review evidence, and approval criteria. Complete the tasks and present the evidence, then pause until the developer explicitly approves progression. Requested changes remain within the current implementation phase. These development approvals remain required; the basic MVP experiment workflow does not impose runtime phase approvals. Existing explicit approval APIs retain their strict contracts. Always qualify “phase” as “implementation phase” or “workflow phase” in prose.

## MVP direction

- Local CSV/Parquet extraction and authored scikit-learn pipelines/estimators.
- Training-only preprocessing, consistent splits/metrics, bounded trials and
  separate final testing.
- MLflow owns run/model records; DVC owns data versions, stage execution and cache.
- Scientist-owned coding assistant prepares, runs, inspects and revises project
  code through installed public interfaces; no toolkit-managed adapter required.
- Reproduction uses committed code/configuration, locked dependencies and DVC
  inputs. Trusted local code is assumed; comprehensive security/recovery and
  acquisition platform features remain uncommitted roadmap work.

Build and check distributable packages using the [distribution verification commands](docs/development/distribution.md#distribution-builds-and-installed-verification). Both wheel paths pass locally on macOS and in hosted Linux/Python 3.12 CI, including verified build/resource failure diagnostics; see [US-33 evidence](docs/verification/us-33-ip3.md). US-33 is complete and developer-accepted.

Check extracted DataFrames and guard dependent operations with the [data-quality guide](docs/data-quality.md).
