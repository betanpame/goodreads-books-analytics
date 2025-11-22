# Task 03 – Explore Categorical Distributions

## Objective

Understand the distribution of key categorical variables in the dataset.

## Instructions

1. Focus on categorical-like columns such as:
   - `authors` (may contain multiple authors delimited by `/`)
   - `publisher`
   - `language_code`
   - (Optionally) derived features later, such as main genre inferred from title.
2. For `language_code`:
   - Compute value counts and visualize the top N languages.
3. For `publisher`:
   - Compute value counts.
   - Plot the top 10–20 publishers by number of books.
4. For `authors` (for now, treat the full string as a category):
   - Compute value counts and inspect the top authors by number of books.
5. Write markdown commentary about:
   - Which languages dominate.
   - Which publishers and authors are most represented.
   - Any surprising patterns (e.g., many one-off publishers).

## Checklist

- [ ] I have computed value counts for `language_code`, `publisher`, and `authors`.
- [ ] I have created bar plots for top categories where appropriate.
- [ ] I have written interpretations for key categorical distributions.

## Result

You understand which authors, publishers, and languages are most common in the dataset, providing context for later analyses.
