## Task 02 – Implement Metric Functions and Summary Tables

### Objective

Implement **reusable Python functions** that compute the metrics defined in Task 01 and return tidy summary tables (DataFrames) ready for visualization.

### Inputs

- Cleaned books dataset `df_clean`.
- Business questions and metric definitions from Task 01.

### Outputs / Deliverables

- A set of Python functions like `top_authors_by_rating`, `top_books_by_engagement`, etc.
- 3–5 summary `DataFrame` objects (e.g., `df_top_authors`, `df_top_books`, `df_ratings_by_year`, `df_language_stats`).
- Optional: Saved CSV/Parquet versions of these summary tables in a `data/derived/` folder.

### Suggested Steps

1. **Set up a metrics section or module**

   - In your main analysis notebook, create a section (markdown heading) called `Metrics and Summary Tables`.
   - Alternatively, create a Python module like `src/metrics.py` and import it into the notebook.

2. **Implement functions for each core metric**

   - Examples (adapt names and details to your design):
     - `def top_authors_by_avg_rating(df, min_ratings=1000, top_n=20)`
     - `def top_books_by_engagement(df, top_n=20)`
     - `def ratings_by_publication_year(df, min_year=1950)`
     - `def language_and_publisher_stats(df, min_books=50)`
   - Each function should:
     - Take `df_clean` (or a subset) as input.
     - Apply necessary filters (e.g., minimum ratings_count).
     - Group, aggregate, and sort to produce a compact summary `DataFrame`.

3. **Create and inspect summary tables**

   - Call your functions and assign results to variables, such as:
     - `df_top_authors = top_authors_by_avg_rating(df_clean, min_ratings=5000, top_n=15)`
     - `df_top_books = top_books_by_engagement(df_clean, top_n=20)`
     - `df_ratings_by_year = ratings_by_publication_year(df_clean)`
   - Display `.head()` for each table and check that columns and values make sense.

4. **Optionally persist summary tables**

   - Create a `data/derived/` folder if it does not exist.
   - Save key summary tables as CSV or Parquet, e.g.:
     - `df_top_authors.to_csv("data/derived/top_authors_by_rating.csv", index=False)`
     - `df_ratings_by_year.to_csv("data/derived/ratings_by_year.csv", index=False)`.

5. **Document metric definitions near the code**
   - Add docstrings to each function describing:
     - Inputs and parameters.
     - Aggregations performed.
     - What the output `DataFrame` represents.
   - Optionally, link back to the mapping table from Task 01.

### Checklist

- [ ] Metrics section or module created.
- [ ] Functions implemented for each core metric.
- [ ] Summary tables generated and inspected.
- [ ] (Optional) Summary tables saved under `data/derived/`.
- [ ] Functions documented with clear docstrings.
