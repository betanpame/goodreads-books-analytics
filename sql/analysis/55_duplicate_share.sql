-- Phase 05 · Step 02 · Task 02
-- M11 – Duplicate share across the catalog using the canonical mapping table.
-- Run inside psql: \i sql/analysis/55_duplicate_share.sql

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END) AS duplicate_rows,
    ROUND(
        SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END)::numeric / NULLIF(COUNT(*), 0) * 100,
        4
    ) AS duplicate_share_pct
FROM books_clean;
