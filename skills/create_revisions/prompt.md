# Create Revisions Prompt

Use this skill to create revision proposals for `needs_revision` and `manual_review` questions only.
Do not generate actual question content in this task.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Do not shuffle before or during revision creation.
Keep order and ID linkage stable until final output preparation.
Use Source Traceability when preparing revision proposals.

- Read generated questions, question audit, IR, and IR audit data.
- Review one question at a time.
- Confirm the linked IR, `source_document_path` or `source_url`, `source_section`, and `source_last_checked` before proposing any change.
- If evidence is insufficient, keep the item as `manual_review`.
- Do not write to `final_questions`.
- Include `reason` in every output item.
- Pass each item through `item_review` and `quality_gate`.
