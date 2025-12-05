-- Phase 05 · Step 02 · Task 03
-- Advanced pattern: author-level top-N ranking using ROW_NUMBER over canonical books.
-- Run inside psql: \i sql/analysis/60_top_books_per_author.sql

WITH params AS (
    SELECT
        3::int AS per_author_limit,
        5000::bigint AS min_total_ratings,
        25::int AS max_authors
),
books_with_canonical AS (
    SELECT
        b.book_id,
        COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
        b.title,
        b.average_rating,
        b.language_code,
        b.ratings_count,
        b.text_reviews_count
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
        language_code
    FROM books_with_canonical
    ORDER BY canonical_book_id,
             CASE WHEN canonical_book_id = book_id THEN 0 ELSE 1 END,
             book_id
),
engagement_rollup AS (
    SELECT
        canonical_book_id,
        MAX(ratings_count) AS ratings_count,
        MAX(text_reviews_count) AS text_reviews_count
    FROM books_with_canonical
    GROUP BY canonical_book_id
),
canonical_rollup AS (
    SELECT
        r.canonical_book_id,
        r.representative_book_id,
        r.title,
        r.average_rating,
        r.language_code,
        GREATEST(0, LEAST(COALESCE(e.ratings_count, 0), 597244)) AS ratings_count_capped,
        GREATEST(0, LEAST(COALESCE(e.text_reviews_count, 0), 14812)) AS text_reviews_capped
    FROM representatives AS r
    JOIN engagement_rollup AS e USING (canonical_book_id)
),
author_books AS (
    SELECT
        a.author_name,
        c.canonical_book_id,
        c.title,
        c.average_rating,
        c.language_code,
        c.ratings_count_capped,
        c.text_reviews_capped
    FROM book_authors_stage AS a
    JOIN canonical_rollup AS c
        ON a.book_id = c.representative_book_id
    WHERE a.author_name IS NOT NULL
),
author_totals AS (
    SELECT
        author_name,
        SUM(ratings_count_capped) AS total_ratings
    FROM author_books
    GROUP BY author_name
),
author_leaders AS (
    SELECT
        author_name,
        total_ratings,
        ROW_NUMBER() OVER (
            ORDER BY total_ratings DESC, author_name
        ) AS author_leaderboard_rank
    FROM author_totals
),
ranked AS (
    SELECT
        ab.author_name,
        ab.canonical_book_id,
        ab.title,
        ab.average_rating,
        ab.language_code,
        ab.ratings_count_capped,
        ab.text_reviews_capped,
        al.total_ratings,
        ROW_NUMBER() OVER (
            PARTITION BY ab.author_name
            ORDER BY ab.ratings_count_capped DESC, ab.average_rating DESC, ab.canonical_book_id
        ) AS author_rank,
        al.author_leaderboard_rank
    FROM author_books AS ab
    JOIN author_leaders AS al USING (author_name)
    CROSS JOIN params
    WHERE al.total_ratings >= params.min_total_ratings
)
SELECT
    author_name,
    author_rank,
    canonical_book_id,
    title,
    average_rating,
    ratings_count_capped,
    text_reviews_capped,
    language_code,
        total_ratings
FROM ranked, params
WHERE author_rank <= params.per_author_limit
    AND author_leaderboard_rank <= params.max_authors
ORDER BY total_ratings DESC, author_name, author_rank;
