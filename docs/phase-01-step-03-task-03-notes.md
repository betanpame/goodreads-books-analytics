## Phase 01 · Step 03 · Task 03 – Mount Project Folder and Verify Access

This note documents how I verified that the running Dockerized Python CLI workflow environment can see and work with the `goodreads-books-analytics` project files. The goal is to mount the project folder into the container, confirm that the container shell shows the repository structure, and prove that changes made from inside the container are visible on the host.

### 1. Objective and high-level idea

The task objective from the plan is:

- Mount the project folder into the container.
- From inside the running container, list the repository contents (e.g., `data/`, `plan/`, `README.md`).
- Create a simple test analysis script inside the mounted folder using the container shell.
- Verify that this new analysis script appears on the host machine.

In practice, this means using a **bind mount** so that the container uses the host project folder as its `/app` directory. Any analysis scripts or code created under `/app` inside the container will be real files in the host repository.

### 2. How the mount is defined in Docker Compose

In this project, the bind mount is already configured in the `docker-compose.python.yml` file. The relevant part for the `app` service is:

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: docker/python/Dockerfile
    container_name: ${PROJECT_NAME}_python
    volumes:
      - ..:/app
```

Key points:

- `..:/app` is a **host:container** path mapping.
  - The host path `..` means "one level up from the compose file directory", which is the project root `goodreads-books-analytics`.
  - The container path `/app` is the working directory inside the Python CLI container.
- When this stack runs, the entire project folder on the host is mounted under `/app` in the container.
- The `docker/python/Dockerfile` is designed to use `/app` as the working directory, so every command executed inside the container operates directly on the mounted project files.

This setup matches the goal of the task: the container should work directly against the same files that are under version control on the host.

### 3. Starting the stack with the project folder mounted

To use the compose file and start both the Python CLI `app` service and the `postgres` service with the project folder mounted, I ran the following commands from a PowerShell terminal.

1. Navigate to the project root:

   ```powershell
   cd "C:\Users\shady\documents\GITHUB\goodreads-books-analytics"
   ```

2. Start the services defined in `docker-compose.python.yml` in detached mode:

   ```powershell
   docker compose -f docker-compose.python.yml up -d
   ```

   What this does:

   - Builds the `app` image if needed, using `docker/python/Dockerfile`.
   - Starts the `app` container (with `/app` bound to the host project folder).
   - Starts the `postgres` container with the configuration from the compose file.

3. Confirm the containers are running:

   ```powershell
   docker compose -f docker-compose.python.yml ps
   ```

   I expect to see at least these services:

   - `${PROJECT_NAME}_python` (the Python CLI container).
   - `${PROJECT_NAME}_postgres` (the PostgreSQL container).

### 4. Inspecting the repository from inside the container shell

Once the services are running, I verify the mount by opening a shell inside the
`app` container instead of using a browser-based UI.

1. Start an interactive shell:

   ```powershell
   docker compose -f docker-compose.python.yml exec app bash
   ```

   (If `bash` is unavailable, `sh` works as well.)

2. Inside the container, check the working directory and list the top-level files:

   ```bash
   pwd
   ls -1
   ```

   The output should show `/app` as the current directory and list folders such as
   `data`, `docs`, `plan`, `src`, `tests`, plus files like `README.md` and
   `requirements.txt`.

This confirms that the bind mount is active and the container sees the exact same
files that exist on the host.

### 5. Creating and saving a test analysis script from inside the container

To explicitly verify that changes made in the container are persisted on the
host, I created a small Python file using the same shell session.

```bash
cat <<'PY' > docs/docker-mount-test.py
import os

print("Current working directory:", os.getcwd())
print("docs/ contains:", os.listdir("."))
PY

python docs/docker-mount-test.py
```

Running the script prints the working directory (for example, `/app/docs`) and a
listing of files in that folder, proving that the interpreter can access the
project just like any other local code.

### 6. Verifying the new analysis script on the host machine

The final step is to check that the newly created analysis script exists in the host repository, proving that the bind mount works both ways.

1. On the host, in VS Code or File Explorer, I navigated to the `docs/` folder of the project:

   - `C:\Users\shady\documents\GITHUB\goodreads-books-analytics\docs`.

2. I confirmed that the new analysis script file I created from within the container shell (for example, `docker-mount-test.py`) appeared in this folder.

3. I could open the analysis script directly in VS Code on the host to double-check that it contained the same quick filesystem check.

This confirms that:

- The project folder is successfully mounted into the container.
- Files created or modified inside the container are immediately visible on the host.

### 7. Stopping the Docker stack when finished

Once I finished verifying the mount and the analysis script, I stopped the running services to free resources.

From the project root, I ran:

```powershell
docker compose -f docker-compose.python.yml down
```

This command:

- Stops the `app` and `postgres` containers.
- Removes the stopped containers and the default network created for this compose file.
- Leaves the named volume `postgres_data` intact, so the PostgreSQL data persists across runs.

### 8. How to repeat this task in the future

To repeat this workflow on another machine or in the future:

1. Ensure Docker Desktop is installed and running.
2. Clone the `goodreads-books-analytics` repository.
3. Navigate to the project root in PowerShell:

   ```powershell
   cd "C:\path\to\goodreads-books-analytics"
   ```

4. Start the stack with the Python and Postgres services:

   ```powershell
   docker compose -f docker-compose.python.yml up -d
   ```

5. Open a shell inside the container and list the project contents:

   ```powershell
   docker compose -f docker-compose.python.yml exec app bash -lc "pwd; ls -1"
   ```

6. Create a tiny test script from the container (or edit any existing file) and run it to confirm the bind mount works both ways.
7. Verify that new or edited scripts appear immediately in the corresponding folders on the host (e.g., open `docs/docker-mount-test.py` in VS Code).
8. When finished, stop the stack:

   ```powershell
   docker compose -f docker-compose.python.yml down
   ```

This completes Phase 01 · Step 03 · Task 03: the Dockerized Python CLI workflow environment is now fully integrated with the project files via a bind mount, making it easy to develop, version, and run analytics code in a reproducible container while editing files directly on the host.
