"""US-26: public results recording inspected through native MLflow interfaces."""

import copy
import json
import shutil
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from mlflow import MlflowClient
from pytest_workspace_support import owned_workspace
from tracking_support import TrackingCase, command, prepare_project

ROOT = Path(__file__).resolve().parents[2]
pytestmark = [pytest.mark.milestone_1, pytest.mark.xdist_group("tracking")]


@pytest.fixture(scope="module")
def installed_project(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> tuple[Path, dict[str, Any]]:
    """Build one direct wheel and install it normally in a separate experiment."""
    workspace = owned_workspace(request, tmp_path_factory, "tracking-project")
    source = workspace / "source"
    source.mkdir()
    shutil.copytree(ROOT / "src", source / "src")
    for name in ("pyproject.toml", "README.md"):
        shutil.copy(ROOT / name, source)
    project = workspace / "experiment"
    project.mkdir()
    command(project, "uv", "init", "--no-package", "--python", "3.12")
    if getattr(request, "param", "wheel") == "git":
        command(source, "git", "init")
        command(source, "git", "config", "user.email", "fixture@example.invalid")
        command(source, "git", "config", "user.name", "US-26 source")
        command(source, "git", "add", ".")
        command(source, "git", "commit", "-m", "feat: tracking source fixture")
        revision = command(source, "git", "rev-parse", "HEAD")
        command(project, "uv", "add", "git+" + source.as_uri() + "@" + revision)
    else:
        command(source, "uv", "build", "--wheel", "--out-dir", str(workspace / "dist"))
        wheel = next((workspace / "dist").glob("*.whl"))
        command(project, "uv", "add", str(wheel))
    provenance = prepare_project(project)
    return project, provenance


@pytest.fixture
def case(
    installed_project: tuple[Path, dict[str, Any]], tmp_path: Path
) -> Iterator[TrackingCase]:
    """Provide a fresh native run and restore declared input bytes after each case."""
    root, provenance = installed_project
    saved = {
        root / name: (root / name).read_bytes()
        for name in [
            "experiment.py",
            "config.json",
            "uv.lock",
            "data.dvc",
            "data/input.csv",
            "data/split.json",
        ]
    }
    (root / "predictions.csv").write_bytes(b"id,prediction\n1,A\n")
    store = tmp_path / uuid.uuid4().hex
    store.mkdir()
    uri = f"sqlite:///{store}/tracking.db"
    client = MlflowClient(tracking_uri=uri)
    experiment = client.create_experiment(
        "results", artifact_location=(store / "artifacts").as_uri()
    )
    yield TrackingCase(
        root,
        uri,
        client,
        client.create_run(experiment).info.run_id,
        copy.deepcopy(provenance),
    )
    for path, data in saved.items():
        path.write_bytes(data)


def test_records_results_in_requested_existing_run(case: TrackingCase) -> None:
    """AC-01/05: native values, output bytes and artifact locations agree."""
    answer = case.invoke()
    assert "error" not in answer, answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == "FINISHED"
    assert run.data.params == {"C": "1", "settings": '{"depth":2}'}
    assert run.data.metrics == {"validation_accuracy": 0.75}
    assert run.data.tags["validation_status"] == "passed"
    assert answer["result"] == {
        "run_id": case.run_id,
        "artifacts": {
            "predictions": run.info.artifact_uri
            + "/outputs/predictions/predictions.csv",
            "provenance": run.info.artifact_uri + "/provenance.json",
        },
        "process_exit_code": 0,
        "validation_status": "passed",
    }
    downloaded = case.client.download_artifacts(
        case.run_id, "outputs/predictions/predictions.csv"
    )
    assert Path(downloaded).read_bytes() == b"id,prediction\n1,A\n"
    provenance = case.client.download_artifacts(case.run_id, "provenance.json")
    assert json.loads(Path(provenance).read_text()) == case.provenance


def test_links_committed_provenance_to_native_run(case: TrackingCase) -> None:
    """AC-02/03/04: native run references match independently read project inputs."""
    answer = case.invoke()
    assert "error" not in answer, answer
    tags = case.client.get_run(case.run_id).data.tags
    assert tags["experiment_commit"] == command(
        case.root,
        "git",
        "rev-parse",
        case.provenance["experiment"]["commit_sha"] + "^{commit}",
    )
    assert tags["toolkit_version"] == "0.1.0"
    assert tags["provenance_schema_version"] == "1.0"


@pytest.mark.parametrize(
    "name", ["experiment.py", "config.json", "uv.lock", "data.dvc"]
)
def test_rejects_changed_committed_reference(case: TrackingCase, name: str) -> None:
    """AC-02/03/04: consumed code/config/lock/pointer cannot differ from commit."""
    (case.root / name).write_bytes((case.root / name).read_bytes() + b"\n")
    # Updating the supplied digest must not bypass the committed-blob comparison.
    from tracking_support import file_ref

    reference = file_ref(case.root, name)
    if name == "experiment.py":
        case.provenance["experiment"]["entrypoint"] = reference
        case.provenance["experiment"]["code"] = [reference]
    elif name == "config.json":
        case.provenance["configuration"]["files"] = [reference]
    elif name == "uv.lock":
        case.provenance["environment"]["lockfile"] = reference
    else:
        for item in case.provenance["data"]:
            item["metadata"] = reference
    answer = case.invoke()
    assert answer.get("error") == "ValueError", answer
    assert name in answer["message"]


@pytest.mark.parametrize("mutation", ["extra", "missing", "version", "nonfinite"])
def test_rejects_invalid_provenance_schema(case: TrackingCase, mutation: str) -> None:
    """AC-02/03: unsupported provenance cannot be recorded as successful output."""
    if mutation == "extra":
        case.provenance["unexpected"] = True
    elif mutation == "missing":
        del case.provenance["schema_version"]
    elif mutation == "version":
        case.provenance["schema_version"] = "2.0"
    else:
        case.provenance["configuration"]["effective"]["C"] = float("nan")
    answer = case.invoke()
    assert answer.get("error") == "ValueError", answer
    assert "provenance" in answer["message"]


@pytest.mark.parametrize(
    "mutation", ["hash", "member", "changed_data", "missing_split"]
)
def test_checks_native_dvc_inputs(case: TrackingCase, mutation: str) -> None:
    """AC-02/05: pointer identity, consumed members and current bytes must agree."""
    if mutation == "hash":
        case.provenance["data"][0]["hash_value"] = "0" * 32 + ".dir"
    elif mutation == "member":
        case.provenance["data"][0]["member_path"] = "absent.csv"
    elif mutation == "changed_data":
        (case.root / "data/input.csv").write_text("id,x,label\n0,999,A\n1,3,B\n")
    else:
        (case.root / "data/split.json").unlink()
    answer = case.invoke()
    assert answer.get("error") in {"ValueError", "FileNotFoundError"}, answer
    assert "data" in answer["message"] or "split" in answer["message"]


@pytest.mark.parametrize(
    "mutation",
    ["library", "python", "wheel_digest", "wheel_version", "invented_source"],
)
def test_checks_installed_environment_identity(
    case: TrackingCase, mutation: str
) -> None:
    """AC-03: installed versions/origin/locked archive must match provenance."""
    if mutation == "library":
        case.provenance["environment"]["libraries"]["pandas"] = "0.0.0"
    elif mutation == "python":
        case.provenance["environment"]["python_version"] = "0.0.0"
    elif mutation == "wheel_digest":
        case.provenance["toolkit"]["installation"]["sha256"] = "0" * 64
    elif mutation == "wheel_version":
        case.provenance["toolkit"]["installation"]["version"] = "0.0.0"
    else:
        case.provenance["toolkit"]["commit_sha"] = "0" * 40
    answer = case.invoke()
    assert answer.get("error") == "ValueError", answer
    assert "environment" in answer["message"] or "toolkit" in answer["message"]


def test_rejects_conflicting_shared_provenance(
    case: TrackingCase, tmp_path: Path
) -> None:
    """AC-02/05: an existing shared record cannot be silently overwritten."""
    other = copy.deepcopy(case.provenance)
    other["configuration"]["effective"]["C"] = 99
    existing = tmp_path / "provenance.json"
    existing.write_text(json.dumps(other))
    case.client.log_artifact(case.run_id, str(existing))
    answer = case.invoke()
    assert answer.get("error") == "FileExistsError", answer
    downloaded = case.client.download_artifacts(case.run_id, "provenance.json")
    assert Path(downloaded).read_bytes() == existing.read_bytes()


@pytest.mark.parametrize("root_kind", ["relative", "missing"])
def test_requires_explicit_absolute_project_root(
    case: TrackingCase, root_kind: str
) -> None:
    """AC-02/04: a caller's cwd cannot supply missing project-root context."""
    root = "." if root_kind == "relative" else str(case.root.parent / "absent")
    answer = case.invoke(project_root=root)
    assert answer.get("error") == "ValueError", answer
    assert "project_root" in answer["message"]


def test_accepts_native_directory_data_reference(case: TrackingCase) -> None:
    """AC-02: a directory output can identify consumed data without a member."""
    case.provenance["data"][0]["member_path"] = None
    answer = case.invoke()
    assert "error" not in answer, answer
    downloaded = case.client.download_artifacts(case.run_id, "provenance.json")
    assert json.loads(Path(downloaded).read_text()) == case.provenance


@pytest.mark.parametrize("installed_project", ["git"], indirect=True)
def test_preserves_full_sha_git_installation(case: TrackingCase) -> None:
    """AC-03: reuse accepted Git origin/pin identity without a fake wheel hash."""
    answer = case.invoke()
    assert "error" not in answer, answer
    installation = case.provenance["toolkit"]["installation"]
    assert installation["kind"] == "git"
    assert len(installation["revision"]) == 40
    downloaded = case.client.download_artifacts(case.run_id, "provenance.json")
    saved = json.loads(Path(downloaded).read_text())
    assert saved["toolkit"]["commit_sha"] == installation["revision"]
    assert saved["toolkit"]["repository_url"] == installation["url"]


@pytest.mark.parametrize("mutation", ["missing", "checksum", "traversal", "symlink"])
def test_rejects_invalid_file_references(case: TrackingCase, mutation: str) -> None:
    """AC-02/04/05: consumed file references must be readable, safe and intact."""
    if mutation == "missing":
        (case.root / "config.json").unlink()
    elif mutation == "checksum":
        case.provenance["configuration"]["files"][0]["sha256"] = "sha256:" + "0" * 64
    elif mutation == "traversal":
        case.provenance["configuration"]["files"][0]["path"] = "../config.json"
    else:
        link = case.root / "linked.json"
        link.symlink_to(case.root / "config.json")
        case.provenance["configuration"]["files"][0]["path"] = "linked.json"
    answer = case.invoke()
    assert answer.get("error") == (
        "FileNotFoundError" if mutation == "missing" else "ValueError"
    ), answer


@pytest.mark.parametrize("failure", ["missing_output", "process_exit"])
def test_failed_execution_retains_available_diagnostics(
    case: TrackingCase, failure: str
) -> None:
    """AC-01/05: failure stays distinct from exit zero and preserves stdout."""
    (case.root / "stdout.txt").write_bytes(b"completed preparation\n")
    if failure == "missing_output":
        (case.root / "predictions.csv").unlink()
    answer = case.invoke(
        outputs={"predictions": "predictions.csv", "stdout": "stdout.txt"},
        process_exit_code=0 if failure == "missing_output" else 7,
    )
    assert answer.get("error") == (
        "FileNotFoundError" if failure == "missing_output" else "RuntimeError"
    ), answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == "FAILED"
    assert run.data.tags["process_exit_code"] == (
        "0" if failure == "missing_output" else "7"
    )
    assert run.data.tags["validation_status"] == "passed"
    assert any(case.run_id in note for note in answer["notes"])
    downloaded = case.client.download_artifacts(
        case.run_id, "outputs/stdout/stdout.txt"
    )
    assert Path(downloaded).read_bytes() == b"completed preparation\n"


@pytest.mark.parametrize(
    ("changes", "error"),
    [
        ({"expected_outputs": []}, "ValueError"),
        ({"expected_outputs": ["predictions", "predictions"]}, "ValueError"),
        ({"expected_outputs": ["absent"]}, "FileNotFoundError"),
        ({"outputs": {"../outside": "predictions.csv"}}, "ValueError"),
        ({"process_exit_code": True}, "TypeError"),
        ({"validation_passed": "passed"}, "TypeError"),
        ({"metrics": {"accuracy": float("nan")}}, "ValueError"),
        ({"metrics": {"accuracy": float("inf")}}, "ValueError"),
        ({"parameters": {"C": float("nan")}}, "ValueError"),
    ],
)
def test_rejects_invalid_result_declarations(
    case: TrackingCase, changes: dict[str, Any], error: str
) -> None:
    """AC-01/05: invalid bounds/status/values cannot become successful records."""
    answer = case.invoke(**changes)
    assert answer.get("error") == error, answer
    assert case.client.get_run(case.run_id).info.status == "FAILED"


@pytest.mark.parametrize("status", ["FINISHED", "FAILED", "KILLED"])
def test_rejects_finalized_run_without_changing_it(
    case: TrackingCase, status: str
) -> None:
    """AC-01/05: existing terminal records cannot be reopened by result logging."""
    case.client.set_terminated(case.run_id, status=status)
    answer = case.invoke()
    assert answer.get("error") == "ValueError", answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == status
    assert run.data.params == {}
    assert case.client.list_artifacts(case.run_id) == []


@pytest.mark.parametrize(
    ("error_cell", "missing_output"), [(False, False), (True, False), (False, True)]
)
def test_preserves_executed_notebook_bytes(
    case: TrackingCase, error_cell: bool, missing_output: bool
) -> None:
    """AC-04/05: fresh-kernel outputs/error cells and committed source are retained."""
    from tracking_support import file_ref

    script = """
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from jupyter_client import KernelManager
cell = "raise ValueError('notebook failure')" if sys.argv[1]=='error' else "print('fresh-kernel output')"
book=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(cell)])
nbformat.write(book,'source.ipynb')
manager=KernelManager(kernel_name='python3')
manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
try:
    NotebookClient(book,km=manager,timeout=30,resources={'metadata':{'path':str(Path.cwd())}}).execute()
except CellExecutionError:
    if sys.argv[1]!='error':
        raise
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
nbformat.write(book,'executed.ipynb')
"""
    command(
        case.root,
        str(case.root / ".venv/bin/python"),
        "-I",
        "-c",
        script,
        "error" if error_cell else "success",
    )
    command(case.root, "git", "add", "source.ipynb")
    command(case.root, "git", "commit", "-m", "feat: commit source notebook")
    case.provenance["experiment"]["commit_sha"] = command(
        case.root, "git", "rev-parse", "HEAD"
    )
    case.provenance["experiment"]["code"].append(file_ref(case.root, "source.ipynb"))
    before = (case.root / "executed.ipynb").read_bytes()
    book = json.loads(before)
    outputs = book["cells"][0]["outputs"]
    assert outputs[0]["output_type"] == ("error" if error_cell else "stream")
    if missing_output:
        (case.root / "predictions.csv").unlink()
    answer = case.invoke(
        executed_notebook="executed.ipynb", process_exit_code=1 if error_cell else 0
    )
    if error_cell or missing_output:
        assert answer.get("error") == (
            "FileNotFoundError" if missing_output else "RuntimeError"
        ), answer
        assert case.client.get_run(case.run_id).info.status == "FAILED"
    else:
        assert "error" not in answer, answer
        assert answer["result"]["artifacts"]["notebook"].endswith(
            "/notebooks/executed.ipynb"
        )
    downloaded = case.client.download_artifacts(case.run_id, "notebooks/executed.ipynb")
    assert Path(downloaded).read_bytes() == before
    assert (case.root / "executed.ipynb").read_bytes() == before


@pytest.mark.parametrize("mutation", ["invalid_structure", "missing_source"])
def test_checks_notebook_structure_and_source_link(
    case: TrackingCase, mutation: str
) -> None:
    """AC-04/05: notebook artifacts require valid structure and committed source."""
    book = {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []}
    if mutation == "invalid_structure":
        book["cells"] = "invalid"
    (case.root / "executed.ipynb").write_text(json.dumps(book))
    answer = case.invoke(executed_notebook="executed.ipynb")
    assert answer.get("error") == "ValueError", answer
    assert "notebook" in answer["message"]
    assert case.client.get_run(case.run_id).info.status == "FAILED"


def test_rejects_existing_output_artifact(case: TrackingCase, tmp_path: Path) -> None:
    """AC-01/05: result publication cannot overwrite another completed artifact."""
    existing = tmp_path / "predictions.csv"
    existing.write_bytes(b"original output\n")
    case.client.log_artifact(case.run_id, str(existing), "outputs/predictions")
    answer = case.invoke()
    assert answer.get("error") == "FileExistsError", answer
    assert case.client.get_run(case.run_id).info.status == "FAILED"
    downloaded = case.client.download_artifacts(
        case.run_id, "outputs/predictions/predictions.csv"
    )
    assert Path(downloaded).read_bytes() == b"original output\n"


@pytest.mark.parametrize("mutation", ["reserved_name", "symlink", "directory"])
def test_rejects_unsafe_output_inputs(case: TrackingCase, mutation: str) -> None:
    """AC-01/05: outputs are unambiguous named regular files without links."""
    name, source = "predictions", "predictions.csv"
    if mutation == "reserved_name":
        name = "provenance"
    elif mutation == "symlink":
        source = "linked-predictions.csv"
        (case.root / source).symlink_to(case.root / "predictions.csv")
    else:
        source = "data"
    answer = case.invoke(outputs={name: source}, expected_outputs=[name])
    assert answer.get("error") == "ValueError", answer
    assert case.client.get_run(case.run_id).info.status == "FAILED"


def test_requires_explicit_tracking_uri(case: TrackingCase) -> None:
    """AC-01: empty storage selection cannot fall back to an ambient store."""
    answer = case.invoke(tracking_uri="")
    assert answer.get("error") == "ValueError", answer
    assert "tracking_uri" in answer["message"]
    assert case.client.get_run(case.run_id).info.status == "RUNNING"


def test_records_process_exit_when_expected_name_is_missing(case: TrackingCase) -> None:
    """AC-05: native recording failure still exposes the supplied zero exit."""
    answer = case.invoke(expected_outputs=["absent"], process_exit_code=0)
    assert answer.get("error") == "FileNotFoundError", answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == "FAILED"
    assert run.data.tags["process_exit_code"] == "0"


@pytest.mark.parametrize("selection", ["unknown_run", "unsupported_store"])
def test_native_selection_error_keeps_run_context(
    case: TrackingCase, selection: str
) -> None:
    """AC-01/05: preserve native selection errors with the requested run/stage."""
    changes = (
        {"run_id": "0" * 32}
        if selection == "unknown_run"
        else {"tracking_uri": "unsupported-tracking://local"}
    )
    answer = case.invoke(**changes)
    # Direct native construction confirms this specific MlflowException subtype.
    native_error = (
        "MlflowException"
        if selection == "unknown_run"
        else "UnsupportedModelRegistryStoreURIException"
    )
    assert answer.get("error") == native_error, answer
    assert any(
        changes.get("run_id", case.run_id) in note and "stage=" in note
        for note in answer["notes"]
    )
    assert case.client.get_run(case.run_id).info.status == "RUNNING"


def test_preserves_native_scalar_and_stable_structured_parameters(
    case: TrackingCase,
) -> None:
    """AC-01: scalar values use native semantics and structures have stable JSON."""
    answer = case.invoke(
        parameters={
            "kernel": "linear",
            "enabled": True,
            "optional": None,
            "settings": {"z": 1, "a": 2},
        }
    )
    assert "error" not in answer, answer
    assert case.client.get_run(case.run_id).data.params == {
        "kernel": "linear",
        "enabled": "True",
        "optional": "None",
        "settings": '{"a":2,"z":1}',
    }


@pytest.mark.parametrize(
    ("outcome", "status"), [(False, "failed"), (None, "not_checked")]
)
def test_validation_outcome_is_separate_from_process_completion(
    case: TrackingCase, outcome: bool | None, status: str
) -> None:
    """AC-01/05: configured validation does not rewrite successful process exit."""
    answer = case.invoke(validation_passed=outcome)
    assert "error" not in answer, answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == "FINISHED"
    assert run.data.tags["process_exit_code"] == "0"
    assert run.data.tags["validation_status"] == status
    assert answer["result"]["validation_status"] == status


def test_explicit_client_ignores_another_active_run(
    case: TrackingCase, tmp_path: Path
) -> None:
    """AC-01/02: fluent active-run state cannot redirect the explicit client."""
    store = tmp_path / uuid.uuid4().hex
    store.mkdir()
    uri = f"sqlite:///{store}/other.db"
    client = MlflowClient(tracking_uri=uri)
    experiment = client.create_experiment(
        "other", artifact_location=(store / "artifacts").as_uri()
    )
    run_id = client.create_run(experiment).info.run_id
    client.log_param(run_id, "ambient_marker", "keep")
    answer = case.invoke(_ambient={"uri": uri, "run_id": run_id})
    assert "error" not in answer, answer
    assert case.client.get_run(case.run_id).info.status == "FINISHED"
    assert client.get_run(run_id).data.params == {"ambient_marker": "keep"}
    assert client.get_run(run_id).data.metrics == {}
    assert client.list_artifacts(run_id) == []


def test_reuses_identical_shared_provenance(case: TrackingCase, tmp_path: Path) -> None:
    """AC-02: shared references can be reused without rewriting their bytes."""
    source = tmp_path / "provenance.json"
    source.write_text(json.dumps(case.provenance, indent=4) + "\n")
    case.client.log_artifact(case.run_id, str(source))
    answer = case.invoke()
    assert "error" not in answer, answer
    downloaded = case.client.download_artifacts(case.run_id, "provenance.json")
    assert Path(downloaded).read_bytes() == source.read_bytes()


def test_artifact_storage_failure_retains_native_error_and_local_evidence(
    case: TrackingCase, tmp_path: Path
) -> None:
    """AC-05: unavailable artifacts do not erase original diagnostics or claim success."""
    blocked = tmp_path / "blocked"
    blocked.write_bytes(b"regular file")
    experiment = case.client.create_experiment(
        "blocked", artifact_location=blocked.as_uri()
    )
    case.run_id = case.client.create_run(experiment).info.run_id
    before = (case.root / "predictions.csv").read_bytes()
    answer = case.invoke()
    assert answer.get("error") == "NotADirectoryError", answer
    assert case.client.get_run(case.run_id).info.status == "FAILED"
    assert any(case.run_id in note for note in answer["notes"])
    assert any("Available local" in note for note in answer["notes"])
    assert (case.root / "predictions.csv").read_bytes() == before


def test_native_parameter_conflict_remains_visible(case: TrackingCase) -> None:
    """AC-01/05: preserve native immutable parameters and failure context."""
    case.client.log_param(case.run_id, "C", "99")
    answer = case.invoke()
    assert answer.get("error") == "MlflowException", answer
    run = case.client.get_run(case.run_id)
    assert run.info.status == "FAILED"
    assert run.data.params["C"] == "99"
    assert any(case.run_id in note for note in answer["notes"])


@pytest.mark.parametrize("mutation", ["archive", "payload"])
def test_checks_retained_wheel_and_installed_payload(
    case: TrackingCase, mutation: str
) -> None:
    """AC-03: metadata identity cannot hide missing archive or altered installed bytes."""
    from urllib.parse import unquote, urlsplit

    if mutation == "archive":
        path = Path(
            unquote(
                urlsplit(case.provenance["toolkit"]["installation"]["locator"]).path
            )
        )
    else:
        path = Path(
            command(
                case.root,
                str(case.root / ".venv/bin/python"),
                "-I",
                "-c",
                "from importlib.resources import files; print(files('agentic_ml').joinpath('templates/provisional.txt'))",
            )
        )
    before = path.read_bytes()
    try:
        if mutation == "archive":
            path.unlink()
        else:
            path.write_bytes(before + b"changed payload\n")
        answer = case.invoke()
        assert answer.get("error") == "ValueError", answer
        assert "toolkit" in answer["message"]
        assert case.client.get_run(case.run_id).info.status == "FAILED"
    finally:
        path.write_bytes(before)


def test_rejects_environment_version_outside_committed_lock(case: TrackingCase) -> None:
    """AC-03: truthful installed metadata cannot disguise an inconsistent lock."""
    from tracking_support import file_ref

    path = case.root / "uv.lock"
    original = path.read_text()
    version = case.provenance["environment"]["libraries"]["pandas"]
    changed = original.replace(
        f'name = "pandas"\nversion = "{version}"', 'name = "pandas"\nversion = "0.0.0"'
    )
    assert changed != original
    path.write_text(changed)
    command(case.root, "git", "add", "uv.lock")
    command(case.root, "git", "commit", "-m", "test: inconsistent environment lock")
    case.provenance["experiment"]["commit_sha"] = command(
        case.root, "git", "rev-parse", "HEAD"
    )
    case.provenance["environment"]["lockfile"] = file_ref(case.root, "uv.lock")
    answer = case.invoke()
    assert answer.get("error") == "ValueError", answer
    assert "environment" in answer["message"] and "pandas" in answer["message"]


def test_rejects_corrupt_shared_provenance_without_overwrite(
    case: TrackingCase, tmp_path: Path
) -> None:
    """AC-02/05: unreadable existing shared records are visible artifact conflicts."""
    source = tmp_path / "provenance.json"
    source.write_bytes(b"not valid JSON\n")
    case.client.log_artifact(case.run_id, str(source))
    answer = case.invoke()
    assert answer.get("error") == "FileExistsError", answer
    downloaded = case.client.download_artifacts(case.run_id, "provenance.json")
    assert Path(downloaded).read_bytes() == b"not valid JSON\n"
