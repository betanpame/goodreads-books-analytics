## Task 02 – Add Task Runner or Convenience Scripts (Optional)

### Objective

Provide **simple commands** to perform common actions (run pipeline, tests, checks) without remembering long commands.

### Outputs

- A task runner configuration (Makefile, PowerShell script in `scripts/`, or similar).

### Steps

1. **Choose a task mechanism**

   - Options:
     - `Makefile` (if you are comfortable with `make`).
     - PowerShell script (e.g., `scripts/run_all.ps1`) for Windows.
     - A simple Python CLI script that dispatches commands.

2. **Define key tasks**

   - At minimum, include:
     - Run full pipeline.
     - Run tests.
     - Run data quality checks.
     - (Optional) Start Docker services.

3. **Implement tasks**

   - For example, in `Makefile` or `run_all.ps1`, add commands that wrap:
     - `python src/run_full_pipeline.py`
     - `pytest`
     - `python -m src.check_data_quality`.

4. **Document usage**
   - Add a small section in README describing these convenience commands and their purpose.

### Checklist

- [ ] Task runner approach chosen.
- [ ] Core tasks (pipeline, tests, checks) implemented.
- [ ] Commands tested.
- [ ] Usage documented in README.
