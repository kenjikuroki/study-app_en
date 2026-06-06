# Failure Report Prompt

Use this skill when a blocking StudyApp failure stops the pipeline.

## Mandatory Rules

- write a failure report whenever the pipeline stops on failure
- include the failed step
- include a non-empty `failure_reason`
- include completed and skipped step lists
- include a concrete `next_action`
- set `manual_review_required=true`

## Required Output Shape

```json
{
  "app_id": "",
  "category": "",
  "cycle": "",
  "failed_step": "",
  "failure_reason": "",
  "completed_steps": [],
  "skipped_steps": [],
  "next_action": "",
  "manual_review_required": true
}
```
