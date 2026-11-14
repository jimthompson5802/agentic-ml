# US-13 IP1: native DVC contract review

Date: 2026-11-13 UTC. Tasks US-13-IP1-T1/T2/T3 complete; **Gate 1 approved**.
This phase defines M1 AC-01/02 boundaries; it does not accept implementation.
Developer “I approve ip1” authorized IP1; “resume” continued that authorization.

## Scope and source refresh

The retrieve-github-issue and execute-plan workflows were followed. The required
GitHub authentication blocker is resolved. Repository helper commands returned
issue #16's complete body and every comment page:

```sh
sh .codex/scripts/github-read.sh issues/16
sh .codex/scripts/github-read.sh issues/16/comments --paginate --slurp
sh .codex/scripts/github-read.sh issues/16 --jq '{number,title,state,comments,updated_at,milestone,pull_request}'
```

One unique comment (6699586819), matching reported count 1. Final refresh retained
`updated_at=2026-11-07T00:28:44Z`, count 1, open state, null milestone and no
pull-request field. The issue body assigns AC-01/02 to M1 and AC-03/04 to M2;
its scope comment is unchanged from the plan snapshot. No issue edits occurred.
Local stories and design 0.15 agree. Reviewed the design reading map, data and
features, interfaces/configuration, execution/governance, repository layout,
ADR-008, milestone capability order, acceptance traceability and related existing
public contracts. Accepted extraction and partition schemas remain unchanged.

## Observed native capability

Source revision `844106a500796e5102317eecf1ea1e48448ff880` on
`US-13-dataset-versioning`. Existing environment: DVC 3.67.1; Python 3.12.16;
Linux 7.0.14-linuxkit aarch64, glibc 2.36. No dependency installation or update.
Lock SHA-256 before/after:
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
No macOS/Windows inference or normal-wheel acceptance is claimed.

Durable raw evidence:
`.dev-records/verification/20261113-us13-ip1-deabb6c7/`.
Disposable workspace retained at `/tmp/us13-ip1-1it6rxku/` (two project roots and
local storage). Logs, command/cwd/exit-code records and native metadata snapshots
remain in the durable directory. These are small native feasibility observations,
not project integration tests or standalone artifact-driver runs.

All DVC calls used the absolute existing executable
`/workspaces/agentic-ml/.venv/bin/dvc` with an explicit disposable project cwd.
`version`, `add --help`, `push --help`, `status --help` completed successfully.
`commands.json`, `clean-commands.json` and `duplicate-command.json` identify
successful and unsuccessful calls; `logs/` preserves stdout/stderr.

| Observation | Result and exact native command arguments |
|---|---|
| Fresh Git/DVC project | `git init`, `dvc init`: 0 in clean project |
| File and directory registration | `dvc add data/source data/file.csv`: 0; native `.dvc` files, directory membership metadata, content cache and ignore entries created |
| External local storage | `dvc remote add --default local /tmp/us13-ip1-1it6rxku/remote`, `dvc push`: 0 |
| In-project storage | `dvc remote add --default inside store`, `dvc push`, `dvc status --cloud`: 0; explicit `/store/` Git exclusion verified with `git check-ignore store/files` |
| Unchanged registration | `dvc add data/source`: 0; pointer bytes unchanged |
| Changed CSV bytes | Change label A to B, `dvc add data/source`, `dvc push`: 0; pointer differs |
| Missing target | `dvc add data/missing`: 1, native missing-target diagnostics |
| Already Git-tracked data | `git add tracked.csv`: 0, then `dvc add tracked.csv`: 1; Git ownership conflict; no automatic untracking |
| Existing directory member | `dvc add data/source/a.csv`: 0; updates existing directory pointer, does not establish conflicting ownership |
| Duplicate output declarations | Copy the native pointer to `data/other.dvc`, then `dvc add data/source`: 1 naming both owners; original source bytes preserved |
| Failed transfer | Configure separate `bad` remote beneath a regular file; `dvc push -r bad`: 255, native filesystem diagnostic; subsequent `dvc status`: 0 with local registration intact; default remote preserved |
| Git exclusions | `git check-ignore data/source/a.csv data/file.csv .dvc/cache`: 0; `git ls-files` contains the intentionally tracked conflict fixture and excludes DVC content |

Official references checked on the same date:
[native add](https://doc.dvc.org/command-reference/add),
[native push](https://doc.dvc.org/command-reference/push),
[native pointer format](https://doc.dvc.org/user-guide/project-structure/dvc-files).
The CLI observations above settle this installed version's concrete behavior.

### Failed feasibility/setup commands

Preserve these failures; none is a product defect or a passing test:

1. Initial sandbox `dvc init` and `add` exited 255 because `/var/tmp/dvc` was
   read-only. The probe then tried to read an absent pointer and raised
   `FileNotFoundError`; its raw logs remain `07.log` and `09.log`.
2. The first escalated retry used a relative executable from the disposable cwd
   and exited 127. Correcting to the absolute executable resolved invocation.
3. Initial `init` had partially created `.dvc`; its resumed invocation exited 1
   because that directory existed. No force/delete was applied. Registration
   and transfer in that fixture succeeded; an independent clean project then
   demonstrated fresh `init` success.
4. The exploratory `dvc add --file other.dvc data/source` exited 254 because
   this installed CLI has no `--file` option. A fixture with two native pointer
   files supplied the actual duplicate-output case; it failed with the expected
   ownership diagnostic. The unsupported command is excluded from the recipe.

No product corrective change was attempted, no test assertion was weakened,
and no suppression/workaround was introduced. The sandbox failure was resolved
through approved escalation. Raw evidence is retained for all native failures.

## Contract decisions proposed for Gate 1

The [candidate guide](../dataset-versioning.md) supplies concrete project code,
configuration and shell commands. The [plan matrix](../plans/milestone-1-us-13.md#public-boundaries-and-independently-defined-scenarios)
remains the public test boundary. Confirm these decisions before executable tests:

- Native DVC suffices: no new package helper, reference schema, resource or
  dependency change. Existing setup configures the project cache and default
  `agentic-ml-store`; a prepared project reuses them without remote rewrites.
- Git owns `versioning.json`, `version_data.py`, dependency declarations/lock,
  native pointers and nonsecret configuration/ignores. `versioning.json` is the
  readable input manifest. It includes configured memberships, whereas each
  DVC-owned `split.json` is the single authoritative result for its layout/version.
  Existing extraction manifests remain within their DVC-owned bundles.
- Stable source snapshots live inside `data/source/`. Extraction reads exactly
  those files; external originals remain untouched. A/B extraction destinations
  are fresh, preserving accepted fresh-bundle publication. No accepted report
  is rewritten with a DVC identity.
- `data/partitions/{A,B}/{layout}/split.json` records exact helper results beside
  the native Parquet partitions. Both supported layouts are explicit. Derived
  CSV is a deterministic row selection, with no fitted-feature behavior.
- `dvc add` establishes local identity/cache; `push` is a separate transfer.
  Commands preserve nonzero status/output and existing configuration. No automatic
  Git removal, conflict repair, cross-command transaction or partial-output cleanup.
- The recipe remains the single execution source: IP2 extracts its named fenced
  config/script/command fragments into isolated projects, substitutes paths and
  runs them. Independent oracles belong in tests, not in a parallel recipe.
  IP3 copies the same recipe fragments into each installed environment.

### Planned boundary evidence and limitations

| Public boundary | Independently expected result | Owning task |
|---|---|---|
| Installed extraction plus native file/directory DVC | Literal CSV/Parquet rows IDs 0–4, labels A–E; report source SHA-256 matches snapshot bytes; native file hashes/member references match stored bytes | IP2-T1; both wheels IP3-T1 |
| Project persistence plus `create_partitions` | Two-way train `[0,2,4]`, test `[1,3]`; three-way train `[0,2,4]`, validation `[1]`, test `[3]`; exact saved records/rows and strict JSON round-trip | IP2-T2; IP3-T1 |
| Project deterministic pandas output | IDs `[0,2,4]`, labels `[A,C,E]` in A; label Z replaces A for ID 0 in B | IP2-T2; IP3-T1 |
| Git/native storage ownership | Real commits A/B, exact tracked inventories and exclusions, configured remote/cache member bytes for both versions; config and native references readable from each commit | IP2-T3; IP3-T1 |
| Repeat/change | Unchanged re-add retains pointers; independently change source bytes, saved membership/partition bytes and derived bytes and observe corresponding native identity change | IP2-T2/T3; IP3-T1 |
| Native failures | Missing target; Git-tracked content; duplicate output declarations; bad remote; local registration survives failed push and default remote is unchanged | IP2-T3; representative cases per wheel IP3-T1 |

Directory evidence reads native manifests and independently hashes file bytes;
there is no second directory hashing algorithm. Native versioning already exists,
so positive/boundary evidence is appropriate; manufacture no failing TDD test.
Any genuinely new/corrected supported executable behavior requires a small
red–green cycle after boundary confirmation. No concurrent-mutation isolation,
restoration/pull, native stages, MLflow, notebook, training or assistant acceptance
is included. US-39 receives the recipe and paths; AC-03/04 remain M2.

### Installed verification seam

Inspected `check_assessment_splits.py`, `verify_assessment_splits.py` and the M1
distribution test. The existing driver already creates direct/rebuilt wheel
environments and copies project-owned code; each probe runs with `-I` from an
unrelated cwd and independently checks package origin. Extend that driver to
copy the guide-derived project code/configuration and invoke the new dataset
checks in its existing probe. Keep existing assessment/split checks, identities,
scheduling group, cleanup and durable records intact. Extend the existing
`test_assessment_splits_from_both_artifact_paths` to require US-13 evidence for
both labels. No new build/install driver or normal-install claim in IP1.

## Gate checks and status

Documentation-only phase: no executable product/test/resource changes, so TDD,
pytest milestone selection and shared Python checks do not apply. No pytest,
artifact build/driver or dependency synchronization ran. Relative file-link
checks passed for all 62 relative file links in the guide/report/plan/checkpoint;
`git diff --check` passed.
Lock hash is unchanged. IP2 owns focused/M1/shared checks; IP3 owns installed
wheel evidence and final M1–6/shared checks. Historical milestone obligations
remain open. Native feasibility does not accept AC-01/02.

**Gate 1: Approved, 2026-11-13.** Developer “i approve gate 1; commit changes”
confirmed the candidate guide contract, ownership, public boundaries and
native-only decision, and authorized committing this review package. Requested
changes: None. IP2 remains Not started; execution is outside this commit request.
