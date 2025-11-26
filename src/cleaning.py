"""Cleaning utilities for the Goodreads books dataset.

This module exposes a single main entry point:

    clean_books(df: pd.DataFrame) -> pd.DataFrame

You should move the cleaning rules you defined during EDA
into this function, so that they are reusable from scripts,
notebooks, and tests.
"""
from __future__ import annotations

from typing import Any

import pandas as pd


def clean_books(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw Goodreads books DataFrame.

    Parameters
    ----------
    df:
        Raw DataFrame loaded from ``books.csv`` or from the
        PostgreSQL ``books`` table. Expected columns include
        at least:

        - ``bookID``
        - ``title``
        - ``authors``
        - ``average_rating``
        - ``num_pages``
        - ``ratings_count``
        - ``text_reviews_count``
        - ``language_code``
        - ``publication_date``
        - ``publisher``

    Returns
    -------
    pd.DataFrame
        A new DataFrame with cleaning rules applied.

    Notes
    -----
    This is a skeleton implementation. Replace the placeholder
    code below with your actual cleaning logic (type casting,
    missing-value handling, outlier treatment, text
    normalization, etc.).
    """

    df_clean = df.copy()

    # TODO: implement your cleaning rules here.
    # Keep changes in small, well-named blocks so they are
    # easy to test and reason about.

    return df_clean
