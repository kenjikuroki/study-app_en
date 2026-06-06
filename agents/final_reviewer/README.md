# final_reviewer

## Role

`final_reviewer` is the agent definition for the last per-question review before final output is written.
It checks approved questions together with revision proposals one by one and decides which questions may enter `final_questions`.

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

1. Read approved questions and revision proposals.
2. Review each candidate final question one by one.
3. Confirm `source_ir_id`, `source`, `explanation`, and `answer`.
4. Confirm the linked IR and IR audit status.
5. Confirm JSON structure, ID uniqueness, category consistency, and true/false balance.
6. Exclude any question whose source cannot be confirmed.
7. Exclude any question whose review record shows `reviewed_individually=false`.
8. Send each item through `item_review` and `quality_gate`.
9. Record per-item `reason` for inclusion or exclusion.

## Quality Gate Usage

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Use `item_review` for the final per-question review.
- Use `quality_gate` before final inclusion.
- Any item with `reviewed_individually=false` is rejected.
- Any item with unchecked source is rejected.
- Any item with unchecked IR linkage is rejected.

## One-Question-At-A-Time Rule

The final reviewer must decide item by item.
Bulk final approval is forbidden.
A valid JSON file alone is not enough.
Content, evidence, explanation, and answer all require per-question confirmation.
StudyApp does not shuffle before final review is complete.
Shuffling is allowed once only after final review and validation.

## Final Review Criteria

Include a question in `final_questions` only when all of the following are true:

- the question is individually reviewed
- `source_ir_id` is valid
- `source` is valid
- the linked IR is usable
- `answer` is correct
- `explanation` is correct
- category matches
- the question is not excluded by audit or revision status

Exclude a question when:

- `reviewed_individually=false`
- source cannot be checked
- linked IR cannot be checked
- the answer or explanation cannot be trusted
- the question remains `manual_review`
- the question is rejected by final review

## Prohibitions

- Do not rely on JSON syntax checks alone.
- Do not batch-approve final output.
- Do not include source-unverified questions.
- Do not silently include `manual_review` items.
- Do not omit `reason` from final inclusion or exclusion logic.
- Do not shuffle before final review is complete.

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

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.
