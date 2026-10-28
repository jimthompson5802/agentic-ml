---
name: reconcile-stories
description: Reconcile the design document against authoritative user stories. Use when checking alignment, identifying coverage gaps or scope drift, or proposing document corrections.
---

# Reconcile Stories and Design

Treat `docs/specs/user-stories.md` as the authoritative source of product
requirements. The supporting design document is
`docs/specs/agentic-ml-harness-design.md`.

Use alternative input paths when supplied by the user. Resolve these paths
against the repository root, not the skill directory.

## Authority and scope

- User stories and their acceptance criteria define required behavior.
- Milestone descriptions and the summary table define delivery expectations.
- The design document explains how the architecture supports those requirements.
- Design acceptance criteria are supporting design assertions, not
  independent authority to expand product scope.
- Distinguish architectural implementation details from additional
  user-facing requirements.
- Preserve accepted, proposed, pending, and deferred decision statuses.
  Flag statuses that conflict with story requirements for review.
- When stories conflict or are ambiguous, identify the decision needed.
  The design document may provide context but cannot settle the requirement.

## Review workflow

### 1. Establish the document baseline

Read both documents in full and record their paths, versions where
available, and current Git revision. Identify uncommitted changes so the
report clearly describes the versions reviewed.

Review the complete documents unless the user explicitly limits scope.
For a limited review, state exclusions and inspect relevant dependencies.

### 2. Inventory the authoritative requirements

Extract each story ID, milestone assignment, user outcome, and acceptance
criterion. Assign report-local references to acceptance criteria that
lack identifiers, such as `US-09 / milestone 1 / criterion 2`.

Treat repeated story IDs across milestones as incremental delivery.
Check whether their combined requirements and sequencing are consistent.

Identify conflicts between the summary table, milestone descriptions,
story text, and acceptance criteria. Report these as story decisions
needed rather than silently choosing an interpretation.

### 3. Map stories to architectural support

For every story acceptance criterion, locate the design document sections
that explain its architectural support.

Classify coverage as:

- Supported: the design document describes a compatible mechanism.
- Partial: some required behavior or architectural responsibility is missing.
- Missing: no supporting design is present.
- Contradictory: the design document specifies incompatible behavior.
- Decision needed: ambiguity prevents a reliable assessment.

Assess meaning rather than relying on matching terminology or AC
citations. Do not claim implementation or test coverage from document
alignment alone.

For each gap, propose the smallest architectural clarification or
change that supports the story. A pending design decision may remain
pending if the design document clearly records the requirement it must satisfy.

### 4. Check the design document for unsupported scope

Account for every substantive design document requirement and capability,
including those expressed outside its numbered acceptance criteria.

Classify each as:

- Story-backed behavior.
- Necessary implementation detail supporting identified stories.
- Optional or future capability clearly outside committed milestone scope.
- Unsupported product requirement requiring a scope decision.

An implementation detail need not become a user story. Explain its
relationship to an existing requirement.

For unsupported product requirements, recommend removal, explicit
deferral, or a user decision about adding a story. Do not automatically
expand the stories to match the design document.

### 5. Check milestone feasibility and cross-cutting controls

Compare the design document's implementation sequence with the story milestones.

Identify dependencies required before a milestone can deliver its stated
outcome. Distinguish partial delivery from claims of complete coverage.

Check that approvals, access restrictions, protected evaluation data,
budget enforcement, independent validation, and provenance accompany
the capabilities that require them.

Check story acceptance criteria for observable outcomes and sufficient
conditions for verification. Flag ambiguities without inventing
thresholds, policies, or product decisions.

### 6. Produce the reconciliation report

Present:

1. Baseline: documents reviewed and any scope limitations.
2. Coverage matrix: one row per story acceptance criterion, with its
   milestone, design document references, status, and any finding ID.
3. Findings: actionable discrepancies, grouped by severity.
4. Decisions needed: unresolved story conflicts or scope choices.
5. Proposed edits: concrete replacement or addition text for findings
   that can be resolved from the authoritative requirements.

For each finding include:

- A report-local ID.
- Severity.
- Story and design document locations, with line references where available.
- Evidence and the practical consequence.
- Recommended target document and correction.

Use these severity levels:

- High: contradicts required behavior, omits a required control, or
  prevents delivery of a stated milestone outcome.
- Medium: partial support, unsupported scope, or ambiguity affecting
  implementation or verification.
- Low: terminology, traceability, or editorial inconsistencies that
  do not change behavior.

Recommend design document changes by default. Recommend story changes only
to resolve ambiguity or inconsistency, or to present an explicit
product-scope decision.

Finish with counts by coverage status and severity. Call out unresolved
decisions that prevent declaring alignment. A clean report requires
every acceptance criterion and substantive design document requirement to
be accounted for.

## Applying approved corrections

Default invocation produces a report without editing either document.

When the user approves corrections:

- Apply only the approved changes and necessary directly related edits.
- Preserve story IDs and the existing document organization.
- Keep summary tables, references, and repeated story increments consistent.
- Leave unapproved product decisions unresolved.
- Rerun reconciliation against the resulting documents and report
  remaining findings.
