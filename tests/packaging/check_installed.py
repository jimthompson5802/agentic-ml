"""Check public resources in an installed distribution using only the stdlib."""

import argparse
import json
import platform
import subprocess
import sys
from dataclasses import FrozenInstanceError
from importlib.metadata import distribution, distributions
from importlib.resources import files
from pathlib import Path

import agentic_ml


def check_initialization_resources() -> None:
    """Check independently specified template inventory and schema properties."""
    import jsonschema
    import yaml

    from agentic_ml.initialization import InitOptions, InitResult, initialize_project

    assert callable(initialize_project)
    for value in (InitOptions(Path.cwd()), InitResult(Path.cwd(), (), (), (), ())):
        try:
            attribute = "project_root"
            setattr(value, attribute, Path("/"))
        except FrozenInstanceError:
            pass
        else:
            raise AssertionError("initialization value must be immutable")
    resources = files("agentic_ml").joinpath("templates/initialization")
    expected = {
        "project.yaml",
        "experiment.md",
        "experiment.yaml",
        "search-space.yaml",
        "package.txt",
        "notebook.json",
        "ignore.txt",
        "schemas",
    }
    assert {p.name for p in resources.iterdir()} == expected, (
        "initialization resource missing"
    )
    for name in ("project", "experiment", "search-space", "state"):
        resource = resources.joinpath(f"schemas/{name}.json")
        assert resource.is_file(), "initialization resource missing"
        schema = json.loads(resource.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False
        assert schema["properties"]["schema_version"] == {"const": "0.1"}
    search = yaml.safe_load(resources.joinpath("search-space.yaml").read_bytes())
    assert search == {"schema_version": "0.1", "algorithms": {}}
    project = yaml.safe_load(resources.joinpath("project.yaml").read_bytes())
    assert project["setup"] == {
        "data_access": "unconfigured",
        "agent": "unconfigured",
        "approval_presentation": "unconfigured",
    }
    assert project["components"] == {} and project["guidance"] == {}
    notebook = json.loads(
        resources.joinpath("notebook.json").read_text(encoding="utf-8")
    )
    assert (notebook["nbformat"], notebook["nbformat_minor"]) == (4, 5)
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == [] and cell["execution_count"] is None
    assert (
        resources.joinpath("package.txt").read_text(encoding="utf-8")
        == '"""Project-owned experiment code."""\n'
    )


def check_planning_resources() -> None:
    """Verify independently specified public planning schema inventory."""
    import jsonschema

    from agentic_ml.planning import (
        ResolveRequest,
        inspect_plan,
        resolve_plan,
        verify_plan,
    )

    assert callable(resolve_plan) and callable(inspect_plan) and callable(verify_plan)
    assert ResolveRequest(Path.cwd(), Path("experiment.yaml")).experiment == Path(
        "experiment.yaml"
    )
    resources = files("agentic_ml").joinpath("schemas/planning/1.0")
    expected = {
        "brief.json",
        "search-space.json",
        "experiment.json",
        "plan.json",
        "manifest.json",
        "result.json",
    }
    assert (
        resources.is_dir() and {entry.name for entry in resources.iterdir()} == expected
    ), "planning resource missing"
    for name in sorted(expected):
        schema = json.loads(resources.joinpath(name).read_bytes())
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False
    experiment = json.loads(resources.joinpath("experiment.json").read_bytes())
    assert experiment["properties"]["schema_version"] == {"const": "1.0"}
    assert set(experiment["required"]) == {
        "schema_version",
        "id",
        "brief",
        "search_space",
        "notebooks",
        "working_directory",
        "data",
        "execution",
    }


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
    assert set(installed.requires or []) == {
        "jsonschema<5,>=4",
        "pyyaml<7,>=6",
        "tomlkit<1,>=0.13",
        "nbclient<1,>=0.10",
        "ipykernel<8,>=6",
        "nbformat<6,>=5",
        "dvc<4,>=3",
        "mlflow<4,>=3",
    }, "unexpected declared runtime dependencies"
    inventory = sorted((d.metadata["Name"], d.version) for d in distributions())
    expected_names = {
        "colorama",
        "pygments",
        "cloudpickle",
        "funcy",
        "flask",
        "voluptuous",
        "matplotlib",
        "dulwich",
        "alembic",
        "gto",
        "sqlparse",
        "vine",
        "google-auth",
        "amqp",
        "opentelemetry-proto",
        "diskcache",
        "contourpy",
        "click-plugins",
        "dvc-task",
        "ruamel.yaml",
        "packaging",
        "nbclient",
        "hydra-core",
        "shortuuid",
        "six",
        "jsonschema",
        "antlr4-python3-runtime",
        "jedi",
        "debugpy",
        "rpds-py",
        "celery",
        "annotated-types",
        "prettytable",
        "pyparsing",
        "python-dotenv",
        "configobj",
        "filelock",
        "pygit2",
        "gitdb",
        "tzlocal",
        "anyio",
        "aiohttp-retry",
        "markupsafe",
        "cycler",
        "pydantic-core",
        "asttokens",
        "fsspec",
        "itsdangerous",
        "fastjsonschema",
        "aiohttp",
        "networkx",
        "pillow",
        "flufl.lock",
        "numpy",
        "entrypoints",
        "tqdm",
        "smmap",
        "uvicorn",
        "skops",
        "pure-eval",
        "platformdirs",
        "aiosignal",
        "multidict",
        "scipy",
        "traitlets",
        "graphql-core",
        "scmrepo",
        "sqlalchemy",
        "stack-data",
        "typing-extensions",
        "tornado",
        "shtab",
        "dvc-studio-client",
        "pyasn1",
        "pyasn1-modules",
        "cachetools",
        "mlflow-tracing",
        "gunicorn",
        "tabulate",
        "dvc-data",
        "attrs",
        "opentelemetry-api",
        "markdown-it-py",
        "huey",
        "dpath",
        "annotated-doc",
        "dvc-http",
        "cffi",
        "flatten-dict",
        "threadpoolctl",
        "nbformat",
        "click-didyoumean",
        "pyarrow",
        "jupyter-core",
        "executing",
        "iterative-telemetry",
        "protobuf",
        "click",
        "graphql-relay",
        "mako",
        "mlflow-skinny",
        "matplotlib-inline",
        "atpublic",
        "fonttools",
        "typing-inspection",
        "propcache",
        "databricks-sdk",
        "pydot",
        "distro",
        "yarl",
        "ipython-pygments-lexers",
        "kombu",
        "parso",
        "tomlkit",
        "omegaconf",
        "gitpython",
        "billiard",
        "cryptography",
        "pexpect",
        "dvc",
        "prompt-toolkit",
        "frozenlist",
        "appdirs",
        "grandalf",
        "semver",
        "appnope",
        "nest-asyncio2",
        "fastapi",
        "kiwisolver",
        "ipython",
        "dvc-render",
        "click-repl",
        "dvc-objects",
        "werkzeug",
        "dictdiffer",
        "ipykernel",
        "zc.lockfile",
        "h11",
        "opentelemetry-semantic-conventions",
        "rich",
        "mlflow",
        "importlib-metadata",
        "aiohappyeyeballs",
        "python-dateutil",
        "docker",
        "blinker",
        "comm",
        "referencing",
        "requests",
        "mdurl",
        "pydantic-settings",
        "pyzmq",
        "agentic-ml",
        "jupyter-client",
        "setuptools",
        "narwhals",
        "scikit-learn",
        "jinja2",
        "opentelemetry-sdk",
        "starlette",
        "graphene",
        "tzdata",
        "zipp",
        "pygtrie",
        "asyncssh",
        "ptyprocess",
        "idna",
        "joblib",
        "charset-normalizer",
        "pydantic",
        "pandas",
        "sqltrie",
        "wcwidth",
        "pyyaml",
        "jsonschema-specifications",
        "flask-cors",
        "orjson",
        "urllib3",
        "psutil",
        "pycparser",
        "certifi",
    }
    expected_names = {name.replace(".", "-") for name in expected_names} | {"pathspec"}
    assert {
        name.lower().replace("_", "-").replace(".", "-") for name, _ in inventory
    } == (
        expected_names
        - ({"appnope", "pexpect", "ptyprocess"} if sys.platform == "win32" else set())
        - ({"appnope"} if sys.platform != "darwin" else set())
        | ({"pywin32", "waitress"} if sys.platform == "win32" else set())
    ), f"unexpected runtime dependency closure: {inventory}"
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
    check_initialization_resources()
    check_planning_resources()


if __name__ == "__main__":
    main()
