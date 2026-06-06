# Question Pipeline

StudyApp is an IR First question creation system.

## Flow

source_documents
IR creation
IR audit
question creation
question audit
revision creation
final review
approved questions collected
validate_questions
shuffle_questions
final_questions JSON

## Shuffle Rule

StudyApp does not shuffle during intermediate stages.
No shuffle is allowed in:

- IR creation
- IR audit
- question creation
- question audit
- revision creation
- any step before final review is complete

Shuffling is executed once only, immediately before `final_questions` output.
This preserves `question_id` and `source_ir_id` traceability during audit and revision.

## Source Input Path

IR Creator and Pipeline Runner must read:

`studyapp/input/source_documents/{app_id}/{category}/`

## Batch Cycle

Each category targets 100 questions.
Questions are created in 4 cycles:

- cycle_01: 30 questions
- cycle_02: 30 questions
- cycle_03: 30 questions
- cycle_04: 10 questions

## Important Rule

Agents and skills created in this task are templates and definitions only.
Do not generate actual Linux, Git, Docker, Kubernetes, or AWS questions in this task.
