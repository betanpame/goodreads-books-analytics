# Phase 01 – Step 01 – Task 01 Notes

This document records in detail everything that was done to complete **Phase 01 → Step 01 → Task 01 – Review Repository Structure** in the `goodreads-books-analytics` project. It is written as a learning reference so you can reuse the same process in future projects.

---

## 1. High-level plan for Task 01

The task description in `plan/phase-01-project-setup-and-environment/steps/step-01-understand-repo-and-tools/tasks/task-01-review-repository-structure.md` asks you to:

1. Open the repository in VS Code.
2. Explore the top-level folders and files (`data/`, `docs/`, `plan/`, `README.md`, etc.).
3. Write notes in a markdown file (`docs/repo-notes.md`) describing what each folder is for and what you expect to store there.
4. Inspect the first ~30–50 lines of `data/books.csv` to get an initial feel for the dataset.

The objectives of this document are:

- To explain **how** those tasks were completed.
- To give you a **step-by-step template** that you can follow in similar analytics projects.
- To keep everything in **clear English**, ready for your portfolio.

---

## 2. Reviewing the repository structure

### 2.1. Opening the repository in VS Code

To open the project in VS Code on Windows using PowerShell:

```powershell
code C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics
```

What this does:

- Launches VS Code (if it is not already open).
- Opens the `goodreads-books-analytics` folder as the **workspace root**.

Once VS Code is open:

- Use the **Explorer** sidebar (usually on the left) to see all top-level folders and files.
- Confirm that you can expand folders like `data/`, `docs/`, `plan/`, `src/`, and `tests/`.

### 2.2. Scanning top-level items

At the root of the repository, the main items are:

- `.env` / `.env.example`
- `.git/` and `.gitignore`
- `data/`
- `docs/`
- `plan/`
- `src/`
- `tests/`
- `docker-compose.postgresql.yml`
- `LICENSE`
- `README.md`

The goal in this step is **not** to read every file in detail. Instead, you want a **mental map**:

- Where is the data?
- Where is the code?
- Where are the tests?
- Where are the docs and the plan?
- How is the database environment defined?

This quick scan is a habit you can repeat whenever you start exploring a new repository.

---

## 3. Inspecting `data/books.csv`

Task 01 asks you to inspect the first 30–50 lines of `data/books.csv` to get a feel for the dataset.

### 3.1. Opening the CSV in VS Code

Steps you can follow:

1. In the VS Code Explorer, expand the `data/` folder.
2. Click on `books.csv`.
3. VS Code will open the file in a tab. Depending on your extensions, you may see:
   - Plain text with comma-separated values, or
   - A table-like view if you have a CSV viewer extension installed.
4. Scroll just a little to review the header and the first several rows.

If you prefer to use Excel or another spreadsheet tool:

```powershell
start excel "C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics\data\books.csv"
```

(You can replace `excel` with another program if needed.)

### 3.2. What you see in the first rows

From the first ~50 rows of `books.csv`, you can observe that the header includes columns such as:

- `bookID`
- `title`
- `authors`
- `average_rating`
- `isbn`
- `isbn13`
- `language_code`
- `num_pages`
- `ratings_count`
- `text_reviews_count`
- `publication_date`
- `publisher`

Basic intuition about the data types:

- `bookID`: integer identifier for each book.
- `title`: string (book title, sometimes with series information).
- `authors`: string (one or more authors separated by `/`).
- `average_rating`: float value around 0–5.
- `isbn`, `isbn13`: strings representing 10- and 13-digit identifiers.
- `language_code`: short code like `eng`, `en-US`, `fre`.
- `num_pages`: integer number of pages.
- `ratings_count`, `text_reviews_count`: integers that measure popularity/engagement.
- `publication_date`: string with a month/day/year format (to be parsed later).
- `publisher`: string with the publisher name.

This quick look already suggests potential analysis directions:

- Highly rated books (`average_rating`).
- Popularity based on `ratings_count` and `text_reviews_count`.
- Differences between languages or publishers.
- Trends over time based on `publication_date`.

The goal at this stage is **not** to perform full EDA, but simply to confirm that the data is rich and understandable.

---

## 4. Updating `docs/repo-notes.md` with repository structure notes

Task 01 also asks you to describe what each top-level folder is for and what you expect to store there later.

### 4.1. Editing `docs/repo-notes.md`

The file `docs/repo-notes.md` originally contained only a few prompts. It was updated to include concrete descriptions of the repository structure and a quick summary of the dataset.

Conceptually, the updated file now has these sections:

1. **Top-level Items** – describes `.env`, `.env.example`, `.git/`, `.gitignore`, `LICENSE`, `README.md`, and `docker-compose.postgresql.yml`.
2. **Data and Code** – explains the purpose of `data/`, `src/`, and `tests/`.
3. **Planning and Documentation** – documents what `plan/` and `docs/` are used for.
4. **Dataset – Quick First Impression** – summarizes the main columns and what they represent.

### 4.2. Meanings of each top-level folder/file

Here is the meaning of each important item:

- `.env` / `.env.example`:

  - **Purpose**: Store environment variables (e.g., PostgreSQL database name, user, password, host, port).
  - `.env.example` is a template you commit to the repo. `.env` is your local copy with real values and should usually be ignored by Git.

- `.git/` and `.gitignore`:

  - `.git/` is the internal folder where Git keeps its metadata (commits, branches, etc.).
  - `.gitignore` lists files and folders that Git should not track (for example, `.env`, `.venv/`, build artifacts).

- `LICENSE`:

  - Contains the license text for the repository, describing how others can use, modify, and share your project.

- `README.md`:

  - The main landing page of the project.
  - Describes the goal (Goodreads books analytics), technologies (Python, PostgreSQL, Docker), prerequisites, and basic run instructions.

- `docker-compose.postgresql.yml`:

  - Defines how to run a PostgreSQL database in Docker using Docker Compose.
  - Reads configuration values (such as `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`) from the `.env` file.

- `data/`:

  - Holds the main dataset(s), currently `books.csv`.
  - In more advanced setups, you might add subfolders like `raw/`, `processed/`, and `external/` to separate different data stages.

- `docs/`:

  - Stores supporting documentation: dataset notes, tool cheat sheets, Docker/PostgreSQL intros, and repository notes.
  - This file (`phase-01-step-01-task-01-notes.md`) lives here as a detailed record for this task.

- `plan/`:

  - Contains the full phase → step → task project plan.
  - Helps you work systematically from environment setup to final documentation.

- `src/`:

  - Contains Python code such as `cleaning.py`, `check_data_quality.py`, `load_books_to_postgres.py`, and `run_full_pipeline.py`.
  - The goal is to keep logic reusable: analysis scripts and scripts can import functions from here.

- `tests/`:
  - Contains tests (like `test_cleaning.py`) that verify key functions in `src/`.
  - Helps you ensure that changes to cleaning or loading logic are safe.

---

## 5. Creating a polished structure document in `docs/`

In addition to updating `repo-notes.md`, a new portfolio-ready document was created: `docs/project-structure-overview.md`.

### 5.1. Purpose of `project-structure-overview.md`

- Provide a **clean, narrative explanation** of the repository for people viewing your portfolio.
- Explain the roles of `data/`, `src/`, `tests/`, `docs/`, `plan/`, `docker-compose.postgresql.yml`, `README.md`, and `LICENSE`.
- Show that you understand how to design a clear and professional project layout.

### 5.2. Main ideas captured in that document

The document is organized into sections that:

1. Summarize the **high-level repository map**.
2. Explain the **data folder** and how to treat raw vs processed data.
3. Describe the **source code** organization in `src/`.
4. Emphasize the importance of **tests** in `tests/`.
5. Show how `plan/` organizes work into phases, steps, and tasks.
6. List the contents and role of `docs/`.
7. Describe the PostgreSQL Docker setup via `docker-compose.postgresql.yml` and `.env`.
8. Clarify the roles of `README.md` and `LICENSE`.
9. Provide guidance on **how to apply this structure to your own projects**.

You can think of `project-structure-overview.md` as a document you would proudly point to when showcasing this repository in your CV or portfolio.

---

## 6. How this completes Task 01

Task 01 checklist from the planning file:

- [x] **I have opened the repository in VS Code.**  
      → Documented how to open the repo with `code` from PowerShell.

- [x] **I have reviewed all top-level folders and files.**  
      → Listed and explained all important top-level items.

- [x] **I have written short notes describing the purpose of each folder in `docs/repo-notes.md`.**  
      → Updated `repo-notes.md` with concrete descriptions for each folder and file.

- [x] **I have briefly inspected `data/books.csv` (in VS Code or a spreadsheet tool).**  
      → Read the first rows, identified columns, and recorded a quick first impression.

With these steps completed and documented, **Phase 01 → Step 01 → Task 01** is fully done.

---

## 7. How to reuse this process in other projects

When you start a new analytics project, you can follow a similar pattern:

1. **Open the repository in your editor** and quickly scan the structure.
2. **Identify top-level concerns**: data, code, tests, docs, infra (Docker), and planning.
3. **Create a `docs/repo-notes.md`** to capture your understanding of the structure.
4. **Briefly inspect your main dataset** to understand columns and basic data types.
5. **Optionally create a polished structure doc** (like `project-structure-overview.md`) for portfolio use.

By doing this early, you:

- Reduce confusion later in the project.
- Build a habit of documenting your work.
- Make your projects easier for others (and future you) to understand.
