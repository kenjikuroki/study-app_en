# Dry Run Policy

Dry Run is used to verify the StudyApp pipeline before production question generation.

Dry Run must execute the same quality rules as production:

- IR First
- source check
- one-by-one review
- Quality Gate
- logging
- failure report
- final validation
- shuffle only before final output

Dry Run output must not be mixed with production output.

## Scope

Dry Run exists to verify that the pipeline can run end to end with a small target set before production-scale execution.

## Dry Run Target

- app_id: `_dry_run_linux`
- category_id: `basic_commands`
- target question count: `3` to `5`

## Verification Goals

- confirm `source_documents` can be read
- confirm `app_config.json` can be read
- confirm IR creation can run
- confirm IR audit can run
- confirm question creation can run
- confirm question audit can run
- confirm revision creation can run
- confirm final check can run
- confirm `validate_questions` can run
- confirm `shuffle_questions` can run
- confirm logging and `failure_report` can be emitted

## Output Rule

Dry Run output must stay under:

`studyapp/output/dry_run/`

Dry Run questions must not be mixed into production `questions.json` or production outputs.

## Quality Rule

Dry Run does not relax quality requirements.
Dry Run must still use:

- source confirmation
- one-by-one review
- Quality Gate
- logging
- failure reporting

## Current Note

This is a Dry Run specification and template setup only.
It does not execute production question generation.
