# Distribution verification

## Distribution builds and installed verification

From the repository root, build into a fresh output directory and verify both paths:

```sh
uv build --out-dir dist
uv run --locked python tests/packaging/verify_distributions.py --artifacts-dir dist
uv run --locked python tests/installation/verify_initialization.py --artifacts-dir dist
```

Use an empty output directory for each reviewed build. If `dist` already contains artifacts from an earlier version, use a new directory in both commands. The driver requires exactly one wheel and one `.tar.gz` source distribution and rejects missing or ambiguous candidates. These same commands are configured in hosted CI. Both hosted wheel paths and separate build/resource failure-and-correction cases passed verification; see the [IP3 report](../verification/us-33-ip3.md).

The driver creates a unique temporary workspace outside the checkout and prints its path. For each wheel it creates an unseeded Python 3.12 environment with `uv venv --no-project --python 3.12`, installs the wheel normally with `uv pip install --python ENV/bin/python WHEEL`, and probes it from a separate minimal experiment project. The probe uses isolated Python (`-I`) and an absolute installed `agentic-ml --version` entrypoint. It verifies CLI exit/stdout/stderr, wheel and installed version agreement, public imports, import/metadata paths, absence of editable installation and contributor dependencies, and independently specified resource contents. The Python 3.12 runtime closure is explicitly checked against the reviewed inventory in each standalone probe, including notebook, DVC and MLflow dependencies. Distribution-name normalization includes dots, underscores and hyphens. Platform-specific dependencies have explicit conditions; only observed platforms count as verified. Contributor tools and type stubs must remain absent. Future runtime dependency changes require reviewing this verification contract.

The second path validates source archive members, rejects links and traversal, and extracts with Python's `data` filter. It runs `uv build EXTRACTED_SOURCE --wheel --out-dir REBUILT_DIRECTORY` with build isolation, then installs that new wheel into another fresh environment. It never substitutes the direct wheel for the rebuilt wheel. Build dependencies remain separate from both runtime environments. Python path/home and active environment overrides are removed from child commands.

The initialization driver first runs those unchanged normal-wheel checks, then uses the validated source distribution to create a temporary full-SHA Git fixture. It compares every package file in both wheels with that source and each installed pinned Git package. Separate fresh CLI and existing-package API projects exercise complete initialization and reruns, including real stores, inert notebooks, imports, lock/pin preservation, Git exclusions and absent authorization. Wheel installs retain wheel origin; pinned-project installs retain Git origin. No origin metadata is fabricated, and unpublished fixture commits are local evidence. All workspaces and logs are retained outside the checkout. The ordinary pytest suite includes this driver; no additional CI service or editor is required.

Installed resources are read with `importlib.resources.files("agentic_ml")`:

| Resource | Exact UTF-8 content (followed by one newline) |
|---|---|
| `templates/provisional.txt` | `Provisional Milestone 0 template; experiment initialization is unavailable.` |
| `runtime_guidance/provisional.md` | `Provisional Milestone 0 runtime guidance; experiment execution is unavailable.` |

These provisional files remain packaging sentinels. US-02 IP2 adds separate `templates/initialization/` resources and versioned draft schemas; the installed probe verifies their inventory, schema properties and inert notebook content. Environment synchronization is implemented in IP3 and local storage initialization in IP4; runtime guidance selection/loading remains subsequent work. Development `AGENTS.md` files are not installed runtime resources.

Diagnostics include artifact paths/SHA-256, stage commands and working directories, interpreter/platform/import paths, installed distributions and CLI output. Every subprocess also writes stdout/stderr to a named stage `.log` in its working directory beneath the printed workspace. Workspaces are retained on success and failure for inspection; remove them manually when no longer needed. A failed installation/build/probe exits nonzero and identifies its stage and artifact. A failed later path never counts as passing because the direct wheel passed. Raw logs remain outside Git.

The ordinary `uv run --locked pytest` suite builds a small real artifact fixture and checks success plus malformed wheels (missing template, altered guidance, wrong CLI version), missing/ambiguous artifacts and corrupted source archives. Source-checkout CLI regressions remain separate. Verification currently uses POSIX `bin/python` and `bin/agentic-ml` paths; Windows remains unverified. See [US-33 IP2 evidence](../verification/us-33-ip2.md) for actual local results; hosted Linux/Python 3.12 package results and failure diagnostics passed in the [IP3 report](../verification/us-33-ip3.md). A default-branch package run remains post-merge follow-up.
