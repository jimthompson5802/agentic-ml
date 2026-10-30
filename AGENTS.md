# Agent Instructions

## Audience and requirements

This file guides agents building, testing, and maintaining the agentic-ml harness in this repository. Maintain instructions for agents conducting experiments separately as packaged runtime guidance. Product behavior described below is an implementation and verification obligation for harness developers.

Before implementing a user story, retrieve its GitHub issue, including the complete body and all comments, using the [retrieve-github-issue skill](.agents/skills/retrieve-github-issue/SKILL.md). Identify the milestone, story ID, acceptance criteria, and recorded scope decisions that govern the work.

Use the GitHub issue as the implementation scope. Consult [user stories](docs/specs/user-stories.md) for milestone context and the [harness design](docs/specs/agentic-ml-harness-design.md) for supporting design. Resolve conflicts between the issue and repository specifications before implementing affected behavior. Design examples describe proposed interfaces unless explicitly settled. Before implementing a capability, use the design’s [reading map](docs/specs/agentic-ml-harness-design.md#reading-map-and-document-authority) to read the relevant topic documents, follow related-contract links for affected behavior, and check the applicable milestone, acceptance traceability, and architecture decisions.

Reference the issue and applicable acceptance criterion IDs in the implementation plan and verification evidence. For stories spanning milestones, identify the criteria covered by the current implementation. Record unresolved design decisions before dependent implementation.

This guidance covers Milestones 0–6. Apply capability-specific rules when implementing the milestone that introduces the capability, and preserve them in subsequent milestones. Milestone 99 remains deferred; moving its work into delivery requires an explicit scope decision recorded in the issue and affected plan.

If no GitHub issue is supplied or identifiable, request the issue before starting user-story implementation.

## Development workflow

When starting or resuming development, read [CHECKPOINTS.md](CHECKPOINTS.md) and follow its maintenance rules. Update it at completed work, approval gates, blockers, and before handing work back. Verify its summary against the owning issues, implementation plans, and current working tree before acting.

For GitHub reads and development checks, follow the [repository-local command approval guidance](docs/development.md#repository-local-codex-command-approvals). Command permissions do not approve implementation phases, story acceptance, or publication.

Use Conventional Commits for commit messages: `<type>[optional scope]: <description>` (for example, `docs: update architecture proposal`).

When creating, revising, or executing detailed user-story implementation plans, follow the [planning terminology](README.md#planning-terminology) and [implementation-plan template](docs/templates/user-story-implementation-plan.md). Organize work as milestone → user story → implementation phases → granular tasks. Each implementation phase ends with an explicit developer approval gate; await approval before progressing. Approval of a written plan does not approve its implementation gates.

When scope changes during implementation-plan execution, or discovered constraints require replanning, use the [manage-plan-scope skill](.agents/skills/manage-plan-scope/SKILL.md). Record the change and decision in the affected plan's scope-change history.

When writing pull request bodies, use the target repository's selected pull request template as the authoritative structure unless the user explicitly overrides it. Apply other skills' writing guidance within that structure; their templates must not replace it.

## Python development

Use Python 3.12 or newer and `uv` with the committed lockfile. Keep dependency declarations and the lockfile consistent. Verification must not silently update the lockfile.

Before implementing or modifying Python code, read the [development guide](docs/development.md), including its Python conventions, suppression rules, and shared verification commands. Follow those conventions for naming, typing, docstrings, imports, and error handling.

Record a specific justification for each rule suppression or check exclusion.

Use documented repository commands for tests, linting, formatting checks, type checks, and the development smoke check. Report commands, outcomes, and any checks that could not run. Distinguish macOS verification from unverified platform support.

## Test-driven development

Use TDD for new harness behavior and bug fixes. Derive test cases from the GitHub issue's acceptance criteria. Before writing tests, record the public interfaces under test and what each test boundary covers or misses; confirm these boundaries with the developer through the implementation plan or an explicit review. Reuse confirmed boundaries while they remain applicable.

Work in small vertical slices:

1. **Red:** Write one behavior-focused test and run it. Confirm that it fails because the required behavior is missing or incorrect, rather than because of an unrelated setup error. For bug fixes, reproduce the defect with a failing regression test.
2. **Green:** Implement only the behavior needed to pass that test, then run it and the relevant existing tests.
3. **Repeat:** Add the next behavior through another red–green cycle. Avoid writing all tests first and implementing them as a batch.

Test through public interfaces with independently defined expected results. Prefer observable outcomes over private methods, internal call sequences, or mocks of internal collaborators. Use existing domain terminology and applicable architecture decisions when naming tests and selecting interfaces.

Review refactoring after the behavior is green; keep relevant tests passing while improving structure. Record red and green commands/results in implementation-phase evidence, and complete the required development checks before presenting the phase for approval.

For documentation-only changes or refactoring that preserves behavior, use appropriate checks and existing regression tests instead of manufacturing a failing test. Record why TDD does not apply when the change has no new or corrected executable behavior.

## Problem-solving attempt limit

Make at most three attempts to fix the same problem. An attempt consists of a proposed corrective change followed by verification against the original failure and relevant tests. Track the hypothesis, change, and verification result for each attempt. Treat an unsuccessful verification as a failed attempt; changing tactics or starting a new turn does not reset the count for the same unresolved problem.

If the third attempt fails, stop corrective work on that problem and present the developer with:

- The original problem and the expected behavior or test criteria.
- Each of the three attempts, its rationale, the changes made, and its result.
- Relevant debugging output, including commands, failing tests, error messages, logs, and stack traces. Redact secrets and link to saved output when it is too large to include directly.
- The current working-tree state, remaining uncertainty, and possible next steps for the developer to choose from.

Wait for the developer's direction before making another attempt. Preserve the failed verification evidence for review.

Keep the original test and acceptance criteria intact while fixing a problem. Never weaken assertions, lower thresholds, skip or disable checks, add suppressions to conceal the failure, or introduce a workaround unless the developer explicitly directs that change. Record any such direction and the resulting change in the implementation evidence and affected plan when applicable.

## Package and project boundaries

Implement reusable harness capabilities in the installable package. Verify the boundary with separate experiment-project fixtures: experiment-specific notebooks, configuration, and custom code must work through the installed public interfaces without modifying or importing from a harness checkout.

Preserve `agentic-ml` as the CLI name and `agentic_ml` as the Python import name. Load templates and runtime guidance through installed-package resources.

Verify distribution changes outside the source checkout, using declared runtime dependencies. Check both the directly built wheel and a wheel rebuilt from the source distribution. Verify CLI version output, imports, and packaged resource contents.

Keep development instructions separate from packaged experiment runtime guidance. Add component-level `AGENTS.md` files only when distinct instructions are needed.

## Harness implementation contracts

For each changed capability, derive implementation and test obligations from the GitHub issue and relevant [harness design](docs/specs/agentic-ml-harness-design.md) contracts. Keep detailed product rules in those sources. Apply the following checks to the affected components as their capabilities are introduced:

- **Execution and initialization:** Implement CLI/API use without an agent adapter, conflict-safe initialization, configuration validation before execution, explicit path/working-directory handling, and reproducible execution of saved notebooks. Verify these behaviors through installed-package integration tests.
- **Policy enforcement:** Implement shared validation and executable authorization, access, search-boundary, and budget controls across supported entrypoints. Test bypass attempts from custom code and interactive kernels; Markdown guidance alone does not enforce a boundary.
- **Provenance and restoration:** Implement capture of exact inputs, required uncommitted/untracked source, environment identities, artifacts, and linked MLflow/DVC records. Test checksum verification, missing/corrupted inputs, fitted-component and checkpoint restoration, and preservation of available evidence after unsuccessful execution.
- **Data and evaluation:** Implement versioned split/pipeline contracts, training-only fitting, component registration/persistence, consistent comparisons, and independent evaluation. Test leakage rejection and protected-test isolation beyond API calls. Verify that execution completion, scientific validity, model quality, and developer acceptance remain distinct outcomes.
- **Workflow and recovery:** Implement authenticated, scoped, durable approvals separately from assistant tool permissions. Test pending gates, terminal outcomes, interruption recovery, uncertain submission, duplicate execution/accounting prevention, preserved configuration/guidance, and original producer provenance on reuse.
- **Acquisition:** Implement authorization and source/resource-limit enforcement, dataset validation/versioning, source lineage, synthetic-data identification, consistent comparison protocols, and recovery. Test unauthorized acquisition and limit exhaustion as well as successful acquisition.
- **Agent integration:** Implement adapters against versioned task/result and capability contracts. Verify concrete supported products/interfaces/versions, guidance delivery, cancellation, and adapter interchangeability when required by the issue. Distinguish agent-task cancellation from experiment-run cancellation and document usage-control limitations.

## Runtime guidance development

When implementing packaged runtime guidance or its loader, follow the design's development/runtime instruction boundary. Verify explicit selection mappings, exclusion of development `AGENTS.md` files from automatic harness loading, and preservation of selected contents, ownership, paths, versions/checksums, and load order.

Test conflicting guidance, approved version changes, and restoration of preserved bundles. Document observable external context and capture limitations. Write experiment-use directions in the runtime resources rather than this development file.

## Verification evidence

Verify changed behavior against the applicable acceptance criteria. Include relevant failure and boundary cases alongside successful runs.

Use separate experiment-project fixtures for installation, initialization, execution, tracking, and restoration checks. Verify reproduction against declared output checks or tolerances.

Select tests from the affected implementation contracts above and the harness design's reference acceptance-test datasets. The GitHub issue defines required coverage. Record which acceptance criteria the evidence verifies and identify any verification limitations.

Use small, controlled test datasets and isolated temporary storage for verification. Keep credentials, generated run storage, and external dataset content outside Git; track DVC metadata and manifests where required by the test scenario.
