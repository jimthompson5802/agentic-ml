# US-15 and US-26 combined publication

Publication owner: `US-15-preprocessing`, 2026-11-15. The developer accepted the
[single-PR recommendation](../reviews/us15-us26-pr-structure.md) and explicitly
authorized acceptance-record integration, reconciliation/verification, ordinary
push, one PR to `main` and a published static COMMENT review. Coordination thread
`01a1db6c-a225-73e0-8796-81a03c4cec7a` relayed this decision. No PR/main merge,
force push, history rewrite, issue closure or cleanup is authorized.

## Accepted scope and integrated history

- US-15 #21: M1 AC-01/02/03 accepted; AC-04 remains M2 and issue #21 stays open.
- US-26 #17: recording AC-01–05 accepted; #33/#43 remain separately owned.
- Actual installed native pipeline/metadata/provenance preservation is verified
  across both direct and genuinely sdist-rebuilt normal wheel projects.

Approved implementation `3ffc7b4df557f9fa8fe873fc68e012b48e9b26e1` preserves both
story implementation histories. US-15 acceptance tip
`aec10af311f3d831c829e5fe0ecfffc7ee0dee13` and US-26 acceptance tip
`ecbceb2aa213da8f3e3f1d902eb9f730eca6bbb7` each add documentation only.
An ordinary merge joins those tips in the existing publication branch, preserving
both decisions. Shared checkpoint/index conflicts are reconciled explicitly;
the historical checkpoint tail was identical in both tips and remains preserved.
No sibling working files, executable changes or new PR branch are introduced.

The first merge invocation could not read tree
`813167f3785a899ad13810ff4b2053e5b08b8a30`; read-only inspection found it readable
and the working tree clean. An identical retry reached the expected document
conflicts. No object/ref/configuration repair was performed. Raw conflict and
attempt records remain under the publication directory below.

## Verification retained

[US-15 final evidence](us-15-ip4.md): 924 passed, one existing authorized
planning-schema skip, zero failures/errors; 925 selected/268 deselected of 1193,
four workers/loadgroup, 427.02 seconds. [US-26 final evidence](us-26-recording-ip4.md):
361 focused passes and 924 M1–6 passes/one existing skip. Both owners completed
shared lock/lint/format/type/CLI checks and installed handoff verification.
All 83 tested executable input fingerprints and the lock hash remain unchanged
through documentation reconciliation; no test renewal is required. New document
links/anchors and whitespace are checked separately before committing.

Lock SHA-256 remains
`6b2a32ce733dcb9b5bacc0fb1169d4e49494a9073871a6173e022e5fa9c33dc4`.
Linux aarch64/Python 3.12.16 only. M2 restoration, historical/MVP milestone
verification obligations, existing skipped coverage and the native float16
limitation remain with their original owners. No broader suite or standalone
artifact driver was launched.

## Publication and review status

Target repository: `jimthompson5802/agentic-ml`; base `main`; head
`US-15-preprocessing`; standard PR. Read-only GitHub checks found no existing
matching PR and confirmed remote main
`1a9864a645084af8cfcec580b1db5fa045a67859`. GitHub authentication verified
outside the network-restricted sandbox; the initial sandbox DNS failure was
not an invalid-credential result.

Ordinary push, PR URL, final published head, CI and static-review outcome are
recorded as they become available. Static review uses the repository
[review skill](../../.agents/skills/review-pull-request/SKILL.md); it inspects
source/diff/requirements and existing CI without executing project checks.
The PR must remain open and unmerged. Issue references use no automatic closing
keywords. Raw publication commands, full diff and verified review/API results
belong in `.dev-records/verification/20261114-us15-ip4/publication/` and survive
temporary workspace cleanup.
