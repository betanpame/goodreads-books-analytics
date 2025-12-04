# Task 03 – Plan docker-compose Structure

## Objective

Design how Docker Compose (or an equivalent tool) will manage your Python CLI container and PostgreSQL container.

## Instructions

1. Decide whether you will:
   - Use an existing `docker-compose.yml` that already defines PostgreSQL, or
   - Create a new `docker-compose.yml` that includes both Python CLI and PostgreSQL services.
2. In your notes or in a new file (for example `docker/compose-design-notes.md`), describe:
   - Service names (e.g., `app` for Python, `db` for PostgreSQL).
   - Which ports will be exposed (e.g., `8888` for Python CLI workflow, `5432` for PostgreSQL).
   - How volumes will be used to:
     - Mount the project folder into the Python container.
     - Persist PostgreSQL data.
   - Environment variables that need to be passed (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
3. Sketch a minimal example of what the `docker-compose.yml` could look like (even in pseudocode form).

## Checklist

- [ ] I have decided how Docker Compose will be used.
- [ ] I have documented service names, ports, volumes, and environment variables.
- [ ] I have a rough sketch of the future `docker-compose.yml`.

## Result

You now have a clear plan for orchestrating your containers, which will simplify the actual implementation in the next step.
