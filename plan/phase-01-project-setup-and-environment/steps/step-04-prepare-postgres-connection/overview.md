# Step 04 – Prepare PostgreSQL Connection Configuration

## Goal

Prepare a **clean and secure way** for your Python/Jupyter environment to connect to PostgreSQL running in Docker.

## Why This Step Matters

Storing connection details (host, port, user, password, database) in a consistent place makes it easier to:
- Reuse the configuration across notebooks and scripts.
- Avoid hardcoding sensitive values in code.
- Switch between local and (future) cloud databases.

## Tasks

Detailed tasks are in the `tasks/` folder:

1. `task-01-define-connection-parameters.md`
2. `task-02-store-credentials-safely.md`
3. `task-03-test-connection-from-python.md`
