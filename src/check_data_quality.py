"""Run basic data quality checks on cleaned Goodreads books data.

By default this script checks the cleaned CSV at
``data/derived/books_clean.csv``. You can extend it to
also check the PostgreSQL ``books_clean`` table.

Usage:

    python -m src.check_data_quality

Exit code is 0 when all critical checks pass, non-zero otherwise.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List

import pandas as pd


def check_clean_csv(path: str = "data/derived/books_clean.csv") -> bool:
    """Run simple sanity checks on the cleaned CSV.

    Returns True if all checks pass, False otherwise.
    """

    csv_path = Path(path)
    if not csv_path.exists():
        print(f"[dq] ERROR: Cleaned CSV not found at {csv_path}")
        return False

    df = pd.read_csv(csv_path)
    print(f"[dq] Loaded cleaned CSV with {len(df):,} rows from {csv_path}")

    passed = True

    # Example checks – extend based on your rules
    if len(df) == 0:
        print("[dq] ERROR: Cleaned dataset is empty.")
        passed = False

    critical_cols = ["average_rating", "num_pages", "ratings_count"]
    for col in critical_cols:
        if col not in df.columns:
            print(f"[dq] ERROR: Missing expected column: {col}")
            passed = False
            continue
        nulls = df[col].isna().sum()
        print(f"[dq] Column {col}: {nulls} nulls")

    if "average_rating" in df.columns:
        invalid = ~df["average_rating"].between(0, 5)
        count_invalid = invalid.sum()
        if count_invalid > 0:
            print(f"[dq] ERROR: {count_invalid} rows with average_rating outside [0, 5].")
            passed = False

    if "num_pages" in df.columns:
        non_positive = (df["num_pages"] <= 0).sum()
        if non_positive > 0:
            print(f"[dq] ERROR: {non_positive} rows with non-positive num_pages.")
            passed = False

    return passed


def main(argv: List[str] | None = None) -> None:
    ok = check_clean_csv()
    if ok:
        print("[dq] Data quality checks PASSED.")
        sys.exit(0)
    else:
        print("[dq] Data quality checks FAILED.")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
