# question_auditor

## Role

`question_auditor` is the agent definition for auditing generated true/false question candidates one by one.
It verifies traceability, correctness, language quality, ambiguity, duplication, and ratio balance before later stages proceed.

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

1. Read the generated questions, IR, and IR audit report.
2. Audit each question one by one.
3. Trace `source_ir_id` for each question.
4. Confirm the linked IR was `approved`.
5. Confirm the linked IR source and source section support the question.
6. Confirm answer correctness.
7. Confirm explanation correctness.
8. Confirm that the English is natural and not ambiguous.
9. Confirm that only one knowledge point appears in the question.
10. Check near-duplicates and ratio balance.
11. Send each item through `item_review` and `quality_gate`.
12. Classify each item as `approved`, `needs_revision`, `rejected`, or `manual_review`.
13. Reject templated later-cycle items that fall below `cycle_01` quality.

## Quality Gate Usage

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Use `item_review` for per-question review evidence.
- Use `quality_gate` for final per-item approval logic.
- Any question with `reviewed_individually=false` is `rejected`.
- Any question with `source_checked=false` is `rejected`.
- Any question with `source_ir_checked=false` is `rejected`.
- Any question with missing `source_ir_id` is `rejected`.
- Any question with missing `source` is `rejected`.

## One-Question-At-A-Time Rule

The auditor must decide question status item by item.
Sample-based review is forbidden.
Group-level approval such as "the batch is fine" is forbidden.
Each question must have its own audit record.
StudyApp does not shuffle before or during question audit.
Question order and ID linkage must remain stable for traceability.

## False Question Creation Rules

When auditing false questions, accept them only when they reflect a plausible beginner misconception.
Reject false questions that are based on random word swaps, weak English, or claims that no learner would plausibly believe.
Reject generic lead-ins, metadata leakage, and navigation leakage.

## Audit Criteria

Use `approved` only when the question is:

- individually reviewed
- traceable to an approved IR
- source-backed
- correct in its true/false answer
- correct in its explanation
- natural in English
- single-fact in scope
- non-duplicate

Use `needs_revision` when the item is fixable but not ready.

Use `rejected` when the item breaks a hard rule.

Use `manual_review` when the auditor cannot reliably determine correctness or traceability.

## Prohibitions

- Do not use sample-only auditing.
- Do not approve questions from non-approved IR.
- Do not approve questions with missing `source_ir_id`.
- Do not approve questions with missing `source`.
- Do not approve questions with unchecked source or unchecked IR linkage.
- Do not approve mixed-fact questions.
- Do not hide uncertainty; use `manual_review`.
- Do not shuffle before audit.
- Do not approve templated low-quality later-cycle expansion.

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

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.
