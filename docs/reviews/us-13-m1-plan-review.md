# US-13 M1 plan review — 2026-11-13

Reviewed the unapproved [plan](../plans/milestone-1-us-13.md) against issue #16's
complete discussion retrieved in this conversation, the current M1/M2 stories,
ADR-008, capability order, existing extraction/partition interfaces and installed
verification structure. Static inspection only; no executable checks were run.
The plan has not entered execution. No approvals or scope decisions are inferred.

## Assessment

The M1 criterion selection is correct. Native DVC, local storage, installed public
interfaces and deferred M2 restoration fit the approved MVP. Preserve the developer
gates, public-boundary confirmation and required verification. Revise the draft
before implementation to make its user deliverable concrete and avoid building
unnecessary metadata/verification infrastructure.

## Findings

### 1. High: Define a deliverable users can actually run

IP2-T1/T2 place project workflow code under `tests/installation/`. IP3-T2 promises
a guide but does not explicitly require a complete runnable example or specify
how a separate experiment project obtains the required project code. With no new
toolkit API by default, all implementation tasks could pass while users still
need to copy test internals or invent glue code.

Require one complete documented example using installed toolkit functions and
native DVC commands, including source preparation, extraction, saved partitions,
version registration and metadata commit. A self-contained guide is sufficient;
do not require a new generator or package API. Test the same example outside the
checkout, and state its handoff to US-39. No training or assistant work belongs here.

### 2. Medium: Reduce duplicate metadata and undefined publication machinery

The proposed layout stores the same split record in both DVC content and Git,
and adds a custom `data-references.json`. IP2 then requires synchronization and
completed-reference failure semantics. These choices may be useful, but neither
their necessity nor their minimal consumer is established. They add multiple
sources of truth before an integrated experiment needs them.

At Gate 1 choose an authoritative split record and explain which relevant
manifests Git retains, satisfying both AC-01/02. Add a second copy or reference
document only for a specific uncovered requirement. Prefer native `.dvc`
identities and existing extraction/split records. If a reference document remains,
bound it to artifact paths/identities; avoid a new publication-state protocol.
Distinguish successful local versioning from a subsequent failed remote transfer.

### 3. Medium: Verify version history, not just the current identity

IP2-T2 checks changed and unchanged hashes; IP2-T3 checks a fixture Git commit.
Neither explicitly requires two committed data revisions with available content
for both. An implementation that overwrites the only reference could satisfy
these checks while failing the practical purpose of dataset versioning.

Require fixture commits A and B, inspect their metadata/manifests through Git,
and confirm each references the independently expected data. Verify both content
versions remain in the chosen cache/storage after the update and transfer. This
is M1 version-retention evidence; fresh-checkout restoration, hash validation
after pull and corrupt-restoration failures stay in M2.

### 4. Medium: Separate integration evidence from new product guarantees

IP1 leaves a reusable package seam undecided, while IP2 prescribes new project
workflow code, TDD and numerous failure contracts. Native commands may already
meet all required behavior. The plan's existing warning against manufactured red
tests is sound, but the executable deliverable and its failure ownership remain
ambiguous.

Make Gate 1 choose explicitly between a native documented recipe with integration
tests and a narrowly justified reusable helper. Apply red–green TDD to new toolkit
or supported project behavior, and integration checks to existing native behavior.
Do not expand this story into a generic path-validation or transaction layer.
Keep preservation of accepted initializer APIs and meaningful failure diagnostics.

### 5. Low: Avoid another independent artifact-verification stack

IP3-T1 proposes a new checker and orchestration driver. Existing
`tests/integration/test_distribution_verification.py` already has direct/rebuilt
wheel cases and installed extraction/assessment drivers. A further driver could
duplicate build/install lifecycle and increase every M1 gate's cost.

Prefer extending an existing installed project probe or sharing its prepared
environments. Keep both independently verified wheel paths and required retention,
isolation and milestone checks. Do not weaken verification to save runtime; reduce
duplicated setup and orchestration instead. Three implementation phases are
reasonable if IP1 stays a bounded contract review rather than open-ended design.

## Review disposition

Recommend revising the draft for findings 1–4 before implementation. Finding 5
is an implementation-design improvement. No product scope expansion is needed;
AC-03/04 remain deferred to M2 and issue #16 remains open after M1 acceptance.
The review does not approve the plan or any implementation gate.

## Draft revision follow-up — 2026-11-13

Developer “ok make the update” authorized the four recommendations discussed
after this review. [US-13-PLAN-REV-01](../plans/milestone-1-us-13.md#us-13-plan-rev-01--mvp-focused-draft-revision-2026-11-13)
records their application. The revised draft requires a complete runnable recipe,
one authoritative DVC-owned split record, Git-owned native metadata and relevant
project configuration/manifests, committed versions A/B with retained content,
and native commands by default. It also addresses finding 5 by extending existing
installed probes/environments rather than requiring a new independent driver.
Findings are addressed in the plan; implementation and verification remain
Not started. Developer subsequently approved the revised plan with “i approve
plan; commit changes” on 2026-11-13. All implementation gates remain Pending;
implementation is not authorized by that plan approval.
