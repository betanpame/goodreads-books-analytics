# Phase 03 – Step 01 – Task 02 – Explore Numeric Distributions

This note explains how I completed **Phase 03 → Step 01 → Task 02**. The deliverable is a repeatable numeric-profiling routine plus plain-language takeaways that tie back to the Phase 03 glossary.

---

## 1. Task definition and goal

Per `plan/phase-03-eda-and-data-quality/steps/step-01-univariate-eda/tasks/task-02-explore-numeric-distributions.md`, this task asked for:

- Summary statistics (mean, median, min, max, standard deviation) for the most important numeric columns.
- Histogram and/or KDE visualizations for those columns, using log scale when the data are strongly skewed.
- Short interpretations that explain whether the distributions are symmetric, skewed, or contain extreme values that might need additional cleaning in later steps.

The focus columns are `average_rating`, `num_pages`, `ratings_count`, and `text_reviews_count`.

---

## 2. Script updates (`src/analyses/eda_books.py`)

- Added `NUMERIC_COLUMNS` / `LOG_SCALE_COLUMNS` dictionaries so we can remap the oddly named Kaggle column `"  num_pages"` to a friendlier output label.
- Introduced an `--output-dir` CLI flag (default `outputs/phase03_univariate`) plus helper functions:
  - `analyze_numeric_distributions()` builds the summary table, logs the key stats, and orchestrates plotting.
  - `save_distribution_plot()` centralizes the histogram + KDE rendering and toggles log scale for count-based metrics.
- Reused `src.raw_ingestion.load_books_csv` so malformed author rows are repaired consistently with Phase 02 ingestion.
- The helper now writes `numeric_summary.csv` and PNG files (one per column) so later notebooks can reuse the outputs without rerunning the script.

All functions include concise log messages so the console transcript doubles as a sanity check for beginners reading along.

---

## 3. How to run it

From the repository root (`C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`), rerun the shared CLI.

### Command block (copy/paste)

```powershell
# Optional: start the dockerized Python environment if you prefer containers
# docker compose -f docker-compose.python.yml up -d

# Run the analysis with verbose logging and default output directory
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe `
    -m src.analyses.eda_books `
    --verbose
```

### Estimated runtime & success checks

- **Runtime:** ≈3 minutes locally (loading 11k rows + generating four plots and CSVs). Docker runs take ~4 minutes.
- **Success checklist:**
  - CLI log shows `Saved numeric summary to outputs\phase03_univariate\numeric_summary.csv` and four `Saved ... distribution plot` lines.
  - `outputs/phase03_univariate/` contains `numeric_summary.csv` plus the four PNGs (`average_rating_distribution.png`, etc.).
  - Terminal prints the interpretation logs (mean/median/min/max) for each numeric column when `--verbose` is set.

Flags remain the same: `--csv-path` (defaults to `data/books.csv`), `--limit` for sampling, and `--output-dir` to redirect artifacts.

---

## 4. Outputs and interpretations

### 4.1 Summary table

File: `outputs/phase03_univariate/numeric_summary.csv`

| column             |  count |   mean |     std |  min |  p25 | median |   p75 |       max |
| ------------------ | -----: | -----: | ------: | ---: | ---: | -----: | ----: | --------: |
| average_rating     | 11,127 |   3.93 |    0.35 | 0.00 | 3.77 |   3.96 |  4.14 |      5.00 |
| num_pages          | 11,127 |    336 |     241 |    0 |  192 |    299 |   416 |     6,576 |
| ratings_count      | 11,127 | 17,936 | 112,479 |    0 |  104 |    745 | 4,993 | 4,597,666 |
| text_reviews_count | 11,127 |    542 |   2,576 |    0 |    9 |     46 |   238 |    94,265 |

(Beginners: “p25/p75” are the 25th/75th percentiles—see the glossary entry on quartiles.)

### 4.2 Distribution snapshots

Plots saved under `outputs/phase03_univariate/`:

- `average_rating_distribution.png`
- `num_pages_distribution.png`
- `ratings_count_distribution.png` (log-scale x-axis)
- `text_reviews_count_distribution.png` (log-scale x-axis)

Key takeaways:

- **Average rating** – Very tight, mildly left-skewed distribution centered near 4. Most Goodreads books cluster between 3.7 and 4.2 stars, so any title below 3 looks unusually weak.
- **Number of pages** – Right-skewed: 75% of titles stay under ~416 pages but the tail stretches past 6,000 pages. The spikes likely correspond to omnibus editions or data-entry artifacts; flag for later quality checks.
- **Ratings count** – Heavily skewed toward small numbers. Half the catalog has fewer than 750 ratings, while a few blockbuster titles exceed 4.5 million ratings. Using a log scale made the long tail readable.
- **Text reviews count** – Follows the same power-law shape as ratings. Most books have fewer than 50 text reviews, yet the top outlier surpasses 94k.

These observations will inform Step 01 Task 03 (categorical distributions) and later Phase 03 quality rules—for example, we may cap or Winsorize counts before building dashboards so averages are not dominated by runaway hits.

---

## 5. Verification log (Dec 4, 2025)

```
INFO __main__ - Loading dataset from data\books.csv
INFO __main__ - Raw loader repaired 453 row(s) out of 11127
INFO __main__ - Column names: ['bookID', 'title', ...]
INFO __main__ - average_rating stats -> mean=3.93, median=3.96, min=0.00, max=5.00
INFO __main__ - ... (similar logs for each column)
INFO __main__ - Saved text_reviews_count distribution plot to outputs\phase03_univariate\text_reviews_count_distribution.png
INFO __main__ - Wrote numeric summary to outputs\phase03_univariate\numeric_summary.csv
INFO __main__ - EDA bootstrap complete. Add univariate plots in follow-up tasks.
```

---

## 6. Checklist review

- [x] Computed summary stats for each key numeric column.
- [x] Generated histogram + KDE plots (with log scale for the two skewed count fields).
- [x] Captured beginner-friendly interpretations tied to potential business questions.

Task complete. The outputs now give us a clear baseline for spotting outliers and prioritizing the next categorical distribution pass.
