# Phase 02 - Step 02 - Task 02 - Define Main Books Table

This guide walks through **Phase 02 → Step 02 → Task 02**, where we turn the column mapping from Task 01 into a concrete `CREATE TABLE books` statement for PostgreSQL. Everything below is written so a beginner can repeat the same steps inside the repo.

---

## 1. Task definition and goal

According to `plan/phase-02-data-loading-and-initial-exploration/steps/step-02-design-postgres-schema/tasks/task-02-define-main-books-table.md`, the deliverable is a SQL file that:

1. Creates a `books` table using the types we mapped previously.
2. Marks `book_id` (or `bookID`) as the primary key.
3. Adds sensible constraints (`NOT NULL`, `CHECK`, defaults) where justified.
4. Lives under a `sql/` folder with inline comments explaining design decisions.

---

## 2. How to run this analysis script (context refresher)

While this task is mostly DDL design, I still start with the standard commands so the dataset and container are ready if I need to double-check anything:

```powershell
cd C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Those commands verify that pandas can still read `data/books.csv` and that our profiling from Task 01 remains accurate.

---

## 3. Environment recap

- **Workspace**: Same Dockerized Python + Postgres stack from Step 01.
- **Reference data**: Column statistics gathered in `docs/phase-02-step-02-task-01-notes.md` (max lengths, numeric ranges, etc.).
- **Target engine**: PostgreSQL 16 (per docker-compose configuration). SQL syntax sticks to standard Postgres features so it runs immediately inside the container or any external instance.

---

## 4. Building the DDL

Steps completed:

1. Created a dedicated `sql/` directory (if missing) to keep schema artifacts together.
2. Wrote `sql/create_books_table.sql` containing the `CREATE TABLE IF NOT EXISTS books (...)` statement.
3. Added inline comments highlighting tricky areas (renaming `"  num_pages"`, why ISBNs are stored as text, future normalization ideas).

Key choices in the DDL:

- Snake_case column names to align with SQL style (`book_id`, `num_pages`, etc.). The ETL step will handle the rename from the raw CSV headers.
- `book_id INTEGER PRIMARY KEY` since the highest observed value is 45,641.
- Numeric metrics (`ratings_count`, `text_reviews_count`) keep `INTEGER NOT NULL DEFAULT 0` with `CHECK (… >= 0)` to prevent negative loads.
- `average_rating NUMERIC(3,2)` with a `CHECK` constraint to enforce the 0–5 range seen in the data.
- `isbn` and `isbn13` defined as `VARCHAR(20)` so leading zeros and hyphens survive.
- Table-level `CHECK (title <> '')` to avoid blank titles.

---

## 5. Expected output checkpoints

After saving `sql/create_books_table.sql`, open it and confirm you see:

- `CREATE TABLE IF NOT EXISTS books (` at the top.
- Every column from Task 01 represented once (11 plus `book_id`).
- Comments explaining the rename requirement for `num_pages` and future normalization notes.
- `CHECK` constraints for `average_rating`, `ratings_count`, `text_reviews_count`, and `title`.

If any column is missing (for example, `publication_date`), go back to the mapping table in Task 01 before moving on to Task 03.

---

## 6. Observations and open questions

- **Malformed CSV row**: Still on the radar from Task 01. When we write the ETL job, we should log any skipped rows so they can be fixed before loading to Postgres.
- **Uniqueness**: I did not add `UNIQUE` on `isbn13` yet because the source data contains duplicates. Once data quality rules exist we can enable it.
- **Normalization**: Authors and publishers remain as `TEXT` columns for now, but Task 03 (normalization planning) will likely introduce bridge tables.

---

## 7. Artifacts refreshed each run

- `sql/create_books_table.sql` – authoritative source of the `books` table definition.
- `docs/phase-02-step-02-task-02-notes.md` – this narrative log.

Copy `create_books_table.sql` into any Postgres client to create the table once the ETL is ready.

---

## 8. Checklist review

- [x] Wrote a `CREATE TABLE books` statement.
- [x] Saved it under `sql/create_books_table.sql` with explanatory comments.
- [x] Documented the decisions and constraints in this note.

---

## 9. Q&A / Data troubleshooting

**Q: Why use `INTEGER` instead of `BIGINT` for counts?**  
The largest value observed (`ratings_count = 4,597,666`) comfortably fits inside 32-bit signed integers. We can widen to `BIGINT` later if new data exceeds that range.

**Q: Do I have to rename `"  num_pages"` in the SQL?**  
No—the SQL already uses the clean `num_pages` identifier. The ETL script must handle the rename during the load step (`SELECT "  num_pages" AS num_pages ...`).

**Q: Can I enforce uniqueness on `isbn13` now?**  
Not yet. The raw dataset contains duplicates for multi-edition titles. Once Tasks 03/Phase 03 introduce deduping rules, we can add a `UNIQUE (isbn13)` constraint.

**Q: How do I run this SQL in Postgres?**  
See the step-by-step guide in section 10. In short: start the containers, copy the SQL file into the running Postgres container, execute it with `psql -f /tmp/create_books_table.sql`, then delete the temporary file. This avoids “No such file or directory” errors that occur when `psql` runs from `/` and cannot see the repo-mounted path.

For broader questions or troubleshooting tips, see `docs/data-faq.md`.

---

## 10. Running the DDL inside Postgres (How-to)

These are the exact commands I ran on December 4, 2025 to create the `books` table inside the Dockerized Postgres instance. Run them from the repo root (`C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics`).

1. **Ensure Postgres is up** (only needed once per session):
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d postgres
   ```
2. **Copy the DDL file into the container** so `psql` can read it from a path that exists inside the container filesystem:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml cp sql/create_books_table.sql postgres:/tmp/create_books_table.sql
   ```
3. **Execute the script** using the credentials defined in `.env` (`POSTGRES_USER=goodreads_user`, `POSTGRES_DB=goodreads`):
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres psql -U goodreads_user -d goodreads -f /tmp/create_books_table.sql
   ```
   Expect output similar to:
   ```text
   NOTICE:  relation "books" already exists, skipping
   CREATE TABLE
   ```
   The notice confirms the `IF NOT EXISTS` guard works when the table is already present.
4. **Clean up the temporary file** (optional but keeps the container tidy):
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres rm /tmp/create_books_table.sql
   ```
5. **Verify the schema** whenever needed:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec postgres psql -U goodreads_user -d goodreads -c "\d books"
   ```

Why copy the file? When `docker compose exec postgres psql -f sql/...` is executed directly, the command runs from the container root (`/`) and cannot see the repo-mounted path, resulting in `psql: sql/create_books_table.sql: No such file or directory`. Copying the file into `/tmp` (or alternatively running `sh -c "cd /workspace && psql ..."`) eliminates that mismatch.
