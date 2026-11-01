"""Public unauthenticated experiment approval requests and records."""

from dataclasses import dataclass
from pathlib import Path

from agentic_ml.planning.models import JSONValue


@dataclass(frozen=True)
class ApprovalRequest:
    """Approve all proposed delegated decisions in an exact preserved plan."""

    project_root: Path
    plan_id: str
    reviewer: str
    reason: str


@dataclass(frozen=True)
class ApprovalRecord:
    """Preserve scoped approval with an explicitly unverified reviewer label."""

    schema_version: str
    approval_id: str
    authentication: str
    reviewer: str
    reason: str
    project_root: str
    experiment_id: str
    plan_id: str
    purpose: str
    decision: str
    decisions: tuple[dict[str, JSONValue], ...]
    recorded_at: str


class ApprovalError(Exception):
    """Report invalid approval scope or operational storage failures safely."""

    def __init__(self, code: str, message: str, *, operational: bool = False) -> None:
        """Set the stable diagnostic code and operational failure category."""
        super().__init__(message)
        self.code = code
        self.operational = operational


@dataclass(frozen=True)
class RevocationRequest:
    """Revoke one existing approval within its exact plan scope."""

    project_root: Path
    plan_id: str
    approval_id: str
    reviewer: str
    reason: str


@dataclass(frozen=True)
class RevocationRecord:
    """Preserve an unauthenticated revocation of one scoped approval."""

    schema_version: str
    revocation_id: str
    authentication: str
    approval_id: str
    project_root: str
    experiment_id: str
    plan_id: str
    reviewer: str
    reason: str
    recorded_at: str
