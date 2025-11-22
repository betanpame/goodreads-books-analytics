# Task 02 – Load Data from CSV to PostgreSQL

## Objective

Load all rows from `books.csv` into the `books` table in PostgreSQL using a repeatable method.

## Instructions

1. Choose a loading approach:
   - **Option A – SQL COPY**: Use `COPY` or `\copy` from `psql` to load the CSV directly.
   - **Option B – Python**: Use a notebook or script with `pandas` and `sqlalchemy` to insert data.
2. Document your chosen approach in a markdown file or in your notebook.
3. Implement the loading process:
   - For `COPY`: write a SQL script (e.g., `sql/load_books_from_csv.sql`).
   - For Python: write a small script or notebook section that reads the CSV and writes to PostgreSQL.
4. Run the process and monitor for errors (e.g., encoding issues, date parsing).
5. Adjust your schema or parsing logic if necessary.

## Checklist

- [ ] I have chosen a loading method (SQL `COPY` or Python).
- [ ] I have implemented the loading process in a script or notebook.
- [ ] I have successfully loaded the data into PostgreSQL.

## Result

The `books` table in PostgreSQL now contains data from `books.csv` and can be queried.
