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

**Can I safely delete the outputs folder?** – Yes; the next script execution recreates the files. This is a good way to verify that the pipeline still works end-to-end.

## CLI / environment

**What commands should I run for any Phase 02 → Step 01 task?** – Always start with:

```powershell
cd C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Swap the module name or flags as needed, but keep the structure so the bind mount and container context stay consistent.

**How do I capture logs for later documentation?** – Pipe the command through `tee` inside the container (e.g., `python -m ... | tee /app/outputs/task03.log`) or copy/paste from the terminal immediately after the run. Mention the date/time in your notes so reviewers know which log you referenced.

## Keeping this FAQ updated

Whenever you repeat the same explanation in more than one task note, migrate it here instead and link back to the relevant question. That keeps the task notes focused while ensuring beginners always know where to look for deeper answers.
