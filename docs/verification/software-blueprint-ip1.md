# Software blueprint IP1 evidence

Date: 2026-11-04. [Owning plan](../plans/software-blueprint.md).
Branch: `embellish-software-component-descriptions`. Documentation-only review.

Created requested branch before edits. Read current checkpoints, source public
exports/models, planning resolution, initialization and validation contracts,
design authority/read map, interfaces, execution/governance, data/features,
repository layout, delivery, ADRs and verification policy.

Retrieved issue metadata/full bodies #8–18, every comment page using the repository
GET helper with `--paginate --slurp`, then refreshed metadata. All requests
succeeded. Each returned zero comments, matching reported count; timestamps stayed
unchanged. GitHub milestone objects are unset; bodies assign M1. No issue/design
scope conflict found. Preserve #9's editor decision, accepted US-03-SC-01 approval
exception and existing ADR slices. Issue closure is not new verification evidence.

The new blueprint maps each M1 criterion slice, preserves accepted existing APIs,
adds proposed owners/interfaces for undelivered software, and names M1-D1 as a
blocking isolation decision. No claim of implemented runner/connectors or expanded
approval authority. No existing Python, schema, dependency or lockfile changes.

Verification: source symbol/signature inspection and criterion matrix review;
local Markdown target existence check (14 targets passed) and `git diff --check`
(passed). Mermaid sequence manually reviewed; renderer not run. No TDD or runtime
suite: no executable behavior changed. No new platform-support evidence.

Remaining: developer approval of IP1; IP2–6 unstarted. Full serialization detail
and enforcement mechanism remain owning-story contract decisions; proposals here
do not accept pending ADRs or authorize executable work.

IP1 review refinement: expanded ExperimentSpec with required field/type constraints,
record authority, preparation/result shapes, submission rechecks and explicit
negative cases. No executable behavior changed. Whitespace and local-target checks
renewed after the refinement; proposed interfaces remain subject to IP1 review.

M1 catalogue refinement at developer request “i agree complete m1 first”:
documented implemented initialization/planning/approval/validation record fields,
defaults, exception constructors and frozen-wrapper limits against source. Added
proposed authorization/accounting, evidence/run, data and restoration records,
including referenced nested types, lifecycle/authority and negative scenarios.
Clarified reservation-before-capture binding and content-ID envelope semantics;
explicitly recorded typed runner refinements to the conceptual protocol.
Later-milestone names are deferred explicitly; no M2 work started.

Renewal checks: 27 existing record/error names covered against source inventory;
14 relative Markdown targets exist; `git diff --check` passes. No renderer, executable tests or platform
verification; new contracts remain proposals, not product acceptance evidence.

Mermaid correction: developer reported sequence-diagram parse failure at the final
note. Reproduced the exact line-20 failure using cached Mermaid's `parse()` from
Node against the Markdown fence. Attempt 1 hypothesis: semicolon in note text
terminates the Mermaid statement and leaves trailing words interpreted as syntax.
Replaced the semicolon phrase with “before any resubmission”; the identical parser
probe now passes, as does `git diff --check`. No package installation or executable
product change. This adds parser validation; visual rendering remains unverified.
