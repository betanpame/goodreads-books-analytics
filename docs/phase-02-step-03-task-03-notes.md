# Phase 02 – Step 03 – Task 03 – Verify Row Counts and Samples

This task validates that the records written by `src.load_books_to_postgres` actually landed inside PostgreSQL and match the pandas-side expectations.

---

## 1. Task definition and goal

Planning reference: `plan/phase-02-data-loading-and-initial-exploration/steps/step-03-load-data-into-postgres/tasks/task-03-verify-row-counts-and-samples.md`.

Required evidence:

1. Compare the row count emitted by the loader (pandas) with the count stored in the `books` table.
2. Confirm the author staging table (`book_authors_stage`) contains the expected number of exploded author rows.
3. Manually inspect a few records to ensure key columns (titles, authors, publication_date) survived the trip to SQL without formatting issues.

---

## 2. Commands to reproduce the checks

All commands run from the project root.

### Command block (copy/paste)

```powershell
# Launch services if needed
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d

# Row counts
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
    psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) AS books_rows FROM books;"

docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
    psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) AS author_stage_rows FROM book_authors_stage;"

# Optional samples
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
    bash -lc "PGOPTIONS='--pset=pager=off' psql -U goodreads_user -d goodreads \
        -c \"SELECT book_id, title, authors, publication_date FROM books ORDER BY book_id LIMIT 5;\""
```

### Estimated runtime & success checks

- **Runtime:** ≈2 minutes (service check plus two row-count queries; add ~30 seconds if you include the sample query).
- **Success checklist:**
  - `books_rows` result equals the pandas count from the loader log (currently 11,119) and `author_stage_rows` equals ~19k.
  - Sample query returns readable titles with normalized author strings and ISO dates—matching the pandas `head()` output.
  - Using `PGOPTIONS='--pset=pager=off'` suppresses the pager, so results print immediately; if you still see `--More--`, re-run with the flag applied.

(Use the same `PGOPTIONS` trick for any additional sample queries to avoid the default pager.)

---

## 3. Results (Dec 4, 2025)

### 3.1 Row counts

| Source                           |   Rows |
| -------------------------------- | -----: |
| pandas / loader log (`df_clean`) | 11,119 |
| PostgreSQL `books`               | 11,119 |
| PostgreSQL `book_authors_stage`  | 19,202 |

Observations:

- `books` rows exactly match the cleaned pandas count, so no records were lost between pandas and SQL.
- `book_authors_stage` contains ~1.73 rows per book (19,202 ÷ 11,119), which matches the earlier profiling that showed roughly half the titles have multiple authors.

### 3.2 Sample queries

A quick look at the first few rows confirms that titles, normalized author strings, and parsed dates all survived the load:

```
 book_id | title                                             | authors                         | publication_date
---------+---------------------------------------------------+--------------------------------+-----------------
       1 | Harry Potter and the Half-Blood Prince ...        | J.K. Rowling / Mary GrandPré   | 2006-09-16
       2 | Harry Potter and the Order of the Phoenix ...     | J.K. Rowling / Mary GrandPré   | 2004-09-01
       4 | Harry Potter and the Chamber of Secrets ...       | J.K. Rowling                   | 2003-11-01
       5 | Harry Potter and the Prisoner of Azkaban ...      | J.K. Rowling / Mary GrandPré   | 2004-05-01
       8 | Harry Potter Boxed Set Books 1-5 ...              | J.K. Rowling / Mary GrandPré   | 2004-09-13
```

These rows line up with the `head()` output from the pandas exploration script, indicating that no unexpected trimming or encoding issues occurred.

For the staging table:

```
 book_id | author_order | author_name
---------+--------------+--------------------
       1 |            1 | J.K. Rowling
       1 |            2 | Mary GrandPré
       2 |            1 | J.K. Rowling
       2 |            2 | Mary GrandPré
       4 |            1 | J.K. Rowling
       5 |            1 | J.K. Rowling
       5 |            2 | Mary GrandPré
       8 |            1 | J.K. Rowling
       8 |            2 | Mary GrandPré
```

The `author_order` column resets per book, confirming that the explode logic preserved ordering.

### 3.3 Malformed rows

Four rows were excluded during the load, all recorded in `logs/load_books_bad_lines_20251204_222632.log`. Keeping the log file allows Phase 03 to either fix the input dataset or continue treating these rows as known exceptions.

---

## 4. Checklist review

- [x] Row counts between pandas and PostgreSQL match.
- [x] Queried both `books` and `book_authors_stage` to confirm expected volumes.
- [x] Manually inspected sample rows to verify author parsing and date normalization.
- [x] Logged discrepancies (the four malformed CSV lines) for future data quality work.

With these validations captured, Phase 02 is complete: data is loaded into Postgres, and we have hard evidence that the transfer preserved record counts and key fields.
