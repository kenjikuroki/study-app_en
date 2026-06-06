# audit_questions

## Skill Purpose

`audit_questions` defines the reusable skill for auditing generated questions one by one before later pipeline stages proceed.
It is responsible for correctness, traceability, ambiguity review, duplicate review, and ratio review.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`
- `studyapp/apps/active_apps/{app_id}/questions.json`

## Output Paths

- `studyapp/output/question_audit_reports/{app_id}/{category}/cycle_XX_question_audit.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read the generated questions and their linked IR data.
2. Audit each question individually.
3. Confirm `source_ir_id`, source, answer, explanation, and category.
4. Confirm the question comes from approved IR only.
5. Reject explanations that repeat the question text.
6. Confirm true explanations say why the statement is correct.
7. Confirm false explanations say why the statement is incorrect and what the correct fact is.
8. Confirm single-fact scope and natural English.
9. Detect ambiguity, duplicates, and near-duplicates.
10. Measure true/false balance.
11. Route each item through `item_review` and `quality_gate`.

## Quality Gate Usage

- Reject any question with `reviewed_individually=false`.
- Reject any question with `source_checked=false`.
- Reject any question with `source_ir_checked=false`.
- Reject any question missing `source_ir_id`.
- Reject any question missing `source`.

## One-Question-At-A-Time Rule

Each question must be judged separately.
Sample review is forbidden.
Set-level approval is forbidden.
StudyApp does not shuffle during question audit.
Question order and ID linkage must remain stable for comparison and traceability.

## False Question Creation Rules

When reviewing false items, keep only those that are believable, source-checkable, and tied to realistic misconceptions.

## Audit Criteria

- approved source IR
- valid traceability
- correct answer
- correct explanation
- explanation not equal to the question text
- explanation gives the reason for correctness or incorrectness
- natural English
- low ambiguity
- one fact only
- no duplicate overlap

## Prohibitions

- Do not sample-check.
- Do not approve questions from non-approved IR.
- Do not approve questions missing required traceability.
- Do not approve unchecked questions.
- Do not approve explanations that simply restate the question.
- Do not shuffle before or during audit.

## JSON Output Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "summary": {
    "total_questions": 0,
    "approved": 0,
    "needs_revision": 0,
    "rejected": 0,
    "manual_review": 0,
    "true_count": 0,
    "false_count": 0
  },
  "items": [
    {
      "question_id": "",
      "status": "approved | needs_revision | rejected | manual_review",
      "issues": [],
      "source_ir_checked": true,
      "source_checked": true,
      "reviewed_individually": true,
      "suggested_fix": "",
      "reason": ""
    }
  ]
}
```
