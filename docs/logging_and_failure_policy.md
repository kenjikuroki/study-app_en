# Logging And Failure Policy

StudyApp requires traceable logs for every stage.

## Purpose

The logging system exists to show:

- what was checked
- what could not be checked
- what was skipped
- why a step stopped

## Required Logging Rule

- every stage must write logs
- every item must have its own review log
- `skipped` requires `skip_reason`
- `failed` requires `failure_reason`
- no item may be approved without a log
- no item may be approved without source confirmation when source confirmation is required
- `reviewed_individually=false` must be treated as `rejected`

## Per-Item Log Format

Path:

`studyapp/output/logs/{app_id}/{category}/cycle_XX_log.json`

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "step": "",
  "item_id": "",
  "reviewed_individually": true,
  "source_checked": true,
  "source_ir_checked": true,
  "status": "approved | needs_revision | rejected | manual_review | skipped | failed",
  "skip_reason": "",
  "failure_reason": "",
  "notes": ""
}
```

## Failure Report Rule

When a blocking failure occurs, StudyApp must emit a failure report.

Path:

`studyapp/output/logs/{app_id}/{category}/cycle_XX_failure_report.json`

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

## Pipeline Stop Conditions

Pipeline Runner must stop when:

- `source_documents` is missing
- `app_config.json` is missing
- IR count is `0`
- approved IR count is `0`
- generated question count is `0`
- approved question count is `0`
- `quality_gate` fails
- `validate_questions` fails
- `shuffle_questions` fails
- log writing fails

## Prohibitions

- do not continue after failure as if the step succeeded
- do not skip without `skip_reason`
- do not approve without a log
- do not use "overall looks fine" instead of per-item logging
- do not approve without source confirmation
