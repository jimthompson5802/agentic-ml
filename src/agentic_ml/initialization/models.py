"""Public initialization options and observable setup results."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InitOptions:
    """Select a project and explicit setup destinations without granting access."""

    project_root: Path
    experiment: str = "initial"
    package_name: str | None = None
    dvc_store: Path | None = None
    mlflow_backend: Path | None = None
    artifact_store: Path | None = None
    state_store: Path | None = None


@dataclass(frozen=True)
class InitResult:
    """Describe setup changes and work that still requires configuration."""

    project_root: Path
    created: tuple[str, ...]
    updated: tuple[str, ...]
    unchanged: tuple[str, ...]
    setup_pending: tuple[str, ...]


class InitializationError(Exception):
    """Report a safe setup failure with stage and recovery information."""

    def __init__(
        self,
        message: str,
        *,
        stage: str = "preflight",
        conflicts: tuple[str, ...] = (),
        completed_steps: tuple[str, ...] = (),
        recovery: str = "Resolve the conflict and rerun init with the same options.",
    ) -> None:
        """Keep user-visible diagnostics separate from exception causes."""
        super().__init__(message)
        self.stage = stage
        self.conflicts = conflicts
        self.completed_steps = completed_steps
        self.recovery = recovery


@dataclass(frozen=True)
class ProjectConfig:
    """Represent the minimal draft project configuration."""

    project: dict[str, str]
    storage: dict[str, str]
    setup: dict[str, str]
    schema_version: str = "0.1"
    guidance: tuple[str, ...] = ()
    components: tuple[str, ...] = ()


@dataclass(frozen=True)
class DraftExperiment:
    """Represent unconfigured experiment inputs without execution authority."""

    id: str
    brief: str
    search_space: str
    notebooks: tuple[str, ...]
    schema_version: str = "0.1"
    working_directory: str = "."
    data: tuple[str, ...] = ()
    execution_status: str = "unconfigured"


@dataclass(frozen=True)
class DraftSearchSpace:
    """Represent an empty allowed-algorithm boundary."""

    schema_version: str = "0.1"
    algorithms: tuple[str, ...] = ()


@dataclass(frozen=True)
class InitialState:
    """Represent initial durable state with no runs or approvals."""

    experiment: str
    schema_version: str = "0.1"
    status: str = "unconfigured"
    approvals: tuple[str, ...] = ()
    runs: tuple[str, ...] = ()
