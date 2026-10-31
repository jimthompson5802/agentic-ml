"""Probe a pinned installation using only installed public interfaces and stdlib."""

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tomllib
from importlib.metadata import distribution, distributions
from importlib.resources import files
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


def main() -> None:
    """Check project and installed identities, printing reviewable JSON evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--checkout", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    checkout = args.checkout.resolve()
    environment = project / ".venv"
    assert Path(sys.prefix).resolve() == environment, "wrong interpreter environment"
    assert not project.is_relative_to(checkout), "project inside harness checkout"
    assert all(not Path(p).resolve().is_relative_to(checkout) for p in sys.path), (
        "harness checkout on import path"
    )
    installed = distribution("agentic-ml")
    import agentic_ml

    assert agentic_ml.__file__ is not None
    package_path = Path(agentic_ml.__file__).resolve()
    assert package_path.is_relative_to(environment), "import outside environment"
    direct_url_text = installed.read_text("direct_url.json")
    assert direct_url_text is not None, "missing direct_url.json"
    direct_url = json.loads(direct_url_text)
    assert not direct_url.get("dir_info", {}).get("editable"), "editable installation"
    lock_bytes = (project / "uv.lock").read_bytes()
    lock = tomllib.loads(lock_bytes.decode())
    declaration = tomllib.loads((project / "pyproject.toml").read_text())
    assert declaration["project"]["dependencies"] == ["agentic-ml"], (
        "declared dependency mismatch"
    )
    source = declaration["tool"]["uv"]["sources"]["agentic-ml"]
    harness = [p for p in lock["package"] if p["name"] == "agentic-ml"]
    assert len(harness) == 1, "expected one locked harness"
    locked_url = urlsplit(harness[0]["source"]["git"])
    assert source["git"] == args.repository, "declared repository mismatch"
    assert direct_url["url"] == args.repository, "installed repository mismatch"
    assert locked_url._replace(query="", fragment="").geturl() == args.repository, (
        "locked repository mismatch"
    )
    assert source["rev"] == args.revision, "declared revision mismatch"
    assert locked_url.fragment == args.revision, "locked revision mismatch"
    assert parse_qs(locked_url.query).get("rev") == [args.revision], (
        "locked requested revision mismatch"
    )
    assert direct_url["vcs_info"]["commit_id"] == args.revision, (
        "installed revision mismatch"
    )
    assert direct_url["vcs_info"]["requested_revision"] == args.revision, (
        "installed requested revision mismatch"
    )
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
    ), f"unexpected installed dependency closure: {inventory}"
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
    assert expected_names <= {p["name"] for p in lock["package"]}, (
        "missing locked runtime dependency"
    )
    assert {p["name"] for p in lock["package"]} <= expected_names | {
        declaration["project"]["name"],
        "pywin32",
        "waitress",
        "tzdata",
    }, "unexpected locked dependency closure"
    assert harness[0]["version"] == installed.version, "locked version mismatch"
    result = subprocess.run(
        [str(environment / "bin/agentic-ml"), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"CLI exit {result.returncode}: {result.stderr}"
    assert result.stdout == installed.version + "\n", "CLI version mismatch"
    assert result.stderr == "", "unexpected CLI stderr"
    template = files("agentic_ml").joinpath("templates/provisional.txt")
    assert template.is_file(), "template resource missing"
    assert template.read_text(encoding="utf-8") == (
        "Provisional Milestone 0 template; experiment initialization is unavailable.\n"
    ), "template contents differ"
    guidance = files("agentic_ml").joinpath("runtime_guidance/provisional.md")
    assert guidance.read_text(encoding="utf-8") == (
        "Provisional Milestone 0 runtime guidance; experiment execution is unavailable.\n"
    ), "runtime guidance contents differ"
    print(
        json.dumps(
            {
                "repository": direct_url["url"],
                "requested_revision": source["rev"],
                "resolved_revision": direct_url["vcs_info"]["commit_id"],
                "locked_revision": locked_url.fragment,
                "lock_request": parse_qs(locked_url.query).get("rev"),
                "package_version": installed.version,
                "lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
                "python_implementation": platform.python_implementation(),
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "package_path": str(package_path),
                "sys_path": sys.path,
                "distributions": inventory,
                "cli_stdout": result.stdout,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
