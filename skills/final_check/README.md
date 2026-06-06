# final_check

## Skill Purpose

`final_check` defines the reusable skill for final per-question validation before final JSON output is written.
It decides which questions are safe to include in `final_questions`.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/question_audit_reports/{app_id}/{category}/cycle_XX_question_audit.json`
- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`

## Output Paths

- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read generated questions, question audit results, revision proposals, and IR data.
2. Review one question at a time.
3. Confirm `source_ir_id`, `source`, `answer`, and `explanation`.
4. Confirm the linked IR is usable.
5. Confirm category match and ID uniqueness.
6. Measure true/false ratio.
7. Exclude unconfirmed, rejected, or manual-review items.
8. Route each item through `item_review` and `quality_gate`.

## Quality Gate Usage

- Reject any item with `reviewed_individually=false`.
- Reject any item with unchecked source.
- Reject any item with unchecked source IR.
- Require per-item reasoning for inclusion or exclusion.

## One-Question-At-A-Time Rule

Each final decision must be made per question.
JSON validation alone is not enough.
Bulk approval is forbidden.
StudyApp does not shuffle before final review is complete.
The single shuffle step happens only after final review and validation.

## Final Review Criteria

- source confirmed
- source_ir_id confirmed
- answer confirmed
- explanation confirmed
- category matches
- no duplicate ID conflict
- final inclusion justified

## Prohibitions

- Do not rely on JSON syntax only.
- Do not include source-unchecked questions.
- Do not silently include `manual_review` items.
- Do not omit `reason` in the decision flow.
- Do not shuffle before final validation is complete.

## JSON Output Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "summary": {
    "total_final_questions": 0,
    "true_count": 0,
    "false_count": 0,
    "manual_review_excluded": 0,
    "rejected_excluded": 0
  },
  "questions": []
}
```
