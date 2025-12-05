-- Phase 05 · Step 02 · Task 02
-- M9 – Average rating and median engagement by language with coverage filters.
-- Run inside psql: \i sql/analysis/50_language_quality_summary.sql

WITH params AS (
    SELECT 50::int AS min_book_threshold
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
        language_code,
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
        r.language_code,
        r.average_rating,
        e.ratings_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
)
SELECT
    language_code,
    COUNT(*) AS canonical_book_count,
    ROUND(AVG(average_rating)::numeric, 4) AS average_rating,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY ratings_count_capped)::numeric AS median_ratings_count_capped
FROM canonical_metrics
WHERE language_code IS NOT NULL
GROUP BY language_code
HAVING COUNT(*) >= (SELECT min_book_threshold FROM params)
ORDER BY average_rating DESC, canonical_book_count DESC;
