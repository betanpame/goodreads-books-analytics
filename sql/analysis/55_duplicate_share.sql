-- Phase 05 · Step 02 · Task 02
-- M11 – Duplicate share across the catalog using the canonical mapping table.
-- Run inside psql: \i sql/analysis/55_duplicate_share.sql

WITH totals AS (
    SELECT COUNT(*) AS total_rows FROM books
),
duplicates AS (
    SELECT COUNT(*) AS duplicate_rows FROM bookid_canonical_map
)
SELECT
    totals.total_rows,
    duplicates.duplicate_rows,
    ROUND(duplicates.duplicate_rows::numeric / NULLIF(totals.total_rows, 0) * 100, 4) AS duplicate_share_pct
FROM totals, duplicates;
