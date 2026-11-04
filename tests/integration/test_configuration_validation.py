"""Verify US-05 semantic validation through its approved public interfaces."""

from pathlib import Path
from typing import cast

import pytest
import yaml
from test_planning import planning_project as planning_project

from agentic_ml.planning.models import JSONValue

pytestmark = pytest.mark.milestone_1


def test_builtin_registry_records_complete_scalar_defaults() -> None:
    """AC-01/03: both tasks have explicit, independently specified defaults."""
    from agentic_ml.validation import validate_registry

    result = validate_registry()
    assert result.status == "valid"
    assert result.registry_id is not None
    assert result.registry is not None
    algorithms = result.registry["algorithms"]
    assert isinstance(algorithms, list)
    defaults: dict[str, dict[str, JSONValue]] = {}
    for entry in algorithms:
        assert isinstance(entry, dict)
        parameters = cast(dict[str, dict[str, JSONValue]], entry["parameters"])
        defaults[str(entry["id"])] = {
            name: value["default"] for name, value in parameters.items()
        }
    assert defaults == {
        "dummy_classifier": {
            "strategy": "prior",
            "random_state": None,
            "constant": None,
        },
        "dummy_regressor": {"strategy": "mean", "constant": None, "quantile": None},
    }


@pytest.mark.parametrize(
    "declarations,code",
    [
        ({"schema_version": "2.0", "algorithms": []}, "unsupported_version"),
        (
            {"schema_version": "1.0", "algorithms": [{"id": "dummy_classifier"}]},
            "duplicate_algorithm",
        ),
        (
            {"schema_version": "1.0", "algorithms": [{"id": "custom"}]},
            "invalid_registry",
        ),
        (
            {"schema_version": "1.0", "algorithms": [], "extra": True},
            "invalid_registry",
        ),
    ],
)
def test_invalid_registry_never_produces_an_identity(
    declarations: dict[str, object], code: str
) -> None:
    """AC-01/04: malformed and conflicting declarations are blocked."""
    from typing import cast

    from agentic_ml.validation import RegistryDocument, validate_registry

    result = validate_registry(cast(RegistryDocument, declarations))
    assert result.status == "blocked"
    assert result.registry is None and result.registry_id is None
    assert result.diagnostics[0].code == code


def test_unsupported_component_interface_is_reported_explicitly() -> None:
    """AC-01/04: unsupported metadata interfaces cannot be registered."""
    from agentic_ml.validation import validate_registry

    result = validate_registry(
        {
            "schema_version": "1.0",
            "algorithms": [
                {
                    "id": "custom",
                    "interface_version": "9.0",
                    "tasks": ["classification"],
                    "adapter": {"id": "custom", "version": "1"},
                    "library": {
                        "distribution": "nonexistent-us05-library",
                        "reference_version": "1",
                    },
                    "parameters": {},
                    "requires_non_null": [],
                }
            ],
        }
    )
    assert result.status == "blocked"
    assert result.diagnostics[0].code == "unsupported_version"


@pytest.fixture
def semantic_project(planning_project: Path) -> Path:
    """Reuse an accepted public-plan project without reading its missing dataset."""
    for name in ("brief.md", "search.yaml"):
        path = planning_project / name
        path.write_text(
            path.read_text().replace("logistic_regression", "dummy_classifier")
        )
    return planning_project


def test_configuration_preserves_defaults_and_separate_plan_readiness(
    semantic_project: Path,
) -> None:
    """AC-01/03: semantic defaults are recorded without changing US-03 plans."""
    from agentic_ml.planning import ResolveRequest, inspect_plan, resolve_plan
    from agentic_ml.validation import ConfigurationRequest, validate_configuration

    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    result = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert result.status == "valid", result.diagnostics
    assert result.validation_id is not None
    assert result.configuration is not None
    assert result.configuration["execution_authorized"] is False
    assert result.configuration["algorithms"] == {
        "dummy_classifier": {
            "task": "classification",
            "adapter": {"id": "sklearn_dummy_scalar", "version": "1.0"},
            "library_distribution": "scikit-learn",
            "fixed": {},
            "defaults": {"strategy": "prior", "constant": None, "random_state": None},
            "search": {},
        }
    }
    assert (
        inspect_plan(project_root=semantic_project, plan_id=plan.plan_id).status
        == "input_ready"
    )


@pytest.mark.parametrize(
    "algorithm,fixed,search,code",
    [
        ("dummy_regressor", {}, {}, "task_mismatch"),
        ("dummy_classifier", {"unknown": 1}, {}, "unknown_parameter"),
        ("dummy_classifier", {"random_state": True}, {}, "invalid_parameter_type"),
        ("dummy_classifier", {"strategy": "constant"}, {}, "incompatible_combination"),
        (
            "dummy_classifier",
            {},
            {"strategy": {"type": "categorical", "choices": ["prior", "constant"]}},
            "incompatible_combination",
        ),
        (
            "dummy_classifier",
            {},
            {
                "random_state": {
                    "type": "integer",
                    "min": -1,
                    "max": 10,
                    "scale": "linear",
                }
            },
            "invalid_domain",
        ),
    ],
)
def test_configuration_rejects_semantic_errors_before_side_effects(
    semantic_project: Path,
    algorithm: str,
    fixed: dict[str, object],
    search: dict[str, object],
    code: str,
) -> None:
    """AC-01/02/04: structural readiness cannot hide semantic configuration errors."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import ConfigurationRequest, validate_configuration

    brief = semantic_project / "brief.md"
    brief.write_text(brief.read_text().replace("dummy_classifier", algorithm))
    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {algorithm: {"fixed": fixed, "search": search}},
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.status == "input_ready" and plan.plan_id is not None
    result = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert result.status == "blocked"
    assert result.diagnostics[0].code == code
    assert result.diagnostics[0].message
    assert not (semantic_project / ".agentic-ml/validations").exists()


def test_candidate_materializes_values_and_rechecks_saved_evidence(
    semantic_project: Path,
) -> None:
    """AC-03/05: candidates inherit fixed/default values and require live evidence."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        inspect_validation,
        validate_candidate,
        validate_configuration,
    )

    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_classifier": {
                        "fixed": {"strategy": "uniform"},
                        "search": {
                            "random_state": {
                                "type": "integer",
                                "min": 0,
                                "max": 10,
                                "scale": "linear",
                            }
                        },
                    }
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    config = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert config.validation_id is not None
    result = validate_candidate(
        CandidateRequest(
            semantic_project,
            config.validation_id,
            "dummy_classifier",
            {"random_state": 10},
        )
    )
    assert result.status == "valid", result.diagnostics
    assert result.parameters == {
        "strategy": "uniform",
        "random_state": 10,
        "constant": None,
    }
    assert result.origins == {
        "strategy": "fixed",
        "random_state": "candidate",
        "constant": "default",
    }
    inspected = inspect_validation(
        project_root=semantic_project, validation_id=config.validation_id
    )
    assert inspected.status == "valid" and inspected.integrity and inspected.current
    assert inspected.configuration == config.configuration


@pytest.mark.parametrize(
    "algorithm,parameters,code",
    [
        ("outside", {"random_state": 1}, "unknown_algorithm"),
        ("dummy_classifier", {}, "missing_parameter"),
        ("dummy_classifier", {"random_state": True}, "outside_boundary"),
        ("dummy_classifier", {"random_state": 1.0}, "outside_boundary"),
        ("dummy_classifier", {"random_state": 11}, "outside_boundary"),
        (
            "dummy_classifier",
            {"random_state": 1, "strategy": "prior"},
            "fixed_parameter",
        ),
        ("dummy_classifier", {"random_state": 1, "constant": 1}, "default_parameter"),
        ("dummy_classifier", {"random_state": 1, "extra": 1}, "unknown_parameter"),
    ],
)
def test_candidates_cannot_expand_fixed_default_or_search_values(
    semantic_project: Path, algorithm: str, parameters: dict[str, object], code: str
) -> None:
    """AC-02–05: every candidate obeys the same explicit immutable boundaries."""
    from typing import cast

    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.planning.models import JSONValue
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        validate_candidate,
        validate_configuration,
    )

    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_classifier": {
                        "fixed": {"strategy": "uniform"},
                        "search": {
                            "random_state": {
                                "type": "integer",
                                "min": 0,
                                "max": 10,
                                "scale": "linear",
                            }
                        },
                    }
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    config = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert config.validation_id is not None
    result = validate_candidate(
        CandidateRequest(
            semantic_project,
            config.validation_id,
            algorithm,
            cast(dict[str, JSONValue], parameters),
        )
    )
    assert result.status == "blocked"
    assert result.parameters is None and result.origins is None
    assert result.diagnostics[0].code == code


def test_identical_validation_reuses_immutable_evidence(semantic_project: Path) -> None:
    """AC-03: repeated validation reuses identities and preserves published bytes."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import ConfigurationRequest, validate_configuration

    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    request = ConfigurationRequest(semantic_project, plan.plan_id)
    first = validate_configuration(request)
    assert first.validation_id is not None
    bundle = semantic_project / ".agentic-ml/validations" / first.validation_id[7:]
    before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in bundle.iterdir()}
    second = validate_configuration(request)
    assert second.status == "valid" and second.validation_id == first.validation_id
    assert before == {
        p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in bundle.iterdir()
    }


def test_validation_cli_matches_public_api_from_unrelated_cwd(
    semantic_project: Path, tmp_path: Path
) -> None:
    """AC-04/05: CLI uses explicit root and identical configuration/candidate rules."""
    import json
    import subprocess
    import sys

    from agentic_ml.planning import ResolveRequest, resolve_plan

    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    cli = str(Path(sys.executable).with_name("agentic-ml"))
    result = subprocess.run(
        [
            cli,
            "config",
            "validate",
            "--project-root",
            str(semantic_project),
            "--plan-id",
            plan.plan_id,
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    config = json.loads(result.stdout)
    assert config["schema_version"] == "1.0" and config["status"] == "valid"
    candidate = semantic_project / "candidate.json"
    candidate.write_text(
        json.dumps(
            {"schema_version": "1.0", "algorithm": "dummy_classifier", "parameters": {}}
        )
    )
    args = [
        cli,
        "candidate",
        "validate",
        "--project-root",
        str(semantic_project),
        "--validation-id",
        config["validation_id"],
        "--candidate",
        "candidate.json",
    ]
    checked = subprocess.run(
        args, cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert checked.returncode == 0, checked.stderr
    assert json.loads(checked.stdout)["parameters"] == {
        "strategy": "prior",
        "constant": None,
        "random_state": None,
    }
    candidate.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "algorithm": "dummy_classifier",
                "parameters": {"random_state": 1},
            }
        )
    )
    rejected = subprocess.run(
        args, cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert rejected.returncode == 2
    assert json.loads(rejected.stdout)["diagnostics"][0]["code"] == "default_parameter"
    assert (
        json.loads(rejected.stdout)["diagnostics"][0]["source_path"] == "candidate.json"
    )


def test_semantic_diagnostic_identifies_original_search_location(
    semantic_project: Path,
) -> None:
    """AC-04: a bad semantic value points to its original selected source field."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import ConfigurationRequest, validate_configuration

    (semantic_project / "search.yaml").write_text(
        'schema_version: "1.0"\nalgorithms:\n  dummy_classifier:\n    fixed:\n      random_state: true\n    search: {}\n'
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    result = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert result.status == "blocked"
    diagnostic = result.diagnostics[0]
    assert diagnostic.source_path == "search.yaml"
    assert (diagnostic.line, diagnostic.column) == (5, 21)


@pytest.mark.parametrize(
    "change",
    [
        "input",
        "configuration",
        "registry",
        "extra_member",
        "missing_member",
        "wrong_root",
    ],
)
def test_inspection_distinguishes_currentness_from_bundle_integrity(
    semantic_project: Path, tmp_path: Path, change: str
) -> None:
    """AC-03–05: stale or damaged evidence cannot validate a new candidate."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        inspect_validation,
        validate_candidate,
        validate_configuration,
    )

    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    result = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert result.validation_id is not None
    bundle = semantic_project / ".agentic-ml/validations" / result.validation_id[7:]
    root = semantic_project
    if change == "input":
        (semantic_project / "uv.lock").write_text("version = 2\n")
    elif change in ("configuration", "registry"):
        (bundle / (change + ".json")).write_text("{}\n")
    elif change == "extra_member":
        (bundle / "extra").write_text("unexpected")
    elif change == "missing_member":
        (bundle / "manifest.json").unlink()
    else:
        root = tmp_path
    checked = inspect_validation(project_root=root, validation_id=result.validation_id)
    assert checked.status == "blocked" and not checked.current
    assert checked.integrity is (change == "input")
    candidate = validate_candidate(
        CandidateRequest(root, result.validation_id, "dummy_classifier", {})
    )
    assert candidate.status == "blocked" and candidate.parameters is None


@pytest.mark.parametrize("value", [0, 10])
def test_integer_candidate_includes_both_endpoints(
    semantic_project: Path, value: int
) -> None:
    """AC-02: exact integer endpoint candidates remain integers."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        validate_candidate,
        validate_configuration,
    )

    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_classifier": {
                        "fixed": {},
                        "search": {
                            "random_state": {
                                "type": "integer",
                                "min": 0,
                                "max": 10,
                                "scale": "linear",
                            }
                        },
                    }
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    config = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert config.validation_id is not None
    result = validate_candidate(
        CandidateRequest(
            semantic_project,
            config.validation_id,
            "dummy_classifier",
            {"random_state": value},
        )
    )
    assert result.status == "valid" and result.parameters is not None
    assert result.parameters["random_state"] == value
    assert type(result.parameters["random_state"]) is int


@pytest.mark.parametrize(
    "value,valid",
    [(0.1, True), (0.9, True), (0.5, True), (0.0, False), (1, False), (True, False)],
)
def test_regression_float_search_obeys_inclusive_bounds_without_coercion(
    semantic_project: Path, value: object, valid: bool
) -> None:
    """AC-01/02/03: regression defaults and continuous domains are checked."""
    from typing import cast

    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.planning.models import JSONValue
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        validate_candidate,
        validate_configuration,
    )

    brief = semantic_project / "brief.md"
    brief.write_text(
        brief.read_text()
        .replace("classification", "regression")
        .replace("dummy_classifier", "dummy_regressor")
    )
    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_regressor": {
                        "fixed": {"strategy": "quantile"},
                        "search": {
                            "quantile": {
                                "type": "float",
                                "min": 0.1,
                                "max": 0.9,
                                "scale": "logarithmic",
                            }
                        },
                    }
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    config = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert config.validation_id is not None, config.diagnostics
    result = validate_candidate(
        CandidateRequest(
            semantic_project,
            config.validation_id,
            "dummy_regressor",
            {"quantile": cast(JSONValue, value)},
        )
    )
    assert (result.status == "valid") is valid
    if valid:
        assert result.parameters == {
            "strategy": "quantile",
            "quantile": value,
            "constant": None,
        }


@pytest.mark.parametrize(
    "bad",
    [float("inf"), float("nan"), {1: "bad"}, {"nested": object()}, {"nested": 2**54}],
)
def test_python_registry_rejects_non_json_objects_without_throwing(bad: object) -> None:
    """AC-04: Python callers receive diagnostics for nonportable values."""
    from typing import cast

    from agentic_ml.validation import RegistryDocument, validate_registry

    result = validate_registry(cast(RegistryDocument, bad))
    assert result.status == "blocked" and result.registry_id is None


@pytest.mark.parametrize(
    "change",
    [
        "default_type",
        "duplicate_choices",
        "bounds_order",
        "integer_float_bounds",
        "rule_parameter",
        "unknown_field",
    ],
)
def test_registry_parameter_contract_is_checked_before_use(change: str) -> None:
    """AC-01/03: complete supported scalar metadata has no invalid defaults or rules."""
    from agentic_ml.validation import validate_registry

    spec: dict[str, JSONValue] = {
        "id": "custom",
        "interface_version": "1.0",
        "tasks": ["classification"],
        "adapter": {"id": "project_metadata", "version": "1.0"},
        "library": {
            "distribution": "nonexistent-us05-library",
            "reference_version": "1",
        },
        "parameters": {"flag": {"types": ["boolean"], "default": False}},
        "requires_non_null": [],
    }
    parameters = cast(dict[str, JSONValue], spec["parameters"])
    if change == "default_type":
        parameters["flag"] = {"types": ["boolean"], "default": 0}
    elif change == "duplicate_choices":
        parameters["flag"] = {
            "types": ["boolean"],
            "default": False,
            "choices": [False, False],
        }
    elif change == "bounds_order":
        parameters["flag"] = {
            "types": ["integer"],
            "default": 2,
            "minimum": 3,
            "maximum": 1,
        }
    elif change == "integer_float_bounds":
        parameters["flag"] = {
            "types": ["integer"],
            "default": 1,
            "minimum": 0.0,
            "maximum": 2.0,
        }
    elif change == "rule_parameter":
        spec["requires_non_null"] = [
            {"if_parameter": "missing", "equals": False, "then_parameter": "flag"}
        ]
    else:
        spec["entrypoint"] = "do_not_import:execute"
    result = validate_registry({"schema_version": "1.0", "algorithms": [spec]})
    assert result.status == "blocked" and result.registry is None


def test_explicit_metadata_preserves_typed_categories_and_missing_library(
    semantic_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-01–05: scalar registrations are additive, inert and sensitive to library drift."""
    import json

    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        inspect_validation,
        validate_candidate,
        validate_configuration,
    )

    registry: dict[str, JSONValue] = {
        "schema_version": "1.0",
        "algorithms": [
            {
                "id": "custom",
                "interface_version": "1.0",
                "tasks": ["classification"],
                "adapter": {"id": "project_metadata", "version": "1"},
                "library": {
                    "distribution": "nonexistent-us05-library",
                    "reference_version": "1",
                },
                "parameters": {
                    "choice": {
                        "types": ["null", "boolean", "integer", "float", "string"],
                        "default": None,
                    }
                },
                "requires_non_null": [],
            }
        ],
    }
    (semantic_project / "registry.json").write_text(json.dumps(registry))
    brief = semantic_project / "brief.md"
    brief.write_text(brief.read_text().replace("dummy_classifier", "custom"))
    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "custom": {
                        "fixed": {},
                        "search": {
                            "choice": {
                                "type": "categorical",
                                "choices": [None, True, 1, 1.0, "1"],
                            }
                        },
                    }
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    config = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id, Path("registry.json"))
    )
    assert config.status == "valid" and config.validation_id is not None
    assert config.configuration is not None
    assert config.configuration["libraries"] == [
        {
            "distribution": "nonexistent-us05-library",
            "reference_version": "1",
            "installed_version": None,
        }
    ]
    snapshot = {
        str(p.relative_to(semantic_project)): p.read_bytes()
        for p in semantic_project.rglob("*")
        if p.is_file()
    }
    for value in (None, True, 1, 1.0, "1"):
        result = validate_candidate(
            CandidateRequest(
                semantic_project, config.validation_id, "custom", {"choice": value}
            )
        )
        assert result.status == "valid" and result.parameters is not None
        assert type(result.parameters["choice"]) is type(value)
    assert snapshot == {
        str(p.relative_to(semantic_project)): p.read_bytes()
        for p in semantic_project.rglob("*")
        if p.is_file()
    }
    metadata = tmp_path / "site-packages" / "nonexistent_us05_library-1.0.dist-info"
    metadata.mkdir(parents=True)
    (metadata / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: nonexistent-us05-library\nVersion: 1.0\n"
    )
    monkeypatch.syspath_prepend(str(metadata.parent))
    stale = inspect_validation(
        project_root=semantic_project, validation_id=config.validation_id
    )
    assert stale.integrity and not stale.current
    assert stale.diagnostics[0].code == "stale_validation"
    renewed = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id, Path("registry.json"))
    )
    assert renewed.status == "valid" and renewed.validation_id != config.validation_id


@pytest.mark.parametrize(
    "kind", ["busy", "store_symlink", "member_symlink", "registry_symlink"]
)
def test_unsafe_or_busy_storage_cannot_publish_or_validate(
    semantic_project: Path, tmp_path: Path, kind: str
) -> None:
    """AC-04/05: no-follow storage and explicit locks fail without external writes."""
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        ConfigurationRequest,
        ValidationError,
        inspect_validation,
        validate_configuration,
    )

    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    request = ConfigurationRequest(semantic_project, plan.plan_id)
    store = semantic_project / ".agentic-ml/validations"
    outside = tmp_path / "outside"
    outside.mkdir()
    if kind == "busy":
        store.mkdir()
        (store / "validate.lock").write_text("review required")
        with pytest.raises(ValidationError, match="lock exists"):
            validate_configuration(request)
        assert (store / "validate.lock").read_text() == "review required"
    elif kind == "store_symlink":
        store.symlink_to(outside, target_is_directory=True)
        with pytest.raises(ValidationError):
            validate_configuration(request)
        assert list(outside.iterdir()) == []
    elif kind == "registry_symlink":
        (outside / "registry.json").write_text(
            '{"schema_version": "1.0", "algorithms": []}'
        )
        (semantic_project / "registry.json").symlink_to(outside / "registry.json")
        result = validate_configuration(
            ConfigurationRequest(semantic_project, plan.plan_id, Path("registry.json"))
        )
        assert (
            result.status == "blocked" and result.diagnostics[0].code == "unsafe_path"
        )
        assert not store.exists()
    else:
        result = validate_configuration(request)
        assert result.validation_id is not None
        member = store / result.validation_id[7:] / "registry.json"
        target = outside / "registry.json"
        target.write_bytes(member.read_bytes())
        member.unlink()
        member.symlink_to(target)
        checked = inspect_validation(
            project_root=semantic_project, validation_id=result.validation_id
        )
        assert checked.status == "blocked" and not checked.integrity


def test_current_delegated_approval_is_required_again_for_every_candidate(
    semantic_project: Path,
) -> None:
    """AC-04/05: revoked planning decisions block reuse of validation evidence."""
    from agentic_ml.approvals import (
        ApprovalRequest,
        RevocationRequest,
        approve_plan,
        revoke_approval,
    )
    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        CandidateRequest,
        ConfigurationRequest,
        validate_candidate,
        validate_configuration,
    )

    brief = semantic_project / "brief.md"
    brief.write_text(
        brief.read_text().replace(
            "metric: f1_macro",
            "metric: {delegate: choose metric, proposal: f1_macro, rationale: task metric}",
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None and plan.status == "blocked"
    request = ConfigurationRequest(semantic_project, plan.plan_id)
    blocked = validate_configuration(request)
    assert blocked.status == "blocked"
    approved = approve_plan(
        ApprovalRequest(semantic_project, plan.plan_id, "developer", "approve metric")
    )
    result = validate_configuration(request)
    assert result.status == "valid" and result.validation_id is not None
    revoke_approval(
        RevocationRequest(
            semantic_project,
            plan.plan_id,
            approved.approval_id,
            "developer",
            "withdraw metric",
        )
    )
    candidate = validate_candidate(
        CandidateRequest(semantic_project, result.validation_id, "dummy_classifier", {})
    )
    assert candidate.status == "blocked" and candidate.parameters is None


def test_recomputed_checksums_do_not_hide_type_changed_fixed_value(
    semantic_project: Path,
) -> None:
    """AC-03/04: semantic replay preserves the exact type of fixed values."""
    import hashlib
    import json

    from agentic_ml.planning import ResolveRequest, resolve_plan
    from agentic_ml.validation import (
        ConfigurationRequest,
        inspect_validation,
        validate_configuration,
    )

    # Both scalar types are registered; only the preserved integer was selected.
    (semantic_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "dummy_classifier": {"fixed": {"constant": 1}, "search": {}}
                },
            }
        )
    )
    plan = resolve_plan(ResolveRequest(semantic_project, Path("experiment.yaml")))
    assert plan.plan_id is not None
    result = validate_configuration(
        ConfigurationRequest(semantic_project, plan.plan_id)
    )
    assert result.validation_id is not None
    original = semantic_project / ".agentic-ml/validations" / result.validation_id[7:]
    config = json.loads((original / "configuration.json").read_bytes())
    config["algorithms"]["dummy_classifier"]["fixed"]["constant"] = 1.0
    encoded = (
        json.dumps(
            config,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()
    changed_id = "sha256:" + hashlib.sha256(encoded).hexdigest()
    changed = original.parent / changed_id[7:]
    changed.mkdir()
    (changed / "configuration.json").write_bytes(encoded)
    (changed / "registry.json").write_bytes((original / "registry.json").read_bytes())
    manifest = json.loads((original / "manifest.json").read_bytes())
    manifest["validation_id"] = changed_id
    manifest["files"]["configuration.json"] = hashlib.sha256(encoded).hexdigest()
    (changed / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    )
    checked = inspect_validation(
        project_root=semantic_project, validation_id=changed_id
    )
    assert checked.status == "blocked" and not checked.current
