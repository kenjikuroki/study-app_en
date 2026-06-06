# Create IR Prompt

Use this skill to create IR records only.
Do not create questions or quiz answers.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Use Source Traceability for every IR.

- Read `studyapp/apps/active_apps/{app_id}/app_config.json` first.
- Read `studyapp/input/source_documents/{app_id}/{category}/` only.
- Extract only source-backed facts.
- Keep one IR to one fact.
- Record `source` and `source_section`.
- Record `source_document_path` or `source_url`, `source_title`, `source_version`, `source_last_checked`, and `source_quote_or_summary`.
- Use `notes` for version or environment scope.
- Mark uncertain items as `confidence=low`.
- Do not output unsupported IR.
