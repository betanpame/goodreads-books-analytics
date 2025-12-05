# Phase 05 · Step 01 · Task 02 – Verify Row Counts and Basic Statistics

## 1. Task definition and goal

Recreate the Phase 02 reference metrics (row count, average `average_rating`, publication date window) in both pandas and PostgreSQL, then store the comparison in git so stakeholders can audit it without spinning up the database. Success criteria: a single documented command block refreshes the CSV + Markdown comparison artifacts, and the logs explicitly confirm every metric matches between `data/books.csv` and `public.books`.

## 2. How to run this analysis script

1. **Start in the repo root** so relative paths resolve inside the container:

   ```powershell
   cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
   ```

2. **Boot (or restart) the Docker stack** to ensure both the Python and PostgreSQL containers are running:

   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   ```

   Verify with `docker compose ps` if needed.

3. **Run the comparison CLI** from the Python container. It reads the CSV using tolerant parsing, queries Postgres via SQLAlchemy, and writes results under `outputs/phase05_postgres_validation/`:

   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
       python -m src.analyses.postgres_compare_stats `
       --csv-path data/books.csv `
       --schema public `
       --table books
   ```

   Optional overrides:

   - `--table books_clean` to validate the cleaned dataset.
   - `--output-prefix books_clean_stats` to keep artifacts distinct when comparing multiple tables.

4. **Review the outputs** inside `outputs/phase05_postgres_validation/`—both `.csv` and `.md` tables update on each run.

## 3. Environment recap

- **Containers:** `app` (Python 3.11 slim) + `postgres` (PostgreSQL 17), orchestrated by the two Compose files.
- **Dependencies:** pandas, SQLAlchemy, psycopg2-binary, python-dotenv (already pinned in `requirements.txt`).
- **Data sources:** `data/books.csv` (raw Goodreads export) and `public.books` (loaded via `src.load_books_to_postgres`).
- **Config plumbing:** `src/db_config.build_database_url_from_env` centralizes credentials, so `.env` works locally and in CI.
- **Output directory:** `outputs/phase05_postgres_validation/` now holds schema snapshots (Task 01), comparison tables (Task 02), and profiling outputs (Task 03) for easy auditing.

## 4. Findings / results

| Metric               | CSV / pandas | PostgreSQL | Matches | Delta    |
| -------------------- | ------------ | ---------- | ------- | -------- |
| row_count            | 11,119       | 11,119     | yes     | 0        |
| average_rating       | 3.93414      | 3.93414    | yes     | 0.000000 |
| min_publication_date | 1900-01-01   | 1900-01-01 | yes     | 0 days   |
| max_publication_date | 2020-03-31   | 2020-03-31 | yes     | 0 days   |

- Every metric aligned perfectly, proving the Docker ingestion still matches the CSV’s tolerant read (skip eight malformed rows, retain the rest).
- Matching average rating to five decimals shows there’s no float drift between pandas and PostgreSQL `double precision`.
- The `[1900-01-01, 2020-03-31]` window confirms downstream SQL dashboards can reuse the same temporal bounds defined back in Phase 02.

## 5. Expected output checkpoints

- CLI logs:

  ```
  INFO __main__ - CSV metrics – rows: 11,119, avg_rating: 3.93414, min_date: 1900-01-01 00:00:00, max_date: 2020-03-31 00:00:00
  INFO __main__ - PostgreSQL metrics – rows: 11,119, avg_rating: 3.93414, min_date: 1900-01-01 00:00:00, max_date: 2020-03-31 00:00:00
  INFO __main__ - Wrote comparison table to outputs/phase05_postgres_validation/books_stats_comparison.csv
  INFO __main__ - All metrics matched between CSV and PostgreSQL
  ```

- `outputs/phase05_postgres_validation/books_stats_comparison.csv` and `.md` contain the table shown in Section 4.

## 6. Observations / insights

- `engine="python"` + `on_bad_lines="skip"` remains non-negotiable for `data/books.csv`; the default C engine fails on malformed rows and would instantly break parity.
- The CLI’s shared `validate_identifier` helper prevents typos and SQL injection when analysts override `--schema` or `--table`, so we can hand this tool to juniors safely.
- Storing both CSV and Markdown outputs gives us machine-readable data for tests plus human-friendly snippets for documentation.
- Re-running this task after every reload or transformation guards against silent drift between pandas and Postgres.

## 7. Artifacts refreshed each run

- `outputs/phase05_postgres_validation/books_stats_comparison.csv`
- `outputs/phase05_postgres_validation/books_stats_comparison.md`
- Command log excerpt (see Appendix) embedded in this note

## 8. Q&A / troubleshooting

| Question                                | Answer                                                                                                                                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Why does pandas need `engine="python"`? | The CSV contains sporadic extra commas; the Python engine plus `on_bad_lines="skip"` mirrors how we ingested data into Postgres, keeping comparisons fair.                                                    |
| Can I compare additional metrics?       | Yes—extend `METRICS` inside `postgres_compare_stats.py` or point the CLI at another table/CSV pair.                                                                                                           |
| What if a metric mismatches?            | The CLI logs the failing metric and its delta. Re-run `python -m src.load_books_to_postgres` or inspect the offending rows with `psql` (e.g., `SELECT * FROM books WHERE publication_date IS NULL LIMIT 5;`). |
| Where do I find the outputs?            | `outputs/phase05_postgres_validation/books_stats_comparison.{csv,md}`—commit both after running the task.                                                                                                     |
| How do I embed the results elsewhere?   | Paste the Markdown table from `books_stats_comparison.md` into docs (see Section 4) or link directly to the artifact in GitHub.                                                                               |

## 9. Checklist review (from the plan)

- [x] Reference metrics computed via pandas/CSV.
- [x] Postsecondary metrics computed via SQL (PostgreSQL `books` table).
- [x] Comparison table generated and stored.
- [x] Discrepancies investigated (none detected) and documented.
- [x] Conclusion on PostgreSQL data validity recorded.

## 10. Appendices (log excerpt)

```
$ docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
    python -m src.analyses.postgres_compare_stats `
    --csv-path data/books.csv --schema public --table books
2025-12-05 05:29:08,855 INFO __main__ - Reading CSV from data/books.csv
2025-12-05 05:29:09,005 INFO __main__ - CSV metrics – rows: 11,119, avg_rating: 3.93414, min_date: 1900-01-01 00:00:00, max_date: 2020-03-31 00:00:00
2025-12-05 05:29:09,059 INFO __main__ - PostgreSQL metrics – rows: 11,119, avg_rating: 3.93414, min_date: 1900-01-01 00:00:00, max_date: 2020-03-31 00:00:00
2025-12-05 05:29:09,071 INFO __main__ - Wrote comparison table to outputs/phase05_postgres_validation/books_stats_comparison.csv
2025-12-05 05:29:09,077 INFO __main__ - All metrics matched between CSV and PostgreSQL
```
