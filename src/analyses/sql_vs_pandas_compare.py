"""Phase 05 · Step 03 · Task 01 – Compare SQL outputs with pandas metrics.

This CLI loads selected analysis queries from ``sql/analysis/``, executes them
through PostgreSQL, loads the previously generated pandas metrics from
``outputs/phase04_core_metrics/``, and compares both results. The summary table
is saved under ``outputs/phase05_step03_task01/`` so task notes (and portfolio
readers) can verify SQL vs pandas parity without spinning up notebooks.
"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.db_config import build_database_url_from_env

LOGGER = logging.getLogger(__name__)
DEFAULT_OUTPUT_DIR = Path("outputs/phase05_step03_task01")
DEFAULT_NUMERIC_TOLERANCE = 1e-4


@dataclass(slots=True)
class ComparisonCase:
    """Metadata for each SQL vs pandas comparison."""

    name: str
    sql_file: Path
    pandas_csv: Path
    key_columns: Sequence[str]
    compare_columns: Sequence[str]
    numeric_columns: Sequence[str] = field(default_factory=tuple)
    metric_filter: str | None = None
    pandas_min_year: int | None = None
    rounding: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True)
class ComparisonResult:
    name: str
    rows_sql: int
    rows_pandas: int
    shared_rows: int
    row_match: bool
    value_mismatches: int
    diff_path: Path | None
    notes: str


COMPARISON_CASES: list[ComparisonCase] = [
    ComparisonCase(
        name="M1_top_authors_by_weighted_rating",
        sql_file=Path("sql/analysis/20_top_authors_weighted_rating.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M1_top_authors_by_weighted_rating.csv"),
        key_columns=("author_name",),
        compare_columns=("weighted_average_rating", "total_ratings", "book_count"),
        numeric_columns=("weighted_average_rating", "total_ratings", "book_count"),
        rounding={"weighted_average_rating": 4},
    ),
    ComparisonCase(
        name="M3_top_books_by_ratings_count",
        sql_file=Path("sql/analysis/30_top_books_by_engagement.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M3_top_books_by_ratings_count.csv"),
        key_columns=("canonical_book_id",),
        compare_columns=(
            "title",
            "average_rating",
            "ratings_count",
            "ratings_count_capped",
            "language_code",
        ),
        numeric_columns=("average_rating", "ratings_count", "ratings_count_capped"),
        metric_filter="ratings_count",
        rounding={"average_rating": 4},
    ),
    ComparisonCase(
        name="M4_top_books_by_text_reviews",
        sql_file=Path("sql/analysis/30_top_books_by_engagement.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M4_top_books_by_text_reviews.csv"),
        key_columns=("canonical_book_id",),
        compare_columns=(
            "title",
            "average_rating",
            "text_reviews_count",
            "text_reviews_count_capped",
            "language_code",
        ),
        numeric_columns=("average_rating", "text_reviews_count", "text_reviews_count_capped"),
        metric_filter="text_reviews",
        rounding={"average_rating": 4},
    ),
    ComparisonCase(
        name="M7_average_rating_by_year",
        sql_file=Path("sql/analysis/40_publication_year_trends.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M7_average_rating_by_year.csv"),
        key_columns=("publication_year",),
        compare_columns=("average_rating", "book_count"),
        numeric_columns=("average_rating", "book_count"),
        pandas_min_year=1950,
        rounding={"average_rating": 4},
    ),
    ComparisonCase(
        name="M8_median_ratings_count_by_year",
        sql_file=Path("sql/analysis/40_publication_year_trends.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M8_median_ratings_count_by_year.csv"),
        key_columns=("publication_year",),
        compare_columns=("median_ratings_count_capped", "book_count"),
        numeric_columns=("median_ratings_count_capped", "book_count"),
        pandas_min_year=1950,
    ),
    ComparisonCase(
        name="M9_language_rating_summary",
        sql_file=Path("sql/analysis/50_language_quality_summary.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M9_language_rating_summary.csv"),
        key_columns=("language_code",),
        compare_columns=("book_count", "average_rating", "median_ratings_count_capped"),
        numeric_columns=("book_count", "average_rating", "median_ratings_count_capped"),
        rounding={"average_rating": 4},
    ),
    ComparisonCase(
        name="M11_duplicate_share",
        sql_file=Path("sql/analysis/55_duplicate_share.sql"),
        pandas_csv=Path("outputs/phase04_core_metrics/M11_duplicate_share.csv"),
        key_columns=("total_rows",),
        compare_columns=("duplicate_rows", "duplicate_share_pct"),
        numeric_columns=("total_rows", "duplicate_rows", "duplicate_share_pct"),
        rounding={"duplicate_share_pct": 4},
    ),
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SQL analysis queries, load pandas counterparts, and compare the outputs."
    )
    parser.add_argument(
        "--cases",
        nargs="*",
        choices=[case.name for case in COMPARISON_CASES],
        help="Subset of comparison cases to run (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for comparison summaries (default: outputs/phase05_step03_task01)",
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


def create_engine_from_env() -> Engine:
    database_url = build_database_url_from_env()
    LOGGER.debug("Connecting to %s", database_url)
    from sqlalchemy import create_engine

    return create_engine(database_url)


def run_sql_file(engine: Engine, sql_path: Path) -> pd.DataFrame:
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    query = sql_path.read_text(encoding="utf-8")
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn)


def load_pandas_table(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Pandas metric not found: {csv_path}")
    return pd.read_csv(csv_path)


def apply_case_adjustments(case: ComparisonCase, df_sql: pd.DataFrame, df_pandas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    sql_df = df_sql.copy()
    pandas_df = df_pandas.copy()

    if case.metric_filter and "metric" in sql_df.columns:
        sql_df = sql_df.loc[sql_df["metric"] == case.metric_filter].copy()
        sql_df = sql_df.drop(columns=["metric"], errors="ignore")

    if case.pandas_min_year is not None and "publication_year" in pandas_df.columns:
        pandas_df = pandas_df.loc[pandas_df["publication_year"] >= case.pandas_min_year].copy()

    if "publication_year" in sql_df.columns:
        sql_df["publication_year"] = sql_df["publication_year"].astype(int)
    if "publication_year" in pandas_df.columns:
        pandas_df["publication_year"] = pandas_df["publication_year"].astype(float).round(0).astype(int)

    if "canonical_book_count" in sql_df.columns and "book_count" not in sql_df.columns:
        sql_df = sql_df.rename(columns={"canonical_book_count": "book_count"})

    return sql_df, pandas_df


def normalize_numeric_columns(df: pd.DataFrame, columns: Iterable[str], rounding: dict[str, int]) -> pd.DataFrame:
    normalized = df.copy()
    for col in columns:
        if col in normalized.columns:
            normalized[col] = pd.to_numeric(normalized[col], errors="coerce")
    for col, decimals in rounding.items():
        if col in normalized.columns:
            normalized[col] = pd.to_numeric(normalized[col], errors="coerce").round(decimals)
    return normalized


def select_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    available = [col for col in columns if col in df.columns]
    missing = sorted(set(columns) - set(available))
    if missing:
        raise KeyError(f"Missing columns {missing} in dataframe with columns {sorted(df.columns)}")
    return df.loc[:, available]


def compare_case(
    case: ComparisonCase,
    engine: Engine,
    output_dir: Path,
    numeric_tolerance: float = DEFAULT_NUMERIC_TOLERANCE,
) -> ComparisonResult:
    LOGGER.info("Running SQL for %s", case.name)
    df_sql_raw = run_sql_file(engine, case.sql_file)
    df_pandas_raw = load_pandas_table(case.pandas_csv)
    df_sql, df_pandas = apply_case_adjustments(case, df_sql_raw, df_pandas_raw)

    df_sql = normalize_numeric_columns(df_sql, case.numeric_columns, case.rounding)
    df_pandas = normalize_numeric_columns(df_pandas, case.numeric_columns, case.rounding)

    sql_subset = select_columns(df_sql, list(case.key_columns) + list(case.compare_columns))
    pandas_subset = select_columns(df_pandas, list(case.key_columns) + list(case.compare_columns))

    merged = sql_subset.merge(
        pandas_subset,
        on=list(case.key_columns),
        how="outer",
        suffixes=("_sql", "_pandas"),
        indicator=True,
    )

    unmatched_rows = merged.loc[merged["_merge"] != "both", case.key_columns].copy()
    row_match = unmatched_rows.empty and len(sql_subset) == len(pandas_subset)

    differences: list[dict[str, object]] = []
    shared_mask = merged["_merge"] == "both"
    shared_rows = int(shared_mask.sum())

    for column in case.compare_columns:
        col_sql = f"{column}_sql"
        col_pandas = f"{column}_pandas"
        if col_sql not in merged.columns or col_pandas not in merged.columns:
            continue

        comparison_block = merged.loc[shared_mask, list(case.key_columns) + [col_sql, col_pandas]].copy()
        if column in case.numeric_columns:
            comparison_block[col_sql] = pd.to_numeric(comparison_block[col_sql], errors="coerce")
            comparison_block[col_pandas] = pd.to_numeric(comparison_block[col_pandas], errors="coerce")
            diff_series = (comparison_block[col_sql] - comparison_block[col_pandas]).abs()
            mismatch_mask = diff_series > numeric_tolerance
        else:
            mismatch_mask = comparison_block[col_sql].fillna("<NA>") != comparison_block[col_pandas].fillna("<NA>")
            diff_series = pd.Series([None] * len(comparison_block), index=comparison_block.index)

        if mismatch_mask.any():
            mismatch_rows = comparison_block.loc[mismatch_mask]
            for _, row in mismatch_rows.iterrows():
                diff_value = diff_series.loc[row.name]
                record = {key: row[key] for key in case.key_columns}
                record.update(
                    {
                        "column": column,
                        "sql_value": row[col_sql],
                        "pandas_value": row[col_pandas],
                        "absolute_diff": diff_value,
                    }
                )
                differences.append(record)

    diff_path: Path | None = None
    if differences:
        diff_df = pd.DataFrame(differences)
        diff_path = output_dir / f"{case.name}_differences.csv"
        diff_df.to_csv(diff_path, index=False)
        LOGGER.warning("%s mismatches recorded for %s", len(diff_df), case.name)

    summary_note = "Match" if row_match and not differences else "Check differences file"
    return ComparisonResult(
        name=case.name,
        rows_sql=len(sql_subset),
        rows_pandas=len(pandas_subset),
        shared_rows=shared_rows,
        row_match=row_match,
        value_mismatches=len(differences),
        diff_path=diff_path,
        notes=summary_note,
    )


def persist_summary(results: Sequence[ComparisonResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "comparison": r.name,
            "rows_sql": r.rows_sql,
            "rows_pandas": r.rows_pandas,
            "shared_rows": r.shared_rows,
            "row_match": "yes" if r.row_match else "no",
            "value_mismatches": r.value_mismatches,
            "diff_path": str(r.diff_path) if r.diff_path else "",
            "notes": r.notes,
        }
        for r in results
    ]
    summary_df = pd.DataFrame(rows)
    csv_path = output_dir / "comparison_summary.csv"
    summary_df.to_csv(csv_path, index=False)
    LOGGER.info("Wrote summary table to %s", csv_path)

    md_lines = [
        "| Comparison | SQL rows | pandas rows | Shared rows | Row match | Value mismatches | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        md_lines.append(
            f"| {r.name} | {r.rows_sql} | {r.rows_pandas} | {r.shared_rows} | {'yes' if r.row_match else 'no'} | {r.value_mismatches} | {r.notes} |"
        )
    (output_dir / "comparison_summary.md").write_text("\n".join(md_lines), encoding="utf-8")


def run(args: argparse.Namespace) -> None:
    configure_logging(args.log_level)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_names = args.cases or [case.name for case in COMPARISON_CASES]
    cases_by_name = {case.name: case for case in COMPARISON_CASES}
    try:
        selected_cases = [cases_by_name[name] for name in selected_names]
    except KeyError as exc:  # pragma: no cover - safeguarded by argparse choices
        raise ValueError(f"Unknown case requested: {exc}") from exc

    engine = create_engine_from_env()
    results: list[ComparisonResult] = []
    for case in selected_cases:
        result = compare_case(case, engine, output_dir)
        results.append(result)

    persist_summary(results, output_dir)

    mismatches = [r for r in results if not r.row_match or r.value_mismatches > 0]
    if mismatches:
        mismatch_names = ", ".join(r.name for r in mismatches)
        LOGGER.warning("Completed with differences in: %s", mismatch_names)
    else:
        LOGGER.info("All SQL vs pandas comparisons matched")


if __name__ == "__main__":  # pragma: no cover
    run(parse_args())