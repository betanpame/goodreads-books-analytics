# Phase 05 · Step 01 · Task 03 – Profile Key Columns and Null Values

## 1. Task definition and goal

Evaluate the completeness of the `books` table inside PostgreSQL by auditing null counts, distinct counts, numeric ranges, and top-category distributions for the business-critical fields we use in SQL analysis. The objective is to validate that our SQL workspace mirrors the pandas-based expectations before we ship any Postgres-only dashboards.

## 2. How to run this analysis script

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
# Ensure Docker services are up
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
# Run the profiling CLI (nulls, distincts, ranges, top categories)
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
  python -m src.analyses.postgres_profile_columns `
  --schema public `
  --table books `
  --top-n 10
```

- The CLI connects via SQLAlchemy, so credentials stay in `.env` and never leak into the command history.
- `--top-n` controls how many language/publisher rows show up in the distribution tables; tweak it as needed for storytelling.
- All evidence persists under `outputs/phase05_postgres_validation/` for portfolio sharing.

## 3. Environment recap

- **Services:** Same Docker Compose stack from Tasks 01–02 (Python app container + PostgreSQL 17 backend).
- **Dependencies:** pandas + SQLAlchemy + psycopg2-binary; no notebooks or external GUIs were used.
- **Source CLI:** `src/analyses/postgres_profile_columns.py`, which reuses `src/db_config.build_database_url_from_env` and the `validate_identifier` guardrails.

## 4. Findings / results

### Null & distinct counts (top-level summary)

| column             | null_count | distinct_count |
| ------------------ | ---------- | -------------- |
| book_id            | 0          | 11,119         |
| title              | 0          | 10,344         |
| authors            | 0          | 6,623          |
| average_rating     | 0          | 209            |
| ratings_count      | 0          | 5,293          |
| text_reviews_count | 0          | 1,822          |
| num_pages          | 0          | 997            |
| language_code      | 0          | 27             |
| publication_date   | 2          | 3,673          |
| publisher          | 0          | 2,289          |

- Only `publication_date` carries nulls (2 rows). Every other key column is fully populated, which simplifies SQL joins and filters.

### Numeric ranges

| column             | min_value | max_value |
| ------------------ | --------- | --------- |
| average_rating     | 0.0       | 5.0       |
| ratings_count      | 0         | 4,597,666 |
| text_reviews_count | 0         | 94,265    |
| num_pages          | 0         | 6,576     |

- The ranges mirror the Phase 03 outlier analysis; Postgres holds the same extremes we saw in pandas (e.g., `ratings_count` for Twilight, `num_pages` for multi-volume anthologies).

### Top categories (row counts)

- **language_code:** `eng` dominates (8,906 rows), with US/UK English variants contributing another ~1,600 rows. Non-English languages are much smaller cohorts (Spanish 218, French 144, German 99).
- **publisher:** Vintage, Penguin-branded imprints, Mariner, Ballantine, HarperCollins, and VIZ Media comprise the top ten. Each retains 80–300 titles, so GROUP BY queries on publisher will produce meaningful aggregates without additional filtering.

## 5. Expected output checkpoints

- CLI logs confirming null/distinct calculations, numeric ranges, and top-N tables (see appendix snippet).
- CSV/Markdown artifacts in `outputs/phase05_postgres_validation/`:
  - `books_null_distinct_summary.{csv,md}`
  - `books_numeric_ranges.{csv,md}`
  - `books_top_language_code.csv`
  - `books_top_publisher.csv`

## 6. Observations / insights

- Having zero nulls for `average_rating`, `ratings_count`, and `language_code` means SQL aggregations can skip COALESCEs unless analysts intentionally bucket missing publication dates.
- The publisher distribution reiterates that our dataset is heavily skewed toward classic literature imprints; modern indie publishers barely appear, so dashboards should clarify that the corpus is biased toward catalog titles rather than 2020s releases.
- `language_code` uses short ISO-ish labels (`eng`, `en-US`, `spa`) rather than descriptive names. Future SQL steps should join against a lookup table if we want presentation-friendly language names.

## 7. Artifacts refreshed each run

- `outputs/phase05_postgres_validation/books_null_distinct_summary.csv`
- `outputs/phase05_postgres_validation/books_null_distinct_summary.md`
- `outputs/phase05_postgres_validation/books_numeric_ranges.csv`
- `outputs/phase05_postgres_validation/books_numeric_ranges.md`
- `outputs/phase05_postgres_validation/books_top_language_code.csv`
- `outputs/phase05_postgres_validation/books_top_publisher.csv`

## 8. Q&A / data troubleshooting

| Question                                                  | Answer                                                                                                                                                                                                       |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| How do I profile a different table (e.g., `books_clean`)? | Pass `--table books_clean` when running the CLI. If the column list differs, edit `KEY_COLUMNS` inside `postgres_profile_columns.py` accordingly.                                                            |
| Can I add more distribution tables (e.g., top authors)?   | Yes – update `CATEGORY_QUERIES` and rerun. Each entry automatically writes its own CSV.                                                                                                                      |
| Why do numeric ranges show `0` for `num_pages`?           | Audiobook placeholders and catalog errors store zero pages. Filter them in downstream SQL if page counts impact the query logic.                                                                             |
| What if I discover unexpected nulls?                      | Re-run `python -m src.load_books_to_postgres` to reload from the raw CSV, then rerun the profiling CLI. If nulls persist, document them in `docs/data-cleaning-rules.md` and adjust SQL queries accordingly. |
| Do I need to copy these results into notebooks?           | No – the Markdown/CSV artifacts already contain the tables needed for documentation and presentations. Reference them directly from GitHub.                                                                  |

## 9. Checklist review (from the plan)

- [x] Key columns list created.
- [x] Profiling queries written and run (via Docker CLI).
- [x] Null counts and distinct counts summarized.
- [x] Basic distribution queries executed (language, publisher).
- [x] Implications for SQL analysis documented.

## 10. Appendices (log excerpt)

```
$ docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app \
    python -m src.analyses.postgres_profile_columns --schema public --table books --top-n 10
2025-12-05 05:32:52,983 INFO __main__ - Computed null/distinct counts for 10 columns
2025-12-05 05:32:52,989 INFO __main__ - Captured numeric ranges for 4 columns
2025-12-05 05:32:52,998 INFO __main__ - Computed top 10 distribution for language_code
2025-12-05 05:32:53,002 INFO __main__ - Computed top 10 distribution for publisher
2025-12-05 05:32:53,071 INFO __main__ - Profiling complete – 10 columns analyzed, category tables: language_code, publisher
```
