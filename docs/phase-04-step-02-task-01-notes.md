# Phase 04 · Step 02 · Task 01 – Define Business Questions & Metrics

## 1. Task definition and goal

Translate the Phase 04 charter into a portfolio-ready list of business questions and measurable metrics that can be computed from `books_clean.csv`. The deliverable is a curated metrics catalog (plus documentation) that beginners can rerun inside Docker without touching notebooks.

## 2. How to run this analysis script

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm `
  app python -m src.analyses.metrics_catalog `
  --books-csv data/derived/books_clean.csv `
  --output-markdown outputs/phase04_metrics_catalog.md
```

- `--no-deps` keeps the workflow Python-only; drop it if you also need PostgreSQL running.
- The script validates required columns, logs coverage stats, and writes a Markdown table for reuse in docs/dashboards.

## 3. Environment recap

- **Runtime:** `python:3.14-slim` container (same image as the cleaning CLI) with pandas 2.x installed through `requirements.txt`.
- **Entrypoint:** `src/analyses/metrics_catalog.py` (new for this task) orchestrates metric definitions and dataset validation.
- **Inputs:** `data/derived/books_clean.csv` generated in Step 01 plus the Phase 03 rulebook for business context.

## 4. Findings / results

### 4.1 Business questions (Q1–Q6)

1. **Q1 – High-performing authors:** Which authors deliver consistently high-rated titles with meaningful readership?
2. **Q2 – Engagement magnets:** Which canonical books mobilize the most ratings and written reviews?
3. **Q3 – Page count effect:** How does book length influence satisfaction and reader engagement cohorts?
4. **Q4 – Publication momentum:** How have average ratings and attention shifted across publication years?
5. **Q5 – Language & publisher mix:** Which languages and publishers dominate both quality and reach?
6. **Q6 – Duplicate impact:** What portion of the catalog consists of deduplicated editions and how much do they matter?

### 4.2 Metrics catalog (auto-generated)

The CLI wrote `outputs/phase04_metrics_catalog.md`. Snapshot:

| Question                                                                              | Metric                                               | Description                                                                            | Columns                                                                   | Notes                                                                                    | Priority |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------- |
| Q1 – Which authors deliver consistently high-rated titles with meaningful readership? | M1 – Top authors by weighted average rating          | Average rating per author with ratings_count >= 5,000 to avoid tiny sample bias.       | `authors, average_rating, ratings_count`                                  | Weight by ratings_count to keep blockbusters influential while still surfacing quality.  | core     |
| Q1 – Which authors deliver consistently high-rated titles with meaningful readership? | M2 – Author engagement index                         | Combined z-score of ratings_count_capped and text_reviews_count_capped per author.     | `authors, ratings_count_capped, text_reviews_count_capped`                | Helps compare participation-heavy fandoms beyond raw averages.                           | stretch  |
| Q2 – Which individual books capture the most reader engagement?                       | M3 – Top books by ratings_count_capped               | Leaderboard of canonical books sorted by capped ratings counts.                        | `canonical_book_id, title, ratings_count_capped, ratings_count`           | Use canonical IDs so audiobook duplicates do not double-count.                           | core     |
| Q2 – Which individual books capture the most reader engagement?                       | M4 – Top books by text_reviews_count_capped          | Highlight books that spark the most written discussion.                                | `canonical_book_id, title, text_reviews_count_capped, text_reviews_count` | Pairs with M3 to compare silent ratings vs vocal reviews.                                | core     |
| Q3 – How does book length influence satisfaction and engagement?                      | M5 – Median rating by page_length_bucket             | Compare sentiment across short_reference / standard / multi_volume buckets.            | `page_length_bucket, average_rating`                                      | Bucket definitions come from Phase 03 rulebook; zero_or_audio is its own cohort.         | core     |
| Q3 – How does book length influence satisfaction and engagement?                      | M6 – Engagement delta by page_length_bucket          | Median ratings_count_capped + text_reviews_count_capped per bucket.                    | `page_length_bucket, ratings_count_capped, text_reviews_count_capped`     | Surface whether long reads actually earn more participation or just niche love.          | stretch  |
| Q4 – How have publication trends influenced quality and reach over time?              | M7 – Average rating by publication_year              | Line chart-ready series summarizing sentiment per release year.                        | `publication_year, average_rating`                                        | Drop rows with null publication_year to prevent misleading dips.                         | core     |
| Q4 – How have publication trends influenced quality and reach over time?              | M8 – Median ratings_count_capped by publication_year | Shows whether new releases are attracting comparable attention versus backlist titles. | `publication_year, ratings_count_capped`                                  | Use median to dampen runaway outliers in 2003–2006 era.                                  | core     |
| Q5 – Which languages and publishers dominate catalog quality and reach?               | M9 – Average rating by language_code                 | Ranks languages with at least 50 canonical titles to keep cohorts meaningful.          | `language_code, canonical_book_id, average_rating`                        | Filter `language_code` != null and require book_count >= 50.                             | core     |
| Q5 – Which languages and publishers dominate catalog quality and reach?               | M10 – Median ratings_count_capped by publisher       | Highlights publishers that consistently mobilize large audiences.                      | `publisher, canonical_book_id, ratings_count_capped`                      | Limit to publishers with >= 25 canonical titles to avoid vanity presses skewing results. | stretch  |
| Q6 – What portion of the catalog consists of deduplicated editions?                   | M11 – Duplicate share of catalog                     | Percentage of rows where is_duplicate == True.                                         | `is_duplicate, canonical_book_id`                                         | Communicates why canonical IDs are required for dashboards.                              | core     |
| Q6 – What portion of the catalog consists of deduplicated editions?                   | M12 – Engagement uplift for canonical editions       | Compare median ratings_count between canonical parents and duplicate children.         | `canonical_book_id, is_duplicate, ratings_count`                          | Quantifies whether duplicate SKUs materially change demand signals.                      | stretch  |

### 4.3 Core metric shortlist

- M1, M3, M4, M5, M7, M8, M9, M11 are tagged **core** and will be implemented first.
- Stretch metrics (M2, M6, M10, M12) remain on deck for future sprints but already have column contracts defined.

### 4.4 Coverage snapshot from CLI logs

- Non-null counts: `average_rating=11,101`, `ratings_count=11,127`, `text_reviews_count=11,127`, `num_pages=11,051`, `publication_year=11,125`.
- Duplicate share: **0.14%** (16 rows), reinforcing the need for `canonical_book_id` in every aggregation.

## 5. Expected output checkpoints

- `Loaded 11,127 rows and 27 columns` – ensures `books_clean.csv` exists and includes canonical fields.
- `All 17 required columns are present` – column validation passed.
- `Non-null coverage snapshot: {...}` – confirms the script inspected the dataset.
- `Metrics_catalog written to outputs/phase04_metrics_catalog.md` – Markdown artifact generated.
- `Defined 12 metrics across 6 business questions` – sanity check on catalog breadth.

## 6. Observations / insights

- Keeping everything in Docker avoids Windows path quirks and guarantees pandas + dataclasses versions stay consistent for reviewers.
- Documenting priorities alongside metrics prevents scope creep when we implement Step 02 Task 02 (metric computation).
- The duplicate share metric (0.14%) is tiny yet crucial—in dashboards, it’s an instant proof that canonical IDs prevent subtle double counting.

## 7. Artifacts refreshed each run

- `src/analyses/metrics_catalog.py` – executable reference for the metric catalog.
- `outputs/phase04_metrics_catalog.md` – Markdown table imported into docs/presentations.
- `data/derived/books_clean.csv` – regenerated earlier in this session to drop `_x/_y` column noise before planning.

## 8. Q&A / data troubleshooting

| Question                                            | Answer                                                                                                                                  |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Where do I see the latest metric definitions?       | Run the CLI above or open `outputs/phase04_metrics_catalog.md`; both stay under version control for transparency.                       |
| How do I update a metric’s filter/threshold?        | Edit `METRIC_DEFINITIONS` inside `metrics_catalog.py` and re-run the script; validation ensures needed columns exist.                   |
| What if the script complains about missing columns? | Re-run the Step 01 cleaning CLI to regenerate `books_clean.csv`, then verify the columns listed in `KEY_COLUMNS` (see FAQ for details). |

## 9. Checklist review

- [x] EDA findings reviewed and referenced (Phase 03 notes + cleaned dataset stats).
- [x] 5–8 business questions written down (we have 6 focused areas).
- [x] At least one metric per question (12 total metrics).
- [x] Mapping table `Question -> Metric -> Columns -> Notes` created via CLI output.
- [x] Core vs stretch metrics prioritized for implementation.

## 10. Appendices (log excerpt)

```
2025-12-05 04:52:20,331 INFO __main__ - Loaded 11,127 rows and 27 columns
2025-12-05 04:52:20,332 INFO __main__ - All 17 required columns are present
2025-12-05 04:52:20,333 INFO __main__ - Duplicate share: 0.14%
2025-12-05 04:52:20,349 INFO __main__ - Metrics catalog written to outputs/phase04_metrics_catalog.md
2025-12-05 04:52:20,350 INFO __main__ - Defined 12 metrics across 6 business questions
```

The CLI timestamps are UTC because the container runs in UTC; the local calendar date was 2025-12-04.
