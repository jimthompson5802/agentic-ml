"""Verify real preprocessing/tracking through direct and sdist-rebuilt wheels."""

import argparse
import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    """Keep independently installed runtime projects until handoff checks finish."""
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
    invocation = support.Invocation(
        checkout=ROOT, workspace=args.workspace, keep_workspace=args.keep_workspace
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
    env["DVC_NO_ANALYTICS"] = "1"
    env["UV_CACHE_DIR"] = str(invocation.create_disposable("cache", create=False))
    distribution_work = workspace / "distributions"
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
                str(distribution_work),
                "--keep-workspace",
                "--parent-records",
                str(invocation.records),
            ],
            workspace,
            env,
        )
        script = Path(__file__).with_name("tracking_project.py").read_text()
        documented = re.search(
            r"<!-- us26-producer-script -->\s*```python\n(.*?)```",
            (ROOT / "docs/experiment-tracking.md").read_text(),
            re.S,
        )
        if documented is None or documented[1] != script:
            raise ValueError(
                "actual producer project script differs from documented script"
            )
        probe = workspace / "check_tracking.py"
        shutil.copy(Path(__file__).with_name("check_tracking.py"), probe)
        for label in ("direct-wheel", "rebuilt-wheel"):
            project = workspace / label
            project.mkdir()
            invocation.create_disposable(label + "/.venv", create=False)
            wheel = next(
                (
                    args.artifacts_dir.resolve()
                    if label == "direct-wheel"
                    else distribution_work / "rebuilt"
                ).glob("*.whl")
            )
            invocation.run(
                label + " project",
                ["uv", "init", "--no-package", "--python", "3.12"],
                project,
                env,
            )
            invocation.run(label + " install", ["uv", "add", str(wheel)], project, env)
            (project / "track.py").write_text(script)
            invocation.run(
                label + " tracking",
                [
                    str(project / ".venv/bin/python"),
                    "-I",
                    str(probe),
                    "--project",
                    str(project),
                ],
                workspace,
                env,
            )
            for name in (
                "identity.json",
                "native-commands.json",
                "data/split.json",
                "run-provenance.json",
            ):
                invocation.preserve(
                    project / name,
                    label
                    + "-"
                    + ("tracking.json" if name == "identity.json" else Path(name).name),
                )
            for artifact in (project / "evidence").rglob("*"):
                if artifact.is_file():
                    invocation.preserve(
                        artifact,
                        label
                        + "-artifact-"
                        + "-".join(artifact.relative_to(project / "evidence").parts),
                    )
            print(f"PASS tracking {label}", flush=True)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL tracking: {error}; workspace={workspace}", file=sys.stderr)
        raise SystemExit(invocation.finish(1)) from error
    raise SystemExit(invocation.finish(0))


if __name__ == "__main__":
    main()
