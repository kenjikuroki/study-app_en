# source_validation

## Skill Purpose

Validate source traceability for IR and question records one item at a time.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/input/source_documents/{app_id}/{category}/`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Review each IR and question one by one.
2. Confirm source paths and source sections individually.
3. Report skipped checks with reasons.

## Check Items

- source exists
- source_section exists
- source_ir_id traceable

## Prohibitions

- Do not batch-approve source validity.
- Do not skip reporting when source confirmation is incomplete.

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

## Output Format

Source validation log
