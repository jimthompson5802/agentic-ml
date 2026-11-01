"""Verify artifact integrity and matching full-SHA installed initialization."""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
PROBE = Path(__file__).with_name("check_initialization.py")


def verify_project(
    project: Path,
    existing: bool,
    repository: str,
    revision: str,
    wheel: Path,
    env: dict[str, str],
    run: Callable[[str, list[str], Path, dict[str, str]], str],
) -> None:
    """Initialize a fresh or existing project and probe its installed interfaces."""
    project.mkdir(parents=True)
    run("git-init", ["git", "init"], project, env)
    run("uv-init", ["uv", "init", "--no-package", "--python", "3.12"], project, env)
    package = "custom" if existing else "fresh"
    if existing:
        source = project / "src/custom/__init__.py"
        source.parent.mkdir(parents=True)
        source.write_text('"""Existing project."""\nVALUE = 42\n')
        with (project / "pyproject.toml").open("a") as stream:
            stream.write(
                '\n[build-system]\nrequires = ["hatchling>=1.27,<2"]\nbuild-backend = "hatchling.build"\n[tool.hatch.build.targets.wheel]\npackages = ["src/custom"]\n'
            )
    run("pin", ["uv", "add", "git+" + repository, "--rev", revision], project, env)
    (project / ".env").write_text("TOKEN=sentinel-secret\n")
    data = project / "data/raw.csv"
    data.parent.mkdir()
    data.write_text("private sentinel dataset\n")
    data.chmod(0o000)
    options = ["--package-name", package] if existing else []
    if existing:
        script = (
            "from pathlib import Path; from agentic_ml.initialization import InitOptions, initialize_project; "
            "import sys; result = initialize_project(InitOptions(project_root=Path(sys.argv[1]), package_name='custom')); "
            "assert result.setup_pending == ()"
        )
        command = [str(project / ".venv/bin/python"), "-I", "-c", script, str(project)]
    else:
        command = [
            "uv",
            "run",
            "--locked",
            "--project",
            str(project),
            "agentic-ml",
            "init",
            "--project-root",
            str(project),
            *options,
        ]
    try:
        run(project.name + "-initialize", command, project.parent, env)
    finally:
        data.chmod(0o600)
    probe = project.parent / "check_initialization.py"
    shutil.copy(PROBE, probe)
    run(
        "probe",
        [
            str(project / ".venv/bin/python"),
            "-I",
            str(probe),
            "--project",
            str(project),
            "--package",
            package,
            "--repository",
            repository,
            "--revision",
            revision,
            "--wheel",
            str(wheel),
        ],
        project,
        env,
    )
    before = (project / "uv.lock").read_bytes()
    run(
        "rerun", [str(project / ".venv/bin/agentic-ml"), "init", *options], project, env
    )
    assert (project / "uv.lock").read_bytes() == before
    run(
        "probe-after-rerun",
        [
            str(project / ".venv/bin/python"),
            "-I",
            str(probe),
            "--project",
            str(project),
            "--package",
            package,
            "--repository",
            repository,
            "--revision",
            revision,
            "--wheel",
            str(wheel),
        ],
        project,
        env,
    )


def main() -> None:
    """Verify both wheel paths and exact matching installed Git project fixtures."""
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
    work = invocation.workspace
    run = invocation.run
    artifact_work = work / "distributions"
    for relative in ("direct-wheel", "rebuilt-wheel", "cache"):
        invocation.create_disposable("distributions/" + relative, create=False)
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
    env.update(
        DVC_NO_ANALYTICS="1",
        MLFLOW_DISABLE_TELEMETRY="true",
        MLFLOW_DISABLE_AGENT_HINT="1",
    )
    try:
        run(
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
            work,
            env,
        )
        source = next((artifact_work / "source").iterdir())
        repository = work / "source"
        shutil.copytree(source, repository)
        run("git-init", ["git", "init"], repository, env)
        run("git-add", ["git", "add", "."], repository, env)
        run(
            "git-commit",
            [
                "git",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-m",
                "reviewed artifact source fixture",
            ],
            repository,
            env,
        )
        revision = run(
            "git-revision", ["git", "rev-parse", "HEAD"], repository, env
        ).strip()
        for label, wheel in (
            ("direct-wheel", next(args.artifacts_dir.resolve().glob("*.whl"))),
            ("rebuilt-wheel", next((artifact_work / "rebuilt").glob("*.whl"))),
        ):
            with ZipFile(wheel) as archive:
                for name in archive.namelist():
                    if name.startswith("agentic_ml/") and not name.endswith("/"):
                        assert (
                            archive.read(name) == (source / "src" / name).read_bytes()
                        ), name
            print(
                f"ARTIFACT {label} sha256={hashlib.sha256(wheel.read_bytes()).hexdigest()} fixture={repository.as_uri()} revision={revision}",
                flush=True,
            )
            for kind in ("fresh", "existing"):
                invocation.create_disposable(f"{label}/{kind}/.venv", create=False)
                manifest = work / f"{label}-{kind}.json"
                manifest.write_text(
                    json.dumps(
                        {
                            "status": "unavailable",
                            "reason": "initialization incomplete",
                            "environment": str(work / label / kind / ".venv"),
                        }
                    )
                )
                invocation.preserve(manifest, manifest.name)
                verify_project(
                    work / label / kind,
                    kind == "existing",
                    repository.as_uri(),
                    revision,
                    wheel,
                    env,
                    run,
                )
                project = work / label / kind
                output = run(
                    f"{label}-{kind}-identity",
                    [
                        str(project / ".venv/bin/python"),
                        "-I",
                        "-c",
                        "import json, sys, platform; from importlib.metadata import distribution, distributions; "
                        "d = distribution('agentic-ml'); "
                        "print(json.dumps({'python': sys.version, 'prefix': sys.prefix, "
                        "'platform': platform.platform(), 'package': str(d.locate_file('agentic_ml')), "
                        "'origin': json.loads(d.read_text('direct_url.json') or '{}'), "
                        "'distributions': sorted((p.metadata['Name'], p.version) for p in distributions())}))",
                    ],
                    project,
                    env,
                )
                manifest.write_text(output)
                invocation.preserve(manifest, manifest.name)
                for name in ("uv.lock", "pyproject.toml"):
                    invocation.preserve(project / name, f"{label}-{kind}-{name}")
            print(f"PASS initialization {label}", flush=True)
    except (OSError, RuntimeError, ValueError, AssertionError, StopIteration) as error:
        print(f"FAIL initialization: {error}; workspace={work}", file=sys.stderr)
        raise SystemExit(invocation.finish(1)) from error
    raise SystemExit(invocation.finish(0))


if __name__ == "__main__":
    main()
