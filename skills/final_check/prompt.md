# Final Check Prompt

Use this skill to perform final per-question validation before writing final output.
Do not generate actual question content in this task.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Do not shuffle before final review and validation are complete.
Allow one shuffle only after this step, immediately before final output.
Use Source Traceability for every final inclusion decision.

- Read generated questions, question audit data, revision proposals, IR, and IR audit data.
- Review one question at a time.
- Confirm `source_ir_id`, `source`, `source_document_path`, `source_section`, `source_last_checked`, `answer`, and `explanation`.
- Reject any item with `reviewed_individually=false`.
- Exclude any item with unconfirmed source.
- Reject later-cycle items that do not meet `cycle_01` language and learner-value quality.
- Reject generic source lead-ins, navigation leakage, or metadata leakage.
- Confirm category match, ID uniqueness, and true/false ratio.
- Do not include unresolved `manual_review` items without confirmed evidence.
- Include `reason` in every final inclusion or exclusion decision.
- Pass each item through `item_review` and `quality_gate`.
