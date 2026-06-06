# Question Quality Rules

StudyApp creates English true/false questions from audited IR only.
This document defines the quality rules for question creation and question auditing.

## Good Question Conditions

- based on approved IR only
- has `source`
- has `source_ir_id`
- contains one fact only
- uses natural English
- is clear and not ambiguous
- has a correct true/false answer
- has a short explanation that matches the IR

## Bad Question Conditions

- derived from non-approved IR
- missing `source`
- missing `source_ir_id`
- mixes multiple facts
- uses awkward or unclear English
- has an incorrect answer
- has an explanation that does not match the IR
- cannot be traced back reliably

## Good False Question Conditions

- based on realistic beginner confusion
- based on similar concepts, similar commands, missing conditions, or mistaken purpose
- can be disproved by the source-backed IR
- sounds natural in English
- still tests a meaningful misunderstanding

## Bad False Question Conditions

- random opposite-word swapping
- obviously absurd claims
- unnatural English
- weak relation to the source-backed IR
- cannot be verified against the source

## Why Questions Must Be Audited One by One

Each question can fail in a different way.
Traceability, correctness, explanation quality, and ambiguity cannot be trusted from batch-level review.
One-by-one review is required to prove that every question was checked.

## Why Quality Gate Must Always Be Used

The Quality Gate prevents silent batch approval.
It enforces individual review, source checking, source IR checking, and skip-reason recording.
Without the Quality Gate, StudyApp cannot prove that quality was prioritized over speed.

## Shuffle Policy

StudyApp does not shuffle questions during creation, audit, or revision.
Creation order and ID linkage stay stable until final output preparation.
Shuffling happens once only, immediately before `final_questions` output.
Even after shuffling, `question_id` and `source_ir_id` must remain unchanged.
