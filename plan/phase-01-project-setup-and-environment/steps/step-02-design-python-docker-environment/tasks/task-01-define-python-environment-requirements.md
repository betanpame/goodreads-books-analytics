# Task 01 – Define Python Environment Requirements

## Objective

List the Python packages and tools that your Docker-based environment must include.

## Instructions

1. Create a new markdown file in the repository (for example `docker/python-requirements-notes.md`) or use your own notes.
2. Based on the project plan, list required packages, such as:
   - `pandas`
   - `numpy`
   - `matplotlib`
   - `seaborn`
   - `python-dotenv`
   - `sqlalchemy`
   - `psycopg2-binary` (for PostgreSQL connections)
3. Mark which packages are **must-have** for Phase 01–04 and which are **optional/for later**.
4. Decide on a base Python image (for example `python:3.11-slim`) and note it down.

## Checklist

- [ ] I have a written list of required Python packages.
- [ ] I have distinguished between must-have and optional packages.
- [ ] I have chosen a base Python image for the Dockerfile.

## Result

You now have a clear definition of what your Python Docker environment needs, making it easier to write the Dockerfile.
