-- Phase 05 · Step 02 · Task 02
-- M3 + M4 – Canonical book leaderboards by ratings_count and text_reviews_count.
-- Run inside psql: \i sql/analysis/30_top_books_by_engagement.sql

WITH params AS (
    SELECT 20::int AS top_n
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
        book_id AS representative_book_id,
        title,
        average_rating,
        language_code,
        publication_date
    FROM ranked_books
    WHERE canonical_rank = 1
),
engagement_rollup AS (
    SELECT
        canonical_book_id,
        MAX(ratings_count) AS ratings_count,
        MAX(ratings_count_capped) AS ratings_count_capped,
        MAX(text_reviews_count) AS text_reviews_count,
        MAX(text_reviews_count_capped) AS text_reviews_count_capped
    FROM books_clean
    GROUP BY canonical_book_id
),
canonical_metrics AS (
    SELECT
        r.canonical_book_id,
        r.representative_book_id,
        r.title,
        r.average_rating,
        r.language_code,
        r.publication_date,
        e.ratings_count,
        e.ratings_count_capped,
        e.text_reviews_count,
        e.text_reviews_count_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
),
metric_leaderboards AS (
    SELECT
        'ratings_count' AS metric,
        ROW_NUMBER() OVER (
            ORDER BY ratings_count_capped DESC, ratings_count DESC, canonical_book_id
        ) AS metric_rank,
        canonical_book_id,
        title,
        average_rating,
        language_code,
        ratings_count,
        ratings_count_capped,
        text_reviews_count,
        text_reviews_count_capped
    FROM canonical_metrics
    UNION ALL
    SELECT
        'text_reviews' AS metric,
        ROW_NUMBER() OVER (
            ORDER BY text_reviews_count_capped DESC, text_reviews_count DESC, canonical_book_id
        ) AS metric_rank,
        canonical_book_id,
        title,
        average_rating,
        language_code,
        ratings_count,
        ratings_count_capped,
        text_reviews_count,
        text_reviews_count_capped
    FROM canonical_metrics
)
SELECT
    metric,
    metric_rank,
    canonical_book_id,
    title,
    average_rating,
    language_code,
    ratings_count,
    ratings_count_capped,
    text_reviews_count,
    text_reviews_count_capped
FROM metric_leaderboards
WHERE metric_rank <= (SELECT top_n FROM params)
ORDER BY metric, metric_rank;
