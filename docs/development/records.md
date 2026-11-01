# Retained development evidence

## Retained development records

Use the harness repository's `.dev-records/` directory for raw development evidence that must survive disposable environment and workspace cleanup. Git ignores this directory. Keep concise, reviewed verification reports in the tracked `docs/verification/` directory and reference the corresponding record locations from those reports.

Verification records use the following layout. Each invocation has a unique directory; concurrent runs must not overwrite one another's records.

```text
.dev-records/
  verification/
    <timestamp>-<commit>-<unique-run-id>/
      summary.json
      commands.json
      identities/
      logs/
```

The records identify the story and acceptance criteria when applicable, source commit and relevant working-tree changes, operating system and tool versions, commands and working directories, stdout/stderr, artifact checksums, installed package and environment identities, and outcomes including failed or incomplete checks. Record unavailable information explicitly. Exclude credentials and sensitive dataset contents from retained records.

Retain these records for the lifetime of agentic-ml development. Automated environment, cache, pytest, and workspace cleanup must preserve `.dev-records/`. Large virtual environments, installer caches, and datasets belong in disposable workspaces rather than this directory. Verification commands must report the absolute record location so that contributors can find the evidence after cleanup.

Contributors are responsible for backing up `.dev-records/` and preserving or transferring it before deleting or replacing a checkout. Ignoring the directory does not protect it from `git clean -fdx`, which can delete ignored files; preserve these records before any such operation. Records from separate checkouts must be included in the backup. Existing historical evidence must not be deleted or migrated automatically.

US-35 defines the verification drivers' adoption of this layout and retention contract; the current drivers still retain logs and environments in their printed temporary workspaces. This documentation does not implement automatic record collection or cleanup. Until the drivers adopt the policy, copy evidence needed for lifetime retention into `.dev-records/verification/` before removing its temporary workspace, and record the original location and source identity. Pytest-owned temporary workspaces under US-36 must keep durable records outside pytest retention paths.

