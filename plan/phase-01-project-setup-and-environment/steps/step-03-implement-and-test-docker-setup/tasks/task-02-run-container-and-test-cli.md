# Task 02 – Run Container and Test CLI Execution

## Objective

Run the Python CLI Docker container and confirm that you can execute project scripts from within it.

## Instructions

1. Start the Python CLI container defined in `docker-compose.python.yml`. Two useful patterns:

   - **One-off execution** (runs a single command, then removes the container):

     ```powershell
     docker compose -f docker-compose.python.yml run --rm app python -m src.analyses.initial_inspection_books --sample-size 100
     ```

   - **Persistent services** (start everything in the background, then exec into the container):

     ```powershell
     docker compose -f docker-compose.python.yml up -d
     docker compose -f docker-compose.python.yml exec app bash
     ```

2. From inside the container (either via the exec shell or by issuing additional `docker compose run` commands), run quick smoke tests:
   - `python --version`
   - `python -m src.run_full_pipeline --help`
   - Optional: `python -m src.analyses.initial_inspection_books --sample-size 100`
3. Confirm that the commands succeed and that `/app` contains the repository files.
4. When finished, exit the shell and stop the services if they are still running:

   ```powershell
   docker compose -f docker-compose.python.yml down
   ```

## Checklist

- [ ] I have started the `app` container via `docker compose`.
- [ ] I successfully ran at least one project module (for example `python -m src.run_full_pipeline --help`).
- [ ] Repository files were accessible inside the container via `/app`.

## Result

You have verified that the Dockerized environment can execute the same CLI scripts you will rely on throughout the project.
