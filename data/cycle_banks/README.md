# Cycle Banks

This directory stores curated per-cycle production inputs for Pipeline Runner.

Required path:

`studyapp/data/cycle_banks/{app_id}/{category}/{cycle}.json`

Rules:

- `cycle_02` and later must use curated cycle banks.
- Each cycle bank must contain only individually reviewed IR and question items.
- Generic 100-question bank slicing is not allowed for production later cycles.
