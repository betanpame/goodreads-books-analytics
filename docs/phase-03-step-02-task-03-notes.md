# Phase 03 - Step 02 - Task 03 - Relationships by Category

This note documents **Phase 03 - Step 02 - Task 03**, where the goal was to profile how Goodreads ratings and engagement shift across key categorical dimensions. Deliverables: aggregated metrics for at least two categories (language and publisher), visual comparisons (bar charts/boxplots), and portfolio-friendly commentary highlighting rating lifts or engagement gaps.

---

## 1. Task definition and goal

From `plan/phase-03-eda-and-data-quality/steps/step-02-bivariate-eda/tasks/task-03-relationships-by-category.md`:

- Pick at least two categorical columns (I selected `language_code` and `publisher`).
- Limit the view to the top N categories so the charts are readable (top 10 languages, top 15 publishers by book count).
- Per category, compute **average rating**, **median ratings_count**, and **book counts** (I also logged median `text_reviews_count` for extra engagement context).
- Produce visual comparisons (bar charts) and document which categories lead on quality vs. popularity.

---

## 2. Script updates (`src/analyses/eda_books.py`)

- Added `CATEGORY_RELATIONSHIP_PLAN` plus a new `analyze_category_relationships()` function that:
  - Normalizes categorical strings (`Unknown` fallback) and filters to the configured "top N" buckets.
  - Aggregates the required metrics and writes CSV summaries plus paired bar charts for rating and engagement signals under `outputs/phase03_univariate/step02_task03_category_relationships/`.
  - Logs exactly which subset was produced (e.g., "Language category summary ... top 10").
- Introduced `plot_category_metric_bar()` to centralize the bar-chart styling so both rating and engagement plots stay consistent.
- Updated the CLI's completion log to mention the new artifacts and wired the analyzer into `main()` so every run refreshes the categorical outputs alongside the existing numeric/categorical/temporal tasks.

---

## 3. How to run it

From `C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`:

```powershell
# Local Python virtualenv
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books

# Or inside Docker
docker compose -f docker-compose.python.yml run --rm app \
    python -m src.analyses.eda_books
```

New artifacts for this task:

- `language_category_summary.csv` + `avg_rating_by_language.png` + `median_ratings_count_by_language.png`
- `publisher_category_summary.csv` + `avg_rating_by_publisher.png` + `median_ratings_count_by_publisher.png`

All six files live in `outputs/phase03_univariate/step02_task03_category_relationships/`.

---

## 4. Findings

### Language-level patterns (top 10 by volume)

- **Quality leaders**: `zho` (Mandarin titles) average **4.46** stars and `jpn` averages **4.27**, but both cohorts are tiny (14 and 46 books respectively). Treat them as signal flare, not a market-sized trend.
- **Core catalog**: English-language entries (`eng`, `en-US`, `en-GB`) hover near **3.91–3.94** stars, forming 97% of the dataset. Their consistency gives us the most reliable benchmark for future comparisons.
- **Engagement**: Median `ratings_count` for `eng` sits around **2,300**, while smaller-language cohorts rarely cross triple digits. This validates that English results drive the platform’s popularity metrics, even if niche languages peak higher on satisfaction.

### Publisher-level patterns (top 15 by volume)

- **Highest-rated publishers**: `VIZ Media LLC` (manga-heavy catalog) tops the list at **4.24** stars across 88 books. `Del Rey` and `HarperCollins` also exceed **4.0** while maintaining 80–112 titles, implying fantasy/SF imprints can balance quality with scale.
- **Engagement spikes**: Mass-market imprints (`Ballantine Books`, `Pocket Books`, `Bantam`, `Berkley`) dominate the median `ratings_count` charts (≈140–220 median reviews). Their ratings linger around 3.88–3.90, so they trade slightly lower sentiment for far more reach.
- **Actionable split**: Use the rating chart when prioritizing prestige-focused partnerships, and the engagement chart when seeking publishers whose titles reliably trigger conversation.

### Practical takeaways

1. **Segment audiences by language before comparing averages.** The high-scoring niche languages have low denominators, so product decisions should rely on the English cohorts unless we can enrich metadata for other locales.
2. **Publisher strategy can bifurcate:** prestige imprints (VIZ Media, Del Rey) raise ratings; mass-market imprints excel at driving participation. Future marketing experiments can map these groups to different campaign goals.
3. **Artifacts are reusable.** Any dashboard or notebook can ingest the CSVs to retell the story without recomputing the aggregations.

---

## 5. Verification log (Dec 4, 2025)

```
2025-12-04 20:35:43,088 INFO __main__ - Loading dataset from data\books.csv
2025-12-04 20:35:49,334 INFO __main__ - Language category summary saved to outputs\phase03_univariate\step02_task03_category_relationships\language_category_summary.csv (top 10)
2025-12-04 20:35:50,003 INFO __main__ - Publisher category summary saved to outputs\phase03_univariate\step02_task03_category_relationships\publisher_category_summary.csv (top 15)
2025-12-04 20:35:50,707 INFO __main__ - EDA pass complete – numeric, categorical, temporal, outlier, rating, and category relationship artifacts ready.
```

---

## 6. Checklist review

- [x] Analyzed two categorical dimensions (language + publisher) with clear "top N" rules.
- [x] Computed average rating, median ratings_count, median text_reviews_count, and book counts per category.
- [x] Generated rating and engagement bar charts, plus CSV exports for downstream reuse.
- [x] Captured narrative-ready insights including caveats about small-sample languages.
