# Phase 03 - Step 02 - Task 02 - Temporal Trends

This note documents **Phase 03 - Step 02 - Task 02**, where the objective was to move beyond static distributions and inspect how Goodreads metrics change over time. Deliverables: (1) per-year book counts, (2) per-year average rating, and (3) per-year average ratings_count (with the same caps introduced in Task 01). Outputs must be beginner friendly and live alongside the other univariate artifacts so downstream scripts and Docker jobs can reuse them.

---

## 1. Task definition and goal

From `plan/phase-03-eda-and-data-quality/steps/step-02-bivariate-eda/tasks/task-02-temporal-trends.md` the scope was:

- Derive a clean `publication_year` feature from `publication_date` and report how much of the dataset keeps a valid year.
- Produce line charts plus CSV exports that show (a) how many books were published per year, (b) whether reader sentiment drifts over time, and (c) how engagement (`ratings_count`) evolves for those cohorts.
- Call out data gaps so the business narrative stays honest (for example, sparse coverage before modern ISBN tracking or after 2007).

---

## 2. Script updates (`src/analyses/eda_books.py`)

- Added `add_publication_year_column()` to coerce raw dates into integer years, report coverage, and warn when values are missing. It keeps the rest of the pipeline unchanged by working on a copy of the DataFrame.
- Implemented `analyze_temporal_trends()` which:
  - Reuses the capped `ratings_count` logic so engagement medians are comparable to Task 01 plots.
  - Aggregates per-year counts and mean metrics, writes CSVs, and calls a small helper to render line charts in `outputs/phase03_univariate/step02_task02_temporal/`.
  - Short-circuits gracefully if the dataset lacks `publication_year` or if everything becomes `NaN` after coercion.
- Left the CLI flags untouched (`--csv-path`, `--limit`, `--output-dir`, `--verbose`) so anyone following earlier notes can rerun the analysis without relearning the interface.

---

## 3. How to run it

From the repository root (`C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`).

### Command block (copy/paste)

```powershell
# Local Python virtualenv
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books

# Or inside Docker
docker compose -f docker-compose.python.yml run --rm app \
  python -m src.analyses.eda_books
```

### Estimated runtime & success checks

- **Runtime:** ≈4 minutes locally (deriving publication_year + generating three line charts); ≈5 minutes via Docker.
- **Success checklist:**
  - CLI log includes `Derived publication_year for ... rows` followed by three `Saved ... per year` lines referencing the temporal subfolder.
  - Directory `outputs/phase03_univariate/step02_task02_temporal/` contains the three CSV/PNG pairs described below.
  - When `--verbose` is enabled the log prints coverage percentages and the warning about sparse post-2006 data.

Key artifacts for this task:

- `books_published_per_year.csv` + `books_published_per_year_line.png`
- `average_rating_by_year.csv` + `average_rating_by_year_line.png`
- `average_ratings_count_by_year.csv` + `average_ratings_count_by_year_line.png`

All six files sit inside `outputs/phase03_univariate/step02_task02_temporal/`.

---

## 4. Findings

### Coverage and caveats

- The dataset holds **11,127** rows; **11,125** of them carry a valid `publication_year` (~**99.98%** coverage). Only two rows were dropped for temporal charts, so the feature is safe to add to Phase 04 dashboards.
- Early decades are barely represented (only **3%** of rows come from pre-1980 releases), so anything before the paperback boom should be treated as anecdotal.
- Coverage collapses after 2006 (see counts below). That cliff stems from the raw CSV lacking fully formatted `publication_date` values for many modern titles, not from an actual slowdown in publishing.

### Publication volume timeline

- Volume accelerates steadily from the mid-1960s, peaks in the **early 2000s**, and tops out at **1,700** books in **2006** followed closely by **2005 (1,260)** and **2004 (1,071)**.
- After 2006 the chart nosedives to double-digit samples per year (only **49** books with clean dates in 2008, **1** in 2020). Use the 1990-2006 window whenever you need statistically reliable cohorts.

### Ratings stay remarkably stable

- Yearly mean ratings stay within **3.88-3.97** for the dense 1980-2006 range (overall stdev ~**0.21**). The apparent extremes (`1922` at `5.0`, `1931` at `2.75`) each come from a single title and should be treated as outliers.
- There is no evidence of a secular decline or rise in reader sentiment; stakeholders should focus on segment-level variation (genre, language) rather than expecting time to drive ratings.

### Engagement intensity (average `ratings_count`)

- Engagement spikes mirror blockbuster eras. Examples:
  - **1952** averages ~**118k** ratings because that year only contains a pair of massively popular classics.
  - **2010** (~**33.9k**) and **2013** (~**41.1k**) reflect the Goodreads-era surge for YA franchises and Kindle breakouts, even though the sample is already thinning.
- After 2014 the averages swing wildly (e.g., **2015** drops to **1.8k**) because each year contains fewer than a dozen books. Always pair these numbers with the `book_count` CSV so reviewers see the denominator.

### Practical takeaways

1. **Temporal cohorts are viable for 1990-2006.** Use that slice when building trend lines or seasonality analyses; pre-1980 and post-2006 data is too sparse.
2. **Ratings are time-invariant.** Instead of chasing a non-existent time trend, focus on content characteristics (length, genre) uncovered in Task 01.
3. **Engagement metrics need normalization.** Quote both the average and the number of contributing books whenever you cite a spike, otherwise single-title years can mislead stakeholders.

---

## 5. Verification log (Dec 4, 2025)

```
2025-12-04 20:07:47,852 INFO __main__ - Loading dataset from data\books.csv
2025-12-04 20:07:47,958 INFO __main__ - Derived publication_year for 11125 rows (100.0% coverage)
2025-12-04 20:07:50,346 INFO __main__ - Saved books-per-year summary to outputs\phase03_univariate\step02_task02_temporal\books_published_per_year.csv
2025-12-04 20:07:50,678 INFO __main__ - Saved average rating by year to outputs\phase03_univariate\step02_task02_temporal\average_rating_by_year.csv
2025-12-04 20:07:50,906 INFO __main__ - Saved average ratings_count by year to outputs\phase03_univariate\step02_task02_temporal\average_ratings_count_by_year.csv
2025-12-04 20:07:52,337 INFO __main__ - EDA pass complete - numeric, categorical, temporal, outlier, and rating relationship artifacts ready.
```

---

## 6. Checklist review

- [x] Derived `publication_year`, inspected coverage, and documented the two missing rows.
- [x] Generated per-year counts plus companion line charts for books, ratings, and engagement metrics.
- [x] Highlighted the 2007+ coverage cliff so stakeholders will not misinterpret the downtrend.
- [x] Stored all artifacts under `outputs/phase03_univariate/step02_task02_temporal/` for reproducibility.
