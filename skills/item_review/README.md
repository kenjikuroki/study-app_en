# item_review

## Skill Purpose

`item_review` defines the per-item review procedure used before any approval decision in StudyApp.
It focuses on one IR, one question, or one revision at a time.

## Input Paths

- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- a single target item from:
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`

## Output Paths

- stage-specific logs or reports
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Read the quality rules.
2. Identify the current item type.
3. Review exactly one item.
4. Apply the required checks for that one item.
5. Record the outcome in the required log shape.
6. Hand the result to `quality_gate` for final gating.

## Check Items

- item reviewed individually
- required source checks completed
- required source IR checks completed
- approval justified
- skip reason present when needed

## Prohibitions

- Do not review multiple items as one group.
- Do not mark an item approved without completing its required checks.
- Do not leave skipped checks unexplained.

## Mandatory Quality Rule

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Log Format

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

## Output Format

Single-item review log entry.
