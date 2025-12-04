# Phase 01 – Step 02 – Task 01 Notes

This document explains, in a learning-focused way, how **Task 01 – Define Python Environment Requirements** was completed for the `goodreads-books-analytics` project. You can reuse the same approach when designing a Docker-based Python environment for other analytics projects.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-02-design-python-docker-environment/tasks/task-01-define-python-environment-requirements.md`.

---

## 1. Goal of this task

Before writing a Dockerfile for the Python CLI environment, you should clearly define:

- Which **Python base image** you will use.
- Which **Python packages** are required for the project.
- Which packages are **must-have now** (for early phases) vs **optional** (for later improvements).

Having this written down helps you:

- Avoid forgetting important libraries when you write the Dockerfile.
- Keep the initial environment focused and not overloaded.
- Communicate your environment design clearly in your portfolio.

---

## 2. Creating a dedicated requirements notes file

The task suggests creating a new markdown file for environment notes (for example, `docker/python-requirements-notes.md`).

In this project, that file was created at:

- `docker/python-requirements-notes.md`

This file acts as a **design document** for the Python environment inside Docker. Later tasks (Dockerfile authoring and Docker Compose design) will refer back to it.

You can adopt the same pattern in other projects by keeping environment design notes under a `docker/` or `infra/` folder.

---

## 3. Choosing a base Python image

The first design decision is the **base image** for the Docker environment.

For this project, the chosen base image is:

- `python:3.14-slim`

Reasons for this choice:

- `3.14` is a current, stable version of Python 3 at the time of writing and is available as an official Docker image.
- The `-slim` variant keeps the image smaller than the full Debian-based image, while still being able to install dependencies needed by packages like `psycopg2-binary` and scientific libraries.

In a future iteration, you could choose a newer slim tag (for example, `python:3.15-slim` when it becomes stable) or pin a minor version more strictly (e.g., `python:3.14.x-slim`) for extra reproducibility.

---

## 4. Listing must-have Python packages

Next, we identify the **core libraries** required by the project, especially for Phases 02–04 (data loading, EDA, and visualization) and Phase 05 (SQL + pandas combination).

The following were marked as **must-have**:

### 4.1 Data manipulation and analysis

- `pandas` – Primary library for working with tabular datasets (reading CSV, grouping, aggregations).
- `numpy` – Numerical computing backbone, used directly and via pandas.

### 4.2 Visualization

- `matplotlib` – Core plotting library for detailed control over figures.
- `seaborn` – Higher-level statistical visualization library that simplifies many common plot types.

### 4.3 CLI workflow and environment handling

- `python-dotenv` – Makes it easy to load configuration from `.env` files into Python (mirroring how Docker Compose uses `.env`).

### 4.4 Database connectivity

- `sqlalchemy` – Database toolkit and ORM; recommended way to manage PostgreSQL connections and SQL from Python.
- `psycopg2-binary` – PostgreSQL driver used by SQLAlchemy.

These libraries cover the key capabilities the project needs:

- Read and transform `books.csv`.
- Create visualizations for EDA and insights.
- Connect to PostgreSQL in Docker.
- Work interactively in VS Code + terminal workflow.

---

## 5. Marking optional packages for later

To keep the initial environment lean, some tools are marked as **optional / later**. They are useful but not strictly required to start Phases 02–04.

Examples of optional packages:

- `pytest` – For running tests inside the container.
- `black` – Automatic code formatter.
- `ruff` – Very fast linter and code-quality tool.
- `typer` or `rich` – Useful if you want more advanced CLI ergonomics.

These can be added after the core environment is stable, or if you want to showcase testing and code-quality practices in your portfolio.

---

## 6. Example requirements list for Docker

To make things concrete, the notes file `docker/python-requirements-notes.md` includes an example set of requirements that could be copied into a future `requirements.txt`:

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

This is **not** yet a final `requirements.txt` used by a Dockerfile in this repository, but it serves as a ready-to-use template for the next task.

---

## 7. Mapping back to the Task 01 checklist

From the planning document:

- [x] **I have a written list of required Python packages.**  
       → The list is written and explained in `docker/python-requirements-notes.md`.

- [x] **I have distinguished between must-have and optional packages.**  
       → Sections 2 and 4 of `python-requirements-notes.md` clearly label must-have vs optional.

- [x] **I have chosen a base Python image for the Dockerfile.**  
       → The base image `python:3.11-slim` is documented with rationale.

Therefore, **Phase 01 → Step 02 → Task 01** is fully completed.

---

## 8. How to reuse this design process in other projects

When you design a Python Docker environment for another data project, you can:

1. **Create a small design doc** (like `docker/python-requirements-notes.md`):
   - List your must-have libraries (pandas, numpy, plotting, DB drivers, CLI helpers).
   - Mark optional tools (tests, linters, extras).
   - Choose a specific base image (e.g., `python:3.11-slim`).
2. **Keep the first version minimal**:
   - Focus on what you need for the first 1–2 phases of work.
   - Add extras only when you know you will use them.
3. **Use the notes to drive your Dockerfile**:
   - When you write the Dockerfile, simply translate the design doc into `FROM python:3.11-slim` and `pip install` using a `requirements.txt` based on the lists you defined.

Documenting this design up front makes your environment decisions **explicit**, which is valuable both for collaborators and for showcasing your work in a portfolio.
