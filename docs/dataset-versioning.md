# Dataset versioning with native DVC

**Status: IP2 integration checks complete; Gate 2 approved, 2026-11-13.** The recipe
covers US-13 M1 AC-01/02 using the existing public APIs and native DVC.
Normal direct/rebuilt wheel verification remains IP3. See the
[plan](plans/milestone-1-us-13.md), [IP1 observations](verification/us-13-ip1.md)
and [IP2 evidence](verification/us-13-ip2.md).

## Ownership and identities

Use a separate experiment project with the toolkit installed as a normal locked
dependency through [experiment setup](experiment-setup.md). Native DVC owns
content; project Python owns extraction, partition persistence and derived data.
No new toolkit API or resource is proposed.

| Path | Owner |
|---|---|
| `versioning.json`, `version_data.py`, `pyproject.toml`, `uv.lock` | Git: runnable project code, effective settings, paths and environment |
| `data/source/` | DVC: copied local CSV/Parquet snapshots consumed by extraction |
| `data/extracted/A/`, `data/extracted/B/` | DVC: fresh extraction bundles, including the existing `extraction.json` manifest |
| `data/partitions/A/`, `data/partitions/B/` | DVC: each layout's partition files and its one authoritative `split.json` |
| `data/derived/A/`, `data/derived/B/` | DVC: deterministic project pandas output |
| `data/source.dvc`, `data/extracted.dvc`, `data/partitions.dvc`, `data/derived.dvc` | Git: native content references |
| `.dvc/config`, `.dvc/.gitignore`, `.dvcignore`, `data/.gitignore`, `.gitignore` | Git: nonsecret configuration and exclusions |
| `.dvc/cache/`, `.dvc/config.local`, local remote bytes | Excluded from Git |

Git-owned `versioning.json` is the relevant readable project manifest: it records
sources, paths and both layouts' exact configured memberships. DVC-owned split
records add actual consumed-frame identity and effective helper settings. There
is one authoritative *result* record per layout/version, with no second saved
copy in Git. The configuration is an input declaration, not a duplicate result.
Do not edit completed extraction reports to insert DVC hashes.

Extraction reports use byte SHA-256; partition records use version-bound native
Parquet SHA-256 for the consumed frame. DVC records its own file/directory hash
and algorithm in `.dvc` metadata. Preserve these distinct domains. Inspect native
directory member metadata/content rather than inventing another directory-hash
algorithm. Commit source/configuration and native pointers together.

## Runnable recipe

The following files are project code. Paths below are concrete examples to replace
with your absolute project/environment paths. Run commands from the explicit
project root. The integration test adapter substitutes temporary paths and extracts
these same file contents, without maintaining a separate test-only recipe.

Save this as `versioning.json`:

```json
{
  "sources": {"input": "data/source/input.csv"},
  "output_format": "parquet",
  "row_id": "id",
  "target": "label",
  "memberships": {
    "train_test": {"train": [0, 2, 4], "test": [1, 3]},
    "train_validation_test": {"train": [0, 2, 4], "validation": [1], "test": [3]}
  },
  "derived_ids": [0, 2, 4]
}
```

Save this as `version_data.py`:

```python
import argparse
import json
from pathlib import Path

from agentic_ml.extraction import extract_data
from agentic_ml.splitting import create_partitions


def extract(frames, settings):
    return frames["input"].loc[:, [settings["row_id"], settings["target"]]].copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--version", choices=["A", "B"], required=True)
    args = parser.parse_args()
    root = args.root
    if not root.is_absolute() or not root.is_dir():
        raise ValueError("root must be an absolute existing project directory")
    config = json.loads((root / "versioning.json").read_text(encoding="utf-8"))
    # Fresh version paths preserve extract_data's accepted publication contract.
    destinations = {
        name: root / "data" / name / args.version
        for name in ("extracted", "partitions", "derived")
    }
    if any(path.exists() for path in destinations.values()):
        raise FileExistsError("choose a fresh version; inspect existing output first")
    for path in destinations.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    frame, report = extract_data(
        extract,
        project_root=root,
        sources={name: Path(path) for name, path in config["sources"].items()},
        destination=destinations["extracted"],
        code_paths=[Path("version_data.py")],
        settings={"row_id": config["row_id"], "target": config["target"]},
        output_format=config["output_format"],
    )
    destinations["partitions"].mkdir()
    for layout, memberships in config["memberships"].items():
        parts, record = create_partitions(
            frame,
            row_id=config["row_id"],
            target=config["target"],
            layout=layout,
            memberships=memberships,
        )
        directory = destinations["partitions"] / layout
        directory.mkdir()
        for name, part in parts.items():
            part.to_parquet(directory / (name + ".parquet"), index=False)
        (directory / "split.json").write_text(
            json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
    destinations["derived"].mkdir()
    frame.set_index(config["row_id"], drop=False).loc[config["derived_ids"]].to_csv(
        destinations["derived"] / "selected.csv", index=False
    )
    print(json.dumps({"version": args.version, "output": report["output"]}))


if __name__ == "__main__":
    main()
```

This code uses the existing public signatures. Integration checks extract these
configuration/script blocks and execute the registration, transfer and project
invocation commands below, with temporary root/environment paths. IP3 separately
verifies normal wheel installation.

For a new disposable example project, after normal toolkit dependency setup:

```sh
cd /absolute/path/to/experiment
export DVC_NO_ANALYTICS=1
git init
/absolute/path/to/experiment/.venv/bin/dvc init
/absolute/path/to/experiment/.venv/bin/dvc remote add --default local /absolute/path/to/separate-local-storage
mkdir -p data/source
printf 'id,label\n0,A\n1,B\n2,C\n3,D\n4,E\n' > data/source/input.csv
/absolute/path/to/experiment/.venv/bin/python -I version_data.py --root /absolute/path/to/experiment --version A
/absolute/path/to/experiment/.venv/bin/dvc add data/source data/extracted data/partitions data/derived
/absolute/path/to/experiment/.venv/bin/dvc push
/absolute/path/to/experiment/.venv/bin/dvc status --cloud
git add version_data.py versioning.json pyproject.toml uv.lock .dvc/config .dvc/.gitignore .dvcignore data/.gitignore data/source.dvc data/extracted.dvc data/partitions.dvc data/derived.dvc
git commit -m 'data: record version A'
```

Use your configured Git identity. Existing initialized projects reuse their cache
and default remote: inspect `dvc config --list` and `dvc remote list` first; omit
initialization/remote-add commands and preserve existing configuration. If the
remote is inside the project, add its exact root-relative path to `.gitignore`
and commit that exclusion before transfer. Keep credentials in excluded local
configuration. Do not automatically replace a remote, untrack Git data or force
DVC initialization. For real local inputs, copy the reviewed CSV/Parquet into
`data/source/` before extraction (for example, `cp /absolute/input.csv
data/source/input.csv`); extraction reads that snapshot, leaving originals alone.
For Parquet use `data/source/input.parquet` and update the configuration source
path; input data must retain the same five literal rows for the fixture oracle.

Repeat registration without running Python to check unchanged pointers:

```sh
/absolute/path/to/experiment/.venv/bin/dvc add data/source data/extracted data/partitions data/derived
git diff --exit-code -- data/source.dvc data/extracted.dvc data/partitions.dvc data/derived.dvc
```

Create the second version by deliberately changing the owned source snapshot:

```sh
printf 'id,label\n0,Z\n1,B\n2,C\n3,D\n4,E\n' > data/source/input.csv
/absolute/path/to/experiment/.venv/bin/python -I version_data.py --root /absolute/path/to/experiment --version B
/absolute/path/to/experiment/.venv/bin/dvc add data/source data/extracted data/partitions data/derived
/absolute/path/to/experiment/.venv/bin/dvc push
/absolute/path/to/experiment/.venv/bin/dvc status --cloud
git add data/source.dvc data/extracted.dvc data/partitions.dvc data/derived.dvc data/.gitignore
git commit -m 'data: record version B'
git show HEAD~1:data/source.dvc
git show HEAD:data/source.dvc
git ls-files
git check-ignore data/source/input.csv .dvc/cache
```

These examples use an unshared disposable source snapshot. Inspect/review owned
files before replacing real project inputs. Native Git commits publish nothing
to a remote repository. Do not run garbage collection during the retention check.
The integration checks inspect both commits, each directory's member references,
and retained A/B bytes in both cache and local remote; `status --cloud` alone
does not prove retention of an earlier version. No checkout/pull is required for
M1 acceptance.

## Failure contract and handoff

Run each command separately and inspect its exit status/stdout/stderr. A nonzero
`dvc add` is failed registration; a later nonzero `push` is failed transfer and
does not undo local versioning. Resolve storage access, then retry `push`.
Do not claim remote availability after a failed push. Native diagnostics govern
missing inputs, Git-tracked data and conflicting output ownership. Inspect the
existing pointer/stage instead of introducing another owner. Re-adding a member
of a DVC directory may update its existing owner rather than create a conflict.
Project/native errors stay visible; this recipe adds no transactional rollback
across extraction, partition writes, DVC and Git. Inspect partial project output
before retrying a fresh version; never silently delete it.

US-39 can reuse this recipe, configuration, source snapshots, extraction bundle,
split records, derived files and Git/native DVC references. US-26 adds MLflow
links; US-27 adds stages. US-13 M2 AC-03/04 owns restore/hash checks and
missing/corrupt restoration failures. This guide claims no stage execution,
training, final-test selection or automatic reproduction.
