# Phase 02 – Step 01 – Task 01 – Create Initial EDA Analysis Script

This document records in detail everything that was done to complete **Phase 02 → Step 01 → Task 01 – Create Initial EDA Analysis Script** in the `goodreads-books-analytics` project. It is written as a **didactic, portfolio-ready guide** so that a beginner can follow it step by step and also see that the work is done at an expert level.

---

## 1. Task definition and goal

The planning file `plan/phase-02-data-loading-and-initial-exploration/steps/step-01-inspect-dataset-with-pandas/tasks/task-01-create-initial-eda-analysis script.md` defines this task as:

1. Start the Python CLI Docker container (prepared in Phase 01).
2. From your local editor (VS Code), open the project’s `src/analyses/` folder.
3. Create a new analysis script called `01_initial_inspection_books.py`.
4. Add introductory module docstring or Markdown notes explaining the purpose of the analysis script and what each row in `data/books.csv` represents.

The **objective** is to have a clean, well-structured analysis script that will serve as the **starting point** for exploratory data analysis (EDA) of the Goodreads Books dataset using pandas.

In this notes file we go beyond the minimal checklist and document:

- The **Docker + Python CLI workflow workflow** for this project.
- How the `src/analyses/` folder fits into the overall project structure.
- The design and content of `01_initial_inspection_books.py`.
- How to run it step by step, even as a beginner.

---

## 2. How to run this analysis script

Every Phase 02 → Step 01 task now shares the same three-command recipe so runs stay reproducible:

1. **Open the repository** (this also keeps VS Code in sync with the docker bind mount):

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
```

2. **Start or refresh the containers** so the Python CLI and Postgres services are ready:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up -d
```

3. **Run the scripted analysis** inside the Python container with the flags required for this phase:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Feel free to open an interactive shell via `docker compose ... exec app bash` if you want to re-run the script multiple times, but the three commands above are the canonical template that every future task note should re-use.

---

## 3. Environment and project context

Before working on the analysis script, it is important to understand the basic structure of this repository and how Docker is used.

### Key files and folders

Key items used in this task:

- `docker/python/Dockerfile` – defines a **Python CLI environment** with `pandas`, database libraries, and the tooling needed for script execution.
- `docker-compose.python.yml` – defines the `app` service (Python CLI) and a `postgres` service for the database.
- `docker-compose.postgresql.yml` – complementary file that configures the PostgreSQL database service.
- `data/books.csv` – the Goodreads Books dataset (CSV file) that we will explore.
- `src/analyses/` – folder where all Python CLI workflow analysis scripts for this project live.
- `src/` and `tests/` – Python modules and tests (used more heavily in later phases).

The Docker Compose configuration mounts the **entire project** into the container at `/app`, which is critical for making data, code, and analysis scripts visible both inside Docker and on the host.

### Starting the Docker-based Python CLI environment

From the project root on Windows (PowerShell), the stack is started with:

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics

docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up --build
```

What this does:

- **Builds** the Python image defined in `docker/python/Dockerfile` if needed.
- Starts an `app` container that mounts the entire repository and idles until you run a CLI command.
- Starts a `postgres` container for the database.
- Mounts the local project folder (`C:\Users\shady\documents\GITHUB\goodreads-books-analytics`) to `/app` inside the `app` container.

With this setup there is no browser-based interface. Instead, open a terminal (either on the host or via `docker compose exec app bash`) and run scripts directly with commands such as `python -m src.analyses.initial_inspection_books`.

---

## 4. Creating the `src/analyses/` folder and analysis script

### Ensure the `src/analyses/` folder exists

The project plan expects a top-level `src/analyses/` folder at the repository root. In this task, that folder is created (if missing) and used as the home for all analysis analysis scripts.

Reasons to centralize analysis scripts in `src/analyses/`:

- Keeps the root of the repository clean and organized.
- Makes it easy for collaborators (or recruiters) to find analysis analysis scripts.
- Mirrors common data-science project layouts.

### Create `01_initial_inspection_books.py`

Use your local editor (VS Code recommended) while the repository is mounted inside Docker:

1. In VS Code’s Explorer pane, expand `src/analyses/` (create the folder if it does not exist yet).
2. Add a new Python file named `01_initial_inspection_books.py`.
3. Save the file on the host; it will automatically appear inside the container at `/app/src/analyses/01_initial_inspection_books.py`.

The naming convention `01_...` is intentional:

- It groups analysis scripts by **sequence** (01, 02, 03...), which is easy to follow.
- The suffix `_initial_inspection_books` clearly states the analysis script’s purpose.

At this point the analysis script exists, but is still empty. The next steps focus on filling it with well-structured, educational content.

---

## 5. Designing the analysis script for a CLI workflow

`src/analyses/01_initial_inspection_books.py` is a **pure Python module** that can
be executed with `python -m src.analyses.initial_inspection_books`. Instead of
interacting with notebook cells, the script focuses on a predictable command-line
flow:

1. A module docstring explains the goal of the file and reiterates that it now
   replaces the former Jupyter notebook.
2. Reusable helper functions (logging configuration, environment verification,
   repository inspection, sample loading, CSV creation) keep the `main()`
   routine concise.
3. `argparse` exposes flags such as `--sample-size`, `--books-path`, and
   `--output-dir` so that the same script can be reused during later phases or
   automated runs.

The end result is a script that is easy to review in version control, simple to
run from any terminal, and free from UI-specific assumptions.

---

## 6. Section-by-section walkthrough of the analysis script

Below is a high-level description of what each major function in
`01_initial_inspection_books.py` does.

### Introduction and logging setup

The script starts by parsing CLI arguments and configuring logging via the
`configure_logging` helper. A `--verbose` flag switches the logger to DEBUG so
you can see additional directory listings or DataFrame previews when needed.

### Environment verification

`verify_environment()` prints the resolved project root, the Python version, and
the pandas version. This is the replacement for the old "run the first cell to
see package versions" workflow and quickly confirms that the container was
built with the right dependencies.

### Repository inspection

`inspect_repository()` iterates over the project root with `Path.iterdir()` and
logs each entry. Because the repo is mounted at `/app` inside the container, the
logged paths show the same structure you see in VS Code on the host. No shell
magics are required—everything is standard Python.

### Creating a didactic CSV example

`create_example_csv()` writes a tiny three-row dataset to
`data/example_people.csv` (unless it already exists). The function illustrates
how `pandas.DataFrame.to_csv()` works and is controlled by `--no-example` and
`--force-example` flags so that you can skip or recreate the file on demand.

### Loading a configurable sample of `books.csv`

`load_books_sample()` validates that `data/books.csv` exists, loads the desired
number of rows (default 1,000), and logs metadata about the resulting DataFrame.
If the file is missing you get an explicit error that explains how to fix the
data volume mount.

### Summaries and optional artifacts

`summarize_sample()` prints the head of the sample and overall descriptive
statistics. If `--output-dir` is provided (the default is
`outputs/initial_inspection`), the function writes both the sampled rows and the
numeric `.describe()` output to CSV so that downstream tasks can reuse them
without rerunning the script.

---

## 7. Verifying that `books.csv` can be read (sanity check)

In addition to running the analysis script, a small standalone Python snippet was executed in the project’s virtual environment to confirm that `data/books.csv` is present and readable:

```python
from pathlib import Path
import pandas as pd

books_path = Path("data") / "books.csv"
print("Exists:", books_path.exists())
if books_path.exists():
		df = pd.read_csv(books_path, nrows=5)
		print("Loaded shape:", df.shape)
		print(df.head())
```

Output (summarized):

- `Exists: True`.
- DataFrame shape `(5, 12)` with expected columns like `bookID`, `title`, `authors`, `average_rating`, `num_pages`, `ratings_count`, `text_reviews_count`, `publication_date`, and `publisher`.

This confirms that the dataset is available and correctly formatted for loading inside both the local environment and the Docker container.

---

## 8. Expected output checkpoints

When you rerun the script with the standard commands from Section 2, your log should include:

- Python `3.14.0` (or whatever version the container image reports) and pandas `2.3.3` confirmation lines.
- A repository listing under `/app` that calls out folders such as `data`, `docs`, `plan`, `src`, and `tests`.
- Either “Example CSV already exists…” or “Wrote example dataset…” so you know the helper file was touched.
- `Loaded shape: (rows=1000, columns=12)` plus the follow-up column list that surfaces the leading spaces in `"  num_pages"`.
- Summary-stat highlights like `Penguin Books` being the most common publisher and `Anna Karenina` appearing six times—handy checkpoints for later phases.

If any of those lines are missing, double-check that you passed `--sample-size 1000 --verbose` and that you are running inside the container.

---

## 9. Artifacts refreshed each run

Every execution touches a few files on disk:

- `data/example_people.csv` – tiny teaching dataset; deleted from git but regenerated or reused as needed.
- `outputs/initial_inspection/books_sample_preview.csv` – persisted version of `head()`; opens nicely in VS Code or Excel.
- `outputs/initial_inspection/books_numeric_summary.csv` – the numeric `.describe()` output for quick comparisons between runs.

Checking timestamps on those files is an easy sanity check if you are unsure whether the script actually completed.

---

## 10. How this completes Phase 02 → Step 01 → Task 01

Checklist from `task-01-create-initial-eda-analysis script.md`:

- [x] **The `src/analyses/` folder exists at the project root.**

  - The `src/analyses/` folder is present and used as the central location for Python CLI workflow analysis scripts.

- [x] **I have created `01_initial_inspection_books.py`.**

  - The analysis script file exists and is connected to the Docker-based Python kernel.

- [x] **The analysis script contains an introductory module docstring or Markdown note.**
  - The introduction clearly states the purpose, context, and main goals of the analysis script.

Additionally, the analysis script now goes **far beyond** the minimum checklist by including:

- A complete, didactic tour of Python CLI workflow analysis scripts, Docker integration, and pandas basics.
- A structured, initial inspection of the Goodreads `books.csv` dataset.
- Examples of selection, filtering, sorting, grouping, and saving results.

This makes it suitable not only for learning, but also as a **portfolio artifact** demonstrating good practices in data exploration.

---

## 11. Reusing this pattern in other projects

This task establishes a reusable pattern for future analytics projects:

1. **Create a dedicated `src/analyses/` folder** at the project root.
2. **Name analysis scripts with a clear sequence and purpose** (e.g., `01_initial_inspection_*.py`).
3. **Start with an introductory section** that explains the goal, context, and environment.
4. **Include environment checks** (library versions, data paths) near the top.
5. **Build up from tiny didactic examples** (toy CSV, small DataFrame) to the real dataset.
6. **Document key pandas patterns**: reading files, inspecting dtypes, selecting/filtering/sorting, handling missing values, grouping and aggregating, saving results.

By following this pattern, each new project gets:

- A beginner-friendly tutorial analysis script.
- A professional, portfolio-ready artifact that clearly demonstrates your approach to data exploration.

Use the same section order from this note (goal → how to run → environment/context → findings → expected outputs → artifacts → checklist) whenever you document future Phase 02 → Step 01 tasks so reviewers always know where to find information.

---

## 12. Run log reference (Dec 3, 2025)

To make the workflow concrete, I ran the script inside the Docker container using the persistent-shell approach:

```powershell
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml up --build -d
docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml exec app bash
python -m src.analyses.initial_inspection_books --sample-size 1000 --verbose
```

Key takeaways (useful for beginners verifying their own run):

- **Environment sanity check**: The log printed Python `3.14.0` and pandas `2.3.3`, proving the container image is configured correctly.
- **Repository listing**: Seeing folders such as `data`, `docs`, `plan`, `src`, and `tests` under `/app` confirms the bind mount is working.
- **Example CSV**: If `data/example_people.csv` already exists, the script reuses it. Otherwise, it creates it and shows a tiny preview so you know file writes succeed.
- **Dataset load**: Reading the first 1,000 rows of `data/books.csv` produced a `(1000, 12)` DataFrame. The column list revealed a leading space in `"  num_pages"`, which we should trim during cleaning.
- **Summary statistics**: `title` appears six times for "Anna Karenina" in this sample, and `Penguin Books` is the most frequent publisher (39 occurrences). These facts are helpful checkpoints for future phases.
- **Output artifacts**: Two CSVs now exist on the host at `outputs/initial_inspection/`—`books_sample_preview.csv` (sample rows) and `books_numeric_summary.csv` (numeric describe). Open them in VS Code to double-check they match the CLI logs. I inspected them directly:
  - `books_sample_preview.csv` begins with the Harry Potter entries shown in the log (IDs 1, 2, 4, 5, 8...), confirming the sample rows were written correctly.
  - `books_numeric_summary.csv` reports aggregates such as `mean ratings_count = 40284.314` and `max text_reviews_count = 55843`, matching the console summary.

If your logs look different, verify the command sequence above, make sure you are inside the container shell when running `python -m ...`, and confirm that `data/books.csv` exists on the host before rerunning.

---

## 13. Q&A / Data troubleshooting

**Where does this script live?** – `src/analyses/initial_inspection_books.py`. Run it with `python -m src.analyses.initial_inspection_books` from inside the container so Python resolves the package correctly.

**How do I confirm the dataset is available before running anything?** – From the repo root (host or container), run `ls data` or `dir data` and make sure `books.csv` is present. Inside Python you can also run the sanity snippet from Section 7.

**The script says it cannot find `books.csv`. What now?** – Ensure you executed `docker compose ... up -d` from the project root so the bind mount includes the `data/` folder. If the file is actually missing, re-download it per `docs/dataset-notes.md` or copy it from `data/books.csv` in the repo history.

**Where do I inspect the saved sample without rerunning the CLI?** – Open `outputs/initial_inspection/books_sample_preview.csv` for row-level checks or `books_numeric_summary.csv` for the numeric stats. Both files refresh every run.

**How do I know which Python/pandas versions were used later on?** – The top of every run logs those versions; if you forgot to save the terminal output, re-run the script with `--verbose`. The environment is defined in `docker/python/Dockerfile`.

For broader dataset questions, see `docs/data-faq.md`, which tracks recurring issues and where to find the right source files.

---

This completes **Phase 02 → Step 01 → Task 01 – Create Initial EDA Analysis Script**.
