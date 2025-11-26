"""Basic tests for the cleaning logic.

These tests are intentionally small and focused. Extend them
as your ``clean_books`` implementation grows.
"""
from __future__ import annotations

import pandas as pd

from src.cleaning import clean_books


def test_clean_books_does_not_drop_all_rows() -> None:
    df = pd.DataFrame(
        {
            "bookID": [1, 2],
            "title": ["Book A", "Book B"],
            "authors": ["Author A", "Author B"],
            "average_rating": [4.5, 3.0],
            "num_pages": [300, 200],
            "ratings_count": [100, 50],
        }
    )

    df_clean = clean_books(df)

    assert len(df_clean) > 0


def test_clean_books_keeps_rating_range() -> None:
    df = pd.DataFrame(
        {
            "bookID": [1, 2, 3],
            "title": ["Book A", "Book B", "Book C"],
            "authors": ["Author A", "Author B", "Author C"],
            "average_rating": [4.5, -1.0, 6.0],
            "num_pages": [300, 200, 150],
            "ratings_count": [100, 50, 10],
        }
    )

    df_clean = clean_books(df)

    # After cleaning, ratings should be within [0, 5].
    if "average_rating" in df_clean.columns and not df_clean.empty:
        assert df_clean["average_rating"].between(0, 5).all()
