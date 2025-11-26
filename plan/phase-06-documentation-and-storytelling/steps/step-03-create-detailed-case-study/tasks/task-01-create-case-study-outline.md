## Task 01 – Create Case Study Outline

### Objective

Design a structured **case study outline** that tells the story of the project from business problem to insights and next steps.

### Outputs

- A markdown file `docs/case-study-outline.md` (or similar) with sections and bullet points.

### Steps

1. **Define main sections**

   - Include sections such as:
     - Introduction & Context.
     - Dataset Description.
     - Business Questions.
     - Methodology (EDA, cleaning, metrics, SQL).
     - Key Insights & Visuals.
     - Limitations.
     - Next Steps.

2. **Add 3–5 bullets under each section**

   - For each section, outline what you plan to cover.
   - Example for Methodology:
     - "Exploratory Data Analysis in pandas (univariate/bivariate)."
     - "Data cleaning rules implemented in Python."
     - "Translation of core metrics into SQL queries in PostgreSQL."

3. **Map sections to artifacts**

   - Next to bullets, note which notebooks, SQL scripts, or figures you will reference.
   - Example: `01_eda_books.ipynb`, `sql/analysis/10_top_authors_by_rating.sql`, `figures/fig_ratings_by_year.png`.

4. **Review flow and adjust**
   - Read the outline from top to bottom.
   - Ensure it flows logically as a narrative, not just a technical checklist.

### Checklist

- [ ] Case study outline file created in `docs/`.
- [ ] Sections defined with 3–5 bullets each.
- [ ] Each section mapped to relevant project artifacts.
- [ ] Outline reviewed for logical narrative flow.
