## Task 02 – Create Data Quality Check Script

### Objective

Build a script that runs **automated data quality checks** on your cleaned data and reports any issues.

### Outputs

- A script such as `src/check_data_quality.py` that prints a small report and optionally returns a non-zero exit code on failure.

### Steps

1. **Decide on data source for checks**

   - Choose whether to run checks against:
     - The cleaned CSV in `data/derived/books_clean.csv`.
     - The `books_clean` table in PostgreSQL.

2. **Define key checks**

   - Examples:
     - Row count above a minimum threshold.
     - No nulls in critical columns (e.g., `average_rating`, `ratings_count`, `num_pages`).
     - Values within expected ranges (ratings 0–5, positive counts/pages).
     - Optional: basic distribution checks (e.g., mean rating within a plausible range).

3. **Implement script**

   - Load data (CSV or via SQL query).
   - Run each check and accumulate results (pass/fail, notes).
   - Print a summary report to the console.

4. **Return exit codes (optional but recommended)**

   - If any critical check fails, exit with a non-zero status code.
   - This enables integration with future CI pipelines.

5. **Document how to run the script**
   - Add instructions to `README.md` or `docs/data-quality.md` (e.g., `python -m src.check_data_quality`).

### Checklist

- [ ] Data source for checks chosen (CSV and/or DB).
- [ ] List of key checks defined.
- [ ] `src/check_data_quality.py` implemented.
- [ ] Script prints a clear summary report.
- [ ] Exit code behavior defined and documented.
