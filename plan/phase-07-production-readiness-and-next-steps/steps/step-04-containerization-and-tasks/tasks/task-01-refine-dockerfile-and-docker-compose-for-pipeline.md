## Task 01 – Refine Dockerfile and docker-compose for Pipeline

### Objective

Update your Docker setup so that it can run **not only Python CLI workflow**, but also the data pipeline scripts inside containers.

### Outputs

- Updated Dockerfile(s) and `docker-compose.yml` that include the pipeline scripts and dependencies.

### Steps

1. **Review current Docker setup**

   - Open existing Docker-related files (Dockerfile, `docker-compose.yml`).
   - Note which services exist (e.g., `app`, `db`) and what they currently do.

2. **Ensure `src/` and `tests/` are included**

   - Update the Dockerfile for the Python service to:
     - Copy `src/`, `tests/`, and other necessary files into the image.
     - Install required dependencies.

3. **Add pipeline command capability**

   - In `docker-compose.yml`, verify you can run commands like:
     - `docker compose run app python src/run_full_pipeline.py`.
   - Optionally define a service or profile specifically for running the pipeline.

4. **Test running pipeline inside container**

   - Start necessary services (`docker compose up db`, etc.).
   - Run the pipeline command inside the container and confirm it completes successfully.

5. **Update docs**
   - In README or a separate doc, add examples for running the pipeline through Docker.

### Checklist

- [ ] Dockerfile updated to include pipeline code and deps.
- [ ] `docker-compose.yml` supports pipeline commands.
- [ ] Pipeline tested inside container.
- [ ] Documentation updated with Docker usage for pipeline.
