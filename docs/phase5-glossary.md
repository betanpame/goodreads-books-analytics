# Phase 05 – SQL Validation & Comparison Glossary

Use this quick-reference while working through Phase 05 tasks (PostgreSQL validation, SQL-first metrics, and the SQL vs pandas comparisons). Pair it with `docs/data-faq.md` for command sequences and troubleshooting.

## Connection & Execution

- **`POSTGRES_*` environment block** – Variables loaded from `.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`). All Python CLIs (validation, comparisons, exports) build the SQLAlchemy URL using `src.db_config.build_database_url_from_env`, so never hard-code credentials in scripts.
- **`params` CTE pattern** – Every analysis SQL file begins with a `params` common table expression that centralizes tunables such as `min_year`, `top_n`, or minimum language coverage. Update those literal values instead of editing downstream joins so SQL and pandas stay aligned.
- **`books_clean` warehouse table** – Populated via `python -m src.load_books_clean_to_postgres`, this table mirrors `data/derived/books_clean.csv` (11127 rows) plus the refreshed `book_authors_stage`. All Phase 05 SQL scripts now query it instead of the raw `books` table, keeping canonical logic consistent with the pandas pipeline.

## Validation & Comparison CLIs

- **Postgres stats comparison CLI** – `python -m src.analyses.postgres_compare_stats` checks row counts, min/max dates, and aggregate ratings between CSV inputs and Postgres tables. Use it right after loading data to confirm the warehouse copy mirrors the source file.
- **SQL vs pandas comparison CLI** – `python -m src.analyses.sql_vs_pandas_compare` runs the numbered SQL analysis files, loads the Phase 04 metric CSVs, and compares key columns per metric. It is purpose-built for Step 03 Task 01 and produces review-friendly CSV/Markdown summaries.
- **Numeric tolerance & rounding** – The comparison CLI coerces numeric columns to floats and rounds configurable columns (e.g., average ratings to 4 decimals) before checking abs-delta ≤ 1e-4. Counts remain exact, so any integer mismatch is surfaced in the differences CSV.

## Output Artifacts

- **`comparison_summary` tables** – CSV/Markdown pair stored under `outputs/phase05_step03_task01/`. Columns include row counts (SQL vs pandas), whether the keys matched, mismatch counts, and an optional pointer to a per-metric differences file. Attach this table to task notes for instant evidence.
- **`<metric>_differences.csv`** – Generated only when mismatches occur. Each row lists the join key values, the column under review, SQL vs pandas values, and the absolute difference. These files are the source of truth when explaining divergences in documentation.
- **`canonical_book_count` (SQL)** – Column emitted by `sql/analysis/40_publication_year_trends.sql` after grouping canonical records per publication year. When renamed to `book_count` in Python, it should match the pandas `book_count` produced from `books_clean.csv` aside from known raw-vs-clean deltas.

## Interpretation Aids

- **Raw vs cleaned data gap** – Phase 05 SQL scripts currently query the raw `books` table plus the canonical mapping, while pandas metrics rely on `books_clean.csv` (winsorized counts, cleaned publication years, zero-to-NaN fixes). Expect small differences until the cleaned table is staged in Postgres.
- **When to prefer SQL** – Use SQL for reproducible, shareable queries that teammates can run directly in Postgres (e.g., creating views, exporting CSVs via `\copy`, or validating ETL pipelines). SQL also shines when filters or window functions run faster server-side.
- **When to prefer pandas** – Use pandas when you need to iterate quickly on transformations that already exist in the cleaning pipeline, or when the logic depends on Python-only helpers (e.g., canonical rollups that lean on derived flags). The pandas outputs remain the canonical artifacts for the portfolio unless SQL inherits the same cleaning steps.

Update this glossary whenever Phase 05 adds new CLIs, parameters, or interpretation nuances so reviewers always have a single glossary for SQL-era terminology.
