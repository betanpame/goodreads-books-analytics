## Task 01 – Implement Core Cleaning Pipeline in Python

### Objective

Translate the data quality rules from Phase 03 into a **reusable Python cleaning pipeline** that takes the raw `books.csv` (or raw books table) and returns a cleaned `DataFrame` ready for analysis.

### Inputs

- Raw Goodreads books data loaded into pandas (`DataFrame` from `books.csv` or from PostgreSQL).
- Data quality assessment and cleaning decisions from Phase 03 (missing values, outliers, duplicates, inconsistent formats, etc.).

### Outputs / Deliverables

- A Python module or analysis script section with a main function, e.g. `clean_books(df_raw) -> df_clean`.
- A list of clear, documented cleaning steps (module docstring or Markdown note in the analysis script or docstring).
- At least 3–5 small checks/prints/assertions that confirm the cleaning behaves as expected.

### Suggested Steps

1. **Create or reuse a analysis script for cleaning**

   - Open your main analysis analysis script (e.g., `02_analysis_and_visualizations.py`) or create a dedicated `01_cleaning_books.py`.
   - Import core libraries: `pandas`, `numpy` (optional), and any helpers you used before.

2. **Load the raw dataset**

   - Load `data/books.csv` or query the raw table from PostgreSQL into a `DataFrame` named `df_raw`.
   - Quickly inspect with `df_raw.head()`, `df_raw.info()`, and `df_raw.describe()` to refresh structure.

3. **Define a `clean_books` function**

   - In a code block, define a function such as:
     - `def clean_books(df: pd.DataFrame) -> pd.DataFrame:`
   - Inside this function, progressively apply the cleaning rules from Phase 03.

4. **Implement type casting and parsing**

   - Ensure numeric columns have numeric types: `average_rating`, `num_pages`, `ratings_count`, `text_reviews_count`.
   - Parse `publication_date` into a proper datetime column (`pd.to_datetime` with the correct format).
   - Optionally, derive `publication_year` as a separate integer column.

5. **Handle missing values**

   - Decide what to do with missing `average_rating`, `ratings_count`, `num_pages`, `language_code`, etc.
   - Common options: drop rows with critical fields missing or impute simple defaults (e.g., `0` for counts, `NaN` allowed but documented).
   - Add comments/markdown explaining why you choose each strategy.

6. **Deal with duplicates and near-duplicates**

   - Use `df.duplicated()` to detect exact duplicates.
   - Decide whether to drop duplicates based on `bookID`, `(title, authors)`, or another key.
   - Document how many rows were removed.

7. **Normalize text fields (optional but recommended)**

   - Strip extra spaces in `title`, `authors`, and `publisher`.
   - Consider lowercasing `language_code` and standardizing variations (e.g., `eng`, `en-US`).
   - Optionally, split `authors` on `/` into a list or main author column for later analysis.

8. **Handle outliers and extreme values**

   - Use simple filters to remove or flag impossible values (e.g., `num_pages <= 0`, `average_rating` outside `[0, 5]`, extremely high `ratings_count` if previously flagged).
   - Decide whether to **drop** these rows or keep them with a flag column (e.g., `is_outlier`).

9. **Return a cleaned DataFrame**

   - At the end of `clean_books`, return a copy of the cleaned data (`df_clean`).
   - Outside the function, call `df_clean = clean_books(df_raw)`.

10. **Add quick validation checks**

    - Print basic stats after cleaning: number of rows, proportion of missing values, min/max of key metrics.
    - Optionally, add a few `assert` statements, for example:
      - `assert df_clean["average_rating"].between(0, 5).all()`
      - `assert df_clean["num_pages"].min() > 0`

11. **Document your pipeline**
    - Add a module docstring or Markdown note summarizing each cleaning step in bullet points.
    - Briefly explain any important trade-offs (e.g., why you chose to drop some rows instead of imputing values).

### Checklist

- [ ] Raw dataset loaded into `df_raw`.
- [ ] `clean_books(df)` function created.
- [ ] Types converted and dates parsed.
- [ ] Missing values handled with clear strategy.
- [ ] Duplicates and obvious outliers addressed.
- [ ] Validation checks added (prints or asserts).
- [ ] Cleaning steps documented in markdown.
