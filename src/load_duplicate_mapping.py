"""Load the duplicate→canonical bookID mapping CSV into PostgreSQL."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .db_config import build_database_url_from_env

LOGGER = logging.getLogger(__name__)
DEFAULT_CSV_PATH = Path("data/derived/duplicate_bookid_mapping.csv")
DEFAULT_TABLE_NAME = "bookid_canonical_map"


def get_engine_from_env() -> Engine:
    """Build a SQLAlchemy engine using environment credentials."""

    database_url = build_database_url_from_env()
    return create_engine(database_url)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load duplicate→canonical bookID mappings into PostgreSQL."
    )
    parser.add_argument(
        "--csv-path",
        default=str(DEFAULT_CSV_PATH),
        help="Path to duplicate mapping CSV (default: data/derived/duplicate_bookid_mapping.csv)",
    )
    parser.add_argument(
        "--table",
        default=DEFAULT_TABLE_NAME,
        help="Destination table name (default: bookid_canonical_map)",
    )
    parser.add_argument(
        "--if-exists",
        default="replace",
        choices=["fail", "replace", "append"],
        help="Behavior if the target table already exists (default: replace)",
    )
    return parser.parse_args(argv)


def validate_mapping_frame(df: pd.DataFrame) -> None:
    required = {"duplicate_bookID", "canonical_bookID"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Mapping CSV missing required columns: {', '.join(sorted(missing))}")


def load_mapping_to_postgres(csv_path: Path, table_name: str, if_exists: str) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find mapping CSV at {csv_path}")

    LOGGER.info("Reading mapping CSV from %s", csv_path)
    df = pd.read_csv(csv_path)
    validate_mapping_frame(df)
    LOGGER.info("Loaded %d duplicate→canonical pairs", len(df))

    engine = get_engine_from_env()
    with engine.begin() as connection:
        df.to_sql(table_name, connection, if_exists=if_exists, index=False)
    LOGGER.info(
        "Wrote %d rows into table %s (if_exists=%s)",
        len(df),
        table_name,
        if_exists,
    )


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    args = parse_args(argv)
    load_mapping_to_postgres(Path(args.csv_path), args.table, args.if_exists)


if __name__ == "__main__":  # pragma: no cover
    main()
