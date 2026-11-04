"""Verify the development invocation lifecycle through its public interface."""

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest
from pytest_workspace_support import owned_workspace

ROOT = Path(__file__).resolve().parents[2]


pytestmark = pytest.mark.milestone_50


def support() -> ModuleType:
    """Load contributor support explicitly without changing product import paths."""
    spec = importlib.util.spec_from_file_location(
        "verification_support", ROOT / "tests/verification_support.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_success_removes_only_created_disposable_paths(tmp_path: Path) -> None:
    """Successful finalization preserves durable records and project source."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("experiment/.venv")
    (environment / "pyvenv.cfg").write_text("home = sentinel\n")
    source = invocation.workspace / "experiment/source.py"
    source.write_text("SOURCE = 42\n")
    assert environment.is_dir()
    assert invocation.finish(0) == 0
    assert not environment.exists()
    assert source.read_text() == "SOURCE = 42\n"
    assert invocation.records.is_absolute()
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["verification_exit_code"] == 0
    assert summary["cleanup"] == "complete"


@pytest.mark.parametrize("code,keep", [(7, False), (0, True)])
def test_failure_or_explicit_retention_keeps_environment(
    tmp_path: Path, code: int, keep: bool
) -> None:
    """Failures and requested successful retention preserve available environments."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work", keep_workspace=keep
    )
    environment = invocation.create_disposable("environment")
    (environment / "diagnostic").write_text("inspect me")
    assert invocation.finish(code) == code
    assert (environment / "diagnostic").read_text() == "inspect me"
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["verification_exit_code"] == code
    assert summary["cleanup"] == "retained"


@pytest.mark.parametrize("relative", ["../caller", "/outside", "source/../../caller"])
def test_disposable_paths_cannot_escape_workspace(
    tmp_path: Path, relative: str
) -> None:
    """Invalid disposable paths cannot adopt caller-owned files for deletion."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    caller = tmp_path / "caller"
    caller.mkdir()
    (caller / "sentinel").write_text("caller owned")
    with pytest.raises(ValueError, match="ownership"):
        invocation.create_disposable(relative)
    assert invocation.finish(0) == 0
    assert (caller / "sentinel").read_text() == "caller owned"


def test_replaced_environment_cannot_redirect_cleanup(tmp_path: Path) -> None:
    """A symlink replacement never causes cleanup of an external environment."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")
    caller = tmp_path / "caller"
    caller.mkdir()
    (caller / "sentinel").write_text("external")
    environment.rmdir()
    environment.symlink_to(caller, target_is_directory=True)
    assert invocation.finish(0) == 1
    assert (caller / "sentinel").read_text() == "external"
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["verification_exit_code"] == 0
    assert summary["cleanup"] == "failed"
    assert "ownership" in summary["cleanup_errors"][0]


def test_stage_records_commands_outputs_and_identity_before_cleanup(
    tmp_path: Path,
) -> None:
    """Successful stages keep independent readable evidence after environment removal."""
    import os
    import sys

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")
    identity = environment / "identity.json"
    identity.write_text('{"package_version": "0.1.0"}\n')
    invocation.preserve(identity, "identity.json")
    output = invocation.run(
        "probe",
        [
            sys.executable,
            "-c",
            "import sys; print('checked'); print('diagnostic', file=sys.stderr)",
        ],
        environment,
        dict(os.environ),
    )
    assert output == "checked\n"
    assert invocation.finish(0) == 0
    assert not environment.exists()
    assert json.loads(
        (invocation.records / "identities/identity.json").read_text()
    ) == {"package_version": "0.1.0"}
    commands = json.loads((invocation.records / "commands.json").read_text())
    assert commands[0]["cwd"] == str(environment)
    assert commands[0]["returncode"] == 0
    log = (invocation.records / commands[0]["log"]).read_text()
    assert "checked\n" in log and "diagnostic\n" in log


@pytest.mark.parametrize("code", [0, 7])
def test_record_write_failure_retains_environment_and_original_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: int
) -> None:
    """Failure to persist outcomes forbids deleting available environments."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")
    write_text = Path.write_text

    def deny_summary(
        path: Path,
        data: str,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        if path.name == "summary.json":
            raise PermissionError("record filesystem unavailable")
        return write_text(path, data, encoding=encoding, errors=errors, newline=newline)

    monkeypatch.setattr(Path, "write_text", deny_summary)
    assert invocation.finish(code) == (code or 1)
    assert environment.is_dir()


@pytest.mark.parametrize("location", ["checkout", "records", "ancestor"])
def test_workspace_cannot_overlap_checkout_or_records(
    tmp_path: Path, location: str
) -> None:
    """Source and durable-record roots cannot be claimed as disposable workspaces."""
    checkout = tmp_path / "checkout"
    workspace = {
        "checkout": checkout / "work",
        "records": checkout / ".dev-records/verification/work",
        "ancestor": tmp_path,
    }[location]
    with pytest.raises(ValueError, match="ownership"):
        support().Invocation(checkout=checkout, workspace=workspace)


def test_existing_directories_are_never_adopted(tmp_path: Path) -> None:
    """Existing workspaces and environments remain caller-owned."""
    workspace = tmp_path / "existing"
    workspace.mkdir()
    (workspace / "sentinel").write_text("caller")
    with pytest.raises(FileExistsError):
        support().Invocation(checkout=tmp_path / "checkout", workspace=workspace)
    assert (workspace / "sentinel").read_text() == "caller"


def test_invocation_reports_records_and_source_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Records are discoverable and include available platform/source identities."""
    invocation = support().Invocation(checkout=ROOT, workspace=tmp_path / "work")
    assert invocation.finish(0) == 0
    assert f"RECORDS {invocation.records}" in capsys.readouterr().out
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert len(summary["source_revision"]) == 40
    assert isinstance(summary["working_tree"], str)
    assert summary["platform"] and summary["python"] and summary["uv"]
    assert summary["invocation_command"]
    assert summary["verification_exit_code"] == 0


def test_command_created_environment_is_owned_only_if_initially_absent(
    tmp_path: Path,
) -> None:
    """An installer can create a reserved environment without adopting an old one."""
    import os
    import sys

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment", create=False)
    assert not environment.exists()
    invocation.run(
        "install",
        [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('environment').mkdir(); Path('environment/pyvenv.cfg').write_text('created')",
        ],
        invocation.workspace,
        dict(os.environ),
    )
    assert (environment / "pyvenv.cfg").read_text() == "created"
    assert invocation.finish(0) == 0
    assert not environment.exists()


def test_private_cache_can_be_released_and_recreated_by_next_stage(
    tmp_path: Path,
) -> None:
    """Cache-independence probes can safely remove their own cache between checks."""
    import os
    import sys

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    cache = invocation.create_disposable("cache")
    invocation.remove_disposable(cache)
    assert not cache.exists()
    invocation.run(
        "offline",
        [sys.executable, "-c", "from pathlib import Path; Path('cache').mkdir()"],
        invocation.workspace,
        dict(os.environ),
    )
    assert cache.is_dir()
    assert invocation.finish(0) == 0
    assert not cache.exists()


def test_spawn_failure_records_attempted_command_and_retains_partial_environment(
    tmp_path: Path,
) -> None:
    """An unavailable executable still leaves the attempted stage in durable evidence."""
    import os

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")
    with pytest.raises(OSError):
        invocation.run(
            "missing executable",
            [str(tmp_path / "missing")],
            environment,
            dict(os.environ),
        )
    assert invocation.finish(3) == 3
    commands = json.loads((invocation.records / "commands.json").read_text())
    assert commands[0]["stage"] == "missing executable"
    assert commands[0]["returncode"] is None
    assert "No such file" in (invocation.records / commands[0]["log"]).read_text()
    assert environment.is_dir()


@pytest.mark.parametrize("code", [0, 9])
def test_cleanup_errors_preserve_verification_outcome(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    code: int,
) -> None:
    """Cleanup errors never overwrite a failed verification outcome."""
    import shutil

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")

    def deny_removal(path: Path) -> None:
        raise PermissionError(f"injected cleanup failure: {path}")

    monkeypatch.setattr(shutil, "rmtree", deny_removal)
    assert invocation.finish(code) == (code or 1)
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["verification_exit_code"] == code
    assert summary["cleanup"] == ("failed" if code == 0 else "retained")
    assert environment.is_dir()
    if code == 0:
        assert "injected cleanup failure" in capsys.readouterr().err


def test_symlink_parent_and_existing_environment_are_not_adopted(
    tmp_path: Path,
) -> None:
    """Caller directories and redirected ancestors cannot acquire cleanup ownership."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    caller = tmp_path / "caller"
    caller.mkdir()
    (caller / "sentinel").write_text("shared-cache sentinel")
    (invocation.workspace / "link").symlink_to(caller, target_is_directory=True)
    with pytest.raises(ValueError, match="ownership"):
        invocation.create_disposable("link/environment")
    existing = invocation.workspace / "existing"
    existing.mkdir()
    with pytest.raises(FileExistsError):
        invocation.create_disposable("existing")
    environment = invocation.create_disposable("environment")
    (environment / "shared-cache").symlink_to(caller, target_is_directory=True)
    assert invocation.finish(0) == 0
    assert existing.is_dir()
    assert (caller / "sentinel").read_text() == "shared-cache sentinel"


def test_concurrent_invocations_do_not_share_records_or_cleanup(tmp_path: Path) -> None:
    """Concurrent finalization cannot remove another invocation's active workspace."""
    from concurrent.futures import ThreadPoolExecutor

    module = support()
    with ThreadPoolExecutor(max_workers=2) as pool:
        invocations = list(
            pool.map(
                lambda index: module.Invocation(
                    checkout=tmp_path / "checkout",
                    workspace=tmp_path / f"work-{index}",
                ),
                range(2),
            )
        )
    first, second = invocations
    assert first.workspace.is_relative_to(tmp_path)
    assert second.workspace.is_relative_to(tmp_path)
    first_environment = first.create_disposable("environment")
    second_environment = second.create_disposable("environment")
    assert first.records != second.records
    assert first.workspace != second.workspace
    assert first.finish(0) == 0
    assert not first_environment.exists()
    assert second_environment.is_dir()
    assert second.finish(0) == 0
    assert (first.records / "summary.json").is_file()
    assert (second.records / "summary.json").is_file()


def test_unfinished_invocation_has_an_incomplete_durable_summary(
    tmp_path: Path,
) -> None:
    """Interrupted commands already have a discoverable incomplete outcome record."""
    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    environment = invocation.create_disposable("environment")
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["verification_exit_code"] is None
    assert summary["cleanup"] == "not attempted"
    assert environment.is_dir()
    assert invocation.finish(4) == 4


def test_child_record_locations_survive_child_failure(tmp_path: Path) -> None:
    """A failed subprocess reports linked records without transferring path ownership."""
    import os
    import sys

    invocation = support().Invocation(
        checkout=tmp_path / "checkout", workspace=tmp_path / "work"
    )
    assert invocation.workspace.is_relative_to(tmp_path)
    child_records = invocation.checkout / ".dev-records/verification/child"
    child_records.mkdir()
    with pytest.raises(RuntimeError, match="exit 4"):
        invocation.run(
            "child",
            [
                sys.executable,
                "-c",
                f"print('RECORDS {child_records}'); raise SystemExit(4)",
            ],
            invocation.workspace,
            dict(os.environ),
        )
    assert invocation.finish(1) == 1
    summary = json.loads((invocation.records / "summary.json").read_text())
    assert summary["child_records"] == [str(child_records)]
    assert child_records.is_dir()


@pytest.fixture(scope="module")
def lifecycle_artifacts(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Build real artifacts for direct parent lifecycle commands."""
    import subprocess

    destination = owned_workspace(request, tmp_path_factory, "lifecycle-artifacts")
    subprocess.run(["uv", "build", "--out-dir", str(destination)], cwd=ROOT, check=True)
    return destination


@pytest.mark.parametrize("keep", [False, True])
def test_initialization_cleans_after_final_consumer(
    lifecycle_artifacts: Path, tmp_path: Path, keep: bool
) -> None:
    """All six installed environments survive their probes and are then removed."""
    import subprocess
    import sys

    workspace = tmp_path / "initialization"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_initialization.py"),
            "--artifacts-dir",
            str(lifecycle_artifacts),
            "--workspace",
            str(workspace),
            *(["--keep-workspace"] if keep else []),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert f"PASS initialization {label}" in result.stdout
    assert len(list(workspace.rglob("pyvenv.cfg"))) == (6 if keep else 0)
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == ("retained" if keep else "complete")
    assert len(summary["child_records"]) == 1
    for label in ("direct-wheel", "rebuilt-wheel"):
        for kind in ("fresh", "existing"):
            identity = json.loads(
                (records / "identities" / f"{label}-{kind}.json").read_text()
            )
            assert identity["origin"]["vcs_info"]["commit_id"]
            assert (workspace / label / kind / "uv.lock").is_file()
    assert (workspace / "source/.git").is_dir()


@pytest.mark.parametrize("driver", ["verify_initialization.py", "verify_planning.py"])
def test_parent_failure_after_child_success_retains_child_environments(
    lifecycle_artifacts: Path, tmp_path: Path, driver: str
) -> None:
    """A filesystem conflict after child validation leaves its evidence and interpreters."""
    import os
    import subprocess
    import sys

    process = subprocess.Popen(
        [
            sys.executable,
            str(ROOT / "tests/installation" / driver),
            "--artifacts-dir",
            str(lifecycle_artifacts),
            "--workspace",
            str(tmp_path / "verification"),
        ],
        cwd=tmp_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    # Read bytes without TextIO read-ahead, so communicate retains all record lines.
    first_bytes = bytearray()
    while not first_bytes.endswith(b"\n"):
        byte = os.read(process.stdout.fileno(), 1)
        assert byte, "driver exited before reporting its workspace"
        first_bytes.extend(byte)
    first = first_bytes.decode()
    assert first.startswith("WORKSPACE "), first
    workspace = Path(first.removeprefix("WORKSPACE ").strip())
    assert workspace == tmp_path / "verification"
    # Inject only at the filesystem boundary, without changing any probe or package.
    if driver == "verify_initialization.py":
        (workspace / "source").write_text("conflicting caller sentinel")
    else:
        (workspace / "check_planning.py").mkdir()
    output, error = process.communicate(timeout=180)
    assert process.returncode != 0, output + error
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in output.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["verification_exit_code"] == 1
    assert summary["cleanup"] == "retained"
    child_records = Path(summary["child_records"][0])
    child = json.loads((child_records / "summary.json").read_text())
    assert child["verification_exit_code"] == 0
    assert child["parent_records"] == str(records)
    for label in ("direct-wheel", "rebuilt-wheel"):
        assert (workspace / "distributions" / label / "bin/python").is_file()
    assert (child_records / "identities/artifacts.json").is_file()


@pytest.mark.parametrize("driver", ["verify_initialization.py", "verify_planning.py"])
def test_parent_early_failure_preserves_linked_diagnostics(
    tmp_path: Path, driver: str
) -> None:
    """Missing artifacts keep separate original child and parent failure records."""
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation" / driver),
            "--artifacts-dir",
            str(tmp_path),
            "--workspace",
            str(tmp_path / "verification"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode != 0
    assert "artifact selection" in result.stderr
    records = Path(
        next(
            line.removeprefix("RECORDS ")
            for line in result.stdout.splitlines()
            if line.startswith("RECORDS ")
        )
    )
    summary = json.loads((records / "summary.json").read_text())
    assert summary["cleanup"] == "retained"
    child = Path(summary["child_records"][0])
    assert (
        json.loads((child / "summary.json").read_text())["verification_exit_code"] == 1
    )


def test_planning_retention_preserves_caller_directory_and_shared_cache(
    lifecycle_artifacts: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Existing directories get a unique child; shared caches and sources survive."""
    import subprocess
    import sys

    caller = tmp_path / "caller"
    caller.mkdir()
    (caller / "sentinel").write_text("caller-owned")
    existing = caller / ".venv"
    existing.mkdir()
    (existing / "sentinel").write_text("existing environment")
    shared = tmp_path / "shared-cache"
    shared.mkdir()
    (shared / "sentinel").write_text("shared cache")
    monkeypatch.setenv("UV_CACHE_DIR", str(shared))
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tests/installation/verify_planning.py"),
            "--artifacts-dir",
            str(lifecycle_artifacts),
            "--workspace",
            str(caller),
            "--keep-workspace",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    workspace = Path(
        next(
            line.removeprefix("WORKSPACE ")
            for line in result.stdout.splitlines()
            if line.startswith("WORKSPACE ")
        )
    )
    assert workspace.parent == caller
    assert (caller / "sentinel").read_text() == "caller-owned"
    assert (existing / "sentinel").read_text() == "existing environment"
    assert list(shared.iterdir()) == [shared / "sentinel"]
    assert (shared / "sentinel").read_text() == "shared cache"
    assert len(list(workspace.rglob("pyvenv.cfg"))) == 2
