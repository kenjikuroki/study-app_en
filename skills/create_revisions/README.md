# create_revisions

## Skill Purpose

`create_revisions` defines the reusable skill for proposing revisions for questions that failed question audit.
It works only on `needs_revision` and `manual_review` items and never applies changes directly.

## Input Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/question_audit_reports/{app_id}/{category}/cycle_XX_question_audit.json`
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`

## Output Paths

- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read the question audit report.
2. Select `needs_revision` and `manual_review` items only.
3. Review one question at a time.
4. Confirm original question, original IR, and audit reason.
5. Propose a revision only if evidence supports it.
6. Keep unresolved items as `manual_review`.
7. Route every item through `item_review` and `quality_gate`.

## Quality Gate Usage

- Reject unreviewed items.
- Reject source-unchecked items.
- Reject IR-unchecked items.
- Require a `reason` in every output item.

## One-Question-At-A-Time Rule

This skill must handle revision targets individually.
Bulk revision output is forbidden.
StudyApp does not shuffle during revision work.
Traceable order and IDs must remain stable until final output preparation.

## Revision Criteria

- revise only fixable items
- keep unsupported items in `manual_review`
- never auto-approve unresolved uncertainty

## Prohibitions

- Do not revise `approved` questions.
- Do not skip the audit reason.
- Do not write directly to final output.
- Do not create unsupported revisions.
- Do not shuffle during revision creation.

## JSON Output Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "items": [
    {
      "question_id": "",
      "status": "revision_proposed | manual_review | rejected",
      "original_question": {},
      "revised_question": {},
      "issues": [],
      "source_ir_checked": true,
      "source_checked": true,
      "reviewed_individually": true,
      "reason": ""
    }
  ]
}
```
