# run_next_cycle

## Skill Purpose

`run_next_cycle` defines the reusable process for checking whether the next cycle is ready and then invoking `pipeline_runner`.

## Input Paths

- `studyapp/apps/active_apps/{app_id}/app_config.json`
- `studyapp/data/cycle_banks/{app_id}/{category}/cycle_XX.json`
- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/pipeline_run_log.json`
- `studyapp/docs/cycle_quality_policy.md`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/pipeline_run_log.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_failure_report.json`

## Processing Steps

1. Determine the next cycle from existing final outputs.
2. Confirm the previous cycle succeeded.
3. Confirm the curated cycle bank exists for the next cycle.
4. Confirm the cycle bank size matches the expected cycle size.
5. Confirm the category still needs more questions.
6. Invoke `pipeline_runner`.

## Check Items

- previous cycle success
- curated cycle bank present
- expected item count present
- no fallback to generic bank slicing
- category target not yet reached

## Prohibitions

- Do not run the next cycle without a curated cycle bank.
- Do not bypass the cycle quality policy.
- Do not continue after a failed readiness check.

## Output Format

This skill does not define a new content JSON format.
It uses existing pipeline logs and failure reports.
