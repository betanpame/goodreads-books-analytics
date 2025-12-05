-- Phase 05 · Step 02 · Task 02
-- M7 + M8 – Publication-year trends for average rating and median engagement.
-- Run inside psql: \i sql/analysis/40_publication_year_trends.sql

WITH params AS (
    SELECT 1950::int AS min_year
),
ranked_books AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY canonical_book_id
            ORDER BY is_duplicate, book_id
        ) AS canonical_rank
    FROM books_clean
    WHERE canonical_book_id IS NOT NULL
),
representatives AS (
    SELECT
        canonical_book_id,
        publication_year,
        average_rating
    FROM ranked_books
    WHERE canonical_rank = 1
),
engagement_rollup AS (
    SELECT
        canonical_book_id,
        MAX(ratings_count_capped) AS ratings_count_capped
    FROM books_clean
    GROUP BY canonical_book_id
),
canonical_metrics AS (
    SELECT
        r.canonical_book_id,
        r.publication_year,
        r.average_rating,
        e.ratings_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
)
SELECT
    publication_year,
    ROUND(AVG(average_rating)::numeric, 4) AS average_rating,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY ratings_count_capped)::numeric AS median_ratings_count_capped,
    COUNT(*) AS canonical_book_count
FROM canonical_metrics, params
WHERE publication_year IS NOT NULL
  AND publication_year >= params.min_year
GROUP BY publication_year
ORDER BY publication_year;
