# create_questions_from_ir

## Skill Purpose

`create_questions_from_ir` defines the reusable skill for creating English true/false question candidates from approved IR only.
It is the primary question creation skill in the IR First pipeline.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`
- `studyapp/apps/active_apps/{app_id}/questions.json`

## Output Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read IR and IR audit data.
2. For `cycle_02` and later, work only from a curated cycle bank.
3. Filter to approved IR only.
4. Exclude `confidence=low` IR.
5. Review the linked IR one by one before creating each question.
6. Confirm `source_ir_id`, `source`, `source_document_path` or `source_url`, `source_section`, `source_last_checked`, `statement`, and `conditions`.
7. Create one question per IR by default.
8. Keep the question single-fact and natural in English.
9. Route each created item through `item_review` and `quality_gate`.

## Quality Gate Usage

- Use `item_review` for each question candidate.
- Use `quality_gate` before approving output.
- Reject items that fail individual review requirements.

## One-Question-At-A-Time Rule

Each question must be created and checked individually.
The skill must never rely on batch approval or sample review.
StudyApp does not shuffle during this step.
Question order and ID linkage must stay stable until final output preparation.

## False Question Creation Rules

- False items must come from realistic misconceptions tied to the IR.
- Do not use shallow opposite-word flips.
- Do not create false items that cannot be verified against the source-backed IR.
- Do not use generic stems like `According to the official source`.
- Do not let navigation text or metadata become question content.

## Audit Criteria

- approved IR only
- source present
- source_ir_id present
- one fact per question
- explanation supported
- English natural

## Prohibitions

- Do not use non-approved IR.
- Do not use `confidence=low` IR.
- Do not create questions without `source_ir_id`.
- Do not create questions without `source`.
- Do not create multi-fact questions.
- Do not shuffle during question creation.
- Do not mass-expand later cycles from a generic bank slice.

## JSON Output Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "questions": [
    {
      "id": "",
      "category": "",
      "question": "",
      "answer": true,
      "explanation": "",
      "source": "",
      "source_ir_id": "",
      "source_document_path": "",
      "source_section": "",
      "source_last_checked": "",
      "difficulty": "basic | intermediate | advanced"
    }
  ]
}
```
