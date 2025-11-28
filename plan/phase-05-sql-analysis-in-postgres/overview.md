# Phase 05 – SQL Analysis in PostgreSQL

## Goal

Reproduce and extend key analyses using **SQL in PostgreSQL**. This phase helps you build SQL skills and see how database queries can complement or replace pandas-based analysis.

In this phase you will focus on:

- Writing **SQL queries** to answer analytical questions.
- Understanding how results from SQL relate to the results you already obtained with pandas.
- Getting more comfortable working directly with a relational database.

## Inputs

- Phases 02–04 completed or partially completed:
  - Data loaded into PostgreSQL.
  - Some business questions already explored with pandas.
- Working connection from Python/Jupyter to PostgreSQL (from Phase 01).

## Outputs / Deliverables

1. A set of **SQL scripts** (e.g., under `sql/`) that:
   - Create necessary tables (if not already done).
   - Run analytical queries answering key questions.
   - Include comments explaining what each query does.
2. A **comparison notebook** (optional but recommended) that:
   - Runs SQL queries from Python using `sqlalchemy` or similar.
   - Compares results from SQL and pandas for the same questions.
3. Comfort with basic to intermediate SQL patterns:
   - Aggregations (`GROUP BY`, `ORDER BY`).
   - Filtering (`WHERE`, `HAVING`).
   - Simple joins.
   - Basic window functions (optional/bonus).

## Steps in This Phase

Detailed steps are under `steps/`:

1. **Step 1 – Validate Data in PostgreSQL**  
   Folder: `steps/step-01-validate-data-in-postgres/`

2. **Step 2 – Implement Core Analysis Queries**  
   Folder: `steps/step-02-implement-analysis-queries/`

3. **Step 3 – Optional: SQL vs pandas Comparison**  
   Folder: `steps/step-03-sql-vs-pandas-comparison/`

## Tips

- Start by translating your favorite pandas analyses into SQL. This creates a direct mental bridge between the two worlds.
- Save your queries in `.sql` files, not only in notebooks. This is more professional and reusable.
- Use comments generously in SQL scripts, especially while learning.
- If you are new to SQL, keep a small "cheat sheet" in `docs/` (for example, common `SELECT`, `WHERE`, and `GROUP BY` patterns) and update it as you learn.
