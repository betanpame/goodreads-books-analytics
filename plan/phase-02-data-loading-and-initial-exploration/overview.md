# Phase 02 – Data Loading and Initial Exploration

## Goal

Understand the structure of the Goodreads Books dataset and perform a **first-pass exploration** using both pandas and SQL. By the end of this phase you should be able to load the data into a pandas DataFrame, view basic summaries, and have a clear idea of how the data will be stored in PostgreSQL.

Some key concepts in this phase:

- **pandas DataFrame**: a table-like data structure in Python (rows and columns) that you can filter, aggregate, and visualize.
- **Schema (database schema)**: the design of your tables and columns in the database (for example, which columns go into which table and which data type each column uses).

## Inputs

- Phase 01 completed (environment and Docker/Python CLI workflow ready).
- `data/books.csv` available locally.
- (Optional but recommended) Access to a running PostgreSQL instance.

## Outputs / Deliverables

1. A **analysis script** that:
   - Loads `books.csv` into pandas.
   - Displays head/tail samples and basic info (`.info()`, `.describe()`).
   - Lists column names and data types.
2. A **draft schema design** for PostgreSQL (which columns map to which data types and tables).
3. A **loading strategy** for PostgreSQL:
   - Either using `COPY`/`psql` or using Python (`pandas.to_sql`, `sqlalchemy`).
4. (Optional) A first **SQL script** that creates the main table for books.

## Steps in This Phase

Detailed steps are under `steps/`:

1. **Step 1 – Inspect the Raw Dataset with pandas**  
   Folder: `steps/step-01-inspect-dataset-with-pandas/`

2. **Step 2 – Design PostgreSQL Table Structure**  
   Folder: `steps/step-02-design-postgres-schema/`

3. **Step 3 – Load Data into PostgreSQL**  
   Folder: `steps/step-03-load-data-into-postgres/`

Work through these steps linearly. It is better to start with pandas because it is very interactive, then move to database design and loading.

## Tips

- Focus on **understanding** the meaning of each column: what does it represent? how might it be used in analysis?
- Keep track of potential data issues you observe (missing values, strange codes, inconsistent formats). These will be explored more deeply in Phase 03. You can write these notes in `docs/dataset-notes.md`.
- Start simple for PostgreSQL: a single main table for books is enough at this stage. You can normalize later if needed.
