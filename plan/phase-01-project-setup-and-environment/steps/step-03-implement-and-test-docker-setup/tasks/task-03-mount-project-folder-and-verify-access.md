# Task 03 – Mount Project Folder and Verify Access

## Objective

Ensure that your running Docker container can see and work with the `goodreads-books-analytics` project files.

## Instructions

1. When starting the container, mount the project folder from your host into the container (e.g., using a Docker volume or bind mount).
2. From within Jupyter, navigate the file browser and confirm that you can see the repository structure (including `data/`, `plan/`, `README.md`).
3. Create a simple test notebook inside the mounted folder and save it.
4. Check on your host machine that the new notebook file appears in the repository.

## Checklist

- [ ] I have mounted the project folder into the container.
- [ ] I can see project files from within Jupyter.
- [ ] I have created and saved a test notebook from inside the container.

## Result

Your Dockerized Jupyter environment is now fully integrated with your project files, ready for analysis.
