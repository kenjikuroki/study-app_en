# Source Traceability Prompt

Use this skill to verify and record source traceability for StudyApp items.

## Mandatory Rules

- every IR must have `source_document_path` or `source_url`
- every IR must have `source_section`
- every IR must have `source_last_checked`
- every question must have `source_ir_id`
- every question must trace back to a valid IR
- if source checking is skipped, record `skip_reason`
- `source_quote_or_summary` must be a short summary
- long quotations are forbidden

## Trace Flow

question
source_ir_id
IR
source_document_path or source_url
source_section
