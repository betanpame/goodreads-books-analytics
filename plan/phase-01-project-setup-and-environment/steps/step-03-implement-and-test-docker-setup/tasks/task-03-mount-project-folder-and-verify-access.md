# Task 03 – Mount Project Folder and Verify Access

## Objective

Ensure that your running Docker container can see and work with the `goodreads-books-analytics` project files.

## Instructions

1. When starting the container, mount the project folder from your host into the container (e.g., using a Docker volume or bind mount).
2. From within the running container shell, list the repository contents (confirm `data/`, `plan/`, `README.md`, etc. are visible under `/app`).
3. Create a simple test analysis script inside the mounted folder using the container shell and save/run it.
4. Check on your host machine that the new analysis script file appears in the repository.

## Checklist

- [ ] I have mounted the project folder into the container.
- [ ] I can list the repository contents from inside the container shell.
- [ ] I have created and saved a test analysis script from inside the container and confirmed it exists on the host.

## Result

Your Dockerized Python CLI workflow environment is now fully integrated with your project files, ready for analysis.
