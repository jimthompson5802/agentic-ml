---
name: reconcile-stories
description: Reconcile design documents against a repository's authoritative user stories or requirements. Use when checking alignment, identifying coverage gaps or scope drift, or proposing document corrections.
---

# Reconcile Stories and Design

Compare authoritative product requirements with supporting design documents, preserving the repository's source authority, terminology, and delivery conventions. Default invocation produces a report; applying corrections requires authorization.

## Resolve inputs and authority

Resolve the active repository from the user's working directory, independently of where this skill is installed. In a Git checkout, use `git rev-parse --show-toplevel`. Resolve repository-relative input paths against that root and preserve explicit absolute paths.

Use sources explicitly identified by the user or active session first. Otherwise read applicable repository instructions and the README, following pointers to authoritative stories or requirements and supporting architecture or design documents. If those pointers are insufficient, use targeted file and text searches to find candidates. Select sources only when their roles and review boundaries are clear; ask for missing paths or authority decisions when ambiguity would change the result. This skill assumes no repository name, specification path, or document title.

Support requirements and designs split across multiple files. Record which sources define product behavior and which explain implementation. Use the repository's declared authority order; surface unresolved conflicts rather than choosing the most detailed document as authoritative. If a required source is missing or unreadable, report the input limitation and refrain from a complete alignment verdict.

## Authority and scope

- Authoritative stories or requirements and their acceptance criteria define required behavior.
- Milestone, release, or other delivery commitments apply where the repository defines them. Preserve their existing meanings; use “Not specified” where absent instead of inventing milestones.
- Supporting designs explain how architecture satisfies those requirements. Design assertions cannot independently expand product scope.
- Distinguish architectural implementation details from additional user-facing requirements.
- Preserve accepted, proposed, pending, and deferred decision statuses. Flag statuses that conflict with requirements for review.
- When authoritative requirements conflict or are ambiguous, identify the decision needed. Supporting design context cannot settle it.

## Review workflow

### 1. Establish the document baseline

Read all selected sources in full and record paths, roles, versions where available, and the current Git revision when applicable. Identify uncommitted changes so the report describes the versions reviewed. If no Git metadata is available, state that limitation.

Review complete sources unless the user explicitly limits scope. For a limited review, state exclusions and inspect relevant dependencies. An unread source is an input limitation, not evidence that its requirements lack design support.

### 2. Inventory the authoritative requirements

Extract each existing story or requirement ID, delivery assignment if any, user outcome, and acceptance criterion. Where requirements lack discrete criteria, inventory their explicit required outcomes as review units without rewriting product requirements.

Preserve existing identifiers. Assign report-local references where identifiers are absent, based on source location and criterion or outcome number. These are report references, not new authoritative IDs.

Where the same identifier appears across delivery increments, check whether it represents cumulative delivery, duplication, or conflict according to repository conventions. Check combined requirements and sequencing for consistency.

Identify conflicts among summaries, delivery commitments, requirement text, and acceptance criteria. Report decisions needed rather than silently choosing an interpretation.

### 3. Map requirements to architectural support

For every inventoried criterion or required outcome, locate supporting design sections and classify coverage:

- Supported: the design describes a compatible mechanism.
- Partial: some required behavior or architectural responsibility is missing.
- Missing: no supporting design is present in the reviewed sources.
- Contradictory: the design specifies incompatible behavior.
- Decision needed: ambiguity prevents a reliable assessment.

Assess meaning rather than relying on terminology or criterion citations. Document alignment does not establish implementation or test coverage.

For each gap, propose the smallest design clarification or change supporting the requirement. A pending design decision may remain pending if the design clearly records the requirement it must satisfy.

### 4. Check designs for unsupported scope

Account for every substantive design requirement and capability, including those outside numbered criteria. Classify each as:

- Requirement-backed behavior.
- Necessary implementation detail supporting identified requirements.
- Optional or future capability clearly outside committed scope.
- Unsupported product requirement requiring a scope decision.

An implementation detail need not become a story; explain its relationship to existing requirements. For unsupported product behavior, recommend removal, explicit deferral, or a user decision about adding a requirement. Keep authoritative requirements independent of unsupported design scope.

### 5. Check delivery feasibility and applicable controls

Where delivery increments exist, compare the design's implementation sequence with their promised outcomes. Identify dependencies required before each increment is usable and distinguish partial delivery from complete coverage. If no increments are defined, assess requirement dependencies without inventing a delivery schedule.

Check controls required by the authoritative sources or applicable repository policies, such as approvals, access restrictions, privacy, budgets, validation, or provenance, alongside the capabilities they govern. Derive obligations from those sources rather than importing controls from another project's domain.

Check criteria and required outcomes for observable behavior and sufficient verification conditions. Flag ambiguity without inventing thresholds, policies, or product decisions.

### 6. Produce the reconciliation report

Include the report creation date and time in the review filename using `yyyy-mm-dd-hh-mm` (24-hour local time), for example `reconciliation-review-2026-10-28-14-30.md`. Preserve the requested or repository-defined directory and descriptive filename prefix.

Present:

1. Baseline: reviewed sources, their authority roles, and scope or input limitations.
2. Coverage matrix: one row per inventoried criterion or required outcome, with its existing ID or report-local reference, delivery assignment when present, design references, coverage status, and any finding ID.
3. Findings: actionable discrepancies grouped by severity.
4. Decisions needed: unresolved requirement conflicts or scope choices.
5. Proposed edits: concrete replacement or addition text for findings resolvable from authoritative requirements.

For each finding include a report-local ID, severity, requirement and design locations with line references where available, evidence, practical consequence, and recommended target document and correction.

Use these severity levels:

- High: contradicts required behavior, omits a required control, or prevents a committed delivery outcome.
- Medium: partial support, unsupported scope, or ambiguity affecting implementation or verification.
- Low: terminology, traceability, or editorial inconsistencies that do not change behavior.

Recommend design changes by default. Recommend requirement changes only to resolve ambiguity or inconsistency, or to present an explicit product-scope decision.

Finish with counts by coverage status and severity, distinguishing missing inputs from evaluated gaps. Call out decisions preventing an alignment verdict. A clean report requires every selected criterion or outcome and substantive design requirement to be accounted for; qualify conclusions for limited reviews.

## Applying authorized corrections

Default invocation reports findings without editing source documents. When the user authorizes corrections:

- Apply only authorized changes and necessary directly related edits.
- Preserve existing IDs, document organization, terminology, and decision history.
- Keep summaries, references, and repeated delivery increments consistent where present.
- Leave unauthorized product decisions unresolved.
- If corrections affect a plan being executed, follow the repository's scope-change procedure and preserve its approval gates. Use `manage-plan-scope` when available; this skill does not itself authorize implementation or progression.
- Rerun reconciliation against the resulting sources and report remaining findings and input limitations.
