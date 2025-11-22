## Task 01 – Set Up `sql/` Folder and Query Conventions

### Objective
Create a clear **project structure and naming convention** for your SQL analysis scripts.

### Inputs
- Existing repository structure.
- Knowledge of the main business questions from Phase 04.

### Outputs / Deliverables
- A `sql/` folder at the project root (if not already present).  
- Subfolders and/or files grouped by topic (e.g., `sql/schema/`, `sql/analysis/`).  
- A short `README.md` in `sql/` explaining how scripts are organized and how to run them.

### Suggested Steps
1. **Create `sql/` folder structure**  
   - At the project root, create:  
     - `sql/schema/` for table DDL (CREATE TABLE, indexes).  
     - `sql/analysis/` for analytical queries.  
     - (Optional) `sql/utils/` for helper views or functions.

2. **Decide naming conventions**  
   - Examples:  
     - `01_create_books_table.sql`, `02_add_indexes_books.sql`.  
     - `10_top_authors_by_rating.sql`, `20_ratings_by_year.sql`.  
   - Prefer numbered prefixes so scripts appear in logical order.

3. **Create a `sql/README.md`**  
   - Describe:  
     - Purpose of the folder.  
     - How to run scripts (psql commands, order).  
     - Any dependencies (e.g., schema script before analysis scripts).

4. **Add a simple example script**  
   - For instance, under `sql/analysis/`, create a file like `00_sanity_checks.sql` with:  
     - `SELECT COUNT(*) FROM books;`  
     - `SELECT AVG(average_rating) FROM books;`  
     - And comments at the top explaining the goal.

5. **Version control check**  
   - Ensure new folders/files are tracked in Git.  
   - Consider adding `*.sql` formatting rules or settings if you use a formatter.

### Checklist
- [ ] `sql/` folder and subfolders created.  
- [ ] Naming convention for SQL scripts decided.  
- [ ] `sql/README.md` written with usage instructions.  
- [ ] At least one example analysis script created.  
- [ ] New SQL files added to version control.
