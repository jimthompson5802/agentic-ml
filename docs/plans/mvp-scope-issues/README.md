# Unpublished MVP issue package

**Unpublished.** Gates 1–3 approved scope, stories, aligned design and this package.
The latest instruction authorizes a local commit, not Phase 4 execution or remote writes.
No issue body, title, comment, state, label or milestone has been changed remotely.

[Manifest](manifest.json) is the exact action inventory. Bodies follow the repository
user-story template; comments preserve scope history. All existing issue states,
labels and other metadata remain unchanged. New US-39/40 use `enhancement`, no
assignee/milestone/type. US-39 spans M1/M2 in one issue; US-40 is M2. US-34/37/38
remain local-only; no issue creation for them is included.

- 32 open issues: edit title/body and add the prepared scope-decision comment.
- 3 accepted issues (#9/#10/#11): comment only; do not rewrite or reopen acceptance.
- 6 accepted foundation/tooling issues: no action.
- 2 new issues: US-39 first experiment and US-40 DVC reproduction.

## Publication prerequisites

Refresh complete bodies/comments at IP4 and reconcile concurrent changes. Verify
write authentication, supported metadata and duplicate absence before creation;
reconcile uncertain writes before retrying. No issue closure/reopening is planned.

The local active design is now version 0.15; archived 0.14 is historical reference.
The GitHub `blob/main` source links below identify intended final locations;
new/updated documents are not published yet. Before IP4, ensure the reviewed
stories/design/report/plan exist at the referenced revision, or prepare explicit
reviewed revision links and renew package approval. Commit/push/merge permission
is separate; do not publish broken links or infer that source publication is
already authorized. Phase 3 may refine the package's references, requiring final
Gate 3 review of exact bodies/comments.

## Draft actions

| Target | Action | Desired title | Body | Scope comment |
|---|---|---|---|---|
| [#1](https://github.com/jimthompson5802/agentic-ml/issues/1) | none | US-31: Set up the harness development environment | — | — |
| [#2](https://github.com/jimthompson5802/agentic-ml/issues/2) | none | US-32: Verify changes automatically in CI | — | — |
| [#3](https://github.com/jimthompson5802/agentic-ml/issues/3) | none | US-33: Build and verify the harness package | — | — |
| [#8](https://github.com/jimthompson5802/agentic-ml/issues/8) | none | US-01: Install a pinned harness version | — | — |
| [#9](https://github.com/jimthompson5802/agentic-ml/issues/9) | comment | US-02: Initialize an experiment project | — | [Draft](issue-9-comment.md) |
| [#10](https://github.com/jimthompson5802/agentic-ml/issues/10) | comment | US-03: Define experiment objectives and boundaries | — | [Draft](issue-10-comment.md) |
| [#11](https://github.com/jimthompson5802/agentic-ml/issues/11) | comment | US-05: Reject invalid configurations before execution | — | [Draft](issue-11-comment.md) |
| [#12](https://github.com/jimthompson5802/agentic-ml/issues/12) | edit_and_comment | US-09: Execute saved notebooks | [Draft](issue-12-body.md) | [Draft](issue-12-comment.md) |
| [#13](https://github.com/jimthompson5802/agentic-ml/issues/13) | edit_and_comment | US-10: Run and inspect local experiments | [Draft](issue-13-body.md) | [Draft](issue-13-comment.md) |
| [#14](https://github.com/jimthompson5802/agentic-ml/issues/14) | edit_and_comment | US-11: Extract local experiment data | [Draft](issue-14-body.md) | [Draft](issue-14-comment.md) |
| [#15](https://github.com/jimthompson5802/agentic-ml/issues/15) | edit_and_comment | US-12: Validate extracted data | [Draft](issue-15-body.md) | [Draft](issue-15-comment.md) |
| [#16](https://github.com/jimthompson5802/agentic-ml/issues/16) | edit_and_comment | US-13: Version and restore datasets with DVC | [Draft](issue-16-body.md) | [Draft](issue-16-comment.md) |
| [#17](https://github.com/jimthompson5802/agentic-ml/issues/17) | edit_and_comment | US-26: Record experiment runs in MLflow | [Draft](issue-17-body.md) | [Draft](issue-17-comment.md) |
| [#18](https://github.com/jimthompson5802/agentic-ml/issues/18) | edit_and_comment | US-27: Reproduce committed experiments | [Draft](issue-18-body.md) | [Draft](issue-18-comment.md) |
| [#19](https://github.com/jimthompson5802/agentic-ml/issues/19) | edit_and_comment | US-12: Assess data quality and define splits | [Draft](issue-19-body.md) | [Draft](issue-19-comment.md) |
| [#20](https://github.com/jimthompson5802/agentic-ml/issues/20) | edit_and_comment | US-14: Build and compare authored feature pipelines | [Draft](issue-20-body.md) | [Draft](issue-20-comment.md) |
| [#21](https://github.com/jimthompson5802/agentic-ml/issues/21) | edit_and_comment | US-15: Preserve training-only preprocessing | [Draft](issue-21-body.md) | [Draft](issue-21-comment.md) |
| [#22](https://github.com/jimthompson5802/agentic-ml/issues/22) | edit_and_comment | US-16: Use compatible project preprocessing | [Draft](issue-22-body.md) | [Draft](issue-22-comment.md) |
| [#23](https://github.com/jimthompson5802/agentic-ml/issues/23) | edit_and_comment | US-27: Run and reuse native DVC stages | [Draft](issue-23-body.md) | [Draft](issue-23-comment.md) |
| [#26](https://github.com/jimthompson5802/agentic-ml/issues/26) | edit_and_comment | US-06: Choose an algorithm execution mode | [Draft](issue-26-body.md) | [Draft](issue-26-comment.md) |
| [#27](https://github.com/jimthompson5802/agentic-ml/issues/27) | edit_and_comment | US-16: Use compatible project models | [Draft](issue-27-body.md) | [Draft](issue-27-comment.md) |
| [#28](https://github.com/jimthompson5802/agentic-ml/issues/28) | edit_and_comment | US-18: Train scikit-learn models | [Draft](issue-28-body.md) | [Draft](issue-28-comment.md) |
| [#29](https://github.com/jimthompson5802/agentic-ml/issues/29) | edit_and_comment | US-19: Manage PyTorch execution | [Draft](issue-29-body.md) | [Draft](issue-29-comment.md) |
| [#30](https://github.com/jimthompson5802/agentic-ml/issues/30) | edit_and_comment | US-20: Tune within declared search limits | [Draft](issue-30-body.md) | [Draft](issue-30-comment.md) |
| [#31](https://github.com/jimthompson5802/agentic-ml/issues/31) | edit_and_comment | US-21: Evaluate experiment outputs consistently | [Draft](issue-31-body.md) | [Draft](issue-31-comment.md) |
| [#32](https://github.com/jimthompson5802/agentic-ml/issues/32) | edit_and_comment | US-24: Evaluate a selected model on a separate test partition | [Draft](issue-32-body.md) | [Draft](issue-32-comment.md) |
| [#33](https://github.com/jimthompson5802/agentic-ml/issues/33) | edit_and_comment | US-26: Compare runs and report final results | [Draft](issue-33-body.md) | [Draft](issue-33-comment.md) |
| [#34](https://github.com/jimthompson5802/agentic-ml/issues/34) | edit_and_comment | US-04: Approve delegated experiment decisions | [Draft](issue-34-body.md) | [Draft](issue-34-comment.md) |
| [#35](https://github.com/jimthompson5802/agentic-ml/issues/35) | edit_and_comment | US-07: Generate reviewable experiment notebooks | [Draft](issue-35-body.md) | [Draft](issue-35-comment.md) |
| [#36](https://github.com/jimthompson5802/agentic-ml/issues/36) | edit_and_comment | US-08: Explore interactively under the same controls | [Draft](issue-36-body.md) | [Draft](issue-36-comment.md) |
| [#37](https://github.com/jimthompson5802/agentic-ml/issues/37) | edit_and_comment | US-17: Respect immutable supplied components | [Draft](issue-37-body.md) | [Draft](issue-37-comment.md) |
| [#38](https://github.com/jimthompson5802/agentic-ml/issues/38) | edit_and_comment | US-22: Improve models using development feedback | [Draft](issue-38-body.md) | [Draft](issue-38-comment.md) |
| [#39](https://github.com/jimthompson5802/agentic-ml/issues/39) | edit_and_comment | US-30: Connect the first agent with preserved runtime guidance | [Draft](issue-39-body.md) | [Draft](issue-39-comment.md) |
| [#40](https://github.com/jimthompson5802/agentic-ml/issues/40) | edit_and_comment | US-23: Approve workflow phase progression and scope changes | [Draft](issue-40-body.md) | [Draft](issue-40-comment.md) |
| [#41](https://github.com/jimthompson5802/agentic-ml/issues/41) | edit_and_comment | US-25: Resume interrupted workflows | [Draft](issue-41-body.md) | [Draft](issue-41-comment.md) |
| [#42](https://github.com/jimthompson5802/agentic-ml/issues/42) | edit_and_comment | US-30: Use interchangeable agent adapters | [Draft](issue-42-body.md) | [Draft](issue-42-comment.md) |
| [#43](https://github.com/jimthompson5802/agentic-ml/issues/43) | edit_and_comment | US-26: Link MLflow results to project provenance | [Draft](issue-43-body.md) | [Draft](issue-43-comment.md) |
| [#47](https://github.com/jimthompson5802/agentic-ml/issues/47) | none | US-35: Clean up successful verification environments | — | — |
| [#49](https://github.com/jimthompson5802/agentic-ml/issues/49) | none | US-36: Give pytest ownership of verification workspaces | — | — |
| [#54](https://github.com/jimthompson5802/agentic-ml/issues/54) | edit_and_comment | US-28: Diagnose data gaps and propose acquisition | [Draft](issue-54-body.md) | [Draft](issue-54-comment.md) |
| [#55](https://github.com/jimthompson5802/agentic-ml/issues/55) | edit_and_comment | US-29: Acquire data and measure its effect within approved limits | [Draft](issue-55-body.md) | [Draft](issue-55-comment.md) |
| US-39 | create | US-39: Complete an assistant-supported tabular experiment | [Draft](new-us-39-body.md) | — |
| US-40 | create | US-40: Reproduce an experiment through DVC with assistant support | [Draft](new-us-40-body.md) | — |

## Source and verification

- [Revised local stories](../../specs/user-stories.md).
- [Approved scope disposition baseline](../../reviews/mvp-scope-criterion-dispositions.md).
- [Migration, follow-up ownership and assistant mapping](../mvp-scope-story-migration.md).
- [Phase 2 evidence](../../verification/mvp-scope-revision-ip2.md).

Body acceptance text must equal its corresponding local criterion text; template
frontmatter is excluded and all criteria remain unchecked. Deferred criteria are
explicitly labeled, not presented as MVP deliverables. Earlier accepted evidence
is not regenerated by comments or documentary scope changes.
