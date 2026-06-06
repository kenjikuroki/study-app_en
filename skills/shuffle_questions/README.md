# shuffle_questions

## Skill Purpose

`shuffle_questions` defines the final-order randomization step for StudyApp.
It is executed only once, immediately before `final_questions` output is written.
It changes order only and preserves all traceability fields.

## Input Paths

- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/config/quality_rules.json`
- `studyapp/config/checklist_rules.json`

## Output Paths

- `studyapp/output/final_questions/{app_id}/{category}/cycle_XX_final_questions.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_shuffle_log.json`

## Processing Steps

1. Run only after `Final Reviewer`, `validate_questions`, and final inclusion decisions are complete.
2. Read the approved final question set.
3. Preserve every question record exactly as-is.
4. Shuffle only the array order.
5. Check the post-shuffle answer sequence.
6. Re-shuffle if four or more identical answers appear in a row.
7. Reject mechanical true/false alternation patterns.
8. Write the shuffle log with before/after ID order and answer sequence.

## Quality Gate Usage

- StudyApp does not shuffle during IR creation.
- StudyApp does not shuffle during IR audit.
- StudyApp does not shuffle during question creation.
- StudyApp does not shuffle during question audit.
- StudyApp does not shuffle during revision creation.
- StudyApp does not shuffle before final review is complete.

## Shuffle Rules

- Execute only once, immediately before final output.
- Do not change `question_id`.
- Do not change `source_ir_id`.
- Do not change `category`.
- Do not change `question`, `answer`, `explanation`, or `source`.
- Change order only.
- Do not force alternating true/false placement.
- Do not allow an obvious `true, false, true, false` pattern.
- Re-shuffle when four or more identical answers appear in a row.
- Evaluate answer ratio at category level, not by forced local ordering.
- Keep valid JSON structure after shuffling.

## Traceability Rule

StudyApp does not perform intermediate shuffling.
During audit and revision, creation order and ID linkage must stay stable.
Shuffling happens only once right before `final_questions` output.
Even after shuffling, `question_id` and `source_ir_id` must remain unchanged.

## Prohibitions

- Do not shuffle immediately after question creation.
- Do not shuffle before question audit.
- Do not shuffle before revision.
- Do not shuffle before final review.
- Do not alternate true/false mechanically.
- Do not reassign `question_id`.
- Do not break `source_ir_id` linkage.

## Shuffle Log Format

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
