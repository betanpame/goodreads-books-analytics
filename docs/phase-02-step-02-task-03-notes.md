# Phase 02 - Step 02 - Task 03 - Consider Future Normalization

This log captures everything needed to complete **Phase 02 → Step 02 → Task 03**. The goal is to look beyond the single `books` table we just created, evaluate how the dataset would benefit from a more normalized layout, and document a pragmatic decision for the current project. Every step below is reproducible so a beginner can follow along without guessing.

---

## 1. Task definition and goal

From `plan/phase-02-data-loading-and-initial-exploration/steps/step-02-design-postgres-schema/tasks/task-03-consider-future-normalization.md`, our deliverables are:

1. Brainstorm the supporting tables that would emerge from normalizing the Goodreads dataset (e.g., `authors`, `book_authors`, `publishers`).
2. Explain why normalization helps (deduplication, flexibility) and why we might postpone it (scope, simplicity).
3. Record a clear decision for Phase 02 so future contributors know whether to expand the schema or keep the single-table layout for now.

---

## 2. How to reproduce the exploratory queries

Even though this task is mostly conceptual, I ran a pandas scan to quantify how often authors, publishers, and languages repeat. Re-run it anytime with these commands from the repo root (`C:\Users\shady\documents\GITHUB\goodreads-books-analytics`).

### Command block (copy/paste)

```powershell
# 1) Make sure dependencies are installed
python -m venv .venv
\.\.venv\Scripts\activate
pip install -r requirements.txt
pip install pandas  # explicit here because the snippet depends on it

# 2) Inspect duplication statistics in the books CSV
@'
import pandas as pd
from pathlib import Path
from pprint import pprint

root = Path('.').resolve()
path = root / 'data' / 'books.csv'
df = pd.read_csv(path, on_bad_lines='skip', engine='python')

summary = {
    'row_count': len(df),
    'unique_authors': df['authors'].nunique(dropna=True),
    'unique_publishers': df['publisher'].nunique(dropna=True),
    'unique_languages': df['language_code'].nunique(dropna=True),
    'rows_with_multiple_authors': int(df['authors'].str.contains('/', na=False).sum()),
}

def split_authors(value: str) -> int:
    if not isinstance(value, str) or not value.strip():
        return 0
    return len([part.strip() for part in value.split('/') if part.strip()])

per_book_author_counts = df['authors'].apply(split_authors)
summary['avg_authors_per_book'] = round(float(per_book_author_counts.mean()), 2)
summary['max_authors'] = int(per_book_author_counts.max())
summary['books_single_author'] = int((per_book_author_counts == 1).sum())
summary['books_multi_author'] = int((per_book_author_counts >= 2).sum())
summary['top_authors'] = df['authors'].value_counts().head(5).to_dict()
summary['top_publishers'] = df['publisher'].value_counts().head(5).to_dict()

pprint(summary)
'@ | Set-Content tmp_normalization_scan.py

python tmp_normalization_scan.py
Remove-Item tmp_normalization_scan.py
```

### Estimated runtime & success checks

- **Runtime:** ≈5 minutes the first time (creating the virtual environment and installing dependencies dominates); reruns after the venv exists take ≈60–90 seconds.
- **Success checklist:**
  - `.\.venv\Scripts\activate` succeeds and `pip install -r requirements.txt` finishes without errors.
  - The script prints a dictionary containing keys such as `'row_count'`, `'unique_authors'`, `'rows_with_multiple_authors'`, and `'top_publishers'`.
  - Temporary file `tmp_normalization_scan.py` is removed at the end, keeping the repo clean.

> 🛈 **Why `on_bad_lines='skip'`?** The raw CSV contains at least one malformed row (line 3350) with 13 columns. Skipping bad lines lets the quick scan finish without blocking this task. The full ETL in Phase 03 will log and clean such rows explicitly.

---

## 3. Environment recap

- **Containers**: Same Python + Postgres stack from prior tasks. Run `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d` if anything is stopped.
- **Primary artifacts**: `sql/create_books_table.sql` (current schema) and `data/books.csv` (source dataset).
- **Tooling**: pandas for profiling, markdown for documentation, optional diagramming tools such as draw.io for ER sketches.

---

## 4. Profiling highlights that motivate normalization

Numbers produced on 4 Dec 2025:

- **11,119 books** were parsed (after skipping malformed rows).
- **6,635 unique author strings** but only **2,289 publishers**, so publisher names repeat a lot.
- **4,560 books list multiple authors** (average 1.73 per book, maximum 51). Slash-delimited author strings cannot scale.
- **27 language codes** appear; mapping them to a lookup table will make reports more readable.
- **Top authors**: `Stephen King (40)`, `P.G. Wodehouse (40)`, `Rumiko Takahashi (39)`, `Orson Scott Card (35)`, `Agatha Christie (33)`.
- **Top publishers**: `Vintage (318)`, `Penguin Books (261)`, `Penguin Classics (184)`, `Mariner Books (150)`, `Ballantine Books (144)`.

These counts demonstrate the duplication pressure that normalization would relieve.

---

## 5. Candidate normalized model

| Table               | Purpose                                        | Key Columns / Notes                                                                                   |
| ------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `books`             | Core facts already implemented.                | Keep existing columns; later add FK references instead of free-text fields.                           |
| `authors`           | Deduplicated author names.                     | `author_id SERIAL PRIMARY KEY`, `author_name TEXT NOT NULL`, optional Goodreads ID.                   |
| `book_authors`      | Many-to-many bridge between books and authors. | `book_id INTEGER`, `author_id INTEGER`, `author_order SMALLINT`, composite PK `(book_id, author_id)`. |
| `publishers`        | Canonical publisher values.                    | `publisher_id SERIAL`, `publisher_name TEXT UNIQUE`, optional HQ country.                             |
| `languages`         | Lookup for `language_code`.                    | `language_code VARCHAR(5) PRIMARY KEY`, `language_name TEXT`.                                         |
| `editions` (future) | One row per ISBN/format.                       | `edition_id SERIAL`, `book_id`, `isbn`, `isbn13`, `format`, `publication_date`.                       |

ASCII view of the relationships:

```
authors --< book_authors >-- books --< editions >-- publishers
                               |
                               +----< languages (lookup)
```

`editions` stays optional because the current CSV does not separate multiple ISBNs for the same work, but the design is ready if we ingest richer metadata.

---

## 6. Benefits vs. current single-table approach

**Normalization benefits:**

- Removes thousands of duplicate publisher strings and makes updates atomic.
- Stores each author once, enabling proper `JOIN`s for co-author metrics.
- Allows `ON UPDATE CASCADE` or `ON DELETE RESTRICT` so referential integrity protects analytics queries.
- Enables richer reporting (e.g., “Top 10 publishers per language”) without writing fragile string parsing logic.

**Reasons to defer in Phase 02:**

- Splitting slash-delimited authors cleanly requires additional ETL work (trimming, deduplicating, ordering) that is still TBD.
- The near-term milestone is "load a trustworthy `books` table," not "ship a full OLTP-grade schema."
- Every new table would increase migration/test surface area before we even validate the baseline data quality issues called out in Task 01.

---

## 7. Decision for this project

1. **Short term (Phase 02–03)**: Keep the single `books` table in Postgres so we can finish the extract/clean/load work quickly.
2. **Documented path forward**: This note and the inline `TODO` in `sql/create_books_table.sql` describe the exact tables to build when we revisit normalization.
3. **Trigger to re-open the work**: When we start producing author-centric dashboards, need to enforce publisher naming standards, or add incremental ingestion where duplicate text would create noisy diffs.

---

## 8. Checklist review

- [x] Listed the potential normalized tables plus how they relate.
- [x] Captured concrete benefits and trade-offs using real dataset statistics.
- [x] Communicated a clear decision for Phase 02 (stay denormalized now, plan for later).

---

## 9. Q&A / Troubleshooting

**Q: Why not normalize immediately?**  
Because we would need to build parsing, deduplication, and QA rules for the slash-delimited `authors` column before we even know whether the raw data is stable. That effort would delay the baseline load.

**Q: How will we map authors to IDs later?**  
Reuse the pandas snippet above to export a CSV of distinct trimmed author names, insert them into `authors`, then populate `book_authors` by splitting each book row and matching names to IDs.

**Q: Do we really need a `publishers` table when typos exist?**  
Yes. A lookup table lets us standardize casing (e.g., `Penguin Books` vs `Penguin books`) and enforce it with `CHECK` constraints or insert triggers. Without that, typos scatter across thousands of rows.

**Q: What about genres or shelves?**  
The public Goodreads CSV lacks shelf/genre data. If a future dataset includes it, follow the same pattern: create a lookup (`genres`) plus a bridge (`book_genres`).

---

## 10. Next steps

1. Carry these findings into Phase 02 → Step 03 when we design the load scripts—especially the requirement to split multi-author strings cleanly.
2. Consider adding lightweight SQL stubs (commented-out `CREATE TABLE authors ...`) to future migrations so the schema work can start quickly once prioritized.
3. When we build automated tests, add assertions that flag rows where `authors` still contains `/`; that will signal when the normalization milestone becomes urgent.
