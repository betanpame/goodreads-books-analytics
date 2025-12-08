# Phase 02 – Step 03 – Task 02 – Load Data from CSV to PostgreSQL

This note records the end-to-end run that loads `data/books.csv` into PostgreSQL using the Python-based ETL implemented in `src/load_books_to_postgres.py`.

---

## 1. Task definition and goal

Planning reference: `plan/phase-02-data-loading-and-initial-exploration/steps/step-03-load-data-into-postgres/tasks/task-02-load-data-from-csv-to-postgres.md`.

Deliverables confirmed in this run:

- Choose and document the loading approach (Python + pandas + SQLAlchemy).
- Execute the loader so the `books` table inside Postgres is fully populated.
- Capture evidence (logs, artifacts) that proves the process succeeded and is repeatable.

---

docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app \

## 2. How to run the loader

All commands execute from the project root: `C:\Users\shady\documents\GITHUB\goodreads-books-analytics`.

### Command block (copy/paste)

```powershell
# 1) Ensure both the Python CLI and Postgres services are online
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d

# 2) Run the ETL inside the Python container
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app \
        python -m src.load_books_to_postgres --csv-path data/books.csv --table books --if-exists replace
```

### Estimated runtime & success checks

- **Runtime:** ≈4–5 minutes for a full reload (containers spin up in ~1 minute, pandas load/clean/write takes ~3 minutes).
- **Success checklist:**
  - `docker compose ... up -d` reports both services as healthy.
  - Loader logs include lines for skipped malformed rows, row counts (`Loaded 11119 rows ...`, `Writing 19202 author rows ...`), and `Load finished successfully.`
  - `logs/load_books_bad_lines_<timestamp>.log` exists when rows are skipped, confirming error handling ran.

Environment notes:

- `DATABASE_URL` is sourced via `src/db_config.py`, so the loader automatically targets the Postgres container defined in `docker-compose.postgresql.yml`.
- The default options (`--table books`, `--if-exists replace`) are sufficient for rerunnable development loads.

---

## 3. Loader behavior (Dec 4, 2025 run)

Key log lines from the most recent execution:

```
2025-12-04 22:26:32 INFO  __main__  Reading CSV from data/books.csv
2025-12-04 22:26:32 WARN  __main__  Skipped 4 malformed rows. Details recorded in logs/load_books_bad_lines_20251204_222632.log
2025-12-04 22:26:32 INFO  __main__  Loaded 11119 rows after skipping 4 malformed entries
2025-12-04 22:26:32 INFO  __main__  Writing 11119 cleaned rows to table books
2025-12-04 22:26:33 INFO  __main__  Writing 19202 author rows to staging table book_authors_stage
2025-12-04 22:26:33 INFO  __main__  Load finished successfully.
```

What happens under the hood:

1. `read_books_csv()` ingests the raw file with `on_bad_lines` hooked to a custom logger so any problematic lines are recorded instead of crashing the job.
2. `clean_books()` applies the full pipeline from `src/cleaning.py` (column renames, ISBN normalization, numeric casting with validation, date parsing, and author normalization).
3. `explode_authors()` derives the `book_authors_stage` DataFrame so multi-author strings are preserved in a long format for future normalization work.
4. Both DataFrames are written through a single SQLAlchemy transaction, guaranteeing that the staging table and the `books` table stay in sync.

---

## 4. Malformed row log

Skipped rows are captured in `logs/load_books_bad_lines_20251204_222632.log`. Example (first entry):

```
12224,Streetcar Suburbs: The Process of Growth in Boston  1870-1900,Sam Bass Warner, Jr./Sam B. Warner,3.58,0674842111,9780674842113,en-US,236,61,6,4/20/2004,Harvard University Press
```

Each entry mirrors the original CSV line so Phase 03 can decide whether to fix the source data or keep excluding it.

---

## 5. Checklist review

- [x] Chose and documented the Python loading method (Module: `src.load_books_to_postgres`).
- [x] Implemented the process using pandas + SQLAlchemy with author-stage support.
- [x] Successfully loaded the dataset into PostgreSQL (`books` table now contains 11,119 rows).

The next task (Phase 02 → Step 03 → Task 03) covers verification of row counts and spot-checking records inside Postgres; see `docs/phase-02-step-03-task-03-notes.md`.
