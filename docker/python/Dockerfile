## Dockerfile for the CLI-focused Python analytics environment
# Phase 01 → Step 02 → Task 02 (updated for script-based workflow)

# 1) Base image: use a small, modern Python 3 image
FROM python:3.14-slim

# 2) Set working directory inside the container
WORKDIR /app

# 3) Install system dependencies needed by psycopg2-binary and scientific libraries
#    - build-essential: compilers and build tools
#    - libpq-dev: PostgreSQL client libraries/headers for psycopg2
#    - curl/ca-certificates: useful for debugging and secure downloads
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  curl \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# 4) Copy requirements file (to be created) and install Python dependencies
#    The requirements file should include packages like:
#    pandas, numpy, matplotlib, seaborn, sqlalchemy, psycopg2-binary,
#    python-dotenv, etc.
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r /app/requirements.txt

# 5) Default command keeps the container alive for interactive CLI execution.
#    Use `docker compose run --rm app python -m src.run_full_pipeline` (or similar)
#    to execute scripts directly from this image.
CMD ["sleep", "infinity"]
