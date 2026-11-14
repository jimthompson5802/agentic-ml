# US-15 / US-26 native parameter encoding revision

Decision ID: US-15-US-26-SC-01, 2026-11-14 UTC. Developer accepted the
recommendation to revise the shared encoding, verify the complete metadata,
settle bounded skops serialization, reconcile records and retain both Gate 1
reviews. This approves the revision work; it does not approve either phase gate.

The [revised producer contract](../preprocessing.md#metadata-10) defines the
exact tagged parameter records. The public signatures, eight top-level metadata
keys, existing partition format, separate provenance ownership, artifact layout
and AC assignments are unchanged. Ordinary JSON numbers remain finite. Tags
describe native parameter settings; they do not authorize arbitrary imports or
introduce a reconstruction API.

The [renewed feasibility report](../verification/us15-us26-contract-revision.md)
verifies complete effective settings, strict JSON, literal tags and native
MLflow save/log/download/load on the composed M1 pipeline. The selected native
configuration is serialization_format="skops", skops_trusted_types=["numpy.dtype"].
No broad trust list or pickle fallback is allowed. Existing native failure
evidence remains in the consumer's report; product integration remains IP4.

## Reconciliation completed

US-26 applied and independently verified SC-01 in its owning session;
[explicit concurrence](../../../US-26-mlflow/docs/verification/us26-sc01-concurrence.md)
is acknowledged by [US-15](../verification/us15-sc01-concurrence.md).
No interface differences remain. US-15 T3 is Complete; both Gate 1 decisions
remain Pending. The patch below is retained as historical handoff evidence,
not an instruction to reapply it to the now-updated consumer documents.

## Historical consumer owning-session handoff

The [reviewable patch](us15-us26-contract-revision.patch) updates the shared index,
tracking contract and consumer plan. It is prepared against the current dirty
US-26 documents, not its committed HEAD; it preserves those edits. Baseline
SHA-256 identities are retained in
`.dev-records/verification/20261114-us15-contract-revision/consumer-inputs.json`.
Read-only `git apply --check` passed against that worktree. No sibling files were
modified and no consumer approval or verification is inferred.

The manage-story-worktree skill requires: “One agent session owns a story
worktree at a time.” The execution skill also prohibits copying another
session's live edits or assuming shared Git objects provide integration.
Apply/reconcile this patch in US-26's owning session, renew its metadata/schema
evidence and checkpoint, and mark reopened T2/T3 Complete only when verified.
If the baseline changed, inspect the diff and reconcile instead of forcing it.

| Remaining action | Owner | Gate |
|---|---|---|
| Adopt exact tags and bounded serialization choice; verify consumer acceptance rules — Complete | US-26 owning session, IP1-T2/T3 | Gate 1 pending |
| Confirm consumer contract/index match revised producer; finish T3 — Complete | US-15 owning session | Gate 1 pending |
| Review both technical results/public test boundaries | Developer | Explicit approvals for both Gate 1 decisions |
| Begin dependent product behavior | Respective owning sessions | Both Gate 1 approvals and Phase 2 authorization |

No issue acceptance criteria or externally published issue scope changed.
No GitHub comment, issue edit, push, merge or cross-branch integration occurred.
