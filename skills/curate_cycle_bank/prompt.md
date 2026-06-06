# Curate Cycle Bank Prompt

Use this skill to prepare one curated cycle bank for StudyApp.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Goal

Prepare:

`studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`

for one specific cycle.

## Quality Rule

`cycle_02`, `cycle_03`, and `cycle_04` must be as strong as `cycle_01`.

## Do Not Do This

- do not slice a generic 100-question bank
- do not use generic lead-ins like `According to the official source`
- do not use navigation or footer text
- do not keep weak false questions
- do not include any item that was not individually reviewed

## Required Review

- verify source
- verify linked IR
- verify answer
- verify explanation
- verify natural English
- verify learner value
- verify category fit
