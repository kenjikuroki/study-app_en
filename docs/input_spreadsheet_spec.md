# Input Spreadsheet Specification

## Purpose

StudyApp will later read the following from spreadsheets:

- app_id
- app_name
- language
- category_id
- category_name
- target_question_count
- source_document_path
- source_url
- difficulty_policy
- notes

## Category Rule

StudyApp should distinguish between:

- `category_id`: machine-safe identifier used in paths, config, and pipeline execution
- `category_name`: human-readable display name used in spreadsheets and UI-facing contexts

Pipeline logic should use `category_id`.
Display text should use `category_name`.

## Source Path Rule

Category source inputs must use:

`studyapp/input/source_documents/{app_id}/{category_id}/`

The spreadsheet should therefore provide a `category_id` that matches the folder name.

## Linux Example

Recommended Linux spreadsheet mapping:

- `category_id=basic_commands`, `category_name=Linux Basics`
- `category_id=filesystem`, `category_name=Filesystem`
- `category_id=permissions`, `category_name=Permissions`
- `category_id=users_groups`, `category_name=Users & Groups`
- `category_id=processes`, `category_name=Processes`
- `category_id=package_management`, `category_name=Package Management`
- `category_id=networking`, `category_name=Networking`
- `category_id=shell_scripting`, `category_name=Shell Scripting`

## Status

This specification is temporary.
Do not implement Spreadsheet Reader yet.

## Future Plan

After the spreadsheet format is finalized, create:

- studyapp/skills/read_spreadsheet/
- studyapp/agents/spreadsheet_reader/

Pipeline Runner will later read spreadsheet data and use it to determine:

- target app
- target category_id
- target category_name
- target question count
- source document location
- output path

## Current Rule

Until the spreadsheet format is finalized,
Pipeline Runner should continue using app_config.json and explicit app_id/category input.

In current StudyApp terminology, that explicit `category` input should be treated as `category_id`.
