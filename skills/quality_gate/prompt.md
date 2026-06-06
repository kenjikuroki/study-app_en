# Quality Gate Prompt

Use this skill as the shared approval gate for all StudyApp stages.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Use Source Traceability as part of approval checks.

- Read `studyapp/config/quality_rules.json`.
- Read `studyapp/config/checklist_rules.json`.
- Review each item one by one.
- Determine whether the item is an IR, a question, or a revision.
- Apply the required checklist for that item type.
- Confirm required traceability fields exist for the item type.
- Reject any item where `reviewed_individually=false`.
- Reject any item with a skipped review and no `skip_reason`.
- Reject any later-cycle question that shows templated low-quality expansion.
- Reject any question with metadata leakage, navigation leakage, or a generic source lead-in.
- Do not allow sample-based approval.
- Do not allow group-level approval.
