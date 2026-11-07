# MVP scope revision — IP1 evidence

Date: 2026-11-06. Documentation/backlog investigation only.

## Outcome and execution identity

- [Plan](../plans/mvp-scope-revision.md), IP1-T1–T4.
- [Gate 1 disposition report](../reviews/mvp-scope-criterion-dispositions.md).
- Branch `refactor-milestones-user-stories`, baseline
  `0a7b64389cf663290d3bf4fc7063aae29ef8f20c`.
- Plan execution authorized by developer “Implement the plan.” Gate 1 remains
  pending; no authoritative requirements, designs, owning historical plans,
  executable files, tests, dependencies or issues revised.
- Pre-existing reassessment checkpoint preserved and updated at this handoff.
- Raw records:
  [invocation directory](../../.dev-records/verification/20261106-mvp-scope-ip1-0a7b643/).
  Retain under the lifetime evidence policy; ignored records need independent backup.

## Source retrieval

Used `gh issue list --repo jimthompson5802/agentic-ml --state all --limit 200
--json number,title,state,updatedAt` to inventory 41 existing story issues.
For each issue N, used these read-only helper calls in order:

```text
sh .codex/scripts/github-read.sh issues/N
sh .codex/scripts/github-read.sh issues/N/comments --paginate --slurp
sh .codex/scripts/github-read.sh issues/N
```

All 123 per-issue calls returned exit 0. Preserved complete bodies, metadata and
all comment bodies/IDs/authors/timestamps/URLs in raw `issues.json`. Compared first
and final update timestamps and comment counts, checked unique comment IDs and
reported counts; every snapshot stable. One comment total, on #3, historical
premature closure/reopening. US-34/37/38 local-only. No authentication changes or
publication attempted. `gh auth status` reported an invalid default token while
the helper reads succeeded; do not equate read success with publication access.

Parsed 204 unique local criteria; 191 belong to retrieved issues and 13 to local-only
stories. Compared exact issue/local criterion text: 28 wording differences, all
equivalent after recorded CLI-name and harness/toolkit terminology normalization.
Both variants are preserved in the report/raw records. Local approval scope
decisions and older issue prerequisite language are explicitly discussed in the
report; no source conflict was silently resolved by changing authoritative text.

## Scope/evidence review

The report inventories original criterion text, old milestone and issue owner,
existing delivery status, proposed retained behavior and deferred obligations.
It maps M1–3 functionality into two delivery increments, preserves M0/M50/M99 and
records old M4–6 as uncommitted roadmap context. It also inventories substantive
design obligations, all original nine protocols, eight blocker/assurance decisions,
accepted ADR-001/007 and bounded US-02/03/05 contracts, and affected owning plans.

Counts: 50 preserve accepted work (including staged/default-usage qualifications),
19 retain remaining scope, 57 revise, 65 defer, 13 retain supporting backlog.
These are scope dispositions, not counts of implemented requirements.

M1-ACCEPT-VERIFY, M50-ACCEPT-VERIFY, prior failed/interrupted checks, three temporary
skips, recorded platform limits and historical approvals remain unchanged. Later
owning-plan annotations must not silently waive them. Current verification policy
and historical stronger requirements require explicit reconciliation, not inference
from a newly numbered milestone.

## Verification

TDD and executable milestone/shared/runtime/artifact checks do not apply: no new
or corrected executable behavior, source/test changes, Python fences or diagrams.
Document checks and baseline identity checks are appropriate under the repository
verification policy. No runtime/platform verification is claimed.

| Check | Method | Actual outcome |
|---|---|---|
| Source retrieval completeness | 41 before/comments/after snapshots; unique IDs/counts and timestamps | Pass; 41 stable, one unique comment |
| Criterion inventory and wording comparison | Raw issue/local parse and normalized comparison | Pass; 204 local, 191 issue, 13 local-only; 28 explained differences |
| Disposition coverage | One row per original ID; source equality and explicit destinations | Pass; all 204, none missing/duplicated |
| Links/anchors/whitespace, including new files | Raw `validate.py` document checker | Pass after correction; 32 links/anchors before final record links added; final count in raw summary |
| Product/specification/history preservation | Git baseline identity and changed-path allowlist | Pass; only plan/report/evidence/checkpoint changes |
| Tracked whitespace | `git diff --check` | Pass |
| Lock identity | SHA-256 before/after | Pass; unchanged |

Original lock SHA-256:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
Original local-stories SHA-256:
`09e43db687e1cd6fb6d816dc1042730a26953bfd52b4883d2b8e51fe657bb9fd`.

### Commands and corrective evidence

Validation command:
`python3 .dev-records/verification/20261106-mvp-scope-ip1-0a7b643/validate.py`.
This one-off evidence utility checks source equality, snapshot stability/comment
counts, terminology normalization, disposition completeness, report IDs, relative
links/anchors, new-file whitespace, Git changed-path allowlist and lock/stories
hashes. It is not a product test or a replacement for future runtime verification.
The raw invocation directory contains its source and `validation-summary.json`.

Initial validation failed on the copied relative link in US-29-AC-07:
`AssertionError: (.../docs/reviews/mvp-scope-criterion-dispositions.md,
'design/milestone-delivery.md#11-milestone-delivery-plan')`.
The link was relative to the original stories file, not the new report.

Corrective attempt 1: rebase that link to `../specs/design/milestone-delivery.md`
in the rendered report and document link rebasing. Preserve exact original source
bytes in raw snapshots/dispositions; do not change source requirements or checker
assertions. Renewed original validation passed, exit 0. No second/third attempt
needed. The initial diagnostic is retained in raw `initial-link-failure.txt`.

Gate 1 approval and progression remain pending independently of technical checks.
Next work after authorized approval: IP2-T1, revise authoritative stories according
to the approved dispositions.

## Assistant walkthrough refinement — 2026-11-06

Developer “make the assistant-support walkthrough explicit” authorized MVP-SC-02
in the plan/report. Added ASW-01–08: scientist-directed setup, extraction, train-only
preprocessing, baseline/tuning, MLflow inspection and a validation-based revision,
selected-model final testing, committed-project DVC reproduction, and notebook/
regression/customization examples. M1 owns the first classification interaction;
M2 owns replay and usability extensions. IP2 assigns actual integration criteria;
IP3 updates the design walkthrough. Existing 204 criteria/dispositions are intact.

Evidence requirements now explicitly include one concrete assistant product,
interface/version, prompts, consequential edits/actions, commands/outcomes and
independently checked MLflow/DVC records. No manual experiment or assistant session
was run; this is an authorized documentation refinement within the current gate.
Renewed document/source validation and `git diff --check` apply. No runtime tests
are needed for this non-executable change. Gate 1 remains pending.
