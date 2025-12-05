"""Command-line entrypoint to execute the Goodreads cleaning pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Callable, Optional

import pandas as pd

from src.cleaning import (
    NUM_PAGES_MULTI_VOLUME_CAP,
    RATINGS_COUNT_CAP,
    TEXT_REVIEWS_COUNT_CAP,
    clean_books,
)
from src.raw_ingestion import load_books_csv

LOGGER = logging.getLogger(__name__)
DEFAULT_BOOKS_CSV = Path("data/books.csv")
DEFAULT_OUTPUT_CSV = Path("data/derived/books_clean.csv")
DEFAULT_MAPPING_CSV = Path("data/derived/duplicate_bookid_mapping.csv")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load raw books data, apply cleaning rules, and persist a curated CSV.",
    )
    parser.add_argument(
        "--books-csv",
        default=str(DEFAULT_BOOKS_CSV),
        help="Path to the raw books CSV exported from Kaggle (default: data/books.csv)",
    )
    parser.add_argument(
        "--mapping-csv",
        default=str(DEFAULT_MAPPING_CSV),
        help="Path to duplicate→canonical mapping CSV (default: data/derived/duplicate_bookid_mapping.csv)",
    )
    parser.add_argument(
        "--output-csv",
        default=str(DEFAULT_OUTPUT_CSV),
        help="Destination for cleaned CSV output (default: data/derived/books_clean.csv)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for quicker iteration (default: full dataset)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python logging level (default: INFO)",
    )
    parser.add_argument(
        "--skip-mapping",
        action="store_true",
        help="Skip duplicate→canonical mapping merge even if a CSV exists.",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def load_duplicate_mapping_frame(csv_path: Path) -> Optional[pd.DataFrame]:
    if not csv_path.exists():
        LOGGER.warning("Duplicate mapping CSV not found at %s; proceeding without it.", csv_path)
        return None

    LOGGER.info("Reading duplicate mapping from %s", csv_path)
    df = pd.read_csv(csv_path)
    df.columns = [col.strip().lower() for col in df.columns]
    required = {"duplicate_bookid", "canonical_bookid"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Duplicate mapping missing required columns: {sorted(missing)}")
    for column in required:
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    LOGGER.info("Loaded %d duplicate pairs", len(df))
    return df


def emit_quick_stats(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> None:
    LOGGER.info("Raw rows: %s", f"{len(df_raw):,}")
    LOGGER.info("Cleaned rows: %s", f"{len(df_clean):,}")

    summary_columns = [
        "publication_year_flag",
        "average_rating_flag",
        "page_length_bucket",
        "media_type_hint",
        "is_duplicate",
    ]
    for column in summary_columns:
        if column in df_clean.columns:
            counts = df_clean[column].value_counts(dropna=False).head(5)
            LOGGER.info("Value counts for %s:\n%s", column, counts)

    for column in ["ratings_count", "text_reviews_count"]:
        if column in df_clean.columns:
            LOGGER.info(
                "Column %s – min=%s max=%s", column, df_clean[column].min(), df_clean[column].max()
            )


def validate_dataframe(df_clean: pd.DataFrame) -> None:
    checks: list[tuple[str, Callable[[pd.DataFrame], None]]] = [
        ("average_rating_bounds", _check_average_rating_bounds),
        ("num_pages_cap", _check_page_cap),
        ("engagement_caps", _check_engagement_caps),
        ("canonical_id_present", _check_canonical_ids),
    ]
    for label, func in checks:
        func(df_clean)
        LOGGER.info("Validation %s passed", label)


def _check_average_rating_bounds(df: pd.DataFrame) -> None:
    if "average_rating" not in df.columns:
        raise AssertionError("average_rating column missing from cleaned dataset")
    numeric = pd.to_numeric(df["average_rating"], errors="coerce").dropna()
    if numeric.empty:
        raise AssertionError("average_rating column only contains missing data")
    if numeric.lt(0).any() or numeric.gt(5).any():
        raise AssertionError("average_rating contains values outside [0, 5]")


def _check_page_cap(df: pd.DataFrame) -> None:
    if "num_pages_capped" not in df.columns:
        raise AssertionError("num_pages_capped column missing from cleaned dataset")
    numeric = pd.to_numeric(df["num_pages_capped"], errors="coerce").dropna()
    if numeric.gt(NUM_PAGES_MULTI_VOLUME_CAP).any():
        raise AssertionError(
            f"num_pages_capped exceeds cap of {NUM_PAGES_MULTI_VOLUME_CAP}"
        )


def _check_engagement_caps(df: pd.DataFrame) -> None:
    for column, cap in {
        "ratings_count_capped": RATINGS_COUNT_CAP,
        "text_reviews_count_capped": TEXT_REVIEWS_COUNT_CAP,
    }.items():
        if column not in df.columns:
            raise AssertionError(f"{column} missing from cleaned dataset")
        numeric = pd.to_numeric(df[column], errors="coerce").dropna()
        if numeric.gt(cap).any():
            raise AssertionError(f"{column} exceeds cap of {cap}")


def _check_canonical_ids(df: pd.DataFrame) -> None:
    if "canonical_book_id" not in df.columns:
        raise AssertionError("canonical_book_id column missing from cleaned dataset")
    missing = df["canonical_book_id"].isna().sum()
    if missing > 0:
        raise AssertionError(f"canonical_book_id contains {missing} null rows")


def run_pipeline(args: argparse.Namespace) -> None:
    books_path = Path(args.books_csv)
    LOGGER.info("Loading raw books CSV from %s", books_path)
    df_raw, stats = load_books_csv(str(books_path))
    LOGGER.info(
        "Loaded %s rows (%s repaired author rows)",
        f"{len(df_raw):,}",
        f"{stats.repaired_rows:,}",
    )

    if args.limit:
        LOGGER.info("Applying row limit of %d for dry-run mode", args.limit)
        df_raw = df_raw.head(args.limit).copy()

    mapping_df: Optional[pd.DataFrame] = None
    if not args.skip_mapping:
        mapping_df = load_duplicate_mapping_frame(Path(args.mapping_csv))
    else:
        LOGGER.info("Skipping duplicate mapping merge per CLI flag")

    df_clean = clean_books(df_raw, duplicate_mapping=mapping_df)
    emit_quick_stats(df_raw, df_clean)
    validate_dataframe(df_clean)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    LOGGER.info("Wrote cleaned dataset to %s", output_path)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    configure_logging(args.log_level)
    run_pipeline(args)


if __name__ == "__main__":  # pragma: no cover
    main()
