# MVP project status

Last updated: 2026-11-07.

The MVP ends at Milestone 2. This overview includes its required stories and the
accepted M0 foundation. Repeated stories represent different milestone slices.
M50 contributor tooling and deferred roadmap stories are outside this table.

“Accepted and merged” records developer acceptance of the delivered scope and its
merge. Qualifications identify remaining integration or story work. “Open” means
the owning GitHub issue remains open; it does not imply implementation is underway.
Story acceptance does not establish milestone acceptance. M1 milestone acceptance
verification remains outstanding; the complete MVP has not been delivered.

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
| M1 | US-12: Validate data and define reproducible splits ([#15](https://github.com/jimthompson5802/agentic-ml/issues/15), [#19](https://github.com/jimthompson5802/agentic-ml/issues/19)) | Validation, assessment and splits accepted and merged; [PR #62](https://github.com/jimthompson5802/agentic-ml/pull/62) squash-merged 2026-11-08 |
| M1 | US-13: Version datasets with DVC ([#16](https://github.com/jimthompson5802/agentic-ml/issues/16)) | Open |
| M1 | US-14: Build and compare feature pipelines ([#20](https://github.com/jimthompson5802/agentic-ml/issues/20)) | Open |
| M1 | US-15: Preserve training-only preprocessing ([#21](https://github.com/jimthompson5802/agentic-ml/issues/21)) | Open |
| M1 | US-18: Train scikit-learn classification models ([#28](https://github.com/jimthompson5802/agentic-ml/issues/28)) | Open |
| M1 | US-20: Tune within declared search limits ([#30](https://github.com/jimthompson5802/agentic-ml/issues/30)) | Open |
| M1 | US-21: Evaluate experiment outputs consistently ([#31](https://github.com/jimthompson5802/agentic-ml/issues/31)) | Open |
| M1 | US-24: Evaluate on a separate test partition ([#32](https://github.com/jimthompson5802/agentic-ml/issues/32)) | Open |
| M1 | US-26: Record and compare experiment results ([#17](https://github.com/jimthompson5802/agentic-ml/issues/17), [#33](https://github.com/jimthompson5802/agentic-ml/issues/33), [#43](https://github.com/jimthompson5802/agentic-ml/issues/43)) | Open |
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

Update this summary and its date when story acceptance, merge status or approved
MVP scope changes. Verify each update against the owning issues, plans and evidence;
this overview does not replace those records or authorize implementation.
