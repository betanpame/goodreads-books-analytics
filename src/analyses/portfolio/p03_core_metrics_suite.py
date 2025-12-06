"""Portfolio 03 - generate the curated Phase 04 core metrics tables.

Running this CLI keeps the demonstration inside the Python/Docker workflow,
reads ``books_clean.csv``, computes the marquee KPI set (M1, M3, M4, M5, M7,
M8, M9, M11), and saves the CSV artifacts recruiters review. It is wired into
`make core-metrics` and the FAQ so reviewers can rerun the exact same exports.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from src.metrics.core_metrics import (
    compute_average_rating_by_publication_year,
    compute_duplicate_share,
    compute_language_rating_summary,
    compute_median_rating_by_page_bucket,
    compute_median_ratings_count_by_publication_year,
    compute_top_authors_by_weighted_rating,
    compute_top_books_by_ratings_count,
    compute_top_books_by_text_reviews,
)

LOGGER = logging.getLogger(__name__)
DEFAULT_BOOKS_CSV = Path("data/derived/books_clean.csv")
DEFAULT_OUTPUT_DIR = Path("outputs/phase04_core_metrics")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute Phase 04 core metrics tables.")
    parser.add_argument(
        "--books-csv",
        default=str(DEFAULT_BOOKS_CSV),
        help="Path to books_clean.csv (default: data/derived/books_clean.csv)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for the generated CSVs (default: outputs/phase04_core_metrics)",
    )
    parser.add_argument(
        "--author-min-ratings",
        type=int,
        default=5_000,
        help="Minimum cumulative ratings per author for M1 (default: 5000)",
    )
    parser.add_argument(
        "--author-top-n",
        type=int,
        default=15,
        help="Number of authors to keep for M1 (default: 15)",
    )
    parser.add_argument(
        "--books-top-n",
        type=int,
        default=20,
        help="Number of books to include in M3/M4 leaderboards (default: 20)",
    )
    parser.add_argument(
        "--language-min-books",
        type=int,
        default=50,
        help="Minimum canonical titles per language for M9 (default: 50)",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=None,
        help="Optional publication_year lower bound for time-series metrics",
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


def load_cleaned_books(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Could not find cleaned CSV at {path}")
    LOGGER.info("Reading cleaned dataset from %s", path)
    df = pd.read_csv(path)
    LOGGER.info("Loaded %s rows and %s columns", f"{len(df):,}", df.shape[1])
    return df


def persist_table(df: pd.DataFrame, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    LOGGER.info("Wrote %s rows to %s", len(df), path)
    return path


def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)
    df_clean = load_cleaned_books(Path(args.books_csv))
    min_year = args.min_year

    tables = {
        "M1_top_authors_by_weighted_rating": compute_top_authors_by_weighted_rating(
            df_clean,
            min_ratings=args.author_min_ratings,
            top_n=args.author_top_n,
        ),
        "M3_top_books_by_ratings_count": compute_top_books_by_ratings_count(
            df_clean,
            top_n=args.books_top_n,
        ),
        "M4_top_books_by_text_reviews": compute_top_books_by_text_reviews(
            df_clean,
            top_n=args.books_top_n,
        ),
        "M5_median_rating_by_page_length": compute_median_rating_by_page_bucket(df_clean),
        "M7_average_rating_by_year": compute_average_rating_by_publication_year(
            df_clean,
            min_year=min_year,
        ),
        "M8_median_ratings_count_by_year": compute_median_ratings_count_by_publication_year(
            df_clean,
            min_year=min_year,
        ),
        "M9_language_rating_summary": compute_language_rating_summary(
            df_clean,
            min_books=args.language_min_books,
        ),
        "M11_duplicate_share": compute_duplicate_share(df_clean),
    }

    for metric_name, table in tables.items():
        if table is None or table.empty:
            LOGGER.warning("Metric %s produced an empty table", metric_name)
            continue
        persist_table(table, Path(args.output_dir), metric_name)
        LOGGER.debug("%s head:\n%s", metric_name, table.head().to_string(index=False))

    LOGGER.info("Generated %d metric tables", len([t for t in tables.values() if not t.empty]))


if __name__ == "__main__":  # pragma: no cover
    run(parse_args())
