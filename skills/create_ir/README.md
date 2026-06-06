# create_ir

## Skill Purpose

`create_ir` defines the reusable skill for extracting atomic, source-backed IR records from source documents.
It exists to prepare high-quality IR for later question creation, without creating any question content now.

## Input Paths

- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/apps/active_apps/{app_id}/app_config.json`

## Output Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Processing Steps

1. Validate the target category against `app_config.json`.
2. Read the source files under `source_documents`.
3. Extract one fact at a time.
4. Split commands, options, behaviors, limitations, best practices, and warnings into separate IR items.
5. Record `source` and `source_section`.
6. Record `source_document_path` or `source_url`, `source_title`, `source_version`, `source_last_checked`, and `source_quote_or_summary`.
7. Score `confidence`.
8. Score `question_potential`.
9. Add notes for version or environment caveats.
10. Exclude unsupported items.

## Check Items

- source read
- category valid
- one fact per IR
- source present
- source path or URL present
- source last checked present
- source section specific
- confidence justified
- question potential justified
- version/environment caveats noted when needed

## Prohibitions

- Do not create questions.
- Do not infer unsupported facts.
- Do not create IR without source metadata.
- Do not mix multiple facts in one IR.

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

IR JSON array

## Handoff Condition To `question_creator`

Only IR with valid category, exact source traceability, one-fact scope, and `confidence` of `high` or `medium` should proceed.
