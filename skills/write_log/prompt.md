# Write Log Prompt

Use this skill to write per-item StudyApp execution logs.

## Mandatory Rules

- write a log entry for every reviewed item
- include the current `step`
- if `status=skipped`, `skip_reason` must be non-empty
- if `status=failed`, `failure_reason` must be non-empty
- if `reviewed_individually=false`, treat the item as `rejected`
- do not allow approval without a log entry

## Required Output Shape

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
