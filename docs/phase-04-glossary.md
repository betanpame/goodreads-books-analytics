# Phase 04 – Business Analysis & Cleaning Glossary

Beginner-friendly definitions for the concepts introduced while operationalizing the cleaning pipeline. Use this alongside `docs/data-faq.md`, which captures step-by-step fixes and reusable commands.

## Cleaning & Canonicalization

- **Cleaning CLI (`src.pipelines.run_cleaning`)** – The Docker-first command-line tool that loads `data/books.csv`, applies every rule in `clean_books`, validates the output, and writes `data/derived/books_clean.csv`. It is the only supported entrypoint for refreshing the curated dataset.
- **Duplicate → Canonical mapping** – The lookup table stored at `data/derived/duplicate_bookid_mapping.csv`. Each row points a duplicate `bookID` (audiobook, translation, omnibus) to the canonical `bookID` chosen in Phase 03. The CLI left-joins this file so analytics can group by `canonical_book_id` without deleting source rows.
- **`canonical_book_id`** – The deduplicated identifier produced by the mapping step. If a book never appeared in the mapping file, `canonical_book_id == book_id`. Dashboards should always use this column to avoid double counting.
- **`is_duplicate` flag** – Boolean indicator emitted after the mapping join. `True` means the row came from the duplicate list and should only contribute to story-level stats after grouping.
- **Flag columns** – Companion text columns (`average_rating_flag`, `publication_year_flag`, `page_length_bucket`, `media_type_hint`) that capture why a record needed special handling. They provide ready-made slice dimensions for analysts and BI tools.

## Engagement Caps & Buckets

- **Winsorized engagement counts** – `ratings_count_capped` and `text_reviews_count_capped` clamp extreme popularity at 597,244 and 14,812 respectively. Use the capped columns for charts that would otherwise be dominated by runaway bestsellers.
- **Page-length buckets** – Labels applied after casting `num_pages`: `short_reference` (<10 pages), `zero_or_audio` (0 or missing pages, often audio editions), and `multi_volume` (>2,000 pages). Everything else remains `<NA>` so plots can focus on outliers when needed.
- **Media type hint** – Derived from the page-length logic to flag likely audiobooks or multimedia bundles (`audio_or_misc`). This helps stakeholders understand why some rows lack page counts.

## Metrics & Insight Concepts

- **Weighted average rating (author-level)** – A mean rating per author that multiplies each title by its `ratings_count`. A minimum threshold (5,000 ratings) keeps tiny releases from jumping ahead of established writers.
- **Author engagement index** – Combined z-score of `ratings_count_capped` and `text_reviews_count_capped` per author. Useful for spotting fandoms that leave reviews, not just stars.
- **Page-length engagement delta** – Median of the capped engagement metrics per `page_length_bucket`, highlighting whether long reads truly garner more attention.
- **Publication momentum** – Pair of time-series metrics (`average_rating` and median `ratings_count_capped` per `publication_year`) that reveal how quality and demand move through time.
- **Language/publisher reach** – Aggregations constrained by minimum canonical titles (≥50 for languages, ≥25 for publishers) so cohorts remain statistically meaningful.
- **Duplicate share & uplift** – Percentage of rows where `is_duplicate == True` plus the engagement comparison between canonical parents and duplicate children. This proves why canonical IDs must power dashboards.

## Validation & Reproducibility

- **Validation suite** – Lightweight functions inside `run_cleaning.py` that assert: (1) ratings stay within [0, 5]; (2) page caps hold; (3) engagement caps hold; (4) `canonical_book_id` has no nulls. Treat a failing validation as a release blocker.
- **`--no-deps` flag** – Docker Compose option used during CLI runs to skip the PostgreSQL container when only file IO is required. This avoids port 5432 conflicts while keeping the workflow entirely inside Docker.
- **Dry-run limit (`--limit`)** – Optional CLI argument that processes only the first _n_ rows. Handy for fast debugging without touching the full CSV.
- **Core metrics CLI** – `python -m src.analyses.portfolio.p03_core_metrics_suite` (or `make core-metrics`) loads `books_clean.csv`, executes the M1/M3/M4/M5/M7/M8/M9/M11 functions, and writes CSVs into `outputs/phase04_core_metrics/` so reviewers have concrete artifacts.

## Visualization & Portfolio Terms

- **Visualization plan** – The structured mapping of business questions to chart types, datasets, and axes. Guides the creation of reproducible, portfolio-ready figures.
- **Figure** – A saved image file (PNG/SVG) representing a chart or plot generated from the analysis scripts. Figures are stored in `outputs/phase04_visualizations/` or `figures/`.
- **Caption** – A short description under each chart explaining its meaning, business relevance, and how to interpret the data. Captions are included in the notes and documentation for clarity.
- **Portfolio-ready** – Charts and notes formatted for clarity, reproducibility, and professional presentation. All steps, commands, and outputs are documented so beginners can follow and reproduce the work.

## Documentation Cross-links

- **Task notes** – `docs/phase-04-step-01-task-01-notes.md` documents every CLI execution (commands, metrics, evidence) following the Phase 02 template so recruiters can trace the work.
- **FAQ bridge** – Whenever you need a “how-to” answer (rerunning the CLI, troubleshooting the mapping, interpreting flags), jump to `docs/data-faq.md` → _Phase 04 cleaning pipeline_. This glossary intentionally stays definition-first so the FAQ can focus on procedures.
- **Make targets** – `make metrics-catalog` and `make core-metrics` wrap the Docker commands so reproducing artifacts during reviews only takes one shell instruction.

Keep this glossary updated as Phase 04 introduces new KPIs, visualization assets, or storytelling features. Linking definitions here keeps the main task notes concise while ensuring beginners have a clear reference.
