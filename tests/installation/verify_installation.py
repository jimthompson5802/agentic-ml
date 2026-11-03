"""Verify full-SHA Git installation in a disposable separate experiment project."""

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

PROBE = Path(__file__).with_name("check_project.py").resolve()
CHECKOUT = PROBE.parents[2]


def main() -> None:
    """Create, install and probe a fresh project without a surviving uv cache."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--upgrade-revision")
    parser.add_argument(
        "--keep-workspace",
        action="store_true",
        help="Preserve successful environments and workspace for inspection.",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("revision must be a full lowercase 40-character commit SHA")
    if args.upgrade_revision is not None:
        if not re.fullmatch(r"[0-9a-f]{40}", args.upgrade_revision):
            parser.error(
                "upgrade revision must be a full lowercase 40-character commit SHA"
            )
        if args.upgrade_revision == args.revision:
            parser.error("upgrade revision must differ from the initial revision")
    spec = importlib.util.spec_from_file_location(
        "verification_support", CHECKOUT / "tests/verification_support.py"
    )
    assert spec is not None and spec.loader is not None
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    invocation = support.Invocation(
        checkout=CHECKOUT, workspace=args.workspace, keep_workspace=args.keep_workspace
    )
    workspace = invocation.workspace
    run = invocation.run
    project = workspace / "experiment"
    project.mkdir()
    invocation.create_disposable("experiment/.venv", create=False)
    cache = invocation.create_disposable("cache", create=False)
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
    shutil.copy(PROBE.with_name("dependency_inventory.py"), workspace)
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
        probe_command = [
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
        ]
        stage = "before-sync-probe"
        before = run(stage, probe_command, project, env)
        (workspace / "identity-before-sync.json").write_text(before)
        invocation.preserve(
            workspace / "identity-before-sync.json", "identity-before-sync.json"
        )
        declaration = (project / "pyproject.toml").read_bytes()
        lock = (project / "uv.lock").read_bytes()
        (workspace / "pyproject-before-sync.toml").write_bytes(declaration)
        (workspace / "uv-before-sync.lock").write_bytes(lock)
        invocation.preserve(workspace / "uv-before-sync.lock", "uv-before-sync.lock")
        invocation.preserve(
            workspace / "pyproject-before-sync.toml", "pyproject-before-sync.toml"
        )
        stage = "locked-sync"
        run(stage, ["uv", "sync", "--locked"], project, env)
        assert (project / "uv.lock").read_bytes() == lock, "locked sync changed lock"
        assert (project / "pyproject.toml").read_bytes() == declaration, (
            "locked sync changed declaration"
        )
        # This cache was created only inside this newly allocated workspace.
        invocation.remove_disposable(cache)
        stage = "installed-probe"
        output = run(stage, probe_command, project, env)
        assert output == before, "locked sync changed environment identity"
        print("PASS stable synchronization", flush=True)
        (workspace / "identity.json").write_text(output)
        invocation.preserve(workspace / "identity.json", "identity.json")
        stage = "offline-cli"
        run(
            stage,
            ["uv", "run", "--no-sync", "--offline", "agentic-ml", "--version"],
            project,
            env,
        )
        # uv may create an empty cache root even without synchronizing.
        if cache.exists():
            invocation.remove_disposable(cache)
        print(output, end="")
        print("PASS pinned installation", flush=True)
        if args.upgrade_revision is not None:
            stage = "explicit-upgrade"
            run(
                stage,
                [
                    "uv",
                    "add",
                    "git+" + args.repository,
                    "--rev",
                    args.upgrade_revision,
                ],
                project,
                env,
            )
            stage = "upgrade-locked-sync"
            run(stage, ["uv", "sync", "--locked"], project, env)
            assert (project / "uv.lock").read_bytes() != lock, (
                "upgrade did not change lock"
            )
            assert (project / "pyproject.toml").read_bytes() != declaration, (
                "upgrade did not change declaration"
            )
            invocation.remove_disposable(cache)
            upgrade_probe = [
                args.upgrade_revision if value == args.revision else value
                for value in probe_command
            ]
            stage = "upgrade-installed-probe"
            upgraded = run(stage, upgrade_probe, project, env)
            assert (
                json.loads(upgraded)["lock_sha256"] != json.loads(before)["lock_sha256"]
            ), "upgrade did not change environment identity"
            (workspace / "identity-after-upgrade.json").write_text(upgraded)
            invocation.preserve(
                workspace / "identity-after-upgrade.json", "identity-after-upgrade.json"
            )
            stage = "upgrade-offline-cli"
            run(
                stage,
                ["uv", "run", "--no-sync", "--offline", "agentic-ml", "--version"],
                project,
                env,
            )
            if cache.exists():
                invocation.remove_disposable(cache)
            print(upgraded, end="")
            print("PASS explicit upgrade", flush=True)
    except (OSError, RuntimeError, ValueError, AssertionError) as error:
        print(f"FAIL {stage}: {error}; diagnostics={workspace}", file=sys.stderr)
        raise SystemExit(invocation.finish(1)) from error
    raise SystemExit(invocation.finish(0))


if __name__ == "__main__":
    main()
