"""Verify the development invocation lifecycle through its public interface."""

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]


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
                lambda _: module.Invocation(checkout=tmp_path / "checkout"), range(2)
            )
        )
    first, second = invocations
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
