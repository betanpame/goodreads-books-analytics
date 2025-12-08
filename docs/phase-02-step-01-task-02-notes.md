# Phase 02 – Step 01 – Task 02 – Load CSV and Basic Summary

This note documents how I satisfied **Phase 02 → Step 01 → Task 02 – Load CSV and Basic Summary**. The goal is to prove that the `books.csv` file loads correctly in pandas, capture the required `head()`, `tail()`, `.info()`, and `.describe()` outputs, and record beginner-friendly observations.

---

## 1. Task definition and goal

The planning file `plan/phase-02-data-loading-and-initial-exploration/steps/step-01-inspect-dataset-with-pandas/tasks/task-02-load-csv-and-basic-summary.md` requires:

1. Loading `data/books.csv` into pandas.
2. Displaying:
   - `head()` and `tail()`
   - `.info()`
   - `.describe()`
3. Writing down first observations about dataset shape, column types, and obvious quirks.

This note follows those instructions exactly so another beginner can reproduce the process without guessing.

---

## 2. How to run this analysis script

Follow the repeatable three-command flow so anyone can regenerate the Task 02 outputs.

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

### Estimated runtime & success checks

- **Runtime:** Typically <2 minutes end to end (containers warm start in ~30 seconds; script finishes in ~20 seconds).
- **Success checklist:**
  - `docker compose ... up -d` shows the `app` and `postgres` services as `Running`.
  - Terminal output includes `head()`, `tail()`, `.info()`, and `.describe()` plus `Loaded shape: (rows=1000, columns=12)`.
  - `outputs/initial_inspection/books_sample_preview.csv` and `books_numeric_summary.csv` have timestamps that match your run.

Each run refreshes the logs and the helper CSV files in `outputs/initial_inspection/`, so reviewers can always trace the exact commands that produced the artifacts. This three-command flow is now the canonical template for every Phase 02 → Step 01 task note—reuse it whenever you document a new deliverable so readers always know how to reproduce your run.

---

## 3. Environment recap

I reused the Docker-based Python CLI environment from Phase 01. Everything happens inside the `app` container so the exact same Python version and dependencies run every time.

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics

# Start Python + Postgres containers in the background
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d

# Open a shell inside the Python container
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app bash
```

Once the prompt changed to `root@...:/app#`, I executed the analysis script:

```bash
python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Using `--sample-size 1000` keeps the output manageable while still showing plenty of variety. The `--verbose` flag prints the repository listing and detailed logs, which is extremely useful when you are just starting out.

---

## 4. Required pandas outputs

The script now logs every deliverable directly in the terminal. Highlights from the latest run (Dec 03 2025):

1. **`head()`** – first five rows.

   - All rows are Harry Potter books from Scholastic, just like the dataset preview in Task 01.
   - Confirms we are reading the same CSV through Docker (paths show `/app/data/books.csv`).

2. **`tail()`** – last five rows.

   - Shows IDs 3404–3417 covering Harper, Cooper Square Press, and Avon publications.
   - Demonstrates that even with only 1,000 rows we still see a broad publisher mix.

3. **`.info()`** – schema + non-null counts.

   - Every column in the sample (12 columns, 1,000 rows) reports `1000 non-null`, meaning there are no missing values in the first slice.
   - Dtypes: 5 integer columns (`bookID`, `isbn13`, `num_pages` [note the leading spaces in the column name], `ratings_count`, `text_reviews_count`), 1 float (`average_rating`), 6 object/string columns.
   - Memory footprint ≈ 94 KB for the sample.

4. **`.describe()`** – numeric and categorical stats.
   - `average_rating` mean ≈ 3.94 with max 5.00.
   - `ratings_count` mean ≈ 40k; maximum 2,418,736 which indicates extreme popularity for the top books.
   - Most frequent publisher is **Penguin Books** (39 occurrences). Top title in the sample is **Anna Karenina** (appears 6 times, likely different editions).

All four outputs are stored in the terminal log (see previous section) so recruiters or reviewers can replay them exactly.

---

## 5. Expected output checkpoints

When the script runs successfully with `--sample-size 1000 --verbose`, you should see the following highlights:

- `Loaded shape: (rows=1000, columns=12)` immediately after the CSV read call.
- `head()` rows dominated by Harry Potter / Scholastic entries and `tail()` rows with IDs 3404–3417 (Harper, Cooper Square Press, Avon).
- `.info()` reporting `1000 non-null` for every column and documenting the dtype mix (5 ints, 1 float, 6 objects).
- `.describe()` lines such as `average_rating mean ≈ 3.94`, `ratings_count max = 2418736`, and `top publisher = Penguin Books`.
- A confirmation that CSV artifacts were written to `outputs/initial_inspection/`.

If one of these checkpoints is missing, verify that you ran from inside the container and that `data/books.csv` is accessible on the host.

---

## 6. Observations for future steps

- **Column naming quirk**: `num_pages` includes two leading spaces (`"  num_pages"`). We need to rename it when building the Postgres schema.
- **Publication dates**: still stored as plain strings (`publication_date` dtype is `object`). Later we should call `pd.to_datetime(..., errors="coerce")` to normalize them.
- **Authors field**: names are separated by `/` when there are multiple contributors (e.g., `J.K. Rowling/Mary GrandPre`). Flagged for Task 03 to discuss splitting logic.
- **Missing values**: none in the first 1,000 rows, but this does not guarantee the full dataset is clean. We will revisit when loading all ~50k records.
- **Outputs folder**: the run refreshed two CSV files at `outputs/initial_inspection/`:
  - `books_sample_preview.csv` – mirrors `head()` results.
  - `books_numeric_summary.csv` – mirrors `.describe()` numeric stats (mean ratings_count, etc.).

These notes were added immediately after running the script so the context stays fresh.

---

## 7. Artifacts refreshed each run

- `outputs/initial_inspection/books_sample_preview.csv` – mirrors the logged `head()` output for quick spreadsheet inspection.
- `outputs/initial_inspection/books_numeric_summary.csv` – numeric `.describe()` export used later for regression testing.

Delete them if you ever want to confirm the script regenerates files from scratch; the timestamps make it obvious whether the latest run succeeded.

---

## 8. Checklist review

- [x] Loaded `books.csv` with pandas inside Docker.
- [x] Captured `head()` and `tail()` for the same sample.
- [x] Logged `.info()` output showing dtypes and non-null counts.
- [x] Logged `.describe()` statistics.
- [x] Wrote beginner-friendly observations in this file.

Result: **Task 02 is complete.** The repository now contains both the executable script (`src/analyses/initial_inspection_books.py`) and this narrative proof of what it does, making it easy to continue with Task 03 (column-by-column exploration) next.

---

## 9. Q&A / Data troubleshooting

**Can I load more (or fewer) rows than 1,000?** – Yes. Change `--sample-size` when you run the script. Keep `--verbose` so the logs still show the column-level context.

**Where do I inspect the exact rows the log referenced?** – Open `outputs/initial_inspection/books_sample_preview.csv`. It mirrors the `head()` output logged in Section 4.

**How do I double-check column dtypes outside the script?** – Run `python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose` and copy the `.info()` portion, or load the CSV in an interactive session (`python -i`) and call `df.dtypes` yourself.

**The script cannot find `data/books.csv`. What should I check?** – Ensure you’re running commands from the repo root so Docker mounts the data folder. If the file is really missing, follow `docs/dataset-notes.md` for download steps.

**Where can I find broader dataset answers?** – Refer to `docs/data-faq.md` for questions that span multiple tasks (source provenance, schema plans, etc.).

---
