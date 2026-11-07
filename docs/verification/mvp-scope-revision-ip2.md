# MVP scope revision — IP2 evidence

Date: 2026-11-06. **IP2-T1–T5 technically complete; Gate 2 pending.**

## Authorization and outcome

Developer “i approve gate 1 and authorize phase 2” approved MVP-SC-01/02 and
authorized IP2 of the [plan](../plans/mvp-scope-revision.md). Branch
`refactor-milestones-user-stories`, baseline `0a7b64389cf663290d3bf4fc7063aae29ef8f20c`.
Prior IP1/checkpoint edits retained. No commit/push/PR or remote issue mutation.

Deliverables:

- [Revised stories](../specs/user-stories.md): all 204 original IDs, retained/
  revised wording per approved matrix, deferred criteria preserved, two revised
  delivery milestones and 18 new integration criteria under US-39/40.
- [Migration and follow-up ownership](../plans/mvp-scope-story-migration.md):
  old/new assignments, ASW-01–08 criterion ownership and future code/test boundaries.
- [Unpublished issue package](../plans/mvp-scope-issues/README.md): 32 open issue
  title/body edits with scope comments, three comments on accepted issues, six
  unchanged accepted issues and two new integration issue drafts; 69 draft files.

## Source reconciliation

Refreshed all-state issue inventory using `gh issue list --repo
jimthompson5802/agentic-ml --state all --limit 200 --json
number,title,state,updatedAt`. Initial sandbox network failure was resolved by
the required escalated read; exit 0. All 41 update timestamps/states match IP1's
complete body/all-comment snapshots, so those stable snapshots remain applicable.
US-39/40 are unused story IDs; GitHub issue numbers #39/#40 already identify
different existing stories. US-34/37/38 remain local-only without new issue drafts.

Raw records:
[IP2 invocation](../../.dev-records/verification/20261106-mvp-scope-ip2-0a7b643/).
Contains inventory refresh and effective-criterion mapping; IP1 complete snapshots
remain retained separately. Reads establish no write authentication or publication.

## Verification strategy and results

Documentation/backlog only. No executable source, tests, markers, dependencies,
lockfile, design topics or historical owning-plan evidence changed. TDD/runtime
milestone/shared executable checks and artifact drivers do not apply. Do not
manufacture a failing test for requirement wording or claim new platform coverage.

| Check | Method | Actual result |
|---|---|---|
| Original ID coverage and approved wording | Compare 204 baseline rows, current source and effective mapping | Pass; all original IDs once; 57 revisions match approved retained behavior |
| Accepted/backlog/deferred preservation | Exact text checks; explicit scope sections; 18 new IDs only | Pass; 50 accepted, 65 deferred, 13 backlog texts preserved; 222 total IDs |
| New integration and assistant coverage | US-39/40, milestone slices, ASW-01–08 ownership | Pass; 11 US-39 and seven US-40 criteria; US-18-AC-01 spanning M1/M2 explicit |
| Issue/local equality and action safety | Manifest/body/comment comparison, template structure, states/metadata | Pass; 43 actions cover all 41 issues and two new stories; 159 criterion occurrences in 34 body drafts match local source |
| Local links/anchors/whitespace | New/changed docs and preserved inbound story anchors | Pass; initial combined checker covers 459 local/intended-source links; final count in raw summary; incoming-story links checked separately |
| Source/test/lock/design/history identity | Git baseline comparison and allowlist | Pass; product/tests/lock/design/development rules unchanged |
| Tracked whitespace | `git diff --check` | Pass |

Command: `python3 .dev-records/verification/20261106-mvp-scope-ip2-0a7b643/validate.py`.
This one-off document utility compares the approved baseline and effective mapping,
all new IDs/sections, issue draft template/body/manifest parity, metadata/state
preservation, historical anchors and changed-path identity. It checks GitHub
blob/main references against intended local files only; it does not claim those
unpublished sources already exist remotely. Raw `validation-summary.json` records
the final counts. A separate Python standard-library scan checks repository-relative
incoming links to the story document across README, AGENTS and docs. No new
automated product test or dependency was introduced. All 913 incoming story links
passed. No failed document verification or corrective attempt occurred; no
executable checks were run.

Lock SHA-256 remains
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
The original 204-criterion source is preserved in IP1 records and the approved
report; its old hash is historical, not a hash claim for the intentionally revised
story document. The IP1 baseline-only validator is not rerun against this new source.

## Limits and handoff

GitHub and design remain on the prior scope; the stories explicitly mark this
transition. Phase 3 must reconcile designs/developer instructions after Gate 2.
Phase 4 must refresh and publish only the approved package after Gate 3, with
reviewed source links available at the referenced GitHub revision. Commit/push
permission is separate; unpublished blob/main links are not ready publication.

No story/MVP acceptance or executed assistant walkthrough is claimed. Preserve
M1/M50 obligations, historical evidence, skips/failures and platform limits.
Stop at Gate 2 for review of revised stories, criteria, milestones and issue drafts.

## Local commit preparation

Developer “commit changes” authorized the local review snapshot. Staging exposed
extra blank lines at EOF in the issue-package README, story-migration report and
criterion-disposition report, which unstaged checks had not covered. Corrective
attempt 1 removed only those extra trailing blank lines. Renewed document
validation and staged `git diff --cached --check` pass. No requirement wording,
criterion, assertion or scope changed; Gate 2 remains pending.
