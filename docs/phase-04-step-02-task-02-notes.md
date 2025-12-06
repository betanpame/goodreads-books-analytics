# Phase 04 · Step 02 · Task 02 – Implement Core Metrics

## 1. Task definition and goal

Implement reproducible Python/Docker functions that compute the core metrics (M1, M3, M4, M5, M7, M8, M9, M11) defined in Task 01. Each metric now has a documented function, CSV artifact, and CLI so hiring managers can see the exact logic used to answer the Phase 04 business questions.

## 2. How to run this analysis script

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
# Option A – direct command
docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm `
  app python -m src.analyses.portfolio.p03_core_metrics_suite `
  --books-csv data/derived/books_clean.csv `
  --output-dir outputs/phase04_core_metrics

# Option B – one-command wrapper
make core-metrics
```

- `--no-deps` keeps the execution limited to the Python container (no PostgreSQL).
- CLI flags expose thresholds (`--author-min-ratings`, `--books-top-n`, `--language-min-books`, `--min-year`).
- `make core-metrics` uses the same Docker invocation so reviewers only need one command.

## 3. Environment recap

- **Image:** `python:3.14-slim` (identical to Step 01 cleaning runs).
- **Dependencies:** pandas 2.x from `requirements.txt`; functions live in `src/metrics/core_metrics.py`.
- **Entrypoint:** `src/analyses/portfolio/p03_core_metrics_suite.py` orchestrates loading, validation, metric generation, and CSV export.
- **Data:** `data/derived/books_clean.csv` (regenerated earlier) is the single input; all outputs land in `outputs/phase04_core_metrics/`.

## 4. Findings / results

| Metric                                            | Highlight                                                                                                                                                                                                                                                                     |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M1 – Top authors by weighted rating**           | Bill Watterson leads with a 4.71 weighted rating across 144,799 ratings (7 canonical titles). Manga localization teams (Kelly Jones, Lee Loughridge, Matt Thorn) fill most of the top 10, proving the page-turner bias we saw in Phase 03.                                    |
| **M3 – Top books by ratings_count**               | `Twilight` still tops the ratings leaderboard with 4.60M raw ratings (capped to 597K for visuals). The rest of the list is dominated by Potter, Tolkien, and high-school staples, confirming engagement skews toward blockbuster fantasy + required reading.                  |
| **M4 – Top books by text reviews**                | `Twilight`, `The Book Thief`, and `The Giver` attract the most written commentary (94K, 86K, 56K reviews respectively), emphasizing YA’s discussion-heavy fandoms.                                                                                                            |
| **M5 – Median rating by page bucket**             | Multi-volume works score the highest median rating (≈4.44 across 12 titles). Zero-page (audio) and short-reference cohorts cluster near 3.95, matching the neutral tone observed during EDA.                                                                                  |
| **M7 – Average rating by publication year**       | The curve spans 1900–2012 and stays between 3.9–4.0. Peak sentiment occurs around 1984–1991 (~4.01–4.02 average), then gradually declines toward 3.91 by 2006 as the catalog fills with mass-market releases.                                                                 |
| **M8 – Median ratings_count by publication year** | Reader attention accelerates sharply post-1998: medians pass 900 by 2004, hit 1.1K in 2006, and spike above 2.5K for the small 2012 cohort, indicating that modern titles either soar or disappear—there’s less middle ground.                                                |
| **M9 – Average rating by language**               | Only six languages beat the ≥50-title criterion. French (`fre`, 3.97 avg) and German (`ger`, 3.95 avg) outpace English, though both draw tiny engagement (median capped ratings ≤100). English variants (US/GB) retain the audience scale (book_count ≥200, medians 198–531). |
| **M11 – Duplicate share**                         | Just 16 rows (0.1438%) are flagged duplicates, but surfacing this metric proves why canonical IDs are still mandatory for accurate aggregations.                                                                                                                              |

## 5. Expected output checkpoints

- `[INFO] Loaded 11,127 rows and 27 columns` – confirms the cleaned dataset was present.
- Eight log lines starting with `Wrote … rows to outputs/phase04_core_metrics/...` – ensures every metric produced a CSV.
- Final line `Generated 8 metric tables` – sanity check that no DataFrame was empty.

## 6. Observations / insights

- Exploding authors via `explode_authors` and weighting by ratings_count avoids the “single novella beats Rowling” issue mentioned in Task 01.
- Canonical rollups (one row per `canonical_book_id`) keep audiobook duplicates from flooding leaderboards while still taking the max engagement value across editions.
- The new `Makefile` targets (`metrics-catalog`, `core-metrics`) give reviewers parity with Docker commands even if they haven’t memorized the full syntax.

## 7. Artifacts refreshed each run

- **Code:** `src/metrics/core_metrics.py`, `src/analyses/run_core_metrics.py`, and `Makefile` (new entries) document the reusable logic.
- **Outputs:**
  - `outputs/phase04_core_metrics/M1_top_authors_by_weighted_rating.csv`
  - `outputs/phase04_core_metrics/M3_top_books_by_ratings_count.csv`
  - `outputs/phase04_core_metrics/M4_top_books_by_text_reviews.csv`
  - `outputs/phase04_core_metrics/M5_median_rating_by_page_length.csv`
  - `outputs/phase04_core_metrics/M7_average_rating_by_year.csv`
  - `outputs/phase04_core_metrics/M8_median_ratings_count_by_year.csv`
  - `outputs/phase04_core_metrics/M9_language_rating_summary.csv`
  - `outputs/phase04_core_metrics/M11_duplicate_share.csv`

## 8. Q&A / data troubleshooting

| Question                                       | Answer                                                                                                                                                                         |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| How do I regenerate every metric table?        | Run the command block above or simply `make core-metrics`. Logs + CSVs will refresh under `outputs/phase04_core_metrics/`.                                                     |
| Can I tweak thresholds without editing Python? | Yes – pass CLI flags (e.g., `--author-min-ratings 10000`, `--books-top-n 50`, `--language-min-books 25`). The docstrings explain each parameter.                               |
| Where do I find the definitions again?         | `outputs/phase04_metrics_catalog.md` plus `docs/phase-04-step-02-task-01-notes.md` describe each metric. The new FAQ/Glossary entries summarize the CLI usage and terminology. |

## 9. Checklist review (from the plan)

- [x] Metrics module created (`src/metrics/core_metrics.py`).
- [x] Functions implemented for each core metric.
- [x] Summary tables generated and inspected.
- [x] Summary tables saved under `outputs/phase04_core_metrics/`.
- [x] Functions documented via module + CLI docstrings and these notes.

## 10. Appendices (log excerpt)

```
2025-12-05 04:59:34,655 INFO __main__ - Loaded 11,127 rows and 27 columns
2025-12-05 04:59:35,280 INFO __main__ - Wrote 15 rows to outputs/phase04_core_metrics/M1_top_authors_by_weighted_rating.csv
2025-12-05 04:59:35,376 INFO __main__ - Wrote 1 rows to outputs/phase04_core_metrics/M11_duplicate_share.csv
2025-12-05 04:59:35,377 INFO __main__ - Generated 8 metric tables
```

Container logs show UTC; the local calendar date for this execution was 2025-12-04.
