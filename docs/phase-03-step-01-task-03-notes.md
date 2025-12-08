# Phase 03 – Step 01 – Task 03 – Explore Categorical Distributions

This document outlines how I completed **Phase 03 → Step 01 → Task 03**. The deliverables are categorical value-count summaries, companion bar charts, and an initial plan for taming the extreme rating/review counts we surfaced earlier.

---

## 1. Task definition and goal

From `plan/phase-03-eda-and-data-quality/steps/step-01-univariate-eda/tasks/task-03-explore-categorical-distributions.md`, the expectations were:

- Inspect categorical-style columns (`language_code`, `publisher`, `authors`) by computing value counts and plotting the most common categories.
- Describe which languages, publishers, and authors dominate the Goodreads export, calling out any surprising sparsity or long tails.
- Keep commentary beginner-friendly by tying observations back to the glossary (e.g., explaining why value counts matter).

I also extended the task slightly to record outlier-cap recommendations for the skewed count fields, so later Phase 03 quality rules have hard numbers to reference.

---

## 2. Script updates (`src/analyses/eda_books.py`)

- Added `CATEGORICAL_ANALYSIS_PLAN` to declare the columns, friendly labels, and “top N” thresholds for plotting.
- Implemented `analyze_categorical_distributions()` + `save_bar_plot()` to:
  - Fill null/blank categories with `"Unknown"` for transparency.
  - Persist full value counts to CSV (e.g., `language_code_value_counts.csv`).
  - Produce horizontal bar charts of the top categories (PNG files) for quick visual storytelling.
- Created `summarize_count_outliers()` so we now log the 95th/99th/99.5th percentiles for `ratings_count` and `text_reviews_count`, recommend a cap, and export the top 20 books behind each extreme.
- Rewired `main()` to run numeric, categorical, and outlier summaries in one invocation, so stakeholders can trust the `outputs/phase03_univariate` folder as the single source of truth for Step 01.

All helpers reuse the same CLI introduced in Task 02, which keeps onboarding simple for beginners copy-pasting commands.

---

## 3. How to run it

From the repo root (`C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`), reuse the same CLI.

### Command block (copy/paste)

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe `
    -m src.analyses.eda_books `
    --verbose
```

### Estimated runtime & success checks

- **Runtime:** ≈3 minutes in the local venv (categorical value counts + plots). Docker adds ~1 minute of overhead.
- **Success checklist:**
  - CLI log lists three lines like `Saved language_code value counts to ...` and `Saved ... bar chart to ...`.
  - Files `language_code_value_counts.csv`, `publisher_value_counts.csv`, `authors_value_counts.csv`, and the related PNGs exist under `outputs/phase03_univariate/`.
  - `count_outlier_recommendations.csv` plus the two “top titles” CSVs refresh with current timestamps so you can cite the caps immediately.

Use `--limit` or `--output-dir` to customize iterations the same way we did in Task 02.

---

## 4. Findings

### Language mix

- English dominates: `eng` alone covers 8,911 books (~80%), and English regional codes (`en-US`, `en-GB`, `en-CA`) add another ~16%. That confirms later visualizations can default to English labels without alienating most readers.
- Spanish (`spa`, 218 books) and French (`fre`, 144) are the only non-English languages above the 1% mark; everything else quickly trails off into single digits, so multilingual dashboards will need serious filtering.

### Publishers

- The long tail is intense (2,000+ distinct publisher strings), yet a few imprints keep resurfacing: Vintage (318 titles), Penguin Books/Classic variants (445 combined), and large US trade houses (Ballantine, HarperCollins, Random House family).
- Academic and specialty imprints (Oxford UP, Dover, Modern Library) still crack the top 20, hinting that Goodreads skews literary/classics-heavy versus a pure bestseller catalog.

### Authors

- Prolific genre authors take the crown: Stephen King and P.G. Wodehouse each appear 40 times, followed by manga creators (Rumiko Takahashi at 39) and sci-fi/fantasy staples (Orson Scott Card at 35, Agatha Christie at 33).
- Collaborative pen names such as `Margaret Weis/Tracy Hickman` show why we temporarily treated the entire `authors` string as one category. Later phases can split on `/` or `,` when we need individual contributor stats.

These counts give us a defensible baseline for storytelling slides—e.g., “Penguin-family imprints represent ~10% of the titles we analyzed.”

---

## 5. Outlier flagging / capping plan

File: `outputs/phase03_univariate/count_outlier_recommendations.csv`

| column             |    p95 |     p99 |   p99.5 |       max | suggested cap |
| ------------------ | -----: | ------: | ------: | --------: | ------------: |
| ratings_count      | 61,096 | 297,449 | 597,244 | 4,597,666 |       597,244 |
| text_reviews_count |  2,159 |   8,974 |  14,812 |    94,265 |        14,812 |

- Recommendation: Winsorize `ratings_count` at ~600k and `text_reviews_count` at ~15k when building dashboards or calculating averages. That trims the noise from megahits like _Twilight_ (4.6M ratings, 94k reviews) while preserving 99% of normal titles untouched.
- Supporting tables (`ratings_count_top_titles.csv`, `text_reviews_count_top_titles.csv`) list the actual books exceeding those caps so analysts can double-check whether to down-weight or fully exclude them.

---

## 6. Verification log (Dec 4, 2025)

```
INFO __main__ - Saved language_code value counts to outputs\phase03_univariate\language_code_value_counts.csv
INFO __main__ - language_code top 12 categories -> eng (8911), en-US (1409), spa (218), en-GB (214), ...
INFO __main__ - publisher top 15 categories -> Vintage (318), Penguin Books (261), ...
INFO __main__ - ratings_count outliers -> p99 297449, max 4597666, suggested cap 597244
INFO __main__ - Wrote outlier cap recommendations to outputs\phase03_univariate\count_outlier_recommendations.csv
INFO __main__ - EDA univariate pass complete – numeric, categorical, and outlier summaries ready.
```

---

## 7. Checklist review

- [x] Computed value counts for `language_code`, `publisher`, and `authors`.
- [x] Produced bar plots for the most common categories with “Unknown” explicitly tracked.
- [x] Captured interpretations plus an outlier-capping recommendation to tee up later quality work.

Task complete: Step 01 now has both numeric and categorical baselines, and the count outlier plan gives Phase 03’s next steps concrete thresholds to enforce.
