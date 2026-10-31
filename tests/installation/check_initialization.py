"""Independently inspect initialized installed projects outside the checkout."""

import argparse
import importlib
import json
import subprocess
import sys
import tomllib
from importlib.metadata import distribution
from pathlib import Path
from zipfile import ZipFile


def main() -> None:
    """Verify initialization inventory, authority, package identity and stores."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("project", "package", "repository", "revision", "wheel"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    root = Path(args.project).resolve()
    assert Path(sys.prefix).resolve() == root / ".venv"
    installed = distribution("agentic-ml")
    origin = json.loads(installed.read_text("direct_url.json") or "{}")
    assert origin["url"] == args.repository
    assert origin["vcs_info"]["commit_id"] == args.revision
    assert not origin.get("dir_info", {}).get("editable")
    with ZipFile(args.wheel) as archive:
        for name in archive.namelist():
            if name.startswith("agentic_ml/") and not name.endswith("/"):
                assert Path(
                    str(installed.locate_file(name))
                ).read_bytes() == archive.read(name), name
    metadata = tomllib.loads((root / "pyproject.toml").read_text())
    assert metadata["tool"]["uv"]["sources"]["agentic-ml"] == {
        "git": args.repository,
        "rev": args.revision,
    }
    for name in (
        "numpy",
        "pandas",
        "sklearn",
        "nbclient",
        "ipykernel",
        "nbformat",
        "dvc",
        "mlflow",
        args.package,
    ):
        module = importlib.import_module(name)
        assert module.__file__ is not None
    project_module = importlib.import_module(args.package)
    assert project_module.__file__ is not None
    assert Path(project_module.__file__).resolve().is_relative_to(root / "src")
    if args.package == "custom":
        assert project_module.VALUE == 42
    config = importlib.import_module("yaml").safe_load(
        (root / "project.yaml").read_text()
    )
    assert config["setup"] == {
        "data_access": "unconfigured",
        "agent": "unconfigured",
        "approval_presentation": "unconfigured",
    }
    assert config["storage"] == {
        "dvc_store": ".agentic-ml/dvc-store",
        "mlflow_backend": ".agentic-ml/mlflow.db",
        "artifacts": ".agentic-ml/artifacts",
        "state": ".agentic-ml/state",
    }
    assert config["guidance"] == {} and config["components"] == {}
    expected = {
        "01_data_assessment.ipynb",
        "02_features_and_baseline.ipynb",
        "03_model_development.ipynb",
        "04_results.ipynb",
    }
    notebooks = root / "experiments/initial/notebooks"
    assert {path.name for path in notebooks.iterdir()} == expected
    for path in notebooks.iterdir():
        document = json.loads(path.read_text())
        importlib.import_module("nbformat").validate(
            importlib.import_module("nbformat").read(path, as_version=4)
        )
        for cell in document["cells"]:
            if cell["cell_type"] == "code":
                assert cell["outputs"] == [] and cell["execution_count"] is None
    assert json.loads((root / ".agentic-ml/state/project.json").read_text()) == {
        "schema_version": "0.1",
        "experiment": "initial",
        "status": "unconfigured",
        "approvals": [],
        "runs": [],
    }
    journal = json.loads((root / ".agentic-ml/init.json").read_text())
    assert journal["status"] == "complete" and journal["pending_steps"] == []
    client = importlib.import_module("mlflow").MlflowClient(
        tracking_uri="sqlite:///" + str(root / ".agentic-ml/mlflow.db")
    )
    experiment = client.get_experiment_by_name("agentic-ml:initial")
    assert experiment is not None
    assert experiment.artifact_location == (root / ".agentic-ml/artifacts").as_uri()
    assert client.search_runs([experiment.experiment_id]) == []
    for command in (
        [str(root / ".venv/bin/dvc"), "root"],
        [str(root / ".venv/bin/dvc"), "config", "core.remote"],
        ["uv", "lock", "--check"],
    ):
        result = subprocess.run(
            command, cwd=root, capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, result.stderr
        if command[-1] == "core.remote":
            assert result.stdout.strip() == "agentic-ml-store"
    assert (root / ".env").read_text() == "TOKEN=sentinel-secret\n"
    assert (root / "data/raw.csv").read_text() == "private sentinel dataset\n"
    for name in (
        ".env",
        "data/raw.csv",
        ".venv/bin/python",
        ".agentic-ml/mlflow.db",
        ".agentic-ml/state/project.json",
        ".dvc/cache/probe",
    ):
        ignored = subprocess.run(
            ["git", "check-ignore", "--no-index", name],
            cwd=root,
            capture_output=True,
            check=False,
        )
        assert ignored.returncode == 0, name
    for name in (
        "project.yaml",
        "uv.lock",
        ".dvc/config",
        "experiments/initial/experiment.md",
        f"src/{args.package}/__init__.py",
    ):
        visible = subprocess.run(
            ["git", "check-ignore", "--no-index", name],
            cwd=root,
            capture_output=True,
            check=False,
        )
        assert visible.returncode == 1, name
    assert not (root / "AGENTS.md").exists()
    print("PASS complete installed initialization", flush=True)


if __name__ == "__main__":
    main()
