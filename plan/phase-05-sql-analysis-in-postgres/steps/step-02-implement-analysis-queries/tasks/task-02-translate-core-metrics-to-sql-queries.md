## Task 02 – Translate Core Metrics to SQL Queries

### Objective
Implement SQL queries that reproduce the **core business metrics** you previously computed in pandas (Phase 04).

### Inputs
- Cleaned data stored in PostgreSQL (or raw `books` table with filters applied in SQL).
- Core metrics definitions from Phase 04 (e.g., top authors, top books, ratings by year, language/publisher stats).

### Outputs / Deliverables
- One SQL file per major analysis theme under `sql/analysis/` (e.g., `10_top_authors_by_rating.sql`, `20_top_books_by_engagement.sql`).  
- Queries that can be run standalone in a SQL client.  
- Inline comments explaining each query.

### Suggested Steps
1. **Review core metrics from Phase 04**  
   - Look at the metric functions and summary tables you built in pandas.  
   - List at least 3–5 metrics you want to reproduce in SQL.

2. **Design SQL equivalents**  
   - For each metric, write down the needed operations:  
     - Filters (e.g., `ratings_count >= 1000`).  
     - Grouping keys (e.g., `authors`, `publisher`, `publication_year`).  
     - Aggregations (e.g., `AVG(average_rating)`, `SUM(ratings_count)`).  
     - Sorting and limits (e.g., `ORDER BY AVG(average_rating) DESC LIMIT 20`).

3. **Create themed SQL files**  
   - Examples:  
     - `10_top_authors_by_rating.sql`: top authors with minimum `ratings_count`.  
     - `20_top_books_by_engagement.sql`: books ranked by `ratings_count` and `text_reviews_count`.  
     - `30_ratings_by_publication_year.sql`: average rating and engagement per year.  
     - `40_language_and_publisher_stats.sql`: aggregates by `language_code` and `publisher`.

4. **Write queries with comments**  
   - At the top of each file, add a header comment explaining:  
     - Business question.  
     - Any filters or thresholds.  
   - Then write the `SELECT` statement(s) implementing the metric.

5. **Run and verify queries**  
   - Execute each script in your SQL client.  
   - Inspect results: column names, order, and values should match your expectations from pandas.  
   - Adjust filters and grouping logic as needed.

### Checklist
- [ ] Core metrics list reviewed from Phase 04.  
- [ ] SQL design (filters, groups, aggregations) written down.  
- [ ] Separate SQL files created for each theme.  
- [ ] Queries written with clear comments.  
- [ ] Queries executed and results verified.
