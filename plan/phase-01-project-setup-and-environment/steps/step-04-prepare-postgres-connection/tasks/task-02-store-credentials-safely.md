# Task 02 – Store Credentials Safely

## Objective

Decide how to store PostgreSQL credentials in a way that is convenient for development but does not expose secrets in the repository.

## Instructions

1. Choose a method for storing credentials locally, such as:
   - A `.env` file (which will be **ignored by Git**), or
   - Environment variables set in Docker Compose or your terminal session.
2. If using a `.env` file:
   - Create a `.env` file at the project root or under `docker/`.
   - Add your PostgreSQL environment variables (`POSTGRES_HOST`, etc.).
   - Ensure `.env` is listed in `.gitignore` so it is not committed.
3. If using Docker Compose environment variables:
   - Plan how these variables will be provided in `docker-compose.yml` (but avoid hardcoding sensitive values in version-controlled files).

## Checklist

- [ ] I have chosen a strategy for storing credentials locally.
- [ ] I have created any necessary local config files (e.g., `.env`).
- [ ] I have confirmed that sensitive files are ignored by Git.

## Result

Your credentials are stored in a safe, reusable way that will work with Docker and Python code.
