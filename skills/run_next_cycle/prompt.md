# Run Next Cycle Prompt

Use this skill to decide whether the next StudyApp cycle is ready and to invoke `pipeline_runner` only when it is safe.

Every readiness check must be checked one by one.
Batch-level approval is forbidden.
If any readiness check is skipped, the agent must report the skipped item and the reason.

## Required Checks

- confirm the previous cycle completed
- confirm the curated cycle bank exists
- confirm the curated cycle bank has the correct count
- confirm the category still needs more questions

## Forbidden Behavior

- do not run `cycle_02`, `cycle_03`, or `cycle_04` without a curated cycle bank
- do not use generic bank slicing
- do not ignore failed prior cycles
- do not start a later cycle only because source files are present
