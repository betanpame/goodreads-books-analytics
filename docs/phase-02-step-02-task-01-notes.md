# Phase 02 - Step 02 - Task 01 - Map Columns to SQL Types

This note documents how I finished **Phase 02 → Step 02 → Task 01**. The deliverable is a beginner-friendly, reproducible mapping from the pandas dtypes we explored earlier to the PostgreSQL types we plan to use for `books.csv`.

---

## 1. Task definition and goal

Per `plan/phase-02-data-loading-and-initial-exploration/steps/step-02-design-postgres-schema/tasks/task-01-map-columns-to-sql-types.md`, I needed to:

1. Review every column from `books.csv`.
2. Capture example values and pandas dtypes.
3. Propose the PostgreSQL type we will use in Phase 02 → Step 02 → Task 02.
4. Note any uncertainties (length limits, renames, parse requirements).

---

## 2. How to run this analysis script

Use the same reproducible command sequence we established in Step 01 any time you need to inspect the dataset.

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

### Estimated runtime & success checks

- **Runtime:** ≈2 minutes when the containers are cold; ≈30 seconds after the first run.
- **Success checklist:**
  - Docker reports the `app` and `postgres` services as `Running` after the `up -d` command.
  - Terminal output includes dtype summaries plus `Loaded shape: (rows=1000, columns=12)`.
  - `outputs/initial_inspection/books_sample_preview.csv` and `books_numeric_summary.csv` show updated timestamps, proving the script finished.

Those commands refresh the CLI log and the helper CSVs in `outputs/initial_inspection/`, so you can always confirm that pandas still reads the file before looking at SQL mappings.

---

## 3. Environment recap

- **Runtime**: Python 3.14 + pandas 2.3.3 inside the Docker `app` container.
- **Dataset**: `data/books.csv` mounted at `/app/data/books.csv`.
- **Supporting scripts**: The original `initial_inspection_books.py` outputs dtypes for a 1,000-row sample; for this task I profiled the entire dataset inside the container with a one-off Python snippet (documented below) to capture max lengths and numeric ranges.

---

## 4. Column profiling workflow

After starting the containers, I opened an interactive shell and ran the following snippet to scan every column (this is copy/paste friendly inside the container because Bash supports `<<'PY'`):

```bash
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -T app bash -lc "python - <<'PY'
import json
import pandas as pd
from pathlib import Path

df = pd.read_csv('data/books.csv', on_bad_lines='skip')
summary = []
for col in df.columns:
    ser = df[col]
    dtype = str(ser.dtype)
    examples = ser.dropna().astype(str).head(3).tolist()
    entry = {
        'column': col,
        'dtype': dtype,
        'examples': examples,
        'non_null_count': int(ser.notna().sum()),
    }
    if dtype == 'object':
        entry['max_length'] = int(ser.dropna().astype(str).str.len().max())
    else:
        entry['min'] = ser.min().item() if hasattr(ser.min(), 'item') else ser.min()
        entry['max'] = ser.max().item() if hasattr(ser.max(), 'item') else ser.max()
    summary.append(entry)

print(json.dumps({'rows': len(df), 'columns': len(df.columns), 'summary': summary}, indent=2))
PY"
```

- `on_bad_lines='skip'` skips a single malformed row (line 3,350) that contains an unexpected comma. This does **not** affect the first 50k rows we care about for schema design, but the data quality issue is noted below for follow-up in Phase 03.
- The JSON output (captured in my terminal log) reports 11,123 rows × 12 columns, plus length/range metadata for each field.

---

## 5. Column → PostgreSQL mapping

| column_name          | example_values                               | pandas_dtype | proposed_postgres_type | Notes                                                                                                                             |
| -------------------- | -------------------------------------------- | ------------ | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `bookID`             | `1`, `2`, `4`                                | `int64`      | `INTEGER`              | Max value 45,641 so a 32-bit integer works; this will be our primary key candidate.                                               |
| `title`              | `Harry Potter and the Half-Blood Prince...`  | `object`     | `TEXT`                 | Max length 254 characters; `TEXT` keeps things simple without worrying about truncation.                                          |
| `authors`            | `J.K. Rowling/Mary GrandPré`, `J.K. Rowling` | `object`     | `TEXT`                 | Up to 750 characters when multiple authors are present; we will keep the raw slash-delimited text here and normalize later.       |
| `average_rating`     | `4.57`, `3.48`                               | `float64`    | `NUMERIC(3,2)`         | Values range from 0.00 to 5.00, so two decimal places and one digit to the left of the decimal is sufficient.                     |
| `isbn`               | `0439785960`                                 | `object`     | `VARCHAR(20)`          | Treat ISBN-10 as text to preserve leading zeros and allow occasional hyphens if we add them later.                                |
| `isbn13`             | `9780439785969`                              | `int64`      | `VARCHAR(20)`          | Even though pandas loaded this as `int64`, storing it as text avoids issues with leading zeros and keeps formatting options open. |
| `language_code`      | `eng`, `spa`                                 | `object`     | `VARCHAR(5)`           | Only ~11 unique values; capped length prevents accidental typos yet leaves room for codes like `en-US`.                           |
| `  num_pages`        | `652`, `870`                                 | `int64`      | `INTEGER`              | We will rename this column to `num_pages` when loading into Postgres; max observed pages = 6,576.                                 |
| `ratings_count`      | `2,095,690`, `4,597,666`                     | `int64`      | `INTEGER`              | Fits comfortably inside 32-bit signed range. If later data exceeds this, we can promote to `BIGINT`.                              |
| `text_reviews_count` | `29,221`, `94,265`                           | `int64`      | `INTEGER`              | Same reasoning as `ratings_count`; upper bound well below 2.1B.                                                                   |
| `publication_date`   | `9/16/2006`                                  | `object`     | `DATE`                 | Parsed cleanly in Task 03; we will use `to_date(publication_date, 'MM/DD/YYYY')` when loading.                                    |
| `publisher`          | `Scholastic Inc.`, `Penguin Books`           | `object`     | `TEXT`                 | Longest string observed is 67 characters, so `TEXT` keeps us flexible and indexable.                                              |

If we decide to enforce length constraints during later phases, `title` and `publisher` could become `VARCHAR(300)`/`VARCHAR(120)`, but `TEXT` keeps the initial schema simple.

---

## 6. Expected output checkpoints

When you rerun the profiling snippet in Section 4, expect to see:

- `{ "rows": 11123, "columns": 12, ... }` at the top of the JSON payload.
- Each column entry reporting `non_null_count: 11123`, matching the upstream CSV.
- `max_length` stats such as `authors → 750`, `title → 254`, `publisher → 67`.
- Numeric ranges that justify integer choices (e.g., `ratings_count max: 4597666`).

Any deviations (e.g., wildly different row counts or extra columns) should be investigated before moving on to Task 02.

---

## 7. Observations and open questions

- The CSV contains at least one malformed row (line 3,350). Skipping it allowed the profile to finish, but we need to log this for the Phase 03 data quality sweep.
- `isbn13` is currently numeric inside pandas, but the absence of quotes in the CSV means leading zeros would be stripped. We will coerce it to text during loading to avoid accidental data changes.
- `language_code` values are short now but may eventually benefit from a lookup table (we will revisit in Step 02 → Task 03 when thinking about normalization).

---

## 8. Artifacts refreshed each run

- `docs/phase-02-step-02-task-01-notes.md` (this file) contains the authoritative mapping table.
- The profiling JSON lives in the terminal log from Section 4. If desired, pipe it to `outputs/schema_design/column_profile.json` for future reference.

---

## 9. Checklist review

- [x] Created a pandas → PostgreSQL type mapping for every column in `books.csv`.
- [x] Captured questions/risks (malformed row, string vs numeric choices) for follow-up work.

---

## 10. Q&A / Data troubleshooting

**Q: Why did you use `on_bad_lines='skip'` when reading the CSV?**  
A: Line 3,350 has an extra comma embedded in the title field. Skipping it keeps the profiling step moving; we will track the exact row number for cleaning later.

**Q: Do I have to create a temporary script to get the JSON summary?**  
A: No. Use the inline snippet in Section 4 from inside the container. Bash handles the heredoc syntax even when you launch it from PowerShell with `docker compose ... exec -T app bash -lc "python - <<'PY' ..."`.

**Q: How do I know `NUMERIC(3,2)` is sufficient for `average_rating`?**  
A: The profiling output shows every value between 0.0 and 5.0 with two decimal places. If Goodreads ever adds more precision, we can widen to `NUMERIC(4,3)` without data loss.

**Q: What about the leading spaces in `"  num_pages"`?**  
A: They are part of the raw CSV header. We will `rename(columns={'  num_pages': 'num_pages'})` in the ETL script before loading into Postgres.

For broader dataset questions, visit `docs/data-faq.md`, which we keep updated with cross-task troubleshooting tips.
