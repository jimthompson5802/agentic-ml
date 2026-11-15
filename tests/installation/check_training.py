"""Inspect classification through installed interfaces and real native stores."""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from importlib.metadata import distributions, version
from pathlib import Path
from typing import Any

import mlflow.sklearn
import numpy as np
import pandas as pd
import yaml
from mlflow import MlflowClient
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import agentic_ml.training
from agentic_ml.planning import ResolveRequest, resolve_plan
from agentic_ml.training import fit_classifier
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    validate_configuration,
)


def main() -> None:
    """Initialize the installed project, run the guide and check independent oracles."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()
    assert Path(sys.prefix).resolve() == root / ".venv"
    assert not Path.cwd().is_relative_to(root)
    commands: list[dict[str, Any]] = []

    def command(*parts: str, expected: int = 0, cwd: Path | None = None) -> str:
        result = subprocess.run(
            parts, cwd=cwd or Path.cwd(), capture_output=True, text=True
        )
        commands.append(
            {
                "command": parts,
                "cwd": str(cwd or Path.cwd()),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        (root / "native-commands.json").write_text(json.dumps(commands, indent=2))
        assert (result.returncode == 0) == (expected == 0), (
            result.stdout + result.stderr
        )
        return result.stdout.strip() if expected == 0 else result.stderr

    command("git", "-C", str(root), "init")
    command("git", "-C", str(root), "config", "user.email", "fixture@example.invalid")
    command(
        "git", "-C", str(root), "config", "user.name", "US-18 installed classification"
    )
    (root / ".gitignore").write_text(
        ".venv/\nidentity.json\nnative-commands.json\nevidence/\n"
    )
    command(str(root / ".venv/bin/agentic-ml"), "init", "--project-root", str(root))
    setup = json.loads(
        command(sys.executable, str(root / "prepare_training.py"), str(root))
    )
    answer = json.loads(
        command(
            sys.executable,
            str(root / "train.py"),
            str(root),
            setup["tracking_uri"],
            setup["experiment_id"],
        )
    )
    client = MlflowClient(tracking_uri=setup["tracking_uri"])
    provenance = json.loads((root / "run-provenance.json").read_text())
    partition = json.loads((root / "data/split.json").read_text())
    baseline = client.get_run(answer["baseline"])
    assert len(client.search_runs([setup["experiment_id"]])) == 3
    evidence = root / "evidence"
    evidence.mkdir()
    predictions, scores = [], []
    for index, (run_id, algorithm, expected) in enumerate(
        zip(
            [answer["baseline"], *answer["candidates"]],
            ["dummy_classifier", "decision_tree", "random_forest"],
            [[0, 0], [0, 1], [0, 1]],
            strict=True,
        )
    ):
        native = client.get_run(run_id)
        assert native.info.status == "FINISHED"
        assert native.data.tags["process_exit_code"] == "0"
        assert native.data.tags["validation_status"] == "not_checked"
        if index:
            assert baseline.info.end_time <= native.info.start_time
            assert native.data.params["baseline_run_id"] == baseline.info.run_id
        score = native.data.metrics["validation_accuracy"]
        assert score == (0.5 if index == 0 else 1.0)
        scores.append(score)
        record = json.loads(
            Path(
                client.download_artifacts(run_id, "outputs/training/training.json")
            ).read_text()
        )
        assert record["algorithm"] == algorithm and record["fit_partition"] == "train"
        assert record["classes"] == [0, 1]
        for field in ("parameters", "parameter_origins", "estimator_class", "versions"):
            assert json.loads(native.data.params[field]) == record[field]
        for name, installed_version in record["versions"].items():
            assert installed_version == version(name)
        preprocessing = json.loads(
            Path(
                client.download_artifacts(run_id, "preprocessing/metadata.json")
            ).read_text()
        )
        assert preprocessing == record["preprocessing"]
        assert preprocessing["partition_record"] == partition
        assert preprocessing["selected_columns"] == ["x"]
        assert preprocessing["output_schema"] == [{"name": "x", "dtype": "float64"}]
        model_path = Path(client.download_artifacts(run_id, "model/pipeline"))
        flavor = yaml.safe_load((model_path / "MLmodel").read_text())["flavors"][
            "sklearn"
        ]
        assert flavor["serialization_format"] == "skops"
        assert flavor["skops_trusted_types"] == [
            "numpy.dtype",
            "sklearn.tree._tree.Tree",
        ]
        model = mlflow.sklearn.load_model(str(model_path))
        observed = model.predict(pd.DataFrame({"x": [-2.0, 2.0]})).tolist()
        assert observed == expected
        predictions.append(observed)
        assert model["estimator"].get_params(deep=False) == record["parameters"]
        np.testing.assert_allclose(
            model["preprocessing"].transform(pd.DataFrame({"x": [0.0, 100.0]})),
            [[0.0], [100.0 / np.sqrt(5.0)]],
            rtol=1e-12,
            atol=1e-12,
        )
        saved = json.loads(
            Path(client.download_artifacts(run_id, "provenance.json")).read_text()
        )
        assert saved == provenance
        (evidence / (algorithm + ".json")).write_text(
            json.dumps(
                {"run": native.to_dictionary(), "record": record, "provenance": saved},
                indent=2,
            )
        )
    for ref in (
        provenance["experiment"]["code"]
        + provenance["configuration"]["files"]
        + [provenance["environment"]["lockfile"]]
        + [item["metadata"] for item in provenance["data"]]
    ):
        data = (root / ref["path"]).read_bytes()
        assert ref["sha256"] == "sha256:" + hashlib.sha256(data).hexdigest()
        assert (
            subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(root),
                    "show",
                    f"{provenance['experiment']['commit_sha']}:{ref['path']}",
                ]
            )
            == data
        )
    assert (
        provenance["split_record"]["sha256"]
        == "sha256:"
        + hashlib.sha256((root / "data/split.json").read_bytes()).hexdigest()
    )
    pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
    assert all(item["hash_value"] == pointer["md5"] for item in provenance["data"])
    assert (
        json.loads(command(sys.executable, "-m", "dvc", "status", "--json", cwd=root))
        == {}
    )
    # Exercise fresh construction through the installed public helper twice.
    spec = importlib.util.spec_from_file_location(
        "project_bindings", root / "training_bindings.py"
    )
    assert spec is not None and spec.loader is not None
    bindings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bindings)
    plan = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    assert plan.plan_id is not None
    configuration = validate_configuration(
        ConfigurationRequest(root, plan.plan_id, Path("registry.yaml"))
    )
    assert configuration.validation_id is not None
    candidate = CandidateRequest(root, configuration.validation_id, "decision_tree", {})
    frame = pd.read_csv(root / "data/input.csv")
    preprocessing_input = Pipeline([("scale", StandardScaler())])

    def fit(selected_bindings: Any) -> tuple[Pipeline, dict[str, object]]:
        return fit_classifier(
            frame,
            project_root=root,
            candidate=candidate,
            estimator_bindings=selected_bindings,
            preprocessing=preprocessing_input,
            partition_record=partition,
            selected_columns=["x"],
            output_schema=[{"name": "x", "dtype": "float64"}],
        )

    first, _ = fit(bindings.ESTIMATOR_BINDINGS)
    second, _ = fit(bindings.ESTIMATOR_BINDINGS)
    assert first["estimator"] is not second["estimator"]
    assert first["preprocessing"] is not second["preprocessing"]
    assert not hasattr(preprocessing_input["scale"], "mean_")
    try:
        fit({"decision_tree": bindings.ESTIMATOR_BINDINGS["dummy_classifier"]})
    except TypeError as error:
        assert "unexpected keyword argument" in str(error)
    else:
        raise AssertionError("Incompatible constructor was accepted")
    # A valid metadata profile still must declare every native constructor setting.
    registry_path, search_path = root / "registry.yaml", root / "search.yaml"
    original_registry, original_search = (
        registry_path.read_text(),
        search_path.read_text(),
    )
    registry = yaml.safe_load(original_registry)
    search = yaml.safe_load(original_search)
    tree_profile = next(
        item for item in registry["algorithms"] if item["id"] == "decision_tree"
    )
    del tree_profile["parameters"]["random_state"]
    del search["algorithms"]["decision_tree"]["fixed"]["random_state"]
    try:
        registry_path.write_text(yaml.safe_dump(registry))
        search_path.write_text(yaml.safe_dump(search))
        incomplete_plan = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
        assert incomplete_plan.plan_id is not None
        incomplete = validate_configuration(
            ConfigurationRequest(root, incomplete_plan.plan_id, Path("registry.yaml"))
        )
        assert incomplete.validation_id is not None, incomplete.diagnostics
        candidate = CandidateRequest(
            root, incomplete.validation_id, "decision_tree", {}
        )
        try:
            fit(bindings.ESTIMATOR_BINDINGS)
        except ValueError as coverage_error:
            assert "parameters must cover and match all native defaults" in str(
                coverage_error
            )
        else:
            raise AssertionError("Incomplete native parameter profile was accepted")
    finally:
        registry_path.write_text(original_registry)
        search_path.write_text(original_search)
    # Missing input and invalid provenance must fail the baseline without candidates.
    outcomes = {}
    for mode in ("missing_input", "invalid_provenance"):
        experiment = client.create_experiment(
            mode, artifact_location=(root / ".agentic-ml" / mode).as_uri()
        )
        if mode == "missing_input":
            (root / "data/input.csv").rename(root / "data/held.csv")
        else:
            invalid = json.loads(json.dumps(provenance))
            invalid["experiment"]["entrypoint"]["sha256"] = "sha256:" + "0" * 64
            (root / "run-provenance.json").write_text(json.dumps(invalid))
        diagnostic_text = command(
            sys.executable,
            str(root / "train.py"),
            str(root),
            setup["tracking_uri"],
            experiment,
            expected=1,
        )
        assert (
            "FileNotFoundError" if mode == "missing_input" else "ValueError"
        ) in diagnostic_text
        runs = client.search_runs([experiment])
        assert len(runs) == 1 and runs[0].info.status == "FAILED"
        outcomes[mode] = runs[0].info.status
        assert (root / ".training" / runs[0].info.run_id / "failure.txt").is_file()
        if mode == "missing_input":
            (root / "data/held.csv").rename(root / "data/input.csv")
    (root / "run-provenance.json").write_text(json.dumps(provenance))
    module = Path(agentic_ml.training.__file__).resolve()
    assert module.is_relative_to(root / ".venv") and "site-packages" in module.parts
    assert not {d.metadata["Name"].lower() for d in distributions()}.intersection(
        {"pytest", "ruff", "mypy", "pytest-xdist"}
    )
    (root / "identity.json").write_text(
        json.dumps(
            {
                "predictions": predictions,
                "scores": scores,
                "outcomes": outcomes,
                "toolkit_identity": provenance["toolkit"]["installation"],
                "training_module": str(module),
                "prefix": sys.prefix,
                "cwd": str(Path.cwd()),
                "provenance": provenance,
                "fresh_instances": True,
                "parameter_coverage_rejected": True,
                "constructor_error_preserved": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
