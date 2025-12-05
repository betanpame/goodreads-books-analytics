# Phase 01 – Step 01 – Task 03 Notes

This document explains, in a step-by-step and reusable way, how **Task 03 – Verify Tools Installation** was completed for the `goodreads-books-analytics` project. You can follow the same procedure in any future data analytics project.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-01-understand-repo-and-tools/tasks/task-03-verify-tools-installation.md`.

---

## 1. Goal of Task 03

Before investing time in Docker configuration, database setup, and Python pipelines, you want to make sure your **core tools are correctly installed and accessible** from the terminal.

The task focuses on verifying:

1. **Git** – version control.
2. **VS Code** (or another editor) – already in use.
3. **Docker Desktop** – container runtime.
4. **Python 3.x** – local Python interpreter.
5. **PostgreSQL in Docker** – the database container defined in `docker-compose.postgresql.yml`.

The outcome should be:

- A simple checklist that says which tools are working.
- Notes on any issues (none in this case), so you know what to fix.
- Confidence that you can proceed to Docker and environment configuration.

---

## 2. Where to run the checks

All checks were run from the **project root** in a **PowerShell** terminal on Windows.

To open a terminal in VS Code already positioned at the project root:

1. Open the repository folder in VS Code.
2. Go to **Terminal → New Terminal**.
3. Confirm the prompt path looks similar to:

```powershell
PS C:\Users\shady\documents\GITHUB\goodreads-books-analytics>
```

If not, you can navigate there with:

```powershell
Set-Location "C:\Users\shady\documents\GITHUB\goodreads-books-analytics"
```

---

## 3. Verifying Git installation

**Why this matters**: Git tracks changes, lets you push to GitHub, and shows a clear history of your work.

**Command used**:

```powershell
git --version
```

**Observed output** (on your machine):

```text
git version 2.51.2.windows.1
```

**How to interpret this**:

- Seeing a version string means **Git is installed and on `PATH`**.
- If you saw an error like `git : The term 'git' is not recognized`, that would mean Git is missing or not added to `PATH`.

**What to do in other projects**:

- Always run `git --version` once when you start working on a new machine.
- If it fails, install Git from the official website and retry.

---

## 4. Verifying Docker installation

**Why this matters**: Docker is how you will run PostgreSQL (and later, possibly a Python CLI container) in an isolated, reproducible way.

**Command used**:

```powershell
docker --version
```

**Observed output**:

```text
Docker version 28.4.0, build d8eb465
```

**How to interpret this**:

- A version string means the Docker CLI is installed and available.
- It does **not** guarantee Docker Desktop is currently running, but it is a good first sanity check.

To further confirm Docker Desktop is running, you can also run:

```powershell
docker info
```

If Docker is not running, this command would typically fail or hang with a message indicating it cannot connect to the Docker daemon.

---

## 5. Verifying Python 3.x installation

**Why this matters**: Even though the project will use Docker, having a working local Python 3 helps with quick tests, scripts, and virtual environments.

**Command used**:

```powershell
python --version
```

**Observed output**:

```text
Python 3.13.9
```

**How to interpret this**:

- Python 3 is installed and available on `PATH`.
- The exact version (3.13.9 here) is modern enough for this project.

If the command failed or showed Python 2, you would:

- Install Python 3 from python.org or the Windows Store.
- Ensure the installer option "Add Python to PATH" is checked.

---

## 6. Verifying PostgreSQL in Docker (via Docker Compose)

**Why this matters**: This project expects PostgreSQL to run in a Docker container defined by `docker-compose.postgresql.yml`. Verifying that the container starts and is reachable is a critical prerequisite.

### 6.1. Checking the PostgreSQL service status

From the project root:

```powershell
docker compose -f docker-compose.postgresql.yml ps
```

**Observed output** (formatted here for clarity):

```text
NAME                                 IMAGE         COMMAND                  SERVICE   CREATED       STATUS     PORTS
goodreads_books_analytics_postgres   postgres:17   "docker-entrypoint.s…"   postgres  2 hours ago   Up 2 hours 0.0.0.0:5491->5432/tcp, [::]:5491->5432/tcp
```

**How to interpret this**:

- The service name is `postgres` and it uses image `postgres:17`.
- `STATUS` is `Up`, which means the container is running.
- The host port `5491` is mapped to the container’s internal port `5432`.
- This matches your earlier note that PostgreSQL is running on **port 5491** on the host.

### 6.2. Knowing how to start and stop PostgreSQL

To start the PostgreSQL container if it is not already running:

```powershell
docker compose -f docker-compose.postgresql.yml up -d
```

To see its status:

```powershell
docker compose -f docker-compose.postgresql.yml ps
```

To stop the container (but keep the data volume):

```powershell
docker compose -f docker-compose.postgresql.yml down
```

To stop the container **and delete the volume/data** (use with care):

```powershell
docker compose -f docker-compose.postgresql.yml down -v
```

Knowing these commands satisfies the checklist item: _"I know how to start and stop my PostgreSQL Docker container."_

---

## 7. Recording results in `docs/repo-notes.md`

As part of Task 03, a new section was appended to `docs/repo-notes.md` titled **"Tooling – Installation and Status (Phase 01 Step 01 Task 03)"**, summarizing:

- The exact commands used:
  - `git --version`
  - `docker --version`
  - `python --version`
  - `docker compose -f docker-compose.postgresql.yml ps`
- The concrete outputs observed (Git version, Docker version, Python version).
- Confirmation that the PostgreSQL container `goodreads_books_analytics_postgres` is running on port `5491`.

This turns `repo-notes.md` into a single place where your environment status is documented, which is helpful for debugging or re-creating the setup on another machine.

---

## 8. Mapping back to the Task 03 checklist

From the planning document:

- [x] **Git is installed and accessible from the terminal.**  
       Verified with `git --version` → `git version 2.51.2.windows.1`.

- [x] **Docker Desktop is installed and running.**  
       Verified with `docker --version` and `docker compose ... ps` showing an active container.

- [x] **Python 3.x is installed (optional but recommended).**  
       Verified with `python --version` → `Python 3.13.9`.

- [x] **I know how to start and stop my PostgreSQL Docker container.**  
       Commands documented: `docker compose -f docker-compose.postgresql.yml up -d`, `ps`, `down`, and `down -v`.

- [x] **I have noted any installation or configuration issues in `docs/repo-notes.md`.**  
       No issues found; instead, the successful configuration has been recorded in the new "Tooling" section.

This means **Phase 01 → Step 01 → Task 03** is fully completed.

---

## 9. How to reuse this verification pattern

When starting any new analytics project, you can copy this pattern:

1. **Open a terminal at the project root.**
2. **Check Git:** `git --version`.
3. **Check Docker:** `docker --version` and optionally `docker info`.
4. **Check Python:** `python --version` (and confirm it is Python 3).
5. **Check database container (if used):**
   - Use the relevant `docker compose -f ... ps` command.
   - Learn the service name, image, status, and port mappings.
6. **Write a short summary** in a notes file (like `docs/repo-notes.md` or a dedicated `task-XX-notes.md`).

This habit ensures that your **toolchain is healthy** before you dive into coding and makes your projects easier for others to reproduce.

---

## 10. Data hygiene note – Publication dates (Dec 2025)

- `src/cleaning.py` now parses publication dates in ordered passes: `MM/DD/YY`, ISO `YYYY-MM-DD`, textual months (e.g., `Sep 1998` / `September 1998`), and bare years. Each fallback normalizes to the first day of the available period (month or year) before a final `pd.to_datetime(..., errors="coerce")` catch-all.
- The new behavior is covered by unit tests in `tests/test_cleaning.py` so future regressions surface quickly.
- When the raw Kaggle export contains malformed CSV rows (unescaped commas inside `authors`), `python -m src.run_full_pipeline` now normalizes the file on the fly (see `src/raw_ingestion.py`) and logs how many rows were repaired before pandas touches the data. Nothing is silently dropped anymore.
- If you ingest refreshed CSVs later, scan `data/books.csv` again for new date patterns and extend `PREFERRED_DATE_FORMATS` as needed—only a single tuple controls the supported formats.

---

## 11. Database schema safeguards (Dec 2025)

- After loading data into PostgreSQL, the pipeline now calls `ensure_books_clean_schema` (see `src/schema.py`) to add a primary key on `book_id` plus three analytics-friendly indexes (`publication_date`, `average_rating`, `authors`).
- A dedicated smoke test `tests/test_postgres_smoke.py` connects to the database (using `DATABASE_URL` or the `POSTGRES_*` variables) and fails CI if the table disappears, row counts drop to zero, the PK is missing, or any of the indexes are absent.
- Run `python -m dotenv run -- python -m pytest tests/test_postgres_smoke.py` whenever you need to validate a fresh environment before running analytical queries.
