# Cycle Quality Policy

StudyApp must keep `cycle_02`, `cycle_03`, and `cycle_04` at the same quality level as `cycle_01`.

## Core Rule

Later cycles must not be mass-expanded from a weak template, generic wording pattern, or auto-generated bank.

Every cycle must be built from individually reviewed, source-traceable IR and question items.

## Required Inputs For Each Cycle

Each `{app_id}/{category}/{cycle}` run must have a curated cycle bank at:

`studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`

The cycle bank must contain only items that were reviewed one by one before pipeline execution.

## Forbidden Expansion Patterns

The following are forbidden for production question creation:

- expanding `cycle_02` and later by slicing a generic 100-question bank
- cloning `cycle_01` phrasing with shallow substitutions
- adding generic stems such as `According to the official source, ...` as a shortcut
- using navigation text, table-of-contents text, footer text, or metadata as question content
- using option descriptions without converting them into natural learner-facing English
- using synthetic false questions made only by word flips or random substitutions

## Required Quality For Each Item

Every IR and every question in every cycle must satisfy all of the following:

- reviewed individually
- source checked individually
- source traceable to `source_document_path` or `source_url`
- source section recorded
- statement or question is natural English
- one fact per IR
- one fact per question
- false question is based on a realistic misconception
- explanation directly supports the answer

## Pipeline Rule

`cycle_02` and later must fail fast when a curated cycle bank is missing.

Pipeline Runner must not silently fall back to:

- generic bank slicing
- weak auto-expansion
- placeholder cycle content

## Audit Rule

Question Auditor and Final Reviewer must reject items that show signs of templated low-quality expansion, including:

- obvious metadata leakage
- navigation text in the question body
- unnatural command naming
- generic lead-in text with weak learner value
- false questions that are not plausible misconceptions

## Goal

The goal is not only to reach 800 questions.
The goal is to reach 800 questions with cycle-to-cycle quality consistency.
