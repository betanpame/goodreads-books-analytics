# Task 01 – Create Dockerfile and Build Image

## Objective

Implement the Dockerfile for your Python + Jupyter environment and build the Docker image.

## Instructions

1. Open the `docker/python/Dockerfile` created in Step 02.
2. Refine the Dockerfile so that it can actually be built:
   - Confirm the base image.
   - Install system dependencies.
   - Copy a `requirements.txt` file (you can create it from your package list).
   - Run `pip install -r requirements.txt`.
3. From the repository root (or the `docker/python/` folder), build the image using Docker.
4. Fix any errors that occur during the build until the image is created successfully.

## Checklist

- [ ] I have a working `Dockerfile` for Python + Jupyter.
- [ ] I have built the Docker image successfully.
- [ ] I have noted the image name and tag (e.g., `goodreads-analytics-python:latest`).

## Result

You now have a Docker image ready to be used for running Jupyter notebooks in a controlled environment.
