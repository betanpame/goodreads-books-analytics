-- Phase 05 · Step 02 · Task 02
-- M9 – Average rating and median engagement by language with coverage filters.
-- Run inside psql: \i sql/analysis/50_language_quality_summary.sql

WITH params AS (
    SELECT 50::int AS min_book_threshold
),
books_with_canonical AS (
    SELECT
        b.book_id,
        COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
        b.title,
        b.average_rating,
        b.language_code,
        b.ratings_count
    FROM books AS b
    LEFT JOIN bookid_canonical_map AS m
        ON b.book_id = m."duplicate_bookID"
),
representatives AS (
    SELECT DISTINCT ON (canonical_book_id)
        canonical_book_id,
        language_code,
        average_rating
    FROM books_with_canonical
    ORDER BY canonical_book_id,
             CASE WHEN canonical_book_id = book_id THEN 0 ELSE 1 END,
             book_id
),
engagement_rollup AS (
    SELECT
        canonical_book_id,
        MAX(ratings_count) AS ratings_count
    FROM books_with_canonical
    GROUP BY canonical_book_id
),
canonical_metrics AS (
    SELECT
        r.canonical_book_id,
        r.language_code,
        r.average_rating,
        GREATEST(0, LEAST(COALESCE(e.ratings_count, 0), 597244)) AS ratings_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
)
SELECT
    language_code,
    COUNT(*) AS canonical_book_count,
    ROUND(AVG(average_rating)::numeric, 4) AS average_rating,
    ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY ratings_count_capped)::numeric, 0) AS median_ratings_count_capped
FROM canonical_metrics
WHERE language_code IS NOT NULL
GROUP BY language_code
HAVING COUNT(*) >= (SELECT min_book_threshold FROM params)
ORDER BY average_rating DESC, canonical_book_count DESC;
