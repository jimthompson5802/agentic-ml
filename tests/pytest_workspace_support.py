"""Own contributor temporary trees through complete pytest outcomes."""

import os
import re
import shutil
import tempfile
from collections.abc import Generator
from dataclasses import dataclass, field
from pathlib import Path

import pytest


@dataclass
class Workspace:
    """An exclusively allocated directory and its fixture lifetime."""

    path: Path
    owner_id: str
    released: bool = False
    failed: bool = False
    identity: tuple[int, int] = field(init=False)
    parent_identity: tuple[int, int] = field(init=False)

    def __post_init__(self) -> None:
        """Capture identities before returning ownership to the caller."""
        self.identity = _identity(self.path)
        self.parent_identity = _identity(self.path.parent)

    def remove(self) -> None:
        """Remove only the original directory under its original parent."""
        if (
            self.path.resolve() != self.path
            or _identity(self.path.parent) != self.parent_identity
            or _identity(self.path) != self.identity
        ):
            raise OSError("Workspace ownership changed")
        shutil.rmtree(self.path)


def _identity(path: Path) -> tuple[int, int]:
    stat = path.lstat()
    return stat.st_dev, stat.st_ino


WORKSPACES = pytest.StashKey[list[Workspace]]()
RETENTION_POLICY = pytest.StashKey[str]()
CHECKOUT = Path(__file__).resolve().parent.parent


def _validate_base(config: pytest.Config, path: Path, *, explicit: bool) -> None:
    resolved = path.resolve()
    protected = (CHECKOUT, config.rootpath / ".dev-records")
    if (
        path.is_symlink()
        or (explicit and path.exists())
        or any(
            resolved.is_relative_to(root.resolve())
            or root.resolve().is_relative_to(resolved)
            for root in protected
        )
    ):
        raise pytest.UsageError(f"Unsafe workspace base: {path.absolute()}")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Expose explicit contributor workspace retention."""
    parser.addoption(
        "--keep-test-workspaces",
        action="store_true",
        help="Retain owned test/shared workspaces outside numbered-session cleanup.",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Preserve numbered generations and separate explicitly retained bases."""
    if config.option.basetemp is not None:
        _validate_base(config, Path(config.option.basetemp), explicit=True)
    if temporary_root := os.environ.get("PYTEST_DEBUG_TEMPROOT"):
        _validate_base(config, Path(temporary_root), explicit=False)
    # Keep the native numbered session container until its normal retention pass.
    # Otherwise a successful session removes the newest number before eviction,
    # and an older failure can remain the newest extant number indefinitely.
    policy = str(config.inicfg.get("tmp_path_retention_policy", "all"))
    if policy not in {"all", "failed", "none"}:
        raise pytest.UsageError(f"Invalid tmp_path_retention_policy: {policy}")
    config.stash[RETENTION_POLICY] = policy
    config.inicfg["tmp_path_retention_policy"] = "all"
    if config.getoption("keep_test_workspaces"):
        if config.option.basetemp is None:
            parent = tempfile.mkdtemp(
                prefix="agentic-ml-pytest-retained-",
                dir=os.environ.get("PYTEST_DEBUG_TEMPROOT"),
            )
            config.option.basetemp = str(Path(parent) / "workspace")


def owned_workspace(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    name: str,
) -> Path:
    """Allocate a directory lasting through its requesting fixture's scope.

    Args:
        request: Request of the fixture that owns this directory.
        tmp_path_factory: The active session's public temporary path factory.
        name: A relative directory basename for the exclusive allocation.

    Returns:
        The new absolute directory. Failed consumers/finalizers retain its tree.
    """
    workspace = Workspace(tmp_path_factory.mktemp(name), request.node.nodeid)
    request.config.stash.setdefault(WORKSPACES, []).append(workspace)

    def release() -> None:
        workspace.released = True

    request.addfinalizer(release)
    return workspace.path


@pytest.fixture
def tmp_path(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Allocate a test root whose lifetime includes every fixture finalizer."""
    name = re.sub(r"\W", "_", request.node.name)[:30]
    return owned_workspace(request, tmp_path_factory, name)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Finalize owned paths after fixture teardown, before report delivery."""
    report = yield
    workspaces = item.config.stash.setdefault(WORKSPACES, [])
    for workspace in workspaces:
        if workspace.owner_id not in {node.nodeid for node in item.listchain()}:
            continue
        workspace.failed |= report.failed
        if report.failed:
            report.sections.append(("Owned workspace", f"WORKSPACE {workspace.path}"))
        retain = item.config.getoption("keep_test_workspaces") or (
            item.config.stash[RETENTION_POLICY] == "all"
        )
        if (
            report.when == "teardown"
            and workspace.released
            and not workspace.failed
            and not retain
        ):
            try:
                workspace.remove()
            except OSError as error:
                report.outcome = "failed"
                report.longrepr = (
                    f"Workspace cleanup failed: {error}\nWORKSPACE {workspace.path}"
                )
                workspace.failed = True
    if report.when == "teardown":
        workspaces[:] = [
            workspace for workspace in workspaces if not workspace.released
        ]
    return report
