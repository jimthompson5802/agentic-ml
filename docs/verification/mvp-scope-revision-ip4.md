# MVP scope revision — IP4 publication evidence

Date: 2026-11-07 UTC (2026-11-06 local). **IP4 complete; final gate approved.**

Developer “execut phase 4” authorized the explained publication sequence after
Gates 1–3 approval and commits `0404916`/`25544e5`. Branch:
`refactor-milestones-user-stories`; approved content head starts
`25544e56990f86aff929c30d9c890b9db3a33cb7`.

## Source publication prerequisite — preflight history

Remote main is `0a7b64389cf663290d3bf4fc7063aae29ef8f20c`; approved source
documents are not on main yet. No existing remote feature branch or PR found.
The approved issue bodies contain blob/main source links. Publishing those exact
bodies must wait until the reviewed source exists there. Branch push and PR
creation are authorized by the Phase 4 request; a merge is not inferred.
Do not rewrite approved links to another revision without the required review.

## Read-only preflight

- GitHub repo identity/default branch verified: jimthompson5802/agentic-ml, main.
- `gh auth status` failed in sandbox but succeeded under required escalation;
  authenticated account jimthompson5802 with repo scope. No credentials changed.
- Remote tips checked with escalated `git ls-remote`; initial sandbox DNS failed.
- All-state inventory: 41 existing story issues; timestamps/states match prior
  baseline. Complete discussion refresh and original-body comparison recorded
  separately below before issue mutation.
- US-39/40 title searches and recent all-state list show no existing matching
  stories. `enhancement` label exists. No issue type/milestone/assignee changes
  planned; existing states/history preserved.

## Progress and evidence

Complete discussion refresh: all 41 before/comments/after snapshots stable;
one unique historical comment, with exact original body/title/state/comment
equality to the review baseline. Raw records:
`.dev-records/verification/20261107-mvp-scope-ip4-25544e5/before-issues.json`.
No new scope decisions or concurrent issue edits to reconcile.

Source publication: pushed `refactor-milestones-user-stories`, opened and verified
[PR #57](https://github.com/jimthompson5802/agentic-ml/pull/57), main base, correct
owner/head and non-draft. Initial head `4d8b398b73c9210cebb5e61f9b94b95a5757a8ea`
contains the approved scope/design plus publication preflight records. PR evidence
links were corrected to that published revision before merge; no issue draft URLs
were changed. All 106 changed paths are documentation/instructions.

Developer answered “Approve squash merge after checks pass”. Hosted
[Linux/Python 3.12 CI](https://github.com/jimthompson5802/agentic-ml/actions/runs/42317228764)
completed successfully; final head was MERGEABLE/CLEAN. Used a matching-head squash
merge. GitHub confirms merged at 2026-11-07T00:28:00Z as
`cef75068e1fd161b97507b0afb038a752f68b615`. No branch deletion. Core source blobs
on main are checked against the reviewed head before any issue writes.

Approved issue writes are in progress using `publish-reviewed-issues.py` in the
raw invocation directory. It preserves prepared file bytes, existing states,
labels/assignees/milestones and comment history; detects concurrent changes;
verifies each write; logs outcomes durably; reconciles uncertain results without
blind retries. Temporary UTF-8 bodies are outside tracked files. Pending: full
post-publication discussion verification and final handoff.

This phase changes documents/backlog only. No executable tests or product
acceptance. Existing document/diagram evidence remains applicable to unchanged
approved content; publication records need link/whitespace checks. Eleven
historical external absolute evidence paths remain unavailable, not waived.

## Final issue publication verification

The publisher completed 69 verified writes without blind retries: 32 title/body
edits, 35 scope comments and two new issues. Six accepted issues received no writes.
Afterward all 43 issues were fetched as metadata → all comment pages → metadata;
unique comment counts and timestamps were stable. Every published body matched
its approved file exactly. Original states, labels, assignees, milestones and
comment bodies were preserved. No issue was closed/reopened, assigned a new type
or moved to a GitHub milestone. Milestone assignments remain explicit in bodies.

- New [US-39 #58](https://github.com/jimthompson5802/agentic-ml/issues/58)
  spans M1/M2; [US-40 #59](https://github.com/jimthompson5802/agentic-ml/issues/59)
  owns M2 reproduction. Both open, enhancement label, no assignee/milestone/type flags.
- Remote issues contain 209 unique criteria. The 13 US-34/37/38 local-only criteria
  remain local, giving 222 total. Edited/new bodies are byte-equal to their approved
  files; accepted untouched bodies preserve legacy harness/toolkit and recorded
  CLI-spelling variants, normalized only for the cross-source criterion comparison.
- CI evidence: hosted full suite **471 passed, three existing skips in 596.63s**;
  lint, formatting (241 files), strict typing, smoke, build, both isolated package
  paths and lock immutability passed. This is hosted Linux/Python 3.12 evidence,
  not renewed local/platform/MVP acceptance. Existing milestone obligations stay open.
- Raw `publication-ledger.json` and per-command records retain exact writes/URLs;
  `after-issues.json` contains full stable discussions; `publication-verification.json`
  contains the final identity/criterion checks. `ci-run.log` preserves hosted output.
  Temporary publication body files were removed only after successful verification.

### Action and comment index

| Issue | Action | Verified scope comment |
|---|---|---|
| [#1](https://github.com/jimthompson5802/agentic-ml/issues/1) | none | — |
| [#2](https://github.com/jimthompson5802/agentic-ml/issues/2) | none | — |
| [#3](https://github.com/jimthompson5802/agentic-ml/issues/3) | none | — |
| [#8](https://github.com/jimthompson5802/agentic-ml/issues/8) | none | — |
| [#9](https://github.com/jimthompson5802/agentic-ml/issues/9) | comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/9#issuecomment-6699582014) |
| [#10](https://github.com/jimthompson5802/agentic-ml/issues/10) | comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/10#issuecomment-6699582465) |
| [#11](https://github.com/jimthompson5802/agentic-ml/issues/11) | comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/11#issuecomment-6699582885) |
| [#12](https://github.com/jimthompson5802/agentic-ml/issues/12) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/12#issuecomment-6699583742) |
| [#13](https://github.com/jimthompson5802/agentic-ml/issues/13) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/13#issuecomment-6699584423) |
| [#14](https://github.com/jimthompson5802/agentic-ml/issues/14) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/14#issuecomment-6699585176) |
| [#15](https://github.com/jimthompson5802/agentic-ml/issues/15) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/15#issuecomment-6699586004) |
| [#16](https://github.com/jimthompson5802/agentic-ml/issues/16) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/16#issuecomment-6699586819) |
| [#17](https://github.com/jimthompson5802/agentic-ml/issues/17) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/17#issuecomment-6699587594) |
| [#18](https://github.com/jimthompson5802/agentic-ml/issues/18) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/18#issuecomment-6699588291) |
| [#19](https://github.com/jimthompson5802/agentic-ml/issues/19) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/19#issuecomment-6699588996) |
| [#20](https://github.com/jimthompson5802/agentic-ml/issues/20) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/20#issuecomment-6699589877) |
| [#21](https://github.com/jimthompson5802/agentic-ml/issues/21) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/21#issuecomment-6699590563) |
| [#22](https://github.com/jimthompson5802/agentic-ml/issues/22) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/22#issuecomment-6699591378) |
| [#23](https://github.com/jimthompson5802/agentic-ml/issues/23) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/23#issuecomment-6699592055) |
| [#26](https://github.com/jimthompson5802/agentic-ml/issues/26) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/26#issuecomment-6699592845) |
| [#27](https://github.com/jimthompson5802/agentic-ml/issues/27) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/27#issuecomment-6699594039) |
| [#28](https://github.com/jimthompson5802/agentic-ml/issues/28) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/28#issuecomment-6699594719) |
| [#29](https://github.com/jimthompson5802/agentic-ml/issues/29) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/29#issuecomment-6699595430) |
| [#30](https://github.com/jimthompson5802/agentic-ml/issues/30) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/30#issuecomment-6699596172) |
| [#31](https://github.com/jimthompson5802/agentic-ml/issues/31) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/31#issuecomment-6699597105) |
| [#32](https://github.com/jimthompson5802/agentic-ml/issues/32) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/32#issuecomment-6699597850) |
| [#33](https://github.com/jimthompson5802/agentic-ml/issues/33) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/33#issuecomment-6699598565) |
| [#34](https://github.com/jimthompson5802/agentic-ml/issues/34) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/34#issuecomment-6699599159) |
| [#35](https://github.com/jimthompson5802/agentic-ml/issues/35) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/35#issuecomment-6699600089) |
| [#36](https://github.com/jimthompson5802/agentic-ml/issues/36) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/36#issuecomment-6699600839) |
| [#37](https://github.com/jimthompson5802/agentic-ml/issues/37) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/37#issuecomment-6699601527) |
| [#38](https://github.com/jimthompson5802/agentic-ml/issues/38) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/38#issuecomment-6699602441) |
| [#39](https://github.com/jimthompson5802/agentic-ml/issues/39) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/39#issuecomment-6699603293) |
| [#40](https://github.com/jimthompson5802/agentic-ml/issues/40) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/40#issuecomment-6699604139) |
| [#41](https://github.com/jimthompson5802/agentic-ml/issues/41) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/41#issuecomment-6699604911) |
| [#42](https://github.com/jimthompson5802/agentic-ml/issues/42) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/42#issuecomment-6699605724) |
| [#43](https://github.com/jimthompson5802/agentic-ml/issues/43) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/43#issuecomment-6699606451) |
| [#47](https://github.com/jimthompson5802/agentic-ml/issues/47) | none | — |
| [#49](https://github.com/jimthompson5802/agentic-ml/issues/49) | none | — |
| [#54](https://github.com/jimthompson5802/agentic-ml/issues/54) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/54#issuecomment-6699607370) |
| [#55](https://github.com/jimthompson5802/agentic-ml/issues/55) | edit_and_comment | [Comment](https://github.com/jimthompson5802/agentic-ml/issues/55#issuecomment-6699608087) |
| [US-39](https://github.com/jimthompson5802/agentic-ml/issues/58) | create | — |
| [US-40](https://github.com/jimthompson5802/agentic-ml/issues/59) | create | — |

### Final-review state

All external synchronization work is verified. Publication/status/issue-ownership
annotations were saved locally for final review and accepted. Developer
“I like this, run those commands” subsequently authorized direct-main commit/push
using stash, switch, fast-forward pull and restore, without another PR. Recording
authorization before publication. No product implementation or runtime acceptance is
claimed. Eleven unavailable historical absolute evidence paths remain explicitly
unverified. Developer “yes i approve” approved the final documentation/backlog
gate on 2026-11-07 UTC. All four phases are accepted; this does not accept an
implemented MVP. Direct-main publication of the accepted records is now authorized;
no new implementation or issue mutation is inferred.

Final local checks: the scoped document validator rechecks unchanged Gate 2
criterion text, 222 design mappings, preserved references/plan bodies/index rows,
37 public exports, all versioned/intended-source links and issue body/action
parity. `git diff --check` and protected source/test/lock/policy diff are required
for this record-only handoff. Renewed scoped document check passed, including all
222 criterion mappings/unchanged text, preserved archives/plan bodies/index rows,
37 exports and versioned/intended-source links (final count in raw
`final-document-check.json`). Whitespace and protected source/test/lock/policy
diff passed. Additional raw checks confirm locked/state-reason/type metadata
unchanged for all 41 original issues. The same 11 external historical evidence
paths remain explicitly unavailable, not passing evidence.
Existing diagram/formatting evidence remains applicable; no changed executable
behavior or diagram fences require another runtime or rendering run.
