# Task 03 – Explore Key Columns and Types

## Objective

Look more closely at specific columns that are important for later analysis and schema design.

## Instructions

1. In your notebook, focus on these key columns:
   - `bookID`
   - `title`
   - `authors`
   - `average_rating`
   - `num_pages`
   - `ratings_count`
   - `text_reviews_count`
   - `publication_date`
   - `publisher`
   - `language_code`
2. For each column, explore:
   - Example values (`df[column].head()`).
   - Data type as reported by pandas.
   - Number of unique values (`nunique()`).
   - Number of missing values (`isna().sum()`).
3. For `publication_date`, try parsing it as a datetime column using `pd.to_datetime` and note any parsing issues.
4. For `authors`, note that multiple authors are separated by `/`. Write down an idea of how you might handle this later (even if you do not implement it yet).
5. Document your findings in markdown cells.

## Checklist

- [ ] I have examined example values, data types, and missing counts for key columns.
- [ ] I have attempted to parse `publication_date` as a datetime.
- [ ] I have written ideas for handling multiple authors and other complexities.

## Result

You have a deeper understanding of the most important columns, which will guide schema design and later EDA.
