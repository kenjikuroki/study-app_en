# curate_cycle_bank

## Skill Purpose

`curate_cycle_bank` defines the reusable process for preparing a production-ready cycle bank that keeps later cycles at `cycle_01` quality.

## Input Paths

- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/output/ir/{app_id}/{category}/`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/docs/cycle_quality_policy.md`

## Output Paths

- `studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`
- `studyapp/output/logs/{app_id}/{category}/{cycle}_log.json`

## Processing Steps

1. Select the target cycle and target question count.
2. Build a source-backed set of approved IR items for that cycle only.
3. Create questions from approved IR only.
4. Audit each question one by one.
5. Keep only individually approved items.
6. Save the cycle bank for Pipeline Runner.

## Check Items

- item reviewed individually
- source checked individually
- natural English
- one fact per item
- false question is a realistic misconception
- no metadata leakage
- no navigation text leakage
- no generic `According to the official source` style lead-in

## Prohibitions

- Do not bulk-expand later cycles from weak templates.
- Do not use a generic 100-question slice as production input.
- Do not store unreviewed items in the cycle bank.

## Output Format

```json
{
  "ir_specs": [],
  "question_specs": []
}
```
