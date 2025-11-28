"""Script to load data/books.csv into PostgreSQL.

Usage (from project root, after setting DATABASE_URL):

    python -m src.load_books_to_postgres --table books

The script expects a ``DATABASE_URL`` environment variable in the
standard form, for example:

    postgresql+psycopg2://user:password@localhost:5432/goodreads
"""
from __future__ import annotations

import argparse
from typing import Any

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .db_config import build_database_url_from_env


def get_engine_from_env() -> Engine:
    """Create a SQLAlchemy Engine using env vars.

    Usa ``DATABASE_URL`` si está definido. En caso contrario,
    construye la URL a partir de las variables de entorno
    relacionadas con PostgreSQL (POSTGRES_DB, POSTGRES_USER, etc.).
    """

    database_url = build_database_url_from_env()
    return create_engine(database_url)


def load_books_csv_to_postgres(csv_path: str, table_name: str, if_exists: str = "replace") -> None:
    """Load the books CSV into a PostgreSQL table.

    Parameters
    ----------
    csv_path:
        Path to ``books.csv``.
    table_name:
        Target table name in PostgreSQL.
    if_exists:
        Behavior if the table already exists (``fail``, ``replace``, ``append``).
    """

    print(f"[load] Reading CSV from {csv_path} ...")
    df = pd.read_csv(csv_path)
    print(f"[load] Loaded {len(df):,} rows.")

    engine = get_engine_from_env()

    print(f"[load] Writing to PostgreSQL table '{table_name}' (if_exists={if_exists}) ...")
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print("[load] Done.")


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
    args = parse_args(argv)
    load_books_csv_to_postgres(
        csv_path=args.csv_path,
        table_name=args.table,
        if_exists=args.if_exists,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
