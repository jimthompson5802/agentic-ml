# US-03 — Delegated cost/currency correction

Status: correction tasks C1-T1–T3 complete; developer accepted the correction on 2026-10-31.

Developer “I accept the recommendation.” authorizes correcting the Medium
[PR #46 finding](https://github.com/jimthompson5802/agentic-ml/pull/46#discussion_r4434227411).
US-03-SC-03 and correction tasks in the owning plan record scope and confirmed
public boundaries. Prior story acceptance and phase approvals remain historical;
this follow-up correction received its own approval by developer “i accept the fix,
commit and push to remote; summarize the fix to PR comment and mark as resolved.”
Commit/push, summary reply and thread resolution are authorized. No merge authorized.
Full-suite deferral under SC-02 remains in force.

Issue #10 complete body and every comment page refreshed on 2026-10-31:
zero unique comments equals reported count; final metadata unchanged at
`2026-10-30T02:06:20Z`. Milestone 1 / US-03-AC-01, AC-03 and AC-04 govern this
correction. IP1 requires cost/currency both set or both null; unresolved choices
remain blocked. No cost measurement or monetary enforcement is added.

## TDD and defect reproduction

Serial focused tests provide immediate red/green feedback through the existing
public planning and approval boundaries. No private calls or internal mocks.

1. Red: `uv run --locked pytest tests/integration/test_plan_approvals.py::test_delegated_cost_cannot_hide_a_missing_currency -q --basetemp=/private/tmp/us03-cost-red1`
   — one failure: conflicting complete cost proposal with null currency
   incorrectly published an integrity-valid plan with `approval_required`.
2. Before the fix, invoke installed CLI `plan approve` then `plan verify` on that
   exact preserved plan. Both exited 0; verification incorrectly returned
   `input_ready`, integrity true and an approval ID. This independently confirms
   the complete reported bypass, rather than only an incorrect diagnostic.
3. Correct the pair check in `planning/parsing.py`: a value is known if explicit
   or a delegation object containing `proposal`, including explicit null. Apply
   pair consistency when both values are known; defer the pair check if either
   proposal is absent, retaining pending/approval blocking.
4. Green: `uv run --locked pytest tests/integration/test_plan_approvals.py tests/integration/test_planning.py -q --basetemp=/private/tmp/us03-cost-green1`
   — **164 passed, 5.86s**, including the original regression.
5. Verify the same previously approved invalid preserved plan after the fix:
   CLI exits 2, `blocked`, integrity false, diagnostic `conflicting_budget`, field
   `budget.max_cost`, source `brief.md`, line 54/column 11. No old record is rebound
   or deleted. Existing invalid bundles must fail current validation.
6. Extend coverage for delegated cost, delegated currency and both delegated:
   valid finite/non-null and both-null pairs become ready only after approval;
   conflicting pairs reject publication; six missing-proposal cases stay blocked
   and cannot receive approval. `uv run --locked pytest tests/integration/test_plan_approvals.py -q --basetemp=/private/tmp/us03-cost-pair-matrix`
   — **48 passed, 4.26s**. No extra product correction required.

Reproduction bundle is retained at
`/private/tmp/us03-cost-red1/test_delegated_cost_cannot_hid0/project with spaces`,
plan `sha256:be4e2120e7cddda2a60f74b484085c12fcde43cbe3adedf797ae12ded966dcf1`,
approval `fb651e0c-29de-4f7e-9c80-63380a73d053`.
One functional correction; no failed corrective attempts. Original assertions,
criterion IDs, check selection and timeouts retained. Added no suppressions.

## Direct verification scope

- Changed product module: `planning/parsing.py`; direct public regressions in
  `test_planning.py` and `test_plan_approvals.py` cover parsing, conflict diagnostics,
  source preservation, approval and readiness integration.
- Changed installed probe: `tests/installation/check_planning.py` adds **18
  CLI/API cost/currency cases** per installed environment, including resolution,
  approval and independent verification from an unrelated cwd. Both real wheel
  paths renew artifact evidence for the changed parser.
- Selector: the two integration modules plus
  `test_distribution_verification.py::test_planning_from_both_artifact_paths`.
- Deferred to M1-ACCEPT-VERIFY: full suite/reserved milestone test and unchanged
  initialization/caller, upgrade/scheduling, other artifact regressions. No fresh
  whole-suite claim. Historical 165-pass evidence remains valid for unchanged
  behavior only; changed parser evidence and artifacts are renewed here.

## Shared checks and final evidence

Locked sync/lock, Ruff lint, strict mypy and version smoke passed. Initial sync/
lock attempts hit the uv cache sandbox restriction; escalated retries passed.
Initial format check required formatting the new parser expression; Ruff
formatted it and the next check passed (111 files). This whitespace-only change
requires renewing final artifacts/direct evidence against final bytes.

First four-worker direct run (before formatting renewal):

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_planning.py tests/integration/test_plan_approvals.py tests/integration/test_distribution_verification.py::test_planning_from_both_artifact_paths --basetemp=/private/tmp/us03-cost-final --junitxml=/private/tmp/us03-cost-final.xml --durations=10
```

**183 passed, 45.03s**, including both wheels; installed driver 41.58s. This is
intermediate evidence because parser formatting changed while verification was
underway. Assertions/timeouts retained; final-byte artifact evidence is renewed
with a separate fresh basetemp and XML.

Final-byte shared lint/format/types/version passed: Ruff lint clean, 112 formatted
files, mypy 37 source files, version `0.1.0`. Full collection:
**314/315**, one reserved milestone test deselected. The 183 direct cases select
134 planning, 48 approval and one installed orchestrator test; 132 total cases
remain outside this correction selection with M1-ACCEPT-VERIFY.

Shared commands: `uv sync --locked --group dev`, `uv lock --check`,
`uv run --locked ruff check .`, `uv run --locked ruff format --check .`,
`uv run --locked mypy src tests`, `uv run --locked agentic-ml --version`,
and `git diff --check`. All final results passed. Documentation-only handoff edits
passed 44 local target/anchor checks; all 52 verified input hashes remained fixed.

Final renewal command uses the same three selectors and four-worker options
above, with `--basetemp=/private/tmp/us03-cost-final-renewed`,
`--junitxml=/private/tmp/us03-cost-final-renewed.xml`, and `--durations=10`.
**183 passed, 45.72s, exit zero**. Installed orchestrator: 42.48s. Both
installed logs explicitly confirm all 18 new CLI/API cases. No failure remains
in the required direct or shared checks. The full suite was not run.

Tested base: `d4ce70c762d7766c92b2a049f8ae126640d60f20` plus parser/probe/test
working-tree changes. Final inventory: 52 Python/schema/build files, aggregate
SHA-256 `78d31d04ea34e1b27cd937af3b72672824d0589fde62330109f779ee3ce038a1`.

| Artifact | SHA-256 |
|---|---|
| Direct and genuine sdist-rebuilt wheel | `e043f66c143bd76f85ea7ec65fc39fddcb203620fc76dcf1aee34e35969379e8` |
| Source distribution | `d3bc6df341e6daa8ad85757617df5698ca13a93c9e8da5c455fba148e6e44c02` |

Artifacts, individual input hashes, copied final XML and both installed logs are
retained in `/private/tmp/us03-cost-correction-evidence/`. Original temporary
projects remain in `/private/tmp/us03-cost-final-renewed/`; installed environments
are under `/private/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/agentic-ml-distributions-eowyy6fm`.
The probe verifies installed imports outside the checkout with Python `-I` and
declared runtime dependencies. Both wheel hashes match; no source injection.

Lock unchanged before/after: 
`90b77d41ded3a40f047e2df636b7fd645a8e94c772caca194b7f96aa084c0fd8`.
No dependencies, schema versions, runtime approval identity claims, test markers,
assertions or timeouts changed. Platform: macOS 15.7.9 arm64, Python 3.12.15,
uv 0.13.1, pytest 9.1.1, xdist 3.8.0; no new Linux/Windows evidence.

## Review gate

AC-01: optional budgets and nullable proposals retained. AC-03: exact-source
plan capture/readiness and both installed artifact paths renewed; the previously
approved invalid bundle now fails current independent verification. AC-04:
complete conflicts reject, valid proposed pairs require approval, and absent
proposals remain pending. Existing unaffected phase evidence is retained.

Developer accepted the correction and authorized commit/push, a summary reply in
PR #46 and resolution of the finding. Correction committed as `ff1db21` and pushed; PR head verified. The
[fix summary reply](https://github.com/jimthompson5802/agentic-ml/pull/46#discussion_r4434259600)
was posted and verified in the original review thread, which was resolved at the
developer's explicit request (`isResolved: true`). Publication outcome records
change documentation only; verified executable inputs remain unchanged. All 132 unselected cases and full-suite
obligations remain with M1-ACCEPT-VERIFY.

