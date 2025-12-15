# Phase 04 · Step 04 · Task 01 – Executive Summary & Key Findings

## 1. Executive Summary

This phase delivers a reproducible, portfolio-ready analysis of the Goodreads books dataset, focusing on business questions relevant to publishing, reader engagement, and catalog quality. The workflow is fully Dockerized, ensuring that any beginner or reviewer can rerun the cleaning, metrics, and visualization steps with a single command. All outputs are documented and saved for transparency and ease of presentation.

- **Dataset:** 11,127 curated book records from Goodreads, cleaned and deduplicated using canonical mapping and engagement caps.
- **Pipeline:** Python scripts executed in Docker, with all metrics and visualizations generated from standardized CSVs.
- **Artifacts:** Cleaned dataset, metrics catalog, eight core metric CSVs, and eight portfolio-ready figures.

## 2. Key Findings

1. **Top Authors by Weighted Rating:**

   - Bill Watterson leads with a 4.71 weighted rating across 144,799 ratings (7 canonical titles).
   - Manga localization teams fill most of the top 10, confirming genre bias in reader engagement.
   - _See_: `M1_top_authors_by_weighted_rating.png`

2. **Top Books by Ratings Count:**

   - Blockbuster fantasy and required reading dominate the leaderboard (Twilight, Potter, Tolkien).
   - _See_: `M3_top_books_by_ratings_count.png`

3. **Top Books by Text Reviews:**

   - YA titles attract the most written commentary, with Twilight and The Book Thief leading.
   - _See_: `M4_top_books_by_text_reviews.png`

4. **Median Rating by Page Length Bucket:**

   - Multi-volume works score the highest median rating (~4.44).
   - Short-reference and audio/zero-page books cluster near 3.95.
   - _See_: `M5_median_rating_by_page_length.png`

5. **Average Rating by Publication Year:**

   - Sentiment peaks around 1984–1991 (~4.01–4.02 average), then gradually declines toward 3.91 by 2006.
   - _See_: `M7_average_rating_by_year.png`

6. **Median Ratings Count by Publication Year:**

   - Reader attention accelerates post-1998, with medians passing 900 by 2004 and spiking above 2,500 for 2012.
   - _See_: `M8_median_ratings_count_by_year.png`

7. **Average Rating by Language:**

   - French and German outpace English in average rating, but English retains audience scale.
   - _See_: `M9_language_rating_summary.png`

8. **Duplicate Share of Catalog:**
   - Only 16 rows (0.14%) are flagged as duplicates, but canonical IDs are essential for accurate aggregations.
   - _See_: `M11_duplicate_share.png`

## 3. Portfolio Guidance

- All figures and CSVs are saved in `outputs/phase04_visualizations/` and `outputs/phase04_core_metrics/`.
- Each chart is referenced by filename and caption in the notes for easy inclusion in presentations or case studies.
- The entire workflow is documented in beginner-friendly language, with step-by-step instructions in the notes and FAQ.

## 4. How to Reproduce

1. Run the cleaning and metrics pipeline as documented in Step 01 and Step 02 notes.
2. Generate all visualizations using the Docker command:
   ```powershell
   docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm app python -m src.analyses.plot_phase04_visualizations --input-dir outputs/phase04_core_metrics --output-dir outputs/phase04_visualizations
   ```
3. Reference the figures and findings in your portfolio, presentation, or case study.

## 5. Next Steps

- Extend the analysis with stretch metrics (author engagement index, publisher-level engagement).
- Add annotated scatter plots for outlier detection and deeper insight.
- Integrate SQL-based validation in Phase 05 for cross-platform comparison.
- Update the FAQ and glossary as new features and findings are added.

---

This summary is designed for portfolio reviewers and beginners. All findings are reproducible, clearly documented, and mapped to concrete artifacts for maximum transparency and impact.
