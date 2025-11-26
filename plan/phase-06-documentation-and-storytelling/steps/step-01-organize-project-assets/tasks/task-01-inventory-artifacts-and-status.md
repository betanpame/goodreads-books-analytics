## Task 01 – Inventory Notebooks, SQL, Data, and Figures

### Objective

Create a clear inventory of all the **project assets** (notebooks, SQL scripts, datasets, figures) and decide which ones are ready for the portfolio and which ones still need work.

### Outputs

- A markdown table listing each asset with: `Name`, `Path`, `Type`, `Purpose`, `Status` (e.g., "keep & polish", "archive").
- A short list of assets you will focus on polishing in this phase.

### Steps

1. **Scan the repository structure**

   - Look at the main folders: `notebooks/` (if present), `data/`, `sql/`, `figures/`, `docs/`, `plan/`.
   - If notebooks are still in the root or another folder, note their locations.

2. **List all notebooks**

   - For each `*.ipynb`, record:
     - File name (e.g., `01_eda_books.ipynb`).
     - Folder path.
     - Brief purpose (EDA, cleaning, analysis, SQL comparison, etc.).

3. **List all SQL scripts**

   - Under `sql/`, list files in `schema/`, `analysis/`, and any other subfolders.
   - For each script, note whether it is DDL (schema), sanity checks, or analysis.

4. **List datasets and derived data**

   - Under `data/`, identify:
     - Raw files (e.g., `data/books.csv`).
     - Derived files (e.g., `data/derived/books_clean.csv`).

5. **List figures and visual outputs**

   - Under `figures/`, list all image files (e.g., `fig_top_authors_by_rating.png`).
   - Note which figures correspond to key insights.

6. **Create an inventory table**

   - In a markdown file (e.g., `docs/phase-06-inventory.md`), create a table with columns:
     - `Name`
     - `Path`
     - `Type` (notebook / SQL / dataset / figure / doc)
     - `Purpose`
     - `Status` (keep & polish / archive / ignore for now).

7. **Mark focus assets**
   - Highlight 3–7 "focus" assets that you definitely want to show in your portfolio (e.g., main analysis notebook, best figures, key SQL queries).
   - Add a short note on why each is important.

### Checklist

- [ ] All notebooks listed with purpose.
- [ ] All SQL scripts listed and categorized.
- [ ] Raw and derived datasets identified.
- [ ] Figures listed and linked to insights.
- [ ] Inventory markdown file created with status for each asset.
- [ ] Focus assets for polishing clearly marked.
