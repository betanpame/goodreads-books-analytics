# Project Structure and Tools Overview

This document explains the structure of the `goodreads-books-analytics` repository and the main tools you will use. It is written as a portfolio‑ready reference so that someone reading your GitHub profile can quickly understand how the project is organized and how to navigate it.

## 1. High‑Level Repository Map

At the top level of the repository you will find:

- `.env` / `.env.example` – Environment variable files for configuring PostgreSQL and other settings.
- `.git/` and `.gitignore` – Git metadata and ignore rules.
- `data/` – Raw dataset(s) used for analysis.
- `docs/` – Documentation and learning notes (pandas, SQL, Docker, PostgreSQL, and repo structure).
- `plan/` – Phase → step → task project plan.
- `src/` – Python source code for data cleaning, loading, and pipeline orchestration.
- `tests/` – Automated tests for the Python code in `src/`.
- `docker-compose.postgresql.yml` – Docker Compose configuration for the PostgreSQL database.
- `LICENSE` – License for the project.
- `README.md` – Main entry point describing the project, requirements, and how to run the pipeline.

This structure separates data, code, documentation, and planning so that each concern has a clear home.

## 2. Data Folder (`data/`)

- **Current contents**: `books.csv`, a CSV file derived from the Goodreads books dataset.
- **Typical columns** (based on the first ~50 rows):
  - `bookID`, `title`, `authors`
  - `average_rating`, `ratings_count`, `text_reviews_count`
  - `isbn`, `isbn13`, `language_code`, `num_pages`
  - `publication_date`, `publisher`
- **Role in the project**:
  - Serves as the primary input for the analytics pipeline.
  - Will be read by Python (pandas) scripts and loaded into PostgreSQL.
- **Best practice for similar projects**:
  - Keep raw data immutable (never manually edit `books.csv`).
  - Store derived or cleaned data in a separate location (e.g., `data/processed/` or `outputs/`).

## 3. Source Code (`src/`)

- **Purpose**: Contains Python modules and scripts that implement the data pipeline.
- **Typical components** in this repository:
  - `cleaning.py` – Functions to clean and transform the raw Goodreads data.
  - `check_data_quality.py` – Basic data quality checks (missing values, duplicates, ranges).
  - `load_books_to_postgres.py` – Script to load `books.csv` (or a cleaned version) into PostgreSQL.
  - `run_full_pipeline.py` – Orchestration script to run cleaning, saving, and optional database loading.
- **How this maps to real‑world projects**:
  - Keeping code in `src/` makes it easy to import functions from analysis scripts and tests.
  - You can later package this into a Python module or CLI if you want to make the project more production‑ready.

## 4. Tests (`tests/`)

- **Purpose**: Provide automated checks that verify the behavior of key functions.
- **Current content example**:
  - `test_cleaning.py` – Tests that verify data cleaning logic (e.g., handling missing values or inconsistent formats).
- **Why this matters for your portfolio**:
  - Showing tests signals that you understand good engineering practices.
  - Even a few well‑chosen tests are enough to demonstrate that you think about correctness and maintainability.

## 5. Planning Folder (`plan/`)

- **Structure**: Organized as **phase → step → task**. For example:
  - `phase-01-project-setup-and-environment/`
    - `overview.md`
    - `steps/step-01-understand-repo-and-tools/overview.md`
    - `steps/step-01-understand-repo-and-tools/tasks/task-01-review-repository-structure.md`
- **Role in the project**:
  - Acts as a roadmap for building the project incrementally.
  - Each task is small and concrete, making the project approachable for beginners.
- **How you can reuse this idea**:
  - For a new analytics project, create a similar `plan/` folder with phases like environment setup, data loading, EDA, modeling/analysis, and documentation.
  - Write tasks as checklists; this helps you track progress and keeps the project structured.

## 6. Documentation Folder (`docs/`)

- **Contents**:
  - `dataset-notes.md` – Notes about the Goodreads dataset and any assumptions or quirks.
  - `pandas-cheatsheet.md` – Quick reference for common pandas operations.
  - `sql-cheatsheet.md` – Quick reference for SQL syntax and patterns.
  - `docker/` – Introductions and how‑tos for Docker and Docker Compose.
  - `postgresql/` – Introductory notes on PostgreSQL.
  - `repo-notes.md` – The file where you record personal notes about the repository structure.
- **Portfolio angle**:
  - Having a rich `docs/` folder shows that you invest in explaining your work.
  - It also gives reviewers insight into how you learn and document tools.

## 7. Docker and PostgreSQL (`docker-compose.postgresql.yml`)

- **File**: `docker-compose.postgresql.yml`
- **Purpose**:
  - Defines a PostgreSQL service that runs inside Docker.
  - Uses environment variables from `.env` to configure database name, user, password, ports, and storage.
- **Why this is useful**:
  - Makes your environment reproducible: others can start the same database with a single command.
  - Avoids installing PostgreSQL directly on the host machine.
- **Command example (PowerShell)**:

```powershell
# Start PostgreSQL in the background
docker compose -f docker-compose.postgresql.yml up -d

# Check status
docker compose -f docker-compose.postgresql.yml ps
```

## 8. README and LICENSE

- `README.md`:
  - Introduces the project (Goodreads books analytics).
  - Lists prerequisites (Python, Docker).
  - Explains environment variables and basic Docker/PostgreSQL usage.
  - Shows how to run the data pipeline scripts.
- `LICENSE`:
  - Defines how others can use the code and materials in this repository.

## 9. How to Apply This Structure to Your Own Projects

If you want to create a similar analytics project from scratch, you can follow this pattern:

1. **Create a clear folder layout**:
   - `data/`, `src/`, `tests/`, `docs/`, `plan/`, and any Docker or configuration files at the root.
2. **Write a simple plan**:
   - Even a single markdown file with phases (setup, data loading, EDA, analysis, documentation) helps you stay organized.
3. **Document as you go**:
   - Use `docs/` for notes on tools and decisions.
   - Use a file like `repo-notes.md` to log how the structure evolves.
4. **Add automation early**:
   - Use simple tests in `tests/` and scripts in `src/` to avoid duplicating work in analysis scripts.
5. **Keep the README up to date**:
   - Treat it as the landing page for people discovering your project.

By structuring your projects in this way, you make them easier to maintain, easier to understand, and more impressive in a portfolio context.
