# write_log

## Skill Purpose

`write_log` defines the shared logging skill for StudyApp pipeline stages.
It records per-item decisions and stage outcomes in a traceable format.

## Input Paths

- stage inputs from any StudyApp pipeline step
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.json`

## Processing Steps

1. Identify the current pipeline step.
2. Write one log entry per item reviewed.
3. Record approval, revision, rejection, manual review, skip, or failure status.
4. Record `skip_reason` for skipped items.
5. Record `failure_reason` for failed items.
6. Reject items that were not reviewed individually.

## Required Rules

- every stage writes logs
- every item writes its own log entry
- `skipped` requires `skip_reason`
- `failed` requires `failure_reason`
- `reviewed_individually=false` becomes `rejected`
- do not approve without a log

## Required Log Format

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
