"""Compare explicitly authored features using installed public toolkit APIs."""

import argparse
import hashlib
import json
import subprocess
import sys
import traceback
from collections.abc import Mapping, Sequence
from importlib.metadata import version
from pathlib import Path
from typing import Literal, cast

import mlflow.sklearn
import pandas as pd
import yaml
from feature_variants import ESTIMATOR_BINDINGS, FeatureVariant, get_variants
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.metrics import accuracy_score, zero_one_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from agentic_ml.data_quality import run_validated_step
from agentic_ml.planning import ResolveRequest, inspect_plan, resolve_plan
from agentic_ml.planning.models import JSONValue
from agentic_ml.splitting import create_partitions
from agentic_ml.tracking import log_preprocessing, log_run_results
from agentic_ml.training import fit_classifier
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    validate_candidate,
    validate_configuration,
)


def document(path: Path) -> dict[str, object]:
    """Load a project-owned JSON object."""
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    json.dumps(value, allow_nan=False)
    return cast(dict[str, object], value)


def project_file(root: Path, value: object) -> Path:
    """Resolve an existing root-relative regular input without symlink traversal."""
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or Path(value).is_absolute()
        or any(p in ("", ".", "..") for p in value.split("/"))
    ):
        raise ValueError("Expected normalized project-relative input path")
    path = root / value
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Symlink input path")
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def read_settings(root: Path, path: str) -> dict[str, object]:
    """Validate the complete comparison settings before creating native runs."""
    settings = document(project_file(root, path))
    keys = {
        "schema_version",
        "experiment",
        "registry",
        "source",
        "split_record",
        "provenance",
        "algorithm",
        "parameters",
        "variants",
        "reference",
        "metric",
        "direction",
        "quality_rules",
        "expected_outputs",
    }
    if set(settings) != keys or settings["schema_version"] != "1.0":
        raise ValueError("Settings require exactly the version 1.0 fields")
    names = settings["variants"]
    if (
        not isinstance(names, list)
        or not names
        or any(not isinstance(n, str) or not n for n in names)
        or len(set(names)) != len(names)
    ):
        raise ValueError("variants must be nonempty unique names")
    if not isinstance(settings["reference"], str) or settings["reference"] not in names:
        raise ValueError("reference must be a selected variant")
    if (settings["metric"], settings["direction"]) not in (
        ("accuracy", "maximize"),
        ("zero_one_loss", "minimize"),
    ):
        raise ValueError("Unsupported metric/direction pair")
    expected = settings["expected_outputs"]
    if (
        not isinstance(expected, list)
        or any(not isinstance(n, str) for n in expected)
        or len(set(expected)) != len(expected)
        or set(expected)
        != {"training", "train_features", "validation_features", "derived_dvc"}
    ):
        raise ValueError("expected_outputs must name all four required outputs")
    if not isinstance(settings["parameters"], dict) or not isinstance(
        settings["quality_rules"], list
    ):
        raise ValueError("parameters must be an object; quality_rules must be a list")
    for key in ("experiment", "registry", "source", "split_record", "provenance"):
        project_file(root, settings[key])
    return settings


def file_ref(root: Path, path: Path) -> dict[str, str]:
    """Describe a project output without replacing its native data identity."""
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def write_json(path: Path, value: object) -> None:
    """Write a finite JSON document without overwriting an earlier output."""
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False))


def native(root: Path, *args: str) -> str:
    """Execute a native project command with explicit cwd and visible errors."""
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def selected_variants(
    names: list[str], frame: pd.DataFrame, partition: dict[str, object]
) -> dict[str, FeatureVariant]:
    """Validate all factory names and fully validate only selected payloads."""
    values: object = get_variants()
    if not isinstance(values, list):
        raise ValueError("get_variants must return a list")
    declarations: dict[str, FeatureVariant] = {}
    for value in values:
        if (
            not isinstance(value, dict)
            or not isinstance(value.get("name"), str)
            or not value["name"]
            or value["name"] in declarations
        ):
            raise ValueError("Factory names must be nonempty and globally unique")
        declarations[value["name"]] = cast(FeatureVariant, value)
    if any(name not in declarations for name in names):
        raise ValueError("Unknown selected variant")
    for name in names:
        value = declarations[name]
        if set(value) != {"name", "pipeline", "selected_columns", "output_schema"}:
            raise ValueError(
                "Selected variant requires exactly four declaration fields"
            )
        if not isinstance(value["pipeline"], Pipeline):
            raise TypeError("Selected pipeline must be a native sklearn Pipeline")
        if name in (".", "..") or "/" in name or "\\" in name:
            raise ValueError("Variant names must be safe output path components")
        columns: object = value["selected_columns"]
        if (
            not isinstance(columns, list)
            or not columns
            or any(
                not isinstance(c, str)
                or c not in frame.columns
                or c in (partition["row_id"], partition["target"])
                for c in columns
            )
            or len(set(columns)) != len(columns)
        ):
            raise ValueError(
                "selected_columns must be unique existing features excluding ID/target"
            )
        schema: object = value["output_schema"]
        if (
            not isinstance(schema, list)
            or not schema
            or any(
                not isinstance(c, dict)
                or set(c) != {"name", "dtype"}
                or any(not isinstance(c[k], str) or not c[k] for k in ("name", "dtype"))
                for c in schema
            )
        ):
            raise ValueError("output_schema requires nonempty name/dtype records")
        labels = [c["name"] for c in schema]
        if len(set(labels)) != len(labels) or partition["row_id"] in labels:
            raise ValueError("output_schema names must be unique and exclude row ID")
        for estimator in value["pipeline"].get_params(deep=True).values():
            if isinstance(estimator, OneHotEncoder) and isinstance(
                estimator.get_params(deep=False)["categories"], str
            ):
                raise ValueError("OneHotEncoder requires predeclared categories")

    return declarations


def fit_variant(
    root: Path,
    frame: pd.DataFrame,
    partition: dict[str, object],
    candidate: CandidateRequest,
    variant: FeatureVariant,
    rules: Sequence[Mapping[str, object]],
) -> tuple[Pipeline, dict[str, object], dict[str, object]]:
    """Fit one fresh pipeline through existing quality and classification APIs."""

    def fit(
        checked: pd.DataFrame, _: dict[str, object]
    ) -> tuple[Pipeline, dict[str, object]]:
        return fit_classifier(
            checked,
            project_root=root,
            candidate=candidate,
            estimator_bindings=ESTIMATOR_BINDINGS,
            preprocessing=variant["pipeline"],
            partition_record=partition,
            selected_columns=variant["selected_columns"],
            output_schema=cast(Sequence[Mapping[str, str]], variant["output_schema"]),
        )

    (pipeline, record), quality = run_validated_step(frame, fit, rules=rules)
    return pipeline, record, quality


def run(root: Path, uri: str, experiment: str, settings_path: str) -> dict[str, object]:
    """Fit and publish a controlled comparison into explicitly selected MLflow."""
    if not root.is_absolute() or not root.is_dir():
        raise ValueError("project-root must be an existing absolute directory")
    for name in (".feature-comparison", "features"):
        base = root / name
        if base.is_symlink() or (base.exists() and not base.is_dir()):
            raise ValueError(f"Unsafe or conflicting output parent: {name}")
    if not isinstance(uri, str) or not uri.strip():
        raise ValueError("tracking-uri must explicitly select a store")
    settings = read_settings(root, settings_path)
    frame = pd.read_csv(root / str(settings["source"]))
    partition = document(root / str(settings["split_record"]))
    provenance = document(root / str(settings["provenance"]))
    if cast(dict[str, object], provenance["configuration"])["effective"] != settings:
        raise ValueError(
            "Provenance effective configuration does not match consumed settings"
        )
    resolved = resolve_plan(ResolveRequest(root, Path(str(settings["experiment"]))))
    if resolved.plan_id is None:
        raise ValueError(f"Plan blocked: {resolved.diagnostics}")
    configuration = validate_configuration(
        ConfigurationRequest(root, resolved.plan_id, Path(str(settings["registry"])))
    )
    if configuration.validation_id is None:
        raise ValueError(f"Configuration blocked: {configuration.diagnostics}")
    candidate = CandidateRequest(
        root,
        configuration.validation_id,
        str(settings["algorithm"]),
        cast(dict[str, JSONValue], settings["parameters"]),
    )
    validated = validate_candidate(candidate)
    if validated.parameters is None:
        raise ValueError(f"Candidate blocked: {validated.diagnostics}")
    inspected = inspect_plan(project_root=root, plan_id=resolved.plan_id)
    if inspected.plan is None:
        raise ValueError("Resolved plan is not inspectable")
    effective = cast(dict[str, object], inspected.plan["effective"])
    evaluation = cast(dict[str, object], effective["evaluation"])
    if (settings["metric"], settings["direction"]) != (
        evaluation["metric"],
        evaluation["direction"],
    ):
        raise ValueError("Settings metric/direction disagree with strict evaluation")
    budget = cast(dict[str, int], effective["budget"])
    count = len(cast(list[str], settings["variants"]))
    if count > budget["max_total_trials"] or count > budget["max_trials_per_algorithm"]:
        raise ValueError("Selected variants exceed configured trial budget")
    if partition.get("layout") != "train_validation_test":
        raise ValueError("Comparison requires a separate validation partition")
    parts, current = create_partitions(
        frame,
        row_id=str(partition["row_id"]),
        target=str(partition["target"]),
        layout=cast(Literal["train_validation_test"], partition["layout"]),
        memberships=cast(Mapping[str, Sequence[str | int]], partition["memberships"]),
        protocol=cast(Mapping[str, object] | None, partition["protocol"]),
    )
    if current["source"] != partition["source"]:
        raise ValueError("Partition source identity is stale")
    declarations = selected_variants(
        cast(list[str], settings["variants"]), frame, partition
    )
    if any(n not in declarations for n in cast(list[str], settings["variants"])):
        raise ValueError("Unknown selected variant")
    reference_name = str(settings["reference"])
    names = [reference_name] + [
        n for n in cast(list[str], settings["variants"]) if n != reference_name
    ]
    client = MlflowClient(tracking_uri=uri)
    reference = client.create_run(experiment).info.run_id
    started = {reference: reference_name}
    stage = "reference fit"
    try:
        rows: list[dict[str, object]] = []
        pending: dict[
            str, tuple[dict[str, object], dict[str, object], dict[str, Path]]
        ] = {}
        protocols: list[dict[str, object]] = []
        for name in names:
            variant = declarations[name]
            run_id = (
                reference
                if name == reference_name
                else client.create_run(experiment).info.run_id
            )
            started[run_id] = name
            stage = "fit and validation scoring"
            pipeline, training, quality = fit_variant(
                root,
                frame,
                partition,
                candidate,
                variant,
                cast(Sequence[Mapping[str, object]], settings["quality_rules"]),
            )
            validation = parts["validation"]
            score_function = (
                accuracy_score if settings["metric"] == "accuracy" else zero_one_loss
            )
            score = float(
                score_function(
                    validation[str(partition["target"])],
                    pipeline.predict(validation[variant["selected_columns"]]),
                )
            )
            staging = root / ".feature-comparison" / reference / name
            staging.mkdir(parents=True, exist_ok=False)
            training_path = staging / "training.json"
            write_json(training_path, training)
            features = root / "features" / reference / name
            features.mkdir(parents=True, exist_ok=False)
            outputs = {"training": training_path}
            for part_name in ("train", "validation"):
                schema = variant["output_schema"]
                transformed = pipeline["preprocessing"].transform(
                    parts[part_name][variant["selected_columns"]]
                )
                labels = [c["name"] for c in schema]
                if isinstance(transformed, pd.DataFrame):
                    values = transformed.copy(deep=True)
                    values.columns = pd.Index(labels)
                else:
                    values = pd.DataFrame(transformed, columns=labels)
                values.insert(
                    0,
                    str(partition["row_id"]),
                    parts[part_name][str(partition["row_id"])].tolist(),
                )
                path = features / f"{part_name}_features.parquet"
                values.to_parquet(path, index=False)
                outputs[f"{part_name}_features"] = path
            stage = "derived DVC data"
            native(
                root,
                sys.executable,
                "-m",
                "dvc",
                "add",
                str(features.relative_to(root)),
            )
            pointer_path = features.with_name(features.name + ".dvc")
            pointer = yaml.safe_load(pointer_path.read_text())["outs"][0]
            pointer_copy = staging / "derived.dvc"
            pointer_copy.write_bytes(pointer_path.read_bytes())
            outputs["derived_dvc"] = pointer_copy
            native(
                root,
                sys.executable,
                "-m",
                "dvc",
                "status",
                str(pointer_path.relative_to(root)),
            )
            model = staging / "pipeline"
            stage = "model serialization"
            mlflow.sklearn.save_model(
                pipeline,
                str(model),
                serialization_format="skops",
                skops_trusted_types=["numpy.dtype", "sklearn.tree._tree.Tree"],
                pip_requirements=[
                    f"{n}=={version(n)}"
                    for n in ("scikit-learn", "numpy", "pandas", "skops", "mlflow")
                ],
            )
            stage = "model publication"
            if client.list_artifacts(run_id, "model/pipeline"):
                raise FileExistsError("model/pipeline already contains artifacts")
            client.log_artifacts(run_id, str(model), "model/pipeline")
            stage = "preprocessing publication"
            log_preprocessing(
                run_id=run_id,
                pipeline=pipeline["preprocessing"],
                record=cast(Mapping[str, object], training["preprocessing"]),
                provenance=provenance,
                project_root=root,
                tracking_uri=uri,
            )
            native_run = client.get_run(run_id)
            artifact_root = native_run.info.artifact_uri
            artifacts = {
                key: f"{artifact_root}/outputs/{key}/{path.name}"
                for key, path in outputs.items()
            }
            artifacts.update(
                {
                    "model": artifact_root + "/model/pipeline",
                    "preprocessing": artifact_root + "/preprocessing",
                    "provenance": artifact_root + "/provenance.json",
                }
            )
            delta = score - cast(float, rows[0]["score"]) if rows else 0.0
            row: dict[str, object] = {
                "variant": name,
                "run_id": run_id,
                "score": score,
                "raw_delta": delta,
                "adjusted_delta": delta
                if settings["direction"] == "maximize"
                else -delta,
                "outcome": "reference"
                if not rows
                else "tie"
                if delta == 0
                else "gain"
                if (delta if settings["direction"] == "maximize" else -delta) > 0
                else "regression",
                "outputs": {key: file_ref(root, path) for key, path in outputs.items()},
                "artifacts": artifacts,
                "derived_data": {
                    "output_path": features.relative_to(root).as_posix(),
                    "hash_name": pointer["hash"],
                    "hash_value": pointer[pointer["hash"]],
                    "metadata": file_ref(root, pointer_path),
                    "members": [
                        "train_features.parquet",
                        "validation_features.parquet",
                    ],
                },
            }
            rows.append(row)
            protocol = {
                key: training[key]
                for key in (
                    "algorithm",
                    "estimator_class",
                    "parameters",
                    "validation_id",
                )
            }
            protocols.append(protocol)
            parameters = {
                key: training[key]
                for key in (
                    "algorithm",
                    "estimator_class",
                    "parameters",
                    "parameter_origins",
                    "versions",
                    "fit_partition",
                )
            }
            parameters.update({"variant": name, "reference_run_id": reference})
            pending[run_id] = parameters, quality, outputs
            if run_id != reference:
                finalize(
                    root,
                    uri,
                    run_id,
                    provenance,
                    parameters,
                    quality,
                    outputs,
                    score,
                    str(settings["metric"]),
                    cast(list[str], settings["expected_outputs"]),
                )
        if any(protocol != protocols[0] for protocol in protocols):
            raise ValueError("Comparison protocol mismatch")
        summary = {
            "schema_version": "1.0",
            "reference": {"variant": reference_name, "run_id": reference},
            "source": partition["source"],
            "split_record": file_ref(root, root / str(settings["split_record"])),
            "estimator": protocols[0],
            "metric": settings["metric"],
            "direction": settings["direction"],
            "validation_membership": cast(dict[str, object], partition["memberships"])[
                "validation"
            ],
            "rows": rows,
        }
        stage = "comparison publication"
        summary_path = root / ".feature-comparison" / reference / "comparison.json"
        write_json(summary_path, summary)
        parameters, quality, outputs = pending[reference]
        outputs["comparison"] = summary_path
        result = finalize(
            root,
            uri,
            reference,
            provenance,
            parameters,
            quality,
            outputs,
            cast(float, rows[0]["score"]),
            str(settings["metric"]),
            [*cast(list[str], settings["expected_outputs"]), "comparison"],
        )
        for row in rows:
            print(
                f"{row['variant']}\t{row['score']}\t{row['adjusted_delta']}\t{row['outcome']}",
                file=sys.stderr,
            )
        return {
            "reference_run_id": reference,
            "variant_run_ids": {str(row["variant"]): row["run_id"] for row in rows},
            "comparison_artifact_uri": cast(dict[str, str], result["artifacts"])[
                "comparison"
            ],
        }

    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(
                f"feature comparison reference={reference}; stage={stage}; project_root={root}"
            )
            for run_id, name in started.items():
                try:
                    native_run = client.get_run(run_id)
                except (OSError, ValueError, MlflowException) as secondary:
                    error.add_note(f"Cannot inspect run {run_id}: {secondary}")
                    continue
                if (
                    native_run.info.status != "RUNNING"
                    or native_run.info.lifecycle_stage != "active"
                ):
                    continue
                diagnostic = (
                    root / ".feature-comparison" / reference / name / "failure.txt"
                )
                try:
                    diagnostic.parent.mkdir(parents=True, exist_ok=True)
                    diagnostic.write_text("".join(traceback.format_exception(error)))
                    error.add_note(f"Available diagnostic for {name}: {diagnostic}")
                    if not client.list_artifacts(run_id, "diagnostics"):
                        client.log_artifact(run_id, str(diagnostic), "diagnostics")
                except (OSError, ValueError, MlflowException) as secondary:
                    error.add_note(
                        f"Diagnostic retention failed for {run_id}: {secondary}"
                    )
                try:
                    client.set_tag(run_id, "process_exit_code", "1")
                    client.set_terminated(run_id, status="FAILED")
                except (OSError, ValueError, MlflowException) as secondary:
                    error.add_note(
                        f"Failed to record native FAILED status for {run_id}: {secondary}"
                    )


def finalize(
    root: Path,
    uri: str,
    run_id: str,
    provenance: dict[str, object],
    parameters: dict[str, object],
    quality: dict[str, object],
    outputs: dict[str, Path],
    score: float,
    metric: str,
    expected: list[str],
) -> dict[str, object]:
    """Publish existing outputs once, then finish the selected native run."""
    for name in expected:
        if name not in outputs:
            raise ValueError(f"Missing required output declaration: {name}")
        if not outputs[name].is_file():
            raise FileNotFoundError(outputs[name])
    return log_run_results(
        run_id=run_id,
        project_root=root,
        tracking_uri=uri,
        provenance=provenance,
        parameters=parameters,
        metrics={f"validation_{metric}": score},
        outputs={key: path.relative_to(root) for key, path in outputs.items()},
        expected_outputs=expected,
        process_exit_code=0,
        validation_passed=None
        if quality["status"] == "not_checked"
        else quality["status"] == "passed",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--tracking-uri", required=True)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--settings", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.project_root, args.tracking_uri, args.experiment_id, args.settings
            ),
            allow_nan=False,
        )
    )
