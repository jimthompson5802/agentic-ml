"""Verify parallel scheduling through the installed pytest command."""

import json
import os
import subprocess
import sys
from pathlib import Path


def test_loadgroup_keeps_each_marked_group_on_one_worker(tmp_path: Path) -> None:
    """Marked cases share one worker while separate groups can run in parallel."""
    (tmp_path / "pytest.ini").write_text("[pytest]\naddopts = --strict-markers\n")
    (tmp_path / "test_groups.py").write_text(
        """
import json
from pathlib import Path
import pytest

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
