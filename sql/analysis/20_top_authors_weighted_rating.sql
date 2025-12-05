-- Phase 05 · Step 02 · Task 02
-- M1 – Weighted author leaderboard matching the pandas core metric.
-- Run inside psql: \i sql/analysis/20_top_authors_weighted_rating.sql

WITH params AS (
    SELECT
        5000::bigint AS min_total_ratings,
        15::int AS top_n
),
books_base AS (
    SELECT
        book_id,
        canonical_book_id,
        average_rating,
        ratings_count
    FROM books_clean
    WHERE average_rating IS NOT NULL
      AND ratings_count > 0
),
author_rollup AS (
    SELECT
        a.author_name,
        SUM(b.average_rating * b.ratings_count) AS weighted_rating_sum,
        SUM(b.ratings_count) AS total_ratings,
        COUNT(DISTINCT b.canonical_book_id) AS book_count
    FROM book_authors_stage AS a
    JOIN books_base AS b
        ON a.book_id = b.book_id
    WHERE
        a.author_name IS NOT NULL
    GROUP BY a.author_name
)
SELECT
    author_name,
    ROUND((weighted_rating_sum / NULLIF(total_ratings, 0))::numeric, 4) AS weighted_average_rating,
    total_ratings,
    book_count
FROM author_rollup
WHERE total_ratings >= (SELECT min_total_ratings FROM params)
ORDER BY weighted_average_rating DESC, total_ratings DESC
LIMIT (SELECT top_n FROM params);
