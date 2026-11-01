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

