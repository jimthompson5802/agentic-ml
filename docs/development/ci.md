# Development CI

## Development CI and diagnostic logs

[Development CI](../../.github/workflows/ci.yml) runs on pull requests and pushes to `main`, without path filters. It selects `ubuntu-24.04`, uv 0.13.1 and Python 3.12. Checkout and setup-uv actions use immutable commit revisions. Each hosted job checks out source, verifies that no virtual environment exists, installs Python, and creates the environment using locked synchronization. Dependency caching is disabled. Runner images and Python 3.12 patch releases can change; the job records the actual image, OS, architecture and tool versions. See [configuration and local evidence](../verification/us-32-ip1.md); the hosted PR baseline and six failure/correction cases passed verification; the [default-branch push run also passed](https://github.com/jimthompson5802/agentic-ml/actions/runs/40975472618). See the [hosted evidence](../verification/us-32-ip2.md).

The workflow runs the shared development checks, with a separate step for every check. Its pytest command explicitly uses `-m ""` to run both verification groups on every CI run. After successful synchronization, independent checks still run when an earlier check fails. Original nonzero exits fail the job. If setup fails, dependent checks are skipped and setup logs explain the failure. A final step compares the lockfile SHA-256 and tracked diff even after a setup/check failure, provided the initial checksum was captured. No command may silently regenerate the lockfile.

On a pull request, open **Checks**, select **Linux / Python 3.12**, and expand the failed step. Alternatively, open **Actions → Development CI → run → job**. The **Set up job** log records the hosted runner image. Use the run menu's **Download log archive** option to save diagnostics; repository access and GitHub sign-in may be needed. GitHub documents [viewing and downloading logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs).

With GitHub CLI, replace the placeholders below with the PR number and run ID:

```sh
gh pr checks --repo jimthompson5802/agentic-ml PR_NUMBER
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log-failed
gh run view --repo jimthompson5802/agentic-ml RUN_ID --log
```

Reproduce failures locally from the same revision using the shared commands, Python 3.12 and uv 0.13.1. Compare `shasum -a 256 uv.lock` before and after, then run `git diff --exit-code -- uv.lock`. A passing local run does not establish hosted event delivery. The named **Build wheel and source distribution** and **Verify isolated installed distributions** steps use the distribution commands below verbatim. Verification runs only after a successful build; both steps can run despite an unrelated development check failure. Their original nonzero exits fail the job, and the final lock comparison still runs. Expand these steps for artifact hashes, both wheel results, retained workspace paths and subprocess diagnostics. The command output is available in the Actions log archive even after the temporary runner is destroyed; the workspace files themselves are not uploaded. Branch protection remains deferred US-34 work.

