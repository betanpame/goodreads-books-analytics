"""Run the end-to-end data pipeline for Goodreads Books.

Typical stages:
- Load raw ``books.csv`` into pandas.
- Clean data using ``clean_books``.
- Save cleaned data to ``data/derived/books_clean.csv``.
- (Optional) Load cleaned data into PostgreSQL.

Usage (from project root):

    python -m src.run_full_pipeline \
        --csv-path data/books.csv \
        --output-csv data/derived/books_clean.csv \
        --load-to-postgres

Requires ``DATABASE_URL`` in the environment if ``--load-to-postgres`` is used.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .cleaning import clean_books
from .db_config import build_database_url_from_env


def get_engine_from_env() -> Engine:
    """Create a SQLAlchemy Engine using env vars.

    Usa ``DATABASE_URL`` si está definido. En caso contrario,
    construye la URL a partir de las variables de entorno
    relacionadas con PostgreSQL (POSTGRES_DB, POSTGRES_USER, etc.).
    """

    database_url = build_database_url_from_env()
    return create_engine(database_url)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Goodreads Books full data pipeline.")
    parser.add_argument(
        "--csv-path",
        default="data/books.csv",
        help="Path to the raw books CSV file (default: data/books.csv)",
    )
    parser.add_argument(
        "--output-csv",
        default="data/derived/books_clean.csv",
        help="Path to save the cleaned CSV (default: data/derived/books_clean.csv)",
    )
    parser.add_argument(
        "--postgres-table",
        default="books_clean",
        help="Target PostgreSQL table for cleaned data (default: books_clean)",
    )
    parser.add_argument(
        "--load-to-postgres",
        action="store_true",
        help="If set, also load the cleaned data into PostgreSQL using DATABASE_URL.",
    )
    return parser.parse_args(argv)


def run_pipeline(
    csv_path: str,
    output_csv: str,
    load_to_postgres: bool = False,
    postgres_table: str = "books_clean",
) -> None:
    print(f"[pipeline] Loading raw CSV from {csv_path} ...")
    df_raw = pd.read_csv(csv_path)
    print(f"[pipeline] Raw rows: {len(df_raw):,}")

    print("[pipeline] Cleaning data ...")
    df_clean = clean_books(df_raw)
    print(f"[pipeline] Cleaned rows: {len(df_clean):,}")

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"[pipeline] Saving cleaned CSV to {output_csv} ...")
    df_clean.to_csv(output_csv, index=False)

    if load_to_postgres:
        print("[pipeline] Loading cleaned data into PostgreSQL ...")
        engine = get_engine_from_env()
        df_clean.to_sql(postgres_table, engine, if_exists="replace", index=False)
        print(f"[pipeline] Loaded cleaned data into table '{postgres_table}'.")

    print("[pipeline] Done.")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run_pipeline(
        csv_path=args.csv_path,
        output_csv=args.output_csv,
        load_to_postgres=args.load_to_postgres,
        postgres_table=args.postgres_table,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
