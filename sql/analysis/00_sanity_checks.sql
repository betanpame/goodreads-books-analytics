-- Quick Postgres sanity checks to prove the books table loaded correctly.
-- Run with: \i sql/analysis/00_sanity_checks.sql (from repo root inside psql)

\echo 'Row count should match the CSV (11,119 rows)'
SELECT COUNT(*) AS total_books
FROM books;

\echo 'Average rating stays within the 0-5 profiling window'
SELECT ROUND(AVG(average_rating), 4) AS avg_rating
FROM books;

\echo 'Top 5 languages by book count (helps validate category distributions)'
SELECT language_code,
       COUNT(*) AS book_count
FROM books
GROUP BY language_code
ORDER BY book_count DESC
LIMIT 5;
