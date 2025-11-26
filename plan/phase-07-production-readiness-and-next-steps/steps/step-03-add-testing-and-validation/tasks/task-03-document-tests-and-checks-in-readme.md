## Task 03 – Document Tests and Checks in README

### Objective

Make testing and data quality checks a **visible, documented part** of the project workflow.

### Outputs

- A "Testing and Data Quality" section in `README.md` (or a linked doc) with clear commands.

### Steps

1. **List available tests and checks**

   - Unit tests for cleaning logic.
   - Data quality check script(s).
   - Any manual checks you still consider important.

2. **Write documentation section**

   - In README, add a section describing:
     - What each test/check validates.
     - When to run them (e.g., before running the pipeline, before committing).
   - Include command examples in PowerShell blocks, for example:

   ```powershell
   # Run unit tests
   pytest

   # Run data quality checks
   python -m src.check_data_quality
   ```

3. **Emphasize benefit for collaborators**

   - Add 1–2 sentences on why these checks exist (catching issues early, ensuring consistent results).

4. **Link to more detailed docs (optional)**
   - If you created `docs/data-quality.md` or similar, link to it from README.

### Checklist

- [ ] All tests and checks listed.
- [ ] README section written with commands.
- [ ] Explanation of when/why to run checks added.
- [ ] Links to any detailed docs included.
