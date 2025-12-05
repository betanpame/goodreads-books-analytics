-- Creates a convenience view that automatically coalesces duplicate book IDs
-- to their canonical counterpart using bookid_canonical_map. Run inside psql:
--   \i sql/schema/02_create_books_canonical_view.sql

CREATE OR REPLACE VIEW books_canonical_v AS
SELECT
    COALESCE(m."canonical_bookID", b.book_id) AS canonical_book_id,
    b.book_id AS original_book_id,
    b.title,
    b.authors,
    b.average_rating,
    b.isbn,
    b.isbn13,
    b.language_code,
    b.num_pages,
    b.ratings_count,
    b.text_reviews_count,
    b.publication_date,
    b.publisher
FROM books b
LEFT JOIN bookid_canonical_map m
    ON b.book_id = m."duplicate_bookID";
