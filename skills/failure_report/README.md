# failure_report

## Skill Purpose

`failure_report` defines the shared failure-reporting skill for blocking pipeline failures.
It records why the pipeline stopped and what should happen next.

## Input Paths

- pipeline state from `pipeline_runner`
- step logs

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/cycle_XX_failure_report.json`

## Processing Steps

1. Capture the failed step.
2. Record the blocking failure reason.
3. Record completed steps.
4. Record skipped steps.
5. Record the recommended next action.
6. Mark `manual_review_required=true`.

## Required Rules

- emit a failure report for every blocking pipeline stop
- do not continue the pipeline after a blocking failure
- `failure_reason` must be non-empty

## Required Failure Report Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "failed_step": "",
  "failure_reason": "",
  "completed_steps": [],
  "skipped_steps": [],
  "next_action": "",
  "manual_review_required": true
}
```
