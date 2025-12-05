# Phase 05 · Step 02 · Task 02 – Translate Core Metrics to SQL Queries

## 1. Task definition and goal

Implement the plan’s "translate core metrics to SQL" checklist by recreating the Phase 04 core KPIs (M1, M3, M4, M7, M8, M9, M11) directly in PostgreSQL. The deliverable is a numbered set of SQL scripts under `sql/analysis/` that anyone can run inside Docker to answer the same business questions without pandas. Success means each script is documented, parameterized, duplicate-aware, and produces the same story we already published from the Python pipeline.

## 2. How to run the analysis scripts

### 2.1 Quick-start runbook

| Step                 | Command                                                                                                                                                           | Expected outcome                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 1. Navigate + start  | `cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`<br>`docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`            | `docker compose ... ps` shows `app` and `postgres` as `Up`.          |
| 2. Mount check       | `docker compose ... exec postgres ls /app/sql/analysis`                                                                                                           | Lists `20_*.sql` through `55_*.sql`.                                 |
| 3. Single-script run | `docker compose ... exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f /app/sql/analysis/20_top_authors_weighted_rating.sql` | Table output plus `(15 rows)` footer; exit code 0.                   |
| 4. Multi-script loop | `foreach($id in 20,30,40,50,55) { docker compose ... -f ("/app/sql/analysis/${id}_*.sql") }`                                                                      | All scripts run sequentially; stop immediately if a statement fails. |
| 5. Evidence capture  | `\copy (SELECT ...) TO '/app/outputs/...csv' WITH CSV HEADER` or rerun via pandas (`python -m src.analyses.export_sql ...`).                                      | CSV saved under `outputs/phase05_step02_task02/` (optional).         |

### 2.2 Detailed workflow

1. **Start from the repo root and boot the stack** so the bind mount exposes `sql/` inside the Postgres container (new in this task):

   ```powershell
   cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml ps
   ```

   Wait for both services to display `Up`. If the Postgres container was recreated, re-run the schema scripts from Task 01 before proceeding.

2. **Run each metric script with `psql` in quiet mode**. The repo now mounts at `/app`, so every file can be executed with a single command plus `ON_ERROR_STOP=1` for CI parity:

   | Metric(s)                           | SQL file                                          | Command                                                                                                                                                                                                                     |
   | ----------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | M1 – Weighted author leaderboard    | `sql/analysis/20_top_authors_weighted_rating.sql` | `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f /app/sql/analysis/20_top_authors_weighted_rating.sql` |
   | M3 & M4 – Canonical book engagement | `sql/analysis/30_top_books_by_engagement.sql`     | same command with the corresponding path                                                                                                                                                                                    |
   | M7 & M8 – Publication-year trends   | `sql/analysis/40_publication_year_trends.sql`     | …                                                                                                                                                                                                                           |
   | M9 – Language quality & reach       | `sql/analysis/50_language_quality_summary.sql`    | …                                                                                                                                                                                                                           |
   | M11 – Duplicate share               | `sql/analysis/55_duplicate_share.sql`             | …                                                                                                                                                                                                                           |

   PowerShell automation keeps the commands short:

   ```powershell
   foreach($script in '20_top_authors_weighted_rating.sql','30_top_books_by_engagement.sql','40_publication_year_trends.sql','50_language_quality_summary.sql','55_duplicate_share.sql') {
     docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
       postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads -f ("/app/sql/analysis/$script")
   }
   ```

3. **Interactive option:** open `psql` once and call `\i sql/analysis/<file>.sql` in numeric order. The `.:/app:ro` mount we added to both Compose files makes the repo visible under `/app` for this workflow. Run `\timing on` before the `\i` commands if you want duration metadata for the notes.

4. **Capture outputs** (either copy/paste the terminal tables or redirect to CSV via `\copy`) so task notes and portfolio artifacts always cite verifiable SQL evidence. Inside `psql`, paste the final `SELECT` from the script inside a `\copy` wrapper, for example:

   ```psql
   \copy (
      WITH params AS (...),
              books_with_canonical AS (...),
              author_rollup AS (...)
      SELECT *
      FROM author_rollup
      WHERE total_ratings >= (SELECT min_total_ratings FROM params)
      ORDER BY weighted_average_rating DESC, total_ratings DESC
      LIMIT (SELECT top_n FROM params)
   ) TO '/app/outputs/phase05_step02_task02/M1_top_authors.csv' WITH CSV HEADER
   ```

   Paste the full text from the SQL file (including the `WITH` block) in place of the ellipses so `psql` runs the identical statement it used for the on-screen results.

   Prefer the lighter pandas export by running `python -m src.analyses.export_sql --query-path sql/analysis/<file>.sql --output outputs/phase05_step02_task02/<file>.csv` inside the `app` container when you need artifacts for multiple scripts. That helper automatically pulls credentials from the `.env` file.

## 3. Environment recap

- **Docker services:** `app` (Python 3.14, pandas CLI) and `postgres` (PostgreSQL 17). Both Compose files now mount the repo read-only into `/app`, unlocking the documented `\i sql/...` workflow.
- **Schemas/tables:** `books` (cleaned Goodreads export), `book_authors_stage` (row-per-author staging table created by `load_books_to_postgres`), and `bookid_canonical_map` (duplicate→canonical pairs). Queries stay in the `public` schema.
- **Canonical rollup pattern:** every analysis script builds a `books_with_canonical` CTE that coalesces duplicate IDs, picks one textual representative via `DISTINCT ON`, and aggregates max engagement counts before applying caps (`ratings_count` ≤ 597,244, `text_reviews_count` ≤ 14,812).
- **Execution flags:** `PAGER=cat` removes Alpine’s `TURN` warning, `-q` trims banners, and `-v ON_ERROR_STOP=1` stops immediately if a query fails so the CI transcript doubles as acceptance evidence.

## 4. Findings / results

| Metric                            | SQL file                             | Highlight from this run                                                                                                                                                                                              | Notes                                                                                                                                                                                     |
| --------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M1 – Weighted authors             | `20_top_authors_weighted_rating.sql` | Bill Watterson tops the list at **4.7137** weighted rating across 144,799 ratings (7 canonical titles).                                                                                                              | Manga localization teams (Kelly Jones, Lee Loughridge, Matt Thorn…) dominate the rest of the top 10, matching the pandas narrative about page-turner bias. Minimum ratings floor = 5,000. |
| M3 – Top books by ratings         | `30_top_books_by_engagement.sql`     | `Twilight` still leads with **4.60M** raw ratings (capped to the 597,244 storytelling ceiling).                                                                                                                      | Leaderboard mirrors the Phase 04 CSV output: Potter, Tolkien, and school staples round out the top 20.                                                                                    |
| M4 – Top books by text reviews    | same as above                        | Written discussion is led by `Twilight` (94,265 reviews), `The Book Thief` (86,881), and `The Giver` (56,604).                                                                                                       | SQL unioned both leaderboards into one result set with a `metric` label so dashboards can consume them together.                                                                          |
| M7 – Average rating by year       | `40_publication_year_trends.sql`     | 1984–1991 stay above **4.00** average, dipping toward **3.91** after the 2006 blockbuster surge.                                                                                                                     | Script filters to years ≥1950 (configurable) and keeps canonical deduping so audiobook variants don’t skew medians.                                                                       |
| M8 – Median ratings count by year | same file                            | Median capped engagement crosses **1,697** in 2006 and spikes to **2,530** for the small 2012 cohort, matching the "all-or-nothing" modern release pattern.                                                          | Uses `percentile_cont(0.5)` directly in SQL to recreate the pandas median.                                                                                                                |
| M9 – Language summary             | `50_language_quality_summary.sql`    | Only six languages meet the ≥50 canonical-book threshold; **fre** (144 titles) leads with avg rating 3.9715 but tiny medians, while English variants carry the audience scale (median capped ratings 532 for en-US). | Threshold controlled by the `params` CTE; table lists coverage + quality for quick storytelling.                                                                                          |
| M11 – Duplicate share             | `55_duplicate_share.sql`             | Exactly **16** duplicates → **0.1439%** of the catalog, reinforcing why canonical IDs stay mandatory.                                                                                                                | Derived straight from `bookid_canonical_map` so any mapping edits reflect here automatically.                                                                                             |

All SQL numbers line up with the previously published pandas metrics, so reviewers can trust either toolchain.

## 5. Expected output checkpoints

- Each `psql -f /app/sql/analysis/<file>.sql` command exits with code 0 thanks to `ON_ERROR_STOP=1`.
- `20_top_authors_weighted_rating.sql` returns exactly 15 rows (top_n default).
- `30_top_books_by_engagement.sql` prints two 20-row blocks labeled `ratings_count` and `text_reviews`.
- `40_publication_year_trends.sql` emits 70 rows (1950–2020 range) and shows medians ≥1,000 for all post-1998 years.
- `50_language_quality_summary.sql` lists six languages after applying the min-book filter.
- `55_duplicate_share.sql` displays `total_rows=11119`, `duplicate_rows=16`, `duplicate_share_pct=0.1439`.

## 6. Observations / insights

- Mounting the repo read-only inside the Postgres container removed the awkward STDIN piping workaround and made the documented `\i sql/...` instructions actually reproducible.
- Parameter-only changes (e.g., `top_n`, `min_year`, `min_book_threshold`) now live inside a `params` CTE at the top of every script, so analysts can tweak thresholds without digging through `GROUP BY` clauses.
- Leveraging `book_authors_stage` provided the same exploded author view we used in pandas, proving that our ingestion job already preserved the heavy-lifting needed for SQL-only analytics.
- Reusing the canonical rollup pattern keeps duplicate SKUs from double counting while still surfacing the highest observed engagement per canonical book.
- Added a dedicated `sql-smoke` job to GitHub Actions that loads the dataset nightly and runs every `sql/analysis/*.sql` file via `psql -f`, so regressions surface automatically without manual Docker sessions.

## 7. Artifacts refreshed this task

- `sql/analysis/20_top_authors_weighted_rating.sql`
- `sql/analysis/30_top_books_by_engagement.sql`
- `sql/analysis/40_publication_year_trends.sql`
- `sql/analysis/50_language_quality_summary.sql`
- `sql/analysis/55_duplicate_share.sql`
- `sql/README.md` (new analysis catalog table)
- `docker-compose.python.yml` + `docker-compose.postgresql.yml` (added `.:/app:ro` mount for `psql \i` workflow)
- `docs/data-faq.md` (Phase 05 SQL section)
- `docs/phase-05-glossary.md` (new entries for canonical SQL terms)
- This note (`docs/phase-05-step-02-task-02-notes.md`)

## 8. Q&A / troubleshooting

| Question                                                               | Answer                                                                                                                                                                                           |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **How do I change ranking thresholds without editing multiple lines?** | Edit the `params` CTE at the top of each SQL file (e.g., set `top_n` to 25 or `min_book_threshold` to 100) and rerun the same command block.                                                     |
| **Can I run everything in one go?**                                    | Yes—`for %f in (20 30 40 50 55) do docker compose ... -f /app/sql/analysis/%f_*.sql` works on Windows, or use a simple PowerShell loop. Keep `ON_ERROR_STOP=1` so the sequence halts on failure. |
| **What if Postgres says it can’t find `sql/...`?**                     | Make sure you restarted the stack after this task so the new `.:/app:ro` mount is in place. `docker compose ... exec postgres ls /app/sql/analysis` should list all scripts.                     |
| **Where do these SQL outputs feed back into the portfolio?**           | Reference this note plus the `sql/README.md` table, and link directly to the SQL files in GitHub. Screenshots aren’t necessary—the tables above already summarize the evidence.                  |

## 9. Checklist review (plan alignment)

- [x] Reviewed Phase 04 metric definitions and selected the core set (M1, M3, M4, M7, M8, M9, M11).
- [x] Designed canonical-friendly SQL equivalents with explicit filters, groupings, and caps.
- [x] Created separate, commented SQL files per analysis theme under `sql/analysis/`.
- [x] Executed every script in Docker and validated outputs against the pandas references.
- [x] Documented commands, findings, FAQs, and artifacts for portfolio readers.

## 10. Appendix – sample command log

```
$ docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat \
    postgres psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads \
    -f /app/sql/analysis/20_top_authors_weighted_rating.sql
     author_name     | weighted_average_rating | total_ratings | book_count
---------------------+-------------------------+---------------+------------
 Bill Watterson      |                  4.7137 |        144799 |          7
 Kelly Jones         |                  4.6500 |         15640 |          1
 ... (11 rows omitted for brevity) ...
(15 rows)
```

Use similar commands for every other SQL file; the logs shown in Section 4 were captured with the same structure.
