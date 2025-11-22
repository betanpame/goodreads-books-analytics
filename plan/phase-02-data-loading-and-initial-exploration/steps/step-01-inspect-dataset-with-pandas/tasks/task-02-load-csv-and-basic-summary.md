# Task 02 – Load CSV and Basic Summary

## Objective

Load the `books.csv` file using pandas and compute basic summary statistics to understand the dataset at a high level.

## Instructions

1. In `01_initial_inspection_books.ipynb`, import the necessary libraries:
   - `import pandas as pd`
2. Load the CSV file:
   - Use a relative path like `../data/books.csv` (depending on where your notebook lives).
   - Consider specifying `encoding` if needed (e.g., `encoding="utf-8"`).
3. Display basic information:
   - First rows (`head()`).
   - Last rows (`tail()`).
   - `.info()` to see column types and non-null counts.
   - `.describe()` for numeric columns.
4. Note any immediate observations in markdown cells (e.g., which columns have many missing values, unusual ranges, etc.).

## Checklist

- [ ] I can successfully load `books.csv` into a pandas DataFrame.
- [ ] I have run `head()`, `tail()`, `.info()`, and `.describe()`.
- [ ] I have written at least a few bullet points with initial observations.

## Result

You have a basic understanding of the size, structure, and numeric ranges in the dataset.
