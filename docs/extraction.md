# Pandas extraction and feature data

**Status:** IP1 contract/test boundaries approved 2026-11-07 UTC under
US-11-SC-01. IP2 component implementation and its M1/shared checks passed;
developer IP2 gate approved 2026-11-07 UTC. IP3 remains explicitly unstarted. Separate installed-project delivery is owned by IP3. The
[owning plan](plans/milestone-1-us-11.md) governs execution and
[issue #14](https://github.com/jimthompson5802/agentic-ml/issues/14) governs outcomes.

## Use pandas directly

Pandas DataFrame is the data representation for extraction and the foundation
for feature engineering. Projects use native pandas readers, column indexing,
boolean masks, merge/join, assign, groupby and other DataFrame operations.
Project-owned functions contain the actual extraction and feature logic.

The proposed toolkit request/result records, source/column classes, predicate and
join classes, callback context, operation union and custom extraction exception
are withdrawn. There is no toolkit query language, custom dataframe wrapper,
restricted predicate catalogue or alternative set of join semantics.

| Work | Interface |
|---|---|
| Read CSV/Parquet | `pd.read_csv`, `pd.read_parquet` with native reader options |
| Inspect schema/metadata | `frame.dtypes`, `frame.shape`, `frame.info`, `frame.describe` as appropriate |
| Select/filter/join | Native column indexing, `.loc`, boolean masks, `.merge` / `.join` |
| Engineer features | Ordinary functions accepting/returning DataFrames, native pandas operations |
| Fit learned preprocessing | Native scikit-learn pipelines/transformers operating on the pandas data boundary; fit training rows only |
| Record toolkit provenance and publish completed output | One small proposed `extract_data` function using native objects and ordinary dictionaries |

The toolkit still owns US-11 metadata, source/output identity, timing, and honest
publication/failure handling. It does not reimplement pandas. Quality rules,
splits, fitted-state handling and feature comparisons retain their owning stories.

## Proposed toolkit integration function

Public import: `from agentic_ml.extraction import extract_data`.
This is the only new extraction export proposed by this revision.

```python
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Literal

import pandas as pd


def extract_data(
    extract: Callable[[dict[str, pd.DataFrame], dict[str, object]], pd.DataFrame],
    *,
    project_root: Path,
    sources: Mapping[str, Path],
    destination: Path,
    code_paths: Sequence[Path],
    settings: Mapping[str, object] | None = None,
    read_options: Mapping[str, Mapping[str, object]] | None = None,
    output_format: Literal["csv", "parquet"] = "parquet",
) -> tuple[pd.DataFrame, dict[str, object]]: ...
```

The callback receives ordinary named DataFrames and a copied settings dictionary,
then returns an ordinary DataFrame. It can call other project functions and use
all appropriate pandas operations. Its signature is a simple integration
convention, not a registration protocol or toolkit class hierarchy. Projects can
also use their pandas functions directly without this recording helper.

The return is `(frame, report)`: the actual extracted DataFrame and a plain
JSON-compatible dictionary. Frame retains its pandas index/dtypes in memory;
serialized output excludes the index. Report identifies actual serialized schema
separately because CSV may lose types. No custom SourceRequest, ExtractionResult,
ColumnSchema, ExtractionContext, typed dictionary class, or exception subclass is
required. Internal helpers use normal functions and standard-library values.

`settings` captures explicit project extraction choices, such as selected columns,
filter thresholds and merge keys/mode/cardinality. The callback consumes these
values directly. The helper records them without interpreting a second operation
language or pretending to prove arbitrary project code obeyed every setting.
`read_options` contains native pandas keyword arguments per named source, not
renamed toolkit options. Both dictionaries must have JSON-compatible values
(null, booleans, strings, integers, finite floats, lists and string-keyed maps)
so settings can be recorded literally. Use string dtype names for native dtype
options. Advanced callable converters can live in project code with declared code
references; the helper does not serialize Python callables as configuration.

Require at least one uniquely named source and at least one declared project
code path for traceable project extraction. These declarations identify recorded
inputs/code, not every hidden dependency. The callback can be any synchronous
callable with the documented signature; do not reject a function simply because
it is local, wrapped or otherwise unregistered. Record module/name when available,
and always record declared code bytes/paths. No complete imported-code capture
or arbitrary-Python isolation is promised.

## Native reading, schema and operation semantics

Source paths ending `.csv` use `pd.read_csv`; `.parquet` use `pd.read_parquet`.
Other suffixes are unsupported by this local convenience helper; ordinary
project pandas code is not a toolkit connector guarantee. Use pyarrow as the
Parquet engine. Forward native `read_options` after adding documented reader
defaults: CSV `encoding="utf-8"`, `sep=","`, `header="infer"`, `index_col=None`,
`on_bad_lines="error"`, `dtype_backend="numpy_nullable"`; Parquet
`engine="pyarrow"`, `dtype_backend="numpy_nullable"`. Suppress the default sep
when the native delimiter alias is supplied. Reject a conflicting Parquet engine.
Record the actual passed options including defaults and any explicit overrides.
Reader options must produce a DataFrame, not an iterator/chunk stream.

Read owned source bytes, hash those bytes and pass a BytesIO to the chosen native
reader. This ties reported content identity to parsed bytes while preserving
pandas semantics. Record each loaded frame's ordered column names, dtype strings
and row count before the project function runs; pass the callback independent
copies in a plain dictionary. Source schema is pandas' parsed/inferred schema,
not a data-quality certificate. Header-only data is supported when pandas can
read it. Reject non-DataFrame reader/callback results and frames with non-string
or duplicate column names needed for unambiguous output reporting. Other dtype
and serialization compatibility follows pandas/pyarrow; do not build a separate
allowed-type registry.

Native pandas defines missing values, comparison/filter behavior, join key
matching, suffixes, cardinality validation, type coercion and row order. Projects
make needed behavior explicit with native `dtype`, `validate`, `sort`,
`sort_values`, `fillna` and similar options. No toolkit `full` join alias: pandas
uses `how="outer"`. There is no toolkit override for null inequality or row-order
reconstruction. Acceptance fixtures explicitly select their dtypes/options and
expected rows instead of depending on unspecified order.

Primary references: [pandas CSV reader](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html),
[pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).

## Paths, identity and report

An explicit absolute existing `project_root` resolves relative source, code and
destination paths. Record the actual caller cwd and leave it unchanged. Absolute
local source files outside the project are allowed; output/code paths remain
inside the project. Reject source/code symlinks, symlink ancestors, traversal in
relative paths, nonregular inputs and output/input overlaps. Existing strict APIs
keep their existing path rules. Recheck declared source/code identity around
reading and before publication; detectable mutation fails. This is trusted local
path/integrity checking, not OS isolation or crash recovery.

Report is a plain UTF-8 JSON dictionary stored as `destination/extraction.json`.
Required keys and meanings:

| Key | Recorded value |
|---|---|
| `schema_version`, `status` | `"1.0"`, `"complete"` for completed extraction only |
| `project_root`, `working_directory` | Absolute strings |
| `started_at`, `completed_at`, `elapsed_seconds` | UTC RFC3339 strings ending Z; nonnegative monotonic duration through preparation for publication |
| `sources` | Ordered list of name, supplied/resolved path, format, byte count, SHA-256, actual native reader options, row count and schema list of name/dtype dictionaries |
| `extraction` | Callable module/name where available, declared code path/hash list, deeply copied settings |
| `output` | Filename, format, byte count/hash, row count, in-memory schema, serialized schema and actual pandas writer options |
| `versions` | Installed toolkit, pandas and pyarrow versions |

Paths are strings; schemas are lists of ordinary dictionaries. Checksums use
`sha256:` plus 64 lowercase hexadecimal digits. The helper does not add a report
class or give the dictionary a general workflow-state lifecycle. Time capture
excludes the final publication syscall. No report self-hash, fabricated DVC ID or
claim of quality-approved data. US-13 supplies real DVC links later and US-26 owns
MLflow results. Committed project code/configuration and explicit settings provide
reproduction context; hidden callback reads/imports remain unrecorded unless
explicitly declared by the scientist.

## Publication and failure handling

Preserve the fresh-bundle rule: nonexistent destination, existing writable parent,
owned sibling staging directory, pandas output writing, independent re-read/hash,
report serialization, then same-filesystem directory rename. Preflight paths and
recordable settings before loading data or invoking the callback. No existing
file/directory is overwritten. Return only after output and report are complete.

Write `dataset.csv` using DataFrame.to_csv (UTF-8, comma, header, LF, index=False),
or `dataset.parquet` using DataFrame.to_parquet (pyarrow, Snappy, index=False).
Re-read serialized output through pandas; validate column names/order and row
count and record actual dtypes. Source/callback failures and failed writes publish
no new completed destination; remove only owned staging files when possible.

Use standard exceptions: ValueError for invalid request/settings and incompatible
returned values; TypeError for a noncallable extractor or non-DataFrame result;
FileNotFoundError/FileExistsError for missing inputs/output conflicts; OSError
for filesystem failures. Preserve native pandas/parser/merge and project callback
exceptions and their original types; attach contextual notes using add_note with
source name, operation or stage, root/cwd and available staging location. No broad
conversion into a proprietary exception. Cleanup errors add a note to the primary
exception rather than replacing it. KeyboardInterrupt/SystemExit are not wrapped.
If a narrow catch at the callable boundary needs a Ruff exception, justify and
register it during implementation; no suppression is added in this design phase.

Ordinary reruns use a new destination or explicit project output management.
Future DVC stages declare the entire non-persistent output bundle; DVC's normal
output removal makes that directory fresh before rerun. Native DVC stage/replay
verification remains US-27/40, not an extraction claim. Concurrent same-destination
writers, forced-kill cleanup and arbitrary callback side effects remain outside
the supported guarantee. [DVC repro](https://doc.dvc.org/command-reference/repro).

## Example using pandas

Usage for the IP2 API; both isolated installed-wheel demonstrations remain IP3:

```python
from pathlib import Path
import pandas as pd
from agentic_ml.extraction import extract_data


def extract_people(
    frames: dict[str, pd.DataFrame], settings: dict[str, object]
) -> pd.DataFrame:
    minimum_age = settings["minimum_age"]
    assert isinstance(minimum_age, int)
    columns = settings["columns"]
    assert isinstance(columns, list) and all(isinstance(c, str) for c in columns)
    join_key = settings["join_key"]
    assert isinstance(join_key, str)
    assert settings["join_how"] == "left"
    assert settings["join_validate"] == "many_to_one"
    people = frames["people"]
    selected = people.loc[people["age"].ge(minimum_age)]
    joined = selected.merge(
        frames["groups"], on=join_key, how="left", validate="many_to_one"
    )
    return joined.loc[:, columns].sort_values("id").reset_index(drop=True)


frame, report = extract_data(
    extract_people,
    project_root=Path("/absolute/path/to/experiment"),
    sources={"people": Path("data/people.csv"), "groups": Path("data/groups.parquet")},
    destination=Path("outputs/extracted-v1"),
    settings={
        "minimum_age": 30,
        "columns": ["id", "label"],
        "join_key": "group",
        "join_how": "left",
        "join_validate": "many_to_one",
    },
    code_paths=[Path("src/project_experiments/extraction.py")],
)
```

The project function resides at the declared code path; `outputs` exists and
`extracted-v1` does not. It returns the plan fixture's literal rows `(2,beta)` and
`(3,alpha)`. A production project may validate settings with its preferred native
Python conventions. Source schema is also inspectable directly with pandas:

```python
people = pd.read_csv(root / "data/people.csv", dtype_backend="numpy_nullable")
print(people.dtypes)
print(people.shape)
people.info()
```

Here `root` is the project's explicit Path. Inspection needs no toolkit source
class or separate schema inspection API.

## Basis for feature engineering

Downstream feature functions accept/return DataFrames and preserve row identity
and target alignment. Stateless authored features can use pandas assign,
column arithmetic, strings/datetimes, merges and aggregation with explicit
settings. The extraction-to-feature handoff is the returned DataFrame or the
pandas-readable persisted dataset, with its source/output identity alongside it.

Pandas remains the tabular foundation. Learned imputation, encoding, scaling and
other fitted transformations still use training-only fitted state and reuse it
unchanged for validation/test/inference through native scikit-learn Pipeline,
ColumnTransformer or compatible project transformers. A stateless pandas function
can integrate using FunctionTransformer. Fitting a transform on the full extracted
frame before splitting remains invalid. No new toolkit feature/model wrapper is
introduced. [FunctionTransformer reference](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html).

This establishes the data boundary for future US-12/14/15/16 plans; it does not
implement or accept their quality, split, pipeline or persistence behavior.

## Dependencies and gate

Keep proposed direct runtime requirements pandas>=3.1,<3.2 and pyarrow>=25,<26,
starting from existing locked 3.1.0 / 25.0.1. Dev-only pandas-stubs>=3,<4 must be
resolved compatibly and checked with strict mypy during IP2. IP2 has resolved pandas-stubs 3.1.0.261029 and added these declared requirements;
see its verification report for actual platform/check results. Update both
independent runtime inventory probes with intentional dependency changes.

IP1 approval confirms this single-function/native-object contract and
[public test matrix](verification/us-11-ip1.md#public-test-boundaries-and-case-matrix).
All five US-11 criteria, M1 phase tests, M1–6 story checks, both installed wheel
paths and existing developer gates are retained. Whole-story acceptance and installed extraction evidence remain pending IP3.
