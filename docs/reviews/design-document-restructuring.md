# Design document restructuring review

**Date:** 2026-10-28
**Status:** Developer approved on 2026-10-29.

## Scope

The developer approved splitting the design into seven topic documents while keeping the existing design path as the entry point. This is documentation reorganization, not user-story implementation. No executable behavior changes; TDD and application regression tests do not apply.

The [design overview](../specs/agentic-ml-harness-design.md) now contains 297 lines, down from 1,094. Detailed sections live in [design topic documents](../specs/design/). Original section numbers remain for continuity. Version 0.13 records this reorganization; accepted and pending decisions retain their statuses.

## Safeguards

- The overview reading map maps implementation tasks to required topic documents.
- Every topic states its scope and links related contracts and architecture decisions.
- The overview states the issue, user-story, and supporting-design authority rules.
- Each original section body has one location; overview placeholders link to moved sections.
- Development AGENTS.md directs agents to the reading map, related contracts, milestones, traceability, and decisions.

Existing fragment links in user stories and review documents now point to the moved headings. Historical review prose and line references remain unchanged; those line references describe the versions originally reviewed.

## Verification

- `python3 /tmp/verify_harness_design.py` — passed: all 15 original section bodies preserved after normalizing Markdown links; only link destinations and conversion of section references into links differ within those bodies.
- The same verification checked 1,740 local links and anchors across the 13 affected Markdown files — passed.
- `git diff --check` — passed.

The comparison used a copy of the pre-edit design saved at `/tmp/harness-design-before.md`. Verification scripts and the comparison copy are temporary review aids outside the repository. Link verification covers local Markdown destinations and heading anchors, not external URLs or rendered Mermaid diagrams.

## Approval gate

The developer approved the resulting restructuring, navigation, and agent-instruction changes on 2026-10-29. Approval was recorded before committing the documentation changes.
