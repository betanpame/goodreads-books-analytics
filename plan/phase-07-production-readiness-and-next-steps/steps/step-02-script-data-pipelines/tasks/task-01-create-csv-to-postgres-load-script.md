## Task 01 – Create CSV to PostgreSQL Load Script

### Objective

Implement a **reusable Python script** that loads `data/books.csv` into a PostgreSQL table in a consistent way.

### Outputs

- A script such as `src/load_books_to_postgres.py` with a simple CLI.

### Steps

1. **Decide script location and name**

   - Create a `src/` folder if it does not exist.
   - Plan a script name like `load_books_to_postgres.py`.

2. **Set up configuration handling**

   - Decide how the script will read database connection info:
     - Option A: environment variables (e.g., `DATABASE_URL`).
     - Option B: a configuration file (e.g., `.env` or `config.yaml`).

3. **Implement basic script structure**

   - Import `pandas` and `sqlalchemy` (or preferred DB library).
   - Parse command-line arguments (e.g., input CSV path, table name, if-exists behavior) using `argparse`.

4. **Load CSV and write to PostgreSQL**

   - Read `data/books.csv` into a DataFrame.
   - Use SQLAlchemy engine or connection string to connect to PostgreSQL.
   - Use `DataFrame.to_sql` or a bulk-load method to write into a `books_raw` or `books` table.

5. **Add minimal logging and error handling**

   - Print what the script is doing (rows loaded, target table, etc.).
   - Catch common errors (e.g., connection failures) and print helpful messages.

6. **Test locally**
   - Run the script against your development database.
   - Confirm the row count in PostgreSQL matches expectations.

### Checklist

- [ ] `src/` folder created if needed.
- [ ] Load script file created with CLI arguments.
- [ ] Script loads `books.csv` into PostgreSQL.
- [ ] Basic logging and error messages added.
- [ ] Script tested and documented for reuse.
