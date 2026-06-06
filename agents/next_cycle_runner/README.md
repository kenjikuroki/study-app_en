# next_cycle_runner

## Role

`next_cycle_runner` decides whether the next StudyApp cycle is ready to run and, if ready, hands execution to `pipeline_runner`.

It does not create questions directly.
It does not curate content directly.
It exists to move from `cycle_01` to `cycle_02`, from `cycle_02` to `cycle_03`, and from `cycle_03` to `cycle_04` without weakening quality.

## Input Paths

- `studyapp/apps/active_apps/{app_id}/app_config.json`
- `studyapp/data/cycle_banks/{app_id}/{category}/cycle_XX.json`
- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/pipeline_run_log.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/docs/cycle_quality_policy.md`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/pipeline_run_log.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_failure_report.json`

## Execution Steps

1. Read `app_config.json` and confirm the target category.
2. Determine the current completed cycle and the next target cycle.
3. Confirm the previous cycle completed successfully.
4. Confirm a curated cycle bank exists for the next cycle.
5. Confirm the curated cycle bank matches the expected cycle size.
6. Confirm the next cycle is needed to reach the category target.
7. Hand execution to `pipeline_runner`.
8. Stop immediately if any readiness check fails.

## Readiness Rules

- `cycle_02` requires a completed `cycle_01`
- `cycle_03` requires a completed `cycle_02`
- `cycle_04` requires a completed `cycle_03`
- `cycle_02` and later require a curated cycle bank
- the cycle bank must contain only individually reviewed items
- the cycle bank must match the expected cycle size:
  - `cycle_01`: 30
  - `cycle_02`: 30
  - `cycle_03`: 30
  - `cycle_04`: 10

## Quality Rule

`next_cycle_runner` must not start a later cycle by falling back to generic bank slicing or weak auto-expansion.

## Prohibitions

- Do not create questions directly.
- Do not revise questions directly.
- Do not bypass `cycle_curator`.
- Do not start `cycle_02` or later without a curated cycle bank.
- Do not ignore a failed previous cycle.
- Do not ignore `write_log` or `failure_report`.

## Logging Rule

This agent must use `write_log`.
If the next cycle is not ready, it must use `failure_report`.
