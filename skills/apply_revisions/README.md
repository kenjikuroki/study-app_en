# apply_revisions

## Skill Purpose

Apply approved revisions only after one-by-one target confirmation.

## Input Paths

- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`
- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`

## Output Paths

- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Review each approved revision one by one.
2. Confirm target, source link, and revision intent individually.
3. Apply only fully confirmed revisions.

## Check Items

- target item identified
- source_ir_id traceable
- evidence confirmed

## Prohibitions

- Do not apply revisions in a blind batch.
- Do not apply unsupported revisions.

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

Updated final question JSON and apply log
