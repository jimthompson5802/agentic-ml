# US-41 IP1 — Wheel identity feasibility and proposed contracts

Date: 2026-11-08 UTC. Issue [#64](https://github.com/jimthompson5802/agentic-ml/issues/64),
M50, US-41-AC-01–06. [Owning plan](../plans/milestone-50-us-41.md).
Developer “implement ip1” authorized this contract phase. T1–T3 are technically
complete. Developer “i approve ip1; commit changes” approved Gate 1, the exact
contracts, archive-history limitation and refined boundaries on 2026-11-08. No product
behavior changed and no acceptance criterion is fully verified by these probes.

## Sources and environment

Complete issue body/metadata and paginated comments were retrieved with
`sh .codex/scripts/github-read.sh issues/64`,
`sh .codex/scripts/github-read.sh issues/64/comments --paginate --slurp`, then
metadata refreshed. Zero comments; stable `updated_at=2026-11-08T18:02:47Z`;
open enhancement in Milestone 50. Criteria agree with the local story. Read the
active reading map, interface, architecture, blueprint, layout, delivery and
traceability documents and current preflight/environment/storage/journal flow.
No scope conflict found; no additional story implementation authorized.

Observed Linux aarch64, Python 3.12.16, uv 0.13.6. Raw records:
`.dev-records/verification/us-41-ip1-20261108/` (commands.json, summary.json,
logs/0.log–11.log, identities/, and three retained probe scripts).
Disposable independent projects: `/tmp/us41-ip1-q56583_b/`.
The probes create minimal real purelib wheel ZIPs named agentic-ml, with versions
1.0.0 and 1.0.1, no dependencies and no toolkit implementation. They establish
native installer metadata feasibility, not toolkit initialization or distribution
verification. No standalone artifact driver, pytest, product build or init ran.
The original project `.venv`, source code and committed lock were not modified.

## Native results (T1)

All 12 recorded subprocess commands exited zero. Python probe invocations were
`python3 /tmp/us41_probe.py`, `python3 /tmp/us41_url_probe.py`, and
`python3 /tmp/us41_local_upgrade.py`; retained scripts contain exact fixture
construction and subprocess argv/cwd. They set a disposable UV_CACHE_DIR and
UV_PYTHON_DOWNLOADS=never. The first URL probe could not open a local socket under
the sandbox (PermissionError); its rerun received escalation approval and served
only synthetic wheels on 127.0.0.1. No corrective product attempt occurred.
The server was stopped after probing; recorded URLs are ephemeral fixture origins.

| Commands / logs | Observation |
|---|---|
| 0–1: `uv add --offline --python /usr/local/bin/python3 ../artifacts/agentic_ml-1.0.0-py3-none-any.whl`, isolated metadata probe | Native path source and wheel SHA-256 in lock; installed file URL, empty archive_info |
| 2–3: `uv add --no-cache 'agentic-ml @ http://127.0.0.1:PORT/agentic_ml-1.0.0-py3-none-any.whl#sha256=DIGEST'`, metadata probe | uv rewrites to a source URL without fragment; lock hashes actual wheel, installed archive_info still empty |
| 4: `uv sync --locked --offline` | Success; selected 1.0.0 URL installation retained |
| 5–6: native URL add 1.0.1 and metadata probe | Explicit version upgrade succeeds |
| 7–8: native URL add reviewed/1.0.1 and metadata probe | Different bytes and locator with same version cause reinstall |
| 9: native URL add with 64 zeroes as SHA-256 fragment | Unexpectedly succeeds; fragment disappears, actual artifact digest is locked. This form cannot be claimed to enforce a supplied expected hash |
| 10–11: native offline path adds for 1.0.1 then reviewed/1.0.1 | Both explicit local transitions succeed; distinct lock source/digest recorded |

Initial local/URL artifact SHA-256 independently computed with hashlib:
`ec99dc34eaa163830ab4f671e501dea10e1d8583389af0f52bea87c20809e82d`.
The snapshots in identities/ retain exact declaration and lock content for each
transition. Native local source is `{ path = "../artifacts/...whl" }`; its lock
wheel entry contains `filename` and `hash = "sha256:..."`.
Installed direct_url.json is `{"url":"file:///tmp/.../artifact.whl","archive_info":{}}`.
No hash is available in that installed origin record. uv_cache.json contains
installer cache timestamps, not suitable public artifact-integrity evidence.

The same-version local installed payload was compared directly to archive member
bytes, excluding rewritten RECORD: all four fixture members matched (independent
`identities/payload-comparison.json`). This is a small feasibility check, not proof
of the complete mapping for genuine toolkit wheels, entrypoints or resources.

## Contracts and refined verification (T2/T3)

The [exact proposal](../specs/design/interfaces-and-configuration.md#us-41-wheel-contract-proposed-at-gate-1)
and [ADR extension](../specs/design/architecture-decisions.md#us-41--adr-007-extension-at-gate-1)
settle reviewable syntax, root resolution, name/version matching, pre-write order,
failure/recovery matrix, additive 0.1 journal identity and completion guards.
The plan refines IP2–IP4 cases and records developer approval of the presented boundaries.

Preferred form is a retained local purelib wheel, because its native lock has
integrity and requires no hosting. URL support is excluded from the proposal.
The proposed replacement for absent installed archive hashes is an independently
hash-verified retained wheel plus installed origin/version and payload comparison.
It cannot prove the digest of the historically installed ZIP when two ZIPs have
identical payloads but different archive encoding. Missing retained bytes fail;
no fabricated archive hash, companion integrity file or version-only equivalence.
**Gate 1 approved this consistency boundary and its limitation on 2026-11-08.**
No product implementation or whole-story acceptance is implied.

New-version and same-version/different-locator upgrades use native uv add, locked
sync and init. Only a fully complete prior wheel journal may refresh after current
identity and compatibility validation; interrupted operations retain checksums
and selected identity. Existing Git behavior and legacy journal safety remain
required. API and CLI signatures stay unchanged. Genuine direct/rebuilt-wheel
initialization and the full Git regression matrix belong to IP2–IP4.

## Verification and limitations

Documentation-only phase: TDD, milestone pytest, shared executable checks and
standalone artifact verification do not apply. Native commands above are
feasibility evidence only. Relative Markdown file/anchor checks and
`git diff --check` passed. Committed uv.lock SHA-256 before/after:
`5f99c2da64eb46bc758f798f364e67eab25246253fc75315ebb404461e466a9d`.
No suppressions, exclusions of existing tests or acceptance criteria changes.
macOS/Windows, other uv releases, missing/corrupt metadata rejection, actual
initializer mutations, storage preservation and recovery are unverified here.
Keep raw records for the repository lifetime under the records policy.
