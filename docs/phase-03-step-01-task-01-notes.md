# Phase 03 – Step 01 – Task 01 – Set Up EDA Analysis Script and Imports

This note documents how I completed **Phase 03 → Step 01 → Task 01**. The deliverable is a reusable EDA bootstrap script plus beginner-friendly glossary updates so future analyses have a consistent starting point.

---

## 1. Task definition and goal

From `plan/phase-03-eda-and-data-quality/steps/step-01-univariate-eda/tasks/task-01-setup-eda-notebook-and-imports.md`, the objectives are:

- Create a dedicated script (suggested name `01_eda_books.py`) under `src/analyses/`.
- Document its purpose (univariate + bivariate EDA for the Goodreads dataset).
- Import the common stack: pandas, numpy, matplotlib, seaborn.
- Configure plotting defaults and load the Phase 02 dataset so later tasks can build on the same DataFrame.

I kept the existing filename `src/analyses/eda_books.py` (already referenced elsewhere) but reshaped it to match the new requirements.

---

## 2. How to run the script

All commands are executed from the repo root (`C:\Users\shady\documents\GITHUB\goodreads-books-analytics`).

```powershell
# Ensure containers are running (Python CLI + Postgres)
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d

# Run the EDA bootstrap script with a 1,000-row limit and verbose logging
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app \
    python -m src.analyses.eda_books --limit 1000 --verbose
```

The script accepts `--csv-path` (defaults to `data/books.csv`), `--limit`, and `--verbose` flags so it is quick to iterate while we build histogram/boxplot helpers later in Step 01.

---

## 3. Script highlights (`src/analyses/eda_books.py`)

- **Docstring & logging** – Describes the scope (“univariate and bivariate EDA”) and emits structured logs so we can trace dataset loading.
- **Imports** – `pandas`, `numpy`, `matplotlib.pyplot`, and `seaborn` are configured with a consistent white-grid theme, larger figure size, and friendlier print options for arrays/DataFrames.
- **CLI** – `argparse` exposes `--csv-path`, `--limit`, and `--verbose`. This pattern mirrors the Phase 02 scripts so automation is easy later.
- **Loader** – `load_dataset()` validates the CSV path, loads the requested number of rows, and reports shape metadata.
- **Preview helper** – When `--verbose` is set we log the column list and the first five rows, giving an immediate sanity check that the file contents look correct.
- **Placeholder for plots** – The script ends with a friendly reminder to add histogram/KDE helpers in follow-up tasks, keeping this commit focused on bootstrapping.

---

## 4. Glossary for beginners

To keep explanations approachable, I added `docs/phase-03-glossary.md`. It defines core EDA terms (histogram, KDE, skewness, outlier, missing value, etc.) plus dataset-specific fields (`average_rating`, `ratings_count`, `language_code`, etc.). Future Phase 03 notes can link back to this glossary instead of repeating definitions.

---

## 5. Verification log (Dec 4, 2025)

Running the script with `--limit 1000 --verbose` produced the expected checkpoints:

```
INFO  __main__ - Loading dataset from data/books.csv
INFO  __main__ - Loaded shape: (rows=1000, columns=12)
INFO  __main__ - Column names: ['bookID', 'title', 'authors', ...]
INFO  __main__ - Head (first 5 rows):
    bookID  title ...
INFO  __main__ - EDA bootstrap complete. Add univariate plots in follow-up tasks.
```

The log confirms that pandas successfully read the CSV and that the script is ready for additional analysis helpers.

---

## 6. Checklist review

- [x] Created / updated the dedicated EDA script under `src/analyses/`.
- [x] Added a docstring describing the univariate+bivariate focus.
- [x] Imported pandas, numpy, matplotlib, seaborn, and configured plotting defaults.
- [x] Loaded the Goodreads dataset into a DataFrame and logged the head for verification.
- [x] Added a glossary so beginner readers can follow along.

Task complete. Next up: Step 01 Tasks 02 and 03 (numeric & categorical distributions) will extend this script with actual plots and summaries.
