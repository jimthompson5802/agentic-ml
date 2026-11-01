"""Run isolated planning probes against direct and sdist-rebuilt installed wheels."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    """Reuse distribution validation, then exercise both installed environments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    workspace = (
        args.workspace.resolve()
        if args.workspace
        else Path(tempfile.mkdtemp(prefix="agentic-ml-planning-")).resolve()
    )
    workspace.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in (
        "PYTHONPATH",
        "PYTHONHOME",
        "VIRTUAL_ENV",
        "UV_PROJECT_ENVIRONMENT",
        "UV_PROJECT",
        "UV_WORKING_DIR",
    ):
        env.pop(name, None)
    print(f"WORKSPACE {workspace}", flush=True)
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/packaging/verify_distributions.py"),
            "--artifacts-dir",
            str(args.artifacts_dir.resolve()),
        ],
        cwd=workspace,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    (workspace / "distributions.log").write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(
            f"Distribution validation failed; see {workspace / 'distributions.log'}"
        )
    print(result.stdout, end="", flush=True)
    artifact_work = Path(
        next(
            line.removeprefix("WORKSPACE ")
            for line in result.stdout.splitlines()
            if line.startswith("WORKSPACE ")
        )
    )
    probe = workspace / "check_planning.py"
    shutil.copy(Path(__file__).with_name("check_planning.py"), probe)
    for label in ("direct-wheel", "rebuilt-wheel"):
        python = artifact_work / label / "bin/python"
        completed = subprocess.run(
            [str(python), "-I", str(probe), "--workspace", str(workspace / label)],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        (workspace / (label + ".log")).write_text(completed.stdout + completed.stderr)
        if completed.returncode:
            raise RuntimeError(
                f"Installed planning failed; see {workspace / (label + '.log')}"
            )
        print(f"PASS planning {label}", flush=True)


if __name__ == "__main__":
    main()
