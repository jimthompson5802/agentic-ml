"""Inspect the exact feature recipe in a separate installed runtime project."""

import argparse
import hashlib
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

import agentic_ml.training


def main() -> None:
    """Run independent numerical, artifact, lineage and failure checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    root = parser.parse_args().project.resolve()
    assert Path(sys.prefix).resolve() == root / ".venv"
    assert not Path.cwd().is_relative_to(root)
    commands: list[dict[str, Any]] = []

    def command(*parts: str, expected: int = 0, cwd: Path | None = None) -> str:
        """Persist complete native command output before checking the outcome."""
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

    def ref(name: str) -> dict[str, str]:
        """Independently hash a real project file."""
        return {
            "path": name,
            "sha256": "sha256:"
            + hashlib.sha256((root / name).read_bytes()).hexdigest(),
        }

    command("git", "-C", str(root), "init")
    command("git", "-C", str(root), "config", "user.email", "fixture@example.invalid")
    command("git", "-C", str(root), "config", "user.name", "US-14 installed comparison")
    (root / ".gitignore").write_text(
        ".venv/\nidentity.json\nnative-commands.json\nevidence/\n"
    )
    command(str(root / ".venv/bin/agentic-ml"), "init", "--project-root", str(root))
    recipe_names = (
        "prepare_comparison.py",
        "compare_features.py",
        "feature_variants.py",
    )
    recipe_sha256 = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in recipe_names
    }
    setup = json.loads(
        command(sys.executable, str(root / "prepare_comparison.py"), str(root))
    )
    client = MlflowClient(tracking_uri=setup["tracking_uri"])
    evidence = root / "evidence"
    evidence.mkdir()
    baseline_settings = json.loads((root / "comparison-settings.json").read_text())
    baseline_brief = (root / "brief.md").read_text()
    partition = json.loads((root / "data/split.json").read_text())
    source = pd.read_csv(root / "data/input.csv")
    assert partition["memberships"] == {
        "train": [0, 1, 2, 3],
        "validation": [4, 5],
        "test": [6, 7],
    }
    assert np.isinf(source.iloc[6:]["n"]).all()

    def renew(settings: dict[str, Any], brief: str) -> dict[str, Any]:
        """Commit an explicit scientist edit and refresh its actual provenance."""
        (root / "comparison-settings.json").write_text(json.dumps(settings))
        (root / "brief.md").write_text(brief)
        command("git", "-C", str(root), "add", ".")
        command(
            "git",
            "-C",
            str(root),
            "commit",
            "--allow-empty",
            "-m",
            "test: revise feature protocol",
        )
        provenance: dict[str, Any] = json.loads(
            (root / "run-provenance.json").read_text()
        )
        provenance["experiment"]["commit_sha"] = command(
            "git", "-C", str(root), "rev-parse", "HEAD"
        )
        provenance["experiment"]["code"] = [ref(n) for n in recipe_names]
        provenance["experiment"]["entrypoint"] = ref("compare_features.py")
        provenance["configuration"]["files"] = [
            ref(item["path"]) for item in provenance["configuration"]["files"]
        ]
        provenance["configuration"]["effective"] = settings
        (root / "run-provenance.json").write_text(json.dumps(provenance))
        return provenance

    def invoke(experiment: str, *, expected: int = 0) -> str:
        """Invoke the copied public script using its required explicit flags."""
        return command(
            sys.executable,
            str(root / "compare_features.py"),
            "--project-root",
            str(root),
            "--tracking-uri",
            setup["tracking_uri"],
            "--experiment-id",
            experiment,
            "--settings",
            "comparison-settings.json",
            expected=expected,
        )

    scores: dict[str, list[float]] = {}
    deltas: list[float] = []
    expected_predictions = [[0, 0], [0, 1], [0, 0], [1, 0]]
    for metric, direction, expected_scores in (
        ("accuracy", "maximize", [0.5, 1.0, 0.5, 0.0]),
        ("zero_one_loss", "minimize", [0.5, 0.0, 0.5, 1.0]),
    ):
        settings = baseline_settings | {"metric": metric, "direction": direction}
        provenance = renew(
            settings,
            baseline_brief.replace("metric: accuracy", f"metric: {metric}").replace(
                "direction: maximize", f"direction: {direction}"
            ),
        )
        answer = json.loads(invoke(setup["experiment_id"]))
        reference = client.get_run(answer["reference_run_id"])
        summary = json.loads(
            Path(
                client.download_artifacts(
                    reference.info.run_id, "outputs/comparison/comparison.json"
                )
            ).read_text()
        )
        assert summary["metric"] == metric and summary["direction"] == direction
        assert summary["source"] == partition["source"]
        assert summary["split_record"] == ref("data/split.json")
        assert summary["validation_membership"] == [4, 5]
        assert [row["variant"] for row in summary["rows"]] == [
            "reference",
            "signal",
            "unchanged",
            "misleading",
        ]
        assert [row["score"] for row in summary["rows"]] == expected_scores
        assert [row["adjusted_delta"] for row in summary["rows"]] == [
            0.0,
            0.5,
            0.0,
            -0.5,
        ]
        assert [row["raw_delta"] for row in summary["rows"]] == (
            [0.0, 0.5, 0.0, -0.5] if direction == "maximize" else [0.0, -0.5, 0.0, 0.5]
        )
        assert [row["outcome"] for row in summary["rows"]] == [
            "reference",
            "gain",
            "tie",
            "regression",
        ]
        records = []
        for row, predicted in zip(summary["rows"], expected_predictions, strict=True):
            run_id = row["run_id"]
            native = client.get_run(run_id)
            assert native.info.status == "FINISHED"
            assert native.info.end_time <= reference.info.end_time
            assert native.data.params["reference_run_id"] == reference.info.run_id
            assert native.data.tags["validation_status"] == "not_checked"
            assert native.data.metrics == {f"validation_{metric}": row["score"]}
            record = json.loads(
                Path(
                    client.download_artifacts(run_id, "outputs/training/training.json")
                ).read_text()
            )
            assert record["preprocessing"]["partition_record"] == partition
            assert (
                record["parameters"]["max_depth"] == 1
                and record["parameters"]["random_state"] == 17
            )
            assert {key: record[key] for key in summary["estimator"]} == summary[
                "estimator"
            ]
            preprocessing = json.loads(
                Path(
                    client.download_artifacts(run_id, "preprocessing/metadata.json")
                ).read_text()
            )
            assert preprocessing == record["preprocessing"]
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
            selected = preprocessing["selected_columns"]
            assert model.predict(source.iloc[4:6][selected]).tolist() == predicted
            assert model["estimator"].get_params(deep=False) == record["parameters"]
            for logical, reference_file in row["outputs"].items():
                assert ref(reference_file["path"]) == reference_file
                output = root / reference_file["path"]
                relative = f"outputs/{logical}/{output.name}"
                assert (
                    row["artifacts"][logical]
                    == native.info.artifact_uri + "/" + relative
                )
                assert (
                    Path(client.download_artifacts(run_id, relative)).read_bytes()
                    == output.read_bytes()
                )
            train = pd.read_parquet(root / row["outputs"]["train_features"]["path"])
            validation = pd.read_parquet(
                root / row["outputs"]["validation_features"]["path"]
            )
            assert train["id"].tolist() == [0, 1, 2, 3] and validation[
                "id"
            ].tolist() == [4, 5]
            if row["variant"] in ("signal", "misleading"):
                np.testing.assert_allclose(
                    train.iloc[:, 1],
                    [
                        -1.2649110640673518,
                        -0.6324555320336759,
                        0.6324555320336759,
                        1.2649110640673518,
                    ],
                    rtol=1e-12,
                    atol=1e-12,
                )
            else:
                np.testing.assert_array_equal(train.iloc[:, 1], [0.0, 0.0, 0.0, 0.0])
            pointer = row["derived_data"]
            dvc_file = root / pointer["metadata"]["path"]
            native_pointer = yaml.safe_load(dvc_file.read_text())["outs"][0]
            assert pointer["hash_value"] == native_pointer[pointer["hash_name"]]
            assert (
                json.loads(
                    command(
                        sys.executable,
                        "-m",
                        "dvc",
                        "status",
                        "--json",
                        pointer["metadata"]["path"],
                        cwd=root,
                    )
                )
                == {}
            )
            assert (
                json.loads(
                    Path(
                        client.download_artifacts(run_id, "provenance.json")
                    ).read_text()
                )
                == provenance
            )
            records.append({"run": native.to_dictionary(), "training": record})
        for item in (
            provenance["experiment"]["code"]
            + provenance["configuration"]["files"]
            + [provenance["environment"]["lockfile"]]
            + [item["metadata"] for item in provenance["data"]]
        ):
            assert ref(item["path"]) == item
            assert (
                subprocess.check_output(
                    [
                        "git",
                        "-C",
                        str(root),
                        "show",
                        f"{provenance['experiment']['commit_sha']}:{item['path']}",
                    ]
                )
                == (root / item["path"]).read_bytes()
            )
        (evidence / (metric + ".json")).write_text(
            json.dumps(
                {"summary": summary, "records": records, "provenance": provenance},
                indent=2,
            )
        )
        scores[metric] = [row["score"] for row in summary["rows"]]
        deltas = [row["adjusted_delta"] for row in summary["rows"]]

    settings = baseline_settings | {
        "variants": ["reference", "mixed_scaled", "mixed_unscaled"]
    }
    provenance = renew(settings, baseline_brief)
    answer = json.loads(invoke(setup["experiment_id"]))
    mixed = json.loads(
        Path(
            client.download_artifacts(
                answer["reference_run_id"], "outputs/comparison/comparison.json"
            )
        ).read_text()
    )
    mixed_columns = ["id", "n_value", "count_value", "is_a", "is_b"]
    assert [row["score"] for row in mixed["rows"]] == [0.5, 1.0, 1.0]
    for row, expected_n in zip(
        mixed["rows"][1:],
        [[-1.414213562373095, 0.0, 0.0, 1.414213562373095], [1.0, 3.0, 3.0, 5.0]],
        strict=True,
    ):
        train = pd.read_parquet(root / row["outputs"]["train_features"]["path"])
        validation = pd.read_parquet(
            root / row["outputs"]["validation_features"]["path"]
        )
        assert list(train.columns) == mixed_columns
        assert train.dtypes.astype(str).tolist() == [
            "int64",
            "float64",
            "float64",
            "float64",
            "float64",
        ]
        np.testing.assert_allclose(train["n_value"], expected_n, rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(
            train[["count_value", "is_a", "is_b"]],
            [[10.0, 1.0, 0.0], [20.0, 0.0, 1.0], [30.0, 1.0, 0.0], [40.0, 0.0, 1.0]],
            rtol=0,
            atol=0,
        )
        np.testing.assert_allclose(
            validation[["count_value", "is_a", "is_b"]],
            [[15.0, 0.0, 0.0], [35.0, 0.0, 1.0]],
            rtol=0,
            atol=0,
        )
    (evidence / "mixed.json").write_text(json.dumps(mixed, indent=2))

    outcomes = {}
    for mode in (
        "missing_input",
        "unknown_variant",
        "invalid_provenance",
        "artifact_storage",
    ):
        provenance = renew(baseline_settings, baseline_brief)
        destination = root / ".agentic-ml" / mode
        if mode == "artifact_storage":
            destination.write_text("prior artifact bytes")
        experiment = client.create_experiment(
            mode, artifact_location=destination.as_uri()
        )
        if mode == "missing_input":
            (root / "data/input.csv").rename(root / "data/held.csv")
        elif mode == "unknown_variant":
            invalid = baseline_settings | {"variants": ["reference", "unknown"]}
            renew(invalid, baseline_brief)
        elif mode == "invalid_provenance":
            invalid = json.loads(json.dumps(provenance))
            invalid["experiment"]["entrypoint"]["sha256"] = "sha256:" + "0" * 64
            (root / "run-provenance.json").write_text(json.dumps(invalid))
        diagnostic = invoke(experiment, expected=1)
        runs = client.search_runs([experiment])
        if mode in ("missing_input", "unknown_variant"):
            assert not runs
            outcomes[mode] = "rejected_before_run"
        else:
            assert len(runs) == 1 and runs[0].info.status == "FAILED"
            assert not client.list_artifacts(runs[0].info.run_id, "outputs/comparison")
            outcomes[mode] = runs[0].info.status
        if mode == "missing_input":
            assert "FileNotFoundError" in diagnostic
            (root / "data/held.csv").rename(root / "data/input.csv")
        if mode == "artifact_storage":
            assert "NotADirectoryError" in diagnostic
            assert destination.read_text() == "prior artifact bytes"
        (evidence / (mode + ".json")).write_text(
            json.dumps(
                {"diagnostic": diagnostic, "runs": [r.to_dictionary() for r in runs]},
                indent=2,
            )
        )
    provenance = renew(baseline_settings, baseline_brief)
    module = Path(agentic_ml.training.__file__).resolve()
    assert module.is_relative_to(root / ".venv") and "site-packages" in module.parts
    assert not {d.metadata["Name"].lower() for d in distributions()}.intersection(
        {"pytest", "ruff", "mypy", "pytest-xdist"}
    )
    (root / "identity.json").write_text(
        json.dumps(
            {
                "scores": scores,
                "adjusted_deltas": deltas,
                "mixed_columns": mixed_columns,
                "outcomes": outcomes,
                "toolkit_identity": provenance["toolkit"]["installation"],
                "training_module": str(module),
                "prefix": sys.prefix,
                "cwd": str(Path.cwd()),
                "recipe_sha256": recipe_sha256,
                "environment": provenance["environment"],
                "provenance": provenance,
                "versions": {
                    n: version(n)
                    for n in (
                        "agentic-ml",
                        "mlflow",
                        "dvc",
                        "pandas",
                        "numpy",
                        "scikit-learn",
                        "pyarrow",
                        "skops",
                    )
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
