"""US-18: inspect project-owned classification runs through native MLflow."""

import json
import re
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml
from mlflow import MlflowClient
from test_planning import planning_project as planning_project
from test_tracking import installed_project as installed_project
from test_training import (
    FOREST_PARAMETERS,
    TREE_PARAMETERS,
    source_frame,
)
from test_training import (
    training_project as training_project,
)
from tracking_support import command, file_ref

from agentic_ml.planning.models import JSONValue

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / ".dev-records/verification/us18-ip3-20261115-c74d76b"
pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("training_tracking")]


@dataclass
class TrainingCase:
    """An independent committed project and its explicit native store."""

    root: Path
    uri: str
    client: MlflowClient
    experiment: str
    provenance: dict[str, Any]

    def commit_inputs(self) -> None:
        """Renew genuine references after a deliberate project configuration edit."""
        command(self.root, "git", "add", ".")
        command(
            self.root, "git", "commit", "-m", "test: revise classification settings"
        )
        self.provenance["experiment"]["commit_sha"] = command(
            self.root, "git", "rev-parse", "HEAD"
        )
        self.provenance["experiment"]["code"] = [
            file_ref(self.root, name)
            for name in ("train.py", "training_bindings.py", "record_one.py")
        ]
        self.provenance["experiment"]["entrypoint"] = file_ref(self.root, "train.py")
        self.provenance["configuration"]["files"] = [
            file_ref(self.root, name)
            for name in (
                "brief.md",
                "search.yaml",
                "experiment.yaml",
                "registry.yaml",
                "training.json",
            )
        ]
        self.provenance["configuration"]["effective"] = json.loads(
            (self.root / "training.json").read_text()
        )
        (self.root / "run-provenance.json").write_text(json.dumps(self.provenance))

    def invoke(self, run_id: str | None = None) -> subprocess.CompletedProcess[str]:
        """Run the committed script with the project interpreter, away from cwd."""
        args = [
            str(self.root / ".venv/bin/python"),
            str(self.root / "train.py"),
            str(self.root),
            self.uri,
            self.experiment,
        ]
        if run_id is not None:
            self.provenance["experiment"]["entrypoint"] = file_ref(
                self.root, "record_one.py"
            )
            (self.root / "run-provenance.json").write_text(json.dumps(self.provenance))
            args = [
                str(self.root / ".venv/bin/python"),
                str(self.root / "record_one.py"),
                str(self.root),
                self.uri,
                run_id,
            ]
        result = subprocess.run(
            args,
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            timeout=180,
        )
        RECORDS.mkdir(parents=True, exist_ok=True)
        (RECORDS / (uuid.uuid4().hex + "-invocation.json")).write_text(
            json.dumps(
                {
                    "command": result.args,
                    "cwd": str(self.root.parent),
                    "project_root": str(self.root),
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "native_runs": [
                        run.to_dictionary()
                        for run in self.client.search_runs([self.experiment])
                    ],
                },
                indent=2,
            )
        )
        return result


@pytest.fixture
def training_case(
    installed_project: tuple[Path, dict[str, Any]],
    training_project: Path,
    tmp_path: Path,
) -> TrainingCase:
    """Commit real strict inputs, class bindings, DVC data and environment refs."""
    root, original = installed_project
    (root / "record_one.py").write_text(
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nfrom train import record_model\nfrom agentic_ml.planning import ResolveRequest, resolve_plan\nfrom agentic_ml.validation import ConfigurationRequest, CandidateRequest, validate_configuration\nplan=resolve_plan(ResolveRequest(root, Path('experiment.yaml')))\nconfiguration=validate_configuration(ConfigurationRequest(root, plan.plan_id, Path('registry.yaml')))\nassert configuration.validation_id is not None, configuration.diagnostics\nrecord_model(root,sys.argv[2],sys.argv[3],CandidateRequest(root,configuration.validation_id,'dummy_classifier',{}))\n"
    )
    for name in ("brief.md", "search.yaml", "experiment.yaml", "notebook.ipynb"):
        shutil.copyfile(training_project / name, root / name)
    for source, destination in (
        ("training_project.py", "train.py"),
        ("training_bindings.py", "training_bindings.py"),
    ):
        path = ROOT / "tests/installation" / source
        if path.exists():
            shutil.copyfile(path, root / destination)
    parameters: dict[str, dict[str, JSONValue]] = {
        "dummy_classifier": {"strategy": "most_frequent"},
        "decision_tree": TREE_PARAMETERS,
        "random_forest": FOREST_PARAMETERS,
    }
    (root / "search.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": {
                    name: {"fixed": values, "search": {}}
                    for name, values in parameters.items()
                },
            }
        )
    )
    kinds = {
        type(None): "null",
        bool: "boolean",
        int: "integer",
        float: "float",
        str: "string",
    }
    (root / "registry.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "algorithms": [
                    {
                        "id": name,
                        "interface_version": "1.0",
                        "tasks": ["classification"],
                        "adapter": {"id": "project_classifier", "version": "1.0"},
                        "library": {
                            "distribution": "scikit-learn",
                            "reference_version": "1.9.1",
                        },
                        "parameters": {
                            key: {"types": [kinds[type(value)]], "default": value}
                            for key, value in values.items()
                        },
                        "requires_non_null": [],
                    }
                    for name, values in parameters.items()
                    if name != "dummy_classifier"
                ],
            }
        )
    )
    brief = root / "brief.md"
    brief.write_text(
        brief.read_text()
        .replace("mode: use", "mode: compare")
        .replace(
            "- dummy_classifier", "- dummy_classifier\n- decision_tree\n- random_forest"
        )
        .replace("max_total_trials: 2", "max_total_trials: 3")
        .replace("churn", "label")
        .replace("age", "x")
        .replace("missing.csv", "data/input.csv")
        .replace("f1_macro", "accuracy")
    )
    config = yaml.safe_load((root / "experiment.yaml").read_text())
    config["data"] = ["data/input.csv"]
    (root / "experiment.yaml").write_text(yaml.safe_dump(config))
    settings = {"candidates": ["decision_tree"], "quality_rules": []}
    (root / "training.json").write_text(json.dumps(settings))
    frame = source_frame()
    frame.to_csv(root / "data/input.csv", index=False)
    command(
        root,
        str(root / ".venv/bin/python"),
        "-I",
        "-c",
        """
import json
from pathlib import Path
import pandas as pd
from agentic_ml.splitting import create_partitions
_, record = create_partitions(pd.read_csv('data/input.csv'), row_id='id', target='label',
    layout='train_validation_test',
    memberships={'train':[0,1,2,3], 'validation':[4,5], 'test':[6,7]})
Path('data/split.json').write_text(json.dumps(record, allow_nan=False))
""",
    )
    ignore = root / ".gitignore"
    ignore.write_text(
        ignore.read_text() + "\n.training/\nrun-provenance.json\n__pycache__/\n"
    )
    command(root, str(root / ".venv/bin/python"), "-m", "dvc", "add", "data")
    command(root, "git", "add", ".")
    command(root, "git", "commit", "-m", "test: commit classification project inputs")
    provenance = json.loads(json.dumps(original))
    provenance["experiment"] = {
        "commit_sha": command(root, "git", "rev-parse", "HEAD"),
        "entrypoint": file_ref(root, "train.py")
        if (root / "train.py").exists()
        else file_ref(root, "experiment.py"),
        "code": [
            file_ref(root, name)
            for name in ("train.py", "training_bindings.py", "record_one.py")
            if (root / name).exists()
        ],
    }
    provenance["configuration"] = {
        "files": [
            file_ref(root, name)
            for name in (
                "brief.md",
                "search.yaml",
                "experiment.yaml",
                "registry.yaml",
                "training.json",
            )
        ],
        "effective": settings,
    }
    pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
    for item in provenance["data"]:
        item["metadata"] = file_ref(root, "data.dvc")
        item["hash_value"] = pointer["md5"]
    provenance["split_record"] = file_ref(root, "data/split.json")
    (root / "run-provenance.json").write_text(json.dumps(provenance))
    store = tmp_path / uuid.uuid4().hex
    store.mkdir()
    uri = f"sqlite:///{store}/training.db"
    client = MlflowClient(tracking_uri=uri)
    experiment = client.create_experiment(
        "classification", artifact_location=(store / "artifacts").as_uri()
    )
    return TrainingCase(root, uri, client, experiment, provenance)


def test_records_baseline_before_candidate(training_case: TrainingCase) -> None:
    """AC-01/02/03/04: independent scores, one run each, shared lineage."""
    case = training_case
    result = case.invoke()
    assert result.returncode == 0, result.stdout + result.stderr
    answer = json.loads(result.stdout)
    baseline = case.client.get_run(answer["baseline"])
    candidate = case.client.get_run(answer["candidates"][0])
    assert len(case.client.search_runs([case.experiment])) == 2
    assert baseline.info.status == candidate.info.status == "FINISHED"
    assert baseline.info.end_time <= candidate.info.start_time
    assert baseline.data.metrics == {"validation_accuracy": 0.5}
    assert candidate.data.metrics == {"validation_accuracy": 1.0}
    assert candidate.data.params["baseline_run_id"] == baseline.info.run_id
    for run in (baseline, candidate):
        assert run.data.tags["validation_status"] == "not_checked"
        assert run.data.tags["process_exit_code"] == "0"
        saved = Path(case.client.download_artifacts(run.info.run_id, "provenance.json"))
        assert json.loads(saved.read_text()) == case.provenance
        assert case.client.list_artifacts(run.info.run_id, "model/pipeline")


def test_loads_native_models_and_records_project_forest(
    training_case: TrainingCase,
) -> None:
    """AC-03/04: fresh native inference and exact recorded fit/data identities."""
    case = training_case
    (case.root / "training.json").write_text(
        json.dumps(
            {"candidates": ["decision_tree", "random_forest"], "quality_rules": []}
        )
    )
    case.commit_inputs()
    result = case.invoke()
    assert result.returncode == 0, result.stdout + result.stderr
    answer = json.loads(result.stdout)
    assert len(case.client.search_runs([case.experiment])) == 3
    ids = [answer["baseline"], *answer["candidates"]]
    for run_id, algorithm, expected in zip(
        ids,
        ["dummy_classifier", "decision_tree", "random_forest"],
        [[0, 0], [0, 1], [0, 1]],
        strict=True,
    ):
        native = case.client.get_run(run_id)
        assert native.info.status == "FINISHED"
        path = Path(
            case.client.download_artifacts(run_id, "outputs/training/training.json")
        )
        record = json.loads(path.read_text())
        assert record["algorithm"] == algorithm
        assert record["fit_partition"] == "train"
        assert record["classes"] == [0, 1]
        assert (
            record["estimator_class"]["qualname"]
            == {
                "dummy_classifier": "DummyClassifier",
                "decision_tree": "DecisionTreeClassifier",
                "random_forest": "RandomForestClassifier",
            }[algorithm]
        )
        for field in ("parameters", "parameter_origins", "estimator_class", "versions"):
            assert json.loads(native.data.params[field]) == record[field]
        if algorithm == "random_forest":
            assert record["parameters"] == FOREST_PARAMETERS
        elif algorithm == "decision_tree":
            assert record["parameters"] == TREE_PARAMETERS
        else:
            assert record["parameters"] == {
                "strategy": "most_frequent",
                "constant": None,
                "random_state": None,
            }
        preprocessing = json.loads(
            Path(
                case.client.download_artifacts(run_id, "preprocessing/metadata.json")
            ).read_text()
        )
        assert preprocessing == record["preprocessing"]
        assert preprocessing["partition_record"] == json.loads(
            (case.root / "data/split.json").read_text()
        )
        assert preprocessing["selected_columns"] == ["x"]
        assert preprocessing["output_schema"] == [{"name": "x", "dtype": "float64"}]
        model = case.client.download_artifacts(run_id, "model/pipeline")
        flavor = yaml.safe_load((Path(model) / "MLmodel").read_text())["flavors"][
            "sklearn"
        ]
        assert flavor["serialization_format"] == "skops"
        assert flavor["skops_trusted_types"] == [
            "numpy.dtype",
            "sklearn.tree._tree.Tree",
        ]
        requirements = (Path(model) / "requirements.txt").read_text().splitlines()
        for name in ("scikit-learn", "numpy", "pandas"):
            assert f"{name}=={record['versions'][name]}" in requirements
        assert any(line.startswith("skops==") for line in requirements)
        assert any(line.startswith("mlflow==") for line in requirements)
        observed = json.loads(
            command(
                case.root,
                str(case.root / ".venv/bin/python"),
                "-I",
                "-c",
                """
import json, sys
from importlib.metadata import version
import mlflow.sklearn
import pandas as pd
import numpy as np
model = mlflow.sklearn.load_model(sys.argv[1])
np.testing.assert_allclose(model['preprocessing'].transform(pd.DataFrame({'x':[0.,100.]})),
                           [[0.],[100./np.sqrt(5.)]], rtol=1e-12, atol=1e-12)
print(json.dumps({'predictions':model.predict(pd.DataFrame({'x':[-2.,2.]})).tolist(),
    'parameters':model['estimator'].get_params(deep=False),
    'versions':{name:version(name) for name in ['agentic-ml','scikit-learn','numpy','pandas','pyarrow']}}))
""",
                model,
            )
        )
        assert observed["predictions"] == expected
        assert observed["parameters"] == record["parameters"]
        assert observed["versions"] == record["versions"]
        saved_provenance = json.loads(
            Path(case.client.download_artifacts(run_id, "provenance.json")).read_text()
        )
        assert saved_provenance == case.provenance
        for ref in (
            saved_provenance["experiment"]["code"]
            + saved_provenance["configuration"]["files"]
        ):
            assert ref == file_ref(case.root, ref["path"])
            assert (
                subprocess.check_output(
                    [
                        "git",
                        "show",
                        f"{saved_provenance['experiment']['commit_sha']}:{ref['path']}",
                    ],
                    cwd=case.root,
                )
                == (case.root / ref["path"]).read_bytes()
            )


def test_failed_baseline_blocks_candidate_comparison(
    training_case: TrainingCase,
) -> None:
    """AC-02/03/04: native baseline fit failure remains FAILED with context."""
    case = training_case
    path = case.root / "search.yaml"
    search = yaml.safe_load(path.read_text())
    search["algorithms"]["dummy_classifier"]["fixed"] = {
        "strategy": "constant",
        "constant": 9,
    }
    path.write_text(yaml.safe_dump(search))
    case.commit_inputs()
    result = case.invoke()
    assert result.returncode != 0
    assert (
        "ValueError: The constant target value must be present in the training data"
        in result.stderr
    )
    runs = case.client.search_runs([case.experiment])
    assert len(runs) == 1
    assert runs[0].info.status == "FAILED"
    assert "stage=fit" in result.stderr


def test_serialization_failure_preserves_training_output(
    training_case: TrainingCase,
) -> None:
    """AC-03/04: real unsupported native object fails without serializer fallback."""
    case = training_case
    path = case.root / "train.py"
    path.write_text(
        path.read_text().replace(
            '        stage = "model serialization"',
            '        import threading\n        pipeline.failure_fixture = threading.Lock()\n        stage = "model serialization"',
        )
    )
    case.commit_inputs()
    result = case.invoke()
    assert result.returncode != 0
    assert (
        "mlflow.exceptions.MlflowException: The saved sklearn model references untrusted types"
        in result.stderr
    )
    assert "['_thread.lock']" in result.stderr
    assert "stage=model serialization" in result.stderr
    runs = case.client.search_runs([case.experiment])
    assert len(runs) == 1 and runs[0].info.status == "FAILED"
    local = case.root / ".training" / runs[0].info.run_id
    assert (local / "training.json").is_file()
    assert (local / "failure.txt").is_file()
    assert not case.client.list_artifacts(runs[0].info.run_id, "model/pipeline")
    assert case.client.list_artifacts(runs[0].info.run_id, "diagnostics")


def test_model_collision_preserves_existing_artifacts(
    training_case: TrainingCase, tmp_path: Path
) -> None:
    """AC-03/04: a preexisting model namespace cannot be overwritten."""
    case = training_case
    run_id = case.client.create_run(case.experiment).info.run_id
    sentinel = tmp_path / "prior.txt"
    sentinel.write_text("previous model bytes")
    case.client.log_artifact(run_id, str(sentinel), "model/pipeline")
    result = case.invoke(run_id)
    assert result.returncode != 0
    assert "FileExistsError: model/pipeline already contains artifacts" in result.stderr
    assert case.client.get_run(run_id).info.status == "FAILED"
    assert (
        Path(
            case.client.download_artifacts(run_id, "model/pipeline/prior.txt")
        ).read_text()
        == "previous model bytes"
    )
    assert [
        item.path for item in case.client.list_artifacts(run_id, "model/pipeline")
    ] == ["model/pipeline/prior.txt"]
    assert (case.root / ".training" / run_id / "pipeline/MLmodel").is_file()


def test_training_output_collision_preserves_prior_bytes(
    training_case: TrainingCase, tmp_path: Path
) -> None:
    """AC-04: output conflicts fail after fit without overwriting prior outputs."""
    case = training_case
    run_id = case.client.create_run(case.experiment).info.run_id
    sentinel = tmp_path / "prior.json"
    sentinel.write_text('{"prior":true}')
    case.client.log_artifact(run_id, str(sentinel), "outputs/training")
    result = case.invoke(run_id)
    assert result.returncode != 0
    assert "FileExistsError" in result.stderr and "outputs/training" in result.stderr
    assert case.client.get_run(run_id).info.status == "FAILED"
    assert (
        Path(
            case.client.download_artifacts(run_id, "outputs/training/prior.json")
        ).read_text()
        == '{"prior":true}'
    )
    assert [
        item.path for item in case.client.list_artifacts(run_id, "outputs/training")
    ] == ["outputs/training/prior.json"]
    assert (case.root / ".training" / run_id / "training.json").is_file()


def test_missing_training_output_fails_run(training_case: TrainingCase) -> None:
    """AC-04: native model publication cannot hide a missing required output."""
    case = training_case
    path = case.root / "train.py"
    path.write_text(
        path.read_text().replace(
            '        stage = "result publication"',
            '        output.unlink()\n        stage = "result publication"',
        )
    )
    case.commit_inputs()
    result = case.invoke()
    assert result.returncode != 0
    assert "FileNotFoundError" in result.stderr and "training.json" in result.stderr
    assert "stage=result publication" in result.stderr
    runs = case.client.search_runs([case.experiment])
    assert len(runs) == 1 and runs[0].info.status == "FAILED"
    assert case.client.list_artifacts(runs[0].info.run_id, "model/pipeline")
    assert not case.client.list_artifacts(runs[0].info.run_id, "outputs/training")


def test_invalid_provenance_fails_without_candidate(
    training_case: TrainingCase,
) -> None:
    """AC-04: a fabricated committed code digest never becomes successful lineage."""
    case = training_case
    case.provenance["experiment"]["entrypoint"]["sha256"] = "sha256:" + "0" * 64
    (case.root / "run-provenance.json").write_text(json.dumps(case.provenance))
    result = case.invoke()
    assert result.returncode != 0
    assert "ValueError" in result.stderr and "train.py" in result.stderr
    runs = case.client.search_runs([case.experiment])
    assert len(runs) == 1 and runs[0].info.status == "FAILED"
    assert not case.client.list_artifacts(runs[0].info.run_id, "provenance.json")
    assert (case.root / ".training" / runs[0].info.run_id / "training.json").is_file()


def test_native_upload_failure_retains_model_and_original_error(
    training_case: TrainingCase, tmp_path: Path
) -> None:
    """AC-03/04: real filesystem failure preserves primary and secondary context."""
    case = training_case
    blocker = tmp_path / "blocked-artifacts"
    blocker.write_text("not a directory")
    case.experiment = case.client.create_experiment(
        "blocked", artifact_location=blocker.as_uri()
    )
    result = case.invoke()
    assert result.returncode != 0
    assert "NotADirectoryError" in result.stderr
    assert "stage=model publication" in result.stderr
    assert "Diagnostic retention failed" in result.stderr
    runs = case.client.search_runs([case.experiment])
    assert len(runs) == 1 and runs[0].info.status == "FAILED"
    assert blocker.read_text() == "not a directory"
    local = case.root / ".training" / runs[0].info.run_id
    assert (local / "pipeline/MLmodel").is_file()
    assert (local / "training.json").is_file()
    assert (local / "failure.txt").is_file()


@pytest.mark.parametrize("required", [True, False])
def test_configured_quality_is_distinct_from_process_status(
    training_case: TrainingCase, required: bool
) -> None:
    """AC-02/04: required failure blocks training; advisory failure permits it."""
    case = training_case
    (case.root / "training.json").write_text(
        json.dumps(
            {
                "candidates": ["decision_tree"],
                "quality_rules": [
                    {"id": "tiny", "kind": "row_count", "max": 0, "required": required}
                ],
            }
        )
    )
    case.commit_inputs()
    result = case.invoke()
    runs = case.client.search_runs([case.experiment])
    if required:
        assert result.returncode != 0
        assert (
            "DataQualityError: Required data-quality checks failed: tiny"
            in result.stderr
        )
        assert len(runs) == 1 and runs[0].info.status == "FAILED"
        assert not (
            case.root / ".training" / runs[0].info.run_id / "training.json"
        ).exists()
        assert not case.client.list_artifacts(runs[0].info.run_id, "model/pipeline")
    else:
        assert result.returncode == 0, result.stdout + result.stderr
        assert len(runs) == 2
        assert all(run.info.status == "FINISHED" for run in runs)
        assert all(run.data.tags["validation_status"] == "failed" for run in runs)
        assert sorted(run.data.metrics["validation_accuracy"] for run in runs) == [
            0.5,
            1.0,
        ]


def test_documented_recipe_runs_from_unrelated_cwd(
    installed_project: tuple[Path, dict[str, Any]],
) -> None:
    """AC-01–04: the literal copyable guide prepares and runs a real project."""
    root, _ = installed_project
    recipes = dict(
        re.findall(
            r"<!-- project-file: ([\w.]+) -->\n\n```python\n(.*?)\n```",
            (ROOT / "docs/classification-training.md").read_text(),
            flags=re.DOTALL,
        )
    )
    assert set(recipes) == {"prepare_training.py", "train.py", "training_bindings.py"}
    for name, code in recipes.items():
        (root / name).write_text(code + "\n")
    setup = json.loads(
        command(
            root.parent,
            str(root / ".venv/bin/python"),
            str(root / "prepare_training.py"),
            str(root),
        )
    )
    answer = json.loads(
        command(
            root.parent,
            str(root / ".venv/bin/python"),
            str(root / "train.py"),
            str(root),
            setup["tracking_uri"],
            setup["experiment_id"],
        )
    )
    observed = json.loads(
        command(
            root.parent,
            str(root / ".venv/bin/python"),
            "-I",
            "-c",
            """
import json, sys
from mlflow import MlflowClient
client=MlflowClient(tracking_uri=sys.argv[1])
answer=json.loads(sys.argv[2])
baseline=client.get_run(answer['baseline'])
assert baseline.info.status=='FINISHED'
assert baseline.data.metrics=={'validation_accuracy':0.5}
assert len(answer['candidates'])==2
for run_id in answer['candidates']:
    native=client.get_run(run_id)
    assert native.info.status=='FINISHED'
    assert native.data.metrics=={'validation_accuracy':1.0}
    assert native.data.params['baseline_run_id']==baseline.info.run_id
    assert baseline.info.end_time<=native.info.start_time
print(json.dumps({'baseline':baseline.to_dictionary(),
                  'candidates':[client.get_run(r).to_dictionary() for r in answer['candidates']]}))
""",
            setup["tracking_uri"],
            json.dumps(answer),
        )
    )
    assert observed["baseline"]["info"]["run_id"] == answer["baseline"]
