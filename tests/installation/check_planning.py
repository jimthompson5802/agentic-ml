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
from agentic_ml.planning import ResolveRequest, inspect_plan, resolve_plan, verify_plan
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
