"""Helpers for loading raw Goodreads CSV files that contain malformed rows."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import pandas as pd

COLUMN_NAMES = [
    "bookID",
    "title",
    "authors",
    "average_rating",
    "isbn",
    "isbn13",
    "language_code",
    "  num_pages",
    "ratings_count",
    "text_reviews_count",
    "publication_date",
    "publisher",
]
EXPECTED_COLUMNS = len(COLUMN_NAMES)
AUTHORS_COLUMN_INDEX = COLUMN_NAMES.index("authors")


@dataclass
class RawLoadStats:
    total_rows: int
    repaired_rows: int


def _repair_row(fields: List[str]) -> Tuple[List[str], bool]:
    """Ensure the row has the expected length by merging split author fields."""

    if len(fields) == EXPECTED_COLUMNS:
        return fields, False
    if len(fields) < EXPECTED_COLUMNS:
        raise ValueError(
            f"Row has {len(fields)} column(s); expected {EXPECTED_COLUMNS}."
        )

    extras = len(fields) - EXPECTED_COLUMNS
    start = AUTHORS_COLUMN_INDEX
    end = start + extras + 1
    repaired_authors = ",".join(fields[start:end])
    repaired_row = fields[:start] + [repaired_authors] + fields[end:]

    if len(repaired_row) != EXPECTED_COLUMNS:
        raise ValueError(
            f"Unable to repair row with {len(fields)} columns (still {len(repaired_row)} after repair)."
        )

    return repaired_row, True


def load_books_csv(csv_path: str) -> Tuple[pd.DataFrame, RawLoadStats]:
    """Load the Kaggle books export while repairing embedded commas in authors."""

    input_path = Path(csv_path)
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")

    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        if header != COLUMN_NAMES:
            raise ValueError("Unexpected header format in books CSV.")
        writer.writerow(header)

        total = 0
        repaired = 0
        for row in reader:
            total += 1
            repaired_row, was_repaired = _repair_row(row)
            if was_repaired:
                repaired += 1
            writer.writerow(repaired_row)

    buffer.seek(0)
    df = pd.read_csv(buffer)
    return df, RawLoadStats(total_rows=total, repaired_rows=repaired)
