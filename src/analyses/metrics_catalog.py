"""Define and validate Phase 04 business questions and metrics.

This utility keeps the project strictly Python/Docker-friendly while
producing a Markdown-ready table of the core metrics we plan to
calculate in Step 02.
"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List

import pandas as pd

LOGGER = logging.getLogger(__name__)
DEFAULT_BOOKS_CSV = Path("data/derived/books_clean.csv")
DEFAULT_OUTPUT_MD = Path("outputs/phase04_metrics_catalog.md")
KEY_COLUMNS = [
    "canonical_book_id",
    "book_id",
    "title",
    "authors",
    "average_rating",
    "ratings_count",
    "ratings_count_capped",
    "text_reviews_count",
    "text_reviews_count_capped",
    "num_pages",
    "num_pages_capped",
    "page_length_bucket",
    "media_type_hint",
    "publication_year",
    "language_code",
    "publisher",
    "is_duplicate",
]


@dataclass(frozen=True)
class MetricDefinition:
    question_id: str
    question: str
    metric_id: str
    metric_name: str
    description: str
    columns: List[str]
    notes: str
    priority: str  # "core" or "stretch"


METRIC_DEFINITIONS: tuple[MetricDefinition, ...] = (
    MetricDefinition(
        question_id="Q1",
        question="Which authors deliver consistently high-rated titles with meaningful readership?",
        metric_id="M1",
        metric_name="Top authors by weighted average rating",
        description="Average rating per author with ratings_count >= 5,000 to avoid tiny sample bias.",
        columns=["authors", "average_rating", "ratings_count"],
        notes="Weight by ratings_count to keep blockbusters influential while still surfacing quality.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q1",
        question="Which authors deliver consistently high-rated titles with meaningful readership?",
        metric_id="M2",
        metric_name="Author engagement index",
        description="Combined z-score of ratings_count_capped and text_reviews_count_capped per author.",
        columns=["authors", "ratings_count_capped", "text_reviews_count_capped"],
        notes="Helps compare participation-heavy fandoms beyond raw averages.",
        priority="stretch",
    ),
    MetricDefinition(
        question_id="Q2",
        question="Which individual books capture the most reader engagement?",
        metric_id="M3",
        metric_name="Top books by ratings_count_capped",
        description="Leaderboard of canonical books sorted by capped ratings counts.",
        columns=["canonical_book_id", "title", "ratings_count_capped", "ratings_count"],
        notes="Use canonical IDs so audiobook duplicates do not double-count.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q2",
        question="Which individual books capture the most reader engagement?",
        metric_id="M4",
        metric_name="Top books by text_reviews_count_capped",
        description="Highlight books that spark the most written discussion.",
        columns=["canonical_book_id", "title", "text_reviews_count_capped", "text_reviews_count"],
        notes="Pairs with M3 to compare silent ratings vs vocal reviews.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q3",
        question="How does book length influence satisfaction and engagement?",
        metric_id="M5",
        metric_name="Median rating by page_length_bucket",
        description="Compare sentiment across short_reference / standard / multi_volume buckets.",
        columns=["page_length_bucket", "average_rating"],
        notes="Bucket definitions come from Phase 03 rulebook; zero_or_audio is its own cohort.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q3",
        question="How does book length influence satisfaction and engagement?",
        metric_id="M6",
        metric_name="Engagement delta by page_length_bucket",
        description="Median ratings_count_capped + text_reviews_count_capped per bucket.",
        columns=[
            "page_length_bucket",
            "ratings_count_capped",
            "text_reviews_count_capped",
        ],
        notes="Surface whether long reads actually earn more participation or just niche love.",
        priority="stretch",
    ),
    MetricDefinition(
        question_id="Q4",
        question="How have publication trends influenced quality and reach over time?",
        metric_id="M7",
        metric_name="Average rating by publication_year",
        description="Line chart-ready series summarizing sentiment per release year.",
        columns=["publication_year", "average_rating"],
        notes="Drop rows with null publication_year to prevent misleading dips.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q4",
        question="How have publication trends influenced quality and reach over time?",
        metric_id="M8",
        metric_name="Median ratings_count_capped by publication_year",
        description="Shows whether new releases are attracting comparable attention versus backlist titles.",
        columns=["publication_year", "ratings_count_capped"],
        notes="Use median to dampen runaway outliers in 2003–2006 era.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q5",
        question="Which languages and publishers dominate catalog quality and reach?",
        metric_id="M9",
        metric_name="Average rating by language_code",
        description="Ranks languages with at least 50 canonical titles to keep cohorts meaningful.",
        columns=["language_code", "canonical_book_id", "average_rating"],
        notes="Filter `language_code` != null and require book_count >= 50.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q5",
        question="Which languages and publishers dominate catalog quality and reach?",
        metric_id="M10",
        metric_name="Median ratings_count_capped by publisher",
        description="Highlights publishers that consistently mobilize large audiences.",
        columns=["publisher", "canonical_book_id", "ratings_count_capped"],
        notes="Limit to publishers with >= 25 canonical titles to avoid vanity presses skewing results.",
        priority="stretch",
    ),
    MetricDefinition(
        question_id="Q6",
        question="What portion of the catalog consists of deduplicated editions?",
        metric_id="M11",
        metric_name="Duplicate share of catalog",
        description="Percentage of rows where is_duplicate == True.",
        columns=["is_duplicate", "canonical_book_id"],
        notes="Communicates why canonical IDs are required for dashboards.",
        priority="core",
    ),
    MetricDefinition(
        question_id="Q6",
        question="What portion of the catalog consists of deduplicated editions?",
        metric_id="M12",
        metric_name="Engagement uplift for canonical editions",
        description="Compare median ratings_count between canonical parents and duplicate children.",
        columns=["canonical_book_id", "is_duplicate", "ratings_count"],
        notes="Quantifies whether duplicate SKUs materially change demand signals.",
        priority="stretch",
    ),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate cleaned dataset columns and emit a metrics catalog table.",
    )
    parser.add_argument(
        "--books-csv",
        default=str(DEFAULT_BOOKS_CSV),
        help="Path to the cleaned books CSV (default: data/derived/books_clean.csv)",
    )
    parser.add_argument(
        "--output-markdown",
        default=str(DEFAULT_OUTPUT_MD),
        help="Destination markdown file for the metrics mapping table (default: outputs/phase04_metrics_catalog.md)",
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
        raise FileNotFoundError(f"Cleaned CSV not found at {path}")
    LOGGER.info("Reading cleaned dataset from %s", path)
    df = pd.read_csv(path)
    LOGGER.info("Loaded %s rows and %s columns", f"{len(df):,}", df.shape[1])
    return df


def ensure_required_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise KeyError(f"Missing required columns for metrics planning: {missing}")
    LOGGER.info("All %d required columns are present", len(set(columns)))


def build_metrics_dataframe() -> pd.DataFrame:
    rows = [asdict(item) for item in METRIC_DEFINITIONS]
    df = pd.DataFrame(rows)
    ordered_cols = [
        "question_id",
        "question",
        "metric_id",
        "metric_name",
        "description",
        "columns",
        "notes",
        "priority",
    ]
    return df[ordered_cols]


def render_markdown_table(df: pd.DataFrame) -> str:
    header = "| Question | Metric | Description | Columns | Notes | Priority |"
    separator = "| --- | --- | --- | --- | --- | --- |"
    lines = [header, separator]
    for _, row in df.iterrows():
        columns_str = ", ".join(row["columns"])
        lines.append(
            f"| {row['question_id']} – {row['question']} | {row['metric_id']} – {row['metric_name']} | "
            f"{row['description']} | `{columns_str}` | {row['notes']} | {row['priority']} |"
        )
    return "\n".join(lines)


def write_markdown_table(markdown: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(markdown, encoding="utf-8")
    LOGGER.info("Metrics catalog written to %s", destination)


def summarize_dataset_for_questions(df: pd.DataFrame) -> None:
    coverage = {column: int(df[column].notna().sum()) for column in [
        "average_rating",
        "ratings_count",
        "text_reviews_count",
        "num_pages",
        "publication_year",
    ] if column in df.columns}
    LOGGER.info("Non-null coverage snapshot: %s", coverage)

    duplicate_share = df["is_duplicate"].mean() if "is_duplicate" in df.columns else float("nan")
    LOGGER.info("Duplicate share: %.2f%%", duplicate_share * 100 if pd.notna(duplicate_share) else float("nan"))


def run(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    configure_logging(args.log_level)
    df_clean = load_cleaned_books(Path(args.books_csv))

    ensure_required_columns(df_clean, KEY_COLUMNS)
    summarize_dataset_for_questions(df_clean)

    metrics_df = build_metrics_dataframe()
    markdown = render_markdown_table(metrics_df)
    write_markdown_table(markdown, Path(args.output_markdown))

    LOGGER.info("Defined %d metrics across %d business questions", metrics_df.shape[0], metrics_df['question_id'].nunique())


if __name__ == "__main__":  # pragma: no cover
    run()
