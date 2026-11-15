"""Prepare a tiny, committed feature-comparison example in an initialized project."""

import hashlib
import json
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from typing import cast

import pandas as pd
import yaml
from mlflow import MlflowClient

from agentic_ml.splitting import create_partitions

root = Path(sys.argv[1])
if not root.is_absolute() or not root.is_dir():
    raise ValueError("Supply an existing absolute initialized project root")


for name in (
    "registry.yaml",
    "search.yaml",
    "brief.md",
    "notebook.ipynb",
    "experiment.yaml",
    "comparison-settings.json",
    "data/input.csv",
    "data/split.json",
    "data.dvc",
    "run-provenance.json",
):
    if (root / name).exists():
        raise FileExistsError(f"Preparation refuses existing input: {name}")


def command(*args: str) -> str:
    """Run an explicit preparation command in the experiment root."""
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def ref(name: str) -> dict[str, str]:
    """Hash a project-owned file for the accepted provenance schema."""
    return {
        "path": name,
        "sha256": "sha256:" + hashlib.sha256((root / name).read_bytes()).hexdigest(),
    }


tree = {
    "ccp_alpha": 0.0,
    "class_weight": None,
    "criterion": "gini",
    "max_depth": 1,
    "max_features": None,
    "max_leaf_nodes": None,
    "min_impurity_decrease": 0.0,
    "min_samples_leaf": 1,
    "min_samples_split": 2,
    "min_weight_fraction_leaf": 0.0,
    "monotonic_cst": None,
    "random_state": 17,
    "splitter": "best",
}
parameters = {"decision_tree": tree}
kinds = {
    type(None): "null",
    bool: "boolean",
    int: "integer",
    float: "float",
    str: "string",
}
registry = {
    "schema_version": "1.0",
    "algorithms": [
        {
            "id": name,
            "interface_version": "1.0",
            "tasks": ["classification"],
            "adapter": {"id": "project_classifier", "version": "1.0"},
            "library": {"distribution": "scikit-learn", "reference_version": "1.9.1"},
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
(root / "registry.yaml").write_text(yaml.safe_dump(registry))
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
sections = {
    "Objective": {
        "schema_version": "1.0",
        "objective": "Compare authored features with a fixed tree.",
    },
    "Data": {
        "sources": ["data/input.csv"],
        "target": "label",
        "task_type": "classification",
    },
    "Features": {
        "include": ["constant", "signal", "misleading", "n", "count", "category"],
        "exclude": ["id"],
        "guidance": "Compare explicitly authored constant and signal features.",
        "availability": "At prediction.",
    },
    "Evaluation": {
        "metric": "accuracy",
        "direction": "maximize",
        "split": {
            "strategy": "random",
            "time_column": None,
            "group_column": None,
            "validation_fraction": 0.25,
            "test_fraction": 0.25,
            "seed": 17,
            "constraints": "Fixed disjoint memberships recorded in data/split.json.",
        },
    },
    "Algorithms": {"mode": "compare", "allowed": list(parameters)},
    "Budget": {
        "max_trials_per_algorithm": 4,
        "max_total_trials": 4,
        "max_runtime_seconds": 60,
        "max_memory_mb": None,
        "max_cost": None,
        "currency": None,
    },
}
(root / "brief.md").write_text(
    "# Experiment: Classification\n\n"
    + "\n".join(
        f"## {name}\n```yaml\n{yaml.safe_dump(value, sort_keys=False)}```\n"
        for name, value in sections.items()
    )
)
(root / "notebook.ipynb").write_text(
    json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []})
)
(root / "experiment.yaml").write_text(
    yaml.safe_dump(
        {
            "schema_version": "1.0",
            "id": "classification",
            "brief": "brief.md",
            "search_space": "search.yaml",
            "notebooks": ["notebook.ipynb"],
            "working_directory": ".",
            "data": ["data/input.csv"],
            "execution": {"status": "configured"},
        }
    )
)
settings = {
    "schema_version": "1.0",
    "experiment": "experiment.yaml",
    "registry": "registry.yaml",
    "source": "data/input.csv",
    "split_record": "data/split.json",
    "provenance": "run-provenance.json",
    "algorithm": "decision_tree",
    "parameters": {},
    "variants": ["reference", "signal", "unchanged", "misleading"],
    "reference": "reference",
    "metric": "accuracy",
    "direction": "maximize",
    "quality_rules": [],
    "expected_outputs": [
        "training",
        "train_features",
        "validation_features",
        "derived_dvc",
    ],
}
(root / "comparison-settings.json").write_text(json.dumps(settings))
(root / "data").mkdir(exist_ok=True)
(root / "data/input.csv").write_text(
    "id,constant,signal,misleading,n,count,category,label\n0,0.,-2.,-2.,1.,10.,a,0\n1,0.,-1.,-1.,,20.,b,0\n2,0.,1.,1.,3.,30.,a,1\n3,0.,2.,2.,5.,40.,b,1\n4,0.,-3.,3.,7.,15.,unseen,0\n5,0.,3.,-3.,1.,35.,b,1\n6,0.,-100.,100.,inf,inf,unseen,1\n7,0.,100.,-100.,-inf,-inf,a,0\n"
)
_, partition = create_partitions(
    pd.read_csv(root / "data/input.csv"),
    row_id="id",
    target="label",
    layout="train_validation_test",
    memberships={"train": [0, 1, 2, 3], "validation": [4, 5], "test": [6, 7]},
)
(root / "data/split.json").write_text(json.dumps(partition, allow_nan=False))
ignore = root / ".gitignore"
ignore.write_text(
    ignore.read_text() + "\n.feature-comparison/\nrun-provenance.json\n__pycache__/\n"
)
command(sys.executable, "-m", "dvc", "add", "data")
command("git", "add", ".")
command("git", "commit", "-m", "feat: prepare classification example")
identity = json.loads((root / ".agentic-ml/init.json").read_text())["environment"][
    "toolkit_identity"
]
pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
provenance = {
    "schema_version": "1.0",
    "experiment": {
        "commit_sha": command("git", "rev-parse", "HEAD"),
        "entrypoint": ref("compare_features.py"),
        "code": [
            ref("compare_features.py"),
            ref("feature_variants.py"),
            ref("prepare_comparison.py"),
        ],
    },
    "configuration": {
        "files": [
            ref(name)
            for name in (
                "brief.md",
                "search.yaml",
                "experiment.yaml",
                "registry.yaml",
                "comparison-settings.json",
            )
        ],
        "effective": settings,
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
        "libraries": {
            name: version(name)
            for name in (
                "agentic-ml",
                "mlflow",
                "dvc",
                "pandas",
                "pyarrow",
                "scikit-learn",
                "numpy",
                "skops",
            )
        },
    },
    "toolkit": {
        "installation": identity,
        "repository_url": identity.get("url"),
        "commit_sha": identity.get("revision"),
        "build_identity": None,
    },
}
(root / "run-provenance.json").write_text(json.dumps(provenance, allow_nan=False))
uri = f"sqlite:///{root}/.agentic-ml/comparison.db"
client = MlflowClient(tracking_uri=uri)
experiment = client.create_experiment(
    "comparison-"
    + str(cast(dict[str, object], provenance["experiment"])["commit_sha"]),
    artifact_location=(root / ".agentic-ml/comparison-artifacts").as_uri(),
)
print(json.dumps({"tracking_uri": uri, "experiment_id": experiment}))
