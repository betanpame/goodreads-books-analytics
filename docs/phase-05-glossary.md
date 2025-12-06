# Phase 05 – SQL Analysis & Validation Glossary

Beginner-friendly reference for every concept introduced while validating and querying PostgreSQL in Phase 05. Pair this with `docs/data-faq.md` for step-by-step troubleshooting.

## Quick run references (Phase 05 · Step 02)

- **Task 01 – SQL workspace bootstrap** – `cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`, run `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`, then launch `psql` with `docker compose ... exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads` and call `\i sql/schema/01_create_books_table.sql`, `\i sql/schema/02_create_books_canonical_view.sql`, and `\i sql/analysis/00_sanity_checks.sql` in order to rebuild the baseline. Expect `SELECT COUNT(*) FROM books;` to return `11119`.
- **Task 02 – Core metric refresh** – After Docker is up, execute `foreach($script in 20,30,40,50,55) { docker compose ... exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f ("/app/sql/analysis/${script}_*.sql") }` to replay the five KPI scripts without retyping each command. Capture evidence with `\copy (...) TO '/app/outputs/phase05_step02_task02/<metric>.csv' WITH CSV HEADER` or by running `python -m src.analyses.export_sql ...` inside the `app` container.
- **Task 03 – Advanced windowing** – Keep the stack running, then trigger `60_`, `70_`, and `80_` scripts with `docker compose ... exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f /app/sql/analysis/<file>.sql`. To capture CSVs without local credentials, run the provided inline Python block inside the `app` container so it inherits `.env` values and writes to `outputs/phase05_step02_task03/`.

## Core definitions

- **Postgres validation CLI (`src.analyses.postgres_validate_books`)** – Docker-first Python script that connects via SQLAlchemy, counts rows, captures the column metadata from `information_schema`, and saves schema + preview CSVs inside `outputs/phase05_postgres_validation/`.
- **Schema snapshot** – CSV exported by the validation CLI listing `column_name`, `data_type`, and `is_nullable` for the inspected table. Commit these snapshots whenever the database schema changes so reviewers can diff evolutions through Git rather than screenshots.
- **Sample preview** – Companion CSV containing the first _n_ ordered rows (default 5) from the validated table. Lets stakeholders verify strings, dates, and numeric columns render correctly via SQL before jumping into analytics.
- **Books table contract** – The `books` table inside Postgres should expose 14 columns: the 12 raw Goodreads fields plus `authors_raw` and `authors_clean`. Expect exactly 11,119 rows after skipping malformed CSV lines (mirrors the loader’s `on_bad_lines="skip"` behavior).
- **`book_authors_stage` table** – Staging table created by `src.load_books_to_postgres` via `explode_authors`. Stores `book_id`, `author_order`, `author_name`, and `raw_authors`, enabling SQL leaderboards to reuse the same exploded author logic as pandas.
- **Author leaderboard rank** – The global `ROW_NUMBER()` applied after aggregating total capped ratings per author. Used in `60_top_books_per_author.sql` to guarantee we only surface the top N most-read authors before looking at their per-author top books.

## Comparison metrics

- **Stats comparison CLI (`src.analyses.postgres_compare_stats`)** – Reads `data/books.csv`, computes the reference metrics in pandas (row count, `AVG(average_rating)`, min/max `publication_date`), runs the same aggregates in PostgreSQL, and writes CSV/Markdown reports into `outputs/phase05_postgres_validation/`.
- **Reference metrics** – The canonical numbers sourced from the CSV using the tolerant parser (`engine="python"`, `on_bad_lines="skip"`). They double as acceptance criteria for any future reload.
- **Row-count parity** – Requirement that `COUNT(*)` in PostgreSQL matches the reference metric exactly. Any non-zero delta in `books_stats_comparison.csv` means the load diverged and must be re-run.
- **Numeric tolerance** – The comparison script allows ±1e-6 when matching floating-point aggregates to account for binary rounding differences between pandas and PostgreSQL `double precision`.
- **Publication window** – The `[1900-01-01, 2020-03-31]` date span verified by both pandas and SQL. Treat it as the official temporal coverage when writing SQL date filters or dashboards.
- **SQL portfolio spotlight** – The recruiter-facing digest published in `README.md` (section “SQL Portfolio Spotlight”) and mirrored in `docs/phase-05-step-03-task-02-notes.md`. It stitches together the comparison outputs, PPTX export, and SQL features practiced so stakeholders can judge Phase 05 without running the code themselves.

## Column profiling

- **Column profiling CLI (`src.analyses.postgres_profile_columns`)** – Executes SQL queries for null counts, distinct counts, numeric ranges, and top categorical distributions, then exports the evidence as CSV/Markdown tables under `outputs/phase05_postgres_validation/`.
- **Key column list** – The curated set of fields the CLI inspects (`book_id`, `average_rating`, `ratings_count`, `language_code`, etc.). Adjust this list if downstream steps introduce new critical fields.
- **Category distributions** – The top-N breakdowns for `language_code`, `publisher`, or any column added to `CATEGORY_QUERIES`. These tables feed Phase 05 notes and help analysts choose safe `GROUP BY` dimensions.
- **Null/distinct summary** – Artifact proving which columns contain nulls (only `publication_date` today) and how many unique values exist per field, ensuring SQL filtering plans align with pandas assumptions.
- **Engagement percentile (`engagement_p75`)** – `percentile_cont(0.75)` over the capped `ratings_count` per publisher/language cohort. Captures “typical” high-end engagement without being skewed by a single blockbuster and matches the quantile approach we used in pandas.

## SQL workflow hygiene

- **`PAGER=cat`** – Environment override passed to `psql` inside Docker so outputs stream directly to the terminal. Without it, `psql` tries to open `less`, which causes the `TURN: No such file or directory` warning and hides the table listings.
- **Quiet mode (`-q`)** – Optional `psql` flag that removes extra headers, keeping logs cleaner for portfolio notes and automation scripts.
- **Information schema probe** – The query used by the validation CLI: `SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema=:schema AND table_name=:table`. Treat it as the authoritative source for schema documentation.
- **Order column** – CLI flag that controls which column sorts the preview rows (default `book_id`). Useful when you want the preview to focus on high-engagement books (`--order-column ratings_count`) or recent dates.
- **`params` CTE** – Tiny configuration block at the top of each analysis script (top_n, min_year, min_book_threshold). Editing these literals is the supported way to change thresholds without touching the rest of the SQL.
- **Python/Docker-only workflow** – Guardrail for Phase 05: run every CLI through `docker compose` (or the PowerShell wrapper) so Python modules, PostgreSQL, and dependencies stay identical across machines. Notebooks are intentionally excluded to keep automation and CI trivial.

## SQL workspace conventions

- **`sql/schema/`** – Folder containing numbered DDL files (`01_create_books_table.sql`, `02_create_books_canonical_view.sql`). Scripts here change database structure and should run before any analysis queries.
- **`sql/analysis/`** – Folder for read-only validation queries and helper snippets. Lower prefixes (e.g., `00_sanity_checks.sql`) are diagnostic commands, while higher prefixes (`10_...`) build on canonicalized views.
- **Numeric prefix** – Two-digit number prepended to every `.sql` filename to make execution order obvious when using `\i` inside `psql`.
- **Sanity checks script** – `sql/analysis/00_sanity_checks.sql` prints the expected row count (11,119), verifies the `average_rating` range, and surfaces the top language codes so you can prove the load succeeded before running heavier analysis.
- **Canonical rollup CTE** – Shared pattern inside analysis scripts that coalesces duplicate book IDs, picks a representative textual row via `DISTINCT ON`, and computes capped engagement metrics so duplicates never double-count.
- **Rolling 3-year window** – The `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` frame used in `80_publication_year_rolling_stats.sql` to smooth average ratings and median engagement over time directly inside SQL.

## SQL analysis metrics (Phase 05 · Step 02 · Task 02)

- **M1 SQL (`analysis/20_top_authors_weighted_rating.sql`)** – Recreates the weighted author leaderboard using `book_authors_stage`, canonical IDs, and a 5,000-ratings floor. Outputs `author_name`, weighted rating, total ratings, and canonical book count.
- **M3/M4 SQL (`analysis/30_top_books_by_engagement.sql`)** – Produces two labeled leaderboards (ratings vs text reviews) from the canonical rollup with capped engagement fields, mirroring the pandas CSV outputs.
- **M7/M8 SQL (`analysis/40_publication_year_trends.sql`)** – Aggregates average rating and median capped ratings count per publication year with a configurable lower bound (default 1950).
- **M9 SQL (`analysis/50_language_quality_summary.sql`)** – Summarizes average rating and median engagement per language_code, filtering to cohorts with at least 50 canonical books.
- **M11 SQL (`analysis/55_duplicate_share.sql`)** – Simple aggregate showing total rows, duplicate rows, and duplicate share percentage from `bookid_canonical_map` so canonical coverage stays transparent.
- **M12 SQL (`analysis/60_top_books_per_author.sql`)** – (Task 03) Surfaces each author’s top 3 books alongside a global author leaderboard using dual `ROW_NUMBER()` windows and a minimum total-ratings filter.
- **M13 SQL (`analysis/70_language_publisher_rankings.sql`)** – (Task 03) Keeps publishers with sufficient catalog depth per language and ranks them by average rating + 75th-percentile engagement to avoid single-book outliers.
- **M14 SQL (`analysis/80_publication_year_rolling_stats.sql`)** – (Task 03) Computes per-year averages, medians, rolling 3-year windows, and year-over-year deltas using Postgres window functions only.

## Documentation links

- **Notes:** `docs/phase-05-step-01-task-01-notes.md` – walkthrough of the Docker + `psql` steps plus the validation CLI output.
- **Notes:** `docs/phase-05-step-01-task-02-notes.md` – captures the CSV vs PostgreSQL comparison results, CLI commands, and interpretation guidance for recruiters.
- **Notes:** `docs/phase-05-step-01-task-03-notes.md` – records the null/distinct profiling outputs, explains language/publisher distributions, and highlights implications for SQL aggregations.
- **FAQ bridge:** `docs/data-faq.md` → _Phase 05 PostgreSQL validation_ – command snippets, row count expectations, and troubleshooting tips (pager issues, sample sizing, reloading data).
- **Related outputs:** `outputs/phase05_postgres_validation/books_schema_snapshot.csv` and `books_sample_preview.csv` – refreshed alongside every validation run.
- **Comparison outputs:** `outputs/phase05_postgres_validation/books_stats_comparison.csv` + `.md` – show the row count, average rating, and publication-window parity that Task 02 requires.
- **Profiling outputs:** `books_null_distinct_summary.*`, `books_numeric_ranges.*`, `books_top_language_code.csv`, `books_top_publisher.csv` – the official evidence set for Task 03’s column audits.
- **Notes:** `docs/phase-05-step-03-task-02-notes.md` – portfolio-focused walkthrough for Step 03 Task 02, including the Python/Docker command block, recruiter narrative, capability bullets, and artifact checklist.
