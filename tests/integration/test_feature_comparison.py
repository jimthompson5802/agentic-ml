"""US-14: copied feature recipes through installed public interfaces."""

import copy
import hashlib
import json
import os
import shutil
import subprocess
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest
import yaml
from mlflow import MlflowClient
from test_tracking import installed_project as installed_project
from tracking_support import command, file_ref

ROOT = Path(__file__).resolve().parents[2]
pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("feature_comparison")]


@dataclass
class ComparisonCase:
    """An independent installed project and explicitly selected native store."""

    root: Path
    uri: str
    experiment: str
    client: MlflowClient

    def invoke(
        self, *, uri_override: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Execute the exact copied recipe from an unrelated working directory."""
        args = [
            str(self.root / ".venv/bin/python"),
            str(self.root / "compare_features.py"),
            "--project-root",
            str(self.root),
            "--tracking-uri",
            self.uri if uri_override is None else uri_override,
            "--experiment-id",
            self.experiment,
            "--settings",
            "comparison-settings.json",
        ]
        env = dict(os.environ)
        env.pop("VIRTUAL_ENV", None)
        env.pop("PYTHONPATH", None)
        env["MLFLOW_TRACKING_URI"] = self.uri
        result = subprocess.run(
            args,
            cwd=self.root.parent,
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
        )
        pointer = ROOT / ".dev-records/us14-ip2-record"
        records = (
            Path(pointer.read_text())
            if pointer.is_file()
            else ROOT / ".dev-records/verification/us14-recipe-invocations"
        )
        (records / "logs").mkdir(parents=True, exist_ok=True)
        (records / "logs" / (uuid.uuid4().hex + "-recipe.json")).write_text(
            json.dumps(
                {
                    "command": args,
                    "cwd": str(self.root.parent),
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "provenance_snapshot": (
                        self.root / "run-provenance.json"
                    ).read_text(),
                    "inputs": {
                        name: (self.root / name).read_text()
                        for name in (
                            "compare_features.py",
                            "feature_variants.py",
                            "brief.md",
                            "search.yaml",
                            "registry.yaml",
                            "comparison-settings.json",
                            "data/split.json",
                            "data/input.csv",
                            "data.dvc",
                        )
                        if (self.root / name).is_file()
                    },
                    "native_runs": [
                        run.to_dictionary()
                        for run in self.client.search_runs([self.experiment])
                    ],
                },
                indent=2,
            )
        )
        return result

    def renew(self) -> None:
        """Commit deliberately revised project inputs and renew their references."""
        command(self.root, "git", "add", ".")
        command(
            self.root, "git", "commit", "--allow-empty", "-m", "test: revise comparison"
        )
        path = self.root / "run-provenance.json"
        provenance = json.loads(path.read_text())
        provenance["experiment"]["commit_sha"] = command(
            self.root, "git", "rev-parse", "HEAD"
        )
        for field in ("code",):
            provenance["experiment"][field] = [
                file_ref(self.root, ref["path"])
                for ref in provenance["experiment"][field]
            ]
        provenance["experiment"]["entrypoint"] = file_ref(
            self.root, "compare_features.py"
        )
        provenance["configuration"]["files"] = [
            file_ref(self.root, ref["path"])
            for ref in provenance["configuration"]["files"]
        ]
        provenance["configuration"]["effective"] = json.loads(
            (self.root / "comparison-settings.json").read_text()
        )
        path.write_text(json.dumps(provenance))


@pytest.fixture(scope="module")
def comparison_project(installed_project: tuple[Path, dict[str, Any]]) -> Path:
    """Prepare the literal recipe in a normal installed, initialized project."""
    root, _ = installed_project
    # These are owned synthetic files from the supplying fixture, not user data.
    for name in ("data/input.csv", "data/split.json", "data.dvc"):
        (root / name).unlink()
    example = ROOT / "examples/feature-comparison"
    assert (example / "prepare_comparison.py").is_file(), (
        "comparison preparation recipe is missing"
    )
    for source in example.glob("*.py"):
        shutil.copyfile(source, root / source.name)
    command(
        root.parent,
        str(root / ".venv/bin/python"),
        str(root / "prepare_comparison.py"),
        str(root),
    )
    return root


@pytest.fixture
def comparison_case(
    comparison_project: Path, tmp_path: Path
) -> Iterator[ComparisonCase]:
    """Restore declared inputs between cases; preserve failed owned workspaces."""
    root = comparison_project
    names = [
        "brief.md",
        "search.yaml",
        "experiment.yaml",
        "registry.yaml",
        "comparison-settings.json",
        "run-provenance.json",
        "feature_variants.py",
        "compare_features.py",
        "data/input.csv",
        "data/split.json",
        "data.dvc",
    ]
    saved = {name: (root / name).read_bytes() for name in names}
    store = tmp_path / uuid.uuid4().hex
    store.mkdir()
    uri = f"sqlite:///{store}/comparison.db"
    client = MlflowClient(tracking_uri=uri)
    experiment = client.create_experiment(
        "comparison", artifact_location=(store / "artifacts").as_uri()
    )
    case = ComparisonCase(root, uri, experiment, client)
    case.renew()
    try:
        yield case
    finally:
        for name, data in saved.items():
            (root / name).write_bytes(data)


def comparison(case: ComparisonCase) -> tuple[dict[str, Any], dict[str, Any]]:
    """Read public success output and the native comparison artifact."""
    result = case.invoke()
    assert result.returncode == 0, result.stdout + result.stderr
    answer = json.loads(result.stdout)
    summary = json.loads(
        Path(
            case.client.download_artifacts(
                answer["reference_run_id"], "outputs/comparison/comparison.json"
            )
        ).read_text()
    )
    return answer, summary


def test_reference_and_signal_have_literal_validation_gain(
    comparison_case: ComparisonCase,
) -> None:
    """AC-01/02/03/05: fixed tree and original split expose the feature gain."""
    case = comparison_case
    settings_path = case.root / "comparison-settings.json"
    settings = json.loads(settings_path.read_text())
    settings["variants"] = ["reference", "signal"]
    settings_path.write_text(json.dumps(settings))
    case.renew()
    before = copy.deepcopy(json.loads((case.root / "data/split.json").read_text()))
    answer, summary = comparison(case)
    assert summary["validation_membership"] == [4, 5]
    assert [
        (row["variant"], row["score"], row["adjusted_delta"], row["outcome"])
        for row in summary["rows"]
    ] == [("reference", 0.5, 0.0, "reference"), ("signal", 1.0, 0.5, "gain")]
    assert list(answer["variant_run_ids"]) == ["reference", "signal"]
    parameters = []
    for row, predictions in zip(summary["rows"], [[0, 0], [0, 1]], strict=True):
        run = case.client.get_run(row["run_id"])
        assert run.info.status == "FINISHED"
        assert run.data.metrics == {"validation_accuracy": row["score"]}
        training = json.loads(
            Path(
                case.client.download_artifacts(
                    row["run_id"], "outputs/training/training.json"
                )
            ).read_text()
        )
        parameters.append(training["parameters"])
        assert training["preprocessing"]["partition_record"] == before
        # Native model inference in its own environment, without toolkit source imports.
        model = case.client.download_artifacts(row["run_id"], "model/pipeline")
        observed = json.loads(
            command(
                case.root.parent,
                str(case.root / ".venv/bin/python"),
                "-I",
                "-c",
                "import sys,json,pandas as pd,mlflow.sklearn; p=mlflow.sklearn.load_model(sys.argv[1]); f=pd.read_csv(sys.argv[2]); print(json.dumps(p.predict(f.iloc[4:6][[sys.argv[3]]]).tolist()))",
                model,
                str(case.root / "data/input.csv"),
                "constant" if row["variant"] == "reference" else "signal",
            )
        )
        assert observed == predictions
    assert parameters[0] == parameters[1]
    signal = summary["rows"][1]
    frame = pd.read_parquet(case.root / signal["outputs"]["train_features"]["path"])
    assert frame["id"].tolist() == [0, 1, 2, 3]
    np.testing.assert_allclose(
        frame["signal"],
        [
            -1.2649110640673518,
            -0.6324555320336759,
            0.6324555320336759,
            1.2649110640673518,
        ],
        rtol=1e-12,
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "metric,direction,expected_scores",
    [
        ("accuracy", "maximize", [0.5, 1.0, 0.5, 0.0]),
        ("zero_one_loss", "minimize", [0.5, 0.0, 0.5, 1.0]),
    ],
)
def test_direction_aware_gain_tie_regression(
    comparison_case: ComparisonCase,
    metric: str,
    direction: str,
    expected_scores: list[float],
) -> None:
    """AC-03/05: all authored alternatives share a protocol in both directions."""
    case = comparison_case
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings.update(
        variants=["signal", "reference", "unchanged", "misleading"],
        metric=metric,
        direction=direction,
    )
    path.write_text(json.dumps(settings))
    brief = case.root / "brief.md"
    brief.write_text(
        brief.read_text()
        .replace("metric: accuracy", f"metric: {metric}")
        .replace("direction: maximize", f"direction: {direction}")
        .replace("max_total_trials: 2", "max_total_trials: 4")
        .replace("max_trials_per_algorithm: 2", "max_trials_per_algorithm: 4")
    )
    case.renew()
    _, summary = comparison(case)
    assert summary["metric"] == metric and summary["direction"] == direction
    assert [r["variant"] for r in summary["rows"]] == [
        "reference",
        "signal",
        "unchanged",
        "misleading",
    ]
    assert [r["score"] for r in summary["rows"]] == expected_scores
    assert [r["adjusted_delta"] for r in summary["rows"]] == [0.0, 0.5, 0.0, -0.5]
    assert [r["raw_delta"] for r in summary["rows"]] == (
        [0.0, 0.5, 0.0, -0.5] if metric == "accuracy" else [0.0, -0.5, 0.0, 0.5]
    )
    assert [r["outcome"] for r in summary["rows"]] == [
        "reference",
        "gain",
        "tie",
        "regression",
    ]


@pytest.mark.parametrize(
    "change",
    [
        "unknown_key",
        "empty",
        "duplicate",
        "unknown_variant",
        "missing_reference",
        "metric",
        "direction",
        "budget",
        "parameters",
        "expected_outputs",
    ],
)
def test_invalid_settings_create_no_runs(
    comparison_case: ComparisonCase, change: str
) -> None:
    """AC-03/05: reject unsupported comparison declarations before fitting."""
    case = comparison_case
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings["variants"] = ["reference"]
    if change == "unknown_key":
        settings["unexpected"] = True
    elif change == "empty":
        settings["variants"] = []
    elif change == "duplicate":
        settings["variants"] = ["reference", "reference"]
    elif change == "unknown_variant":
        settings["variants"] = ["reference", "unknown"]
    elif change == "missing_reference":
        settings["variants"] = ["signal"]
    elif change == "metric":
        settings["metric"] = "unsupported"
    elif change == "direction":
        settings["direction"] = "minimize"
    elif change == "parameters":
        settings["parameters"] = {"max_depth": 99}
    elif change == "expected_outputs":
        settings["expected_outputs"] = []
    elif change == "budget":
        settings["variants"] = ["reference", "signal"]
        brief = case.root / "brief.md"
        brief.write_text(
            brief.read_text()
            .replace("max_total_trials: 4", "max_total_trials: 1")
            .replace("max_trials_per_algorithm: 4", "max_trials_per_algorithm: 1")
        )
    path.write_text(json.dumps(settings))
    case.renew()
    result = case.invoke()
    assert result.returncode != 0, result.stdout
    assert case.client.search_runs([case.experiment]) == []


@pytest.mark.parametrize(
    "mode", ["duplicate_name", "empty_name", "not_list", "selected_pipeline"]
)
def test_invalid_factory_declarations_create_no_runs(
    comparison_case: ComparisonCase, mode: str
) -> None:
    """AC-01/05: the agreed factory validates global names and selected payloads."""
    case = comparison_case
    path = case.root / "feature_variants.py"
    modifications = {
        "duplicate_name": "return original + [original[0]]",
        "empty_name": "return original + [{'name': ''}]",
        "not_list": "return tuple(original)",
        "selected_pipeline": "original[0]['pipeline'] = 42; return original",
    }
    path.write_text(
        path.read_text()
        + "\n_factory = get_variants\ndef get_variants():\n    original = _factory()\n    "
        + modifications[mode]
        + "\n"
    )
    case.renew()
    result = case.invoke()
    assert result.returncode != 0, result.stdout
    assert case.client.search_runs([case.experiment]) == []


def test_unselected_payload_is_not_validated_and_factories_are_fresh(
    comparison_case: ComparisonCase,
) -> None:
    """AC-01/05: valid selection ignores unused payloads and never fits declarations."""
    case = comparison_case
    path = case.root / "feature_variants.py"
    path.write_text(
        path.read_text()
        + "\n_factory = get_variants\ndef get_variants():\n    return _factory() + [{'name': 'unused', 'pipeline': 42}]\n"
    )
    settings_path = case.root / "comparison-settings.json"
    settings = json.loads(settings_path.read_text())
    settings["variants"] = ["reference", "signal"]
    settings_path.write_text(json.dumps(settings))
    case.renew()
    command(
        case.root,
        str(case.root / ".venv/bin/python"),
        "-c",
        "from feature_variants import get_variants; a=get_variants(); b=get_variants(); assert a is not b; assert all(x['pipeline'] is not y['pipeline'] for x,y in zip(a[:-1],b[:-1])); assert not hasattr(a[0]['pipeline']['scale'],'mean_')",
    )
    _, summary = comparison(case)
    assert [r["variant"] for r in summary["rows"]] == ["reference", "signal"]


@pytest.mark.parametrize(
    "variant,expected_numeric",
    [
        ("mixed_scaled", [-1.414213562373095, 0.0, 0.0, 1.414213562373095]),
        ("mixed_unscaled", [1.0, 3.0, 3.0, 5.0]),
    ],
)
def test_mixed_columns_have_literal_schema_and_train_only_state(
    comparison_case: ComparisonCase,
    variant: str,
    expected_numeric: list[float],
) -> None:
    """AC-01/02/04: numeric groups and predeclared encoding retain row alignment."""
    case = comparison_case
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings["variants"] = ["reference", variant]
    path.write_text(json.dumps(settings))
    case.renew()
    _, summary = comparison(case)
    row = summary["rows"][1]
    assert row["score"] == 1.0 and row["outcome"] == "gain"
    train = pd.read_parquet(case.root / row["outputs"]["train_features"]["path"])
    assert list(train.columns) == ["id", "n_value", "count_value", "is_a", "is_b"]
    assert train["id"].tolist() == [0, 1, 2, 3]
    np.testing.assert_allclose(
        train["n_value"], expected_numeric, rtol=1e-12, atol=1e-12
    )
    np.testing.assert_allclose(
        train[["count_value", "is_a", "is_b"]],
        [[10.0, 1.0, 0.0], [20.0, 0.0, 1.0], [30.0, 1.0, 0.0], [40.0, 0.0, 1.0]],
        rtol=0,
        atol=0,
    )
    assert train.dtypes.astype(str).tolist() == [
        "int64",
        "float64",
        "float64",
        "float64",
        "float64",
    ]
    validation = pd.read_parquet(
        case.root / row["outputs"]["validation_features"]["path"]
    )
    assert validation["id"].tolist() == [4, 5]
    np.testing.assert_allclose(
        validation[["count_value", "is_a", "is_b"]],
        [[15.0, 0.0, 0.0], [35.0, 0.0, 1.0]],
        rtol=0,
        atol=0,
    )
    np.testing.assert_allclose(
        validation["n_value"],
        [2.82842712474619, -1.414213562373095]
        if variant == "mixed_scaled"
        else [7.0, 1.0],
        rtol=1e-12,
        atol=1e-12,
    )
    # Final-test infinities would fail native transformation if accidentally used.
    original = pd.read_csv(case.root / "data/input.csv")
    assert np.isinf(original.iloc[6:]["n"]).all()
    metadata = json.loads(
        Path(
            case.client.download_artifacts(row["run_id"], "preprocessing/metadata.json")
        ).read_text()
    )
    assert metadata["selected_columns"] == ["n", "count", "category"]
    assert [c["name"] for c in metadata["output_schema"]] == [
        "n_value",
        "count_value",
        "is_a",
        "is_b",
    ]


@pytest.mark.parametrize(
    "mode",
    [
        "two_way",
        "stale_source",
        "overlap",
        "target",
        "missing_column",
        "empty_schema",
        "auto_categories",
    ],
)
def test_invalid_data_and_feature_boundaries_create_no_runs(
    comparison_case: ComparisonCase, mode: str
) -> None:
    """AC-01/02/04: reject invalid split and feature declarations before fitting."""
    case = comparison_case
    if mode in {"two_way", "overlap"}:
        path = case.root / "data/split.json"
        split = json.loads(path.read_text())
        if mode == "two_way":
            split["layout"] = "train_test"
            split["memberships"] = {"train": [0, 1, 2, 3], "test": [4, 5, 6, 7]}
        else:
            split["memberships"]["validation"] = [0, 5]
        path.write_text(json.dumps(split))
    elif mode == "stale_source":
        path = case.root / "data/input.csv"
        frame = pd.read_csv(path)
        frame.loc[0, "signal"] = -99.0
        frame.to_csv(path, index=False)
    else:
        path = case.root / "feature_variants.py"
        if mode == "auto_categories":
            path.write_text(
                path.read_text().replace('categories=[["a", "b"]]', 'categories="auto"')
            )
            config = case.root / "comparison-settings.json"
            settings = json.loads(config.read_text())
            settings["variants"] = ["reference", "mixed_scaled"]
            config.write_text(json.dumps(settings))
        else:
            mutation = {
                "target": "v['selected_columns'] = ['label']",
                "missing_column": "v['selected_columns'] = ['absent']",
                "empty_schema": "v['output_schema'] = []",
            }[mode]
            path.write_text(
                path.read_text()
                + "\n_factory = get_variants\ndef get_variants():\n    values = _factory()\n    for v in values:\n        if v['name'] == 'reference':\n            "
                + mutation
                + "\n    return values\n"
            )
    case.renew()
    result = case.invoke()
    assert result.returncode != 0, result.stdout
    assert case.client.search_runs([case.experiment]) == []


@pytest.mark.parametrize("failure", ["later_transform", "artifact_storage"])
def test_native_failure_retains_available_results_and_failed_status(
    comparison_case: ComparisonCase,
    tmp_path: Path,
    failure: str,
) -> None:
    """AC-02/04: real native failures preserve prior successes and diagnostics."""
    case = comparison_case
    if failure == "later_transform":
        source = case.root / "data/input.csv"
        frame = pd.read_csv(source)
        frame.loc[4, "misleading"] = np.inf
        frame.to_csv(source, index=False)
        command(
            case.root,
            str(case.root / ".venv/bin/python"),
            "-I",
            "-c",
            "import json,pandas as pd; from pathlib import Path; from agentic_ml.splitting import create_partitions; _,r=create_partitions(pd.read_csv('data/input.csv'),row_id='id',target='label',layout='train_validation_test',memberships={'train':[0,1,2,3],'validation':[4,5],'test':[6,7]}); Path('data/split.json').write_text(json.dumps(r))",
        )
        command(
            case.root, str(case.root / ".venv/bin/python"), "-m", "dvc", "add", "data"
        )
        path = case.root / "run-provenance.json"
        provenance = json.loads(path.read_text())
        pointer = yaml.safe_load((case.root / "data.dvc").read_text())["outs"][0]
        for item in provenance["data"]:
            item["metadata"] = file_ref(case.root, "data.dvc")
            item["hash_value"] = pointer["md5"]
        provenance["split_record"] = file_ref(case.root, "data/split.json")
        path.write_text(json.dumps(provenance))
        path = case.root / "comparison-settings.json"
        settings = json.loads(path.read_text())
        settings["variants"] = ["reference", "signal", "misleading"]
        path.write_text(json.dumps(settings))
    else:
        blocker = tmp_path / "blocked-artifacts"
        blocker.write_text("prior bytes")
        case.experiment = case.client.create_experiment(
            "blocked", artifact_location=blocker.as_uri()
        )
    case.renew()
    result = case.invoke()
    assert result.returncode != 0
    assert not result.stdout.strip()
    runs = case.client.search_runs([case.experiment])
    if failure == "later_transform":
        assert "infinity" in result.stderr
        assert sorted(r.info.status for r in runs) == ["FAILED", "FAILED", "FINISHED"]
        finished = next(r for r in runs if r.info.status == "FINISHED")
        assert finished.data.params["variant"] == "signal"
        assert finished.data.metrics == {"validation_accuracy": 1.0}
    else:
        assert "NotADirectoryError" in result.stderr
        assert len(runs) == 1 and runs[0].info.status == "FAILED"
        assert blocker.read_text() == "prior bytes"
    reference = min(runs, key=lambda r: r.info.start_time)
    staging = case.root / ".feature-comparison" / reference.info.run_id
    assert list(staging.rglob("training.json"))
    assert list(staging.rglob("failure.txt"))
    assert not case.client.list_artifacts(reference.info.run_id, "outputs/comparison")


def test_native_artifacts_and_dvc_pointers_match_committed_protocol(
    comparison_case: ComparisonCase,
) -> None:
    """AC-02/03/04: inspect real outputs, fitted artifacts, lineage and ordering."""
    case = comparison_case
    commit = command(case.root, "git", "rev-parse", "HEAD")
    answer, summary = comparison(case)
    assert set(summary) == {
        "schema_version",
        "reference",
        "source",
        "split_record",
        "estimator",
        "metric",
        "direction",
        "validation_membership",
        "rows",
    }
    assert summary["schema_version"] == "1.0"
    reference = case.client.get_run(answer["reference_run_id"])
    for row in summary["rows"]:
        assert set(row) == {
            "variant",
            "run_id",
            "score",
            "raw_delta",
            "adjusted_delta",
            "outcome",
            "outputs",
            "artifacts",
            "derived_data",
        }
        run = case.client.get_run(row["run_id"])
        assert run.info.status == "FINISHED"
        assert run.data.tags["validation_status"] == "not_checked"
        assert run.data.params["reference_run_id"] == reference.info.run_id
        assert reference.info.start_time <= run.info.start_time
        assert run.info.end_time <= reference.info.end_time
        for logical, ref in row["outputs"].items():
            path = case.root / ref["path"]
            assert (
                "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
                == ref["sha256"]
            )
            relative = f"outputs/{logical}/{path.name}"
            assert row["artifacts"][logical] == run.info.artifact_uri + "/" + relative
            assert (
                Path(
                    case.client.download_artifacts(row["run_id"], relative)
                ).read_bytes()
                == path.read_bytes()
            )
        training = json.loads(
            (case.root / row["outputs"]["training"]["path"]).read_text()
        )
        assert {key: training[key] for key in summary["estimator"]} == summary[
            "estimator"
        ]
        assert (
            training["preprocessing"]["partition_record"]["source"] == summary["source"]
        )
        metadata = json.loads(
            Path(
                case.client.download_artifacts(
                    row["run_id"], "preprocessing/metadata.json"
                )
            ).read_text()
        )
        assert metadata == training["preprocessing"]
        dvc = row["derived_data"]
        pointer_path = case.root / dvc["metadata"]["path"]
        pointer = yaml.safe_load(pointer_path.read_text())["outs"][0]
        assert pointer[dvc["hash_name"]] == dvc["hash_value"]
        assert (
            json.loads(
                command(
                    case.root,
                    str(case.root / ".venv/bin/python"),
                    "-m",
                    "dvc",
                    "status",
                    "--json",
                    dvc["metadata"]["path"],
                )
            )
            == {}
        )
        provenance = json.loads(
            Path(
                case.client.download_artifacts(row["run_id"], "provenance.json")
            ).read_text()
        )
        assert provenance == json.loads((case.root / "run-provenance.json").read_text())
        assert provenance["experiment"]["commit_sha"] == commit
        for ref in (
            provenance["experiment"]["code"]
            + provenance["configuration"]["files"]
            + [provenance["environment"]["lockfile"]]
        ):
            assert (
                "sha256:"
                + hashlib.sha256((case.root / ref["path"]).read_bytes()).hexdigest()
                == ref["sha256"]
            )
            content = subprocess.run(
                ["git", "show", f"{commit}:{ref['path']}"],
                cwd=case.root,
                capture_output=True,
                check=True,
            ).stdout
            assert content == (case.root / ref["path"]).read_bytes()
    assert command(case.root, "git", "rev-parse", "HEAD") == commit


@pytest.mark.parametrize(
    "damage",
    [
        "missing_output",
        "model_collision",
        "missing_dvc",
        "bad_provenance",
        "missing_source",
    ],
)
def test_missing_or_conflicting_evidence_never_completes(
    comparison_case: ComparisonCase, damage: str
) -> None:
    """AC-04: damage real project files/native destinations without toolkit mocks."""
    case = comparison_case
    path = case.root / "compare_features.py"
    if damage == "missing_output":
        source = path.read_text()
        needle = '        outputs["comparison"] = summary_path'
        assert needle in source
        path.write_text(
            source.replace(needle, '        outputs["training"].unlink()\n' + needle)
        )
    elif damage == "model_collision":
        source = path.read_text()
        needle = '            stage = "model publication"'
        assert needle in source
        path.write_text(
            source.replace(
                needle,
                needle
                + '\n            client.log_artifact(run_id, str(training_path), "model/pipeline")',
            )
        )
    elif damage == "missing_dvc":
        (case.root / "data.dvc").unlink()
    elif damage == "missing_source":
        (case.root / "data/input.csv").unlink()
    case.renew()
    if damage == "bad_provenance":
        path = case.root / "run-provenance.json"
        provenance = json.loads(path.read_text())
        provenance["experiment"]["code"][0]["sha256"] = "sha256:" + "0" * 64
        path.write_text(json.dumps(provenance))
    result = case.invoke()
    assert result.returncode != 0 and not result.stdout.strip()
    runs = case.client.search_runs([case.experiment])
    if damage == "missing_source":
        assert not runs
        return
    assert runs and any(r.info.status == "FAILED" for r in runs)
    assert not any(r.info.status == "RUNNING" for r in runs)
    reference = min(runs, key=lambda r: r.info.start_time)
    assert not case.client.list_artifacts(reference.info.run_id, "outputs/comparison")
    if damage == "model_collision":
        saved = Path(
            case.client.download_artifacts(
                reference.info.run_id, "model/pipeline/training.json"
            )
        )
        local = (
            case.root
            / ".feature-comparison"
            / reference.info.run_id
            / "reference/training.json"
        )
        assert saved.read_bytes() == local.read_bytes()
        assert "FileExistsError" in result.stderr


def test_effective_provenance_must_match_consumed_settings(
    comparison_case: ComparisonCase,
) -> None:
    """AC-02/04: a valid-looking provenance document cannot misdescribe this run."""
    case = comparison_case
    path = case.root / "run-provenance.json"
    provenance = json.loads(path.read_text())
    provenance["configuration"]["effective"]["variants"] = ["reference"]
    path.write_text(json.dumps(provenance))
    result = case.invoke()
    assert result.returncode != 0, result.stdout
    assert case.client.search_runs([case.experiment]) == []


def test_variant_names_with_dots_keep_native_dvc_pointer_names(
    comparison_case: ComparisonCase,
) -> None:
    """AC-02/05: safe authored names retain their full native output identity."""
    case = comparison_case
    path = case.root / "feature_variants.py"
    path.write_text(
        path.read_text().replace(
            '("reference", "constant")', '("reference.v1", "constant")'
        )
    )
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings.update(reference="reference.v1", variants=["reference.v1", "signal"])
    path.write_text(json.dumps(settings))
    case.renew()
    _, summary = comparison(case)
    assert summary["rows"][0]["derived_data"]["metadata"]["path"].endswith(
        "/reference.v1.dvc"
    )


def test_empty_tracking_uri_never_falls_back_to_ambient_store(
    comparison_case: ComparisonCase,
) -> None:
    """AC-02/04: the explicit-store contract rejects blank URI before side effects."""
    case = comparison_case
    result = case.invoke(uri_override="")
    assert result.returncode != 0
    assert "tracking-uri must explicitly select a store" in result.stderr
    assert case.client.search_runs([case.experiment]) == []


@pytest.mark.parametrize("required", [True, False])
def test_quality_outcome_remains_distinct_from_process_success(
    comparison_case: ComparisonCase, required: bool
) -> None:
    """AC-02/04: delegate required/advisory rules without confusing model quality."""
    case = comparison_case
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings.update(
        variants=["reference", "signal"],
        quality_rules=[
            {"id": "tiny", "kind": "row_count", "max": 0, "required": required}
        ],
    )
    path.write_text(json.dumps(settings))
    case.renew()
    result = case.invoke()
    runs = case.client.search_runs([case.experiment])
    if required:
        assert result.returncode != 0 and "DataQualityError" in result.stderr
        assert len(runs) == 1 and runs[0].info.status == "FAILED"
        assert not case.client.list_artifacts(runs[0].info.run_id, "model/pipeline")
    else:
        assert result.returncode == 0, result.stderr
        assert len(runs) == 2 and all(r.info.status == "FINISHED" for r in runs)
        assert all(r.data.tags["validation_status"] == "failed" for r in runs)
        assert sorted(r.data.metrics["validation_accuracy"] for r in runs) == [0.5, 1.0]


def test_preparation_refuses_existing_inputs_without_rewriting(
    comparison_case: ComparisonCase,
) -> None:
    """AC-04: repeating explicit preparation preserves existing project inputs."""
    case = comparison_case
    paths = [
        case.root / name
        for name in (
            "comparison-settings.json",
            "brief.md",
            "data/input.csv",
            "data/split.json",
            "uv.lock",
        )
    ]
    before = {str(p): p.read_bytes() for p in paths}
    result = subprocess.run(
        [
            str(case.root / ".venv/bin/python"),
            str(case.root / "prepare_comparison.py"),
            str(case.root),
        ],
        cwd=case.root.parent,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert (
        result.returncode != 0 and "Preparation refuses existing input" in result.stderr
    )
    assert {str(p): p.read_bytes() for p in paths} == before


def test_symlink_output_parent_is_rejected_before_writing(
    comparison_case: ComparisonCase, tmp_path: Path
) -> None:
    """AC-04: an unsafe output parent cannot redirect generated project files."""
    case = comparison_case
    output = case.root / ".feature-comparison"
    backup = case.root / (".feature-comparison-saved-" + uuid.uuid4().hex)
    existed = output.exists()
    if existed:
        output.rename(backup)
    outside = tmp_path / "outside"
    outside.mkdir()
    output.symlink_to(outside, target_is_directory=True)
    try:
        result = case.invoke()
        assert result.returncode != 0
        assert list(outside.iterdir()) == []
        assert case.client.search_runs([case.experiment]) == []
    finally:
        output.unlink()
        if existed:
            backup.rename(output)


def test_pandas_outputs_use_project_schema_names_by_position(
    comparison_case: ComparisonCase,
) -> None:
    """AC-01/02/04: labeling pandas output preserves values instead of aligning names."""
    case = comparison_case
    path = case.root / "feature_variants.py"
    path.write_text(
        path.read_text()
        + "\n_factory = get_variants\ndef get_variants():\n    values = _factory()\n    for v in values:\n        if v['name'] == 'mixed_scaled':\n            v['pipeline'].set_output(transform='pandas')\n    return values\n"
    )
    path = case.root / "comparison-settings.json"
    settings = json.loads(path.read_text())
    settings["variants"] = ["reference", "mixed_scaled"]
    path.write_text(json.dumps(settings))
    case.renew()
    _, summary = comparison(case)
    row = summary["rows"][1]
    values = pd.read_parquet(case.root / row["outputs"]["train_features"]["path"])
    assert values["id"].tolist() == [0, 1, 2, 3]
    assert list(values.columns) == ["id", "n_value", "count_value", "is_a", "is_b"]
    np.testing.assert_allclose(
        values.iloc[:, 1:],
        [
            [-1.414213562373095, 10.0, 1.0, 0.0],
            [0.0, 20.0, 0.0, 1.0],
            [0.0, 30.0, 1.0, 0.0],
            [1.414213562373095, 40.0, 0.0, 1.0],
        ],
        rtol=1e-12,
        atol=1e-12,
    )
