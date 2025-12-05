# SQL Workspace

Organizes every PostgreSQL artifact used in Phase 05. Scripts live in Docker-friendly folders so you can recreate the database schema and run portfolio-ready analysis queries from `psql` without guessing the order.

## Folder layout

- `schema/` – DDL, views, and other structural changes. Files use two-digit prefixes (`01_`, `02_`) so you can apply them in order.
- `analysis/` – Read-only queries, sanity checks, and reusable snippets for validation work. Numbering stays loose; lower numbers are foundational checks, higher numbers build on prior outputs.

Add new folders (e.g., `utils/`) only if a script category does not fit the two buckets above.

## Naming convention

1. Use a numeric prefix (`00`, `10`, `20`, …) to keep scripts sorted chronologically.
2. Describe the action in the filename: `01_create_books_table.sql`, `10_apply_canonical_bookid.sql`.
3. Begin every file with a short comment describing why it exists and which task/phase references it.

## Running scripts

All commands must run inside Docker so paths resolve to `/app/...` in the containers.

1. Ensure the stack is online:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   ```
2. Open an interactive `psql` session (pager disabled for clean logs):
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat \
       postgres psql -q -U goodreads_user -d goodreads
   ```
3. From inside `psql`, run scripts with `\i` and the repo-relative path:
   ```psql
   \i sql/schema/01_create_books_table.sql
   \i sql/schema/02_create_books_canonical_view.sql
   \i sql/analysis/00_sanity_checks.sql
   ```

Because the repository is mounted at `/app`, the relative `sql/...` paths resolve automatically. Repeat the pattern for any new scripts. If a script depends on environment variables or temp tables, document that inline at the top of the file.

## Example workflow

1. Create/refresh the books table.
2. Create the canonical view so duplicate mappings are always available.
3. Run `analysis/00_sanity_checks.sql` to confirm the row count, average rating, and top languages match the CSV evidence (11,119 rows, rating within 0–5, English dominating the language split).
4. Explore deeper helpers like `analysis/10_apply_canonical_bookid.sql` when building future metrics or ETL jobs.

Commit any new SQL alongside the task note that references it so reviewers can trace every analytic artifact back to a documented step.

## Analysis catalog (Phase 05 · Step 02 · Task 02)

| Script                                        | Business question / metric                                                                    | How to run                                                                          |
| --------------------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `analysis/20_top_authors_weighted_rating.sql` | M1 – weighted author leaderboard with a 5K ratings floor using `book_authors_stage`.          | `\i sql/analysis/20_top_authors_weighted_rating.sql` inside `psql`.                 |
| `analysis/30_top_books_by_engagement.sql`     | M3 & M4 – canonical books ranked by capped ratings/text reviews with duplicate-aware rollups. | Same `\i` pattern; returns two labeled leaderboards in one result set.              |
| `analysis/40_publication_year_trends.sql`     | M7 & M8 – publication-year averages + median engagement with a configurable minimum year.     | `\i sql/analysis/40_publication_year_trends.sql` (adjust `min_year` CTE as needed). |
| `analysis/50_language_quality_summary.sql`    | M9 – language quality + engagement summary with a minimum canonical book threshold.           | `\i sql/analysis/50_language_quality_summary.sql`.                                  |
| `analysis/55_duplicate_share.sql`             | M11 – duplicate share of the catalog sourced from `bookid_canonical_map`.                     | `\i sql/analysis/55_duplicate_share.sql`.                                           |

Each script defines its own parameters via a `params` CTE so you can raise thresholds (e.g., `min_book_threshold`) without editing multiple lines. Prefer running them from within Docker so the repo-relative paths resolve to `/app/sql/...` inside the container.
