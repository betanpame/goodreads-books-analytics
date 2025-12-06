# Phase 06 · Step 01 · Task 02 – Analysis Script Structure Proposal

This note documents the folder/naming scheme we will apply in Task 03 so reviewers understand the rationale before any files move.

## 1. Task definition and goal

Define a beginner-friendly yet professional structure for all analysis scripts. The deliverable is a prescriptive plan that tells future readers which scripts to run (and in what order), where supportive utilities live, and how legacy experiments will be archived.

## 2. How to run this analysis script

No Python/Docker execution is necessary; we only enumerate files with PowerShell to capture the current state before reorganizing.

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
Get-ChildItem .\src\analyses | Sort-Object Name
```

Command purpose: produce the authoritative list of existing CLIs so the renaming plan references exact filenames. Keep the console output (excerpt in Appendix B) for the Task 03 change log.

## 3. Environment recap

- OS / shell: Windows 11 · PowerShell 5.1.
- Repo state: `main` branch after completing Phase 06 · Step 01 · Task 01 inventory.
- No containers or virtual environments were activated; this task is purely organizational planning.

## 4. Findings / results

1. `src/analyses/` already contains every actively used CLI, but filenames lack the numeric ordering and grouping we want for a portfolio walkthrough.
2. Supporting SQL utilities (`postgres_*`, `plot_*`, `export_*`) should be grouped so recruiters can differentiate “core scripts to run” from helper modules.
3. Legacy helpers (`src/check_data_quality.py`, `tmp/column_summary.py`) live outside `src/analyses/`, making it easy to forget they need archival.
4. We now have a concrete proposal (Section 10) that:
   - Introduces a `portfolio/` subfolder with four numbered scripts.
   - Establishes a `support/` subfolder split into `validation/`, `storytelling/`, and `documentation/` buckets.
   - Creates an `archive/` subfolder to park deprecated experiments inside the same namespace.

## 5. Expected output checkpoints

- This note (`docs/phase6-step1-task2-notes.md`) contains the full plan, ready to execute in Task 03.
- Appendix A table lists **current → future** locations/names for every analysis script so pulling requests can reference a single mapping.
- Appendix B stores the PowerShell listing, proving the baseline before we refactor.

## 6. Observations / insights

- Numbering the “portfolio spine” scripts (01–04) mirrors the storytelling order already documented in README (EDA → core metrics → SQL parity).
- By keeping helper modules inside `support/`, we reduce onboarding friction: a new user can run `portfolio/*.py` sequentially and then drill into support modules if they need validation details.
- Moving legacy experiments into `src/analyses/archive/` (instead of leaving them in `tmp/`) keeps the repo tidy and prevents CI hooks from touching stray folders.

## 7. Artifacts refreshed each run

- `docs/phase6-step1-task2-notes.md` – this plan.
- `docs/data-faq.md` – new entries describing the portfolio spine and how to regenerate the PowerShell listing.
- `docs/phase-06-glossary.md` – updated with terms introduced in this structure plan.

## 8. Q&A / data troubleshooting

**Q: Which scripts make up the “portfolio spine”?**  
A: Four numbered files under `src/analyses/portfolio/`: `01_initial_inspection_books.py`, `02_deep_dive_eda.py`, `03_core_metrics_suite.py`, `04_sql_vs_pandas_compare.py`. Run them in order to recreate the narrative.

**Q: Where do I find helper scripts for SQL validation and storytelling?**  
A: `src/analyses/support/validation/` (three `postgres_*` files) and `src/analyses/support/storytelling/` (`plot_comparison_summary.py`, `export_phase05_slide.py`).

**Q: What happens to experimental scripts like `tmp/column_summary.py`?**  
A: They move into `src/analyses/archive/` with descriptive names (for example, `column_summary_experiment.py`) so future maintainers know they are not part of the primary pipeline.

**Q: Do we rename helper modules such as `metrics/core_metrics.py`?**  
A: No change. Helpers stay where they are; only runnable analysis scripts receive numeric prefixes to guide readers.

## 9. Checklist review

- [x] Selected the main analysis folder (`src/analyses/portfolio/`).
- [x] Defined the 4 flagship scripts and their numbering.
- [x] Categorized all remaining scripts into `support/` and `archive/` buckets.
- [x] Documented the outcome in this note plus the glossary/FAQ updates.

## 10. Appendix A – Current vs future structure

| Current path                               | Future path                                                    | Notes                                                                    |
| ------------------------------------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `src/analyses/initial_inspection_books.py` | `src/analyses/portfolio/01_initial_inspection_books.py`        | Adds numeric prefix, lives in portfolio spine as the quick-start script. |
| `src/analyses/eda_books.py`                | `src/analyses/portfolio/02_deep_dive_eda.py`                   | Renamed to highlight scope (Phase 03 deep-dive) and execution order.     |
| `src/analyses/run_core_metrics.py`         | `src/analyses/portfolio/03_core_metrics_suite.py`              | Keeps CLI logic but renames to match README terminology.                 |
| `src/analyses/sql_vs_pandas_compare.py`    | `src/analyses/portfolio/04_sql_vs_pandas_compare.py`           | Simply moves under `portfolio/` and gains the `04_` prefix.              |
| `src/analyses/metrics_catalog.py`          | `src/analyses/support/documentation/metrics_catalog.py`        | Documentation helper; stays runnable but outside the main walkthrough.   |
| `src/analyses/postgres_validate_books.py`  | `src/analyses/support/validation/postgres_validate_books.py`   | Validation bucket (no rename required).                                  |
| `src/analyses/postgres_profile_columns.py` | `src/analyses/support/validation/postgres_profile_columns.py`  | Same as above.                                                           |
| `src/analyses/postgres_compare_stats.py`   | `src/analyses/support/validation/postgres_compare_stats.py`    | Same as above.                                                           |
| `src/analyses/plot_comparison_summary.py`  | `src/analyses/support/storytelling/plot_comparison_summary.py` | Storytelling helper grouped with PPTX exporter.                          |
| `src/analyses/export_phase05_slide.py`     | `src/analyses/support/storytelling/export_phase05_slide.py`    | Same grouping as chart script.                                           |
| `src/check_data_quality.py`                | `src/analyses/archive/check_data_quality_legacy.py`            | Renamed + relocated to archive to signal deprecation.                    |
| `tmp/column_summary.py`                    | `src/analyses/archive/column_summary_experiment.py`            | Moves out of `tmp/` and receives a descriptive suffix.                   |

## Appendix B – PowerShell listing

```
Get-ChildItem .\src\analyses | Sort-Object Name
... (see console log dated 2025-12-06)
```

Use this baseline to verify that Task 03 applies the planned structure exactly.
