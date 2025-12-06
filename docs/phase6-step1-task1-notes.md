# Phase 06 · Step 01 · Task 01 – Analysis Script Inventory

This note follows the standard template so reviewers can trace exactly how the Phase 06 documentation/storytelling inventory was produced.

## 1. Task definition and goal

Inventory every analysis-oriented Python script (EDA, metrics, SQL parity, experiments) so we know what evidence already exists and which files need reorganization in later tasks. The deliverable is a portfolio-ready table that lists location, purpose, and status for each script, plus a call-out of legacy assets that may be archived.

## 2. How to run this analysis script

Use PowerShell only; Docker is not required for this bookkeeping task.

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
# 1) Enumerate every Python file and keep a copy for auditing
Get-ChildItem -Recurse -Include *.py -File |
  Sort-Object FullName |
  Tee-Object -FilePath tmp\phase06_step01_task01_pyfiles.txt |
  Select-Object -ExpandProperty FullName
# 2) Double-check the analysis folder so no CLI is missed
Get-ChildItem .\src\analyses | Sort-Object Name
```

The first command satisfies the "search the repository for all \*.py files" requirement and produces a reproducible manifest under `tmp/phase06_step01_task01_pyfiles.txt`. The second command confirms the contents of `src/analyses/` (where most CLIs live) so we can classify each script with confidence.

## 3. Environment recap

- OS: Windows 11 · PowerShell 5.1 (default shell for this repo).
- No virtualenv or Docker containers are required; the commands above read the working tree only.
- Repository state: `main` branch, clean prior to this task.

## 4. Findings / results

- The recursive search returned **24** Python files in total.
- **13** of those files are analysis-focused CLIs or helpers; the remainder are loaders, pipelines, or tests.
- Appendix A contains the requested table with script name, directory, category, purpose, and status/action column for each analysis file.
- Two scripts surfaced as legacy/duplicate work (`tmp/column_summary.py`, `src/check_data_quality.py`). They are now flagged for archival in later tasks so the official portfolio references the modern CLIs only.

## 5. Expected output checkpoints

- `tmp/phase06_step01_task01_pyfiles.txt` lists all `.py` paths (24 lines today). The log excerpt in Appendix B shows the same order that appeared in the terminal.
- Appendix A is present in this note and mirrors the table layout requested in the plan.
- The note references both PowerShell commands and cites the counts above, making it easy for reviewers to re-run and confirm.

## 6. Observations / insights

- All modern analysis CLIs already live under `src/analyses/`, which will make future renaming/promotion straightforward.
- Legacy scripts live outside that folder (`tmp/` and root `src/`). Keeping them isolated prevents accidental execution but we should either delete them or move them into an `archive/` namespace in Step 01 Task 03.
- The SQL storytelling stack is well-covered: validation (three CLIs), comparison, plotting, and PowerPoint export each have their own module, which gives us a strong narrative for recruiters.

## 7. Artifacts refreshed each run

- `tmp/phase06_step01_task01_pyfiles.txt` – manifest of every Python file (generated via Command #1).
- `docs/phase6-step1-task1-notes.md` – this task note.
- `docs/phase-06-glossary.md` – glossary created alongside this task (see separate section once updated).
- `docs/data-faq.md` – FAQ entry referencing the new inventory (updated after this note).

## 8. Q&A / data troubleshooting

**Q: How do I quickly re-check the script inventory after new commits?**  
Run the command block in Section 2; the manifest file in `tmp/` will update instantly and can be diffed in Git.

**Q: Which scripts should I point recruiters to for SQL storytelling?**  
Use the portfolio spine and storytelling helpers: `src/analyses/portfolio/p04_sql_vs_pandas_compare.py`, `src/analyses/support/storytelling/plot_comparison_summary.py`, and `src/analyses/support/storytelling/export_phase05_slide.py`. They already tie into the README's "SQL Portfolio Spotlight" section.

**Q: Which files look deprecated and safe to archive?**  
`tmp/column_summary.py` (ad-hoc JSON column dump) and `src/check_data_quality.py` (pre-pipeline data-quality script) duplicate the EDA/QA CLIs. Flag them for removal or archival when reorganizing notebooks.

**Q: Where do the helper functions for pandas metrics live?**  
`src/metrics/core_metrics.py` holds the reusable functions while `src/analyses/portfolio/p03_core_metrics_suite.py` handles CLI parsing/writes. Keep both when reshaping documentation so the separation of concerns remains obvious.

## 9. Checklist review

- [x] Searched the repository for all `*.py` files.
- [x] Classified each analysis script by main purpose.
- [x] Recorded a table with file name, folder, type/purpose.
- [x] Flagged legacy/duplicate scripts for follow-up.

## 10. Appendix A – Analysis script inventory

| Script                                            | Directory                            | Category                  | Primary purpose                                                                               | Status / Action                                                |
| ------------------------------------------------- | ------------------------------------ | ------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `p01_initial_inspection_books.py`                 | `src/analyses/portfolio`             | Phase 02 – Initial EDA    | Generates sample preview + numeric summary CSVs for basic sanity checks.                      | Active reference for onboarding/portfolio evidence.            |
| `p02_deep_dive_eda.py`                            | `src/analyses/portfolio`             | Phase 03 – Deep-dive EDA  | Refreshes univariate, temporal, categorical, and outlier artifacts under `outputs/phase03_*`. | Active; keep as canonical EDA CLI.                             |
| `p03_core_metrics_suite.py`                       | `src/analyses/portfolio`             | Phase 04 – Core KPIs      | Runs the Phase 04 metric suite and writes `outputs/phase04_core_metrics/*.csv`.               | Active; pairs with metrics catalog + README.                   |
| `p04_sql_vs_pandas_compare.py`                    | `src/analyses/portfolio`             | Phase 05 – SQL parity     | Executes SQL queries, compares against pandas CSVs, and emits comparison summary files.       | Active; cornerstone for Phase 05 storytelling.                 |
| `metrics/core_metrics.py`                         | `src/metrics`                        | Phase 04 – Metric helpers | Holds reusable pandas functions (weighted authors, median buckets, etc.) consumed by the CLI. | Active helper; keep documented for reviewers.                  |
| `support/documentation/metrics_catalog.py`        | `src/analyses/support/documentation` | Phase 04 – Documentation  | Builds the Markdown metrics catalog explaining each KPI.                                      | Active portfolio artifact.                                     |
| `support/validation/postgres_validate_books.py`   | `src/analyses/support/validation`    | Phase 05 – SQL validation | Captures schema snapshot + sample preview from Postgres.                                      | Active; feeds validation notes.                                |
| `support/validation/postgres_profile_columns.py`  | `src/analyses/support/validation`    | Phase 05 – SQL validation | Produces null/distinct/category distributions straight from Postgres.                         | Active; keep for QA evidence.                                  |
| `support/validation/postgres_compare_stats.py`    | `src/analyses/support/validation`    | Phase 05 – SQL validation | Confirms row count + aggregate parity between CSV and Postgres.                               | Active; run whenever data reloads.                             |
| `support/storytelling/plot_comparison_summary.py` | `src/analyses/support/storytelling`  | Phase 05 – Visualization  | Converts comparison CSV results into `comparison_summary.png`.                                | Active; supports README visuals.                               |
| `support/storytelling/export_phase05_slide.py`    | `src/analyses/support/storytelling`  | Phase 05 – Storytelling   | Builds `docs/phase-05-step-03-task-01-slide.pptx` for portfolio presentations.                | Active; keep tied to PowerShell wrapper.                       |
| `archive/check_data_quality_legacy.py`            | `src/analyses/archive`               | Legacy QA                 | Older null/duplicate checker predating the Phase 03 CLI.                                      | Archived – keep for context only.                              |
| `archive/column_summary_experiment.py`            | `src/analyses/archive`               | Experiment                | Ad-hoc column summary JSON helper from early exploration.                                     | Archived – safe to delete after mirror screenshot, if desired. |

## Appendix B – Command output snippet

```
Get-ChildItem -Recurse -Include *.py -File | Sort-Object FullName | Select-Object -ExpandProperty FullName
C:\Users\shady\Documents\GITHUB\goodreads-books-analytics\src\analyses\portfolio\p01_initial_inspection_books.py
...
C:\Users\shady\Documents\GITHUB\goodreads-books-analytics\src\analyses\archive\column_summary_experiment.py
```

(The full manifest is stored in `tmp/phase06_step01_task01_pyfiles.txt`.)
