## Task 02 – Verify Row Counts and Basic Statistics

### Objective

Confirm that the data in PostgreSQL matches the source CSV / pandas DataFrame in terms of **row counts** and a few basic **aggregations**.

### Inputs

- `books.csv` file and/or pandas EDA notebook from previous phases.
- `books` table in PostgreSQL.

### Outputs / Deliverables

- A small markdown table comparing row count and key aggregates between CSV/pandas and PostgreSQL.
- Confidence that there were no major issues during the load.

### Suggested Steps

1. **Get reference numbers from pandas or CSV**

   - In a notebook, compute:
     - `n_rows_csv = len(df_raw)`
     - `avg_rating_csv = df_raw["average_rating"].mean()`
     - `min_pub_date_csv`, `max_pub_date_csv` if dates are parsed.
   - Note these values in a markdown cell.

2. **Compute the same metrics in PostgreSQL**

   - In your SQL client, run queries like:
     - `SELECT COUNT(*) FROM books;`
     - `SELECT AVG(average_rating) FROM books;`
     - `SELECT MIN(publication_date), MAX(publication_date) FROM books;`
   - Record the results.

3. **Compare results**

   - Create a simple comparison table (markdown is fine), for example:
     - Metric | Source (pandas/CSV) | PostgreSQL
     - Row count | ... | ...
     - Avg rating | ... | ...

4. **Investigate discrepancies (if any)**

   - If counts or averages differ significantly:
     - Check for filtered rows during load.
     - Check data types in PostgreSQL (e.g., numeric vs text).
     - Look for rows with missing/invalid values that may have been dropped.

5. **Document conclusions**
   - Add a short note summarizing whether the PostgreSQL data is consistent with the source.
   - If you accept small differences (e.g., due to rounding), explain why.

### Checklist

- [ ] Reference metrics computed in pandas or from CSV.
- [ ] Equivalent metrics computed in PostgreSQL.
- [ ] Comparison table created.
- [ ] Any discrepancies investigated and documented.
- [ ] Overall conclusion about data validity in PostgreSQL written.
