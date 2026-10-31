"""Public experiment planning requests and results."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

PlanStatus = Literal["blocked", "input_ready"]
type JSONValue = (
    None | bool | int | float | str | list[JSONValue] | dict[str, JSONValue]
)


@dataclass(frozen=True)
class ResolveRequest:
    """Select an experiment input relative to an explicit project root."""

    project_root: Path
    experiment: Path


@dataclass(frozen=True)
class Diagnostic:
    """Describe a blocking field or source problem without exposing content."""

    code: str
    field: str
    source_path: str
    line: int | None
    column: int | None
    message: str


@dataclass(frozen=True)
class PlanResult:
    """Report immutable capture identity and derived input readiness."""

    plan_id: str | None
    status: PlanStatus
    diagnostics: tuple[Diagnostic, ...]


class PlanningError(Exception):
    """Report an operational failure using a stable code and safe message."""

    def __init__(self, code: str, message: str) -> None:
        """Initialize the operational failure."""
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class VerificationResult(PlanResult):
    """Report recomputed integrity and preserved-input readiness."""

    integrity: bool


@dataclass(frozen=True)
class PlanInspection:
    """Expose preserved plan evidence with independently checked integrity."""

    plan_id: str
    status: PlanStatus
    integrity: bool
    plan: dict[str, JSONValue] | None
    diagnostics: tuple[Diagnostic, ...]
