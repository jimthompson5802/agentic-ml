# MVP scope revision — IP3 evidence

Date: 2026-11-06. **IP3-T1–T5 complete; Gate 3 approved.**

Developer “I approve Gate 3; commit the changes” approved the aligned design and
issue package and authorized the local commit. Record-only status updates use
renewed document/whitespace checks; existing formatting/diagram evidence remains
applicable. No source push/PR/merge, issue writes or Phase 4 execution requested.

## Authorization and reviewed baseline

Developer “I approve gate 2 and authorize phase 3” approved revised stories,
milestones, criteria and issue drafts and authorized IP3 of the
[plan](../plans/mvp-scope-revision.md). Branch `refactor-milestones-user-stories`,
starting from clean committed IP1/IP2 snapshot `0404916`.

Current [stories](../specs/user-stories.md) contain 222 criteria. Phase 3 changes
only status/supporting-reference prose there; acceptance IDs/text remain identical
to Gate 2. Existing complete issue snapshots and inventory remain read-only source
history. No issue publication, product implementation or new acceptance is claimed.

## Deliverables

- Design 0.15 overview/reading map, architecture/decision dispositions and ownership.
- Reconciled interface, execution/evaluation/tracking/reproduction, data/features,
  delivery and layout topics; compact existing/planned software blueprint.
- Three labeled historical 0.14 references: complete blueprint, architecture
  decisions and walkthrough, preserving original contents after their separators.
- Current 222-criterion design mapping and explicit ASW-01–08 walkthrough with
  scientist prompts, artifact expectations and owning criteria.
- README, setup/validation guide and repository developer instructions aligned;
  TDD, development gates, command policy and verification requirements retained.
- Historical owning plans annotated without modifying their original bodies;
  old 160-criterion index retains rows/statuses with contract links repaired to
  preserved blueprint. Existing verification obligations/skips/failures remain open.
- Issue drafts refreshed to active design context and Gate 2 approval; unchanged
  action/criterion inventory, no remote writes. Intended source links still require
  separate source publication before issue publication can safely proceed.

## Verification strategy

Documentation-only; no source/tests/resources/dependencies/lockfile changes.
TDD, executable milestone/shared tests and artifact drivers do not apply. Check
links/anchors (including historical aliases), Mermaid parsing, documentation
formatting, complete criterion mapping, API export accuracy, archive fidelity,
preserved plan bodies and issue/local/template parity. No OS/runtime/assistant
execution or broader platform support is established.

Raw records: `.dev-records/verification/20261106-mvp-scope-ip3-0404916/`.
Record actual commands/results, limits and any corrective attempts below.

| Check | Actual result |
|---|---|
| All 222 criteria and unchanged Gate 2 acceptance text | Pass; exact ID/text equality to `0404916`; one design row per ID |
| Archive fidelity and old plan/evidence preservation | Pass; three original reference bodies, eight original plan bodies, 160 original index rows/statuses; only wrappers/link repairs |
| Existing public API exports and CLI status | Pass; 37 exports matched by AST without importing/executing product code; CLI registrations inspected |
| Local/intended-source links and historical anchors | Pass for 3,680 repository/intended-source links and preserved old anchors; external absolute evidence limits below |
| Mermaid parse and documentation formatting | Pass; seven browser-DOM parses, 13 files already formatted |
| Issue body/template/manifest parity | Pass; 34 bodies equal criterion text/template, unchanged 43-action inventory and states |
| Product/tests/resources/lock/policy identity | Pass; no executable/dependency/verification-policy change |
| Whitespace including new files | Pass after EOF/annotation normalization; `git diff --check` passes |

## Commands, corrections and limitations

Scoped document command:
`python3 .dev-records/verification/20261106-mvp-scope-ip3-0404916/validate-current-design.py`.
It checks the versioned design scope and records unavailable external absolute
evidence separately. Raw `validation-summary.json` contains counts and all 11
unavailable paths. No product tests or assertions were changed.

The original broader diagnostic `validate.py` is preserved unchanged. It fails
on unavailable `/private/tmp/us-01-ip1-evidence` links in unchanged US-01 reports.
The 11 paths include historical logs/identity manifests/diffs under that location
and `/private/tmp/us-01-ip2-evidence`. Their availability is **not verified**;
do not recreate placeholder evidence, delete links or interpret this scoped check
as closing the historical obligation. The current design check verifies every
repository-relative/intended-source target and asserts external absolute references
occur only in unchanged historical reports. Exclusion from the versioned-doc scope
is justified by their being pre-existing external raw records, not this phase's
artifacts; the failed broader probe and limitation remain visible.

Preservation correction: initial exact-body check exposed an extra blank line
after annotation wrappers. Attempt 1 normalized eight plan wrappers; the same
check exposed the index wrapper. Attempt 2 normalized that wrapper and exact
historical body/row checks passed. Source assertions and original content retained.
Separate link correction attempt 1 added two duplicate-heading legacy aliases
(`ownership-and-criterion-map-1/2`); all old design anchors then passed.
Separate whitespace correction attempt 1 removed extra EOF blank lines from five
rewritten topic docs; renewed scoped validation and whitespace passed.

Formatting command:
`uv run --locked ruff format --check docs/specs/agentic-ml-harness-design.md docs/specs/design docs/specs/example-walkthrough.md docs/specs/example-walkthrough-v0.14-reference.md`.
Initial sandbox uv-cache lock access failed; required escalated renewal exited 0,
13 files already formatted. Lock unchanged; no dependency download/change claimed.

Mermaid command:
`node .dev-records/verification/20261106-mvp-scope-ip3-0404916/parse-mermaid.mjs`.
Cached Mermaid 12.0.0 parse in plain Node first failed because DOMPurify lacked a DOM
(`purify.sanitize is not a function`). An exploratory Puppeteer import used a
nonexistent old-layout path; package metadata supplied its actual local entrypoint.
The final parser uses installed headless Chrome with cached Mermaid in a real DOM,
under escalated execution. It parsed one active flowchart and six unchanged
historical sequence diagrams, exit 0, with no downloads. See `mermaid-summary.json`.
This is syntax parsing, not visual rendering or a product runtime demonstration.

Raw `diagnostics.txt` retains the initial failures and corrective results. Original
lock SHA-256 remains
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

## Scope and verification boundaries

The active design enforces no arbitrary-Python/assistant OS security claim and
requires no managed agents, durable workflow engine or mandatory experiment gates.
It preserves supported-path validation, trial limits, train-only fitting,
consistent metrics/final testing and committed-project reproduction obligations.
Exact future basic-path shape, real estimator inventory, fitted persistence and
example tolerances remain owning story contract decisions before dependent code.
Archived records are not active schema or assurance prerequisites.

Historical M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY stay open under their owners.
New proposed MVP milestone verification owners must reconcile those obligations
explicitly, not infer closure or waived checks from renumbering. No test markers,
assertions, timeouts or temporary skips were changed. Current developer verification
policy remains byte-identical; no broader suite or standalone artifact run occurs.

## Handoff

Stop at Gate 3 for review of reconciled documents and exact issue package. IP4
needs explicit publication authorization, refreshed source discussions, verified
write access and reviewed source links available at the referenced GitHub revision.
Commit/push/merge/PR permission remains separate. No implicit source publication or
automated assistant demonstration is authorized by this documentation phase.
