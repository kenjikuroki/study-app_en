# create_questions

## Skill Purpose

Legacy question creation helper kept aligned with the IR First one-by-one review rule.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`

## Output Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Review each question candidate one by one.
2. Confirm `source_ir_id`, source, and explanation individually.

## Check Items

- source_ir_id traceable
- answer checked
- explanation checked

## Prohibitions

- Do not create questions directly from source documents.
- Do not batch-generate without individual review.

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

Question JSON
