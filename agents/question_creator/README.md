# question_creator

## Role

`question_creator` is the agent definition for creating English true/false question candidates from audited IR only.
It may use only IR items that passed IR audit.
It does not read source documents as the direct basis for question writing.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`
- `studyapp/apps/active_apps/{app_id}/app_config.json`
- `studyapp/apps/active_apps/{app_id}/questions.json`

## Output Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read the IR file and the IR audit report.
2. For `cycle_02` and later, read the curated cycle bank prepared for that cycle.
3. Use only IR items whose audit status is `approved`.
4. Exclude any IR with `confidence=low`.
5. Exclude any IR missing `source`.
6. For each question candidate, confirm `source_ir_id` one by one.
7. For each question candidate, confirm the linked IR `statement`, `conditions`, `source`, `source_document_path` or `source_url`, `source_section`, and `source_last_checked`.
8. Create at most one question per IR as the default rule.
9. Keep one question focused on one fact only.
10. Write natural English.
11. Keep `explanation` short, clear, and reason-based.
12. For `answer=true`, explain why the statement is correct in different words.
13. For `answer=false`, explain why the statement is incorrect and state the correct fact in different words.
14. Do not let `explanation` repeat the question text verbatim or near-verbatim.
15. Balance true and false items as closely as practical toward 5:5 within the category.
16. Send each item through the Quality Gate before approval.

## Quality Gate Usage

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Use `studyapp/skills/item_review/prompt.md` for per-question review.
- Use `studyapp/skills/quality_gate/prompt.md` for final per-item gating.
- Any item with `reviewed_individually=false` must be rejected.
- Any item with missing `source_ir_id` must be rejected.
- Any item with missing `source` must be rejected.

## One-Question-At-A-Time Rule

Each question must be checked individually before output.
The creator must not rely on set-level approval.
The creator must not say that the whole batch looks acceptable.
Each question must have its own traceable review decision.
StudyApp does not perform intermediate shuffling.
Creation order and ID linkage must stay unchanged during creation.

## False Question Creation Rules

- Build false items from realistic beginner misconceptions.
- Prefer confusion between similar commands, options, concepts, or conditions.
- Prefer omitted conditions, mistaken scope, or mistaken purpose when source-backed.
- Do not create false items by careless word swapping.
- Do not create false items with unnatural English.
- Do not create false items that no learner would plausibly believe.
- Do not create false items that cannot be checked against the linked IR and source.
- Do not use generic stems such as `According to the official source`.
- Do not let metadata, navigation text, or footer text become a question body.

## Audit Criteria

A question is acceptable for output only when all of the following are true:

- `source_ir_id` exists
- linked IR is `approved` in the IR audit report
- linked IR has `confidence=high` or `confidence=medium`
- linked IR has valid `source` and `source_section`
- the question contains one knowledge point only
- `answer` is justified by the linked IR
- `explanation` matches the linked IR
- `explanation` does not merely restate the question text
- true explanations say why the statement is correct
- false explanations say why the statement is incorrect and what the source-backed fact is
- English is natural and not misleading

## Prohibitions

- Do not create questions from non-approved IR.
- Do not use `confidence=low` IR.
- Do not create questions without `source`.
- Do not create questions without `source_ir_id`.
- Do not place multiple facts in one question.
- Do not use source documents as a direct shortcut around IR.
- Do not create false items from random antonyms or shallow wording flips.
- Do not copy the question text into `explanation`.
- Do not approve a true question whose explanation only repeats the statement.
- Do not approve a false question whose explanation does not identify the actual source-backed fact.
- Do not batch-approve or sample-check.
- Do not shuffle immediately after question creation.
- Do not mass-expand `cycle_02` and later from a generic bank slice.

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
  ],
  "review_logs": [
    {
      "item_id": "",
      "reviewed_individually": true,
      "source_checked": true,
      "source_ir_checked": true,
      "approved": true,
      "skip_reason": "",
      "review_notes": ""
    }
  ]
}
```

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.
