# create_false_questions

## Skill Purpose

`create_false_questions` defines the reusable skill for creating high-quality false questions from approved IR.
It exists to produce believable, source-checkable false items rather than shallow trick wording.

## Input Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/ir_audit_reports/{app_id}/{category}/cycle_XX_ir_audit.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`
- `studyapp/skills/quality_gate/prompt.md`
- `studyapp/skills/item_review/prompt.md`

## Output Paths

- `studyapp/output/generated_questions/{app_id}/{category}/cycle_XX_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read approved IR only.
2. Review one IR at a time.
3. Identify realistic beginner misconceptions.
4. Build a false question grounded in the linked IR.
5. Confirm the false claim is source-checkable.
6. Confirm the explanation clearly shows why the claim is false and what the correct fact is.
7. Pass the item through `item_review` and `quality_gate`.

## Quality Gate Usage

- Review each false item individually.
- Reject any false item that cannot be source-checked.
- Reject any false item not individually reviewed.

## One-Question-At-A-Time Rule

Each false question must be considered individually.
The skill must not produce or approve false items in bulk.
StudyApp does not shuffle during false-question creation.
Traceable order must stay stable until the final shuffle step.

## False Question Creation Rules

Good false questions:

- are based on learner confusion
- reflect realistic misunderstanding
- involve similar concepts or commands
- capture omitted conditions
- capture mistaken usage or purpose

Bad false questions:

- use random opposite words
- sound unnatural in English
- are obviously absurd
- have weak relation to the linked IR
- cannot be verified from the source-backed IR

## Audit Criteria

- believable misconception
- strong IR linkage
- source checkable
- short clear explanation
- explanation not equal to the question text
- explanation names the actual source-backed fact
- natural English

## Prohibitions

- Do not create false items from random antonyms.
- Do not create false items that nobody would believe.
- Do not create false items that cannot be checked against the IR and source.
- Do not copy the false question text into `explanation`.
- Do not bypass Quality Gate.
- Do not shuffle during false-question creation.

## JSON Output Format

```json
{
  "id": "",
  "category": "",
  "question": "",
  "answer": false,
  "explanation": "",
  "source": "",
  "source_ir_id": "",
  "difficulty": "basic | intermediate | advanced"
}
```
