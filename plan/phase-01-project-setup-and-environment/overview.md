# Phase 01 – Project Setup and Environment

## Goal

Set up a **reproducible development environment** for the Goodreads Books Analytics project using Docker, Jupyter Notebooks, and PostgreSQL. By the end of this phase you will be able to open a notebook, access the `books.csv` file, and (optionally) connect to a PostgreSQL database running in Docker.

In this phase you will see a few important tools for the first time:

- **Docker**: a tool that lets you run your code inside small, isolated environments called _containers_. Each container has its own Python, libraries, and configuration.
- **PostgreSQL**: a popular open-source relational database used to store and query data with SQL.
- **Jupyter Notebook / JupyterLab**: an interactive environment where you can run Python code in small cells and see results immediately (tables, charts, text).

## Inputs

- This repository cloned locally.
- Docker Desktop installed and running.
- Basic familiarity with the command line (PowerShell, bash, etc.).
- Access to a PostgreSQL instance in Docker (either already running or planned to be set up).

## Outputs / Deliverables

By completing this phase you should have:

1. A **clean project structure** locally (cloned repo, basic folders verified).
2. A **Python environment inside Docker** with:
   - Jupyter Notebook or JupyterLab available.
   - Required base libraries installed (e.g., `pandas`, `matplotlib`, `seaborn`, `sqlalchemy`, `psycopg2-binary`).
3. A **running Jupyter server** that can see the project files.
4. A **connection configuration** (environment variables or config file) prepared for PostgreSQL.
5. (Optional) A **docker-compose setup** that can orchestrate the Python/Jupyter container and the PostgreSQL container together.

## Steps in This Phase

The detailed steps for this phase are documented under `steps/`:

1. **Step 1 – Understand Repository and Tools**  
   Folder: `steps/step-01-understand-repo-and-tools/`

2. **Step 2 – Design Python + Jupyter Docker Environment**  
   Folder: `steps/step-02-design-python-docker-environment/`

3. **Step 3 – Implement and Test Docker Setup**  
   Folder: `steps/step-03-implement-and-test-docker-setup/`

4. **Step 4 – Prepare PostgreSQL Connection Configuration**  
   Folder: `steps/step-04-prepare-postgres-connection/`

Work through these steps in order. Each step contains tasks with checklists to guide you.

## Tips

- If Docker is new to you, take your time with Step 2 and 3. The goal is not just to get it running but to understand **why** the Dockerfile and compose file are written in a certain way. You can also read a short beginner article or watch a short video on "What is Docker?" before or during this phase.
- Keep notes of any issues you hit and how you solved them. These notes are useful later and can be added to the project documentation (for example, in `docs/repo-notes.md`).
- Use Git from the beginning. Even small setup changes (like adding a Dockerfile) should be committed with clear messages.
