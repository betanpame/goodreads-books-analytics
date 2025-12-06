"""Portfolio 02 - deep-dive EDA entry point for the Goodreads books dataset.

This CLI standardizes the exploratory flow after the initial inspection by
loading the Phase 02 cleaned export, configuring plotting defaults, and
producing the univariate/bivariate visuals that later storytelling phases reuse.
It acts as the long-form evidence that the raw ingestion rules translate into
defensible insights, all while remaining automatable via Docker.
"""

from __future__ import annotations

import argparse
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.raw_ingestion import load_books_csv

LOGGER = logging.getLogger(__name__)
DEFAULT_CSV_PATH = Path("data") / "books.csv"
DEFAULT_OUTPUT_DIR = Path("outputs") / "phase03_univariate"
CLEANING_RULES_DOC = Path("docs") / "data-cleaning-rules.md"

NUMERIC_COLUMNS = {
    "average_rating": "average_rating",
    "num_pages": "  num_pages",
    "ratings_count": "ratings_count",
    "text_reviews_count": "text_reviews_count",
}
LOG_SCALE_COLUMNS = {"ratings_count", "text_reviews_count"}
CATEGORICAL_ANALYSIS_PLAN = [
    {"column": "language_code", "label": "language_code", "top_n": 12},
    {"column": "publisher", "label": "publisher", "top_n": 15},
    {"column": "authors", "label": "authors", "top_n": 15},
]
CATEGORY_RELATIONSHIP_PLAN = [
    {"column": "language_code", "label": "language", "title": "Language", "top_n": 10},
    {"column": "publisher", "label": "publisher", "title": "Publisher", "top_n": 15},
]
PARTIAL_DUPLICATE_SUBSET = ["title", "authors", "publication_date"]
OUTLIER_INSPECTION_PLAN = [
    {
        "label": "average_rating",
        "column": NUMERIC_COLUMNS["average_rating"],
        "display_name": "Average Rating",
        "log_scale": False,
        "valid_min": 0.0,
        "valid_max": 5.0,
    },
    {
        "label": "num_pages",
        "column": NUMERIC_COLUMNS["num_pages"],
        "display_name": "Number of Pages",
        "log_scale": False,
        "valid_min": 1.0,
        "suspect_low": 10.0,
        "suspect_high": 2000.0,
    },
    {
        "label": "ratings_count",
        "column": NUMERIC_COLUMNS["ratings_count"],
        "display_name": "Ratings Count",
        "log_scale": True,
        "valid_min": 0.0,
    },
    {
        "label": "text_reviews_count",
        "column": NUMERIC_COLUMNS["text_reviews_count"],
        "display_name": "Text Reviews Count",
        "log_scale": True,
        "valid_min": 0.0,
    },
]
COUNT_OUTLIER_COLUMNS = ("ratings_count", "text_reviews_count")
PAGE_BUCKET_BOUNDS = [0, 200, 400, 600, float("inf")]
PAGE_BUCKET_LABELS = ["0-199", "200-399", "400-599", "600+"]
RATINGS_COUNT_CAP = 597_244
TEXT_REVIEWS_COUNT_CAP = 14_812
PUBLICATION_YEAR_MIN = 1800
FUTURE_YEAR_BUFFER_YEARS = 2
LANGUAGE_CODE_PATTERN = r"^[A-Za-z-]+$"

sns.set_theme(style="whitegrid", palette="deep", context="notebook")
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 11,
})
pd.options.display.max_columns = 20
np.set_printoptions(suppress=True, linewidth=120)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap script for Goodreads univariate EDA."
    )
    parser.add_argument(
        "--csv-path",
        default=str(DEFAULT_CSV_PATH),
        help="Path to the books CSV produced in Phase 02 (default: data/books.csv)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optionally limit the number of rows loaded for quicker iterations.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Emit additional DataFrame metadata for sanity checks.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where numeric summaries and plots will be written.",
    )
    return parser.parse_args(argv)


def configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def load_dataset(csv_path: Path, limit: Optional[int] = None) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find CSV at {csv_path.resolve()}")

    LOGGER.info("Loading dataset from %s", csv_path)
    df, stats = load_books_csv(str(csv_path))
    LOGGER.info(
        "Raw loader repaired %d row(s) out of %d",
        stats.repaired_rows,
        stats.total_rows,
    )

    if limit:
        df = df.head(limit)
        LOGGER.info("Applied row limit -> new shape %s", df.shape)
    else:
        LOGGER.info("Loaded shape: (rows=%d, columns=%d)", df.shape[0], df.shape[1])
    return df


def add_publication_year_column(df: pd.DataFrame) -> pd.DataFrame:
    if "publication_date" not in df.columns:
        LOGGER.warning("publication_date column missing; skipping year derivation")
        return df

    df = df.copy()
    parsed_dates = pd.to_datetime(df["publication_date"], errors="coerce")
    df["publication_year"] = parsed_dates.dt.year

    populated = df["publication_year"].notna().sum()
    total = len(df)
    coverage = (populated / total * 100) if total else 0
    LOGGER.info(
        "Derived publication_year for %d rows (%.1f%% coverage)",
        populated,
        coverage,
    )
    missing = total - populated
    if missing:
        LOGGER.warning("publication_year missing for %d row(s)", missing)
    return df


def preview_dataframe(df: pd.DataFrame, *, max_rows: int = 5) -> None:
    LOGGER.info("Column names: %s", df.columns.tolist())
    LOGGER.info("Head (first %d rows):\n%s", max_rows, df.head(max_rows))


def analyze_numeric_distributions(
    df: pd.DataFrame,
    *,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for clean_name, raw_name in NUMERIC_COLUMNS.items():
        if raw_name not in df.columns:
            LOGGER.warning("Column %s missing from DataFrame", raw_name)
            continue

        series = pd.to_numeric(df[raw_name], errors="coerce").dropna()
        if series.empty:
            LOGGER.warning("Column %s has no numeric data after coercion", raw_name)
            continue

        describe = series.describe(percentiles=[0.25, 0.5, 0.75])
        summaries.append(
            {
                "column": clean_name,
                "count": int(describe["count"]),
                "mean": float(describe["mean"]),
                "std": float(describe["std"]),
                "min": float(describe["min"]),
                "25%": float(describe["25%"]),
                "50%": float(describe["50%"]),
                "75%": float(describe["75%"]),
                "max": float(describe["max"]),
            }
        )

        LOGGER.info(
            "%s stats -> mean=%.2f, median=%.2f, min=%.2f, max=%.2f",
            clean_name,
            describe["mean"],
            describe["50%"],
            describe["min"],
            describe["max"],
        )

        save_distribution_plot(
            series,
            clean_name=clean_name,
            output_dir=output_dir,
            log_scale=clean_name in LOG_SCALE_COLUMNS,
        )

    if summaries:
        summary_df = pd.DataFrame(summaries)
        summary_path = output_dir / "numeric_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        LOGGER.info("Wrote numeric summary to %s", summary_path)


def save_distribution_plot(
    series: pd.Series,
    *,
    clean_name: str,
    output_dir: Path,
    log_scale: bool = False,
) -> None:
    fig, ax = plt.subplots()
    sns.histplot(series, bins=50, kde=True, ax=ax, color="#0066CC")
    ax.set_title(f"Distribution of {clean_name}")
    ax.set_xlabel(clean_name)
    ax.set_ylabel("Count")
    if log_scale:
        ax.set_xscale("log")
        ax.set_xlabel(f"{clean_name} (log scale)")
    fig.tight_layout()
    plot_path = output_dir / f"{clean_name}_distribution.png"
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)
    LOGGER.info("Saved %s distribution plot to %s", clean_name, plot_path)


def analyze_categorical_distributions(df: pd.DataFrame, *, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for plan in CATEGORICAL_ANALYSIS_PLAN:
        column = plan["column"]
        if column not in df.columns:
            LOGGER.warning("Column %s missing from DataFrame", column)
            continue

        label = plan["label"]
        top_n = plan["top_n"]
        series = df[column].fillna("Unknown").astype(str).str.strip()
        series = series.replace("", "Unknown")
        counts = series.value_counts(dropna=True)

        value_count_path = output_dir / f"{label}_value_counts.csv"
        counts.to_csv(value_count_path, header=["count"])
        LOGGER.info("Saved %s value counts to %s", label, value_count_path)

        top_counts = counts.head(top_n)
        if top_counts.empty:
            continue

        bar_path = output_dir / f"{label}_top_{top_n}_bar.png"
        save_bar_plot(top_counts, clean_name=label, output_path=bar_path)
        LOGGER.info(
            "%s top %d categories -> %s",
            label,
            top_n,
            ", ".join(
                f"{cat} ({count})" for cat, count in top_counts.items()
            ),
        )


def save_bar_plot(counts: pd.Series, *, clean_name: str, output_path: Path) -> None:
    fig, ax = plt.subplots()
    counts.sort_values().plot(kind="barh", ax=ax, color="#157A6E")
    ax.set_title(f"Top {len(counts)} {clean_name}")
    ax.set_xlabel("Number of books")
    ax.set_ylabel(clean_name)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_numeric_boxplot(
    series: pd.Series,
    *,
    label: str,
    output_path: Path,
    log_scale: bool = False,
) -> None:
    cleaned = series.dropna()
    if log_scale:
        cleaned = cleaned[cleaned > 0]
    if cleaned.empty:
        LOGGER.warning("Skipping %s boxplot; no valid values", label)
        return

    fig, ax = plt.subplots(figsize=(8, 2.8))
    sns.boxplot(x=cleaned, ax=ax, color="#E15759")
    if log_scale:
        ax.set_xscale("log")
    ax.set_title(f"{label.replace('_', ' ').title()} boxplot (IQR rule)")
    ax.set_xlabel(label.replace("_", " ").title())
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_numeric_histogram(
    series: pd.Series,
    *,
    label: str,
    output_path: Path,
    log_scale: bool = False,
) -> None:
    cleaned = series.dropna()
    if log_scale:
        cleaned = cleaned[cleaned > 0]
    if cleaned.empty:
        LOGGER.warning("Skipping %s histogram; no valid values", label)
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(cleaned, bins=40, ax=ax, color="#4E79A7")
    if log_scale:
        ax.set_xscale("log")
    ax.set_title(f"{label.replace('_', ' ').title()} distribution (log={'yes' if log_scale else 'no'})")
    ax.set_xlabel(label.replace("_", " ").title())
    ax.set_ylabel("Book count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def record_rule_violation(
    df: pd.DataFrame,
    *,
    mask: pd.Series,
    source_column: str,
    label: str,
    rule_key: str,
    description: str,
    output_dir: Path,
    records: list[dict[str, object]],
    extra_columns: Optional[list[str]] = None,
    sample_limit: int = 25,
) -> None:
    if mask is None:
        return
    effective_mask = mask.fillna(False)
    if not bool(effective_mask.any()):
        return

    sample_cols = [col for col in ["bookID", "title", "authors"] if col in df.columns]
    if extra_columns:
        sample_cols.extend(extra_columns)
    elif source_column:
        sample_cols.append(source_column)
    sample_cols = [col for col in dict.fromkeys(sample_cols) if col in df.columns]
    sample_frame = df.loc[effective_mask, sample_cols].head(sample_limit).copy()
    if source_column and source_column in sample_frame.columns and source_column != label:
        sample_frame = sample_frame.rename(columns={source_column: label})

    sample_path = output_dir / f"{label}_{rule_key}.csv"
    sample_frame.to_csv(sample_path, index=False)
    records.append(
        {
            "column": label,
            "rule": rule_key,
            "description": description,
            "row_count": int(effective_mask.sum()),
            "sample_file": sample_path.name,
        }
    )


def compute_iqr_bounds(series: pd.Series, *, multiplier: float = 1.5) -> Optional[dict[str, float]]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None

    q1 = float(clean.quantile(0.25))
    q3 = float(clean.quantile(0.75))
    iqr = q3 - q1
    if iqr == 0:
        lower = upper = q1
    else:
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower": float(lower),
        "upper": float(upper),
        "median": float(clean.median()),
        "min": float(clean.min()),
        "max": float(clean.max()),
        "count": int(clean.count()),
    }


def detect_language_code_issues(
    df: pd.DataFrame,
    *,
    output_dir: Path,
    records: list[dict[str, object]],
) -> None:
    column = "language_code"
    if column not in df.columns:
        LOGGER.warning("%s column missing; skipping language checks", column)
        return

    series = df[column].fillna("").astype(str).str.strip()
    pattern = re.compile(LANGUAGE_CODE_PATTERN)
    non_ascii_mask = series.str.contains(r"[^A-Za-z-]", na=False)
    empty_mask = series.eq("")
    long_mask = series.str.len() > 8
    invalid_pattern_mask = ~series.str.match(pattern, na=False)

    record_rule_violation(
        df,
        mask=empty_mask,
        source_column=column,
        label=column,
        rule_key="blank_language_code",
        description="Language code is blank after trimming",
        output_dir=output_dir,
        records=records,
    )
    record_rule_violation(
        df,
        mask=non_ascii_mask,
        source_column=column,
        label=column,
        rule_key="non_alpha_language_code",
        description="Language code contains digits or special characters",
        output_dir=output_dir,
        records=records,
    )
    record_rule_violation(
        df,
        mask=long_mask,
        source_column=column,
        label=column,
        rule_key="language_code_too_long",
        description="Language code exceeds 8 characters",
        output_dir=output_dir,
        records=records,
    )
    record_rule_violation(
        df,
        mask=invalid_pattern_mask & ~empty_mask,
        source_column=column,
        label=column,
        rule_key="language_code_pattern_mismatch",
        description="Language code fails the alpha-or-hyphen pattern",
        output_dir=output_dir,
        records=records,
    )


def detect_publication_year_issues(
    df: pd.DataFrame,
    *,
    output_dir: Path,
    records: list[dict[str, object]],
) -> None:
    column = "publication_year"
    if column not in df.columns:
        LOGGER.warning("%s column missing; skipping year checks", column)
        return

    year_series = pd.to_numeric(df[column], errors="coerce")
    if year_series.dropna().empty:
        LOGGER.warning("No valid publication_year rows to inspect")
        return

    current_year = datetime.utcnow().year
    future_cap = current_year + FUTURE_YEAR_BUFFER_YEARS
    old_mask = year_series < PUBLICATION_YEAR_MIN
    future_mask = year_series > future_cap

    record_rule_violation(
        df,
        mask=old_mask,
        source_column=column,
        label=column,
        rule_key="year_too_old",
        description=f"Publication year < {PUBLICATION_YEAR_MIN}",
        output_dir=output_dir,
        records=records,
        extra_columns=["publication_date"],
    )
    record_rule_violation(
        df,
        mask=future_mask,
        source_column=column,
        label=column,
        rule_key="year_in_future",
        description=f"Publication year > {future_cap}",
        output_dir=output_dir,
        records=records,
        extra_columns=["publication_date"],
    )


def analyze_outliers_and_inconsistencies(df: pd.DataFrame, *, output_dir: Path) -> None:
    quality_dir = output_dir / "step03_task02_outliers"
    plots_dir = quality_dir / "plots"
    quality_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    numeric_summary: list[dict[str, object]] = []
    rule_records: list[dict[str, object]] = []

    for plan in OUTLIER_INSPECTION_PLAN:
        column = plan["column"]
        label = plan["label"]
        if column not in df.columns:
            LOGGER.warning("Column %s missing; skipping outlier check", column)
            continue

        series = pd.to_numeric(df[column], errors="coerce")
        clean = series.dropna()
        if clean.empty:
            LOGGER.warning("Column %s has no numeric data to inspect", column)
            continue

        bounds = compute_iqr_bounds(series)
        if bounds is None:
            continue

        summary_row = {
            "column": label,
            "count": bounds["count"],
            "min": bounds["min"],
            "q1": bounds["q1"],
            "median": bounds["median"],
            "q3": bounds["q3"],
            "max": bounds["max"],
            "iqr": bounds["iqr"],
            "iqr_lower": bounds["lower"],
            "iqr_upper": bounds["upper"],
        }
        for rule_key in ("valid_min", "valid_max", "suspect_low", "suspect_high"):
            if rule_key in plan:
                summary_row[rule_key] = plan[rule_key]
        numeric_summary.append(summary_row)

        plot_numeric_boxplot(
            clean,
            label=label,
            output_path=plots_dir / f"{label}_boxplot.png",
            log_scale=plan.get("log_scale", False),
        )
        plot_numeric_histogram(
            clean,
            label=label,
            output_path=plots_dir / f"{label}_hist.png",
            log_scale=plan.get("log_scale", False),
        )

        iqr_mask = (series < bounds["lower"]) | (series > bounds["upper"])
        record_rule_violation(
            df,
            mask=iqr_mask,
            source_column=column,
            label=label,
            rule_key="iqr_outlier",
            description="Outside 1.5×IQR bounds",
            output_dir=quality_dir,
            records=rule_records,
        )

        valid_min = plan.get("valid_min")
        valid_max = plan.get("valid_max")
        if valid_min is not None:
            record_rule_violation(
                df,
                mask=series < valid_min,
                source_column=column,
                label=label,
                rule_key="below_valid_min",
                description=f"Falls below hard minimum {valid_min}",
                output_dir=quality_dir,
                records=rule_records,
            )
        if valid_max is not None:
            record_rule_violation(
                df,
                mask=series > valid_max,
                source_column=column,
                label=label,
                rule_key="above_valid_max",
                description=f"Exceeds hard maximum {valid_max}",
                output_dir=quality_dir,
                records=rule_records,
            )

        suspect_low = plan.get("suspect_low")
        suspect_high = plan.get("suspect_high")
        if suspect_low is not None:
            record_rule_violation(
                df,
                mask=series < suspect_low,
                source_column=column,
                label=label,
                rule_key="suspect_low",
                description=f"Below soft lower bound {suspect_low}",
                output_dir=quality_dir,
                records=rule_records,
            )
        if suspect_high is not None:
            record_rule_violation(
                df,
                mask=series > suspect_high,
                source_column=column,
                label=label,
                rule_key="suspect_high",
                description=f"Above soft upper bound {suspect_high}",
                output_dir=quality_dir,
                records=rule_records,
            )

    detect_publication_year_issues(df, output_dir=quality_dir, records=rule_records)
    detect_language_code_issues(df, output_dir=quality_dir, records=rule_records)

    if numeric_summary:
        summary_path = quality_dir / "numeric_outlier_summary.csv"
        pd.DataFrame(numeric_summary).to_csv(summary_path, index=False)
        LOGGER.info("Saved numeric outlier summary to %s", summary_path)

    if rule_records:
        rules_path = quality_dir / "outlier_rule_violations.csv"
        pd.DataFrame(rule_records).to_csv(rules_path, index=False)
        LOGGER.info("Saved %d rule violations to %s", len(rule_records), rules_path)
    else:
        LOGGER.info("No rule violations detected for Task 02")


def summarize_count_outliers(df: pd.DataFrame, *, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    quantiles = {
        "p95": 0.95,
        "p99": 0.99,
        "p99_5": 0.995,
    }

    for column in COUNT_OUTLIER_COLUMNS:
        if column not in df.columns:
            LOGGER.warning("Column %s missing from DataFrame", column)
            continue

        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if series.empty:
            continue

        quantile_values = {
            name: float(series.quantile(value)) for name, value in quantiles.items()
        }
        suggested_cap = quantile_values["p99_5"]
        summaries.append(
            {
                "column": column,
                **quantile_values,
                "max": float(series.max()),
                "suggested_cap": suggested_cap,
            }
        )

        LOGGER.info(
            "%s outliers -> p99 %.0f, max %.0f, suggested cap %.0f",
            column,
            quantile_values["p99"],
            series.max(),
            suggested_cap,
        )

        top_titles = (
            df[["title", column]]
            .assign(**{column: pd.to_numeric(df[column], errors="coerce")})
            .dropna(subset=[column])
            .sort_values(by=column, ascending=False)
            .head(20)
        )
        top_path = output_dir / f"{column}_top_titles.csv"
        top_titles.to_csv(top_path, index=False)
        LOGGER.info("Saved top %s titles to %s", column, top_path)

    if summaries:
        summary_path = output_dir / "count_outlier_recommendations.csv"
        pd.DataFrame(summaries).to_csv(summary_path, index=False)
        LOGGER.info("Wrote outlier cap recommendations to %s", summary_path)


def analyze_temporal_trends(df: pd.DataFrame, *, output_dir: Path) -> None:
    if "publication_year" not in df.columns:
        LOGGER.warning("publication_year column missing; skipping temporal trends")
        return

    temporal_dir = output_dir / "step02_task02_temporal"
    temporal_dir.mkdir(parents=True, exist_ok=True)

    temporal_frame = pd.DataFrame({
        "publication_year": pd.to_numeric(df["publication_year"], errors="coerce"),
        "average_rating": pd.to_numeric(df["average_rating"], errors="coerce"),
        "ratings_count": pd.to_numeric(df["ratings_count"], errors="coerce").clip(upper=RATINGS_COUNT_CAP),
    }).dropna(subset=["publication_year"])

    if temporal_frame.empty:
        LOGGER.warning("No valid publication_year values for temporal analysis")
        return

    temporal_frame["publication_year"] = temporal_frame["publication_year"].astype(int)

    book_counts = (
        temporal_frame.groupby("publication_year")
        .size()
        .reset_index(name="book_count")
        .sort_values("publication_year")
    )
    book_counts_path = temporal_dir / "books_published_per_year.csv"
    book_counts.to_csv(book_counts_path, index=False)
    LOGGER.info("Saved books-per-year summary to %s", book_counts_path)
    plot_line_trend(
        data=book_counts,
        x_col="publication_year",
        y_col="book_count",
        title="Books published per year",
        ylabel="Book count",
        output_path=temporal_dir / "books_published_per_year_line.png",
    )

    avg_rating = (
        temporal_frame.dropna(subset=["average_rating"])
        .groupby("publication_year")
        .agg(avg_rating=("average_rating", "mean"))
        .reset_index()
        .sort_values("publication_year")
    )
    avg_rating_path = temporal_dir / "average_rating_by_year.csv"
    avg_rating.to_csv(avg_rating_path, index=False)
    LOGGER.info("Saved average rating by year to %s", avg_rating_path)
    plot_line_trend(
        data=avg_rating,
        x_col="publication_year",
        y_col="avg_rating",
        title="Average rating by publication year",
        ylabel="Average rating",
        output_path=temporal_dir / "average_rating_by_year_line.png",
    )

    avg_ratings_count = (
        temporal_frame.dropna(subset=["ratings_count"])
        .groupby("publication_year")
        .agg(avg_ratings_count=("ratings_count", "mean"))
        .reset_index()
        .sort_values("publication_year")
    )
    avg_ratings_count_path = temporal_dir / "average_ratings_count_by_year.csv"
    avg_ratings_count.to_csv(avg_ratings_count_path, index=False)
    LOGGER.info("Saved average ratings_count by year to %s", avg_ratings_count_path)
    plot_line_trend(
        data=avg_ratings_count,
        x_col="publication_year",
        y_col="avg_ratings_count",
        title="Average ratings count by publication year",
        ylabel="Average ratings count (capped)",
        output_path=temporal_dir / "average_ratings_count_by_year_line.png",
    )


def analyze_rating_relationships(df: pd.DataFrame, *, output_dir: Path) -> None:
    relationships_dir = output_dir / "step02_task01_relationships"
    relationships_dir.mkdir(parents=True, exist_ok=True)

    rating_series = pd.to_numeric(df.get("average_rating"), errors="coerce")
    pages_series = pd.to_numeric(df.get("  num_pages"), errors="coerce")
    ratings_count = pd.to_numeric(df.get("ratings_count"), errors="coerce")
    text_reviews = pd.to_numeric(df.get("text_reviews_count"), errors="coerce")

    if rating_series.isna().all():
        LOGGER.warning("average_rating column is missing or empty; skipping relationships analysis")
        return

    plot_scatter_relationship(
        x=pages_series,
        y=rating_series,
        xlabel="Number of pages",
        ylabel="Average rating",
        title="Average rating vs. number of pages",
        output_path=relationships_dir / "average_rating_vs_pages_scatter.png",
    )
    log_pair_summary(pages_series, rating_series, label="num_pages vs rating")

    capped_ratings_count = ratings_count.clip(upper=RATINGS_COUNT_CAP)
    plot_scatter_relationship(
        x=capped_ratings_count,
        y=rating_series,
        xlabel="Ratings count (capped, log scale)",
        ylabel="Average rating",
        title="Average rating vs. ratings count",
        output_path=relationships_dir / "average_rating_vs_ratings_count_scatter.png",
        log_x=True,
    )
    log_pair_summary(capped_ratings_count, rating_series, label="ratings_count vs rating")

    capped_text_reviews = text_reviews.clip(upper=TEXT_REVIEWS_COUNT_CAP)
    plot_scatter_relationship(
        x=capped_text_reviews,
        y=rating_series,
        xlabel="Text reviews count (capped, log scale)",
        ylabel="Average rating",
        title="Average rating vs. text reviews count",
        output_path=relationships_dir / "average_rating_vs_text_reviews_scatter.png",
        log_x=True,
    )
    log_pair_summary(capped_text_reviews, rating_series, label="text_reviews_count vs rating")

    summarize_page_buckets(
        pages_series=pages_series,
        rating_series=rating_series,
        output_dir=relationships_dir,
    )


def plot_scatter_relationship(
    *,
    x: pd.Series,
    y: pd.Series,
    xlabel: str,
    ylabel: str,
    title: str,
    output_path: Path,
    log_x: bool = False,
) -> None:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if frame.empty:
        LOGGER.warning("Insufficient data for plot %s", output_path.name)
        return

    fig, ax = plt.subplots()
    sns.scatterplot(
        data=frame,
        x="x",
        y="y",
        ax=ax,
        alpha=0.3,
        s=18,
        color="#1f77b4",
        edgecolor=None,
    )
    if log_x:
        ax.set_xscale("log")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    LOGGER.info("Saved relationship plot to %s", output_path)


def plot_line_trend(
    *,
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    ylabel: str,
    output_path: Path,
) -> None:
    if data.empty:
        LOGGER.warning("No data provided for line plot %s", output_path.name)
        return

    fig, ax = plt.subplots()
    sns.lineplot(data=data, x=x_col, y=y_col, ax=ax, marker="o", color="#2ca02c")
    ax.set_title(title)
    ax.set_xlabel("Publication year")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    LOGGER.info("Saved line plot to %s", output_path)


def log_pair_summary(x: pd.Series, y: pd.Series, *, label: str) -> None:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if frame.empty:
        LOGGER.warning("No overlapping data points for %s", label)
        return
    correlation = frame["x"].corr(frame["y"])
    LOGGER.info(
        "%s -> n=%d, pearson_corr=%.3f, x_median=%.2f, y_median=%.2f",
        label,
        len(frame),
        correlation,
        frame["x"].median(),
        frame["y"].median(),
    )


def summarize_page_buckets(
    *,
    pages_series: pd.Series,
    rating_series: pd.Series,
    output_dir: Path,
) -> None:
    bucketed = pd.cut(
        pages_series,
        bins=PAGE_BUCKET_BOUNDS,
        labels=PAGE_BUCKET_LABELS,
        right=False,
    )
    bucket_frame = pd.DataFrame({
        "bucket": bucketed,
        "rating": rating_series,
    }).dropna()
    if bucket_frame.empty:
        LOGGER.warning("No data available for page bucket summary")
        return

    grouped = (
        bucket_frame
        .groupby("bucket", observed=True)
        .agg(
            avg_rating=("rating", "mean"),
            median_rating=("rating", "median"),
            book_count=("rating", "size"),
        )
        .reset_index()
    )
    output_csv = output_dir / "average_rating_by_page_bucket.csv"
    grouped.to_csv(output_csv, index=False)
    LOGGER.info("Saved page bucket summary to %s", output_csv)

    fig, ax = plt.subplots()
    sns.barplot(data=grouped, x="bucket", y="avg_rating", ax=ax, color="#ff7f0e")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f")
    ax.set_xlabel("Page bucket")
    ax.set_ylabel("Average rating")
    ax.set_title("Average rating by page bucket")
    fig.tight_layout()
    fig.savefig(output_dir / "average_rating_by_page_bucket_bar.png", dpi=150)
    plt.close(fig)

def analyze_category_relationships(df: pd.DataFrame, *, output_dir: Path) -> None:
    category_dir = output_dir / "step02_task03_category_relationships"
    category_dir.mkdir(parents=True, exist_ok=True)

    rating_series = pd.to_numeric(df.get("average_rating"), errors="coerce")
    ratings_count_series = pd.to_numeric(df.get("ratings_count"), errors="coerce")
    text_reviews_series = pd.to_numeric(df.get("text_reviews_count"), errors="coerce")

    if rating_series.isna().all():
        LOGGER.warning("average_rating column missing; skipping category relationships")
        return

    base_frame = pd.DataFrame({
        "average_rating": rating_series,
        "ratings_count": ratings_count_series,
        "text_reviews_count": text_reviews_series,
    })

    for plan in CATEGORY_RELATIONSHIP_PLAN:
        column = plan["column"]
        if column not in df.columns:
            LOGGER.warning("Column %s missing; skipping category relationship", column)
            continue

        series = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )
        working = base_frame.copy()
        working[column] = series
        working = working.dropna(subset=["average_rating"])
        if working.empty:
            LOGGER.warning("No usable rows for column %s", column)
            continue

        top_n = plan["top_n"]
        top_categories = (
            working[column]
            .value_counts()
            .head(top_n)
            .index
        )
        filtered = working[working[column].isin(top_categories)].copy()
        if filtered.empty:
            LOGGER.warning("No rows left after filtering top %d categories for %s", top_n, column)
            continue

        filtered[column] = pd.Categorical(filtered[column], categories=top_categories, ordered=True)
        grouped = (
            filtered
            .groupby(column, observed=True)
            .agg(
                avg_rating=("average_rating", "mean"),
                median_ratings_count=("ratings_count", "median"),
                median_text_reviews=("text_reviews_count", "median"),
                book_count=("average_rating", "size"),
            )
            .reset_index()
        )

        summary_csv = category_dir / f"{plan['label']}_category_summary.csv"
        grouped.to_csv(summary_csv, index=False)
        LOGGER.info(
            "%s category summary saved to %s (top %d)",
            plan["title"],
            summary_csv,
            top_n,
        )

        plot_category_metric_bar(
            grouped,
            category_column=column,
            value_column="avg_rating",
            ylabel="Average rating",
            title=f"Average rating by top {plan['title'].lower()}s",
            output_path=category_dir / f"avg_rating_by_{plan['label']}.png",
        )
        plot_category_metric_bar(
            grouped,
            category_column=column,
            value_column="median_ratings_count",
            ylabel="Median ratings count",
            title=f"Median ratings count by top {plan['title'].lower()}s",
            output_path=category_dir / f"median_ratings_count_by_{plan['label']}.png",
        )


def normalize_categorical_series(series: pd.Series) -> pd.Series:
    return series.fillna("Unknown").astype(str).str.strip().replace("", "Unknown")

def plot_category_metric_bar(
    grouped: pd.DataFrame,
    *,
    category_column: str,
    value_column: str,
    ylabel: str,
    title: str,
    output_path: Path,
) -> None:
    if grouped.empty:
        LOGGER.warning("Cannot plot %s because grouped frame is empty", output_path.name)
        return

    ordered = grouped.sort_values(value_column, ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ordered, x=category_column, y=value_column, ax=ax, color="#1f77b4")
    ax.set_xlabel(category_column.replace("_", " ").title())
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def analyze_missing_and_duplicates(df: pd.DataFrame, *, output_dir: Path) -> None:
    quality_dir = output_dir / "step03_task01_missing_duplicates"
    quality_dir.mkdir(parents=True, exist_ok=True)

    total_rows = len(df)
    missing_counts = df.isna().sum().rename("missing_count")
    missing_pct = ((missing_counts / total_rows) * 100).rename("missing_pct")
    missing_summary = (
        pd.concat([missing_counts, missing_pct], axis=1)
        .reset_index()
        .rename(columns={"index": "column"})
        .sort_values("missing_pct", ascending=False)
    )
    missing_path = quality_dir / "missing_values_summary.csv"
    missing_summary.to_csv(missing_path, index=False)
    LOGGER.info("Saved missing-value summary to %s", missing_path)

    full_duplicate_count = int(df.duplicated().sum())
    LOGGER.info("Full row duplicates identified: %d", full_duplicate_count)
    duplicate_report = pd.DataFrame([
        {
            "duplicate_type": "full_row",
            "count": full_duplicate_count,
        }
    ])

    duplicates_sample = df[df.duplicated(keep=False)].copy()
    if not duplicates_sample.empty:
        sample_path = quality_dir / "full_duplicate_records.csv"
        duplicates_sample.to_csv(sample_path, index=False)
        LOGGER.info("Saved %d duplicate rows to %s", len(duplicates_sample), sample_path)

    subset = [col for col in PARTIAL_DUPLICATE_SUBSET if col in df.columns]
    partial_count = 0
    if len(subset) >= 2:
        normalized = {col: normalize_categorical_series(df[col]) for col in subset}
        subset_frame = pd.DataFrame(normalized)
        mask = subset_frame.duplicated(keep=False)
        partial = df.loc[mask, subset + ["bookID"]].copy() if "bookID" in df.columns else df.loc[mask, subset].copy()
        partial_count = int(mask.sum())
        duplicate_report = pd.concat([
            duplicate_report,
            pd.DataFrame([
                {
                    "duplicate_type": "partial_subset",
                    "subset": "|".join(subset),
                    "count": partial_count,
                }
            ]),
        ], ignore_index=True)
        if not partial.empty:
            partial_path = quality_dir / "partial_duplicates_by_subset.csv"
            partial.to_csv(partial_path, index=False)
            LOGGER.info(
                "Saved %d partial-duplicate rows (subset=%s) to %s",
                len(partial),
                ", ".join(subset),
                partial_path,
            )
    else:
        LOGGER.warning("Not enough columns available for partial duplicate check; need at least 2, found %d", len(subset))

    duplicate_report_path = quality_dir / "duplicate_summary.csv"
    duplicate_report.to_csv(duplicate_report_path, index=False)
    LOGGER.info("Wrote duplicate summary to %s", duplicate_report_path)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    configure_logging(verbose=args.verbose)

    dataset_path = Path(args.csv_path)
    df = load_dataset(dataset_path, limit=args.limit)
    df = add_publication_year_column(df)

    if args.verbose:
        preview_dataframe(df)

    output_dir = Path(args.output_dir)
    analyze_numeric_distributions(df, output_dir=output_dir)
    analyze_categorical_distributions(df, output_dir=output_dir)
    summarize_count_outliers(df, output_dir=output_dir)
    analyze_outliers_and_inconsistencies(df, output_dir=output_dir)
    analyze_temporal_trends(df, output_dir=output_dir)
    analyze_rating_relationships(df, output_dir=output_dir)
    analyze_category_relationships(df, output_dir=output_dir)
    analyze_missing_and_duplicates(df, output_dir=output_dir)

    LOGGER.info(
        "EDA pass complete – numeric, categorical, temporal, outlier, rating, category, and data-quality artifacts ready."
    )
    LOGGER.info(
        "Documented cleaning decisions live in %s — review before Phase 04 implementations.",
        CLEANING_RULES_DOC,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
