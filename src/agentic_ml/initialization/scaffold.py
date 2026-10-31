"""Render inert project templates from installed package resources."""

import json
from importlib.resources import files

from .models import InitOptions


def render(options: InitOptions, package: str) -> dict[str, bytes]:
    """Render draft inputs without executing notebook code or reading data."""
    resources = files("agentic_ml").joinpath("templates/initialization")
    replacements = {"__EXPERIMENT__": options.experiment, "__PACKAGE__": package}
    contents: dict[str, bytes] = {}
    base = f"experiments/{options.experiment}"
    for source, destination in (
        ("project.yaml", "project.yaml"),
        ("experiment.md", f"{base}/experiment.md"),
        ("search-space.yaml", f"{base}/search-space.yaml"),
        ("experiment.yaml", f"{base}/experiment.yaml"),
        ("package.txt", f"src/{package}/__init__.py"),
    ):
        text = resources.joinpath(source).read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        contents[destination] = text.encode()
    for name in (
        "01_data_assessment",
        "02_features_and_baseline",
        "03_model_development",
        "04_results",
    ):
        notebook = resources.joinpath("notebook.json").read_text(encoding="utf-8")
        notebook = notebook.replace("__TITLE__", name.replace("_", " "))
        notebook = notebook.replace("__EXPERIMENT__", options.experiment)
        json.loads(notebook)
        contents[f"{base}/notebooks/{name}.ipynb"] = notebook.encode()
    return contents
