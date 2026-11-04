"""Observe contributor workspace lifetimes through real pytest processes."""

import json
import os
import queue
import subprocess
import sys
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SUPPORT = ROOT / "tests/pytest_workspace_support.py"


pytestmark = pytest.mark.milestone_50


def workspace_measurement(path: Path) -> dict[str, int]:
    """Measure an observed tree without following symlinked caller files."""
    if not path.exists():
        return {
            "workspaces": 0,
            "environments": 0,
            "logical_bytes": 0,
            "allocated_kib": 0,
        }
    files = [
        file for file in path.rglob("*") if file.is_file() and not file.is_symlink()
    ]
    allocated = subprocess.check_output(["du", "-sk", str(path)], text=True)
    return {
        "workspaces": 1,
        "environments": sum(file.name == "pyvenv.cfg" for file in files),
        "logical_bytes": sum(file.stat().st_size for file in files),
        "allocated_kib": int(allocated.split()[0]),
    }


BOOTSTRAP = f"""
import importlib.util
import json
import sys
import time
from pathlib import Path
import pytest

support_path = Path({str(SUPPORT)!r})
if support_path.exists():
    pytest.register_assert_rewrite('pytest_workspace_support')
    spec = importlib.util.spec_from_file_location('pytest_workspace_support', support_path)
    support = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = support
    spec.loader.exec_module(support)
    pytest_plugins = ['pytest_workspace_support']

def pytest_runtest_logreport(report):
    if report.when == 'teardown':
        print('EVENT ' + json.dumps(dict(node=report.nodeid, outcome=report.outcome)), flush=True)

def await_release():
    deadline = time.monotonic() + 30
    while not Path('release').exists():
        if time.monotonic() > deadline:
            raise TimeoutError('parent did not release later case')
        time.sleep(0.01)
"""


class PytestProcess:
    """A bounded parent/child handshake around completed teardown reports."""

    def __init__(
        self,
        project: Path,
        arguments: tuple[str, ...],
        temporary_root: Path | None = None,
    ) -> None:
        """Start pytest with isolated environment and stream completion events."""
        self.project = project
        environment = dict(os.environ)
        temporary = temporary_root or project / "temporary"
        temporary.mkdir(parents=True, exist_ok=True)
        environment["PYTEST_DEBUG_TEMPROOT"] = str(temporary)
        for key in (
            "PYTEST_ADDOPTS",
            "PYTEST_XDIST_WORKER",
            "PYTEST_XDIST_WORKER_COUNT",
            "PYTEST_CURRENT_TEST",
        ):
            environment.pop(key, None)
        self.process = subprocess.Popen(
            [sys.executable, "-m", "pytest", "-s", "-q", *arguments],
            cwd=project,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.events: queue.Queue[dict[str, str]] = queue.Queue()
        self.lines: list[str] = []
        self.reader = threading.Thread(target=self.read_output, daemon=True)
        self.reader.start()

    def read_output(self) -> None:
        """Collect stdout and expose teardown events independently of timing."""
        assert self.process.stdout is not None
        for line in self.process.stdout:
            self.lines.append(line)
            if "EVENT " in line:
                self.events.put(json.loads(line.split("EVENT ", 1)[1]))
        self.events.put({"node": "<process-exit>", "outcome": "exit"})

    def completed(self, name: str, timeout: float = 45) -> dict[str, str]:
        """Wait for the requested public teardown report."""
        while True:
            try:
                event = self.events.get(timeout=timeout)
            except queue.Empty as error:
                raise AssertionError(
                    "Missing teardown event:\n" + self.output
                ) from error
            if name in event["node"]:
                return event
            if event["node"] == "<process-exit>":
                raise AssertionError("Pytest exited before teardown:\n" + self.output)

    @property
    def output(self) -> str:
        """Return collected diagnostics."""
        return "".join(self.lines)

    def finish(self) -> int:
        """Release the later case and wait for a bounded child exit."""
        (self.project / "release").touch()
        code = self.process.wait(timeout=60)
        self.reader.join(timeout=5)
        return code


@contextmanager
def run_project(
    project: Path,
    source: str,
    *arguments: str,
    conftest: str = "",
    temporary_root: Path | None = None,
) -> Iterator[PytestProcess]:
    """Run a fresh generated project loading actual support when available."""
    project.mkdir(parents=True, exist_ok=True)
    (project / "pytest.ini").write_text(
        "[pytest]\ntmp_path_retention_count = 1\ntmp_path_retention_policy = failed\n"
    )
    (project / "conftest.py").write_text(BOOTSTRAP + conftest)
    (project / "test_example.py").write_text(source)
    process = PytestProcess(project, arguments, temporary_root)
    try:
        yield process
    finally:
        if process.process.poll() is None:
            try:
                process.finish()
            finally:
                if process.process.poll() is None:
                    process.process.kill()
                    process.process.wait(timeout=10)


def test_success_is_removed_after_finalizer_before_completion(tmp_path: Path) -> None:
    """The parent sees deletion before releasing a later test in the same session."""
    with run_project(
        tmp_path / "project",
        """
import json
from pathlib import Path
import pytest
from conftest import await_release

@pytest.fixture
def late_consumer():
    yield
    owned = Path(json.loads(Path('owned.json').read_text()))
    assert (owned / 'driver/child/diagnostic').read_text() == 'available'
    Path('late-finalized').touch()

@pytest.fixture
def consumer(tmp_path):
    nested = tmp_path / 'driver' / 'child'
    nested.mkdir(parents=True)
    (nested / 'diagnostic').write_text('available')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    yield nested
    assert (nested / 'diagnostic').read_text() == 'available'
    Path('finalized').touch()

def test_first(late_consumer, consumer):
    assert consumer.is_dir()

def test_later():
    await_release()
""",
    ) as child:
        assert child.completed("test_first")["outcome"] == "passed"
        assert (child.project / "finalized").is_file()
        assert (child.project / "late-finalized").is_file()
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert not owned.exists(), child.output
        assert child.process.poll() is None
        assert child.finish() == 0, child.output


def test_all_policy_retention_expires_with_numbered_session(tmp_path: Path) -> None:
    """The all override retains one numbered invocation rather than permanent data."""
    source = """
import json
from pathlib import Path
def test_first(tmp_path):
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    (tmp_path / 'diagnostic').write_text('numbered retention')
"""
    project = tmp_path / "project"
    with run_project(project, source, "-o", "tmp_path_retention_policy=all") as child:
        assert child.finish() == 0, child.output
        retained = Path(json.loads((project / "owned.json").read_text()))
        assert (retained / "diagnostic").is_file()
    with run_project(project, source) as child:
        assert child.finish() == 0, child.output
    assert not retained.exists()


def test_nested_links_do_not_transfer_caller_ownership(tmp_path: Path) -> None:
    """Cleaning an owned tree unlinks nested links without touching caller files."""
    with run_project(
        tmp_path / "project",
        """
from pathlib import Path
def test_first(tmp_path):
    caller = Path('caller').resolve()
    caller.mkdir()
    (caller / 'sentinel').write_text('caller evidence')
    (tmp_path / 'cache-link').symlink_to(caller, target_is_directory=True)
""",
    ) as child:
        assert child.finish() == 0, child.output
        assert (child.project / "caller/sentinel").read_text() == "caller evidence"


@pytest.mark.parametrize("phase", ["setup", "call", "teardown"])
def test_failure_retains_available_tree_and_reports_owner(
    tmp_path: Path, phase: str
) -> None:
    """Failures in every phase retain diagnostics through and after completion."""
    with run_project(
        tmp_path / "project",
        f"""
import json
from pathlib import Path
import pytest
from conftest import await_release

@pytest.fixture
def resource(tmp_path):
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    (tmp_path / 'diagnostic').write_text('failure evidence')
    if {phase!r} == 'setup':
        raise RuntimeError('original setup failure')
    yield
    if {phase!r} == 'teardown':
        raise RuntimeError('original teardown failure')

def test_first(resource):
    if {phase!r} == 'call':
        raise RuntimeError('original call failure')

def test_later():
    await_release()
""",
    ) as child:
        child.completed("test_first")
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert (owned / "diagnostic").read_text() == "failure evidence"
        assert child.process.poll() is None
        assert child.finish() == 1, child.output
        assert (owned / "diagnostic").is_file()
        assert f"WORKSPACE {owned}" in child.output
        assert f"original {phase} failure" in child.output


def test_cleanup_error_is_a_failed_teardown_with_remaining_path(tmp_path: Path) -> None:
    """A filesystem refusal is reported without crashing pytest or hiding the path."""
    with run_project(
        tmp_path / "project",
        """
import json
import shutil
from pathlib import Path

def test_first(tmp_path):
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    (tmp_path / 'diagnostic').write_text('cleanup evidence')
    original = shutil.rmtree
    def deny(path, *args, **kwargs):
        if Path(path) == tmp_path:
            raise PermissionError('injected filesystem refusal')
        return original(path, *args, **kwargs)
    shutil.rmtree = deny
""",
    ) as child:
        assert child.finish() == 1, child.output
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert (owned / "diagnostic").read_text() == "cleanup evidence"
        assert f"WORKSPACE {owned}" in child.output
        assert "injected filesystem refusal" in child.output
        assert "INTERNALERROR" not in child.output


@pytest.mark.parametrize("control", ["--keep-test-workspaces", "ini-all"])
def test_explicit_retention_preserves_successful_workspace(
    tmp_path: Path, control: str
) -> None:
    """CLI retention and the public all policy retain successful-test contents."""
    arguments = (
        ("-o", "tmp_path_retention_policy=all") if control == "ini-all" else (control,)
    )
    with run_project(
        tmp_path / "project",
        """
import json
from pathlib import Path
from conftest import await_release

def test_first(tmp_path):
    (tmp_path / 'diagnostic').write_text('retained success')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))

def test_later():
    await_release()
""",
        *arguments,
    ) as child:
        assert child.completed("test_first")["outcome"] == "passed"
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert (owned / "diagnostic").read_text() == "retained success"
        assert child.finish() == 0, child.output
        assert owned.is_dir()


def test_numbered_sessions_bound_failures_and_protect_explicit_retention(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    """A later completed numbered invocation evicts old failures, not kept trees."""
    project = tmp_path / "project"
    source = """
import json
from pathlib import Path

def test_first(tmp_path):
    (tmp_path / 'diagnostic').write_text('retention evidence')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    assert not Path('fail').exists(), 'intentional retained failure'
"""
    project.mkdir()
    (project / "fail").touch()
    with run_project(project, source) as child:
        assert child.finish() == 1, child.output
        failed = Path(json.loads((project / "owned.json").read_text()))
        assert failed.is_dir()
        failure_measurement = workspace_measurement(failed)
    (project / "fail").unlink()
    with run_project(project, source, "--keep-test-workspaces") as child:
        assert child.finish() == 0, child.output
        retained = Path(json.loads((project / "owned.json").read_text()))
        assert retained.is_dir()
        assert failed.is_dir()
    with run_project(project, source) as child:
        assert child.finish() == 0, child.output
        successful = Path(json.loads((project / "owned.json").read_text()))
        assert not successful.exists()
    assert not failed.exists()
    assert (retained / "diagnostic").read_text() == "retention evidence"
    request.node.user_properties.append(
        (
            "retention_measurements",
            json.dumps(
                {
                    "failure_at_session_exit": failure_measurement,
                    "failure_after_next_numbered_session": workspace_measurement(
                        failed
                    ),
                    "explicit_retention_after_next_session": workspace_measurement(
                        retained
                    ),
                }
            ),
        )
    )


@pytest.mark.parametrize("scope", ["module", "session"])
@pytest.mark.parametrize("failure", ["none", "consumer", "finalizer"])
def test_shared_workspace_waits_for_final_consumer_and_retains_failures(
    tmp_path: Path, scope: str, failure: str
) -> None:
    """Shared trees live across consumers and include the finalizer outcome."""
    with run_project(
        tmp_path / "project",
        f"""
import json
from pathlib import Path
import pytest
from conftest import await_release, support

@pytest.fixture(scope={scope!r})
def shared(request, tmp_path_factory):
    root = support.owned_workspace(request, tmp_path_factory, 'shared')
    (root / 'diagnostic').write_text('shared evidence')
    Path('shared.json').write_text(json.dumps(str(root)))
    yield root
    assert (root / 'diagnostic').read_text() == 'shared evidence'
    Path('shared-finalized').touch()
    if {failure!r} == 'finalizer':
        raise RuntimeError('original shared finalizer failure')

def test_first(shared):
    assert shared.is_dir()
    if {failure!r} == 'consumer':
        raise RuntimeError('original shared consumer failure')

def test_last(shared):
    await_release()
    assert (shared / 'diagnostic').read_text() == 'shared evidence'
""",
    ) as child:
        child.completed("test_first")
        shared = Path(json.loads((child.project / "shared.json").read_text()))
        assert (shared / "diagnostic").is_file()
        assert not (child.project / "shared-finalized").exists()
        assert child.process.poll() is None
        assert child.finish() == (0 if failure == "none" else 1), child.output
        assert (child.project / "shared-finalized").exists()
        assert shared.exists() == (failure != "none")
        if failure != "none":
            assert f"WORKSPACE {shared}" in child.output


@pytest.mark.parametrize("replacement", ["symlink", "directory", "parent"])
def test_replaced_ownership_cannot_delete_caller_or_records(
    tmp_path: Path, replacement: str
) -> None:
    """A changed root or parent is rejected and all caller evidence survives."""
    with run_project(
        tmp_path / "project",
        f"""
import json
from pathlib import Path

def test_first(tmp_path):
    caller = Path('.dev-records/verification').resolve()
    caller.mkdir(parents=True)
    (caller / 'sentinel').write_text('durable caller evidence')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    (tmp_path / 'original').write_text('original diagnostic')
    if {replacement!r} == 'parent':
        parent = tmp_path.parent
        parent.rename(parent.with_name(parent.name + '-original'))
        parent.symlink_to(caller, target_is_directory=True)
    else:
        tmp_path.rename(tmp_path.with_name(tmp_path.name + '-original'))
        if {replacement!r} == 'symlink':
            tmp_path.symlink_to(caller, target_is_directory=True)
        else:
            tmp_path.mkdir()
            (tmp_path / 'sentinel').write_text('replacement directory')
""",
        "--basetemp",
        str(tmp_path / "child-base"),
    ) as child:
        assert child.finish() == 1, child.output
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert "Workspace ownership changed" in child.output
        assert f"WORKSPACE {owned}" in child.output
        assert (
            child.project / ".dev-records/verification/sentinel"
        ).read_text() == "durable caller evidence"
        if replacement == "directory":
            assert (owned / "sentinel").read_text() == "replacement directory"


@pytest.mark.parametrize("target", ["caller", "records", "symlink"])
def test_unsafe_bases_are_rejected_before_pytest_clears_them(
    tmp_path: Path, target: str
) -> None:
    """Existing caller paths and durable-record overlaps cannot become bases."""
    project = tmp_path / "project"
    caller = tmp_path / "caller"
    caller.mkdir()
    (caller / "sentinel").write_text("caller evidence")
    records = project / ".dev-records/verification"
    records.mkdir(parents=True)
    (records / "sentinel").write_text("durable evidence")
    link = tmp_path / "link"
    link.symlink_to(caller, target_is_directory=True)
    base = {"caller": caller, "records": records / "new", "symlink": link}[target]
    with run_project(
        project,
        "def test_first(tmp_path):\n    assert tmp_path.is_dir()\n",
        "--basetemp",
        str(base),
    ) as child:
        assert child.finish() == 4, child.output
        assert "Unsafe workspace base" in child.output
    assert (caller / "sentinel").read_text() == "caller evidence"
    assert (records / "sentinel").read_text() == "durable evidence"


def wait_for_file(path: Path) -> None:
    """Wait for a child readiness signal, with a deadline rather than a delay."""
    deadline = time.monotonic() + 30
    while not path.exists():
        assert time.monotonic() < deadline, f"Missing child readiness signal: {path}"
        threading.Event().wait(0.01)


def test_concurrent_numbered_sessions_protect_active_workspaces(
    tmp_path: Path, request: pytest.FixtureRequest
) -> None:
    """A completed newer invocation cannot prune another active invocation."""
    source = """
import json
from pathlib import Path
from conftest import await_release

def test_active(tmp_path):
    (tmp_path / 'diagnostic').write_text('active evidence')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    Path('ready').touch()
    await_release()
"""
    common = tmp_path / "numbered"
    with run_project(tmp_path / "first", source, temporary_root=common) as first:
        wait_for_file(first.project / "ready")
        first_owned = Path(json.loads((first.project / "owned.json").read_text()))
        with run_project(tmp_path / "second", source, temporary_root=common) as second:
            wait_for_file(second.project / "ready")
            second_owned = Path(json.loads((second.project / "owned.json").read_text()))
            assert first_owned != second_owned
            assert first_owned.parent != second_owned.parent
            assert second.finish() == 0, second.output
            assert not second_owned.exists()
            assert (first_owned / "diagnostic").read_text() == "active evidence"
            assert first.process.poll() is None
            active_measurement = workspace_measurement(first_owned)
            completed_measurement = workspace_measurement(second_owned)
        assert first.finish() == 0, first.output
        assert not first_owned.exists()
        request.node.user_properties.append(
            (
                "concurrent_measurements",
                json.dumps(
                    {
                        "first_active_after_second_exit": active_measurement,
                        "second_after_exit": completed_measurement,
                        "first_after_exit": workspace_measurement(first_owned),
                    }
                ),
            )
        )


def test_four_workers_clean_distinct_roots_before_later_case(tmp_path: Path) -> None:
    """Four real workers publish absent roots while another case is still active."""
    with run_project(
        tmp_path / "project",
        """
import json
from pathlib import Path
import pytest
from conftest import await_release

@pytest.mark.parametrize('case', range(4))
def test_first(tmp_path, worker_id, case):
    nested = tmp_path / 'driver/child'
    nested.mkdir(parents=True)
    (nested / 'sentinel').write_text('worker evidence')
    Path(f'case-{case}.json').write_text(json.dumps(dict(root=str(tmp_path), worker=worker_id)))

def test_later():
    Path('later-ready').touch()
    await_release()
""",
        "-n",
        "4",
        "--dist=loadgroup",
        "--basetemp",
        str(tmp_path / "nested-workers"),
    ) as child:
        for _ in range(4):
            assert child.completed("test_first")["outcome"] == "passed"
        wait_for_file(child.project / "later-ready")
        records = [
            json.loads(path.read_text()) for path in child.project.glob("case-*.json")
        ]
        assert len(records) == 4
        assert len({record["worker"] for record in records}) == 4
        roots = [Path(record["root"]) for record in records]
        assert len(set(roots)) == 4
        assert all(root.is_relative_to(tmp_path / "nested-workers") for root in roots)
        assert all(not root.exists() for root in roots)
        assert child.process.poll() is None
        assert child.finish() == 0, child.output


def test_nested_pytest_uses_child_base_and_preserves_parent_until_teardown(
    tmp_path: Path,
) -> None:
    """Nested pytest deletes its own roots without clearing its active parent."""
    with run_project(
        tmp_path / "project",
        """
import json
import subprocess
import sys
from pathlib import Path
from conftest import await_release

def test_first(tmp_path):
    parent = tmp_path / 'sentinel'
    parent.write_text('parent evidence')
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    project = Path('nested').resolve()
    project.mkdir()
    (project / 'pytest.ini').write_text('[pytest]\\ntmp_path_retention_policy=failed\\ntmp_path_retention_count=1\\n')
    (project / 'conftest.py').write_text(Path('conftest.py').read_text())
    (project / 'test_inner.py').write_text("import json\\nfrom pathlib import Path\\ndef test_inner(tmp_path):\\n    Path('inner.json').write_text(json.dumps(str(tmp_path)))\\n    (tmp_path / 'child').mkdir()\\n")
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '--basetemp', str(tmp_path / 'nested-pytest')], cwd=project, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    inner = Path(json.loads((project / 'inner.json').read_text()))
    assert inner.is_relative_to(tmp_path / 'nested-pytest')
    assert not inner.exists()
    assert parent.read_text() == 'parent evidence'

def test_later():
    await_release()
""",
    ) as child:
        assert child.completed("test_first")["outcome"] == "passed"
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert not owned.exists()
        assert child.process.poll() is None
        assert child.finish() == 0, child.output


@pytest.mark.parametrize(
    "module_name,fixture_name",
    [
        ("test_distribution_verification", "artifacts"),
        ("test_installation_verification", "source_repository"),
        ("test_initialization", "source_repository"),
        ("test_verification_lifecycle", "lifecycle_artifacts"),
        ("test_installation_verification", "installed_project"),
    ],
)
def test_existing_shared_fixture_survives_consumers_then_is_removed(
    tmp_path: Path, module_name: str, fixture_name: str
) -> None:
    """Actual contributor fixtures release their original scope after consumers."""
    module_path = ROOT / "tests/integration" / (module_name + ".py")
    with run_project(
        tmp_path / "project",
        f"""
import importlib.util
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from conftest import await_release

spec = importlib.util.spec_from_file_location('actual_fixtures', {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if hasattr(module, 'source_repository'):
    source_repository = module.source_repository
shared = getattr(module, {fixture_name!r})

def root_of(value):
    if isinstance(value, tuple):
        if isinstance(value[0], str):
            return Path(unquote(urlsplit(value[0]).path))
        return value[0].parent.parent
    return value

def test_first(shared):
    root = root_of(shared)
    assert root.is_dir()
    Path('shared.json').write_text(json.dumps(str(root)))

def test_last(shared):
    await_release()
    assert root_of(shared).is_dir()
""",
    ) as child:
        child.completed("test_first")
        shared = Path(json.loads((child.project / "shared.json").read_text()))
        assert shared.is_dir()
        assert child.finish() == 0, child.output
        assert not shared.exists()


@pytest.mark.parametrize(
    "driver,mode",
    [
        ("distribution", "success"),
        ("distribution", "failure"),
        ("distribution", "keep"),
        ("installation", "success"),
        ("initialization", "success"),
        ("planning", "success"),
    ],
)
def test_real_driver_tree_obeys_outer_test_outcome_before_session_exit(
    tmp_path: Path, driver: str, mode: str, request: pytest.FixtureRequest
) -> None:
    """Real installed probes finish before the outer owner releases their trees."""
    modules = {
        "distribution": "test_distribution_verification",
        "installation": "test_installation_verification",
        "initialization": "test_verification_lifecycle",
        "planning": "test_distribution_verification",
    }
    calls = {
        "distribution": "module.test_explicit_distribution_retention_keeps_both_interpreters(artifacts, tmp_path)",
        "installation": "module.test_pinned_project_runs_without_checkout_or_cache(source_repository, tmp_path)",
        "initialization": "module.test_initialization_cleans_after_final_consumer(lifecycle_artifacts, tmp_path, False)",
        "planning": "module.test_planning_from_both_artifact_paths(artifacts, tmp_path)",
    }
    dependencies = {
        "distribution": "artifacts",
        "installation": "source_repository",
        "initialization": "lifecycle_artifacts",
        "planning": "artifacts",
    }
    module_path = ROOT / "tests/integration" / (modules[driver] + ".py")
    dependency = dependencies[driver]
    arguments = ("--keep-test-workspaces",) if mode == "keep" else ()
    with run_project(
        tmp_path / "project",
        f"""
import importlib.util
import json
from pathlib import Path
from conftest import await_release

spec = importlib.util.spec_from_file_location('actual_driver_tests', {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
{dependency} = getattr(module, {dependency!r})

def test_first(tmp_path, {dependency}):
    Path('owned.json').write_text(json.dumps(str(tmp_path)))
    {calls[driver]}
    Path('probes-finished').touch()
    assert {mode!r} != 'failure', 'outer test fails after successful driver probes'

def test_later():
    await_release()
""",
        *arguments,
    ) as child:
        # The initialization command keeps its existing 600-second timeout.
        child.completed("test_first", timeout=600)
        assert (child.project / "probes-finished").is_file(), child.output
        owned = Path(json.loads((child.project / "owned.json").read_text()))
        assert owned.exists() == (mode != "success")
        if driver == "distribution" and mode != "success":
            assert len(list(owned.rglob("pyvenv.cfg"))) == 2
        teardown_measurement = workspace_measurement(owned)
        assert child.process.poll() is None
        assert child.finish() == (1 if mode == "failure" else 0), child.output
        request.node.user_properties.append(
            (
                "real_driver_measurements",
                json.dumps(
                    {
                        "driver": driver,
                        "mode": mode,
                        "at_completed_teardown": teardown_measurement,
                        "at_session_exit": workspace_measurement(owned),
                    }
                ),
            )
        )


@pytest.mark.parametrize(
    "driver", ["distribution", "installation", "initialization", "planning"]
)
@pytest.mark.parametrize("keep", [False, True])
def test_standalone_default_allocation_reports_diagnostics_without_pytest_context(
    tmp_path: Path, driver: str, keep: bool
) -> None:
    """Independent commands retain failed diagnostics in a caller-controlled temp root."""
    paths = {
        "distribution": "tests/packaging/verify_distributions.py",
        "installation": "tests/installation/verify_installation.py",
        "initialization": "tests/installation/verify_initialization.py",
        "planning": "tests/installation/verify_planning.py",
    }
    temporary = tmp_path / "standalone-temporary"
    temporary.mkdir()
    cwd = tmp_path / "unrelated-cwd"
    cwd.mkdir()
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("PYTEST")
    }
    environment["TMPDIR"] = str(temporary)
    arguments = (
        [
            "--repository",
            (tmp_path / "missing-repository").as_uri(),
            "--revision",
            "0" * 40,
        ]
        if driver == "installation"
        else ["--artifacts-dir", str(tmp_path / "missing-artifacts")]
    )
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / paths[driver]),
            *arguments,
            *(["--keep-workspace"] if keep else []),
        ],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    workspaces = [
        Path(line.removeprefix("WORKSPACE "))
        for line in result.stdout.splitlines()
        if line.startswith("WORKSPACE ")
    ]
    assert workspaces, result.stdout + result.stderr
    assert all(path.is_dir() and path.is_relative_to(temporary) for path in workspaces)
    records = [
        Path(line.removeprefix("RECORDS "))
        for line in result.stdout.splitlines()
        if line.startswith("RECORDS ")
    ]
    assert records
    for record in records:
        assert record.is_relative_to(ROOT / ".dev-records/verification")
        summary = json.loads((record / "summary.json").read_text())
        assert summary["cleanup"] == "retained"
        assert summary["verification_exit_code"] != 0
