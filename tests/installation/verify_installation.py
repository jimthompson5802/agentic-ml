"""Verify full-SHA Git installation in a disposable separate experiment project."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROBE = Path(__file__).with_name("check_project.py").resolve()
CHECKOUT = PROBE.parents[2]


def run(stage: str, command: list[str], cwd: Path, env: dict[str, str]) -> str:
    """Run a stage and retain stdout/stderr before propagating failure."""
    print(f"STAGE {stage}: {command!r} cwd={cwd}", flush=True)
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    (cwd.parent / f"{stage}.log").write_text(
        f"{command!r}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    if result.returncode:
        raise RuntimeError(
            f"{stage}: exit {result.returncode}\n{result.stdout}{result.stderr}"
        )
    return result.stdout


def main() -> None:
    """Create, install and probe a fresh project without a surviving uv cache."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("revision must be a full lowercase 40-character commit SHA")
    if args.workspace is None:
        workspace = Path(tempfile.mkdtemp(prefix="agentic-ml-installation-")).resolve()
    else:
        workspace = args.workspace.resolve()
        workspace.mkdir(parents=True, exist_ok=False)
    print(f"WORKSPACE {workspace}", flush=True)
    project = workspace / "experiment"
    project.mkdir()
    cache = workspace / "cache"
    env = dict(os.environ)
    for name in (
        "PYTHONPATH",
        "PYTHONHOME",
        "VIRTUAL_ENV",
        "UV_PROJECT_ENVIRONMENT",
        "UV_PROJECT",
        "UV_WORKING_DIR",
        "UV_VENV_SEED",
        "UV_SYSTEM_PYTHON",
    ):
        env.pop(name, None)
    env["UV_CACHE_DIR"] = str(cache)
    env["UV_LINK_MODE"] = "copy"
    env["UV_PYTHON_DOWNLOADS"] = "never"
    probe = workspace / "check_project.py"
    shutil.copy(PROBE, probe)
    stage = "initialize"
    try:
        run("git-init", ["git", "init"], project, env)
        run("uv-init", ["uv", "init", "--no-package", "--python", "3.12"], project, env)
        stage = "install"
        run(
            stage,
            ["uv", "add", "git+" + args.repository, "--rev", args.revision],
            project,
            env,
        )
        stage = "locked-sync"
        run(stage, ["uv", "sync", "--locked"], project, env)
        # This cache was created only inside this newly allocated workspace.
        shutil.rmtree(cache)
        stage = "installed-probe"
        output = run(
            stage,
            [
                str(project / ".venv/bin/python"),
                "-I",
                str(probe),
                "--project",
                str(project),
                "--repository",
                args.repository,
                "--revision",
                args.revision,
                "--checkout",
                str(CHECKOUT),
            ],
            project,
            env,
        )
        (workspace / "identity.json").write_text(output)
        stage = "offline-cli"
        run(
            stage,
            ["uv", "run", "--no-sync", "--offline", "agentic-ml", "--version"],
            project,
            env,
        )
        # uv may create an empty cache root even without synchronizing.
        if cache.exists():
            shutil.rmtree(cache)
        print(output, end="")
        print("PASS pinned installation", flush=True)
    except (OSError, RuntimeError) as error:
        print(f"FAIL {stage}: {error}; diagnostics={workspace}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
