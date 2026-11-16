# MVP project status

Last updated: 2026-11-16 (UTC).

The MVP ends at Milestone 2. This overview includes its required stories and the
accepted M0 foundation. Repeated stories represent different milestone slices.
M50 contributor tooling and deferred roadmap stories are outside this table.

“Accepted and merged” records developer acceptance of the delivered scope and its
merge. Qualifications identify remaining integration or story work. “Open” means
the owning GitHub issue remains open; it does not imply implementation is underway.
Story acceptance does not establish milestone acceptance. M1 milestone acceptance
verification remains outstanding; the complete MVP has not been delivered.

US-14 AC-01–05 were accepted locally on 2026-11-16 UTC; publication/merge
remain pending. See the [plan](plans/milestone-1-us-14.md) and
[final verification](verification/us-14-ip3.md).

The accepted M1 preprocessing/recording delivery is US-15 training-only preprocessing (AC-01–03)
and US-26 MLflow recording (#17 AC-01–05), merged together in
[PR #68](https://github.com/jimthompson5802/agentic-ml/pull/68) as `a2c6262`
on 2026-11-15 UTC. Both hosted Linux CI jobs passed. See the
[US-15 plan](plans/milestone-1-us-15.md),
[US-26 recording plan](plans/milestone-1-us-26-recording.md) and
[publication evidence](verification/us15-us26-publication.md).
US-15 M2 restoration and US-26 comparison/provenance work remain open.
Issue #17 still appears open on GitHub despite acceptance of its delivered scope.

US-13 M1 AC-01/02 are accepted and merged in
[PR #66](https://github.com/jimthompson5802/agentic-ml/pull/66); issue #16
remains open for M2 restoration AC-03/04. See its
[plan](plans/milestone-1-us-13.md) and [evidence](verification/us-13-ip3.md).
US-41 distribution-based initialization is also accepted and merged in PR #65;
M50 tooling remains outside the MVP story count.

There are **13 distinct user stories with MVP implementation/acceptance work remaining**:

- **M1: 8 stories** — US-10, US-18, US-20, US-21, US-24,
  US-26 (remaining slices), US-27 and US-39.
- **M2: 9 stories/slices** — US-09, US-13, US-15, US-16, US-18,
  US-21, US-27, US-39 and US-40. Five are additional stories; four
  continue stories already counted in M1.

M1 delivers the first complete local classification experiment. M2 completes the
approved MVP with regression, customization, notebooks and committed-project
reproduction. Final integration acceptance verification remains required for both
milestones; accepted component work and passing CI do not establish MVP acceptance.
Historical M1/M50 verification obligations remain separately recorded in
[CHECKPOINTS.md](../CHECKPOINTS.md).

| Milestone | User story | Status |
|---|---|---|
| M0 — Foundation | US-31: Set up development environment ([#1](https://github.com/jimthompson5802/agentic-ml/issues/1)) | Accepted and merged |
| M0 | US-32: Verify changes automatically in CI ([#2](https://github.com/jimthompson5802/agentic-ml/issues/2)) | Accepted and merged |
| M0 | US-33: Build and verify toolkit package ([#3](https://github.com/jimthompson5802/agentic-ml/issues/3)) | Accepted and merged |
| M1 — Complete one experiment | US-01: Install a pinned toolkit version ([#8](https://github.com/jimthompson5802/agentic-ml/issues/8)) | Accepted and merged |
| M1 | US-02: Initialize an experiment project ([#9](https://github.com/jimthompson5802/agentic-ml/issues/9)) | Accepted and merged; runnable defaults pending under US-39 |
| M1 | US-03: Define experiment objectives and boundaries ([#10](https://github.com/jimthompson5802/agentic-ml/issues/10)) | Accepted and merged; simpler workflow pending under US-39 |
| M1 | US-05: Reject invalid configurations ([#11](https://github.com/jimthompson5802/agentic-ml/issues/11)) | Validation accepted and merged; training integration pending |
| M1 | US-10: Run and inspect local experiments ([#13](https://github.com/jimthompson5802/agentic-ml/issues/13)) | Open |
| M1 | US-11: Extract local experiment data ([#14](https://github.com/jimthompson5802/agentic-ml/issues/14)) | Accepted and merged |
| M1 | US-12: Validate data and define reproducible splits ([#15](https://github.com/jimthompson5802/agentic-ml/issues/15), [#19](https://github.com/jimthompson5802/agentic-ml/issues/19)) | AC-01/02/03/05 accepted and merged; both issues closed; AC-04 deferred |
| M1 | US-13: Version datasets with DVC ([#16](https://github.com/jimthompson5802/agentic-ml/issues/16)) | M1 AC-01/02 accepted and merged; M2 remains open |
| M1 | US-14: Build and compare feature pipelines ([#20](https://github.com/jimthompson5802/agentic-ml/issues/20)) | Accepted locally; [verification](verification/us-14-ip3.md) complete; publication/merge pending |
| M1 | US-15: Preserve training-only preprocessing ([#21](https://github.com/jimthompson5802/agentic-ml/issues/21)) | M1 AC-01–03 accepted and merged; M2 AC-04 remains open |
| M1 | US-18: Train scikit-learn classification models ([#28](https://github.com/jimthompson5802/agentic-ml/issues/28)) | Open |
| M1 | US-20: Tune within declared search limits ([#30](https://github.com/jimthompson5802/agentic-ml/issues/30)) | Open |
| M1 | US-21: Evaluate experiment outputs consistently ([#31](https://github.com/jimthompson5802/agentic-ml/issues/31)) | Open |
| M1 | US-24: Evaluate on a separate test partition ([#32](https://github.com/jimthompson5802/agentic-ml/issues/32)) | Open |
| M1 | US-26: Record and compare experiment results ([#17](https://github.com/jimthompson5802/agentic-ml/issues/17), [#33](https://github.com/jimthompson5802/agentic-ml/issues/33), [#43](https://github.com/jimthompson5802/agentic-ml/issues/43)) | #17 AC-01–05 accepted and merged; #17 still open; #33/#43 remain open |
| M1 | US-27: Define and run native DVC stages ([#23](https://github.com/jimthompson5802/agentic-ml/issues/23)) | Open |
| M1 | US-39: Complete an assistant-supported classification experiment ([#58](https://github.com/jimthompson5802/agentic-ml/issues/58)) | Open |
| M2 — Usability and reproduction | US-09: Execute saved notebooks ([#12](https://github.com/jimthompson5802/agentic-ml/issues/12)) | Open |
| M2 | US-13: Restore datasets with DVC ([#16](https://github.com/jimthompson5802/agentic-ml/issues/16)) | Open |
| M2 | US-15: Restore fitted preprocessing ([#21](https://github.com/jimthompson5802/agentic-ml/issues/21)) | Open |
| M2 | US-16: Use compatible project components ([#22](https://github.com/jimthompson5802/agentic-ml/issues/22), [#27](https://github.com/jimthompson5802/agentic-ml/issues/27)) | Open |
| M2 | US-18: Train scikit-learn regression models ([#28](https://github.com/jimthompson5802/agentic-ml/issues/28)) | Open |
| M2 | US-21: Reproduce outputs within declared tolerances ([#31](https://github.com/jimthompson5802/agentic-ml/issues/31)) | Open |
| M2 | US-27: Reproduce committed pipelines and reuse stages ([#18](https://github.com/jimthompson5802/agentic-ml/issues/18), [#23](https://github.com/jimthompson5802/agentic-ml/issues/23)) | Open |
| M2 | US-39: Demonstrate regression, customization and notebooks ([#58](https://github.com/jimthompson5802/agentic-ml/issues/58)) | Open |
| M2 | US-40: Reproduce an experiment through DVC with assistant support ([#59](https://github.com/jimthompson5802/agentic-ml/issues/59)) | Open |

## Sources and updates

[User stories](specs/user-stories.md) define milestone scope. Linked GitHub issues
govern implementation scope; [implementation plans](plans/) and
[verification reports](verification/) hold approvals and evidence.
[CHECKPOINTS.md](../CHECKPOINTS.md) records the current development position and
outstanding verification obligations.

Issue states were rechecked against GitHub on 2026-11-15 UTC. Acceptance and
merge status were reconciled with the owning plans and current checkpoint;
PR #68 merge status was independently checked on GitHub.

Update this summary and its date when story acceptance, merge status or approved
MVP scope changes. Verify each update against the owning issues, plans and evidence;
this overview does not replace those records or authorize implementation.
