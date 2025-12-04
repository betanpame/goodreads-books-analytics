# Task 01 – Create Dockerfile and Build Image

## Objective

Implement the Dockerfile for your Python CLI environment and build the Docker image.

## Instructions

1. Open the `docker/python/Dockerfile` created in Step 02.
2. Refine the Dockerfile so that it can actually be built:
   - Confirm the base image.
   - Install system dependencies.
   - Copy a `requirements.txt` file (you can create it from your package list).
   - Run `pip install -r requirements.txt`.
3. Build the image via Docker Compose so it stays in sync with the rest of the stack:
   ```powershell
   docker compose -f docker-compose.python.yml build app
   ```
   or, if you want the Postgres service built too:
   ```powershell
   docker compose -f docker-compose.python.yml -f docker-compose.postgresql.yml build
   ```
4. Fix any errors that occur during the build until `docker compose ... build` finishes successfully.

## Checklist

- [ ] I have a working `Dockerfile` for Python CLI.
- [ ] I have built the Docker image successfully via `docker compose ... build`.
- [ ] I know which compose service/tag will be reused (e.g., the `app` service image defined in `docker-compose.python.yml`).

## Result

You now have a Docker image ready to be used for running Python CLI workflow analysis scripts in a controlled environment.
