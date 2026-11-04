"""Public metadata, configuration and candidate validation interfaces."""

from agentic_ml.validation.candidates import validate_candidate
from agentic_ml.validation.configuration import (
    inspect_validation,
    validate_configuration,
)
from agentic_ml.validation.models import (
    CandidateRequest,
    CandidateResult,
    ConfigurationRequest,
    ConfigurationResult,
    RegistryDocument,
    RegistryResult,
    ValidationError,
    ValidationInspection,
)
from agentic_ml.validation.registry import validate_registry

__all__ = [
    "CandidateRequest",
    "CandidateResult",
    "ConfigurationRequest",
    "ConfigurationResult",
    "RegistryDocument",
    "RegistryResult",
    "ValidationError",
    "ValidationInspection",
    "validate_candidate",
    "validate_configuration",
    "validate_registry",
    "inspect_validation",
]
