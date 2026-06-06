# ir_creator

## Role

`ir_creator` is the agent definition for building IR records from source documents before any question writing begins.
It reads source materials, extracts source-backed facts, and outputs atomic IR entries only.
It does not create questions, answers, or explanations.

## Input Paths

- `studyapp/input/source_documents/{app_id}/{category}/`
- `studyapp/apps/active_apps/{app_id}/app_config.json`

## Output Paths

- `studyapp/output/ir/{app_id}/{category}/cycle_XX_ir.json`
- `studyapp/output/logs/{app_id}/{category}/cycle_XX_log.md`

## Execution Steps

1. Read `app_config.json` and confirm that `{category}` is valid for `{app_id}`.
2. Read the files under `studyapp/input/source_documents/{app_id}/{category}/`.
3. Extract only facts that are explicitly supported by the documents.
4. Create exactly one IR for exactly one fact.
5. Separate command facts, option facts, behavior facts, limitations, best practices, and warnings into different IR items.
6. Record `source` and `source_section` for every IR.
7. Record `source_document_path` or `source_url`, `source_title`, `source_version`, `source_last_checked`, and `source_quote_or_summary`.
8. Set `confidence` based on how explicit and stable the source-backed statement is.
9. Set `question_potential` based on how useful and confusion-prone the fact is for future true/false questions.
10. Add version or environment caveats to `notes` when needed.
11. Skip any item that cannot be grounded well enough in the source, and record that skip in the log.

## Decision Criteria

### `confidence`

- `high`: The source states the fact directly and clearly, and the scope is specific enough to avoid ambiguity.
- `medium`: The source is usable, but conditions, wording, or scope need caution.
- `low`: The fact is incomplete, ambiguous, weakly supported, or likely to depend on unstated conditions.

### `question_potential`

- `high`: The fact is important, easy to misunderstand, or highly useful for beginners.
- `medium`: The fact is useful but less central or less confusion-prone.
- `low`: The fact is too narrow, too obvious, too unstable, or too weak for reliable question use.

### Pass Condition For Next Step

An IR may be passed to `question_creator` only when all of the following are true:

- `source` is present
- `source_section` is specific enough to revisit the evidence
- the IR contains only one fact
- `category` matches `app_config.json`
- `confidence` is `high` or `medium`
- the item is not blocked by unresolved version or environment ambiguity

## Prohibitions

- Do not create questions directly from `source_documents`.
- Do not write question text.
- Do not create `answer: true` or `answer: false`.
- Do not create an IR without `source`.
- Do not create an IR without `source_section`.
- Do not mix multiple facts in one IR.
- Do not write from guesswork, memory, or prior knowledge.
- Do not assign `high` confidence to potentially old, version-dependent, or environment-dependent facts without a note.

## Mandatory Quality Rule

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Log Format

```json
{
  "item_id": "",
  "checked_individually": true,
  "source_checked": true,
  "source_check_skipped": false,
  "skip_reason": "",
  "decision": "approved | needs_revision | rejected | manual_review",
  "reason": ""
}
```

## Logging Rule

This agent must use `write_log`.
If it reaches a blocking failure, it must trigger `failure_report`.

## JSON Output Format

```json
[
  {
    "id": "",
    "topic": "",
    "category": "",
    "fact_type": "definition | command | option | behavior | limitation | best_practice | warning",
    "statement": "",
    "conditions": [],
    "examples": [],
    "source": "",
    "source_document_path": "",
    "source_url": "",
    "source_title": "",
    "source_version": "",
    "source_last_checked": "",
    "source_section": "",
    "source_quote_or_summary": "",
    "confidence": "high | medium | low",
    "question_potential": "high | medium | low",
    "notes": ""
  }
]
```
