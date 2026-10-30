---
name: create-pull-request
description: Create GitHub pull requests using the active repository's conventions, templates, and actual change evidence. Use when asked to open or create a PR; description-only requests remain unpublished.
---

# Create a pull request

A request to create a PR authorizes publication; a request for a description, example, or skill authorizes only that deliverable. A draft PR is published on GitHub; an unpublished draft description is not. Resolve that distinction if the request is ambiguous. Creating a PR does not authorize merging or advancing a developer gate.

## Establish the change and target

For CLI reads, follow the working repository's documented command forms and read helpers when they support the resolved target and required data. Resolve helper paths from that checkout. Use the generic commands below when no suitable helper applies; follow normal tool approval for unsupported reads. Keep pagination, completeness checks, and publication authorization requirements intact.

Resolve the checkout with `git rev-parse --show-toplevel` from the user's working directory. Read applicable repository instructions and their pointers to planning conventions and requirements. Resolve repository files from the checkout, independently of where this skill is installed.

Inspect the working tree, current branch, remotes, upstream, intended base, and full commit and file diff against that base. Use an explicitly requested GitHub target when supplied; otherwise reconcile remotes and `gh repo view --json nameWithOwner,url,defaultBranchRef` with the user's intent. Pay particular attention to fork head ownership and the upstream base repository. Use the requested base branch or resolve the target's default branch. Ask only when target, branch, or scope remains ambiguous. Pass the resolved `OWNER/REPO` explicitly to GitHub commands.

Distinguish committed changes that will appear in the PR from uncommitted work. Read linked issues and applicable specifications for scope, acceptance criteria, evidence, and gates. Complete authorized work and applicable checks before publication. Commit or push only intended work when authorized by the request and session context; use an ordinary push when needed to publish the head branch. Preserve unrelated work.

## Select and fill the template

Discover the target repository's current PR templates in supported locations such as `.github/`, the repository root, or `docs/`, including `PULL_REQUEST_TEMPLATE/` directories and a template named by repository instructions. Read the selected template on each invocation. When the target differs from the checkout, retrieve its template and instructions rather than assuming local copies apply. Use the requested template or the applicable default; resolve a material choice between alternatives with the user.

If no template exists, use a concise body describing the problem, resulting behavior, related issues, validation, and material limitations. If repository instructions mandate a template and it is unavailable, report the blocker.

The selected repository template takes precedence over PR-body templates supplied by other skills. Apply their compatible writing, evidence, and risk guidance within the repository template's sections, preserving its headings, fields, and checklists. Use another skill's template only when no repository template applies and repository instructions permit it. Honor explicit user overrides.

Write a concrete title and fill all applicable template sections from the actual diff and evidence, preserving headings and checklist items. Lead with the concrete problem and resulting behavior; scale detail to the change.

- Link related issues. Use `Closes #NUMBER` only when the PR fulfills that issue; use non-closing references for partial work and repository-qualified references for cross-repository issues. Replace unused closing placeholders with an explanation.
- Where planning conventions apply, identify the implementation phase and deliverables from the actual plan. For work outside a planned implementation phase, say so briefly. Use the repository's terminology.
- Map applicable acceptance criteria to changes and evidence, documenting exceptions and incomplete work.
- Record checks actually performed and their results. Discover available tooling from the checkout and instructions. Explain unavailable or inapplicable checks based on evidence; proposed commands are not test results.
- Mark checkboxes only when evidence supports them. Leave developer approval and reviewer items pending until the corresponding review occurs. Opening a PR does not satisfy an approval gate.
- Describe material risks and limitations. Use repository URLs and sanitized evidence, keeping credentials and personal paths out of published content.

For a description-only request, return the prepared content without requiring authentication or publishing a branch or PR. State any remote facts that could not be checked.

## Publish and verify

1. Verify `gh` availability and authentication with `gh --version` and `gh auth status`. Ask the user to authenticate manually if needed.
2. Resolve the remote head explicitly, including its owner for a fork. Before publishing, check existing PRs:

   ```bash
   gh pr list --repo OWNER/REPO --state all --head HEAD_BRANCH --base BASE_BRANCH --json number,title,state,url
   ```

   Replace placeholders before execution. Inspect relevant candidates to confirm head repository ownership, head branch, and base. Return an existing open PR for the same work; ask before reopening or replacing closed or merged work if intent is unclear.
3. Write the complete Markdown body with real newlines to a unique temporary UTF-8 file outside tracked project files, using a file-writing tool or safely quoted input. Use `--body-file` to preserve literal Markdown and shell metacharacters.
4. Once the remote head contains the intended commits and creation is authorized, publish once:

   ```bash
   gh pr create --repo OWNER/REPO --base BASE_BRANCH --head HEAD_OR_OWNER_COLON_HEAD --title 'Actual change title' --body-file /tmp/UNIQUE-pr-body.md
   ```

   Substitute the resolved branches, fork owner if needed, title, and actual temporary path. Add `--draft` for a requested draft PR. Apply labels, reviewers, assignees, or milestones only when requested or required by repository instructions or applicable template defaults; confirm their availability before publication.
5. Verify the returned PR with `gh pr view --repo OWNER/REPO PR_NUMBER --json number,title,body,url,baseRefName,headRefName,headRepositoryOwner,isDraft`. Confirm content, head ownership, branches, and draft status against the prepared result, as well as any requested metadata. Remove only the operation's temporary file after successful verification.

If creation fails or its outcome is uncertain, inspect any returned URL and query relevant head/base PRs before retrying. Retry only when reliable inspection establishes that no matching PR was created and the cause is resolved. When publication or verification remains uncertain, retain the prepared body, report the limitation, and stop. Use the environment's approval mechanism for sandbox restrictions.

Return the PR title and URL, validation results, and remaining gates or limitations. For description-only requests, identify the content as unpublished.
