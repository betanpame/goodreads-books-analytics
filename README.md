# goodreads-books-analytics

End-to-end analysis of the public Goodreads Books dataset using Python CLI modules, PostgreSQL, and Docker. The repository bundles reproducible scripts, phase-by-phase notes, and portfolio-ready artifacts (CSV, PNG, PPTX).

## Project Snapshot & Outcomes

- Curated dataset `books_clean.csv` plus a PostgreSQL schema ready for repeat loads.
- CLI coverage for EDA/QA (`p01`, `p02`), KPI generation (`p03`), and SQL vs pandas parity checks (`p04`) with versioned outputs.
- Dedicated SQL suite under `sql/` and Postgres validation helpers (`support/validation`) to prove pandas ↔ SQL alignment.
- Full documentation spine: README, phase plan, FAQs, glossaries, and storytelling deliverables (Phase 06).

## Stack Highlights

- Python 3.10 CLI modules running inside Docker · pandas · seaborn · matplotlib.
- PostgreSQL 17 orchestrated with Docker Compose (`docker-compose.python.yml`, `docker-compose.postgresql.yml`).
- PowerShell wrappers (in `scripts/`) to run loads, comparisons, and slide exports end-to-end.
- GitHub Actions CI pipeline plus sanity tests in `tests/`.

## Quick Links

- Start Here Map (phases, prerequisites, notes): ↓
- SQL Portfolio Spotlight: `docs/phase-05-step-03-task-02-notes.md` and `docs/phase-05-step-03-task-01-slide.pptx`.
- Phase 06 restructure log: `docs/phase6-step1-task3-notes.md`.
- FAQs & glossaries: `docs/data-faq.md`, `docs/phase-05-glossary.md`, `docs/phase-06-glossary.md`.

## Start Here Map (Step-by-Step)

Follow the phases in order. Each step links to its detailed notes and lists the prerequisites you must satisfy before running commands.

1. **Phase 01 – Project Setup and Environment**

   - [Step 01 – Understand Repository and Tools](plan/phase-01-project-setup-and-environment/steps/step-01-understand-repo-and-tools/) — Guided tour of folders and tooling checklist. _Prereqs: repo cloned locally, Git and VS Code installed._ Notes: [T1](docs/phase-01-step-01-task-01-notes.md) · [T2](docs/phase-01-step-01-task-02-notes.md) · [T3](docs/phase-01-step-01-task-03-notes.md)
   - [Step 02 – Design Python CLI Docker Environment](plan/phase-01-project-setup-and-environment/steps/step-02-design-python-docker-environment/) — Define the base image, dependencies, and env vars. _Prereqs: Step 01 complete, Docker Desktop running._ Notes: [T1](docs/phase-01-step-02-task-01-notes.md) · [T2](docs/phase-01-step-02-task-02-notes.md) · [T3](docs/phase-01-step-02-task-03-notes.md)
   - [Step 03 – Implement and Test Docker Setup](plan/phase-01-project-setup-and-environment/steps/step-03-implement-and-test-docker-setup/) — Build and validate the Python + Postgres containers. _Prereqs: Step 02 configured, `.env` initialized._ Notes: [T1](docs/phase-01-step-03-task-01-notes.md) · [T2](docs/phase-01-step-03-task-02-notes.md) · [T3](docs/phase-01-step-03-task-03-notes.md)

2. **Phase 02 – Data Loading and Initial Exploration**

   - [Step 01 – Inspect Dataset with pandas](plan/phase-02-data-loading-and-initial-exploration/steps/step-01-inspect-dataset-with-pandas/) — Run `.info()`, `.describe()`, and capture first observations. _Prereqs: Phase 01 environment running, `data/books.csv` present._ Notes: [T1](docs/phase-02-step-01-task-01-notes.md) · [T2](docs/phase-02-step-01-task-02-notes.md) · [T3](docs/phase-02-step-01-task-03-notes.md)
   - [Step 02 – Design PostgreSQL Schema](plan/phase-02-data-loading-and-initial-exploration/steps/step-02-design-postgres-schema/) — Map columns to table structures and data types. _Prereqs: Step 01 complete, Postgres reachable._ Notes: [T1](docs/phase-02-step-02-task-01-notes.md) · [T2](docs/phase-02-step-02-task-02-notes.md) · [T3](docs/phase-02-step-02-task-03-notes.md)
   - [Step 03 – Load Data into PostgreSQL](plan/phase-02-data-loading-and-initial-exploration/steps/step-03-load-data-into-postgres/) — Execute the first `books.csv → postgres` load. _Prereqs: Step 02 approved, Postgres container up._ Notes: [T1](docs/phase-02-step-03-task-01-notes.md) · [T2](docs/phase-02-step-03-task-02-notes.md) · [T3](docs/phase-02-step-03-task-03-notes.md)

3. **Phase 03 – EDA and Data Quality**

   - [Step 01 – Univariate EDA](plan/phase-03-eda-and-data-quality/steps/step-01-univariate-eda/) — Check distributions, outliers, and summary tables. _Prereqs: Phase 02 outputs available._ Notes: [T1](docs/phase-03-step-01-task-01-notes.md) · [T2](docs/phase-03-step-01-task-02-notes.md) · [T3](docs/phase-03-step-01-task-03-notes.md)
   - [Step 02 – Bivariate & Relationships](plan/phase-03-eda-and-data-quality/steps/step-02-bivariate-eda/) — Correlate metrics (rating vs pages, etc.). _Prereqs: Step 01 charts saved._ Notes: [T1](docs/phase-03-step-02-task-01-notes.md) · [T2](docs/phase-03-step-02-task-02-notes.md) · [T3](docs/phase-03-step-02-task-03-notes.md)
   - [Step 03 – Data Quality & Cleaning Rules](plan/phase-03-eda-and-data-quality/steps/step-03-data-quality-and-cleaning-rules/) — Document null, duplicate, and formatting decisions. _Prereqs: Step 02 findings, `docs/dataset-notes.md` open._ Notes: [T1](docs/phase-03-step-03-task-01-notes.md) · [T2](docs/phase-03-step-03-task-02-notes.md) · [T3](docs/phase-03-step-03-task-03-notes.md)

4. **Phase 04 – Business Analysis & Visualizations**

   - [Step 01 – Implement Cleaning in Python](plan/phase-04-business-analysis-and-visualizations/steps/step-01-implement-cleaning-in-python/) — Produce `books_clean.csv`. _Prereqs: Data-quality playbook finalized._ Notes: [T1](docs/phase-04-step-01-task-01-notes.md)
   - [Step 02 – Define Metrics and Visuals](plan/phase-04-business-analysis-and-visualizations/steps/step-02-define-and-compute-metrics/) — Calculate KPIs and prototype visuals. _Prereqs: Clean dataset plus `src/metrics/core_metrics.py` ready._ Notes: [T1](docs/phase-04-step-02-task-01-notes.md) · [T2](docs/phase-04-step-02-task-02-notes.md)
   - [Step 03 – Build Insightful Visualizations](plan/phase-04-business-analysis-and-visualizations/steps/step-03-build-visualizations/) — Assemble charts and narrative (see plan folder).

5. **Phase 05 – SQL Analysis in PostgreSQL**

   - [Step 01 – Validate Data in PostgreSQL](plan/phase-05-sql-analysis-in-postgres/steps/step-01-validate-data-in-postgres/) — Run validation CLIs under `support/validation`. _Prereqs: Docker stack running._ Notes: [T1](docs/phase-05-step-01-task-01-notes.md) · [T2](docs/phase-05-step-01-task-02-notes.md) · [T3](docs/phase-05-step-01-task-03-notes.md)
   - [Step 02 – Implement Core SQL Queries](plan/phase-05-sql-analysis-in-postgres/steps/step-02-implement-analysis-queries/) — Write CTEs, windows, and canonical tables. _Prereqs: Step 01 parity checks green._ Notes: [T1](docs/phase-05-step-02-task-01-notes.md) · [T2](docs/phase-05-step-02-task-02-notes.md) · [T3](docs/phase-05-step-02-task-03-notes.md)
   - [Step 03 – SQL vs pandas Comparison](plan/phase-05-sql-analysis-in-postgres/steps/step-03-sql-vs-pandas-comparison/) — Execute `p04_sql_vs_pandas_compare`. _Prereqs: Step 02 SQL stored, Phase 04 metrics exported._ Notes: [T1](docs/phase-05-step-03-task-01-notes.md) · [T2](docs/phase-05-step-03-task-02-notes.md)

6. **Phase 06 – Documentation and Storytelling**

   - [Step 01 – Organize Portfolio Scripts](plan/phase-06-documentation-and-storytelling/steps/step-01-organize-src/analyses/) — Restructure `src/analyses/` into portfolio/support/archive and add docstrings. _Prereqs: Phase 05 artifacts generated._ Notes: [T1](docs/phase6-step1-task1-notes.md) · [T2](docs/phase6-step1-task2-notes.md) · [T3](docs/phase6-step1-task3-notes.md)
   - [Step 02 – Write and Polish README](plan/phase-06-documentation-and-storytelling/steps/step-02-write-readme/) — Improve the main narrative. _Prereqs: Step 01 finished._
   - [Step 03 – Create Summary Narrative or Slides](plan/phase-06-documentation-and-storytelling/steps/step-03-create-summary-narrative/) — Produce the slide/story package (see `docs/phase-05-step-03-task-01-slide.pptx`).
   - [Step 04 – Polish Analysis Scripts and Visuals](plan/phase-06-documentation-and-storytelling/steps/step-04-polish-analysis-scripts-and-visuals/) — Final pass on docstrings, annotations, charts.
   - [Step 05 – Prepare Sharing and Next Notes](plan/phase-06-documentation-and-storytelling/steps/step-05-prepare-sharing-and-next-notes/) — Update FAQs, glossaries, and next steps.

7. **Phase 07 – Production Readiness and Next Steps**
   - [Step 01 – Refine Docker Setup](plan/phase-07-production-readiness-and-next-steps/steps/step-01-refine-docker-setup/) — Consolidate orchestration artifacts. _Prereqs: Phases 01–06 stabilized._
   - [Step 02 – Document End-to-End Run Instructions](plan/phase-07-production-readiness-and-next-steps/steps/step-02-document-run-instructions/) — Write a runbook for collaborators/interviewers. _Prereqs: Step 01 containers tuned._
   - [Step 03 – Define Cloud + Extension Roadmap](plan/phase-07-production-readiness-and-next-steps/steps/step-03-define-next-steps/) — Outline cloud deployment, dashboards, jobs.

---

## Environment Prerequisites

- Python 3.10+ (use `.venv` if running outside Docker).
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine.
- PowerShell 5.1 (repo default shell).

### Step-by-Step: Configure `.env`

1. Copy the template: `Copy-Item .env.example .env`.
2. Edit `POSTGRES_*`, `PROJECT_NAME`, and optionally `DATABASE_URL`.
3. Save the file; all CLIs read these variables automatically.

### Step-by-Step: Start PostgreSQL Only

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.postgresql.yml up -d
```

4. Check status: `docker compose -f docker-compose.postgresql.yml ps`.
5. Tail logs if needed: `docker compose -f docker-compose.postgresql.yml logs -f postgres`.
6. Stop services: `docker compose -f docker-compose.postgresql.yml down` (add `-v` to drop volumes).

### Step-by-Step: Run the Python Pipeline Locally (optional)

```powershell
.venv\Scripts\python.exe -m src.load_books_to_postgres --table books
.venv\Scripts\python.exe -m src.run_full_pipeline
.venv\Scripts\python.exe -m src.run_full_pipeline --load-to-postgres
```

Docker-first runs remain the recommended approach for reproducibility, but these commands help for quick local checks.

## Repository Structure (Phase 06 Layout)

- `src/analyses/portfolio/`
  - `p01_initial_inspection_books.py` – Phase 02 sanity checks.
  - `p02_deep_dive_eda.py` – Phase 03 EDA coverage.
  - `p03_core_metrics_suite.py` – Phase 04 KPI automation.
  - `p04_sql_vs_pandas_compare.py` – Phase 05 SQL parity CLI.
- `src/analyses/support/`
  - `validation/` – Postgres schema/profile/parity CLIs.
  - `storytelling/` – `plot_comparison_summary.py`, `export_phase05_slide.py`.
  - `documentation/metrics_catalog.py` – Markdown metrics catalog generator.
- `src/analyses/archive/` – Legacy scripts (see `docs/phase6-step1-task3-notes.md`).

## Key Portfolio Artifacts

| Artifact               | Location                                                        | How to regenerate                                                                                                     |
| ---------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Clean dataset          | `data/derived/books_clean.csv`                                  | `python -m src.run_full_pipeline`                                                                                     |
| Phase 03 EDA outputs   | `outputs/phase03_*`                                             | `python -m src.analyses.portfolio.p02_deep_dive_eda`                                                                  |
| Phase 04 metrics suite | `outputs/phase04_core_metrics/*.csv`                            | `python -m src.analyses.portfolio.p03_core_metrics_suite`                                                             |
| SQL comparison summary | `outputs/phase05_step03_task01/comparison_summary.{csv,md,png}` | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.portfolio.p04_sql_vs_pandas_compare` |
| Slide deck             | `docs/phase-05-step-03-task-01-slide.pptx`                      | `powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide`                 |

## Phase 05 · Step 03 Runbook (SQL vs pandas)

### Fast Path

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide
```

This wrapper lifts the stack, reloads `books_clean`, runs `p04_sql_vs_pandas_compare`, saves `comparison_summary.{csv,md,png}`, and exports the PPTX. Use `-Cases` to limit metrics or `-SkipChart` to skip the PNG.

### Manual Step-by-Step

1. **Start the stack**
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
   ```
2. **Reload the curated dataset (only if `books_clean` changed)**
   ```powershell
   docker compose -f docker-compose.python.yml run --rm app \
     python -m src.load_books_clean_to_postgres \
     --csv-path data/derived/books_clean.csv \
     --table books_clean
   ```
3. **Run the comparator**
   ```powershell
   docker compose -f docker-compose.python.yml run --rm app \
     python -m src.analyses.portfolio.p04_sql_vs_pandas_compare \
     --output-dir outputs/phase05_step03_task01
   ```
4. **Generate visuals and slide**
   ```powershell
   docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.support.storytelling.plot_comparison_summary
   docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.support.storytelling.export_phase05_slide
   ```

### Expected Results

- `comparison_summary.csv` / `.md` with all metrics marked `Match`.
- `comparison_summary.png` ready for recruiters or presentations.
- Updated PPTX at `docs/phase-05-step-03-task-01-slide.pptx`.
- Logs matching the snippets archived in `docs/phase-05-step-03-task-02-notes.md`.

### Troubleshooting Checklist

1. **`*_differences.csv` appears** – Inspect the file under `outputs/phase05_step03_task01/`. If parity was expected, rerun step 2 (reload `books_clean`) and rerun step 3.
2. **Stack drift** – Re-run `scripts/Invoke-Phase05ComparisonRefresh.ps1` to enforce the full sequence (containers → load → comparator → storytelling).
3. **Storytelling helper errors** – Execute `python -m src.analyses.support.storytelling.plot_comparison_summary` or `export_phase05_slide` directly to debug paths and dependencies.
4. **New SQL features to showcase** – Link the relevant `.sql` files in `sql/` plus cite the commit hash in README/FAQ to prove the capabilities you mention.

## Additional Documentation

- `docs/dataset-notes.md` – Dataset context and caveats.
- `docs/data-faq.md` – Frequently asked questions (Docker, SQL, storytelling tips).
- `docs/phase-05-step-03-task-02-notes.md` – Full SQL portfolio narrative.
- `docs/phase-05-glossary.md`, `docs/phase-06-glossary.md` – Phase-specific terminology.
- `docs/sql-cheatsheet.md`, `docs/pandas-cheatsheet.md` – Quick-reference sheets.
- `plan/` – Phase/step/task guides with checklists.

Contributions: open an issue/PR summarizing the change, attach relevant outputs (`comparison_summary.*`, screenshots), and run the appropriate tests before submitting.
