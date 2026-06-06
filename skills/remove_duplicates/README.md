# remove_duplicates

## Skill Purpose

Detect duplicate and near-duplicate questions with one-by-one review.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/apps/active_apps/{app_id}/questions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`

## Output Paths

- `studyapp/output/question_audit_reports/{app_id}/{category}/cycle_XX_question_audit.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Review each question one by one.
2. Compare each item against existing and new items individually.
3. Confirm duplicates with content and evidence context.

## Check Items

- duplicate ids
- duplicate facts
- near-duplicate wording

## Prohibitions

- Do not rely on string match only.
- Do not mark duplicates in bulk without item review.

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

Duplicate check report or audit section
