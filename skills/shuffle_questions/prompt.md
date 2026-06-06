# Shuffle Questions Prompt

Use this skill only once, immediately before writing `final_questions`.
Do not generate actual question content in this task.

## Mandatory Rules

- Do not shuffle during IR creation.
- Do not shuffle during IR audit.
- Do not shuffle during question creation.
- Do not shuffle during question audit.
- Do not shuffle during revision creation.
- Do not shuffle before final review is complete.
- Shuffle only at this sequence:
- `Final Reviewer`
- approved questions collected
- `validate_questions`
- `shuffle_questions`
- `final_questions` JSON output

## Shuffle Procedure

- Read the approved final questions.
- Preserve every question item exactly.
- Change array order only.
- Do not change `question_id`.
- Do not change `source_ir_id`.
- Do not change `category`.
- Do not change `question`, `answer`, `explanation`, or `source`.
- Reject obvious alternating answer patterns such as `true, false, true, false`.
- Re-shuffle if four or more identical answers appear consecutively.
- Do not use shuffle order to force answer ratio balancing.
- Write the before/after order and answer sequence to the shuffle log.

## Required Shuffle Log

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "shuffle_executed": true,
  "reason": "final output randomization",
  "before_order": [],
  "after_order": [],
  "answer_sequence": [],
  "has_alternating_pattern": false,
  "has_four_or_more_same_answers": false,
  "notes": ""
}
```
