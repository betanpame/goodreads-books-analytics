# Data FAQ and Troubleshooting Guide

Use this FAQ whenever you need quick answers about the Goodreads books dataset, Docker workflow, or script outputs. Each task note links back here so we keep common guidance in one place.

## Dataset basics

**Where is the raw dataset stored?** – `data/books.csv`. The repository already includes the file; if it goes missing, follow `docs/dataset-notes.md` for download steps, then re-run the scripts.

**How do I confirm the file exists before running anything?** – From the repo root, run `dir data` (PowerShell) or `ls data` (bash). You should see `books.csv` (≈16 MB) plus any helper files like `example_people.csv`.

**What if Docker can’t see `data/books.csv`?** – Make sure you start containers from the project root so the bind mount includes the `data/` folder:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
```

If the mount is correct but the container still can’t read the file, check file permissions or re-copy the CSV.

## Column questions

**Why does `num_pages` have leading spaces?** – The original CSV ships with two spaces (`"  num_pages"`). Don’t rename it until you reach the cleaning phase; the current scripts expect the raw column name so they can demonstrate quirks.

**How can I inspect unique values or dtypes quickly?** – Run `python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose`. Task 03 logs the dtype, `nunique()`, missing count, and sample values for every key column.

**How do I troubleshoot `publication_date` parsing failures?** – In an interactive session, reuse the code from Task 03:

```python
parsed = pd.to_datetime(sample["publication_date"], errors="coerce")
bad_rows = sample.loc[parsed.isna(), ["bookID", "title", "publication_date"]]
```

Document repeated failures here so the cleaning phase can normalize them.

## Output artifacts

**Which files prove the scripts ran?** – Every run refreshes:

- `outputs/initial_inspection/books_sample_preview.csv`
- `outputs/initial_inspection/books_numeric_summary.csv`

Inspect those when you need to cite evidence without re-running the CLI.

**Where can I find the Step 02 Task 01 relationship outputs?** – After running `python -m src.analyses.eda_books --verbose`, check `outputs/phase03_univariate/step02_task01_relationships/`. It stores:

- Scatter plots for `average_rating` vs `num_pages`, `ratings_count`, and `text_reviews_count`.
- `average_rating_by_page_bucket.csv` plus its companion bar chart for the four page-length buckets.

Reference these files in presentations or notebooks so recruiters can see the actual visual evidence.

**Where can I find the Step 02 Task 02 temporal outputs?** – The same CLI call refreshes `outputs/phase03_univariate/step02_task02_temporal/` with:

- `books_published_per_year.csv` and `books_published_per_year_line.png`
- `average_rating_by_year.csv` and `average_rating_by_year_line.png`
- `average_ratings_count_by_year.csv` and `average_ratings_count_by_year_line.png`

These artifacts already include the `publication_year` feature, so any downstream analysis can reuse the CSVs without re-deriving dates.

**Why do the per-year charts collapse after 2006?** – Only 2 of the 11,127 rows are missing `publication_date`, but many post-2006 entries have malformed strings (for example, `"9/2007"` instead of a full date). Those rows are excluded once we convert to `publication_year`, so the raw dataset simply lacks trustworthy metadata for modern releases. Highlight this caveat whenever you cite the temporal charts so readers know the drop is data-related, not a business trend.

**Where can I find the Step 02 Task 03 category outputs?** – Look under `outputs/phase03_univariate/step02_task03_category_relationships/`. Each CLI run rebuilds:

- `language_category_summary.csv`, `avg_rating_by_language.png`, and `median_ratings_count_by_language.png`
- `publisher_category_summary.csv`, `avg_rating_by_publisher.png`, and `median_ratings_count_by_publisher.png`

The CSVs list average rating, median `ratings_count`, median `text_reviews_count`, and book counts for the configured "top N" languages/publishers so dashboards can reuse the aggregates without rerunning pandas code.

**Where can I find the Phase 05 Step 02 Task 03 SQL exports?** – The Postgres-first versions of the language/publisher rankings and rolling publication metrics live under `outputs/phase05_step02_task03/` as `70_language_publisher_rankings.csv` and `80_publication_year_rolling_stats.csv`. Regenerate them by running the corresponding SQL files with `psycopg2` (see Task 03 notes for the snippet) or via `docker compose ... psql -f /app/sql/analysis/<file>.sql` plus `\copy`.

**Where do the SQL vs pandas comparison results live (Phase 05 Step 03 Task 01)?** – Run the Docker-only CLI `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.sql_vs_pandas_compare`. The command executes the Phase 05 SQL scripts, loads the Phase 04 pandas CSVs, and writes `comparison_summary.{csv,md}` plus any `<metric>_differences.csv` files to `outputs/phase05_step03_task01/`.

**What if the summary shows mismatches?** – Now that `books_clean` lives in Postgres and every SQL script queries it, the comparison CLI should report a clean sweep. If you see differences, rerun `python -m src.load_books_clean_to_postgres` (to refresh `books_clean` + `book_authors_stage`) and re-execute the SQL scripts. The per-metric differences CSVs remain the fastest way to debug any lingering drift.

**Where can I find the Phase 05 Step 03 Task 02 portfolio summary?** – The recruiter-facing narrative lives in `README.md` under “SQL Portfolio Spotlight (Fase 05)” and is mirrored in `docs/phase-05-step-03-task-02-notes.md`. Both files describe the SQL questions solved, the PostgreSQL features exercised, and where to download the supporting CSV/PNG/PPTX artifacts.

**How do I refresh the SQL portfolio artifacts without Jupyter?** – Stay inside Docker + PowerShell: `cd` to the repo, run `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`, then execute `powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide`. This single command reloads `books_clean`, reruns the SQL vs pandas comparison, regenerates `comparison_summary.{csv,md,png}`, and exports `phase05_sql_vs_pandas.pptx`—no notebooks required.

**How should I interpret small-sample categories?** – Some high-scoring languages (e.g., `zho` or `jpn`) and prestige publishers have fewer than 100 titles. Treat their averages as directional insight, cite the `book_count` column, and pair them with the engagement chart so readers know whether a spike reflects broad sentiment or a niche cohort.

**Why do the SQL publisher rankings mostly show English rows?** – The SQL script filters to languages where each publisher ships at least 20 canonical books. Today only `eng` and `en-US` satisfy that threshold. Lower the limit inside the script’s `params` CTE if you need to explore smaller cohorts, but keep the documented outputs strict to avoid one-book leaderboards.

**Where are the Step 03 Task 01 data-quality outputs?** – After running `python -m src.analyses.eda_books`, inspect `outputs/phase03_univariate/step03_task01_missing_duplicates/`. It contains `missing_values_summary.csv` plus `duplicate_summary.csv` and detailed samples (`partial_duplicates_by_subset.csv`). These files are the single source of truth for missingness rates and duplicate counts referenced in the task notes.

**Where are the Step 03 Task 02 outlier outputs?** – The same CLI refreshes `outputs/phase03_univariate/step03_task02_outliers/`. Expect `numeric_outlier_summary.csv`, `outlier_rule_violations.csv`, per-rule sample CSVs (e.g., `num_pages_suspect_high.csv`), and paired boxplot/histogram PNGs under the nested `plots/` folder. Link to these files whenever you cite an anomaly so everyone references the same evidence.

**Where can I see the final cleaning decisions?** – Task 03 generated `docs/data-cleaning-rules.md`. It lists every rule (issue, affected columns, decision, rationale, priority) plus links back to the supporting CSV samples. The EDA CLI prints the file path at the end of each run to keep it top-of-mind.

**How do I apply the rules in code?** – Treat `docs/data-cleaning-rules.md` as the contract. Phase 04 scripts should: (1) join to `duplicate_bookid_mapping.csv` for canonical IDs, (2) winsorize `ratings_count`/`text_reviews_count` at the documented caps, (3) convert `num_pages=0` to `NaN` and bucket `<10` / `>2000` page records, and (4) set `average_rating=0` to missing. Update the markdown file whenever logic changes so documentation and code stay aligned.
**What caps should I apply to popularity metrics?** – To keep analyses readable, clip `ratings_count` at 597,244 and `text_reviews_count` at 14,812 (both values come from the p99.5 quantiles computed in Phase 03 Step 01 Task 03). The logic already lives inside `src/analyses.eda_books.py`; reuse the same thresholds in notebooks, dashboards, or Postgres views so every downstream chart stays consistent.

**Why do some books show `num_pages = 0` or 2,000+?** – Audiobook bundles and study guides inherit placeholder page counts (often zero), while boxed sets and medical references legitimately exceed 2,000 pages. Treat `<10` pages and `>2,000` pages as suspect cohorts; the Task 02 CLI exports them to `num_pages_suspect_low.csv` and `num_pages_suspect_high.csv` so you can flag them or bucket them separately.

**What does “partial duplicate subset” mean?** – We normalize the `title`, `authors`, and `publication_date` strings (fill blanks with `Unknown`, trim whitespace) and then look for repeated combinations. A match indicates the same story appears multiple times (hardcover vs audiobook, translation, etc.). Use the sample CSV’s `bookID` column to decide which record should stay canonical before Phase 04 loads data into Postgres.

**How do I use the duplicate→canonical mapping in SQL?** – Load `data/derived/duplicate_bookid_mapping.csv` into a staging table (for example, `bookid_canonical_map`) with columns `duplicate_bookid` and `canonical_bookid`. When building fact tables, left join on `duplicate_bookid`; coalesce to `canonical_bookid` if present, else fall back to the original `bookID`. This ensures audiobook/translation variants roll up to the same canonical record without deleting the source rows.

**What command loads the mapping into Postgres?** – After setting `DATABASE_URL`, run either `python -m src.load_duplicate_mapping --table bookid_canonical_map` (local venv) or `docker compose -f docker-compose.python.yml exec app python -m src.load_duplicate_mapping --table bookid_canonical_map`. The script validates the CSV and writes it with `to_sql`, so the table is ready for Phase 04 ETL jobs.

**How do I load the cleaned dataset into Postgres for SQL analysis?** – Use the Docker-only CLI so every Phase 05 query touches the curated data:

```powershell
docker compose -f docker-compose.python.yml run --rm app `
	python -m src.load_books_clean_to_postgres `
	--csv-path data/derived/books_clean.csv `
	--table books_clean
```

The command writes `books_clean` (11127 rows) and refreshes `book_authors_stage`, so the SQL scripts no longer depend on the raw CSV or the standalone duplicate mapping.

**Can I safely delete the outputs folder?** – Yes; the next script execution recreates the files. This is a good way to verify that the pipeline still works end-to-end.

**What caps should I apply to popularity metrics?** – To keep analyses readable, clip `ratings_count` at 597,244 and `text_reviews_count` at 14,812 (both values come from the p99.5 quantiles computed in Phase 03 Step 01 Task 03). The logic already lives inside `src/analyses/eda_books.py`; reuse the same thresholds in notebooks, dashboards, or Postgres views so every downstream chart stays consistent.

## Phase 04 cleaning pipeline

**What is the canonical command to refresh `books_clean.csv`?** – Run the CLI strictly inside Docker:

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm `
	app python -m src.pipelines.run_cleaning `
	--books-csv data/books.csv `
	--mapping-csv data/derived/duplicate_bookid_mapping.csv `
	--output-csv data/derived/books_clean.csv
```

`--no-deps` keeps the workflow Python-only when PostgreSQL is already running elsewhere; drop the flag if you need database access.
**Shortcut:** `make metrics-catalog` runs the same CLI via Docker when GNU Make is available (also used by CI).

**Where do the duplicate pairs live and how are they validated?** – The mapping file is `data/derived/duplicate_bookid_mapping.csv`. The CLI lowercases and trims the headers, converts both ID columns to `Int64`, drops nulls, and logs `Loaded 16 duplicate pairs` (or whatever the count is). If the columns go missing, the CLI raises a `ValueError` before any data is written.

**How do I confirm the canonical join actually worked?** – After the run, review the log snippet:

```
[INFO] Value counts for is_duplicate:
is_duplicate
False    11111
True        16
```

You should also open `data/derived/books_clean.csv` and verify that it contains `canonical_book_id` with no nulls. The CLI’s `canonical_id_present` validation fails (and exits non-zero) if any null sneaks in.

**What validations guard the cleaning output?** – `run_cleaning.py` asserts four invariants: (1) `average_rating` stays within `[0, 5]`; (2) `num_pages_capped ≤ 2,000`; (3) `ratings_count_capped ≤ 597,244` and `text_reviews_count_capped ≤ 14,812`; (4) `canonical_book_id` has full coverage. These checks run automatically and will halt the process if violated.

**Can I run partial tests without waiting for the full CSV?** – Yes. Use `--limit 1000` (or any row count) to slice the DataFrame before cleaning. This keeps iteration fast while still exercising every transformation and validation.

**Where can I learn what each new flag means?** – See `docs/phase-04-glossary.md` for definitions (`average_rating_flag`, `page_length_bucket`, `media_type_hint`, `is_duplicate`, etc.). That glossary mirrors the Phase 03 style so recruiters and teammates can understand the features without re-reading the entire notebook.

**How should I document my runs for the portfolio?** – Follow `docs/task-note-template.md`. Phase 04 Task 01 already uses it in `docs/phase-04-step-01-task-01-notes.md`, capturing commands, metrics, validations, and artifacts in a beginner-friendly yet professional tone.

## Phase 04 metrics planning

**Where do the official metric definitions live?** – Run `python -m src.analyses.metrics_catalog` (see Task 01 notes for the exact Docker command) or open the generated file `outputs/phase04_metrics_catalog.md`. Both include the `Question → Metric → Columns → Notes → Priority` mapping.

**What should I do if the metrics script fails column validation?** – Recreate `data/derived/books_clean.csv` with `python -m src.pipelines.run_cleaning`, then confirm the columns listed in `KEY_COLUMNS` inside `metrics_catalog.py` exist. The script intentionally fails fast so dashboards never rely on stale schemas.

**How can I add or tweak a metric?** – Edit the `METRIC_DEFINITIONS` tuple in `src/analyses/metrics_catalog.py`, rerun the CLI inside Docker, and commit the refreshed Markdown output. Update `docs/phase-04-glossary.md` whenever you introduce new terminology (e.g., “engagement index”).

**What classifies a metric as core vs stretch?** – Use the `priority` field in the metrics catalog. Core metrics (labelled `core`) must be implemented in Phase 04 Step 02 Task 02; stretch metrics are documented for future sprints but can be deferred without blocking the narrative.

## Phase 04 core metrics CLI

**How do I compute all core metrics at once?** – Run the command block in Task 02 notes or, more simply, `make core-metrics`. Both execute `python -m src.analyses.run_core_metrics` inside Docker and refresh `outputs/phase04_core_metrics/`.

**What files should appear afterward?** – Expect eight CSVs named `M*_*.csv` (top authors, top books by ratings, top books by text reviews, page-length median ratings, average rating by year, median ratings_count by year, language summary, duplicate share). Each file is logged during the run.

**Can I change thresholds for reviews, author minimums, or language coverage?** – Yes. The CLI exposes `--author-min-ratings`, `--author-top-n`, `--books-top-n`, `--language-min-books`, and `--min-year`. Combine them with `make core-metrics FLAGS="--author-min-ratings 10000 --books-top-n 50"` if you want a one-liner.

**Where do these metrics map to the documentation?** – Definitions live in `outputs/phase04_metrics_catalog.md`, Task 01 notes, and the Glossary. Task 02 notes explain how each CSV ties back to business questions for the portfolio narrative.

## Phase 05 PostgreSQL validation

**Where do the SQL scripts live and how do I run them?** – All database assets now live under `sql/`. `sql/schema/` houses DDL + views, while `sql/analysis/` stores read-only validation and analytics queries. Start Docker with `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`, open psql via `docker compose ... exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads`, then execute scripts inside the session using `\i sql/schema/01_create_books_table.sql` (or non-interactively with `-f /app/sql/...`). Follow the numeric prefixes so files run in the intended order.

**How do I run the new validation CLI?** – From the repo root:

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
	python -m src.analyses.postgres_validate_books --table books --sample-limit 5
```

This reads the connection info from `.env`, inspects the requested table, and writes schema + preview CSVs under `outputs/phase05_postgres_validation/`.

**Which `psql` commands should I capture for Task 01?** – Run them inside the Postgres container with the pager disabled so the logs stay clean:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
	postgres psql -q -U goodreads_user -d goodreads -c "\\l"
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
	postgres psql -q -U goodreads_user -d goodreads -c "\\dt"
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
	postgres psql -q -U goodreads_user -d goodreads -c "\\d+ books"
```

**What row count should I see for `books`?** – `SELECT COUNT(*) FROM books;` returns `11119`. The number matches `pd.read_csv('data/books.csv', on_bad_lines="skip", engine="python")` because the loader skips 8 malformed rows. If the count drifts, rerun `python -m src.load_books_to_postgres --table books`.

**How can I change the preview size or ordering?** – Pass `--sample-limit` and `--order-column` to `src.analyses.postgres_validate_books`. Example: `--sample-limit 20 --order-column ratings_count`.

**Where do the schema snapshots live?** – Every CLI run refreshes `outputs/phase05_postgres_validation/books_schema_snapshot.csv` and `books_sample_preview.csv`. Commit those files when documenting Phase 05 so reviewers can diff schema changes without standing up Postgres themselves.

**Why does `psql` complain about `TURN: No such file or directory`?** – Without `PAGER=cat`, `psql` tries to spawn `less`, which is not installed in the lightweight container. Keeping `PAGER=cat` (and optionally `-q`) removes the warning and prints the full table listings inline.

**How do I compare CSV vs PostgreSQL metrics automatically?** – Run the stats CLI:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
	python -m src.analyses.postgres_compare_stats --csv-path data/books.csv --schema public --table books
```

It reads the CSV with the same `on_bad_lines="skip"` logic as the loader, fetches aggregate metrics from PostgreSQL, and logs whether each metric matches.

**Which metrics does the comparison cover and what tolerance is used?** – The CLI validates `row_count`, `AVG(average_rating)`, and the min/max `publication_date`. Float comparisons allow ±1e-6, so rounding noise is tolerated. Dates must match exactly.

**Where are the comparison artifacts stored?** – After the run you will find `books_stats_comparison.csv` and `books_stats_comparison.md` under `outputs/phase05_postgres_validation/`. Embed these files in task notes so reviewers can inspect the evidence straight from GitHub.

**Can I point the comparison at `books_clean` or add more metrics?** – Yes. Swap `--table books_clean` (or another table) and edit `src/analyses/postgres_compare_stats.py` to add new aggregations. The helper validates identifier names so schema/table overrides stay safe.

**How do I profile nulls, distinct counts, and top categories in Postgres?** – Run the profiling CLI:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app `
	python -m src.analyses.postgres_profile_columns --schema public --table books --top-n 10
```

This inspects the key columns listed in the plan (IDs, ratings, counts, language, publisher, publication_date) and saves summary CSV/Markdown tables in `outputs/phase05_postgres_validation/`.

**What if I want to focus on other columns or a different table?** – Edit `KEY_COLUMNS` and `CATEGORY_QUERIES` inside `postgres_profile_columns.py`, or pass `--table books_clean` if you want to profile the cleaned dataset. The CLI validates identifiers to keep ad-hoc runs safe.

**Where are the profiling artifacts stored and how should I use them?** – Look for `books_null_distinct_summary.{csv,md}`, `books_numeric_ranges.{csv,md}`, `books_top_language_code.csv`, and `books_top_publisher.csv` under `outputs/phase05_postgres_validation/`. Reference them directly in task notes or presentations to prove the SQL workspace mirrors the pandas expectations.

**Why do I see `num_pages = 0` in the numeric range output?** – Audiobook placeholders and faulty catalog entries deliberately keep `num_pages=0`. Downstream SQL queries should either filter them out or bucket them (e.g., `CASE WHEN num_pages = 0 THEN 'audio_or_unknown'`).

## Phase 05 SQL analysis (Step 02 · Task 02)

**How do I run the new SQL metric scripts?** – After `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`, run `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f /app/sql/analysis/<file>.sql`. Replace `<file>` with the numbered script (20, 30, 40, 50, 55). Because the repo now mounts inside the Postgres container, the `/app/sql/...` path also works inside interactive `psql` via `\i`.

**Why does `psql` now see the `sql/` folder?** – We added a `.:/app:ro` volume to both Compose files, exposing the repo read-only within the Postgres service. If you still get "No such file" errors, recreate the container with `docker compose ... up -d --force-recreate postgres`, then verify with `docker compose ... exec postgres ls /app/sql/analysis`.

**How do I tweak thresholds like `top_n`, `min_year`, or the language coverage filter?** – Each script declares a `params` CTE at the top. Adjust the literal values (e.g., set `SELECT 25::int AS top_n`) and rerun the same command. No other clauses need editing.

**Where should I document or export the SQL outputs?** – Copy/paste the tabular results into `docs/phase-05-step-02-task-02-notes.md`, or add `\copy` statements if you need CSVs for dashboards. Reference the `sql/README.md` analysis catalog whenever you cite one of the scripts in a presentation.

## Phase 05 Step 02 quick walkthroughs

**What is the fastest way to rerun the Task 01 sanity scripts?** – From the repo root run `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`, then start `psql` with `docker compose ... exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads`. Inside the prompt execute `\i sql/schema/01_create_books_table.sql`, `\i sql/schema/02_create_books_canonical_view.sql`, and `\i sql/analysis/00_sanity_checks.sql`, then confirm `SELECT COUNT(*) FROM books;` returns `11119` before exiting with `\q`.

**Is there a single command sequence for all Task 02 SQL files?** – Yes. Use PowerShell’s `foreach` to iterate over the numbered scripts: `foreach($script in '20_top_authors_weighted_rating.sql','30_top_books_by_engagement.sql','40_publication_year_trends.sql','50_language_quality_summary.sql','55_duplicate_share.sql') { docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f ("/app/sql/analysis/$script") }`. The loop stops on the first failure because each call includes `ON_ERROR_STOP=1`.

**How can I regenerate the Task 03 CSV exports without storing credentials locally?** – Keep the stack running and execute the inline Python helper inside the `app` container so it reuses the `.env` secrets: `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python - <<'PY' ... PY` (see the Task 03 note for the exact snippet). The script reads each SQL file, runs it against Postgres, and saves fresh CSVs to `outputs/phase05_step02_task03/`.

## CLI / environment

**What commands should I run for any Phase 02 → Step 01 task?** – Always start with:

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Swap the module name or flags as needed, but keep the structure so the bind mount and container context stay consistent.

**How do I capture logs for later documentation?** – Pipe the command through `tee` inside the container (e.g., `python -m ... | tee /app/outputs/task03.log`) or copy/paste from the terminal immediately after the run. Mention the date/time in your notes so reviewers know which log you referenced.

## Keeping this FAQ updated

Whenever you repeat the same explanation in more than one task note, migrate it here instead and link back to the relevant question. That keeps the task notes focused while ensuring beginners always know where to look for deeper answers.
