"""Record experiment results in explicitly selected native MLflow runs."""

import json
import re
import shutil
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

from .artifacts import require_available
from .provenance import (
    committed_references,
    dvc_references,
    environment_identity,
    provenance_schema,
)
from .results import output_file, validate_notebook, validate_results


def log_run_results(
    *,
    run_id: str,
    project_root: Path,
    tracking_uri: str,
    provenance: Mapping[str, object],
    parameters: Mapping[str, object],
    metrics: Mapping[str, float],
    outputs: Mapping[str, Path],
    expected_outputs: Sequence[str],
    process_exit_code: int,
    validation_passed: bool | None,
    executed_notebook: Path | None = None,
) -> dict[str, object]:
    """Record supplied results and finalize an existing native experiment run.

    Args:
        run_id: Existing native MLflow run identifier.
        project_root: Explicit absolute experiment project directory.
        tracking_uri: Explicit tracking store selected independently of active runs.
        provenance: Shared JSON experiment references.
        parameters: Supplied effective parameter values.
        metrics: Supplied finite metric values, not computed by this helper.
        outputs: Named project output files.
        expected_outputs: Names of required output files.
        process_exit_code: Observed project process exit code.
        validation_passed: Independent configured-validation outcome, or None.
        executed_notebook: Optional already-executed notebook artifact.

    Returns:
        Native run ID, artifact URIs, process exit code and validation status.

    Raises:
        TypeError: A declaration has an unsupported type or non-JSON value.
        ValueError: References, status values or finite-value checks are invalid.
        FileNotFoundError: Required references or outputs are unavailable.
        FileExistsError: Publication would overwrite a prior artifact.
        RuntimeError: The supplied project process exited nonzero.
        Exception: Native storage/logging failures propagate with run/stage notes.
            Available outputs remain inspectable and FAILED is recorded where
            the selected backend permits it; no atomic publication is promised.
    """
    client: MlflowClient | None = None
    eligible = False
    stage = "run selection"
    artifacts: dict[str, str] = {}
    try:
        if not isinstance(tracking_uri, str) or not tracking_uri.strip():
            raise ValueError("tracking_uri must explicitly select a store")
        client = MlflowClient(tracking_uri=tracking_uri)
        run = client.get_run(run_id)
        if run.info.status != "RUNNING" or run.info.lifecycle_stage != "active":
            raise ValueError(
                f"Run {run_id} must be active and RUNNING; found {run.info.status}"
            )
        eligible = True
        stage = "configuration"
        if not isinstance(project_root, Path):
            raise TypeError("project_root must be a Path")
        if not project_root.is_absolute() or not project_root.is_dir():
            raise ValueError("project_root must be an existing absolute directory")
        validate_results(
            parameters,
            metrics,
            outputs,
            expected_outputs,
            process_exit_code,
            validation_passed,
        )
        stage = "provenance schema"
        provenance_schema(provenance)
        stage = "committed references"
        committed_references(project_root, provenance)
        stage = "DVC integrity"
        dvc_references(project_root, provenance)
        stage = "installation identity"
        environment_identity(project_root, provenance)
        if executed_notebook is not None:
            stage = "notebook validation"
            validate_notebook(project_root / executed_notebook, provenance)
        experiment = cast(Mapping[str, object], provenance["experiment"])
        toolkit = cast(Mapping[str, object], provenance["toolkit"])
        installation = cast(Mapping[str, object], toolkit["installation"])
        client.set_tag(run_id, "experiment_commit", str(experiment["commit_sha"]))
        client.set_tag(run_id, "toolkit_version", str(installation["version"]))
        client.set_tag(
            run_id, "provenance_schema_version", str(provenance["schema_version"])
        )
        artifacts = {}
        stage = "shared provenance"
        existing = {item.path: item for item in client.list_artifacts(run_id)}
        if "provenance.json" in existing:
            if existing["provenance.json"].is_dir:
                raise FileExistsError("provenance.json is already a directory")
            previous = Path(client.download_artifacts(run_id, "provenance.json"))
            try:
                saved_provenance = json.loads(previous.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as decode_error:
                raise FileExistsError(
                    "Existing provenance.json is corrupt"
                ) from decode_error
            if saved_provenance != dict(provenance):
                raise FileExistsError("Conflicting shared provenance.json")
        else:
            with tempfile.TemporaryDirectory(prefix="agentic-ml-tracking-") as local:
                path = Path(local) / "provenance.json"
                path.write_text(
                    json.dumps(dict(provenance), allow_nan=False), encoding="utf-8"
                )
                client.log_artifact(run_id, str(path))
        artifacts["provenance"] = run.info.artifact_uri + "/provenance.json"
        stage = "parameters and metrics"
        for name, value in parameters.items():
            recorded = (
                json.dumps(
                    value, allow_nan=False, sort_keys=True, separators=(",", ":")
                )
                if isinstance(value, (dict, list))
                else value
            )
            client.log_param(run_id, name, recorded)
        for name, value in metrics.items():
            client.log_metric(run_id, name, value)
        validation_status = (
            "not_checked"
            if validation_passed is None
            else "passed"
            if validation_passed
            else "failed"
        )
        client.set_tag(run_id, "validation_status", validation_status)
        client.set_tag(run_id, "process_exit_code", str(process_exit_code))
        if executed_notebook is not None:
            stage = "notebook artifact"
            source = output_file(project_root, executed_notebook)
            require_available(client, run_id, "notebooks/executed.ipynb")
            with tempfile.TemporaryDirectory(prefix="agentic-ml-notebook-") as local:
                notebook = Path(local) / "executed.ipynb"
                shutil.copyfile(source, notebook)
                client.log_artifact(run_id, str(notebook), "notebooks")
            artifacts["notebook"] = run.info.artifact_uri + "/notebooks/executed.ipynb"
        stage = "output artifacts"
        for name, path in outputs.items():
            source = output_file(project_root, path)
            require_available(client, run_id, f"outputs/{name}")
            client.log_artifact(run_id, str(source), f"outputs/{name}")
            artifacts[name] = f"{run.info.artifact_uri}/outputs/{name}/{source.name}"
        if process_exit_code != 0:
            raise RuntimeError(f"Project process exited with code {process_exit_code}")
        stage = "finalization"
        client.set_terminated(run_id, status="FINISHED")
        return {
            "run_id": run_id,
            "artifacts": artifacts,
            "process_exit_code": process_exit_code,
            "validation_status": validation_status,
        }
    finally:
        error = sys.exception()
        if isinstance(error, Exception):
            error.add_note(
                f"tracking run_id={run_id}; stage={stage}; project_root={project_root}"
            )
            if eligible and client is not None:
                # Preserve every available explicit output without overwriting prior artifacts.
                for name, path in (
                    outputs.items() if isinstance(outputs, Mapping) else ()
                ):
                    if name in artifacts:
                        continue
                    if (
                        not isinstance(name, str)
                        or name in {"provenance", "notebook"}
                        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name) is None
                    ):
                        continue
                    try:
                        source = output_file(project_root, path)
                    except (OSError, ValueError, TypeError) as unavailable:
                        error.add_note(
                            f"Unavailable diagnostic/output {path}: {unavailable}"
                        )
                        continue
                    if source.is_file():
                        error.add_note(f"Available local diagnostic/output: {source}")
                        try:
                            prior = client.list_artifacts(run_id, f"outputs/{name}")
                            if not prior:
                                client.log_artifact(
                                    run_id, str(source), f"outputs/{name}"
                                )
                        except (
                            OSError,
                            ValueError,
                            MlflowException,
                        ) as diagnostic_error:
                            error.add_note(
                                f"Diagnostic retention failed: {diagnostic_error}"
                            )
                if isinstance(process_exit_code, int) and not isinstance(
                    process_exit_code, bool
                ):
                    try:
                        client.set_tag(
                            run_id, "process_exit_code", str(process_exit_code)
                        )
                    except (OSError, ValueError, MlflowException) as tag_error:
                        error.add_note(
                            f"Failed to record observed process exit: {tag_error}"
                        )
                try:
                    client.set_terminated(run_id, status="FAILED")
                except (OSError, ValueError, MlflowException) as status_error:
                    error.add_note(
                        f"Failed to record native FAILED status: {status_error}"
                    )
