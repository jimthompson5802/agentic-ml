# Training-only preprocessing contract

Status: proposed US-15 M1 contract for Gate 1 review. The helper below is not
implemented. See the [owning plan](plans/milestone-1-us-15.md) and
[native feasibility evidence](verification/us-15-ip1.md).

## Public interface

```python
from agentic_ml.preprocessing import fit_preprocessing

fitted_pipeline, record = fit_preprocessing(
    frame,
    partition_record=partition_record,
    pipeline=pipeline,
    selected_columns=["x"],
    output_schema=[{"name": "x", "dtype": "float64"}],
    fit_partition="train",
)
```

`frame` is a native pandas DataFrame; `pipeline` is a native sklearn Pipeline.
The result is `(Pipeline, dict[str, object])`. Selected columns are ordered,
unique nonempty feature names excluding the row-ID and target columns.
The existing [partition record](data-assessment-and-splits.md) supplies row ID,
target, layout, source identity and memberships. Project code owns JSON loading.
No project root or filesystem persistence is needed for this in-memory helper.

Use `create_partitions` supplied mode to validate/reconstruct current rows from
the record's row_id, target, layout, memberships and protocol. Compare its current
source identity with the consumed record. Do not pass original seed/fractions
into supplied mode; preserve the original record, including seed/settings, in
the metadata rather than replacing it with the reconstruction record.
Seeded records have protocol null; supplied mode may normalize that to a supplied
protocol internally. That normalization must not rewrite the consumed record.

Clone the caller's pipeline; fit only the selected training columns. Transform
training columns to validate declared output width/dtypes before returning.
Project code then invokes the returned native `transform` on selected validation,
test and inference columns. Preserve caller frame, pipeline, record and cwd.
This helper does not generate a new partition scheme or refit held-out rows.

## Metadata 1.0

The proposed exact dictionary is shared with the US-26-owned
[coordination index](../../US-26-mlflow/docs/plans/milestone-1-us-15-us-26-execution-order.md#proposed-handoff-types).
The shared index now incorporates the developer-approved
[encoding revision](plans/us15-us26-contract-revision.md). US-15 explicitly
acknowledges [US-26 concurrence](../../US-26-mlflow/docs/verification/us26-sc01-concurrence.md);
[producer reconciliation](verification/us15-sc01-concurrence.md) confirms no
remaining interface differences. Both Gate 1 decisions remain pending.

| Required field | Value |
|---|---|
| schema_version | String `"1.0"` |
| fit_partition | String `"train"` |
| partition_record | Existing full 1.0 record with schema_version, layout, row_id, target, source, method, settings, protocol, memberships |
| selected_columns | Nonempty unique ordered list of strings |
| input_schema | Ordered list of `{name: str, dtype: str}` for actual selected columns |
| output_schema | Nonempty ordered list of unique `{name: str, dtype: str}`, checked against native training output |
| pipeline | `{class_name: str, parameters: dict[str, Json]}` |
| versions | String version map requiring agentic-ml, pandas, pyarrow, scikit-learn |

Reject unknown keys in versioned structures; variable parameters/version maps
retain their permitted keys. `Json` is null, bool, string, integer, finite float,
list of Json or string-keyed dictionary of Json. JSON numbers remain finite.
Native parameter sentinels and dtype descriptors use the exact tagged records
below; reject other unsupported objects and cycles. Counts exclude booleans.

Encode each estimator using its fully qualified class name and
`get_params(deep=False)` recursively. Encode tuples/lists as lists, numpy scalar
values as ordinary JSON scalars and supported arrays as lists. Ordered native
Pipeline steps and ColumnTransformer triples retain names, order and effective
defaults. The following narrow native settings have explicit representations:

| Native parameter | Exact JSON representation |
|---|---|
| NaN at SimpleImputer.missing_values | `{"kind": "missing_value", "value": "nan"}` |
| Supported numpy scalar type or native dtype object | `{"kind": "numpy_dtype", "name": "float64"}` (name varies within the list below) |

Allowed canonical dtype names: bool, int8, int16, int32, int64, uint8, uint16,
uint32, uint64, float16, float32, float64. Dtype classes are recognized through
this explicit native list, not by importing an arbitrary supplied class path.
Finite numpy scalar instances remain ordinary JSON values. Dtype descriptors
record the native numeric dtype, not an arbitrary callable.

The missing-value tag is allowed only for NaN in the built-in SimpleImputer's
missing_values parameter. Infinity remains invalid everywhere; NaN metrics,
provenance values and ordinary numeric settings remain invalid. Tagged records
require exactly their displayed keys and values. Reserve these two `kind` values
within parameter mappings: reject caller-supplied literal mappings using them
rather than confusing them with native parameter descriptions. These tags are
metadata descriptions, not a new pipeline reconstruction API. Rejection of
literal reserved maps applies while encoding caller settings; the consumer
accepts canonical generated tags in supported contexts and validates them.

US-26 must validate these same representations and retain them unchanged in
metadata.json. Do not serialize settings with repr or pickle text. Preserve source
SHA-256 as its existing bare digest and existing source versions; do not convert
it to a DVC identity or add a new split identifier.

## Supported native composition and errors

The M1 verification matrix uses Pipeline, ColumnTransformer, SimpleImputer,
StandardScaler and OneHotEncoder. Use explicit ordered column-name lists for
ColumnTransformer selections; callable selectors/settings remain outside the
recordable M1 boundary. Default `memory=None` and `transform_input=None` are
recordable Pipeline settings. Native passthrough/drop strings and ordinary
scalar/list/dictionary estimator settings use the revised JSON rules. Custom
components and callable capture remain M2/US-16 work.

Declared names describe the project's output schema. Check width, uniqueness
and per-column dtype against the training transform; native generated feature
names may help the project declare names but do not silently replace its schema.
For sparse output, use native shape/dtype inspection without densifying merely
to validate schema. Native composition feasibility was probed with dense output;
sparse behavior still needs a public regression case before support is claimed.
All-null default mean imputation can drop a column. An incompatible declaration
fails; do not silently change the imputer's native defaults.

Reject invalid fit_partition, non-Pipeline input, duplicate/missing features,
ID/target selection, invalid schema and unrecordable settings before affected
fit. Existing supplied-mode checks reject wrong layout keys, empty partitions,
overlap, repeated/unknown/missing IDs and incompatible ID types. Compare current
source identity before fit to detect changed values under otherwise valid IDs.
Type errors use TypeError; invalid values use ValueError with field context.
Native fitting/transform errors retain their type/cause with stage context.
Output-shape errors necessarily follow training fit but return no successful
result. These checks do not constrain arbitrary project Python.

## Public verification and tracking boundary

The [plan's fixture matrix](plans/milestone-1-us-15.md#proposed-interface-and-independently-defined-test-boundary)
defines independent literal expectations for both layouts, held-out/inference
values, imputation, unseen categories, reordered/string IDs and invalid records.
Tests will call the proposed public helper and native transform, check input
preservation and strict JSON, and avoid private helpers or mocked fit counts.
Gate 1 must confirm those boundaries before executable toolkit tests.

US-15 returns no Git, DVC or MLflow discoveries and no intermediate joblib file.
US-26 receives the native fitted object and metadata plus separately supplied
shared provenance, then preserves them in an existing MLflow run. US-26's
native findings are now available. The agreed bounded serialization choice is
`serialization_format="skops", skops_trusted_types=["numpy.dtype"]` for the
locked M1 fixture, without broad trust discovery or pickle fallback. Producer
and independent consumer feasibility passed the complete-metadata/native-save
probes. Consumer contract/index adoption and producer acknowledgement are
complete; both Gate 1 decisions remain pending. Actual
installed integration belongs to US-26 IP4 and is required for US-15 AC-03.
Restored transformation equivalence (AC-04) remains M2.
