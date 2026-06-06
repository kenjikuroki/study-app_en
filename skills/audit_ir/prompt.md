# Audit IR Prompt

Use this skill to audit IR records only.
Do not create questions.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Use Source Traceability for every IR audit.

- Read `studyapp/apps/active_apps/{app_id}/app_config.json`.
- Read `studyapp/output/ir/{app_id}/{category}/{cycle_id}_ir.json`.
- Return to `studyapp/input/source_documents/{app_id}/{category}/` for each IR check.
- Do not use any other category input path.
- Confirm `source_document_path` or `source_url`, `source_section`, `source_last_checked`, and short `source_quote_or_summary`.
- Audit each IR individually.
