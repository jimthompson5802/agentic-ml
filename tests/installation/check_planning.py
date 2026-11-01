"""Probe installed US-03 interfaces in an independent experiment project."""

import argparse
import hashlib
import json
import subprocess
import sys
from importlib.resources import files
from pathlib import Path
from typing import cast

import yaml

import agentic_ml
from agentic_ml.planning import (
    ResolveRequest,
    SearchSelection,
    inspect_plan,
    resolve_plan,
    validate_boundaries,
    verify_plan,
)
from agentic_ml.planning.models import JSONValue


def create_project(tmp_path: Path, project_root: Path | None = None) -> Path:
    """Write controlled declarative inputs with an unread dataset and notebook."""
    root = (
        project_root if project_root is not None else tmp_path / "project with spaces"
    )
    if project_root is None:
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


def check_boundaries(root: Path, workspace: Path) -> None:
    """Check IP3 success and adversarial selections through installed interfaces."""
    search_path, config_path = root / "search.yaml", root / "experiment.yaml"
    search_original, config_original = (
        search_path.read_bytes(),
        config_path.read_bytes(),
    )
    declared: dict[str, JSONValue] = {
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
            },
            "other": {"fixed": {}, "search": {}},
        },
    }
    accepted = validate_boundaries(
        declared,
        SearchSelection(
            mode="use",
            allowed=["logistic_regression"],
            execution={"parameters": {"logistic_regression": {"C": 10}}},
        ),
    )
    assert not accepted.diagnostics and accepted.effective_search is not None
    rejected = validate_boundaries(
        declared,
        SearchSelection(
            mode="use",
            allowed=["logistic_regression"],
            execution={"parameters": {"logistic_regression": {"C": 10.01}}},
        ),
    )
    assert rejected.effective_search is None and rejected.diagnostics
    search_path.write_text(yaml.safe_dump(declared))
    cli = str(Path(sys.executable).parent / "agentic-ml")
    # Independently chosen endpoints, expansions, unknown names and type changes.
    cases: list[tuple[dict[str, JSONValue], bool]] = [
        ({}, True),
        (
            {
                "parameters": {
                    "logistic_regression": {"C": 0.1, "count": 1, "kind": None}
                }
            },
            True,
        ),
        (
            {
                "parameters": {
                    "logistic_regression": {"C": 10, "count": 10, "kind": 1.0}
                }
            },
            True,
        ),
        ({"parameters": {"logistic_regression": {"seed": 42.0}}}, False),
        ({"parameters": {"logistic_regression": {"C": 10.01}}}, False),
        ({"parameters": {"logistic_regression": {"C": True}}}, False),
        ({"parameters": {"logistic_regression": {"count": 1.0}}}, False),
        ({"parameters": {"logistic_regression": {"new": 1}}}, False),
        ({"parameters": {"other": {}}}, False),
        ({"algorithm_subset": ["other"]}, False),
        (
            {
                "search_overrides": {
                    "logistic_regression": {
                        "C": {
                            "type": "float",
                            "min": 1,
                            "max": 2,
                            "scale": "logarithmic",
                        }
                    }
                }
            },
            True,
        ),
        (
            {
                "search_overrides": {
                    "logistic_regression": {
                        "C": {
                            "type": "float",
                            "min": 0.01,
                            "max": 2,
                            "scale": "logarithmic",
                        }
                    }
                }
            },
            False,
        ),
        (
            {
                "search_overrides": {
                    "logistic_regression": {
                        "kind": {"type": "categorical", "choices": [False]}
                    }
                }
            },
            False,
        ),
        ({"budget_overrides": {"max_runtime_seconds": 30}}, True),
        ({"budget_overrides": {"max_runtime_seconds": 61}}, False),
        ({"budget_overrides": {"max_memory_mb": 1}}, False),
    ]
    baseline_id = None
    for overrides, ready in cases:
        config = yaml.safe_load(config_original)
        config["execution"].update(overrides)
        config_path.write_text(yaml.safe_dump(config))
        result = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
        assert result.status == ("input_ready" if ready else "blocked"), result
        completed = subprocess.run(
            [
                cli,
                "plan",
                "resolve",
                "--project-root",
                str(root),
                "--experiment",
                "experiment.yaml",
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == (0 if ready else 2), (
            completed.stdout + completed.stderr
        )
        response = json.loads(completed.stdout)
        assert response["plan_id"] == result.plan_id
        if ready:
            assert result.plan_id is not None
            assert verify_plan(project_root=root, plan_id=result.plan_id).integrity
            plan = inspect_plan(project_root=root, plan_id=result.plan_id).plan
            assert plan is not None and plan["declared_search"] == declared
            if not overrides:
                baseline_id = result.plan_id
                assert plan["effective_search"] == {
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
        else:
            assert result.plan_id is None
            assert response["diagnostics"][0]["code"] == result.diagnostics[0].code
    assert baseline_id is not None
    assert verify_plan(project_root=root, plan_id=baseline_id).integrity
    search_path.write_bytes(search_original)
    config_path.write_bytes(config_original)
    print("PASS installed boundaries (16 CLI/API cases and public checker)", flush=True)


def main() -> None:
    """Exercise installed CLI/API, preservation and blocking without source imports."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--project", type=Path)
    args = parser.parse_args()
    assert agentic_ml.__file__ is not None
    assert (
        Path(agentic_ml.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    )
    args.workspace.mkdir()
    root = create_project(args.workspace, args.project)
    (root / "missing.csv").write_bytes(b"Private dataset sentinel")
    (root / "missing.csv").chmod(0)
    root_bytes = {
        name: (root / name).read_bytes()
        for name in ("pyproject.toml", "uv.lock", "project.yaml", "notebook.ipynb")
    }
    drafts = root / "experiments/initial"
    drafts.mkdir(parents=True, exist_ok=True)
    if args.project is None:
        for name in ("experiment.md", "search-space.yaml", "experiment.yaml"):
            (drafts / name).write_bytes(
                files("agentic_ml")
                .joinpath("templates/initialization/" + name)
                .read_bytes()
            )
    draft_bytes = {
        path.name: path.read_bytes() for path in drafts.iterdir() if path.is_file()
    }
    result = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert result.status == "input_ready", result
    assert result.plan_id is not None
    bundle = root / ".agentic-ml/plans" / result.plan_id[7:]
    assert (
        hashlib.sha256((bundle / "plan.json").read_bytes()).hexdigest()
        == result.plan_id[7:]
    )
    for item in json.loads((bundle / "manifest.json").read_bytes())["files"]:
        preserved = (bundle / item["path"]).read_bytes()
        assert len(preserved) == item["length"]
        assert hashlib.sha256(preserved).hexdigest() == item["sha256"]
    inspection = inspect_plan(project_root=root, plan_id=result.plan_id)
    assert inspection.integrity and inspection.plan is not None
    effective = inspection.plan["effective"]
    assert isinstance(effective, dict)
    evaluation = effective["evaluation"]
    assert isinstance(evaluation, dict)
    assert evaluation["metric"] == "f1_macro"
    cli = str(Path(sys.executable).parent / "agentic-ml")

    def command(arguments: list[str], expected: int, cwd: Path) -> dict[str, JSONValue]:
        completed = subprocess.run(
            [cli, "plan", *arguments],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == expected, completed.stdout + completed.stderr
        return cast(dict[str, JSONValue], json.loads(completed.stdout))

    for cwd in (root, drafts, args.workspace):
        captured = command(
            ["resolve", "--project-root", str(root), "--experiment", "experiment.yaml"],
            0,
            cwd,
        )
        assert captured["plan_id"] == result.plan_id
    assert command(
        ["inspect", "--project-root", str(root), "--plan", result.plan_id],
        0,
        args.workspace,
    )["integrity"]
    assert (
        command(["resolve", "--experiment", "experiment.yaml"], 0, drafts)["plan_id"]
        == result.plan_id
    )
    check_boundaries(root, args.workspace)
    brief = root / "brief.md"
    original = brief.read_bytes()
    for task, mode in (
        ("classification", "use"),
        ("regression", "select"),
        ("classification", "compare"),
    ):
        brief.write_bytes(
            original.replace(
                b"task_type: classification", b"task_type: " + task.encode()
            ).replace(b"mode: use", b"mode: " + mode.encode())
        )
        changed = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
        assert changed.status == "input_ready", changed
        assert changed.plan_id is not None
        assert (
            verify_plan(
                project_root=root, plan_id=changed.plan_id, check_current=True
            ).status
            == "input_ready"
        )
    brief.write_bytes(
        original.replace(
            b"metric: f1_macro",
            b'metric: {delegate: "Choose metric", proposal: f1_macro, rationale: "Class balance"}',
        )
    )
    proposed = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert proposed.status == "blocked" and proposed.plan_id is not None
    assert verify_plan(project_root=root, plan_id=proposed.plan_id).status == "blocked"
    command(
        ["verify", "--project-root", str(root), "--plan", proposed.plan_id],
        2,
        args.workspace,
    )
    from agentic_ml.approvals import (
        ApprovalRequest,
        RevocationRequest,
        approve_plan,
        revoke_approval,
    )

    approval = approve_plan(
        ApprovalRequest(root, proposed.plan_id, "Scientist", "Reviewed metric")
    )
    assert approval.authentication == "none"
    assert approval.decisions == (
        {
            "field": "evaluation.metric",
            "value": "f1_macro",
            "rationale": "Class balance",
        },
    )
    verified = command(
        ["verify", "--project-root", str(root), "--plan", proposed.plan_id],
        0,
        args.workspace,
    )
    assert verified["authentication"] == "none" and verified["approval_ids"] == [
        approval.approval_id
    ]
    revoke_approval(
        RevocationRequest(
            root, proposed.plan_id, approval.approval_id, "Scientist", "Reconsider"
        )
    )
    assert verify_plan(project_root=root, plan_id=proposed.plan_id).status == "blocked"
    cli_approval = command(
        [
            "approve",
            "--project-root",
            str(root),
            "--plan",
            proposed.plan_id,
            "--reviewer",
            "Self-declared scientist",
            "--reason",
            "Reviewed",
        ],
        0,
        args.workspace,
    )
    assert cli_approval["authentication"] == "none"
    command(
        [
            "revoke-approval",
            "--project-root",
            str(root),
            "--plan",
            proposed.plan_id,
            "--approval",
            str(cli_approval["approval_id"]),
            "--reviewer",
            "Scientist",
            "--reason",
            "Reconsider",
        ],
        0,
        args.workspace,
    )
    command(
        ["verify", "--project-root", str(root), "--plan", proposed.plan_id],
        2,
        args.workspace,
    )
    record_dir = root / ".agentic-ml/plan-approvals" / proposed.plan_id[7:]
    record_path = record_dir / "approvals" / (approval.approval_id + ".json")
    saved_record = record_path.read_bytes()
    for key, value in (
        ("project_root", "/other"),
        ("experiment_id", "other"),
        ("plan_id", "sha256:" + "0" * 64),
        ("recorded_at", "2026-02-30T00:00:00Z"),
        ("decisions", []),
        ("extra", True),
    ):
        payload = json.loads(saved_record)
        payload[key] = value
        record_path.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
        )
        checked = verify_plan(project_root=root, plan_id=proposed.plan_id)
        assert (
            checked.status == "blocked"
            and checked.diagnostics[0].code == "invalid_approval"
        )
        command(
            ["verify", "--project-root", str(root), "--plan", proposed.plan_id],
            2,
            args.workspace,
        )
        record_path.write_bytes(saved_record)
    fresh = approve_plan(
        ApprovalRequest(root, proposed.plan_id, "Scientist", "Reviewed again")
    )
    assert verify_plan(project_root=root, plan_id=proposed.plan_id).approval_ids == (
        fresh.approval_id,
    )
    # A new source identity cannot reuse old records, while the old bundle remains inspectable.
    brief.write_bytes(
        brief.read_bytes().replace(b"proposal: f1_macro", b"proposal: accuracy")
    )
    revised = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert revised.plan_id != proposed.plan_id and revised.status == "blocked"
    assert (
        verify_plan(project_root=root, plan_id=proposed.plan_id).status == "input_ready"
    )
    assert (
        verify_plan(
            project_root=root, plan_id=proposed.plan_id, check_current=True
        ).status
        == "blocked"
    )
    brief.write_bytes(original.replace(b"metric: f1_macro", b"metric: TODO"))
    invalid = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert invalid.status == "blocked" and invalid.plan_id is None
    response = command(
        ["resolve", "--project-root", str(root), "--experiment", "experiment.yaml"],
        2,
        args.workspace,
    )
    diagnostics = response["diagnostics"]
    assert isinstance(diagnostics, list)
    first_diagnostic = diagnostics[0]
    assert isinstance(first_diagnostic, dict)
    assert first_diagnostic["source_path"] == "brief.md"
    assert (
        verify_plan(project_root=root, plan_id=result.plan_id).status == "input_ready"
    )
    stale = verify_plan(project_root=root, plan_id=result.plan_id, check_current=True)
    assert stale.status == "blocked" and stale.diagnostics[0].code == "stale_source"
    (bundle / "sources/experiment.md").write_bytes(b"corrupt")
    assert not verify_plan(project_root=root, plan_id=result.plan_id).integrity
    for name, content in root_bytes.items():
        assert (root / name).read_bytes() == content
    assert {
        path.name: path.read_bytes() for path in drafts.iterdir() if path.is_file()
    } == draft_bytes
    if args.project is None:
        assert not (root / ".agentic-ml/init.json").exists()
    (root / "missing.csv").chmod(0o600)
    print("PASS installed planning", flush=True)


if __name__ == "__main__":
    main()
