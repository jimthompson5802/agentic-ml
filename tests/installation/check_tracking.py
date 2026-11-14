"""Check actual producer artifacts in a normal installed experiment project."""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from importlib.metadata import distributions, version
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import mlflow.sklearn
import pandas as pd
import yaml
from mlflow import MlflowClient

import agentic_ml.preprocessing
import agentic_ml.tracking
from agentic_ml.splitting import create_partitions


def main() -> None:
    """Commit real inputs, execute the guide, and independently inspect MLflow."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    root = Path(args.project).resolve()
    assert Path(sys.prefix).resolve() == root / ".venv"
    assert not Path.cwd().is_relative_to(root)
    commands: list[dict[str, Any]] = []

    def command(*parts: str) -> str:
        result = subprocess.run(parts, cwd=root, capture_output=True, text=True)
        commands.append(
            {
                "command": parts,
                "cwd": str(root),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        (root / "native-commands.json").write_text(json.dumps(commands, indent=2))
        assert result.returncode == 0, result.stdout + result.stderr
        return result.stdout.strip()

    def ref(name: str) -> dict[str, str]:
        return {
            "path": name,
            "sha256": "sha256:"
            + hashlib.sha256((root / name).read_bytes()).hexdigest(),
        }

    command("git", "init")
    command("git", "config", "user.email", "fixture@example.invalid")
    command("git", "config", "user.name", "US-26 installed handoff")
    command(sys.executable, "-m", "dvc", "init")
    (root / ".gitignore").write_text(
        ".venv/\nfeatures.csv\nrun-provenance.json\nexecuted.ipynb\nidentity.json\nnative-commands.json\n"
    )
    (root / "data").mkdir()
    (root / "data/input.csv").write_text(
        "id,x,category,label\n0,1.0,a,A\n1,,b,B\n2,3.0,a,A\n3,100.0,unseen,B\n4,200.0,a,A\n"
    )
    frame = pd.read_csv(root / "data/input.csv")
    _, partition = create_partitions(
        frame,
        row_id="id",
        target="label",
        layout="train_validation_test",
        memberships={"train": [0, 1, 2], "validation": [3], "test": [4]},
    )
    (root / "data/split.json").write_text(json.dumps(partition, allow_nan=False))
    (root / "config.json").write_text(
        '{"selected_columns":["x","category"],"with_std":false}\n'
    )
    (root / "source.ipynb").write_text(
        json.dumps(
            {
                "nbformat": 4,
                "nbformat_minor": 5,
                "metadata": {},
                "cells": [
                    {
                        "id": "source-cell",
                        "cell_type": "code",
                        "metadata": {},
                        "source": "import sys; print(sys.prefix)",
                        "outputs": [],
                        "execution_count": None,
                    }
                ],
            }
        )
    )
    command(sys.executable, "-m", "dvc", "add", "data")
    command("git", "add", ".")
    command("git", "commit", "-m", "data: commit installed handoff inputs")
    command(str(root / ".venv/bin/agentic-ml"), "init")
    command("git", "add", ".")
    command("git", "commit", "-m", "chore: commit initialized experiment")
    commit = command("git", "rev-parse", "HEAD")
    identity = json.loads((root / ".agentic-ml/init.json").read_text())["environment"][
        "toolkit_identity"
    ]
    pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
    libraries = {
        name: version(name)
        for name in ("agentic-ml", "mlflow", "dvc", "pandas", "pyarrow", "scikit-learn")
    }
    provenance = {
        "schema_version": "1.0",
        "experiment": {
            "commit_sha": commit,
            "entrypoint": ref("track.py"),
            "code": [ref("track.py"), ref("source.ipynb")],
        },
        "configuration": {
            "files": [ref("config.json")],
            "effective": json.loads((root / "config.json").read_text()),
        },
        "data": [
            {
                "metadata": ref("data.dvc"),
                "output_path": "data",
                "hash_name": "md5",
                "hash_value": pointer["md5"],
                "member_path": name,
            }
            for name in ("input.csv", "split.json")
        ],
        "split_record": ref("data/split.json"),
        "environment": {
            "lockfile": ref("uv.lock"),
            "python_version": sys.version.split()[0],
            "libraries": libraries,
        },
        "toolkit": {
            "installation": identity,
            "repository_url": None,
            "commit_sha": None,
            "build_identity": None,
        },
    }
    (root / "run-provenance.json").write_text(json.dumps(provenance, allow_nan=False))
    assert identity["kind"] == "wheel"
    assert (
        identity["sha256"]
        == hashlib.sha256(
            Path(unquote(urlparse(identity["locator"]).path)).read_bytes()
        ).hexdigest()
    )
    for name in ("track.py", "source.ipynb", "config.json", "uv.lock", "data.dvc"):
        blob = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=root)
        assert blob == (root / name).read_bytes()
    assert json.loads(command(sys.executable, "-m", "dvc", "status", "--json")) == {}
    uri = f"sqlite:///{root}/.agentic-ml/handoff.db"
    client = MlflowClient(tracking_uri=uri)
    experiment = client.create_experiment(
        "actual-producer",
        artifact_location=(root / ".agentic-ml/handoff-artifacts").as_uri(),
    )

    def execute_notebook(error: bool) -> bytes:
        script = """
import sys
from pathlib import Path
import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
root=Path(sys.argv[1]); error=sys.argv[2]=='error'
source="raise ValueError('installed notebook failure')" if error else "import sys; print(sys.prefix)"
notebook=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)])
manager=KernelManager(kernel_name='python3')
manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
try:
    NotebookClient(notebook,km=manager,timeout=30,resources={'metadata':{'path':str(root)}}).execute()
except CellExecutionError:
    assert error
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
outputs=notebook.cells[0].outputs
assert outputs[0].output_type==('error' if error else 'stream')
if not error:
    assert outputs[0].text.strip()==sys.prefix
nbformat.write(notebook,root/'executed.ipynb')
"""
        command(
            sys.executable,
            "-I",
            "-c",
            script,
            str(root),
            "error" if error else "success",
        )
        return (root / "executed.ipynb").read_bytes()

    # The project script is the exact documented executable, not a toolkit copy.
    spec = importlib.util.spec_from_file_location(
        "experiment_tracking", root / "track.py"
    )
    assert spec is not None and spec.loader is not None
    project = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(project)
    before = execute_notebook(False)
    run_id = client.create_run(experiment).info.run_id
    answer = project.run(root, uri, run_id, executed_notebook=Path("executed.ipynb"))
    native = client.get_run(run_id)
    assert native.info.status == "FINISHED" and native.info.run_id == run_id
    assert native.data.metrics == {"validation_accuracy": 0.75}
    assert native.data.tags["validation_status"] == "failed"
    assert native.data.tags["process_exit_code"] == "0"
    assert (
        json.loads(native.data.params["preprocessing"]) == answer["record"]["pipeline"]
    )
    metadata = json.loads(
        Path(
            client.download_artifacts(run_id, "preprocessing/metadata.json")
        ).read_text()
    )
    assert metadata == answer["record"]
    assert metadata["partition_record"] == partition
    assert metadata["fit_partition"] == "train" and metadata["selected_columns"] == [
        "x",
        "category",
    ]
    assert metadata["output_schema"] == [
        {"name": name, "dtype": "float64"}
        for name in ("centered_x", "category_a", "category_b")
    ]
    params = metadata["pipeline"]["parameters"]
    assert set(params) == {"memory", "steps", "transform_input", "verbose"}
    transformers = params["steps"][0][1]["parameters"]["transformers"]
    assert [item[0] for item in transformers] == ["numeric", "category"]
    assert transformers[0][1]["parameters"]["steps"][0][1]["parameters"][
        "missing_values"
    ] == {"kind": "missing_value", "value": "nan"}
    assert transformers[1][1]["parameters"]["dtype"] == {
        "kind": "numpy_dtype",
        "name": "float64",
    }
    assert (
        json.loads(
            Path(client.download_artifacts(run_id, "provenance.json")).read_text()
        )
        == provenance
    )
    expected = b"centered_x,category_a,category_b\n-1.0,1.0,0.0\n0.0,0.0,1.0\n1.0,1.0,0.0\n98.0,0.0,0.0\n198.0,1.0,0.0\n"
    assert (
        Path(
            client.download_artifacts(run_id, "outputs/features/features.csv")
        ).read_bytes()
        == expected
    )
    assert (
        Path(client.download_artifacts(run_id, "notebooks/executed.ipynb")).read_bytes()
        == before
    )
    model_path = client.download_artifacts(run_id, "preprocessing/pipeline")
    model = mlflow.sklearn.load_model(model_path)
    # Readability and retained fitted state; no M2 restored transformation replay.
    assert model["features"].named_transformers_["numeric"][
        "impute"
    ].statistics_.tolist() == [2.0]
    assert model["features"].named_transformers_["numeric"]["scale"].mean_.tolist() == [
        2.0
    ]
    assert model["features"].named_transformers_["category"].categories_[
        0
    ].tolist() == ["a", "b"]
    for section in ("preprocessing", "result"):
        assert answer[section]["run_id"] == run_id
        assert all(
            value.startswith(native.info.artifact_uri + "/")
            for value in answer[section]["artifacts"].values()
        )
    outcomes = {"success": native.info.status}
    failures: dict[str, Any] = {}
    for mode, exception in (
        ("notebook_error", RuntimeError),
        ("missing_output", FileNotFoundError),
        ("invalid_reference", ValueError),
    ):
        failed_id = client.create_run(experiment).info.run_id
        options: dict[str, Any] = {}
        expected_notebook = None
        if mode == "notebook_error":
            expected_notebook = execute_notebook(True)
            options = {
                "process_exit_code": 1,
                "executed_notebook": Path("executed.ipynb"),
            }
        elif mode == "missing_output":
            options = {"expected_output": "predictions"}
        else:
            (root / "config.json").write_text('{"changed":true}\n')
        try:
            project.run(root, uri, failed_id, **options)
        except exception as error:
            failures[mode] = {
                "run_id": failed_id,
                "type": type(error).__name__,
                "message": str(error),
                "notes": getattr(error, "__notes__", []),
            }
        else:
            raise AssertionError(f"{mode} was incorrectly accepted")
        outcomes[mode] = client.get_run(failed_id).info.status
        assert outcomes[mode] == "FAILED"
        if expected_notebook is not None:
            assert (
                Path(
                    client.download_artifacts(failed_id, "notebooks/executed.ipynb")
                ).read_bytes()
                == expected_notebook
            )
        if mode == "missing_output":
            assert client.get_run(failed_id).data.tags["process_exit_code"] == "0"
            assert Path(
                client.download_artifacts(failed_id, "preprocessing/metadata.json")
            ).is_file()
        if mode == "invalid_reference":
            assert "config.json" in failures[mode]["message"]
            assert client.list_artifacts(failed_id) == []
    evidence = root / "evidence"
    evidence.mkdir()
    (evidence / "metadata.json").write_text(
        json.dumps(metadata, allow_nan=False, indent=2)
    )
    (evidence / "provenance.json").write_text(
        json.dumps(provenance, allow_nan=False, indent=2)
    )
    (evidence / "features.csv").write_bytes(expected)
    (evidence / "executed-success.ipynb").write_bytes(before)
    (evidence / "executed-error.ipynb").write_bytes(
        (root / "executed.ipynb").read_bytes()
    )
    shutil.copytree(model_path, evidence / "pipeline")
    package = Path(agentic_ml.preprocessing.__file__).resolve()
    tracking = Path(agentic_ml.tracking.__file__).resolve()
    for module in (package, tracking):
        assert module.is_relative_to(root / ".venv") and "site-packages" in module.parts
    installed = {item.metadata["Name"].lower() for item in distributions()}
    assert not installed.intersection({"pytest", "pytest-xdist", "mypy", "ruff"})
    (root / "identity.json").write_text(
        json.dumps(
            {
                "outcomes": outcomes,
                "run_id": run_id,
                "artifact_uri": native.info.artifact_uri,
                "metadata": answer["record"],
                "downloaded_metadata": metadata,
                "provenance": provenance,
                "pipeline_module": str(package),
                "tracking_module": str(tracking),
                "prefix": sys.prefix,
                "cwd": str(Path.cwd()),
                "versions": libraries,
                "failures": failures,
                "script_sha256": hashlib.sha256(
                    (root / "track.py").read_bytes()
                ).hexdigest(),
                "environment": {
                    name: os.environ.get(name)
                    for name in ("PYTHONPATH", "VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT")
                },
            },
            indent=2,
            allow_nan=False,
        )
    )
    print("PASS actual producer handoff", flush=True)


if __name__ == "__main__":
    main()
