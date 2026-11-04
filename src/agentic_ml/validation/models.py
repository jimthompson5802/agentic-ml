"""Typed public requests and outcomes for semantic configuration validation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from agentic_ml.planning.models import Diagnostic, JSONValue

type RegistryDocument = dict[str, JSONValue]
type ValidationStatus = Literal["valid", "blocked"]


@dataclass(frozen=True)
class RegistryResult:
    """Return a checked metadata registry or blocking diagnostics."""

    status: ValidationStatus
    registry: RegistryDocument | None
    registry_id: str | None
    diagnostics: tuple[Diagnostic, ...] = ()


@dataclass(frozen=True)
class ConfigurationRequest:
    """Select a preserved plan and optional project-relative registry file."""

    project_root: Path
    plan_id: str
    registry: Path | None = None


@dataclass(frozen=True)
class ConfigurationResult:
    """Report semantic configuration validation and immutable evidence identity."""

    status: ValidationStatus
    validation_id: str | None
    configuration: dict[str, JSONValue] | None
    diagnostics: tuple[Diagnostic, ...] = ()


class ValidationError(Exception):
    """Report an operational failure separately from invalid scientific inputs."""

    def __init__(self, code: str, message: str) -> None:
        """Initialize a safe operational diagnostic."""
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class CandidateRequest:
    """Bind proposed algorithm parameters to current validation evidence."""

    project_root: Path
    validation_id: str
    algorithm: str
    parameters: dict[str, JSONValue]


@dataclass(frozen=True)
class CandidateResult:
    """Return complete effective parameters and their independently checked origins."""

    status: ValidationStatus
    validation_id: str
    algorithm: str
    parameters: dict[str, JSONValue] | None
    origins: dict[str, str] | None
    diagnostics: tuple[Diagnostic, ...] = ()


@dataclass(frozen=True)
class ValidationInspection(ConfigurationResult):
    """Distinguish preserved evidence integrity from its present currentness."""

    integrity: bool = False
    current: bool = False
