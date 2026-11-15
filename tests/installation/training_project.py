"""Train and record a baseline before authored classification candidates."""

import json
import sys
import traceback
from collections.abc import Mapping
from importlib.metadata import version
from pathlib import Path
from typing import cast

import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from training_bindings import ESTIMATOR_BINDINGS

from agentic_ml.data_quality import run_validated_step
from agentic_ml.planning import ResolveRequest, resolve_plan
from agentic_ml.splitting import create_partitions
from agentic_ml.tracking import log_preprocessing, log_run_results
from agentic_ml.training import fit_classifier
from agentic_ml.validation import (
    CandidateRequest,
    ConfigurationRequest,
    validate_configuration,
)


def record_model(
    root: Path,
    uri: str,
    run_id: str,
    candidate: CandidateRequest,
    *,
    baseline_run_id: str | None = None,
) -> None:
    """Fit, score and persist one model in the explicitly selected native run."""
    client = MlflowClient(tracking_uri=uri)
    native = client.get_run(run_id)
    if native.info.status != "RUNNING" or native.info.lifecycle_stage != "active":
        raise ValueError("Selected run must be active and RUNNING")
    stage = "inputs"
    try:
        settings = json.loads((root / "training.json").read_text())
        provenance = json.loads((root / "run-provenance.json").read_text())
        frame = pd.read_csv(root / "data/input.csv")
        partition = json.loads((root / "data/split.json").read_text())
        if partition["layout"] != "train_validation_test":
            raise ValueError(
                "Project comparison requires a separate validation partition"
            )

        def fit(
            checked: pd.DataFrame, _: dict[str, object]
        ) -> tuple[Pipeline, dict[str, object]]:
            return fit_classifier(
                checked,
                project_root=root,
                candidate=candidate,
                estimator_bindings=ESTIMATOR_BINDINGS,
                preprocessing=Pipeline([("scale", StandardScaler())]),
                partition_record=partition,
                selected_columns=["x"],
                output_schema=[{"name": "x", "dtype": "float64"}],
            )

        stage = "fit"
        (pipeline, record), quality = run_validated_step(
            frame, fit, rules=settings["quality_rules"]
        )
        partitions, _ = create_partitions(
            frame,
            row_id=partition["row_id"],
            target=partition["target"],
            layout=partition["layout"],
            memberships=partition["memberships"],
        )
        validation = partitions["validation"]
        predictions = pipeline.predict(validation[["x"]])
        score = float(accuracy_score(validation[partition["target"]], predictions))
        staging = root / ".training" / run_id
        staging.mkdir(parents=True, exist_ok=False)
        output = staging / "training.json"
        output.write_text(json.dumps(record, indent=2, allow_nan=False))
        model = staging / "pipeline"
        stage = "model serialization"
        mlflow.sklearn.save_model(
            pipeline,
            str(model),
            serialization_format="skops",
            skops_trusted_types=["numpy.dtype", "sklearn.tree._tree.Tree"],
            pip_requirements=[
                f"{name}=={version(name)}"
                for name in ("scikit-learn", "numpy", "pandas", "skops", "mlflow")
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
            record=cast(Mapping[str, object], record["preprocessing"]),
            provenance=provenance,
            project_root=root,
            tracking_uri=uri,
        )
        parameters = {
            key: record[key]
            for key in (
                "algorithm",
                "estimator_class",
                "parameters",
                "parameter_origins",
                "versions",
                "fit_partition",
            )
        }
        if baseline_run_id is not None:
            parameters["baseline_run_id"] = baseline_run_id
        stage = "result publication"
        log_run_results(
            run_id=run_id,
            project_root=root,
            tracking_uri=uri,
            provenance=provenance,
            parameters=parameters,
            metrics={"validation_accuracy": score},
            outputs={"training": output.relative_to(root)},
            expected_outputs=["training"],
            process_exit_code=0,
            validation_passed=None
            if quality["status"] == "not_checked"
            else quality["status"] == "passed",
        )
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(
                f"classification run_id={run_id}; stage={stage}; project_root={root}"
            )
            diagnostic = root / ".training" / run_id / "failure.txt"
            try:
                diagnostic.parent.mkdir(parents=True, exist_ok=True)
                diagnostic.write_text("".join(traceback.format_exception(error)))
                error.add_note(f"Available local diagnostic: {diagnostic}")
                if not client.list_artifacts(run_id, "diagnostics"):
                    client.log_artifact(run_id, str(diagnostic), "diagnostics")
            except (OSError, ValueError, MlflowException) as secondary:
                error.add_note(f"Diagnostic retention failed: {secondary}")
            try:
                client.set_tag(run_id, "process_exit_code", "1")
                client.set_terminated(run_id, status="FAILED")
            except (OSError, ValueError, MlflowException) as secondary:
                error.add_note(f"Failed to record native FAILED status: {secondary}")


def run(root: Path, uri: str, experiment: str) -> dict[str, str | list[str]]:
    """Resolve genuine strict inputs, then finish baseline before candidates."""
    if not root.is_absolute() or not root.is_dir():
        raise ValueError("root must be an existing absolute project directory")
    plan = resolve_plan(ResolveRequest(root, Path("experiment.yaml")))
    if plan.plan_id is None:
        raise ValueError(f"Plan resolution blocked: {plan.diagnostics}")
    configuration = validate_configuration(
        ConfigurationRequest(root, plan.plan_id, Path("registry.yaml"))
    )
    if configuration.validation_id is None:
        raise ValueError(f"Configuration blocked: {configuration.diagnostics}")
    client = MlflowClient(tracking_uri=uri)
    settings = json.loads((root / "training.json").read_text())
    baseline = client.create_run(experiment).info.run_id
    record_model(
        root,
        uri,
        baseline,
        CandidateRequest(root, configuration.validation_id, "dummy_classifier", {}),
    )
    candidates = []
    for algorithm in settings["candidates"]:
        run_id = client.create_run(experiment).info.run_id
        record_model(
            root,
            uri,
            run_id,
            CandidateRequest(root, configuration.validation_id, algorithm, {}),
            baseline_run_id=baseline,
        )
        candidates.append(run_id)
    return {"baseline": baseline, "candidates": candidates}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), sys.argv[2], sys.argv[3]), allow_nan=False))
