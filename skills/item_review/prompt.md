# Item Review Prompt

Use this skill to review exactly one StudyApp item at a time.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Behavior

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Review one item only.
- If the item is an IR, confirm source, source section, statement, and category.
- If the item is a question, confirm source_ir_id, answer, explanation, source, and category.
- If the item is a revision, confirm original IR, original question, and revision evidence.
- If review cannot be completed, record the reason.
- If `reviewed_individually=false`, treat the item as rejected.

## Required Log Shape

```json
{
  "item_id": "",
  "reviewed_individually": true,
  "source_checked": true,
  "source_ir_checked": true,
  "approved": true,
  "skip_reason": "",
  "review_notes": ""
}
```
