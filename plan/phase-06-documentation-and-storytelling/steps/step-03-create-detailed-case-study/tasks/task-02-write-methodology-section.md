## Task 02 – Write Methodology Section

### Objective

Explain **how** you approached the analysis in a way that demonstrates your thinking and technical skills.

### Outputs

- A fleshed-out "Methodology" section in `docs/case-study-goodreads-books.md` (or similar).

### Steps

1. **Summarize overall workflow**

   - Briefly describe the major phases:
     - Environment setup (Docker, Postgres).
     - Data loading (CSV to pandas and PostgreSQL).
     - EDA and data quality assessment.
     - Cleaning and feature preparation.
     - Metrics, visualization, and SQL replication.

2. **Describe EDA approach**

   - Explain what kinds of plots and statistics you used.
   - Mention key libraries (`pandas`, `matplotlib`, `seaborn`).
   - Note how EDA informed later cleaning and metrics.

3. **Describe cleaning and transformation**

   - Summarize main cleaning rules:
     - Handling missing values.
     - Removing or flagging outliers.
     - Parsing dates and deriving `publication_year`.
     - Standardizing `language_code` and text fields.

4. **Describe metrics and visual analysis**

   - Explain how you defined metrics (e.g., top authors, engagement, trends).
   - Mention how you implemented them in pandas and then in SQL.

5. **Describe SQL analysis**

   - Explain why you moved analyses into PostgreSQL.
   - Highlight use of `GROUP BY`, `HAVING`, and window functions for advanced questions.

6. **Emphasize reproducibility**
   - Note how scripts, notebooks, Docker, and SQL together make the analysis reproducible.

### Checklist

- [ ] Methodology section drafted in the case study file.
- [ ] EDA, cleaning, metrics, and SQL all described.
- [ ] Reproducibility considerations mentioned.
- [ ] Section reads clearly for a technical audience.
