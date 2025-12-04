"""Command-line initial inspection of the Goodreads books dataset.

This module replaces the earlier notebook-style walkthrough and focuses on a
repeatable CLI flow that can run inside or outside Docker. It demonstrates how
pandas reads local CSV assets, how the repository structure looks from the
script, and how to persist lightweight exploratory outputs for later phases.
"""

from __future__ import annotations

import argparse
import logging
import sys
from io import StringIO
from pathlib import Path
from typing import Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_BOOKS_PATH = DATA_DIR / "books.csv"
EXAMPLE_CSV = DATA_DIR / "example_people.csv"

KEY_COLUMNS = {
    "bookID": "bookID",
    "title": "title",
    "authors": "authors",
    "average_rating": "average_rating",
    "num_pages": "  num_pages",
    "ratings_count": "ratings_count",
    "text_reviews_count": "text_reviews_count",
    "publication_date": "publication_date",
    "publisher": "publisher",
    "language_code": "language_code",
}


def configure_logging(verbose: bool) -> None:
    """Configure a simple logging setup for CLI output."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )


def verify_environment() -> None:
    """Log versions of Python and pandas available to the script."""
    logging.info("Python CLI workflow detected at: %s", PROJECT_ROOT)
    logging.info("Python version: %s", sys.version.replace("\n", " "))
    logging.info("pandas version: %s", pd.__version__)


def inspect_repository() -> None:
    """Print the top-level directory contents for quick orientation."""
    logging.info("Inspecting project layout under %s", PROJECT_ROOT)
    for path in sorted(PROJECT_ROOT.iterdir()):
        logging.debug("- %s", path.name)


def create_example_csv(force: bool = False) -> Path:
    """Create a tiny CSV that illustrates how ``pandas.read_csv`` works."""
    if EXAMPLE_CSV.exists() and not force:
        logging.debug("Example CSV already exists at %s", EXAMPLE_CSV)
        return EXAMPLE_CSV

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    example_df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Carla"],
            "age": [25, 32, 29],
            "city": ["Madrid", "London", "Buenos Aires"],
        }
    )
    example_df.to_csv(EXAMPLE_CSV, index=False)
    logging.info("Wrote example dataset to %s", EXAMPLE_CSV)
    logging.debug("Example preview:\n%s", example_df)
    return EXAMPLE_CSV


def load_books_sample(path: Path, sample_size: int) -> pd.DataFrame:
    """Load a subset of the Goodreads dataset for a lightweight preview."""
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Confirm that the repository data folder is available."
        )

    logging.info("Loading %s rows from %s", sample_size, path)
    sample = pd.read_csv(path, nrows=sample_size)
    logging.info("Loaded shape: (rows=%s, columns=%s)", *sample.shape)
    logging.debug("Columns: %s", sample.columns.tolist())
    logging.debug("Dtypes:\n%s", sample.dtypes)
    return sample


def summarize_sample(sample: pd.DataFrame, output_dir: Optional[Path]) -> None:
    """Emit simple descriptive statistics and persist optional artifacts."""
    logging.info("Head:\n%s", sample.head())
    logging.info("Tail:\n%s", sample.tail())

    info_buffer = StringIO()
    sample.info(buf=info_buffer)
    logging.info("DataFrame info:\n%s", info_buffer.getvalue())

    try:
        summary_all = sample.describe(include="all", datetime_is_numeric=True)
    except TypeError:
        # Older pandas releases do not support datetime_is_numeric; fall back gracefully.
        summary_all = sample.describe(include="all")

    logging.info("Summary statistics:\n%s", summary_all)

    if output_dir is None:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    preview_path = output_dir / "books_sample_preview.csv"
    stats_path = output_dir / "books_numeric_summary.csv"

    sample.to_csv(preview_path, index=False)
    sample.describe().to_csv(stats_path)
    logging.info("Saved quick-look files at %s", output_dir)


def explore_key_columns(sample: pd.DataFrame) -> None:
    """Log dtype, uniqueness, and missingness for key columns, plus date parsing ideas."""
    logging.info("Exploring key columns and types (Task 03 focus)")
    for label, column_name in KEY_COLUMNS.items():
        if column_name not in sample.columns:
            logging.warning("Column %s (%s) missing from sample", column_name, label)
            continue

        series = sample[column_name]
        unique_count = series.nunique(dropna=True)
        missing_count = series.isna().sum()
        logging.info(
            "Column '%s' -> dtype=%s | unique=%s | missing=%s",
            column_name,
            series.dtype,
            unique_count,
            missing_count,
        )
        logging.debug("Example values for %s: %s", column_name, series.head(5).tolist())

    # Publication date parsing check
    if KEY_COLUMNS["publication_date"] in sample.columns:
        parsed_dates = pd.to_datetime(sample[KEY_COLUMNS["publication_date"]], errors="coerce")
        parsed_ratio = parsed_dates.notna().mean() * 100
        logging.info(
            "publication_date parsing success: %.2f%% (%s/%s rows)",
            parsed_ratio,
            parsed_dates.notna().sum(),
            len(parsed_dates),
        )
        logging.debug(
            "Sample parsed publication dates: %s",
            parsed_dates.dropna().head().dt.strftime("%Y-%m-%d").tolist(),
        )

    # Authors splitting idea
    if KEY_COLUMNS["authors"] in sample.columns:
        authors_series = sample[KEY_COLUMNS["authors"]]
        multi_author_ratio = authors_series.str.contains("/").mean() * 100
        logging.info(
            "Authors column: %.2f%% of rows list multiple authors (split on '/')",
            multi_author_ratio,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initial CLI inspection of the Goodreads dataset. "
            "Prints metadata, creates a tiny example CSV, and loads a configurable sample."
        )
    )
    parser.add_argument(
        "--books-path",
        type=Path,
        default=DEFAULT_BOOKS_PATH,
        help="Path to books.csv (defaults to data/books.csv)",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=1000,
        help="Number of rows to load for the sample preview",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "outputs" / "initial_inspection",
        help="Directory where preview CSVs will be stored (set to '' to skip)",
    )
    parser.add_argument(
        "--force-example",
        action="store_true",
        help="Recreate the tiny example CSV even if it already exists",
    )
    parser.add_argument(
        "--no-example",
        action="store_true",
        help="Skip writing the tiny illustrative CSV",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging for more detailed output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    verify_environment()
    inspect_repository()

    if not args.no_example:
        create_example_csv(force=args.force_example)

    sample = load_books_sample(args.books_path, args.sample_size)
    output_dir = None if str(args.output_dir).strip() == "" else args.output_dir
    summarize_sample(sample, output_dir)
    explore_key_columns(sample)


if __name__ == "__main__":
    main()
