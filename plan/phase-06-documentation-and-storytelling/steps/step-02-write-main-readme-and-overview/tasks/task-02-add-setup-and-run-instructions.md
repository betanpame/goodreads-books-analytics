## Task 02 – Add Setup and Run Instructions to README

### Objective

Document how to **set up the environment and run the project** so that others can reproduce your work.

### Outputs

- A "Setup" or "Getting Started" section in `README.md`.
- A "How to Run" section with concrete, copy-pasteable commands.

### Steps

1. **List prerequisites**

   - Mention tools and versions you expect:
     - Python (version range).
     - Docker Desktop (if using).
     - PostgreSQL (local or via Docker).
   - Note any recommended extensions (e.g., VS Code Python, Jupyter).

2. **Describe environment setup**

   - Provide instructions for:
     - Cloning the repository.
     - Creating/activating a virtual environment (if applicable).
     - Installing dependencies (`pip install -r requirements.txt` or similar).
   - If using Docker, explain how to build and start containers.

3. **Explain how to load data**

   - Briefly describe where `data/books.csv` comes from and how to place it in the project.
   - Reference any scripts or notebooks that load the CSV into pandas and/or PostgreSQL.

4. **Document how to run main analyses**

   - Provide step-by-step instructions for:
     - Opening Jupyter (via VS Code or browser).
     - Running the main notebooks in order (EDA → cleaning → analysis → SQL comparison).
   - Include PowerShell code blocks for common commands, for example:

   ```powershell
   # Start environment (example)
   docker compose up

   # Run analysis notebook (example command if using jupyter lab)
   jupyter lab
   ```

5. **Add troubleshooting tips (optional)**
   - Note common issues (e.g., connection errors to PostgreSQL, missing data file) and how to resolve them.

### Checklist

- [ ] Prerequisites clearly listed.
- [ ] Environment setup steps written.
- [ ] Data loading instructions included.
- [ ] Main analysis run instructions documented with commands.
- [ ] (Optional) Troubleshooting tips added.
