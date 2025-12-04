# Python Environment Requirements – Docker-based Analytics Environment

This document defines the Python environment requirements for the Docker-based analytics container used in the `goodreads-books-analytics` project. It is designed to satisfy **Phase 01 → Step 02 → Task 01 – Define Python Environment Requirements** and to be reusable for similar projects.

---

## 1. Base Python Image

For the Docker image, we will use a modern, slim Python base image suitable for data analytics with additional libraries installed on top:

- **Base image**: `python:3.14-slim`

Rationale:

- `3.14` is a current, stable Python 3 version at the time of writing.
- The `-slim` variant keeps the image smaller while still allowing us to install the required system dependencies for packages like `psycopg2-binary` and scientific libraries.

You can adapt the version in the future if needed (for example, to a newer `python:3.15-slim` when it is stable), but it is important to pin a specific major/minor version to keep the environment reproducible.

---

## 2. Core Python Packages – Must-Have for Phase 01–04

These packages are essential for the main workflow of this project (data loading, cleaning, analysis, visualization, and database connectivity).

### 2.1 Data manipulation and analysis

- `pandas`
  - Primary library for tabular data analysis (reading CSV, transforming data, computing aggregations).
- `numpy`
  - Numerical computing foundation; used under the hood by pandas and for array operations.

### 2.2 Visualization

- `matplotlib`
  - Low-level plotting library; provides full control over charts.
- `seaborn`
  - High-level interface for statistical visualizations built on top of matplotlib; useful for EDA and presentation-ready charts.

### 2.3 CLI workflow helpers

- `python-dotenv`
  - Loads `.env` variables into the process so standalone scripts (for example, `src.run_full_pipeline`) can reuse the same connection settings defined for Docker Compose.
- (Optional) `rich` / `typer`
  - Not required yet, but good candidates if you later add more advanced CLI entry points with progress bars or argument parsing beyond `argparse`.

### 2.4 Database connectivity and ORM/SQL toolkit

- `sqlalchemy`
  - Database toolkit and ORM; used to build database connections and execute SQL from Python.
- `psycopg2-binary`
  - PostgreSQL driver used by SQLAlchemy to connect to the PostgreSQL instance running in Docker.

These packages together cover the needs of **Phase 02–05** (pandas/SQL workflows with PostgreSQL).

---

## 3. Supporting and Utility Packages (Recommended Must-Have)

These are not strictly required by the plan, but they are highly recommended to make development smoother and more professional.

- `pytest`
  - Testing framework to run and extend tests in `tests/`.
- `black` or `ruff`
  - Code formatting and/or linting tools (optional but useful for code quality).

For a minimal initial setup, you can treat `ipykernel` and `python-dotenv` as **must-have**, and `pytest`, `black`, `ruff` as **optional** (depending on how much you want to focus on testing and style inside the container).

---

## 4. Package Priority – Must-Have vs Optional

### 4.1 Must-have packages (Phase 01–04)

These should be installed in the first iteration of the Docker image because they are directly used by the CLI-driven pipeline:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `sqlalchemy`
- `psycopg2-binary`
- `python-dotenv`

### 4.2 Optional / later additions

These can be added once the basic environment is stable, or if you decide to extend the project:

- `pytest` – if you want to run tests from inside the container.
- `black` – automatic code formatting.
- `ruff` – fast linter and code quality checks.
- `typer` or `rich` – if you decide to build more sophisticated CLI interfaces later on.

Marking packages as **must-have** vs **optional** helps keep the initial image simpler and ensures you focus on the minimum needed for the early phases.

---

## 5. Example requirements.txt (for Docker image)

An example `requirements.txt` for the Docker image based on the above decisions could look like this:

```text
pandas
numpy
matplotlib
seaborn
sqlalchemy
psycopg2-binary
python-dotenv
# Optional tools (uncomment if needed)
# pytest
# black
# ruff
```

This list matches the committed `requirements.txt` in the repository and should be kept in sync as you add new CLI entry points.

---

## 6. How to reuse these requirements in other projects

For a similar data analytics project using Python, PostgreSQL, and terminal-driven scripts, you can:

1. Start from a modern base image like `python:3.11-slim`.
2. Include at least:
   - `pandas`, `numpy` for data manipulation.

- `matplotlib`, `seaborn` for visualizations.
- `sqlalchemy`, `psycopg2-binary` for database connectivity.
- `python-dotenv` for consistent environment handling across scripts.

3. Add testing and formatting tools as the project matures.

By defining these requirements **before** writing a Dockerfile, you make the next steps (Dockerfile authoring and Docker Compose design) much simpler and more deliberate.
