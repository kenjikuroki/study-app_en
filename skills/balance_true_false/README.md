# balance_true_false

## Skill Purpose

Measure true/false balance while still reviewing each question individually.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/apps/active_apps/{app_id}/questions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`

## Output Paths

- `studyapp/output/question_audit_reports/{app_id}/{category}/cycle_XX_question_audit.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Review each question one by one before any balance judgment.
2. Confirm current answer labels and source links individually.
3. Report skew only after per-item checks.

## Check Items

- per-item answer reviewed
- ratio measured
- quality preserved

## Prohibitions

- Do not force balance by lowering quality.
- Do not judge balance without item review.

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

Balance report or audit section
