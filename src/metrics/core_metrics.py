"""Reusable helpers for the Phase 04 core metrics (M1, M3, M4, M5, M7, M8, M9, M11).

All functions accept the cleaned Goodreads dataset (``books_clean.csv``) and
return tidy pandas DataFrames suitable for CSV export or downstream
visualizations. The calculations intentionally mirror the catalog produced in
Task 01 so the project stays reproducible for reviewers.
"""
from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd

from src.cleaning import explode_authors

__all__ = [
    "compute_top_authors_by_weighted_rating",
    "compute_top_books_by_ratings_count",
    "compute_top_books_by_text_reviews",
    "compute_median_rating_by_page_bucket",
    "compute_average_rating_by_publication_year",
    "compute_median_ratings_count_by_publication_year",
    "compute_language_rating_summary",
    "compute_duplicate_share",
]


def _ensure_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def _canonical_rollup(df: pd.DataFrame) -> pd.DataFrame:
    """Return a canonical-level view (one row per canonical_book_id)."""

    text_cols = [
        "title",
        "authors_clean",
        "language_code",
        "page_length_bucket",
        "media_type_hint",
        "publication_year",
        "average_rating",
        "num_pages",
        "num_pages_capped",
    ]
    numeric_cols = [
        "ratings_count",
        "ratings_count_capped",
        "text_reviews_count",
        "text_reviews_count_capped",
    ]

    _ensure_columns(df, ["canonical_book_id", "book_id", "is_duplicate", *text_cols, *numeric_cols])

    textual = (
        df.sort_values(["is_duplicate", "book_id"], ascending=[True, True])
        .drop_duplicates("canonical_book_id", keep="first")
        .loc[:, ["canonical_book_id", *text_cols]]
    )

    aggregated = (
        df.groupby("canonical_book_id", dropna=False)
        .agg({
            "ratings_count": "max",
            "ratings_count_capped": "max",
            "text_reviews_count": "max",
            "text_reviews_count_capped": "max",
        })
        .reset_index()
    )

    return textual.merge(aggregated, on="canonical_book_id", how="left")


def compute_top_authors_by_weighted_rating(
    df: pd.DataFrame,
    *,
    min_ratings: int = 5_000,
    top_n: int = 15,
) -> pd.DataFrame:
    """M1 – Weighted average rating per author with a ratings floor."""

    _ensure_columns(df, ["book_id", "authors_clean", "authors_raw", "average_rating", "ratings_count", "canonical_book_id"])

    exploded = explode_authors(df[["book_id", "authors_clean", "authors_raw"]])
    if exploded.empty:
        return pd.DataFrame(columns=["author_name", "weighted_average_rating", "total_ratings", "book_count"])

    merged = exploded.merge(
        df[["book_id", "canonical_book_id", "average_rating", "ratings_count"]],
        on="book_id",
        how="left",
    )
    merged = merged.dropna(subset=["author_name", "average_rating", "ratings_count"])
    merged["weighted_sum"] = merged["average_rating"] * merged["ratings_count"]

    grouped = (
        merged.groupby("author_name", dropna=False)
        .agg(
            weighted_rating_sum=("weighted_sum", "sum"),
            total_ratings=("ratings_count", "sum"),
            book_count=("canonical_book_id", "nunique"),
        )
        .reset_index()
    )
    filtered = grouped[grouped["total_ratings"] >= min_ratings]
    if filtered.empty:
        return pd.DataFrame(columns=["author_name", "weighted_average_rating", "total_ratings", "book_count"])

    filtered = filtered.copy()
    filtered["weighted_average_rating"] = filtered["weighted_rating_sum"] / filtered["total_ratings"]
    result = filtered.sort_values(
        ["weighted_average_rating", "total_ratings"], ascending=[False, False]
    ).head(top_n)
    return result[["author_name", "weighted_average_rating", "total_ratings", "book_count"]]


def compute_top_books_by_ratings_count(
    df: pd.DataFrame,
    *,
    top_n: int = 20,
) -> pd.DataFrame:
    """M3 – Leaderboard of canonical books sorted by capped ratings counts."""

    canonical = _canonical_rollup(df)
    result = canonical.sort_values(
        ["ratings_count_capped", "ratings_count"], ascending=[False, False]
    ).head(top_n)
    columns = [
        "canonical_book_id",
        "title",
        "average_rating",
        "ratings_count",
        "ratings_count_capped",
        "language_code",
    ]
    return result[columns]


def compute_top_books_by_text_reviews(
    df: pd.DataFrame,
    *,
    top_n: int = 20,
) -> pd.DataFrame:
    """M4 – Highlight canonical books with the most written reviews."""

    canonical = _canonical_rollup(df)
    result = canonical.sort_values(
        ["text_reviews_count_capped", "text_reviews_count"], ascending=[False, False]
    ).head(top_n)
    columns = [
        "canonical_book_id",
        "title",
        "average_rating",
        "text_reviews_count",
        "text_reviews_count_capped",
        "language_code",
    ]
    return result[columns]


def compute_median_rating_by_page_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """M5 – Median rating per page_length_bucket."""

    _ensure_columns(df, ["page_length_bucket", "average_rating", "canonical_book_id"])
    canonical = _canonical_rollup(df)
    grouped = (
        canonical.groupby("page_length_bucket", dropna=False)
        .agg(
            median_rating=("average_rating", "median"),
            book_count=("canonical_book_id", "nunique"),
        )
        .reset_index()
    )
    return grouped.sort_values("median_rating", ascending=False)


def compute_average_rating_by_publication_year(
    df: pd.DataFrame,
    *,
    min_year: int | None = None,
) -> pd.DataFrame:
    """M7 – Average rating per publication year."""

    _ensure_columns(df, ["publication_year", "average_rating", "canonical_book_id"])
    canonical = _canonical_rollup(df)
    data = canonical.dropna(subset=["publication_year"])
    if min_year is not None:
        data = data[data["publication_year"] >= min_year]
    grouped = (
        data.groupby("publication_year", dropna=False)
        .agg(
            average_rating=("average_rating", "mean"),
            book_count=("canonical_book_id", "nunique"),
        )
        .reset_index()
        .sort_values("publication_year")
    )
    return grouped


def compute_median_ratings_count_by_publication_year(
    df: pd.DataFrame,
    *,
    min_year: int | None = None,
) -> pd.DataFrame:
    """M8 – Median capped ratings count per publication year."""

    _ensure_columns(df, ["publication_year", "ratings_count_capped", "canonical_book_id"])
    canonical = _canonical_rollup(df)
    data = canonical.dropna(subset=["publication_year"])
    if min_year is not None:
        data = data[data["publication_year"] >= min_year]
    grouped = (
        data.groupby("publication_year", dropna=False)
        .agg(
            median_ratings_count_capped=("ratings_count_capped", "median"),
            book_count=("canonical_book_id", "nunique"),
        )
        .reset_index()
        .sort_values("publication_year")
    )
    return grouped


def compute_language_rating_summary(
    df: pd.DataFrame,
    *,
    min_books: int = 50,
) -> pd.DataFrame:
    """M9 – Average rating per language with sufficient canonical coverage."""

    _ensure_columns(df, ["language_code", "average_rating", "canonical_book_id", "ratings_count_capped"])
    canonical = _canonical_rollup(df)
    data = canonical.dropna(subset=["language_code"])
    grouped = (
        data.groupby("language_code", dropna=False)
        .agg(
            book_count=("canonical_book_id", "nunique"),
            average_rating=("average_rating", "mean"),
            median_ratings_count_capped=("ratings_count_capped", "median"),
        )
        .reset_index()
    )
    filtered = grouped[grouped["book_count"] >= min_books]
    return filtered.sort_values(["average_rating", "book_count"], ascending=[False, False])


def compute_duplicate_share(df: pd.DataFrame) -> pd.DataFrame:
    """M11 – Share of rows flagged as duplicates (for canonical awareness)."""

    _ensure_columns(df, ["is_duplicate", "canonical_book_id"])
    total_rows = len(df)
    duplicate_rows = int(df["is_duplicate"].sum())
    share = duplicate_rows / total_rows if total_rows else 0.0
    return pd.DataFrame(
        {
            "total_rows": [total_rows],
            "duplicate_rows": [duplicate_rows],
            "duplicate_share_pct": [round(share * 100, 4)],
        }
    )
