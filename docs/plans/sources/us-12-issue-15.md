# US-12 issue #15: complete source snapshot

Retrieved 2026-11-07 UTC. All comment pages fetched; 1 unique comment(s), matching metadata; final metadata unchanged. No pull_request field. GitHub milestone unset; body assigns M1 scope. Linked pages, timeline and deleted comments are outside this snapshot.

## Issue metadata and complete body

```json
{
  "url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15",
  "repository_url": "https://api.github.com/repos/jimthompson5802/agentic-ml",
  "labels_url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15/labels{/name}",
  "comments_url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15/comments",
  "events_url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15/events",
  "html_url": "https://github.com/jimthompson5802/agentic-ml/issues/15",
  "id": 6111871903,
  "node_id": "I_kwDOVZ7kv88AAAABbEvDnw",
  "number": 15,
  "title": "US-12: Validate extracted data",
  "user": {
    "login": "jimthompson5802",
    "id": 1425269,
    "node_id": "MDQ6VXNlcjE0MjUyNjk=",
    "avatar_url": "https://avatars.githubusercontent.com/u/1425269?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/jimthompson5802",
    "html_url": "https://github.com/jimthompson5802",
    "followers_url": "https://api.github.com/users/jimthompson5802/followers",
    "following_url": "https://api.github.com/users/jimthompson5802/following{/other_user}",
    "gists_url": "https://api.github.com/users/jimthompson5802/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/jimthompson5802/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/jimthompson5802/subscriptions",
    "organizations_url": "https://api.github.com/users/jimthompson5802/orgs",
    "repos_url": "https://api.github.com/users/jimthompson5802/repos",
    "events_url": "https://api.github.com/users/jimthompson5802/events{/privacy}",
    "received_events_url": "https://api.github.com/users/jimthompson5802/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "labels": [
    {
      "id": 12862971353,
      "node_id": "LA_kwDOVZ7kv88AAAAC_rFd2Q",
      "url": "https://api.github.com/repos/jimthompson5802/agentic-ml/labels/enhancement",
      "name": "enhancement",
      "color": "a2eeef",
      "default": true,
      "description": "New feature or request",
      "archived_at": null,
      "archived_by": null
    }
  ],
  "state": "open",
  "locked": false,
  "assignees": [],
  "milestone": null,
  "comments": 1,
  "created_at": "2026-10-30T02:06:28Z",
  "updated_at": "2026-11-07T00:28:41Z",
  "closed_at": null,
  "assignee": null,
  "author_association": "OWNER",
  "active_lock_reason": null,
  "sub_issues_summary": {
    "total": 0,
    "completed": 0,
    "percent_completed": 0
  },
  "issue_dependencies_summary": {
    "blocked_by": 0,
    "total_blocked_by": 0,
    "blocking": 0,
    "total_blocking": 0
  },
  "body": "## User Story\n\nAs a data scientist, I want to check data quality and record distinct partitions so that training and evaluation use suitable inputs.\n\n## Description\n\nDelivery: M1. No implementation acceptance is claimed.\n\nOriginal criterion IDs and issue discussion are preserved. The approved disposition changes this issue's remaining scope; this is not completed implementation.\n\nCriterion assignment: US-12-AC-01: M1; US-12-AC-05: M1.\n\nScope source: MVP-SC-01/MVP-SC-02, Gate 1 approved on 2026-11-06 by\n“i approve gate 1 and authorize phase 2”. This scope revision does not claim\nnew implementation acceptance. Preserve the scope-decision comment and original\nissue history.\n\n## Acceptance Criteria\n\n- [ ] **US-12-AC-01:** Validation checks schema, row counts, types, nulls, duplicates, and configured quality rules, reporting mismatches and failures.\n- [ ] **US-12-AC-05:** Report validation results and block supported pipeline steps when configured required checks fail.\n\n## Scope / Non-Goals\n\n**In Scope:**\n\n- The milestone slices above, through installed public interfaces in a separate experiment project.\n- Trusted local code; project-owned configuration, models and preprocessing; MLflow records and native DVC stages.\n- Component criteria own technical behavior; integration criteria own cross-component and assistant usability evidence.\n\n**Out of Scope:**\n\n- Managed agents and autonomous loops; mandatory experiment workflow approvals.\n- OS-enforced filesystem/network/credential/holdout isolation and arbitrary-Python bypass prevention.\n- Hard runtime/resource/cost quotas, durable workflow recovery and comprehensive dirty-source replay.\n- Additional frameworks and connectors beyond the approved MVP. Displaced clauses remain in the migration record.\n\n## Implementation Phase\n\n**Phase:** Not specified. Define story/milestone implementation phases and granular tasks in a separate owning plan.\n\n**Deliverables:** The assigned milestone outcomes and criterion-mapped evidence above.\n\n**Developer Validation:** Confirm public test boundaries before executable tests. Stop at every implementation phase gate, including the final gate, for explicit developer approval.\n\n**Exit Criteria:** Verify the assigned criteria; phase approval and whole-story/milestone acceptance remain distinct. Written-plan approval does not approve implementation gates.\n\n## Validation Approach\n\n### Automated Validation\n\n- Configured data quality checks, split disjointness, seeded membership and supplied time/group-aware partition cases.\n- Use independently defined outcomes through installed public interfaces and separate experiment-project fixtures; follow small vertical red–green TDD slices.\n- Follow the repository verification policy: current milestone at executable gates; M1–6 selection at story acceptance; preserve failures/skips and explicit authorization requirements for broader/artifact checks.\n\n### Developer Validation\n\n- Review criterion-mapped evidence, failures, artifact/run/data references and platform/tool identities.\n- Preserve development approval gates and separate milestone verification obligations; do not infer runtime behavior from documentation.\n\n## Dependencies / References\n\n- [Authoritative user stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md).\n- [Approved original scope dispositions and assistant walkthrough](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md).\n- [Revision plan and approval history](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/plans/mvp-scope-revision.md).\n- [Verification policy](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/development/verification.md#phase-and-story-verification).\n- [Active MVP design](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/agentic-ml-harness-design.md) defines the revised trusted-local scope; archived 0.14 platform contracts are historical reference. Synchronize issue scope and the reviewed source revision before product implementation.\n",
  "closed_by": null,
  "reactions": {
    "url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15/reactions",
    "total_count": 0,
    "+1": 0,
    "-1": 0,
    "laugh": 0,
    "hooray": 0,
    "confused": 0,
    "heart": 0,
    "rocket": 0,
    "eyes": 0
  },
  "timeline_url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15/timeline",
  "performed_via_github_app": null,
  "state_reason": null,
  "pinned_comment": null
}
```

## Complete comments (creation order)

```json
[
  {
    "url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/comments/6699586004",
    "html_url": "https://github.com/jimthompson5802/agentic-ml/issues/15#issuecomment-6699586004",
    "issue_url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/15",
    "id": 6699586004,
    "node_id": "IC_kwDOVZ7kv88AAAABj1OR1A",
    "user": {
      "login": "jimthompson5802",
      "id": 1425269,
      "node_id": "MDQ6VXNlcjE0MjUyNjk=",
      "avatar_url": "https://avatars.githubusercontent.com/u/1425269?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/jimthompson5802",
      "html_url": "https://github.com/jimthompson5802",
      "followers_url": "https://api.github.com/users/jimthompson5802/followers",
      "following_url": "https://api.github.com/users/jimthompson5802/following{/other_user}",
      "gists_url": "https://api.github.com/users/jimthompson5802/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/jimthompson5802/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/jimthompson5802/subscriptions",
      "organizations_url": "https://api.github.com/users/jimthompson5802/orgs",
      "repos_url": "https://api.github.com/users/jimthompson5802/repos",
      "events_url": "https://api.github.com/users/jimthompson5802/events{/privacy}",
      "received_events_url": "https://api.github.com/users/jimthompson5802/received_events",
      "type": "User",
      "user_view_type": "public",
      "site_admin": false
    },
    "created_at": "2026-11-07T00:28:41Z",
    "updated_at": "2026-11-07T00:28:41Z",
    "body": "MVP scope decision MVP-SC-01/MVP-SC-02 — 2026-11-06\n\nGate 2 was subsequently approved by “I approve gate 2 and authorize phase 3”; this records scope/design context, not new executable acceptance.\n\nDeveloper “i approve gate 1 and authorize phase 2” approved the criterion dispositions and milestone migration. The revised body preserves original IDs and distinguishes active outcomes from deferred scope. The issue remains open; no criterion is newly verified by this edit.\n\nAssignments: US-12-AC-01: M1; US-12-AC-05: M1.\n\n[Original criterion text and displaced guarantees](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/reviews/mvp-scope-criterion-dispositions.md#criterion-level-disposition-matrix) remain review history. [Revised stories](https://github.com/jimthompson5802/agentic-ml/blob/main/docs/specs/user-stories.md) govern the new delivery scope after synchronized publication. Existing development/testing gates and historical verification obligations remain unchanged. Managed security, approvals, recovery and broader platform capabilities are deferred only as recorded in the approved matrix.\n",
    "author_association": "OWNER",
    "pin": null,
    "reactions": {
      "url": "https://api.github.com/repos/jimthompson5802/agentic-ml/issues/comments/6699586004/reactions",
      "total_count": 0,
      "+1": 0,
      "-1": 0,
      "laugh": 0,
      "hooray": 0,
      "confused": 0,
      "heart": 0,
      "rocket": 0,
      "eyes": 0
    },
    "performed_via_github_app": null,
    "minimized": null
  }
]
```
