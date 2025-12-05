-- Example snippet for Phase 04+ ETL jobs to apply canonical book IDs.
-- Assumes `bookid_canonical_map` has duplicate_bookid + canonical_bookid columns
-- loaded via `python -m src.load_duplicate_mapping`.

WITH canonicalized AS (
    SELECT
        COALESCE(m.canonical_bookid, b.book_id) AS canonical_book_id,
        b.*
    FROM books b
    LEFT JOIN bookid_canonical_map m
        ON b.book_id = m.duplicate_bookid
)
SELECT *
FROM canonicalized;
