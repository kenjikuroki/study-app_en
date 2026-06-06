# validate_questions

## Skill Purpose

Validate question JSON and required fields with one-by-one item checks.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Check each question one by one.
2. Confirm JSON fields and link integrity.
3. Confirm `source_ir_id`, category, and required values per item.

## Check Items

- valid JSON
- required keys
- allowed values
- traceable source_ir_id

## Prohibitions

- Do not treat schema validation as full final review.
- Do not batch-approve all items.

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

Validation log or checklist
