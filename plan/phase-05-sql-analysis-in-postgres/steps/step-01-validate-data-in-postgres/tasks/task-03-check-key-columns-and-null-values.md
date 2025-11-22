## Task 03 – Check Key Columns and Null Values

### Objective
Understand the completeness and quality of key columns in the PostgreSQL `books` table by analyzing **nulls, distinct counts, and simple distributions**.

### Inputs
- `books` table in PostgreSQL.
- Knowledge of important columns from earlier phases (e.g., `average_rating`, `ratings_count`, `num_pages`, `language_code`, `publication_date`).

### Outputs / Deliverables
- A set of SQL queries that profile key columns.  
- Notes summarizing null rates and distinct value counts.  
- A short list of any data quality concerns relevant to SQL analysis.

### Suggested Steps
1. **Identify key columns**  
   - Make a short list: `bookID`, `title`, `authors`, `average_rating`, `ratings_count`, `num_pages`, `language_code`, `publication_date`, `publisher`.

2. **Write profiling queries**  
   - For each key column, write queries such as:  
     - `SELECT COUNT(*) FROM books WHERE column_name IS NULL;`  
     - `SELECT COUNT(DISTINCT column_name) FROM books;`  
   - For numeric columns, also compute min/max:  
     - `SELECT MIN(num_pages), MAX(num_pages) FROM books;`.

3. **Check basic distributions (optional)**  
   - Example queries:  
     - `SELECT language_code, COUNT(*) FROM books GROUP BY language_code ORDER BY COUNT(*) DESC LIMIT 10;`  
     - `SELECT publisher, COUNT(*) FROM books GROUP BY publisher ORDER BY COUNT(*) DESC LIMIT 10;`.

4. **Capture results and observations**  
   - Paste query results or summarize them in markdown:  
     - Null counts per column.  
     - Distinct counts where relevant (e.g., number of unique authors/publishers).  
   - Note any surprises (e.g., many missing `language_code`, extreme `num_pages`).

5. **Decide on implications for SQL analysis**  
   - Note which columns are safe to use in `GROUP BY`/aggregations.  
   - Note where you may want to filter out nulls or obvious outliers in SQL queries.

### Checklist
- [ ] Key columns list created.  
- [ ] Profiling queries written and run.  
- [ ] Null counts and distinct counts summarized.  
- [ ] Basic distribution queries (language/publisher) executed.  
- [ ] Implications for future SQL analysis documented.
