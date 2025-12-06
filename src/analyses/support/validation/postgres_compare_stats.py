"""Phase 05 Step 01 Task 02 – Compare CSV vs PostgreSQL stats for `books`.

The CLI loads the raw Goodreads CSV, computes reference metrics in pandas, runs
the same aggregations inside PostgreSQL, and writes a comparison table for the
task notes / portfolio artifacts.
"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.db_config import build_database_url_from_env

LOGGER = logging.getLogger(__name__)
DEFAULT_CSV_PATH = Path("data/books.csv")
DEFAULT_OUTPUT_DIR = Path("outputs/phase05_postgres_validation")
DEFAULT_SCHEMA: Final[str] = "public"
DEFAULT_TABLE: Final[str] = "books"
FLOAT_TOLERANCE: Final[float] = 1e-6


@dataclass
class MetricResult:
    metric: str
    csv_value: str
    postgres_value: str
    matches: bool
    delta: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Goodreads CSV metrics with PostgreSQL aggregates."
    )
    parser.add_argument(
        "--csv-path",
        default=str(DEFAULT_CSV_PATH),
        help="Path to data/books.csv (default: data/books.csv)",
    )
    parser.add_argument(
        "--schema",
        default=DEFAULT_SCHEMA,
        help="PostgreSQL schema name (default: public)",
    )
    parser.add_argument(
        "--table",
        default=DEFAULT_TABLE,
        help="PostgreSQL table name (default: books)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for comparison CSV/Markdown (default: outputs/phase05_postgres_validation)",
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


def compute_csv_metrics(csv_path: Path) -> dict[str, object]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV path not found: {csv_path}")

    LOGGER.info("Reading CSV from %s", csv_path)
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")

    metrics = {
        "row_count": int(len(df)),
        "average_rating": float(df["average_rating"].mean()),
        "min_publication_date": pd.Timestamp(df["publication_date"].min()) if not df[
            "publication_date"
        ].isna().all()
        else pd.NaT,
        "max_publication_date": pd.Timestamp(df["publication_date"].max()) if not df[
            "publication_date"
        ].isna().all()
        else pd.NaT,
    }
    LOGGER.info(
        "CSV metrics – rows: %s, avg_rating: %.5f, min_date: %s, max_date: %s",
        f"{metrics['row_count']:,}",
        metrics["average_rating"],
        metrics["min_publication_date"],
        metrics["max_publication_date"],
    )
    return metrics


def create_engine_from_env() -> Engine:
    database_url = build_database_url_from_env()
    LOGGER.debug("Connecting to %s", database_url)
    return create_engine(database_url)


def fetch_postgres_metrics(engine: Engine, schema: str, table: str) -> dict[str, object]:
    sql = text(
        f"""
        SELECT COUNT(*) AS row_count,
               AVG(average_rating) AS average_rating,
               MIN(publication_date) AS min_publication_date,
               MAX(publication_date) AS max_publication_date
        FROM {schema}.{table}
        """
    )
    with engine.connect() as conn:
        row = conn.execute(sql).mappings().one()

    metrics = {
        "row_count": int(row["row_count"]),
        "average_rating": float(row["average_rating"]),
        "min_publication_date": pd.Timestamp(row["min_publication_date"])
        if row["min_publication_date"]
        else pd.NaT,
        "max_publication_date": pd.Timestamp(row["max_publication_date"])
        if row["max_publication_date"]
        else pd.NaT,
    }
    LOGGER.info(
        "PostgreSQL metrics – rows: %s, avg_rating: %.5f, min_date: %s, max_date: %s",
        f"{metrics['row_count']:,}",
        metrics["average_rating"],
        metrics["min_publication_date"],
        metrics["max_publication_date"],
    )
    return metrics


def format_value(value: object) -> str:
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return "<NA>"
        return value.date().isoformat()
    if isinstance(value, float):
        return f"{value:.5f}"
    return str(value)


def compute_delta(metric: str, csv_value: object, pg_value: object) -> tuple[bool, str]:
    if metric == "row_count":
        csv_int = int(csv_value)
        pg_int = int(pg_value)
        return csv_int == pg_int, str(pg_int - csv_int)
    if metric == "average_rating":
        diff = abs(float(csv_value) - float(pg_value))
        return diff <= FLOAT_TOLERANCE, f"{diff:.6f}"
    if "publication_date" in metric:
        csv_ts = pd.Timestamp(csv_value) if pd.notna(csv_value) else pd.NaT
        pg_ts = pd.Timestamp(pg_value) if pd.notna(pg_value) else pd.NaT
        matches = (pd.isna(csv_ts) and pd.isna(pg_ts)) or (csv_ts == pg_ts)
        return matches, "0 days" if matches else "mismatch"
    return False, "n/a"


def build_comparison_records(csv_metrics: dict[str, object], pg_metrics: dict[str, object]) -> list[MetricResult]:
    metrics_order = [
        "row_count",
        "average_rating",
        "min_publication_date",
        "max_publication_date",
    ]
    records: list[MetricResult] = []
    for metric in metrics_order:
        csv_val = csv_metrics[metric]
        pg_val = pg_metrics[metric]
        matches, delta = compute_delta(metric, csv_val, pg_val)
        records.append(
            MetricResult(
                metric=metric,
                csv_value=format_value(csv_val),
                postgres_value=format_value(pg_val),
                matches=matches,
                delta=delta,
            )
        )
    return records


def persist_outputs(records: list[MetricResult], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        [
            {
                "metric": r.metric,
                "csv_value": r.csv_value,
                "postgres_value": r.postgres_value,
                "matches": "yes" if r.matches else "no",
                "delta": r.delta,
            }
            for r in records
        ]
    )
    csv_path = output_dir / "books_stats_comparison.csv"
    df.to_csv(csv_path, index=False)
    LOGGER.info("Wrote comparison table to %s", csv_path)

    md_path = output_dir / "books_stats_comparison.md"
    md_lines = ["| Metric | CSV / pandas | PostgreSQL | Matches | Delta |", "| --- | --- | --- | --- | --- |"]
    for r in records:
        md_lines.append(
            f"| {r.metric} | {r.csv_value} | {r.postgres_value} | {'yes' if r.matches else 'no'} | {r.delta} |"
        )
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    LOGGER.info("Wrote Markdown comparison table to %s", md_path)
    return csv_path


def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)

    csv_path = Path(args.csv_path)
    schema = validate_identifier(args.schema, "Schema")
    table = validate_identifier(args.table, "Table")

    csv_metrics = compute_csv_metrics(csv_path)
    engine = create_engine_from_env()
    pg_metrics = fetch_postgres_metrics(engine, schema, table)

    records = build_comparison_records(csv_metrics, pg_metrics)
    mismatches = [r for r in records if not r.matches]
    persist_outputs(records, Path(args.output_dir))

    if mismatches:
        LOGGER.warning("Found %d mismatched metrics", len(mismatches))
    else:
        LOGGER.info("All metrics matched between CSV and PostgreSQL")


if __name__ == "__main__":  # pragma: no cover
    run(parse_args())