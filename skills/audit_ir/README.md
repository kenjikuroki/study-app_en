# audit_ir

## Skill Purpose

`audit_ir` defines the reusable skill for reviewing IR quality before question creation.
It checks whether each IR is atomic, traceable, category-correct, and suitable for later question generation.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/apps/active_apps/{app_id}/app_config.json`

## Output Paths

- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Validate the category against `app_config.json`.
2. Read the IR file.
3. Audit each IR one by one.
4. Trace each item to `source` and `source_section`.
5. Confirm the statement against the source.
6. Detect duplicates and near-duplicates.
7. Detect mixed-fact items.
8. Reassess confidence and question potential.
9. Classify each item as `approved`, `needs_revision`, or `rejected`.

## Check Items

- source exists
- source section is specific
- statement supported by source
- one fact only
- category valid
- confidence reasonable
- question potential reasonable
- duplicate risk checked
- version/environment caveats handled

## Prohibitions

- Do not convert IR into questions.
- Do not approve source-less IR.
- Do not approve `confidence=low` IR.
- Do not approve category mismatch.
- Do not approve mixed-fact IR.

## Mandatory Quality Rule

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Log Format

```json
{
  "item_id": "",
  "checked_individually": true,
  "source_checked": true,
  "source_check_skipped": false,
  "skip_reason": "",
  "decision": "approved | needs_revision | rejected | manual_review",
  "reason": ""
}
```

## Output Format

IR audit report JSON

## Handoff Condition To `question_creator`

Only items marked `approved` may be handed to `question_creator`.
`needs_revision` and `rejected` items must be blocked from question creation.
