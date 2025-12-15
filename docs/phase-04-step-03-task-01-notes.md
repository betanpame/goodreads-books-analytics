# Phase 04 · Step 03 · Task 01 – Visualization Plan

## 1. Task definition and goal

Design a portfolio-ready visualization plan that answers the business questions and showcases the metrics computed in Phase 04. This note will guide beginners through the process of mapping metrics to charts, selecting appropriate chart types, and preparing for reproducible, professional visualizations.

## 2. Visualization planning workflow

Follow these steps to create a clear, actionable visualization plan:

### Step 1: List candidate charts for each business question

- Review the metrics catalog (see `outputs/phase04_metrics_catalog.md` and Step 02 notes).
- For each business question, brainstorm 1–2 chart types that best communicate the insight.

### Step 2: Map metrics to chart types

- For each metric, select the most effective chart type (bar, line, scatter, boxplot, etc.).
- Document the rationale for each choice so beginners understand why it fits the data.

### Step 3: Create a visualization plan table

- Build a markdown table with columns:
  - Question
  - Metric(s)
  - Dataset / Table
  - Chart type
  - X axis
  - Y axis
  - Filters / Notes

### Step 4: Prioritize 5–8 must-have charts

- Mark the most important charts for the portfolio.
- List optional extras for future improvement.

## 3. Visualization plan table

| Question                     | Metric(s)                                           | Dataset / Table                       | Chart type     | X axis             | Y axis                        | Filters / Notes                       |
| ---------------------------- | --------------------------------------------------- | ------------------------------------- | -------------- | ------------------ | ----------------------------- | ------------------------------------- |
| Q1: High-performing authors  | M1: Top authors by weighted rating                  | M1_top_authors_by_weighted_rating.csv | Horizontal bar | Author             | Weighted rating               | Top 15 authors, ratings_count ≥ 5,000 |
| Q2: Engagement magnets       | M3: Top books by ratings_count_capped               | M3_top_books_by_ratings_count.csv     | Horizontal bar | Book title         | Ratings count (capped)        | Top 20 books                          |
| Q2: Engagement magnets       | M4: Top books by text_reviews_count_capped          | M4_top_books_by_text_reviews.csv      | Horizontal bar | Book title         | Text reviews count (capped)   | Top 20 books                          |
| Q3: Page count effect        | M5: Median rating by page_length_bucket             | M5_median_rating_by_page_length.csv   | Boxplot        | Page length bucket | Median rating                 | All buckets                           |
| Q4: Publication momentum     | M7: Average rating by publication_year              | M7_average_rating_by_year.csv         | Line           | Publication year   | Average rating                | Years 1900–2012                       |
| Q4: Publication momentum     | M8: Median ratings_count_capped by publication_year | M8_median_ratings_count_by_year.csv   | Line           | Publication year   | Median ratings count (capped) | Years 1900–2012                       |
| Q5: Language & publisher mix | M9: Average rating by language_code                 | M9_language_rating_summary.csv        | Bar            | Language code      | Average rating                | Languages with ≥50 books              |
| Q6: Duplicate impact         | M11: Duplicate share of catalog                     | M11_duplicate_share.csv               | Pie            | Duplicate status   | Share (%)                     | Canonical vs duplicate                |

## 4. Chart prioritization

**Must-have charts:**

- Top authors by weighted rating (Q1)
- Top books by ratings count (Q2)
- Top books by text reviews (Q2)
- Median rating by page length bucket (Q3)
- Average rating by publication year (Q4)
- Median ratings count by publication year (Q4)
- Average rating by language (Q5)
- Duplicate share pie chart (Q6)

**Optional extras:**

- Author engagement index (stretch metric)
- Publisher-level engagement (stretch metric)
- Annotated scatter plots for outlier detection

## 5. Chart outputs and documentation

All must-have charts have been generated using the portfolio visualization script (`src/analyses/plot_phase04_visualizations.py`). Each figure is saved in `outputs/phase04_visualizations/` and includes a caption for clarity and reproducibility.

### Chart outputs and captions

1. **Top Authors by Weighted Rating**

- File: `M1_top_authors_by_weighted_rating.png`
- Caption: Shows the 15 highest-rated authors (weighted by ratings count, min 5,000 ratings).
- Data: `author_name`, `weighted_average_rating`, `total_ratings`, `book_count`.

2. **Top Books by Ratings Count (Capped)**

- File: `M3_top_books_by_ratings_count.png`
- Caption: Highlights the 20 most-rated books (ratings count capped at 597,244).
- Data: `title`, `ratings_count_capped`.

3. **Top Books by Text Reviews (Capped)**

- File: `M4_top_books_by_text_reviews.png`
- Caption: Highlights the 20 books with the most text reviews (capped at 14,812).
- Data: `title`, `text_reviews_count_capped`.

4. **Median Rating by Page Length Bucket**

- File: `M5_median_rating_by_page_length.png`
- Caption: Compares median ratings across page length buckets (multi_volume, short_reference, zero_or_audio).
- Data: `page_length_bucket`, `median_rating`.

5. **Average Rating by Publication Year**

- File: `M7_average_rating_by_year.png`
- Caption: Shows average rating trends from 1900 to 2012.
- Data: `publication_year`, `average_rating`.

6. **Median Ratings Count by Publication Year**

- File: `M8_median_ratings_count_by_year.png`
- Caption: Shows median ratings count trends from 1900 to 2012.
- Data: `publication_year`, `median_ratings_count_capped`.

7. **Average Rating by Language**

- File: `M9_language_rating_summary.png`
- Caption: Ranks languages with at least 50 canonical books by average rating.
- Data: `language_code`, `average_rating`.

8. **Duplicate Share of Catalog**

- File: `M11_duplicate_share.png`
- Caption: Pie chart showing the proportion of canonical vs duplicate rows in the catalog.
- Data: `total_rows`, `duplicate_rows`, `duplicate_share_pct`.

### How to reproduce these figures

1. Ensure all metric CSVs exist in `outputs/phase04_core_metrics/`.
2. Run the visualization script inside Docker:

```powershell
docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm app python -m src.analyses.plot_phase04_visualizations --input-dir outputs/phase04_core_metrics --output-dir outputs/phase04_visualizations
```

3. All figures will be saved in `outputs/phase04_visualizations/` with descriptive filenames.
4. Each chart is documented with a caption in this note and can be referenced in portfolio presentations or case studies.

## 6. Success checklist

- [x] Visualization plan table completed and reviewed
- [x] Chart types and axes clearly documented
- [x] Must-have charts prioritized and generated
- [x] Implementation steps outlined for beginners
- [x] All notes written in professional, beginner-friendly language
- [x] Chart outputs and captions documented for portfolio use

## 7. FAQ and troubleshooting (see `data-faq.md`)

- How do I rerun the visualization scripts? (Docker command above)
- Where are the figures saved? (`outputs/phase04_visualizations/`)
- What if a chart fails to render? (Check CSV paths, Python package versions)

## 8. Glossary additions (see `phase-04-glossary.md`)

- Visualization plan: The structured mapping of business questions to chart types, datasets, and axes.
- Figure: A saved image file (PNG/SVG) representing a chart or plot.
- Caption: A short description under each chart explaining its meaning and relevance.
- Portfolio-ready: Charts and notes formatted for clarity, reproducibility, and professional presentation.

---

This note is designed for portfolio reviewers and beginners alike. All steps and outputs are documented to ensure your visualizations are clear, reproducible, and directly answer the business questions posed in Phase 04.
