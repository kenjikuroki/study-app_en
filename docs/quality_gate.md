# Quality Gate

StudyApp uses a shared Quality Gate across all pipeline stages.

## Purpose

The Quality Gate exists to prove that each item was reviewed individually.
Quality has priority over speed.
More time is acceptable.
More token use is acceptable.

## Covered Stages

- IR creation
- IR audit
- question creation
- question audit
- revision
- final review

## Core Rule

Every IR, every question, and every revision must be checked one by one.
Batch-level approval is forbidden.
If an item cannot be checked, the reason must be recorded.

## Forbidden Actions

- batch approval
- sample review
- random spot-check review
- approval without source check
- approval without source_ir_id check
- "the set looks fine" style approval

## Required IR Checks

- source check
- source_section check
- statement check
- category check

## Required Question Checks

- source_ir_id check
- answer check
- explanation check
- source check
- category check

## Required Revision Checks

- original IR check
- original question check
- revision evidence check

## Required Log Format

```json
{
  "item_id": "",
  "reviewed_individually": true,
  "source_checked": true,
  "source_ir_checked": true,
  "approved": true,
  "skip_reason": "",
  "review_notes": ""
}
```

## Auto-Reject Rule

If `reviewed_individually=false`, the item must be treated as `rejected`.

If a review step is skipped, a reason must be recorded.
Missing skip reasons are forbidden.

## Shared Design Rule

All future agents must call this Quality Gate before approving IR, questions, revisions, or final outputs.
All future agents must also use `write_log` for per-item traceability.
Blocking failures must emit `failure_report`.

## Shuffle Restriction

StudyApp does not allow intermediate shuffling.
No shuffle is allowed during IR creation, IR audit, question creation, question audit, revision creation, or pre-final-review handling.
Shuffling is allowed once only, right before `final_questions` output after final review and validation are complete.
This rule exists to preserve `question_id` and `source_ir_id` traceability.

## Logging Restriction

No item may be approved without a log.
No skipped item may omit `skip_reason`.
No failed item may omit `failure_reason`.
