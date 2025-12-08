# Phase 03 · Step 03 · Task 01 — Missing Values & Duplicate Scan (Run: 2025-12-04)

## 1. Task definition and goal

- Quantify missingness in the Goodreads Phase 02 export so downstream teams know whether additional imputations are needed.
- Detect partial duplicate clusters (multi-format releases, translations) and create a canonical mapping that keeps future facts from double-counting.
- Capture every step (Python CLI, Docker commands, SQL checks) for beginner-friendly reproducibility.

## 2. How to run this analysis script

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate
```

Optional local venv run:

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books --output-dir outputs/phase03_univariate
```

### Estimated runtime & success checks

- **Runtime:** ≈5 minutes in Docker (includes duplicate scans + Postgres writes); ≈4 minutes via local venv.
- **Success checklist:**
  - CLI log mentions `Saved missing-value summary ...`, `Full row duplicates identified: 0`, and `Saved ... partial duplicates ...` plus mapping creation lines.
  - `outputs/phase03_univariate/step03_task01_missing_duplicates/` contains the three CSV evidence files.
  - `data/derived/duplicate_bookid_mapping.csv` refreshes and, if you run the loader, `SELECT COUNT(*) FROM bookid_canonical_map;` returns 16.

## 3. Environment recap

- Data: `data/books.csv` (Phase 02 output) with derived artifacts in `data/derived/`.
- Outputs: `outputs/phase03_univariate/step03_task01_missing_duplicates/` for evidence CSVs.
- Postgres: `goodreads_books_analytics_postgres` (exposed at `localhost:5491`) + `DATABASE_URL=postgresql+psycopg2://goodreads_user:<password>@localhost:5491/goodreads` set in PowerShell.
- Tooling: `src/analyses/eda_books.py`, `src/load_duplicate_mapping.py`, `sql/create_books_canonical_view.sql`.

## 4. Findings / results

### Missing values

| Column             | Missing Rows | % of Dataset | Notes                              |
| ------------------ | -----------: | -----------: | ---------------------------------- |
| `publication_year` |            2 |       0.018% | Parsing failed but raw dates exist |

- All other columns report 0 missing entries. See `missing_values_summary.csv` for the full column list sorted by `% missing`.

### Duplicate scan

- Full-row duplicates: **0** (Phase 02 dedupe still holds).
- Partial duplicates (`title`, `authors`, `publication_date` normalized via `fillna('Unknown')/strip`): **31 rows**, covering audiobooks and translations (`The Da Vinci Code`, `The Shining`, `Cien años de soledad`, etc.).
- Evidence: `partial_duplicates_by_subset.csv` + `duplicate_summary.csv`.

### Duplicate → canonical mapping

- Created with pandas `groupby(...).transform('min')` to pick the lowest `bookID` per cluster; saved under `data/derived/duplicate_bookid_mapping.csv` (16 rows).
- Loaded into Postgres using `python -m src.load_duplicate_mapping --table bookid_canonical_map` (default `if_exists=replace`).
- Verification (2025-12-04):
  ```
  docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
    psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) FROM bookid_canonical_map;"
   count
  -------
      16
  (1 row)
  ```

### Canonical view

- Executed `\i sql/create_books_canonical_view.sql` inside `psql`, which exposes `canonical_book_id`, `original_book_id`, and all book columns.
- Row count: `SELECT COUNT(*) FROM books_canonical_v;` ⇒ **11,119** (base table has 11,127 rows; eight duplicates collapsed).
- Duplicate inspection:
  ```
  SELECT canonical_book_id, COUNT(*) AS row_count, MIN(title) AS sample_title
  FROM books_canonical_v
  GROUP BY canonical_book_id
  HAVING COUNT(*) > 1
  ORDER BY row_count DESC;
  ```
  → Only three canonical IDs remain with two rows apiece (`21665` “The Best American Mystery Stories 2004”, `12682` “The Shining”, `5414` “'Salem's Lot”). Downstream aggregations should group on `canonical_book_id` to avoid double counts.

## 5. Expected output checkpoints

- CLI logs: `Loaded 11127 rows after skipping 0 malformed entries`, `Saved missing-value summary ...`, `Full row duplicates identified: 0`, `Saved 31 partial-duplicate rows ...`.
- Mapping loader: `Loaded 16 duplicate→canonical pairs`, `Wrote 16 rows into table bookid_canonical_map (if_exists=replace)`.
- SQL: `SELECT COUNT(*) FROM bookid_canonical_map;` ⇒ 16, `SELECT COUNT(*) FROM books_canonical_v;` ⇒ 11119, `GROUP BY canonical_book_id HAVING COUNT(*)>1` ⇒ three IDs only.

## 6. Observations / insights

- Publication dates are intact; the two `publication_year` gaps stem from parse glitches, not missing source data.
- Duplicate pressure is small but concentrated in marquee titles; canonical IDs keep leaderboards honest without deleting raw rows.
- Housing the mapping in both CSV and Postgres keeps notebooks, dashboards, and SQL views aligned.

## 7. Artifacts refreshed each run

- `outputs/phase03_univariate/step03_task01_missing_duplicates/missing_values_summary.csv`
- `outputs/phase03_univariate/step03_task01_missing_duplicates/duplicate_summary.csv`
- `outputs/phase03_univariate/step03_task01_missing_duplicates/partial_duplicates_by_subset.csv`
- `data/derived/duplicate_bookid_mapping.csv`
- Postgres table `bookid_canonical_map`
- Postgres view `books_canonical_v`

## 8. Q&A / data troubleshooting

- **Where is the canonical mapping CSV?** `data/derived/duplicate_bookid_mapping.csv` (regenerate via pandas helper, then reload with `src/load_duplicate_mapping.py`).
- **How do I reapply the SQL without copying files?** From the repo root: `docker compose ... exec postgres psql -U goodreads_user -d goodreads -f sql/create_books_canonical_view.sql` (volumes already mount `/app`).
- **What if new duplicates appear after a data refresh?** Rerun the CLI, rebuild the mapping CSV, reload it into Postgres, rerun the view script, and re-check the row counts. Update `docs/data-faq.md` if the new pattern becomes recurring.

## 9. Checklist review

- [x] Missingness profile captured and exported.
- [x] Partial duplicate subset analyzed and logged.
- [x] Duplicate→canonical CSV generated and loaded into Postgres.
- [x] `books_canonical_v` view created and verified with SQL counts.
- [x] Documentation (notes + FAQ + glossary) updated with findings and commands.

## 10. Appendices

### Key commands (2025-12-04)

```powershell
# Run EDA CLI
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate

# Load mapping into Postgres
python -m src.load_duplicate_mapping --table bookid_canonical_map

# SQL verifications
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) FROM bookid_canonical_map;"
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) FROM books_canonical_v;"
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT canonical_book_id, COUNT(*) AS row_count, MIN(title) AS sample_title FROM books_canonical_v GROUP BY canonical_book_id HAVING COUNT(*) > 1 ORDER BY row_count DESC;"
```

### Mapping refresh checklist

1. Rerun the CLI to refresh `partial_duplicates_by_subset.csv`.
2. Rebuild `data/derived/duplicate_bookid_mapping.csv` with the pandas helper.
3. `python -m src.load_duplicate_mapping --table bookid_canonical_map` (Docker or venv).
4. `docker compose ... exec postgres psql ... "SELECT COUNT(*) FROM bookid_canonical_map;"` → confirm 16+ rows.
5. `\i sql/create_books_canonical_view.sql` to refresh the view if schema changed.
6. Update these notes + `docs/data-faq.md` if new caveats appear.

# Phase 03 · Step 03 · Task 01 — Missing Values & Duplicate Scan

## Objective

- Quantify column-level missingness to confirm Phase 02 outputs are production-ready.
- Flag both full-row duplicates and softer duplicate clusters (same title/author/date) so the data-cleaning phase knows what to reconcile.
- Keep everything reproducible through the `src/analyses/eda_books.py` CLI and capture evidence for the portfolio docs/FAQ/glossary.

## How to Reproduce

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books --output-dir outputs/phase03_univariate
```

The command refreshes every artifact under `outputs/phase03_univariate/`. Task 01 results live in the new `step03_task01_missing_duplicates/` subfolder.

## Missing Values Findings

| Column             | Missing Rows | % of Dataset | Notes                                                                                             |
| ------------------ | -----------: | -----------: | ------------------------------------------------------------------------------------------------- |
| `publication_year` |            2 |       0.018% | These rows lost their year when `publication_date` was parsed. Everything else has full coverage. |

- The raw `publication_date` column itself has 0 blanks, so future fixes can focus on re-parsing edge-case strings (e.g., month-only timestamps).
- No action needed for other columns; every metric used in Phase 03 charts is already complete.

Artifacts: `outputs/phase03_univariate/step03_task01_missing_duplicates/missing_values_summary.csv` (sorted by `% missing`).

## Duplicate Findings

- **Full-row duplicates:** 0 — the deduplication done in Phase 02 held up.
- **Partial duplicates (title + authors + publication_date):** 31 rows, clustered around multi-format releases (hardcover vs audiobook) and translation variants. Examples include `The Da Vinci Code` (print vs audiobook), `The Shining` (narrated editions), and `Cien años de soledad` (duplicate Spanish entries).
- Evidence files:
  - `duplicate_summary.csv` – quick counts for each duplicate type.
  - `partial_duplicates_by_subset.csv` – concrete rows with `bookID` so downstream scripts can decide which record to keep.
  - `data/derived/duplicate_bookid_mapping.csv` – duplicate → canonical pairs generated by grouping the partial subset and keeping the lowest `bookID` in each cluster.

### Recommendations

1. Treat the 31-row subset as candidates for consolidation in Phase 04+ (pick a canonical `bookID` per story, leave alternates in a companion table if narration/publisher differences still matter).
2. When creating features that rely on unique books (e.g., best-seller league tables), aggregate by `(title, authors, publication_year)` to avoid inflating counts.
3. Before loading Postgres tables, ingest `data/derived/duplicate_bookid_mapping.csv` into a staging table (e.g., `bookid_canonical_map`) and `LEFT JOIN` it so downstream facts always roll up to the canonical IDs.

### Mapping Generation Details

The mapping CSV is produced by `pandas` logic that:

1. Loads `partial_duplicates_by_subset.csv`.
2. Uses `groupby(['title','authors','publication_date']).transform('min')` to mark the canonical `bookID` (lowest value) for each cluster.
3. Filters out the canonical rows and writes the remaining duplicate IDs with their canonical partner plus context columns.

The resulting 16-row CSV is committed under `data/derived/duplicate_bookid_mapping.csv`. Treat it as an input file for Phase 04 ETL jobs; regenerate it whenever the duplicate sample file changes and re-ingest the refreshed mapping table.

### Loading the Mapping into Postgres

- Venv run: `python -m src.load_duplicate_mapping --table bookid_canonical_map`
- Docker run: `docker compose -f docker-compose.python.yml exec app python -m src.load_duplicate_mapping --table bookid_canonical_map`

The script validates the CSV columns, then writes them into PostgreSQL (default `replace`). Reference the table in SQL with:

```sql
SELECT COALESCE(m.canonical_bookid, b.book_id) AS canonical_book_id,
       b.*
FROM books b
LEFT JOIN bookid_canonical_map m
  ON b.book_id = m.duplicate_bookid;
```

Use this pattern in Phase 04 fact views so every duplicate rolls up to its canonical counterpart without deleting the source rows.

**Verification Log (2025-12-04)**

```
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) FROM bookid_canonical_map;"
 count
-------
    16
(1 row)
```

The query confirms the canonical map is present in Postgres with the expected rowcount before any Phase 04 ETL job consumes it.

### Canonical View for Downstream Queries

Execute `i sql/create_books_canonical_view.sql` inside `psql` (or run the statements manually) to create `books_canonical_v`. The view exposes both the canonical ID and original `book_id`, so analysts can join to the view instead of remembering the `LEFT JOIN` logic each time.

**Canonical View Verification (2025-12-04)**

```
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT COUNT(*) FROM books_canonical_v;"
 count
-------
 11119
(1 row)
```

The base `books` table holds 11,127 rows, so the view removes 8 records by rolling duplicates under their canonical IDs.

```
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres \
  psql -U goodreads_user -d goodreads -c "SELECT canonical_book_id, COUNT(*) AS row_count, MIN(title) AS sample_title FROM books_canonical_v GROUP BY canonical_book_id HAVING COUNT(*) > 1 ORDER BY row_count DESC LIMIT 5;"
 canonical_book_id | row_count |          sample_title
-------------------+-----------+-------------------------------------
             21665 |         2 | The Best American Mystery Stories 2004
             12682 |         2 | The Shining
              5414 |         2 | 'Salem's Lot
(3 rows)
```

Only three canonical IDs surface with two rows each (audiobook vs print). Aggregations should group on `canonical_book_id` to avoid reintroducing those duplicates.

### Mapping Refresh Checklist

Run this list whenever duplicate analysis is rerun or the CSV changes:

1. Rebuild `data/derived/duplicate_bookid_mapping.csv` via the pandas helper (see earlier "Mapping Generation" section).
2. `python -m src.load_duplicate_mapping --table bookid_canonical_map` (or Docker equivalent) after confirming `DATABASE_URL` targets the correct environment.
3. `docker compose ... exec postgres psql ... "SELECT COUNT(*) FROM bookid_canonical_map;"` to confirm the expected rowcount.
4. Re-run `\i sql/create_books_canonical_view.sql` if the view exists but needs to pick up renamed columns or schema tweaks.

## Next Steps / Hand-off

- Link this note (plus the FAQ + glossary updates) in the Phase 03 status doc so reviewers can trace data-quality sign-off.
- If we later import Goodreads updates, rerun the same CLI command and diff the new CSVs to spot regressions quickly.
