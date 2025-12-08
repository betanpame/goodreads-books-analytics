# Phase 05 · Step 03 · Task 02 – SQL Learnings Summary

This task capture follows the standard note template so recruiters (and future you) can reproduce the storytelling deliverable without guessing commands.

## 1. Task definition and goal

Summarize every SQL insight from Phase 05 in a portfolio-ready format while reinforcing that the workflow lives entirely inside Python + Docker (no Jupyter notebooks). The deliverable is a narrative section that explains:

- Which business questions were answered in SQL.
- Which PostgreSQL features and patterns you practiced (CTEs, window functions, canonical views).
- How the SQL layer validates and complements the pandas metrics from Phase 04.
- Where reviewers can pull fresh evidence (CSV, PNG, PPTX) in one command.

## 2. How to run this analysis script

### Command block (copy/paste)

```powershell
cd C:\Users\shady\Documents\GITHUB\goodreads-books-analytics
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide
```

### Estimated runtime & success outputs

- **Runtime:** ≈45 seconds end-to-end on a warm Docker stack (Ryzen 7 / 16 GB RAM). First run may take ~2 minutes while pulling images.
- **Success checklist:**
  - `outputs/phase05_step03_task01/comparison_summary.{csv,md,png}` refreshed with the latest timestamp.
  - `docs/phase-05-step-03-task-01-slide.pptx` rewritten with the same timestamp as the PNG/CSV.
  - PowerShell log prints `All SQL vs pandas comparisons matched` and lists all 11 metrics (M1–M11).

### Prerequisites before running anything

- Docker Desktop running and logged in (the compose files depend on the default Docker Desktop context).
- `.env` copied from `.env.example` and updated with PostgreSQL credentials—the PowerShell script reads the same variables used by the Python modules.
- `books_clean.csv` present under `data/derived/`; if missing, rerun the cleaning pipeline from Phase 04 first.

Run the canonical three-command block above, then call the orchestration script with slide export enabled. This keeps everything reproducible without leaving PowerShell.

What the script does (and the internal commands it triggers):

| Stage                 | Internal CLI                                                                                                                                                                                                                                  | Key log lines                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Stack bootstrap       | `docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d`                                                                                                                                                          | `Ensuring docker compose stack is up...` followed by container IDs.                                                     |
| Table refresh         | `docker compose -f docker-compose.python.yml run --rm app python -m src.load_books_clean_to_postgres --csv-path data/derived/books_clean.csv --table books_clean`                                                                             | `Writing 11127 rows to table books_clean` and `Writing 19216 author rows to book_authors_stage`.                        |
| Metric comparison     | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.portfolio.p04_sql_vs_pandas_compare --output-dir outputs/phase05_step03_task01`                                                                              | `Running SQL for M1_...` through `M11_...` plus `Wrote summary table... All SQL vs pandas comparisons matched`.         |
| Visualization + slide | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.support.storytelling.plot_comparison_summary` and `python -m src.analyses.support.storytelling.export_phase05_slide` (invoked inside the PowerShell wrapper) | `Saved chart to outputs/.../comparison_summary.png` and `Saved slide deck to docs/phase-05-step-03-task-01-slide.pptx`. |

## 3. Environment recap

- Runtime: Docker Desktop with both compose files (`python` + `postgresql`). Confirm via `docker compose -f docker-compose.python.yml ps` before running the PowerShell script.
- Python: 3.10-slim image defined in `docker/python/Dockerfile`. All modules execute with `python -m ...` inside the `app` container; notebooks stay out of scope to keep CI-friendly logs.
- Database: PostgreSQL 17 container reading `/var/lib/postgresql/data` volume. Data is reloaded from `data/derived/books_clean.csv` every time the wrapper runs so parity evidence is never stale.
- Source control: `main` branch; commit README + docs edits together with regenerated outputs to keep reviewers aligned with portfolio screenshots.

## 4. Findings / results

1. **Narrative upgraded for recruiters** – Added "SQL Portfolio Spotlight" to `README.md` with 3 paragraphs describing CSV→PostgreSQL parity, automation story, and direct instructions to rerun `Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide`.
2. **Key SQL accomplishments catalogued** – Document now references the exact SQL files (`20_`, `30_`, `40_`, `55_`, `60_`, `70_`, `80_`) plus the Python comparator module, so reviewers can open the source next to the artifacts.
3. **Capability bullets** – Explicitly call out `GROUP BY`, `HAVING`, `ROW_NUMBER`, `PERCENTILE_CONT`, rolling 3-year frames, and canonical staging tables; this mirrors the skills matrix typically requested in interview screens.
4. **Asset table for portfolios** – README section now lists each proof artifact (CSV/MD/PNG/PPTX + this note) with regeneration commands, making it trivial to cite in a cover letter or GitHub README.
5. **Strict Python/Docker positioning** – All steps reference the compose files and ban notebooks, satisfying the user story constraint and making it clear to recruiters that automation/CI are first-class.

## 5. Expected output checkpoints

- PowerShell script logs `comparison_summary.csv`, `.md`, `.png`, and the PPTX path (see sample snippet below) so you can screenshot evidence for the portfolio.
- `README.md` shows the "SQL Portfolio Spotlight (Fase 05)" section with narrative paragraphs, capability bullets, and the artifact table.
- This note file (`docs/phase-05-step-03-task-02-notes.md`) references the commands above and mirrors the template section order.
- `git status` lists updates to `README.md`, this note, `outputs/phase05_step03_task01/*`, and `docs/phase-05-step-03-task-01-slide.pptx`.

Sample log excerpt from the PowerShell wrapper (Dec 5, 2025 run):

```
2025-12-05 23:33:40,985 INFO __main__ - Writing 11127 rows to table books_clean
2025-12-05 23:33:44,625 INFO __main__ - Wrote summary table to outputs/phase05_step03_task01/comparison_summary.csv
2025-12-05 23:33:44,630 INFO __main__ - All SQL vs pandas comparisons matched
Saved chart to outputs/phase05_step03_task01/comparison_summary.png
Saved slide deck to docs/phase-05-step-03-task-01-slide.pptx
```

## 6. Observations / insights

- Recruiters respond better when SQL + pandas parity is framed as an audit trail; the summary emphasizes that SQL is not a side quest but a validation layer.
- Calling the PowerShell wrapper is faster (≈40s) than running each module manually and guarantees the chart + PPTX stay in sync, which is critical for a portfolio artifact.
- Explicitly stating "no notebooks" removes friction for reviewers who expect bash/PowerShell scripts and also signals CI friendliness.

## 7. Artifacts refreshed each run

- `outputs/phase05_step03_task01/comparison_summary.csv`
- `outputs/phase05_step03_task01/comparison_summary.md`
- `outputs/phase05_step03_task01/comparison_summary.png`
- `docs/phase-05-step-03-task-01-slide.pptx`
- `README.md` · sección "SQL Portfolio Spotlight (Fase 05)" (textual artifact, no binary refresh needed once added)
- `docs/phase-05-step-03-task-02-notes.md` (this file)

## 8. Q&A / data troubleshooting

**Q: Where do I copy the portfolio snippet from?**  
A: Use the Appendix below (same text as the README section). Paste it into LinkedIn, personal sites, or case-study slides.

**Q: Can I run this without Docker?**  
A: No. The project standard is Docker-only for Phase 05 to keep Python, PostgreSQL, and dependencies consistent. If you must run locally, replicate the container image first.

**Q: How do I prove the SQL features mentioned actually exist?**  
A: Link directly to the SQL files in `sql/analysis/` (e.g., `60_top_books_per_author.sql`, `80_publication_year_rolling_stats.sql`) and to the comparison outputs. Mention commit hashes when sharing externally.

**Q: What if I want to spotlight different metrics?**  
A: Update the bullet list in README plus this note, then rerun `scripts/Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide` so the chart/PPTX align with the new narrative.

**Q: How do I verify the PPTX exported correctly?**  
A: After the command finishes, open `docs/phase-05-step-03-task-01-slide.pptx` (single-slide deck) and confirm the timestamp + metric summary match the newest CSV. The PowerShell log prints the absolute path when the export completes.

## 9. Checklist review

- [x] Key SQL accomplishments listed.
- [x] Narrative paragraphs about SQL experience written.
- [x] Bullet list of SQL capabilities added.
- [x] Links to SQL scripts and analysis script added (README section + Appendix).
- [x] Text reviewed for clarity and portfolio readiness.

## 10. Appendix – Portfolio-ready summary (copy/paste)

```
## SQL Portfolio Spotlight (Fase 05)

Durante Step 03 consolidamos todo el trabajo SQL dentro del flujo de Python/Docker para que cualquier reclutador pueda reproducirlo sin abrir notebooks. El guion es el siguiente:

- **Narrativa** -> Partimos de los CSV generados en pandas (Fase 04), los cargamos en PostgreSQL con `src.load_books_clean_to_postgres`, y luego usamos `src.analyses.portfolio.p04_sql_vs_pandas_compare` para demostrar que ambas capas responden las mismas preguntas de negocio.
- **Preguntas respondidas** → Rankings de autores/libros, evolución temporal de ratings, idiomas/publishers más sólidos, duplicados, engagement percentiles y rolling windows.
- **Entrega visual** → `scripts/Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide` refresca métricas, genera `comparison_summary.png` y exporta una diapositiva (`outputs/phase05_step03_task01/phase05_sql_vs_pandas.pptx`) lista para portfolios o entrevistas.

### Capacidades SQL practicadas

- Agrupaciones con `GROUP BY`, filtros con `HAVING` y cláusulas `WHERE` parametrizadas vía CTEs.
- Ventanas (`ROW_NUMBER`, `PERCENTILE_CONT`, frames de 3 años) para rankings por autor y métricas rolling.
- Combinación de vistas canonicalizadas + staging (`book_authors_stage`) para evitar duplicados en los KPIs.
- Exportación repetible desde Python (sin Jupyter) usando Docker Compose para garantizar el mismo entorno en cualquier máquina.

### Activos para mostrar en el portfolio

| Activo | Descripción | Cómo regenerarlo |
| --- | --- | --- |
| `README.md` · sección “SQL Portfolio Spotlight” | Resumen ejecutivo en tono profesional, listo para recruiters. | Actual archivo (sin pasos adicionales). |
| `docs/phase-05-step-03-task-02-notes.md` | Bitácora detallada (paso a paso, comandos PowerShell). | `powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-Phase05ComparisonRefresh.ps1` + seguir la nota. |
| `outputs/phase05_step03_task01/comparison_summary.{csv,md,png}` | Evidencia cuantitativa y visual del parity SQL vs pandas. | `docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.portfolio.p04_sql_vs_pandas_compare`. |
| `docs/phase-05-step-03-task-01-slide.pptx` | Diapositiva con storytelling (ingresa directo en portafolios). | `scripts/Invoke-Phase05ComparisonRefresh.ps1 -ExportSlide`. |
```
