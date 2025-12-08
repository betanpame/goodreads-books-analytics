# Phase 01 – Step 02 – Task 03 Notes

This document explains how **Task 03 – Plan docker-compose Structure** was completed for the `goodreads-books-analytics` project. It focuses on designing how Docker Compose will orchestrate a Python CLI container alongside the existing PostgreSQL container.

Task reference: `plan/phase-01-project-setup-and-environment/steps/step-02-design-python-docker-environment/tasks/task-03-plan-docker-compose-structure.md`.

---

## 1. High-level decision: separate compose files

### Command block (copy/paste)

```powershell
cd C:\Users\shady\documents\GITHUB\goodreads-books-analytics
New-Item -ItemType File -Path docker-compose.python.yml -Force | Out-Null
code docker-compose.python.yml
docker compose -f docker-compose.python.yml config
```

### Estimated runtime & success outputs

- **Runtime:** ~20 seconds to scaffold + validate the compose file; `docker compose ... config` runs in under 3 seconds if the YAML is valid.
- **Success checklist:**
  - `docker-compose.python.yml` exists in the repo root and opens in VS Code for editing.
  - `docker compose ... config` prints the merged configuration without errors, confirming that YAML syntax and env references are correct.
  - The generated config shows both the `app` and `postgres` services with the expected volume/network definitions.

The first decision in this task is **how** to organize Docker Compose files. There are two common options:

1. A **single** `docker-compose.yml` that defines both Python CLI and PostgreSQL.
2. **Separate** compose files (for example, one for PostgreSQL only, and another for the Python CLI environment).

For this project, we chose **option 1 from your answer, which corresponds to keeping the existing Postgres-only compose file and adding a separate compose file for Python CLI**:

- Keep the existing `docker-compose.postgresql.yml` focused on the PostgreSQL database.
- Add a new file dedicated to the Python CLI app that can also start Postgres when needed.

This approach is flexible and keeps concerns separated:

- You can run **only PostgreSQL** if you want (using the existing compose file).
- You can run **Python CLI + PostgreSQL together** using the new compose file.

---

## 2. New compose file: `docker-compose.python.yml`

A new Docker Compose file was created at:

- `docker-compose.python.yml`

This file defines two services:

- `app` – the Python CLI service built from `docker/python/Dockerfile`.
- `postgres` – a PostgreSQL service configured in a similar way to `docker-compose.postgresql.yml`.

It also defines:

- A named volume `postgres_data` for database persistence.
- A `backend` network to allow the two services to communicate.

---

## 3. Service design: `app` (Python CLI)

### 3.1. Basic configuration

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: docker/python/Dockerfile
    container_name: ${PROJECT_NAME}_python
    restart: unless-stopped
```

- `build.context: ..` – The build context is the project root (one level above the `docker/` folder).
- `dockerfile: docker/python/Dockerfile` – Points to the Dockerfile created in Task 02.
- `container_name` – Uses the `PROJECT_NAME` value from `.env` to name the container (e.g., `goodreads_books_analytics_python`).
- `restart: unless-stopped` – Automatically restarts the container unless you explicitly stop it.

### 3.2. Environment variables

```yaml
environment:
  PROJECT_NAME: ${PROJECT_NAME}
  POSTGRES_DB: ${POSTGRES_DB}
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  POSTGRES_HOST: postgres
  POSTGRES_PORT: 5432
```

- Reuses values from `.env` (`PROJECT_NAME`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`).
- Sets `POSTGRES_HOST` to `postgres`, which is the **service name** of the database container inside the `backend` network.
- Sets `POSTGRES_PORT` to `5432`, which is the internal port of PostgreSQL inside the network.

This configuration ensures that your Python code (via `db_config.py`) can connect to the PostgreSQL service using service discovery instead of `localhost`.

### 3.3. Volumes and ports

```yaml
volumes:
  - ..:/app
```

- `..:/app` – Mounts the entire project root into `/app` inside the container.
  - This allows you to edit files on the host and have those changes instantly visible inside the container.
- **No ports are exposed** because the Python container now runs purely as a CLI environment. You interact with it via `docker compose run ...` or `docker compose exec ...` instead of a browser session.

### 3.4. Dependency on PostgreSQL and network

```yaml
depends_on:
  - postgres
networks:
  - backend
```

- `depends_on: postgres` – Ensures that Docker Compose starts the `postgres` service before the `app` service.
- `networks: backend` – Connects the `app` service to the `backend` network, where `postgres` is also attached.

---

## 4. Service design: `postgres` (database)

The `postgres` service in `docker-compose.python.yml` mirrors the configuration from `docker-compose.postgresql.yml` so that this single compose file can manage both services together.

```yaml
postgres:
  image: postgres:${POSTGRES_VERSION}
  container_name: ${PROJECT_NAME}_postgres
  restart: unless-stopped
  environment:
    POSTGRES_DB: ${POSTGRES_DB}
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    PGDATA: /var/lib/postgresql/data/pgdata
  ports:
    - "${POSTGRES_PORT}:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - backend
```

Key points:

- Uses the same image and environment variables (`POSTGRES_VERSION`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) as the existing Postgres-only compose file.
- Maps host port `${POSTGRES_PORT}` (from `.env`, e.g., `5491`) to container port `5432`.
- Persists data in the named volume `postgres_data`.
- Attaches to the `backend` network.

This keeps behavior consistent whether you start Postgres via the old compose file or via this new combined one.

---

## 5. Volumes and networks

At the bottom of `docker-compose.python.yml`:

```yaml
volumes:
  postgres_data:

networks:
  backend:
    driver: bridge
```

- `postgres_data` – Named Docker volume used to persist PostgreSQL data.
- `backend` – Bridge network that allows `app` and `postgres` to communicate using service names.

This matches the existing pattern from `docker-compose.postgresql.yml` and ensures consistent networking.

---

## 6. How this satisfies the Task 03 checklist

From the planning document:

- [x] **I have decided how Docker Compose will be used.**  
       → Decision: keep `docker-compose.postgresql.yml` for database-only usage and add a separate `docker-compose.python.yml` that defines both `app` and `postgres`.

- [x] **I have documented service names, ports, volumes, and environment variables.**  
       → Documented above and encoded in `docker-compose.python.yml`.

- [x] **I have a rough sketch of the future `docker-compose.yml`.**  
       → `docker-compose.python.yml` is a concrete draft that can be used as-is or refined later.

Thus, **Phase 01 → Step 02 → Task 03** is completed at the planning level.

---

## 7. Commands to run this setup (PowerShell)

From the project root (`goodreads-books-analytics`), you will be able to:

- Build and start both services (Python CLI + PostgreSQL):

```powershell
docker compose -f docker-compose.python.yml up -d
```

- Check running services:

```powershell
docker compose -f docker-compose.python.yml ps
```

- View logs (for example, Postgres):

```powershell
docker compose -f docker-compose.python.yml logs -f postgres
```

- Stop services (keeping data):

```powershell
docker compose -f docker-compose.python.yml down
```

- Stop services and remove the database volume (dangerous: deletes data):

```powershell
docker compose -f docker-compose.python.yml down -v
```

These commands will be refined and reused in later phases when you actually run analysis scripts and the pipeline inside the container.

---

## 8. How to reuse this design in other projects

When planning Docker Compose for a similar analytics stack (Python CLI + PostgreSQL), you can:

1. Decide whether to use **one main compose file** or **separate ones** for database and app.
2. Define an `app` service that:
   - Builds from a Dockerfile in a `docker/` subfolder.
   - Mounts the project root as a volume.

- Only exposes ports if the service actually hosts an API or UI (our CLI-only container does not publish any ports).
- Uses environment variables to connect to the database service.

3. Define a `postgres` (or `db`) service that:
   - Uses the official Postgres image.
   - Reads credentials and ports from a `.env` file.
   - Persists data in a named volume.
   - Shares a network with `app`.
4. Document all of this in a short notes file (like this one) inside `docs/`.

By doing this planning before implementation, you make the orchestration of containers clearer, more maintainable, and easier to explain in your portfolio.
