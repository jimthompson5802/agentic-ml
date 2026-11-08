# Assistant-supported MVP walkthrough

Design 0.15; scope and document accepted at Gates 1–3.
**This is the required acceptance scenario, not a currently runnable end-to-end
tutorial.** Setup/planning/validation, extraction, quality checks, assessment and
recorded partitions exist; experiment execution/training/tracking/
DVC stages and this full demonstration remain implementation work.

## Audience, entry conditions and ownership

A data scientist owns a separate experiment project and an external coding-assistant
session. They supply local CSV/Parquet data, target/task, metric/direction, split
settings and search/trial bounds. The assistant helps edit project code/notebooks,
invoke installed public interfaces and native DVC, inspect MLflow evidence and
make a scientist-directed revision. It does not require a toolkit-managed adapter.

Use trusted local code. Keep credentials/generated storage outside Git. The
scientist directs final selection and avoids using final-test scores for further
development. Toolkit development gates are separate from this product workflow.

## What works today

Follow [installation/setup](../experiment-setup.md) and
[configuration validation](../configuration-validation.md) for current public
commands and their required inputs. After the documented pinned installation,
these commands exist:

```sh
uv run --locked agentic-ml --version
uv run --locked agentic-ml init
```

Initialization preserves conflicts and the pin and configures local storage, but
its 0.1 drafts do not run an experiment. Strict planning uses separate 1.0 inputs;
current config/candidate APIs need real plan/validation identities. No toolkit
`run`, `train` or `reproduce` command exists. New basic-path invocation and
runnable defaults must be reviewed/implemented under US-39-AC-01/02.
Do not present archival proposed APIs as available commands.

The installed Python APIs also provide
[pandas extraction/provenance](../extraction.md) via `extract_data`,
[quality checks](../data-quality.md) via `validate_data`/`run_validated_step`, and
[assessment/partitions](../data-assessment-and-splits.md) via
`assess_data`/`create_partitions`. These accepted components support seeded and
supplied two-way/three-way partitions. Project code owns report/split JSON
persistence and saved-source comparisons; time/group protocols are declarations.
Fitted preprocessing, training, MLflow records and DVC pipeline integration in
ASW-02–06 still need implementation and assistant evidence.

## M1: classification with scientist-directed assistant help

Each prompt below is an intended interaction. Replace placeholders with explicit
scientist choices in the acceptance fixture. The eventual runnable guide must name
verified entrypoints and commands once implemented; current omissions are explicit,
not an instruction to guess an API.

| Step | Scientist prompt and assistant work | Expected observable output | Criterion owner |
|---|---|---|---|
| ASW-01 setup | “Set up a classification experiment in this project using the installed toolkit. Explain the files and how I will run it.” | Pinned dependency/lock, runnable project configuration and public run path; no manual draft migration, toolkit edits or adapter. | US-39-AC-01/02/03/07; US-01/02/03/05 |
| ASW-02 extract | “Read these local files, apply these column/filter/join rules and check the target/data quality.” | Expected extracted data, quality diagnostics, extraction settings and DVC identity; missing/invalid required inputs fail clearly. | US-39-AC-03/04/08; US-11/12/13 |
| ASW-03 prepare | “Create reproducible partitions and a preprocessing pipeline. Show which rows fit learned preprocessing.” | Recorded disjoint train/validation/test membership, settings/seed and training-only fitted pipeline. | US-39-AC-04; US-12/14/15 |
| ASW-04 baseline/search | “Train a baseline and tune these candidates within this search space and maximum trial count.” | Real MLflow baseline/candidate runs, effective parameters, validation scores, trial count/elapsed time and fitted artifacts. | US-39-AC-04/07/08; US-05/10/18/20/26 |
| ASW-05 inspect/revise | “Inspect the validation results, explain one justified feature or parameter revision, then rerun it.” | At least one actual assistant edit and rerun, consistent split/metric, linked before/after validation evidence. A tie/regression is a valid result. No final-test scores feed the revision. | US-39-AC-05/07; US-14/18/20/21/26 |
| ASW-06 final test | “Evaluate this selected pipeline on the final test partition and show the saved model and results.” | Selected fitted pipeline/model, separate final scores/summary and actual MLflow artifact references. Quality shortfalls differ from process failure; no automatic final-feedback retuning. | US-39-AC-06/07; US-18/21/24/26 |

Commit required experiment source/configuration/lock/DVC metadata for reproducible
evidence. During exploratory edits, describe unsaved/uncommitted work honestly;
the MVP does not promise automatic capture/replay of arbitrary dirty project state.

## M2: reproduction, notebooks and customization

| Step | Scientist prompt and assistant work | Expected observable output | Criterion owner |
|---|---|---|---|
| ASW-07 reproduce | “Restore this committed experiment in a fresh project environment, reproduce it with DVC and compare its outputs.” | Restored versioned inputs, recorded identities, actual reruns or explicit cache reuse, comparable outputs within declared checks/tolerances and MLflow references. Demonstrate dependency invalidation and missing/corrupt-input failures. | US-40-AC-01–07; US-13/15/16/21/27 |
| ASW-08 extend | “Run the saved notebook version from a fresh kernel, demonstrate regression and use this compatible project transformer/estimator.” | Preserved notebook outputs/errors with explicit inputs/artifact references; regression results and restored compatible custom fitted state without toolkit edits/registry. | US-39-AC-09–11; US-40-AC-07; US-09/15/16/18/21/27 |

Once native DVC stage definitions and accessible storage exist, acceptance uses
documented DVC operations such as `uv run --locked dvc pull` and
`uv run --locked dvc repro`. These are native DVC commands, not a toolkit API
promise or a claim that current initialization creates runnable stages.

Run the unchanged declared pipeline to observe cache reuse. Change a declared
data/code/parameter dependency and record which stages rerun and their outputs.
Do not label cached training as newly executed; real reruns record actual MLflow
results and references to compared evidence. Required missing/corrupt source/data
must fail, never silently substitute alternate inputs.

## Evidence and acceptance

Automated installed-project tests check numerical outcomes, paths, data identities,
split/fit boundaries, invalid settings and expected artifacts. A manual assistant
demonstration checks that a scientist can discover, invoke, inspect and revise
through those same interfaces. These prove different boundaries.

Record at least one assistant product/interface/version, scientist prompts,
consequential project changes, commands and outcomes, committed source/config/
environment identities, MLflow run/model references, DVC identities and declared
comparison checks. A concise log is sufficient; complete transcripts and multiple
assistant products are not required. Assistant narrative is not independent proof.

M1 covers ASW-01–06, M2 ASW-07/08. No model gain is required for a truthful recorded
experiment. Tests define concrete fixtures/tolerances in reviewed implementation
plans before execution. No demonstration has been run by this design revision.
The [coverage matrix](design/acceptance-traceability.md) maps the criteria.

## Historical platform walkthrough

The [0.14 walkthrough/reference](example-walkthrough-v0.14-reference.md) preserves
the previously reviewed managed-agent workflow, proposed commands and detailed
type catalogue. It is historical reference, not the MVP run guide.

## Historical link aliases

These anchors retain old links as historical context; they do not reinstate
superseded platform requirements. See the [previous reviewed document](example-walkthrough-v0.14-reference.md).

<a id="example-scenario-build-a-customer-churn-model"></a>

<a id="how-to-read-the-sample-prompts"></a>

<a id="1-create-the-experiment-project"></a>

<a id="open-this-project-in-vs-code-and-select-its-venv-notebook-kernel"></a>

<a id="2-describe-the-prediction-problem-and-boundaries"></a>

<a id="3-assess-the-data-and-approve-the-splits"></a>

<a id="4-develop-features-and-establish-a-baseline"></a>

<a id="5-compare-models-then-tune-candidates"></a>

<a id="6-authorize-independent-final-evaluation"></a>

<a id="7-inspect-reproduce-or-resume-work"></a>

<a id="interactive-and-managed-operation"></a>

<a id="delivery-expectations"></a>

<a id="class-and-function-reference"></a>

<a id="how-the-objects-work-together"></a>

<a id="functions-by-responsibility"></a>

<a id="behavioral-classes-and-protocol-methods"></a>

<a id="complete-record-and-alias-index"></a>

<a id="error-classes-and-conceptual-name-replacements"></a>

<a id="boundaries-and-remaining-decisions"></a>
