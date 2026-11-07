"""Run isolated data_quality probes against direct and sdist-rebuilt installed wheels."""

import argparse
import importlib.util
import os
import shutil
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    """Retain child environments until both installed data_quality probes finish."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--keep-workspace", action="store_true")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location(
        "verification_support", ROOT / "tests/verification_support.py"
    )
    assert spec is not None and spec.loader is not None
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    requested = args.workspace
    if requested is not None and requested.exists():
        requested = requested / ("verification-" + uuid4().hex)
    invocation = support.Invocation(
        checkout=ROOT, workspace=requested, keep_workspace=args.keep_workspace
    )
    workspace = invocation.workspace
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
    env["UV_CACHE_DIR"] = str(invocation.create_disposable("cache", create=False))
    artifact_work = workspace / "distributions"
    for relative in ("direct-wheel", "rebuilt-wheel", "cache"):
        invocation.create_disposable("distributions/" + relative, create=False)
    try:
        invocation.run(
            "distributions",
            [
                sys.executable,
                str(ROOT / "tests/packaging/verify_distributions.py"),
                "--artifacts-dir",
                str(args.artifacts_dir.resolve()),
                "--workspace",
                str(artifact_work),
                "--keep-workspace",
                "--parent-records",
                str(invocation.records),
            ],
            workspace,
            env,
        )
        probe = workspace / "check_data_quality.py"
        shutil.copy(Path(__file__).with_name("check_data_quality.py"), probe)
        project_code = workspace / "project_data_quality.py"
        shutil.copy(Path(__file__).with_name("data_quality_project.py"), project_code)
        for label in ("direct-wheel", "rebuilt-wheel"):
            python = artifact_work / label / "bin/python"
            invocation.run(
                label + " data_quality",
                [
                    str(python),
                    "-I",
                    str(probe),
                    "--workspace",
                    str(workspace / label),
                    "--project-code",
                    str(project_code),
                ],
                workspace,
                env,
            )
            invocation.preserve(
                workspace / label / "identity.json", label + "-data_quality.json"
            )
            print(f"PASS data_quality {label}", flush=True)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL data_quality: {error}; workspace={workspace}", file=sys.stderr)
        raise SystemExit(invocation.finish(1)) from error
    raise SystemExit(invocation.finish(0))


if __name__ == "__main__":
    main()
