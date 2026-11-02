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

The initialization driver first runs those unchanged normal-wheel checks, then uses the validated source distribution to create a temporary full-SHA Git fixture. It compares every package file in both wheels with that source and each installed pinned Git package. Separate fresh CLI and existing-package API projects exercise complete initialization and reruns, including real stores, inert notebooks, imports, lock/pin preservation, Git exclusions and absent authorization. Wheel installs retain wheel origin; pinned-project installs retain Git origin. No origin metadata is fabricated, and unpublished fixture commits are local evidence. Successful commands remove only owned environments and private caches after the last probe; source fixtures and project files remain. The reserved milestone acceptance test exercises the complete initialization contract; no additional CI service or editor is required.

Installed resources are read with `importlib.resources.files("agentic_ml")`:

| Resource | Exact UTF-8 content (followed by one newline) |
|---|---|
| `templates/provisional.txt` | `Provisional Milestone 0 template; experiment initialization is unavailable.` |
| `runtime_guidance/provisional.md` | `Provisional Milestone 0 runtime guidance; experiment execution is unavailable.` |

These provisional files remain packaging sentinels. US-02 IP2 adds separate `templates/initialization/` resources and versioned draft schemas; the installed probe verifies their inventory, schema properties and inert notebook content. Environment synchronization is implemented in IP3 and local storage initialization in IP4; runtime guidance selection/loading remains subsequent work. Development `AGENTS.md` files are not installed runtime resources.

All four standalone drivers (installation, distribution, initialization and
planning) print `WORKSPACE <absolute-path>` and `RECORDS <absolute-path>`.
Durable commands, cwd, stdout/stderr logs, artifact SHA-256 identities, installed
identity manifests and results live under the checkout's
`.dev-records/verification/`, including when launched from another cwd. Consult
`commands.json` for stage logs and `summary.json` for independent verification and
cleanup outcomes; unavailable identities are recorded explicitly. See the
[records policy](records.md) for lifetime retention and backup responsibilities.

Default successful completion removes registered environments and private installer
caches after every dependent probe finishes. Add `--keep-workspace` to any driver
to retain successful environments for inspection. Verification failure preserves
available environments and records. All drivers accept `--workspace`; installation,
distribution and initialization require a new path. Planning allocates a unique
child when given an existing directory, preserving caller files. These flags do
not change pytest retention policy.

When pytest launches a driver, its workspace is beneath the owning test or
active shared-fixture root. The successful outer test removes that whole tree
after its finalizers finish, including source/project files and environments
retained by a driver's `--keep-workspace`. Add pytest `--keep-test-workspaces`
for post-test inspection. Failed outer tests retain available trees for one
numbered invocation; shared paths wait for their last consumer. Standalone
commands retain their existing source/project preservation behavior. See
[pytest workspace ownership and retention](verification.md#pytest-workspace-ownership-and-retention)
for overrides, explicit bases, concurrent/nested runs and interruption limits.

Initialization and planning invoke distribution verification with an explicit
new child workspace and `--keep-workspace`. Child records link to parent records;
the parent reports both locations. The parent owns cleanup of the known child
environments/cache after its last consumer; it preserves extracted source,
rebuilt wheels, Git fixtures, project files and records. The child summary records
its retained outcome; the parent summary records eventual cleanup. No arbitrary
external path is adopted for deletion. Shared installer caches remain untouched.

A failed build/install/probe exits nonzero and identifies its stage and records.
A later failure cannot count as passing because the direct wheel passed. Failure
to persist records prevents cleanup. Cleanup failure exits nonzero while retaining
the original verification outcome; an already nonzero verification status takes
precedence. Diagnostics identify remaining workspace and records. No historical
workspace or evidence is deleted or migrated. Interruption may leave partial
workspaces and incomplete records; forced process termination cannot guarantee
finalization or capture of a running child's buffered output. Raw records remain
outside Git and require contributor backup.

The ordinary `uv run --locked pytest` suite builds a small real artifact fixture and checks success plus malformed wheels (missing template, altered guidance, wrong CLI version), missing/ambiguous artifacts and corrupted source archives. Source-checkout CLI regressions remain separate. Verification currently uses POSIX `bin/python` and `bin/agentic-ml` paths; Windows remains unverified. See [US-33 IP2 evidence](../verification/us-33-ip2.md) for actual local results; hosted Linux/Python 3.12 package results and failure diagnostics passed in the [IP3 report](../verification/us-33-ip3.md). A default-branch package run remains post-merge follow-up.
