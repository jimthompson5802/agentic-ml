# Development CI

## Development CI and diagnostic logs

[Development CI](../../.github/workflows/ci.yml) runs on pull requests and pushes to `main`, excluding changes limited to `docs/**` and root Markdown files. It selects `ubuntu-24.04`, uv 0.13.1 and Python 3.12. Checkout and setup-uv actions use immutable commit revisions. Each hosted job checks out source, verifies that no virtual environment exists, installs Python, and creates the environment using locked synchronization. Dependency caching is disabled. Runner images and Python 3.12 patch releases can change; the job records the actual image, OS, architecture and tool versions. See [configuration and local evidence](../verification/us-32-ip1.md); the hosted PR baseline and six failure/correction cases passed verification; the [default-branch push run also passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). See the [hosted evidence](../verification/us-32-ip2.md).

The workflow runs the shared development checks, with a separate step for every check. Two jobs collectively run the complete pytest suite without overlap:

| Job | Pytest selection | Supporting checks |
|---|---|---|
| Linux / Python 3.12 — Default tests | Configured default M1–6 | Lint, formatting, strict typing, CLI smoke |
| Linux / Python 3.12 — Other tests | Complement of M1–6 | Wheel/sdist build and isolated distribution verification |

Neither job has a `needs:` dependency. GitHub schedules them concurrently as
runner capacity permits, each on a separate Ubuntu runner with its own checkout,
Python environment and four pytest workers (`--dist=loadgroup`). Each job has a
30-minute timeout. A failure in one does not cancel the other; the workflow waits
for both and fails if either fails. Each repeats environment setup, diagnostics,
locked synchronization, lock consistency and final lock immutability checks.
No cross-job artifact transfer is needed.

The commands are:

```sh
# Default tests
uv run --locked pytest -n 4 --dist=loadgroup
# Other tests
uv run --locked pytest -n 4 --dist=loadgroup -m "not (milestone_1 or milestone_2 or milestone_3 or milestone_4 or milestone_5 or milestone_6)"
```

The explicit complement overrides the configured default and excludes any test
associated with M1–6, even when it also has another marker. Counts change with
the inventory; they are not hard-coded CI expectations.
 After successful synchronization, independent checks still run when an earlier check fails. Original nonzero exits fail the job. If setup fails, dependent checks are skipped and setup logs explain the failure. A final step compares the lockfile SHA-256 and tracked diff even after a setup/check failure, provided the initial checksum was captured. No command may silently regenerate the lockfile.

On a pull request, open **Checks**, select **Linux / Python 3.12 — Default tests** or **Linux / Python 3.12 — Other tests**, and expand the failed step. Alternatively, open **Actions → Development CI → run → job**. The **Set up job** log records the hosted runner image. Use the run menu's **Download log archive** option to save diagnostics; repository access and GitHub sign-in may be needed. GitHub documents [viewing and downloading logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).

With GitHub CLI, replace the placeholders below with the PR number and run ID:

```sh
gh pr checks --repo jimthompson5802/agentic-ml PR_NUMBER
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log-failed
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log
```

Reproduce failures locally from the same revision using the shared commands, Python 3.12 and uv 0.13.1. Compare `shasum -a 256 uv.lock` before and after, then run `git diff --exit-code -- uv.lock`. A passing local run does not establish hosted event delivery. The named **Build wheel and source distribution** and **Verify isolated installed distributions** steps use the distribution commands below verbatim. Verification runs only after a successful build; both steps can run despite an unrelated development check failure. Their original nonzero exits fail the job, and the final lock comparison still runs. Expand these steps for artifact hashes, both wheel results, retained workspace paths and subprocess diagnostics. The command output is available in the Actions log archive even after the temporary runner is destroyed; the workspace files themselves are not uploaded. Branch protection remains deferred US-34 work.

