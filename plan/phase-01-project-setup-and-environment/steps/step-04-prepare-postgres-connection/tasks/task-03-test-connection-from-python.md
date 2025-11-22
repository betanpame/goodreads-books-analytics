# Task 03 – Test Connection from Python

## Objective

Verify that your Python code (running in the Docker container) can successfully connect to your PostgreSQL database.

## Instructions

1. Start your PostgreSQL Docker container (if it is not already running).
2. Start your Python/Jupyter container and open a notebook.
3. In the notebook, write a small Python snippet that:
   - Reads connection parameters from environment variables or a config file.
   - Uses `sqlalchemy` or `psycopg2` to open a connection.
   - Runs a simple query like `SELECT 1;`.
4. Confirm that the query runs without errors.

## Checklist

- [ ] Both PostgreSQL and Python/Jupyter containers are running.
- [ ] I have written Python code to connect to PostgreSQL.
- [ ] I have successfully executed a test query.

## Result

You have a working connection from your analysis environment to PostgreSQL, enabling SQL-based analysis in later phases.
