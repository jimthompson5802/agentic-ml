# Documentation consistency after the design split

Created 2026-10-29 00:03 EDT (America/New_York).

**Current status:** Both findings resolved on 2026-10-29. All eight review units are Supported; no open findings remain. Original evidence is retained below.

## Baseline, authority, and scope

Reviewed Git revision `5ad63b48140ac75ee0cd7908352702313ae4a97b`, with a clean working tree before this report. The baseline is design version 0.13: the [overview](../specs/agentic-ml-harness-design.md) and all seven topic documents in its reading map. The comparison baseline is the complete version 0.12 design at `5ad63b4^`.

GitHub issues govern implementation scope and recorded scope decisions; [user stories](../specs/user-stories.md) define product requirements. The design provides supporting contracts. This review does not implement a story or resolve a pending architecture decision; no issue discussion was retrieved or independently reconciled.

The review covers consistency affected by the restructuring: content preservation, navigation, terminology, document authority, milestone assignments, and compatibility of the active walkthrough and development guidance with the design. It does not repeat the previous full architectural assessment of every acceptance criterion or certify implementation/test coverage. Criterion counts below are structural traceability checks, not new semantic coverage verdicts.

Sources inspected:

- [README](../../README.md), [AGENTS.md](../../AGENTS.md), the complete [user stories](../specs/user-stories.md), [example walkthrough](../specs/example-walkthrough.md), and [plan template](../templates/user-story-implementation-plan.md).
- The design overview and topic contracts for interfaces/configuration, execution/governance, data/features, acceptance traceability, milestone delivery, repository layout, and architecture decisions.
- The repository-local create-implementation-plan, execute-plan, manage-plan-scope, and reconcile-stories skills for source-following and approval behavior. All tracked Markdown, including other local skills, was included in the link scan; other skills were not semantically re-reviewed.
- Baseline/disposition text and reference navigation in the [proposal reconciliation](user-stories-proposal-reconciliation.md), [current-baseline reconciliation](user-stories-current-reconciliation.md), [2026-10-28 reconciliation](reconciliation-review-2026-10-28-21-26.md), and [restructuring record](design-document-restructuring.md). Historical coverage judgments were not re-evaluated row by row.

## Coverage of the restructuring review

The table reflects the approved corrections and scoped re-review. The identifiers below are report-local review units, not additional product acceptance criteria. All delivery assignments remain Milestones 0–6 and deferred Milestone 99.

| Unit | Required consistency outcome | Evidence | Status | Finding |
|---|---|---|---|---|
| N-01 | Preserve existing design behavior and decision statuses | All 15 original section bodies match after normalizing Markdown links; ADR status text is preserved | Supported | — |
| N-02 | Preserve requirements authority and planning gates | README planning terminology; AGENTS.md audience/workflow rules; overview authority rules; plan template and planning/execution/scope skills | Supported | — |
| N-03 | Resolve existing local Markdown navigation | 2,021 links across 29 tracked Markdown files resolve to existing paths and heading/HTML anchors | Supported | — |
| N-04 | Preserve criterion identities and delivery assignments | 34 unique stories, 40 increments, 184 criterion definitions and 184 traceability links; no missing/unknown criteria or milestone mismatches | Supported | — |
| N-05 | Keep active story-to-contract navigation usable after the split | All 36 architecture-reference paragraphs link directly to the relevant contracts; original labels are preserved | Supported | R-01 resolved |
| N-06 | Use the repository's distinction between milestone delivery and detailed implementation plans | US-29-AC-07 refers and links to the milestone delivery plan | Supported | R-02 resolved |
| N-07 | Keep the walkthrough compatible with the design | Interactive mode requires no adapter; scoped approvals precede execution; feature comparison uses a fixed approved estimator; final evaluation protects holdout data; restoration and recovery remain distinct; delivery table matches milestones | Supported | — |
| N-08 | Preserve historical evidence without treating it as the new baseline | Historical reviews state their baseline revisions/dispositions; overview explains retained section numbers and historical line references; restructuring record records developer approval | Supported | — |

## Findings

### R-01 — Resolved: story architecture references link to the contracts

**Resolution (2026-10-29):** Applied the approved links in all 36 architecture-reference paragraphs and verified their destinations. Original severity: Low. The evidence and correction below describe the pre-correction finding.

**Location:** [user stories, line 83](../specs/user-stories.md#us-01-install-a-pinned-harness-version), and the other 35 “Architecture references” paragraphs through line 574. The [reading map](../specs/agentic-ml-harness-design.md#reading-map-and-document-authority) now directs readers to separate topic files.

**Original evidence:** US-01 ended with `Architecture references: §8 Project initialization and installation; §9 Execution.` The detailed contracts now live in separate files; the overview's corresponding sections contain forwarding links. Other paragraphs used the same plain-text pattern, including ADR-006 references.

**Consequence:** The references remain substantively correct because section numbers were retained. Readers and agents starting from a story must perform extra lookups to find the specific contract. This is a navigation improvement, not a missing requirement or broken link.

**Approved correction (applied):** Convert these references to direct links while retaining their section numbers and labels. For US-01:

> Architecture references: [§8 Project initialization and installation](../specs/design/interfaces-and-configuration.md#project-initialization-and-installation); [§9 Execution](../specs/design/execution-and-governance.md#execution).

When applying this text in `user-stories.md`, use targets relative to that file: `design/interfaces-and-configuration.md#project-initialization-and-installation` and `design/execution-and-governance.md#execution`. Link conceptual interface references to their enclosing contract section; do not invent headings for individual methods or protocols.

### R-02 — Resolved: US-29-AC-07 references the milestone delivery plan

**Resolution (2026-10-29):** Applied the approved terminology and link correction, preserving the criterion ID and behavior. Original severity: Low. The evidence and replacement below describe the pre-correction finding.

**Location:** [US-29-AC-07, line 572](../specs/user-stories.md#us-29-ac-07); [README planning terminology](../../README.md#planning-terminology); [milestone delivery](../specs/design/milestone-delivery.md#11-milestone-delivery-plan), especially its future-ideas row and deferred-enhancements subsection.

**Original evidence:** The criterion said advanced acquisition strategies remain deferred according to “the design document's implementation plan.” The relevant material is now titled “Milestone Delivery Plan”; repository terminology reserves implementation phases and detailed implementation plans for story-level work.

**Consequence:** The deferral remains consistent with the design. The old term can lead a reader or agent to look for a separate detailed implementation plan instead of the milestone delivery contract. No scope decision is required to clarify the reference.

**Approved replacement (applied), preserving the existing ID and behavior:**

> **US-29-AC-07:** Resumption after acquisition retains approvals, budget usage, dataset lineage, and completed-run identities; advanced acquisition strategies remain deferred according to the design's [milestone delivery plan](../specs/design/milestone-delivery.md#11-milestone-delivery-plan).

Use `design/milestone-delivery.md#11-milestone-delivery-plan` as the target when applying the replacement in `user-stories.md`.

## Historical reports and optional navigation

The 160- and 179-criterion counts in older reports belong to their recorded baselines; the current source has 184 criteria. Those counts should not be overwritten. Similarly, labels such as “design version 0.12” and old line numbers describe historical evidence. Their relative links open the current documents, not immutable snapshots. The baseline Git revisions allow the original evidence to be retrieved, and the overview already states that historical line references refer to the reviewed versions.

An optional follow-up is to add a short navigation notice to older reports linking to version 0.13's reading map, while retaining their original findings and counts. Immutable revision links would also make historical source inspection easier. Neither change is necessary for product alignment, and neither is counted as an additional discrepancy.

The walkthrough and template can continue to enter through the overview. AGENTS.md and the overview already require agents to follow the reading map and related contracts; duplicating the complete map in every document would add maintenance work.

## Verification and limits

- `python3 /tmp/audit_design_consistency.py` passed the structural audit. It obtained tracked Markdown with `git ls-files -- '*.md'`, checked local link destinations and heading/HTML anchors outside fenced code, compared version 0.12 section bodies from `git show 5ad63b4^:docs/specs/agentic-ml-harness-design.md` with their current locations after stripping Markdown link wrappers, and matched criterion IDs and milestone assignments independently between stories and traceability.
- Results: 29 baseline Markdown files; 1,932 local links; zero link errors; 15 preserved original sections; 184 criteria mapped exactly once with zero milestone mismatches.
- The audit script is a temporary review aid, not a new repository tool. It does not fetch external URLs, render Markdown/Mermaid, or prove semantic completeness of every contract. File/anchor existence alone does not prove that a historical line citation still points at the original evidence.
- Manual review checked the active documents' described behavior against the corresponding design contracts. No application checks or TDD cycle apply because only this review report was added.

## Decisions and result

No product-scope or architecture decision is needed for the proposed editorial corrections. The initial review added only this report. The developer subsequently approved applying both corrections; their disposition and verification appear below.

Current coverage of the eight report-local review units: **8 Supported, 0 Partial, 0 Missing, 0 Contradictory, 0 Decision needed**. Open findings: **0 High, 0 Medium, 0 Low**. Both original Low findings are resolved. No substantive contradiction attributable to the split was identified. This is a restructuring-consistency conclusion, not a fresh full requirements reconciliation or implementation verdict.


## Approved corrections and scoped re-review (2026-10-29)

The developer answered “yes” to applying the two proposed corrections. Updated `docs/specs/user-stories.md` within that authorization:

- **R-01 resolved:** All 36 architecture-reference paragraphs now link to the corresponding design contracts. References to conceptual workflow activities and adapter interfaces link to their enclosing sections; ADR-006 links to pending decisions. Existing reference labels remain unchanged.
- **R-02 resolved:** US-29-AC-07 now refers and links to the design's milestone delivery plan. Its ID, acquisition recovery obligation, and advanced-strategy deferral remain unchanged.

Scoped verification:

- `python3 /tmp/apply_design_review_corrections.py` — passed after correcting the verification helper to normalize pre-existing links on both sides of its comparison. The initial guard failed before writing any source file; it compared normalized output with unnormalized input. The corrected guard confirms that the only visible wording change is the approved US-29-AC-07 reference clarification.
- `python3 /tmp/audit_design_consistency.py` — passed: 2,021 local links across 29 tracked Markdown files; zero missing files or anchors; all 184 criterion identities and milestone mappings preserved; all 15 original design section bodies still preserved apart from link markup.
- `git diff --check` — passed.

The two affected review units N-05 and N-06 are now Supported. Updated scoped result: **8 Supported, 0 Partial, 0 Missing, 0 Contradictory, 0 Decision needed**; **0 open High, Medium, or Low findings**. The original finding evidence and baseline verification counts above remain historical; the coverage table and result summary reflect the resolved status. Historical-review navigation improvements remain optional and were not applied. TDD does not apply to these link and terminology edits; no executable behavior changed.
