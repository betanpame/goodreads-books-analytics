## Task 01 – Define Business Questions and Metrics

### Objective

Translate the project goals into a **clear list of business questions** and **quantitative metrics** that can be computed from the Goodreads books dataset.

### Inputs

- Cleaned books dataset from Step 01 (`df_clean`).
- EDA findings and data quality notes from Phase 03.

### Outputs / Deliverables

- A markdown section (in the analysis script or a separate `.md` file) listing 5–8 key business questions.
- For each question, a set of 1–3 specific metrics with a short description.
- A simple table (could be Markdown) mapping: `Question -> Metric -> Columns needed -> Notes`.

### Suggested Business Question Areas

Feel free to adapt these to your interests:

- **Top-performing books and authors**
- **Reader engagement** (ratings counts, text reviews).
- **Role of book length** (num_pages) in ratings and popularity.
- **Publication trends** over time (by year).
- **Languages and publishers** that dominate the catalog.

### Suggested Steps

1. **Review EDA findings**

   - Skim your EDA analysis script from Phase 03.
   - Note down patterns or questions that felt interesting or surprising.

2. **Draft 5–8 business questions**

   - Examples (adapt or rewrite in your own words):
     - "Which authors and publishers have the highest-rated books?"
     - "Do longer books tend to receive higher or lower ratings?"
     - "Which books generate the most reader engagement (ratings_count, text_reviews_count)?"
     - "How have average ratings changed over publication years?"
     - "Which languages have the highest average rating and engagement?"

3. **Define metrics for each question**

   - For each question, define measurable metrics. Examples:
     - Top authors by **average_rating** (with a minimum ratings_count threshold).
     - Top books by **ratings_count** and **text_reviews_count**.
     - Correlation or grouped summaries of **num_pages** vs **average_rating**.
     - Average rating and ratings_count by **publication_year**.
     - Aggregations by **language_code** and **publisher**.

4. **Create a mapping table**

   - In a module docstring or Markdown note, create a simple table with columns:
     - `Question`
     - `Metric(s)`
     - `Columns used` (e.g., `average_rating`, `ratings_count`, `authors`, `publication_year`, etc.).
     - `Notes` (e.g., thresholds, filters such as minimum ratings_count).

5. **Prioritize metrics**
   - Mark 3–5 **core metrics** that you definitely want to compute and visualize.
   - Mark remaining metrics as "nice to have" for later.

### Checklist

- [ ] EDA findings reviewed.
- [ ] 5–8 business questions written down.
- [ ] At least one metric defined per question.
- [ ] Mapping table `Question -> Metric -> Columns -> Notes` created.
- [ ] 3–5 core metrics prioritized for implementation.
