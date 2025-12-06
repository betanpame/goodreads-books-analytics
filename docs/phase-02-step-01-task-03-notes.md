# Phase 02 - Step 01 - Task 03 - Explore Key Columns and Types

This log documents how I completed **Phase 02 - Step 01 - Task 03**. The goal is to inspect the highest-priority columns from `books.csv`, capture their types, uniqueness, and missingness, and note any quirks that will influence downstream schema design.

---

## 1. Task definition and goal

Per `plan/phase-02-data-loading-and-initial-exploration/steps/step-01-inspect-dataset-with-pandas/tasks/task-03-explore-key-columns-and-types.md`, I needed to:

1. Look at the ten key columns listed in the task file.
2. Record example values, pandas dtypes, `nunique()`, and `isna().sum()` for each column.
3. Attempt to parse `publication_date` as `datetime` and log any failures.
4. Describe how multi-author rows should be handled in future steps.
5. Capture everything in Markdown so another beginner can retrace the steps.

---

## 2. How to run this analysis script

Use the same reproducible command sequence every time you revisit this task:

1. **Move into the repository**

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
```

2. **Start (or verify) Docker services** so the Python CLI container and Postgres are online:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
```

3. **Run the scripted inspection** inside the Python container with the same flags I documented for Tasks 01 and 02:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.portfolio.p01_initial_inspection_books --sample-size 1000 --verbose
```

This command emits all Task 03 metrics to the terminal and refreshes the helper CSV files under `outputs/initial_inspection/` so reviewers can diff results over time.

Use the same trio of commands whenever you document a new Phase 02 → Step 01 task so readers never have to guess how to reproduce your run.

---

## 3. Environment recap and command

I reused the same Dockerized CLI workflow from Tasks 01 and 02:

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
# Ensure Python + Postgres services are running
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
# Execute the scripted analysis inside the Python container
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

The script prints every required metric directly to the terminal log and refreshes the helper CSV files under `outputs/initial_inspection/` for anyone who prefers to inspect the data in another tool.

---

## 4. Column-by-column findings

The run above produced the following summary for the ten required columns (sample size = 1,000 rows):

| Column               | pandas dtype | Unique values | Missing values | Example values                       | Notes                                                |
| -------------------- | ------------ | ------------- | -------------- | ------------------------------------ | ---------------------------------------------------- |
| `bookID`             | `int64`      | 1,000         | 0              | `1, 2, 4, 5, 8`                      | Acts as a stable primary key in every row inspected. |
| `title`              | `object`     | 916           | 0              | `"Harry Potter...", "Anna Karenina"` | Repeated titles confirm multiple editions exist.     |
| `authors`            | `object`     | 711           | 0              | `"J.K. Rowling/Mary GrandPre"`       | Slash-separated names highlight multi-author rows.   |
| `average_rating`     | `float64`    | 142           | 0              | `4.57, 3.48`                         | Continuous metric in [1, 5]; no coercion needed.     |
| `  num_pages`        | `int64`      | 450           | 0              | `652, 870, 352`                      | Column name includes two leading spaces in the CSV.  |
| `ratings_count`      | `int64`      | 776           | 0              | `2,095,690`, `6,333`                 | Heavy skew (mean ~ 40k, max 2.4M).                   |
| `text_reviews_count` | `int64`      | 432           | 0              | `27,591`, `244`                      | Similar skew to `ratings_count`.                     |
| `publication_date`   | `object`     | 746           | 0              | `"9/16/2006"`                        | Parsed cleanly to datetime (details below).          |
| `publisher`          | `object`     | 429           | 0              | `"Scholastic Inc.", "Penguin Books"` | Long tail of publishers.                             |
| `language_code`      | `object`     | 11            | 0              | `"eng", "spa", "fre"`                | Mostly `eng`, with a handful of other codes.         |

No missing values surfaced inside the 1,000-row slice, but this sample is not proof that the full dataset is pristine. The script now highlights missing counts so we will notice any gaps immediately when we increase the sample size later.

---

## 5. Expected output checkpoints

Successful Task 03 runs emit a few tell-tale log lines:

- `Exploring key columns and types (Task 03 focus)` to signal that the new helper executed.
- Ten consecutive lines like `Column 'title' -> dtype=object | unique=916 | missing=0` (one per key column).
- `publication_date parsing success: 100.00% (1000/1000 rows)`—the percentage may dip when we load more than 1,000 rows, but it should always print.
- `Authors column: 50.40% of rows list multiple authors (split on '/')` so we can track the prevalence of slash-separated names over time.

Missing any of these lines usually means `--verbose` was omitted or the helper was not invoked.

---

## 6. Publication date parsing check

Task 03 asked for an explicit datetime parsing attempt. The script now calls:

```python
parsed_dates = pd.to_datetime(sample[KEY_COLUMNS["publication_date"]], errors="coerce")
```

In this run, **100% of the rows (1,000 / 1,000)** converted successfully, producing ISO-formatted strings such as `2006-09-16`. Because parsing uses `errors="coerce"`, any invalid entry in a larger sample will turn into `NaT`, and the log will immediately show the success percentage so we can quantify how much cleanup is needed.

---

## 7. Multi-author handling idea

Roughly **50.40%** of the sampled rows contain multiple authors separated by `/`. When the time comes to normalize this field, the plan is to:

1. Split on `/` with `df["authors"].str.split("/")`.
2. Trim whitespace from each resulting token.
3. Explode the list into a long table so each author/title pair becomes one row (ideal for a bridge table in Postgres).

Documenting this approach now should make it trivial to implement in Phase 03 (data quality rules) or Phase 05 (SQL schema design).

---

## 8. Artifacts refreshed each run

- `outputs/initial_inspection/books_sample_preview.csv` – re-exported with every execution so you can spot-check column values outside the terminal.
- `outputs/initial_inspection/books_numeric_summary.csv` – numeric describe metrics for regression-testing later automation.

Because Task 03 adds additional logging but not new files, these two artifacts remain the single source of truth for downstream teams—double-check their timestamps after each run.

---

## 9. Code references

- `src/analyses/initial_inspection_books.py` now exposes a `KEY_COLUMNS` dictionary and an `explore_key_columns` helper. The helper logs dtype, uniqueness, missingness, sample values, publication-date parsing stats, and the multi-author ratio every time the script runs.
- `outputs/initial_inspection/books_sample_preview.csv` and `outputs/initial_inspection/books_numeric_summary.csv` continue to refresh on each run, so the artifacts always match the logs.

---

## 10. Checklist review

- [x] Examined example values, types, and missing counts for every key column.
- [x] Parsed `publication_date` with `pd.to_datetime` and logged the 100% success rate.
- [x] Captured a concrete plan for splitting multi-author rows.

**Result:** Task 03 is complete. The repository now includes both the executable analysis (`src/analyses/initial_inspection_books.py`) and this beginner-friendly walkthrough so anyone can reproduce the column-level inspection without guesswork.

---

## 11. Q&A / Data troubleshooting

**How do I check the raw column names to confirm typos (like the double space in `"  num_pages"`)?** – Run the script with `--verbose` and look for the `Columns: [...]` line near the top, or open `books_sample_preview.csv` and inspect the header row directly.

**What if a key column is missing when I log `KEY_COLUMNS`?** – Make sure you didn’t accidentally trim column names when saving the CSV. If the column truly doesn’t exist, revisit `data/books.csv` (or the upstream source) to restore it before continuing with schema design.

**publication_date parsing success is less than 100%—how do I find the broken rows?** – Copy the snippet from Section 6 into an interactive session, then run `sample[KEY_COLUMNS["publication_date"]][parsed_dates.isna()]` to list problematic entries. Document anything suspicious in `docs/data-faq.md`.

**How can I quickly estimate how many rows have multiple authors beyond the first 1,000?** – Increase `--sample-size` (e.g., 5000) and rerun. The log line `Authors column: XX% of rows list multiple authors` will update automatically.

**Where can I find more answers about the dataset in general?** – Check `docs/data-faq.md` for cross-task questions and links to source documentation.
