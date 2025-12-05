-- Phase 05 · Step 02 · Task 02
-- M1 – Weighted author leaderboard matching the pandas core metric.
-- Run inside psql: \i sql/analysis/20_top_authors_weighted_rating.sql

WITH params AS (
    SELECT
        5000::bigint AS min_total_ratings,
        15::int AS top_n
),
books_with_canonical AS (
    SELECT
        b.book_id,
        COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
        b.average_rating,
        b.ratings_count
    FROM books AS b
    LEFT JOIN bookid_canonical_map AS m
        ON b.book_id = m."duplicate_bookID"
),
author_rollup AS (
    SELECT
        a.author_name,
        SUM(b.average_rating * b.ratings_count) AS weighted_rating_sum,
        SUM(b.ratings_count) AS total_ratings,
        COUNT(DISTINCT b.canonical_book_id) AS book_count
    FROM book_authors_stage AS a
    JOIN books_with_canonical AS b
        ON a.book_id = b.book_id
    WHERE
        a.author_name IS NOT NULL
        AND b.average_rating IS NOT NULL
        AND b.ratings_count > 0
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
