"""Cleaning utilities for the Goodreads books dataset."""

from __future__ import annotations

from typing import List

import pandas as pd

__all__ = [
    "clean_books",
    "rename_columns",
    "cast_numeric_columns",
    "parse_publication_date",
    "normalize_authors_column",
    "explode_authors",
]


COLUMN_RENAMES = {
    "bookID": "book_id",
    "  num_pages": "num_pages",
}

INT_COLUMNS = ["book_id", "num_pages", "ratings_count", "text_reviews_count"]
FLOAT_COLUMNS = ["average_rating"]

AUTHOR_SEPARATORS = (" and ", " & ", ";", "|", "+")
# Ordered by frequency in the raw export; fall back to generic parsing afterward.
PREFERRED_DATE_FORMATS = ("%m/%d/%y", "%Y-%m-%d", "%b %Y", "%B %Y", "%Y")


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to match the SQL schema."""

    if not COLUMN_RENAMES:
        return df
    return df.rename(columns=COLUMN_RENAMES, errors="ignore")


def cast_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cast numeric columns to their expected dtypes."""

    df_cast = df.copy()

    for column in INT_COLUMNS:
        if column in df_cast.columns:
            df_cast[column] = pd.to_numeric(df_cast[column], errors="coerce").astype("Int64")

    for column in FLOAT_COLUMNS:
        if column in df_cast.columns:
            df_cast[column] = pd.to_numeric(df_cast[column], errors="coerce")
            df_cast[column] = df_cast[column].clip(lower=0, upper=5)

    return df_cast


def parse_publication_date(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the publication_date column into ISO dates."""

    if "publication_date" not in df.columns:
        return df

    df_dates = df.copy()
    raw_dates = df_dates["publication_date"]
    parsed = pd.Series(pd.NaT, index=df_dates.index, dtype="datetime64[ns]")

    for fmt in PREFERRED_DATE_FORMATS:
        mask = parsed.isna()
        if not mask.any():
            break
        parsed.loc[mask] = pd.to_datetime(raw_dates[mask], format=fmt, errors="coerce")

    mask = parsed.isna()
    if mask.any():
        parsed.loc[mask] = pd.to_datetime(raw_dates[mask], errors="coerce")

    df_dates["publication_date"] = parsed.dt.date
    return df_dates


def normalize_authors_column(df: pd.DataFrame) -> pd.DataFrame:
    """Create raw + normalized author columns and clean whitespace."""

    if "authors" not in df.columns:
        return df

    df_authors = df.copy()
    df_authors["authors_raw"] = df_authors["authors"].fillna("")
    collapsed = (
        df_authors["authors_raw"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    df_authors["authors_clean"] = collapsed
    df_authors["authors"] = collapsed.apply(
        lambda value: " / ".join(_split_authors(value)) if isinstance(value, str) else value
    ).replace("", pd.NA)
    return df_authors


def _standardize_author_separators(value: str) -> str:
    normalized = value
    for separator in AUTHOR_SEPARATORS:
        normalized = normalized.replace(separator, "/")
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    return normalized


def _split_authors(value: str) -> List[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    normalized = _standardize_author_separators(value)
    tokens = [token.strip() for token in normalized.split("/") if token.strip()]
    # Deduplicate while preserving order
    return list(dict.fromkeys(tokens))


def explode_authors(
    df: pd.DataFrame,
    *,
    book_id_column: str = "book_id",
    authors_column: str = "authors_clean",
    raw_column: str = "authors_raw",
) -> pd.DataFrame:
    """Expand multi-author strings into a row-per-author DataFrame."""

    required_columns = {book_id_column, raw_column}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise KeyError(f"Missing required columns for explode_authors: {missing}")

    rows: list[dict[str, object]] = []

    for _, record in df.iterrows():
        book_id = record.get(book_id_column)
        if pd.isna(book_id):
            continue

        authors_value = record.get(authors_column, "")
        tokens = _split_authors(authors_value)
        for idx, token in enumerate(tokens, start=1):
            rows.append(
                {
                    "book_id": int(book_id),
                    "author_order": idx,
                    "author_name": token,
                    "raw_authors": record.get(raw_column, ""),
                }
            )

    return pd.DataFrame(rows)


def clean_books(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the composed cleaning pipeline to the raw books DataFrame."""

    pipeline = [rename_columns, cast_numeric_columns, parse_publication_date, normalize_authors_column]

    df_clean = df.copy()
    for step in pipeline:
        df_clean = step(df_clean)

    return df_clean
