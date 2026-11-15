# Proposed PR structure for US-15 and US-26

Status: proposal only, 2026-11-15. No push, PR, new branch, history rewrite,
main merge, issue closure or cleanup is authorized or performed.

The developer accepted US-15's M1 AC-01/02/03 slice and US-26's #17 scope,
authorized local record commits, and requested this explanation before
publication. [US-15 plan](../plans/milestone-1-us-15.md) and
[US-26 plan](../plans/milestone-1-us-26-recording.md) own acceptance evidence.
US-15 #21 remains open for M2 AC-04. US-26 #33/#43 remain separate.

## Recommendation: one combined implementation PR

| Item | Concrete proposal |
|---|---|
| Repository | `jimthompson5802/agentic-ml` |
| Base | `main` |
| Head | Existing `US-15-preprocessing`, after separately authorized integration of US-26's acceptance-record commit |
| Suggested title | `feat: preserve and track training-only preprocessing` |
| Coverage | US-15 #21 M1 AC-01/02/03 plus accepted US-26 #17 recording scope; actual installed producer-to-consumer preservation |
| Issue references | Reference #17 and #21 explicitly; avoid automatic closing keywords under the current no-closure instruction |
| Verification | Both owners' M1–6 runs: 924 passes, one existing authorized skip, zero failures/errors; installed direct/rebuilt matrix, shared checks and independent preservation review |
| Merge order | One implementation PR; no second implementation PR from `US-26-mlflow` |

Both existing branches contain merge commit
`3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1`, whose parents preserve the separate
approved preprocessing and tracking histories. Against local `main` at
`1a9864a645084af8cfcec580b1db5fa045a67859`, that combined revision contains
nine commits and both implementations. Creating two independent PRs against
`main` now would present the same implementation in both diffs.

Both owning sessions concur with this recommendation. US-26 committed five
acceptance/status documents at `ecbceb2aa213da8f3e3f1d902eb9f730eca6bbb7`,
subject `docs(us-26): record issue 17 acceptance`: checkpoint, its plan/report, tracking guide and
shared index. US-15 is committing its final plan/report/checkpoint/index and
this proposal. US-15 and US-26 therefore have separate acceptance documents after the common
combined revision. The recommended head must contain both final record commits.
That requires an ordinary future merge of the US-26 acceptance tip into the
existing US-15 branch, preserving both records and resolving any overlapping
checkpoint/index text. This proposal does not perform or authorize that merge.
It needs explicit direction before publication; no rebase, split, reset or new
PR branch is necessary. The final PR diff must reconcile CHECKPOINTS.md with
the actual target-main state and preserve all historical obligations.

With one implementation PR, either merge-commit or squash policy can deliver the
combined source without a second PR repeating it. A merge commit preserves the
story commits as target-branch ancestry. A squash preserves their resulting
content in one target commit; local story commits remain in branch history but
are not ancestors of that squash. Do not subsequently open another main-based
implementation PR from the old story tips without reconciling that ancestry.
No merge method is selected or executed here.

## Alternative: stacked combined implementation and acceptance records

| PR | Base | Head | Review scope and order |
|---|---|---|---|
| 1 | `main` | `US-26-mlflow` at its accepted #17 tip | Contains both implementations and shared installed matrix, not just tracking; review and merge first |
| 2 | Initially `US-26-mlflow` | `US-15-preprocessing` at its accepted M1 tip | Shows US-15 final verification/acceptance documents from their common combined revision; retarget to `main` after PR 1 merges |

PR 2 does not represent a separate preprocessing implementation: PR 1 already
contains that code. The acceptance tips may diverge in shared documents, so
conflicts must be reviewed before merging PR 2. Preserving PR 1's head as an
ancestor of `main` through a merge commit lets PR 2 retain its documentation-only
diff after retargeting. Squashing or rebasing PR 1 would leave the original
combined ancestry outside `main`; then PR 2 can redisplay combined changes until
an explicitly authorized history reconciliation. This adds review and merge
ordering work, so the single combined PR is preferred.

## Before any publication

Read-only GitHub checks on 2026-11-15 confirm remote `main` at
`1a9864a645084af8cfcec580b1db5fa045a67859`, matching local `main`/`origin/main`,
and no open PRs. The repository allows merge commits, squash and rebase merges.
No fetch or remote write occurred; recheck these mutable facts before publishing.
Under later authorization, integrate both accepted record tips,
review the final complete diff and reconcile the checkpoint. Renew affected
verification if executable or build inputs change; documentation-only record
integration needs document/whitespace checks and preserved input hashes.
Then use the repository PR template and its required publication/review workflow.
No remote write or issue-state change follows from acceptance in this session.
