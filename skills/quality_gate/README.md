# quality_gate

## Skill Purpose

`quality_gate` defines the shared review gate used by all StudyApp agents.
It verifies that each IR, question, or revision item was reviewed individually before approval.

## Input Paths

- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- per-stage item files such as:
- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/revision_proposals/{app_id}/{category}/cycle_XX_revisions.json`

## Output Paths

- stage-specific audit or log outputs
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Read `quality_rules.json`.
2. Read `checklist_rules.json`.
3. Determine the item type: IR, question, or revision.
4. Review each item individually.
5. Verify that all required checks for the item type were completed.
6. Reject any item with `reviewed_individually=false`.
7. Reject any skipped review without a reason.
8. Emit per-item review logs.

## Check Items

- no batch approval
- no sampling review
- source checks completed when required
- source IR checks completed when required
- per-item review log exists
- skip reasons recorded when needed

## Prohibitions

- Do not approve item groups in bulk.
- Do not rely on sample review.
- Do not approve without source confirmation where required.
- Do not accept missing skip reasons.

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

Per-item gate decision logs and stage-level review status.
