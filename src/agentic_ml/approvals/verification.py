"""Derive approval scope solely from independently verified preserved plans."""

import json
from datetime import UTC, datetime
from importlib.resources import files
from uuid import UUID, uuid4

from jsonschema import Draft202012Validator, FormatChecker

from agentic_ml.approvals.models import (
    ApprovalError,
    ApprovalRecord,
    ApprovalRequest,
    RevocationRecord,
    RevocationRequest,
)
from agentic_ml.approvals.storage import append_record, locked, read_records
from agentic_ml.planning.models import JSONValue
from agentic_ml.planning.parsing import InputError, mapping, sequence
from agentic_ml.planning.paths import ProjectAccess
from agentic_ml.planning.storage import canonical, checked_json


def decisions(plan: dict[str, JSONValue]) -> tuple[dict[str, JSONValue], ...]:
    """Extract every delegated proposal and its rationale in preserved order."""
    result = []
    for raw in sequence(plan["decisions"]):
        item = mapping(raw)
        if item["origin"] == "delegated":
            original = mapping(item["original"])
            if "proposal" not in original or not item["rationale"]:
                raise ApprovalError(
                    "pending_decision",
                    "Every delegation needs a proposal and rationale.",
                )
            result.append(
                {
                    "field": item["field"],
                    "value": item["proposed"],
                    "rationale": item["rationale"],
                }
            )
    return tuple(result)


def scope(plan: dict[str, JSONValue], plan_id: str) -> dict[str, JSONValue]:
    """Bind a record to this project, experiment and exact immutable version."""
    return {
        "schema_version": "1.0",
        "authentication": "none",
        "project_root": mapping(plan["project"])["root"],
        "experiment_id": plan["experiment_id"],
        "plan_id": plan_id,
    }


def approval_record(value: dict[str, JSONValue]) -> ApprovalRecord:
    """Convert a validated record into the public frozen result."""
    return ApprovalRecord(
        schema_version=str(value["schema_version"]),
        approval_id=str(value["approval_id"]),
        authentication=str(value["authentication"]),
        reviewer=str(value["reviewer"]),
        reason=str(value["reason"]),
        project_root=str(value["project_root"]),
        experiment_id=str(value["experiment_id"]),
        plan_id=str(value["plan_id"]),
        purpose=str(value["purpose"]),
        decision=str(value["decision"]),
        decisions=tuple(mapping(item) for item in sequence(value["decisions"])),
        recorded_at=str(value["recorded_at"]),
    )


def validate_record(raw: bytes, name: str, kind: str) -> dict[str, JSONValue]:
    """Check canonical JSON, strict schema, timestamp and filename identity."""
    value = mapping(checked_json(raw))
    schema = json.loads(
        files("agentic_ml").joinpath(f"schemas/approvals/1.0/{kind}.json").read_bytes()
    )
    if list(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)
    ):
        raise ApprovalError("invalid_approval", "Invalid approval record schema.")
    datetime.strptime(str(value["recorded_at"]), "%Y-%m-%dT%H:%M:%SZ")
    key = kind + "_id"
    if str(value[key]) + ".json" != name:
        raise ApprovalError(
            "invalid_approval", "Record filename does not match its identity."
        )
    return value


def approval_ids(
    access: ProjectAccess, plan_id: str, plan: dict[str, JSONValue]
) -> tuple[str, ...]:
    """Return matching current approvals, rejecting malformed final records."""
    expected = decisions(plan)
    with locked(access, plan_id) as (path, _):
        result = []
        for name, raw in read_records(access, path, "approvals"):
            value = validate_record(raw, name, "approval")
            record = approval_record(value)
            if any(
                value.get(key) != item for key, item in scope(plan, plan_id).items()
            ):
                raise ApprovalError(
                    "invalid_approval", "Approval scope does not match."
                )
            if canonical(value["decisions"]) != canonical(list(expected)):
                raise ApprovalError(
                    "invalid_approval", "Approval decisions do not match."
                )
            if (
                record.purpose != "delegated_input_decisions"
                or record.decision != "approve"
            ):
                raise ApprovalError("invalid_approval", "Invalid approval purpose.")
            UUID(record.approval_id)
            result.append(record.approval_id)
        revoked = set()
        for name, raw in read_records(access, path, "revocations"):
            value = validate_record(raw, name, "revocation")
            if (
                any(
                    value.get(key) != item for key, item in scope(plan, plan_id).items()
                )
                or value.get("approval_id") not in result
            ):
                raise ApprovalError(
                    "invalid_approval", "Invalid revocation scope or reference."
                )
            revoked.add(str(value["approval_id"]))
        return tuple(item for item in result if item not in revoked)


def approve_plan(request: ApprovalRequest) -> ApprovalRecord:
    """Append explicit unauthenticated approval for every proposed decision."""
    from agentic_ml.planning.resolution import verify_evidence

    access = None
    try:
        if not request.reviewer.strip() or not request.reason.strip():
            raise ApprovalError(
                "invalid_approval", "Reviewer and reason must be nonempty."
            )
        access = ProjectAccess(request.project_root)
        result, plan = verify_evidence(access, request.plan_id, False, approvals=False)
        if not result.integrity or plan is None:
            raise ApprovalError("invalid_plan", "Plan integrity must be verified.")
        proposed = decisions(plan)
        if not proposed:
            raise ApprovalError("no_delegations", "Plan has no delegated decisions.")
        value = scope(plan, request.plan_id) | {
            "approval_id": str(uuid4()),
            "reviewer": request.reviewer,
            "reason": request.reason,
            "purpose": "delegated_input_decisions",
            "decision": "approve",
            "decisions": list(proposed),
            "recorded_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        with locked(access, request.plan_id) as (path, _):
            append_record(access, path, "approvals", str(value["approval_id"]), value)
        return approval_record(value)
    except InputError as error:
        raise ApprovalError(error.diagnostic.code, error.diagnostic.message) from error
    except (ValueError, TypeError, KeyError) as error:
        raise ApprovalError("invalid_approval", "Invalid approval evidence.") from error
    except OSError as error:
        raise ApprovalError(
            "approval_io", "Unable to access approval evidence.", operational=True
        ) from error
    finally:
        if access is not None:
            access.close()


def revoke_approval(request: RevocationRequest) -> RevocationRecord:
    """Append a scoped revocation; preserve the original approval and plan."""
    from agentic_ml.planning.resolution import verify_evidence

    access = None
    try:
        if not request.reviewer.strip() or not request.reason.strip():
            raise ApprovalError(
                "invalid_approval", "Reviewer and reason must be nonempty."
            )
        access = ProjectAccess(request.project_root)
        _, plan = verify_evidence(access, request.plan_id, False, approvals=False)
        if plan is None:
            raise ApprovalError("invalid_plan", "Plan integrity must be verified.")
        with locked(access, request.plan_id) as (path, _):
            found = False
            for name, raw in read_records(access, path, "approvals"):
                value = validate_record(raw, name, "approval")
                if value.get("approval_id") == request.approval_id:
                    if any(
                        value.get(key) != item
                        for key, item in scope(plan, request.plan_id).items()
                    ) or canonical(value["decisions"]) != canonical(
                        list(decisions(plan))
                    ):
                        raise ApprovalError(
                            "invalid_approval", "Approval scope does not match."
                        )
                    found = True
            if not found:
                raise ApprovalError(
                    "missing_approval", "Referenced approval is missing."
                )
            value = scope(plan, request.plan_id) | {
                "revocation_id": str(uuid4()),
                "approval_id": request.approval_id,
                "reviewer": request.reviewer,
                "reason": request.reason,
                "recorded_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            append_record(
                access, path, "revocations", str(value["revocation_id"]), value
            )
        return RevocationRecord(
            "1.0",
            str(value["revocation_id"]),
            "none",
            request.approval_id,
            str(request.project_root),
            str(plan["experiment_id"]),
            request.plan_id,
            request.reviewer,
            request.reason,
            str(value["recorded_at"]),
        )
    except InputError as error:
        raise ApprovalError(error.diagnostic.code, error.diagnostic.message) from error
    except (ValueError, TypeError, KeyError) as error:
        raise ApprovalError("invalid_approval", "Invalid approval evidence.") from error
    except OSError as error:
        raise ApprovalError(
            "approval_io", "Unable to access approval evidence.", operational=True
        ) from error
    finally:
        if access is not None:
            access.close()
