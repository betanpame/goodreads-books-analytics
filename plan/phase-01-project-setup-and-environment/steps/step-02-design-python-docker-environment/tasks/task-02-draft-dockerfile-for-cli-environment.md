# Task 02 – Draft Dockerfile for Python and Python CLI workflow

## Objective

Create a first draft of the Dockerfile that will define your Python CLI environment.

## Instructions

1. In the repository, create a folder for Docker-related files, for example `docker/python/`.
2. Inside that folder, create a file named `Dockerfile` (you will fill it in later during implementation).
3. In `Dockerfile`, write a **draft** (not necessarily final) that includes:
   - The base image you chose (e.g., `FROM python:3.11-slim`).
   - Instructions to install system dependencies needed by `psycopg2-binary` and other libraries.
   - A way to install Python packages (for example by copying a `requirements.txt` and running `pip install -r requirements.txt`).
4. Add comments to explain each major block of the Dockerfile, so future you understands it.

## Checklist

- [ ] I have created a `docker/python/` folder.
- [ ] I have created a `Dockerfile` inside it.
- [ ] I have written a first draft of the Dockerfile with comments.

## Result

You have a starting point for your Python CLI Docker image, which you will implement and refine in the next step.
