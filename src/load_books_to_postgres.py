"""Script to load data/books.csv into PostgreSQL."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, List

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .cleaning import clean_books, explode_authors
from .db_config import build_database_url_from_env

LOGGER = logging.getLogger(__name__)
LOG_DIR = Path("logs")
AUTHOR_STAGE_TABLE = "book_authors_stage"


def get_engine_from_env() -> Engine:
    """Create a SQLAlchemy Engine using env vars."""

    database_url = build_database_url_from_env()
    return create_engine(database_url)


def _bad_line_logger(bad_lines: List[str]) -> Callable[[list[str]], None]:
    def handler(bad_line: list[str]) -> None:
        bad_lines.append(",".join(bad_line))

    return handler


def read_books_csv(csv_path: str) -> tuple[pd.DataFrame, list[str]]:
    """Read the books CSV while capturing malformed rows."""

    bad_lines: list[str] = []
    df = pd.read_csv(
        csv_path,
        on_bad_lines=_bad_line_logger(bad_lines),
        engine="python",
    )
    return df, bad_lines


def log_bad_lines(bad_lines: list[str]) -> None:
    if not bad_lines:
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"load_books_bad_lines_{timestamp}.log"
    log_path.write_text("\n".join(bad_lines), encoding="utf-8")
    LOGGER.warning("Skipped %d malformed rows. Details recorded in %s", len(bad_lines), log_path)


def load_books_csv_to_postgres(csv_path: str, table_name: str, if_exists: str = "replace") -> None:
    """Load the books CSV into PostgreSQL, emitting author staging rows."""

    LOGGER.info("Reading CSV from %s", csv_path)
    df_raw, bad_lines = read_books_csv(csv_path)
    log_bad_lines(bad_lines)
    LOGGER.info("Loaded %d rows after skipping %d malformed entries", len(df_raw), len(bad_lines))

    df_clean = clean_books(df_raw)
    author_stage = explode_authors(df_clean)

    LOGGER.info("Writing %d cleaned rows to table %s", len(df_clean), table_name)
    engine = get_engine_from_env()

    with engine.begin() as connection:
        df_clean.to_sql(table_name, connection, if_exists=if_exists, index=False)
        if not author_stage.empty:
            LOGGER.info(
                "Writing %d author rows to staging table %s", len(author_stage), AUTHOR_STAGE_TABLE
            )
            author_stage.to_sql(AUTHOR_STAGE_TABLE, connection, if_exists="replace", index=False)
        else:
            LOGGER.info("No multi-author rows detected. Dropping staging table if it exists.")
            connection.execute(text(f"DROP TABLE IF EXISTS {AUTHOR_STAGE_TABLE}"))

    LOGGER.info("Load finished successfully.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load books.csv into PostgreSQL using DATABASE_URL.")
    parser.add_argument(
        "--csv-path",
        default="data/books.csv",
        help="Path to the books CSV file (default: data/books.csv)",
    )
    parser.add_argument(
        "--table",
        default="books",
        help="Target PostgreSQL table name (default: books)",
    )
    parser.add_argument(
        "--if-exists",
        default="replace",
        choices=["fail", "replace", "append"],
        help="Behavior if target table already exists (default: replace)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    args = parse_args(argv)
    load_books_csv_to_postgres(
        csv_path=args.csv_path,
        table_name=args.table,
        if_exists=args.if_exists,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
