"""Verify scoped delegated decisions through the public experiment interfaces."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from test_planning import planning_project as planning_project

from agentic_ml.planning import ResolveRequest, resolve_plan, verify_plan


def test_delegated_cost_cannot_hide_a_missing_currency(planning_project: Path) -> None:
    """AC-04: a complete cost proposal must obey the explicit pair contract."""
    path = planning_project / "brief.md"
    path.write_text(
        path.read_text().replace(
            "max_cost: null",
            'max_cost: {delegate: "Choose cost", proposal: 10, rationale: "Trial budget"}',
        )
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is None
    assert result.diagnostics[0].code == "conflicting_budget"
    assert result.diagnostics[0].source_path == "brief.md"


@pytest.mark.parametrize("delegated", ["cost", "currency", "both"])
@pytest.mark.parametrize(
    "cost,currency,conflict",
    [(10, "USD", False), (None, None, False), (10, None, True), (None, "USD", True)],
)
def test_cost_currency_pair_contract_applies_to_complete_proposals(
    planning_project: Path,
    delegated: str,
    cost: int | None,
    currency: str | None,
    conflict: bool,
) -> None:
    """AC-01/03/04: approval cannot turn a complete conflicting pair ready."""
    from agentic_ml.approvals import ApprovalRequest, approve_plan
    from agentic_ml.planning import inspect_plan

    cost_value = json.dumps(
        {"delegate": "Choose cost", "proposal": cost, "rationale": "Trial budget"}
        if delegated in ("cost", "both")
        else cost
    )
    currency_value = json.dumps(
        {
            "delegate": "Choose currency",
            "proposal": currency,
            "rationale": "Accounting unit",
        }
        if delegated in ("currency", "both")
        else currency
    )
    path = planning_project / "brief.md"
    path.write_text(
        path.read_text()
        .replace("max_cost: null", "max_cost: " + cost_value)
        .replace("currency: null", "currency: " + currency_value)
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    if conflict:
        assert result.plan_id is None
        assert result.diagnostics[0].code == "conflicting_budget"
        assert result.diagnostics[0].field == "budget.max_cost"
        return
    assert result.plan_id is not None
    record = approve_plan(
        ApprovalRequest(planning_project, result.plan_id, "Scientist", "Reviewed pair")
    )
    checked = verify_plan(project_root=planning_project, plan_id=result.plan_id)
    assert checked.status == "input_ready" and checked.integrity
    assert checked.approval_ids == (record.approval_id,)
    inspection = inspect_plan(project_root=planning_project, plan_id=result.plan_id)
    assert inspection.plan is not None
    effective = inspection.plan["effective"]
    assert isinstance(effective, dict)
    budget = effective["budget"]
    assert isinstance(budget, dict)
    assert budget["max_cost"] == cost and budget["currency"] == currency


@pytest.mark.parametrize(
    "cost,currency",
    [
        ('{delegate: "Choose cost"}', "USD"),
        ('{delegate: "Choose cost"}', "null"),
        ("10", '{delegate: "Choose currency"}'),
        ("null", '{delegate: "Choose currency"}'),
        (
            '{delegate: "Choose cost"}',
            '{delegate: "Choose currency", proposal: null, rationale: "No cost"}',
        ),
        (
            '{delegate: "Choose cost", proposal: null, rationale: "No cost"}',
            '{delegate: "Choose currency"}',
        ),
    ],
)
def test_unresolved_cost_or_currency_remains_pending(
    planning_project: Path,
    cost: str,
    currency: str,
) -> None:
    """AC-04: missing proposals are not confused with explicit null proposals."""
    from agentic_ml.approvals import ApprovalError, ApprovalRequest, approve_plan

    path = planning_project / "brief.md"
    path.write_text(
        path.read_text()
        .replace("max_cost: null", "max_cost: " + cost)
        .replace("currency: null", "currency: " + currency)
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is not None
    assert any(item.code == "pending_decision" for item in result.diagnostics)
    with pytest.raises(ApprovalError) as raised:
        approve_plan(
            ApprovalRequest(planning_project, result.plan_id, "Scientist", "Reviewed")
        )
    assert raised.value.code == "pending_decision"
    assert (
        verify_plan(project_root=planning_project, plan_id=result.plan_id).status
        == "blocked"
    )


def test_approval_store_cannot_overlap_configured_storage(
    planning_project: Path,
) -> None:
    """AC-03/04: approval publication must not enter a configured artifact store."""
    from agentic_ml.approvals import ApprovalError, ApprovalRequest, approve_plan

    project = planning_project / "project.yaml"
    project.write_text(
        project.read_text().replace(
            "artifacts: .agentic-ml/artifacts", "artifacts: .agentic-ml/plan-approvals"
        )
    )
    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None
    with pytest.raises(ApprovalError) as raised:
        approve_plan(ApprovalRequest(planning_project, result.plan_id, "A", "Reviewed"))
    assert raised.value.code == "storage_conflict"
    assert not (planning_project / ".agentic-ml/plan-approvals").exists()


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "malformed",
        "wrong_reference",
        "staging",
        "symlink",
        "lock",
    ],
)
def test_current_record_storage_is_independently_rechecked(
    planning_project: Path,
    mutation: str,
) -> None:
    """AC-03/04: corruption blocks, staging is ignored and stale locks remain."""
    from agentic_ml.approvals import (
        ApprovalRequest,
        RevocationRequest,
        approve_plan,
        revoke_approval,
    )
    from agentic_ml.planning import PlanningError

    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    plan_id = resolve_plan(
        ResolveRequest(planning_project, Path("experiment.yaml"))
    ).plan_id
    assert plan_id is not None
    record = approve_plan(ApprovalRequest(planning_project, plan_id, "A", "Reviewed"))
    directory = planning_project / ".agentic-ml/plan-approvals" / plan_id[7:]
    path = directory / "approvals" / (record.approval_id + ".json")
    if mutation == "missing":
        path.unlink()
    elif mutation == "duplicate":
        path.write_bytes(path.read_bytes().replace(b"{", b'{"reason":"duplicate",', 1))
    elif mutation == "malformed":
        path.write_bytes(b"{")
    elif mutation == "wrong_reference":
        revoke = revoke_approval(
            RevocationRequest(
                planning_project, plan_id, record.approval_id, "A", "Reconsider"
            )
        )
        path = directory / "revocations" / (revoke.revocation_id + ".json")
        payload = json.loads(path.read_bytes())
        payload["approval_id"] = "00000000-0000-0000-0000-000000000000"
        path.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        )
    elif mutation == "staging":
        (directory / "approvals/.pending-incomplete").write_bytes(b"{")
    elif mutation == "symlink":
        content = path.read_bytes()
        path.unlink()
        target = planning_project.parent / "external.json"
        target.write_bytes(content)
        path.symlink_to(target)
    else:
        (directory / "approval.lock").write_bytes(b"operator review")
        with pytest.raises(PlanningError, match="operator review"):
            verify_plan(project_root=planning_project, plan_id=plan_id)
        assert (directory / "approval.lock").read_bytes() == b"operator review"
        return
    checked = verify_plan(project_root=planning_project, plan_id=plan_id)
    assert checked.status == ("input_ready" if mutation == "staging" else "blocked")


@pytest.mark.parametrize("changed", ["metric", "budget", "search"])
def test_approval_never_rebinds_to_revised_inputs(
    planning_project: Path, changed: str
) -> None:
    """AC-03/04: old evidence stays valid; revised inputs need new approval."""
    from agentic_ml.approvals import ApprovalRequest, approve_plan

    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    request = ResolveRequest(planning_project, Path("experiment.yaml"))
    original = resolve_plan(request)
    assert original.plan_id is not None
    approve_plan(ApprovalRequest(planning_project, original.plan_id, "A", "Reviewed"))
    if changed == "metric":
        brief.write_text(
            brief.read_text().replace("proposal: f1_macro", "proposal: accuracy")
        )
    elif changed == "budget":
        brief.write_text(
            brief.read_text().replace(
                "max_runtime_seconds: 60", "max_runtime_seconds: 30"
            )
        )
    else:
        path = planning_project / "search.yaml"
        path.write_text(path.read_text() + "\n# revised boundary source\n")
    revised = resolve_plan(request)
    assert revised.plan_id is not None and revised.plan_id != original.plan_id
    assert revised.status == "blocked"
    assert (
        verify_plan(project_root=planning_project, plan_id=original.plan_id).status
        == "input_ready"
    )
    current = verify_plan(
        project_root=planning_project, plan_id=original.plan_id, check_current=True
    )
    assert current.status == "blocked" and current.diagnostics[0].code == "stale_source"
    bundle = (
        planning_project
        / ".agentic-ml/plans"
        / original.plan_id[7:]
        / "sources/experiment.md"
    )
    bundle.write_bytes(b"corrupt")
    assert not verify_plan(
        project_root=planning_project, plan_id=original.plan_id
    ).integrity


@pytest.mark.parametrize("delegation", [False, True])
def test_approval_requires_complete_proposals(
    planning_project: Path, delegation: bool
) -> None:
    """AC-04: explicit-only and unresolved plans cannot receive approval records."""
    from agentic_ml.approvals import ApprovalError, ApprovalRequest, approve_plan

    if delegation:
        path = planning_project / "brief.md"
        path.write_text(
            path.read_text().replace("metric: f1_macro", 'metric: {delegate: "Choose"}')
        )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None
    with pytest.raises(ApprovalError) as raised:
        approve_plan(ApprovalRequest(planning_project, result.plan_id, "A", "Reviewed"))
    assert raised.value.code == ("pending_decision" if delegation else "no_delegations")


def test_approved_proposal_becomes_ready_without_changing_plan(
    planning_project: Path,
) -> None:
    """AC-03/04: one explicit record covers the preserved proposed decision."""
    from agentic_ml.approvals import ApprovalRequest, approve_plan

    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose metric", proposal: f1_macro, rationale: "Class balance"}',
        )
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is not None
    record = approve_plan(
        ApprovalRequest(
            planning_project, result.plan_id, "Scientist", "Reviewed metric"
        )
    )
    assert record.authentication == "none"
    assert record.reviewer == "Scientist"
    assert record.decisions == (
        {
            "field": "evaluation.metric",
            "value": "f1_macro",
            "rationale": "Class balance",
        },
    )
    checked = verify_plan(project_root=planning_project, plan_id=result.plan_id)
    assert checked.status == "input_ready" and checked.integrity
    assert checked.plan_id == result.plan_id
    assert checked.authentication == "none"
    assert checked.approval_ids == (record.approval_id,)
    assert (
        resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml"))).status
        == "input_ready"
    )


def test_revocation_blocks_only_its_approval_and_new_approval_restores_readiness(
    planning_project: Path,
) -> None:
    """AC-04: readiness uses current append-only records, never a cached flag."""
    from agentic_ml.approvals import (
        ApprovalRequest,
        RevocationRequest,
        approve_plan,
        revoke_approval,
    )

    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    plan_id = resolve_plan(
        ResolveRequest(planning_project, Path("experiment.yaml"))
    ).plan_id
    assert plan_id is not None
    first = approve_plan(ApprovalRequest(planning_project, plan_id, "A", "Reviewed"))
    second = approve_plan(ApprovalRequest(planning_project, plan_id, "B", "Reviewed"))
    revoked = revoke_approval(
        RevocationRequest(
            planning_project, plan_id, first.approval_id, "A", "Reconsider"
        )
    )
    assert revoked.authentication == "none" and revoked.approval_id == first.approval_id
    assert verify_plan(project_root=planning_project, plan_id=plan_id).approval_ids == (
        second.approval_id,
    )
    revoke_approval(
        RevocationRequest(
            planning_project, plan_id, second.approval_id, "B", "Reconsider"
        )
    )
    checked = verify_plan(project_root=planning_project, plan_id=plan_id)
    assert checked.status == "blocked" and checked.integrity
    third = approve_plan(ApprovalRequest(planning_project, plan_id, "C", "Reapproved"))
    assert verify_plan(project_root=planning_project, plan_id=plan_id).approval_ids == (
        third.approval_id,
    )


@pytest.mark.parametrize(
    "change",
    [
        {"extra": True},
        {"reviewer": " "},
        {"reason": 7},
        {"recorded_at": "2026-02-30T00:00:00Z"},
        {"approval_id": "invalid"},
        {"authentication": "verified"},
        {"project_root": "/other"},
        {"experiment_id": "other"},
        {"plan_id": "sha256:" + "0" * 64},
        {"purpose": "execution"},
        {"decision": "reject"},
        {
            "decisions": [
                {
                    "field": "evaluation.metric",
                    "value": "accuracy",
                    "rationale": "Balance",
                }
            ]
        },
    ],
)
def test_invalid_final_approval_blocks_readiness(
    planning_project: Path,
    change: dict[str, object],
) -> None:
    """AC-04: independently edited records cannot silently change reviewed scope."""
    from agentic_ml.approvals import ApprovalRequest, approve_plan

    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    plan_id = resolve_plan(
        ResolveRequest(planning_project, Path("experiment.yaml"))
    ).plan_id
    assert plan_id is not None
    record = approve_plan(ApprovalRequest(planning_project, plan_id, "A", "Reviewed"))
    path = (
        planning_project
        / ".agentic-ml/plan-approvals"
        / plan_id[7:]
        / "approvals"
        / (record.approval_id + ".json")
    )
    payload = json.loads(path.read_bytes())
    payload.update(change)
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    checked = verify_plan(project_root=planning_project, plan_id=plan_id)
    assert checked.status == "blocked" and checked.integrity
    assert checked.diagnostics[0].code == "invalid_approval"


def test_cli_records_approval_and_revocation(planning_project: Path) -> None:
    """AC-04/05: commands work from an unrelated cwd and emit versioned records."""
    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            'metric: {delegate: "Choose", proposal: f1_macro, rationale: "Balance"}',
        )
    )
    plan_id = resolve_plan(
        ResolveRequest(planning_project, Path("experiment.yaml"))
    ).plan_id
    assert plan_id is not None
    common = ["--project-root", str(planning_project), "--plan", plan_id]
    approved = subprocess.run(
        [
            str(Path(sys.executable).with_name("agentic-ml")),
            "plan",
            "approve",
            *common,
            "--reviewer",
            "Scientist",
            "--reason",
            "Reviewed",
        ],
        cwd=planning_project.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert approved.returncode == 0, approved.stderr
    payload = json.loads(approved.stdout)
    assert payload["authentication"] == "none"
    assert payload["decisions"] == [
        {"field": "evaluation.metric", "value": "f1_macro", "rationale": "Balance"}
    ]
    revoked = subprocess.run(
        [
            str(Path(sys.executable).with_name("agentic-ml")),
            "plan",
            "revoke-approval",
            *common,
            "--approval",
            payload["approval_id"],
            "--reviewer",
            "Scientist",
            "--reason",
            "Reconsider",
        ],
        cwd=planning_project.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert revoked.returncode == 0, revoked.stderr
    assert json.loads(revoked.stdout)["approval_id"] == payload["approval_id"]
    assert (
        verify_plan(project_root=planning_project, plan_id=plan_id).status == "blocked"
    )


def test_null_proposal_is_resolved_and_inspection_exposes_approval(
    planning_project: Path,
) -> None:
    """AC-01/04: an explicitly proposed nullable budget still requires approval."""
    from agentic_ml.approvals import ApprovalRequest, approve_plan
    from agentic_ml.planning import inspect_plan

    path = planning_project / "brief.md"
    path.write_text(
        path.read_text().replace(
            "max_memory_mb: null",
            'max_memory_mb: {delegate: "Choose memory ceiling", proposal: null, rationale: "No ceiling"}',
        )
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None and result.status == "blocked"
    record = approve_plan(
        ApprovalRequest(planning_project, result.plan_id, "A", "Reviewed")
    )
    checked = inspect_plan(project_root=planning_project, plan_id=result.plan_id)
    assert checked.status == "input_ready"
    assert checked.authentication == "none" and checked.approval_ids == (
        record.approval_id,
    )
