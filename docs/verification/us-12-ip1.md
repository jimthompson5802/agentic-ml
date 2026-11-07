# US-12 IP1: Quality contract and public boundaries

**Status:** IP1-T1–T4 complete; Gate 1 approved by developer
“i approve ip1; commit”, 2026-11-07 UTC. Local commit authorized; IP2 authorization pending.
**Authorization:** Developer “start ip1”, 2026-11-07 UTC, after approved plan
commit `2cf6b33`. Branch `US-12-data-validation`, clean at entry.
Owning [plan](../plans/milestone-1-us-12.md), approved
[contract](../data-quality.md), [issue #15](https://github.com/jimthompson5802/agentic-ml/issues/15).

## Source refresh and scope reconciliation

Used the retrieve-github-issue workflow with repository-local GET helper:

```sh
sh .codex/scripts/github-read.sh issues/15
sh .codex/scripts/github-read.sh issues/15/comments --paginate --slurp
sh .codex/scripts/github-read.sh issues/15
sh .codex/scripts/github-read.sh issues/19
sh .codex/scripts/github-read.sh issues/19/comments --paginate --slurp
sh .codex/scripts/github-read.sh issues/19
```

All six reads succeeded. Each issue has one unique comment, matching metadata;
all comment pages retrieved, final metadata stable, neither resource is a PR.
#15 updated_at `2026-11-07T00:28:41Z`, comment 6699586004; #19 updated_at
`2026-11-07T00:28:54Z`, comment 6699588996. Complete refreshed JSON is retained
in `.dev-records/verification/20261107-2cf6b33-us12-ip1/issue-{15,19}.json`.
Tracked complete [#15](../plans/sources/us-12-issue-15.md) and
[#19](../plans/sources/us-12-issue-19.md) planning snapshots remain applicable.
No issue edits, closure, metadata changes or publication performed.

Issue #15 owns AC-01/05, M1. Issue #19 owns AC-02/03, M1; its AC-04 is deferred.
GitHub milestone fields are unset; issue bodies supply milestone assignments.
Active story/design/ADR-008 requirements agree with these decisions. Common
issue validation prose mentioning splits does not add them to #15. No criterion ownership change or new prerequisite story implementation is
required. Contract revision US-12-SC-01 below stays within configured-check scope.

Accepted supplier: `agentic_ml.extraction.extract_data` returns a native frame
and dictionary; its publication status is extraction completion, not quality.
US-11 plan's IP1–IP3 gate approvals, accepted criterion table and IP3 installed
evidence were inspected. These remain historical supplier evidence, not new
quality verification. No dependency on #19, US-13, strict plans or a runner is
introduced merely to call the quality functions.

## Concrete decisions for Gate 1 review

The contract settles the initial alternatives within IP1's approved decision
scope. Developer confirmed the decisions below at Gate 1 on 2026-11-07 UTC:

| Topic | Selected decision | Criterion |
|---|---|---|
| Interface | Separate `agentic_ml.data_quality` exports `validate_data`, generic `run_validated_step`, `DataQualityError`; native frames, dictionaries and a project callable | AC-01/05 |
| Checks | Seven rule kinds: columns, dtypes, row_count, nulls, duplicates, range, allowed_values; explicit required/advisory; no arbitrary rule callback/registry | AC-01 |
| Rules and edge cases | Canonical dtype strings; excess duplicate count; range/membership exclude missing values; nonfinite range values violate; malformed declarations error; missing data columns report failures | AC-01 |
| Reports | Explicit no-check mode returns not_checked/blocked false/empty checks; otherwise strict JSON, ordered checks and measured values, effective parameters/defaults, required/advisory, aggregate status/blocked; no row dumps or automatic persistence | AC-01/05 |
| Blocking | Validate private scalar-valued snapshot immediately before project operation; no old-report reuse; required failure carries report and prevents invocation | AC-05 |
| Process errors | Preserve original operation exception instance/type/traceback with stage note; no quality-success claim from process completion | AC-05 |
| Copying bounds | Scalar tabular cells; unsupported mutable object cells error; caller supplies stable inputs during call | AC-01/05 |
| Test expectations | Seven-rule baseline with fixed dtypes and independent literal mutations; sentinel file verifies operation proceeds/stops | AC-01/05 |

Developer “I want to support "no checks"” authorized US-12-SC-01 during IP1.
The initial contract rejected empty rules. The revised contract explicitly permits
`rules=[]`: report `not_checked`, no blocking, operation proceeds. Rules remain
an explicit required argument; malformed rules still error. Literal report and
sentinel cases are added to IP2/IP3; no acceptance criteria or verification
requirements were reduced, and unchecked data is never reported as passed.
Gate 1 review applies to this revised contract; no executable work is authorized.

The contract contains exact signatures, rule keys/defaults, per-check report shapes,
baseline/example check, empty/all-null/nullable/exact-boundary/error cases and
future consumer responsibilities. Plan now references that concrete matrix and
selected files rather than leaving alternatives for dependent implementation.
Developer Gate 1 approval confirms these public test boundaries and fixtures.

## Installation seam and downstream ownership

Inspected existing module-scoped artifacts fixture, distribution xdist group,
`test_extraction_from_both_artifact_paths`, extraction driver/probe/project module,
normal distribution verifier and retained-evidence policy. IP3 will add selected
`tests/installation/data_quality_project.py`, `check_data_quality.py`,
`verify_data_quality.py` and M1 `test_data_quality_from_both_artifact_paths`.
The new driver composes existing distribution verification/Invocation support;
it does not add another installer or change existing fixture scopes/timeouts.

Copied runtime-only project code/probes run under each actual wheel environment
with isolated Python and unrelated cwd. Both direct and independently rebuilt
wheel paths must pass inventory/origin/CLI/resources first, then extraction-to-
quality and every quality-rule family, explicit no-check, JSON/error and block/proceed assertions.
Each path saves identities/results before normal cleanup. Existing resources,
dependency requirements and lock stay unchanged. No new runtime guide loader,
CLI or registry is proposed.

Future US-10/14/15/18/39 consumers must invoke the selected validation boundary
before affected work and verify adoption in their own issue scope. A project
sentinel proves this component's blocking behavior, not a nonexistent toolkit
runner. No task is added to another story, so no execution index is needed.

## Verification and limitations

Developer review clarification: added a rule-by-rule explanation immediately
after the example, including default limits, required/advisory/no-check behavior
and the `prepare` operation. This explains the existing contract without changing
its behavior. Renewed document/source checks pass; Gate 1 is now approved; IP2 authorization remains pending.

IP1 is documentation/contract work only. TDD, M1 pytest, M1–6, locked sync,
lint/format/mypy/CLI, builds and standalone artifact drivers were not run:
no executable behavior or dependency/resource change exists to verify here.
Their owning tasks remain IP2-T1–T4 and IP3-T1–T4. Product acceptance is pending.

Document/source checker and results are retained in the raw records directory.
Checks cover changed local links/anchors, Python/JSON example syntax, stable
source snapshot parity, task/gate/criterion consistency, whitespace and equality
of source/tests/dependencies/resources to entry commit. No example imports the
future module and no example is represented as a successful runtime call.

Lock SHA-256 observed at entry:
`4b21570fb52b7a4eea94c5d85404e95afefe2d7c44eab014f2122fc9793d847b`.
Final document/source checks: **passed**, 48 local links/anchors and four
Python/JSON syntax blocks; both complete issue snapshots equal their refreshed
metadata/body/comments; task/gate/criterion consistency, source/tests/dependency/
resource equality and whitespace passed. Lock hash unchanged. Exact command:
`python .dev-records/verification/20261107-2cf6b33-us12-ip1/check-docs.py`;
final exit 0, output in raw `checks.log`. `git diff --check` also exited 0.
Observed document-check platform: Linux aarch64; no runtime/platform support
claim is added. The initial document checker falsely parsed Python type brackets as a Markdown
link; its original failure is retained in `checks-initial.log`. Checker corrective
attempt 1 excludes fenced code from Markdown-link parsing and renews all original
document checks. This is checker repair, not a product implementation failure;
no suppression, skip or weakened product assertion. Historical M1/M50 acceptance obligations and three skips
remain independently open; #19 criteria are not satisfied by this phase.

**Next action:** await explicit IP2 authorization. Developer “i approve ip1;
commit” approved the contract, fixture matrix and public boundaries and authorized
a local commit of IP1 documentation/evidence. No push, PR or GitHub writes requested.
