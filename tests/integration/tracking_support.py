"""Separate installed experiment fixture support for public tracking checks."""

import hashlib
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlflow import MlflowClient

PROBE = """
import json, sys
from pathlib import Path
from agentic_ml.tracking import log_run_results
args=json.load(sys.stdin)
ambient=args.pop('_ambient',None)
if ambient is not None:
    import mlflow
    mlflow.set_tracking_uri(ambient['uri'])
    mlflow.start_run(run_id=ambient['run_id'])
args['project_root']=Path(args['project_root'])
args['outputs']={k:Path(v) for k,v in args['outputs'].items()}
if args.get('executed_notebook') is not None:
    args['executed_notebook']=Path(args['executed_notebook'])
try:
    result=log_run_results(**args)
except Exception as error:
    print(json.dumps({'error':type(error).__name__,'message':str(error),'notes':getattr(error,'__notes__',[])}))
else:
    print(json.dumps({'result':result}))
"""


def command(root: Path, *args: str) -> str:
    """Run native fixture commands and expose diagnostic failures."""
    env = dict(os.environ)
    for key in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    env["DVC_NO_ANALYTICS"] = "1"
    result = subprocess.run(
        args, cwd=root, env=env, capture_output=True, text=True, timeout=180
    )
    records = (
        Path(__file__).resolve().parents[2]
        / ".dev-records/verification/us26-ip2-native-commands"
    )
    records.mkdir(parents=True, exist_ok=True)
    (records / (uuid.uuid4().hex + ".json")).write_text(
        json.dumps(
            {
                "story": "US-26 IP2",
                "cwd": str(root),
                "command": list(args),
                "test": os.environ.get("PYTEST_CURRENT_TEST"),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
            indent=2,
        )
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def file_ref(root: Path, name: str) -> dict[str, str]:
    """Independently hash a declared fixture file."""
    return {
        "path": name,
        "sha256": "sha256:" + hashlib.sha256((root / name).read_bytes()).hexdigest(),
    }


@dataclass
class TrackingCase:
    """Hold public experiment inputs and native inspection interfaces."""

    root: Path
    uri: str
    client: MlflowClient
    run_id: str
    provenance: dict[str, Any]

    def invoke(self, **changes: Any) -> dict[str, Any]:
        """Call the normally installed public helper from an unrelated cwd."""
        args = {
            "run_id": self.run_id,
            "project_root": str(self.root),
            "tracking_uri": self.uri,
            "provenance": self.provenance,
            "parameters": {"C": 1, "settings": {"depth": 2}},
            "metrics": {"validation_accuracy": 0.75},
            "outputs": {"predictions": "predictions.csv"},
            "expected_outputs": ["predictions"],
            "process_exit_code": 0,
            "validation_passed": True,
        }
        args.update(changes)
        result = subprocess.run(
            [str(self.root / ".venv/bin/python"), "-I", "-c", PROBE],
            input=json.dumps(args),
            cwd=self.root.parent,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        answer: dict[str, Any] = json.loads(result.stdout)
        native = self.client.get_run(self.run_id)
        records = (
            Path(__file__).resolve().parents[2]
            / ".dev-records/verification/us26-ip2-native-commands"
        )
        records.mkdir(parents=True, exist_ok=True)
        (records / (uuid.uuid4().hex + "-invocation.json")).write_text(
            json.dumps(
                {
                    "story": "US-26 IP2",
                    "test": os.environ.get("PYTEST_CURRENT_TEST"),
                    "cwd": str(self.root.parent),
                    "arguments_json": json.dumps(args),
                    "reply": answer,
                    "stderr": result.stderr,
                    "native": {
                        "run_id": native.info.run_id,
                        "status": native.info.status,
                        "artifact_uri": native.info.artifact_uri,
                        "parameters": native.data.params,
                        "metrics": native.data.metrics,
                        "tags": native.data.tags,
                    },
                },
                indent=2,
                allow_nan=False,
            )
        )
        return answer


def prepare_project(root: Path) -> dict[str, Any]:
    """Commit real source/configuration/lock/DVC references in the fixture."""
    python = str(root / ".venv/bin/python")
    command(root, "git", "init")
    command(root, "git", "config", "user.email", "fixture@example.invalid")
    command(root, "git", "config", "user.name", "US-26 fixture")
    command(root, python, "-m", "dvc", "init")
    (root / "experiment.py").write_text("print('fixture experiment')\n")
    (root / "config.json").write_text('{"C":1}\n')
    (root / ".gitignore").write_text(
        ".venv/\npredictions.csv\nstdout.txt\nexecuted.ipynb\n"
    )
    (root / "data").mkdir()
    (root / "data/input.csv").write_text("id,x,label\n0,1,A\n1,3,B\n")
    # Existing public split format; native data owns its saved JSON.
    script = """import json, pandas as pd
from agentic_ml.splitting import create_partitions
from pathlib import Path
_, record=create_partitions(pd.read_csv('data/input.csv'),row_id='id',target='label',layout='train_test',memberships={'train':[0],'test':[1]})
Path('data/split.json').write_text(json.dumps(record,allow_nan=False))
"""
    command(root, python, "-I", "-c", script)
    command(root, python, "-m", "dvc", "add", "data")
    command(root, "git", "add", ".")
    command(root, "git", "commit", "-m", "data: commit experiment inputs")
    import yaml

    pointer = yaml.safe_load((root / "data.dvc").read_text())["outs"][0]
    # Read native installed identity independently through the public initializer
    # journal after initialization (no private identity calls in the test).
    command(root, str(root / ".venv/bin/agentic-ml"), "init")
    command(root, "git", "add", ".")
    command(root, "git", "commit", "-m", "chore: commit initialized experiment lock")
    commit = command(root, "git", "rev-parse", "HEAD")
    identity = json.loads((root / ".agentic-ml/init.json").read_text())["environment"][
        "toolkit_identity"
    ]
    versions: dict[str, str] = json.loads(
        command(
            root,
            python,
            "-I",
            "-c",
            "import json; from importlib.metadata import version; print(json.dumps({n:version(n) for n in ['agentic-ml','mlflow','dvc','pandas','pyarrow','scikit-learn']}))",
        )
    )
    return {
        "schema_version": "1.0",
        "experiment": {
            "commit_sha": commit,
            "entrypoint": file_ref(root, "experiment.py"),
            "code": [file_ref(root, "experiment.py")],
        },
        "configuration": {
            "files": [file_ref(root, "config.json")],
            "effective": {"C": 1},
        },
        "data": [
            {
                "metadata": file_ref(root, "data.dvc"),
                "output_path": "data",
                "hash_name": "md5",
                "hash_value": pointer["md5"],
                "member_path": member,
            }
            for member in ("input.csv", "split.json")
        ],
        "split_record": file_ref(root, "data/split.json"),
        "environment": {
            "lockfile": file_ref(root, "uv.lock"),
            "python_version": sys.version.split()[0],
            "libraries": versions,
        },
        "toolkit": {
            "installation": identity,
            "repository_url": identity.get("url"),
            "commit_sha": identity.get("revision"),
            "build_identity": None,
        },
    }
