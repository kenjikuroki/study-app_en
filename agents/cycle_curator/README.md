# cycle_curator

## Role

`cycle_curator` prepares a production-quality cycle bank for one `{app_id}/{category}/{cycle}` run.
It exists to keep `cycle_02` and later at the same quality level as `cycle_01`.
It does not perform final output shuffling or pipeline orchestration.

## Input Paths

- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/output/ir/{app_id}/{category}/`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/`
- `studyapp/apps/active_apps/{app_id}/app_config.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/docs/cycle_quality_policy.md`

## Output Paths

- `studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`
- `studyapp/output/logs/{app_id}/{category}/{cycle}_log.json`

## Execution Steps

1. Read source documents for the target category.
2. Read the app config and confirm the requested category.
3. Build or reuse only source-backed IR items.
4. Audit each IR individually.
5. Create learner-facing question candidates from approved IR only.
6. Audit each question individually.
7. Keep only the items that are ready for that cycle size:
   - `cycle_01`: 30
   - `cycle_02`: 30
   - `cycle_03`: 30
   - `cycle_04`: 10
8. Store the curated IR and question set as one cycle bank.

## Quality Rule

`cycle_curator` must not mass-expand later cycles from generic templates or weak bank slicing.

Each cycle bank item must be individually reviewed before it is written.

## Prohibitions

- Do not auto-expand `cycle_02` or later from a generic 100-question bank.
- Do not use navigation text, footer text, or metadata as question content.
- Do not use generic stems like `According to the official source` as a shortcut.
- Do not write placeholder or unreviewed items to the cycle bank.

## JSON Output Format

```json
{
  "ir_specs": [],
  "question_specs": []
}
```

## Logging Rule

This agent must use `write_log`.
If curation cannot safely continue, it must write `failure_report`.
