## Task 03 – Explore Advanced SQL Patterns (Window Functions)

### Objective
Practice **intermediate SQL patterns**, especially window functions, to answer more nuanced questions about the Goodreads books data.

### Inputs
- `books` table in PostgreSQL.
- Basic analytical queries already implemented in Task 02.

### Outputs / Deliverables
- At least 2–3 SQL queries using window functions (e.g., `ROW_NUMBER`, `RANK`, `AVG() OVER`).  
- Scripts saved under `sql/analysis/` with clear comments.  
- Notes on what each window function is doing and why it’s useful.

### Suggested Steps
1. **Pick questions suited for window functions**  
   - Examples:  
     - "What are the top 3 books by rating **per author**?"  
     - "How do average ratings evolve year-over-year?" (rolling averages).  
     - "Within each language, which publishers have the highest average ratings?".

2. **Design window-based queries**  
   - For top-N per group, consider patterns like:  
     - `ROW_NUMBER() OVER (PARTITION BY authors ORDER BY average_rating DESC)`.
   - For rolling trends, consider:  
     - `AVG(average_rating) OVER (ORDER BY publication_year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.

3. **Create SQL files for advanced queries**  
   - Examples:  
     - `50_top_books_per_author.sql`  
     - `60_rolling_avg_rating_by_year.sql`.

4. **Write and run the queries**  
   - Include comments at the top explaining:  
     - The business question.  
     - Why a window function is used instead of a simple `GROUP BY`.  
   - Execute them and inspect results, focusing on whether rankings and rolling averages look reasonable.

5. **Document learnings**  
   - In a markdown file or notebook, briefly explain:  
     - What each window function does in your queries.  
     - Any gotchas you encountered (ordering, partitions, performance).

### Checklist
- [ ] At least 2–3 questions chosen for window-function analysis.  
- [ ] SQL files created under `sql/analysis/` for advanced queries.  
- [ ] Queries using `OVER (PARTITION BY ...)` or similar patterns implemented.  
- [ ] Results inspected and validated.  
- [ ] Notes on window functions and learnings written.
