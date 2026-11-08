---
name: report-test-progress
description: Report remaining, total, completed, and failed test counts every minute for a pytest run already active in the current chat. Use when asked to monitor existing test progress; never launch or restart tests.
---

# Report test progress

Monitor the existing pytest session until it ends. This skill authorizes observation only: never start, restart, collect, interrupt, or modify a test run, install a plugin, or change its output settings.

## Find the session

Use the current conversation's pytest command, session handle, and accumulated output. If several active runs are plausible, ask which to monitor. If no accessible session exists, explain that this skill requires an existing pytest session in this chat and stop. Do not substitute another terminal's process.

Read the session using its existing tool: for an exec-command session, poll with `write_stdin` and empty `chars`; for a yielded functions exec cell, use `wait` only with its returned cell ID. Preserve the session handle and consume each returned output chunk once. Never send input or terminate the process.

## Count from evidence

- Use the selected test total from collection or xdist scheduling output, rather than the pre-deselection collected total. Do not sum identical worker collection totals.
- Track completed cases, remaining cases, failed cases, and setup/teardown errors from available output. Skips and expected failures are completed cases. A failed case is completed once its execution, including teardown, ends.
- Prefer explicit counters or identifiable per-case results. Interpret carriage-return updates as refreshed displays, not additional results. Avoid counting worker collection messages, failure-detail sections, or repeated summaries as new completions.
- Count each identifiable failed test case once. Report setup/teardown errors separately when pytest does so. Preserve pytest's expected-failure and strict unexpected-pass classifications.
- Compute remaining as selected total minus completed only when both counts are supported. Rounded percentages, progress dots without enough context, and missing earlier output cannot establish exact counts. Mark unavailable values as `unknown` and incomplete observations as `at least N observed`.
- Report collection errors separately; they are not failed test cases. Reconcile observations against the final pytest summary and disclose discrepancies rather than forcing counts to agree.

## Report every minute

Post an initial snapshot, then poll with waits no longer than 60 seconds. Use elapsed wall time to post a chat update approximately every 60 seconds, even when counts have not changed. Do not finish the monitoring turn while the accessible session is still running. Tool and message latency may delay delivery; do not promise exact timing.

Example:

> 125 of 589 tests remaining; 464 completed; 3 failed; 1 error. Elapsed: 3m.

During collection say `Collecting tests; total pending`. When evidence is incomplete, use a qualified message such as `Remaining/total unknown; at least 3 failures observed`. Report zero failures only when the output supports that count. A quiet poll means no new output, not completion.

## Finish

When the session ends, report immediately rather than waiting for the next minute. Include the final pytest summary, failed and skipped counts, errors when present, and the exit status when available. Distinguish passing completion, completion with failures, collection failure, interruption, and early stopping.

Report unfinished cases when known. Claim zero remaining only when evidence supports that all selected cases completed. If the session becomes inaccessible or has no final summary, report the last known counts and that completion could not be verified. Preserve existing logs and never rerun tests to fill a monitoring gap.
