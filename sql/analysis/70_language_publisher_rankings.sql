-- Phase 05 · Step 02 · Task 03
-- Advanced pattern: language-level publisher standings using RANK and 75th-percentile engagement.
-- Run inside psql: \i sql/analysis/70_language_publisher_rankings.sql

WITH params AS (
    SELECT
        20::int AS min_canonical_books,
        5::int AS per_language_limit
),
books_with_canonical AS (
    SELECT
        b.book_id,
        COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
        b.title,
        b.average_rating,
        b.language_code,
        b.publisher,
        b.ratings_count
    FROM books AS b
    LEFT JOIN bookid_canonical_map AS m
        ON b.book_id = m."duplicate_bookID"
),
representatives AS (
    SELECT DISTINCT ON (canonical_book_id)
        canonical_book_id,
        book_id AS representative_book_id,
        title,
        average_rating,
        language_code,
        publisher
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
        r.publisher,
        r.average_rating,
        GREATEST(0, LEAST(COALESCE(e.ratings_count, 0), 597244)) AS ratings_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
    WHERE r.language_code IS NOT NULL
      AND r.publisher IS NOT NULL
),
publisher_summary AS (
    SELECT
        language_code,
        publisher,
        COUNT(*) AS canonical_book_count,
        ROUND(AVG(average_rating)::numeric, 4) AS average_rating,
        ROUND(percentile_cont(0.75) WITHIN GROUP (ORDER BY ratings_count_capped)::numeric, 0) AS engagement_p75
    FROM canonical_metrics
    GROUP BY language_code, publisher
),
eligible_publishers AS (
    SELECT
        ps.*
    FROM publisher_summary AS ps
    WHERE canonical_book_count >= (SELECT min_canonical_books FROM params)
),
ranked AS (
    SELECT
        ep.*,
        RANK() OVER (
            PARTITION BY language_code
            ORDER BY average_rating DESC, engagement_p75 DESC, canonical_book_count DESC
        ) AS language_rank
    FROM eligible_publishers AS ep
)
SELECT
        language_code,
        language_rank,
        publisher,
        canonical_book_count,
        average_rating,
        engagement_p75
FROM ranked
WHERE language_rank <= (SELECT per_language_limit FROM params)
ORDER BY language_code, language_rank;
