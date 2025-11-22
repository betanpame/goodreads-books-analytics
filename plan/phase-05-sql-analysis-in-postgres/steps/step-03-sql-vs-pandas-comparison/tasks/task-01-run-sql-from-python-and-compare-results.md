## Task 01 – Run SQL from Python and Compare Results

### Objective
Execute your SQL analysis queries from Python, load results into pandas, and compare them directly with the pandas-based metrics from Phase 04.

### Inputs
- Working SQL analysis scripts in `sql/analysis/`.
- Python environment with `sqlalchemy` (or similar) configured.
- Pandas summary tables from Phase 04.

### Outputs / Deliverables
- A notebook section (or a dedicated notebook) that:  
  - Runs selected SQL files/queries.  
  - Loads results into pandas DataFrames.  
  - Compares them with existing pandas outputs.  
- Notes on any differences and reflections on using SQL vs pandas.

### Suggested Steps
1. **Set up database connection in Python**  
   - Use `create_engine` from `sqlalchemy` or a direct driver.  
   - Test with a simple query, e.g., `SELECT COUNT(*) FROM books;`.

2. **Choose 2–3 core analyses to compare**  
   - For example:  
     - Top authors by rating.  
     - Top books by engagement.  
     - Ratings by publication year.

3. **Run SQL and load into pandas**  
   - For each chosen analysis:  
     - Either read the `.sql` file content or embed the query as a string.  
     - Use `pd.read_sql(query, con)` to get a DataFrame, e.g., `df_sql_top_authors`.

4. **Align and compare DataFrames**  
   - Ensure column names and filters match the pandas version (e.g., same thresholds).  
   - Compare:  
     - Row counts.  
     - Key values (e.g., top 5 authors, metrics).  
   - You can use simple checks like `df_sql.equals(df_pandas)` or more relaxed comparisons.

5. **Document differences and reflections**  
   - Note any mismatches and why they happen (e.g., rounding, filtering).  
   - Reflect on:  
     - Which tasks felt easier in SQL vs pandas.  
     - When you would choose SQL or pandas in a real project.

### Checklist
- [ ] Database connection from Python tested.  
- [ ] 2–3 analyses selected for comparison.  
- [ ] SQL results loaded into pandas DataFrames.  
- [ ] Comparisons performed and interpreted.  
- [ ] Reflections on SQL vs pandas written.
