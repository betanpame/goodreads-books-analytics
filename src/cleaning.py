"""Cleaning utilities for the Goodreads books dataset."""

from __future__ import annotations

import numbers
from datetime import datetime
from typing import List, Optional

import pandas as pd

__all__ = [
    "clean_books",
    "rename_columns",
    "cast_numeric_columns",
    "parse_publication_date",
    "normalize_authors_column",
    "explode_authors",
    "normalize_identifier_columns",
    "derive_publication_year",
    "enforce_publication_year_bounds",
    "sanitize_average_rating",
    "apply_page_length_rules",
    "apply_engagement_winsorization",
    "apply_canonical_mapping",
]


COLUMN_RENAMES = {
    "bookID": "book_id",
    "  num_pages": "num_pages",
}

INT_COLUMNS = ["book_id", "num_pages", "ratings_count", "text_reviews_count"]
FLOAT_COLUMNS = ["average_rating"]
IDENTIFIER_COLUMNS = ["isbn", "isbn13"]

AUTHOR_SEPARATORS = (" and ", " & ", ";", "|", "+")
# Ordered by frequency in the raw export; fall back to generic parsing afterward.
PREFERRED_DATE_FORMATS = ("%m/%d/%y", "%Y-%m-%d", "%b %Y", "%B %Y", "%Y")

PUBLICATION_YEAR_MIN = 1800
FUTURE_YEAR_BUFFER_YEARS = 2
NUM_PAGES_SHORT_THRESHOLD = 10
NUM_PAGES_MULTI_VOLUME_CAP = 2_000
RATINGS_COUNT_CAP = 597_244
TEXT_REVIEWS_COUNT_CAP = 14_812
MEDIA_TYPE_AUDIO = "audio_or_misc"
PAGE_BUCKET_SHORT = "short_reference"
PAGE_BUCKET_MULTI = "multi_volume"
PAGE_BUCKET_ZERO = "zero_or_audio"


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
            series = df_cast[column]
            numeric = pd.to_numeric(series, errors="coerce")
            _raise_if_invalid_numeric(series, numeric, column)
            df_cast[column] = numeric.astype("Int64")

    for column in FLOAT_COLUMNS:
        if column in df_cast.columns:
            series = df_cast[column]
            numeric = pd.to_numeric(series, errors="coerce")
            _raise_if_invalid_numeric(series, numeric, column)
            df_cast[column] = numeric.clip(lower=0, upper=5)

    return df_cast


def normalize_identifier_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure identifiers such as ISBNs are stored as trimmed strings."""

    df_ids = df.copy()

    for column in IDENTIFIER_COLUMNS:
        if column not in df_ids.columns:
            continue
        df_ids[column] = (
            df_ids[column]
            .apply(_format_identifier_value)
            .astype("string")
        )

    return df_ids


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


def derive_publication_year(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a publication_year integer column exists."""

    source_col = "publication_date"
    df_years = df.copy()
    if source_col in df_years.columns:
        parsed = pd.to_datetime(df_years[source_col], errors="coerce")
    else:
        parsed = pd.to_datetime(df_years.get("publication_year"), errors="coerce")

    df_years["publication_year"] = parsed.dt.year.astype("Int64")
    return df_years


def enforce_publication_year_bounds(df: pd.DataFrame) -> pd.DataFrame:
    """Clamp publication_year to believable bounds or mark it as missing."""

    if "publication_year" not in df.columns:
        return df

    df_bounds = df.copy()
    years = pd.to_numeric(df_bounds["publication_year"], errors="coerce")
    current_year = datetime.utcnow().year
    future_cap = current_year + FUTURE_YEAR_BUFFER_YEARS

    mask_low = years < PUBLICATION_YEAR_MIN
    mask_high = years > future_cap
    flag_series = pd.Series(pd.NA, index=df_bounds.index, dtype="string")
    flag_series.loc[mask_low] = "below_min"
    flag_series.loc[mask_high] = "future_year"
    df_bounds["publication_year_flag"] = flag_series
    years.loc[mask_low | mask_high] = pd.NA
    df_bounds["publication_year"] = years.astype("Int64")
    return df_bounds


def sanitize_average_rating(df: pd.DataFrame) -> pd.DataFrame:
    """Mark placeholder ratings (0) as missing so KPIs do not skew."""

    if "average_rating" not in df.columns:
        return df

    df_ratings = df.copy()
    numeric = pd.to_numeric(df_ratings["average_rating"], errors="coerce")
    zero_mask = numeric.eq(0)
    df_ratings["average_rating_flag"] = pd.Series(pd.NA, index=df_ratings.index, dtype="string")
    df_ratings.loc[zero_mask, "average_rating_flag"] = "placeholder_zero"
    numeric.loc[zero_mask] = pd.NA
    df_ratings["average_rating"] = numeric.astype("Float64")
    return df_ratings


def apply_page_length_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Apply page-count specific rules (zero tagging, buckets, capping)."""

    if "num_pages" not in df.columns:
        return df

    df_pages = df.copy()
    pages = pd.to_numeric(df_pages["num_pages"], errors="coerce")
    df_pages["num_pages_raw"] = pages.astype("Int64")
    df_pages["page_length_bucket"] = pd.Series(pd.NA, index=df_pages.index, dtype="string")
    df_pages["media_type_hint"] = pd.Series(pd.NA, index=df_pages.index, dtype="string")

    zero_mask = pages.le(0) | pages.isna()
    df_pages.loc[zero_mask, "media_type_hint"] = MEDIA_TYPE_AUDIO
    df_pages.loc[zero_mask, "page_length_bucket"] = PAGE_BUCKET_ZERO
    pages.loc[zero_mask] = pd.NA

    short_mask = (~zero_mask) & pages.lt(NUM_PAGES_SHORT_THRESHOLD)
    df_pages.loc[short_mask, "page_length_bucket"] = PAGE_BUCKET_SHORT

    multi_mask = pages.gt(NUM_PAGES_MULTI_VOLUME_CAP)
    df_pages.loc[multi_mask, "page_length_bucket"] = PAGE_BUCKET_MULTI

    capped = pages.clip(upper=NUM_PAGES_MULTI_VOLUME_CAP)
    df_pages["num_pages_capped"] = capped.astype("Int64")
    df_pages["num_pages"] = pages.astype("Int64")
    return df_pages


def apply_engagement_winsorization(df: pd.DataFrame) -> pd.DataFrame:
    """Attach capped versions of engagement counts so visuals can use them."""

    df_caps = df.copy()
    cap_plan = {
        "ratings_count": RATINGS_COUNT_CAP,
        "text_reviews_count": TEXT_REVIEWS_COUNT_CAP,
    }

    for column, cap in cap_plan.items():
        if column not in df_caps.columns:
            continue
        numeric = pd.to_numeric(df_caps[column], errors="coerce")
        df_caps[f"{column}_raw"] = numeric.astype("Int64")
        capped = numeric.clip(lower=0, upper=cap)
        df_caps[f"{column}_capped"] = capped.astype("Int64")

    return df_caps


def apply_canonical_mapping(
    df: pd.DataFrame,
    duplicate_mapping: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Join duplicate→canonical pairs so analytics can de-duplicate."""

    df_joined = df.copy()
    if "book_id" not in df_joined.columns:
        return df_joined

    if duplicate_mapping is None or duplicate_mapping.empty:
        df_joined["canonical_book_id"] = df_joined["book_id"].astype("Int64")
        df_joined["is_duplicate"] = False
        return df_joined

    mapping = duplicate_mapping.rename(
        columns={
            "duplicate_bookid": "duplicate_book_id",
            "canonical_bookid": "canonical_target_id",
        }
    )
    required = {"duplicate_book_id", "canonical_target_id"}
    if not required.issubset(mapping.columns):
        missing = required - set(mapping.columns)
        raise KeyError(f"Duplicate mapping missing columns: {missing}")

    mapping = mapping.dropna(subset=["duplicate_book_id", "canonical_target_id"])
    for col in required:
        mapping[col] = pd.to_numeric(mapping[col], errors="coerce").astype("Int64")
    mapping = mapping[list(required)]

    merged = df_joined.merge(
        mapping,
        how="left",
        left_on="book_id",
        right_on="duplicate_book_id",
    )
    canonical = merged["canonical_target_id"].fillna(merged["book_id"])
    merged["canonical_book_id"] = canonical.astype("Int64")
    merged["is_duplicate"] = merged["canonical_book_id"] != merged["book_id"]
    merged = merged.drop(
        columns=[
            col
            for col in ["duplicate_book_id", "canonical_target_id"]
            if col in merged.columns
        ]
    )
    return merged


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


def _format_identifier_value(value: object) -> pd._libs.missing.NAType | str:
    if pd.isna(value):
        return pd.NA

    if isinstance(value, numbers.Integral) and not isinstance(value, bool):
        return str(int(value))

    text = str(value).strip()
    if not text or text.lower() in {"nan", "nat"}:
        return pd.NA
    if text.endswith(".0") and text[:-2].isdigit():
        return text[:-2]
    return text


def _raise_if_invalid_numeric(original: pd.Series, numeric: pd.Series, column: str) -> None:
    mask = original.notna() & numeric.isna()
    if mask.any():
        sample = original[mask].head(5).tolist()
        raise ValueError(
            f"Column '{column}' contains non-numeric values that cannot be coerced: {sample}"
        )


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


def clean_books(
    df: pd.DataFrame,
    *,
    duplicate_mapping: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Apply the composed cleaning pipeline to the raw books DataFrame."""

    pipeline = [
        rename_columns,
        normalize_identifier_columns,
        cast_numeric_columns,
        parse_publication_date,
        derive_publication_year,
        enforce_publication_year_bounds,
        sanitize_average_rating,
        apply_page_length_rules,
        apply_engagement_winsorization,
        normalize_authors_column,
    ]

    df_clean = df.copy()
    for step in pipeline:
        df_clean = step(df_clean)

    df_clean = apply_canonical_mapping(df_clean, duplicate_mapping)
    return df_clean
