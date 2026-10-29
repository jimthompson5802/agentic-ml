---
name: create-github-issue
description: Create GitHub issues using the active repository's templates and requirements, including user stories with sourced acceptance criteria. Use when asked to file or create issues; draft-only requests remain unpublished.
---

# Create a GitHub issue

A request to create an issue authorizes publication; a request for a draft, example, or skill only authorizes that deliverable. Creating an issue does not authorize implementation or advancing a developer gate.

## Resolve the repository and sources

Resolve the working checkout with `git rev-parse --show-toplevel` from the user's working directory. Read applicable repository instructions and follow their pointers to requirements and templates. Resolve repository files from that checkout, independently of where this skill is installed.

Use an explicitly requested GitHub repository when supplied. Otherwise inspect Git remotes and resolve the current repository with `gh repo view --json nameWithOwner,url`. Reconcile the result with the remotes and user intent, especially for forks or multiple remotes. Ask for a target only when it remains ambiguous. Use the resolved `OWNER/REPO` explicitly in every issue command; never inherit a repository name from an example or this skill's source repository.

Read the specification relevant to the requested issue. Preserve existing story identifiers, dependencies, scope boundaries, acceptance criteria, and developer gates. Use repository URLs for published references, keeping local absolute paths out of the body. If an authoritative source is missing, identify the gap rather than inventing requirements.

## Select and fill the template

Discover the target repository's issue templates, including Markdown templates and YAML issue forms in `.github/ISSUE_TEMPLATE/`, or a template required by repository instructions. Use the template matching the issue type and read its current content on each invocation, including drafts. If the target differs from the checkout, retrieve the target's templates and instructions rather than assuming the local copies apply.

When several templates plausibly apply, use the user's requested type or ask only if the choice materially affects the issue. If no template exists, use a concise body covering the problem or outcome, scope, acceptance criteria, and verification expectations. If repository instructions require a particular template and it is missing or unreadable, report that blocker instead of silently substituting another format.

- Preserve Markdown template headings and fields in order. For YAML forms, render the relevant field labels and responses as Markdown; the form schema itself is not an issue body. Honor required fields and conditional applicability. Use “Not specified” for unknown optional information and “Not applicable” where appropriate; resolve missing information that materially affects scope or acceptance before publishing.
- Preserve acceptance criteria as unchecked checkboxes, keeping implementation tasks distinct. Preserve source wording and local planning terminology; apply template-specific wording only where required. Carry forward required evidence and approval checkpoints without inventing phases or completed results.
- Keep approval checkpoints distinct from manual verification steps when the template includes both. Map them to the actual template fields rather than requiring particular field names.
- Exclude frontmatter and form configuration from the body. Apply nonempty supported metadata defaults unless overridden by the user, except GitHub issue types. Ignore template `type` defaults, including `Feature`; omit `--type` and issue-type API updates. Use the selected template and its labels to classify feature requests. Template name and description are template-selection information, not issue metadata. For an existing story, lead the title with its identifier unless repository conventions require otherwise.

Use a concrete title describing the outcome. Leave labels, assignees, projects, and milestones unset unless requested or supplied by applicable template defaults or repository instructions.

## Prepare and publish

For an unpublished draft, prepare and return the title and body without requiring GitHub authentication. State any remote information that could not be checked.

For publication:

1. Verify `gh` availability and authentication with `gh --version` and `gh auth status`. If authentication is missing, ask the user to authenticate manually; never collect credentials.
2. Search for existing work, including closed issues, using the resolved repository and actual story identifier or distinctive title:

   ```bash
   gh issue list --repo OWNER/REPO --state all --search 'STORY_ID in:title' --json number,title,state,url
   gh issue list --repo OWNER/REPO --state all --limit 100 --json number,title,body,state,url,createdAt
   ```

   Replace placeholders before execution. Inspect relevant matches from both lists; recent issues may not yet appear in search. Return an existing issue for the same work unless the user requested a separate issue.
3. Prepare the complete title and body before publication. Check them against the selected template and authoritative sources. Write the body with real newlines to a unique temporary UTF-8 file outside tracked project files using a file-writing tool or safely quoted input. Use `--body-file` to preserve Markdown and shell metacharacters literally.
4. Inspect installed CLI capabilities and verify that requested metadata and template defaults exist in the target repository. Use `gh label list --repo OWNER/REPO` and `gh api` as appropriate. Report unsupported defaults and omit them; resolve required metadata or lookup failures before publishing.
5. Record the attempt's start time and publish once with the resolved repository, actual title, temporary path, and confirmed metadata:

   ```bash
   gh issue create --repo OWNER/REPO --title 'Actual issue title' --body-file /tmp/UNIQUE-issue-body.md
   ```

6. Verify the returned issue using `gh issue view ISSUE_NUMBER --repo OWNER/REPO --json number,title,body,url`. Check the complete prepared content and resolved metadata, using `gh api` for fields unavailable through the CLI. Remove only the operation's temporary file after successful verification.

Use the environment's approval mechanism for sandbox restrictions. Reconcile any uncertain publication before retrying.

### Reconcile failed or uncertain creation

A nonzero exit can occur after issue creation, for example while applying metadata. Treat failed creation as potentially published.

1. Inspect any returned issue number or URL directly. Fetch recent issues without `--search`, comparing exact titles and prepared bodies. Inspect candidates individually and paginate if necessary to cover the entire attempt window. An empty search is insufficient evidence of failure.
2. Reuse a matching issue and repair only missing or incorrect authorized metadata. If multiple matches exist, report them and stop publication rather than guessing which to retain.
3. If the result remains uncertain, retain the prepared body and report the uncertainty. Authentication, permission, service, or incomplete-listing failures are blockers, not evidence that no issue exists.
4. Retry only after reliable inspection establishes that no matching issue was created, the failure is resolved, and no potentially in-flight operation remains. Reconcile any failed retry the same way.

## Completion

Return the created or existing issue's title and URL. For a draft-only request, return the title and body as unpublished. Report verification limitations explicitly; an attempted command alone is not proof of publication.
