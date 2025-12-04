# Task 01 – Map Columns to SQL Types

## Objective

Decide appropriate PostgreSQL data types for each column in `books.csv`.

## Instructions

1. Based on your pandas exploration, create a mapping table (in a markdown file or your analysis script) with columns:
   - `column_name`
   - `example_values`
   - `pandas_dtype`
   - `proposed_postgres_type`
2. Suggested starting points:
   - `bookID` → `INTEGER` or `BIGINT` (primary key candidate).
   - `title` → `TEXT`.
   - `authors` → `TEXT`.
   - `average_rating` → `NUMERIC(3,2)` or `REAL`.
   - `isbn`, `isbn13` → `TEXT` (to preserve leading zeros).
   - `language_code` → `TEXT` or a small `VARCHAR`.
   - `num_pages` → `INTEGER`.
   - `ratings_count`, `text_reviews_count` → `INTEGER` or `BIGINT` if very large.
   - `publication_date` → `DATE`.
   - `publisher` → `TEXT`.
3. Pay attention to potential maximum lengths (for titles, publishers) and whether some columns might need indexing later.

## Checklist

- [ ] I have created a mapping from pandas dtypes to PostgreSQL types for all columns.
- [ ] I have noted any uncertainties or open questions about data types.

## Result

You now have a proposed set of SQL data types that will inform table creation.
