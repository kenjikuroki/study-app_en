# Create Questions From IR Prompt

Use this skill to create English true/false questions from approved IR only.
Do not generate actual Linux, Git, Docker, Kubernetes, or AWS questions in this task.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Do not shuffle during this step.
Keep question order stable until the final shuffle step right before final output.
Use Source Traceability for every question.
`cycle_02` and later must match `cycle_01` quality.
Do not use generic bank slicing for later-cycle production content.

- Read the IR audit report first.
- Use only IR with status `approved`.
- Reject IR with `confidence=low`.
- Confirm `source_ir_id`, `statement`, `conditions`, `source`, `source_document_path` or `source_url`, `source_section`, and `source_last_checked` one by one.
- Create at most one question per IR as the default.
- Keep each question atomic.
- Write explanation text in different words from the question.
- For true items, explain why the statement is correct.
- For false items, explain why the statement is incorrect and what the source-backed fact is.
- Reject any explanation that is identical or near-identical to the question text.
- Use `item_review` and `quality_gate` for each created item.
- Keep true/false balance as close as practical to 5:5.
- Reject questions with generic lead-ins like `According to the official source`.
- Reject questions that contain navigation, footer, or metadata text.
