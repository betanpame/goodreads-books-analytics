# Phase 05 · Step 02 · Task 01 – Set Up `sql/` Folder and Query Conventions

## 1. Task definition and goal

Translate the plan’s “set up sql folder and conventions” checklist into concrete assets: build a schema/analysis subfolder structure, migrate the existing DDL + helper scripts into that structure with numbered filenames, document execution order, and capture the canonical Docker/`psql` workflow. Success criteria: any teammate can clone the repo, run a single documented command block, and reproduce the schema plus sanity-check queries without guessing at file paths.

## 2. How to run the SQL scripts

### 2.1 Quick-start checklist (follow top-to-bottom)

| Step                  | Command                                                                                | What to see                                                         |
| --------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| 1. Navigate           | `cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`                         | Prompt shows repo root.                                             |
| 2. Start stack        | `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`   | `app` and `postgres` display as `Up` in `docker compose ps`.        |
| 3. Sanity check mount | `docker compose ... exec postgres ls /app/sql`                                         | Lists `schema/` and `analysis/`.                                    |
| 4. Open psql          | `docker compose ... exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads` | Prompt changes to `goodreads=#`.                                    |
| 5. Run scripts        | Inside `psql`: `\i sql/schema/01_create_books_table.sql`, etc.                         | Each script echoes `psql:...: command executed` plus result tables. |
| 6. Verify             | `SELECT COUNT(*) FROM books;`                                                          | Returns `11119`.                                                    |
| 7. Exit               | `\q`                                                                                   | Back to PowerShell prompt.                                          |

### 2.2 Detailed steps (with additional context)

1. **Start from the repo root** so the bind mount aligns with `/app` inside the containers:

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
```

2. **Boot (or restart) the shared Docker stack** whenever you start a new terminal session:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
```

Immediately follow up with `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml ps` and wait until both services show `Up`.

3. **Confirm Postgres can read the repo** (skip this check after the first success):

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres ls /app/sql/analysis
```

If the directory is missing, recreate the container (`... up -d --force-recreate postgres`).

4. **Open an interactive `psql` shell** with pagination disabled (eliminates the `TURN: No such file or directory` warning) and quiet output for clean transcripts:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
  postgres psql -q -U goodreads_user -d goodreads
```

Expected prompt: `goodreads=#`. If authentication fails, re-source `.env` or run `docker compose ... exec postgres env | findstr GOODREADS` to confirm credentials.

5. **Execute scripts from inside `psql`** using repo-relative paths (the repo mounts at `/app`). Run schema files before analysis files to keep dependencies aligned:

```psql
\i sql/schema/01_create_books_table.sql
\i sql/schema/02_create_books_canonical_view.sql
\i sql/analysis/00_sanity_checks.sql
```

Each `\i` prints `psql:...: command executed` plus any query output; capture these logs for documentation. After the schema is in place, quickly re-run `SELECT COUNT(*) FROM books;` to confirm the expected 11,119 rows.

6. **Leave the session or run scripts non-interactively** once you capture the outputs. For automation, feed the script directly without the interactive shell:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
  postgres psql -q -U goodreads_user -d goodreads -v ON_ERROR_STOP=1 -f /app/sql/analysis/00_sanity_checks.sql
```

Swap the file path for any script under `sql/schema/` or `sql/analysis/`. The `-v ON_ERROR_STOP=1` flag makes CI fail fast if any statement errors. Use PowerShell to loop through multiple files when needed:

```powershell
foreach($file in 'schema/01_create_books_table.sql','schema/02_create_books_canonical_view.sql','analysis/00_sanity_checks.sql') {
  docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
   postgres psql -q -U goodreads_user -d goodreads -v ON_ERROR_STOP=1 -f ("/app/sql/$file")
}
```

## 3. Environment recap

- **Containers:** `app` (Python 3.11, houses CLI modules) and `postgres` (PostgreSQL 17) orchestrated via `docker-compose.python.yml` + `docker-compose.postgresql.yml`.
- **Networking:** Both services share the default Compose network, so `app` reaches the database via `postgres:5432` using credentials stored in `.env` (`goodreads_user` / `goodreads`).
- **Bind mount:** Repo root → `/app` in both containers, enabling relative references like `sql/schema/...` without Windows paths.
- **`psql` defaults:** `PAGER=cat` prevents pager errors; `-q` trims banners; `-v ON_ERROR_STOP=1` (optional) enforces fail-fast behavior in automation.

## 4. Deliverables and results

| Deliverable                                     | Description                                                                                                                                                                  |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sql/schema/01_create_books_table.sql`          | Relocated the existing DDL into a numbered file; now the canonical entry point for recreating the `books` table.                                                             |
| `sql/schema/02_create_books_canonical_view.sql` | View definition that joins `books` to `bookid_canonical_map`; comments now include the exact `\i` path.                                                                      |
| `sql/analysis/00_sanity_checks.sql`             | Smoke test printing the row count, average rating, and top language codes (evidence that the load matched pandas).                                                           |
| `sql/analysis/10_apply_canonical_bookid.sql`    | Reusable snippet showing how to coalesce duplicate IDs—placed under `analysis` so teams can copy/paste into future metrics.                                                  |
| `sql/README.md`                                 | Documents structure, numeric prefixes, Docker commands, and example workflows for both interactive and non-interactive execution.                                            |
| Doc updates                                     | `docs/data-faq.md` gained a “Where do the SQL scripts live?” entry; `docs/phase-05-glossary.md` gained definitions for the schema/analysis folders and the numbering system. |

Together, these assets satisfy the plan’s “structure + README + example query” requirements and provide a repeatable reference for future tasks.

## 5. Expected output checkpoints

- `tree sql` shows only `analysis/`, `schema/`, and `README.md`—no stray root-level `.sql` files remain.
- Running `\i sql/analysis/00_sanity_checks.sql` inside `psql` prints:

  ```
  total_books
  ------------
        11119
  (1 row)

      avg_rating
  ----------------
            4.0057
  (1 row)

  language_code | book_count
  --------------+-----------
  eng           |      8906
  en-US         |       634
  en-GB         |       386
  spa           |       218
  mul           |       129
  ```

- `git status -- sql docs/data-faq.md docs/phase-05-glossary.md` shows only the expected tracked files from this task.
- `sql/README.md` includes both interactive (`\i ...`) and `-f /app/sql/...` usage blocks so new contributors can follow along verbatim.

## 6. Observations / insights

- Numeric prefixes (00/01/02/10/20/…) solved the “which script runs first?” problem immediately; GitHub diff viewers also sort correctly without extra tooling.
- Parking the canonical-ID helper under `analysis/` keeps the schema folder exclusively DDL while still giving analysts a copy-ready snippet for metrics or ETL.
- Documenting both interactive and non-interactive modes prevents future contributors from guessing how to automate `psql` runs in CI.
- Re-reading the outputs from `00_sanity_checks.sql` provides an instant regression test whenever the loader is rerun—no pandas notebook required.

## 7. Artifacts refreshed this task

- `sql/schema/01_create_books_table.sql`
- `sql/schema/02_create_books_canonical_view.sql`
- `sql/analysis/00_sanity_checks.sql`
- `sql/analysis/10_apply_canonical_bookid.sql`
- `sql/README.md`
- `docs/data-faq.md`
- `docs/phase-05-glossary.md`
- This note (`docs/phase-05-step-02-task-01-notes.md`)

## 8. Q&A / troubleshooting

| Question                                             | Answer                                                                                                                                                                                                   |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **How do I run multiple scripts back-to-back?**      | Stay inside one `psql` session and call `\i` in ascending numeric order (`sql/schema/` first, then `sql/analysis/`). Each `\i` respects the same working directory (`/app`).                             |
| **Can I execute a script non-interactively?**        | Yes. Use `docker compose ... exec -e PAGER=cat postgres psql -q -U goodreads_user -d goodreads -v ON_ERROR_STOP=1 -f /app/sql/analysis/00_sanity_checks.sql`. Replace the file path for other scripts.   |
| **Where do I document or add new SQL helpers?**      | Store them under the correct subfolder, prefix the filename with the next available number, add a short comment header referencing the phase/task, then update `sql/README.md` + the relevant task note. |
| **How can I confirm the repo is mounted correctly?** | Inside `psql`, run `\! pwd` (prints `/app`) or query `":r"` after executing `\i sql/...`. If the path fails, ensure you ran the `docker compose ... exec` command from the repo root.                    |
| **What if `psql` warns about the pager?**            | Set `PAGER=cat` (already shown in the command) or run `\pset pager off` once inside the session. This eliminates the `TURN: No such file or directory` warning produced by the minimal container image.  |

## 9. Checklist review (from the plan)

- [x] `sql/` structure (schema/, analysis/) created and populated.
- [x] File naming convention (two-digit prefix + descriptive slug) defined and applied.
- [x] `sql/README.md` documents purpose, structure, and execution workflow.
- [x] Example analysis script (`analysis/00_sanity_checks.sql`) created, documented, and referenced in notes.
- [x] Repository documentation (`docs/data-faq.md`, `docs/phase-05-glossary.md`, this note) updated to reflect the new conventions.

## 10. Appendix – single-command execution example

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec -e PAGER=cat `
  postgres psql -q -U goodreads_user -d goodreads -v ON_ERROR_STOP=1 -f /app/sql/analysis/00_sanity_checks.sql
```

Use this variant for CI or smoke tests. The `-v ON_ERROR_STOP=1` flag makes the command exit non-zero if any statement fails, which keeps automated pipelines honest.
