# US-03 IP4 — Delegated experiment approvals

Status: IP4-T1–T4 complete; developer IP4 gate approved by “i approve ip4”
on 2026-10-31. Developer accepted US-03 by “i accept us-03; we can bypass the full-suite test for now; commit; push” on 2026-10-31.

Authorized by developer “excute ip4” on 2026-10-31. IP3 approval and clean
`US-03-experiment-boundaries` checkout confirmed at entry. Issue #10 complete
body and all comment pages refreshed: zero unique comments, stable metadata
`updated_at=2026-10-30T02:06:20Z`; Milestone 1 / US-03-AC-01–05 unchanged.
Sandbox GitHub reads failed intermittently; escalated reads and final metadata
refresh succeeded. No issue mutation.

Public test boundaries remain those approved at IP1: typed approval/revocation
API, independent readiness/inspection, CLI from unrelated cwd, and direct/rebuilt
installed wheels in separate projects. These establish scope/record semantics,
not authenticated authorship, history protection or execution authorization.
Changed modules: new `approvals/`, planning models/parsing/resolution and CLI
planning dispatch; new approval schemas. Direct selectors: integration planning
and plan-approval modules, plus installed planning probes through both wheel
paths. Existing boundary evidence is reused unless affected. Unchanged caller,
initialization, upgrade, scheduling and full-suite checks belong to
**M1-ACCEPT-VERIFY**, including the reserved milestone test. This follows the
approved local-verification scope revision at the end of the owning plan.

## TDD evidence

Focused cycles run serially to keep one behavior's red/green result immediate.
Each uses `uv run --locked pytest SELECTOR -q --basetemp=/private/tmp/NAME`.

| Cycle / selector in `tests/integration/test_plan_approvals.py` | Red | Green / correction |
|---|---|---|
| `test_approved_proposal_becomes_ready_without_changing_plan` | `us03-ip4-red1c`: missing public approvals package | `us03-ip4-green1`: return decisions list mismatched declared tuple; correction 1 converts typed result. `green1b`: 135 passed including planning regressions, 3.20s |
| `test_revocation_blocks_only_its_approval_and_new_approval_restores_readiness` | `red2`: missing RevocationRequest, 1 failed/1 passed | `green2`: 2 passed, 0.33s |
| `test_invalid_final_approval_blocks_readiness` | `red3`: 4 failed/10 passed (unknown field, blank reviewer, reason type, calendar date) | `green3`: schema correction rejected first three, date still failed (1 failed/13 passed); correction 2 adds explicit calendar parsing. `green3b`: 14 passed, 1.18s |
| `test_cli_records_approval_and_revocation` | `red4b`: approve command absent | CLI dispatch implementation; final phase run renews evidence |
| `test_null_proposal_is_resolved_and_inspection_exposes_approval` | `red5`: explicit nullable proposal remained blocked | Distinguish absent proposal from explicit null; expose current approval IDs/authentication in inspection; final phase run renews evidence |
| `test_approval_store_cannot_overlap_configured_storage` | `red6`: approval incorrectly published into configured artifact storage | Reuse storage-overlap validation before creating approval directories; `green6`: 29 passed, 2.95s |

Setup failures preserved: `red1` missing fixture; `red1b` incorrect `tests`
namespace import; corrected to pytest's existing module import and reached the
valid red in `red1c`. `red4` incorrectly invoked nonexistent `python -m
agentic_ml`; corrected test to the existing `agentic-ml` console interface before
recording behavior red. These are setup failures, not product reds. No assertions,
timeouts or criteria weakened. Initial lint found import ordering; Ruff fixed
imports/formatting. Initial strict mypy passed (37 files).

Additional boundary coverage required no corrections: missing/deleted records,
duplicate JSON fields, malformed JSON, orphan revocation, ignored private staging,
symlinks, retained stale locks, explicit-only/unresolved approval rejection, and
old/new metric, budget and search-source identities. `us03-ip4-boundaries`:
28 passed, 2.56s. `green5` renewed API/CLI/null-proposal and planning regressions:
150 passed, 4.56s. TDD tests and acceptance assertions were retained throughout.

## Final verification

Tested base `8ea1a8266972ef84eb87fd71956141727133b5b5` plus the IP4 working-tree
changes. Developer “commit changes” subsequently authorized the local IP4 commit;
Git history records its result. No push authorized. Final maintained source/schema/test/build
inventory: 52 files, aggregate SHA-256
`49c5e88161cbe320d5214dcce2f7cd7a5294a1bad41c8f0d36245e3333fc73aa`;
individual hashes saved in `/private/tmp/us03-ip4-evidence/input-hashes.json`.

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_plan_approvals.py tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths tests/integration/test_distribution_verification.py::test_missing_approval_schema_fails_installed_inventory --basetemp=/private/tmp/us03-ip4-final --junitxml=/private/tmp/us03-ip4-final.xml --durations=10
```

**165 passed, 30.63s, four workers, exit zero.** Mapping: planning models,
parsing, resolution, storage and CLI → 134 planning tests plus 29 approval tests;
new approval modules/schemas → 29 approval tests and the installed probe;
installed schema inventory and approval/planning interfaces → two distribution
selectors. The second selector proves removal of an approval schema fails
installed inventory. No assertions, timeouts or test scheduling rules changed.
Full collection: **295/296**, one reserved milestone test deselected. The final
selected run executes 165; 131 total cases are outside this phase selection.

The both-wheel test builds fresh artifacts and runs
`tests/installation/verify_planning.py`, which invokes distribution validation
and then the installed planning probe under each environment's Python `-I`.
Each retains the 16 installed boundary cases/public checker and now adds API and
CLI approval/revocation, authentication labeling, six invalid-record mutations
through independent CLI/API verification, reapproval and old/new-source checks.
Imports use installed packages outside the checkout and declared runtime
dependencies. Both genuine sdist-rebuilt and directly built wheel bytes match.
No source path injection, fabricated origin, dataset reading or notebook execution.

| Artifact | SHA-256 |
|---|---|
| Direct wheel and genuine sdist-rebuilt wheel | `241c30b11afc8b888ccbdd010506312d4dc6a19cf6b76b743a163280e3c772b3` |
| Source distribution | `3e58ac4b442c5530e66fd880acf19dcb03f3ab76dad16ce77a732a13c501d0af` |

Artifacts, copied XML, distribution/install logs, and two example-walkthrough
JSON transcripts are preserved in `/private/tmp/us03-ip4-evidence/`.
Original phase temporary projects remain in `/private/tmp/us03-ip4-final/`.
Distribution environment:
`/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-lwguhvpo`.

Shared checks all passed: `uv sync --locked --group dev`, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked ruff format --check .`
(111 formatted files), `uv run --locked mypy src tests` (37 files),
`uv run --locked agentic-ml --version` (`0.1.0`), and `git diff --check`.
Initial cache-denial results were infrastructure failures; each affected command
was rerun with escalation and passed. Initial inventory type check found two
always-truthy class assertions; replaced them with public request construction
checks, then strict types passed. No suppressions or dependencies added.
Lock hash before/after unchanged:
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.

Both installed environments also executed the new example inputs in separate
projects through CLI resolve → inspect → approve → verify-current → revoke →
blocked verify. Explicit input readiness and delegated blocking/approval passed;
datasets remained absent. Example notebook-path documentation was corrected to
the existing initialization filename before those checks. Local Markdown target
and anchor check: **44 passed** initially; **63 passed** after final plan/checkpoint
edits. All 52 recorded executable/schema/build hashes remained unchanged after
documentation updates; final whitespace check passed.

Platform: macOS 15.7.9 arm64, Python 3.12.15, uv 0.13.1, pytest 9.1.1,
xdist 3.8.0, PyYAML 6.0.3, jsonschema 4.26.0 (installed environment).
No new Linux/Windows or remote-filesystem evidence. Source/scientific outcomes,
training candidate validation, runtime isolation and execution remain outside scope.

## Acceptance reconciliation and handoff

| Criterion | Evidence / result |
|---|---|
| US-03-AC-01 | IP2/IP3 evidence retained; renewed direct parsing and classification/regression/mode cases, nullable/delegated proposals, installed brief resolution pass |
| US-03-AC-02 | IP3 checker evidence retained; renewed resolver narrowing/rejection and 16 installed CLI/API boundary cases on both paths pass |
| US-03-AC-03 | Preserved immutable plans, manifests/checksums, old/new identities, corruption and independent inspection pass; approvals remain separate and do not change plan ID |
| US-03-AC-04 | Proposed-only and unresolved decisions block; exact approved proposals become ready; revocation/malformed/stale/wrong-binding/missing/orphan cases block; self-declared reviewer and authentication:none observable |
| US-03-AC-05 | Renewed root/cwd/path tests plus installed example commands from unrelated cwd pass; notebook cwd preserved without execution |

All required direct phase evidence passes. IP1/IP2/IP3 approvals are retained;
valid earlier evidence is reused, affected evidence renewed above. Under the
approved scope revision, **M1-ACCEPT-VERIFY** owns the 131 unselected tests
(including reserved milestone acceptance), unchanged initialization/caller,
upgrade/scheduling/other artifact regressions, full `-m ""` suite, and remaining
milestone/manual/platform checks. No full-suite verification is claimed here.
No known required direct failure remains.

Approval records authenticate nobody and cannot protect against schema-valid
fabrication or history rewriting. Verification establishes present record scope
and integrity, not who approved. Input readiness grants no access/execution
permission or scientific acceptance. Development/testing approvals remain
separate. **Developer approved the final IP4 gate by “i approve ip4” on
2026-10-31. All phase gates are approved; US-03 was
accepted on 2026-10-31 with the additional full-suite run deferred.** Approval-record-only documentation changes preserve the verified
executable inputs; document/whitespace checks apply instead of another test run.


## Additional full-suite run requested after phase approval

Developer “run full test suite including the milestone_acceptance test” authorized:

```sh
uv run --locked pytest -n 4 --dist=loadgroup -m "" --basetemp=/private/tmp/us03-full-20261031 --junitxml=/private/tmp/us03-full-20261031.xml --durations=20
```

All 296 tests collected, including the reserved milestone acceptance test.
The run was in progress when approved IP4 work was committed as `63aa346` under
developer “commit changes”. Developer subsequently directed “stop the test”.
Ctrl-C stopped session 93414 with **exit 130 / KeyboardInterrupt**. A total of
120 completion markers were observed (176 tests had not reported completion),
with no reported failures. There was no final pytest summary, and the requested
JUnit XML was not written. This is an interrupted run, not passing full-suite
evidence; the milestone acceptance test's completion is not independently known.
Existing basetemp/output evidence is preserved. An escalated `pgrep` check for the
basetemp, execnet workers and initialization/planning verification drivers returned
no matching processes. No test code or executable inputs changed; phase evidence
remains valid. US-03 acceptance and commit/push/publication were subsequently authorized;
publication outcomes are recorded in the owning plan and checkpoint.


## Story acceptance

Developer “i accept us-03; we can bypass the full-suite test for now; commit; push”
(2026-10-31) accepts the story and authorizes publication. US-03-SC-02 in the
owning plan records the temporary full-suite deferral. All five acceptance
criteria have passing direct evidence, and all phase gates are approved. The
interrupted full run is preserved without a success claim. M1-ACCEPT-VERIFY and
CI retain their full-suite obligations; Milestone 1 is not accepted by this decision.


## Publication and subsequent static finding

Accepted implementation `63aa346` and acceptance records `2c9522d` were pushed.
[PR #46](https://github.com/jimthompson5802/agentic-ml/pull/46) is open against main.
The required [static COMMENT review](https://github.com/jimthompson5802/agentic-ml/pull/46#pullrequestreview-5726207741)
identified one Medium issue: cost/currency consistency is skipped for complete
delegated proposals, so matching approval can make a conflicting budget ready.
This case was not covered by the passing phase evidence. No reproduction or
implementation correction was performed during static review. The finding is
unresolved and requires separate developer direction. CI was pending when read.
The owning plan records publication/review scope and the follow-up handoff.


Subsequent developer-authorized correction is technically complete locally; see
[correction evidence](us-03-cost-currency-correction.md) and US-03-SC-03. The
developer accepted the correction and authorized publication, a PR summary and
resolution of the inline thread. The owning plan records final outcomes.
Historical acceptance and verification results above are preserved.
