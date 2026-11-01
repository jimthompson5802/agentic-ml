"""Verify US-03 input resolution through public planning interfaces."""

import json
from pathlib import Path

import pytest
import yaml

from agentic_ml.planning import ResolveRequest, resolve_plan
from agentic_ml.planning.models import JSONValue


@pytest.mark.parametrize(
    "mode,subset,ready",
    [
        ("use", ["logistic_regression"], True),
        ("compare", ["logistic_regression"], False),
        ("compare", ["logistic_regression", "other"], True),
        ("select", ["logistic_regression"], True),
        ("select", ["outside"], False),
    ],
)
def test_algorithm_selection_obeys_brief_mode(
    planning_project: Path, mode: str, subset: list[str], ready: bool
) -> None:
    """AC-01/02/04: only select mode permits dropping an allowed member."""
    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text()
        .replace("mode: use", "mode: " + mode)
        .replace(
            "- logistic_regression",
            "- logistic_regression\n- other"
            if mode != "use"
            else "- logistic_regression",
        )
    )
    (planning_project / "search.yaml").write_text(
        'schema_version: "1.0"\nalgorithms:\n  logistic_regression: {fixed: {}, search: {}}\n  other: {fixed: {}, search: {}}\n'
    )
    config_path = planning_project / "experiment.yaml"
    config = yaml.safe_load(config_path.read_bytes())
    config["execution"]["algorithm_subset"] = subset
    config_path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == ("input_ready" if ready else "blocked")
    if ready:
        from agentic_ml.planning import inspect_plan, verify_plan

        assert result.plan_id is not None
        plan = inspect_plan(project_root=planning_project, plan_id=result.plan_id).plan
        assert plan is not None
        effective = plan["effective_search"]
        assert isinstance(effective, dict)
        algorithms = effective["algorithms"]
        assert isinstance(algorithms, dict)
        assert list(algorithms) == sorted(subset)
        effective_decisions = plan["effective"]
        assert isinstance(effective_decisions, dict)
        algorithm_decisions = effective_decisions["algorithms"]
        assert isinstance(algorithm_decisions, dict)
        allowed = algorithm_decisions["allowed"]
        assert isinstance(allowed, list)
        assert sorted(str(name) for name in allowed) == sorted(subset)
        assert verify_plan(
            project_root=planning_project, plan_id=result.plan_id
        ).integrity
    else:
        assert result.plan_id is None
        assert result.diagnostics[0].field == "execution.algorithm_subset"


def test_resolution_preserves_declared_and_narrows_effective_space(
    planning_project: Path,
) -> None:
    """AC-02/03: selections fix allowed values and retain omitted tunables."""
    from agentic_ml.planning import inspect_plan, verify_plan

    declared = {
        "schema_version": "1.0",
        "algorithms": {
            "logistic_regression": {
                "fixed": {"seed": 42},
                "search": {
                    "C": {
                        "type": "float",
                        "min": 0.1,
                        "max": 10,
                        "scale": "logarithmic",
                    },
                    "count": {
                        "type": "integer",
                        "min": 1,
                        "max": 10,
                        "scale": "linear",
                    },
                    "kind": {
                        "type": "categorical",
                        "choices": [None, True, 1, 1.0, "1"],
                    },
                },
            }
        },
    }
    (planning_project / "search.yaml").write_text(yaml.safe_dump(declared))
    path = planning_project / "experiment.yaml"
    original = path.read_bytes()
    config = yaml.safe_load(original)
    config["execution"]["parameters"] = {"logistic_regression": {"C": 0.1, "seed": 42}}
    config["execution"]["search_overrides"] = {
        "logistic_regression": {
            "count": {"type": "integer", "min": 2, "max": 10, "scale": "linear"},
            "kind": {"type": "categorical", "choices": [True, 1.0]},
        }
    }
    before = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert before.plan_id is not None
    path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "input_ready"
    assert result.plan_id is not None and result.plan_id != before.plan_id
    plan = inspect_plan(project_root=planning_project, plan_id=result.plan_id).plan
    assert plan is not None
    assert plan["declared_search"] == declared
    assert plan["effective_search"] == {
        "schema_version": "1.0",
        "algorithms": {
            "logistic_regression": {
                "fixed": {"seed": 42, "C": 0.1},
                "search": {
                    "count": {
                        "type": "integer",
                        "min": 2,
                        "max": 10,
                        "scale": "linear",
                    },
                    "kind": {"type": "categorical", "choices": [True, 1.0]},
                },
            }
        },
    }
    assert verify_plan(project_root=planning_project, plan_id=result.plan_id).integrity
    assert verify_plan(project_root=planning_project, plan_id=before.plan_id).integrity


@pytest.mark.parametrize(
    "section,parameter,value",
    [
        ("parameters", "seed", 43),
        ("parameters", "seed", 42.0),
        ("parameters", "new", 1),
        ("parameters", "C", 0.09),
        ("parameters", "C", 10.01),
        ("parameters", "C", True),
        ("parameters", "count", 1.0),
        ("parameters", "kind", 1),
        ("search_overrides", "seed", {"type": "categorical", "choices": [42]}),
        ("search_overrides", "new", {"type": "categorical", "choices": [1]}),
        ("search_overrides", "kind", {"type": "categorical", "choices": [True, 1]}),
        (
            "search_overrides",
            "C",
            {"type": "float", "min": 0.01, "max": 10, "scale": "logarithmic"},
        ),
        (
            "search_overrides",
            "C",
            {"type": "float", "min": 0.1, "max": 11, "scale": "logarithmic"},
        ),
        (
            "search_overrides",
            "C",
            {"type": "float", "min": 0.1, "max": 10, "scale": "linear"},
        ),
        (
            "search_overrides",
            "count",
            {"type": "float", "min": 1, "max": 10, "scale": "linear"},
        ),
        (
            "search_overrides",
            "count",
            {"type": "integer", "min": 5, "max": 1, "scale": "linear"},
        ),
    ],
)
def test_execution_cannot_widen_parameter_boundaries(
    planning_project: Path, section: str, parameter: str, value: JSONValue
) -> None:
    """AC-02/04: reject fixed changes, unknown names and domain expansions."""
    (planning_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "logistic_regression": {
                        "fixed": {"seed": 42},
                        "search": {
                            "C": {
                                "type": "float",
                                "min": 0.1,
                                "max": 10,
                                "scale": "logarithmic",
                            },
                            "count": {
                                "type": "integer",
                                "min": 1,
                                "max": 10,
                                "scale": "linear",
                            },
                            "kind": {
                                "type": "categorical",
                                "choices": [True, "1", None],
                            },
                        },
                    }
                },
            }
        )
    )
    path = planning_project / "experiment.yaml"
    config = yaml.safe_load(path.read_bytes())
    config["execution"][section] = {"logistic_regression": {parameter: value}}
    path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics[0].code == "invalid_boundary"
    assert (
        result.diagnostics[0].field
        == f"execution.{section}.logistic_regression.{parameter}"
    )
    assert result.diagnostics[0].source_path == "experiment.yaml"
    assert result.diagnostics[0].line is not None


@pytest.mark.parametrize(
    "override,ready",
    [
        ({"max_runtime_seconds": 30}, True),
        ({"max_runtime_seconds": 60, "max_total_trials": 1}, True),
        ({"max_runtime_seconds": 61}, False),
        ({"max_memory_mb": 10}, False),
        ({"max_cost": 1.0}, False),
        ({"max_runtime_seconds": None}, False),
    ],
)
def test_execution_budget_only_lowers_explicit_ceiling(
    planning_project: Path, override: dict[str, JSONValue], ready: bool
) -> None:
    """AC-01/04: execution cannot invent, remove or increase budget authority."""
    from agentic_ml.planning import inspect_plan

    path = planning_project / "experiment.yaml"
    config = yaml.safe_load(path.read_bytes())
    config["execution"]["budget_overrides"] = override
    path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == ("input_ready" if ready else "blocked")
    if ready:
        assert result.plan_id is not None
        plan = inspect_plan(project_root=planning_project, plan_id=result.plan_id).plan
        assert plan is not None
        effective = plan["effective"]
        assert isinstance(effective, dict)
        budget = effective["budget"]
        assert isinstance(budget, dict)
        for key, value in override.items():
            assert budget[key] == value
        decisions = plan["decisions"]
        assert isinstance(decisions, list)
        assert any(
            isinstance(item, dict)
            and item["field"] == "execution.budget_overrides"
            and item["origin"] == "explicit"
            and item["effective"] == override
            for item in decisions
        )
        defaults = plan["defaults"]
        assert isinstance(defaults, list)
        assert not any(
            isinstance(item, dict) and item["field"] == "execution.budget_overrides"
            for item in defaults
        )
    else:
        assert result.plan_id is None
        assert result.diagnostics[0].source_path == "experiment.yaml"


@pytest.mark.parametrize(
    "execution",
    [
        {"unknown": True},
        {"parameters": {"outside": {"C": 1}}},
        {"parameters": {"model": {"C": []}}},
        {"parameters": []},
        {"search_overrides": {"model": {"C": {"type": "categorical", "choices": []}}}},
        {"budget_overrides": {"currency": 1}},
        {"budget_overrides": {"max_runtime_seconds": True}},
        {"budget_overrides": {"max_total_trials": 1.5}},
        {"algorithm_subset": []},
    ],
)
def test_public_checker_rejects_invalid_execution_shape(
    execution: dict[str, JSONValue],
) -> None:
    """AC-02/04: direct Python use cannot bypass execution shape validation."""
    from agentic_ml.planning import SearchSelection, validate_boundaries

    declared: dict[str, JSONValue] = {
        "schema_version": "1.0",
        "algorithms": {
            "model": {
                "fixed": {},
                "search": {
                    "C": {"type": "float", "min": 0.1, "max": 1, "scale": "linear"}
                },
            }
        },
    }
    result = validate_boundaries(
        declared,
        SearchSelection(
            mode="use",
            allowed=["model"],
            execution=execution,
            budgets={"max_total_trials": 2, "max_runtime_seconds": 60},
        ),
    )
    assert result.effective_search is None
    assert result.diagnostics
    assert result.diagnostics[0].source_path == "experiment.yaml"


@pytest.mark.parametrize("value", [float("inf"), float("nan"), 9007199254740992])
def test_public_checker_rejects_non_json_fixed_values(value: JSONValue) -> None:
    """AC-02: direct checker applies the parser's finite numeric contract."""
    from agentic_ml.planning import SearchSelection, validate_boundaries

    declared: dict[str, JSONValue] = {
        "schema_version": "1.0",
        "algorithms": {"model": {"fixed": {"seed": value}, "search": {}}},
    }
    result = validate_boundaries(declared, SearchSelection())
    assert result.effective_search is None
    assert result.diagnostics[0].field == "algorithms.model.fixed.seed"


def test_public_checker_preserves_type_distinct_categories() -> None:
    """AC-02: public structural checking accepts distinct JSON scalar types."""
    from agentic_ml.planning import SearchSelection, validate_boundaries

    declared: dict[str, JSONValue] = {
        "schema_version": "1.0",
        "algorithms": {
            "model": {
                "fixed": {"seed": 42},
                "search": {
                    "choice": {
                        "type": "categorical",
                        "choices": [None, True, 1, 1.0, "1"],
                    },
                    "count": {"type": "integer", "min": 1, "max": 1, "scale": "linear"},
                    "rate": {
                        "type": "float",
                        "min": 1,
                        "max": 2.5,
                        "scale": "logarithmic",
                    },
                },
            }
        },
    }
    result = validate_boundaries(declared, SearchSelection())
    assert result.diagnostics == ()
    assert result.effective_search == declared
    assert result.effective_search is not declared
    invalid = validate_boundaries(
        {"schema_version": "1.0", "algorithms": {}}, SearchSelection()
    )
    assert invalid.effective_search is None
    assert invalid.diagnostics[0].source_path == "search-space.yaml"


@pytest.mark.parametrize(
    "space",
    [
        {},
        {"type": "categorical", "choices": []},
        {"type": "categorical", "choices": [1, 1]},
        {"type": "categorical", "choices": [[1]]},
        {"type": "categorical", "choices": [1], "extra": True},
        {"type": "integer", "min": 2, "max": 1, "scale": "linear"},
        {"type": "integer", "min": 1.0, "max": 2, "scale": "linear"},
        {"type": "integer", "min": True, "max": 2, "scale": "linear"},
        {"type": "float", "min": False, "max": 2, "scale": "linear"},
        {"type": "float", "min": 1, "max": 2, "scale": "unknown"},
        {"type": "float", "min": 0, "max": 2, "scale": "logarithmic"},
        {"type": "integer", "min": -1, "max": 2, "scale": "logarithmic"},
        {"type": "float", "min": 1, "max": float("inf"), "scale": "linear"},
        {"type": "float", "min": 1, "max": float("nan"), "scale": "linear"},
        {"type": "float", "min": 1, "max": 2},
        {"type": "conditional", "choices": [1]},
    ],
)
def test_invalid_search_definitions_block(
    planning_project: Path, space: JSONValue
) -> None:
    """AC-02/04: malformed tuning domains cannot produce a usable plan."""
    (planning_project / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    "logistic_regression": {"fixed": {}, "search": {"C": space}}
                },
            }
        )
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics[0].source_path == "search.yaml"
    assert "algorithms.logistic_regression.search.C" in result.diagnostics[0].field


def test_fixed_parameter_cannot_also_be_tunable(planning_project: Path) -> None:
    """AC-02/04: declared fixed/search overlap blocks with parameter location."""
    (planning_project / "search.yaml").write_text(
        'schema_version: "1.0"\nalgorithms:\n  logistic_regression:\n'
        "    fixed: {seed: 42}\n"
        "    search:\n      seed: {type: integer, min: 1, max: 100, scale: linear}\n"
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    diagnostic = result.diagnostics[0]
    assert diagnostic.code == "invalid_boundary"
    assert diagnostic.field == "algorithms.logistic_regression.search.seed"
    assert diagnostic.source_path == "search.yaml"
    assert diagnostic.line == 6


@pytest.fixture
def planning_project(tmp_path: Path) -> Path:
    """Create separate declarative inputs without datasets or executable code."""
    root = tmp_path / "project with spaces"
    root.mkdir()
    (root / ".git").mkdir()
    (root / "project.yaml").write_text(
        'schema_version: "0.1"\nproject: {package: experiment, environment: .venv}\n'
        "storage: {dvc_store: .agentic-ml/dvc-store, mlflow_backend: .agentic-ml/mlflow.db, artifacts: .agentic-ml/artifacts, state: .agentic-ml/state}\n"
        "setup: {data_access: unconfigured, agent: unconfigured, approval_presentation: unconfigured}\nguidance: {}\ncomponents: {}\n"
    )
    (root / "pyproject.toml").write_text('[project]\nname="experiment"\n')
    (root / "uv.lock").write_bytes(b"version = 1\n")
    (root / "notebook.ipynb").write_bytes(b"Do not open or execute this notebook")
    sections = {
        "Objective": {"schema_version": "1.0", "objective": "Predict churn."},
        "Data": {
            "sources": ["missing.csv"],
            "target": "churn",
            "task_type": "classification",
        },
        "Features": {
            "include": ["age"],
            "exclude": ["id"],
            "guidance": "Use age.",
            "availability": "At signup.",
        },
        "Evaluation": {
            "metric": "f1_macro",
            "direction": "maximize",
            "split": {
                "strategy": "random",
                "time_column": None,
                "group_column": None,
                "validation_fraction": 0.2,
                "test_fraction": 0.2,
                "seed": 42,
                "constraints": "Independent rows.",
            },
        },
        "Algorithms": {"mode": "use", "allowed": ["logistic_regression"]},
        "Budget": {
            "max_trials_per_algorithm": 2,
            "max_total_trials": 2,
            "max_runtime_seconds": 60,
            "max_memory_mb": None,
            "max_cost": None,
            "currency": None,
        },
    }
    brief = "# Experiment: Churn\n\n" + "\n".join(
        f"## {name}\n```yaml\n{yaml.safe_dump(value, sort_keys=False)}```\n"
        for name, value in sections.items()
    )
    (root / "brief.md").write_text(brief)
    (root / "search.yaml").write_text(
        'schema_version: "1.0"\nalgorithms:\n  logistic_regression:\n    fixed: {}\n    search: {}\n'
    )
    (root / "experiment.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "id": "churn",
                "brief": "brief.md",
                "search_space": "search.yaml",
                "notebooks": ["notebook.ipynb"],
                "working_directory": ".",
                "data": ["missing.csv"],
                "execution": {"status": "configured"},
            }
        )
    )
    return root


def test_explicit_inputs_resolve_to_versioned_plan(planning_project: Path) -> None:
    """AC-01/03/05: explicit inputs resolve without reading absent data."""
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "input_ready"
    assert result.diagnostics == ()
    assert result.plan_id is not None
    bundle = (
        planning_project / ".agentic-ml/plans" / result.plan_id.removeprefix("sha256:")
    )
    plan = json.loads((bundle / "plan.json").read_bytes())
    assert plan["effective"]["evaluation"]["metric"] == "f1_macro"
    assert plan["effective"]["working_directory"] == "."
    assert plan["effective"]["data"]["task_type"] == "classification"
    assert not (planning_project / "missing.csv").exists()


@pytest.mark.parametrize(
    "original,replacement,field",
    [
        ("metric: f1_macro", "metric: TODO", "evaluation.metric"),
        ("task_type: classification", "task_type: clustering", "data.task_type"),
        ("max_total_trials: 2", "max_total_trials: true", "budget.max_total_trials"),
        ("direction: maximize", "direction: sideways", "evaluation.direction"),
        ("target: churn", "target: churn\ntarget: other", ""),
        ("## Data", "## Unknown", ""),
        (
            "objective: Predict churn.",
            "objective: Predict churn.\nunknown: true",
            "objective",
        ),
    ],
)
def test_invalid_brief_blocks_with_source_diagnostic(
    planning_project: Path, original: str, replacement: str, field: str
) -> None:
    """AC-01/04: unsupported and ambiguous author input never resolves."""
    brief = planning_project / "brief.md"
    brief.write_text(brief.read_text().replace(original, replacement))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics
    diagnostic = result.diagnostics[0]
    assert diagnostic.source_path == "brief.md"
    assert diagnostic.line is not None
    assert diagnostic.column is not None
    assert field in diagnostic.field


@pytest.mark.parametrize(
    "value",
    [
        '{delegate: "Choose metric"}',
        '{delegate: "Choose metric", proposal: f1_macro, rationale: "Class balance"}',
    ],
)
def test_delegations_are_preserved_and_blocked(
    planning_project: Path, value: str
) -> None:
    """AC-04: proposals are never treated as experiment approval."""
    brief = planning_project / "brief.md"
    brief.write_text(brief.read_text().replace("metric: f1_macro", "metric: " + value))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is not None
    assert result.diagnostics[0].code in {"pending_decision", "approval_required"}
    bundle = (
        planning_project / ".agentic-ml/plans" / result.plan_id.removeprefix("sha256:")
    )
    plan = json.loads((bundle / "plan.json").read_bytes())
    assert plan["pending_decisions"] == ["evaluation.metric"]
    decision = next(
        item for item in plan["decisions"] if item["field"] == "evaluation.metric"
    )
    assert decision["origin"] == "delegated"
    assert decision["line"] > 0


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("validation_fraction: 0.2", "validation_fraction: 0.9"),
        ("time_column: null", "time_column: date"),
        ("exclude:\n- id", "exclude:\n- age"),
        ("max_cost: null", "max_cost: 2"),
    ],
)
def test_inconsistent_decisions_block(
    planning_project: Path, original: str, replacement: str
) -> None:
    """AC-01/04: valid field types cannot conceal contradictory decisions."""
    brief = planning_project / "brief.md"
    assert original in brief.read_text()
    brief.write_text(brief.read_text().replace(original, replacement))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None


@pytest.mark.parametrize(
    "change",
    [
        "escape",
        "symlink",
        "notebook_symlink",
        "absolute_input",
        "bad_project",
        "draft",
        "unknown_execution",
    ],
)
def test_unsafe_or_unconfigured_project_inputs_block(
    planning_project: Path, change: str
) -> None:
    """AC-04/05: bounded configuration reads reject unsafe and draft inputs."""
    config_path = planning_project / "experiment.yaml"
    config = yaml.safe_load(config_path.read_bytes())
    if change == "escape":
        config["brief"] = "../brief.md"
    elif change == "symlink":
        (planning_project / "linked.md").symlink_to(planning_project / "brief.md")
        config["brief"] = "linked.md"
    elif change == "notebook_symlink":
        (planning_project / "linked.ipynb").symlink_to(
            planning_project / "notebook.ipynb"
        )
        config["notebooks"] = ["linked.ipynb"]
    elif change == "absolute_input":
        config["brief"] = str(planning_project / "brief.md")
    elif change == "bad_project":
        (planning_project / "project.yaml").write_text("schema_version: bad\n")
    elif change == "draft":
        config["schema_version"] = "0.1"
    else:
        config["execution"]["run_code"] = "evil.py"
    config_path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics
    assert not (planning_project / ".agentic-ml/plans").exists()


def test_capture_preserves_bytes_and_retains_old_versions(
    planning_project: Path,
) -> None:
    """AC-03: independent hashes identify exact preserved source bytes."""
    import hashlib

    before = {
        name: (planning_project / name).read_bytes()
        for name in (
            "brief.md",
            "search.yaml",
            "experiment.yaml",
            "project.yaml",
            "pyproject.toml",
            "uv.lock",
        )
    }
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None
    bundle = planning_project / ".agentic-ml/plans" / result.plan_id[7:]
    manifest = json.loads((bundle / "manifest.json").read_bytes())
    assert manifest["schema_version"] == "1.0"
    for entry in manifest["files"]:
        data = (bundle / entry["path"]).read_bytes()
        assert len(data) == entry["length"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
    for logical, source in (
        ("experiment.md", "brief.md"),
        ("search-space.yaml", "search.yaml"),
        ("experiment.yaml", "experiment.yaml"),
        ("project.yaml", "project.yaml"),
        ("pyproject.toml", "pyproject.toml"),
        ("uv.lock", "uv.lock"),
    ):
        assert (bundle / "sources" / logical).read_bytes() == before[source]
    assert (
        result.plan_id
        == "sha256:" + hashlib.sha256((bundle / "plan.json").read_bytes()).hexdigest()
    )
    assert (
        resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
        == result
    )
    original_plan = (bundle / "plan.json").read_bytes()
    brief = planning_project / "brief.md"
    brief.write_bytes(before["brief.md"] + b"\n")
    updated = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert updated.plan_id != result.plan_id
    assert (bundle / "plan.json").read_bytes() == original_plan
    assert (planning_project / "uv.lock").read_bytes() == before["uv.lock"]


def test_verification_rederives_preserved_plan_and_detects_current_drift(
    planning_project: Path,
) -> None:
    """AC-03/04: current edits cannot silently rebind a preserved plan."""
    from agentic_ml.planning import inspect_plan, verify_plan

    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None
    verified = verify_plan(project_root=planning_project, plan_id=result.plan_id)
    assert verified.status == "input_ready"
    assert verified.integrity
    inspection = inspect_plan(project_root=planning_project, plan_id=result.plan_id)
    assert inspection.integrity
    assert inspection.plan is not None
    assert inspection.plan["experiment_id"] == "churn"
    (planning_project / "brief.md").write_bytes(b"Current broken brief")
    assert (
        verify_plan(project_root=planning_project, plan_id=result.plan_id).status
        == "input_ready"
    )
    stale = verify_plan(
        project_root=planning_project, plan_id=result.plan_id, check_current=True
    )
    assert stale.status == "blocked"
    assert stale.diagnostics[0].code == "stale_source"
    bundle = planning_project / ".agentic-ml/plans" / result.plan_id[7:]
    (bundle / "sources/experiment.md").write_bytes(b"Damaged evidence")
    corrupt = verify_plan(project_root=planning_project, plan_id=result.plan_id)
    assert corrupt.status == "blocked"
    assert not corrupt.integrity
    assert corrupt.diagnostics[0].code == "corrupt_plan"


@pytest.mark.parametrize("caller", ["root", "nested", "unrelated"])
def test_cli_resolves_and_verifies_from_independent_working_directories(
    planning_project: Path, tmp_path: Path, caller: str
) -> None:
    """AC-05: cwd does not change selected root-relative input identity."""
    import subprocess
    import sysconfig

    nested = planning_project / "nested"
    nested.mkdir()
    cwd = {"root": planning_project, "nested": nested, "unrelated": tmp_path}[caller]
    cli = str(Path(sysconfig.get_path("scripts")) / "agentic-ml")
    resolved = subprocess.run(
        [
            cli,
            "plan",
            "resolve",
            "--project-root",
            str(planning_project),
            "--experiment",
            "experiment.yaml",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert resolved.returncode == 0, resolved.stderr
    output = json.loads(resolved.stdout)
    assert output["schema_version"] == "1.0"
    assert output["status"] == "input_ready"
    api = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert output["plan_id"] == api.plan_id
    verified = subprocess.run(
        [
            cli,
            "plan",
            "verify",
            "--project-root",
            str(planning_project),
            "--plan",
            output["plan_id"],
            "--check-current",
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert verified.returncode == 0, verified.stderr
    assert json.loads(verified.stdout)["integrity"] is True
    if caller != "unrelated":
        discovered = subprocess.run(
            [cli, "plan", "resolve", "--experiment", "experiment.yaml"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        assert discovered.returncode == 0, discovered.stderr
        assert json.loads(discovered.stdout)["plan_id"] == api.plan_id


def test_undeclared_parameter_cannot_be_silently_accepted(
    planning_project: Path,
) -> None:
    """AC-02/04: omission never authorizes selecting an undeclared parameter."""
    path = planning_project / "experiment.yaml"
    config = yaml.safe_load(path.read_bytes())
    config["execution"]["parameters"] = {"logistic_regression": {"C": 999}}
    path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics[0].code == "invalid_boundary"
    assert result.diagnostics[0].field == "execution.parameters.logistic_regression.C"


@pytest.mark.parametrize(
    "mutation",
    ["missing", "extra", "duplicate_manifest", "symlink", "rehash_decisions"],
)
def test_corrupt_bundles_never_verify_ready(
    planning_project: Path, mutation: str
) -> None:
    """AC-03/04: inventory and derived decisions are checked independently."""
    import hashlib

    from agentic_ml.planning import verify_plan

    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.plan_id is not None
    bundle = planning_project / ".agentic-ml/plans" / result.plan_id[7:]
    if mutation == "missing":
        (bundle / "sources/uv.lock").unlink()
    elif mutation == "extra":
        (bundle / "extra.json").write_bytes(b"{}")
    elif mutation == "duplicate_manifest":
        path = bundle / "manifest.json"
        path.write_bytes(
            path.read_bytes().replace(b'{"files":', b'{"schema_version":"1.0","files":')
        )
    elif mutation == "symlink":
        path = bundle / "sources/uv.lock"
        path.unlink()
        path.symlink_to(planning_project / "uv.lock")
    else:
        plan = json.loads((bundle / "plan.json").read_bytes())
        plan["effective"]["evaluation"]["metric"] = "fabricated_metric"
        content = (
            json.dumps(plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            + "\n"
        ).encode()
        (bundle / "plan.json").write_bytes(content)
        manifest = json.loads((bundle / "manifest.json").read_bytes())
        for entry in manifest["files"]:
            if entry["path"] == "plan.json":
                entry["length"] = len(content)
                entry["sha256"] = hashlib.sha256(content).hexdigest()
        (bundle / "manifest.json").write_bytes(
            (
                json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
            ).encode()
        )
        new_id = "sha256:" + hashlib.sha256(content).hexdigest()
        bundle.rename(bundle.with_name(new_id[7:]))
        result = type(result)(new_id, result.status, result.diagnostics)
    assert result.plan_id is not None
    verified = verify_plan(project_root=planning_project, plan_id=result.plan_id)
    assert verified.status == "blocked"
    assert not verified.integrity


def test_interrupted_storage_and_busy_lock_are_preserved(
    planning_project: Path,
) -> None:
    """AC-03: stale locks and staging need explicit operator review."""
    from agentic_ml.planning import PlanningError, verify_plan

    parent = planning_project / ".agentic-ml/plans"
    staging = parent / ".pending-interrupted"
    staging.mkdir(parents=True)
    (staging / "plan.json").write_bytes(b"partial")
    lock = parent / "resolve.lock"
    lock.write_bytes(b"operator review required")
    with pytest.raises(PlanningError) as error:
        resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert error.value.code == "plan_busy"
    assert lock.read_bytes() == b"operator review required"
    assert (staging / "plan.json").read_bytes() == b"partial"
    assert not verify_plan(
        project_root=planning_project, plan_id="sha256:" + "0" * 64
    ).integrity
    lock.unlink()  # Simulate explicit operator review and recovery.
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "input_ready"
    assert (staging / "plan.json").read_bytes() == b"partial"


def test_concurrent_resolvers_do_not_overwrite_evidence(planning_project: Path) -> None:
    """AC-03: concurrent calls either publish/reuse or return a busy lock."""
    from concurrent.futures import ThreadPoolExecutor

    from agentic_ml.planning import PlanningError, verify_plan

    def capture(_: int) -> str:
        try:
            result = resolve_plan(
                ResolveRequest(planning_project, Path("experiment.yaml"))
            )
            assert result.plan_id is not None
            return result.plan_id
        except PlanningError as error:
            assert error.code == "plan_busy"
            return "busy"

    with ThreadPoolExecutor(max_workers=4) as workers:
        outcomes = list(workers.map(capture, range(4)))
    identities = {outcome for outcome in outcomes if outcome != "busy"}
    assert len(identities) == 1
    assert (
        verify_plan(project_root=planning_project, plan_id=identities.pop()).status
        == "input_ready"
    )


@pytest.mark.parametrize(
    "task,mode",
    [
        ("classification", "use"),
        ("regression", "select"),
        ("classification", "compare"),
    ],
)
def test_explicit_task_and_algorithm_modes(
    planning_project: Path, task: str, mode: str
) -> None:
    """AC-01: task/mode are literal author decisions, with no model imports."""
    brief = planning_project / "brief.md"
    brief.write_text(
        brief.read_text()
        .replace("task_type: classification", "task_type: " + task)
        .replace("mode: use", "mode: " + mode)
    )
    assert (
        resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml"))).status
        == "input_ready"
    )


def test_external_references_and_explicit_notebook_cwd_are_recorded(
    planning_project: Path, tmp_path: Path
) -> None:
    """AC-05: external data locations confer no read access or existence claim."""
    external = str(tmp_path / "does not exist.csv")
    brief = planning_project / "brief.md"
    brief.write_text(brief.read_text().replace("missing.csv", external))
    path = planning_project / "experiment.yaml"
    config = yaml.safe_load(path.read_bytes())
    config["data"] = [external]
    config["working_directory"] = "notebook cwd"
    (planning_project / "notebook cwd").mkdir()
    path.write_text(yaml.safe_dump(config))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "input_ready"
    assert result.plan_id is not None
    bundle = planning_project / ".agentic-ml/plans" / result.plan_id[7:]
    effective = json.loads((bundle / "plan.json").read_bytes())["effective"]
    assert effective["data_references"] == [
        {"original": external, "absolute": external, "external": True}
    ]
    assert effective["working_directory"] == "notebook cwd"
    assert not Path(external).exists()


@pytest.mark.parametrize("document", ["null\n", "[]\n", "a string\n"])
def test_nonmapping_project_config_reports_validation_diagnostic(
    planning_project: Path, document: str
) -> None:
    """AC-04: malformed project configuration produces a safe public result."""
    (planning_project / "project.yaml").write_text(document)
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked"
    assert result.plan_id is None
    assert result.diagnostics[0].source_path == "project.yaml"


BRIEF_FIELDS = (
    ("Objective", "schema_version"),
    ("Objective", "objective"),
    ("Data", "sources"),
    ("Data", "target"),
    ("Data", "task_type"),
    ("Features", "include"),
    ("Features", "exclude"),
    ("Features", "guidance"),
    ("Features", "availability"),
    ("Evaluation", "metric"),
    ("Evaluation", "direction"),
    ("Evaluation", "split"),
    ("Algorithms", "mode"),
    ("Algorithms", "allowed"),
    ("Budget", "max_trials_per_algorithm"),
    ("Budget", "max_total_trials"),
    ("Budget", "max_runtime_seconds"),
    ("Budget", "max_memory_mb"),
    ("Budget", "max_cost"),
    ("Budget", "currency"),
)


@pytest.mark.parametrize("section,field", BRIEF_FIELDS)
def test_every_required_brief_field_blocks_when_missing(
    planning_project: Path, section: str, field: str
) -> None:
    """AC-01/04: no scientific decision is silently filled by a default."""
    path = planning_project / "brief.md"
    text = path.read_text()
    prefix, body = text.split("## " + section + "\n```yaml\n", 1)
    document, suffix = body.split("```", 1)
    values = yaml.safe_load(document)
    del values[field]
    path.write_text(
        prefix
        + "## "
        + section
        + "\n```yaml\n"
        + yaml.safe_dump(values, sort_keys=False)
        + "```"
        + suffix
    )
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is None
    assert result.diagnostics[0].source_path == "brief.md"
    assert result.diagnostics[0].line is not None


@pytest.mark.parametrize(
    "replacement",
    [
        b"metric: &metric f1_macro",
        b"metric: !!str f1_macro",
        b"metric: [unclosed",
        b"metric: .nan",
        b"metric: null",
        b'metric: {delegate: "Choose", proposal: f1_macro}',
        b'metric: {delegate: "Choose", rationale: "Missing proposal"}',
        b'metric: {delegate: "", proposal: f1_macro, rationale: "Empty reason"}',
    ],
)
def test_invalid_yaml_or_delegation_never_publishes(
    planning_project: Path, replacement: bytes
) -> None:
    """AC-04: strict author input rejects YAML extensions and incomplete envelopes."""
    path = planning_project / "brief.md"
    path.write_bytes(path.read_bytes().replace(b"metric: f1_macro", replacement))
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is None
    assert result.diagnostics


def test_crlf_and_notes_preserve_exact_brief_bytes(planning_project: Path) -> None:
    """AC-01/03: annotations are inert and original line endings are retained."""
    path = planning_project / "brief.md"
    content = (
        path.read_bytes()
        .replace(b"## Data\n", b"## Data\n> Note: Commentary only.\n")
        .replace(b"\n", b"\r\n")
    )
    path.write_bytes(content)
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "input_ready" and result.plan_id is not None
    bundle = planning_project / ".agentic-ml/plans" / result.plan_id[7:]
    assert (bundle / "sources/experiment.md").read_bytes() == content


@pytest.mark.parametrize(
    "kind",
    ["store_symlink", "store_file", "configured_overlap", "input_limit", "yaml_depth"],
)
def test_storage_and_input_limits_fail_before_publication(
    planning_project: Path, tmp_path: Path, kind: str
) -> None:
    """AC-03/05: invalid destinations and bounded inputs never publish a plan."""
    from agentic_ml.planning import PlanningError

    parent = planning_project / ".agentic-ml"
    if kind == "store_symlink":
        parent.symlink_to(tmp_path, target_is_directory=True)
    elif kind == "store_file":
        parent.write_bytes(b"Existing user content")
    elif kind == "configured_overlap":
        path = planning_project / "project.yaml"
        path.write_text(
            path.read_text().replace(".agentic-ml/state", ".agentic-ml/plans/state")
        )
    elif kind == "input_limit":
        (planning_project / "brief.md").write_bytes(b"a" * 1048577)
    else:
        (planning_project / "search.yaml").write_text("a: " + "[" * 30 + "0" + "]" * 30)
    if kind == "configured_overlap":
        with pytest.raises(PlanningError) as error:
            resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
        assert error.value.code == "storage_conflict"
    else:
        result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
        assert result.status == "blocked" and result.plan_id is None
    assert not (tmp_path / "plans").exists()


def test_duplicate_yaml_key_points_to_original_markdown_line(
    planning_project: Path,
) -> None:
    """AC-04: fenced YAML diagnostics locate the actual brief source line."""
    path = planning_project / "brief.md"
    content = path.read_text().replace(
        "target: churn\n", "target: churn\ntarget: duplicate\n"
    )
    path.write_text(content)
    result = resolve_plan(ResolveRequest(planning_project, Path("experiment.yaml")))
    assert result.status == "blocked" and result.plan_id is None
    diagnostic = result.diagnostics[0]
    assert diagnostic.source_path == "brief.md"
    assert diagnostic.line == content.splitlines().index("target: duplicate") + 1
    assert diagnostic.column == 1
