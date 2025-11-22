# Task 03 – Verify Row Counts and Samples

## Objective

Confirm that the data in PostgreSQL matches the CSV file in terms of row count and basic content.

## Instructions

1. In pandas, compute the number of rows in the DataFrame created from `books.csv`.
2. In PostgreSQL, run a query like `SELECT COUNT(*) FROM books;`.
3. Compare the counts; they should match. If not, investigate and document any differences.
4. Fetch a few sample rows from PostgreSQL (e.g., `SELECT * FROM books LIMIT 5;`) and compare them to samples from pandas to ensure fields look correct (especially dates and numeric values).
5. Note any issues or quirks you observe for later data quality analysis.

## Checklist

- [ ] I have compared row counts between pandas and PostgreSQL.
- [ ] I have visually compared a few sample rows.
- [ ] I have documented any discrepancies or concerns.

## Result

You have validated that the data has been loaded correctly into PostgreSQL, setting a solid foundation for SQL-based analysis.
