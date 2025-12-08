# Phase 01 – Step 02 – Task 02 Notes

This document explains how **Task 02 – Draft Dockerfile for Python and Python CLI workflow** was completed for the `goodreads-books-analytics` project. It is written as a learning guide so you can follow the same steps when creating a Docker-based Python CLI environment in other projects.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-02-design-python-docker-environment/tasks/task-02-draft-dockerfile-for-cli-environment.md`.

---

## 1. Goal of this task

The aim of Task 02 is to create a **first draft** of the Dockerfile that will define your Python CLI environment. At this stage, it does not have to be perfect or fully optimized, but it should:

- Use the base Python image you selected in Task 01.
- Install the system dependencies required by key Python packages (especially `psycopg2-binary`).
- Install your Python dependencies from a `requirements.txt` file.
- Provide a default command to start VS Code + terminal workflow inside the container.

This draft becomes the foundation for later refinement and integration with Docker Compose.

---

## 2. Creating the Docker folder structure

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
New-Item -ItemType Directory -Path docker\python -Force | Out-Null
New-Item -ItemType File -Path docker\python\Dockerfile -Force | Out-Null
code docker\python\Dockerfile
```

### Estimated runtime & success outputs

- **Runtime:** ~15 seconds including opening the Dockerfile in VS Code.
- **Success checklist:** - Folder `docker/python/` exists with a `Dockerfile` inside. - VS Code opens the Dockerfile so you can start pasting the base image + RUN blocks. - `git status` now shows `docker/python/Dockerfile` as a tracked file.

The task suggests creating a dedicated folder such as `docker/python/` to hold the Dockerfile.

In this project:

- The folder `docker/python/` was created.
- Inside that folder, a file named `Dockerfile` was added.

This keeps Docker-related configuration close to the project root but logically separated from application code (`src/`) and documentation (`docs/`).

You can follow the same pattern in other projects by placing infrastructure files under a `docker/` or `infra/` directory.

---

## 3. Drafting the Dockerfile

The draft Dockerfile lives at:

- `docker/python/Dockerfile`

Below is an explanation of each major block.

### 3.1. Base image

```dockerfile
FROM python:3.14-slim
```

- Uses the base image defined in Task 01 (`python:3.14-slim`).
- Provides a recent, stable Python 3 runtime in a relatively small image.

### 3.2. Working directory

```dockerfile
WORKDIR /app
```

- Sets `/app` as the default working directory inside the container.
- Subsequent commands (`COPY`, `RUN`, `CMD`) are relative to this directory.

### 3.3. System dependencies

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```

- `apt-get update`: refreshes package lists.
- `build-essential`: provides compilers and build tools; some Python packages may need to compile native extensions.
- `libpq-dev`: PostgreSQL client development files required by `psycopg2-binary`.
- `curl` and `ca-certificates`: useful for debugging, HTTPS downloads, and general networking.
- `rm -rf /var/lib/apt/lists/*`: cleans up apt lists to keep the image smaller.

This block ensures the container has the necessary OS-level dependencies to install and run the Python libraries you defined earlier.

### 3.4. Python dependencies via requirements.txt

To keep the Dockerfile simple and maintainable, the Python dependencies are pulled from a `requirements.txt` file in the project root.

A new file was created:

- `requirements.txt` (at the project root)

With content based on the environment design from Task 01:

```text
pandas
numpy
matplotlib
seaborn
sqlalchemy
psycopg2-binary
python-dotenv
# Optional tools (uncomment if needed)
# pytest
# black
# ruff
```

In the Dockerfile, this file is copied and installed:

```dockerfile
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
```

- `COPY requirements.txt /app/requirements.txt` copies the project’s `requirements.txt` into the container.
- `pip install --no-cache-dir --upgrade pip` ensures you have a recent pip version.
- `pip install --no-cache-dir -r /app/requirements.txt` installs all required Python packages.

Using a `requirements.txt` file:

- Makes dependency management clear and editable outside the Dockerfile.
- Allows you to reuse the same file locally (e.g., for a virtual environment).

### 3.5. Default command for the CLI container

```dockerfile
CMD ["sleep", "infinity"]
```

- The container now stays alive waiting for commands. You can run entry points such as `docker compose run --rm app python -m src.run_full_pipeline` without needing to expose a browser port.
- This keeps the image focused on script execution and avoids bundling unnecessary UI packages.

---

## 4. How this matches the Task 02 checklist

From the planning document:

- [x] **I have created a `docker/python/` folder.**  
       → The folder `docker/python/` now exists.

- [x] **I have created a `Dockerfile` inside it.**  
       → `docker/python/Dockerfile` is present.

- [x] **I have written a first draft of the Dockerfile with comments.**  
       → The Dockerfile includes commented sections for base image, system dependencies, Python dependencies, and the VS Code + terminal workflow command.

This means **Phase 01 → Step 02 → Task 02** is completed at the draft level.

---

## 5. How to reuse this pattern in other projects

When creating a Docker-based Python CLI environment for another analytics project, you can:

1. **Create a dedicated Docker folder** (e.g., `docker/python/`) and place your `Dockerfile` there.
2. **Choose a base image** such as `python:3.14-slim`.
3. **Install system dependencies** required by any database drivers or scientific libraries you plan to use.
4. **Copy a `requirements.txt` file** from the project root into the image and install dependencies with `pip install -r requirements.txt`.
5. **Expose a port and set a sensible CMD** (like starting VS Code + terminal workflow or another entrypoint script).
6. **Comment your Dockerfile** to explain major decisions, which is particularly valuable in a portfolio.

By following this pattern, your Dockerfile will be both practical and easy for reviewers (and future you) to understand.
