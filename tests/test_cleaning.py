"""Tests for the cleaning helpers used by the ETL."""

from __future__ import annotations

import pandas as pd

from src.cleaning import (
    cast_numeric_columns,
    clean_books,
    explode_authors,
    normalize_authors_column,
    parse_publication_date,
    rename_columns,
)


def test_rename_columns_normalizes_known_headers() -> None:
    df = pd.DataFrame({"bookID": [1], "  num_pages": [321]})

    renamed = rename_columns(df)

    assert "book_id" in renamed.columns
    assert "num_pages" in renamed.columns


def test_cast_numeric_columns_coerces_strings_and_clips_rating() -> None:
    df = pd.DataFrame(
        {
            "book_id": ["1"],
            "num_pages": ["250"],
            "ratings_count": ["10"],
            "text_reviews_count": ["5"],
            "average_rating": ["6.7"],
        }
    )

    casted = cast_numeric_columns(df)

    assert casted["book_id"].iloc[0] == 1
    assert casted["ratings_count"].dtype.name == "Int64"
    assert casted["average_rating"].iloc[0] == 5  # clipped to max 5


def test_parse_publication_date_handles_multiple_formats() -> None:
    df = pd.DataFrame({"publication_date": ["9/1/98", "2015-07-30"]})

    parsed = parse_publication_date(df)

    assert parsed["publication_date"].astype(str).tolist() == ["1998-09-01", "2015-07-30"]


def test_parse_publication_date_handles_year_and_month_strings() -> None:
    df = pd.DataFrame({"publication_date": ["1998", "September 1998", "Sep 1998"]})

    parsed = parse_publication_date(df)

    assert parsed["publication_date"].astype(str).tolist() == [
        "1998-01-01",
        "1998-09-01",
        "1998-09-01",
    ]


def test_normalize_authors_column_preserves_raw_and_trims() -> None:
    df = pd.DataFrame({"authors": ["  Foo  / Bar  ", None]})

    normalized = normalize_authors_column(df)

    assert normalized.loc[0, "authors_raw"] == "  Foo  / Bar  "
    assert normalized.loc[0, "authors"] == "Foo / Bar"
    assert pd.isna(normalized.loc[1, "authors"])


def test_explode_authors_supports_multiple_delimiters_and_deduplication() -> None:
    df = pd.DataFrame(
        {
            "book_id": [101, 102],
            "authors": ["Foo / Bar and Baz", "Solo / Solo"],
        }
    )
    normalized = normalize_authors_column(df)
    exploded = explode_authors(normalized)

    assert set(exploded["book_id"]) == {101, 102}
    book_101 = exploded[exploded["book_id"] == 101]
    assert book_101["author_name"].tolist() == ["Foo", "Bar", "Baz"]
    book_102 = exploded[exploded["book_id"] == 102]
    assert book_102["author_name"].tolist() == ["Solo"]


def test_clean_books_runs_full_pipeline() -> None:
    df = pd.DataFrame(
        {
            "bookID": [1],
            "authors": [" Alice  & Bob "],
            "average_rating": [7.2],
            "publication_date": ["9/1/98"],
            "ratings_count": ["5"],
            "text_reviews_count": ["1"],
        }
    )

    cleaned = clean_books(df)

    assert cleaned.loc[0, "authors"] == "Alice / Bob"
    assert cleaned.loc[0, "average_rating"] == 5
    assert str(cleaned.loc[0, "publication_date"]) == "1998-09-01"
