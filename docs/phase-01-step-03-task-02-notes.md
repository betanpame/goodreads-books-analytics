## Phase 01 · Step 03 · Task 02 – Run Container and Test CLI Execution

This note documents how I verified that the Dockerized Python environment actually runs and can execute the same Python modules we will use later in the project. The goal is to turn the Docker image created in Task 01 into a working, script-friendly environment.

### 1. Prerequisites and context

- I already built the image `goodreads-analytics-python:latest` in Task 01 using `docker/python/Dockerfile` and the root `requirements.txt`.
- Docker Desktop is running on Windows.
- I am working from the project root folder:
  `C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics`

### 2. Start a container for CLI verification

From a PowerShell terminal opened in the project root, I launched an interactive container session that mounts the repository and lands me in `/app`:

```powershell
docker run --rm -it -v ${PWD}:/app --name goodreads_python_test goodreads-analytics-python:latest /bin/bash
```

Key flags and options:

- `--rm`: automatically removes the container when it stops, so I do not accumulate stopped containers during experimentation.
- `-it`: attaches STDIN/STDOUT so I get an interactive shell.
- `-v ${PWD}:/app`: bind-mounts the project into the container, matching the path used by Docker Compose.
- `--name goodreads_python_test`: gives the container a readable name for easier management (logs, stopping, etc.).
- `/bin/bash`: overrides the default `sleep infinity` command so I can explore the environment immediately.

Once the container started, I saw the Bash prompt inside `/app`, confirming that the repository files were visible from the CLI session.

### 3. Run a sample Python script inside the container

With the interactive shell open, I validated the environment with a few quick commands:

```bash
python --version
python - <<'PY'
import pandas as pd
from pathlib import Path

books = Path("data") / "books.csv"
print("books.csv exists:", books.exists())
print("pandas version:", pd.__version__)
PY

python -m src.run_full_pipeline --help
```

These checks confirm that:

- The correct Python interpreter is available inside the container.
- Core dependencies such as `pandas` load without errors.
- Project modules under `src/` can be executed the same way they will be run during later phases.

### 4. Stopping the container cleanly

Because the session was interactive, shutting it down only required typing `exit` (or pressing `Ctrl+D`). Docker immediately stopped and removed the container thanks to the `--rm` flag.

If I had needed to terminate it from another terminal (for example if the shell became unresponsive), I could have run `docker stop goodreads_python_test`.

### 5. How to repeat this in the future

To re-run this task on another machine or at a later time:

1. Ensure Docker Desktop is installed and running.
2. Build the image (if not already built):

   ```powershell
   cd "C:\Users\shady\OneDrive\Documentos\GITHUB\goodreads-books-analytics"
   docker build -f docker/python/Dockerfile -t goodreads-analytics-python:latest .
   ```

3. Start an interactive container session with project files mounted:

   ```powershell
   docker run --rm -it -v ${PWD}:/app --name goodreads_python_test goodreads-analytics-python:latest /bin/bash
   ```

4. Run whichever Python modules or scripts you need (for example, `python -m src.run_full_pipeline` or `python -m src.analyses.initial_inspection_books --help`).
5. Type `exit` when finished.

This completes Phase 01 · Step 03 · Task 02: the Dockerized Python environment now runs successfully, exposes the repository via a bind mount, and executes CLI scripts exactly the way they will be used throughout the project.
