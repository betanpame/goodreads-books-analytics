# Goodreads Books Analytics – Project Plan

This plan describes a complete beginner-level but professional-grade data analytics project using the **Goodreads Books** dataset. It is organized in **phases → steps → tasks** to guide you from environment setup to a portfolio-ready deliverable.

## Project Summary

- **Goal**: Build an end‑to‑end data analytics project that answers key business questions about books, authors, and publishers using the Goodreads dataset.
- **Audience**: Beginner in data analytics with basic Python or SQL knowledge.
- **Technologies**:
  - **Python**: `pandas`, `matplotlib` / `seaborn`, CLI-first analysis scripts
  - **SQL**: PostgreSQL (running in Docker)
  - **Dev Tools**: Git, GitHub, VS Code
  - **Containers**: Docker for the Python CLI environment, Docker for PostgreSQL
- **Dataset**: `data/books.csv` in this repository (derived from the Goodreads dataset on Kaggle).
- **Duration**: 4–6 weeks (self‑paced; phases do not map strictly to calendar weeks).

## Learning Objectives

By the end of this project you will be able to:

1. **Set up a reproducible analytics environment** using Docker for Python CLI and PostgreSQL.
2. **Explore and understand a real‑world dataset** using both **pandas** and **SQL**.
3. **Perform Exploratory Data Analysis (EDA)** and basic data quality checks.
4. **Answer concrete business questions** about books, authors, publishers, and reader behavior.
5. **Create clear visualizations** that communicate insights effectively.
6. **Use SQL and pandas together**: load data into PostgreSQL, write analytical queries, and compare with pandas workflows.
7. **Document your project professionally** with analysis scripts, a structured README, and clear project organization.
8. **Prepare the project to be cloud‑ready**, using containers to make deployment and sharing easier.

## High-Level Questions to Answer

These questions guide the analysis and will be refined in later phases:

- What characteristics are associated with **highly rated books**?
- Which **authors and publishers** perform best by average rating and engagement (ratings count, text reviews)?
- How do **genres / themes (proxied by title and known fields)** and **book length (pages)** relate to reader satisfaction?
- How have **publication patterns over time** changed (e.g., number of books per year, popularity trends)?

## Project Structure (Phases)

The plan is implemented in subfolders under `plan/`, one folder per phase. Each phase has its own `overview.md`, `steps/` folder, and under each step a `tasks/` folder.

Planned phases:

1. **Phase 01 – Project Setup and Environment**  
   Folder: `phase-01-project-setup-and-environment/`

   - Define scope, set up Git/GitHub, prepare Docker for Python CLI, connect to existing PostgreSQL in Docker.

2. **Phase 02 – Data Loading and Initial Exploration**  
   Folder: `phase-02-data-loading-and-initial-exploration/`

   - Inspect `books.csv`, load data with pandas, design database schema, and load data into PostgreSQL.

3. **Phase 03 – EDA and Data Quality Assessment**  
   Folder: `phase-03-eda-and-data-quality/`

   - Perform univariate and bivariate EDA, identify data quality issues, and document assumptions and cleaning rules.

4. **Phase 04 – Business Analysis and Visualizations (Python)**  
   Folder: `phase-04-business-analysis-and-visualizations/`

   - Use pandas + visualizations to answer key business questions and create insight‑driven charts.

5. **Phase 05 – SQL Analysis in PostgreSQL**  
   Folder: `phase-05-sql-analysis-in-postgres/`

   - Reproduce and extend key analyses using SQL queries, practicing joins, aggregations, and basic window functions.

6. **Phase 06 – Documentation, Storytelling, and Portfolio Packaging**  
   Folder: `phase-06-documentation-and-storytelling/`

   - Organize analysis scripts, write a professional README, summarize insights, and prepare the repo for portfolio use.

7. **Phase 07 – Production Readiness and Cloud-Ready Setup**  
   Folder: `phase-07-production-readiness-and-next-steps/`
   - Refine Docker setup, document how to run the project end‑to‑end, and propose next steps for cloud deployment.

Each phase has:

- **Goal**: What you should achieve.
- **Inputs**: What is required before starting.
- **Outputs / Deliverables**: Concrete artifacts (files, scripts, analysis scripts, queries).
- **Steps**: Logical groupings of work.
- **Tasks**: Actionable items with checklists.

## Recommended Final Deliverables (Portfolio-Ready)

By the end of the project, this repository should include at least:

1. **Clean and organized folder structure**:

   - `data/` – raw dataset(s) (or download instructions if data cannot be committed).
   - `src/analyses/` – Python CLI workflow analysis scripts for EDA, analysis, and final report.
   - `sql/` – SQL scripts for table creation and analytical queries.
   - `src/` (optional) – Python modules if you decide to refactor code out of analysis scripts.
   - `docker/` – Dockerfile(s) and compose file(s) for Python CLI and PostgreSQL.
   - `plan/` – This planning structure.

2. **Analysis Scripts**:

   - `src/analyses/01_eda_books.py` – Initial exploration and data quality checks.
   - `src/analyses/02_analysis_and_visualizations.py` – Main business analysis and charts.
   - `src/analyses/03_sql_vs_pandas_comparison.py` (optional/advanced) – Compare SQL and pandas approaches.

3. **SQL Assets**:

   - `sql/create_tables.sql` – DDL for the PostgreSQL schema.
   - `sql/load_books.sql` or notes on using `COPY`/`psql` to load data.
   - `sql/analysis_queries.sql` – Saved queries answering key questions.

4. **Documentation**:

   - Root `README.md` with:
     - Project overview
     - Tech stack
     - How to run with Docker (Python container + PostgreSQL container)
     - Quick demo of insights and screenshots of charts
   - `plan/` documentation (this folder) kept in sync with what was actually implemented.

5. **Docker and Environment**:

   - `docker/python/` or similar folder with a `Dockerfile` for the Python CLI environment.
   - A `docker-compose.yml` (or similar file) that:
     - Starts the Python CLI container.
     - Connects to your existing PostgreSQL Docker container (or defines one if needed in the future).

6. **Version Control and Collaboration**:
   - Clear commit history showing progression through phases.
   - Optional: basic Git branching (e.g., feature branches for major changes).

## How to Use This Plan

1. Start with **Phase 01** and work top‑down:
   - Read `plan/phase-01-project-setup-and-environment/overview.md`.
   - Then follow the steps in the `steps/` and `tasks/` subfolders.
2. Only move to the next phase when:
   - You have completed the tasks and produced the outputs for the current phase.
   - You understand _why_ each task was done.
3. Use this project to practice professional habits:
   - Write meaningful commit messages.
   - Keep notes of decisions in markdown files.
   - Regularly review whether the project still answers the original business questions.

As you progress, you can modify this plan to fit your pace and interests, but keep the **phase → step → task** structure to maintain clarity and discipline.
