"""Build and probe wheels in fresh environments outside the source checkout."""

import argparse
import hashlib
import os
import subprocess
import sys
import tarfile
import tempfile
from email.parser import BytesParser
from pathlib import Path
from zipfile import BadZipFile, ZipFile

PROBE = Path(__file__).with_name("check_installed.py").resolve()


def run(stage: str, command: list[str], cwd: Path, env: dict[str, str]) -> None:
    """Record a command and preserve its output, failing at the affected stage."""
    print(f"STAGE {stage}: {command!r} cwd={cwd}", flush=True)
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    log = cwd / (stage.replace(" ", "-") + ".log")
    log.write_text(
        f"{command!r} cwd={cwd}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        encoding="utf-8",
    )
    print(result.stdout, end="", flush=True)
    print(result.stderr, end="", file=sys.stderr, flush=True)
    if result.returncode:
        raise RuntimeError(f"{stage}: command exited {result.returncode}")


def identity(artifact: Path) -> None:
    """Print the exact artifact identity."""
    print(
        f"ARTIFACT {artifact} sha256={hashlib.sha256(artifact.read_bytes()).hexdigest()}"
    )


def verify(wheel: Path, label: str, work: Path, env: dict[str, str]) -> None:
    """Install one wheel normally and run the independent installed probe."""
    identity(wheel)
    with ZipFile(wheel) as archive:
        metadata_files = [
            n for n in archive.namelist() if n.endswith(".dist-info/METADATA")
        ]
        if len(metadata_files) != 1:
            raise RuntimeError(f"{label}: expected one wheel METADATA")
        metadata = BytesParser().parsebytes(archive.read(metadata_files[0]))
    version = str(metadata["Version"])
    environment = work / label
    project = work / f"{label}-project"
    project.mkdir()
    (project / "README.md").write_text("Separate installation verification project.\n")
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
    run(
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
    print(f"PASS {label}", flush=True)


def main() -> None:
    """Verify the supplied artifact pair, retaining diagnostics on failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    args = parser.parse_args()
    work = Path(tempfile.mkdtemp(prefix="agentic-ml-distributions-")).resolve()
    print(f"WORKSPACE {work}", flush=True)
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
    stage = "artifact selection"
    try:
        wheels = sorted(args.artifacts_dir.resolve().glob("*.whl"))
        sdists = sorted(args.artifacts_dir.resolve().glob("*.tar.gz"))
        if len(wheels) != 1 or len(sdists) != 1:
            raise RuntimeError(
                f"artifact selection: expected exactly one wheel and one sdist; found {len(wheels)} wheel(s), {len(sdists)} sdist(s)"
            )
        stage = f"direct-wheel {wheels[0]}"
        verify(wheels[0], "direct-wheel", work, env)
        stage = f"sdist extraction {sdists[0]}"
        identity(sdists[0])
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
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
