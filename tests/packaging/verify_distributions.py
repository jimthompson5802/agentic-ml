"""Build and probe wheels in fresh environments outside the source checkout."""

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tarfile
from email.parser import BytesParser
from pathlib import Path
from zipfile import BadZipFile, ZipFile

PROBE = Path(__file__).with_name("check_installed.py").resolve()


def identity(artifact: Path) -> None:
    """Print the exact artifact identity."""
    print(
        f"ARTIFACT {artifact} sha256={hashlib.sha256(artifact.read_bytes()).hexdigest()}"
    )


def main() -> None:
    """Verify the supplied artifact pair, retaining diagnostics on failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--keep-workspace", action="store_true")
    parser.add_argument("--parent-records", type=Path)
    args = parser.parse_args()
    checkout = PROBE.parents[2]
    spec = importlib.util.spec_from_file_location(
        "verification_support", checkout / "tests/verification_support.py"
    )
    assert spec is not None and spec.loader is not None
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    invocation = support.Invocation(
        checkout=checkout, workspace=args.workspace, keep_workspace=args.keep_workspace
    )
    work = invocation.workspace
    run = invocation.run
    if args.parent_records is not None:
        invocation.identity["parent_records"] = str(args.parent_records.resolve())
    artifacts: dict[str, str] = {}

    def record_artifact(artifact: Path) -> None:
        identity(artifact)
        artifacts[str(artifact)] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        manifest = work / "artifacts.json"
        manifest.write_text(json.dumps(artifacts, indent=2))
        invocation.preserve(manifest, "artifacts.json")

    def verify(wheel: Path, label: str, work: Path, env: dict[str, str]) -> None:
        """Install one wheel normally and run the independent installed probe."""
        record_artifact(wheel)
        manifest = work / (label + ".json")
        manifest.write_text(
            json.dumps(
                {
                    "status": "unavailable",
                    "reason": "installed probe incomplete",
                    "environment": str(work / label),
                    "artifact": str(wheel),
                }
            )
        )
        invocation.preserve(manifest, label + ".json")
        with ZipFile(wheel) as archive:
            metadata_files = [
                n for n in archive.namelist() if n.endswith(".dist-info/METADATA")
            ]
            if len(metadata_files) != 1:
                raise RuntimeError(f"{label}: expected one wheel METADATA")
            metadata = BytesParser().parsebytes(archive.read(metadata_files[0]))
        version = str(metadata["Version"])
        environment = invocation.create_disposable(label, create=False)
        project = work / f"{label}-project"
        project.mkdir()
        (project / "README.md").write_text(
            "Separate installation verification project.\n"
        )
        run(
            label + " create environment",
            ["uv", "venv", "--no-project", "--python", "3.12", str(environment)],
            project,
            env,
        )
        python = environment / "bin/python"
        run(
            label + " install",
            ["uv", "pip", "install", "--python", str(python), str(wheel)],
            project,
            env,
        )
        output = run(
            label + " installed checks",
            [
                str(python),
                "-I",
                str(PROBE),
                "--expected-version",
                version,
                "--environment",
                str(environment),
            ],
            project,
            env,
        )
        manifest = work / (label + ".json")
        manifest.write_text(output)
        invocation.preserve(manifest, label + ".json")
        print(f"PASS {label}", flush=True)

    env = dict(os.environ)
    for name in (
        "PYTHONPATH",
        "PYTHONHOME",
        "VIRTUAL_ENV",
        "UV_PROJECT_ENVIRONMENT",
        "UV_VENV_SEED",
        "UV_SYSTEM_PYTHON",
    ):
        env.pop(name, None)
    env["UV_CACHE_DIR"] = str(invocation.create_disposable("cache", create=False))
    stage = "artifact selection"
    try:
        wheels = sorted(args.artifacts_dir.resolve().glob("*.whl"))
        sdists = sorted(args.artifacts_dir.resolve().glob("*.tar.gz"))
        if len(wheels) != 1 or len(sdists) != 1:
            raise RuntimeError(
                f"artifact selection: expected exactly one wheel and one sdist; found {len(wheels)} wheel(s), {len(sdists)} sdist(s)"
            )
        record_artifact(wheels[0])
        record_artifact(sdists[0])
        stage = f"direct-wheel {wheels[0]}"
        verify(wheels[0], "direct-wheel", work, env)
        stage = f"sdist extraction {sdists[0]}"
        record_artifact(sdists[0])
        source = work / "source"
        source.mkdir()
        with tarfile.open(sdists[0], "r:gz") as archive:
            members = archive.getmembers()
            roots = {Path(m.name).parts[0] for m in members if Path(m.name).parts}
            if len(roots) != 1 or any(
                not (m.isfile() or m.isdir())
                or not (source / m.name).resolve().is_relative_to(source)
                for m in members
            ):
                raise RuntimeError("sdist extraction: unsafe archive layout")
            archive.extractall(source, filter="data")
        extracted = source / roots.pop()
        rebuilt = work / "rebuilt"
        stage = f"sdist rebuild {extracted}"
        run(
            "sdist rebuild",
            ["uv", "build", str(extracted), "--wheel", "--out-dir", str(rebuilt)],
            work,
            env,
        )
        rebuilt_wheels = list(rebuilt.glob("*.whl"))
        if len(rebuilt_wheels) != 1:
            raise RuntimeError("sdist rebuild: expected one wheel")
        stage = f"rebuilt-wheel {rebuilt_wheels[0]}"
        verify(rebuilt_wheels[0], "rebuilt-wheel", work, env)
    except (OSError, RuntimeError, ValueError, BadZipFile, tarfile.TarError) as error:
        print(f"FAIL: {stage}: {error}; diagnostics workspace={work}", file=sys.stderr)
        raise SystemExit(invocation.finish(1)) from error
    raise SystemExit(invocation.finish(0))


if __name__ == "__main__":
    main()
