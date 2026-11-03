"""Validate isolated runtime inventories against installed dependency metadata."""

from importlib.metadata import Distribution, distributions
from typing import NotRequired, TypedDict

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


class LockDependency(TypedDict):
    """Dependency reference in a uv universal lockfile."""

    name: str
    version: NotRequired[str]
    source: NotRequired[dict[str, str]]
    extra: NotRequired[list[str]]


class LockPackage(TypedDict):
    """Package fields used to check a uv universal dependency graph."""

    name: str
    version: NotRequired[str]
    source: NotRequired[dict[str, str]]
    dependencies: NotRequired[list[LockDependency]]
    optional_dependencies: NotRequired[dict[str, list[LockDependency]]]


def check_installed_dependencies() -> set[str]:
    """Reject missing, incompatible, unrelated, or contributor distributions.

    Follow active Requires-Dist edges from agentic-ml, including requested
    extras, using this interpreter's platform and Python version markers.
    """
    installed: dict[str, Distribution] = {
        canonicalize_name(item.metadata["Name"]): item for item in distributions()
    }
    required: set[str] = set()
    expanded: set[tuple[str, frozenset[str]]] = set()
    extras: dict[str, set[str]] = {}
    pending = [("agentic-ml", set[str]())]
    missing: set[str] = set()
    incompatible: set[str] = set()
    while pending:
        name, requested = pending.pop()
        required.add(name)
        active = extras.setdefault(name, set())
        active.update(requested)
        state = (name, frozenset(active))
        if state in expanded:
            continue
        expanded.add(state)
        package = installed.get(name)
        if package is None:
            missing.add(name)
            continue
        for text in package.requires or []:
            requirement = Requirement(text)
            if requirement.marker is not None and not any(
                requirement.marker.evaluate({"extra": extra}) for extra in active | {""}
            ):
                continue
            dependency = canonicalize_name(requirement.name)
            candidate = installed.get(dependency)
            if candidate is None:
                missing.add(f"{name} requires {requirement}")
            elif not requirement.specifier.contains(
                candidate.version, prereleases=True
            ):
                incompatible.add(
                    f"{name} requires {requirement}; installed {candidate.version}"
                )
            pending.append(
                (dependency, {canonicalize_name(extra) for extra in requirement.extras})
            )
    unexpected = set(installed) - required
    forbidden = {
        name
        for name in installed
        if name in {"pytest", "pytest-xdist", "mypy", "ruff"}
        or name.startswith("types-")
    }
    assert not (missing or incompatible or unexpected or forbidden), (
        "invalid runtime dependencies: "
        f"missing={sorted(missing)}; incompatible={sorted(incompatible)}; "
        f"unexpected={sorted(unexpected)}; development={sorted(forbidden)}"
    )
    return required


def check_locked_dependencies(
    packages: list[LockPackage], project_name: str, required: set[str]
) -> None:
    """Check universal lock reachability and active installed version agreement.

    Universal locks can contain dependencies for other platforms. Follow every
    locked marker branch, but only optional dependencies requested by an edge.
    Installed metadata separately establishes the active platform's closure.
    """
    by_name: dict[str, list[int]] = {}
    for index, package in enumerate(packages):
        by_name.setdefault(canonicalize_name(package["name"]), []).append(index)
    roots = by_name.get(canonicalize_name(project_name), [])
    assert len(roots) == 1, "expected one locked experiment project"
    project_dependencies = {
        canonicalize_name(edge["name"])
        for edge in packages[roots[0]].get("dependencies", [])
    }
    assert project_dependencies == {"agentic-ml"}, (
        "invalid locked dependencies: "
        f"missing={sorted({'agentic-ml'} - project_dependencies)}; "
        f"unexpected={sorted(project_dependencies - {'agentic-ml'})}"
    )
    pending = [(roots[0], set[str]())]
    reached: set[int] = set()
    expanded: set[tuple[int, frozenset[str]]] = set()
    extras: dict[int, set[str]] = {}
    missing: set[str] = set()
    while pending:
        index, requested = pending.pop()
        reached.add(index)
        active = extras.setdefault(index, set())
        active.update(requested)
        state = (index, frozenset(active))
        if state in expanded:
            continue
        expanded.add(state)
        package = packages[index]
        dependencies = list(package.get("dependencies", []))
        # uv spells this table with a hyphen; the caller normalizes its key.
        for extra, optional in package.get("optional_dependencies", {}).items():
            if canonicalize_name(extra) in active:
                dependencies.extend(optional)
        for dependency in dependencies:
            candidates = [
                candidate
                for candidate in by_name.get(canonicalize_name(dependency["name"]), [])
                if (
                    "version" not in dependency
                    or packages[candidate].get("version") == dependency["version"]
                )
                and (
                    "source" not in dependency
                    or packages[candidate].get("source") == dependency["source"]
                )
            ]
            if not candidates:
                missing.add(f"{package['name']} requires {dependency['name']}")
            for candidate in candidates:
                pending.append(
                    (
                        candidate,
                        {canonicalize_name(e) for e in dependency.get("extra", [])},
                    )
                )
    unexpected = sorted(
        packages[i]["name"] for i in set(range(len(packages))) - reached
    )
    installed: dict[str, str] = {
        canonicalize_name(item.metadata["Name"]): item.version
        for item in distributions()
    }
    incompatible = sorted(
        f"{name}=={installed[name]}"
        for name in required
        if not any(
            canonicalize_name(packages[i]["name"]) == name
            and packages[i].get("version") == installed[name]
            for i in reached
        )
    )
    assert not (missing or unexpected or incompatible), (
        "invalid locked dependencies: "
        f"missing={sorted(missing)}; incompatible={incompatible}; unexpected={unexpected}"
    )
