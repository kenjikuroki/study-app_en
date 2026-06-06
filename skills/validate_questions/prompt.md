# Validate Questions Prompt Template

Validate question JSON one item at a time.

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.
Do not shuffle during validation.
Validation happens before the one allowed final shuffle step.
