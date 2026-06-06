# source_traceability

## Skill Purpose

`source_traceability` defines the shared StudyApp skill for recording and verifying source evidence links for IR, questions, and revision proposals.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/`
- `studyapp/output/generated_questions/{app_id}/{category}/`
- `studyapp/output/revision_proposals/{app_id}/{category}/`
- `studyapp/input/source_documents/{app_id}/{category}/`

## Output Paths

- `studyapp/output/logs/{app_id}/{category}/`

## Processing Steps

1. Check that each IR has required source metadata.
2. Check that each question links back to a valid IR.
3. Check that each revision proposal preserves traceability.
4. Record `source_last_checked`.
5. Record `skip_reason` when a source check is skipped.

## Required Rules

- every IR must have `source_document_path` or `source_url`
- every IR must have `source_section`
- every IR must have `source_last_checked`
- every question must have `source_ir_id`
- every question must trace back to IR
- `source_quote_or_summary` must be short
- long quotations are forbidden
