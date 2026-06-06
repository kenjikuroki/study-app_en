# Create False Questions Prompt

Use this skill to create false questions from approved IR only.
Do not generate actual Linux, Git, Docker, Kubernetes, or AWS questions in this task.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Skill Instructions

- Review one IR at a time.
- Use only approved IR.
- Create false items from realistic beginner misconceptions.
- Prefer confusion between similar commands, similar concepts, omitted conditions, or mistaken purpose.
- Do not use shallow word reversal.
- Confirm the false statement can be disproved by the linked IR and source.
- Pass every item through `item_review` and `quality_gate`.
