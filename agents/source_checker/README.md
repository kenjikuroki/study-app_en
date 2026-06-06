# source_checker

## Role

Check source quality and source availability one item at a time for IR-first pipelines.

## Input Paths

- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Review each source reference one by one.
2. Confirm each IR can be traced back to a readable source item.
3. Record missing or weak evidence for manual review.

## Prohibitions

- Do not mark all sources valid in bulk.
- Do not skip source traceability checks silently.

## Mandatory Quality Rule

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Log Format

```json
{
  "item_id": "",
  "checked_individually": true,
  "source_checked": true,
  "source_check_skipped": false,
  "skip_reason": "",
  "decision": "approved | needs_revision | rejected | manual_review",
  "reason": ""
}
```

## Output JSON Format

Source validation logs.
