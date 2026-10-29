# US-31 Implementation Phase 1 verification

Date: 2026-10-29. Source issue: [US-31 / #1](https://github.com/jimthompson5802/agentic-ml/issues/1). Owning tasks: US-31-IP1-T1–T3 in the [approved plan](../plans/milestone-0-us-31.md). Developer authorization: “you can begin us-31 ip 1” in this conversation. Plan and public boundaries were approved before execution.

## Environment and scope

macOS 15.7.9 (24G830), Darwin 24.6.0 arm64; CPython 3.12.15; Git 2.54.0; uv 0.13.1 (Homebrew 2026-10-14 aarch64-apple-darwin). Development resolutions: pytest 9.2.0, Ruff 0.17.3, mypy 1.20.2. Initial `uv lock` resolved 13 packages; locked bootstrap synchronization installed 11 development packages. Metadata uses Hatchling >=1.27,<2, distribution agentic-ml 0.1.0 and Python >=3.12, with no runtime dependencies. Hatchling is not built or verified here; full build verification belongs to US-33.

Issue #1 was refreshed before implementation: complete body and successful paginated zero-comment response; repeated metadata retained zero comments and updated_at 2026-10-29T03:08:20Z. Its body assigns Milestone 0; no GitHub milestone object is set. Requirements still match the approved plan. Relevant contributor, delivery, ADR-007 and package-layout contracts were reviewed during planning and the contributor contract rechecked during execution.

This implementation phase adds configuration and documentation, not executable harness behavior. TDD red/green is therefore not applicable. The negative tool examples below verify enforcement through public tool commands, using approved test boundaries. No product source, CLI, tests, CI or resources have been added. Full source checks and fresh-clone macOS verification remain pending later implementation phases; tool-version checks are not product tests.

## Results and acceptance mapping

- **US-31-IP1-T1 / AC-02,08:** pyproject metadata parsed with Python tomllib; project name and Python requirement checked; uv lock consistency and locked bootstrap sync passed. Exact resolutions are committed in uv.lock. Python selection is configured; existing Git ignores are preserved and extended for generated `.agentic-ml/` state.
- **US-31-IP1-T2 / AC-04,08–10:** pytest discovery/strict configuration, Ruff naming/import/docstring/error checks and formatting, and strict mypy configured. Six independent invalid examples failed for the intended reasons: N802, I001/F401, D100/D103, BLE001, return-value type mismatch, and formatter differences. All six corrected examples passed lint, formatting and typing. No rule suppression or checker exclusion was introduced.
- **US-31-IP1-T3 / AC-01,02,04,06,09,10:** README links the contributor guide. Reviewed prerequisites, clone/bootstrap commands, future shared commands, platform and CI status, conventions-to-check mapping, credentials/local defaults, and exception policy. All current bootstrap commands were executed. Future commands are explicitly pending package implementation. These are criterion portions advanced, not full-story acceptance.

Lock SHA-256 before and after verification: `ab8b6c9de02061ea788fa13a2dba162bcb963fb211ca938af3408e01bb1f5d9d`. All 15 final command outcomes matched expectations. Temporary examples were created outside the checkout and removed after the checks. Raw results are locally available at `/tmp/us31-ip1-results.json`; the complete durable command/output evidence follows.

## Problems and corrective verification

1. Initial uv Python discovery could not write the sandbox-blocked user cache; repeated with approved external cache access and succeeded. This was an environment permission failure, not a product defect.
2. Initial `uv run --no-sync ruff format --check .` exited 1 for Python code-block formatting in `docs/specs/design/interfaces-and-configuration.md` (1 file needed formatting, 35 already formatted). Corrective attempt 1: ran `uv run --no-sync ruff format docs/specs/design/interfaces-and-configuration.md`; repeated the original check and it passed (36 files already formatted). Changes are whitespace/line wrapping only; no checks were excluded or weakened.
3. The durable verification script initially named a temporary file `typing.py`; mypy exited 2 because it shadowed the standard-library typing module, rather than the expected type error exit 1. Corrective attempt 1: renamed temporary files to `example_<case>.py` and reran the original verification suite. Mypy reported the intended return-value mismatch, and every final check passed. This was a verification-fixture correction; no harness requirement or tool rule changed.

No unresolved corrective failure remains. No source-rule suppressions or custom checker exclusions exist. Default tool/generated-file exclusions and Git ignore rationale are documented in the contributor guide.

## Reproduction of tool probes

From the bootstrapped environment, the following standalone diagnostic uses only Python's standard library and the installed tools. It is evidence, not a product test suite. It writes diagnostics to /tmp, uses temporary files and compares the lock hash before/after.

```python
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

root = Path.cwd()
report = {
    "lock_before": hashlib.sha256(Path("uv.lock").read_bytes()).hexdigest(),
    "results": [],
}


def run(args, expected):
    result = subprocess.run(args, capture_output=True, text=True)
    report["results"].append(
        {
            "command": " ".join(args),
            "expected_exit": expected,
            "exit": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    )
    Path("/tmp/us31-ip1-results.json").write_text(json.dumps(report, indent=2))
    assert result.returncode == expected, report["results"][-1]


with tempfile.TemporaryDirectory(prefix="us31-tools-") as directory:
    base = Path(directory)
    examples = {
        "naming": '"""Naming example."""\ndef BadName() -> int:\n    """Return a value."""\n    return 1\n',
        "imports": '"""Import example."""\nimport sys\nimport os\n',
        "docstrings": "def value() -> int:\n    return 1\n",
        "errors": '"""Error example."""\ndef value() -> int:\n    """Return an integer."""\n    try:\n        return int("1")\n    except Exception:\n        return 0\n',
        "typing": '"""Typing example."""\ndef value() -> int:\n    """Return an integer."""\n    return "wrong"\n',
        "formatting": '"""Formatting example."""\n\ndef value( )->int:\n    """Return an integer."""\n    return 1\n',
    }
    for name, content in examples.items():
        path = base / f"example_{name}.py"
        path.write_text(content)
        if name == "typing":
            command = [
                "mypy",
                "--config-file",
                str(root / "pyproject.toml"),
                "--strict",
            ]
        elif name == "formatting":
            command = [
                "ruff",
                "format",
                "--check",
                "--config",
                str(root / "pyproject.toml"),
            ]
        else:
            command = ["ruff", "check", "--config", str(root / "pyproject.toml")]
        run(["uv", "run", "--no-sync", *command, str(path)], 1)
    for path in base.glob("*.py"):
        path.write_text(
            '"""Corrected example."""\n\n\ndef value() -> int:\n    """Return an integer."""\n    return 1\n'
        )
    for command in [
        ["ruff", "check", "--config", str(root / "pyproject.toml")],
        ["ruff", "format", "--check", "--config", str(root / "pyproject.toml")],
        ["mypy", "--config-file", str(root / "pyproject.toml"), "--strict"],
    ]:
        run(["uv", "run", "--no-sync", *command, str(base)], 0)
for command in [
    ["uv", "lock", "--check"],
    ["uv", "sync", "--locked", "--group", "dev", "--no-install-project"],
    ["uv", "run", "--no-sync", "ruff", "check", "."],
    ["uv", "run", "--no-sync", "ruff", "format", "--check", "."],
    ["uv", "run", "--no-sync", "pytest", "--version"],
    ["uv", "run", "--no-sync", "mypy", "--version"],
]:
    run(command, 0)
report["lock_after"] = hashlib.sha256(Path("uv.lock").read_bytes()).hexdigest()
assert report["lock_before"] == report["lock_after"]
Path("/tmp/us31-ip1-results.json").write_text(json.dumps(report, indent=2))
print(
    f"{len(report['results'])} expected outcomes verified; lock unchanged: {report['lock_after']}"
)
```

## Complete final command results

### `uv run --no-sync ruff check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_naming.py`

Expected exit: 1; actual exit: 1.

```text
N802 Function name `BadName` should be lowercase
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_naming.py:2:5
  |
1 | """Naming example."""
2 | def BadName() -> int:
  |     ^^^^^^^
3 |     """Return a value."""
4 |     return 1
  |

Found 1 error.
```

### `uv run --no-sync ruff check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_imports.py`

Expected exit: 1; actual exit: 1.

```text
I001 [*] Import block is un-sorted or un-formatted
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_imports.py:2:1
  |
1 |   """Import example."""
2 | / import sys
3 | | import os
  | |_________^
help: Organize imports
  |
1 | """Import example."""
2 + import os
3 | import sys
  - import os
  |

F401 [*] `sys` imported but unused
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_imports.py:2:8
  |
1 | """Import example."""
2 | import sys
  |        ^^^
3 | import os
  |
help: Remove unused import: `sys`
  |
1 | """Import example."""
  - import sys
2 | import os
  |

F401 [*] `os` imported but unused
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_imports.py:3:8
  |
1 | """Import example."""
2 | import sys
3 | import os
  |        ^^
help: Remove unused import: `os`
  |
2 | import sys
  - import os
  |

Found 3 errors.
[*] 3 fixable with `--fix`.
```

### `uv run --no-sync ruff check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_docstrings.py`

Expected exit: 1; actual exit: 1.

```text
D100 Missing docstring in public module
--> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_docstrings.py:1:1

D103 Missing docstring in public function
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_docstrings.py:1:5
  |
1 | def value() -> int:
  |     ^^^^^
2 |     return 1
  |

Found 2 errors.
```

### `uv run --no-sync ruff check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_errors.py`

Expected exit: 1; actual exit: 1.

```text
BLE001 Do not catch blind exception: `Exception`
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_errors.py:6:12
  |
4 |     try:
5 |         return int("1")
6 |     except Exception:
  |            ^^^^^^^^^
7 |         return 0
  |

Found 1 error.
```

### `uv run --no-sync mypy --config-file /Users/jim/Desktop/genai/agentic-ml/pyproject.toml --strict /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_typing.py`

Expected exit: 1; actual exit: 1.

```text
/var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_typing.py:4: error: Incompatible return value type (got "str", expected "int")  [return-value]
Found 1 error in 1 file (checked 1 source file)
```

### `uv run --no-sync ruff format --check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_formatting.py`

Expected exit: 1; actual exit: 1.

```text
unformatted: File would be reformatted
 --> /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz/example_formatting.py:3:1
  |
2 |
  - def value( )->int:
3 +
4 + def value() -> int:
5 |     """Return an integer."""
  |

1 file would be reformatted
```

### `uv run --no-sync ruff check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz`

Expected exit: 0; actual exit: 0.

```text
All checks passed!
```

### `uv run --no-sync ruff format --check --config /Users/jim/Desktop/genai/agentic-ml/pyproject.toml /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz`

Expected exit: 0; actual exit: 0.

```text
6 files already formatted
```

### `uv run --no-sync mypy --config-file /Users/jim/Desktop/genai/agentic-ml/pyproject.toml --strict /var/folders/8_/h2tjc94d2y5fwx8dhbcrnbfc0000gn/T/us31-tools-cfubu0vz`

Expected exit: 0; actual exit: 0.

```text
Success: no issues found in 6 source files
```

### `uv lock --check`

Expected exit: 0; actual exit: 0.

```text
Resolved 13 packages in 4ms
```

### `uv sync --locked --group dev --no-install-project`

Expected exit: 0; actual exit: 0.

```text
Resolved 13 packages in 2ms
Checked 11 packages in 0.50ms
```

### `uv run --no-sync ruff check .`

Expected exit: 0; actual exit: 0.

```text
All checks passed!
```

### `uv run --no-sync ruff format --check .`

Expected exit: 0; actual exit: 0.

```text
36 files already formatted
```

### `uv run --no-sync pytest --version`

Expected exit: 0; actual exit: 0.

```text
pytest 9.2.0
```

### `uv run --no-sync mypy --version`

Expected exit: 0; actual exit: 0.

```text
mypy 1.20.2 (compiled: yes)
```

## Review and remaining limitations

`git diff --check` and local Markdown file-target validation passed. Python tomllib parsed the metadata and verified distribution identity/Python baseline. No application tests, source CLI checks, wheel builds, fresh-checkout setup, or CI jobs were run. Those capabilities do not exist in this implementation phase. Full US-31 acceptance remains pending IP2. Developer approval of the IP1 gate is pending; do not start US-33 IP1 until approved progression is authorized.
