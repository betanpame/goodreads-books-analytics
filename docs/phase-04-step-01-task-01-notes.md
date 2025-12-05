# Phase 04 · Step 01 · Task 01 – Implement Core Cleaning Pipeline

## 1. Task definition and goal

Paraphrasing the plan: convert the Phase 03 cleaning rulebook into executable Python so any analyst can run `clean_books(df)` on the raw Goodreads export, apply duplicate mapping, cap extreme engagement values, and emit a reproducible CSV for downstream metrics. This task lives entirely inside the Dockerized Python workflow—no notebooks or ad-hoc scripts.

## 2. How to run this analysis script

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose --env-file .env.example -f docker-compose.python.yml run --no-deps --rm `
  app python -m src.pipelines.run_cleaning `
  --books-csv data/books.csv `
  --mapping-csv data/derived/duplicate_bookid_mapping.csv `
  --output-csv data/derived/books_clean.csv
```

- Keep execution inside Docker so the same Python 3.14 + requirements stack runs everywhere.
- `--no-deps` skips PostgreSQL when you only need the CSV; drop the flag if you also plan to load the database.
- Optional flags: `--limit 1000` for dry runs, `--skip-mapping` if you need to debug the raw IDs.

## 3. Environment recap

- **Runtime:** `python:3.14-slim` container defined in `docker/python/Dockerfile` (pip installs from `requirements.txt`).
- **Entrypoint:** `src/pipelines/run_cleaning.py`, which wraps `clean_books` plus validation helpers.
- **Inputs:** `data/books.csv` (raw Kaggle export) and `data/derived/duplicate_bookid_mapping.csv` (Phase 03 canonical IDs).
- **Outputs:** `data/derived/books_clean.csv` refreshed in-place; no Jupyter artifacts are produced.

## 4. Findings / results

| Metric                                      | Value                                                        |
| ------------------------------------------- | ------------------------------------------------------------ |
| Run date (local)                            | 2025-12-04                                                   |
| Raw rows loaded                             | 11,127                                                       |
| Repaired author rows                        | 4                                                            |
| Cleaned rows written                        | 11,127                                                       |
| Duplicate pairs loaded                      | 16                                                           |
| `is_duplicate=True` rows                    | 16 (exactly the provided mapping)                            |
| `average_rating_flag == "placeholder_zero"` | 26 rows (0 converted to null)                                |
| `page_length_bucket`                        | `short_reference=119`, `zero_or_audio=76`, `multi_volume=12` |
| `media_type_hint == audio_or_misc`          | 76                                                           |
| `ratings_count` min/max                     | 0 / 4,597,666 (capped view available)                        |
| `text_reviews_count` min/max                | 0 / 94,265 (capped view available)                           |

Validations embedded in the CLI all passed:

1. `average_rating` stays within `[0, 5]` after zero sanitization.
2. `num_pages_capped` ≤ 2,000 for every title.
3. `ratings_count_capped` ≤ 597,244 and `text_reviews_count_capped` ≤ 14,812.
4. `canonical_book_id` populated for all 11,127 rows.

## 5. Expected output checkpoints

- `[INFO] Loaded 11,127 rows (4 repaired author rows)` ensures `raw_ingestion.load_books_csv` repaired embedded commas.
- `[INFO] Loaded 16 duplicate pairs` confirms the mapping CSV is read and validated.
- `[INFO] Cleaned rows: 11,127` proves no records were dropped unexpectedly.
- `[INFO] Value counts for is_duplicate` should show `True 16 / False 11111` as long as the mapping file is unchanged.
- Final log line: `[INFO] Wrote cleaned dataset to data/derived/books_clean.csv`.

## 6. Observations / insights

- Port conflicts can pop up if PostgreSQL is already bound to 5432 locally. Running the CLI with `--no-deps` keeps this task lightweight and still reproducible.
- The new `apply_canonical_mapping` logic now renames intermediate columns (`canonical_target_id`) so pandas merges never collide, making the dedupe step easier to audit.
- Flag columns (`average_rating_flag`, `page_length_bucket`, `media_type_hint`) give analysts immediate slice points for dashboards without revisiting the raw rules doc.

## 7. Artifacts refreshed each run

- `data/derived/books_clean.csv` – canonical, capped, beginner-friendly dataset for Phase 04 metrics.
- Terminal log (capture via VS Code output or `tee`) – evidence of row counts, flag distributions, and validation success.
- Source updates (if any) – during this run we tightened `apply_canonical_mapping` and the CLI validator; those changes are already merged into `src/cleaning.py` and `src/pipelines/run_cleaning.py`.

## 8. Q&A / data troubleshooting

| Question                                           | Short answer                                                                                                                          |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| How do I rerun the CLI without Postgres conflicts? | Use the exact command above with `--no-deps`; see `docs/data-faq.md` → **Phase 04 cleaning pipeline** for context.                    |
| What proves the duplicate mapping worked?          | Check `is_duplicate` counts in the log and review `canonical_book_id` in the CSV; troubleshooting steps live in the same FAQ section. |
| Where can I find the cap thresholds again?         | `docs/data-cleaning-rules.md` plus the glossary/FAQ additions below summarize the numeric caps so you never guess.                    |

## 9. Checklist review (from the plan)

- [x] Raw dataset loaded into `df_raw`.
- [x] `clean_books(df)` applied through the CLI.
- [x] Types converted and dates parsed via helper functions.
- [x] Missing values handled (zero ratings to null, suspect pages flagged).
- [x] Duplicates resolved using canonical IDs.
- [x] Validation checks embedded (`assert`-style helpers).
- [x] Documentation updated using this template.

## 10. Appendices

```
2025-12-05 04:00:48,130 INFO __main__ - Validation engagement_caps passed
2025-12-05 04:00:48,131 INFO __main__ - Validation canonical_id_present passed
2025-12-05 04:00:48,293 INFO __main__ - Wrote cleaned dataset to data/derived/books_clean.csv
```

Time stamps are UTC because the container runs on UTC; local date for this run was 2025-12-04.
