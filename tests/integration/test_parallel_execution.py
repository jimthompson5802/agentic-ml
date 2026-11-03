"""Verify parallel scheduling through the installed pytest command."""

import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.story_acceptance


def test_loadgroup_keeps_each_marked_group_on_one_worker(tmp_path: Path) -> None:
    """Marked cases share one worker while separate groups can run in parallel."""
    (tmp_path / "pytest.ini").write_text("[pytest]\naddopts = --strict-markers\n")
    (tmp_path / "test_groups.py").write_text(
        """
import json
from pathlib import Path
import pytest

@pytest.fixture(scope='session', autouse=True)
def record_temporary_base(tmp_path_factory, worker_id):
    Path(f'temp-base-{worker_id}.txt').write_text(str(tmp_path_factory.getbasetemp()))

@pytest.mark.parametrize('case', range(4))
@pytest.mark.xdist_group('alpha')
def test_alpha(case, worker_id):
    Path(f'alpha-{case}.json').write_text(json.dumps(worker_id))

@pytest.mark.parametrize('case', range(4))
@pytest.mark.xdist_group('beta')
def test_beta(case, worker_id):
    Path(f'beta-{case}.json').write_text(json.dumps(worker_id))
"""
    )
    env = dict(os.environ)
    for key in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER", "PYTEST_XDIST_WORKER_COUNT"):
        env.pop(key, None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-n",
            "4",
            "--dist=loadgroup",
            # Keep nested pytest out of unrelated sessions' retention cleanup.
            "--basetemp",
            str(tmp_path / "nested-pytest"),
            "-q",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "8 passed" in result.stdout
    group_workers: list[str] = []
    for group in ("alpha", "beta"):
        records = list(tmp_path.glob(f"{group}-*.json"))
        assert len(records) == 4
        workers = {json.loads(record.read_text()) for record in records}
        assert len(workers) == 1, f"{group} split across workers: {workers}"
        group_workers.append(workers.pop())
    assert group_workers[0] != group_workers[1]
    for worker in group_workers:
        temporary_base = Path((tmp_path / f"temp-base-{worker}.txt").read_text())
        assert temporary_base.is_relative_to((tmp_path / "nested-pytest").resolve())


@pytest.mark.parametrize(
    "selector,expected",
    [
        (None, "1 passed, 1 deselected"),
        ("story_acceptance", "1 passed, 1 deselected"),
        ("", "2 passed"),
    ],
)
def test_verification_schedule_selects_expected_group(
    tmp_path: Path, selector: str | None, expected: str
) -> None:
    """Real pytest honors the repository schedule for new and acceptance tests."""
    root = Path(__file__).resolve().parents[2]
    configuration = tomllib.loads((root / "pyproject.toml").read_text())
    options = configuration["tool"]["pytest"]["ini_options"]
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\naddopts = "
        + options["addopts"]
        + "\nmarkers =\n"
        + "".join("    " + marker + "\n" for marker in options["markers"])
    )
    shutil.copyfile(root / "tests/conftest.py", tmp_path / "conftest.py")
    (tmp_path / "test_schedule.py").write_text(
        "import pytest\n"
        "def test_new_phase():\n    pass\n"
        "@pytest.mark.story_acceptance\n"
        "def test_acceptance():\n    pass\n"
    )
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--basetemp",
        str(tmp_path / "nested-pytest"),
    ]
    if selector is not None:
        command.extend(["-m", selector])
    env = dict(os.environ)
    for key in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER", "PYTEST_XDIST_WORKER_COUNT"):
        env.pop(key, None)
    env["PYTHONPATH"] = str(root / "tests")
    result = subprocess.run(
        command,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert expected in result.stdout
    if selector is None:
        # Ensure the selected case is the new phase test, not the acceptance test.
        assert "test_new_phase PASSED" in result.stdout
    elif selector == "story_acceptance":
        assert "test_acceptance PASSED" in result.stdout


def test_verification_schedule_rejects_conflicting_groups(tmp_path: Path) -> None:
    """Conflicting module and function schedules fail even with a selector."""
    root = Path(__file__).resolve().parents[2]
    shutil.copyfile(root / "tests/conftest.py", tmp_path / "conftest.py")
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\nmarkers =\n    phase\n    story_acceptance\n"
    )
    (tmp_path / "test_conflict.py").write_text(
        "import pytest\npytestmark = pytest.mark.story_acceptance\n"
        "@pytest.mark.phase\ndef test_conflict():\n    pass\n"
    )
    env = dict(os.environ)
    for key in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER", "PYTEST_XDIST_WORKER_COUNT"):
        env.pop(key, None)
    env["PYTHONPATH"] = str(root / "tests")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-m",
            "phase",
            "--basetemp",
            str(tmp_path / "nested-pytest"),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 4, result.stdout + result.stderr
    assert "Conflicting verification groups" in result.stderr
