"""Verify parallel scheduling through the installed pytest command."""

import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.infrastructure


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
        (None, "7 passed, 4 deselected"),
        ("milestone_1", "2 passed, 9 deselected"),
        ("milestone_50", "1 passed, 10 deselected"),
        ("", "11 passed"),
    ],
)
def test_verification_schedule_selects_expected_group(
    tmp_path: Path, selector: str | None, expected: str
) -> None:
    """Real pytest selects exactly the declared milestone associations."""
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
    cases = "import pytest\n"
    for milestone in (0, 1, 2, 3, 4, 5, 6, 50, 99):
        cases += f"@pytest.mark.milestone_{milestone}\ndef test_m{milestone}(): pass\n"
    cases += "@pytest.mark.infrastructure\ndef test_infrastructure(): pass\n"
    cases += (
        "@pytest.mark.milestone_1\n@pytest.mark.milestone_2\ndef test_overlap(): pass\n"
    )
    (tmp_path / "test_schedule.py").write_text(cases)
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
    expected_cases = {
        None: {"m1", "m2", "m3", "m4", "m5", "m6", "overlap"},
        "milestone_1": {"m1", "overlap"},
        "milestone_50": {"m50"},
        "": {
            "m0",
            "m1",
            "m2",
            "m3",
            "m4",
            "m5",
            "m6",
            "m50",
            "m99",
            "infrastructure",
            "overlap",
        },
    }
    executed = re.findall(r"::test_(\w+) PASSED", result.stdout)
    assert set(executed) == expected_cases[selector]
    assert len(executed) == len(expected_cases[selector])


def test_verification_schedule_rejects_missing_classification(tmp_path: Path) -> None:
    """Unclassified tests fail collection even when the selector excludes them."""
    root = Path(__file__).resolve().parents[2]
    shutil.copyfile(root / "tests/conftest.py", tmp_path / "conftest.py")
    (tmp_path / "pytest.ini").write_text("[pytest]\nmarkers =\n    milestone_1\n")
    (tmp_path / "test_conflict.py").write_text("def test_unclassified():\n    pass\n")
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
            "milestone_1",
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
    assert "Missing test classification" in result.stderr
    assert "test_conflict.py::test_unclassified" in result.stderr
