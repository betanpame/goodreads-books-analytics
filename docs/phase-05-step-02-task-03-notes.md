# Phase 05 · Step 02 · Task 03 – Advanced SQL windowing & percentiles

## 1. Task definition and goal

Translate the "advanced SQL" plan items (top books per author, language/publisher standings, and rolling publication trends) into executable PostgreSQL scripts that rely on window functions, canonical rollups, and percentile math. Success means:

- `sql/analysis/60_*.sql`, `70_*.sql`, and `80_*.sql` all run inside Docker with `ON_ERROR_STOP=1` and reuse the canonical book pattern established in earlier tasks.
- Each query explains how we cap engagement metrics, enforce author/language minimums, and compute rolling windows without leaving SQL.
- Outputs are captured as CSVs under `outputs/phase05_step02_task03/` so recruiters can download raw evidence without running Postgres.
- This note plus the FAQ/Glossary update show exactly how the windowing/percentile pieces fit into the broader analytics story.

## 2. Step-by-step execution guide

### Quick-run overview (TL;DR)

| Step | Command                                                                                                                         | Expected signal                                           |
| ---- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 1    | `cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`                                                                  | Prompt switches to repo root.                             |
| 2    | `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`                                            | `docker compose ... ps` shows `app` + `postgres` as `Up`. |
| 3    | `docker compose ... exec postgres ls /app/sql/analysis \| findstr 6`                                                            | Numbered `60_`, `70_`, `80_` scripts are visible.         |
| 4    | `.\scripts\Invoke-Task03Run.ps1` or `.\scripts\Invoke-Task03Run.ps1 -Script 70`                                                 | Helper runs all or specific scripts via Docker.           |
| 5    | (Manual alternative) `docker compose ... exec -e PAGER=cat postgres psql -q -v ON_ERROR_STOP=1 -f /app/sql/analysis/<file>.sql` | Tables show documented row counts.                        |
| 6    | Export evidence via `\copy` or the Python helper in Section 3.                                                                  | CSVs appear under `outputs/phase05_step02_task03/`.       |

### 2.1 Prepare the Docker/Postgres stack (run once per session)

1. From the repo root start both services so the repo is mounted under `/app` inside each container:
   ```powershell
   cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   ```
2. Confirm Postgres can see the SQL directory:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres ls /app/sql/analysis
   ```
   You should see the numbered scripts (`60_*.sql`, `70_*.sql`, `80_*.sql`, …). If the folder is missing, rebuild the container with `--force-recreate`.

### 2.2 Run each analysis script interactively (psql route)

Use the same base command and swap only the file name:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat postgres `
	 psql -q -v ON_ERROR_STOP=1 -U goodreads_user -d goodreads `
	 -f /app/sql/analysis/<file>.sql
```

| Purpose                                 | `<file>` value                          | Expected row count                |
| --------------------------------------- | --------------------------------------- | --------------------------------- |
| Author top-N with dual window functions | `60_top_books_per_author.sql`           | 75 rows (25 authors × 3 books)    |
| Language + publisher standings          | `70_language_publisher_rankings.sql`    | 9 rows today (5 `eng`, 4 `en-US`) |
| Publication-year rolling stats          | `80_publication_year_rolling_stats.sql` | 26 rows (1995–2020)               |

**Parameter tweaks:** Each script starts with a `params` CTE. Adjust the literal values there (e.g., change `per_author_limit`, `min_total_ratings`, `min_canonical_books`, or `min_year`) and rerun the same command. No other clause editing required.

### 2.3 PowerShell helper (Invoke-Task03Run)

To avoid retyping compose/psql flags, use the bundled helper:

```powershell
# Run all Task 03 scripts in numeric order
./scripts/Invoke-Task03Run.ps1

# Run a single script (aliases: 60/authors, 70/publishers, 80/rolling)
./scripts/Invoke-Task03Run.ps1 -Script 70
./scripts/Invoke-Task03Run.ps1 -Script authors,rolling
```

The function wraps the same Docker command used elsewhere (`PAGER=cat`, `-q`, `ON_ERROR_STOP=1`). It stops on the first failure and prints a green “completed” line when all requested scripts succeed.

> **Execution policy note:** Windows blocks unsigned scripts by default. If you see `running scripts is disabled on this system`, rerun with `powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Task03Run.ps1 -Script all` (or set a less restrictive policy for the current process scope).

### 2.4 Optional: Run once and stay inside psql

If you prefer a single `psql` session:

1. Open the shell:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads
   ```
2. Inside `psql`, execute the scripts in numeric order with `\i sql/analysis/60_top_books_per_author.sql` (the repo is mounted at `/app`).
3. Type `\q` to exit.

### 2.5 Export results to CSV for documentation

Use either approach:

1. **psql \copy** (pure SQL):
   ```powershell
   docker compose ... exec postgres psql -q -U goodreads_user -d goodreads -c "\\copy (\
   	 \i /app/sql/analysis/70_language_publisher_rankings.sql
   ) TO '/app/outputs/phase05_step02_task03/70_language_publisher_rankings.csv' WITH CSV HEADER"
   ```
2. **Python helper (used for this task):** see Section 3 for the psycopg2+pandas snippet that writes `outputs/phase05_step02_task03/*.csv` directly.

Either path keeps the evidence in-source so future reviewers can diff the raw outputs.

## 3. Fresh CSV artifacts

| Description                                          | Path                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------- |
| Author leaderboard slices (top 25 × 3 books)         | `outputs/phase05_step02_task03/60_top_books_per_author.csv`           |
| Language + publisher standings (post-filtered top-N) | `outputs/phase05_step02_task03/70_language_publisher_rankings.csv`    |
| Publication-year rolling stats (1995–2020 coverage)  | `outputs/phase05_step02_task03/80_publication_year_rolling_stats.csv` |

The CSVs were regenerated with this repeatable snippet (run from the repo root after starting Docker):

```python
from pathlib import Path
import pandas as pd
import psycopg2

conn = psycopg2.connect(host="localhost", port=5491, dbname="goodreads", user="goodreads_user", password="<password>")
for sql_name in [
   "60_top_books_per_author.sql",
   "70_language_publisher_rankings.sql",
   "80_publication_year_rolling_stats.sql"
]:
	sql = Path("sql/analysis") / sql_name
	df = pd.read_sql_query(sql.read_text(encoding="utf-8"), conn)
	out = Path("outputs/phase05_step02_task03") / sql_name.replace(".sql", ".csv")
	out.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(out, index=False)
conn.close()
```

Swap in the password from `.env` or run inside the `app` container where environment variables are already available.
To run the same snippet without storing credentials locally:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python - <<'PY'
from pathlib import Path
import pandas as pd
import psycopg2
import os

conn = psycopg2.connect(host=os.environ['PGHOST'], port=os.environ['PGPORT'],
						dbname=os.environ['PGDATABASE'], user=os.environ['PGUSER'],
						password=os.environ['PGPASSWORD'])
for sql_name in [
   "60_top_books_per_author.sql",
   "70_language_publisher_rankings.sql",
   "80_publication_year_rolling_stats.sql"
]:
	sql = Path("sql/analysis") / sql_name
	df = pd.read_sql_query(sql.read_text(encoding="utf-8"), conn)
	out = Path("outputs/phase05_step02_task03") / sql_name.replace(".sql", ".csv")
	out.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(out, index=False)
conn.close()
PY

**Latest refresh:** Ran the containerized snippet above on `2025-12-05 14:04:14 -06:00` after executing all three SQL scripts interactively. The command re-generated the three CSV artifacts listed in the table (see PowerShell history for the full `docker compose ... exec app bash -lc` invocation).
```

Finish by running `dir outputs\phase05_step02_task03` (Windows) or `ls outputs/phase05_step02_task03` (inside the container) to confirm both CSVs exist.

## 4. Findings & highlights

| Query                                   | What it measures                                                                                                                                                    | Key numbers from this run                                                                                                                                                                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `60_top_books_per_author.sql`           | Uses `ROW_NUMBER()` twice—once per author (top 3 books) and once globally (top 25 authors with ≥5,000 capped ratings).                                              | Stephen King leads with 3.9M capped ratings; Rowling, Shakespeare, and Nicholas Sparks fill the next slots. Output shows 75 rows (25 authors × 3 books), proving the per-author and global limits work in tandem.                                           |
| `70_language_publisher_rankings.sql`    | Filters publishers that ship ≥20 canonical titles per language, then ranks them via `RANK()` using average rating + 75th percentile engagement.                     | For English, Library of America (47 canonicals, avg 4.29, p75 527) and VIZ Media LLC (76, 4.28, p75 10,455) take the top spots. US-English surfaces HarperCollins (20, 4.07), Mariner Books (26, 4.01), Penguin Books (22, 3.88), and Tor Books (24, 3.77). |
| `80_publication_year_rolling_stats.sql` | Aggregates per-year averages + medians, then computes 3-year rolling averages and year-over-year deltas using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` + `LAG()`. | Coverage spans 1995–2020 (26 rows). Early years average ~3.95 rating with median engagement in the 600s; 2018 shows the only positive YoY bump (+0.1469) before ratings descend again. Rolling medians stay smooth despite thin late-year cohorts.          |

**Verification checklist after each run:**

1. Confirm column headers match the `SELECT` clause (especially `author_rank`, `author_leaderboard_rank`, `language_rank`, and the rolling metrics).
2. Spot-check at least one row per script:
   - Author script: verify that `author_rank` never exceeds 3 and that `total_ratings` matches the aggregated sum for that author (e.g., Stephen King shows 3.9M capped ratings across his rows).
   - Publisher script: ensure every row’s `canonical_book_count` ≥ 20 and that ranks reset within each language partition.
   - Rolling script: confirm the first row has `avg_rating_delta_vs_prior_year = NULL` and that rolling averages start filling in on the third year (due to the 3-year window).

## 5. Execution checkpoints

- ✅ **Exit codes:** Each `psql -f` command includes `-v ON_ERROR_STOP=1`, so any SQL issue halts immediately. Rerun the command after fixing the script to confirm a zero exit status.
- 🔢 **Row counts:**
  - `60_...`: row count should equal `per_author_limit × max_authors`. If you set `per_author_limit=5` and `max_authors=30`, expect 150 rows.
  - `70_...`: row count equals `(number of languages that meet the canonical threshold) × per_language_limit`. Currently 2 languages × 5 ranks = 10, but one rank slot is unused, so 9 rows output.
  - `80_...`: row count equals `2020 - min_year + 1` as long as each year has data. If you lower `min_year` to 1985, expect 36 rows.
- 🧪 **Filters firing:** In `70_...`, verify the `eligible_publishers` CTE (added this task) actually removes one-book outliers by temporarily lowering `min_canonical_books` to 1—ranks will suddenly fill with perfect scores, proving the filter matters.
- 📈 **Rolling metrics:** In `80_...`, check that `avg_rating_rolling_3yr` for 1997 equals the mean of 1995–1997 results. This quick calculation confirms the window frame is applied correctly.

## 6. Window & percentile callouts

- **Author ranking:** `ROW_NUMBER()` partitions by `author_name` to keep only the top 3 per author, while another `ROW_NUMBER()` over the aggregate leaderboard enforces the "top 25" global slice. Because parameters live in the `params` CTE, analysts can scale either constraint up or down.
- **Percentiles in Postgres:** `percentile_cont(0.75) WITHIN GROUP (ORDER BY ratings_count_capped)` gives a resistant engagement metric per language/publisher pair, mirroring pandas’ quantile logic without exporting data.
- **Rolling windows:** Publication stats use `AVG(...) OVER (ORDER BY publication_year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` plus `LAG()` to keep all smoothing inside SQL. This matches the pandas rolling window we shared earlier, but it is reproducible straight from the database.

## 7. Artifacts touched

- `sql/analysis/70_language_publisher_rankings.sql` (pre-filter step moved ahead of `RANK`).
- `sql/analysis/80_publication_year_rolling_stats.sql` (validated, no logic changes).
- `outputs/phase05_step02_task03/*.csv` (new evidence for this task).
- `docs/data-faq.md` (new FAQ entries describing the Task 03 exports and publisher-threshold guidance).
- `docs/phase-05-glossary.md` (definitions for `author_leaderboard_rank`, capped engagement percentiles, and rolling 3-year windows).

## 8. FAQs addressed in this task

| Question                                                       | Answer                                                                                                                                                                                                                                  |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| How do I grab these SQL outputs without `psql \copy`?          | Use the documented Python snippet (psycopg2 + pandas) or rerun `python -m src.analyses.export_sql --query-path sql/analysis/70_*.sql --output outputs/phase05_step02_task03/...`. The FAQ now links to the ready-made CSVs.             |
| Why do only English variants appear in the publisher rankings? | The dataset only has ≥20 canonical titles for `eng` and `en-US`. Lower thresholds can be tested by editing the `params` CTE, but the documented outputs keep the stricter filter to avoid misleading one-book leaderboards.             |
| How should I describe the rolling metrics in the portfolio?    | Call out that they are pure SQL calculations using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` and `LAG()`. The note, FAQ, and glossary all highlight this so stakeholders see we can work natively in Postgres without pandas crutches. |

---

These results, CSVs, and documentation entries complete Phase 05 · Step 02 · Task 03 and set the stage for reusing the advanced SQL patterns in dashboards or stored procedures.
