# IR Quality Rules

StudyApp uses an IR First pipeline.
This document defines the quality rules for IR creation and IR auditing.

## Core Principle

IR is an intermediate representation, not a question.
IR must be built before question creation.
IR must be reviewed one item at a time.

## IR Creation Rules

- Read `studyapp/input/source_documents/{app_id}/{category}/`.
- Use `studyapp/input/source_documents/{app_id}/{category}/` as the official category-specific source input path.
- Read `studyapp/apps/active_apps/{app_id}/app_config.json`.
- Create one IR for one fact only.
- Use only facts explicitly supported by the source.
- Record `source` and `source_section` for every IR.
- Separate command, option, behavior, limitation, best practice, and warning facts.
- Use `notes` for version dependence, environment dependence, and scope caveats.
- Mark weak or ambiguous items as `confidence=low`.
- Assume `confidence=low` IR will not proceed to question creation.

## IR Audit Rules

- Audit each IR one by one.
- Confirm that `category` matches `app_config.json`.
- Confirm that `source` exists.
- Confirm that `source_section` is specific enough to revisit the evidence.
- Confirm that the source supports the statement.
- Reject IR with multiple facts in one statement.
- Detect duplicates and near-duplicates.
- Reassess `confidence` and `question_potential`.
- Detect outdated, version-dependent, or environment-dependent risk.

## Confidence Guidance

- `high`: direct, clear, explicit source support
- `medium`: supported, but needs caution or conditions
- `low`: weak, incomplete, ambiguous, or unstable support

## Question Potential Guidance

- `high`: important and easy to confuse
- `medium`: useful but less central
- `low`: weak, narrow, trivial, or unstable for question use

## Audit Classification

- `approved`: ready for `question_creator`
- `needs_revision`: fixable but not ready
- `rejected`: should not proceed

## Handoff Rule

Only `approved` IR may be passed to `question_creator`.
Any IR with missing source, vague source section, wrong category, mixed facts, or `confidence=low` must not proceed.

## Mandatory Quality Rule

Every IR and every question must be checked one by one.
Batch-level approval is forbidden.
If any source check is skipped, the agent must report the skipped item and the reason.

## Required Log Record

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
