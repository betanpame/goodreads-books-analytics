"""Phase 05 Step 01 Task 03 – Profile key columns inside PostgreSQL.

The CLI computes null counts, distinct counts, min/max ranges, and top category
distributions for the `books` table (or any table structure with the same
columns) and persists the results as CSV/Markdown evidence for documentation.
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
DEFAULT_SCHEMA: Final[str] = "public"
DEFAULT_TABLE: Final[str] = "books"
DEFAULT_OUTPUT_DIR = Path("outputs/phase05_postgres_validation")

KEY_COLUMNS: Final[list[str]] = [
    "book_id",
    "title",
    "authors",
    "average_rating",
    "ratings_count",
    "text_reviews_count",
    "num_pages",
    "language_code",
    "publication_date",
    "publisher",
]

CATEGORY_QUERIES: Final[dict[str, str]] = {
    "language_code": "language_code",
    "publisher": "publisher",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile key columns in PostgreSQL books table.")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, help="Schema name (default: public)")
    parser.add_argument("--table", default=DEFAULT_TABLE, help="Table name (default: books)")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for profiling outputs (default: outputs/phase05_postgres_validation)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of categories to show for distribution tables (default: 10)",
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


def validate_identifier(value: str, label: str) -> str:
    if not value.replace("_", "").isalnum():
        raise ValueError(f"{label} must be alphanumeric with optional underscores. Got: {value}")
    return value


def create_db_engine() -> Engine:
    database_url = build_database_url_from_env()
    LOGGER.debug("Connecting to %s", database_url)
    return create_engine(database_url)


def fetch_null_and_distinct_counts(engine: Engine, schema: str, table: str) -> pd.DataFrame:
    rows = []
    with engine.connect() as conn:
        for column in KEY_COLUMNS:
            null_sql = text(f"SELECT COUNT(*) FROM {schema}.{table} WHERE {column} IS NULL")
            distinct_sql = text(f"SELECT COUNT(DISTINCT {column}) FROM {schema}.{table}")
            null_count = conn.execute(null_sql).scalar_one()
            distinct_count = conn.execute(distinct_sql).scalar_one()
            rows.append(
                {
                    "column": column,
                    "null_count": int(null_count),
                    "distinct_count": int(distinct_count),
                }
            )
    df = pd.DataFrame(rows)
    LOGGER.info("Computed null/distinct counts for %d columns", len(df))
    return df


def fetch_numeric_ranges(engine: Engine, schema: str, table: str) -> pd.DataFrame:
    numeric_columns = ["average_rating", "ratings_count", "text_reviews_count", "num_pages"]
    rows = []
    with engine.connect() as conn:
        for column in numeric_columns:
            sql = text(f"SELECT MIN({column}) AS min_val, MAX({column}) AS max_val FROM {schema}.{table}")
            result = conn.execute(sql).mappings().one()
            rows.append(
                {
                    "column": column,
                    "min_value": result["min_val"],
                    "max_value": result["max_val"],
                }
            )
    df = pd.DataFrame(rows)
    LOGGER.info("Captured numeric ranges for %d columns", len(df))
    return df


def fetch_top_categories(engine: Engine, schema: str, table: str, top_n: int) -> dict[str, pd.DataFrame]:
    outputs: dict[str, pd.DataFrame] = {}
    with engine.connect() as conn:
        for label, column in CATEGORY_QUERIES.items():
            sql = text(
                f"""
                SELECT {column} AS value, COUNT(*) AS row_count
                FROM {schema}.{table}
                GROUP BY {column}
                ORDER BY row_count DESC, value
                LIMIT :top_n
                """
            )
            df = pd.read_sql(sql, conn, params={"top_n": top_n})
            outputs[label] = df
            LOGGER.info("Computed top %d distribution for %s", top_n, column)
    return outputs


def persist_dataframe(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOGGER.info("Wrote %s rows to %s", len(df), path)


def persist_markdown(df: pd.DataFrame, path: Path) -> None:
    lines = ["| " + " | ".join(df.columns) + " |", "| " + " | ".join(["---"] * len(df.columns)) + " |"]
    for _, row in df.iterrows():
        formatted = " | ".join(str(value) for value in row.tolist())
        lines.append(f"| {formatted} |")
    path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Wrote Markdown table to %s", path)


def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)
    schema = validate_identifier(args.schema, "Schema")
    table = validate_identifier(args.table, "Table")
    top_n = args.top_n

    engine = create_db_engine()
    output_dir = Path(args.output_dir)

    nulls_df = fetch_null_and_distinct_counts(engine, schema, table)
    ranges_df = fetch_numeric_ranges(engine, schema, table)
    category_tables = fetch_top_categories(engine, schema, table, top_n)

    persist_dataframe(nulls_df, output_dir / "books_null_distinct_summary.csv")
    persist_dataframe(ranges_df, output_dir / "books_numeric_ranges.csv")
    persist_markdown(nulls_df, output_dir / "books_null_distinct_summary.md")
    persist_markdown(ranges_df, output_dir / "books_numeric_ranges.md")

    for label, df in category_tables.items():
        csv_path = output_dir / f"books_top_{label}.csv"
        persist_dataframe(df, csv_path)

    LOGGER.info(
        "Profiling complete – %d columns analyzed, category tables: %s",
        len(nulls_df),
        ", ".join(category_tables.keys()),
    )


if __name__ == "__main__":  # pragma: no cover
    run(parse_args())