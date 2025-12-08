# Phase 01 – Step 03 – Task 01 Notes

This document explains how **Task 01 – Create Dockerfile and Build Image** was completed for the `goodreads-books-analytics` project. It focuses on turning the draft Dockerfile into a buildable image and recording the exact build commands and results.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-03-implement-and-test-docker-setup/tasks/task-01-create-dockerfile-and-build-image.md`.

---

## 1. Goal of this task

The goal is to:

1. Refine the existing `docker/python/Dockerfile` so it is actually buildable.
2. Make sure a `requirements.txt` file exists and matches the package list.
3. Build the Docker image using `docker build`.
4. Confirm that the image builds successfully and record its name and tag.

After this task, you have a concrete, runnable image for the Python CLI environment.

---

## 2. Reviewing the Dockerfile and requirements

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
code docker\python\Dockerfile
code requirements.txt
docker build -f docker/python/Dockerfile -t goodreads-analytics-python:latest .
docker images goodreads-analytics-python
```

### Estimated runtime & success outputs

- **Runtime:** ~90 seconds on the first build (Docker pulls base image + installs packages); subsequent builds take ~20 seconds thanks to caching.
- **Success checklist:**
  - VS Code opens both the Dockerfile and `requirements.txt` so you can verify contents before building.
  - `docker build ...` finishes without errors and prints `Successfully tagged goodreads-analytics-python:latest`.
  - `docker images goodreads-analytics-python` lists the image with a recent `CREATED` timestamp.

Before building, we checked two files:

- `docker/python/Dockerfile`
- `requirements.txt` (at the project root)

### 2.1. Dockerfile status

The Dockerfile already contained all the necessary elements from Step 02:

- Base image:

  ```dockerfile
  FROM python:3.14-slim
  ```

- Working directory:

  ```dockerfile
  WORKDIR /app
  ```

- System dependencies for `psycopg2-binary` and scientific libraries:

  ```dockerfile
  RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*
  ```

- Copying and installing Python dependencies from `requirements.txt`:

  ```dockerfile
  COPY requirements.txt /app/requirements.txt

  RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
  ```

- Setting the container to stay alive for CLI execution by default:

  ```dockerfile
  CMD ["sleep", "infinity"]
  ```

This means no additional changes were required to make the Dockerfile buildable.

### 2.2. Requirements file

The `requirements.txt` file contained the packages defined in Step 02:

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

Together, the Dockerfile and `requirements.txt` fully describe the environment to be built.

---

## 3. Building the Docker image

### 3.1. Command used (PowerShell)

From the project root (`goodreads-books-analytics`), the image was built with:

```powershell
cd "C:\Users\shady\documents\GITHUB\goodreads-books-analytics"

docker build -f docker/python/Dockerfile -t goodreads-analytics-python:latest .
```

Explanation:

- `-f docker/python/Dockerfile` – tells Docker which Dockerfile to use.
- `-t goodreads-analytics-python:latest` – tags the image as `goodreads-analytics-python` with the `latest` tag.
- `.` – sets the build context to the project root, so `requirements.txt` and other files are available during the build.

### 3.2. Build output (summary)

The build completed successfully. Key steps in the output included:

- Pulling the base image `python:3.14-slim`.
- Running `apt-get update` and installing system packages.
- Copying `requirements.txt` into `/app/requirements.txt`.
- Running `pip install --no-cache-dir --upgrade pip`.
- Installing packages from `requirements.txt`.
- Exporting layers and naming the image `docker.io/library/goodreads-analytics-python:latest`.

This confirms that the Dockerfile and `requirements.txt` are valid and the image can be built without errors.

---

## 4. Image name and tag

The built image is identified as:

- **Repository**: `goodreads-analytics-python`
- **Tag**: `latest`

In Docker notation:

- `goodreads-analytics-python:latest`

You can verify the image exists with:

```powershell
docker images goodreads-analytics-python
```

This name and tag will be useful later when referencing the image directly or integrating it into Docker Compose configurations.

---

## 5. Mapping to the Task 01 checklist

From the planning document:

- [x] **I have a working `Dockerfile` for Python CLI.**  
       → Confirmed that `docker/python/Dockerfile` includes base image, system dependencies, pip installs, and VS Code + terminal workflow command.

- [x] **I have built the Docker image successfully.**  
       → `docker build -f docker/python/Dockerfile -t goodreads-analytics-python:latest .` completed without errors.

- [x] **I have noted the image name and tag (e.g., `goodreads-analytics-python:latest`).**  
       → Documented above in Section 4.

Therefore, **Phase 01 → Step 03 → Task 01** is complete.

---

## 6. How to reuse this process in other projects

When implementing and building a Docker image for a Python CLI environment in another analytics project, you can follow these steps:

1. **Draft a Dockerfile** with:

   - A suitable base image (e.g., `python:3.14-slim`).
   - System dependencies for any special libraries you need.
   - A `COPY requirements.txt` + `pip install -r requirements.txt` pattern.
   - An exposed port and a sensible default command.

2. **Create a `requirements.txt`** that lists your Python packages (pandas, numpy, visualization libs, DB drivers, Python CLI workflow, etc.).

3. **Build the image** from the project root using:

   ```powershell
   docker build -f path/to/Dockerfile -t your-image-name:tag .
   ```

4. **Confirm success** by checking the build output and using `docker images`.

5. **Record the image name and tag** in a notes file (like this one) so you and others know how to reference it later.

Documenting these steps makes your environment setup reproducible and easy to explain in a professional portfolio.
