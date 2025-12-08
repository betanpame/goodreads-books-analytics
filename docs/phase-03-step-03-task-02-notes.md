# Phase 03 · Step 03 · Task 02 — Outliers & Inconsistencies Review (Run: 2025-12-05)

## 1. Task definition and goal

- Follow the plan checklist for Phase 03 → Step 03 → Task 02 to surface numeric outliers, implausible publication dates, and broken categorical labels.
- Use visuals (boxplots + histograms) plus simple rule checks to flag any values that would skew summary stats before we formalize cleaning rules.
- Capture concrete row samples so the next task (cleaning rules) has evidence, not just thresholds.

## 2. How to run this analysis script

Run the CLI from the repo root to regenerate the outlier evidence.

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose
```

Optional local venv call:

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose
```

### Estimated runtime & success checks

- **Runtime:** ≈5 minutes in Docker (plots + CSV samples); ≈4 minutes via the local venv.
- **Success checklist:**
  - CLI log emits `Saved numeric outlier summary ...`, multiple `Saved ... histogram/boxplot` lines, and `outlier_rule_violations.csv` summary.
  - Folder `outputs/phase03_univariate/step03_task02_outliers/` exists with rule-specific CSVs and the `plots/` subfolder containing eight PNGs.
  - When `--verbose` is active, the console lists row counts per rule (e.g., `num_pages suspect_low -> 195 rows`).

Optional local venv call:

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose
```

## 3. Environment recap

- Dataset: `data/books.csv` (Phase 02 export). The CLI still derives `publication_year` on the fly.
- Containers: `app` for Python, `postgres` for SQL checks, both launched via the combined compose file.
- Outputs: `outputs/phase03_univariate/step03_task02_outliers/` holds CSV samples, rule summaries, and plots. Plots live under the nested `plots/` folder.
- Dependencies: `matplotlib`, `seaborn`, `pandas`, plus the new helper functions inside `src/analyses/eda_books.py` for IQR bounds, rule logging, and regex checks.

## 4. Findings / results

### 4.1 Numeric outlier scan (IQR rule + business thresholds)

| Column               | IQR lower | IQR upper | Hard bounds    | Soft bounds                                 | Outlier rows                                                                      |
| -------------------- | --------- | --------- | -------------- | ------------------------------------------- | --------------------------------------------------------------------------------- |
| `average_rating`     | 3.22      | 4.68      | 0–5 enforced   | —                                           | 250 rows (mixture of 0.0 placeholders and cult-classic 5.0s)                      |
| `num_pages`          | -144      | 752       | minimum 1 page | `<10` = suspect low, `>2000` = suspect high | 540 IQR hits, 76 hard violations (`0` pages), 195 soft-low, 12 soft-high          |
| `ratings_count`      | -7,230    | 12,327    | ≥0 enforced    | —                                           | 1,729 rows above IQR upper bound (mega franchises such as _Harry Potter_, _Dune_) |
| `text_reviews_count` | -334      | 580       | ≥0 enforced    | —                                           | 1,631 rows above IQR upper bound                                                  |

Artifacts:

- `numeric_outlier_summary.csv` – percentile, IQR, and threshold table.
- Plot bundle (boxplot + histogram per column) saved under `step03_task02_outliers/plots/`.
- Sample CSVs for each rule (e.g., `num_pages_suspect_high.csv`).

### 4.2 Concrete anomalies to highlight in Task 03

- **Zero-page audiobooks (76 rows):** Titles such as `"The 5 Love Languages"` audiobook bundle and multiple Sherlock Holmes radio plays report `num_pages = 0`, proving that the source mixes print and audio metadata. Evidence in `num_pages_below_valid_min.csv`.
- **Giant omnibuses (12 rows):** Boxed sets like `"The Complete Aubrey/Maturin Novels"` (6,576 pages) and medical references like `"Harrison's Principles of Internal Medicine"` exceed the 2,000-page soft cap. These rows belong in a "multi-volume" bucket so they do not distort page-length averages.
- **Ratings pile-ups (1,729 rows):** Franchise pillars (_Harry Potter_, _Lord of the Rings_, _Hatchet_) exceed 12k ratings. They confirm the need for the previously defined caps (597,244 for `ratings_count`, 14,812 for `text_reviews_count`) before plotting log scales.
- **Rating extremes (250 rows):** Items with `average_rating = 0` are mostly placeholder guides or metadata-only entries (`"Out to Eat London"`, `"Boogaloo on 2nd Avenue"`). On the high end, curated anthologies and teacher guides show perfect 5.0s. Both cases need special treatment (drop, label, or winsorize) prior to KPI calculations.

### 4.3 Publication year & language integrity

- No publication years fell outside the 1800 lower bound or the "current year + 2" future buffer, so no CSVs were generated for those rules.
- Language codes already follow the `[A-Za-z-]+` pattern and stay under eight characters. The `language_code` regex checks logged zero violations.

### 4.4 Evidence snapshots

- `num_pages_suspect_low.csv` → 195 rows, mostly audiobook box sets and study guides with `<10` reported pages.
- `num_pages_suspect_high.csv` → 12 rows, dominated by multi-volume omnibuses (Rowling, Montgomery, Proust, Tolkien, Churchill, medical textbooks).
- `average_rating_iqr_outlier.csv` → 250 rows calling out both the 0.0 placeholders and hyper-positive references (`"Literature Circle Guide: Bridge to Terabithia"`, etc.).
- `ratings_count_iqr_outlier.csv` → Top of file shows the million-plus Harry Potter titles; useful for verifying our caps.

## 5. Expected output checkpoints

- CLI logs mention `Saved numeric outlier summary to ... step03_task02_outliers/numeric_outlier_summary.csv` followed by per-plot INFO lines.
- `outlier_rule_violations.csv` lists seven rows (one per rule) with the exact row counts cited above.
- New folder `outputs/phase03_univariate/step03_task02_outliers/plots/` contains eight PNG files.
- No publication-year or language-code CSVs should exist for this run (absence confirms the checks passed).

## 6. Observations / insights

- Business rules matter more than pure IQR for `num_pages`; otherwise all omnibuses would look fine because the dataset is so wide. Splitting "soft" vs "hard" bounds gives us remediation options instead of blanket deletion.
- Audiobook/guide entries that inherited the `num_pages` column explain many zero-page findings. We should tag those rows (via `format` or `media_type`) before Phase 04 metrics rely on length.
- Ratings and review counts are extremely long-tailed. Keeping the clip thresholds from Task 01 ensures upcoming plots (Step 04 and beyond) do not become unreadable.
- Regex-based categorical checks are cheap to keep running in CI; even though this dataset is clean today, they protect us once we ingest future Goodreads exports with new locales.

## 7. Artifacts refreshed each run

- `outputs/phase03_univariate/step03_task02_outliers/numeric_outlier_summary.csv`
- `outputs/phase03_univariate/step03_task02_outliers/outlier_rule_violations.csv`
- Rule-specific sample CSVs: `average_rating_iqr_outlier.csv`, `num_pages_*`, `ratings_count_iqr_outlier.csv`, `text_reviews_count_iqr_outlier.csv`
- Plot PNGs for each numeric column (boxplot + histogram) under `.../plots/`

## 8. Q&A / data troubleshooting

- **Where do I grab the raw samples for documentation?** Every rule writes a CSV into `step03_task02_outliers/` with the same name listed in `outlier_rule_violations.csv`. Use those instead of re-filtering in notebooks.
- **How do I change the thresholds?** Edit the `OUTLIER_INSPECTION_PLAN` inside `src/analyses/eda_books.py`. The CLI rereads that plan on every run, so bumps to `suspect_high` or new columns automatically propagate.
- **Why are there no publication-year CSVs?** The helper only writes files when the boolean mask is non-empty. Seeing no `publication_year_year_too_old.csv` means the data cleared both the 1800 and future-year rules, so nothing is wrong.
- **Can I reuse the plots in presentations?** Yes; the PNGs are sized for 1,200×675 slides and live under `step03_task02_outliers/plots/`. Cite them directly in Phase 04 storytelling to prove you inspected the tails.

## 9. Checklist review

- [x] Created numeric visualizations (boxplots, histograms) for key columns.
- [x] Identified concrete outlier samples with CSV evidence.
- [x] Evaluated publication_year + language_code for impossible values.
- [x] Logged everything in markdown with commands and artifact pointers.

## 10. Appendices

### 10.1 Key commands (2025-12-05)

```powershell
# Run the full EDA stack with verbose logs
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose

# Optional: copy plots off the container volume
robocopy outputs\phase03_univariate\step03_task02_outliers ..\evidence\task02_outliers /E
```

### 10.2 Next-step reminders

- Feed the CSV evidence into Phase 03 → Step 03 → Task 03 to design actual cleaning rules (winsorize, drop, or tag).
- Update `docs/data-faq.md` + `docs/phase-03-glossary.md` whenever these thresholds change so downstream teams stay aligned.
