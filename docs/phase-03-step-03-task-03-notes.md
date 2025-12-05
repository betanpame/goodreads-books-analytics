# Phase 03 · Step 03 · Task 03 — Cleaning Rules Blueprint (Run: 2025-12-05)

## 1. Task definition and goal

- Convert the anomalies from Tasks 01–02 (missing data, duplicates, outliers) into a documented cleaning rulebook.
- Package every rule with enough context (issue, columns, decision, rationale, priority) so future maintainers can implement them without re-running EDA.
- Keep the documentation portfolio-ready: professional tone, but beginner-friendly explanations and exact reproduction steps.

## 2. How to run this analysis script

Same CLI one-liner continues to regenerate every artifact supporting the rules:

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose
```

Optional local run:

```powershell
C:/Users/shady/Documents/GITHUB/goodreads-books-analytics/.venv/Scripts/python.exe -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose
```

## 3. Environment recap

- **Data**: `data/books.csv` (Phase 02 export) + derived CSVs in `outputs/phase03_univariate/` and `data/derived/`.
- **Containers**: `app` (Python) and `postgres` from the combined compose file; no notebooks were used.
- **New artifacts**: `docs/data-cleaning-rules.md` consolidates every rule; `src/analyses/eda_books.py` now logs where to find it.

## 4. Findings / results — Cleaning rule highlights

| Theme                    | Issue & Evidence                                                                                          | Rule summary                                                                                                                                   | Priority                                            |
| ------------------------ | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Missing / derived fields | Two rows lost `publication_year` after parsing (see `missing_values_summary.csv`).                        | Re-parse with expanded formats; if still null, label `publication_year="Unknown"` but keep the row.                                            | Must-do now                                         |
| Duplicates               | 31 partial duplicates documented in `partial_duplicates_by_subset.csv`.                                   | Join every analysis to `data/derived/duplicate_bookid_mapping.csv` and aggregate on `canonical_book_id`.                                       | Must-do now                                         |
| Page counts              | 76 rows show `num_pages=0`; 195 rows <10 pages; 12 omnibuses exceed 2,000 pages (see `num_pages_*` CSVs). | Convert zeros to `NaN` + tag as `audio_or_misc`; bucket `<10` as `short_reference`; cap >2,000 at 2,000 for visuals and tag as `multi_volume`. | Must-do now (zeros & >2,000), nice-to-have (`<10`). |
| Ratings                  | 250 rows outside the IQR bounds, often placeholder `average_rating=0`.                                    | Treat zero ratings as missing; keep legitimate 5.0s but flag for review.                                                                       | Must-do now                                         |
| Engagement metrics       | 1,729 and 1,631 rows exceed the IQR upper bounds for `ratings_count` / `text_reviews_count`.              | Winsorize at p99.5 (597,244 and 14,812) before plotting or aggregating; store both raw and capped columns.                                     | Must-do now                                         |
| Categorical hygiene      | Regex checks for `language_code` and publication-year bounds currently pass.                              | Keep automated checks in CI; normalize or drop should violations appear in future exports.                                                     | Nice-to-have                                        |

Full details (issue descriptions, rationale, and evidence links) live in `docs/data-cleaning-rules.md`.

## 5. Expected output checkpoints

- CLI log now ends with `Documented cleaning decisions live in docs/data-cleaning-rules.md — review before Phase 04 implementations.`
- `docs/data-cleaning-rules.md` exists and lists nine rules with columns, decisions, rationale, and priorities.
- Existing Task 01/02 CSVs provide the proof for every rule (no new CSVs were generated for Task 03 by design).

## 6. Observations / insights

- Tagging problematic records (zeros, ultralong omnibuses) is more flexible than deleting them; this preserves lineage and lets analysts choose filters later.
- Explicit priority labels (“Must-do now” vs “Nice-to-have”) keep the cleaning backlog manageable once Phase 04 automation begins.
- Surfacing the rulebook path directly in the CLI means every teammate who runs the script immediately discovers the documentation without digging through `/docs`.

## 7. Artifacts refreshed each run

- `docs/data-cleaning-rules.md`
- `outputs/phase03_univariate/` (unchanged structure, but rerun confirms traceability)

## 8. Q&A / data troubleshooting

- **Where are the actual rules?** – `docs/data-cleaning-rules.md`, linked in the CLI log and this note.
- **How do I prove the rules are grounded in data?** – Each rule cites a CSV (e.g., `num_pages_below_valid_min.csv`) generated by Task 02. Keep those side-by-side when presenting to stakeholders.
- **What if a new anomaly appears later?** – Re-run the CLI, inspect `outlier_rule_violations.csv`, append a rule section to the markdown, and mention it here plus in `docs/data-faq.md`.

## 9. Checklist review

- [x] Created `docs/data-cleaning-rules.md`.
- [x] Documented rules for missing values, duplicates, and outliers.
- [x] Explained the rationale for each rule with evidence links.
- [x] Updated the EDA CLI to point readers to the rulebook.

## 10. Appendices

### 10.1 Key commands (2025-12-05)

```powershell
# Refresh artifacts and see the new log pointer
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.eda_books --output-dir outputs/phase03_univariate --verbose

# Inspect the cleaning rulebook in PowerShell
Get-Content docs\data-cleaning-rules.md | more
```

### 10.2 Next-step reminders

1. Phase 04 cleaning scripts will implement the “Must-do now” rules first (winsorize counts, canonical joins, page-length tagging).
2. Keep `docs/data-cleaning-rules.md` under version control; reference it in the Phase 03 status report so reviewers know the data is ready for production hardening.
