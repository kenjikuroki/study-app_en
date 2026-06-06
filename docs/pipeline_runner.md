# Pipeline Runner

StudyApp uses Pipeline Runner to orchestrate one category pipeline run.
For multi-cycle production work, `next_cycle_runner` should decide whether the next cycle is ready before `pipeline_runner` is invoked.

## Purpose

Pipeline Runner is the command center of StudyApp.
It controls execution order for the pipeline.
It does not create questions or revisions by itself.

## Responsibility Split

- Pipeline Runner guarantees process order
- individual agents perform the work
- Quality Gate performs quality gating
- `write_log` records per-item and per-step traceability
- `failure_report` records blocking pipeline failures

Pipeline Runner does not guarantee quality.
For `cycle_02` and later, Pipeline Runner must require a curated cycle bank.

## Ordered Steps

1. read `app_config.json`
2. determine `category`
3. determine `cycle`
4. run `create_ir`
5. run `audit_ir`
6. run `quality_gate`
7. run `create_questions_from_ir`
8. run `create_false_questions`
9. run `audit_questions`
10. run `quality_gate`
11. run `create_revisions`
12. run `final_check`
13. run `validate_questions`
14. run `shuffle_questions`
15. write `final_questions`

## Multi-Cycle Control

Recommended later-cycle controller:

`studyapp/agents/next_cycle_runner/`

This agent should:

- detect the next required cycle
- confirm the previous cycle completed
- confirm the curated cycle bank exists
- then call `pipeline_runner`

## Later Cycle Rule

`cycle_02`, `cycle_03`, and `cycle_04` must not be populated by generic bank slicing.

Required curated input path:

`studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`

If the curated cycle bank is missing, Pipeline Runner must stop.

## Source Input Path

Pipeline Runner must use:

`studyapp/input/source_documents/{app_id}/{category}/`

as the official category-specific source input path.

In this context, `category` means `category_id`.
Pipeline Runner should resolve human-readable category names to `category_id` before using filesystem paths.

## Failure Handling

Pipeline Runner must stop when a blocking condition is reached.
It must not silently continue after failure.
Later steps should be recorded as `skipped` when the pipeline has already stopped.
Blocking failure must produce `cycle_XX_failure_report.json`.

## Blocking Conditions

- missing `app_config.json`
- missing `source_documents`
- approved IR count is `0`
- IR count is `0`
- approved question count is `0`
- generated question count is `0`
- `quality_gate` fails
- `validate_questions` fails
- `shuffle_questions` fails
- log writing fails
- missing curated cycle bank for `cycle_02`, `cycle_03`, or `cycle_04`

## Pipeline Log

Path:

`studyapp/output/logs/{app_id}/{category}/pipeline_run_log.json`

Format:

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "steps": [
    {
      "step": "create_ir",
      "status": "success | failed | skipped",
      "reason": ""
    }
  ],
  "pipeline_completed": false
}
```

## Prohibitions

- Pipeline Runner must not create questions
- Pipeline Runner must not revise questions
- Pipeline Runner must not skip audits
- Pipeline Runner must not skip Quality Gate
- Pipeline Runner must not backfill later cycles with weak auto-expansion
