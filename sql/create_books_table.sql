-- Phase 02 → Step 02 → Task 02
-- Draft definition of the main books table based on the pandas → SQL mapping
-- captured in docs/phase-02-step-02-task-01-notes.md.

CREATE TABLE IF NOT EXISTS books (
    book_id            INTEGER PRIMARY KEY,
    title              TEXT            NOT NULL,
    authors            TEXT            NOT NULL,
    average_rating     NUMERIC(3, 2)   NOT NULL CHECK (average_rating BETWEEN 0 AND 5),
    isbn               VARCHAR(20),
    isbn13             VARCHAR(20),
    language_code      VARCHAR(5),
    num_pages          INTEGER         CHECK (num_pages >= 0),
    ratings_count      INTEGER         NOT NULL DEFAULT 0 CHECK (ratings_count >= 0),
    text_reviews_count INTEGER         NOT NULL DEFAULT 0 CHECK (text_reviews_count >= 0),
    publication_date   DATE,
    publisher          TEXT,

    -- The raw CSV column is spelled "  num_pages" (with two leading spaces).
    -- Our ETL step (Phase 03) must rename it before loading into this table.
    -- ISBN values are stored as VARCHAR to preserve leading zeros and optional hyphens.
    -- NUMERIC(3,2) captures the 0.00–5.00 rating range observed in profiling.
    -- Future work: normalize authors/publishers into separate tables once cleaning rules exist.
    -- TODO: consider UNIQUE constraints on isbn13 when data quality improves.

    CHECK (title <> '')
);
