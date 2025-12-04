## Task 01 – Inventory Reproducible vs Manual Workflows

### Objective

Identify which parts of your current workflow are **scripted and reproducible** and which are still manual or ad hoc.

### Outputs

- A markdown summary (e.g., `docs/phase-07-inventory.md`) listing main workflows and their status.

### Steps

1. **List main workflows**

   - Examples:
     - Environment setup (Docker, virtualenv).
     - CSV → pandas loading.
     - CSV → PostgreSQL loading.
     - Data cleaning.
     - Metric computation and visualizations.
     - SQL analysis in PostgreSQL.

2. **Classify each workflow**

   - For each workflow, mark it as:
     - "Scripted" (can be run via script or single command).
     - "Partially scripted" (some scripts, some manual steps).
     - "Manual" (mostly done by clicking/typing in analysis scripts or tools).

3. **Describe current implementation briefly**

   - Add 1–2 sentences per workflow explaining how you currently perform it (e.g., "Load CSV by running a helper function inside `src/analyses/01_eda_books.py`", "Run `to_sql` in a one-off script").

4. **Highlight gaps and pain points**
   - Note where manual steps are slow, error-prone, or hard to remember.
   - These will be targets for scripting in later tasks.

### Checklist

- [ ] All major workflows listed.
- [ ] Each workflow labeled as Scripted / Partially Scripted / Manual.
- [ ] Short description written for each workflow.
- [ ] Pain points and gaps identified.
