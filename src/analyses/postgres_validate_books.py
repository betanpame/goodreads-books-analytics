"""Phase 05 Step 01 Task 01 – Validate PostgreSQL books table.

This CLI confirms Docker-based Python connectivity to PostgreSQL, captures the
`books` schema metadata, previews sample rows, and persists evidence CSVs for the
portfolio notes.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Final

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.db_config import build_database_url_from_env

LOGGER = logging.getLogger(__name__)
DEFAULT_TABLE: Final[str] = "books"
DEFAULT_OUTPUT_DIR = Path("outputs/phase05_postgres_validation")
DEFAULT_SAMPLE_LIMIT: Final[int] = 5


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate PostgreSQL connectivity and inspect a target table."
    )
    parser.add_argument(
        "--table",
        default=DEFAULT_TABLE,
        help="Target table name (default: books)",
    )
    parser.add_argument(
        "--schema",
        default="public",
        help="Schema that owns the table (default: public)",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=DEFAULT_SAMPLE_LIMIT,
        help="Number of preview rows to persist (default: 5)",
    )
    parser.add_argument(
        "--order-column",
        default="book_id",
        help="Column used to order the preview rows (default: book_id)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for schema + sample CSVs (default: outputs/phase05_postgres_validation)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Python logging level (default: INFO)",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def create_db_engine() -> Engine:
    database_url = build_database_url_from_env()
    LOGGER.debug("Connecting to PostgreSQL at %s", database_url)
    return create_engine(database_url)


def validate_identifier(value: str, label: str) -> str:
    if not value.replace("_", "").isalnum():
        raise ValueError(f"{label} must be alphanumeric with optional underscores. Got: {value}")
    return value


def fetch_columns(engine: Engine, schema: str, table: str) -> pd.DataFrame:
    sql = text(
        """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = :schema
          AND table_name = :table
        ORDER BY ordinal_position
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(sql, {"schema": schema, "table": table}).fetchall()
    df = pd.DataFrame(rows, columns=["column_name", "data_type", "is_nullable"])
    LOGGER.info("Discovered %d columns in %s.%s", len(df), schema, table)
    return df


def fetch_row_count(engine: Engine, schema: str, table: str) -> int:
    stmt = text(f"SELECT COUNT(*) FROM {schema}.{table}")
    with engine.connect() as conn:
        count = conn.execute(stmt).scalar_one()
    LOGGER.info("Row count for %s.%s: %s", schema, table, f"{count:,}")
    return int(count)


def fetch_sample(engine: Engine, schema: str, table: str, order_column: str, limit: int) -> pd.DataFrame:
    stmt = text(
        f"SELECT * FROM {schema}.{table} ORDER BY {order_column} LIMIT :limit"
    )
    with engine.connect() as conn:
        df_sample = pd.read_sql(stmt, conn, params={"limit": limit})
    LOGGER.info("Retrieved %d preview rows from %s.%s", len(df_sample), schema, table)
    return df_sample


def persist_dataframe(df: pd.DataFrame, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    LOGGER.info("Wrote %d rows to %s", len(df), output_path)
    return output_path


def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)
    schema = validate_identifier(args.schema, "Schema")
    table = validate_identifier(args.table, "Table")
    order_column = validate_identifier(args.order_column, "Order column")

    engine = create_db_engine()

    columns_df = fetch_columns(engine, schema, table)
    row_count = fetch_row_count(engine, schema, table)
    sample_df = fetch_sample(engine, schema, table, order_column, args.sample_limit)

    output_dir = Path(args.output_dir)
    persist_dataframe(columns_df, output_dir / f"{table}_schema_snapshot.csv")
    persist_dataframe(sample_df, output_dir / f"{table}_sample_preview.csv")

    LOGGER.info(
        "Validation summary – table: %s.%s, columns: %d, rows: %s, sample saved to %s",
        schema,
        table,
        len(columns_df),
        f"{row_count:,}",
        output_dir,
    )


if __name__ == "__main__":  # pragma: no cover
    run(parse_args())