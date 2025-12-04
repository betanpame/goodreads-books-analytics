# Phase 02 - Step 03 - Task 01 - Prepare Books Table & ETL Requirements

This document kicks off **Phase 02 → Step 03 → Task 01**. The plan directions say to ensure PostgreSQL is ready to receive data, but per our latest scope we are also translating the normalization ideas from Step 02 into concrete ETL requirements—especially around splitting multi-author strings. Follow the steps below to prep your environment, reproduce the profiling results, and understand what needs to be built before we run the first full load.

---

## 1. Task definition and goal

Source: `plan/phase-02-data-loading-and-initial-exploration/steps/step-03-load-data-into-postgres/tasks/task-01-prepare-books-table-in-postgres.md`

Deliverables:

1. Verify the Postgres container is running and the `books` table defined in `sql/create_books_table.sql` exists.
2. Produce an ETL-ready requirements list covering column-by-column transformations and the future bridge tables described in Task 03 of Step 02.
3. Document the author-splitting algorithm so the loading script can stage both the denormalized `books` table and the normalized artifacts when we are ready.

---

## 2. Reproduce the container + schema state

Run these commands from the repo root (`C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics`). They keep Postgres available and confirm the table is present.

```powershell
# Start/ensure services
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d postgres

# Run the DDL (safe because the script uses IF NOT EXISTS)
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml cp sql/create_books_table.sql postgres:/tmp/create_books_table.sql

docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres psql -U goodreads_user -d goodreads -f /tmp/create_books_table.sql

# Double-check
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres psql -U goodreads_user -d goodreads -c "\d books"

# Optional cleanup
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres rm /tmp/create_books_table.sql
```

Expected: `CREATE TABLE` plus `NOTICE: relation "books" already exists, skipping` if you have run it before.

---

## 3. How to profile the authors column (required for ETL rules)

We need hard numbers on author delimiters so our ETL script can parse them deterministically. Run the following once your virtual environment is active (`.\.venv\Scripts\activate`).

```powershell
@'
import pandas as pd
from pathlib import Path
from collections import Counter
from pprint import pprint

root = Path('.')
df = pd.read_csv(root / 'data' / 'books.csv', on_bad_lines='skip', engine='python')

summary = {}
summary['row_count'] = len(df)
summary['null_authors'] = int(df['authors'].isna().sum())
summary['unique_author_strings'] = df['authors'].nunique(dropna=True)

multi_author_flag = df['authors'].str.contains('/', na=False)
summary['multi_author_rows'] = int(multi_author_flag.sum())

# Delimiter inspection
counter = Counter()
for value in df['authors'].dropna():
    if ' / ' in value or '/' in value:
        counter['/'] += 1
    elif ' and ' in value:
        counter['and'] += 1
    elif ';' in value:
        counter[';'] += 1

summary['delimiter_counts'] = dict(counter)

# Sample multi-author strings
examples = df[multi_author_flag]['authors'].head(3).tolist()
summary['samples'] = examples

pprint(summary)
'@ | Set-Content tmp_author_scan.py

python tmp_author_scan.py
Remove-Item tmp_author_scan.py
```

> 🛈 Keep `on_bad_lines='skip'` because line 3350 in `books.csv` has 13 columns and otherwise breaks the quick scan. We will record those row numbers for the ETL later.

---

## 4. Key observations from profiling (4 Dec 2025)

- **11,119 rows** after skipping malformed records.
- **0 null author strings** and **6,635 distinct author strings**.
- **4,561 rows** contain multiple authors; **avg 1.73 authors/book**, **max 51**.
- **Delimiter distribution**: `"/"` appears in 4,560 rows, the literal word `"and"` appears once, other separators (comma, semicolon, ampersand) are negligible but still need guards.
- Sample multi-author strings to test against:
  1. `J.K. Rowling/Mary GrandPré`
  2. `Roald Dahl/Artists and Writers Guild/Walt Disney Company/Leonard Maltin`
  3. `Denny Caringer/Better Homes and Gardens`

These stats tell us a simple slash-based splitter covers >99.9% of cases, but we must also normalize `" and "`, `" & "`, `";"`, `"|"`, and `"+"` just in case.

---

## 5. ETL requirements checklist

| Stage                | Requirement                                                                                                                                                                                                        | Notes                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Ingest               | Read `data/books.csv` with `on_bad_lines='skip'` and log skipped row numbers.                                                                                                                                      | Pandas `read_csv(..., on_bad_lines='skip', engine='python')` is sufficient.   |
| Column rename        | Map raw headers to SQL names (`bookID → book_id`, `"  num_pages" → num_pages`, etc.).                                                                                                                              | Keep a dictionary in `src/cleaning.py` so notebooks and scripts share it.     |
| Type casting         | Cast numeric fields (`book_id`, `average_rating`, `num_pages`, `ratings_count`, `text_reviews_count`) to the types defined in `sql/create_books_table.sql`.                                                        | Fail fast if coercion introduces NaNs.                                        |
| Date parsing         | Convert `publication_date` (string like `"9/1/98"`) to ISO `YYYY-MM-DD` using `pd.to_datetime(..., errors='coerce')`.                                                                                              | We will later decide how to handle null dates.                                |
| Author normalization | Trim whitespace, collapse repeated spaces, and preserve the original raw string in a `raw_authors` column for auditing.                                                                                            | This raw copy will help reconcile future bridge tables.                       |
| Author splitting     | Expand slash-delimited strings into ordered lists and emit two artifacts: (a) aggregated JSON/list column inside `books` for now, (b) a staging DataFrame with `book_id`, `author_order`, `author_name`.           | Details in Section 6.                                                         |
| Loading              | Use `src/load_books_to_postgres.py` to write the cleaned `books` DataFrame via SQLAlchemy with `if_exists="replace"`, then bulk load the `book_authors` staging set into a temporary table (`book_authors_stage`). | This keeps Task 02 straightforward while laying groundwork for normalization. |
| Validation           | Compare pandas row counts vs. `SELECT COUNT(*) FROM books;` and ensure `book_id` stays unique before committing.                                                                                                   | Adds guardrails for Task 03 in this phase.                                    |

---

## 6. Author-splitting specification

1. **Tokenizer**

   - Normalize separators: `text.replace(' and ', '/').replace(' & ', '/').replace(';', '/').replace('|', '/').replace('+', '/')`.
   - Split on `'/'`, trim each token, drop empties, and de-duplicate while preserving order (use `dict.fromkeys`).

2. **Output schema**

   - `book_id INTEGER NOT NULL`
   - `author_order SMALLINT NOT NULL` (1-based index)
   - `author_name TEXT NOT NULL`
   - `raw_authors TEXT` (original string for traceability)

3. **Python helper sketch**

```python
def explode_authors(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        authors = row['authors_clean']  # already normalized string
        if not authors:
            continue
        normalized = (
            authors.replace(' and ', '/')
            .replace(' & ', '/')
            .replace(';', '/')
            .replace('|', '/')
            .replace('+', '/')
        )
        tokens = [token.strip() for token in normalized.split('/') if token.strip()]
        deduped = list(dict.fromkeys(tokens))
        for idx, token in enumerate(deduped, start=1):
            rows.append(
                {
                    'book_id': row['book_id'],
                    'author_order': idx,
                    'author_name': token,
                    'raw_authors': row['authors_raw'],
                }
            )
    return pd.DataFrame(rows)
```

4. **Acceptance criteria**
   - Stage table row count must equal the sum of per-book author counts (≈ 19,200 rows given current stats).
   - `author_order` restarts at 1 per `book_id` and increments by 1.
   - Special characters (e.g., accented names, apostrophes) survive unchanged.

---

## 7. Implementation plan for repo scripts

- `src/load_books_to_postgres.py`

  1. Read CSV with `on_bad_lines='skip'` and capture skipped line numbers via a custom callback.
  2. Call a soon-to-be-updated `clean_books` helper that performs renames, type casting, and date parsing.
  3. Persist the cleaned DataFrame to `books` (use `if_exists='replace'`).
  4. Call `explode_authors` and write the result to a staging table (`book_authors_stage`).
  5. Optionally, `DROP TABLE book_authors_stage` at the end if we only need the data during Task 02 prototyping.

- `src/cleaning.py`

  - Add pure functions: `rename_columns(df)`, `cast_numeric(df)`, `parse_publication_date(df)`, `normalize_authors_string(df)`.
  - Ensure every function returns a DataFrame so the cleaning pipeline composes cleanly.

- Tests (`tests/test_cleaning.py`)
  - Add unit tests for the new helper functions, covering edge cases like repeated `'//'`, trailing separators, and names that already contain `/` legitimately.

---

## 8. Validation and monitoring steps

1. After loading, run `SELECT COUNT(*) FROM books;` and compare with `len(df_clean)`.
2. Run `SELECT COUNT(*) FROM book_authors_stage WHERE author_order = 1;` to ensure every book with authors has at least one entry.
3. Spot-check a handful of records:
   - `SELECT book_id, authors FROM books WHERE authors LIKE '%/%' LIMIT 5;`
   - `SELECT * FROM book_authors_stage WHERE book_id = <id>`
4. Keep a log file (e.g., `logs/load_books_<timestamp>.log`) capturing warnings for malformed rows and serialization errors.

---

## 9. Checklist review

- [x] PostgreSQL container is confirmed running and `books` exists.
- [x] Profiling output and author delimiter stats are documented for repeatability.
- [x] ETL + author-splitting requirements are specified for implementation in `src/load_books_to_postgres.py`.

---

## 10. Q&A / Troubleshooting

**Q: What happens to the row we skip because of malformed columns?**  
Record the `line_number` from pandas' `warn_bad_lines`-style hook (or simply note that `len(raw_df) - len(df_clean)` equals the number of skipped rows) and store it in a small CSV for future cleanup.

**Q: Do we need to create the normalized tables now?**  
Not yet. We only load into `books` plus a staging bridge. Once Task 02 finishes smoothly, we can promote the staging table into real `authors`/`book_authors` tables via migrations.

**Q: Should we deduplicate authors during splitting?**  
Yes—use `dict.fromkeys(tokens)` so if an author is repeated twice in the same slash-separated string we only keep the first occurrence.

**Q: How do we keep the process repeatable?**  
Parameterize `src/load_books_to_postgres.py` (already accepts `--csv-path`, `--table`, `--if-exists`) and ensure cleaning functions are deterministic. Store any hard-coded paths (like logs) under `data/processed/` so they can be version-controlled if needed.

---

## 11. Next actions

1. Update `src/cleaning.py` with the column-transform + author-normalization helpers described above.
2. Extend `src/load_books_to_postgres.py` to call the cleaning helpers and write both `books` and `book_authors_stage`.
3. Add pytest cases exercising the author-splitting edge cases (slashes, "and", repeated names) before attempting the full load in Task 02.
