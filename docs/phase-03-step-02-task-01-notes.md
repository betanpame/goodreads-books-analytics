# Phase 03 – Step 02 – Task 01 – Relationships Between Rating and Size

This note captures how I executed **Phase 03 → Step 02 → Task 01**. The goal was to quantify and visualize how Goodreads ratings behave relative to book size and engagement metrics, while keeping the write-up portfolio-ready and beginner friendly.

---

## 1. Task definition and goal

From `plan/phase-03-eda-and-data-quality/steps/step-02-bivariate-eda/tasks/task-01-relationships-between-rating-and-size.md`, the deliverables were:

- Scatter (or equivalent) plots for `average_rating` versus `num_pages`, `ratings_count`, and `text_reviews_count`.
- Appropriate scaling (log axes or bucketed summaries) so the heavy-tailed “popularity” metrics remain readable.
- Commentary that answers practical questions, such as whether longer books tend to earn better scores or whether popular titles receive harsher/lower ratings.

---

## 2. Script updates (`src/analyses/eda_books.py`)

- Expanded the module scope beyond univariate summaries by adding `analyze_rating_relationships()`.
- Added helper utilities (`plot_scatter_relationship`, `log_pair_summary`, `summarize_page_buckets`) plus constants for:
  - Page-count buckets: `[0–199, 200–399, 400–599, 600+]`.
  - Popularity caps: `ratings_count` clipped at 597,244 and `text_reviews_count` clipped at 14,812 (the p99.5 thresholds from Step 01 Task 03). This protects scatter plots from being dominated by one or two mega-franchises.
- All new artifacts land under `outputs/phase03_univariate/step02_task01_relationships/` so future Python scripts, dashboards, or Docker jobs can reuse the CSV/PNG outputs without recalculating.

The rest of the CLI (`--csv-path`, `--limit`, `--output-dir`, `--verbose`) stays the same, so onboarding remains simple.

---

## 3. How to run it

From the repository root (`C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`):

```powershell
# Local Python virtualenv
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe `
  -m src.analyses.eda_books `
  --verbose

# Or inside Docker
docker compose -f docker-compose.python.yml run --rm app \
  python -m src.analyses.eda_books --verbose
```

Key outputs for this task:

- `average_rating_vs_pages_scatter.png`
- `average_rating_vs_ratings_count_scatter.png`
- `average_rating_vs_text_reviews_scatter.png`
- `average_rating_by_page_bucket.csv`
- `average_rating_by_page_bucket_bar.png`

All five files live in `outputs/phase03_univariate/step02_task01_relationships/`.

---

## 4. Findings

### Length vs. rating

- **Correlation:** `num_pages` vs. `average_rating` shows a modest positive Pearson correlation of **0.151 (n ≈ 11k)**.
- **Bucketed insight:**
  | Page bucket | Avg rating | Median rating | Book count |
  | ----------- | ---------: | ------------: | ----------: |
  | 0–199 | 3.92 | 3.96 | 2,898 |
  | 200–399 | 3.89 | 3.92 | 5,104 |
  | 400–599 | 3.97 | 3.99 | 2,050 |
  | 600+ | 4.09 | 4.12 | 1,075 |
- **Takeaway:** Longer works trend slightly higher. A 600+ page release averages ~0.2 stars more than a sub-200 page novella. That’s a small gap, but it suggests epic fantasy/literary sagas resonate more with Goodreads’ core audience.

### Ratings count vs. rating

- After clipping at 597k and applying a log-x axis, the scatter shows a dense vertical band between 10² and 10⁴ ratings.
- **Correlation:** `0.054` – essentially flat. Popular books do **not** inherently receive better or worse ratings once we control for the extreme outliers.
- **Interpretation:** Readers maintain roughly the same sentiment regardless of how many people rated the title. Popularity affects visibility, not necessarily quality perception.

### Text reviews count vs. rating

- Also log-scaled and capped (14,812). The Pearson correlation is **0.043**, reinforcing that written-review volume is mostly independent of rating score.
- Interpretation for stakeholders: emphasizing “review campaigns” might boost engagement metrics but won’t automatically elevate a title’s average rating.

Overall, Step 02 Task 01 indicates that **length** has the clearest (though still moderate) relationship with ratings, while sheer popularity metrics do not move the needle much.

---

## 5. Verification log (Dec 4, 2025)

```
INFO __main__ - Saved relationship plot to outputs\phase03_univariate\step02_task01_relationships\average_rating_vs_pages_scatter.png
INFO __main__ - num_pages vs rating -> n=11127, pearson_corr=0.151, x_median=299.00, y_median=3.96
INFO __main__ - Saved relationship plot to outputs\phase03_univariate\step02_task01_relationships\average_rating_vs_ratings_count_scatter.png
INFO __main__ - ratings_count vs rating -> n=11127, pearson_corr=0.054, x_median=745.00, y_median=3.96
INFO __main__ - Saved relationship plot to outputs\phase03_univariate\step02_task01_relationships\average_rating_vs_text_reviews_scatter.png
INFO __main__ - text_reviews_count vs rating -> n=11127, pearson_corr=0.043, x_median=46.00, y_median=3.96
INFO __main__ - Saved page bucket summary to outputs\phase03_univariate\step02_task01_relationships\average_rating_by_page_bucket.csv
INFO __main__ - EDA pass complete – numeric, categorical, outlier, and rating relationship artifacts ready.
```

---

## 6. Checklist review

- [x] Created scatter plots for rating vs. `num_pages`, `ratings_count`, and `text_reviews_count`, using transparency and log scales to fight overplotting.
- [x] Bucketed page counts to show trend lines a beginner can interpret without reading scatter plots.
- [x] Documented the minimal relationship between engagement counts and ratings, and the slight lift for longer books.

Task complete. These artifacts close out Step 02 Task 01 and provide the baseline needed before moving on to temporal and categorical relationship analyses.
