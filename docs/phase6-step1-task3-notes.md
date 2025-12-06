# Phase 06 · Step 01 · Task 03 – Clean & Annotate Main Scripts

## 1. Task definition and goal

Implement the structure plan from Task 02: reorganize analysis scripts into a portfolio spine, categorize helper modules, archive legacy experiments, and annotate the flagship CLIs with portfolio-ready descriptions. The result should be a `src/analyses/` tree that tells recruiters exactly where to start, plus updated docs explaining how to run each entry point.

## 2. Commands executed (chronological)

```powershell
# 1. Create destination folders for the new taxonomy
New-Item -ItemType Directory src/analyses/portfolio, support/storytelling, support/validation, support/documentation, archive

# 2. Move scripts into their new homes with descriptive names
Move-Item src/analyses/initial_inspection_books.py src/analyses/portfolio/01_initial_inspection_books.py
Move-Item src/analyses/eda_books.py src/analyses/portfolio/02_deep_dive_eda.py
Move-Item src/analyses/run_core_metrics.py src/analyses/portfolio/03_core_metrics_suite.py
Move-Item src/analyses/sql_vs_pandas_compare.py src/analyses/portfolio/04_sql_vs_pandas_compare.py
Move-Item src/analyses/plot_comparison_summary.py src/analyses/support/storytelling/plot_comparison_summary.py
Move-Item src/analyses/export_phase05_slide.py src/analyses/support/storytelling/export_phase05_slide.py
Move-Item src/analyses/metrics_catalog.py src/analyses/support/documentation/metrics_catalog.py
Move-Item src/analyses/postgres_*.py src/analyses/support/validation/
Move-Item src/check_data_quality.py src/analyses/archive/check_data_quality_legacy.py
Move-Item tmp/column_summary.py src/analyses/archive/column_summary_experiment.py

# 3. Rename portfolio modules to valid module identifiers
Rename-Item src/analyses/portfolio/01_initial_inspection_books.py src/analyses/portfolio/p01_initial_inspection_books.py
...

# 4. Update docstrings and module references
code src/analyses/portfolio/p0*_*.py  # Added portfolio-facing descriptions + fixed PROJECT_ROOT path in p01.
code tests/test_reporting_artifacts.py   # Adjusted imports to storytelling namespace.
code Makefile, .github/workflows/ci.yml, scripts/Invoke-Phase05ComparisonRefresh.ps1  # Updated module paths.
```

_All commands were executed from the repo root (`C:\Users\shady\Documents\GITHUB\goodreads-books-analytics`). See Git history for precise PowerShell transcripts._

## 3. New folder structure snapshot

```
src/analyses/
├── portfolio/
│   ├── p01_initial_inspection_books.py
│   ├── p02_deep_dive_eda.py
│   ├── p03_core_metrics_suite.py
│   └── p04_sql_vs_pandas_compare.py
├── support/
│   ├── documentation/metrics_catalog.py
│   ├── storytelling/
│   │   ├── plot_comparison_summary.py
│   │   └── export_phase05_slide.py
│   └── validation/
│       ├── postgres_compare_stats.py
│       ├── postgres_profile_columns.py
│       └── postgres_validate_books.py
└── archive/
    ├── check_data_quality_legacy.py
    └── column_summary_experiment.py
```

## 4. Portfolio spine annotations

| Script                                                   | Purpose                                                                                                                                                     | How to run                                                                                                                                        |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/analyses/portfolio/p01_initial_inspection_books.py` | CLI walkthrough that verifies the repo structure, fabricates the tiny CSV demo, and exports quick-look artifacts to `outputs/initial_inspection/`.          | `docker compose -f docker-compose.python.yml exec app python -m src.analyses.portfolio.p01_initial_inspection_books --sample-size 1000 --verbose` |
| `src/analyses/portfolio/p02_deep_dive_eda.py`            | Phase 03 deep-dive EDA: configures plotting defaults, loads `books.csv`, outputs numeric/categorical/outlier summaries under `outputs/phase03_univariate/`. | `docker compose ... exec app python -m src.analyses.portfolio.p02_deep_dive_eda --verbose --limit 5000`                                           |
| `src/analyses/portfolio/p03_core_metrics_suite.py`       | Phase 04 core KPI generator: loads `books_clean.csv`, computes M1/M3/M4/M5/M7/M8/M9/M11, saves CSVs in `outputs/phase04_core_metrics/`.                     | `make core-metrics` (wraps `python -m src.analyses.portfolio.p03_core_metrics_suite`)                                                             |
| `src/analyses/portfolio/p04_sql_vs_pandas_compare.py`    | Phase 05 SQL vs pandas comparator: runs SQL files via Postgres, loads Phase 04 CSVs, and writes parity evidence to `outputs/phase05_step03_task01/`.        | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.portfolio.p04_sql_vs_pandas_compare --log-level INFO`            |

Each module now begins with a portfolio-focused docstring so newcomers understand what role it plays before reading the code.

## 5. Support bench recap

| Folder                   | Scripts                                                                                  | Description                                                                                                                  |
| ------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `support/storytelling/`  | `plot_comparison_summary.py`, `export_phase05_slide.py`                                  | Turn SQL vs pandas outputs into visuals and slide decks; imports updated in tests, CI, and PowerShell wrappers.              |
| `support/documentation/` | `metrics_catalog.py`                                                                     | Generates `outputs/phase04_metrics_catalog.md`; Makefile + CI now call `src.analyses.support.documentation.metrics_catalog`. |
| `support/validation/`    | `postgres_validate_books.py`, `postgres_profile_columns.py`, `postgres_compare_stats.py` | PostgreSQL validation CLIs used throughout Phase 05 notes; no rename beyond folder move.                                     |

## 6. Archive bucket

- `check_data_quality_legacy.py` – preserved for historical context but removed from the default import path.
- `column_summary_experiment.py` – the former `tmp/` helper now archived with a descriptive suffix.

## 7. Documentation + glossary updates

- `README.md` – references to analysis scripts now point to the portfolio folders; the SQL portfolio section mentions the new CLI module name.
- `docs/data-faq.md` – added entries describing the portfolio spine, support folders, and how to regenerate the PowerShell manifest after folder moves.
- `docs/phase-06-glossary.md` – expanded terms (portfolio spine, support bench, archive bucket) with the final paths.
- `docs/phase5-glossary.md` and Phase 05 task notes – updated module names for the SQL vs pandas comparator, chart renderer, and slide exporter.

## 8. Testing and automation

- `tests/test_reporting_artifacts.py` imports now use `src.analyses.support.storytelling.*` after the move.
- `Makefile` (`metrics-catalog`, `core-metrics`) points to the new module paths.
- GitHub Actions and `scripts/Invoke-Phase05ComparisonRefresh.ps1` were updated to call the renamed modules.

## 9. Checklist review

- [x] Portfolio spine created with numbered scripts and docstrings.
- [x] Support helpers regrouped under `support/`.
- [x] Legacy experiments archived.
- [x] Docs (notes, README, FAQ, glossaries) updated to reference the new structure.
- [x] Tests, CI, and automation scripts validated with the updated import paths.

## 10. Next steps

- Re-run the full portfolio spine (p01→p04) inside Docker to capture fresh screenshots for the Phase 06 storytelling deliverables.
- Consider deleting fully deprecated scripts after the archive folder remains untouched for one sprint.
- Iterate on README screenshots to reflect the new folder tree once we finalize Step 01 Task 04.
