# ir_auditor

## Role

`ir_auditor` is the agent definition for auditing IR quality before any question creation starts.
It reviews each IR one by one, checks traceability and granularity, detects duplicates and weak items, and classifies each record as `approved`, `needs_revision`, or `rejected`.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/apps/active_apps/{app_id}/app_config.json`

## Output Paths

- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read `app_config.json` and confirm the target category is valid.
2. Read the IR file for the cycle.
3. Review each IR one by one.
4. Trace each IR back to its `source` and `source_section`.
5. Confirm the statement against the source material.
6. Detect duplicate or near-duplicate IR items.
7. Detect mixed-fact IR items.
8. Reassess `confidence`, `question_potential`, category validity, and version or environment risks.
9. Classify each IR as `approved`, `needs_revision`, or `rejected`.
10. Record per-item reasons and suggested fixes in the audit report.

## Decision Criteria

### `approved`

Use `approved` only when all of the following are true:

- `source` exists
- `source_section` is specific enough
- the statement is supported by the source
- only one fact is present
- `category` matches `app_config.json`
- `confidence` is not `low`
- the item is usable for later question creation

### `needs_revision`

Use `needs_revision` when the item may be usable after repair, such as:

- `source_section` is too broad
- `statement` is slightly too vague
- conditions are missing
- `notes` should mention version or environment scope
- `confidence` or `question_potential` appears misclassified
- the item overlaps another IR and needs consolidation

### `rejected`

Use `rejected` when the item should not proceed, such as:

- source evidence is missing
- the source does not support the statement
- multiple facts are mixed in one IR
- `category` is wrong
- the fact is outdated or too unstable to trust
- `confidence=low`

### Pass Condition For Next Step

Only IR items with `status=approved` may be passed to `question_creator`.
Items marked `needs_revision` or `rejected` must not move forward.

## Prohibitions

- Do not convert IR into questions.
- Do not approve IR without `source`.
- Do not approve IR with vague or unusable `source_section`.
- Do not approve `confidence=low` IR.
- Do not approve category-mismatched IR.
- Do not approve mixed-fact IR.
- Do not perform sample-only auditing.

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

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.

## JSON Output Format

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "summary": {
    "total_ir": 0,
    "approved": 0,
    "needs_revision": 0,
    "rejected": 0
  },
  "items": [
    {
      "ir_id": "",
      "status": "approved | needs_revision | rejected",
      "issues": [],
      "suggested_fix": "",
      "reason": ""
    }
  ]
}
```
