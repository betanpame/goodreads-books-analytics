-- Phase 05 · Step 02 · Task 02
-- M7 + M8 – Publication-year trends for average rating and median engagement.
-- Run inside psql: \i sql/analysis/40_publication_year_trends.sql

WITH params AS (
    SELECT 1950::int AS min_year
),
books_with_canonical AS (
    SELECT
        b.book_id,
        COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
        b.title,
        b.average_rating,
        b.language_code,
        b.publication_date,
        b.ratings_count,
        b.text_reviews_count,
        EXTRACT(YEAR FROM b.publication_date)::int AS publication_year
    FROM books AS b
    LEFT JOIN bookid_canonical_map AS m
        ON b.book_id = m."duplicate_bookID"
),
representatives AS (
    SELECT DISTINCT ON (canonical_book_id)
        canonical_book_id,
        book_id AS representative_book_id,
        average_rating,
        language_code,
        publication_date,
        publication_year
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
        r.publication_year,
        r.average_rating,
        GREATEST(0, LEAST(COALESCE(e.ratings_count, 0), 597244)) AS ratings_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
)
SELECT
    publication_year,
    ROUND(AVG(average_rating)::numeric, 4) AS average_rating,
    ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY ratings_count_capped)::numeric, 0) AS median_ratings_count_capped,
    COUNT(*) AS canonical_book_count
FROM canonical_metrics, params
WHERE publication_year IS NOT NULL
  AND publication_year >= params.min_year
GROUP BY publication_year
ORDER BY publication_year;
