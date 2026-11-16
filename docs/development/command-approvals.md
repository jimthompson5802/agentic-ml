# Repository command approvals

## Repository-local Codex command approvals

The trusted project layer loads [command rules](../../.codex/rules/default.rules) for this repository. Restart Codex after changing these rules. They allow the shared locked test, type, lint, formatting and smoke commands above, plus the distribution and installation verification drivers. Ruff formatting edits and `ruff check --fix` are included. Existing bootstrap allowances remain available.

For automatic GitHub read approvals, place the repository argument immediately after the subcommand:

```sh
gh pr view --repo jimthompson5802/agentic-ml 44
gh issue list --repo jimthompson5802/agentic-ml
sh .codex/scripts/github-read.sh issues/8/comments --paginate --slurp
sh .codex/scripts/github-read.sh pulls/44/files --jq '.[].filename'
```

Allowed GitHub subcommands are issue list/view; PR list/view/diff/checks; run, workflow and release list/view; and repository view. The [API helper](../../.codex/scripts/github-read.sh) fixes github.com, the repository and GET. It accepts relative issues, pulls, actions/runs, actions/workflows, releases and commits endpoints, with optional `--paginate`, `--slurp` and `--jq EXPRESSION`. It rejects query strings, traversal, other hosts/repositories and arbitrary API options.

For complete issue retrieval, use the helper for issue metadata, every comment page, and the final metadata refresh. Omit `?per_page=100`; `--paginate --slurp` still retrieves all pages and returns an array of pages. Preserve the retrieval skill's unique-comment counts and snapshot checks. For PR review reads, use the helper for PR metadata, files, reviews and comments. Unsupported lookups, including labels, continue through normal tool approval without expanding the rules.

These are command-prefix permissions, not restrictions on every trailing argument, file access or subprocess. Tests execute trusted repository code outside the sandbox. Run commands directly: shell redirections or complex wrappers can still prompt. The new rules do not grant general Python, general `uv run`, dependency installation, Git writes or GitHub publication. User-level grants still apply and can be broader; project rules do not revoke them. Save these project allowances in the repository file rather than through TUI persistent approvals, which can write user-level rules.

## Autonomy within an authorized implementation phase

Once execution is authorized, follow the [phase approval policy](phase-approvals.md)
for contract review and automatic progression. Carry out scoped edits, selected tests,
relevant regressions, shared checks, formatting, diagnostics and corrective retries
without another development confirmation. Follow the existing verification policy
and three-attempt limit. Locked environment synchronization needed for that work
is included; dependency declaration or lockfile changes require the applicable
scope authorization.

Record the authorization reference, owning checkout, phase, verification scope,
authorized external actions and next required gate in the owning plan. Reference
that record from CHECKPOINTS.md. On resumption, verify the checkout and recover
those decisions before continuing. Request a new decision when authorization is
missing or the scope, risk or required gate materially changes.

Use the runtime approval mechanism whenever execution permissions require it.
An operational prompt does not revoke the recorded development authorization.
Keep public contract review, whole-story acceptance, publication and cleanup
boundaries defined by repository instructions and the invoked workflow.

## Command forms and evidence capture

Run supported checks and GitHub reads as direct commands with the documented
argument order. Perform file edits in a separate tool call. Examples:

```sh
uv run --locked pytest -n 4 --dist=loadgroup tests/integration/test_training.py
uv run --locked ruff check .
uv run --locked mypy src tests
gh pr view --repo jimthompson5802/agentic-ml 69
sh .codex/scripts/github-read.sh issues/28/comments --paginate --slurp
```

Choose test paths and selectors from the authorized plan. Preserve the existing
worker policy and any justified serial invocation. Run formatting edits separately
with the documented Ruff command.

Retain stdout/stderr and command outcomes under the [evidence policy](records.md).
Record the command, exit code, and available output separately from execution,
using file-writing tools to save accessible tool output literally. For long
output, use a supported tool log artifact or an existing reviewed verification
driver that retains complete output and the original exit code. Do not introduce
ad hoc Python or shell logging wrappers, or add pipes or output redirection to
otherwise allowed commands for evidence capture.

If the execution tool cannot provide complete required output, report the
limitation before choosing a capture method. Record missing or truncated output
explicitly; a truncated response or JUnit report alone does not satisfy complete
stdout/stderr retention. Use an existing reviewed verification driver when
available. If no supported capture method meets the requirement, request direction
on evidence capture rather than automatically retaining or creating a logging
wrapper. Runtime approval remains required whenever the selected method needs it.

Shell redirection and heredoc scripts can prevent a direct command allowance from
matching. Keep allowances specific to reviewed commands or constrained drivers;
an arbitrary-command shell or Python runner is not an equivalent replacement.

## Validate permissions in the active runtime

At setup, after permission/rule changes, or when an expected allowance fails:

1. Check the active Codex version, cwd and permission status in the actual host or
   container session. Confirm the story worktree, trusted project layer and active
   rules, rather than inferring container state from host configuration.
2. Check the documented command against the repository rules, for example:

   ```sh
   codex execpolicy check --pretty --rules .codex/rules/default.rules -- uv run --locked pytest tests/integration/test_training.py
   ```

   This checks the explicit file; it does not establish that the session loaded it.
3. Restart the affected Codex session after changing rules or project trust. Use
   one already-authorized focused check and supported repository read to confirm
   runtime behavior. Record any remaining prompt and its command form.
4. For a mismatch, inspect command wrapping, argument order, trust/loading and the
   active filesystem/network boundary before proposing another allowance. Respect
   managed restrictions. Reuse the verified setup during the phase unless it
   changes or an allowance fails again.
