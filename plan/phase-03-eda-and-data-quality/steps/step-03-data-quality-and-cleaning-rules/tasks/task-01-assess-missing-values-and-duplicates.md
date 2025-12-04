# Task 01 – Assess Missing Values and Duplicates

## Objective

Quantify missing data and identify potential duplicate or near-duplicate records.

## Instructions

1. In your EDA analysis script, compute missing values:
   - Use `df.isna().sum()` to see missing counts per column.
   - Compute the percentage of missing entries for each column.
2. Investigate duplicates:
   - Use `df.duplicated().sum()` to see full-row duplicates.
   - Explore possible partial duplicates using subsets of columns, such as `['title', 'authors', 'publication_date']`.
3. Create a small table or markdown section summarizing:
   - Columns with high missingness and possible reasons.
   - How many duplicates exist and what patterns they follow (e.g., same book different edition).

## Checklist

- [ ] I have computed missing values per column and their percentages.
- [ ] I have checked for full-row duplicates.
- [ ] I have explored potential partial duplicates.
- [ ] I have summarized findings in markdown.

## Result

You have a clear picture of missing data and duplicate patterns, which you will address with cleaning rules.
