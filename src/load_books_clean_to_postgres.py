"""Load data/derived/books_clean.csv into PostgreSQL for Phase 05 analyses."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import Boolean, Date, Integer, Numeric, String, Text, create_engine, text
from sqlalchemy.engine import Engine

from .cleaning import explode_authors
from .db_config import build_database_url_from_env
from .schema import ensure_books_clean_schema

LOGGER = logging.getLogger(__name__)
DEFAULT_CSV = Path("data/derived/books_clean.csv")
DEFAULT_TABLE = "books_clean"
AUTHOR_STAGE_TABLE = "book_authors_stage"

INT_COLUMNS = [
    "book_id",
    "num_pages",
    "ratings_count",
    "text_reviews_count",
    "publication_year",
    "num_pages_raw",
    "num_pages_capped",
    "ratings_count_raw",
    "ratings_count_capped",
    "text_reviews_count_raw",
    "text_reviews_count_capped",
    "canonical_book_id",
]

DTYPE_MAP = {
    "book_id": Integer(),
    "title": Text(),
    "authors": Text(),
    "average_rating": Numeric(4, 3),
    "isbn": String(20),
    "isbn13": String(20),
    "language_code": String(10),
    "num_pages": Integer(),
    "ratings_count": Integer(),
    "text_reviews_count": Integer(),
    "publication_date": Date(),
    "publisher": Text(),
    "publication_year": Integer(),
    "publication_year_flag": String(32),
    "average_rating_flag": String(32),
    "num_pages_raw": Integer(),
    "page_length_bucket": String(32),
    "media_type_hint": String(32),
    "num_pages_capped": Integer(),
    "ratings_count_raw": Integer(),
    "ratings_count_capped": Integer(),
    "text_reviews_count_raw": Integer(),
    "text_reviews_count_capped": Integer(),
    "authors_raw": Text(),
    "authors_clean": Text(),
    "canonical_book_id": Integer(),
    "is_duplicate": Boolean(),
}


def get_engine() -> Engine:
    database_url = build_database_url_from_env()
    return create_engine(database_url)


def read_books_clean(csv_path: Path) -> pd.DataFrame:
    LOGGER.info("Reading cleaned dataset from %s", csv_path)
    df = pd.read_csv(
        csv_path,
        parse_dates=["publication_date"],
        keep_default_na=True,
    )

    if "publication_date" in df.columns:
        df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce").dt.date

    for column in INT_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    if "is_duplicate" in df.columns:
        df["is_duplicate"] = df["is_duplicate"].astype("boolean")

    return df


def write_author_stage(df: pd.DataFrame, engine: Engine) -> None:
    subset = df[["book_id", "authors_clean", "authors_raw"]].copy()
    authors_stage = explode_authors(subset)
    with engine.begin() as connection:
        if authors_stage.empty:
            LOGGER.info("No author rows to persist. Dropping %s if it exists.", AUTHOR_STAGE_TABLE)
            connection.execute(text(f"DROP TABLE IF EXISTS {AUTHOR_STAGE_TABLE}"))
            return

        LOGGER.info("Writing %d author rows to %s", len(authors_stage), AUTHOR_STAGE_TABLE)
        authors_stage.to_sql(AUTHOR_STAGE_TABLE, connection, if_exists="replace", index=False)


def load_books_clean_to_postgres(csv_path: Path, table_name: str, if_exists: str) -> None:
    df = read_books_clean(csv_path)
    engine = get_engine()

    with engine.begin() as connection:
        LOGGER.info("Writing %d rows to table %s", len(df), table_name)
        df.to_sql(table_name, connection, if_exists=if_exists, index=False, dtype=DTYPE_MAP)

    ensure_books_clean_schema(engine, table_name)
    write_author_stage(df, engine)
    LOGGER.info("Load completed successfully.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load books_clean.csv into PostgreSQL.")
    parser.add_argument(
        "--csv-path",
        default=str(DEFAULT_CSV),
        help="Path to books_clean.csv (default: data/derived/books_clean.csv)",
    )
    parser.add_argument(
        "--table",
        default=DEFAULT_TABLE,
        help="Target table name (default: books_clean)",
    )
    parser.add_argument(
        "--if-exists",
        default="replace",
        choices=["fail", "replace", "append"],
        help="Behavior if the target table already exists (default: replace)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python logging level (default: INFO)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    load_books_clean_to_postgres(
        csv_path=Path(args.csv_path),
        table_name=args.table,
        if_exists=args.if_exists,
    )


if __name__ == "__main__":  # pragma: no cover
    main()