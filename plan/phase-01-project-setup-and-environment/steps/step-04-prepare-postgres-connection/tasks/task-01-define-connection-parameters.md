# Task 01 – Define Connection Parameters

## Objective

Clearly define the connection details that Python will use to reach your PostgreSQL database.

## Instructions

1. Identify the following values for your PostgreSQL container:
   - Hostname (e.g., `localhost` or the Docker service name like `db`).
   - Port (commonly `5432`).
   - Database name (e.g., `goodreads_db`).
   - Username.
   - Password.
2. Write these values in a **configuration note** (e.g., `docker/postgres-connection-notes.md`) but avoid committing real passwords to the repository.
3. Decide on environment variable names, such as:
   - `POSTGRES_HOST`
   - `POSTGRES_PORT`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`

## Checklist

- [ ] I know the host, port, database, user, and password for PostgreSQL.
- [ ] I have defined environment variable names for these values.
- [ ] I have documented this in a local configuration note.

## Result

You have a clear set of connection parameters ready to be used by your Python code and/or Docker Compose.
