## Task 02 – Standardize Folder Structure and Document It

### Objective

Make the repository structure **clear and predictable** so that a new person (or future you) can quickly understand where to find everything.

### Outputs

- A cleaned-up folder structure (no confusing duplicates or orphaned files).
- A short documentation file describing the structure and purpose of each main folder.

### Steps

1. **Review current structure and inventory**

   - Use the inventory from Task 01.
   - Identify any files that are misplaced (e.g., notebooks in random folders, figures mixed with data).

2. **Decide on target structure**

   - A reasonable structure might include:
     - `data/` – raw and derived datasets.
     - `notebooks/` – all Jupyter notebooks.
     - `sql/` – schema and analysis SQL scripts.
     - `src/` – Python modules and scripts.
     - `figures/` – exported charts and images.
     - `docs/` – documentation and case studies.
     - `plan/` – project planning documents (this folder).

3. **Move files into the target structure**

   - Relocate notebooks into `notebooks/` (create it if needed).
   - Ensure derived datasets live under `data/derived/` rather than next to raw data.
   - Group all images into `figures/` with meaningful names.

4. **Check for broken references (optional)**

   - If notebooks refer to file paths, update them where necessary (e.g., `../data/books.csv` instead of `books.csv`).

5. **Create a project structure document**

   - In `docs/project-structure.md`, describe:
     - Each top-level folder and its purpose.
     - Any naming conventions (e.g., `01_`, `02_` prefixes for notebooks).
   - Include a simplified tree view of the repo.

6. **Update README (if needed)**
   - If the existing README references old paths, adjust them to match the new structure.

### Checklist

- [ ] Target folder structure defined.
- [ ] Files moved into the correct folders.
- [ ] Derived vs raw data clearly separated.
- [ ] `docs/project-structure.md` created and filled.
- [ ] Any broken path references fixed.
