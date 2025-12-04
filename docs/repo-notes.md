# Repository Notes – Project Structure Overview

This file collects concise notes about the current structure of the `goodreads-books-analytics` repository. It is meant to be a living document that you can update as the project evolves.

## Top-level Items

- `.env` / `.env.example`: Environment variable files used to configure PostgreSQL and other settings (database name, user, password, ports, etc.). `.env.example` is a template; `.env` is your local copy that should not be committed with secrets.
- `.git/` and `.gitignore`: Git metadata folder and ignore rules. Git tracks changes to the project so you can create a clean, documented history across phases.
- `LICENSE`: License file for the project. It specifies how others may use or share this repository.
- `README.md`: Main entry point for the project. It currently explains the goal (Goodreads books analytics), prerequisites, Docker/PostgreSQL usage, and how to run the data pipeline.
- `docker-compose.postgresql.yml`: Docker Compose definition for a PostgreSQL database container. It is used to quickly spin up and manage the Postgres environment required by the project.

## Data and Code

- `data/`:

  - **Purpose**: Stores the main dataset files used in the project.
  - **Current contents**: `books.csv` with book-level information (IDs, titles, authors, ratings, ISBNs, language, number of pages, ratings/reviews counts, publication date, publisher).
  - **Future use**: Keep raw data (like the original Goodreads CSV) and possibly derived/cleaned versions (e.g., `books_clean.csv`). Avoid mixing raw data with outputs from analysis (those can go in another folder such as `outputs/` or `src/analyses/`).

- `src/`:

  - **Purpose**: Python source code for the data pipeline and helpers.
  - **Current contents** (high level): scripts to clean the data, check data quality, load books into PostgreSQL, and run the full pipeline.
  - **Future use**: As the project grows, this folder can include reusable Python modules that are imported from analysis scripts or CLI entry points (for example, functions for cleaning, quality checks, and metrics).

- `tests/`:
  - **Purpose**: Automated tests for the Python code in `src/`.
  - **Current contents**: at least one test file (`test_cleaning.py`) that verifies data cleaning behavior.
  - **Future use**: Add more tests as the pipeline becomes more complex (e.g., tests for schema expectations, data validation rules, or SQL-related utilities).

## Planning and Documentation

- `plan/`:

  - **Purpose**: Detailed project plan organized by **phase → step → task**. It guides the work from environment setup, through EDA and analysis, to documentation and production readiness.
  - **Structure**: Each phase (e.g., `phase-01-project-setup-and-environment/`) has its own `overview.md` plus `steps/` subfolders. Each step contains an `overview.md` and a `tasks/` folder with task-level markdown files.
  - **Future use**: Use this folder as your roadmap. As you complete tasks, you can add brief notes or links to the actual artifacts created (analysis scripts, SQL files, Docker configs).

- `docs/`:
  - **Purpose**: Supporting documentation and learning resources for tools and concepts used in the project.
  - **Current contents**: notes about the dataset, pandas, SQL, Docker, and PostgreSQL, plus this `repo-notes.md` file.
  - **Future use**: Add how‑to guides (for example, “How to run the full pipeline with Docker”, “How to connect to PostgreSQL from a local SQL client”), design decisions, and any extra explanations that help future you or portfolio reviewers understand the project.

## Dataset – Quick First Impression

From the first ~50 rows of `data/books.csv`, the main columns appear to be:

- `bookID`: Numeric identifier for each book.
- `title`: Full book title (often including series information).
- `authors`: One or more authors separated by `/`.
- `average_rating`: Average user rating on Goodreads (e.g., 4.57).
- `isbn` / `isbn13`: Book identifiers in 10‑ and 13‑digit formats.
- `language_code`: Short language code (e.g., `eng`, `en-US`, `fre`).
- `num_pages`: Number of pages.
- `ratings_count`: Total number of ratings.
- `text_reviews_count`: Total number of text reviews.
- `publication_date`: Date string (month/day/year).
- `publisher`: Publisher name.

This quick review confirms that the dataset is rich enough for questions about ratings, popularity (ratings/reviews counts), languages, publishers, and time trends.

## Tooling – Installation and Status (Phase 01 Step 01 Task 03)

Basic toolchain checks performed from the project root in PowerShell:

- Git:

  - Command: `git --version`
  - Result: `git version 2.51.2.windows.1` → Git is installed and available on `PATH`.

- Docker:

  - Command: `docker --version`
  - Result: `Docker version 28.4.0, build d8eb465` → Docker CLI is installed and working.

- Python:

  - Command: `python --version`
  - Result: `Python 3.13.9` → A recent Python 3.x interpreter is installed and available on `PATH`.

- PostgreSQL in Docker (via Docker Compose):
  - Command: `docker compose -f docker-compose.postgresql.yml ps`
  - Result: shows service `postgres` running from image `postgres:17` and mapped to host port `5491`.
  - Interpretation: Docker Compose works, and the PostgreSQL container `goodreads_books_analytics_postgres` is up and reachable on `localhost:5491`.

These checks confirm that Git, Docker, Python, and the PostgreSQL Docker container are all correctly installed and running, which satisfies the goals of Task 03 (verify tools installation).
