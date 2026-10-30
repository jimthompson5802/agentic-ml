"""Check public resources in an installed distribution using only the stdlib."""

import argparse
import json
import platform
import subprocess
import sys
from importlib.metadata import distribution, distributions
from importlib.resources import files
from pathlib import Path

import agentic_ml


def main() -> None:
    """Compare installed resources with independently specified contents."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--environment", type=Path, required=True)
    args = parser.parse_args()
    environment = args.environment.resolve()
    installed = distribution("agentic-ml")
    assert installed.version == args.expected_version, (
        "artifact/installed version mismatch"
    )
    assert Path(sys.prefix).resolve() == environment, "wrong interpreter environment"
    assert sys.version_info[:2] == (3, 12), "verification requires Python 3.12"
    assert agentic_ml.__file__ is not None
    assert Path(agentic_ml.__file__).resolve().is_relative_to(environment), (
        "import outside environment"
    )
    assert Path(str(installed.locate_file(""))).resolve().is_relative_to(environment), (
        "metadata outside environment"
    )
    assert not (installed.requires or []), (
        "review dependency closure when runtime dependencies change"
    )
    inventory = sorted((d.metadata["Name"], d.version) for d in distributions())
    assert inventory == [("agentic-ml", args.expected_version)], (
        f"unexpected distributions: {inventory}"
    )
    direct_url = installed.read_text("direct_url.json")
    assert direct_url is not None and not json.loads(direct_url).get(
        "dir_info", {}
    ).get("editable"), "editable install"
    checkout = Path(__file__).resolve().parents[2]
    assert not Path.cwd().resolve().is_relative_to(checkout), "project inside checkout"
    assert all(not Path(p).resolve().is_relative_to(checkout) for p in sys.path), (
        "checkout on import path"
    )
    result = subprocess.run(
        [str(environment / "bin/agentic-ml"), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"CLI exit {result.returncode}: {result.stderr}"
    assert result.stdout == args.expected_version + "\n", (
        f"CLI version mismatch: {result.stdout!r}"
    )
    assert result.stderr == "", f"CLI stderr: {result.stderr}"
    print(
        json.dumps(
            {
                "python": sys.version,
                "platform": platform.platform(),
                "cwd": str(Path.cwd()),
                "prefix": sys.prefix,
                "sys_path": sys.path,
                "package": agentic_ml.__file__,
                "metadata": str(installed.locate_file("")),
                "distributions": inventory,
                "cli_stdout": result.stdout,
                "cli_stderr": result.stderr,
            }
        )
    )
    resource = files("agentic_ml").joinpath("templates/provisional.txt")
    assert resource.is_file(), "template resource missing"
    assert resource.read_text(encoding="utf-8") == (
        "Provisional Milestone 0 template; experiment initialization is unavailable.\n"
    ), "template contents differ"

    guidance = files("agentic_ml").joinpath("runtime_guidance/provisional.md")
    assert guidance.read_text(encoding="utf-8") == (
        "Provisional Milestone 0 runtime guidance; experiment execution is unavailable.\n"
    ), "runtime guidance contents differ"


if __name__ == "__main__":
    main()
