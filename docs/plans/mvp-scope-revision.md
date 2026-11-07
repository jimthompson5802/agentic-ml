# MVP scope, user stories, and design revision

## Scope, source and authorization

Source: developer conversation, 2026-11-06, proposed plan “Revise the MVP scope,
user stories, and design”; developer “Implement the plan.” This instruction
approves the execution plan and authorizes IP1. It does not approve Gate 1 or
later implementation gates, nor the proposed criterion-level scope reductions.
Branch: `refactor-milestones-user-stories`; baseline
`0a7b64389cf663290d3bf4fc7063aae29ef8f20c`. Pre-existing change: reassessment
entry in `CHECKPOINTS.md`, preserved.

This is documentation/backlog maintenance, not a new toolkit story. Do not
invent an owning product story ID. Follow the repository
[plan template](../templates/user-story-implementation-plan.md),
[scope-change procedure](../../.agents/skills/manage-plan-scope/SKILL.md), and
[verification policy](../development/verification.md#phase-and-story-verification).
GitHub issues govern scope. Gate 1 now authorizes local
[story revisions](../specs/user-stories.md); the
[design](../specs/agentic-ml-harness-design.md) is aligned in IP3 under Gate 2 approval.
Product implementation waits for source reconciliation and publication.

Deliver local, reviewable revisions, then synchronize approved changes to GitHub.
No product code, dependencies, tests, executable behavior, or acceptance of
unfinished capability is included. Commits, pushes and PRs require separate
direction. The explicitly approved publication package is limited to GitHub
issue edits, new issues and scope-decision comments in IP4.

## Proposed MVP outcome

Trusted local code; separate experiment project; CSV/Parquet selection, filtering
and joins; reproducible splits; training-only scikit-learn pipelines; CPU tabular
classification/regression; baseline comparison and bounded tuning; consistent
evaluation and fitted artifacts; MLflow records; native DVC dataset and pipeline
reproduction; Python/notebook use with external assistant help. Preserve
development/testing gates.

Assistant-supported experimentation is an explicit MVP acceptance scenario, not
merely a possible use of the public interfaces. The data scientist owns an
external coding-assistant session that prepares project code, invokes the
installed toolkit and DVC, inspects MLflow results, and makes a validation-based
revision before final testing. The
[walkthrough specification](../reviews/mvp-scope-criterion-dispositions.md#assistant-supported-walkthrough)
defines the steps, expected outputs and evidence. No managed adapter is required.

Defer managed agents, mandatory experiment phase approvals, enforced security
isolation, durable workflow recovery, comprehensive uncommitted/untracked source
restoration, autonomous acquisition and additional ML frameworks. Reproduction
uses committed code/configuration, locked dependencies, versioned data and seeds.
No guarantee of preventing deliberate Python/API bypass or holdout-file access.

Proposed delivery: M1 complete one classification experiment end to end; M2
validate regression, customization, fresh-kernel notebook use and committed-project
reproduction. M0 acceptance and M50 history remain intact. Old M1–6 assignments
remain in the migration record; deferred capabilities are uncommitted roadmap
items, not silently reassigned to M99.

## Review and scope-change history

- Plan review: Approved for IP1 execution by “Implement the plan,” 2026-11-06.
- Gate 1: Approved, 2026-11-06, developer “i approve gate 1 and authorize phase 2”.
- Gate 2: Approved, 2026-11-06, developer “I approve gate 2 and authorize phase 3”.
- Gate 3: Approved, 2026-11-06, developer “I approve Gate 3; commit the changes”.
  Local commit authorized; Phase 4 execution/source publication not requested.
  Final acceptance remains pending.
- Change ID: MVP-SC-01, 2026-11-06.
- Reason: original lightweight experiment MVP has expanded into a supervised agent
  platform; narrow remaining delivery to a complete usable experiment.
- Impact: existing criterion dispositions, M1–6 sequencing, supporting designs,
  accepted/pending decisions and future usage of implemented interfaces.
- Decision: Approved at Gate 1, 2026-11-06, developer “i approve gate 1 and authorize phase 2”.
- Existing approvals/evidence remain historical facts. Do not weaken tests,
  remove evidence, close verification obligations, or imply new acceptance.
- Resume: Commit approved IP3 locally; await publication direction and source-link prerequisites before IP4.

### MVP-SC-02 — Explicit assistant-supported walkthrough

- Date/source: 2026-11-06, developer “make the assistant-support walkthrough explicit”.
- Decision: Refinement authorized by its request; included in Gate 1 approval,
  2026-11-06, developer “i approve gate 1 and authorize phase 2”.
- Change: Make scientist-directed external assistant use a required MVP scenario,
  including setup, extraction, feature engineering, baseline/tuning, validation-based
  revision, final evaluation, MLflow inspection and DVC reproduction.
- Impact: Refines IP1-T4 scope presentation; IP2-T3 must assign walkthrough outcomes
  to the proposed first-experiment/DVC integration story criteria; IP3-T4 must
  update the design walkthrough and acceptance traceability. Preserve the 204
  existing criterion IDs/dispositions; new criteria are assigned only in IP2.
- Verification: Renew document/link/source checks. Future executable/manual
  evidence must name one concrete assistant product/version and record prompts,
  actions, outputs and run/data identities; this does not promise multiple products.
- Gates/resume: This records the requested refinement, not Gate 1 approval or
  permission to edit authoritative stories/design or publish issues. Resume IP2
  only after Gate 1 and progression authorization.

## IP1 — Baseline and scope disposition

Entry: developer execution instruction above. Outcome: complete issue snapshots,
criterion inventory, decision/plan impacts and old-to-new milestone mapping.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP1-T1 | Complete | Save this plan; preserve branch/worktree | None | Plan, progress, gates, sources recorded | Revision process |
| IP1-T2 | Complete | Retrieve every story issue body/metadata/all comments with final metadata refresh | T1 | 41 stable snapshots, one comment; US-34/37/38 local-only; source differences recorded | Every issue criterion |
| IP1-T3 | Complete | Inventory all source criteria and approved design obligations in a separate disposition report | T2 | 204 unique rows; original text, milestone, status and proposed disposition; design/decision inventory | Every local/source criterion |
| IP1-T4 | Complete | Record scope change, milestone map, accepted decision and owning-plan impacts | T3 | MVP-SC-01, migration/impact tables and preserved obligations ready for Gate 1 | MVP-SC-01 |

Disposition: preserve completed US-01/02/03/05/31/32/33/35/36; revise
US-09–16/18/20/21/24/26/27; defer US-04/06/07/08/17/19/22/23/25/28/29/30;
retain US-34/37/38 backlog. Preserve IDs. Split retained/deferred clauses explicitly;
do not disguise narrowing as unchanged coverage. Assign new criterion numbers
only in IP2. Distinguish criterion implementation from story/milestone acceptance.

**Gate 1:** Approved, 2026-11-06. Developer “i approve gate 1 and authorize phase 2”
approved criterion dispositions, milestone mapping, design reductions and explicit
assistant walkthrough. IP2 authorized. This does not approve Gate 2 or design edits.

## IP2 — Stories and delivery milestones

Entry: Gate 1 approval and progression authorization.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP2-T1 | Complete | Revise authoritative stories using approved matrix | Gate 1 | All 204 original IDs preserved; 57 revised, 65 explicitly deferred, retained/accepted/backlog wording preserved | Approved source dispositions |
| IP2-T2 | Complete | Replace remaining MVP delivery with M1/M2 and migration map | T1 | Classification end-to-end first; regression/usability/reproduction second; old assignment/anchor history preserved | Revised milestone exits |
| IP2-T3 | Complete | Add integration stories US-39/40; map explicit assistant walkthrough outcomes | T2 | 18 criteria allocated; M1/M2 slices and ASW-01–08 owners/evidence recorded | New US-39/40 criteria; ASW-01–08 |
| IP2-T4 | Complete | Prepare exact GitHub titles/bodies/comments and action manifest locally | T3 | 69 draft files; 32 edit/comment, three comment-only, six no-action and two new-issue actions; no external writes | Issue/local consistency |
| IP2-T5 | Complete | Record follow-up code gaps and their story/criterion owners | T4 | Runnable defaults, optional basic planning, estimator/training integrations, data/features/results/reproduction and verification boundaries owned | MVP delivery ownership |

Closed accepted issues remain closed. Preserve original scope and acceptance
history. New integration criteria cover separate project setup through MLflow
results, and DVC reproduction/cache reuse/dependency invalidation/missing or corrupt
inputs. Component criteria retain ownership rather than being duplicated.

**Gate 2:** Approved, 2026-11-06. Developer “I approve gate 2 and authorize phase 3”
approved revised stories, criteria, milestones and local issue drafts. IP3 design/
guidance alignment authorized. Gate 3 publication authorization remains pending.

Review artifacts: [revised stories](../specs/user-stories.md),
[migration and follow-up ownership](mvp-scope-story-migration.md),
[unpublished issue package](mvp-scope-issues/README.md),
[IP2 verification evidence](../verification/mvp-scope-revision-ip2.md).

## IP3 — Design and guidance alignment

Entry: Gate 2 approval and progression authorization.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP3-T1 | Complete | Revise overview and architecture decisions | Gate 2 | Design 0.15 and ADR-008 state approved MVP scope; all earlier decisions/history distinguished | Approved MVP scope |
| IP3-T2 | Complete | Revise interface, execution/governance, data/features, delivery and layout topics | T1 | Active contracts match local stories; trusted-code and optional-path boundaries explicit | Revised source criteria |
| IP3-T3 | Complete | Preserve old blueprint as a reference; write concise active MVP blueprint | T2 | 37 exports checked; three full 0.14 references preserved; future platform catalogue not prerequisite | API ownership/status |
| IP3-T4 | Complete | Align traceability, README, walkthrough and applicable developer instructions; make external assistant interaction explicit | T3 | All 222 criteria mapped, ASW-01–08 explicit, commands/status truthful; development controls preserved | Criterion/design coverage; ASW-01–08 |
| IP3-T5 | Complete | Annotate affected plans/evidence indexes; refresh checkpoints | T4 | Eight historical plan bodies and 160 index rows preserved; issue package refreshed; checks and historical evidence limits recorded | MVP-SC-01 |

Ownership: project owns extraction/custom transformations/model choices;
scikit-learn owns fit/predict/search; MLflow owns records/artifacts; DVC owns
data/pipeline execution/cache; toolkit owns setup/validation/helpers/evaluation
and linkage. Preserve implemented APIs. Specify compatibility changes as later
story work. Do not finalize unnecessary future APIs/wire schemas.

**Gate 3:** Approved, 2026-11-06, developer “I approve Gate 3; commit the changes”.
Aligned design and refreshed issue package approved; local commit authorized.
This instruction does not request Phase 4 execution, push/PR/merge or issue writes.
Referenced source publication and explicit progression remain prerequisites to IP4.

Review: [design overview](../specs/agentic-ml-harness-design.md),
[assistant walkthrough](../specs/example-walkthrough.md),
[current blueprint](../specs/design/software-blueprint.md),
[criterion mapping](../specs/design/acceptance-traceability.md),
[refreshed issue package](mvp-scope-issues/README.md) and
[IP3 evidence](../verification/mvp-scope-revision-ip3.md).
Document publication at the referenced GitHub revision remains a prerequisite
before IP4 issue writes; commit/push/merge permissions are separate.

## IP4 — GitHub synchronization and handoff

Entry: Gate 3 approval, progression and explicit issue publication authorization.

| Task ID | Status | Action and relevant files or components | Depends on | Expected output / completion condition | Acceptance criteria |
|---|---|---|---|---|---|
| IP4-T1 | Not started | Refresh affected issues and reconcile concurrent changes | Gate 3 | Reviewed baseline remains applicable or changes return for review | Publication consistency |
| IP4-T2 | Not started | Publish approved issue edits/comments/new issues | T1 | Exact action manifest applied; history intact | Approved package |
| IP4-T3 | Not started | Re-retrieve issues and verify bodies/states | T2 | Local/GitHub equality; actual issue links recorded | Published source consistency |
| IP4-T4 | Not started | Final reconciliation, verification report and checkpoint handoff | T3 | Next implementation story identified with remaining work | All revision outcomes |

**Final gate:** Pending. Developer acceptance of documentation/backlog revision;
not product, story implementation or MVP acceptance. Do not close unfinished
stories as completed.

## Verification, evidence and execution rules

For each phase, use document/link/anchor/whitespace checks and appropriate
formatting checks for changed Python fences; parse any changed Mermaid diagrams.
Run `git diff --check`. Record commands and actual results in phase evidence.
Every existing criterion needs a disposition; every MVP criterion needs design,
delivery and verification ownership. Confirm no deferred control is an implicit
prerequisite. Check source/dependency/test identity unchanged.

TDD, executable milestone tests, full-suite and artifact drivers are inapplicable
to documentation-only changes, not waived for future code work. Preserve lock
identity, historical failures, skips, M1-ACCEPT-VERIFY and M50-ACCEPT-VERIFY;
reductions require explicit owning-plan scope decisions. IP4-T4 owns final
reconciliation; future executable work follows the verification policy.

Record task completion only after verification. Stop at every phase gate; silence
is not approval. Use scope-change procedure for material changes; pause affected
work. Follow the repository's three-attempt limit and retain failed evidence.
No automatic commits/pushes/PRs: the user's explicit plan limits publication to
the separately approved issue package.

## Actual evidence

IP1-T1–T4 technically complete, 2026-11-06. See
[criterion dispositions and impacts](../reviews/mvp-scope-criterion-dispositions.md)
and [IP1 evidence](../verification/mvp-scope-revision-ip1.md). All 204 criteria
accounted for; 41 stable issue snapshots, one comment, 28 explained wording
differences. Document/source validation passes, including 32 local links/anchors;
lock, stories, executable source and historical evidence unchanged. One copied
source link needed rebasing; corrective attempt 1 passed, details retained.
No executable verification or platform support is claimed. The original IP1
handoff left Gate 1 pending; the subsequent approval above authorized IP2.

IP2-T1–T5 technically complete, 2026-11-06. Revised local stories contain 222
criteria (204 original, 18 new); accepted/deferred/backlog wording and all original
anchors preserved. Issue bodies agree with local criteria and template structure;
all planned existing issue states remain unchanged. Document checks and whitespace
pass; source/tests/lock/design/history unchanged. See the linked IP2 evidence.
The original IP2 handoff left Gate 2 pending; subsequent approval above authorized IP3.

IP3-T1–T5 technically complete, 2026-11-06. Active design 0.15, 222-criterion
coverage, assistant walkthrough and developer guidance align with approved scope.
Historical references/plan bodies/index rows preserved. Scoped design checks,
formatting and seven Mermaid parses pass; 11 pre-existing external absolute raw
evidence paths remain unavailable and explicitly unverified. No product changes,
new runtime/platform evidence or external publication. Gate 3 subsequently approved
by “I approve Gate 3; commit the changes”; commit this approved snapshot locally.

## Local commit authorization

Developer “commit changes”, 2026-11-06, authorizes committing the current IP1/IP2
documentation, local story revisions and unpublished issue drafts. This preserves
the review snapshot; it does not approve Gate 2, start IP3, or authorize push/PR/
issue publication. Checkpoint and plan record authorization before the commit.

Developer “I approve Gate 3; commit the changes”, 2026-11-06, approves IP3 and
authorizes a local Conventional Commit of the design, historical references,
guidance, draft context and approval records. No source push/PR/merge, Phase 4
execution or remote issue writes requested. Record authorization before commit;
await publication direction with source-link prerequisites preserved.
