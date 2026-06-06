# Audit Questions Prompt

Use this skill to audit generated true/false questions one by one.
Do not generate actual Linux, Git, Docker, Kubernetes, or AWS questions in this task.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Do not shuffle before or during audit.
Keep order stable for traceability and comparison.
Use Source Traceability for every question audit.

- Read generated questions, IR, and IR audit results.
- Review one question at a time.
- Confirm `source_ir_id`.
- Confirm linked IR approval status.
- Confirm source, `source_document_path` or `source_url`, `source_section`, `source_last_checked`, answer, explanation, category, and English quality.
- Reject questions that look like templated expansion rather than learner-facing English.
- Reject questions that contain navigation text, metadata text, or generic source lead-ins.
- Reject any question that fails mandatory traceability checks.
- Use `manual_review` when correctness cannot be decided safely.
- Route every item through `item_review` and `quality_gate`.
