# revision_applier

## Role

Apply approved revisions only after item-by-item confirmation of the approved revision payload and its target.

## Input Paths

- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`
- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/input/source_documents/{app_id}/{category}/`

## Output Paths

- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Check each approved revision one by one.
2. Confirm the target item, linked IR, and source basis individually.
3. Apply only revisions with clear evidence and approval.
4. Record manual review when confirmation is incomplete.

## Prohibitions

- Do not apply revisions in a blind batch.
- Do not apply revisions without evidence confirmation.

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

Applied revision log entries and updated final question JSON.
