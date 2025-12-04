# Task 03 – Validate end-to-end execution of analysis scripts

## Objective

Ensure that key analysis scripts can be executed from start to finish without errors and in a reasonably short time.

## Steps

- [ ] Choose the main analysis scripts defined in Phase 06 (for example, 01_eda, 02_analysis, 03_sql_vs_pandas).
- [ ] For each one:
  - [ ] Open a fresh terminal (or new container) and run the script via `python -m src.analyses.<name>`.
  - [ ] Check that there are no errors, missing imports, or hanging sections.
  - [ ] Adjust if necessary:
    - File paths.
    - Database connection parameters.
    - Random seeds or filters that could break the flow.
- [ ] Note any special prerequisites you discover so you can document them (for example in the README or a notes file).

## Expected outcome

Analysis Scripts that work end to end and that anyone can run by following the project instructions.
