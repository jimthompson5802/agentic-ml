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

The four standalone verification drivers implement this layout. Their `RECORDS`
lines identify each invocation; composed initialization/planning commands report
parent and child records. Parent summaries link child records, and child summaries
identify the parent. Logs and manifests survive default successful removal of
owned environments/private caches. Child retention allows all parent probes to
finish; the parent's summary owns the final cleanup result. Source fixtures and
project files are preserved separately from environments.

`summary.json` separates `verification_exit_code` from `cleanup` (`not attempted`,
`pending`, `complete`, `retained` or `failed`). A null exit code denotes incomplete
verification. `commands.json` lists attempted stages and log paths, including
failed/spawn-failed commands. `identities/` contains selected manifests and their
checksums; unavailable identities must not be interpreted as passing probes.
Record-write failure prevents cleanup. Verification failure and `--keep-workspace`
retain environments; cleanup failure reports a nonzero command result while
preserving the verification outcome. See [driver usage](distribution.md).

No historical records are moved or deleted. Forced termination may prevent final
status writes or child output capture; incomplete records and workspaces need
inspection. Earlier drivers stored evidence only in temporary workspaces; copy
historical evidence needed for lifetime retention into this layout manually,
preserving its original location and source identity. Pytest-owned workspaces
under US-36 must keep durable records outside pytest retention paths.
