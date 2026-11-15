# Implementation phase approvals

## Classify by public contract impact

Each implementation phase records one approval mode:

- **Contract review:** The phase defines or refines a public interface contract.
  Complete the proposal and its applicable verification, then obtain explicit
  developer approval before implementing or testing dependent behavior.
- **Automatic:** The phase implements, tests, documents or verifies an already
  approved contract without changing it. Record completion and continue within
  authorized scope when the verification conditions below pass.

Public contracts include Python signatures and observable behavior, CLI commands
and options, configuration and data schemas, persisted artifact formats,
producer/consumer boundaries, validation/error behavior and compatibility promises.
A phase that changes the agreed contract for any of these requires contract review
even if it also writes code or keeps the same signatures. Correcting an implementation
to match an approved contract remains automatic. Tests that
only verify an approved contract belong to automatic phases; tests that introduce
new contract expectations need prior contract approval. Reuse existing approved
contracts and public test boundaries when they apply.

Contract phases may use bounded feasibility probes to make the proposal concrete.
Approval covers the reviewed contract and public test boundaries, not an assertion
that dependent production behavior is already implemented. Record the contract
reference/version, changed decisions and developer decision source. If an
approved plan already settles the exact contract and test boundaries, reuse that
approval rather than requesting the same decision again.

## Start and continue execution

Plan review and execution authorization remain distinct. An instruction to execute
an approved plan authorizes its ordered phases within the stated story or
coordinated scope, subject to contract reviews and any explicit developer limits.
It does not authorize another story merely because that story is a dependency.
For the first phase, verify its entry conditions and existing prerequisite evidence.

At every phase boundary, retain the tasks, verification and checkpoint evidence.
An automatic phase may start when:

1. The preceding phase and applicable prerequisite tasks are complete.
2. Every required preceding-phase check has a passing final result against the
   current relevant inputs, including focused tests, regressions and shared checks.
   Required checks that failed, errored, were interrupted, skipped or never run
   block progression. Retain earlier failed attempts; an expected TDD red result
   is valid history only after the corresponding green verification passes.
   Document-only checks may replace executable checks only where the verification
   policy makes them inapplicable and the rationale is recorded.
3. Every public contract needed by the next phase has a recorded approval, and
   its scope and behavior remain within that approval.
4. No unresolved blocker, scope decision or explicit developer hold prevents it.

Record the result as `Automatic — verification passed`, with evidence and the next
phase, and continue without a developer question. Never record automatic
progression as developer approval. If a condition is unmet, stay in the current
phase and diagnose/fix within scope and the three-attempt limit; escalate when
that limit is exhausted or a developer decision is needed. A test failure alone
does not introduce a new approval gate. Renew evidence invalidated by later edits.

If coding discovers a needed public contract change, pause affected work before
changing its implementation or dependent test expectations. Refine the contract,
run applicable proposal checks and request approval; independent authorized work
may continue. Uncertain contract impact requires clarification before affected
work proceeds. Material scope/dependency/security changes retain their existing
authorization requirements.

## Completion and other decisions

At a contract phase boundary, request review of the concrete contract and evidence.
At an automatic phase boundary, report completion without blocking progression.
When the last phase passes, request whole-story acceptance without adding a
separate final coding-phase approval. A contract decision may also serve as story
acceptance only when explicitly stated and all story verification is complete.

Whole-story acceptance, publication, merge and cleanup retain their existing
boundaries. Broader local tests and standalone artifact checks still require an
explicit developer command. Phase verification requirements and runtime command
permissions are unchanged; removing a manual gate does not remove any check.

## Existing plans and resumption

The developer approved this policy on 2026-11-15. It replaces the default mandatory
manual gate at every implementation phase. On resumption, classify unfinished
phases and update their pending progression fields and coordinated execution
index under the scope-change procedure, citing this policy approval. Preserve
completed approvals, original failures and verification evidence as historical
records. Existing verification obligations remain unless separately revised.
Honor explicit developer holds or task-specific decisions; resolve ambiguous
contract impact before dependent work. A checkpoint or automatic progression
record cannot manufacture developer approval of an unresolved contract.
