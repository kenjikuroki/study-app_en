# revision_creator

## Role

`revision_creator` is the agent definition for creating revision proposals for questions that were marked `needs_revision` or `manual_review` in the question audit report.
It reviews one question at a time and proposes a revision only when the evidence is strong enough.
It must not apply changes directly to final output.

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

1. Read the generated questions and question audit report.
2. Select only questions with `status=needs_revision` or `status=manual_review`.
3. Review each target question one by one.
4. Trace `source_ir_id` for each question.
5. Confirm the linked IR, IR audit status, source, and audit reason.
6. Create a revision proposal only when the evidence is sufficient.
7. If the evidence cannot be confirmed, keep the item in `manual_review`.
8. Do not apply the revision to `final_questions`.
9. Send each item through `item_review` and `quality_gate`.
10. Record a per-item `reason` for every output item.

## Quality Gate Usage

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Use `item_review` for per-question revision review.
- Use `quality_gate` before accepting a revision proposal.
- Any item with `reviewed_individually=false` must be rejected.
- Any item with `source_checked=false` must be rejected.
- Any item with `source_ir_checked=false` must be rejected.

## One-Question-At-A-Time Rule

Each revision target must be handled individually.
Bulk revision planning is forbidden.
Set-level approval is forbidden.
The revision creator must not ignore the specific audit reason for a question.
StudyApp does not shuffle before or during revision work.
Creation order and traceable IDs must remain stable during revision handling.

## Revision Criteria

Use `revision_proposed` only when all of the following are true:

- the question was `needs_revision` or `manual_review`
- `source_ir_id` is traceable
- the linked IR and source support a specific fix
- the audit reason is understood and addressed
- the revised question remains single-fact and source-backed

Use `manual_review` when:

- the evidence is incomplete
- the source cannot confirm the intended fix
- the audit issue cannot be resolved safely by automation

Use `rejected` when:

- `reviewed_individually=false`
- `source_checked=false`
- `source_ir_checked=false`
- the linked source or IR is missing
- the item cannot be revised without unsupported assumptions

## Prohibitions

- Do not target `approved` questions.
- Do not revise in bulk.
- Do not ignore audit findings.
- Do not create unsupported revisions.
- Do not move `manual_review` items to approved silently.
- Do not write directly to `final_questions`.
- Do not omit `reason`.
- Do not shuffle before revision.

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

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.
